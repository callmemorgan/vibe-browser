#!/usr/bin/env python3
"""Small local plumbing for Vibe Browser benchmark smoke runs.

The script intentionally uses only the Python standard library so it can run in a
fresh checkout. It does not try to be a full agent harness; it provides the
repeatable pieces needed for a first local-model bench:

- create a run branch and benchmark-run.md manifest,
- render the participant prompt for a target milestone,
- call an OpenAI-compatible local chat endpoint and log transcript turns,
- serve public fixtures with simple HTTP status/header behavior,
- validate local docs links and expected harness inputs.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import http.server
import json
import os
from pathlib import Path
import re
import socketserver
import subprocess
import sys
import textwrap
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TASK_PATH = ROOT / "docs" / "participant-task.md"
PROMPT_SET_PATH = ROOT / "docs" / "prompt-sets" / "browser-build-v0.md"
RUNS_DIR = ROOT / ".vibe-bench" / "runs"
FIXTURES_DIR = ROOT / "fixtures"

PROFILE_DEFAULTS: dict[str, dict[str, str]] = {
    "smoke-v0": {
        "wall_clock_limit": "30m",
        "token_limit": "200000",
        "turn_limit": "8",
        "tool_call_limit": "unknown",
        "cost_limit": "unknown",
        "idle_limit": "2",
        "failure_limit": "2",
    },
    "sprint-v0": {
        "wall_clock_limit": "4h",
        "token_limit": "1500000",
        "turn_limit": "40",
        "tool_call_limit": "unknown",
        "cost_limit": "unknown",
        "idle_limit": "3",
        "failure_limit": "5",
    },
    "standard-v0": {
        "wall_clock_limit": "24h",
        "token_limit": "8000000",
        "turn_limit": "200",
        "tool_call_limit": "unknown",
        "cost_limit": "unknown",
        "idle_limit": "6",
        "failure_limit": "5",
    },
}

CONTINUATION_PROMPT = (
    "Continue pursuing the configured target milestone. Prefer implementation, "
    "tests, verification, or concrete blocker diagnosis over additional planning. "
    "Do not add scope beyond the target milestone unless required for verification."
)

SYSTEM_PROMPT = (
    "You are participating in the Vibe Browser benchmark. Your goal is to produce "
    "a runnable browser implementation, tests, and design notes according to the "
    "configured target milestone. Continue making concrete progress until the "
    "harness stop condition is reached."
)


def run_git(args: list[str], *, check: bool = True) -> str:
    proc = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if check and proc.returncode != 0:
        raise SystemExit(proc.stderr.strip() or f"git {' '.join(args)} failed")
    return proc.stdout.strip()


def slug(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value or "unknown"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def benchmark_input_digest() -> str:
    specs_zip = ROOT / "specs.zip"
    if specs_zip.exists():
        return f"sha256:specs.zip:{sha256_file(specs_zip)}"
    digest = hashlib.sha256()
    for path in sorted((ROOT / "specs").glob("*")):
        if path.is_file():
            digest.update(path.name.encode("utf-8"))
            digest.update(b"\0")
            digest.update(str(path.stat().st_size).encode("ascii"))
            digest.update(b"\0")
    return f"sha256:specs-directory-manifest:{digest.hexdigest()}"


def render_task(target: str) -> str:
    return TASK_PATH.read_text(encoding="utf-8").replace("{{TARGET_MILESTONE}}", target)


def prompt_checksum() -> str:
    digest = hashlib.sha256()
    for path in (TASK_PATH, PROMPT_SET_PATH):
        digest.update(path.relative_to(ROOT).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return f"sha256:{digest.hexdigest()}"


def manifest_text(args: argparse.Namespace, branch: str, run_id: str) -> str:
    profile = PROFILE_DEFAULTS.get(args.profile, PROFILE_DEFAULTS["smoke-v0"])
    now = dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat()
    base_commit = run_git(["rev-parse", "HEAD"])
    return f"""# Benchmark Run

## Identity

- Run ID: {run_id}
- Branch: {branch}
- Base benchmark commit: {base_commit}
- Benchmark input digest: {benchmark_input_digest()}
- Target: {args.target}

## Harness

- Harness: {args.harness}
- Harness version: 0.1.0
- Meta-harness profile: {args.profile}
- Tool: {args.tool}
- Tool version: unknown
- Model provider: {args.model_provider}
- Model: {args.model}
- Model snapshot: unknown
- Prompt set: browser-build-v0
- Prompt checksum: {prompt_checksum()}

## Budgets

- Wall-clock limit: {profile['wall_clock_limit']}
- Token limit: {profile['token_limit']}
- Turn limit: {profile['turn_limit']}
- Tool-call limit: {profile['tool_call_limit']}
- Cost limit: {profile['cost_limit']}
- Idle limit: {profile['idle_limit']}
- Failure limit: {profile['failure_limit']}

## Environment

- Operating system: {os.uname().sysname} {os.uname().release}
- Runtime dependencies: Python standard library; local model runner supplied separately
- Network access: local model endpoint and optional local fixture server
- Tool permissions: {args.tool_permissions}
- Human intervention policy: {args.human_intervention_policy}

## Verification

- Build command:
- Test command:
- Smoke-test command:
- Latest verification result: not-run

## Completion

- Stop reason:
- Observed elapsed time:
- Observed token usage: unknown
- Observed turns: 0
- Observed tool calls: unknown
- Final commit:
- Comparison eligible: unknown
- Notes: Created by `scripts/vibe_bench.py init-run` at {now}.
"""


def command_init_run(args: argparse.Namespace) -> None:
    timestamp = args.timestamp or dt.datetime.now(dt.UTC).strftime("%Y%m%d-%H%M")
    run_id = args.run_id or f"r{timestamp.replace('-', '')[-6:]}"
    branch = args.branch or "/".join(
        [
            "runs",
            slug(args.profile),
            slug(args.harness),
            slug(args.tool),
            slug(args.model),
            f"{timestamp}-{slug(args.target)}-{slug(run_id)}",
        ]
    )

    if args.create_branch:
        current_branch = run_git(["branch", "--show-current"], check=False)
        if current_branch != branch:
            run_git(["checkout", "-b", branch])

    manifest = ROOT / "benchmark-run.md"
    if manifest.exists() and not args.force:
        raise SystemExit("benchmark-run.md already exists; pass --force to replace it")
    manifest.write_text(manifest_text(args, branch, run_id), encoding="utf-8")

    run_dir = RUNS_DIR / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "initial-prompt.md").write_text(render_task(args.target), encoding="utf-8")
    metadata = {
        "run_id": run_id,
        "branch": branch,
        "target": args.target,
        "profile": args.profile,
        "model": args.model,
        "prompt_set": "browser-build-v0",
        "prompt_checksum": prompt_checksum(),
        "created_at": dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat(),
    }
    (run_dir / "metadata.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    print(f"Created benchmark-run.md and {run_dir.relative_to(ROOT)}/initial-prompt.md")
    print(f"Run branch: {branch}")


def command_render_prompt(args: argparse.Namespace) -> None:
    prompt = render_task(args.target)
    if args.include_system:
        prompt = f"# System Instruction\n\n{SYSTEM_PROMPT}\n\n---\n\n{prompt}"
    if args.output:
        Path(args.output).write_text(prompt, encoding="utf-8")
    else:
        print(prompt)


def post_chat_completion(
    endpoint: str, api_key: str | None, payload: dict[str, Any]
) -> dict[str, Any]:
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        endpoint.rstrip("/") + "/chat/completions",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    if api_key:
        request.add_header("Authorization", f"Bearer {api_key}")
    try:
        with urllib.request.urlopen(request, timeout=600) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"Model endpoint returned HTTP {exc.code}: {body}") from exc


def append_jsonl(path: Path, record: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, sort_keys=True) + "\n")


def command_run_openai(args: argparse.Namespace) -> None:
    run_id = args.run_id or dt.datetime.now(dt.UTC).strftime("manual-%Y%m%d-%H%M%S")
    run_dir = RUNS_DIR / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    transcript_path = run_dir / "transcript.jsonl"

    messages: list[dict[str, str]] = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": render_task(args.target)},
    ]
    endpoint = args.endpoint or os.environ.get("OPENAI_BASE_URL") or "http://localhost:11434/v1"
    api_key = args.api_key if args.api_key is not None else os.environ.get("OPENAI_API_KEY")

    for turn in range(1, args.turns + 1):
        payload: dict[str, Any] = {
            "model": args.model,
            "messages": messages,
            "temperature": args.temperature,
        }
        if args.max_tokens:
            payload["max_tokens"] = args.max_tokens
        started = time.time()
        response = post_chat_completion(endpoint, api_key, payload)
        elapsed = round(time.time() - started, 3)
        choice = response.get("choices", [{}])[0]
        message = choice.get("message", {})
        content = message.get("content", "")
        messages.append({"role": "assistant", "content": content})
        record = {
            "turn": turn,
            "elapsed_seconds": elapsed,
            "request": payload,
            "response": response,
        }
        append_jsonl(transcript_path, record)
        print(f"\n===== assistant turn {turn} ({elapsed}s) =====\n")
        print(content)
        if turn < args.turns:
            messages.append({"role": "user", "content": args.continuation_prompt})

    (run_dir / "latest-messages.json").write_text(
        json.dumps(messages, indent=2) + "\n", encoding="utf-8"
    )
    print(f"\nTranscript written to {transcript_path.relative_to(ROOT)}")
    print(
        "This runner records model output only; apply or review any proposed edits "
        "manually."
    )


class FixtureHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *handler_args: Any, directory: str | None = None, **kwargs: Any) -> None:
        super().__init__(*handler_args, directory=str(FIXTURES_DIR), **kwargs)

    def do_GET(self) -> None:  # noqa: N802 - stdlib handler API
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/m2-network/redirect.html":
            self.send_response(302)
            self.send_header("Location", "/m2-network/redirect-target.html")
            self.end_headers()
            return
        if parsed.path == "/m2-network/not-found.html":
            body = (FIXTURES_DIR / "m2-network" / "not-found.html").read_bytes()
            self.send_response(404)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        return super().do_GET()

    def guess_type(self, path: str) -> str:
        if path.endswith("/m2-network/content-type-html.txt"):
            return "text/html; charset=utf-8"
        return super().guess_type(path)


def command_serve_fixtures(args: argparse.Namespace) -> None:
    class ReusableTCPServer(socketserver.TCPServer):
        allow_reuse_address = True

    with ReusableTCPServer((args.host, args.port), FixtureHandler) as httpd:
        host, port = httpd.server_address
        print(
            f"Serving fixtures from {FIXTURES_DIR.relative_to(ROOT)} "
            f"at http://{host}:{port}/"
        )
        print("Redirect smoke URL: /m2-network/redirect.html")
        print("Stop with Ctrl-C.")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nFixture server stopped.")


def markdown_links() -> list[tuple[Path, str]]:
    missing: list[tuple[Path, str]] = []
    markdown_files = [
        ROOT / "README.md",
        *ROOT.joinpath("docs").glob("**/*.md"),
        ROOT / "fixtures" / "README.md",
    ]
    for path in markdown_files:
        text = path.read_text(encoding="utf-8")
        for match in re.finditer(r"\[[^\]]+\]\(([^)]+)\)", text):
            target = match.group(1).split("#", 1)[0]
            if not target or "://" in target or target.startswith("mailto:"):
                continue
            candidate = (path.parent / target).resolve()
            if not candidate.exists():
                missing.append((path.relative_to(ROOT), target))
    return missing


def command_validate(args: argparse.Namespace) -> None:
    expected = [
        TASK_PATH,
        PROMPT_SET_PATH,
        ROOT / "docs" / "evaluator-procedure.md",
        FIXTURES_DIR / "README.md",
        FIXTURES_DIR / "m2-network" / "hello.html",
        FIXTURES_DIR / "m2-network" / "redirect-target.html",
        FIXTURES_DIR / "m3-html-dom" / "title.html",
        FIXTURES_DIR / "m4-style-layout" / "block-layout.html",
        FIXTURES_DIR / "m5-paint" / "colors-and-borders.html",
    ]
    missing_files = [
        path.relative_to(ROOT).as_posix() for path in expected if not path.exists()
    ]
    missing_links = markdown_links()
    if missing_files or missing_links:
        if missing_files:
            print("Missing expected files:", file=sys.stderr)
            for path in missing_files:
                print(f"- {path}", file=sys.stderr)
        if missing_links:
            print("Missing local Markdown links:", file=sys.stderr)
            for path, target in missing_links:
                print(f"- {path}: {target}", file=sys.stderr)
        raise SystemExit(1)
    print("Harness inputs and local Markdown links look OK")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Local plumbing for Vibe Browser benchmark smoke runs.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(
            """
            Examples:
              scripts/vibe_bench.py init-run --target m1 --model llama3.2 --create-branch
              scripts/vibe_bench.py render-prompt --target m1 --include-system
              scripts/vibe_bench.py run-openai --target m1 --model llama3.2 --turns 1
              scripts/vibe_bench.py serve-fixtures --port 8765
              scripts/vibe_bench.py validate
            """
        ),
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_run = subparsers.add_parser(
        "init-run", help="create run branch metadata and prompt files"
    )
    init_run.add_argument("--target", default="m1")
    init_run.add_argument("--profile", default="smoke-v0", choices=sorted(PROFILE_DEFAULTS))
    init_run.add_argument("--harness", default="manual-v0")
    init_run.add_argument("--tool", default="local-cli")
    init_run.add_argument("--model", required=True)
    init_run.add_argument("--model-provider", default="local")
    init_run.add_argument("--human-intervention-policy", default="administrative-only")
    init_run.add_argument("--tool-permissions", default="local shell and filesystem")
    init_run.add_argument("--run-id")
    init_run.add_argument("--timestamp")
    init_run.add_argument("--branch")
    init_run.add_argument("--create-branch", action="store_true")
    init_run.add_argument("--force", action="store_true")
    init_run.set_defaults(func=command_init_run)

    render_prompt = subparsers.add_parser(
        "render-prompt", help="render participant task for a target"
    )
    render_prompt.add_argument("--target", default="m1")
    render_prompt.add_argument("--include-system", action="store_true")
    render_prompt.add_argument("--output")
    render_prompt.set_defaults(func=command_render_prompt)

    run_openai = subparsers.add_parser(
        "run-openai", help="call a local OpenAI-compatible chat endpoint"
    )
    run_openai.add_argument("--target", default="m1")
    run_openai.add_argument("--model", required=True)
    run_openai.add_argument(
        "--endpoint", help="base URL, e.g. http://localhost:11434/v1"
    )
    run_openai.add_argument(
        "--api-key", help="API key; defaults to OPENAI_API_KEY when set"
    )
    run_openai.add_argument("--turns", type=int, default=1)
    run_openai.add_argument("--temperature", type=float, default=0.2)
    run_openai.add_argument("--max-tokens", type=int)
    run_openai.add_argument("--run-id")
    run_openai.add_argument("--continuation-prompt", default=CONTINUATION_PROMPT)
    run_openai.set_defaults(func=command_run_openai)

    serve_fixtures = subparsers.add_parser(
        "serve-fixtures", help="serve public fixtures over HTTP"
    )
    serve_fixtures.add_argument("--host", default="127.0.0.1")
    serve_fixtures.add_argument("--port", type=int, default=8765)
    serve_fixtures.set_defaults(func=command_serve_fixtures)

    validate = subparsers.add_parser(
        "validate", help="validate local bench docs and links"
    )
    validate.set_defaults(func=command_validate)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
