#!/usr/bin/env python3
"""Docker wrapper for 10-minute PI/Ollama benchmark smoke runs."""

from __future__ import annotations

import argparse
import datetime as dt
import os
from pathlib import Path
import re
import shlex
import subprocess
import sys
import tarfile
import textwrap


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_IMAGE = "vibe-browser-pi-benchmark:latest"
DEFAULT_DOCKERFILE = Path("docker/pi-benchmark.Dockerfile")
DEFAULT_PASS_ENV = ("OLLAMA_HOST", "OLLAMA_API_KEY")


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


def build_docker_build_argv(root: Path, image: str, dockerfile: Path) -> list[str]:
    return [
        "docker",
        "build",
        "-f",
        str((root / dockerfile).resolve()),
        "-t",
        image,
        str(root),
    ]


def shell_quote_command(args: list[str]) -> str:
    return " ".join(shlex.quote(arg) for arg in args)


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
    if args.turn_limit is not None:
        init_args.extend(["--turn-limit", str(args.turn_limit)])
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

    export_dir = f".vibe-bench/docker-export/{shlex.quote(run_id)}"
    artifact_script = (
        f"mkdir -p {export_dir} && "
        f"{shell_quote_command(init_args)} && "
        f"{shell_quote_command(run_args)}; "
        "status=$?; "
        f"git status --short > {export_dir}/git-status.txt || true; "
        f"git diff --binary > {export_dir}/worktree.diff || true; "
        f"git ls-files --others --exclude-standard -z > {export_dir}/untracked-files.zlist || true; "
        f"python3 scripts/pi_docker_benchmark.py archive-untracked "
        f"--list-file {export_dir}/untracked-files.zlist "
        f"--output {export_dir}/untracked-files.tar || true; "
        f"cp -R .vibe-bench/runs/{shlex.quote(run_id)} {export_dir}/run || true; "
        f"cp benchmark-run.md {export_dir}/benchmark-run.md || true; "
        "exit $status"
    )
    return artifact_script


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
    argv = build_docker_build_argv(root, args.image, args.dockerfile)
    if args.print_only:
        print(shell_quote_command(argv))
        return
    proc = run_command(argv, cwd=root)
    sys.stdout.write(proc.stdout)
    sys.stderr.write(proc.stderr)
    raise SystemExit(proc.returncode)


def command_run(args: argparse.Namespace) -> None:
    root = args.repo_root.resolve()
    run_id = args.run_id or timestamp_run_id()
    artifacts_dir = (root / ".vibe-bench" / "docker-artifacts" / run_id).resolve()
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    if not args.skip_build:
        build_argv = build_docker_build_argv(root, args.image, args.dockerfile)
        if args.print_only:
            print(shell_quote_command(build_argv))
        else:
            build_proc = run_command(build_argv, cwd=root)
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
    if pre_rm_proc.returncode == 0:
        sys.stdout.write(pre_rm_proc.stdout)
    elif pre_rm_proc.stderr and "No such container" not in pre_rm_proc.stderr:
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
    sys.stdout.write(rm_proc.stdout)
    sys.stderr.write(rm_proc.stderr)
    raise SystemExit(proc.returncode)


def command_archive_untracked(args: argparse.Namespace) -> None:
    root = args.repo_root.resolve()
    output = args.output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    raw_paths = args.list_file.read_bytes() if args.list_file.exists() else b""
    paths = [
        item.decode("utf-8", errors="surrogateescape")
        for item in raw_paths.split(b"\0")
        if item
    ]
    with tarfile.open(output, "w") as archive:
        for relative in paths:
            path = (root / relative).resolve()
            if not path.is_file() or not path.is_relative_to(root):
                continue
            if ".git" in path.relative_to(root).parts:
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
    run.add_argument("--pi-command", default="pi")
    run.add_argument("--pi-tools", default="read,write,edit,bash,grep,find,ls")
    run.add_argument("--network", default="bridge")
    run.add_argument("--network-policy", default="provider and dependency access")
    run.add_argument("--human-intervention-policy", default="administrative-only")
    run.add_argument("--pass-env", action="append", default=list(DEFAULT_PASS_ENV))
    run.add_argument("--env", action="append", default=[])
    run.set_defaults(stream_agent_events=True)
    run.set_defaults(func=command_run)

    archive = subparsers.add_parser(
        "archive-untracked",
        help=argparse.SUPPRESS,
    )
    archive.add_argument("--list-file", type=Path, required=True)
    archive.add_argument("--output", type=Path, required=True)
    archive.set_defaults(func=command_archive_untracked)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
