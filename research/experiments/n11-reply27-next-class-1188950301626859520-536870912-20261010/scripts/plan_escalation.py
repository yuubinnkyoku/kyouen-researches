"""Revalidate one S5 target before a higher-budget retry."""
from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = Path(__file__).resolve().parents[1]
OUT = EXP / "output"
KEY = (3494793310840553472, 536870912)
NEXT_BUDGET = 15_000_000


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    plan = json.loads((OUT / "probe-plan.json").read_text(encoding="utf-8"))
    raw = json.loads((OUT / "raw-history-before-15m.json").read_text(encoding="utf-8"))
    layer = json.loads((OUT / "saved-s6-s7-before-15m.json").read_text(encoding="utf-8"))
    with (OUT / "probe-2m.csv").open(newline="", encoding="utf-8-sig") as stream:
        row = next(item for item in csv.reader(stream) if item and item[0] == "replay")
    token = f"{KEY[0]},{KEY[1]}"
    observations = raw["observations"].get(token, [])

    assert tuple(plan["s5_target"]["key"]) == KEY
    assert row[0] == "replay" and int(row[3]) == 88 and int(row[5]) == 2_000_000
    assert int(row[6]) == 0 and int(row[7]) == 2_000_000
    assert raw["dispatch_ready_keys"] == [list(KEY)]
    assert raw["exact_verdict_conflicts"] == []
    assert not any(item["verdict"] in (1, 2) for item in observations)
    assert not any(item["verdict"] == 0 and item["budget"] >= NEXT_BUDGET for item in observations)
    assert token not in layer["s5_results_from_raw_s6_s7_only"]
    assert token not in layer["s5_results_with_saved_cache_s6_s7"]
    assert not layer["saved_cache_s7"]["target_intersections"]

    inputs = [OUT / "probe-2m.csv", OUT / "raw-history-before-15m.json",
              OUT / "saved-s6-s7-before-15m.json"]
    result = {
        "schema": "n11-reply27-s5-single-escalation-plan-v1",
        "main_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "s4_parent": [1188950301626859520, 536870912],
        "s5_target": {"key": list(KEY), "legal_count": 88, "previous_budget": 2_000_000,
                      "previous_result": "UNKNOWN", "previous_nodes": 2_000_000,
                      "next_budget": NEXT_BUDGET, "workers": 1, "watchdog_seconds": 180},
        "fresh_evidence": [{"path": path.relative_to(ROOT).as_posix(), "sha256": sha(path)} for path in inputs],
        "raw_history": {"prior_exact": 0, "unknown_below_budget": 1,
                         "same_or_higher_15m_unknown": 0, "verdict_conflicts": 0,
                         "dispatch_ready": True},
        "saved_layers": {"s6_boundary_keys": layer["s6_boundary"]["distinct_canonical_keys"],
                         "raw_s6_exact": len(layer["raw_s6"]["exact_keys"]),
                         "cache_s6_exact": len(layer["saved_cache_s6"]["exact_keys"]),
                         "raw_s7_exact": len(layer["raw_s7"]["exact_keys"]),
                         "s7_cache_intersection": 0, "s5_derived_result": False},
        "solver": plan["solver"],
    }
    path = OUT / "escalation-plan.json"
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"target": list(KEY), "budget": NEXT_BUDGET, "plan_sha256": sha(path)}, sort_keys=True))


if __name__ == "__main__":
    main()
