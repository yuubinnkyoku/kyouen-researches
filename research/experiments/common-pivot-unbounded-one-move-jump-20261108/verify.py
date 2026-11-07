#!/usr/bin/env python3
"""Known cograph powers lifted to pure triples with an unbounded one-move increase."""
from functools import lru_cache
import argparse
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


GEOMETRY = module('jump_geometry', 'research/experiments/rank-three-residual-universality-20261107/verify.py')


def mex(values):
    answer = 0
    while answer in values:
        answer += 1
    return answer


def cograph(k):
    if k == 0:
        return 1, ()
    n, edges = cograph(k - 1)
    result = [edge << (copy * n) for copy in range(3) for edge in edges]
    result += [(1 << a) | (1 << b) for a in range(2 * n) for b in range(2 * n, 3 * n)]
    return 3 * n, tuple(sorted(result))


def graph_values(n, edges):
    closed = [1 << v for v in range(n)]
    for edge in edges:
        a = (edge & -edge).bit_length() - 1
        b = (edge ^ (1 << a)).bit_length() - 1
        closed[a] |= 1 << b
        closed[b] |= 1 << a

    @lru_cache(None)
    def game(active):
        return mex({game(active & ~closed[v]) for v in range(n) if active >> v & 1})

    active = (1 << n) - 1
    options = {game(active & ~closed[v]) for v in range(n)}
    return game(active), sorted(options), game.cache_info().currsize


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--with-free-geometry', action='store_true')
    args = parser.parse_args()
    directory = Path(__file__).resolve().parent
    # Symbolic option supports use only union/xor and join/union identities.
    value = 1; options = {0}; symbolic = []
    for k in range(13):
        assert value == 1 << k and options == set(range(1 << k))
        if k:
            n = 3 ** k; count = 3 ** (k - 1) * (3 ** k - 1)
            symbolic.append(dict(k=k, link_points=n, triple_edges=count, initial_grundy=1,
                                 after_pivot_grundy=1 << k, board_points=n + 1 + count,
                                 with_one_free_initial=0, with_one_free_after_pivot=(1 << k) ^ 1))
        next_options = options | {value ^ child for child in options}
        value = mex(next_options); options = next_options
    records = []; graph_audits = []; geometry = []
    for k in range(4):
        n, edges = cograph(k)
        g, moves, states = graph_values(n, edges)
        assert n == 3 ** k and g == 1 << k and moves == list(range(1 << k))
        assert len(edges) == (3 ** (k - 1) * (3 ** k - 1) if k else 0)
        graph_audits.append(dict(k=k, n=n, edge_count=len(edges), grundy=g, option_values=moves, active_states=states))
        if not 1 <= k <= 2:
            continue
        triples = tuple(1 | (edge << 1) for edge in edges)
        for free in (0, 1):
            records.append(dict(kind='before', k=k, n=n + 1 + free, edges=triples, grundy=1 ^ free))
            records.append(dict(kind='after', k=k, n=n + free, edges=edges, grundy=g ^ free))
        for free in ((0, 1) if args.with_free_geometry else (0,)):
            board = GEOMETRY.audit(n + 1 + free, triples)
            assert board['grundy'] == 1 ^ free and all(0 in quad for quad in board['actual_quads'])
            occupied = sum(1 << v for v in board['occupied']) | 1
            after = sorted((sum(1 << v for v in quad) & ~occupied) >> 1 for quad in board['actual_quads'])
            assert after == sorted(edges)
            board['k'] = k; board['free'] = free; board['after_pivot_grundy'] = g ^ free
            geometry.append(board)
            print(dict(k=k, free=free, graph_states=states, geometry_board_points=len(board['points'])), flush=True)
    compiler = shutil.which('g++')
    if not compiler:
        raise SystemExit('g++ is required')
    with tempfile.TemporaryDirectory(prefix='kyouen-pivot-jump-') as scratch:
        temp = Path(scratch).resolve()
        assert temp.parent == Path(tempfile.gettempdir()).resolve()
        data = temp / 'cases.txt'; exe = temp / 'verify.exe'; values = temp / 'values.bin'
        data.write_text(str(len(records)) + '\n' + '\n'.join(' '.join(map(str, [r['n'], len(r['edges']), *r['edges']])) for r in records) + '\n', encoding='ascii')
        cpp = ROOT / 'research/experiments/pure-triple-few-edge-grundy-20261107/independent.cpp'
        subprocess.run([compiler, '-std=c++17', '-O3', str(cpp), '-o', str(exe)], check=True)
        raw = json.loads(subprocess.check_output([str(exe), str(data), str(values)], text=True))
        assert values.read_bytes() == bytes(row['grundy'] for row in records)
    output = dict(audit='PASS', source='Bodlaender and Kratsch, Kayles and nimbers, Lemma 21',
                  source_url='https://webdoc.sub.gwdg.de/ebook/serien/ah/UU-CS/2000-42.pdf',
                  symbolic_audits=symbolic, graph_audits=graph_audits, records=records,
                  cpp_safe_states=raw['safe_states'], integer_realizations=geometry,
                  limitation='Specified finite integer-point boards with occupied anchors; not full square grids. Infinite claim follows by induction, not finite extrapolation.')
    target = directory / ('output/audit_with_free.json' if args.with_free_geometry else 'output/audit.json')
    target.parent.mkdir(exist_ok=True)
    target.write_text(json.dumps(output, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k:v for k,v in output.items() if k not in ('records','integer_realizations','symbolic_audits')}, indent=2), flush=True)


if __name__ == '__main__':
    main()
