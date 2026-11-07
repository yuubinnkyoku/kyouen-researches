#!/usr/bin/env python3
"""Bounded complete one-edge augmentation of selected seven-edge cores."""
import argparse
from collections import Counter
from itertools import combinations
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--minimum-base-grundy', type=int, default=8)
    args = parser.parse_args()
    directory = Path(__file__).resolve().parent
    seven = ROOT / 'research/experiments/pure-triple-seven-edge-complete-20261108'
    rows = json.loads((seven / 'output/audit.json').read_text())['records']
    selected = [row for row in rows if row['grundy'] >= args.minimum_base_grundy]
    families = set()
    for row in selected:
        n = row['n']; base = tuple(sorted(row['edges']))
        for k in range(4):
            private = 3 - k
            for old in combinations(range(n), k):
                edge = sum(1 << v for v in old) + sum(1 << (n + j) for j in range(private))
                if edge in base:
                    continue
                edges = tuple(sorted(base + (edge,)))
                for free in (0, 1):
                    families.add((n + private + free, edges))
    cases = sorted(families)
    compiler = shutil.which('g++')
    if not compiler:
        raise SystemExit('g++ is required')
    with tempfile.TemporaryDirectory(prefix='kyouen-eight-augmentation-') as scratch:
        temp = Path(scratch).resolve()
        assert temp.parent == Path(tempfile.gettempdir()).resolve()
        data = temp / 'cases.txt'; cell = temp / 'cell.exe'; raw = temp / 'raw.exe'
        a = temp / 'cell.bin'; b = temp / 'raw.bin'; meta = temp / 'raw.json'
        data.write_text(str(len(cases)) + '\n' + '\n'.join(' '.join(map(str, [n, 8, *edges])) for n, edges in cases) + '\n', encoding='ascii')
        subprocess.run([compiler, '-std=c++17', '-O3', str(seven / 'cell_both.cpp'), '-o', str(cell)], check=True)
        first = json.loads(subprocess.check_output([str(cell), str(data), str(a)], text=True))
        print(first, flush=True)
        subprocess.run([compiler, '-std=c++17', '-O3', '-DMAX_LEGAL_POINTS=24', str(ROOT / 'research/experiments/common-pivot-misere-bound-20261108/independent.cpp'), '-o', str(raw)], check=True)
        subprocess.run([str(raw), str(data), str(b), str(meta)], check=True)
        values = a.read_bytes()
        assert values == b.read_bytes() and len(values) == 2 * len(cases)
        second = json.loads(meta.read_text())
    histogram = Counter((values[2*i], values[2*i+1]) for i in range(len(cases)))
    maximum = [max(pair[k] for pair in histogram) for k in (0, 1)]
    witnesses = {}
    for k, kind in enumerate(('normal', 'misere_aux')):
        indices = [i for i in range(len(cases)) if values[2*i+k] == maximum[k]]
        i = min(indices, key=lambda j: cases[j][0])
        n, edges = cases[i]
        witnesses[kind] = dict(n=n, edges=edges, normal=values[2*i], misere_aux=values[2*i+1])
    output = dict(audit='PASS', minimum_base_grundy=args.minimum_base_grundy, selected_base_types=len(selected),
                  cases=len(cases), cpp_cell_states=first['cell_states'], cpp_safe_states=second['safe_states'],
                  maximum_normal=maximum[0], maximum_misere_aux=maximum[1], witnesses=witnesses,
                  pair_histogram={f'{g},{h}': count for (g, h), count in sorted(histogram.items())},
                  limitation='Only one-edge extensions of selected seven-edge cores; not a complete eight-edge census.')
    target = directory / f'output/base_g{args.minimum_base_grundy}.json'
    target.parent.mkdir(exist_ok=True)
    target.write_text(json.dumps(output, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(output, indent=2), flush=True)


if __name__ == '__main__':
    main()
