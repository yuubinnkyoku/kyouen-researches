"""Pin a single 15M escalation after refreshed raw/S6/S7 history checks."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = Path(__file__).resolve().parents[1]
LOW_PLAN = EXP / "input/followup-s5-probe2m-plan.json"
RAW_AUDIT = EXP / "output/followup-raw-history-after2m.json"
LAYER_AUDIT = EXP / "output/followup-saved-layer-after2m.json"
HISTORY = ROOT / "research/experiments/n11-strategy-redesign-20261010/output/history.json"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    low = json.loads(LOW_PLAN.read_text(encoding="utf-8"))
    raw = json.loads(RAW_AUDIT.read_text(encoding="utf-8"))
    layer = json.loads(LAYER_AUDIT.read_text(encoding="utf-8"))
    target = low["targets"][0]
    key = tuple(target["key"])
    token = f"{key[0]},{key[1]}"
    observations = raw["observations"].get(token, [])
    ready = {tuple(row) for row in raw["dispatch_ready_keys"]}
    assert key in ready and target["budget"] == 2_000_000
    assert not any(row["verdict"] in (1, 2) for row in observations)
    assert max((row["budget"] for row in observations if row["verdict"] == 0), default=0) == 2_000_000
    assert token not in layer["s5_results_from_raw_s6_s7_only"]
    assert token not in layer["s5_results_with_saved_cache_s6_s7"]
    escalated = target | {"arm": "next-cover-candidate-escalation-15m", "budget": 15_000_000}
    plan = {
        "schema": "n11-reply27-followup-single-s5-escalation-plan-v1",
        "s4_key": low["s4_key"], "coverage": low["coverage"],
        "low_budget_plan": {"path": LOW_PLAN.relative_to(ROOT).as_posix(), "sha256": sha(LOW_PLAN)},
        "raw_history_audit": {"path": RAW_AUDIT.relative_to(ROOT).as_posix(), "sha256": sha(RAW_AUDIT)},
        "saved_layer_audit": {"path": LAYER_AUDIT.relative_to(ROOT).as_posix(), "sha256": sha(LAYER_AUDIT)},
        "history_sha256": sha(HISTORY), "targets": [escalated],
    }
    out = EXP / "input/followup-s5-probe15m-plan.json"
    out.write_text(json.dumps(plan, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"plan": out.relative_to(ROOT).as_posix(), "plan_sha256": sha(out),
                      "previous_unknown_budget": 2_000_000, "target": escalated}, sort_keys=True))


if __name__ == "__main__":
    main()
