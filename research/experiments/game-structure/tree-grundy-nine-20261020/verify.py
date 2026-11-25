#!/usr/bin/env python3
"""No third-party Python packages: leaf extension / AHU tree canonicalization.
Two independent C++ Grundy recurrences. Run from anywhere.
"""
from collections import Counter
from pathlib import Path
import json
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent


def canonical(adj):
    n = len(adj)
    deg = [len(a) for a in adj]
    leaves = [i for i in range(n) if deg[i] <= 1]
    left = n
    while left > 2:
        left -= len(leaves)
        nxt = []
        for v in leaves:
            for w in adj[v]:
                deg[w] -= 1
                if deg[w] == 1:
                    nxt.append(w)
        leaves = nxt

    def rooted(v, parent):
        return '(' + ''.join(sorted(rooted(w, v) for w in adj[v] if w != parent)) + ')'
    return min(rooted(c, -1) for c in leaves)


def compile_cpp(source, destination):
    subprocess.run(['g++', '-O3', '-std=c++17', str(HERE/source), '-o', str(destination)], check=True)


def main():
    with tempfile.TemporaryDirectory() as tmp:
        bins = [Path(tmp)/'occupied', Path(tmp)/'remaining']
        for src, binpath in zip(['occupied_mex.cpp', 'remaining_mex.cpp'], bins):
            compile_cpp(src, binpath)
        trees = [(set(),)]
        results = {}
        for n in range(1, 18):
            if n > 1:
                unique = {}
                for t in trees:
                    for v in range(n-1):
                        child = tuple(set(s) for s in t) + ({v},)
                        child[v].add(n-1)
                        unique.setdefault(canonical(child), child)
                trees = list(unique.values())
            data = ''.join(str(n)+' '+' '.join(str(sum(1<<j for j in a)) for a in t)+'\n' for t in trees)+'0\n'
            values = []
            for binary in bins:
                p = subprocess.run([str(binary)], input=data, text=True, capture_output=True, check=True)
                values.append([int(s) for s in p.stdout.split()])
            assert values[0] == values[1], f'Independent SG mismatch at n={n}'
            assert len(values[0]) == len(trees)
            counts = dict(sorted(Counter(values[0]).items()))
            results[n] = {'count':len(trees),'nimbers':counts}
            print(n, results[n], flush=True)
            if n == 17:
                i = values[0].index(9)
                t = trees[i]
                results[n]['witness9'] = [[v,w] for v in range(n) for w in sorted(t[v]) if v < w]
        assert results[16]['count'] == 19320
        assert results[17]['count'] == 48629
        assert 9 not in results[16]['nimbers']
        assert results[17]['nimbers'][9] == 47
        # Direct, third recurrence on the explicitly published 17-vertex witness.
        from functools import lru_cache
        edges = [(0,1),(0,9),(1,2),(2,3),(2,8),(3,4),(4,5),(4,7),
                 (5,6),(9,10),(10,11),(11,12),(11,15),(11,16),(12,13),(12,14)]
        adj = [0]*17
        for a,b in edges:
            adj[a] |= 1 << b
            adj[b] |= 1 << a
        @lru_cache(None)
        def grundy(rem):
            values = set()
            for v in range(17):
                if rem & (1 << v):
                    values.add(grundy(rem & ~(1 << v | adj[v])))
            mex = 0
            while mex in values:
                mex += 1
            return mex
        full = (1 << 17)-1
        children = [grundy(full & ~(1 << v | adj[v])) for v in range(17)]
        assert children == [1,2,0,5,4,3,8,3,7,0,1,0,5,3,3,6,6]
        assert grundy(full) == 9
        results[17]['published_witness9'] = {'edges':edges,'children':children}
        (HERE/'output'/'leaf_ahu.json').write_text(json.dumps(results,indent=2)+'\n')
        print('INDEPENDENT RECURRENCES AGREE; MINIMUM TREE NIMBER 9 ORDER = 17')

if __name__ == '__main__':
    main()
