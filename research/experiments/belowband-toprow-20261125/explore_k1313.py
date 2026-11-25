#!/usr/bin/env python3
"""K1313 pre-declaration exploration: T-BB, the TOP ROW of the below band
(k = z+n-3) for ALL n >= 2. Claim (single-coordinate collapse in (E, z)):

    u := E + z + n - 4
    H(S+k; X; z) = [E odd]  if u >= 1
                 = 2        if u == 0
                 = 1-[E odd] if u <= -1

with E := 2*max(X) - S (K1311 convention), the row k := z+n-3, covering
negative E for n >= 3 (E unbounded below), and for n=2 the single wall row
(z=0, k=-1). Waves (frozen; the declaration note SS3 quotes them):

  X1   n=3 top row full multiset census heaps<=9, z<=12 (negative E incl.).
  X2   n=2 top row k=z-1 (z>=1) + wall row (z=0,k=-1) pair census vs PB.
  X3   n=4..7 top row censuses (full small multisets + wide-E reps).
  X4   shape independence: same-(E,z) agreement across all census shapes.
  X5   far z: reps z<=26 across wide E (negative included).
  X6   typed self-check: children built ONLY from claim tables
       (PB for n>=2 heirs, published K0832 single-token closed form for
       n=1 heirs) -> mex == claim == engine, n=2..6.
  X7   cross-engine canonical vs ordered samples.
  X8   published anchors: n=2 beds E=0 (T-NCW-B transcribed constants),
       boundary-row T-DB (K1311 D-transcription) adjacency, L-SDB spot.
  X9   OBS-BBL watershed: K1311's frozen below-row naive-law mismatch
       reproduction + PB bad 0 on the same domain.
  X10  L-BR1: single-token packet-row law (x, Z>=1, R=x+Z-2) vs
       published closed form and both engines.
"""
import json
from itertools import combinations_with_replacement
from engine_block import H_canonical, H_ordered, single_token

def PB(n, E, z):
    u = E + z + n - 4
    if u >= 1:
        return E % 2
    if u == 0:
        return 2
    return 1 - (E % 2)

def E_of(X):
    return 2 * max(X) - sum(X)

def multisets(n, hi):
    return list(combinations_with_replacement(range(1, hi + 1), n))

def clear():
    H_canonical.cache_clear(); H_ordered.cache_clear()

def out_json(o):
    print(json.dumps(o, indent=1, sort_keys=True))

def main():
    out = []

    # X1 n=3 full census
    bad = 0; tot = 0
    for z in range(0, 13):
        for X in multisets(3, 9):
            S = sum(X); E = E_of(X)
            h = H_canonical(S + z, tuple(sorted(X, reverse=True)), z)
            tot += 1
            bad += 0 if h == PB(3, E, z) else 1
        clear()
    out.append(['X1-n3-full-census', tot, bad])

    # X2 n=2 census: k=z-1 for z>=1, and wall row z=0 -> k=-1
    bad = 0; tot = 0
    for z in range(0, 13):
        k = z - 1
        for a in range(1, 9):
            for g in range(0, 17):
                X = (a + g, a)
                if a + g > 24: continue
                h = H_canonical(2 * a + g + k, X, z)
                E = g
                tot += 1
                bad += 0 if h == PB(2, E, z) else 1
        clear()
    out.append(['X2-n2-census-kzm1-wall', tot, bad])

    # X3 n=4..7 censuses: full small + wide-E reps
    for n in (4, 5, 6, 7):
        bad = 0; tot = 0
        hi = {4: 7, 5: 6, 6: 5, 7: 5}[n]
        for z in range(0, 11):
            for X in multisets(n, hi):
                S = sum(X); E = E_of(X)
                h = H_canonical(S + z + n - 3, tuple(sorted(X, reverse=True)), z)
                tot += 1
                bad += 0 if h == PB(n, E, z) else 1
            clear()
        # wide-E reps at z<=10
        for z in range(0, 11):
            for E in range(2 - n - 6, 15):
                x1 = E + n - 1
                if x1 < 1: continue
                for X in (tuple(sorted([x1] + [1] * (n - 1), reverse=True)),
                          tuple(sorted([x1 + 1, 2] + [1] * (n - 2), reverse=True)),
                          tuple(sorted([max(x1, 3), 3, 2] + [1] * (n - 3), reverse=True))):
                    if min(X) < 1: continue
                    S = sum(X); E2 = E_of(X)
                    h = H_canonical(S + z + n - 3, X, z)
                    tot += 1
                    bad += 0 if h == PB(n, E2, z) else 1
            clear()
        out.append(['X3-n%d-census' % n, tot, bad])

    # X4 shape independence across censuses n=2..6
    viol = 0; checks = 0
    for n in (2, 3, 4, 5, 6):
        hi = {2: 12, 3: 8, 4: 6, 5: 5, 6: 5}[n]
        for z in range(0, 9):
            bucket = {}
            for X in multisets(n, hi):
                if sum(X) > 34: continue
                S = sum(X); E = E_of(X)
                h = H_canonical(S + z + n - 3, tuple(sorted(X, reverse=True)), z)
                if E in bucket and bucket[E] != h:
                    viol += 1
                bucket[E] = h
                checks += 1
            clear()
    out.append(['X4-shape-independence', checks, viol])

    # X5 far z wide E (reps), n=2..5, z<=26 (sparse shapes)
    bad = 0; tot = 0
    for n in (2, 3, 4, 5):
        for z in range(13, 27):
            for E in range(2 - n - 8, 10):
                x1 = E + n - 1
                if x1 < 1: continue
                for X in (tuple(sorted([x1] + [1] * (n - 1), reverse=True)),
                          tuple(sorted([x1 + 1, 2] + [1] * (n - 2), reverse=True))):
                    S = sum(X); E2 = E_of(X)
                    h = H_canonical(S + z + n - 3, X, z)
                    tot += 1
                    bad += 0 if h == PB(n, E2, z) else 1
            clear()
    out.append(['X5-far-z', tot, bad])

    # X6 typed self-check: children ONLY from claim tables + published
    # single-token closed form for n=1 heirs.
    def typed_children_values(n, X, z, k):
        """typed option VALUES, X descending tuple."""
        S = sum(X); R = S + k
        vals = set()
        x1 = X[0]
        tied = (n >= 2 and X[1] == x1)
        for i, v in enumerate(X):
            if v > 1:
                kid = tuple(sorted(X[:i] + (v - 1,) + X[i + 1:], reverse=True))
                if i == 0 and not tied:
                    # A-a: unique top reduce: (n, z, k, E-1)
                    vals.add(PB(n, E_of(kid), z))
                else:
                    # A-b: (n, z, k, E+1)
                    vals.add(PB(n, E_of(kid), z))
            else:
                # B: removal -> (n-1, plane z+1, same k), heir E+1
                kid = tuple(sorted(X[:i] + X[i + 1:], reverse=True))
                if n - 1 == 1:
                    xtok = kid[0]; Z = z + 1
                    vals.add(single_token(xtok, Z, R - 1))
                else:
                    vals.add(PB(n - 1, E_of(kid), z + 1))
        if z >= 1:
            # C: (n, z-1, k-1, same E)
            vals.add(1 ^ PB(n, E_of(X), z - 1))
        return vals

    tybad = 0; tot6 = 0; mexbad = 0
    for n in (2, 3, 4, 5, 6):
        hi = {2: 9, 3: 8, 4: 6, 5: 5, 6: 4}[n]
        for z in range(0, 9):
            for X in multisets(n, hi):
                if sum(X) > 30: continue
                S = sum(X); k = z + n - 3
                Xd = tuple(sorted(X, reverse=True))
                claim = PB(n, E_of(Xd), z)
                h = H_canonical(S + k, Xd, z)
                vals = typed_children_values(n, Xd, z, k)
                tot6 += 1
                # typed battery 1: mex of typed option values == claim
                m = 0
                s = set(vals)
                while m in s:
                    m += 1
                if m != claim:
                    mexbad += 1
                    if mexbad <= 5:
                        out.append(['X6-typemex-VIOL', n, z, list(X), claim, sorted(vals), m])
                # typed battery 2: engine value == claim (census, again, small)
                if h != claim:
                    tybad += 1
                    if tybad <= 5:
                        out.append(['X6-claim-VIOL', n, z, list(X), h, claim])
            clear()
    out.append(['X6-typed-self-check', tot6, tybad, mexbad])

    # X7 cross-engine
    xb = 0; tot = 0
    for n in (2, 3, 4):
        hi = {2: 10, 3: 7, 4: 6}[n]
        for z in (0, 3, 7, 11):
            for X in multisets(n, hi):
                S = sum(X); k = z + n - 3
                hc = H_canonical(S + k, tuple(sorted(X, reverse=True)), z)
                ho = H_ordered(S + k, tuple(sorted(X, reverse=True)), z)
                tot += 1
                xb += 0 if hc == ho else 1
            clear()
    out.append(['X7-cross-engine', tot, xb])

    # X8 published anchors
    # (a) n=2 beds E=0: transcribed T-NCW-B values on k=z-1 rows:
    #     z=1 -> 1, z=2 -> 2, z>=3 -> 0
    bad = 0
    for z in (1, 2, 3, 4, 5, 6):
        exp = {1: 1, 2: 2}.get(z, 0)
        for a in range(1, 10):
            X = (a, a)
            h = H_canonical(2 * a + z - 1, X, z)
            bad += 0 if h == exp else 1
        clear()
    out.append(['X8a-beds-ncwb', 54, bad])
    # (b) T-DB boundary-row adjacency (K1311 D transcription) k=z+n-2
    #     and PB at k=z+n-3: same cells must agree with respective laws.
    def D(g, p):
        if g <= p: return g % 2
        if g == p + 1: return 2
        return (g + 1) % 2
    bad = 0; tot = 0
    for n in (2, 3, 4):
        hi = {2: 8, 3: 7, 4: 6}[n]
        for z in range(0, 9):
            for X in multisets(n, hi):
                S = sum(X); E = E_of(X)
                Xd = tuple(sorted(X, reverse=True))
                hb = H_canonical(S + z + n - 2, Xd, z)   # boundary row
                ht = H_canonical(S + z + n - 3, Xd, z)   # top below row
                tot += 2
                bad += 0 if hb == D(E, z + n - 2) else 1
                bad += 0 if ht == PB(n, E, z) else 1
            clear()
    out.append(['X8b-db-adjacency', tot, bad])

    # X9 OBS-BBL watershed reproduction: triples k=z row, heaps<=8, S<=15,
    # z=1..7: naive D(E,z-1)/D(E,z) mismatch pairs + PB bad 0.
    res = []
    for z in range(1, 8):
        d = {}
        for X in multisets(3, 8):
            if sum(X) > 15: continue
        cells = [X for X in multisets(3, 8) if sum(X) <= 15]
        n1 = 0; n2 = 0; pb = 0
        for X in cells:
            S = sum(X); E = E_of(X)
            Xd = tuple(sorted(X, reverse=True))
            h = H_canonical(S + z, Xd, z)
            n1 += 0 if h == D(E, z - 1) else 1
            n2 += 0 if h == D(E, z) else 1
            pb += 0 if h == PB(3, E, z) else 1
        clear()
        res.append([z, len(cells), n1, n2, pb])
    out.append(['X9-obsbbl-watershed', res])

    # X10 L-BR1: single-token packet row law (x, Z>=1, R=x+Z-2)
    def PB1(x, Z):
        u = x + Z - 3
        if u >= 1: return x % 2
        if u == 0: return 2
        return 1 - (x % 2)
    bad = 0; tot = 0
    for x in range(1, 21):
        for Z in range(1, 16):
            R = x + Z - 2
            h = H_canonical(R, (x,), Z)
            st = single_token(x, Z, R)
            ho = H_ordered(R, (x,), Z)
            tot += 3
            bad += (0 if h == PB1(x, Z) else 1) + (0 if st == PB1(x, Z) else 1) + (0 if ho == PB1(x, Z) else 1)
        clear()
    out.append(['X10-lbr1', tot, bad])


    # X5b deep-negative-E families: all-equal & near-equal, z<=40
    bad = 0; tot = 0
    for n in (3, 4, 5):
        for a in range(1, 9):
            Xe = tuple(sorted([a] * n, reverse=True))
            Xn = tuple(sorted([a + 1] + [a] * (n - 1), reverse=True))
            for X in (Xe, Xn):
                for z in range(0, 41):
                    S = sum(X); E = E_of(X)
                    h = H_canonical(S + z + n - 3, X, z)
                    tot += 1
                    bad += 0 if h == PB(n, E, z) else 1
            clear()
    out.append(['X5b-deep-negE-families', tot, bad])

    out_json(out)

main()
