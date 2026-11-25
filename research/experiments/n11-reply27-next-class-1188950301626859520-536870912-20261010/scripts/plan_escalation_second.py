"""Pin a 15M retry after the second target's fresh raw/layer audit."""
from __future__ import annotations

import csv
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = Path(__file__).resolve().parents[1]
OUT = EXP / "output"
def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--key", type=int, nargs=2, default=[1188950301626859520, 536936448])
    parser.add_argument("--probe", type=Path, default=OUT / "probe-2m-second.csv")
    parser.add_argument("--raw-audit", type=Path, default=OUT / "raw-history-before-15m-second.json")
    parser.add_argument("--layer-audit", type=Path, default=OUT / "saved-s6-s7-before-15m-second.json")
    parser.add_argument("--dispatch-plan", type=Path, default=OUT / "probe-2-plan.json")
    parser.add_argument("--output-name", default="escalation-plan-second.json")
    args = parser.parse_args()
    key = tuple(args.key)
    resolve = lambda path: path if path.is_absolute() else ROOT / path
    probe_path, raw_path, layer_path, dispatch_plan_path = map(
        resolve, (args.probe, args.raw_audit, args.layer_audit, args.dispatch_plan)
    )
    raw = json.loads(raw_path.read_text(encoding="utf-8"))
    layer = json.loads(layer_path.read_text(encoding="utf-8"))
    previous_plan = json.loads(dispatch_plan_path.read_text(encoding="utf-8"))
    with probe_path.open(newline="", encoding="utf-8-sig") as stream:
        row = next(item for item in csv.reader(stream) if item and item[0] == "replay")
    token = f"{key[0]},{key[1]}"
    observations = raw["observations"].get(token, [])
    assert tuple(previous_plan["s5_target"]["key"]) == key
    assert int(row[3]) == previous_plan["s5_target"]["legal_count"]
    if (tuple(map(int, (row[2], row[3], row[5], row[6], row[7], row[9], row[10])))
            != (5, int(row[3]), 2_000_000, 0, 2_000_000, *key)):
        raise SystemExit(f"unexpected prior probe row: {row}")
    assert raw["dispatch_ready_keys"] == [list(key)]
    assert not raw["exact_verdict_conflicts"]
    assert not any(item["verdict"] in (1, 2) for item in observations)
    assert not any(item["verdict"] == 0 and item["budget"] >= 15_000_000 for item in observations)
    assert token not in layer["s5_results_from_raw_s6_s7_only"]
    assert token not in layer["s5_results_with_saved_cache_s6_s7"]
    assert not layer["saved_cache_s7"]["target_intersections"]

    paths = [probe_path, raw_path, layer_path]
    result = {
        "schema": "n11-reply27-s5-single-escalation-plan-v1",
        "main_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "s4_parent": [1188950301626859520, 536870912],
        "s5_target": {"key": list(key), "legal_count": int(row[3]), "previous_budget": 2_000_000,
                      "previous_result": "UNKNOWN", "previous_nodes": 2_000_000,
                      "next_budget": 15_000_000, "workers": 1, "watchdog_seconds": 180},
        "fresh_evidence": [{"path": path.relative_to(ROOT).as_posix(), "sha256": sha(path)} for path in paths],
        "raw_history": {"prior_exact": 0, "same_or_higher_15m_unknown": 0,
                         "verdict_conflicts": 0, "dispatch_ready": True},
        "saved_layers": {"s6_boundary_keys": layer["s6_boundary"]["distinct_canonical_keys"],
                         "raw_s6_exact": len(layer["raw_s6"]["exact_keys"]),
                         "cache_s6_exact": len(layer["saved_cache_s6"]["exact_keys"]),
                         "raw_s7_exact": len(layer["raw_s7"]["exact_keys"]),
                         "s7_cache_intersection": 0, "s5_derived_result": False},
        "solver": previous_plan["solver"],
    }
    path = OUT / args.output_name
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"target": list(key), "budget": 15_000_000, "plan_sha256": sha(path)}, sort_keys=True))


if __name__ == "__main__":
    main()
