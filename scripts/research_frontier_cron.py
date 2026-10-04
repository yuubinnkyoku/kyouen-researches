#!/usr/bin/env python3
"""Run one bounded research session from cron on a persistent Linux host.

Runtime state and logs live outside the checkout. This is not a cloud task
scheduler: neither this process nor a local cron survives a stopped cloud VM.
"""

from __future__ import annotations

import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import os
from pathlib import Path
import shlex
import shutil
import signal
import stat
import subprocess
import sys
import time


MARKER_START = "# BEGIN kyouen-research-frontier"
MARKER_END = "# END kyouen-research-frontier"
EXPECTED_REMOTE = "https://github.com/yuubinnkyoku/kyouen-researches.git"
PROMPT_PATH = Path("docs/research-frontier-prompt.md")
RATE_LIMIT_CODES = {"usage_limit_reached", "rate_limit_exceeded", "insufficient_quota"}


class Blocked(RuntimeError):
    pass


def command(args: list[str], cwd: Path | None = None) -> str:
    result = subprocess.run(args, cwd=cwd, text=True, capture_output=True, timeout=120)
    if result.returncode:
        # Do not echo arbitrary stderr from authentication or repository URLs.
        raise Blocked(f"command failed ({result.returncode}): {args[0]} {args[1]}")
    return result.stdout.strip()


def checkout_identity(repo: Path) -> None:
    if command(["git", "rev-parse", "--show-toplevel"], repo) != str(repo):
        raise Blocked("--repo must be the root of a dedicated checkout")
    if command(["git", "branch", "--show-current"], repo) != "main":
        raise Blocked("the dedicated checkout must be on main")


def clean_checkout(repo: Path) -> None:
    checkout_identity(repo)
    if command(["git", "status", "--porcelain", "--untracked-files=all"], repo):
        raise Blocked("checkout has changes; preserve and review them before another session")


def checkout_fingerprint(repo: Path) -> str:
    """Hash Git-visible pending work without following untracked symlinks.

    A resume can preserve the exact checkout left by this runner. It cannot
    adopt changes added by another task between runs or a stale HEAD.
    """
    digest = hashlib.sha256()
    for args in (
        ["git", "rev-parse", "HEAD"],
        ["git", "status", "--porcelain", "--untracked-files=all", "-z"],
        ["git", "diff", "--binary", "--no-ext-diff", "--no-textconv"],
        ["git", "diff", "--cached", "--binary", "--no-ext-diff", "--no-textconv"],
    ):
        process = subprocess.Popen(args, cwd=repo, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        while chunk := process.stdout.read(1024 * 1024):
            digest.update(chunk)
        process.stdout.close()
        if process.wait() != 0:
            raise Blocked("cannot fingerprint pending Git work")
        digest.update(b"\0")
    paths = subprocess.run(["git", "ls-files", "--others", "--exclude-standard", "-z"],
                           cwd=repo, capture_output=True, check=True).stdout
    for name in sorted(paths.split(b"\0")):
        if not name:
            continue
        digest.update(name + b"\0")
        path = repo / os.fsdecode(name)
        mode = path.lstat().st_mode
        if stat.S_ISLNK(mode):
            digest.update(b"symlink\0" + os.fsencode(os.readlink(path)))
        elif stat.S_ISREG(mode):
            digest.update(b"file\0")
            with path.open("rb") as source:
                while chunk := source.read(1024 * 1024):
                    digest.update(chunk)
        else:
            raise Blocked("pending work includes a non-regular untracked file")
        digest.update(b"\0")
    return digest.hexdigest()


def refresh_main(repo: Path, pending: dict | None = None) -> str:
    if pending:
        checkout_identity(repo)
        if pending.get("end_head") != command(["git", "rev-parse", "HEAD"], repo):
            raise Blocked("HEAD changed since interrupted research; preserve and review it")
        if pending.get("checkout_fingerprint") != checkout_fingerprint(repo):
            raise Blocked("pending work changed since interrupted research; preserve and review it")
    else:
        clean_checkout(repo)
    # Inspect the declared repository, allowing the host's normal HTTPS proxy
    # or insteadOf rewrite to provide its supported authentication route.
    remote = command(["git", "config", "--get", "remote.origin.url"], repo)
    if remote.rstrip("/").removesuffix(".git") != EXPECTED_REMOTE.removesuffix(".git"):
        raise Blocked("origin must be the expected HTTPS GitHub repository")
    command(["git", "fetch", "origin", "main"], repo)
    if not pending:
        ahead = command(["git", "rev-list", "--count", "origin/main..HEAD"], repo)
        if ahead != "0":
            raise Blocked("main has unpublished commits; review/push them before another session")
        command(["git", "merge", "--ff-only", "origin/main"], repo)
    return command(["git", "rev-parse", "HEAD"], repo)


@contextmanager
def exclusive_lock(state_dir: Path):
    state_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
    with (state_dir / "runner.lock").open("a") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            yield False
            return
        yield True


def save_state(path: Path, value: dict) -> None:
    temp = path.with_suffix(".tmp")
    temp.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")
    temp.replace(path)


def event_failure(events: Path) -> str | None:
    """Recognize structured failures, even if a CLI version exits zero.

    This does not infer rate limits from mathematical/agent discussion text.
    Unknown failures are failures and retain the same bounded cron retry policy.
    """
    failure = None
    for line in events.read_text(errors="replace").splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(event, dict):
            continue
        if event.get("type") not in {"error", "turn.failed"}:
            continue
        failure = "cli_error"
        error = event.get("error", event)
        if not isinstance(error, dict):
            continue
        code = error.get("code") or error.get("type")
        if code in RATE_LIMIT_CODES:
            return "quota"
        message = str(error.get("message", "")).lower()
        if any(phrase in message for phrase in (
            "usage limit", "rate limit", "quota exceeded", "insufficient quota",
        )):
            return "quota"
    return failure


def codex_args(codex: str, repo: Path, final: Path, *, preflight: bool) -> list[str]:
    if preflight:
        return [codex, "--no-daemon", "-a", "never", "-s", "read-only", "-C", str(repo),
                "exec", "--ephemeral", "--color", "never", "Do not use tools. Reply READY only."]
    # The approval reviewer, filesystem sandbox, and TLS verification stay enabled.
    return [codex, "--no-daemon", "--approve-for-me", "-C", str(repo), "exec",
            "--ephemeral", "--color", "never", "--json", "--output-last-message", str(final), "-"]


def run_bounded(args: list[str], prompt: str, events: Path, stderr: Path, seconds: int) -> int:
    with events.open("w") as output, stderr.open("w") as errors:
        process = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=output, stderr=errors,
                                   text=True, start_new_session=True)
        try:
            process.communicate(prompt, timeout=seconds)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGTERM)
            try:
                process.wait(timeout=15)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                process.wait()
            return 124
        return process.returncode


def cron_text(existing: str, cron_line: str) -> str:
    """Replace only our one managed block; preserve unrelated entries."""
    lines = existing.splitlines()
    if lines.count(MARKER_START) != lines.count(MARKER_END) or lines.count(MARKER_START) > 1:
        raise Blocked("malformed managed cron block; inspect the existing crontab")
    if MARKER_START in lines:
        start, end = lines.index(MARKER_START), lines.index(MARKER_END)
        if start >= end:
            raise Blocked("malformed managed cron block; inspect the existing crontab")
        lines[start:end + 1] = []
    return "\n".join(lines + [MARKER_START, cron_line, MARKER_END]) + "\n"


def preflight(repo: Path, state_dir: Path, codex: str) -> None:
    command([codex, "login", "status"])
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
    events = state_dir / f"{stamp}.preflight.stdout"
    errors = state_dir / f"{stamp}.preflight.stderr"
    code = run_bounded(codex_args(codex, repo, state_dir / "unused-final", preflight=True), "", events, errors, 60)
    if code != 0 or events.read_text().strip() != "READY":
        raise Blocked(f"read-only Codex inference failed (exit {code}); inspect local logs")


def install_cron(args, codex: str) -> None:
    crontab = shutil.which("crontab")
    if not crontab:
        raise Blocked("crontab is absent; use a persistent host with a running cron service")
    clean_checkout(args.repo)
    # Authentication metadata alone does not establish inference readiness.
    # Never install an entry until the current CLI completes real read-only inference.
    preflight(args.repo, args.state_dir, codex)
    previous = subprocess.run([crontab, "-l"], text=True, capture_output=True, timeout=30)
    if previous.returncode and "no crontab" not in previous.stderr.lower():
        raise Blocked("cannot read existing crontab; it has not been replaced")
    runner = Path(__file__).resolve()
    cli = [sys.executable, str(runner), "--repo", str(args.repo), "--state-dir", str(args.state_dir),
           "--codex", codex, "--max-seconds", str(args.max_seconds)]
    # Cron interprets '%' before shell quoting; reject it in paths instead of
    # producing a subtly broken command or replacing someone else's entries.
    if any("%" in part or "\n" in part or "\r" in part for part in cli):
        raise Blocked("cron paths must not contain percent signs or newlines")
    line = "17 * * * * " + shlex.join(cli) + " >> " + shlex.quote(str(args.state_dir / "cron.log")) + " 2>&1"
    text = cron_text(previous.stdout if previous.returncode == 0 else "", line)
    result = subprocess.run([crontab, "-"], input=text, text=True, capture_output=True, timeout=30)
    if result.returncode:
        raise Blocked("crontab installation failed")
    if command([crontab, "-l"]) != text.strip():
        raise Blocked("crontab read-back did not match; installation is unconfirmed")
    print("Installed hourly research entry at minute 17; cron service/runtime still requires a persistent host.")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--state-dir", type=Path, required=True)
    parser.add_argument("--codex", default="codex")
    parser.add_argument("--max-seconds", type=int, default=17400)
    parser.add_argument("--preflight", action="store_true", help="bounded read-only inference check")
    parser.add_argument("--install-cron", action="store_true", help="preserve existing cron entries and add ours")
    args = parser.parse_args(argv)
    args.repo = args.repo.resolve()
    args.state_dir = args.state_dir.resolve()
    if args.state_dir == args.repo or args.repo in args.state_dir.parents:
        parser.error("--state-dir must be outside the checkout")
    if not 60 <= args.max_seconds <= 17400:
        parser.error("--max-seconds must be between 60 and 17400 (4h50m)")
    if args.preflight and args.install_cron:
        parser.error("run --preflight before --install-cron")
    os.umask(0o077)
    codex = shutil.which(args.codex)
    if not codex:
        print("BLOCKED: codex executable not found", file=sys.stderr)
        return 2
    try:
        with exclusive_lock(args.state_dir) as acquired:
            if not acquired:
                print("SKIP: another research session holds the lock")
                return 0
            if args.install_cron:
                install_cron(args, codex)
                return 0
            state_path = args.state_dir / "state.json"
            previous = json.loads(state_path.read_text()) if state_path.exists() else {}
            now = time.time()
            if not args.preflight and previous.get("next_retry_at", 0) > now:
                print("SKIP: waiting for next bounded retry")
                return 0
            if not args.preflight and previous.get("status") in {"needs_review", "running"}:
                raise Blocked("last session is unfinished or left changes/unpublished commits; check that no agent is still running, preserve and review changes, then remove state.json")
            stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
            events = args.state_dir / f"{stamp}.events.jsonl"
            errors = args.state_dir / f"{stamp}.stderr.log"
            final = args.state_dir / f"{stamp}.final.md"
            if args.preflight:
                preflight(args.repo, args.state_dir, codex)
                print("READY: authenticated read-only Codex inference succeeded")
                return 0
            pending = previous if previous.get("pending_owned_work") else None
            head = refresh_main(args.repo, pending)
            prompt_file = args.repo / PROMPT_PATH
            if not prompt_file.is_file():
                raise Blocked(f"missing current-main research prompt: {PROMPT_PATH}")
            deadline = datetime.fromtimestamp(now + max(1, args.max_seconds - 900), timezone.utc).isoformat()
            origin_head = command(["git", "rev-parse", "origin/main"], args.repo)
            continuation = ("Continue the exact pending work left by the previous interrupted session; the runner checked its HEAD and content fingerprint. "
                            "Preserve those artifacts, read the newly fetched origin/main, and integrate upstream safely before new research or push. "
                            "No other dirty work is authorized.\n\n") if pending else ""
            prompt = (f"This cron invocation fetched latest origin/main {origin_head}; local HEAD is {head}. Finish validation, integration and final report by {deadline} UTC. "
                      "A hard process limit follows 15 minutes later.\n\n" + prompt_file.read_text())
            prompt = continuation + prompt
            save_state(state_path, {"status": "running", "started_at": now, "start_head": head})
            code = run_bounded(codex_args(codex, args.repo, final, preflight=False), prompt, events, errors, args.max_seconds)
            kind = event_failure(events) or ("timeout" if code == 124 else "cli_error" if code else None)
            dirty = bool(command(["git", "status", "--porcelain", "--untracked-files=all"], args.repo))
            unpublished = command(["git", "rev-list", "--count", "origin/main..HEAD"], args.repo) != "0"
            failures = previous.get("failures", 0) + 1 if kind else 0
            # Quota recovery is tested by later cron invocations, never bypassed.
            retry_seconds = min(3600 * 2 ** min(failures - 1, 3), 21600) if kind else 0
            pending_owned = bool(kind and (dirty or unpublished))
            status = kind or ("needs_review" if dirty or unpublished else "complete")
            save_state(state_path, {"status": status, "started_at": now, "finished_at": time.time(),
                                    "start_head": head, "end_head": command(["git", "rev-parse", "HEAD"], args.repo),
                                    "exit_code": code, "failures": failures,
                                    "pending_owned_work": pending_owned,
                                    "checkout_fingerprint": checkout_fingerprint(args.repo) if pending_owned else None,
                                    "next_retry_at": time.time() + retry_seconds,
                                    "events": events.name, "final": final.name})
            print(f"Session finished: {status}; see {state_path}")
            return 0 if status == "complete" else 1
    except (Blocked, subprocess.TimeoutExpired, subprocess.CalledProcessError, OSError, json.JSONDecodeError) as error:
        print(f"BLOCKED: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
