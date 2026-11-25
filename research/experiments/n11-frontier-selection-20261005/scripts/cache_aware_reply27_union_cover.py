#!/usr/bin/env python3
"""Exact cache-aware reply=27 repair minimizing distinct uncached s5 roots.

Compared with cache_aware_reply27_cover.py, which minimizes the additive sum of
uncached children per selected s4 class, this formulation introduces one binary
variable per distinct uncached s5 root.  Selecting an s4 class forces every one
of its uncached s5 children into the target union.  The primary objective is the
size of that union; the secondary objective is the number of selected s4
classes.

Only exact cached WIN/LOSS verdicts are used.  Selected UNKNOWN classes remain
work targets, not certificates.
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

from dfpn_edge_classes import d4_canonical_key, legal_after  # noqa: E402

FIRST, R2 = 60, 27


import sys as _policy_sys
from pathlib import Path as _PolicyPath
_policy_sys.path.insert(0, str(_PolicyPath(__file__).resolve().parents[4] / 'research/experiments/n11-frontier-selection-20261005/scripts'))
from s5_evidence_policy import quarantined_cache_keys

def load_cache(path: Path):
    _s5_quarantine = quarantined_cache_keys()
    out = {}
    with path.open(newline="", encoding="utf-8") as fp:
        for row in csv.reader(fp):
            if not row or row[0].startswith("#"):
                continue
            if row[0] != "s5verdict":
                continue
            key = (int(row[1]), int(row[2]))
            if key in _s5_quarantine:
                continue
            verdict = int(row[4])
            if verdict not in (1, 2):
                raise SystemExit(f"UNKNOWN/invalid cache verdict {verdict}: {key}")
            old = out.get(key)
            if old is not None and old != verdict:
                raise SystemExit(f"CONFLICT key={key} old={old} new={verdict}")
            out[key] = verdict
    return out


def build():
    base = {FIRST, R2}
    verts = legal_after(base)
    groups = defaultdict(list)
    for a in verts:
        for b in legal_after(base | {a}):
            if b <= a:
                continue
            groups[d4_canonical_key([FIRST, R2, a, b])].append((a, b))
    assert len(verts) == 119
    assert len(groups) == 3384

    coverage = {
        key: {x for a, b in edges for x in (a, b)}
        for key, edges in groups.items()
    }
    children = {}
    for key, edges in groups.items():
        ss = set()
        for a, b in edges:
            occ = base | {a, b}
            for z in legal_after(occ):
                ss.add(d4_canonical_key(list(occ | {z})))
        children[key] = ss
    return set(verts), coverage, children


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--s5-cache", type=Path, required=True)
    ap.add_argument("--out", type=Path)
    ap.add_argument("--time-limit", type=float, default=None)
    args = ap.parse_args()

    cache = load_cache(args.s5_cache)
    verts, coverage, children = build()

    status = {}
    unknown_children = {}
    for key, ss in children.items():
        vals = [cache.get(ch, 0) for ch in ss]
        if 1 in vals:
            status[key] = "WIN"
        elif all(v == 2 for v in vals):
            status[key] = "LOSS"
        else:
            status[key] = "UNKNOWN"
            unknown_children[key] = {ch for ch in ss if ch not in cache}

    secured = set()
    loss_keys = []
    for key, s in status.items():
        if s == "LOSS":
            loss_keys.append(key)
            secured.update(coverage[key])
    uncovered = sorted(verts - secured)

    selected = []
    selected_targets = set()
    res = None

    if uncovered:
        candidates = sorted(
            key for key, s in status.items()
            if s == "UNKNOWN" and (coverage[key] & set(uncovered))
        )
        targets = sorted(set().union(*(unknown_children[k] for k in candidates)))
        vidx = {v: i for i, v in enumerate(uncovered)}
        tidx = {t: i for i, t in enumerate(targets)}
        nc = len(candidates)
        nt = len(targets)

        # Variables are [x_class..., y_target...].
        # Coverage: sum x_class >= 1 for every still-unsecured vertex.
        rows = []
        cols = []
        data = []
        for j, key in enumerate(candidates):
            for v in coverage[key]:
                if v in vidx:
                    rows.append(vidx[v])
                    cols.append(j)
                    data.append(1.0)
        A_cov = csc_matrix(
            (data, (rows, cols)),
            shape=(len(uncovered), nc + nt),
        )
        cov_constraint = LinearConstraint(
            A_cov,
            lb=np.ones(len(uncovered)),
            ub=np.full(len(uncovered), np.inf),
        )

        # Link: x_j <= y_t for every uncached child t required by class j.
        # Thus y is exactly the union indicator at optimum.
        lrows = []
        lcols = []
        ldata = []
        lr = 0
        for j, key in enumerate(candidates):
            for t in unknown_children[key]:
                lrows.extend((lr, lr))
                lcols.extend((j, nc + tidx[t]))
                ldata.extend((1.0, -1.0))
                lr += 1
        A_link = csc_matrix(
            (ldata, (lrows, lcols)),
            shape=(lr, nc + nt),
        )
        link_constraint = LinearConstraint(
            A_link,
            lb=np.full(lr, -np.inf),
            ub=np.zeros(lr),
        )

        # Lexicographic objective:
        # first minimize number of distinct target s5 roots, then class count.
        # BIG exceeds the maximum possible change in class count.
        big = nc + 1
        objective = np.concatenate(
            [np.ones(nc), np.full(nt, float(big))]
        )
        options = {"presolve": True, "mip_rel_gap": 0.0}
        if args.time_limit is not None:
            options["time_limit"] = args.time_limit

        res = milp(
            c=objective,
            constraints=[cov_constraint, link_constraint],
            integrality=np.ones(nc + nt),
            bounds=Bounds(0, 1),
            options=options,
        )
        if res.x is None or res.status != 0:
            raise SystemExit(
                "union MILP did not prove optimum: "
                f"status={res.status} gap={getattr(res, 'mip_gap', None)} "
                f"{res.message}"
            )

        selected = [
            candidates[j] for j in range(nc) if res.x[j] > 0.5
        ]
        selected_targets = set().union(
            *(unknown_children[k] for k in selected)
        ) if selected else set()

        # The explicit y solution and the reconstructed union must agree.
        y_count = sum(res.x[nc + i] > 0.5 for i in range(nt))
        assert y_count == len(selected_targets), (y_count, len(selected_targets))

    repaired = set(secured)
    for key in selected:
        repaired.update(coverage[key])
    assert repaired == verts

    hist = Counter(status.values())
    out = {
        "root": [FIRST, R2],
        "cache_entries": len(cache),
        "class_status_counts": dict(sorted(hist.items())),
        "secured_vertices": len(secured),
        "uncovered_vertices_before_repair": len(uncovered),
        "repair_classes": len(selected),
        "repair_unique_unknown_s5": len(selected_targets),
        "covered_vertices_after_repair": len(repaired),
        "milp_status": int(res.status) if res is not None else 0,
        "milp_gap": float(res.mip_gap) if res is not None else 0.0,
        "proved_loss_classes": [list(k) for k in sorted(loss_keys)],
        "repair_selected": [
            {
                "key": list(k),
                "coverage": sorted(coverage[k]),
                "uncached_s5": len(unknown_children[k]),
            }
            for k in selected
        ],
        "claim": (
            "exact optimization of distinct uncached s5 work targets; "
            "selected UNKNOWN classes are not certificates"
        ),
    }

    text = json.dumps(out, indent=2, sort_keys=True) + "\n"
    print(text, end="")
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding="utf-8")
    print("CACHE_AWARE_REPLY27_UNION_COVER_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
