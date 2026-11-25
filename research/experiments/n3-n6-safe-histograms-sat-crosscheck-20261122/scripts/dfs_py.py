#!/usr/bin/env python3
"""dfs_py.py — FRESH second implementation (Python) of the maximal-safe
configuration enumeration on the n x n standard kyouen board (q=4).

Written independently from the Node enum_catalog.mjs: same mathematical
semantics, own code line by line. Geometry source: the Leibniz-system
catalog text (quartets_nN.txt, produced by forbidgen.py and sha256-checked
against the published census.mjs machinery). This script never reads Node
outputs except for the external comparison step.

Two modes:
  maximal  : dfs_py.py <n> <k> <quartets.txt> <out_configs.csv> --maximal
      enumerate inclusion-maximal safe k-sets. Emits a one-line JSON summary
      (found, nodes, sha256 of the canonically sorted config list) and writes
      the sorted config list "a,b,..." one per line.
  safehist : dfs_py.py <n> <quartets.txt> --safehist
      walk the ENTIRE safe-prefix tree (no k bound) and histogram the sizes
      of ALL safe subsets, including the empty set (size 0).

Semantics (re-derived here from first principles):
  A cell c is PLACEABLE on a stone prefix P iff no forbidden quartet
  contains c together with three cells of P (cov[c] == 0, where cov counts
  per quartet the number of its three placed "other" cells).
  A k-set S is SAFE iff it can be built by cov==0 placements in ascending
  cell order (all quartets stay short of 4 stones); equivalently no
  forbidden quartet is a subset of S.
  S is MAXIMAL iff additionally every non-stone cell has cov > 0, i.e. it
  completes some quartet together with three stones of S (so it is
  unplaceable).
"""
import hashlib, json, sys


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
    """cell_cq[c] = list of (qi, other_three_cells_sorted)"""
    N = n * n
    cell_cq = [[] for _ in range(N)]
    for qi, (a, b, c, d) in enumerate(Q):
        for cell in (a, b, c, d):
            others = tuple(sorted(x for x in (a, b, c, d) if x != cell))
            cell_cq[cell].append((qi, others))
    return cell_cq


def maximal_mode(n, k, qtext, out_path):
    N = n * n
    Q = load_quartets(qtext)
    cell_cq = build_cell_quartets(n, Q)
    nq = len(Q)
    st = [0] * nq          # stones currently in each quartet
    cov = [0] * N          # missing-cell occupation count
    placed = [False] * N
    stones = []
    configs = []
    nodes = 0

    def dfs(start, depth):
        nonlocal nodes
        for c in range(start, N - (k - 1 - depth)):
            if cov[c]:
                continue
            nodes += 1
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
            if depth == k - 1:
                # maximal iff every non-stone cell is covered (cov > 0)
                if all(cov[x] > 0 for x in range(N) if not placed[x]):
                    configs.append(list(stones))
            else:
                dfs(c + 1, depth + 1)
            for o in deltas:
                cov[o] -= 1
            for qi, _ in cell_cq[c]:
                st[qi] -= 1
            stones.pop()
            placed[c] = False

    sys.setrecursionlimit(10000)
    dfs(0, 0)
    configs.sort()
    canon = '\n'.join(','.join(map(str, s)) for s in configs)
    h = hashlib.sha256(canon.encode()).hexdigest()
    with open(out_path, 'w') as f:
        f.write(canon + '\n')
    return {'n': n, 'k': k, 'mode': 'maximal', 'found': len(configs),
            'nodes': nodes, 'canonical_list_sha256': h}


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
    mode = sys.argv[-1]
    if mode == '--safehist':
        n = int(sys.argv[1]); qtext = sys.argv[2]
        print(json.dumps(safehist_mode(n, qtext)))
        return 0
    if mode == '--maximal':
        n = int(sys.argv[1]); k = int(sys.argv[2]); qtext = sys.argv[3]
        out = sys.argv[4]
        print(json.dumps(maximal_mode(n, k, qtext, out)))
        return 0
    print('usage: dfs_py.py <n> <k> <quartets.txt> <out.csv> --maximal | dfs_py.py <n> <quartets.txt> --safehist',
          file=sys.stderr)
    return 2


if __name__ == '__main__':
    sys.exit(main())
