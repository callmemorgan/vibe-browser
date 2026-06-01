#!/usr/bin/env python3
"""Docker wrapper for 10-minute PI/Ollama benchmark smoke runs."""

from __future__ import annotations

import argparse
from contextlib import contextmanager
import datetime as dt
import json
import os
from pathlib import Path
import re
import shutil
import shlex
import subprocess
import sys
import tarfile
import tempfile
import textwrap


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_IMAGE = "vibe-browser-pi-benchmark:latest"
DEFAULT_DOCKERFILE = Path("docker/pi-benchmark.Dockerfile")
DEFAULT_PASS_ENV = ("OLLAMA_HOST", "OLLAMA_API_KEY")
DEFAULT_WALL_CLOCK_TURN_LIMIT = 100


def slug(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value or "unknown"


def timestamp_run_id() -> str:
    return "pi" + dt.datetime.now(dt.UTC).strftime("%Y%m%d%H%M%S")


def container_name(run_id: str) -> str:
    return f"vibe-browser-pi-{slug(run_id)}"


def run_command(args: list[str], *, cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def run_command_live(args: list[str], *, cwd: Path) -> subprocess.CompletedProcess[None]:
    return subprocess.run(args, cwd=cwd, text=True, check=False)


def git_status_short(root: Path) -> str:
    proc = run_command(["git", "status", "--short"], cwd=root)
    if proc.returncode != 0:
        raise SystemExit(proc.stderr.strip() or "git status failed")
    return proc.stdout


def git_head(root: Path) -> str:
    proc = run_command(["git", "rev-parse", "HEAD"], cwd=root)
    if proc.returncode != 0:
        raise SystemExit(proc.stderr.strip() or "git rev-parse HEAD failed")
    return proc.stdout.strip()


def assert_clean_git_baseline(root: Path, *, allow_dirty: bool = False) -> None:
    if allow_dirty:
        return
    status = git_status_short(root)
    if status.strip():
        raise SystemExit(
            "Refusing to start benchmark from a dirty git worktree.\n"
            "Commit or stash baseline changes so participant artifacts stay clean, "
            "or pass --allow-dirty-baseline for an intentionally non-comparable run.\n\n"
            f"{status}"
        )


@contextmanager
def git_archive_build_context(root: Path):
    with tempfile.TemporaryDirectory(prefix="vibe-browser-docker-context-") as temp:
        temp_path = Path(temp)
        archive_path = temp_path / "repo.tar"
        context_path = temp_path / "context"
        context_path.mkdir()
        proc = run_command(
            ["git", "archive", "--format=tar", "--output", str(archive_path), "HEAD"],
            cwd=root,
        )
        if proc.returncode != 0:
            raise SystemExit(proc.stderr.strip() or "git archive failed")
        with tarfile.open(archive_path) as archive:
            archive.extractall(context_path)
        yield context_path


def build_docker_build_argv(
    root: Path,
    image: str,
    dockerfile: Path,
    *,
    build_args: dict[str, str] | None = None,
) -> list[str]:
    argv = [
        "docker",
        "build",
        "-f",
        str((root / dockerfile).resolve()),
        "-t",
        image,
    ]
    for name, value in (build_args or {}).items():
        argv.extend(["--build-arg", f"{name}={value}"])
    argv.append(str(root))
    return argv


def shell_quote_command(args: list[str]) -> str:
    return " ".join(shlex.quote(arg) for arg in args)


def effective_turn_limit(args: argparse.Namespace) -> int | None:
    if args.turn_limit is not None:
        return args.turn_limit
    if args.wall_clock_limit and args.wall_clock_limit != "unknown":
        return DEFAULT_WALL_CLOCK_TURN_LIMIT
    return None


def container_shell_command(args: argparse.Namespace, run_id: str) -> str:
    init_args = [
        "python3",
        "scripts/codex_meta_harness.py",
        "init",
        "--agent-kind",
        "pi",
        "--target",
        args.target,
        "--profile",
        args.profile,
        "--wall-clock-limit",
        args.wall_clock_limit,
        "--model-provider",
        args.provider,
        "--model",
        args.model,
        "--pi-command",
        args.pi_command,
        "--pi-tools",
        args.pi_tools,
        "--container-execution",
        "docker-admin-v0",
        "--network-policy",
        args.network_policy,
        "--human-intervention-policy",
        args.human_intervention_policy,
        "--run-id",
        run_id,
        "--force",
    ]
    base_benchmark_commit = getattr(args, "base_benchmark_commit", None)
    if base_benchmark_commit:
        init_args.extend(["--base-benchmark-commit", base_benchmark_commit])
    turn_limit = effective_turn_limit(args)
    if turn_limit is not None:
        init_args.extend(["--turn-limit", str(turn_limit)])
    if args.failure_limit is not None:
        init_args.extend(["--failure-limit", str(args.failure_limit)])
    if args.idle_limit is not None:
        init_args.extend(["--idle-limit", str(args.idle_limit)])

    run_args = [
        "python3",
        "scripts/codex_meta_harness.py",
        "run",
        "--run-id",
        run_id,
    ]
    if args.stream_agent_events:
        run_args.append("--stream-agent-events")
    if args.max_new_turns is not None:
        run_args.extend(["--max-new-turns", str(args.max_new_turns)])
    if args.stop_on_pass:
        run_args.append("--stop-on-pass")

    export_dir = shlex.quote(f".vibe-bench/docker-export/{run_id}")
    run_dir_path = shlex.quote(f".vibe-bench/runs/{run_id}")
    baseline_guard = ""
    if not args.allow_dirty_baseline:
        baseline_guard = (
            f"if [ -s {export_dir}/baseline-git-status.txt ]; then "
            "echo 'Dirty benchmark baseline inside Docker image; refusing to run.' >&2; "
            f"cat {export_dir}/baseline-git-status.txt >&2; "
            "exit 125; "
            "fi; "
        )
    return "".join(
        [
            f"mkdir -p {export_dir} && ",
            f"git status --short > {export_dir}/baseline-git-status.txt && ",
            baseline_guard,
            f"{shell_quote_command(init_args)} && ",
            f"{shell_quote_command(run_args)}; ",
            "status=$?; ",
            f"git status --short > {export_dir}/participant-git-status.txt || true; ",
            f"git diff --binary > {export_dir}/participant.diff || true; ",
            f"git ls-files --others --exclude-standard -z > {export_dir}/participant-untracked-files.zlist || true; ",
            f"python3 scripts/pi_docker_benchmark.py archive-untracked ",
            f"--list-file {export_dir}/participant-untracked-files.zlist ",
            f"--output {export_dir}/participant-untracked-files.tar || true; ",
            f"python3 scripts/pi_docker_benchmark.py export-submission ",
            f"--status-file {export_dir}/participant-git-status.txt ",
            f"--untracked-list-file {export_dir}/participant-untracked-files.zlist ",
            f"--output-dir {export_dir}/submission || true; ",
            f"python3 scripts/pi_docker_benchmark.py record-version-info ",
            f"--output {export_dir}/version-info.json || true; ",
            f"cp {export_dir}/participant-git-status.txt {export_dir}/git-status.txt || true; ",
            f"cp {export_dir}/participant.diff {export_dir}/worktree.diff || true; ",
            f"cp {export_dir}/participant-untracked-files.zlist {export_dir}/untracked-files.zlist || true; ",
            f"cp {export_dir}/participant-untracked-files.tar {export_dir}/untracked-files.tar || true; ",
            f"cp -R {run_dir_path} {export_dir}/run || true; ",
            f"cp benchmark-run.md {export_dir}/benchmark-run.md || true; ",
            "exit $status",
        ]
    )


def docker_env_args(args: argparse.Namespace, run_id: str) -> list[str]:
    env_args = [
        "-e",
        "PI_SKIP_VERSION_CHECK=1",
        "-e",
        f"PI_CODING_AGENT_DIR=/workspace/vibe-browser/.vibe-bench/runs/{run_id}/pi/agent",
        "-e",
        f"PI_CODING_AGENT_SESSION_DIR=/workspace/vibe-browser/.vibe-bench/runs/{run_id}/pi/sessions",
    ]
    for name in args.pass_env:
        if name in os.environ:
            env_args.extend(["-e", name])
    for value in args.env:
        env_args.extend(["-e", value])
    return env_args


def build_docker_run_argv(
    root: Path,
    args: argparse.Namespace,
    *,
    run_id: str,
) -> list[str]:
    name = container_name(run_id)
    command = container_shell_command(args, run_id)
    return [
        "docker",
        "run",
        "--name",
        name,
        "--user",
        "root",
        "--workdir",
        "/workspace/vibe-browser",
        "--network",
        args.network,
        *docker_env_args(args, run_id),
        args.image,
        "bash",
        "-lc",
        command,
    ]


def build_docker_cp_argv(run_id: str, artifacts_dir: Path) -> list[str]:
    name = container_name(run_id)
    return [
        "docker",
        "cp",
        f"{name}:/workspace/vibe-browser/.vibe-bench/docker-export/{run_id}/.",
        str(artifacts_dir.resolve()),
    ]


def build_docker_rm_argv(run_id: str) -> list[str]:
    return ["docker", "rm", "-f", container_name(run_id)]


def assert_no_forbidden_mounts(argv: list[str]) -> None:
    joined = "\n".join(argv)
    forbidden = ("/var/run/docker.sock", f"{Path.home()}:", f"{Path.home()}/.pi")
    for value in forbidden:
        if value in joined:
            raise SystemExit(f"forbidden Docker mount or path in command: {value}")


def command_build_image(args: argparse.Namespace) -> None:
    root = args.repo_root.resolve()
    build_args = {"VIBE_BENCHMARK_BASE_COMMIT": git_head(root)}
    if args.print_only:
        argv = build_docker_build_argv(
            root,
            args.image,
            args.dockerfile,
            build_args=build_args,
        )
        print(shell_quote_command(argv))
        return
    with git_archive_build_context(root) as context_root:
        argv = build_docker_build_argv(
            context_root,
            args.image,
            args.dockerfile,
            build_args=build_args,
        )
        proc = run_command(argv, cwd=context_root)
    sys.stdout.write(proc.stdout)
    sys.stderr.write(proc.stderr)
    raise SystemExit(proc.returncode)


def command_run(args: argparse.Namespace) -> None:
    root = args.repo_root.resolve()
    run_id = args.run_id or timestamp_run_id()
    artifacts_dir = (root / ".vibe-bench" / "docker-artifacts" / run_id).resolve()
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    if not args.print_only:
        assert_clean_git_baseline(root, allow_dirty=args.allow_dirty_baseline)
    if not getattr(args, "base_benchmark_commit", None):
        args.base_benchmark_commit = git_head(root)

    if not args.skip_build:
        if args.print_only:
            build_argv = build_docker_build_argv(
                root,
                args.image,
                args.dockerfile,
                build_args={
                    "VIBE_BENCHMARK_BASE_COMMIT": args.base_benchmark_commit
                },
            )
            print(shell_quote_command(build_argv))
        else:
            with git_archive_build_context(root) as context_root:
                build_argv = build_docker_build_argv(
                    context_root,
                    args.image,
                    args.dockerfile,
                    build_args={
                        "VIBE_BENCHMARK_BASE_COMMIT": args.base_benchmark_commit
                    },
                )
                build_proc = run_command(build_argv, cwd=context_root)
            sys.stdout.write(build_proc.stdout)
            sys.stderr.write(build_proc.stderr)
            if build_proc.returncode != 0:
                raise SystemExit(build_proc.returncode)

    run_argv = build_docker_run_argv(
        root,
        args,
        run_id=run_id,
    )
    assert_no_forbidden_mounts(run_argv)
    rm_argv = build_docker_rm_argv(run_id)
    if args.print_only:
        print(shell_quote_command(rm_argv))
        print(shell_quote_command(run_argv))
        print(shell_quote_command(build_docker_cp_argv(run_id, artifacts_dir)))
        print(shell_quote_command(rm_argv))
        return
    pre_rm_proc = run_command(rm_argv, cwd=root)
    if pre_rm_proc.returncode != 0 and "No such container" not in pre_rm_proc.stderr:
        sys.stderr.write(pre_rm_proc.stderr)
    name = container_name(run_id)
    print(f"Container: {name}")
    print(f"Watch live: docker logs -f {name}")
    sys.stdout.flush()
    proc = run_command_live(run_argv, cwd=root)
    cp_proc = run_command(build_docker_cp_argv(run_id, artifacts_dir), cwd=root)
    sys.stdout.write(cp_proc.stdout)
    sys.stderr.write(cp_proc.stderr)
    rm_proc = run_command(rm_argv, cwd=root)
    if rm_proc.returncode != 0:
        sys.stderr.write(rm_proc.stderr)
    image_id = docker_image_id(root, args.image)
    summary = write_summary_json(
        run_id=run_id,
        container=name,
        artifacts_dir=artifacts_dir,
        image=args.image,
        image_id=image_id,
        container_exit_code=proc.returncode,
        artifact_copy_exit_code=cp_proc.returncode,
    )
    print_run_summary(
        run_id=run_id,
        container=name,
        artifacts_dir=artifacts_dir,
        summary=summary,
        container_exit_code=proc.returncode,
        artifact_copy_exit_code=cp_proc.returncode,
    )
    raise SystemExit(proc.returncode if proc.returncode != 0 else cp_proc.returncode)


def docker_image_id(root: Path, image: str) -> str:
    proc = run_command(
        ["docker", "image", "inspect", "--format", "{{.Id}}", image],
        cwd=root,
    )
    if proc.returncode != 0:
        return "unknown"
    return proc.stdout.strip() or "unknown"


def read_json_file(path: Path) -> dict[str, object]:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return data if isinstance(data, dict) else {}


def parse_status_paths(status_text: str) -> list[str]:
    paths: list[str] = []
    for line in status_text.splitlines():
        if not line:
            continue
        path = line[3:] if len(line) > 3 else line
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        if path.endswith("/"):
            continue
        if path and path not in paths:
            paths.append(path)
    return paths


def read_zlist(path: Path) -> list[str]:
    raw = path.read_bytes() if path.exists() else b""
    return [
        item.decode("utf-8", errors="surrogateescape")
        for item in raw.split(b"\0")
        if item
    ]


def safe_relative_file(root: Path, relative: str) -> Path | None:
    path = (root / relative).resolve()
    if not path.is_file() or not path.is_relative_to(root):
        return None
    rel_parts = path.relative_to(root).parts
    if ".git" in rel_parts or ".vibe-bench" in rel_parts or "__pycache__" in rel_parts:
        return None
    return path


def participant_paths_from_files(status_file: Path, untracked_list_file: Path) -> list[str]:
    paths = parse_status_paths(
        status_file.read_text(encoding="utf-8", errors="replace")
        if status_file.exists()
        else ""
    )
    for path in read_zlist(untracked_list_file):
        if path not in paths:
            paths.append(path)
    return sorted(paths)


def command_export_submission(args: argparse.Namespace) -> None:
    root = args.repo_root.resolve()
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    for relative in participant_paths_from_files(
        args.status_file,
        args.untracked_list_file,
    ):
        source = safe_relative_file(root, relative)
        if source is None:
            continue
        destination = output_dir / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)


def command_record_version_info(args: argparse.Namespace) -> None:
    root = args.repo_root.resolve()
    commands = {
        "python": ["python3", "--version"],
        "node": ["node", "--version"],
        "npm": ["npm", "--version"],
        "git": ["git", "--version"],
        "pi": ["pi", "--version"],
        "kernel": ["uname", "-a"],
    }
    data: dict[str, object] = {
        "recorded_at": dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat(),
        "commands": {},
        "environment": {
            "OLLAMA_HOST": os.environ.get("OLLAMA_HOST", ""),
            "OLLAMA_API_KEY_present": bool(os.environ.get("OLLAMA_API_KEY")),
            "PI_CODING_AGENT_PACKAGE": os.environ.get("PI_CODING_AGENT_PACKAGE", ""),
            "PI_CODING_AGENT_VERSION": os.environ.get("PI_CODING_AGENT_VERSION", ""),
            "VIBE_BENCHMARK_BASE_COMMIT": os.environ.get(
                "VIBE_BENCHMARK_BASE_COMMIT",
                "",
            ),
        },
    }
    command_results: dict[str, object] = {}
    for name, argv in commands.items():
        proc = run_command(argv, cwd=root)
        command_results[name] = {
            "argv": argv,
            "exit_code": proc.returncode,
            "stdout": proc.stdout.strip(),
            "stderr": proc.stderr.strip(),
        }
    data["commands"] = command_results
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")


def collect_turn_metrics(artifacts_dir: Path) -> list[dict[str, object]]:
    metrics: list[dict[str, object]] = []
    checkpoint_dir = artifacts_dir / "run" / "checkpoints"
    for path in sorted(checkpoint_dir.glob("checkpoint-*.json")):
        data = read_json_file(path)
        metrics.append(
            {
                "turn": data.get("observed_turns"),
                "elapsed_seconds": data.get("elapsed_seconds"),
                "agent_elapsed_seconds": data.get("latest_agent_elapsed_seconds"),
                "agent_exit_code": data.get("latest_agent_exit_code"),
                "verification": data.get("latest_verification"),
                "verification_log": data.get("latest_verification_log"),
                "tokens": data.get("observed_token_usage"),
                "tool_calls": data.get("observed_tool_calls"),
                "material_progress": data.get("material_progress"),
                "material_paths": data.get("latest_material_paths"),
                "idle_count": data.get("idle_count"),
                "failure_count": data.get("failure_count"),
            }
        )
    return metrics


def write_summary_json(
    *,
    run_id: str,
    container: str,
    artifacts_dir: Path,
    image: str,
    image_id: str,
    container_exit_code: int,
    artifact_copy_exit_code: int,
) -> dict[str, object]:
    state = read_json_file(artifacts_dir / "run" / "state.json")
    config = read_json_file(artifacts_dir / "run" / "config.json")
    version_info = read_json_file(artifacts_dir / "version-info.json")
    participant_status_path = artifacts_dir / "participant-git-status.txt"
    participant_status = (
        participant_status_path.read_text(encoding="utf-8", errors="replace")
        if participant_status_path.exists()
        else ""
    )
    participant_files = participant_paths_from_files(
        artifacts_dir / "participant-git-status.txt",
        artifacts_dir / "participant-untracked-files.zlist",
    )
    turn_metrics = collect_turn_metrics(artifacts_dir)
    summary: dict[str, object] = {
        "run_id": run_id,
        "container": container,
        "artifacts_dir": str(artifacts_dir),
        "container_exit_code": container_exit_code,
        "artifact_copy_exit_code": artifact_copy_exit_code,
        "docker": {
            "image": image,
            "image_id": image_id,
            "build_context": "git-archive-head",
        },
        "state": state,
        "config": {
            key: config.get(key)
            for key in (
                "agent_kind",
                "model_provider",
                "model",
                "profile",
                "target",
                "harness_version",
                "base_benchmark_commit",
                "benchmark_input_digest",
            )
            if key in config
        },
        "versions": version_info,
        "participant_files": participant_files,
        "participant_status": participant_status,
        "turn_metrics": turn_metrics,
    }
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    (artifacts_dir / "turn-metrics.json").write_text(
        json.dumps(turn_metrics, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (artifacts_dir / "summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return summary


def print_run_summary(
    *,
    run_id: str,
    container: str,
    artifacts_dir: Path,
    summary: dict[str, object] | None = None,
    container_exit_code: int,
    artifact_copy_exit_code: int,
) -> None:
    print()
    print(f"Benchmark run {run_id} finished")
    print(f"Container: {container} (exit {container_exit_code})")
    print(f"Artifacts: {artifacts_dir}")
    print(f"Artifact copy exit: {artifact_copy_exit_code}")

    if summary is None:
        state = read_json_file(artifacts_dir / "run" / "state.json")
    else:
        maybe_state = summary.get("state")
        state = maybe_state if isinstance(maybe_state, dict) else {}
    if not state:
        print("State summary: unavailable")
        return
    for label, key in (
        ("State", "state"),
        ("Stop reason", "stop_reason"),
        ("Latest verification", "latest_verification"),
        ("Observed turns", "observed_turns"),
        ("Observed tokens", "observed_token_usage"),
        ("Comparison eligible", "comparison_eligible"),
    ):
        value = state.get(key)
        if value is not None:
            print(f"{label}: {value}")


def command_archive_untracked(args: argparse.Namespace) -> None:
    root = args.repo_root.resolve()
    output = args.output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    with tarfile.open(output, "w") as archive:
        for relative in read_zlist(args.list_file):
            path = safe_relative_file(root, relative)
            if path is None:
                continue
            archive.add(path, arcname=relative)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run a PI/Ollama Vibe Browser benchmark in Docker.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(
            """
            Example:
              python3 scripts/pi_docker_benchmark.py run --target m1 --wall-clock-limit 10m --provider ollama --model glm-5.1:cloud
            """
        ),
    )
    parser.add_argument("--repo-root", type=Path, default=ROOT)
    subparsers = parser.add_subparsers(dest="command", required=True)

    build = subparsers.add_parser("build-image", help="build the PI benchmark image")
    build.add_argument("--image", default=DEFAULT_IMAGE)
    build.add_argument("--dockerfile", type=Path, default=DEFAULT_DOCKERFILE)
    build.add_argument("--print-only", action="store_true")
    build.set_defaults(func=command_build_image)

    run = subparsers.add_parser("run", help="run the 10-minute PI benchmark")
    run.add_argument("--image", default=DEFAULT_IMAGE)
    run.add_argument("--dockerfile", type=Path, default=DEFAULT_DOCKERFILE)
    run.add_argument("--skip-build", action="store_true")
    run.add_argument("--print-only", action="store_true")
    run.add_argument("--run-id")
    run.add_argument("--target", default="m1")
    run.add_argument("--profile", default="smoke-v0")
    run.add_argument("--wall-clock-limit", default="10m")
    run.add_argument("--turn-limit", type=int)
    run.add_argument("--failure-limit", type=int)
    run.add_argument("--idle-limit", type=int)
    run.add_argument("--max-new-turns", type=int)
    run.add_argument("--stop-on-pass", action="store_true")
    run.add_argument(
        "--no-stream-agent-events",
        dest="stream_agent_events",
        action="store_false",
        help="Disable compact live agent progress in container logs.",
    )
    run.add_argument("--provider", default="ollama")
    run.add_argument("--model", default="glm-5.1:cloud")
    run.add_argument("--base-benchmark-commit", help=argparse.SUPPRESS)
    run.add_argument("--pi-command", default="pi")
    run.add_argument("--pi-tools", default="read,write,edit,bash,grep,find,ls")
    run.add_argument("--network", default="bridge")
    run.add_argument("--network-policy", default="provider and dependency access")
    run.add_argument("--human-intervention-policy", default="administrative-only")
    run.add_argument("--pass-env", action="append", default=list(DEFAULT_PASS_ENV))
    run.add_argument("--env", action="append", default=[])
    run.add_argument(
        "--allow-dirty-baseline",
        action="store_true",
        help=(
            "Run even when the host worktree is dirty; treat the run as "
            "non-comparable."
        ),
    )
    run.set_defaults(stream_agent_events=True)
    run.set_defaults(func=command_run)

    archive = subparsers.add_parser(
        "archive-untracked",
        help=argparse.SUPPRESS,
    )
    archive.add_argument("--list-file", type=Path, required=True)
    archive.add_argument("--output", type=Path, required=True)
    archive.set_defaults(func=command_archive_untracked)

    submission = subparsers.add_parser(
        "export-submission",
        help=argparse.SUPPRESS,
    )
    submission.add_argument("--status-file", type=Path, required=True)
    submission.add_argument("--untracked-list-file", type=Path, required=True)
    submission.add_argument("--output-dir", type=Path, required=True)
    submission.set_defaults(func=command_export_submission)

    versions = subparsers.add_parser(
        "record-version-info",
        help=argparse.SUPPRESS,
    )
    versions.add_argument("--output", type=Path, required=True)
    versions.set_defaults(func=command_record_version_info)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
