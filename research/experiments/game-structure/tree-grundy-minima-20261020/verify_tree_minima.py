#!/usr/bin/env python3
"""Independent leaf-extension unlabeled-tree generator + C++ occupied-subset SG.
No third-party Python packages. Usage: python verify_tree_minima.py [max_n].
"""
import sys, json, subprocess, pathlib, tempfile
from collections import Counter


def canonical(adj):
    n = len(adj)
    degrees = [len(a) for a in adj]
    leaves = [i for i in range(n) if degrees[i] <= 1]
    left = n
    while left > 2:
        left -= len(leaves)
        nxt = []
        for v in leaves:
            for w in adj[v]:
                degrees[w] -= 1
                if degrees[w] == 1:
                    nxt.append(w)
        leaves = nxt

    def rooted(v, parent):
        return '(' + ''.join(sorted(rooted(w, v) for w in adj[v] if w != parent)) + ')'
    return min(rooted(c, -1) for c in leaves)


def main(max_n):
    here = pathlib.Path(__file__).resolve().parent
    binary = pathlib.Path(tempfile.gettempdir())/'kyouen_tree_occupied_mex_20261020'
    if not binary.exists():
        subprocess.run(['g++', '-std=c++17','-O3',str(here/'tree_occupied_mex.cpp'),'-o',str(binary)],check=True)
    trees = [(set(),)]
    stats, first = {}, {}
    for n in range(1, max_n+1):
        if n > 1:
            unique = {}
            for t in trees:
                for v in range(n-1):
                    child = tuple(set(s) for s in t) + ({v},)
                    child[v].add(n-1)
                    key = canonical(child)
                    if key not in unique:
                        unique[key] = child
            trees = list(unique.values())
        inp = ''.join(str(n)+' '+' '.join(str(sum(1<<j for j in a)) for a in t)+'\n' for t in trees)+'0\n'
        run = subprocess.run([str(binary)],input=inp,text=True,capture_output=True,check=True)
        values = [int(x) for x in run.stdout.split()]
        assert len(values) == len(trees)
        counts = Counter(values)
        for t,v in zip(trees,values):
            if v not in first:
                first[v] = {'n':n, 'edges':[[i,j] for i in range(n) for j in sorted(t[i]) if i<j], 'canonical':canonical(t)}
        stats[n] = {'total':len(trees), 'nimbers':dict(sorted(counts.items()))}
        print(n, stats[n], flush=True)
    result = {'method':'AHU leaf-extension generator + C++ occupied-subset mex', 'stats':stats, 'first':first}
    with open(here/'output/tree_minima_independent.json','w') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print('minima', {g:first[g]['n'] for g in sorted(first)})

if __name__ == '__main__':
    main(int(sys.argv[1]) if len(sys.argv)>1 else 15)
