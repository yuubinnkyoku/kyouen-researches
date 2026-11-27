#!/usr/bin/env python3
"""Streaming two-edit surgery engine (q- and board-parameterized), v2.

Semantically identical candidate set to surgery_general.py (sha256
8ae82dde4b4959c1e0cfdc388f619d32508623befb29b0c91968bab25d3b6b6a):
S' = seed - R + A with |R| <= 2, |A| <= 2, final size <= |seed|, A disjoint
from seed minus R, in-board, T occupied or blocked in S'.

The published engine materializes the global candidate set in memory; on
8x26 q10 around the 71-stone m=25 seed that set (~5M pairs) exceeds the
sandbox memory budget (OOM kill). This v2 streams per-R: for each removal
set R the additions A are collected in a small per-R set (exact dedup,
since a duplicate (R, A) can only arise within the same R), checked, and
discarded. Global unique-candidate count = sum over R of |Aset(R)|, equal
to len(cands) of the published engine (calibration required to reproduce
the published 7x32 q6 counters exactly).

Further differences, all disclosed:
  - chunking partitions the sorted R list (not the global candidate list);
  - the --sample dump uses deterministic reservoir sampling over the
    stream (seed 20261127) instead of random.sample on a materialized list;
  - everything else (curve construction, safety/blocking thresholds,
    safe_and_max logic, output schema) is byte-for-byte the same code.

Exact Fraction arithmetic; no repo code; self-tests included.
"""
import json, itertools, time, os, sys, argparse
from math import gcd
from fractions import Fraction


def circum(a, b, c):
    ax, ay = a; bx, by = b; cx, cy = c
    d = 2*(ax*(by-cy) + bx*(cy-ay) + cx*(ay-by))
    if d == 0: return None
    a2, b2, c2 = ax*ax+ay*ay, bx*bx+by*by, cx*cx+cy*cy
    return (Fraction(a2*(by-cy) + b2*(cy-ay) + c2*(ay-by), d),
            Fraction(a2*(cx-bx) + b2*(ax-cx) + c2*(bx-ax), d))


def selftest():
    u = circum((0,0), (1,0), (0,1))
    assert u == (Fraction(1,2), Fraction(1,2)), u
    u2 = circum((0,2), (13,2), (12,3))
    assert u2 == (Fraction(13,2), Fraction(-7,2)), u2
    print("selftest PASS")


def build_curves(stones, BX, BY, S):
    curves = {}
    n = len(stones)
    for i, j in itertools.combinations(range(n), 2):
        a, b = stones[i], stones[j]
        A, B = b[1]-a[1], a[0]-b[0]
        C = -(A*a[0] + B*a[1])
        if A < 0 or (A == 0 and B < 0): A, B, C = -A, -B, -C
        g = gcd(gcd(abs(A), abs(B)), abs(C)) or 1
        curves[("L", A//g, B//g, C//g)] = None
    for i, j, k in itertools.combinations(range(n), 3):
        a, b, c = stones[i], stones[j], stones[k]
        if (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0]) == 0: continue
        u = circum(a, b, c)
        if u is None: continue
        r2 = (Fraction(a[0])-u[0])**2 + (Fraction(a[1])-u[1])**2
        curves[("C", u[0], u[1], r2)] = None
    out = []
    for key in curves:
        st_on = set(); full = []
        for x in range(BX):
            for y in range(BY):
                if key[0] == "L":
                    on = key[1]*x + key[2]*y + key[3] == 0
                else:
                    _, ux, uy, r2 = key
                    on = (Fraction(x)-ux)**2 + (Fraction(y)-uy)**2 == r2
                if on:
                    full.append((x, y))
                    if (x, y) in S: st_on.add((x, y))
        if len(st_on) >= 3:
            out.append((key, frozenset(st_on), frozenset(full)))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bx", type=int, required=True)
    ap.add_argument("--by", type=int, required=True)
    ap.add_argument("--q", type=int, required=True)
    ap.add_argument("--target", required=True)          # "x,y"
    ap.add_argument("--seed", required=True)           # json list of [x,y]
    ap.add_argument("--out", required=True)
    ap.add_argument("--chunk", default=None)           # "i:n" over the R list
    ap.add_argument("--sample", type=int, default=0)  # reservoir N (unchunked only)
    args = ap.parse_args()
    BX, BY, Q = args.bx, args.by, args.q
    T = tuple(int(v) for v in args.target.split(","))
    t0 = time.time()
    selftest()
    seed = [tuple(p) for p in json.load(open(args.seed))]
    S = set(seed)
    N = len(S)
    assert T not in S
    curves = build_curves(seed, BX, BY, S)
    by_c = {}
    for key, st_on, full in curves:
        by_c.setdefault(len(st_on), []).append((key, st_on, full))
    for c in sorted(by_c): print(f"curves c={c}: {len(by_c[c])}")
    assert max(by_c) <= Q - 1, "seed unsafe"
    board = [(x, y) for x in range(BX) for y in range(BY)]
    empty = [p for p in board if p not in S]
    assert T in empty and len(empty) == BX*BY - N

    # uncovered-cell census of the seed on this board (one-stone-short check)
    block_thr = Q - 1
    tab_all = {}
    for c in sorted(by_c):
        for key, st_on, full in by_c[c]:
            for p in full:
                tab_all.setdefault(p, []).append((len(st_on), st_on, full))
    uncovered = []
    for e in board:
        if e in S: continue
        if any(c >= block_thr for c, st_on, full in tab_all.get(e, ())):
            continue
        uncovered.append(e)
    print(f"seed uncovered cells on {BX}x{BY}: {sorted(uncovered)}")
    assert T in uncovered, "target must be unblocked in the seed"

    # T-curve census
    tcs = {}
    for c in (Q-3, Q-2):
        tcs[c] = [(k, s, f) for (k, s, f) in by_c.get(c, []) if T in f]
    print("T-curve census:", {f"c{k}": len(v) for k, v in sorted(tcs.items())})
    for c in sorted(tcs):
        for k, s, f in tcs[c]:
            print(f"  c{c} curve:", sorted(s), "empty_on:", len(f) - c - 1)

    # tables
    tabS = {}; tabB = {}; blockF = {}
    for c in sorted(by_c):
        for key, st_on, full in by_c[c]:
            for p in full:
                if c >= Q - 2: tabS.setdefault(p, []).append((st_on, full))
                if c >= Q - 3: tabB.setdefault(p, []).append((st_on, full))
                if c == Q - 1: blockF.setdefault(p, []).append(st_on)

    def cnt_on(st_on, full, R, A):
        return len(st_on - set(R)) + len(A & full)

    def safe_and_max(R, A):
        Rs = set(R)
        for z in A:
            for st_on, full in tabS.get(z, ()):
                if cnt_on(st_on, full, Rs, A) >= Q: return None
        Sp = (S - Rs) | set(A)
        for e in board:
            if e in Sp: continue
            blocked = False
            for st_on in blockF.get(e, ()):
                if not (st_on & Rs): blocked = True; break
            if blocked: continue
            for st_on, full in tabB.get(e, ()):
                if cnt_on(st_on, full, Rs, A) >= Q - 3: blocked = True; break
            if not blocked: return None
        return Sp

    Rsets = [(frozenset(p), len(p)) for p in
             [()] + [(a,) for a in seed] + list(itertools.combinations(seed, 2))]
    idx0, idx1 = 0, len(Rsets)
    if args.chunk:
        i, n = (int(v) for v in args.chunk.split(":"))
        assert not args.sample, "sample only supported unchunked"
        idx0 = i * len(Rsets) // n
        idx1 = (i + 1) * len(Rsets) // n
    reservoir = []
    K = args.sample
    rng_state = None
    if K:
        import random
        rng = random.Random(20261127)
        rng_state = rng
    total = 0
    witnesses = []; safe = 0
    for ridx in range(idx0, idx1):
        R, r = Rsets[ridx]
        if r == 0: continue
        Aset = set()
        def add(A, R=R, r=r, Aset=Aset):
            A = frozenset(A)
            if len(A) > 2 or len(A & (S - set(R))): return
            if N - len(R) + len(A) > N: return
            Aset.add(A)
        add([T])
        if r == 2:
            for w in empty:
                if w != T: add([T, w])
        for c in sorted(tcs):
            for key, st_on, full in tcs[c]:
                ec = [z for z in full if z not in st_on and z != T]
                t = len(set(R) & set(st_on))
                need = (Q - 1) - (c - t)
                if need <= 0 or need > 2: continue
                if need == 1:
                    for z in ec: add([z])
                    if r == 2:
                        for z in ec:
                            for w in empty:
                                if w != z: add([z, w])
                else:
                    if r == 2:
                        for z1, z2 in itertools.combinations(ec, 2):
                            add([z1, z2])
        for A in sorted(Aset):
            total += 1
            if rng_state is not None:
                item = (sorted(map(list, R)), sorted(map(list, A)))
                if total <= K:
                    reservoir.append(item)
                else:
                    j = rng_state.randrange(total)
                    if j < K: reservoir[j] = item
            Sp = safe_and_max(R, A)
            if Sp is None: continue
            safe += 1
            if len(witnesses) < 5:
                witnesses.append({"R": sorted(map(list, R)), "A": sorted(map(list, A)),
                              "stones": sorted(map(list, Sp))})
            print("WITNESS R=", sorted(map(list, R)), "A=", sorted(map(list, A)))
        if (ridx - idx0) % 256 == 255:
            print(f"progress R {ridx-idx0+1}/{idx1-idx0} total={total} safe={safe} [{time.time()-t0:.0f}s]", flush=True)
    print(f"checked={total} safe={safe} witnesses={len(witnesses)} [{time.time()-t0:.0f}s]")
    if K:
        with open(args.out + ".sample.jsonl", "w") as fh:
            for item in reservoir:
                fh.write(json.dumps({"R": item[0], "A": item[1]}) + "\n")
        print("wrote", args.out + ".sample.jsonl")
    out = {"seed": sorted(map(list, seed)), "target": list(T), "board": [BX, BY], "q": Q,
           "seed_uncovered": sorted(map(list, uncovered)),
           "tcurve_census": {f"c{c}": len(v) for c, v in sorted(tcs.items())},
           "engine": "TAMPER-T3b-weakened-max",
           "r_chunk": [idx0, idx1], "r_total": len(Rsets),
           "candidates_total": total, "chunk": args.chunk,
           "checked": total, "safe": safe, "witnesses": witnesses[:5], "witnesses_total_recorded": len(witnesses)}
    json.dump(out, open(args.out, "w"), indent=1)
    print("wrote", args.out)


if __name__ == "__main__":
    main()
