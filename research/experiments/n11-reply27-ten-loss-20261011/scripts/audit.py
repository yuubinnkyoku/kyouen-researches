#!/usr/bin/env python3
"""Independent geometry, raw replay and exact-cache audit for 10 S5 LOSS."""
from __future__ import annotations

import argparse
import ast
import collections
import csv
import gzip
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EX = ROOT / "research/experiments/n11-reply27-ten-loss-20261011"
RAW = EX / "output/raw"
BASE = ROOT / "research/experiments/n11-reply27-next-candidate-20261011/output/merged-exact-s5.cache"
GEOM = ROOT / "research/experiments/n11-strategy-redesign-20261010/output/geometry.json.gz"
TARGET = (1297036692683752448, 0)
INITIAL_FILES = ["group1-2m.csv", "group2-2m.csv"]
FINAL_FILES = [
    "group1a-15m.csv", "group1b-15m.csv", "single91-15m.csv", "single92-15m.csv",
    "group2a-15m.csv", "group2b-15m.csv",
]
sys.path.insert(0, str(ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts"))
sys.path.insert(0, str(ROOT / "research/experiments/n11-frontier-selection-20261005/scripts"))
from independent import Board
from s5_evidence_policy import quarantined_cache_keys

def asmask(k):
    return k[0] | (k[1] << 64)

def askey(m):
    return (m & ((1 << 64) - 1), m >> 64)

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def rows_of(path):
    with path.open(encoding="utf-8-sig", newline="") as f:
        return [row for row in csv.reader(f) if row and not row[0].startswith("#")]

def load_cache(path):
    quarantine = quarantined_cache_keys()
    vals = {}
    for row in rows_of(path):
        assert len(row) == 6 and row[0] == "s5verdict", row
        k = int(row[1]), int(row[2])
        value = int(row[4])
        assert int(row[3]) == 5 and value in (1, 2) and int(row[5]) >= 0
        assert k not in quarantine, ("quarantined cache key", k)
        assert k not in vals or vals[k] == value, ("duplicate conflict", k)
        vals[k] = value
    return vals

def class_status(children, verdicts):
    seen = [verdicts.get(tuple(k), 0) for k in children]
    if 1 in seen:
        return "WIN"
    if all(v == 2 for v in seen):
        return "LOSS"
    return "UNKNOWN"

def check_replay(path, expected, limit):
    rows = [row for row in rows_of(path) if row[0] == "replay"]
    assert rows, ("empty replay", path)
    seen = {}
    for row in rows:
        assert len(row) == 11, row
        seq, stones, legal, isor, budget, verdict, nodes, secs, lo, hi = map(int, row[1:])
        k = (lo, hi)
        assert k in expected and k not in seen, ("missing/unexpected/duplicate root", k)
        assert stones == 5 and isor == 0 and budget == limit, (path, row)
        assert legal == expected[k]["legal"], ("wrong legal count", path, row)
        assert 0 < nodes <= budget and secs >= 0
        if limit == 2_000_000:
            assert verdict == 0 and nodes == budget, row
        elif limit == 15_000_000:
            assert verdict == 2, row
        else:
            raise AssertionError("unexpected budget")
        seen[k] = {"nodes": nodes, "verdict": verdict, "legal": legal,
                   "source": path.relative_to(ROOT).as_posix()}
    return seen

def main():
    board = Board(11)
    known = {}
    for j in (1, 2):
        path = RAW / f"input-group{j}.csv"
        lines = rows_of(path)
        assert len(lines) == 5
        for row in lines:
            assert len(row) == 11 and row[0] == "target" and int(row[2]) == 5
            assert int(row[7]) == 0 and all(int(x) == 0 for x in row[8:])
            k = int(row[3]), int(row[4])
            legal = int(row[5])
            assert k not in known and asmask(k).bit_count() == 5, k
            assert board.canonical(asmask(k)) == asmask(k), k
            assert board.legal(asmask(k)).bit_count() == legal, (k, legal)
            known[k] = {"legal": legal, "initial_input": path.relative_to(ROOT).as_posix()}
    assert len(known) == 10

    small = {}
    for f in INITIAL_FILES:
        data = check_replay(RAW / f, known, 2_000_000)
        assert len(data) == 5
        for k, v in data.items():
            assert k not in small
            small[k] = v
    assert set(small) == set(known)

    # The 3-row group1b subprocess exceeded the external 60-second limit
    # after completing one exact row. Retain the raw partial file; no missing
    # or cutoff position is promoted. The other two were rerun individually.
    exact = {}
    expected_splits = {
        "group1a-15m.csv": 2,
        "group1b-15m.csv": 1,
        "single91-15m.csv": 1,
        "single92-15m.csv": 1,
        "group2a-15m.csv": 2,
        "group2b-15m.csv": 3,
    }
    for name in FINAL_FILES:
        data = check_replay(RAW / name, known, 15_000_000)
        assert len(data) == expected_splits[name], (name, len(data))
        for k, v in data.items():
            assert k not in exact, ("duplicated decisive row", k)
            exact[k] = v
    assert set(exact) == set(known), ("not every key exact", set(known) - set(exact))
    for k in known:
        assert small[k]["verdict"] == 0 and exact[k]["verdict"] == 2
    total_nodes = sum(x["nodes"] for x in small.values()) + sum(x["nodes"] for x in exact.values())
    exact_nodes = sum(x["nodes"] for x in exact.values())

    with gzip.open(GEOM, "rt", encoding="utf-8") as f:
        geom = json.load(f)
    assert len(geom) == 3384
    parents = {tuple(item["key"]): item for item in geom}
    target = parents[TARGET]
    assert len(target["children"]) == 106
    assert target["coverage"] == [100, 108, 110, 120]
    children = set(map(tuple, target["children"]))
    assert set(known) <= children
    incidence = {key: [] for key in known}
    for p, g in parents.items():
        for key in set(map(tuple, g["children"])) & set(known):
            assert asmask(key) in board.children(asmask(p)), ("illegal S4/S5 relation", p, key)
            incidence[key].append(list(p))
    for key, ps in incidence.items():
        assert ps, key

    before = load_cache(BASE)
    assert len(before) == 5755 and sum(v == 1 for v in before.values()) == 159
    assert all(k not in before for k in known), "exact cache already includes selected root"
    after = dict(before)
    after.update({key: 2 for key in known})
    assert len(after) == 5765
    old_status = collections.Counter(class_status(g["children"], before) for g in geom)
    new_status = collections.Counter(class_status(g["children"], after) for g in geom)
    target_before = collections.Counter({v: sum(before.get(k, 0) == v for k in children) for v in (0, 1, 2)})
    target_after = {v: sum(after.get(k, 0) == v for k in children) for v in (0, 1, 2)}
    assert target_before[2] == 10 and target_before[0] == 96 and target_before[1] == 0
    assert target_after == {0: 86, 1: 0, 2: 20}, target_after
    assert new_status["LOSS"] == old_status["LOSS"] == 31
    assert new_status["WIN"] == old_status["WIN"] == 274
    assert new_status["UNKNOWN"] == old_status["UNKNOWN"] == 3079
    secured = set()
    for item in geom:
        if class_status(item["children"], after) == "LOSS":
            secured.update(item["coverage"])
    remaining = sorted(set(range(121)) - {60, 27} - secured)
    assert len(secured) == 117 and remaining == [100, 108]

    outcache = EX / "output/merged-exact-s5.cache"
    with outcache.open("w", encoding="utf-8", newline="") as f:
        f.write("# n11 S5 direct solver-trusted exact, 10 new raw LOSS, independent geometry audit\n")
        for k, v in sorted(after.items()):
            f.write(f"s5verdict,{k[0]},{k[1]},5,{v},0\n")
    report = {
        "version": "n11-reply27-ten-loss-v1",
        "baseline_main_sha": "3db4b36cd647bf895c96f4484e0884d20b29e5d3",
        "solver_build_commit": "f33693cdd8be54738cedea8fc141553209c9a669",
        "solver_binary_sha256": "2878dc74ab1228c1bba6b13140dcd8f65f457f9813ae98d801a1709c77497ee5",
        "solver_command": "--n=11 --memo=22 --only=5 --exact-order=count --exact-replay-budget=2000000/15000000; cold per target",
        "independent_board_sha256": sha(ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts/independent.py"),
        "geometry_sha256": sha(GEOM),
        "baseline_cache_sha256": sha(BASE),
        "raw_sha256": {str(p.relative_to(ROOT)): sha(p) for p in sorted(RAW.iterdir()) if p.is_file()},
        "probe_count": len(known),
        "probe_initial_2m_unknown": 10,
        "probe_15m_exact_loss": 10,
        "probe_15m_win": 0,
        "run_15m_partial": {"file": "group1b-15m.csv", "completed_rows": 1, "incomplete_last_two": "not used; single91/single92 rerun separately"},
        "total_nodes_excluding_unreported_interrupted_work": total_nodes,
        "decisive_replay_nodes": exact_nodes,
        "results": [{"key": list(k), "legal": known[k]["legal"],
                     "parents": incidence[k], "pilot": small[k], "exact": exact[k]} for k in sorted(known)],
        "before_cache_rows": len(before),
        "after_cache_rows": len(after),
        "after_cache_win": sum(v == 1 for v in after.values()),
        "after_cache_loss": sum(v == 2 for v in after.values()),
        "cache_conflicts": 0,
        "target": {"key": list(TARGET), "coverage": target["coverage"], "s5_complete_children": 106,
                   "before_loss": 10, "before_unknown": 96, "after_loss": 20, "after_unknown": 86, "after_win": 0,
                   "status": class_status(target["children"], after)},
        "s4_before": dict(old_status), "s4_after": dict(new_status),
        "third_moves_secured": len(secured),
        "third_moves_remaining": remaining,
        "minimal_additional_loss_classes": 1,
        "independent_terminal_only_certificates_for_new_s5": 0,
        "verdict_trust": "exact solver raw verdicts; independent canonical/legal/transition/cache checks, not terminal-only minimax",
        "merged_cache_sha256": sha(outcache),
    }
    (EX / "output/audit.json").write_text(json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2) + "\n")
    print(json.dumps({"exact_loss": len(known), "decisive_nodes": exact_nodes,
                      "reported_total_nodes": total_nodes, "target": report["target"],
                      "cache": [len(after), report["after_cache_win"], report["after_cache_loss"]],
                      "s4": dict(new_status)}, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
