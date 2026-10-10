"""Pin a single S5 target after raw-history and saved-layer preflights."""
from __future__ import annotations

import csv
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = Path(__file__).resolve().parents[1]
OUT = EXP / "output"
CACHE = ROOT / "research/experiments/n11-reply27-class-1297036692683751424-16-20261010/output/current-exact-s5-after-followup-loss.cache"
sys.path.insert(0, str(ROOT / "research/experiments/n11-frontier-selection-20261005/scripts"))
from s5_evidence_policy import quarantined_cache_keys  # noqa: E402


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_cache() -> dict[tuple[int, int], int]:
    result = {}
    for line in CACHE.read_text(encoding="utf-8").splitlines():
        if not line or line.startswith("#"):
            continue
        fields = line.split(",")
        key = (int(fields[1]), int(fields[2]))
        if key in result and result[key] != int(fields[4]):
            raise ValueError(f"cache conflict for {key}")
        result[key] = int(fields[4])
    return result


def main() -> None:
    preflight_path = OUT / "geometric-cache-preflight.json"
    raw_path = OUT / "raw-history-audit.json"
    layer_path = OUT / "saved-s6-s7-preflight.json"
    preflight = json.loads(preflight_path.read_text(encoding="utf-8"))
    raw = json.loads(raw_path.read_text(encoding="utf-8"))
    layer = json.loads(layer_path.read_text(encoding="utf-8"))
    target = preflight["lowest_legal_unknown_s5"][0]
    key = tuple(target["key"])
    token = f"{key[0]},{key[1]}"
    observations = raw["observations"].get(token, [])
    quarantine = quarantined_cache_keys()
    cache = read_cache()

    assert tuple(preflight["class"]["key"]) == (1188950301626859520, 536870912)
    assert preflight["class"]["status"] == "UNKNOWN"
    assert key in {tuple(item) for item in raw["dispatch_ready_keys"]}
    assert not any(row["verdict"] in (1, 2) for row in observations)
    assert not any(row["verdict"] == 0 and row["budget"] >= 2_000_000 for row in observations)
    assert token not in layer["s5_results_from_raw_s6_s7_only"]
    assert token not in layer["s5_results_with_saved_cache_s6_s7"]
    assert key not in quarantine and key not in cache
    assert raw["exact_verdict_conflicts"] == []
    assert not (set(cache) & quarantine)

    target_csv = EXP / "input/probe-target.csv"
    target_csv.parent.mkdir(parents=True, exist_ok=True)
    with target_csv.open("w", encoding="utf-8", newline="") as stream:
        csv.writer(stream, lineterminator="\n").writerow(
            ["s5target", 0, 5, key[0], key[1], target["legal_count"], 0, 0, 0, 0, 0]
        )

    registry = ROOT / "results/n11-s5-evidence-quarantine.json"
    solver = ROOT / ".local/n11-independent-audit-solver.exe"
    solver_source = ROOT / "cpp/solvers/kyouen_dfpn_root.cpp"
    inputs = [preflight_path, raw_path, layer_path]
    plan = {
        "schema": "n11-reply27-s5-single-probe-plan-v1",
        "main_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "s4_parent": preflight["class"]["key"],
        "s5_target": {"key": list(key), "legal_count": target["legal_count"], "budget": 2_000_000,
                      "workers": 1, "watchdog_seconds": 180},
        "preflights": [{"path": path.relative_to(ROOT).as_posix(), "sha256": sha(path)} for path in inputs],
        "effective_cache": {"path": CACHE.relative_to(ROOT).as_posix(), "sha256": sha(CACHE),
                            "rows": len(cache), "quarantine_registry_sha256": sha(registry),
                            "active_quarantine_keys": [list(item) for item in sorted(quarantine)]},
        "solver": {"path": solver.relative_to(ROOT).as_posix(), "sha256": sha(solver),
                   "source_path": solver_source.relative_to(ROOT).as_posix(),
                   "source_sha256": sha(solver_source),
                   "options": ["--n=11", "--memo=22", "--exact-order=count"]},
        "dispatch_checks": {"raw_history_conflicts": len(raw["exact_verdict_conflicts"]),
                            "prior_exact_observations": 0, "unknown_at_or_above_budget": 0,
                            "raw_s6_s7_derived": False, "saved_s6_s7_derived": False,
                            "active_quarantine": False},
        "target_input": {"path": target_csv.relative_to(ROOT).as_posix(), "sha256": sha(target_csv)},
    }
    plan_path = OUT / "probe-plan.json"
    plan_path.write_text(json.dumps(plan, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"target": list(key), "legal_count": target["legal_count"],
                      "input_sha256": sha(target_csv), "plan_sha256": sha(plan_path),
                      "solver_sha256": sha(solver), "source_sha256": sha(solver_source)}, sort_keys=True))


if __name__ == "__main__":
    main()
