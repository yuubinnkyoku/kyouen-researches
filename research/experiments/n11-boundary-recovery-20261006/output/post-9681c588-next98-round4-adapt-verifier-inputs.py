#!/usr/bin/env python3
"""Bind the exact subset of a probe8 run for the round-4 S5 WIN verifier."""
from __future__ import annotations
import csv, hashlib, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / "research/experiments/n11-boundary-recovery-20261006/output"
PREFIX = "post-9681c588-next98-round4"
def sha(p: Path) -> str: return hashlib.sha256(p.read_bytes()).hexdigest()
def rel(p: Path) -> str: return p.resolve().relative_to(ROOT.resolve()).as_posix()
raw = OUT / f"{PREFIX}-raw-exact.csv"
delta = OUT / f"{PREFIX}-exact-s5.cache"
targets = OUT / f"{PREFIX}-exact-targets.csv"
collected = OUT / f"{PREFIX}-collected-summary.json"
manifest = OUT / f"{PREFIX}-collected-manifest.json"
runner = OUT / f"{PREFIX}-runner-summary.json"
def keys(path: Path, target: bool = False):
    result = {}
    with path.open(newline="", encoding="utf-8-sig") as f:
        for row in csv.reader(f):
            if not row or row[0].lstrip().startswith("#"): continue
            if target:
                assert len(row) == 11 and int(row[2]) == 5
                key = (int(row[3]), int(row[4]))
                assert key not in result
                result[key] = None
            else:
                assert len(row) == 6 and row[0] == "s5verdict" and int(row[3]) == 5
                key, verdict = (int(row[1]), int(row[2])), int(row[4])
                assert verdict in (1, 2) and key not in result
                result[key] = verdict
    return result
raw_rows = {}
with raw.open(newline="", encoding="utf-8-sig") as f:
    for row in csv.reader(f):
        if not row or row[0].lstrip().startswith("#"): continue
        assert len(row) == 11 and row[0] == "replay" and int(row[2]) == 5 and int(row[4]) == 0
        key, verdict = (int(row[9]), int(row[10])), int(row[6])
        assert verdict in (1, 2) and key not in raw_rows
        raw_rows[key] = verdict
delta_rows = keys(delta)
target_rows = keys(targets, target=True)
assert set(raw_rows) == set(delta_rows) == set(target_rows)
assert raw_rows == delta_rows
counts = {"WIN": sum(v == 1 for v in raw_rows.values()), "LOSS": sum(v == 2 for v in raw_rows.values())}
collect = json.loads(collected.read_text(encoding="utf-8"))
run = json.loads(runner.read_text(encoding="utf-8"))
source_manifest = json.loads(manifest.read_text(encoding="utf-8"))
assert collect["exact_rows"] == len(raw_rows) == 7
assert {name: collect["verdict_counts"][name] for name in counts} == counts
assert run["new_win"] == counts["WIN"] == 1 and run["new_loss"] == counts["LOSS"] == 6
assert run["unknown"] == 1 and run["class_status"] == "WIN"
summary = {
    "schema": "n11-round4-exact-subset-verifier-adapter-v1",
    "exact_replay_counts": counts,
    "raw_output": {"path": rel(raw), "sha256": sha(raw)},
    "new_exact_cache": {"path": rel(delta), "sha256": sha(delta)},
    "runner_summary": {"path": rel(runner), "sha256": sha(runner)},
    "collected_summary": {"path": rel(collected), "sha256": sha(collected)},
    "collector_manifest": {"path": rel(manifest), "sha256": sha(manifest)},
}
summary_path = OUT / f"{PREFIX}-verification-summary.json"
summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
target_manifest = {
    "schema": "n11-round4-exact-target-source-binding-v1",
    "inputs": [{"path": rel(targets), "sha256": sha(targets)}],
    "collector_manifest": {"path": rel(manifest), "sha256": sha(manifest)},
    "scheduled_probe": source_manifest.get("source_inputs", []),
}
manifest_path = OUT / f"{PREFIX}-verification-input-manifest.json"
manifest_path.write_text(json.dumps(target_manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
print(f"ROUND4_VERIFIER_INPUTS_OK exact={len(raw_rows)} win={counts['WIN']} loss={counts['LOSS']} unknown_outside_exact={len(collect['unknown_keys'])}")
