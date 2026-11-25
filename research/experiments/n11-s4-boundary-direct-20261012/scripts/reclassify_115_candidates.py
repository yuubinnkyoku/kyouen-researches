#!/usr/bin/env python3
"""Reclassify and rank the historical 115 classes touching moves 100 or 108."""
from __future__ import annotations

import csv
import gzip
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = ROOT / "research/experiments/n11-s4-boundary-direct-20261012"
CURRENT = EXP / "output/current-exact-s5.cache"
GEOMETRY = ROOT / "research/experiments/n11-strategy-redesign-20261010/output/geometry.json.gz"
PROFILE = ROOT / "research/experiments/n11-strategy-redesign-20261010/output/historical-cost-profile.json"
HISTORY_MOVES = {100, 108}


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def main() -> None:
    sys.path.insert(0, str(ROOT / "research/experiments/n11-frontier-selection-20261005/scripts"))
    from s5_evidence_policy import quarantined_cache_keys
    sys.path.insert(0, str(ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts"))
    from independent import Board
    board = Board(11)
    quarantine = quarantined_cache_keys()
    cache = {}
    with CURRENT.open(encoding="utf-8-sig", newline="") as f:
        for line, row in enumerate(csv.reader(f), 1):
            if not row or row[0].strip().startswith("#"):
                continue
            if len(row) != 6 or row[0] != "s5verdict":
                raise ValueError(f"invalid exact cache row {line}: {row}")
            lo, hi, stones, verdict, nodes = map(int, row[1:])
            key = (lo, hi)
            if stones != 5 or verdict not in (1, 2) or nodes < 0 or key in quarantine:
                raise ValueError(f"invalid/quarantined cache evidence at row {line}: {key}")
            if key in cache and cache[key][0] != verdict:
                raise ValueError(f"opposite exact cache conflict for {key}")
            cache[key] = (verdict, nodes)
    with gzip.open(GEOMETRY, "rt", encoding="utf-8") as f:
        geometry = json.load(f)
    if len(geometry) != 3384:
        raise ValueError("expected 3,384 S4 classes")
    profile_doc = json.loads(PROFILE.read_text(encoding="utf-8"))
    profile = {int(k): float(v["mean_truncated_nodes"]) for k, v in profile_doc["profile"].items()}
    rows = []
    all_coverage = set()
    for item in geometry:
        s4 = tuple(item["key"])
        mask = s4[0] | (s4[1] << 64)
        generated = {(child & ((1 << 64) - 1), child >> 64) for child in board.children(mask)}
        stored = {tuple(child) for child in item["children"]}
        if generated != stored or len(stored) != len(item["children"]):
            raise ValueError(f"independent S4 child boundary mismatch: {s4}")
        coverage = set(item["coverage"])
        all_coverage.update(coverage)
        if not coverage.intersection(HISTORY_MOVES):
            continue
        verdicts = [cache.get(child, (0, 0))[0] for child in generated]
        status = "WIN" if 1 in verdicts else "LOSS" if verdicts and all(v == 2 for v in verdicts) else "UNKNOWN"
        unknown = [child for child in generated if cache.get(child, (0, 0))[0] == 0]
        legals = [board.legal(child[0] | (child[1] << 64)).bit_count() for child in unknown]
        estimate = sum(profile.get((n // 10) * 10, 15_000_000) for n in legals)
        rows.append({"key": list(s4), "status": status, "coverage": sorted(coverage),
                     "s5_children": len(generated), "s5_win": verdicts.count(1),
                     "s5_loss": verdicts.count(2), "s5_unknown": verdicts.count(0),
                     "legal_min": min(legals) if legals else None,
                     "legal_max": max(legals) if legals else None,
                     "completion_15m_censored_node_proxy": round(estimate),
                     "historically_covered_moves": sorted(coverage & HISTORY_MOVES),
                     "active_uncovered_moves_now": [],
                     "ranking_note": "The former residual moves are already secured 119/119; this is a retrospective status/cost ranking, not a remaining proof target."})
    if len(all_coverage) != 119 or len(rows) != 115:
        raise ValueError(f"expected 119 third moves and 115 historical candidates, got {len(all_coverage)}/{len(rows)}")
    status_counts = Counter(r["status"] for r in rows)
    rank_order = {"UNKNOWN": 0, "LOSS": 1, "WIN": 2}
    rows.sort(key=lambda r: (rank_order[r["status"]], r["completion_15m_censored_node_proxy"],
                             r["key"][1], r["key"][0]))
    for i, row in enumerate(rows, 1):
        row["rank"] = i
    target = next(r for r in rows if tuple(r["key"]) == (1297036692683752448, 0))
    if target["status"] != "LOSS" or target["s5_children"] != 106 or target["s5_loss"] != 106:
        raise ValueError("target S4 does not reclassify to complete LOSS")
    output_csv = EXP / "output/candidate-classes-after-s6-parent-loss.csv"
    with output_csv.open("w", encoding="utf-8", newline="") as f:
        cols = ["rank", "status", "key", "coverage", "s5_children", "s5_win", "s5_loss", "s5_unknown",
                "legal_min", "legal_max", "completion_15m_censored_node_proxy", "active_uncovered_moves_now"]
        writer = csv.DictWriter(f, fieldnames=cols, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({"rank": row["rank"], "status": row["status"], "key": json.dumps(row["key"]),
                             "coverage": json.dumps(row["coverage"]), "s5_children": row["s5_children"],
                             "s5_win": row["s5_win"], "s5_loss": row["s5_loss"],
                             "s5_unknown": row["s5_unknown"], "legal_min": row["legal_min"],
                             "legal_max": row["legal_max"],
                             "completion_15m_censored_node_proxy": row["completion_15m_censored_node_proxy"],
                             "active_uncovered_moves_now": json.dumps(row["active_uncovered_moves_now"])})
    output_json = EXP / "output/candidate-ranking-after-s6-parent-loss.json"
    doc = {
        "schema": "n11-reply27-115-historical-candidate-reclassification-v1",
        "source_frontier_sha256": sha(EXP / "output/frontier-after-s6-parent-loss.json"),
        "s5_cache_sha256": sha(CURRENT), "independent_geometry_source_sha256": sha(GEOMETRY),
        "historical_cost_profile_sha256": sha(PROFILE),
        "third_moves": len(all_coverage), "secured_third_moves": 119,
        "remaining_third_moves": [], "historical_candidate_coverage": sorted(HISTORY_MOVES),
        "historical_candidate_count": len(rows), "status_counts": dict(sorted(status_counts.items())),
        "target_s4": {"key": list(target["key"]), "status": target["status"],
                      "s5_loss": target["s5_loss"], "s5_children": target["s5_children"]},
        "ranking_rule": "UNKNOWN first, then historical 15M-censored mean-node proxy; this is a retrospective queue and no longer an active target because the root is covered",
        "classes_csv": str(output_csv.relative_to(ROOT)), "classes_csv_sha256": sha(output_csv),
        "ranked_classes": rows,
    }
    output_json.write_text(json.dumps(doc, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in doc.items() if k != "ranked_classes"}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
