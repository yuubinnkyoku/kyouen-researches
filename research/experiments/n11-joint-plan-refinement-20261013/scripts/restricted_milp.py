#!/usr/bin/env python3
"""Bounded exact minimum-union MILP on an explicitly restricted S4 pool.

An S5 used by only one candidate is folded into that candidate's integer
weight; an S5 used by multiple candidates has a shared binary union variable.
This contraction is exact within the saved candidate pool.  The restricted
optimum is an upper bound, never a lower bound for the full selection problem.
SciPy/HiGHS is a research-only optional system dependency, not a repo change.
"""
from collections import Counter
import argparse
import gzip
import json
from pathlib import Path
import sys
import time
import warnings

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import coo_matrix

sys.path.insert(0, str(Path(__file__).resolve().parent))
from refine_plan import ROOT, EXP, OLD, REPAIRED, CACHE, Instance, sha, verify_and_save, log


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, default=REPAIRED)
    parser.add_argument('--overlay', type=Path)
    parser.add_argument('--top', type=int, default=2)
    parser.add_argument('--seconds', type=float, default=60)
    parser.add_argument('--output', type=Path, default=EXP / 'output/restricted-milp-plan.json')
    args = parser.parse_args()
    began = time.time()
    with gzip.open(OLD / 'dependency-graph.json.gz', 'rt') as stream:
        graph = json.load(stream)
    plan = json.loads(args.input.read_text())
    verdicts = {int(i): v for i, v in plan['resolved_s5_verdicts'].items()}
    sources = {str(p.relative_to(ROOT)): sha(p) for p in (OLD / 'dependency-graph.json.gz', args.input, CACHE)}
    for relative, digest in plan['source_sha256'].items():
        assert sha(ROOT / relative) == digest
        sources[relative] = digest
    if args.overlay:
        overlay = json.loads(args.overlay.read_text())
        for i, value in overlay['resolved_s5_verdicts'].items():
            index = int(i)
            assert value in (1, 2) and 0 <= index < len(graph['s5_masks'])
            assert index not in verdicts or verdicts[index] == value
            verdicts[index] = value
        for relative, digest in overlay['source_sha256'].items():
            assert sha(ROOT / relative) == digest
            sources[relative] = digest
        sources[str(args.overlay.relative_to(ROOT))] = sha(args.overlay)
    inst = Instance(graph, verdicts)
    assign, union = inst.initial(plan['groups'])
    pool = set(assign[i] for i in inst.paid)
    for i in inst.paid:
        rankings = (
            lambda s: (len(inst.cost[s]) / len(inst.cover[s]), len(inst.cost[s]), s),
            lambda s: (len(inst.cost[s] - union) / len(inst.cover[s]), len(inst.cost[s]), s),
        )
        for rank in rankings:
            pool.update(sorted(inst.groups[i], key=rank)[:args.top])
    options = sorted(pool)
    degree = Counter(e for s in options for e in inst.cost[s])
    shared = sorted(e for e, count in degree.items() if count > 1)
    sindex = {s: i for i, s in enumerate(options)}
    eindex = {e: len(options) + i for i, e in enumerate(shared)}
    coefficients = np.zeros(len(options) + len(shared))
    for s in options:
        coefficients[sindex[s]] = sum(degree[e] == 1 for e in inst.cost[s])
    coefficients[len(options):] = 1
    rows, cols, values, lows, highs = [], [], [], [], []
    for i in inst.paid:
        row = len(lows)
        for s in inst.groups[i]:
            if s in pool:
                rows.append(row); cols.append(sindex[s]); values.append(1)
        lows.append(1); highs.append(np.inf)
    for s in options:
        for e in inst.cost[s]:
            if e in eindex:
                row = len(lows)
                rows.extend((row, row)); cols.extend((eindex[e], sindex[s])); values.extend((1, -1))
                lows.append(0); highs.append(np.inf)
    matrix = coo_matrix((values, (rows, cols)), shape=(len(lows), len(coefficients))).tocsc()
    assert matrix.shape[0] == len(inst.paid) + sum(degree[e] for e in shared)
    history = [{'phase': 'restricted_pool', 'initial_union': len(union),
                'candidate_s4': len(options), 'candidate_s5': len(degree),
                'shared_s5_variables': len(shared), 'variables': len(coefficients),
                'constraints': len(lows), 'top_per_ranking_per_group': args.top,
                'candidate_s4_indices': options}]
    log(f'MILP: {len(options)} candidate S4, {len(shared)} shared S5, {len(coefficients)} vars, {len(lows)} constraints')
    with warnings.catch_warnings():
        warnings.filterwarnings('ignore', message='Unrecognized options detected.*')
        result = milp(coefficients, integrality=np.ones(len(coefficients)),
                      bounds=Bounds(0, 1), constraints=LinearConstraint(matrix, lows, highs),
                      options={'time_limit': args.seconds, 'mip_rel_gap': 0, 'threads': 1,
                               'mip_max_nodes': 50000, 'presolve': True})
    history.append({'phase': 'milp', 'status': int(result.status), 'message': result.message,
                    'objective': None if result.fun is None else float(result.fun),
                    'restricted_dual_bound': float(getattr(result, 'mip_dual_bound', np.nan)),
                    'nodes': int(getattr(result, 'mip_node_count', 0)),
                    'seconds_total': round(time.time() - began, 3),
                    'scope': 'All objective and dual values apply only to the saved restricted candidate pool. Full-instance lower bound is unchanged.'})
    if result.x is not None:
        bits = np.rint(result.x).astype(int)
        assert np.max(np.abs(result.x - bits)) < 1e-5
        assert np.all(matrix @ bits >= np.array(lows))
        selected = {s for s in options if bits[sindex[s]]}
        out = list(assign)
        for i in inst.paid:
            feasible = selected.intersection(inst.groups[i])
            assert feasible
            out[i] = min(feasible, key=lambda s: (len(inst.cost[s]), s))
        candidate = inst.union(out)
        assert len(candidate) <= int(round(result.fun))
        log(f'MILP candidate union {len(candidate)} vs initial {len(union)}; restricted objective {result.fun}')
        if len(candidate) < len(union):
            assign, union = out, candidate
    history.append({'phase': 'selected', 'union_size': len(union)})
    args.output.parent.mkdir(parents=True, exist_ok=True)
    verify_and_save(inst, assign, union, sources, history, args.output)


if __name__ == '__main__':
    main()
