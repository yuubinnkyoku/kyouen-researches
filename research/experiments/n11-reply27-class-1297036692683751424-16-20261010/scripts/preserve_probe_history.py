"""Preserve the two exact replay history snapshots without modifying sources."""
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = Path(__file__).resolve().parents[1]
HISTORY_REL = "research/experiments/n11-strategy-redesign-20261010/output/history.json"
BASE_COMMIT = "154f3b7a67b97e13acbaee8b04dc74ddca728d19"
EXPECTED_BASE = "1ed1f0f4d94417ab1b81ec6ddbe81cbeaef0596a0b62db9929a7f3f794d58791"
EXPECTED_LATER = "212ce320b141ad2a322b13f788a0d60ba31d594860768b5de7d578883bb9bd3e"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def preserve(path: Path, data: bytes, expected_sha: str) -> dict:
    if digest(data) != expected_sha:
        raise SystemExit(f"source hash mismatch for {path}: {digest(data)} != {expected_sha}")
    if path.exists():
        if path.read_bytes() != data:
            raise SystemExit(f"refusing to overwrite different snapshot: {path}")
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("xb") as stream:
            stream.write(data)
    return {"path": path.resolve().relative_to(ROOT.resolve()).as_posix(),
            "sha256": digest(path.read_bytes()), "bytes": path.stat().st_size}


def main() -> None:
    baseline = subprocess.check_output(["git", "show", f"{BASE_COMMIT}:{HISTORY_REL}"], cwd=ROOT)
    current_path = ROOT / HISTORY_REL
    current = current_path.read_bytes()
    baseline_copy = preserve(EXP / "input/probe-history-at-start-main.json", baseline, EXPECTED_BASE)
    later_copy = preserve(EXP / "input/probe-history-before-candidate-probes.json", current, EXPECTED_LATER)
    result = {
        "schema": "n11-reply27-probe-history-snapshot-manifest-v1",
        "original_path": HISTORY_REL,
        "original_workspace_file_preserved_unmodified": True,
        "snapshots": [
            {"used_by": ["s5-probe2m", "s5-probe15m-first"],
             "source": f"git:{BASE_COMMIT}:{HISTORY_REL}", "copy": baseline_copy},
            {"used_by": ["candidate-s5-probe2m", "candidate-s5-probe15m", "followup-s5-probe2m", "followup-s5-probe15m"],
             "source": "workspace file copied byte-for-byte; the workspace file was not edited by this task",
             "workspace_source_sha256": digest(current), "copy": later_copy},
        ],
    }
    out = EXP / "output/probe-history-snapshots.json"
    encoded = (json.dumps(result, indent=2, sort_keys=True) + "\n").encode("utf-8")
    if out.exists() and out.read_bytes() != encoded:
        raise SystemExit(f"refusing to overwrite different snapshot manifest: {out}")
    if not out.exists():
        out.write_bytes(encoded)
    print(json.dumps({"snapshots": [baseline_copy, later_copy],
                      "manifest_sha256": digest(out.read_bytes())}, sort_keys=True))


if __name__ == "__main__":
    main()
