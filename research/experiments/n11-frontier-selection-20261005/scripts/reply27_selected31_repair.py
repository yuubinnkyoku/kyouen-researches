#!/usr/bin/env python3
"""Repair the reply=27 frontier after the selected 31 classes were classified.

This is a scheduling/structure calculation, not a two-stone-root proof.
The selected-class verdict manifest contains 16 LOSS and 15 WIN classes.
Every child of a proved LOSS s4 class is therefore an exact LOSS s5, so those
children may be used as a derived cache.  The independently archived hard9
boundary cache contributes one exact WIN s5 and confirms eight hard LOSS s5.

The script rebuilds all 3,384 canonical s4 classes from board geometry, verifies
that the verdict manifest names exactly the previously selected 31 classes,
then solves three repair problems:
  1. minimum number of additional structurally usable classes;
  2. minimum additive number of still-uncached s5 children;
  3. minimum additive unknown-s5 work subject to exactly 15 repair classes.

The additive objectives are scheduling proxies.  UNKNOWN repair classes are not
certificates until their remaining s5 children are proved LOSS.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import csc_matrix, vstack

ROOT = Path(__file__).resolve().parents[4]
EDGE_DIR = ROOT / "research/experiments/n11-search-methods/scripts"
sys.path.insert(0, str(EDGE_DIR))

from dfpn_edge_classes import d4_canonical_key, forbidden, legal_after  # noqa: E402

HERE = Path(__file__).resolve().parents[1]
SELECTED = HERE / "output/reply27-direct-union-cover.json"
VERDICTS = HERE / "output/reply27-selected31-verdicts.json"
HARD9 = HERE / "output/reply27-hard9-s5.cache"
FIRST, R2 = 60, 27
V = 121


def load_hard9(path: Path):
    out = {}
    with path.open(newline="", encoding="utf-8") as fp:
        for row in csv.reader(fp):
            if not row or row[0].startswith("#"):
                continue
            if row[0] != "s5verdict":
                raise SystemExit(f"unexpected hard9 row: {row[:2]}")
            key = (int(row[1]), int(row[2]))
            value = int(row[4])
            if value not in (1, 2):
                raise SystemExit(f"invalid hard9 verdict {value}: {key}")
            old = out.get(key)
            if old is not None and old != value:
                raise SystemExit(f"HARD9 CONFLICT {key}: {old} vs {value}")
            out[key] = value
    return out


def build_geometry():
    base = {FIRST, R2}
    verts = [v for v in range(V) if v not in base]

    groups = defaultdict(list)
    coverage = defaultdict(set)
    for ia, a in enumerate(verts):
        for b in verts[ia + 1:]:
            if forbidden(FIRST, R2, a, b):
                continue
            key = d4_canonical_key([FIRST, R2, a, b])
            groups[key].append((a, b))
            coverage[key].update((a, b))

    assert len(verts) == 119
    assert sum(map(len, groups.values())) == 6871
    assert len(groups) == 3384

    children = {}
    for key, edges in groups.items():
        a, b = edges[0]
        occ = base | {a, b}
        children[key] = {
            d4_canonical_key(list(occ | {z}))
            for z in legal_after(occ)
        }
    return set(verts), groups, coverage, children


def solve_cover(uncovered, candidates, coverage, costs, exact_count=None):
    vidx = {v: i for i, v in enumerate(sorted(uncovered))}
    rows = []
    cols = []
    for j, key in enumerate(candidates):
        for v in coverage[key]:
            if v in vidx:
                rows.append(vidx[v])
                cols.append(j)
    A = csc_matrix(
        (np.ones(len(rows)), (rows, cols)),
        shape=(len(vidx), len(candidates)),
    )
    lb = np.ones(len(vidx))
    ub = np.full(len(vidx), np.inf)
    if exact_count is not None:
        A = vstack([A, csc_matrix(np.ones((1, len(candidates))))],
                   format="csc")
        lb = np.concatenate([lb, [exact_count]])
        ub = np.concatenate([ub, [exact_count]])

    res = milp(
        c=np.asarray(costs, dtype=float),
        constraints=LinearConstraint(A, lb=lb, ub=ub),
        integrality=np.ones(len(candidates)),
        bounds=Bounds(0, 1),
        options={"presolve": True, "mip_rel_gap": 0.0},
    )
    if res.x is None or res.status != 0:
        raise SystemExit(f"MILP failed: status={res.status} {res.message}")
    chosen = [candidates[i] for i, x in enumerate(res.x) if x > 0.5]
    return res, chosen


def decode_key(key):
    lo, hi = key
    pts = {p for p in range(64) if (lo >> p) & 1}
    pts.update(q + 64 for q in range(64) if (hi >> q) & 1)
    return pts


def exact_replay_row(tag, seq, key):
    legal = len(legal_after(decode_key(key)))
    return f"{tag},{seq},5,{key[0]},{key[1]},{legal},0,0,0,0,0\n"


def details(keys, coverage, children, derived_cache):
    out = []
    union = set()
    additive = 0
    for key in keys:
        unknown = {ch for ch in children[key] if ch not in derived_cache}
        union.update(unknown)
        additive += len(unknown)
        out.append({
            "key": list(key),
            "coverage": sorted(coverage[key]),
            "all_s5": len(children[key]),
            "unknown_s5": len(unknown),
        })
    return out, additive, len(union)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path)
    ap.add_argument("--targets-out", type=Path)
    ap.add_argument("--sample-out", type=Path)
    ap.add_argument("--sample-per-class", type=int, default=2)
    ap.add_argument("--extra-s5-cache", type=Path, action="append", default=[])
    args = ap.parse_args()

    selected_doc = json.loads(SELECTED.read_text(encoding="utf-8"))
    verdict_doc = json.loads(VERDICTS.read_text(encoding="utf-8"))
    selected = {tuple(x) for x in selected_doc["classes"]}
    status = {
        tuple(map(int, row["key"])): row["status"]
        for row in verdict_doc["classes"]
    }
    if set(status) != selected:
        raise SystemExit("selected verdict manifest does not match 31-class witness")
    counts = Counter(status.values())
    if counts != Counter({"LOSS": 16, "WIN": 15}):
        raise SystemExit(f"unexpected selected status counts: {counts}")

    verts, groups, coverage, children = build_geometry()
    if not selected <= set(groups):
        raise SystemExit("selected class key missing from regenerated geometry")

    selected_loss = {k for k, v in status.items() if v == "LOSS"}
    selected_win = {k for k, v in status.items() if v == "WIN"}

    # Every child of a proved LOSS s4 class is exact LOSS.
    derived_cache = {}
    for key in selected_loss:
        for child in children[key]:
            old = derived_cache.get(child)
            if old not in (None, 2):
                raise SystemExit(f"derived LOSS conflict: {child}")
            derived_cache[child] = 2

    hard9 = load_hard9(HARD9)
    for key, value in hard9.items():
        old = derived_cache.get(key)
        if old is not None and old != value:
            raise SystemExit(f"hard9/selected conflict {key}: {old} vs {value}")
        derived_cache[key] = value

    extra_entries = 0
    for extra_path in args.extra_s5_cache:
        extra = load_hard9(extra_path)
        for key, value in extra.items():
            old = derived_cache.get(key)
            if old is not None and old != value:
                raise SystemExit(
                    f"extra-cache conflict {key}: {old} vs {value}"
                )
            if old is None:
                extra_entries += 1
            derived_cache[key] = value

    # Propagate only verdicts justified by this derived cache.
    propagated = {}
    unknown_children = {}
    for key, ss in children.items():
        vals = [derived_cache.get(ch, 0) for ch in ss]
        if 1 in vals:
            propagated[key] = "WIN"
        elif vals and all(v == 2 for v in vals):
            propagated[key] = "LOSS"
        else:
            propagated[key] = "UNKNOWN"
            unknown_children[key] = {ch for ch in ss if ch not in derived_cache}

    # The manual selected WIN verdicts are also exact exclusions, even when
    # their particular winning s5 witness is not in the compact derived cache.
    loss_keys = {k for k, v in propagated.items() if v == "LOSS"} | selected_loss
    win_keys = {k for k, v in propagated.items() if v == "WIN"} | selected_win
    if loss_keys & win_keys:
        raise SystemExit("class verdict conflict")
    if len(loss_keys) != 16:
        raise SystemExit(f"expected 16 derived LOSS classes, got {len(loss_keys)}")

    secured = set()
    for key in loss_keys:
        secured.update(coverage[key])
    uncovered = verts - secured

    candidates = sorted(
        k for k in groups
        if k not in loss_keys and k not in win_keys and coverage[k] & uncovered
    )

    # Exact structural minimum number of additional classes.
    count_res, count_sel = solve_cover(
        uncovered, candidates, coverage,
        np.ones(len(candidates)),
    )

    # Scheduling optimum under additive unknown-s5 cost.
    additive_costs = [len(unknown_children[k]) for k in candidates]
    add_res, add_sel = solve_cover(
        uncovered, candidates, coverage, additive_costs,
    )
    add_detail, add_sum, add_union = details(
        add_sel, coverage, children, derived_cache
    )

    # Compare with the structurally minimal 15-class repair.
    fixed_res, fixed_sel = solve_cover(
        uncovered, candidates, coverage, additive_costs, exact_count=15,
    )
    fixed_detail, fixed_sum, fixed_union = details(
        fixed_sel, coverage, children, derived_cache
    )

    out = {
        "root": [FIRST, R2],
        "selected_status_counts": dict(sorted(counts.items())),
        "derived_s5_cache": {
            "entries": len(derived_cache),
            "extra_entries": extra_entries,
            "LOSS": sum(v == 2 for v in derived_cache.values()),
            "WIN": sum(v == 1 for v in derived_cache.values()),
        },
        "class_status_from_derived_cache_plus_manifest": {
            "LOSS": len(loss_keys),
            "WIN_forbidden": len(win_keys),
            "UNKNOWN": len(groups) - len(loss_keys) - len(win_keys),
        },
        "secured_vertices": len(secured),
        "uncovered_vertices": len(uncovered),
        "minimum_additional_classes": int(round(count_res.fun)),
        "minimum_additional_classes_mip_gap": float(count_res.mip_gap),
        "additive_optimum": {
            "repair_classes": len(add_sel),
            "additive_unknown_s5": add_sum,
            "unique_unknown_s5": add_union,
            "mip_gap": float(add_res.mip_gap),
            "selected": add_detail,
        },
        "exact_15_class_repair": {
            "repair_classes": len(fixed_sel),
            "additive_unknown_s5": fixed_sum,
            "unique_unknown_s5": fixed_union,
            "mip_gap": float(fixed_res.mip_gap),
            "selected": fixed_detail,
        },
        "claim": (
            "repair scheduling only; UNKNOWN selected repair classes are not "
            "certificates until their remaining s5 children are proved LOSS"
        ),
        "evidence_note": verdict_doc["sources"]["stage1"]["note"],
    }

    # Stable baseline regression values. Extra measured cache entries are
    # expected to change the scheduling optimum, so only the no-extra arm is
    # pinned to the original numbers.
    if not args.extra_s5_cache:
        assert len(derived_cache) == 1341
        assert sum(v == 2 for v in derived_cache.values()) == 1340
        assert sum(v == 1 for v in derived_cache.values()) == 1
        assert len(secured) == 62
        assert len(uncovered) == 57
        assert int(round(count_res.fun)) == 15
        assert len(add_sel) == 17
        assert add_sum == 1393
        assert add_union == 1375
        assert len(fixed_sel) == 15
        assert fixed_sum == 1471
        assert fixed_union == 1471

    repair_unknown = {
        key: sorted(ch for ch in children[key] if ch not in derived_cache)
        for key in add_sel
    }
    all_targets = sorted(
        set().union(*repair_unknown.values()),
        key=lambda key: (len(legal_after(decode_key(key))), key[1], key[0]),
    )
    if args.sample_per_class < 1:
        raise SystemExit("--sample-per-class must be >=1")
    sample_seen = set()
    sample = []
    for key in sorted(add_sel):
        ranked = sorted(
            repair_unknown[key],
            key=lambda ch: (len(legal_after(decode_key(ch))), ch[1], ch[0]),
        )
        for ch in ranked[:args.sample_per_class]:
            if ch not in sample_seen:
                sample_seen.add(ch)
                sample.append(ch)
    sample.sort(
        key=lambda key: (len(legal_after(decode_key(key))), key[1], key[0])
    )
    out["materialized_targets"] = len(all_targets)
    out["sample_targets"] = len(sample)
    out["sample_per_class"] = args.sample_per_class

    if args.targets_out:
        args.targets_out.parent.mkdir(parents=True, exist_ok=True)
        with args.targets_out.open("w", encoding="utf-8") as fp:
            for seq, key in enumerate(all_targets):
                fp.write(exact_replay_row("reply27-repair-s5", seq, key))
    if args.sample_out:
        args.sample_out.parent.mkdir(parents=True, exist_ok=True)
        with args.sample_out.open("w", encoding="utf-8") as fp:
            for seq, key in enumerate(sample):
                fp.write(exact_replay_row("reply27-repair-sample", seq, key))

    text = json.dumps(out, indent=2, sort_keys=True) + "\n"
    print(text, end="")
    print("REPLY27_SELECTED31_REPAIR_OK")
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
