#!/usr/bin/env python3
"""dfs_py.py — FRESH second implementation (Python) of the safe-subset size
histogram on the n x n standard kyouen board (q=4).

Mode:
  safehist : dfs_py.py <n> <quartets.txt> --safehist
      walk the ENTIRE safe-prefix tree (no k bound) and histogram the sizes
      of ALL safe subsets, including the empty set (size 0).

Semantics (re-derived here from first principles):
  A cell c is PLACEABLE on a stone prefix P iff no forbidden quartet
  contains c together with three cells of P (cov[c] == 0, where cov counts
  per quartet the number of its three placed "other" cells).
"""
import json, sys


def load_quartets(path):
    recs = []
    with open(path, encoding='utf8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('n='):
                continue
            a, b, c, d = (int(t) for t in line.split())
            assert a < b < c < d, line
            recs.append((a, b, c, d))
    return recs


def build_cell_quartets(n, Q):
    N = n * n
    cell_cq = [[] for _ in range(N)]
    for qi, (a, b, c, d) in enumerate(Q):
        for cell in (a, b, c, d):
            others = tuple(sorted(x for x in (a, b, c, d) if x != cell))
            cell_cq[cell].append((qi, others))
    return cell_cq


def safehist_mode(n, qtext):
    N = n * n
    Q = load_quartets(qtext)
    cell_cq = build_cell_quartets(n, Q)
    nq = len(Q)
    st = [0] * nq
    cov = [0] * N
    placed = [False] * N
    stones = []
    hist = {}

    def dfs(start):
        hist[len(stones)] = hist.get(len(stones), 0) + 1
        for c in range(start, N):
            if cov[c]:
                continue
            placed[c] = True
            stones.append(c)
            deltas = []
            for qi, others in cell_cq[c]:
                st[qi] += 1
                if st[qi] == 3:
                    for o in others:
                        if not placed[o]:
                            cov[o] += 1
                            deltas.append(o)
            dfs(c + 1)
            for o in deltas:
                cov[o] -= 1
            for qi, _ in cell_cq[c]:
                st[qi] -= 1
            stones.pop()
            placed[c] = False

    sys.setrecursionlimit(10000)
    dfs(0)
    return {'n': n, 'mode': 'safehist', 'safe_subset_histogram': hist,
            'total_safe_subsets': sum(hist.values()), 'max_safe_size': max(hist)}


def main():
    if sys.argv[-1] == '--safehist':
        n = int(sys.argv[1]); qtext = sys.argv[2]
        print(json.dumps(safehist_mode(n, qtext)))
        return 0
    print('usage: dfs_py.py <n> <quartets.txt> --safehist', file=sys.stderr)
    return 2


if __name__ == '__main__':
    sys.exit(main())
