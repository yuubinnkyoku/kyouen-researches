#!/usr/bin/env python3
"""Central-reply 19-root joint-plan refresh against the current chain cache.

Read-only planning/audit computation (no solver search, no new verdicts):

* frozen dependency graph geometry (n11-joint-s5-proof-planning-20261012
  output, Board-derived, cache-independent),
* the IF-ADOPTED scenario cache for the batch-12 (class 8106) n005/n006 what-if
  (2 WIN rows (n005 s5 188395, n006 s5 219608) only; Part Y canonical 95e868d6... plus the increment, sha256 below),
* the twenty-three update8 terminal/receipt S5 verdicts
  (research/experiments/n11-night-plan-update8-20261016 output).

For every S4 class of the frozen graph the refreshed status is recomputed from
`s4_cost` (its unknown children at graph-build time):
* a baseline-LOSS/UNKNOWN class counts as free coverage ONLY after the
  independent integer-geometry Board regenerates the class's FULL canonical
  S5 child boundary and every child is an exact LOSS in the merged chain
  cache (fail-closed; no reliance on the stale graph-time cache),
* any cost child that is a known WIN now marks the class excluded,
* still-unknown children are scheduling quantities only.

Outputs: refreshed per-root coverage, the frozen-update8-plan union refresh,
per-root and joint greedy remaining-requirement sizes, and a fail-closed
probing worklist.  No unknown verdict is asserted anywhere.  The standard
11x11 empty board and every one of the 19 central-reply roots stay UNKNOWN
unless and until the required S5 children are all exact LOSS.
"""
from __future__ import annotations

import csv
import gzip
import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
EXP = Path(__file__).resolve().parents[1]
GRAPH = ROOT / "research/experiments/n11-joint-s5-proof-planning-20261012/output/dependency-graph.json.gz"
CACHE = ROOT / "research/experiments/n11-centralreply-class8106-win-n005n006-ifadopted-20261122/pwin2/output/cache-pwin2-IFADOPTED.cache"
UPDATE8 = ROOT / "research/experiments/n11-night-plan-update8-20261016/output/repaired-joint-plan-update8.json"
BOARD_SOURCE = ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts/independent.py"
POLICY = ROOT / "research/experiments/n11-frontier-selection-20261005/scripts/s5_evidence_policy.py"
QUARANTINE = ROOT / "results/n11-s5-evidence-quarantine.json"

CACHE_SHA_EXPECTED = "c13f81d75f3837b1331f05742d046fac9ae3b3821c24ec26a311833ae4bbf986"
BOARD_SHA_EXPECTED = "954d3a104c1723ebb15b8c9bae63a4494f07f9eb73446a6d067c4fd6a4ba189f"
POLICY_SHA_EXPECTED = "78655e94480920de48a6fe8792e02e611513ddee7f685b422bbb2b08af5c95e2"
QUARANTINE_SHA_EXPECTED = "81d231604d3a095c115135e05ca393d6be83e1aadde4f614d3b5a9cc67d17fe9"


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    pins = {}
    for name, path in (("dependency_graph", GRAPH), ("merged_cache", CACHE),
                       ("update8_plan", UPDATE8), ("board_source", BOARD_SOURCE),
                       ("evidence_policy", POLICY), ("quarantine", QUARANTINE)):
        if not path.is_file():
            raise ValueError(f"missing pinned input {name}: {path}")
        pins[name] = {"path": str(path.relative_to(ROOT)), "sha256": sha(path)}
    if pins["merged_cache"]["sha256"] != CACHE_SHA_EXPECTED:
        raise ValueError("merged cache sha256 drift")
    if pins["board_source"]["sha256"] != BOARD_SHA_EXPECTED:
        raise ValueError("board source sha256 drift")
    if pins["evidence_policy"]["sha256"] != POLICY_SHA_EXPECTED:
        raise ValueError("evidence policy sha256 drift")
    if pins["quarantine"]["sha256"] != QUARANTINE_SHA_EXPECTED:
        raise ValueError("quarantine registry sha256 drift")

    sys.path.insert(0, str(BOARD_SOURCE.parent))
    sys.path.insert(0, str(POLICY.parent))
    from independent import Board          # noqa: E402
    from s5_evidence_policy import quarantined_cache_keys, is_canonical_safe_s5_key  # noqa: E402

    quarantined = quarantined_cache_keys()
    board = Board(11)

    with gzip.open(GRAPH, "rt", encoding="utf-8") as stream:
        g = json.load(stream)
    if g["counts"]["s4_classes_total"] != len(g["s4_masks"]) or len(g["s4_status"]) != len(g["s4_masks"]):
        raise ValueError("graph s4 arrays disagree")
    if len(g["s4_cost"]) != len(g["s4_masks"]):
        raise ValueError("graph s4 cost array disagrees")
    s4_masks = g["s4_masks"]
    s4_status = g["s4_status"]
    s4_cost = g["s4_cost"]
    roots = g["roots"]

    # --- merged chain cache -------------------------------------------------
    cache = {}
    with CACHE.open(encoding="utf-8-sig", newline="") as stream:
        for lineno, row in enumerate(csv.reader(stream), 1):
            if not row or row[0].lstrip().startswith("#"):
                continue
            if len(row) != 6 or row[0] != "s5verdict":
                raise ValueError(f"invalid cache row {lineno}: {row}")
            lo, hi, stones, verdict, nodes = map(int, row[1:])
            key = (lo, hi)
            if stones != 5 or verdict not in (1, 2) or nodes < 0:
                raise ValueError(f"invalid cache verdict at row {lineno}: {row}")
            if key in quarantined:
                raise ValueError(f"quarantined key inside merged cache: {key}")
            if key in cache and verdict != cache[key][0]:
                raise ValueError(f"cache conflict for {key}")
            cache[key] = (verdict, nodes)
    # geometry sanity: every cache row must be a canonical safe 5-stone key
    for key in cache:
        if not is_canonical_safe_s5_key(key):
            raise ValueError(f"noncanonical/unsafe cache key {key}")

    # --- update8 receipt verdicts ------------------------------------------
    update8 = json.loads(UPDATE8.read_text(encoding="utf-8"))
    if update8["schema"] != "n11-night-repaired-joint-plan-update8-v1":
        raise ValueError("update8 schema drift")
    if update8["union_size"] != 31859 or len(update8["required_new_s5"]) != 31859:
        raise ValueError("update8 baseline drift")
    if not update8["verification"]["passed"]:
        raise ValueError("update8 verification flag not passed")

    s5_masks = g["s5_masks"]
    mask_to_index = {(lo, hi): i for i, (lo, hi) in enumerate(s5_masks)}

    index_verdict = {}
    cache_in_universe = 0
    for (lo, hi), (verdict, _nodes) in cache.items():
        i = mask_to_index.get((lo, hi))
        if i is None:
            continue
        cache_in_universe += 1
        index_verdict[i] = verdict
    receipt_verdicts = {int(k): int(v) for k, v in update8["resolved_s5_verdicts"].items()}
    for i, v in receipt_verdicts.items():
        if not (0 <= i < len(s5_masks)):
            raise ValueError(f"receipt index outside universe: {i}")
        prior = index_verdict.get(i)
        if prior is not None and prior != v:
            raise ValueError(f"receipt/cache conflict at index {i}")
        index_verdict[i] = v

    def known(idx: int):
        return index_verdict.get(idx)

    # --- refresh every S4 class -------------------------------------------
    LOSS, UNKNOWN, EXCLUDED = 0, 1, -1
    classes = {}
    for i in range(len(s4_masks)):
        lo, hi = s4_masks[i]
        base = s4_status[i]
        cost = s4_cost[i]
        entry = {
            "class_index": i, "mask": [lo, hi], "base_status": base,
            "base_cost_size": len(cost), "cost_size_now": None,
            "unknown_now": None, "win_hit": False,
            "status_now": None, "board_verified_free": False,
        }
        if base == EXCLUDED:
            entry["status_now"] = "excluded"
            entry["unknown_now"] = []
            entry["cost_size_now"] = len(cost)
        elif base in (LOSS, UNKNOWN):
            unknown = []
            win_hit = False
            for j in cost:
                v = known(j)
                if v == 1:
                    win_hit = True
                elif v is None:
                    unknown.append(j)
            entry["win_hit"] = win_hit
            entry["unknown_now"] = unknown
            entry["cost_size_now"] = len(cost)
            if base == UNKNOWN:
                if win_hit:
                    entry["status_now"] = "excluded_now"
                elif not unknown:
                    entry["status_now"] = "free_now"
                else:
                    entry["status_now"] = "unknown"
            else:  # baseline LOSS
                entry["status_now"] = "excluded_now" if win_hit else "free_now"
        else:
            raise ValueError(f"unexpected base status {base} at class {i}")
        classes[i] = entry

    # --- Board fail-closed child verification for candidate free classes --
    def board_children_of_class(class_index: int):
        lo, hi = s4_masks[class_index]
        mask = lo | (hi << 64)
        children = board.children(mask)
        return children

    board_verified = set()
    board_rejected = {}
    free_candidates = [i for i, e in classes.items() if e["status_now"] == "free_now"]
    for i in free_candidates:
        lo, hi = s4_masks[i]
        if not is_canonical_safe_s5_key((lo, hi)):
            # a 4-stone class mask is not a 5-stone key; check safety directly
            try:
                board.legal(lo | (hi << 64))
            except ValueError:
                board_rejected[i] = "unsafe class mask"
                continue
        missing = []
        for child in board_children_of_class(i):
            key = (child & ((1 << 64) - 1), child >> 64)
            have = cache.get(key)
            if have is None:
                ci = mask_to_index.get(key)
                rv = receipt_verdicts.get(ci) if ci is not None else None
                if rv is None:
                    missing.append([key[0], key[1]])
                    continue
                have = (rv, 0)
            if have[0] != 2:
                missing.append([key[0], key[1]])
        if not missing:
            board_verified.add(i)
            classes[i]["board_verified_free"] = True
        else:
            board_rejected[i] = {
                "missing_or_nonloss_children": missing,
                "count": len(missing),
            }
            classes[i]["status_now"] = "free_now_unverified"
    # keep only Board-verified classes as free coverage
    for i, e in classes.items():
        if e["status_now"] == "free_now" and i not in board_verified:
            e["status_now"] = "free_now_unverified"

    # --- per-root coverage --------------------------------------------------
    root_rows = []
    per_root_groups = {}
    for r in roots:
        role = r["role"]
        free_thirds = 0
        groups = []
        for third in r["thirds"]:
            opts = third["options"]
            has_free = bool(opts) and any(classes[o]["board_verified_free"] for o in opts)
            best = None
            excluded_all = True
            for o in opts:
                e = classes[o]
                if e["status_now"] not in ("excluded", "excluded_now"):
                    excluded_all = False
                if e["board_verified_free"]:
                    continue
                remain = len(e["unknown_now"]) if e["unknown_now"] is not None else e["base_cost_size"]
                if best is None or remain < best[1]:
                    best = (o, remain)
            groups.append({
                "first": r["origin_first"], "reply": r["origin_reply"],
                "third": third["third"], "free": has_free,
                "best_option": None if best is None else best[0],
                "best_remaining": None if best is None else best[1],
                "excluded_all": excluded_all and bool(opts),
                "options": opts,
            })
            if has_free:
                free_thirds += 1
        row = {
            "origin_first": r["origin_first"], "role": role,
            "thirds": len(groups), "free_thirds_now": free_thirds,
            "groups": groups,
        }
        groups_for_plan = [x for x in groups if not x["free"]]
        row["uncovered"] = len(groups_for_plan)
        per_root_groups[r["origin_first"]] = groups_for_plan
        root_rows.append(row)

    # baseline root must still reproduce the published 119/119 coverage
    baseline_row = root_rows[0]
    if baseline_row["origin_first"] != 27 or baseline_row["free_thirds_now"] != 119:
        raise ValueError(
            "baseline root refresh mismatch: "
            f"{baseline_row['origin_first']} free={baseline_row['free_thirds_now']}")

    # --- per-root individual greedy requirement ----------------------------
    def greedy_union(groups, improve_passes=6):
        choice = {}
        union = set()
        for x in groups:
            best_o, best_add = None, None
            for o in x["options"]:
                e = classes[o]
                if e["board_verified_free"]:
                    best_o, best_add = o, 0
                    break
                remain = set(e["unknown_now"])
                add = len(remain - union)
                if best_add is None or add < best_add:
                    best_o, best_add = o, add
            choice[(x["first"], x["reply"], x["third"])] = best_o
            e = classes[best_o]
            if best_add:
                union |= set(e["unknown_now"])
        for _ in range(improve_passes):
            improved = False
            for x in groups:
                cur = choice[(x["first"], x["reply"], x["third"])]
                if classes[cur]["board_verified_free"]:
                    continue
                cur_set = set(classes[cur]["unknown_now"])
                rest = union - cur_set
                best_o, best_add = cur, len(cur_set - rest)
                for o in x["options"]:
                    e = classes[o]
                    if e["board_verified_free"]:
                        best_o, best_add = o, 0
                        break
                    alt_set = set(e["unknown_now"])
                    add = len(alt_set - rest)
                    if add < best_add:
                        best_o, best_add = o, add
                if best_o != cur:
                    choice[(x["first"], x["reply"], x["third"])] = best_o
                    union = rest | (set(classes[best_o]["unknown_now"] or []))
                    improved = True
            if not improved:
                break
        return choice, union

    per_root_plan = {}
    for r in root_rows:
        if r["role"] != "central":
            continue
        first = r["origin_first"]
        groups = per_root_groups[first]
        choice, union = greedy_union(groups)
        per_root_plan[first] = {
            "free_thirds": r["free_thirds_now"],
            "uncovered_thirds": len(groups),
            "greedy_union_size": len(union),
            "choice": {f"{k[2]}": v for k, v in choice.items()},
            "union_indices": sorted(union),
        }

    # --- joint greedy across all 19 roots (shared groups deduplicated) -----
    joint_groups = []
    seen = set()
    for r in root_rows:
        if r["role"] != "central":
            continue
        for x in r["groups"]:
            if x["free"]:
                continue
            key = (x["reply"], x["third"], tuple(x["options"]))
            if key in seen:
                continue
            seen.add(key)
            joint_groups.append(x)
    joint_choice, joint_union = greedy_union(joint_groups)
    joint_summary = {
        "unique_groups": len(joint_groups),
        "greedy_union_size": len(joint_union),
        "union_indices": sorted(joint_union),
    }

    # --- frozen update8 plan refresh ---------------------------------------
    frozen = {
        "total_groups": len(update8["groups"]),
        "union_size_baseline": update8["union_size"],
        "remaining_now": None,
        "win_hit_groups": [],
        "per_root_remaining": {},
    }
    frozen_remaining = set()
    frozen_by_root = defaultdict(int)
    frozen_free_now = 0
    for gr in update8["groups"]:
        idx = gr["s4_class_index"]
        if idx >= len(s4_masks):
            raise ValueError("update8 selected class outside graph")
        e = classes[idx]
        if e["status_now"] == "excluded_now":
            frozen["win_hit_groups"].append(gr)
            continue
        if e["board_verified_free"]:
            frozen_free_now += 1
            continue
        rem = set(e["unknown_now"])
        frozen_remaining |= rem
        frozen_by_root[str(gr["first"])] += len(rem)
    frozen["remaining_now"] = len(frozen_remaining)
    frozen["groups_free_now"] = frozen_free_now
    frozen["per_root_remaining"] = {k: v for k, v in sorted(frozen_by_root.items(), key=lambda kv: kv[1])}
    baseline_req = set(update8["required_new_s5"])
    resolved_in_baseline_req = sorted(baseline_req & set(index_verdict))
    frozen["resolved_among_baseline_requirement"] = resolved_in_baseline_req
    frozen["resolved_count"] = len(resolved_in_baseline_req)

    # --- profiling for the probing worklist ---------------------------------
    # group-closure view: for every non-free unique group, the option class with
    # the fewest still-unknown children is the cheapest certificate candidate
    # to close that third move completely.
    group_best = {}
    for x in joint_groups:
        best_o, best_r = None, None
        for o in x["options"]:
            e = classes[o]
            if e["board_verified_free"]:
                best_o, best_r = o, 0
                break
            if best_r is None or len(e["unknown_now"]) < best_r:
                best_o, best_r = o, len(e["unknown_now"])
        if best_r:
            group_best.setdefault((x["first"], x["reply"], x["third"]), best_o)

    # child -> classes still containing it in their unknown sets (membership)
    child_membership = defaultdict(list)
    for i, e in classes.items():
        if e["status_now"] == "unknown":
            for j in e["unknown_now"]:
                child_membership[j].append(i)

    # closure worklist: order candidate classes by remaining count, each closing
    # the group(s) it was chosen for; keys ordered by class then index.
    best_class_groups = defaultdict(list)
    for ident, best_o in group_best.items():
        best_class_groups[best_o].append({"first": ident[0], "third": ident[2]})
    worklist = []
    ranked = sorted(best_class_groups.items(), key=lambda kv: (len(classes[kv[0]]["unknown_now"]), -len(kv[1])))
    for class_index, served in ranked:
        e = classes[class_index]
        for j in sorted(e["unknown_now"]):
            lo, hi = s5_masks[j]
            mask = lo | (hi << 64)
            legal_moves = board.legal(mask)
            worklist.append({
                "probe_order": len(worklist) + 1,
                "s5_index": j, "lo": lo, "hi": hi,
                "legal": bin(legal_moves).count("1"),
                "serving_class": class_index,
                "class_unknown_now": len(e["unknown_now"]),
                "class_mask": s4_masks[class_index],
                "closure_candidates_served": sorted(served, key=lambda k: (k["first"], k["third"])),
                "membership_class_count": len(child_membership[j]),
            })
    closure_classes = [
        {"class_index": ci, "class_mask": s4_masks[ci],
         "unknown_now": len(classes[ci]["unknown_now"]),
         "groups_served": sorted(served, key=lambda k: (k["first"], k["third"]))}
        for ci, served in ranked
    ]

    # --- outputs ------------------------------------------------------------
    summary = {
        "schema": "n11-centralreply-19root-frontier-refresh-20261122-v1",
        "pins": pins,
        "inputs": {
            "graph_counts": g["counts"],
            "cache_rows": len(cache),
            "cache_verdicts": dict(Counter(v for v, _ in cache.values())),
            "update8_resolved_verdicts": receipt_verdicts,
            "cost_universe_masks": len(s5_masks),
            "cache_rows_in_universe": cache_in_universe,
            "known_universe_indices": len(index_verdict),
        },
        "class_status_counts": dict(Counter(e["status_now"] for e in classes.values())),
        "board_verification": {
            "free_candidates": len(free_candidates),
            "board_verified_free": len(board_verified),
            "rejected": {str(k): v for k, v in board_rejected.items()},
        },
        "roots": [
            {k: v for k, v in r.items() if k != "groups"} for r in root_rows
        ],
        "per_root_greedy": {
            str(first): {k: v for k, v in plan.items()
                         if k not in ("choice", "union_indices")}
            for first, plan in per_root_plan.items()
        },
        "joint_greedy": {k: v for k, v in joint_summary.items() if k != "union_indices"},
        "frozen_update8_refresh": frozen,
        "group_best_options_nonfree": len(group_best),
        "closure_classes_first": [c for c in closure_classes if c["unknown_now"] <= 12],
        "closure_classes_count": len(closure_classes),
        "worklist_first": worklist[:40],
        "worklist_total": len(worklist),
    }
    out = EXP / "output/refresh-summary.json"
    out.write_text(json.dumps(summary, indent=1, sort_keys=True), encoding="utf-8")

    with (EXP / "output/per-root-coverage.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["first", "role", "thirds", "free_now", "uncovered", "individual_greedy_union"])
        for r in root_rows:
            plan = per_root_plan.get(r["origin_first"], {})
            w.writerow([r["origin_first"], r["role"], r["thirds"], r["free_thirds_now"],
                        r["uncovered"], plan.get("greedy_union_size", "")])

    with (EXP / "output/closure-classes.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["class_rank", "class_index", "class_lo", "class_hi",
                    "unknown_now", "first_group_first", "first_group_third", "groups_served_count"])
        for rank, item in enumerate(closure_classes, 1):
            served = item["groups_served"]
            w.writerow([rank, item["class_index"], item["class_mask"][0], item["class_mask"][1],
                        item["unknown_now"], served[0]["first"] if served else "",
                        served[0]["third"] if served else "", len(served)])

    with (EXP / "output/probe-worklist.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["probe_order", "s5_index", "lo", "hi", "legal", "serving_class",
                    "class_unknown_now", "closure_first", "closure_third", "membership_class_count"])
        for item in worklist:
            served = item["closure_candidates_served"]
            w.writerow([item["probe_order"], item["s5_index"], item["lo"], item["hi"], item["legal"],
                        item["serving_class"], item["class_unknown_now"],
                        served[0]["first"] if served else "", served[0]["third"] if served else "",
                        item["membership_class_count"]])

    print(json.dumps({
        "class_status_counts": summary["class_status_counts"],
        "board_verification": summary["board_verification"],
        "roots": summary["roots"],
        "per_root_greedy": {str(k): v["greedy_union_size"] for k, v in per_root_plan.items()},
        "joint_greedy": {k: joint_summary[k] for k in ("unique_groups", "greedy_union_size")},
        "frozen_update8_refresh": {k: frozen[k] for k in
                                   ("union_size_baseline", "remaining_now", "groups_free_now",
                                    "resolved_count", "win_hit_groups")},
        "worklist_total": summary["worklist_total"],
        "group_best_options_nonfree": summary["group_best_options_nonfree"],
        "closure_classes_first": summary["closure_classes_first"],
    }, indent=1))


if __name__ == "__main__":
    main()
