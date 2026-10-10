"""Geometry-check and merge the direct S5 LOSS into a fresh exact cache."""
from __future__ import annotations

import csv
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = Path(__file__).resolve().parents[1]
OUT = EXP / "output"
CACHE = ROOT / "research/experiments/n11-reply27-class-1297036692683751424-16-20261010/output/current-exact-s5-after-followup-loss.cache"
sys.path.insert(0, str(ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts"))
from independent import Board  # noqa: E402
sys.path.insert(0, str(ROOT / "research/experiments/n11-frontier-selection-20261005/scripts"))
from s5_evidence_policy import quarantined_cache_keys  # noqa: E402


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_cache() -> tuple[str, dict[tuple[int, int], int]]:
    header = "# s5 verdict cache: n=11 schema=1 (merged exact evidence; see receipt)"
    result = {}
    for number, line in enumerate(CACHE.read_text(encoding="utf-8").splitlines(), 1):
        if not line:
            continue
        if line.startswith("#"):
            header = line
            continue
        fields = line.split(",")
        if len(fields) != 6 or fields[0] != "s5verdict" or int(fields[3]) != 5:
            raise ValueError(f"malformed S5 cache row {number}: {line}")
        key, verdict = (int(fields[1]), int(fields[2])), int(fields[4])
        if verdict not in (1, 2) or key in result and result[key] != verdict:
            raise ValueError(f"invalid/conflicting cache verdict {key}: {verdict}")
        result[key] = verdict
    return header, result


def main() -> None:
    plan_path = OUT / "probe-plan.json"
    raw_path = OUT / "probe-15m.csv"
    audit_path = OUT / "raw-history-after-15m.json"
    geom_path = OUT / "geometric-cache-preflight.json"
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    audit = json.loads(audit_path.read_text(encoding="utf-8"))
    geometry_preflight = json.loads(geom_path.read_text(encoding="utf-8"))
    target = plan["s5_target"]
    key = tuple(target["key"])
    parent_key = tuple(plan["s4_parent"])
    rows = [row for row in csv.reader(raw_path.open(newline="", encoding="utf-8-sig"))
            if row and row[0] == "replay"]
    if len(rows) != 1 or len(rows[0]) != 11:
        raise SystemExit(f"expected one exact replay row, found {len(rows)}")
    row = rows[0]
    stones, legal, is_or, budget, verdict, nodes = map(int, row[2:8])
    observed_key = (int(row[9]), int(row[10]))
    if (observed_key, stones, legal, is_or, budget, verdict) != (key, 5, target["legal_count"], 0, 15_000_000, 2):
        raise SystemExit(f"raw S5 verdict/geometry fields differ from the plan: {row}")
    if nodes < 0 or nodes > budget:
        raise SystemExit(f"invalid exact node count: {nodes}")
    obs = audit["observations"].get(f"{key[0]},{key[1]}", [])
    if audit["exact_verdict_conflicts"] or not any(item["verdict"] == 2 and item["budget"] == budget for item in obs):
        raise SystemExit("raw history does not independently confirm the exact LOSS without conflict")

    board = Board(11)
    parent = parent_key[0] | (parent_key[1] << 64)
    child = key[0] | (key[1] << 64)
    if board.canonical(parent) != parent or board.canonical(child) != child or child.bit_count() != 5:
        raise SystemExit("parent/child is unsafe or noncanonical")
    if child not in board.children(parent) or board.legal(child).bit_count() != legal:
        raise SystemExit("independent geometry does not verify the S4->S5 edge and legal count")
    full_children = {tuple(item["key"]) for item in geometry_preflight["s5_children"]}
    if key not in full_children or len(full_children) != geometry_preflight["class"]["children"]:
        raise SystemExit("S5 exact is outside the independently regenerated complete parent boundary")

    quarantine = quarantined_cache_keys()
    if key in quarantine:
        raise SystemExit("quarantined exact cache key requires explicit rehabilitation")
    header, exact = read_cache()
    if set(exact) & quarantine:
        raise SystemExit("active quarantined key present in base cache")
    if key in exact:
        raise SystemExit(f"new raw key already exists in base cache: {key}")
    exact[key] = 2

    cache_path = OUT / "current-exact-s5-after-probe.cache"
    with cache_path.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(header + "\n")
        for (lo, hi), value in sorted(exact.items()):
            stream.write(f"s5verdict,{lo},{hi},5,{value},0\n")
    counts = Counter(exact.values())
    receipt = {
        "schema": "n11-reply27-direct-s5-loss-merge-v1",
        "base_cache": {"path": CACHE.relative_to(ROOT).as_posix(), "sha256": sha(CACHE),
                       "rows": len(exact) - 1},
        "plan": {"path": plan_path.relative_to(ROOT).as_posix(), "sha256": sha(plan_path)},
        "raw_history_audit": {"path": audit_path.relative_to(ROOT).as_posix(), "sha256": sha(audit_path),
                              "conflicts": len(audit["exact_verdict_conflicts"])},
        "raw_solver": {"path": raw_path.relative_to(ROOT).as_posix(), "sha256": sha(raw_path),
                       "input_path": plan["target_input"]["path"], "input_sha256": plan["target_input"]["sha256"],
                       "budget": budget, "nodes": nodes, "verdict": "LOSS"},
        "solver": plan["solver"],
        "independent_geometry": {"safe_canonical_s5": True, "legal_s4_parent_edge": True,
                                 "legal_count": legal, "complete_parent_boundary": len(full_children)},
        "quarantine_registry_sha256": sha(ROOT / "results/n11-s5-evidence-quarantine.json"),
        "merged_key": list(key), "merged_verdict": "LOSS", "conflicts": 0,
        "cache": {"path": cache_path.relative_to(ROOT).as_posix(), "sha256": sha(cache_path),
                  "rows": len(exact), "verdict_counts": {str(k): v for k, v in sorted(counts.items())}},
    }
    receipt_path = OUT / "merge-receipt.json"
    receipt_path.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"key": list(key), "verdict": "LOSS", "nodes": nodes, "cache_rows": len(exact),
                      "counts": dict(counts), "cache_sha256": sha(cache_path),
                      "receipt_sha256": sha(receipt_path)}, sort_keys=True))


if __name__ == "__main__":
    main()
