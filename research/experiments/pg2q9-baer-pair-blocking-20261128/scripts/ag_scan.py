"""AG(2,q^2) restriction scan: can a Baer-pair union give an AG double
blocking smaller than the known 3q-1 bound?

For a Baer-pair union U in PG(2,q^2) and a choice of line at infinity l_inf,
the AG witness is U \\ l_inf; it AG-double-blocks iff every PG line L != l_inf
satisfies |U cap L| - [e(L) in U] >= 2, where e(L) is the point L cap l_inf.

Scans disjoint Baer pairs (double-blocking-safe) over sampled pairs, all
choices of l_inf, and reports the minimum feasible AG size found.
Discloses sample size. Definition-direct verification of any reported witness.
"""
import json, math, os, random, sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import baer as B

def main():
    q2 = 9
    board = B.build_pg(q2)
    q, check = B.verify_baer_base(board)
    base_mask = sum(1 << p for p in board['baer_base'])
    lineM = [sum(1 << p for p in L) for L in board['lines']]
    gens = B.generators(board)
    orbit = B.orbit_bfs(base_mask, gens)
    masks = sorted(orbit)
    N = len(masks)
    print(f'orbit {N}')
    # precompute per line: point list
    n = board['n']
    random.seed(20261129)
    # collect disjoint pairs by scanning with early stop at LIMIT
    LIMIT = int(sys.argv[1]) if len(sys.argv) > 1 else 3000
    pairs = []
    for i in range(N):
        if len(pairs) >= LIMIT:
            break
        for j in range(i + 1, N):
            if (masks[i] & masks[j]).bit_count() == 0:
                pairs.append((masks[i], masks[j]))
                if len(pairs) >= LIMIT:
                    break
    print(f'{len(pairs)} disjoint pairs collected')
    best = None  # (ag_size, umask, linf)
    for (A, Bm) in pairs:
        U = A | Bm
        for linf in range(n):
            linfM = lineM[linf]
            uinf = (U & linfM).bit_count()
            size = U.bit_count() - uinf
            if best is not None and size >= best[0]:
                continue
            ok = True
            for li in range(n):
                if li == linf:
                    continue
                t = (U & lineM[li]).bit_count()
                e_in_U = (U & lineM[li] & linfM).bit_count()
                if t - e_in_U < 2:
                    ok = False
                    break
            if ok and (best is None or size < best[0]):
                best = (size, U, linf)
                print(f'  new best AG size {size} (linf={linf}, uinf={uinf})')
    result = {'samples': len(pairs), 'best_ag_size': best[0] if best else None}
    if best:
        size, U, linf = best
        pts = sorted([k for k in range(n) if (U >> k) & 1 and not (lineM[linf] >> k) & 1])
        assert len(pts) == size
        # independent re-verification of the AG witness on the affine board
        aff_lines = [[p for p in L if p not in set(board['lines'][linf])]
                     for L in board['lines'] if L != board['lines'][linf]]
        sset = set(pts)
        assert all(len(sset.intersection(L)) >= 2 for L in aff_lines)
        result['ag_witness_points'] = pts
        result['linf'] = linf
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(os.path.join(root, 'out', 'ag_scan.json'), 'w') as f:
        json.dump(result, f, indent=1)
    print(json.dumps({k: v for k, v in result.items() if k != 'ag_witness_points'}))

if __name__ == '__main__':
    main()
