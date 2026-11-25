#!/usr/bin/env python3
"""K1312 (C-SUM tail) pre-declaration exploration: the multi-token C-SUM
tail collapse. (Header edited for the K1312 publication; the K1311 slot was
concurrently taken by the orthogonal boundary-band lane. Output bytes are
byte-identical to the original frozen run: see kit README.)

Waves (all frozen in explore_k1311.out; the declaration note SS3 quotes them):

  E1  T-CSUM census n=3: z0..12, tokens<=6, k=z+2..z+4 vs claim [S odd].
  E2  uniformity (engine-valued children, 1^ applied to the C option):
      n=3,4,5 in-region cells: set(children)=={1-[S odd]}.
  E3  T-CSUM census n=4 (z0..9, tokens<=5, k=z+3..z+5), n=5 (z0..7,
      tokens<=5, k=z+4..z+6), n=6 (z0..6, tokens<=4, k=z+5..z+6),
      n=7 (z0..5, tokens<=3, k=z+6..z+7), far n=3/n=4 spot boxes.
  E4  L-2 empty positions: H(R, (), z)==0 for R<=19, z<=9.
  E5  n=1 in-region uniformity incl. x=1 (removal->empty).
  E6  sharpness hunts at k=z+n-2: n=3 (z0..6, tokens<=9; full list),
      n=4 (z0..3, tokens<=10; full list), n=5 (z0..3, tokens<=8; full list),
      n=6 (z0..2, tokens<=12; full list), n=7 (z0..1, tokens<=14; capped).
  E7  near-threshold OBS: k=z+n-2 value distributions n=3 (z0..10,
      tokens<=6) and n=4 (z0..8, tokens<=5).
  E8  pure-family rows (a,...,a): n=3 z<=12 a<=9; n=4 z<=10 a<=9;
      n=5 z<=8 a<=8; k-offsets 0..n-1 vs [S odd] bad counts
      (the non-monotone pure stabilization pattern).
  E9  cross-engine canonical vs ordered samples (n=1..4).
"""
import json
from itertools import combinations_with_replacement
from engine_block import H_canonical, H_ordered, single_token

def multisets(n, hi):
    return list(combinations_with_replacement(range(1, hi + 1), n))

def clear():
    H_canonical.cache_clear(); H_ordered.cache_clear()

def engine_children_values(R, X, z):
    """Ground-truth option VALUES of H_canonical (mirrors engine code,
    1^ XOR applied to the C option)."""
    Xs = tuple(sorted(X, reverse=True))
    vals = set()
    i = 0
    while i < len(Xs):
        v = Xs[i]
        if v > 1:
            kid = tuple(sorted(Xs[:i] + (v - 1,) + Xs[i + 1:], reverse=True))
            vals.add(H_canonical(R - 1, kid, z))
        else:
            kid = tuple(sorted(Xs[:i] + Xs[i + 1:], reverse=True))
            vals.add(H_canonical(R - 1, kid, z + 1))
        while i + 1 < len(Xs) and Xs[i + 1] == v:
            i += 1
        i += 1
    if z >= 1:
        vals.add(1 ^ H_canonical(R - 1, Xs, z - 1))
    return vals

def main():
    out = []
    # E1 n=3 census
    nb = 0; tot = 0
    for z in range(0, 13):
        for X in multisets(3, 6):
            S = sum(X)
            for k in range(z + 2, z + 5):
                tot += 1
                nb += (0 if H_canonical(S + k, X, z) == S % 2 else 1)
        clear()
    out.append(['E1-n3-census', tot, nb])

    # E2 uniformity
    for (n, hi, zmax, koffs) in ((3, 5, 10, 3), (4, 4, 9, 3), (5, 3, 7, 3)):
        ub = 0; tot = 0
        for z in range(0, zmax + 1):
            for X in multisets(n, hi):
                S = sum(X)
                for k in range(z + n - 1, z + n - 1 + koffs):
                    tot += 1
                    vals = engine_children_values(S + k, X, z)
                    ub += (0 if vals == {1 - S % 2} else 1)
            clear()
        out.append(['E2-uniformity-n%d' % n, tot, ub])

    # E3 censuses n=4,5,6,7 + far boxes
    for (n, hi, zmax, koffs) in ((4, 5, 9, 3), (5, 5, 7, 3), (6, 4, 6, 2),
                                 (7, 3, 5, 2)):
        nb = 0; tot = 0
        for z in range(0, zmax + 1):
            for X in multisets(n, hi):
                S = sum(X)
                for k in range(z + n - 1, z + n - 1 + koffs):
                    tot += 1
                    nb += (0 if H_canonical(S + k, X, z) == S % 2 else 1)
            clear()
        out.append(['E3-n%d-census' % n, tot, nb])
    for (n, hi, zs) in ((3, 5, (15, 18, 21)), (4, 4, (15, 18))):
        nb = 0; tot = 0
        for z in zs:
            for X in multisets(n, hi):
                S = sum(X)
                for k in (z + n - 1, z + n):
                    tot += 1
                    nb += (0 if H_canonical(S + k, X, z) == S % 2 else 1)
            clear()
        out.append(['E3-far-n%d' % n, tot, nb])

    # E4 L-2
    bad = 0
    for R in range(0, 20):
        for z in range(0, 10):
            bad += (0 if H_canonical(R, (), z) == 0 else 1)
        clear()
    out.append(['E4-L2-empty', 200, bad])

    # E5 n=1 uniformity
    bad = 0; tot = 0
    for z in range(0, 9):
        for x in range(1, 11):
            for k in range(z, z + 4):
                R = x + k
                tot += 1
                vals = set()
                if x >= 2:
                    vals.add(H_canonical(R - 1, (x - 1,), z))
                else:
                    vals.add(H_canonical(R - 1, (), z + 1))
                if z >= 1:
                    vals.add(1 ^ H_canonical(R - 1, (x,), z - 1))
                bad += (0 if vals == {1 - x % 2} else 1)
        clear()
    out.append(['E5-n1-uniformity', tot, bad])

    # E6 sharpness hunts at k=z+n-2 (full frozen lists for n<=6)
    for (n, hi, zmax, cap) in ((3, 9, 6, None), (4, 10, 3, None),
                              (5, 8, 3, None), (6, 12, 2, None),
                              (7, 14, 1, 8)):
        tot = 0; cs = []
        for z in range(0, zmax + 1):
            for X in multisets(n, hi):
                S = sum(X)
                k = z + n - 2
                h = H_canonical(S + k, X, z)
                tot += 1
                if h != S % 2:
                    cs.append([list(X), z, k, h, S % 2])
            clear()
        out.append(['E6-n%d-sharp' % n, tot, len(cs),
                    (cs if cap is None else cs[:cap])])

    # E7 near-threshold OBS distributions
    for (n, hi, zmax) in ((3, 6, 10), (4, 5, 8)):
        dist = {}
        for z in range(0, zmax + 1):
            d = {}
            for X in multisets(n, hi):
                S = sum(X)
                h = H_canonical(S + z + n - 2, X, z)
                d[h] = d.get(h, 0) + 1
            dist[z] = d
            clear()
        out.append(['E7-n%d-z+n-2-dist' % n, dist])

    # E8 pure-family rows
    for (n, zmax, amax) in ((3, 12, 9), (4, 10, 9), (5, 8, 8)):
        res = {}
        for koff in range(0, n):
            nb = 0; tot = 0
            for z in range(0, zmax + 1):
                for a in range(1, amax + 1):
                    X = tuple([a] * n)
                    S = n * a
                    h = H_canonical(S + z + koff, X, z)
                    tot += 1
                    nb += (0 if h == S % 2 else 1)
            clear()
            res['koff%d' % koff] = [tot, nb]
        out.append(['E8-pure-n%d' % n, res])

    # E9 cross-engine
    xb = 0; tot = 0
    for (n, hi, zs) in ((3, 5, (0, 3, 7, 11)), (4, 4, (0, 4, 9)), (2, 6, (0, 5, 10))):
        for z in zs:
            for X in multisets(n, hi):
                S = sum(X)
                for k in (z + n - 1, z + n + 1):
                    hc = H_canonical(S + k, X, z)
                    ho = H_ordered(S + k, X, z)
                    tot += 1
                    xb += (0 if hc == ho else 1)
            clear()
    out.append(['E9-cross-engine', tot, xb])

    print(json.dumps(out, indent=1, sort_keys=True))

main()
