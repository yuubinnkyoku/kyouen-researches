#!/usr/bin/env python3
"""Scheduler regression tests use local bare Git and fake CLI, never real inference."""

from __future__ import annotations

from contextlib import redirect_stdout
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


spec = importlib.util.spec_from_file_location("research_frontier_cron", Path(__file__).with_name("research_frontier_cron.py"))
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)


class SchedulerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def git(self, repo, *args):
        result = subprocess.run(["git", "-C", str(repo), *args], text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout.strip()

    def make_repository(self):
        bare = self.root / "origin.git"
        self.assertEqual(subprocess.run(["git", "init", "--bare", "--initial-branch=main", str(bare)], capture_output=True).returncode, 0)
        repo = self.root / "repo"
        repo.mkdir()
        self.git(repo, "init", "--initial-branch=main")
        self.git(repo, "config", "user.name", "Scheduler Regression")
        self.git(repo, "config", "user.email", "scheduler@example.invalid")
        (repo / "docs").mkdir()
        (repo / runner.PROMPT_PATH).write_text("Research prompt for isolated test.\n")
        self.git(repo, "add", "docs")
        self.git(repo, "commit", "-m", "initial")
        self.git(repo, "remote", "add", "origin", runner.EXPECTED_REMOTE)
        # Exact local rewrite means no test reaches the real GitHub repository.
        self.git(repo, "config", f"url.{bare.as_uri()}.insteadOf", runner.EXPECTED_REMOTE)
        self.git(repo, "push", "-u", "origin", "main")
        return repo, bare

    def make_codex(self, body):
        path = self.root / "fake-codex"
        path.write_text("#!" + sys.executable + "\n" + body)
        path.chmod(0o700)
        return path

    def test_refresh_obtains_latest_main(self):
        repo, bare = self.make_repository()
        upstream = self.root / "upstream"
        self.assertEqual(subprocess.run(["git", "clone", str(bare), str(upstream)], capture_output=True).returncode, 0)
        self.git(upstream, "config", "user.name", "Upstream")
        self.git(upstream, "config", "user.email", "upstream@example.invalid")
        (upstream / "new-evidence.txt").write_text("upstream evidence\n")
        self.git(upstream, "add", "new-evidence.txt")
        self.git(upstream, "commit", "-m", "upstream evidence")
        self.git(upstream, "push", "origin", "main")
        self.assertEqual(runner.refresh_main(repo), self.git(upstream, "rev-parse", "HEAD"))
        self.assertEqual((repo / "new-evidence.txt").read_text(), "upstream evidence\n")

    def test_dirty_checkout_preserved_before_fetch(self):
        repo, _ = self.make_repository()
        evidence = repo / "unfinished.txt"
        evidence.write_text("keep this user evidence\n")
        with self.assertRaisesRegex(runner.Blocked, "checkout has changes"):
            runner.refresh_main(repo)
        self.assertEqual(evidence.read_text(), "keep this user evidence\n")

    def test_unpublished_commits_preserved(self):
        repo, _ = self.make_repository()
        (repo / "new.txt").write_text("not reviewed\n")
        self.git(repo, "add", "new.txt")
        self.git(repo, "commit", "-m", "not reviewed")
        head = self.git(repo, "rev-parse", "HEAD")
        with self.assertRaisesRegex(runner.Blocked, "unpublished commits"):
            runner.refresh_main(repo)
        self.assertEqual(head, self.git(repo, "rev-parse", "HEAD"))

    def test_single_session_lock(self):
        with runner.exclusive_lock(self.root / "state") as first:
            with runner.exclusive_lock(self.root / "state") as second:
                self.assertTrue(first)
                self.assertFalse(second)
        with runner.exclusive_lock(self.root / "state") as later:
            self.assertTrue(later)

    def test_quota_events_and_normal_discussion(self):
        events = self.root / "events.jsonl"
        for event in (
            {"type": "turn.failed", "error": {"code": "usage_limit_reached"}},
            {"type": "error", "message": "You have hit your usage limit"},
        ):
            events.write_text(json.dumps(event) + "\n")
            self.assertEqual(runner.event_failure(events), "quota")
        events.write_text(json.dumps({"type": "item.completed", "text": "quota exceeded was last week's hypothesis"}) + "\n[]\nnot json\n")
        self.assertIsNone(runner.event_failure(events))

    def test_quota_recovery_is_scheduled_without_busy_retry(self):
        repo, _ = self.make_repository()
        codex = self.make_codex("import json, sys\nsys.stdin.read()\nprint(json.dumps({'type':'turn.failed','error':{'code':'usage_limit_reached'}}))\n")
        state_dir = self.root / "state"
        args = ["--repo", str(repo), "--state-dir", str(state_dir), "--codex", str(codex), "--max-seconds", "60"]
        with redirect_stdout(io.StringIO()):
            self.assertEqual(runner.main(args), 1)
        state = json.loads((state_dir / "state.json").read_text())
        self.assertEqual(state["status"], "quota")
        self.assertGreater(state["next_retry_at"], state["finished_at"] + 3500)
        with redirect_stdout(io.StringIO()) as output:
            self.assertEqual(runner.main(args), 0)
        self.assertIn("waiting for next bounded retry", output.getvalue())
        # A later cron can retry after recovery: no saved session continuity is required.
        state["next_retry_at"] = 0
        runner.save_state(state_dir / "state.json", state)
        codex.write_text("#!" + sys.executable + "\nimport sys\nsys.stdin.read()\nprint('{\"type\":\"turn.completed\"}')\n")
        with redirect_stdout(io.StringIO()):
            self.assertEqual(runner.main(args), 0)
        self.assertEqual(json.loads((state_dir / "state.json").read_text())["status"], "complete")

    def test_unfinished_session_never_restarts_an_agent(self):
        repo, _ = self.make_repository()
        codex = self.make_codex("raise RuntimeError('must not be invoked')\n")
        state_dir = self.root / "state"
        state_dir.mkdir()
        runner.save_state(state_dir / "state.json", {"status": "running"})
        with patch.object(runner, "run_bounded") as invoke, patch("sys.stderr", io.StringIO()):
            self.assertEqual(runner.main(["--repo", str(repo), "--state-dir", str(state_dir), "--codex", str(codex)]), 2)
        invoke.assert_not_called()

    def test_owned_dirty_work_resumes_after_quota_and_rejects_other_edits(self):
        repo, _ = self.make_repository()
        codex = self.make_codex("import pathlib, sys\nrepo=pathlib.Path(sys.argv[sys.argv.index('-C')+1])\nsys.stdin.read()\n(repo/'pending.txt').write_text('first-session evidence\\n')\nprint('{\"type\":\"turn.failed\",\"error\":{\"code\":\"usage_limit_reached\"}}')\n")
        state_dir = self.root / "state"
        args = ["--repo", str(repo), "--state-dir", str(state_dir), "--codex", str(codex)]
        with redirect_stdout(io.StringIO()):
            self.assertEqual(runner.main(args), 1)
        state = json.loads((state_dir / "state.json").read_text())
        self.assertTrue(state["pending_owned_work"])
        self.assertEqual(runner.refresh_main(repo, state), state["end_head"])
        (repo / "pending.txt").write_text("user changed this after the interrupted session\n")
        with self.assertRaisesRegex(runner.Blocked, "pending work changed"):
            runner.refresh_main(repo, state)
        self.assertEqual((repo / "pending.txt").read_text(), "user changed this after the interrupted session\n")

    def test_owned_unpublished_commit_is_not_reset(self):
        repo, _ = self.make_repository()
        (repo / "pending.txt").write_text("own result\n")
        self.git(repo, "add", "pending.txt")
        self.git(repo, "commit", "-m", "pending own result")
        head = self.git(repo, "rev-parse", "HEAD")
        pending = {"end_head": head, "checkout_fingerprint": runner.checkout_fingerprint(repo)}
        self.assertEqual(runner.refresh_main(repo, pending), head)
        self.assertEqual(self.git(repo, "rev-parse", "HEAD"), head)

    def test_fingerprint_does_not_read_symlink_target(self):
        repo, _ = self.make_repository()
        target = self.root / "private-outside.txt"
        target.write_text("private material one\n")
        (repo / "untracked-link").symlink_to(target)
        before = runner.checkout_fingerprint(repo)
        target.write_text("private material two\n")
        self.assertEqual(before, runner.checkout_fingerprint(repo))

    def test_crontab_preserves_unrelated_entries_and_is_idempotent(self):
        existing = "# personal jobs\n1 2 * * * /home/user/backup\n"
        first = runner.cron_text(existing, "17 * * * * python runner")
        updated = runner.cron_text(first, "17 * * * * python newer-runner")
        self.assertTrue(updated.startswith(existing))
        self.assertEqual(updated.count(runner.MARKER_START), 1)
        self.assertNotIn("python runner\n", updated)
        self.assertEqual(updated, runner.cron_text(updated, "17 * * * * python newer-runner"))
        with self.assertRaises(runner.Blocked):
            runner.cron_text(runner.MARKER_START + "\n", "new command")

    def test_timeout_terminates_process(self):
        events, errors = self.root / "events", self.root / "errors"
        self.assertEqual(runner.run_bounded([sys.executable, "-c", "import time; time.sleep(60)"], "", events, errors, 0.05), 124)

    def test_installer_runs_preflight_and_preserves_crontab(self):
        repo, _ = self.make_repository()
        codex = self.make_codex("import sys\nprint('logged in' if sys.argv[1:3]==['login','status'] else 'READY')\n")
        cron_file = self.root / "saved-crontab"
        cron_file.write_text("# unrelated job\n1 2 * * * /srv/backup\n")
        crontab = self.root / "fake-crontab"
        crontab.write_text("#!" + sys.executable + "\nimport pathlib, sys\np=pathlib.Path(" + repr(str(cron_file)) + ")\nif sys.argv[1]=='-l':\n print(p.read_text(),end='')\nelse:\n p.write_text(sys.stdin.read())\n")
        crontab.chmod(0o700)
        original_which = runner.shutil.which
        def which(name):
            return str(crontab) if name == "crontab" else original_which(name)
        with patch.object(runner.shutil, "which", side_effect=which), redirect_stdout(io.StringIO()):
            self.assertEqual(runner.main(["--repo", str(repo), "--state-dir", str(self.root / "state"),
                                          "--codex", str(codex), "--install-cron"]), 0)
        text = cron_file.read_text()
        self.assertTrue(text.startswith("# unrelated job\n1 2 * * * /srv/backup\n"))
        self.assertIn("17 * * * *", text)
        self.assertEqual(text.count(runner.MARKER_START), 1)
        # A failed real-inference preflight must leave the existing crontab byte-for-byte.
        codex.write_text("#!" + sys.executable + "\nimport sys\nprint('logged in' if sys.argv[1:3]==['login','status'] else 'NOT_READY')\n")
        with patch.object(runner.shutil, "which", side_effect=which), patch("sys.stderr", io.StringIO()):
            self.assertEqual(runner.main(["--repo", str(repo), "--state-dir", str(self.root / "state"),
                                          "--codex", str(codex), "--install-cron"]), 2)
        self.assertEqual(text, cron_file.read_text())

    def test_codex_uses_auto_review_and_keeps_sandbox(self):
        args = runner.codex_args("codex", self.root, self.root / "final.md", preflight=False)
        self.assertIn("--approve-for-me", args)
        self.assertNotIn("--dangerously-bypass-approvals-and-sandbox", args)
        self.assertNotIn("danger-full-access", args)


if __name__ == "__main__":
    unittest.main()
