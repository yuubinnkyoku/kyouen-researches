"""Create a single 15M escalation after 2M/raw/S6/S7 reconciliation."""
from __future__ import annotations

import hashlib
import json
import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = Path(__file__).resolve().parents[1]
LOW_PLAN = EXP / "input/candidate-s5-probe2m-plan.json"
RAW_AUDIT = EXP / "output/candidate-raw-history-after15m.json"
LAYER_AUDIT = EXP / "output/candidate-saved-layer-after15m.json"
STRATEGY_HISTORY = ROOT / "research/experiments/n11-strategy-redesign-20261010/output/history.json"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target-index", type=int, default=0)
    parser.add_argument("--raw-audit", type=Path, default=RAW_AUDIT)
    parser.add_argument("--layer-audit", type=Path, default=LAYER_AUDIT)
    args = parser.parse_args()
    raw_path = args.raw_audit if args.raw_audit.is_absolute() else ROOT / args.raw_audit
    layer_path = args.layer_audit if args.layer_audit.is_absolute() else ROOT / args.layer_audit
    raw = json.loads(raw_path.read_text(encoding="utf-8"))
    layer = json.loads(layer_path.read_text(encoding="utf-8"))
    low = json.loads(LOW_PLAN.read_text(encoding="utf-8"))
    if not 0 <= args.target_index < len(low["targets"]):
        raise SystemExit(f"invalid target index: {args.target_index}")
    prior_target = low["targets"][args.target_index]
    key = tuple(prior_target["key"])
    ready = {tuple(k) for k in raw["dispatch_ready_keys"]}
    observations = raw["observations"].get(f"{key[0]},{key[1]}", [])
    if key not in ready or any(r["verdict"] in (1, 2) for r in observations):
        raise SystemExit(f"escalation target is not unresolved and dispatch-ready: {key}")
    if max((r["budget"] for r in observations if r["verdict"] == 0), default=0) != 2_000_000:
        raise SystemExit(f"unexpected earlier UNKNOWN budget for {key}: {observations}")
    s5_layer = f"{key[0]},{key[1]}"
    if s5_layer in layer["s5_results_from_raw_s6_s7_only"] or s5_layer in layer["s5_results_with_saved_cache_s6_s7"]:
        raise SystemExit(f"saved S6/S7 evidence now resolves S5 target: {key}")
    target = prior_target | {"arm": "next-class-escalation-15m", "budget": 15_000_000}
    plan = {"schema": "n11-reply27-single-s5-escalation-plan-v1",
            "s4_key": low["s4_key"], "coverage": low["coverage"],
            "raw_history_audit": {"path": raw_path.relative_to(ROOT).as_posix(), "sha256": sha(raw_path)},
            "saved_layer_audit": {"path": layer_path.relative_to(ROOT).as_posix(), "sha256": sha(layer_path)},
            "history_sha256": sha(STRATEGY_HISTORY), "targets": [target]}
    name = "candidate-s5-probe15m-plan.json" if args.target_index == 0 else f"candidate-s5-probe15m-target{args.target_index}-plan.json"
    out = EXP / "input" / name
    out.write_text(json.dumps(plan, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"plan": out.relative_to(ROOT).as_posix(), "plan_sha256": sha(out),
                      "target": target, "previous_unknown_budget": 2_000_000}, sort_keys=True))


if __name__ == "__main__":
    main()
