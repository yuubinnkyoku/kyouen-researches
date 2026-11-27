# Quick check: is a dodecad a maximal cap of the W_24 s=7 game?
#
# The s=7 game allows at most 7 points of each octad in a position (a kyouen
# is a full octad).  A dodecad D meets every octad in 2, 4 or 6 points, so
# adding any outside point p keeps |D+{p} ∩ B| <= 7 for every octad B: D
# should have 12 legal moves, all leading to maximal 13-caps (G=0), hence
# Grundy(D) = mex{0} = 1 and D is NOT terminal.
#
# This contradicts the k=12 row of K1348 ("dodecad G=0 maximal terminal")
# and the parenthetical in the evidence of K1342.  Verified here directly
# with the exact ok_add rule of fullcheck.c.
import sys
from itertools import combinations
from functools import lru_cache

def load_board(path):
    with open(path) as f:
        vals = list(map(int, f.read().split()))
    n, nb = vals[0], vals[1]
    i, blocks = 2, []
    for _ in range(nb):
        k = vals[i]; i += 1
        blocks.append(sum(1 << p for p in vals[i:i+k])); i += k
    return n, blocks

def golay_span(blocks):
    piv = {}
    for b in blocks:
        x = b
        while x:
            hb = x.bit_length() - 1
            if hb in piv:
                x ^= piv[hb]
            else:
                piv[hb] = x
                break
    basis = [piv[h] for h in sorted(piv)]
    span = [0]
    for b in basis:
        span += [s ^ b for s in span]
    return span

def main():
    board = sys.argv[1]
    n, blocks = load_board(board)
    span = golay_span(blocks)
    weights = {}
    for w in span:
        weights[bin(w).count('1')] = weights.get(bin(w).count('1'), 0) + 1
    print('weight distribution', dict(sorted(weights.items())))
    dodecads = [w for w in span if bin(w).count('1') == 12]
    print('dodecads', len(dodecads))

    full = (1 << n) - 1

    def popcount(x):
        return bin(x).count('1')

    # per-point octad lists
    pc = [[b for b in blocks if b & (1 << p)] for p in range(n)]

    def ok_add(mask, p):
        for b in pc[p]:
            if popcount(mask & b) >= 7:
                return False
        return True

    memo = {}

    def grundy(mask):
        if mask in memo:
            return memo[mask]
        seen = set()
        for p in range(n):
            if mask & (1 << p):
                continue
            if ok_add(mask, p):
                seen.add(grundy(mask | (1 << p)))
        m = 0
        while m in seen:
            m += 1
        memo[mask] = m
        return m

    for dnum, D in enumerate(dodecads[:5]):
        prof = {}
        for b in blocks:
            c = popcount(D & b)
            prof[c] = prof.get(c, 0) + 1
        moves = [p for p in range(n) if not (D & (1 << p)) and ok_add(D, p)]
        children = sorted(set(bin(D | (1 << p)).count('1') for p in moves))
        g = grundy(D)
        print(f'dodecad #{dnum}: octad-intersection profile {dict(sorted(prof.items()))}, '
              f'legal moves {len(moves)} (child sizes {children}), Grundy {g}')

if __name__ == '__main__':
    main()
