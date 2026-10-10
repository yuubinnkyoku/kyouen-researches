"""Geometry-check and merge the second direct S5 LOSS."""
from __future__ import annotations

import csv
import argparse
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = Path(__file__).resolve().parents[1]
OUT = EXP / "output"
sys.path.insert(0, str(ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts"))
from independent import Board  # noqa: E402
sys.path.insert(0, str(ROOT / "research/experiments/n11-frontier-selection-20261005/scripts"))
from s5_evidence_policy import quarantined_cache_keys  # noqa: E402


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", type=Path, default=OUT / "probe-2-plan.json")
    parser.add_argument("--raw", type=Path, default=OUT / "probe-15m-second.csv")
    parser.add_argument("--audit", type=Path, default=OUT / "raw-history-after-second-15m.json")
    parser.add_argument("--preflight", type=Path, default=OUT / "geometric-cache-preflight.json")
    parser.add_argument("--base-cache", type=Path, default=OUT / "current-exact-s5-after-probe.cache")
    parser.add_argument("--output-cache", default="current-exact-s5-after-probe-2.cache")
    parser.add_argument("--receipt", default="merge-receipt-second.json")
    args = parser.parse_args()
    resolve = lambda path: path if path.is_absolute() else ROOT / path
    plan_path, raw_path, audit_path, preflight_path, cache_path = map(
        resolve, (args.plan, args.raw, args.audit, args.preflight, args.base_cache)
    )
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    audit = json.loads(audit_path.read_text(encoding="utf-8"))
    preflight = json.loads(preflight_path.read_text(encoding="utf-8"))
    target = plan["s5_target"]
    key = tuple(target["key"])
    parent_key = tuple(plan["s4_parent"])
    rows = [row for row in csv.reader(raw_path.open(newline="", encoding="utf-8-sig"))
            if row and row[0] == "replay"]
    if len(rows) != 1 or len(rows[0]) != 11:
        raise SystemExit(f"expected one raw exact replay, found {len(rows)}")
    row = rows[0]
    stones, legal, is_or, budget, verdict, nodes = map(int, row[2:8])
    observed_key = (int(row[9]), int(row[10]))
    if (observed_key, stones, legal, is_or, budget, verdict) != (key, 5, target["legal_count"], 0, 15_000_000, 2):
        raise SystemExit(f"raw S5 verdict/geometry fields differ from its plan: {row}")
    if nodes < 0 or nodes > budget:
        raise SystemExit(f"invalid node count: {nodes}")
    observations = audit["observations"].get(f"{key[0]},{key[1]}", [])
    if audit["exact_verdict_conflicts"] or not any(item["budget"] == budget and item["verdict"] == 2
                                                    for item in observations):
        raise SystemExit("full raw-history audit does not confirm this direct LOSS")

    board = Board(11)
    parent = parent_key[0] | (parent_key[1] << 64)
    child = key[0] | (key[1] << 64)
    if board.canonical(parent) != parent or board.canonical(child) != child or child.bit_count() != 5:
        raise SystemExit("S4/S5 key is unsafe or noncanonical")
    if child not in board.children(parent) or board.legal(child).bit_count() != legal:
        raise SystemExit("independent geometry disagrees with the raw S5 child")
    complete_children = {tuple(item["key"]) for item in preflight["s5_children"]}
    if key not in complete_children or len(complete_children) != preflight["class"]["children"]:
        raise SystemExit("S5 position is outside the complete regenerated S4 boundary")

    quarantine = quarantined_cache_keys()
    if key in quarantine:
        raise SystemExit("active quarantine requires explicit rehabilitation")
    header = "# s5 verdict cache: n=11 schema=1 (merged exact evidence; see receipt)"
    exact = {}
    for number, line in enumerate(cache_path.read_text(encoding="utf-8").splitlines(), 1):
        if not line:
            continue
        if line.startswith("#"):
            header = line
            continue
        fields = line.split(",")
        if len(fields) != 6 or fields[0] != "s5verdict" or int(fields[3]) != 5:
            raise ValueError(f"malformed cache row {number}: {line}")
        cache_key, value = (int(fields[1]), int(fields[2])), int(fields[4])
        if value not in (1, 2) or cache_key in exact and exact[cache_key] != value:
            raise ValueError(f"invalid/conflicting cache row {number}: {line}")
        exact[cache_key] = value
    if set(exact) & quarantine:
        raise SystemExit("active quarantined cache key present in base")
    if key in exact:
        raise SystemExit(f"duplicate or conflicting exact cache key: {key}")
    exact[key] = 2

    output_cache = OUT / args.output_cache
    with output_cache.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(header + "\n")
        for (lo, hi), value in sorted(exact.items()):
            stream.write(f"s5verdict,{lo},{hi},5,{value},0\n")
    counts = Counter(exact.values())
    receipt = {
        "schema": "n11-reply27-direct-s5-loss-merge-v1",
        "base_cache": {"path": cache_path.relative_to(ROOT).as_posix(), "sha256": sha(cache_path), "rows": len(exact) - 1},
        "plan": {"path": plan_path.relative_to(ROOT).as_posix(), "sha256": sha(plan_path)},
        "raw_history_audit": {"path": audit_path.relative_to(ROOT).as_posix(),
                              "sha256": sha(audit_path), "conflicts": len(audit["exact_verdict_conflicts"])},
        "raw_solver": {"path": raw_path.relative_to(ROOT).as_posix(), "sha256": sha(raw_path),
                       "input_path": plan["preflight_sources"][2]["path"],
                       "input_sha256": plan["preflight_sources"][2]["sha256"],
                       "budget": budget, "nodes": nodes, "verdict": "LOSS"},
        "solver": plan["solver"],
        "independent_geometry": {"safe_canonical_s5": True, "legal_s4_parent_edge": True,
                                 "legal_count": legal, "complete_parent_boundary": len(complete_children)},
        "quarantine_registry_sha256": sha(ROOT / "results/n11-s5-evidence-quarantine.json"),
        "merged_key": list(key), "merged_verdict": "LOSS", "conflicts": 0,
        "cache": {"path": output_cache.relative_to(ROOT).as_posix(), "sha256": sha(output_cache),
                  "rows": len(exact), "verdict_counts": {str(k): v for k, v in sorted(counts.items())}},
    }
    receipt_path = OUT / args.receipt
    receipt_path.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"key": list(key), "verdict": "LOSS", "nodes": nodes,
                      "cache_rows": len(exact), "counts": dict(counts),
                      "cache_sha256": sha(output_cache), "receipt_sha256": sha(receipt_path)}, sort_keys=True))


if __name__ == "__main__":
    main()
