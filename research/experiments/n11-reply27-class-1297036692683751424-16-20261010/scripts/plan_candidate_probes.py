"""Create a four-target, low-legal-count 2M S5 probe plan after fresh preflight."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = Path(__file__).resolve().parents[1]
PREFLIGHT = EXP / "output/candidate-preflight.json"
RAW_AUDIT = EXP / "output/candidate-raw-history-audit.json"
STRATEGY_HISTORY = ROOT / "research/experiments/n11-strategy-redesign-20261010/output/history.json"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    pre = json.loads(PREFLIGHT.read_text(encoding="utf-8"))
    audit = json.loads(RAW_AUDIT.read_text(encoding="utf-8"))
    ready = {tuple(k) for k in audit["dispatch_ready_keys"]}
    rows = [r for r in pre["s5_children"] if tuple(r["key"]) in ready]
    rows.sort(key=lambda r: (r["legal_count"], tuple(r["key"])))
    chosen = rows[:4]
    if len(chosen) != 4 or any(r["legal_count"] > 85 for r in chosen):
        raise SystemExit(f"expected four lowest-cost ready targets, found {[r['legal_count'] for r in chosen]}")
    targets = [{"arm": "next-class-low-legal-2m", "stones": 5, "key": r["key"],
                "budget": 2_000_000, "group": "candidate-s4-1224979098645823488-536870912",
                "preflight_legal_count": r["legal_count"]} for r in chosen]
    plan = {"schema": "n11-reply27-low-legal-probe-plan-v1",
            "s4_key": pre["candidate_s4"]["key"], "coverage": pre["candidate_s4"]["coverage"],
            "preflight": {"path": PREFLIGHT.relative_to(ROOT).as_posix(), "sha256": sha(PREFLIGHT)},
            "raw_history_audit": {"path": RAW_AUDIT.relative_to(ROOT).as_posix(), "sha256": sha(RAW_AUDIT)},
            "history_sha256": sha(STRATEGY_HISTORY), "targets": targets}
    out = EXP / "input/candidate-s5-probe2m-plan.json"
    out.write_text(json.dumps(plan, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"plan": out.relative_to(ROOT).as_posix(), "plan_sha256": sha(out),
                      "targets": targets}, sort_keys=True))


if __name__ == "__main__":
    main()
