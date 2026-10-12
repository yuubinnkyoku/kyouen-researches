#!/usr/bin/env python3
"""Reclassify the 115 reply27 candidates and freeze a diverse second S5 batch."""
from __future__ import annotations

import csv
import argparse
import gzip
import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = ROOT / "research/experiments/n11-s4-boundary-direct-20261012"
CURRENT = EXP / "output/current-exact-s5.cache"
FRONTIER = EXP / "output/frontier-after-batch.json"
FIRST_SELECTION = EXP / "input/first-batch-selection.json"
FIRST_RUN = EXP / "output/first-batch-run.json"
GEOMETRY = ROOT / "research/experiments/n11-strategy-redesign-20261010/output/geometry.json.gz"
HISTORY = ROOT / "research/experiments/n11-strategy-redesign-20261010/output/history.json"
PROFILE = ROOT / "research/experiments/n11-strategy-redesign-20261010/output/historical-cost-profile.json"
BUILD = EXP / "input/solver-build.json"
TARGET = (1297036692683752448, 0)
LIMIT = 15_000_000


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def read_cache(path: Path, quarantine: set[tuple[int, int]]):
    cache = {}
    with path.open(encoding="utf-8-sig", newline="") as f:
        for line, row in enumerate(csv.reader(f), 1):
            if not row or row[0].strip().startswith("#"):
                continue
            if len(row) != 6 or row[0] != "s5verdict":
                raise ValueError(f"malformed exact S5 cache row {path}:{line}")
            lo, hi, stones, verdict, nodes = map(int, row[1:])
            key = (lo, hi)
            if stones != 5 or verdict not in (1, 2) or nodes < 0:
                raise ValueError(f"invalid exact cache value {path}:{line}")
            if key in quarantine:
                raise ValueError(f"quarantined key present in current cache: {key}")
            previous = cache.get(key)
            if previous is not None and previous[0] != verdict:
                raise ValueError(f"cache conflict for {key}")
            cache[key] = (verdict, nodes if previous is None else min(nodes, previous[1]))
    return cache


def freeze(path: Path, content: bytes):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if path.read_bytes() != content:
            raise ValueError(f"refusing to overwrite different frozen artifact: {path}")
    else:
        path.write_bytes(content)


def json_bytes(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def ordinal_word(number: int) -> str:
    words = {2: "second", 3: "third", 4: "fourth", 5: "fifth", 6: "sixth",
             7: "seventh", 8: "eighth", 9: "ninth", 10: "tenth"}
    if number not in words:
        raise ValueError("batch number must be from 2 through 10")
    return words[number]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--batch-number", type=int, default=2,
                        help="1-based S5 batch number; batch 1 is already frozen")
    parser.add_argument("--prior-selection", type=Path, action="append",
                        help="completed prior selection; repeat once per prior batch")
    parser.add_argument("--prior-run", type=Path, action="append",
                        help="completed prior run manifest; repeat once per prior batch")
    parser.add_argument("--frontier", type=Path, default=FRONTIER,
                        help="full independent frontier receipt for the latest completed batch")
    args = parser.parse_args()
    number = args.batch_number
    word = ordinal_word(number)
    prior_selection_paths = args.prior_selection or [FIRST_SELECTION]
    prior_run_paths = args.prior_run or [FIRST_RUN]
    if len(prior_selection_paths) != len(prior_run_paths) or not prior_run_paths:
        raise ValueError("provide matching --prior-selection and --prior-run paths")
    prior_selection_paths = [p if p.is_absolute() else ROOT / p for p in prior_selection_paths]
    prior_run_paths = [p if p.is_absolute() else ROOT / p for p in prior_run_paths]
    frontier_path = args.frontier if args.frontier.is_absolute() else ROOT / args.frontier
    sys.path.insert(0, str(ROOT / "research/experiments/n11-frontier-selection-20261005/scripts"))
    from s5_evidence_policy import quarantined_cache_keys
    sys.path.insert(0, str(ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts"))
    from independent import Board

    board = Board(11)
    cache = read_cache(CURRENT, quarantined_cache_keys())
    with gzip.open(GEOMETRY, "rt", encoding="utf-8") as f:
        geometry = json.load(f)
    if len(geometry) != 3384:
        raise ValueError("independent geometry source must contain all 3,384 S4 classes")
    classes = {}
    full_coverage = set()
    secured = set()
    counts = Counter()
    for item in geometry:
        parent = tuple(item["key"])
        mask = parent[0] | (parent[1] << 64)
        generated = {(k & ((1 << 64) - 1), k >> 64) for k in board.children(mask)}
        stored = {tuple(k) for k in item["children"]}
        if generated != stored or len(stored) != len(item["children"]):
            raise ValueError(f"independent boundary mismatch for S4 {parent}")
        if mask.bit_count() != 4 or board.canonical(mask) != mask:
            raise ValueError(f"noncanonical S4 class {parent}")
        verdicts = [cache.get(k, (0, 0))[0] for k in generated]
        status = "WIN" if 1 in verdicts else ("LOSS" if verdicts and all(v == 2 for v in verdicts) else "UNKNOWN")
        coverage = set(item["coverage"])
        if status == "LOSS":
            secured.update(coverage)
        counts[status] += 1
        full_coverage.update(coverage)
        classes[parent] = {"status": status, "children": generated, "coverage": coverage,
                           "s5_counts": Counter({1: verdicts.count(1), 2: verdicts.count(2), 0: verdicts.count(0)})}
    remaining = sorted(full_coverage - secured)
    if len(classes) != 3384 or len(full_coverage) != 119:
        raise ValueError("reply27 class/third-move universe changed")
    if remaining != [100, 108]:
        raise ValueError(f"this batch selector expects the two symmetric remaining moves, got {remaining}")

    candidates = [parent for parent, info in classes.items() if info["coverage"] & set(remaining)]
    candidate_status = Counter(classes[k]["status"] for k in candidates)
    if len(candidates) != 115 or candidate_status != Counter({"WIN": 54, "UNKNOWN": 61}):
        raise ValueError(f"unexpected 115-candidate classification: {candidate_status}")
    active = {k for k in candidates if classes[k]["status"] == "UNKNOWN" and set(remaining).issubset(classes[k]["coverage"])}
    if len(active) != 61:
        raise ValueError(f"unexpected live candidate count: {len(active)}")
    incidence: dict[tuple[int, int], list[tuple[int, int]]] = defaultdict(list)
    for parent in active:
        for child in classes[parent]["children"]:
            if cache.get(child, (0, 0))[0] == 0:
                incidence[child].append(parent)

    history_list = json.loads(HISTORY.read_text(encoding="utf-8"))
    history = {(row["stones"], *row["key"]): row for row in history_list}
    profile_doc = json.loads(PROFILE.read_text(encoding="utf-8"))
    profile = {int(k): v for k, v in profile_doc["profile"].items()}
    prior_selections = [json.loads(p.read_text(encoding="utf-8")) for p in prior_selection_paths]
    prior_runs = [json.loads(p.read_text(encoding="utf-8")) for p in prior_run_paths]
    for sel_path, sel_doc, run_doc in zip(prior_selection_paths, prior_selections, prior_runs):
        if run_doc.get("selection_sha256") != sha(sel_path):
            raise ValueError(f"prior run does not match frozen selection: {sel_path}")
        if run_doc.get("solver_binary_sha256") != sel_doc["solver"]["binary_sha256"]:
            raise ValueError(f"prior run solver does not match frozen selection: {sel_path}")
    for sel_path, sel_doc, run_doc in zip(prior_selection_paths, prior_selections, prior_runs):
        if run_doc.get("selection_sha256") != sha(sel_path):
            raise ValueError(f"prior run does not match frozen selection: {sel_path}")
        if run_doc.get("solver_binary_sha256") != sel_doc["solver"]["binary_sha256"]:
            raise ValueError(f"prior run solver does not match frozen selection: {sel_path}")
    all_prior_runs = [row for doc in prior_runs for row in doc["runs"]]
    attempted = {tuple(r["key"]) for r in all_prior_runs}
    if len(attempted) != len(all_prior_runs):
        raise ValueError("a prior S5 root is repeated across completed batches")
    if any(r["nodes"] > LIMIT for r in all_prior_runs):
        raise ValueError("prior batch exceeds pinned 15M cap")
    first_selection = json.loads(FIRST_SELECTION.read_text(encoding="utf-8"))
    target_mask = TARGET[0] | (TARGET[1] << 64)
    target_children = {(k & ((1 << 64) - 1), k >> 64) for k in board.children(target_mask)}
    if len(target_children) != 106:
        raise ValueError("target S4 did not regenerate to 106 children")
    unresolved = sorted(k for k in target_children if cache.get(k, (0, 0))[0] == 0)
    eligible = []
    for key in unresolved:
        if key in attempted or key in quarantined_cache_keys():
            continue
        hist = history.get((5, *key), {})
        observations = hist.get("observations", [])
        prior_15m_unknown = any(o.get("verdict") == 0 and o.get("budget", 0) >= LIMIT for o in observations)
        if prior_15m_unknown:
            continue
        parents = sorted(incidence.get(key, []))
        mask = key[0] | (key[1] << 64)
        if mask.bit_count() != 5 or board.canonical(mask) != mask:
            raise ValueError(f"noncanonical S5 candidate {key}")
        legal = board.legal(mask).bit_count()
        s6_children = {(x & ((1 << 64) - 1), x >> 64) for x in board.children(mask)}
        exact_s6 = {}
        for s6 in s6_children:
            h = history.get((6, *s6))
            if h and h.get("verdict") in (1, 2):
                exact_s6[s6] = int(h["verdict"])
        eligible.append({
            "key": key, "legal": legal, "parents": parents,
            "sharing": "shared" if len(parents) > 1 else "single",
            "saved_s6_exact_children": len(exact_s6),
            "saved_s6_win_children": sum(v == 1 for v in exact_s6.values()),
            "saved_s6_loss_children": sum(v == 2 for v in exact_s6.values()),
            "historical_s5_rows": len(observations), "historical_15m_unknown": False,
            "live_incidence": len(parents),
        })
    groups = {kind: sorted((r for r in eligible if r["sharing"] == kind), key=lambda r: (r["legal"], r["key"]))
              for kind in ("shared", "single")}
    if not eligible:
        raise ValueError("no eligible unresolved target children remain")
    batch_size = min(8, len(eligible))
    shared_count = min(len(groups["shared"]), batch_size // 2)
    single_count = min(len(groups["single"]), batch_size - shared_count)
    shared_count = min(len(groups["shared"]), batch_size - single_count)
    if shared_count + single_count < batch_size:
        single_count = min(len(groups["single"]), batch_size - shared_count)
    if shared_count > len(groups["shared"]) or single_count > len(groups["single"]) or shared_count + single_count != batch_size:
        raise ValueError(f"cannot form a {batch_size}-target batch: available shared/single={len(groups['shared'])}/{len(groups['single'])}")

    def pick_group(rows, count):
        if count == 0:
            return []
        n = len(rows)
        indexes = ([((n - 1) // 2)] if count == 1 else
                   sorted(set(round(i * (n - 1) / (count - 1)) for i in range(count))))
        chosen = [rows[i] for i in indexes]
        partial = [r for r in rows if r["saved_s6_exact_children"] > 0]
        if partial and not any(r["saved_s6_exact_children"] > 0 for r in chosen):
            replacement = partial[0]
            replace_at = max(range(len(chosen)), key=lambda i: (abs(chosen[i]["legal"] - replacement["legal"]), i))
            chosen[replace_at] = replacement
        unique = {tuple(r["key"]): r for r in chosen}
        if len(unique) != count:
            for r in rows:
                unique.setdefault(tuple(r["key"]), r)
                if len(unique) == count:
                    break
        chosen = list(unique.values())
        chosen.sort(key=lambda r: (r["legal"], r["key"]))
        return chosen

    selected_rows = pick_group(groups["shared"], shared_count) + pick_group(groups["single"], single_count)
    # Compute the established 15M-censored completion proxy for all 115 classes.
    ranking = []
    for parent in candidates:
        info = classes[parent]
        vals = [cache.get(ch, (0, 0))[0] for ch in info["children"]]
        unknown_children = sorted(ch for ch in info["children"] if cache.get(ch, (0, 0))[0] == 0)
        legals = [board.legal(ch[0] | (ch[1] << 64)).bit_count() for ch in unknown_children]
        estimated = sum(float(profile.get((n // 10) * 10, {"mean_truncated_nodes": LIMIT}).get("mean_truncated_nodes", LIMIT)) for n in legals)
        shared_unknown = sum(len(incidence.get(ch, [])) > 1 for ch in unknown_children)
        ranking.append({
            "key": list(parent), "coverage": sorted(info["coverage"]),
            "status": classes[parent]["status"], "s5_children": len(info["children"]),
            "s5_win": vals.count(1), "s5_loss": vals.count(2), "s5_unknown": vals.count(0),
            "legal_min": min(legals) if legals else None, "legal_max": max(legals) if legals else None,
            "unknown_active_incidence_sum": sum(len(incidence.get(ch, [])) for ch in unknown_children),
            "unknown_shared_with_other_live_classes": shared_unknown,
            "completion_15m_truncated_nodes_proxy": round(estimated),
            "full_remaining_coverage": set(remaining).issubset(info["coverage"]),
        })
    ranking.sort(key=lambda r: (r["status"] == "WIN", r["completion_15m_truncated_nodes_proxy"], -r["s5_loss"], r["key"]))
    target_rank = next(i + 1 for i, row in enumerate(ranking) if row["key"] == list(TARGET))

    batch = []
    for offset, row in enumerate(selected_rows, start=(number - 1) * 8):
        key = row["key"]
        input_path = EXP / f"input/s5-{offset:02}.csv"
        input_content = f"target,{offset},5,{key[0]},{key[1]},{row['legal']},0,0,0,0,0\n".encode("utf-8")
        freeze(input_path, input_content)
        batch.append({
            "sequence": offset, "key": list(key), "sharing": row["sharing"],
            "live_parent_count": row["live_incidence"], "live_parent_keys": [list(p) for p in row["parents"]],
            "legal": row["legal"], "historical_s5_rows": row["historical_s5_rows"],
            "historical_15m_unknown": False,
            "saved_s6_exact_children": row["saved_s6_exact_children"],
            "saved_s6_win_children": row["saved_s6_win_children"],
            "saved_s6_loss_children": row["saved_s6_loss_children"],
            "reason": (f"{row['sharing']}; legal-count quantile stratum; {row['live_incidence']} live parents; "
                       f"{row['saved_s6_exact_children']} saved exact S6 children; no S5 raw or prior 15M UNKNOWN"),
            "input_path": str(input_path.relative_to(ROOT)), "input_sha256": sha(input_path),
        })
    build = json.loads(BUILD.read_text(encoding="utf-8"))
    selection = {
        "schema": f"n11-s4-direct-s5-{word}-batch-selection-v1",
        "source_main_commit": first_selection["source_main_commit"],
        "target_s4": list(TARGET), "target_s4_children": 106,
        "classification": {
            "all_s4_classes": len(classes), "all_s4_status_counts": dict(sorted(counts.items())),
            "third_moves": len(full_coverage), "secured": len(secured), "remaining": remaining,
            "115_candidates": len(candidates), "115_candidate_status_counts": dict(sorted(candidate_status.items())),
            "active_unknown_classes_covering_both_remaining": len(active),
            "target_s4_children_now": {"LOSS": sum(cache.get(k, (0, 0))[0] == 2 for k in target_children),
                                        "WIN": sum(cache.get(k, (0, 0))[0] == 1 for k in target_children),
                                        "UNKNOWN": len(unresolved)},
            "target_s4_rank_by_15m_censored_completion_proxy": target_rank,
        },
        "sources": {
            "exact_cache": str(CURRENT.relative_to(ROOT)), "exact_cache_sha256": sha(CURRENT),
            "frontier": str(FRONTIER.relative_to(ROOT)), "frontier_sha256": sha(FRONTIER),
            "geometry": str(GEOMETRY.relative_to(ROOT)), "geometry_sha256": sha(GEOMETRY),
            "history": str(HISTORY.relative_to(ROOT)), "history_sha256": sha(HISTORY),
            "historical_cost_profile": str(PROFILE.relative_to(ROOT)), "historical_cost_profile_sha256": sha(PROFILE),
            "frontier_sha256": sha(frontier_path),
            "prior_run_manifest_sha256s": [sha(p) for p in prior_run_paths],
            "prior_selection_sha256s": [sha(p) for p in prior_selection_paths],
        },
        "cost_evaluation_prior_batches": {
            "batch_count": len(prior_runs), "targets": len(all_prior_runs),
            "total_nodes": sum(int(r["nodes"]) for r in all_prior_runs),
            "total_seconds": sum(float(r["elapsed_seconds"]) for r in all_prior_runs),
            "exact_loss": sum(r["verdict"] == "LOSS" for r in all_prior_runs),
            "exact_win": sum(r["verdict"] == "WIN" for r in all_prior_runs),
            "unknown": sum(r["verdict"] == "UNKNOWN" for r in all_prior_runs),
            "cold_direct_cost_note": "Cold process per root; UNKNOWN stayed out of exact cache. This observed aggregate is not a universal budget-cost claim.",
        },
        "selection_rule": f"up to eight target S5s; shared/single count {shared_count}/{single_count} based on available parent incidence; legal-count quantiles within each group; include partial exact S6 evidence if available; exclude prior exact roots and all prior >=15M UNKNOWN; no repeated UNKNOWN",
        "solver": {
            "frozen_build_manifest": str((EXP / "input/solver-build.json").relative_to(ROOT)),
            "build_manifest_sha256": sha(BUILD), "binary_path": build["binary_path"],
            "binary_sha256": build["binary_sha256"], "source_sha256": build["source_sha256"],
            "node_limit": LIMIT, "mode": "cold exact replay; one target per fresh process; profile off",
        },
        "selected": batch,
    }
    out_dir = EXP / ("output/new-ranking-after-batch" if number == 2 else f"output/new-ranking-after-batch-{number - 1:02}")
    out_dir.mkdir(parents=True, exist_ok=True)
    rank_doc = {
        "schema": "n11-s4-candidate-ranking-after-direct-batch-v1",
        "source_exact_cache_sha256": sha(CURRENT), "source_geometry_sha256": sha(GEOMETRY),
        "candidate_count": len(ranking), "candidate_status_counts": dict(sorted(candidate_status.items())),
        "remaining_moves": remaining, "ranking_model": "current exact S5 class status; capped completion proxy = sum historical legal-decile mean nodes for each unresolved S5; scheduling signal only, not a bound/probability",
        "historical_cost_profile_sha256": sha(PROFILE), "target_candidate_rank": target_rank,
        "candidates": ranking,
    }
    freeze(out_dir / "candidate-ranking.json", json_bytes(rank_doc))
    with (out_dir / "candidate-classes.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(ranking[0].keys()))
        writer.writeheader()
        for row in ranking:
            writer.writerow({**row, "key": f"{row['key'][0]}:{row['key'][1]}",
                             "coverage": ";".join(map(str, row["coverage"]))})
    selection_path = EXP / f"input/{word}-batch-selection.json"
    freeze(selection_path, json_bytes(selection))
    print(json.dumps({
        "target_status": classes[TARGET]["status"], "target_children": selection["classification"]["target_s4_children_now"],
        "target_rank": target_rank, "candidate_status": dict(candidate_status),
        "remaining_moves": remaining,
        "selected": [{"sequence": r["sequence"], "key": r["key"], "sharing": r["sharing"],
                      "legal": r["legal"], "saved_s6_exact_children": r["saved_s6_exact_children"],
                      "parents": r["live_parent_count"]} for r in batch],
        "ranking_sha256": sha(out_dir / "candidate-ranking.json"),
        "selection_sha256": sha(selection_path),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
