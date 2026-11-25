#!/usr/bin/env python3
"""Compare full fixed-edge counts from adjacency and cycle-mask enumerators."""
from math import comb
from pathlib import Path
import json
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
SOURCES = ['enumerate_sparse_unpruned_n10.cpp', 'enumerate_sparse_masks_n10.cpp']


def run(binary, n, size):
    result = subprocess.run([str(binary), str(n), str(size)], check=True, capture_output=True, text=True)
    return dict(part.split('=', 1) for part in result.stdout.strip().split())


def main():
    with tempfile.TemporaryDirectory(prefix='c4-enumeration-audit-') as tmp:
        binaries = [Path(tmp)/f'program{i}' for i in range(2)]
        for source, binary in zip(SOURCES, binaries):
            subprocess.run(['g++', '-std=c++17', '-O3', '-Wall', '-Wextra', '-Werror',
                            str(HERE/source), '-o', str(binary)], check=True)
        cases = [(n,k) for n in (4,5,6) for k in range(2, n*(n-1)//2)] + [(7,8)]
        summary = []
        for n, size in cases:
            a, b = (run(program,n,size) for program in binaries)
            assert a['n'] == b['n'] == str(n) and a['edges'] == b['edges'] == str(size)
            assert a['fixed_edge'] == b['fixed_edge'] == '0-1'
            assert int(b['checked']) == comb(n*(n-1)//2-1, size-1)
            assert a['c4_free'] == b['c4_free'] and a['saturated'] == b['saturated']
            summary.append({'vertices':n, 'edges':size, 'checked':int(b['checked']),
                            'c4_free':int(a['c4_free']), 'saturated':int(a['saturated'])})
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
