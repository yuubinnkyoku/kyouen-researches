#!/usr/bin/env python3
"""One board, matched stone/mobility/height counts, unbounded normal SG gap."""
from functools import lru_cache
import argparse
from itertools import combinations
import json
from math import comb
from pathlib import Path
import importlib.util
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
SPEC = importlib.util.spec_from_file_location('pivot_jump', ROOT / 'research/experiments/common-pivot-unbounded-one-move-jump-20261108/verify.py')
JUMP = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(JUMP)


def cliques(n, count):
    q, r = divmod(n, count); edges = []; selected = 0; offset = 0
    for i in range(count):
        size = q + (i < r)
        selected |= 1 << offset
        edges += [(1 << a) | (1 << b) for a, b in combinations(range(offset, offset + size), 2)]
        offset += size
    assert offset == n
    return tuple(sorted(edges)), selected


def maximum_set(k, offset=0):
    if k == 0:
        return 1 << offset
    size = 3 ** (k - 1)
    return maximum_set(k - 1, offset) | maximum_set(k - 1, offset + size)


def graph_audit(n, edges):
    closed = [1 << v for v in range(n)]
    for edge in edges:
        for v in range(n):
            if edge >> v & 1:
                closed[v] |= edge

    @lru_cache(None)
    def solve(active):
        children = [solve(active & ~closed[v]) for v in range(n) if active >> v & 1]
        lengths = tuple(sorted({1 + length for g, lengths in children for length in lengths})) if children else (0,)
        return JUMP.mex({g for g, lengths in children}), lengths

    result = solve((1 << n) - 1)
    return dict(grundy=result[0], maximum_remaining_moves=max(result[1]), terminal_length_support=result[1],
                states=solve.cache_info().currsize)


def matched_terminal_support(k):
    n, base = JUMP.cograph(k); a = 1 << k
    target = 4 * n + 1
    size, high = JUMP.cograph(k + 1)
    neighbors = [v for v in range(1, size) if (1 | 1 << v) in high]
    expanded = list(high)
    for v in range(size, target):
        expanded += [(1 << v) | (1 << u) for u in [0, *neighbors, *range(size, v)]]
    high = tuple(sorted(expanded))
    low = [edge << (copy * n) for copy in range(4) for edge in base]
    low += [(1 << u) | (1 << v) for u in range(2*n) for v in range(2*n, 4*n)]
    low += [(1 << (4*n)) | (1 << u) for u in range(4*n)]
    low = tuple(sorted(low))
    x = graph_audit(target, high); y = graph_audit(target, low)
    assert x['grundy'] == 2*a and y['grundy'] == 1
    assert x['terminal_length_support'] == y['terminal_length_support'] == tuple(range(1, 2*a+1))
    return dict(k=k, legal_points=target, high=x, low=y), (target, high, 2*a), (target, low, 1)


def geometric_pair():
    k = 1; n, high = JUMP.cograph(k); height = 1 << k
    low, low_selected = cliques(n, height)
    graph_edges = high + tuple(edge << n for edge in low)
    triples = tuple(1 | (edge << 1) for edge in graph_edges)
    points, anchors, expected = JUMP.GEOMETRY.realize(2 * n + 1, triples)
    actual = [quad for quad in combinations(range(len(points)), 4)
              if JUMP.GEOMETRY.BASE.independent_determinant([points[v] for v in quad]) == 0]
    assert actual == expected
    quads = [sum(1 << v for v in quad) for quad in actual]
    initial = sum(1 << v for v in anchors) | 1
    seeds = [initial | (low_selected << (n + 1)), initial | (maximum_set(k) << 1)]

    def safe(stones):
        return not any(stones & quad == quad for quad in quads)

    @lru_cache(None)
    def solve(stones):
        children = [solve(stones | (1 << v)) for v in range(len(points))
                    if not stones >> v & 1 and safe(stones | (1 << v))]
        return JUMP.mex({g for g, height in children}), max((height + 1 for g, height in children), default=0)

    records = []
    for seed, g in zip(seeds, (height, 0)):
        legal = [v for v in range(len(points)) if not seed >> v & 1 and safe(seed | (1 << v))]
        value, actual_height = solve(seed)
        assert safe(seed) and value == g and actual_height == height and len(legal) == n
        records.append(dict(occupied=[v for v in range(len(points)) if seed >> v & 1],
                            stone_count=seed.bit_count(), legal_points=legal, mobility=len(legal),
                            maximum_remaining_moves=actual_height, grundy=value))
    assert records[0]['stone_count'] == records[1]['stone_count']
    return dict(k=k, points=points, actual_quads=actual, quadruples_checked=comb(len(points), 4),
                states=records, game_states=solve.cache_info().currsize)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--matched-terminal-support', action='store_true')
    args = parser.parse_args()
    directory = Path(__file__).resolve().parent
    symbolic = []
    for k in range(1, 13):
        n = 3 ** k; height = 1 << k; q, r = divmod(n, height)
        high_edges = 3 ** (k - 1) * (3 ** k - 1)
        low_edges = r * comb(q + 1, 2) + (height - r) * comb(q, 2)
        symbolic.append(dict(k=k, board_points=2*n+1+high_edges+low_edges,
                             occupied_count=1+high_edges+low_edges+height,
                             mobility=n, maximum_remaining_moves=height, grundy_pair=[height, 0]))
    graph_records = []; raw_cases = []
    for k in range(1, 4):
        n, high = JUMP.cograph(k); height = 1 << k
        low, selected = cliques(n, height)
        independent = maximum_set(k)
        assert independent.bit_count() == height and not any(independent & e == e for e in high)
        assert selected.bit_count() == height and not any(selected & e == e for e in low)
        a = graph_audit(n, high); b = graph_audit(n, low)
        assert (a['grundy'], b['grundy']) == (height, 0)
        assert a['maximum_remaining_moves'] == b['maximum_remaining_moves'] == height
        graph_records.append(dict(k=k, legal_points=n, high=a, low=b))
        if k <= 2:
            raw_cases.extend([(n, high, height), (n, low, 0)])
    geometry = geometric_pair()
    strong = []
    if args.matched_terminal_support:
        for k in (1, 2):
            row, high, low = matched_terminal_support(k)
            strong.append(row)
            if k == 1:
                raw_cases.extend([high, low])
    compiler = shutil.which('g++')
    if not compiler:
        raise SystemExit('g++ is required')
    with tempfile.TemporaryDirectory(prefix='kyouen-matched-counts-') as scratch:
        temp = Path(scratch).resolve()
        assert temp.parent == Path(tempfile.gettempdir()).resolve()
        data = temp / 'cases.txt'; exe = temp / 'verify.exe'; values = temp / 'values.bin'
        data.write_text(str(len(raw_cases))+'\n'+'\n'.join(' '.join(map(str,[n,len(edges),*edges])) for n,edges,g in raw_cases)+'\n', encoding='ascii')
        cpp = ROOT / 'research/experiments/pure-triple-few-edge-grundy-20261107/independent.cpp'
        subprocess.run([compiler, '-std=c++17', '-O3', str(cpp), '-o', str(exe)], check=True)
        native = json.loads(subprocess.check_output([str(exe), str(data), str(values)], text=True))
        assert values.read_bytes() == bytes(g for n,edges,g in raw_cases)
    output = dict(audit='PASS', symbolic_audits=symbolic, graph_audits=graph_records, matched_terminal_support=strong,
                  cpp_safe_states=native['safe_states'], same_integer_board=geometry,
                  limitation='Specified finite integer-point boards; full square-grid version remains open.')
    target = directory / ('output/audit_terminal_support.json' if args.matched_terminal_support else 'output/audit.json')
    target.parent.mkdir(exist_ok=True)
    target.write_text(json.dumps(output, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k:v for k,v in output.items() if k not in ('symbolic_audits','same_integer_board')}, indent=2), flush=True)
    print(json.dumps(geometry['states'], indent=2), flush=True)


if __name__ == '__main__':
    main()
