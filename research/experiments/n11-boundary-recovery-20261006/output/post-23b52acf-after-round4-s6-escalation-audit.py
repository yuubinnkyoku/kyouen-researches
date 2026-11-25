#!/usr/bin/env python3
"""Reconcile the 23b52acf checkpoint cache and replay corpus without solver work."""
from __future__ import annotations

import csv
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
BOUNDARY_SCRIPTS = ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts"
FRONTIER_SCRIPTS = ROOT / "research/experiments/n11-frontier-selection-20261005/scripts"
sys.path.insert(0, str(BOUNDARY_SCRIPTS))
sys.path.insert(0, str(FRONTIER_SCRIPTS))
from derive_shared_s6_witness_cache import canonical_safe_key  # noqa: E402
from merge_exact_s5_evidence import merge  # noqa: E402


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def verify_saved_sources(records, label):
    for record in records:
        path = ROOT / record["path"]
        actual = sha256(path)
        if actual != record["sha256"]:
            raise SystemExit(f"{label} source hash mismatch: {path}")


def main() -> None:
    prior_cache_path = OUT / "post-23b52acf-after-probe8-round2-s5-cache-corpus-audit.json"
    prior_raw_path = OUT / "post-23b52acf-after-probe8-round2-s5-raw-replay-corpus-audit.json"
    prior_cache = load_json(prior_cache_path)
    prior_raw = load_json(prior_raw_path)
    verify_saved_sources(prior_cache["cache_files"], "prior cache corpus")
    verify_saved_sources(prior_raw["source_files_with_s5_replay_rows"], "prior raw corpus")

    delta_caches = [
        OUT / "post-23b52acf-after-round2-round3-completed-new-exact-s5.cache",
        OUT / "post-23b52acf-after-round3-round4-completed-new-exact-s5.cache",
    ]
    current_cache = OUT / "post-23b52acf-after-round3-round4-completed-merged-s5.cache"
    cache_paths = [ROOT / record["path"] for record in prior_cache["cache_files"]] + delta_caches
    union, cache_sources = merge(cache_paths, [])
    current, _ = merge([current_cache], [])
    if union != current:
        missing = sorted(set(current) - set(union))[:10]
        extra = sorted(set(union) - set(current))[:10]
        raise SystemExit(f"cache corpus != current cache; missing={missing}, extra={extra}")
    union_path = OUT / "post-23b52acf-after-round4-s6-escalation-s5-cache-corpus-union.cache"
    counts = Counter(union.values())
    union_path.write_text(
        "# s5 verdict cache: n=11 schema=1 (reconciled exact corpus through round4)\n"
        + "".join(f"s5verdict,{lo},{hi},5,{value},0\n" for (lo, hi), value in sorted(union.items())),
        encoding="utf-8",
    )

    new_raw_paths = [
        OUT / "post-23b52acf-after-round2-round3-completed-raw-all.csv",
        OUT / "post-23b52acf-after-round3-round4-completed-raw-all.csv",
    ]
    raw_records = list(prior_raw["source_files_with_s5_replay_rows"])
    raw_records.extend(
        {"path": path.relative_to(ROOT).as_posix(), "sha256": sha256(path)}
        for path in new_raw_paths
    )
    added_raw_rows = 0
    added_exact_rows = 0
    added_unknown_rows = 0
    added_exact_keys: dict[tuple[int, int], int] = {}
    exact_conflicts = []
    exact_missing = []
    same_budget_unknowns = list(prior_raw["same_budget_unknown_rows"])
    verdict_counts = Counter({int(k): int(v) for k, v in prior_raw["raw_verdict_counts"].items()})
    budget_exact_counts = Counter({int(k): int(v) for k, v in prior_raw["exact_replay_budget_counts"].items()})
    for path in new_raw_paths:
        record_path = path.relative_to(ROOT).as_posix()
        with path.open(newline="", encoding="utf-8") as stream:
            for row_number, row in enumerate(csv.reader(stream), start=1):
                if not row or row[0] != "replay":
                    continue
                if len(row) != 11 or int(row[2]) != 5:
                    continue
                added_raw_rows += 1
                raw_key = (int(row[9]), int(row[10]))
                key = canonical_safe_key(raw_key, 5)
                verdict = int(row[6])
                budget = int(row[5])
                verdict_counts[verdict] += 1
                if verdict in (1, 2):
                    added_exact_rows += 1
                    budget_exact_counts[budget] += 1
                    old = added_exact_keys.get(key)
                    if old is not None and old != verdict:
                        exact_conflicts.append({"key": list(key), "old": old, "new": verdict,
                                                "path": record_path, "row": row_number})
                    added_exact_keys[key] = verdict
                    if key not in current:
                        exact_missing.append({"key": list(key), "verdict": verdict,
                                              "path": record_path, "row": row_number})
                    elif current[key] != verdict:
                        exact_conflicts.append({"key": list(key), "old": current[key],
                                                "new": verdict, "path": record_path,
                                                "row": row_number})
                elif verdict == 0:
                    added_unknown_rows += 1
                    if budget == 15_000_000:
                        same_budget_unknowns.append({"key": list(key), "budget": budget,
                                                     "path": record_path, "row": row_number})
    if exact_conflicts or exact_missing:
        raise SystemExit(f"raw replay/cache mismatch: conflicts={len(exact_conflicts)}, missing={len(exact_missing)}")

    old_cache_hash = sha256(prior_cache_path)
    old_raw_hash = sha256(prior_raw_path)
    cache_audit = {
        "schema": "n11-reply27-s5-cache-corpus-audit-v2",
        "claim": "Persisted exact cache evidence only; no solver was run and no UNKNOWN was propagated.",
        "dispatch_main_commit": "23b52acfb96c95a258296b4ffda45562db0e74ea",
        "prior_audit": {"path": prior_cache_path.relative_to(ROOT).as_posix(), "sha256": old_cache_hash,
                        "cache_files": prior_cache["cache_files_discovered"],
                        "unique_exact_rows": prior_cache["corpus_unique_exact_rows"]},
        "added_delta_caches": [
            {"path": p.relative_to(ROOT).as_posix(), "sha256": sha256(p)} for p in delta_caches
        ],
        "source_cache_files": len(cache_sources["sources"]),
        "checkpoint_cache": {"path": current_cache.relative_to(ROOT).as_posix(),
                             "sha256": sha256(current_cache), "rows": len(current),
                             "WIN": counts[1], "LOSS": counts[2], "conflicts": 0},
        "corpus_union": {"path": union_path.relative_to(ROOT).as_posix(),
                         "sha256": sha256(union_path), "rows": len(union),
                         "WIN": counts[1], "LOSS": counts[2], "conflicts": 0,
                         "missing_from_current": 0, "extra_vs_current": 0},
        "sources": cache_sources["sources"],
    }
    cache_audit_path = OUT / "post-23b52acf-after-round4-s6-escalation-s5-cache-corpus-audit.json"
    cache_audit_path.write_text(json.dumps(cache_audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    raw_audit = {
        "schema": "n11-reply27-s5-raw-replay-corpus-audit-v2",
        "claim": "Saved raw replay rows were checked against the exact cache; no solver was run.",
        "prior_audit": {"path": prior_raw_path.relative_to(ROOT).as_posix(), "sha256": old_raw_hash,
                        "raw_s5_replay_rows": prior_raw["raw_s5_replay_rows"],
                        "raw_exact_s5_replay_rows": prior_raw["raw_exact_s5_replay_rows"],
                        "raw_unique_exact_s5_keys": prior_raw["raw_unique_exact_s5_keys"],
                        "same_budget_unknown_rows": len(prior_raw["same_budget_unknown_rows"])},
        "added_raw_files": [
            {"path": p.relative_to(ROOT).as_posix(), "sha256": sha256(p)} for p in new_raw_paths
        ],
        "source_files_with_s5_replay_rows": raw_records,
        "raw_s5_replay_rows": prior_raw["raw_s5_replay_rows"] + added_raw_rows,
        "raw_exact_s5_replay_rows": prior_raw["raw_exact_s5_replay_rows"] + added_exact_rows,
        "raw_unknown_s5_replay_rows": (prior_raw["raw_s5_replay_rows"]
                                        - prior_raw["raw_exact_s5_replay_rows"] + added_unknown_rows),
        "raw_unique_exact_s5_keys": prior_raw["raw_unique_exact_s5_keys"] + len(added_exact_keys),
        "raw_verdict_counts": {str(k): v for k, v in sorted(verdict_counts.items())},
        "exact_replay_budget_counts": {str(k): v for k, v in sorted(budget_exact_counts.items())},
        "same_budget_unknown_rows": same_budget_unknowns,
        "same_budget_unknown_count": len(same_budget_unknowns),
        "raw_exact_not_in_cache": exact_missing,
        "raw_exact_verdict_conflicts": exact_conflicts,
        "cache_rows_without_raw_s5_replay": len(current) - prior_raw["raw_unique_exact_s5_keys"] - len(added_exact_keys),
        "current_cache": {"path": current_cache.relative_to(ROOT).as_posix(),
                          "sha256": sha256(current_cache), "entries": len(current),
                          "WIN": counts[1], "LOSS": counts[2], "conflicts": 0},
    }
    raw_audit_path = OUT / "post-23b52acf-after-round4-s6-escalation-s5-raw-replay-corpus-audit.json"
    raw_audit_path.write_text(json.dumps(raw_audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(json.dumps({"cache_rows": len(current), "WIN": counts[1], "LOSS": counts[2],
                      "cache_sources": len(cache_sources["sources"]), "cache_conflicts": 0,
                      "raw_rows": prior_raw["raw_s5_replay_rows"] + added_raw_rows,
                      "raw_exact_rows": prior_raw["raw_exact_s5_replay_rows"] + added_exact_rows,
                      "raw_unique_exact_keys": prior_raw["raw_unique_exact_s5_keys"] + len(added_exact_keys),
                      "same_budget_unknowns": len(same_budget_unknowns),
                      "raw_exact_missing": len(exact_missing), "raw_conflicts": len(exact_conflicts)},
                     sort_keys=True))


if __name__ == "__main__":
    main()
