"""Pin one lowest-cost S5 probe for the next dual-tight cover candidate."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = Path(__file__).resolve().parents[1]
PREFLIGHT = EXP / "output/followup-preflight.json"
RAW_AUDIT = EXP / "output/followup-raw-history-audit.json"
LAYER_AUDIT = EXP / "output/followup-saved-layer-preflight.json"
HISTORY = ROOT / "research/experiments/n11-strategy-redesign-20261010/output/history.json"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    pre = json.loads(PREFLIGHT.read_text(encoding="utf-8"))
    raw = json.loads(RAW_AUDIT.read_text(encoding="utf-8"))
    layer = json.loads(LAYER_AUDIT.read_text(encoding="utf-8"))
    candidate = pre["class"]
    key = tuple(candidate["key"])
    assert candidate["status"] == "UNKNOWN" and candidate["coverage"] == [55, 65, 100, 108]
    wanted = pre["lowest_legal_unknown_s5"][0]
    target_key = tuple(wanted["key"])
    assert wanted["legal_count"] == 87
    assert target_key in {tuple(row["key"]) for row in pre["s5_children"]}
    assert target_key in {tuple(x) for x in raw["dispatch_ready_keys"]}
    token = f"{target_key[0]},{target_key[1]}"
    observations = raw["observations"].get(token, [])
    assert not any(row["verdict"] in (1, 2) for row in observations)
    assert not any(row["verdict"] == 0 and row["budget"] >= 2_000_000 for row in observations)
    assert token not in layer["s5_results_from_raw_s6_s7_only"]
    assert token not in layer["s5_results_with_saved_cache_s6_s7"]
    target = {"arm": "next-cover-candidate-low-legal-2m", "stones": 5,
              "key": list(target_key), "budget": 2_000_000,
              "group": "next-cover-candidate-1188950301626859520-536870912",
              "preflight_legal_count": wanted["legal_count"]}
    plan = {
        "schema": "n11-reply27-followup-single-s5-probe-v1",
        "s4_key": list(key), "coverage": candidate["coverage"],
        "preflight": {"path": PREFLIGHT.relative_to(ROOT).as_posix(), "sha256": sha(PREFLIGHT)},
        "raw_history_audit": {"path": RAW_AUDIT.relative_to(ROOT).as_posix(), "sha256": sha(RAW_AUDIT)},
        "saved_layer_audit": {"path": LAYER_AUDIT.relative_to(ROOT).as_posix(), "sha256": sha(LAYER_AUDIT)},
        "history_sha256": sha(HISTORY), "targets": [target],
    }
    out = EXP / "input/followup-s5-probe2m-plan.json"
    out.write_text(json.dumps(plan, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"plan": out.relative_to(ROOT).as_posix(), "plan_sha256": sha(out),
                      "class": list(key), "target": target}, sort_keys=True))


if __name__ == "__main__":
    main()
