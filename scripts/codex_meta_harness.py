#!/usr/bin/env python3
"""Agent CLI meta-harness for long Vibe Browser benchmark runs.

The harness is intentionally standard-library-only. It owns benchmark run
metadata, prompt files, agent invocation, verification logs, checkpoints, and
stop-condition accounting. It does not score the submitted browser.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import re
import shlex
import subprocess
import sys
import tempfile
import threading
import textwrap
import time
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TASK_PATH = Path("docs/participant-task.md")
PROMPT_SET_PATH = Path("docs/prompt-sets/browser-build-v0.md")
RUNS_DIR = Path(".vibe-bench/runs")
HARNESS_NAME = "codex-meta-harness"
HARNESS_VERSION = "0.1.0"
PROMPT_SET = "browser-build-v0"
PI_DEFAULT_TOOLS = "read,write,edit,bash,grep,find,ls"

PROFILE_DEFAULTS: dict[str, dict[str, str]] = {
    "smoke-v0": {
        "wall_clock_limit": "30m",
        "token_limit": "200000",
        "turn_limit": "8",
        "tool_call_limit": "unknown",
        "cost_limit": "unknown",
        "idle_limit": "2",
        "failure_limit": "2",
        "checkpoint_interval": "10m",
    },
    "sprint-v0": {
        "wall_clock_limit": "4h",
        "token_limit": "1500000",
        "turn_limit": "40",
        "tool_call_limit": "unknown",
        "cost_limit": "unknown",
        "idle_limit": "3",
        "failure_limit": "5",
        "checkpoint_interval": "30m",
    },
    "standard-v0": {
        "wall_clock_limit": "24h",
        "token_limit": "8000000",
        "turn_limit": "200",
        "tool_call_limit": "unknown",
        "cost_limit": "unknown",
        "idle_limit": "6",
        "failure_limit": "5",
        "checkpoint_interval": "30m",
    },
}

CONTINUATION_PROMPT = (
    "Continue pursuing the configured target milestone. Prefer implementation, "
    "tests, verification, or concrete blocker diagnosis over additional planning. "
    "Do not add scope beyond the target milestone unless required for verification."
)

VERIFICATION_PROMPT = (
    "Run the submitted build, test, and smoke-test commands if available. Fix "
    "failures that block the configured target milestone, and update "
    "benchmark-run.md with the latest verification result."
)

PREMATURE_STOP_PROMPT = (
    "The task is not complete unless the target milestone acceptance criteria "
    "are met or a concrete blocker is recorded. Continue with the next "
    "implementation or verification step."
)

BLOCKED_PROMPT = (
    "Record the blocker, evidence, attempted fixes, and the smallest useful "
    "fallback milestone. Continue with that fallback if possible."
)


def utc_now() -> str:
    return dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat()


def repo_path(root: Path, relative: Path | str) -> Path:
    return root / relative


def slug(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value or "unknown"


def parse_duration_seconds(value: str) -> int | None:
    if value == "unknown":
        return None
    match = re.fullmatch(r"(\d+)([smhd]?)", value.strip())
    if not match:
        raise ValueError(f"unsupported duration: {value}")
    amount = int(match.group(1))
    unit = match.group(2) or "s"
    multipliers = {"s": 1, "m": 60, "h": 3600, "d": 86400}
    return amount * multipliers[unit]


def parse_int_limit(value: str) -> int | None:
    return None if value == "unknown" else int(value)


def atomic_write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", dir=path.parent, delete=False
    ) as handle:
        json.dump(data, handle, indent=2, sort_keys=True)
        handle.write("\n")
        temp_name = handle.name
    Path(temp_name).replace(path)


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def run_command(
    args: list[str],
    *,
    cwd: Path,
    input_text: str | None = None,
    timeout: int | None = None,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            args,
            cwd=cwd,
            input=input_text,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
            check=False,
            env=env,
        )
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout or ""
        stderr = exc.stderr or ""
        if isinstance(stdout, bytes):
            stdout = stdout.decode("utf-8", errors="replace")
        if isinstance(stderr, bytes):
            stderr = stderr.decode("utf-8", errors="replace")
        stderr = f"{stderr}\nTIMEOUT after {timeout}s\n"
        return subprocess.CompletedProcess(args, 124, stdout, stderr)
    except OSError as exc:
        stderr = f"{exc.__class__.__name__}: {exc}\n"
        return subprocess.CompletedProcess(args, 127, "", stderr)


def compact_text(value: Any, limit: int = 180) -> str:
    if isinstance(value, str):
        text = value
    else:
        text = json.dumps(value, sort_keys=True)
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) > limit:
        return f"{text[: limit - 1]}…"
    return text


def message_content_at(event: dict[str, Any], index: int | None) -> dict[str, Any] | None:
    if index is None:
        return None
    message = event.get("message")
    if not isinstance(message, dict):
        return None
    content = message.get("content")
    if not isinstance(content, list) or index >= len(content):
        return None
    item = content[index]
    return item if isinstance(item, dict) else None


def summarize_agent_event_line(
    config: dict[str, Any],
    turn_number: int,
    line: str,
) -> str | None:
    try:
        event = json.loads(line)
    except json.JSONDecodeError:
        text = compact_text(line)
        return f"turn {turn_number}: {text}" if text else None
    if not isinstance(event, dict):
        return None

    prefix = f"[{config['run_id']} turn {turn_number}]"
    event_type = event.get("type")
    if event_type in {"agent_start", "turn_start"}:
        return f"{prefix} {str(event_type).replace('_', ' ')}"
    if event_type == "session":
        return f"{prefix} session {event.get('id', config['run_id'])}"

    message = event.get("message")
    if isinstance(message, dict):
        role = message.get("role")
        if role == "assistant" and event_type == "message_start":
            model = message.get("model") or message.get("responseModel")
            return f"{prefix} assistant started" + (f" ({model})" if model else "")
        if role == "assistant" and event_type == "message_end":
            usage = message.get("usage")
            tokens = None
            if isinstance(usage, dict):
                tokens = usage.get("totalTokens") or usage.get("total_tokens")
            stop_reason = message.get("stopReason")
            details = []
            if stop_reason:
                details.append(f"stop={stop_reason}")
            if tokens:
                details.append(f"tokens={tokens}")
            suffix = f" ({', '.join(details)})" if details else ""
            return f"{prefix} assistant finished{suffix}"
        if role == "toolResult" and event_type in {"message_start", "message_end"}:
            tool = message.get("toolName") or "tool"
            is_error = " error" if message.get("isError") else ""
            return f"{prefix} {tool} result{is_error}"

    assistant_event = event.get("assistantMessageEvent")
    if isinstance(assistant_event, dict):
        assistant_type = assistant_event.get("type")
        if assistant_type in {"thinking_start", "thinking_delta", "thinking_end"}:
            return None
        if assistant_type == "toolcall_start":
            item = message_content_at(event, assistant_event.get("contentIndex"))
            if item:
                name = item.get("name", "tool")
                args = item.get("arguments") or item.get("partialArgs") or {}
                return f"{prefix} tool {name} {compact_text(args)}"
        if assistant_type == "text_start":
            return f"{prefix} assistant writing"
    return None


def run_command_streaming(
    args: list[str],
    *,
    cwd: Path,
    stdout_path: Path,
    stderr_path: Path,
    input_text: str | None = None,
    timeout: int | None = None,
    env: dict[str, str] | None = None,
    stdout_callback: Any | None = None,
    stderr_callback: Any | None = None,
) -> subprocess.CompletedProcess[str]:
    stdout_chunks: list[str] = []
    stderr_chunks: list[str] = []
    try:
        proc = subprocess.Popen(
            args,
            cwd=cwd,
            stdin=subprocess.PIPE if input_text is not None else subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            env=env,
        )
    except OSError as exc:
        stderr = f"{exc.__class__.__name__}: {exc}\n"
        stdout_path.write_text("", encoding="utf-8")
        stderr_path.write_text(stderr, encoding="utf-8")
        return subprocess.CompletedProcess(args, 127, "", stderr)

    def read_stream(
        stream: Any,
        path: Path,
        chunks: list[str],
        callback: Any | None,
    ) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as handle:
            for chunk in iter(stream.readline, ""):
                chunks.append(chunk)
                handle.write(chunk)
                handle.flush()
                if callback:
                    callback(chunk)
        stream.close()

    stdout_thread = threading.Thread(
        target=read_stream,
        args=(proc.stdout, stdout_path, stdout_chunks, stdout_callback),
        daemon=True,
    )
    stderr_thread = threading.Thread(
        target=read_stream,
        args=(proc.stderr, stderr_path, stderr_chunks, stderr_callback),
        daemon=True,
    )
    stdout_thread.start()
    stderr_thread.start()

    if proc.stdin is not None:
        try:
            proc.stdin.write(input_text or "")
            proc.stdin.close()
        except BrokenPipeError:
            pass

    try:
        return_code = proc.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        proc.kill()
        return_code = 124
        timeout_text = f"\nTIMEOUT after {timeout}s\n"
        stderr_chunks.append(timeout_text)
        with stderr_path.open("a", encoding="utf-8") as handle:
            handle.write(timeout_text)

    stdout_thread.join(timeout=5)
    stderr_thread.join(timeout=5)
    return subprocess.CompletedProcess(
        args,
        return_code,
        "".join(stdout_chunks),
        "".join(stderr_chunks),
    )


def run_git(root: Path, args: list[str], *, check: bool = True) -> str:
    proc = run_command(["git", *args], cwd=root)
    if check and proc.returncode != 0:
        raise SystemExit(proc.stderr.strip() or f"git {' '.join(args)} failed")
    return proc.stdout.strip()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def benchmark_input_digest(root: Path) -> str:
    specs_zip = repo_path(root, "specs.zip")
    if specs_zip.exists():
        return f"sha256:specs.zip:{sha256_file(specs_zip)}"
    digest = hashlib.sha256()
    specs_dir = repo_path(root, "specs")
    if specs_dir.exists():
        for path in sorted(specs_dir.glob("*")):
            if path.is_file():
                digest.update(path.name.encode("utf-8"))
                digest.update(b"\0")
                digest.update(str(path.stat().st_size).encode("ascii"))
                digest.update(b"\0")
    return f"sha256:specs-directory-manifest:{digest.hexdigest()}"


def prompt_checksum(root: Path) -> str:
    digest = hashlib.sha256()
    for relative in (TASK_PATH, PROMPT_SET_PATH):
        path = repo_path(root, relative)
        digest.update(relative.as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return f"sha256:{digest.hexdigest()}"


def render_task(root: Path, target: str) -> str:
    return repo_path(root, TASK_PATH).read_text(encoding="utf-8").replace(
        "{{TARGET_MILESTONE}}", target
    )


def profile_defaults(profile: str) -> dict[str, str]:
    if profile not in PROFILE_DEFAULTS:
        raise SystemExit(f"unknown profile: {profile}")
    return dict(PROFILE_DEFAULTS[profile])


def detect_codex_version(codex_command: str, root: Path) -> str:
    argv = shlex.split(codex_command)
    if argv == ["codex"]:
        proc = run_command(["codex", "--version"], cwd=root)
        if proc.returncode == 0:
            return proc.stdout.strip() or "unknown"
    return "unknown"


def detect_pi_version(pi_command: str, root: Path) -> str:
    argv = [*shlex.split(pi_command), "--version"]
    proc = run_command(argv, cwd=root)
    if proc.returncode == 0:
        return proc.stdout.strip() or "unknown"
    return "unknown"


def validate_codex_command_policy(args: argparse.Namespace) -> None:
    if args.agent_kind != "codex":
        return
    argv = shlex.split(args.codex_command)
    dangerous = "--dangerously-bypass-approvals-and-sandbox"
    if dangerous in argv and not args.allow_dangerous_codex_bypass:
        raise SystemExit(
            f"{dangerous} requires --allow-dangerous-codex-bypass and a documented "
            "disposable sandbox condition"
        )


def manifest_text(config: dict[str, Any]) -> str:
    budgets = config["budgets"]
    environment = config["environment"]
    launch_line = (
        f"- Codex launch command: {config['codex_command']}"
        if config["agent_kind"] == "codex"
        else f"- PI command: {config['pi_command']}"
    )
    return f"""# Benchmark Run

## Identity

- Run ID: {config['run_id']}
- Branch: {config['branch']}
- Base benchmark commit: {config['base_benchmark_commit']}
- Benchmark input digest: {config['benchmark_input_digest']}
- Target: {config['target']}

## Harness

- Harness: {config['harness']}
- Harness version: {config['harness_version']}
- Meta-harness profile: {config['profile']}
- Tool: {config['tool_name']}
- Tool version: {config['tool_version']}
- Agent kind: {config['agent_kind']}
- Provider interface: {config['provider_interface']}
- Model provider: {config['model_provider']}
- Model: {config['model']}
- Model snapshot: {config['model_snapshot']}
- Prompt set: {config['prompt_set']}
- Prompt checksum: {config['prompt_checksum']}

## Budgets

- Wall-clock limit: {budgets['wall_clock_limit']}
- Token limit: {budgets['token_limit']}
- Turn limit: {budgets['turn_limit']}
- Tool-call limit: {budgets['tool_call_limit']}
- Cost limit: {budgets['cost_limit']}
- Idle limit: {budgets['idle_limit']}
- Failure limit: {budgets['failure_limit']}
- Checkpoint interval: {budgets['checkpoint_interval']}

## Environment

- Operating system: {environment['operating_system']}
- Runtime dependencies: Python standard library; Codex CLI supplied separately
- Network access: {environment['network_policy']}
- Tool permissions: {config['tool_permissions']}
- Human intervention policy: {config['human_intervention_policy']}
{launch_line}

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
- Notes: Created by `scripts/codex_meta_harness.py init` at {config['created_at']}.
"""


def run_dir(root: Path, run_id: str) -> Path:
    return repo_path(root, RUNS_DIR / run_id)


def config_path(root: Path, run_id: str) -> Path:
    return run_dir(root, run_id) / "config.json"


def state_path(root: Path, run_id: str) -> Path:
    return run_dir(root, run_id) / "state.json"


def load_config(root: Path, run_id: str) -> dict[str, Any]:
    path = config_path(root, run_id)
    if not path.exists():
        raise SystemExit(f"no config for run {run_id}: {path}")
    return read_json(path)


def load_state(root: Path, run_id: str) -> dict[str, Any]:
    path = state_path(root, run_id)
    if not path.exists():
        raise SystemExit(f"no state for run {run_id}: {path}")
    return read_json(path)


def save_state(root: Path, run_id: str, state: dict[str, Any]) -> None:
    state["updated_at"] = utc_now()
    atomic_write_json(state_path(root, run_id), state)


def initial_state(config: dict[str, Any]) -> dict[str, Any]:
    now = time.time()
    return {
        "state": "created",
        "run_id": config["run_id"],
        "created_at": config["created_at"],
        "started_at_epoch": now,
        "updated_at": config["created_at"],
        "observed_turns": 0,
        "observed_token_usage": "unknown",
        "observed_tool_calls": "unknown",
        "observed_cost": "unknown",
        "idle_count": 0,
        "failure_count": 0,
        "session_id": None,
        "latest_prompt": None,
        "latest_agent_log": None,
        "latest_codex_log": None,
        "latest_last_message": None,
        "latest_verification": "not-run",
        "latest_verification_log": None,
        "latest_checkpoint": None,
        "latest_material_progress": False,
        "stop_reason": None,
        "comparison_eligible": "unknown",
    }


def build_branch(config: dict[str, Any], timestamp: str) -> str:
    tool_slug = "codex-cli" if config["agent_kind"] == "codex" else "pi"
    return "/".join(
        [
            "runs",
            slug(config["profile"]),
            slug(config["harness"]),
            tool_slug,
            slug(config["model"]),
            f"{timestamp}-{slug(config['target'])}-{slug(config['run_id'])}",
        ]
    )


def command_init(args: argparse.Namespace) -> None:
    root = args.repo_root.resolve()
    validate_codex_command_policy(args)
    timestamp = args.timestamp or dt.datetime.now(dt.UTC).strftime("%Y%m%d-%H%M")
    run_id = args.run_id or f"r{timestamp.replace('-', '')[-6:]}"
    budgets = profile_defaults(args.profile)
    if args.turn_limit:
        budgets["turn_limit"] = str(args.turn_limit)
    if args.wall_clock_limit:
        budgets["wall_clock_limit"] = args.wall_clock_limit
    if args.idle_limit:
        budgets["idle_limit"] = str(args.idle_limit)
    if args.failure_limit:
        budgets["failure_limit"] = str(args.failure_limit)
    if args.checkpoint_interval:
        budgets["checkpoint_interval"] = args.checkpoint_interval

    base_commit = run_git(root, ["rev-parse", "HEAD"], check=False) or "unknown"
    model_provider = args.model_provider or (
        "ollama" if args.agent_kind == "pi" else "openai"
    )
    tool_name = "pi" if args.agent_kind == "pi" else "codex-cli"
    tool_version = (
        detect_pi_version(args.pi_command, root)
        if args.agent_kind == "pi"
        else detect_codex_version(args.codex_command, root)
    )
    tool_permissions = (
        f"pi-tools={args.pi_tools}"
        if args.agent_kind == "pi"
        else f"sandbox={args.sandbox}"
    )
    config: dict[str, Any] = {
        "run_id": run_id,
        "agent_kind": args.agent_kind,
        "profile": args.profile,
        "target": args.target,
        "harness": HARNESS_NAME,
        "harness_version": HARNESS_VERSION,
        "tool_name": tool_name,
        "tool_version": tool_version,
        "provider_interface": "pi-cli-v0"
        if args.agent_kind == "pi"
        else "codex-exec-v0",
        "model_provider": model_provider,
        "model": args.model,
        "model_snapshot": args.model_snapshot,
        "prompt_set": PROMPT_SET,
        "prompt_checksum": prompt_checksum(root),
        "base_benchmark_commit": args.base_benchmark_commit or base_commit,
        "benchmark_input_digest": args.benchmark_input_digest
        or benchmark_input_digest(root),
        "codex_command": args.codex_command,
        "codex_command_mode": args.codex_command_mode,
        "codex_cli_version": detect_codex_version(args.codex_command, root)
        if args.agent_kind == "codex"
        else "not-used",
        "codex_model_arg": args.codex_model_arg,
        "allow_dangerous_codex_bypass": args.allow_dangerous_codex_bypass,
        "pi_command": args.pi_command,
        "pi_tools": args.pi_tools,
        "pi_mode": args.pi_mode,
        "container_execution": args.container_execution,
        "checkpoint_commits": args.checkpoint_commits,
        "sandbox_mode": args.sandbox,
        "tool_permissions": tool_permissions,
        "human_intervention_policy": args.human_intervention_policy,
        "budgets": budgets,
        "environment": {
            "operating_system": f"{os.uname().sysname} {os.uname().release}",
            "network_policy": args.network_policy,
        },
        "created_at": utc_now(),
    }
    config["branch"] = args.branch or build_branch(config, timestamp)

    if args.create_branch:
        current_branch = run_git(root, ["branch", "--show-current"], check=False)
        if current_branch != config["branch"]:
            run_git(root, ["checkout", "-b", config["branch"]])

    manifest = repo_path(root, "benchmark-run.md")
    if manifest.exists() and not args.force:
        raise SystemExit("benchmark-run.md already exists; pass --force to replace it")

    this_run_dir = run_dir(root, run_id)
    for child in ("prompts", "codex", "pi", "verification", "checkpoints"):
        (this_run_dir / child).mkdir(parents=True, exist_ok=True)
    (this_run_dir / "initial-prompt.md").write_text(
        initial_prompt_text(root, config), encoding="utf-8"
    )
    atomic_write_json(config_path(root, run_id), config)
    save_state(root, run_id, initial_state(config))
    manifest.write_text(manifest_text(config), encoding="utf-8")

    print(f"Initialized {config['agent_kind']} benchmark run {run_id}")
    print(f"Run branch: {config['branch']}")
    print(f"Run directory: {(this_run_dir).relative_to(root)}")


def command_contains_model_arg(prefix: list[str]) -> bool:
    return "--model" in prefix or "-m" in prefix


def should_append_codex_model(config: dict[str, Any], prefix: list[str]) -> bool:
    mode = config.get("codex_model_arg", "auto")
    if mode == "always":
        return True
    if mode == "never":
        return False
    return not command_contains_model_arg(prefix)


def build_codex_argv(
    config: dict[str, Any],
    root: Path,
    *,
    turn_number: int,
    output_last_message: Path,
    session_id: str | None,
) -> list[str]:
    prefix = shlex.split(config["codex_command"])
    if not prefix:
        raise SystemExit("codex command cannot be empty")

    if session_id:
        suffix = ["exec", "resume", "--json"]
    else:
        suffix = [
            "exec",
            "--json",
            "--cd",
            str(root),
        ]

    if should_append_codex_model(config, prefix):
        suffix.extend(["--model", config["model"]])

    if not session_id:
        suffix.extend(["--sandbox", config["sandbox_mode"]])

    suffix.extend(["--output-last-message", str(output_last_message)])
    if session_id:
        suffix.extend([session_id, "-"])
    else:
        suffix.append("-")

    argv = [*prefix, *suffix]
    if config.get("codex_command_mode", "argv") == "interactive-shell":
        return ["zsh", "-ic", shlex.join(argv)]
    return argv


def build_pi_argv(
    config: dict[str, Any],
    root: Path,
    *,
    prompt: str,
    session_dir: Path,
) -> list[str]:
    argv = [
        *shlex.split(config.get("pi_command", "pi")),
        "--provider",
        config["model_provider"],
        "--model",
        config["model"],
        "--mode",
        config.get("pi_mode", "json"),
        "--print",
        "--session-id",
        config["run_id"],
        "--session-dir",
        str(session_dir),
        "--tools",
        config.get("pi_tools", PI_DEFAULT_TOOLS),
        prompt,
    ]
    return argv


def resolve_run_local_path(root: Path, value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else root / path


def pi_agent_dir(root: Path, config: dict[str, Any]) -> Path:
    configured = os.environ.get("PI_CODING_AGENT_DIR")
    if configured:
        return resolve_run_local_path(root, configured)
    return run_dir(root, config["run_id"]) / "pi" / "agent"


def pi_environment(
    root: Path,
    config: dict[str, Any],
    *,
    session_dir: Path,
) -> dict[str, str]:
    env = os.environ.copy()
    env["PI_CODING_AGENT_DIR"] = str(pi_agent_dir(root, config))
    env["PI_CODING_AGENT_SESSION_DIR"] = str(session_dir)
    env.setdefault("PI_SKIP_VERSION_CHECK", "1")
    return env


def normalize_ollama_base_url(value: str) -> str:
    value = value.strip() or "http://localhost:11434"
    if not re.match(r"https?://", value):
        value = f"http://{value}"
    value = value.rstrip("/")
    return value if value.endswith("/v1") else f"{value}/v1"


def default_ollama_host(config: dict[str, Any]) -> str:
    if config.get("container_execution") == "docker-admin-v0":
        return "http://host.docker.internal:11434"
    return "http://localhost:11434"


def prepare_pi_provider_config(
    root: Path,
    config: dict[str, Any],
    env: dict[str, str],
) -> None:
    if config["model_provider"] != "ollama":
        return
    agent_dir = resolve_run_local_path(root, env["PI_CODING_AGENT_DIR"])
    agent_dir.mkdir(parents=True, exist_ok=True)
    models_path = agent_dir / "models.json"
    data: dict[str, Any] = {"providers": {}}
    if models_path.exists():
        data = read_json(models_path)
        data.setdefault("providers", {})

    base_url = normalize_ollama_base_url(
        env.get("OLLAMA_BASE_URL")
        or env.get("OLLAMA_HOST")
        or default_ollama_host(config)
    )
    data["providers"]["ollama"] = {
        "baseUrl": base_url,
        "api": "openai-completions",
        "apiKey": "$OLLAMA_API_KEY" if env.get("OLLAMA_API_KEY") else "ollama",
        "compat": {
            "supportsDeveloperRole": False,
            "supportsReasoningEffort": False,
        },
        "models": [{"id": config["model"]}],
    }
    atomic_write_json(models_path, data)


def agent_log_dir(root: Path, config: dict[str, Any]) -> Path:
    return run_dir(root, config["run_id"]) / (
        "pi" if config.get("agent_kind") == "pi" else "codex"
    )


def initial_prompt_text(root: Path, config: dict[str, Any]) -> str:
    context = f"""# Harness Context

- Run ID: {config['run_id']}
- Agent kind: {config['agent_kind']}
- Target milestone: {config['target']}
- Meta-harness profile: {config['profile']}
- Wall-clock limit: {config['budgets']['wall_clock_limit']}
- Turn limit: {config['budgets']['turn_limit']}
- Token limit: {config['budgets']['token_limit']}
- Human intervention policy: {config['human_intervention_policy']}
- Base benchmark commit: {config['base_benchmark_commit']}
- Benchmark input digest: {config['benchmark_input_digest']}

Do not edit files under `specs/`. Keep generated implementation artifacts
separate from benchmark-authored docs unless you are updating run metadata or
design notes.
"""
    return f"{context}\n---\n\n{render_task(root, config['target'])}"


def continuation_prompt_text(state: dict[str, Any]) -> str:
    lines = [
        CONTINUATION_PROMPT,
        "",
        "# Mechanical State",
        f"- Observed turns: {state['observed_turns']}",
        f"- Latest verification result: {state.get('latest_verification', 'not-run')}",
        f"- Idle count: {state.get('idle_count', 0)}",
        f"- Failure count: {state.get('failure_count', 0)}",
    ]
    if state.get("stop_reason"):
        lines.append(f"- Stop reason already recorded: {state['stop_reason']}")
    return "\n".join(lines) + "\n"


def prompt_for_turn(
    root: Path, config: dict[str, Any], state: dict[str, Any], prompt_kind: str
) -> str:
    if state["observed_turns"] == 0:
        return initial_prompt_text(root, config)
    if prompt_kind == "verify":
        return VERIFICATION_PROMPT + "\n"
    if prompt_kind == "premature-stop":
        return PREMATURE_STOP_PROMPT + "\n"
    if prompt_kind == "blocked":
        return BLOCKED_PROMPT + "\n"
    return continuation_prompt_text(state)


def changed_paths(status_text: str) -> list[str]:
    paths: list[str] = []
    for line in status_text.splitlines():
        if not line:
            continue
        path = line[3:] if len(line) > 3 else line
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        paths.append(path)
    return paths


def material_paths(paths: list[str]) -> list[str]:
    return [
        path
        for path in paths
        if not path.startswith(".vibe-bench/")
        and path != ".vibe-bench"
        and "__pycache__" not in path
    ]


def specs_changed(paths: list[str]) -> bool:
    return any(path == "specs" or path.startswith("specs/") for path in paths)


def recursive_find(data: Any, keys: set[str]) -> Any:
    if isinstance(data, dict):
        for key, value in data.items():
            if key in keys:
                return value
            found = recursive_find(value, keys)
            if found is not None:
                return found
    elif isinstance(data, list):
        for item in data:
            found = recursive_find(item, keys)
            if found is not None:
                return found
    return None


def parse_codex_events(jsonl_path: Path) -> dict[str, Any]:
    session_id = None
    total_tokens = None
    tool_calls = None
    for line in jsonl_path.read_text(encoding="utf-8", errors="replace").splitlines():
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if session_id is None:
            session_id = recursive_find(
                event, {"session_id", "sessionId", "conversation_id", "thread_id"}
            )
        usage = recursive_find(event, {"usage"})
        if isinstance(usage, dict):
            maybe_total = usage.get("total_tokens")
            if isinstance(maybe_total, int):
                total_tokens = maybe_total
        maybe_total = recursive_find(event, {"total_tokens"})
        if isinstance(maybe_total, int):
            total_tokens = maybe_total
        maybe_tool_calls = recursive_find(event, {"tool_calls", "tool_call_count"})
        if isinstance(maybe_tool_calls, int):
            tool_calls = maybe_tool_calls
    return {
        "session_id": session_id,
        "total_tokens": total_tokens,
        "tool_calls": tool_calls,
    }


def parse_pi_events(log_path: Path) -> dict[str, Any]:
    session_id = None
    total_tokens = None
    tool_calls = None
    for line in log_path.read_text(encoding="utf-8", errors="replace").splitlines():
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if session_id is None:
            session_id = recursive_find(event, {"session_id", "sessionId", "session"})
        for key in ("total_tokens", "totalTokens", "tokens", "contextTokens"):
            value = recursive_find(event, {key})
            if isinstance(value, int):
                total_tokens = value
                break
        maybe_tool_calls = recursive_find(event, {"tool_calls", "toolCalls", "tool_call_count"})
        if isinstance(maybe_tool_calls, int):
            tool_calls = maybe_tool_calls
    return {
        "session_id": session_id,
        "total_tokens": total_tokens,
        "tool_calls": tool_calls,
    }


def parse_agent_events(config: dict[str, Any], log_path: Path) -> dict[str, Any]:
    if config.get("agent_kind") == "pi":
        return parse_pi_events(log_path)
    return parse_codex_events(log_path)


def manifest_commands(root: Path) -> list[tuple[str, str]]:
    manifest = repo_path(root, "benchmark-run.md")
    if not manifest.exists():
        return []
    commands: list[tuple[str, str]] = []
    labels = {
        "- Build command:": "build",
        "- Test command:": "test",
        "- Smoke-test command:": "smoke",
    }
    for line in manifest.read_text(encoding="utf-8").splitlines():
        for prefix, label in labels.items():
            if line.startswith(prefix):
                command = extract_manifest_command(line.removeprefix(prefix).strip())
                if command:
                    commands.append((label, command))
    return commands


def extract_manifest_command(value: str) -> str:
    inline = re.findall(r"`([^`\n]+)`", value)
    if inline:
        return inline[0].strip()
    return value.strip()


def is_noop_manifest_command(command: str) -> bool:
    normalized = command.strip().lower()
    normalized = normalized.strip("()[] ")
    return (
        not normalized
        or normalized in {"none", "n/a", "na", "not applicable", "no build step"}
        or normalized.startswith("none ")
        or normalized.startswith("no build")
        or normalized.startswith("not required")
    )


def split_command_env(command: str) -> tuple[list[str], dict[str, str]]:
    argv = shlex.split(command)
    extra_env: dict[str, str] = {}
    while argv and re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*=.*", argv[0]):
        name, value = argv.pop(0).split("=", 1)
        extra_env[name] = value
    return argv, extra_env


def run_verification(
    root: Path,
    run_id: str,
    turn_number: int,
    *,
    timeout: int | None = None,
) -> tuple[str, Path]:
    log_path = run_dir(root, run_id) / "verification" / f"turn-{turn_number:04d}.txt"
    chunks: list[str] = []
    overall_return = 0

    validate_script = repo_path(root, "scripts/vibe_bench.py")
    if validate_script.exists():
        proc = run_command(
            [sys.executable, str(validate_script), "validate"],
            cwd=root,
            timeout=timeout,
        )
        chunks.append("$ python3 scripts/vibe_bench.py validate\n")
        chunks.append(proc.stdout)
        chunks.append(proc.stderr)
        chunks.append(f"\nexit={proc.returncode}\n")
        overall_return = max(overall_return, proc.returncode)

    for label, command in manifest_commands(root):
        if is_noop_manifest_command(command):
            chunks.append(f"\n$ {command}\n")
            chunks.append(f"skipped ({label})\n")
            continue
        argv, extra_env = split_command_env(command)
        if not argv:
            continue
        command_env = None
        if extra_env:
            command_env = os.environ.copy()
            command_env.update(extra_env)
        proc = run_command(argv, cwd=root, timeout=timeout, env=command_env)
        chunks.append(f"\n$ {command}\n")
        chunks.append(proc.stdout)
        chunks.append(proc.stderr)
        chunks.append(f"\nexit={proc.returncode} ({label})\n")
        overall_return = max(overall_return, proc.returncode)

    result = "passed" if overall_return == 0 else f"failed exit={overall_return}"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text("".join(chunks) or "No verification commands found.\n", encoding="utf-8")
    return result, log_path


def update_manifest_completion(root: Path, state: dict[str, Any]) -> None:
    manifest = repo_path(root, "benchmark-run.md")
    if not manifest.exists():
        return
    final_commit = run_git(root, ["rev-parse", "HEAD"], check=False) or "unknown"
    elapsed = int(time.time() - float(state.get("started_at_epoch", time.time())))
    replacements = {
        "- Latest verification result:": state.get("latest_verification", "not-run"),
        "- Stop reason:": state.get("stop_reason") or "",
        "- Observed elapsed time:": f"{elapsed}s",
        "- Observed token usage:": str(state.get("observed_token_usage", "unknown")),
        "- Observed turns:": str(state.get("observed_turns", 0)),
        "- Observed tool calls:": str(state.get("observed_tool_calls", "unknown")),
        "- Final commit:": final_commit,
        "- Comparison eligible:": str(state.get("comparison_eligible", "unknown")),
    }
    new_lines: list[str] = []
    for line in manifest.read_text(encoding="utf-8").splitlines():
        matched = False
        for prefix, value in replacements.items():
            if line.startswith(prefix):
                new_lines.append(f"{prefix} {value}")
                matched = True
                break
        if not matched:
            new_lines.append(line)
    manifest.write_text("\n".join(new_lines) + "\n", encoding="utf-8")


def checkpoint(root: Path, config: dict[str, Any], state: dict[str, Any]) -> Path:
    checkpoint_number = int(state.get("observed_turns", 0))
    path = (
        run_dir(root, config["run_id"])
        / "checkpoints"
        / f"checkpoint-{checkpoint_number:04d}.json"
    )
    commit = run_git(root, ["rev-parse", "HEAD"], check=False) or "unknown"
    status = run_git(root, ["status", "--short"], check=False)
    data = {
        "run_id": config["run_id"],
        "state": state["state"],
        "current_branch": run_git(root, ["branch", "--show-current"], check=False),
        "current_commit": commit,
        "elapsed_seconds": int(time.time() - float(state["started_at_epoch"])),
        "observed_turns": state["observed_turns"],
        "observed_token_usage": state.get("observed_token_usage", "unknown"),
        "observed_tool_calls": state.get("observed_tool_calls", "unknown"),
        "latest_prompt": state.get("latest_prompt"),
        "latest_agent_log": state.get("latest_agent_log"),
        "latest_codex_log": state.get("latest_codex_log"),
        "latest_verification": state.get("latest_verification"),
        "material_progress": state.get("latest_material_progress", False),
        "idle_count": state.get("idle_count", 0),
        "failure_count": state.get("failure_count", 0),
        "stop_reason": state.get("stop_reason"),
        "git_status": status,
        "created_at": utc_now(),
    }
    atomic_write_json(path, data)
    state["latest_checkpoint"] = str(path.relative_to(root))
    return path


def maybe_commit_checkpoint(root: Path, config: dict[str, Any], state: dict[str, Any]) -> None:
    if not config.get("checkpoint_commits"):
        return
    paths = [
        path
        for path in state.get("latest_material_paths", [])
        if path
        and not path.startswith(".vibe-bench/")
        and not path.startswith("specs/")
        and path != "specs"
    ]
    if not paths:
        state["latest_checkpoint_commit"] = "skipped: no new material paths"
        return
    add_proc = run_command(["git", "add", *paths], cwd=root)
    if add_proc.returncode != 0:
        state["latest_checkpoint_commit"] = f"git add failed: {add_proc.stderr.strip()}"
        return
    message = f"checkpoint({config['run_id']}): turn {state['observed_turns']}"
    commit_proc = run_command(["git", "commit", "-m", message], cwd=root)
    if commit_proc.returncode != 0:
        state["latest_checkpoint_commit"] = (
            f"git commit failed: {commit_proc.stderr.strip()}"
        )
        return
    state["latest_checkpoint_commit"] = run_git(root, ["rev-parse", "HEAD"], check=False)


def stop_reason_if_budget_exhausted(config: dict[str, Any], state: dict[str, Any]) -> str | None:
    budgets = config["budgets"]
    elapsed = int(time.time() - float(state["started_at_epoch"]))
    wall_limit = parse_duration_seconds(budgets["wall_clock_limit"])
    if wall_limit is not None and elapsed >= wall_limit:
        return "budget-exhausted-wall-clock"
    turn_limit = parse_int_limit(budgets["turn_limit"])
    if turn_limit is not None and int(state["observed_turns"]) >= turn_limit:
        return "budget-exhausted-turn-limit"
    token_limit = parse_int_limit(budgets["token_limit"])
    observed = state.get("observed_token_usage")
    if token_limit is not None and isinstance(observed, int) and observed >= token_limit:
        return "budget-exhausted-token-limit"
    return None


def finalize_state(
    root: Path,
    config: dict[str, Any],
    state: dict[str, Any],
    *,
    stop_reason: str,
    comparison_eligible: str,
) -> None:
    state["state"] = "complete" if stop_reason == "success" else "blocked"
    state["stop_reason"] = stop_reason
    state["comparison_eligible"] = comparison_eligible
    update_manifest_completion(root, state)
    checkpoint(root, config, state)
    save_state(root, config["run_id"], state)


def select_prompt_kind(state: dict[str, Any], config: dict[str, Any]) -> str:
    if state.get("idle_count", 0) >= parse_int_limit(config["budgets"]["idle_limit"]):
        return "blocked"
    latest = str(state.get("latest_verification", "not-run"))
    if latest.startswith("failed"):
        return "verify"
    last_message_path = state.get("latest_last_message")
    if last_message_path:
        text = repo_path(Path(config["repo_root"]), last_message_path).read_text(
            encoding="utf-8", errors="replace"
        )
        if "complete" in text.lower() and latest != "passed":
            return "premature-stop"
    return "continue"


def remaining_wall_clock_seconds(config: dict[str, Any], state: dict[str, Any]) -> int | None:
    wall_limit = parse_duration_seconds(config["budgets"]["wall_clock_limit"])
    if wall_limit is None:
        return None
    elapsed = int(time.time() - float(state["started_at_epoch"]))
    return max(1, wall_limit - elapsed)


def run_one_turn(
    root: Path,
    config: dict[str, Any],
    state: dict[str, Any],
    *,
    stream_agent_events: bool = False,
) -> dict[str, Any]:
    run_id = config["run_id"]
    turn_number = int(state["observed_turns"]) + 1
    prompt_kind = "initial" if turn_number == 1 else select_prompt_kind(state, config)
    prompt = prompt_for_turn(root, config, state, prompt_kind)
    prompt_path = run_dir(root, run_id) / "prompts" / f"turn-{turn_number:04d}.md"
    log_dir = agent_log_dir(root, config)
    agent_log_path = log_dir / f"turn-{turn_number:04d}.jsonl"
    stderr_path = log_dir / f"turn-{turn_number:04d}.stderr.txt"
    last_message_path = log_dir / f"turn-{turn_number:04d}.last.md"
    prompt_path.parent.mkdir(parents=True, exist_ok=True)
    prompt_path.write_text(prompt, encoding="utf-8")

    state["state"] = "running-turn"
    state["latest_prompt"] = str(prompt_path.relative_to(root))
    save_state(root, run_id, state)

    pre_status = run_git(root, ["status", "--short"], check=False)
    if config.get("agent_kind") == "pi":
        session_dir = log_dir / "sessions"
        session_dir.mkdir(parents=True, exist_ok=True)
        agent_env = pi_environment(root, config, session_dir=session_dir)
        prepare_pi_provider_config(root, config, agent_env)
        argv = build_pi_argv(config, root, prompt=prompt, session_dir=session_dir)
        input_text = None
    else:
        agent_env = None
        argv = build_codex_argv(
            config,
            root,
            turn_number=turn_number,
            output_last_message=last_message_path,
            session_id=state.get("session_id"),
        )
        input_text = prompt
    started = time.time()
    if stream_agent_events:
        print(f"[{run_id} turn {turn_number}] starting {config['tool_name']}", flush=True)

        def stdout_callback(line: str) -> None:
            summary = summarize_agent_event_line(config, turn_number, line)
            if summary:
                print(summary, flush=True)

        def stderr_callback(line: str) -> None:
            text = compact_text(line)
            if text:
                print(f"[{run_id} turn {turn_number}] stderr {text}", flush=True)

        proc = run_command_streaming(
            argv,
            cwd=root,
            stdout_path=agent_log_path,
            stderr_path=stderr_path,
            input_text=input_text,
            timeout=remaining_wall_clock_seconds(config, state),
            env=agent_env,
            stdout_callback=stdout_callback,
            stderr_callback=stderr_callback,
        )
    else:
        proc = run_command(
            argv,
            cwd=root,
            input_text=input_text,
            timeout=remaining_wall_clock_seconds(config, state),
            env=agent_env,
        )
        agent_log_path.write_text(proc.stdout, encoding="utf-8")
        stderr_path.write_text(proc.stderr, encoding="utf-8")
    elapsed = round(time.time() - started, 3)
    if config.get("agent_kind") == "pi":
        last_message_path.write_text(proc.stdout, encoding="utf-8")
    if stream_agent_events:
        print(
            f"[{run_id} turn {turn_number}] exited code={proc.returncode} elapsed={elapsed}s",
            flush=True,
        )

    state["state"] = "post-turn-audit"
    state["latest_agent_log"] = str(agent_log_path.relative_to(root))
    if config.get("agent_kind") == "codex":
        state["latest_codex_log"] = str(agent_log_path.relative_to(root))
    state["latest_last_message"] = str(last_message_path.relative_to(root))
    state["latest_agent_exit_code"] = proc.returncode
    state["latest_agent_elapsed_seconds"] = elapsed

    events = parse_agent_events(config, agent_log_path)
    if events["session_id"]:
        state["session_id"] = events["session_id"]
    if events["total_tokens"] is not None:
        state["observed_token_usage"] = events["total_tokens"]
    if events["tool_calls"] is not None:
        state["observed_tool_calls"] = events["tool_calls"]

    if proc.returncode != 0:
        state["failure_count"] = int(state.get("failure_count", 0)) + 1
    else:
        state["failure_count"] = 0
    state["observed_turns"] = turn_number

    post_status = run_git(root, ["status", "--short"], check=False)
    post_paths = changed_paths(post_status)
    pre_paths = changed_paths(pre_status)
    new_material = sorted(set(material_paths(post_paths)) - set(material_paths(pre_paths)))
    any_material = bool(new_material or material_paths(post_paths))
    state["latest_material_paths"] = new_material
    state["latest_material_progress"] = any_material
    if any_material:
        state["idle_count"] = 0
    else:
        state["idle_count"] = int(state.get("idle_count", 0)) + 1

    if specs_changed(post_paths):
        state["state"] = "invalid"
        state["stop_reason"] = "invalid-specs-modified"
        state["comparison_eligible"] = "no: specs modified"
        save_state(root, run_id, state)
        return state

    state["state"] = "verifying"
    save_state(root, run_id, state)
    verification_result, verification_log = run_verification(
        root,
        run_id,
        turn_number,
        timeout=remaining_wall_clock_seconds(config, state),
    )
    state["latest_verification"] = verification_result
    state["latest_verification_log"] = str(verification_log.relative_to(root))

    state["state"] = "checkpointing"
    checkpoint(root, config, state)
    maybe_commit_checkpoint(root, config, state)
    save_state(root, run_id, state)
    return state


def command_run(args: argparse.Namespace) -> None:
    root = args.repo_root.resolve()
    config = load_config(root, args.run_id)
    config["repo_root"] = str(root)
    state = load_state(root, args.run_id)
    if state["state"] in {"complete", "blocked", "invalid"} and not args.force:
        print(json.dumps(state, indent=2, sort_keys=True))
        return

    while True:
        stop_reason = stop_reason_if_budget_exhausted(config, state)
        if stop_reason:
            finalize_state(
                root,
                config,
                state,
                stop_reason=stop_reason,
                comparison_eligible="yes" if stop_reason.startswith("budget") else "unknown",
            )
            break

        state = run_one_turn(
            root,
            config,
            state,
            stream_agent_events=args.stream_agent_events,
        )
        failure_limit = parse_int_limit(config["budgets"]["failure_limit"]) or 0
        idle_limit = parse_int_limit(config["budgets"]["idle_limit"]) or 0

        if state["state"] == "invalid":
            update_manifest_completion(root, state)
            checkpoint(root, config, state)
            save_state(root, args.run_id, state)
            break
        if int(state.get("failure_count", 0)) >= failure_limit:
            finalize_state(
                root,
                config,
                state,
                stop_reason="blocked-infrastructure",
                comparison_eligible="no: infrastructure failure limit reached",
            )
            break
        if int(state.get("idle_count", 0)) > idle_limit:
            finalize_state(
                root,
                config,
                state,
                stop_reason="blocked-idle",
                comparison_eligible="yes",
            )
            break
        if state.get("latest_verification") == "passed" and args.stop_on_pass:
            finalize_state(
                root,
                config,
                state,
                stop_reason="success",
                comparison_eligible="yes",
            )
            break

        if args.max_new_turns is not None:
            args.max_new_turns -= 1
            if args.max_new_turns <= 0:
                state["state"] = "post-turn-audit"
                save_state(root, args.run_id, state)
                break


def command_resume(args: argparse.Namespace) -> None:
    command_run(args)


def command_status(args: argparse.Namespace) -> None:
    root = args.repo_root.resolve()
    state = load_state(root, args.run_id)
    print(json.dumps(state, indent=2, sort_keys=True))


def command_finalize(args: argparse.Namespace) -> None:
    root = args.repo_root.resolve()
    config = load_config(root, args.run_id)
    state = load_state(root, args.run_id)
    finalize_state(
        root,
        config,
        state,
        stop_reason=args.stop_reason,
        comparison_eligible=args.comparison_eligible,
    )
    print(f"Finalized run {args.run_id}: {args.stop_reason}")


def command_log_intervention(args: argparse.Namespace) -> None:
    root = args.repo_root.resolve()
    state = load_state(root, args.run_id)
    entry = {
        "timestamp": utc_now(),
        "actor": args.actor,
        "action": args.action,
        "reason": args.reason,
        "model_visible_guidance_changed": args.model_visible_guidance_changed,
    }
    path = run_dir(root, args.run_id) / "interventions.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, sort_keys=True) + "\n")
    state["latest_intervention"] = entry
    save_state(root, args.run_id, state)
    print(f"Recorded intervention for run {args.run_id}")


def add_common_run_arg(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--max-new-turns", type=int)
    parser.add_argument("--stop-on-pass", action="store_true")
    parser.add_argument(
        "--stream-agent-events",
        action="store_true",
        help="Print compact live agent progress while teeing raw output to run logs.",
    )
    parser.add_argument("--force", action="store_true")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Meta-harness for Vibe Browser benchmark agent runs.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(
            """
            Examples:
              python3 scripts/codex_meta_harness.py init --target m5 --profile standard-v0 --model glm-5.1:cloud --codex-command "ollama-codex --model glm-5.1:cloud" --codex-command-mode interactive-shell
              python3 scripts/codex_meta_harness.py init --agent-kind pi --target m1 --profile smoke-v0 --wall-clock-limit 10m --model glm-5.1:cloud --model-provider ollama
              python3 scripts/codex_meta_harness.py run --run-id r001
              python3 scripts/codex_meta_harness.py status --run-id r001
            """
        ),
    )
    parser.add_argument("--repo-root", type=Path, default=ROOT)
    subparsers = parser.add_subparsers(dest="command", required=True)

    init = subparsers.add_parser("init", help="initialize a benchmark agent run")
    init.add_argument("--agent-kind", choices=["codex", "pi"], default="codex")
    init.add_argument("--target", default="m5")
    init.add_argument("--profile", default="standard-v0", choices=sorted(PROFILE_DEFAULTS))
    init.add_argument("--model", required=True)
    init.add_argument("--model-provider")
    init.add_argument("--model-snapshot", default="unknown")
    init.add_argument("--codex-command", default="codex")
    init.add_argument(
        "--codex-command-mode",
        choices=["argv", "interactive-shell"],
        default="argv",
        help="Use interactive-shell for zsh aliases/functions such as ollama-codex.",
    )
    init.add_argument("--codex-model-arg", choices=["auto", "always", "never"], default="auto")
    init.add_argument("--allow-dangerous-codex-bypass", action="store_true")
    init.add_argument("--pi-command", default="pi")
    init.add_argument("--pi-tools", default=PI_DEFAULT_TOOLS)
    init.add_argument("--pi-mode", default="json")
    init.add_argument("--container-execution", default="host")
    init.add_argument("--checkpoint-commits", action="store_true")
    init.add_argument("--sandbox", default="workspace-write")
    init.add_argument("--network-policy", default="recorded benchmark policy")
    init.add_argument("--human-intervention-policy", default="administrative-only")
    init.add_argument("--run-id")
    init.add_argument("--timestamp")
    init.add_argument("--branch")
    init.add_argument("--base-benchmark-commit")
    init.add_argument("--benchmark-input-digest")
    init.add_argument("--turn-limit", type=int)
    init.add_argument("--wall-clock-limit")
    init.add_argument("--idle-limit", type=int)
    init.add_argument("--failure-limit", type=int)
    init.add_argument("--checkpoint-interval")
    init.add_argument("--create-branch", action="store_true")
    init.add_argument("--force", action="store_true")
    init.set_defaults(func=command_init)

    run = subparsers.add_parser("run", help="run until a stop condition")
    add_common_run_arg(run)
    run.set_defaults(func=command_run)

    resume = subparsers.add_parser("resume", help="resume a run by run id")
    add_common_run_arg(resume)
    resume.set_defaults(func=command_resume)

    status = subparsers.add_parser("status", help="print current run state")
    status.add_argument("--run-id", required=True)
    status.set_defaults(func=command_status)

    finalize = subparsers.add_parser("finalize", help="write final manifest state")
    finalize.add_argument("--run-id", required=True)
    finalize.add_argument("--stop-reason", default="evaluator-stop")
    finalize.add_argument("--comparison-eligible", default="unknown")
    finalize.set_defaults(func=command_finalize)

    intervention = subparsers.add_parser(
        "log-intervention", help="append an administrative intervention record"
    )
    intervention.add_argument("--run-id", required=True)
    intervention.add_argument("--actor", required=True)
    intervention.add_argument("--action", required=True)
    intervention.add_argument("--reason", required=True)
    intervention.add_argument("--model-visible-guidance-changed", action="store_true")
    intervention.set_defaults(func=command_log_intervention)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
