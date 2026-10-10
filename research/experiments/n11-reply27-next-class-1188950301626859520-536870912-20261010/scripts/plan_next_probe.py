"""Select one low-legal-count S5 child using the current complete class audit."""
from __future__ import annotations

import csv
import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = Path(__file__).resolve().parents[1]
OUT = EXP / "output"
CACHE = OUT / "current-exact-s5-after-probe.cache"
sys.path.insert(0, str(ROOT / "research/experiments/n11-frontier-selection-20261005/scripts"))
from s5_evidence_policy import quarantined_cache_keys  # noqa: E402


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw", type=Path, default=OUT / "raw-history-after-15m.json")
    parser.add_argument("--layer", type=Path, default=OUT / "saved-layer-after-15m.json")
    parser.add_argument("--cache", type=Path, default=CACHE)
    parser.add_argument("--suffix", default="2")
    args = parser.parse_args()
    raw_path = args.raw if args.raw.is_absolute() else ROOT / args.raw
    layer_path = args.layer if args.layer.is_absolute() else ROOT / args.layer
    cache_path = args.cache if args.cache.is_absolute() else ROOT / args.cache
    pre = json.loads((OUT / "geometric-cache-preflight.json").read_text(encoding="utf-8"))
    raw = json.loads(raw_path.read_text(encoding="utf-8"))
    layer = json.loads(layer_path.read_text(encoding="utf-8"))
    exact = {}
    for line in cache_path.read_text(encoding="utf-8").splitlines():
        if line and not line.startswith("#"):
            fields = line.split(",")
            exact[(int(fields[1]), int(fields[2]))] = int(fields[4])
    quarantine = quarantined_cache_keys()
    if set(exact) & quarantine:
        raise SystemExit("active quarantined cache key is present")
    ready = {tuple(key) for key in raw["dispatch_ready_keys"]}
    choices = sorted((item["legal_count"], tuple(item["key"]))
                     for item in pre["s5_children"] if tuple(item["key"]) not in exact)
    selected = next((item for item in choices if item[1] in ready), None)
    if selected is None:
        raise SystemExit("no raw-history-ready UNKNOWN child remains")
    legal, key = selected
    token = f"{key[0]},{key[1]}"
    observations = raw["observations"].get(token, [])
    if any(item["verdict"] in (1, 2) for item in observations):
        raise SystemExit(f"raw exact evidence already exists for {key}")
    if any(item["verdict"] == 0 and item["budget"] >= 2_000_000 for item in observations):
        raise SystemExit(f"same-or-higher-budget UNKNOWN exists for {key}")
    if key in quarantine:
        raise SystemExit(f"target is actively quarantined: {key}")
    if token in layer["s5_results_from_raw_s6_s7_only"] or token in layer["s5_results_with_saved_cache_s6_s7"]:
        raise SystemExit(f"saved-layer evidence already classifies {key}")
    if raw["exact_verdict_conflicts"]:
        raise SystemExit("raw history contains a verdict conflict")

    target_csv = EXP / f"input/probe-target-{args.suffix}.csv"
    target_csv.parent.mkdir(parents=True, exist_ok=True)
    with target_csv.open("w", encoding="utf-8", newline="") as stream:
        csv.writer(stream, lineterminator="\n").writerow(
            ["s5target", 0, 5, key[0], key[1], legal, 0, 0, 0, 0, 0]
        )
    solver = ROOT / ".local/n11-independent-audit-solver.exe"
    solver_source = ROOT / "cpp/solvers/kyouen_dfpn_root.cpp"
    evidence = [OUT / "raw-history-after-15m.json", OUT / "saved-layer-after-15m.json",
                target_csv, CACHE]
    result = {
        "schema": "n11-reply27-s5-next-low-cost-probe-plan-v1",
        "main_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "s4_parent": pre["class"]["key"],
        "s5_target": {"key": list(key), "legal_count": legal, "budget": 2_000_000,
                      "workers": 1, "watchdog_seconds": 180},
        "preflight_sources": [{"path": path.relative_to(ROOT).as_posix(), "sha256": sha(path)}
                              for path in [raw_path, layer_path, target_csv, cache_path]],
        "prior_observations": observations,
        "solver": {"path": solver.relative_to(ROOT).as_posix(), "sha256": sha(solver),
                   "source_path": solver_source.relative_to(ROOT).as_posix(),
                   "source_sha256": sha(solver_source),
                   "options": ["--n=11", "--memo=22", "--exact-order=count"]},
        "dispatch_checks": {"raw_exact": False, "unknown_at_or_above_budget": False,
                            "raw_s6_s7_derived": False, "saved_s6_s7_derived": False,
                            "raw_cache_conflicts": 0},
    }
    plan_path = OUT / f"probe-{args.suffix}-plan.json"
    plan_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"target": list(key), "legal_count": legal, "input_sha256": sha(target_csv),
                      "plan_sha256": sha(plan_path)}, sort_keys=True))


if __name__ == "__main__":
    main()
