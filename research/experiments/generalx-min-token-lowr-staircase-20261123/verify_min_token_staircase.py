#!/usr/bin/env python3
"""
verify_min_token_staircase.py -- machine audit for the min-token staircase theorem.

THEOREM (min-token staircase, universal structural induction; see report.md):
  For every nonempty finite multiset X of positive integers, every z>=0,
  every 0<=R<=z+min(X):   H(R;X;z) = v(sum(X), z, R)   where v = single-token.

The universal claim rests on the written induction in report.md (Lemma Z +
option-set lifting). This machine provides: dual raw engines cross-checked
pointwise, Lemma Z exhaustives (raw + published closed form), theorem window
sweeps (exhaustive small + fixed-seed random deep), boundary+1 census, and
published witness anchors (K0832 sharpness, K1087, K1259, K1261, K1262).
Fail-closed: any bad point => rc=1. Deterministic output: sorted JSON.
--tamper runs the mutation battery (each mutation MUST be detected).
"""
import sys, json, hashlib, random, itertools
from functools import lru_cache

sys.setrecursionlimit(1_000_000)

def mex(values):
    values = set(values)
    m = 0
    while m in values:
        m += 1
    return m

# ------------------------------------------------------------------
# Raw engines (verbatim from the published K1138 verifier block; the same
# transcription is embedded in the published y22 machine K1257).
# ------------------------------------------------------------------
@lru_cache(maxsize=6_000_000)
def H_ordered(R, X, z):
    if R == 0:
        return 0
    opts = set()
    for i, v in enumerate(X):
        if v > 1:
            opts.add(H_ordered(R - 1, X[:i] + (v - 1,) + X[i + 1:], z))
        else:
            opts.add(H_ordered(R - 1, X[:i] + X[i + 1:], z + 1))
    if z >= 1:
        opts.add(1 ^ H_ordered(R - 1, X, z - 1))
    return mex(opts)

@lru_cache(maxsize=6_000_000)
def H_canonical(R, X, z):
    X = tuple(sorted(X, reverse=True))
    if R == 0:
        return 0
    opts = set()
    i = 0
    while i < len(X):
        v = X[i]
        if v > 1:
            child = tuple(sorted(X[:i] + (v - 1,) + X[i + 1:], reverse=True))
            opts.add(H_canonical(R - 1, child, z))
        else:
            child = tuple(sorted(X[:i] + X[i + 1:], reverse=True))
            opts.add(H_canonical(R - 1, child, z + 1))
        while i + 1 < len(X) and X[i + 1] == v:
            i += 1
        i += 1
    if z >= 1:
        opts.add(1 ^ H_canonical(R - 1, X, z - 1))
    return mex(opts)

def vC(x, z, R):  # canonical-engine single token
    return H_canonical(R, (x,), z)
def vO(x, z, R):  # ordered-engine single token
    return H_ordered(R, (x,), z)

# ------------------------------------------------------------------
# Published K0832 single-token closed form (transcription of the published
# single_token block in the y22 machine K1257; see report provenance).
# ------------------------------------------------------------------
def q_odd(k):
    return k if k % 2 else k - 1

def single_token(x, z, R):
    if R == 0 or x <= 0:
        return 0
    if z == 0:
        return min(R, x) % 2
    if z == x:
        if R % 2 and R <= 2 * x - 1:
            return 2
        if R % 2 == 0 and R <= x - 1:
            return 0
        return x % 2
    if 1 <= z <= x - 1:
        m = q_odd(z)
        if R <= m:
            return 2 if R % 2 else 0
        if m < R < x + z:
            return (R + z) % 2
        return x % 2
    if z >= x + 1:
        m = q_odd(x)
        if R <= m:
            return 2 if R % 2 else 0
        return x % 2
    raise ValueError((x, z, R))

SELF_SHA = hashlib.sha256(open(__file__, 'rb').read()).hexdigest()

def window_pts(bad, label):
    return {'bad': bad, 'label': label}

def check_C0(anchor_bad=None):
    # raw single-token engines vs published closed form
    bad1 = bad2 = pts = 0
    for x in range(1, 81):
        for z in range(0, 41):
            rmax = min(x + z + 2, 60)
            for R in range(0, rmax + 1):
                s = single_token(x, z, R)
                pts += 1
                if vC(x, z, R) != s: bad1 += 1
                if vO(x, z, R) != s: bad2 += 1
    return {'label': 'C0 raw-vs-closedform anchor', 'points': pts,
            'bad_canonical': bad1, 'bad_ordered': bad2}

def check_C1():
    # Lemma Z: v(x,z+1,n) == v(x,z,n) for 0<=n<=z. raw + closed-form grids.
    badR = ptsR = 0
    for x in range(1, 61):
        for z in range(1, 46):
            for n in range(0, z + 1):
                ptsR += 1
                if vC(x, z + 1, n) != vC(x, z, n): badR += 1
    badF = ptsF = 0
    for x in range(1, 301):
        for z in range(1, 151):
            for n in range(0, min(z, 60) + 1):
                ptsF += 1
                if single_token(x, z + 1, n) != single_token(x, z, n): badF += 1
    return {'label': 'C1 Lemma Z z-shift invariance', 'points_raw': ptsR, 'bad_raw': badR,
            'points_closedform': ptsF, 'bad_closedform': badF}

def check_C2():
    # exhaustive small multisets: tokens<=6, arity 1..4, z<=6, all R<=z+min
    bad = pts = 0
    for arity in range(1, 5):
        for xs in itertools.combinations_with_replacement(range(1, 7), arity):
            minX = min(xs); S = sum(xs)
            for z in range(0, 7):
                for R in range(0, z + minX + 1):
                    s = single_token(S, z, R)
                    gc = H_canonical(R, xs, z)
                    go = H_ordered(R, xs, z)
                    pts += 1
                    if gc != s or go != s or gc != go: bad += 1
    return {'label': 'C2 theorem exhaustive small', 'points': pts, 'bad': bad}

def check_C3(seed1=20261123, seed2=97):
    # fixed-seed random deep: arity 1..3 wide + arity 4..6 narrow; window + boundary census
    rng = random.Random(seed1)
    bad = pts = bnd_break = bnd_pts = 0
    for _ in range(350):
        arity = rng.randint(1, 3)
        xs = tuple(sorted(rng.randint(1, 22) for _ in range(arity)))
        z = rng.randint(0, 14); minX = min(xs); S = sum(xs)
        for R in range(0, z + minX + 2):
            s = single_token(S, z, R)
            gc = H_canonical(R, xs, z); go = H_ordered(R, xs, z)
            if gc != go: bad += 1
            if R <= z + minX:
                pts += 1
                if gc != s or go != s: bad += 1
            else:
                bnd_pts += 1
                if gc != s: bnd_break += 1
    rng2 = random.Random(seed2)
    for _ in range(120):
        arity = rng2.randint(4, 6)
        xs = tuple(sorted(rng2.randint(1, 9) for _ in range(arity)))
        z = rng2.randint(0, 6); minX = min(xs); S = sum(xs)
        for R in range(0, z + minX + 2):
            s = single_token(S, z, R)
            gc = H_canonical(R, xs, z); go = H_ordered(R, xs, z)
            if gc != go: bad += 1
            if R <= z + minX:
                pts += 1
                if gc != s or go != s: bad += 1
            else:
                bnd_pts += 1
                if gc != s: bnd_break += 1
    return {'label': 'C3 theorem random deep (fixed seed)', 'points_in_window': pts,
            'boundary_points': bnd_pts, 'boundary_breaks': bnd_break, 'bad': bad}

def check_C4():
    # two-token boundary census: y 1..8, x y..y+24, z 0..26:
    # R=z+y must equal; R=z+y+1 census of breaks.
    bad = pts = breaks = 0
    broke_at = {}
    for y in range(1, 9):
        for d in range(0, 25):
            x = y + d
            for z in range(0, 27):
                S = x + y
                Rh = z + y
                if H_canonical(Rh, (x, y), z) != single_token(S, z, Rh): bad += 1
                if H_ordered(Rh, (x, y), z) != single_token(S, z, Rh): bad += 1
                pts += 1
                Rb = z + y + 1
                if H_canonical(Rb, (x, y), z) != single_token(S, z, Rb):
                    breaks += 1
                    broke_at.setdefault(y, 0)
                    broke_at[y] += 1
    return {'label': 'C4 two-token boundary census', 'points': pts, 'bad': bad,
            'boundary_breaks': breaks, 'breaks_by_y': broke_at}

def check_C5():
    # published witness anchors (exact values from published K items)
    anchors = [
        # (X, z, R, expected_parent, expected_single, source)
        ((12, 6), 17, 24, 0, 1, 'K1087 z=17 witness'),
        ((12, 6), 18, 25, 0, 2, 'K1259 z=18 witness'),
        ((14, 6), 19, 26, 0, 1, 'K1261 z=19 witness'),
        ((16, 6), 20, 27, 2, 1, 'K1262 z=20 witness'),
        # sharpness of the staircase window (R=z+min+1 breaks; fromthis lane's pre-declaration probes)
        ((2, 1), 1, 3, 2, 0, 'staircase sharpness (2,1)'),
        ((1, 1, 1), 1, 3, 2, 0, 'staircase sharpness {1}^3'),
        ((2, 2), 2, 5, 2, 1, 'staircase sharpness (2,2)'),
        ((4, 3), 5, 9, 2, 0, 'staircase sharpness (4,3)'),
        ((4, 4), 6, 11, 2, 1, 'staircase sharpness (4,4)'),
        ((6, 5), 9, 15, 2, 0, 'staircase sharpness (6,5)'),
        ((6, 6), 10, 17, 2, 1, 'staircase sharpness (6,6)'),
    ]
    bad = pts = 0
    details = []
    for (X, z, R, ep, es, src) in anchors:
        xs = tuple(X)
        gc = H_canonical(R, xs, z); go = H_ordered(R, xs, z)
        s = single_token(sum(xs), z, R)
        pts += 2
        ok_p = (gc == ep and go == ep)
        ok_s = (s == es)
        if not ok_p or not ok_s: bad += 1
        # window boundary equality for the same family at R=z+min
        Rw = z + min(xs)
        eW = single_token(sum(xs), z, Rw)
        pts += 1
        if H_canonical(Rw, xs, z) != eW or H_ordered(Rw, xs, z) != eW: bad += 1
        details.append({'X': list(xs), 'z': z, 'R': R, 'parent': gc, 'single': s, 'src': src})
    return {'label': 'C5 published witness anchors', 'points': pts, 'bad': bad,
            'details': details}

def run_audit():
    res = {}
    res['C0'] = check_C0()
    H_ordered.cache_clear(); H_canonical.cache_clear()
    res['C1'] = check_C1()
    H_ordered.cache_clear(); H_canonical.cache_clear()
    res['C2'] = check_C2()
    H_ordered.cache_clear(); H_canonical.cache_clear()
    res['C3'] = check_C3()
    H_ordered.cache_clear(); H_canonical.cache_clear()
    res['C4'] = check_C4()
    H_ordered.cache_clear(); H_canonical.cache_clear()
    res['C5'] = check_C5()
    total_bad = 0
    totals = {}
    for k in sorted(res):
        v = res[k]
        b = sum(x2 for k2, x2 in v.items() if k2 == 'bad' or k2.startswith('bad_'))
        total_bad += b
        totals[k] = v.get('points') or (v.get('points_raw', 0) + v.get('points_closedform', 0)) or v.get('points_in_window', 0)
    res['meta'] = {
        'verifier_sha256': SELF_SHA,
        'total_bad': total_bad,
        'theorem': 'min-token staircase: H(R;X;z)=v(sum X,z,R) for all R<=z+min(X), all multisets, all z>=0',
        'proof': 'structural strong induction on R (report.md); lemma Z: v(x,z+1,n)=v(x,z,n) for n<=z',
    }
    return res, total_bad


# =====================================================================
# Tamper battery (--tamper): each mutation MUST produce at least one bad
# point. A missed mutation => TAMPER-MISSED => rc=1.
# =====================================================================
def _mex(vals):
    vals = set(vals); m = 0
    while m in vals: m += 1
    return m

@lru_cache(maxsize=2_000_000)
def H_ordered_noC(R, X, z):
    # T4: C-move removed from the ordered engine.
    if R == 0: return 0
    opts = set()
    for i, v in enumerate(X):
        if v > 1:
            opts.add(H_ordered_noC(R - 1, X[:i] + (v - 1,) + X[i + 1:], z))
        else:
            opts.add(H_ordered_noC(R - 1, X[:i] + X[i + 1:], z + 1))
    return _mex(opts)

def q_odd_mut(k):
    # T5: corrupted odd-rounding.
    return k if k % 2 else k + 1

def single_token_mut(x, z, R):
    if R == 0 or x <= 0: return 0
    if z == 0: return min(R, x) % 2
    if z == x:
        if R % 2 and R <= 2 * x - 1: return 2
        if R % 2 == 0 and R <= x - 1: return 0
        return x % 2
    if 1 <= z <= x - 1:
        m = q_odd_mut(z)
        if R <= m: return 2 if R % 2 else 0
        if m < R < x + z: return (R + z) % 2
        return x % 2
    if z >= x + 1:
        m = q_odd_mut(x)
        if R <= m: return 2 if R % 2 else 0
        return x % 2
    raise ValueError((x, z, R))

def tamper():
    results = []

    def rec(name, bad):
        results.append({'mutation': name, 'bad': bad})
        print(f"{'CAUGHT' if bad > 0 else 'TAMPER-MISSED'}: {name} bad={bad}")
        return bad

    total = 0
    # T1: window weakened to R<=z+min+1 -- counterexample must exist.
    bad = 0
    for y in range(1, 8):
        for d in range(0, 20):
            x = y + d
            for z in range(0, 20):
                if H_canonical(z + y + 1, (x, y), z) != single_token(x + y, z, z + y + 1):
                    bad += 1
    total += rec('T1 window+1 (R<=z+min+1 claimed)', bad)
    # T2: Lemma Z extended to n<=z+1 -- counterexample must exist.
    bad = 0
    for x in range(1, 30):
        for z in range(1, 25):
            for n in range(0, z + 2):
                if vC(x, z + 1, n) != vC(x, z, n): bad += 1
    total += rec('T2 Lemma Z range n<=z+1', bad)
    # T3: anchor expected value flip (K1259 single 2 -> 1).
    got = single_token(18, 18, 25)
    bad = 0 if got == 1 else 1  # flipped expectation must FAIL i.e. bad=1 detected
    if got == 2: bad = 1  # actual value is 2, the flip 1 mismatches -> caught
    total += rec('T3 K1259 anchor value flip', bad)
    # T4: C-move removed from ordered engine -- must disagree somewhere.
    bad = 0
    for z in range(1, 15):
        for R in range(1, z + 8):
            if H_ordered_noC(R, (3, 2), z) != H_canonical(R, (3, 2), z): bad += 1
    total += rec('T4 ordered engine without C-move', bad)
    # T5: corrupted q_odd in the closed form -- C0-style anchor must find bads.
    bad = 0
    for x in range(2, 60):
        for z in range(1, 40):
            for R in range(0, min(x + z + 1, 50) + 1):
                if single_token_mut(x, z, R) != vC(x, z, R): bad += 1
    total += rec('T5 corrupted q_odd closed form', bad)
    # T6: window defined with max(X) instead of min(X) -- counterexample must exist.
    bad = 0
    for xs in [((2, 1), 1), ((2, 1), 2), ((3, 1), 1), ((5, 2), 3), ((1, 1, 3), 1)]:
        X, z = xs
        mX = max(X)
        for R in range(0, z + mX + 1):
            if H_canonical(R, X, z) != single_token(sum(X), z, R): bad += 1
    total += rec('T6 max-token window', bad)
    # T7: boundary claimed to also collapse (R=z+y+1 always equal) -- breaks must exist.
    bad = 0
    for y in range(1, 8):
        for d in range(0, 20):
            for z in range(0, 20):
                if H_canonical(z + y + 1, (y + d, y), z) != single_token(2 * y + d, z, z + y + 1):
                    bad += 1
    total += rec('T7 boundary+1 claimed equal', bad)
    # T8: witness parent value flip ((4,3)@z=5 expected parent 2 -> 0).
    bad = 0 if H_canonical(9, (4, 3), 5) == 0 else 1
    total += rec('T8 staircase witness parent flip', bad)

    missed = [r['mutation'] for r in results if r['bad'] == 0]
    print('TAMPER BATTERY:', 'ALL CAUGHT' if not missed else 'MISSED: ' + str(missed))
    if missed:
        sys.exit(1)
    sys.exit(0)

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else 'audit'
    if mode == 'tamper':
        tamper()
        return
    if mode == 'audit':
        res, bad = run_audit()
        out = json.dumps(res, indent=1, sort_keys=True, ensure_ascii=True)
        with open('output/audit.json', 'w') as f:
            f.write(out + '\n')
        print(out)
        pts = 0
        for k in res:
            v = res[k]
            pts += v.get('points', 0) + v.get('points_raw', 0) + v.get('points_closedform', 0) + v.get('points_in_window', 0) + v.get('boundary_points', 0)
        print('TOTAL points checked:', pts)
        if bad: 
            print('AUDIT FAIL: bad =', bad)
            sys.exit(1)
        print('AUDIT PASS')
        sys.exit(0)

if __name__ == '__main__':
    main()
