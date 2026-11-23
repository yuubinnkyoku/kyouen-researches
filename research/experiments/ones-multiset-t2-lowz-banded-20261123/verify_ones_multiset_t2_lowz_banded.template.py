#!/usr/bin/env python3
"""verify_ones_multiset_t2_lowz_banded.py -- machine audit for the
single-owner declaration
(research/log/2026-11-23-ones-multiset-t2-lowz-banded-single-owner-note.md,
commit pinned at publication):
(1) M1 / K1269 (proved, paper proof published in the unified-window report):
    for every t>=3, {1}^t separates at (z,R)=(1,3): parent H=2 vs single
    v(t,1,3)=0; t=2 collapses (0=0). Dedicated battery + chain anchors
    (a)-(e), t extended to 24 (published report covered t<=16).
    Cross-block: K1267 z=0 side parent-0/single-1 re-checked t=2..24.
(2) M2 / K1270 (proved, paper proof in the declaration note): low-z
    banded window extension, for every m>=2 and every finite multiset X
    with min(X)=m:
      (z=0 slice) H(m+1;X;0) == v(sumX,0,m+1)
      (z=1 slice) H(m+2;X;1) == v(sumX,1,m+2)
    i.e. exactly +1 past the unified window W(z,m)=max(z+m,2) on the
    z<=1 rows. Boundary sharpness re-checked against published anchors
    (min=1 separates at T1/T2; z=2,m=2 is frontier with published
    witness (2,2)@R*=5) and lemma LW (min=1, exactly one 1, budget 3
    at z=1 classification: {1}->1, sum>=3 ->2).
Fail-closed rules (rc=1 on any bad): banded-claim equalities vs both
engines and published closed form, window-edge equalities, engine
mutual agreement, published anchors, paper pre-registration values.
Beyond-window (W+2) evaluations are census records, NOT failures.
--tamper runs the mutation battery (each mutation MUST be caught).

Engines + closed form: byte-exact block machine-extracted from the
published unified-window verifier
(SHA-256 0ab66665dc9990f5399a661ccb2f9c3ba75f5a010c7e915f6a44e3d4fe6d3103;
see build_lowz_banded_verifier.py; sha-gated; provenance chain
K1138 -> y22 K1257 -> K1264 108fdd65... -> unified window 0ab66665... -> this).
"""
import sys, json, hashlib, random
from functools import lru_cache

sys.setrecursionlimit(1_000_000)

# === ENGINE BLOCK (machine-extracted from published unified-window machine) ===
<<<BLOCK>>>
# === END ENGINE BLOCK ===

SELF_SHA = hashlib.sha256(open(__file__, 'rb').read()).hexdigest()

def clear_engines():
    # value-transparent memo reset (bounds live cache entries; pure
    # deterministic recursion is unaffected) -- same convention as the
    # published unified-window machine.
    H_ordered.cache_clear()
    H_canonical.cache_clear()

# ------------------------------------------------------------------
# D0: closed form x dual-engine anchor grid
# ------------------------------------------------------------------
def check_D0():
    bad = pts = 0
    for x in range(1, 41):
        for z in range(0, 21):
            rmax = min(x + z + 2, 40)
            for R in range(0, rmax + 1):
                s = single_token(x, z, R)
                pts += 1
                if vC(x, z, R) != s: bad += 1
                if vO(x, z, R) != s: bad += 1
        clear_engines()
    return {'label': 'D0 closedform x dual-engine anchor grid',
            'points': pts, 'comparisons': pts * 2, 'bad': bad}

# ------------------------------------------------------------------
# D0b: published witness anchors (K1264 C5 x11 + K1265 D5 x6;
#      identical spec to the published unified-window E1)
# ------------------------------------------------------------------
ANCHORS = [
    ((12, 6), 17, 24, 0, 1),
    ((12, 6), 18, 25, 0, 2),
    ((14, 6), 19, 26, 0, 1),
    ((16, 6), 20, 27, 2, 1),
    ((2, 1), 1, 3, 2, 0),
    ((1, 1, 1), 1, 3, 2, 0),
    ((2, 2), 2, 5, 2, 1),
    ((4, 3), 5, 9, 2, 0),
    ((4, 4), 6, 11, 2, 1),
    ((6, 5), 9, 15, 2, 0),
    ((6, 6), 10, 17, 2, 1),
    ((1, 1), 0, 1, 1, 1),
    ((1, 1), 0, 2, 0, 0),
    ((1, 1, 1), 0, 3, 0, 1),
    ((1, 1), 1, 3, 0, 0),
    ((2, 1), 0, 3, 2, 1),
    ((2, 1), 1, 3, 2, 0),
]

def check_D0b():
    bad = comp = 0
    for (X, z, R, ep, es) in ANCHORS:
        xs = tuple(X)
        hc = H_canonical(R, xs, z); ho = H_ordered(R, xs, z)
        s = single_token(sum(xs), z, R)
        Rw = max(z + min(xs), 2)
        cw = single_token(sum(xs), z, Rw)
        comp += 5
        if hc != ho: bad += 1
        if hc != ep or ho != ep: bad += 1
        if s != es: bad += 1
        if H_canonical(Rw, xs, z) != cw or H_ordered(Rw, xs, z) != cw: bad += 1
    clear_engines()
    return {'label': 'D0b published witness anchors (17)',
            'comparisons': comp, 'bad': bad}

# ------------------------------------------------------------------
# D0c: declaration paper pre-registration values (from the note)
# ------------------------------------------------------------------
def check_D0c():
    bad = comp = 0
    def eq(a, b):
        nonlocal comp, bad
        comp += 1
        if a != b: bad += 1
    # multiset paper values (both engines + closed form)
    eq(H_canonical(3, (2, 2), 0), 1); eq(H_ordered(3, (2, 2), 0), 1)
    eq(single_token(4, 0, 3), 1)
    eq(H_canonical(6, (5, 5), 0), 0); eq(H_ordered(6, (5, 5), 0), 0)
    eq(single_token(10, 0, 6), 0)
    # corrected entry (honest record): the declaration pre-registered value 0
    # citing the K0832 band, but K0832 binds R<=2 only and R=3 is outside;
    # the true value is 2 via mex{B-child: v(2,1,2)=1, A-child: v(2,0,2)=0}.
    # Audit run 1 caught this as the only bad (D0c bad=2); the correction is
    # recorded in report.md / run log (pre-registration failure handling).
    eq(H_canonical(3, (1, 2), 0), 2); eq(H_ordered(3, (1, 2), 0), 2)
    eq(single_token(3, 0, 2), 0)
    eq(H_canonical(4, (2, 3), 1), 1); eq(H_ordered(4, (2, 3), 1), 1)
    eq(single_token(5, 1, 4), 1)
    eq(H_canonical(5, (3,), 1), 1); eq(H_ordered(5, (3,), 1), 1)
    eq(single_token(3, 1, 5), 1)
    eq(H_canonical(4, (2, 2), 1), 1); eq(H_ordered(4, (2, 2), 1), 1)
    eq(single_token(4, 1, 4), 1)
    eq(H_canonical(3, (1,), 1), 1); eq(H_ordered(3, (1,), 1), 1)
    # closed-form registration block (paper formulas in the note)
    for u in range(2, 26):
        eq(single_token(u, 0, 2), 0)
    for u in range(3, 41):
        eq(single_token(u, 1, 3), 0)
        eq(single_token(u - 1, 2, 2), 0)
        eq(single_token(u - 1, 1, 2), 1)
    for m in range(2, 26):
        eq(single_token(2 * m, 0, m + 1), (m + 1) % 2)  # sum>=2m witness
    clear_engines()
    return {'label': 'D0c declaration paper pre-registration values',
            'comparisons': comp, 'bad': bad}

# ------------------------------------------------------------------
# D1: M1/K1269 battery (z=1,R=3) t=2..24 + K1267 cross (z=0,R=3)
#     + proof chain anchors (a)-(e)
# ------------------------------------------------------------------
def check_D1():
    bad = comp = 0
    rec = []
    for t in range(2, 25):
        xs = tuple([1] * t)
        hc = H_canonical(3, xs, 1); ho = H_ordered(3, xs, 1)
        s = single_token(t, 1, 3)
        exp = 2 if t >= 3 else 0
        comp += 4
        if hc != ho: bad += 1
        if hc != exp: bad += 1
        if ho != exp: bad += 1
        if s != 0: bad += 1
        # K1267 cross-check at (z=0, R=3): parent 0 vs single 1 (t>=3)
        hc0 = H_canonical(3, xs, 0); ho0 = H_ordered(3, xs, 0)
        s0 = single_token(t, 0, 3)
        comp += 4
        if hc0 != ho0: bad += 1
        if hc0 != 0 or ho0 != 0: bad += 1
        if s0 != (1 if t >= 3 else 0): bad += 1
        rec.append({'t': t, 'parent_z1': hc, 'single_z1': s,
                    'parent_z0': hc0, 'single_z0': s0})
    # (a) H(1;{1}^j;z)=2 for j>=1, z>=2
    for j in range(1, 13):
        for z in range(2, 15):
            hc = H_canonical(1, tuple([1] * j), z)
            ho = H_ordered(1, tuple([1] * j), z)
            comp += 2
            if hc != ho: bad += 1
            if hc != 2: bad += 1
    # (b) H(2;{1}^k;z)=0 for k>=2, z>=2
    for k in range(2, 13):
        for z in range(2, 15):
            hc = H_canonical(2, tuple([1] * k), z)
            ho = H_ordered(2, tuple([1] * k), z)
            comp += 2
            if hc != ho: bad += 1
            if hc != 0: bad += 1
    # (c) H(1;{1}^k;0)=1 for k>=1
    for k in range(1, 13):
        hc = H_canonical(1, tuple([1] * k), 0)
        ho = H_ordered(1, tuple([1] * k), 0)
        comp += 2
        if hc != ho: bad += 1
        if hc != 1: bad += 1
    # (d) H(2;{1}^t;0)=0 for t>=2
    for t in range(2, 13):
        hc = H_canonical(2, tuple([1] * t), 0)
        ho = H_ordered(2, tuple([1] * t), 0)
        comp += 2
        if hc != ho: bad += 1
        if hc != 0: bad += 1
    # (e) window edges at z=1: H(1;{1}^t;1)=v(t,1,1), H(2;{1}^t;1)=v(t,1,2)
    for t in range(3, 13):
        xs = tuple([1] * t)
        c1 = single_token(t, 1, 1); c2 = single_token(t, 1, 2)
        comp += 4
        if H_canonical(1, xs, 1) != c1 or H_ordered(1, xs, 1) != c1: bad += 1
        if H_canonical(2, xs, 1) != c2 or H_ordered(2, xs, 1) != c2: bad += 1
    clear_engines()
    return {'label': 'D1 T2 battery t=2..24 (z=1,R=3) + K1267 cross + chain (a)-(e)',
            'comparisons': comp, 'bad': bad, 't_values': rec}

# ------------------------------------------------------------------
# D2/D3: M2/K1270 banded slice batteries
# ------------------------------------------------------------------
def shapes(m):
    return [(m,), (m, m), (m, m, m), (m, m, m, m), (m, m + 1),
            (m, m + 2), (m, m + 3), (m, 2 * m), (m, m, m + 1),
            (m, m + 1, m + 2), (m, 3 * m)]

def random_shapes(m, rng, n=12):
    out = []
    for _ in range(n):
        arity = rng.randint(1, 5)
        toks = [m] + [rng.randint(m, m + 40) for _ in range(arity - 1)]
        out.append(tuple(toks))
    return out

def banded_point(X, z, m):
    """checks window edge (fail-closed), banded claim (fail-closed),
    beyond (census record only). Returns (bad, comps, beyond_rec)."""
    S = sum(X)
    Rw = max(z + m, 2)      # unified window
    Rb = Rw + 1             # banded extension (the M2 claim)
    Rz = Rw + 2             # beyond: census record only
    bad = comps = 0
    cw = single_token(S, z, Rw)
    hw_c = H_canonical(Rw, X, z); hw_o = H_ordered(Rw, X, z)
    comps += 4
    if hw_c != cw: bad += 1
    if hw_o != cw: bad += 1
    if hw_c != hw_o: bad += 1
    cb = single_token(S, z, Rb)
    hb_c = H_canonical(Rb, X, z); hb_o = H_ordered(Rb, X, z)
    comps += 4
    if hb_c != cb: bad += 1
    if hb_o != cb: bad += 1
    if hb_c != hb_o: bad += 1
    cz = single_token(S, z, Rz)
    hz_c = H_canonical(Rz, X, z); hz_o = H_ordered(Rz, X, z)
    comps += 3
    if hz_c != hz_o: bad += 1   # engine agreement still fail-closed
    rec = {'X': list(X), 'z': z, 'R': Rz,
           'parent': hz_c, 'single': cz,
           'beyond_separates': (hz_c != cz)}
    return bad, comps, rec

def check_D2():
    bad = comps = 0
    beyond = []
    rng = random.Random(20261123)
    for m in range(2, 15):
        for X in shapes(m) + random_shapes(m, rng):
            b, c, rec = banded_point(X, 0, m)
            bad += b; comps += c
            beyond.append(rec)
        clear_engines()
    # deep m=15..25, light shapes
    for m in range(15, 26):
        for X in [(m,), (m, m), (m, m + 1)]:
            b, c, rec = banded_point(X, 0, m)
            bad += b; comps += c
            beyond.append(rec)
        clear_engines()
    n_sep = sum(1 for r in beyond if r['beyond_separates'])
    return {'label': 'D2 z=0 banded slice battery (m=2..14 full, 15..25 deep)',
            'comparisons': comps, 'bad': bad, 'beyond_points': len(beyond),
            'beyond_separations': n_sep, 'beyond_records': beyond}

def check_D3():
    bad = comps = 0
    beyond = []
    rng = random.Random(20261124)
    for m in range(2, 15):
        for X in shapes(m) + random_shapes(m, rng):
            b, c, rec = banded_point(X, 1, m)
            bad += b; comps += c
            beyond.append(rec)
        clear_engines()
    for m in range(15, 26):
        for X in [(m,), (m, m), (m, m + 1)]:
            b, c, rec = banded_point(X, 1, m)
            bad += b; comps += c
            beyond.append(rec)
        clear_engines()
    # m=2 extension: X=(2+d,2), d=0..40, claim H(4;X;1)=v(sum,1,4)=1
    ext_vals = []
    for d in range(0, 41):
        X = (2 + d, 2); S = d + 4
        cb = single_token(S, 1, 4)
        hc = H_canonical(4, X, 1); ho = H_ordered(4, X, 1)
        comps += 4
        if hc != cb or ho != cb: bad += 1
        if hc != ho: bad += 1
        if cb != 1: bad += 1
        ext_vals.append({'d': d, 'parent': hc, 'single': cb})
    n_sep = sum(1 for r in beyond if r['beyond_separates'])
    return {'label': 'D3 z=1 banded slice battery + m=2 extension (d<=40)',
            'comparisons': comps, 'bad': bad, 'beyond_points': len(beyond),
            'beyond_separations': n_sep, 'beyond_records': beyond,
            'm2_extension_all_one': all(v['parent'] == 1 and v['single'] == 1
                                        for v in ext_vals),
            'm2_extension_first10': ext_vals[:10]}

# ------------------------------------------------------------------
# D3b: lemma LW (min=1, exactly one 1, z=1, budget 3)
# ------------------------------------------------------------------
def check_D3b():
    bad = comps = 0
    lw_shapes = [(1,)]
    for k in range(2, 13):
        lw_shapes.append((1, k))
    for Xs in [(1, 2, 2), (1, 2, 3), (1, 3, 3)]:
        lw_shapes.append(Xs)
    for k in range(3, 9):
        lw_shapes.append((1, 2, k))
    for X in lw_shapes:
        u = sum(X)
        exp = 1 if len(X) == 1 else 2
        hc = H_canonical(3, X, 1); ho = H_ordered(3, X, 1)
        comps += 3
        if hc != ho: bad += 1
        if hc != exp: bad += 1
    clear_engines()
    return {'label': 'D3b lemma LW classification battery',
            'comparisons': comps, 'bad': bad, 'n_shapes': len(lw_shapes)}

# ------------------------------------------------------------------
# D4: fixed-seed deep probes on both slices
# ------------------------------------------------------------------
def check_D4():
    bad = comps = 0
    rng = random.Random(20261125)
    n = 0
    while n < 300:
        m = rng.randint(2, 20)
        arity = rng.randint(1, 5)
        X = tuple([m] + [rng.randint(m, 60) for _ in range(arity - 1)])
        z = rng.randint(0, 1)
        b, c, _ = banded_point(X, z, m)
        bad += b; comps += c
        n += 1
        if n % 60 == 0:
            clear_engines()
    clear_engines()
    return {'label': 'D4 fixed-seed deep probes (300 points)',
            'points': n, 'comparisons': comps, 'bad': bad}

# =====================================================================
# tamper battery
# =====================================================================
def _mex(vals):
    vals = set(vals); m = 0
    while m in vals: m += 1
    return m

@lru_cache(maxsize=1_000_000)
def H_ordered_noC(R, X, z):
    if R == 0: return 0
    opts = set()
    for i, w in enumerate(X):
        if w > 1:
            opts.add(H_ordered_noC(R - 1, X[:i] + (w - 1,) + X[i + 1:], z))
        else:
            opts.add(H_ordered_noC(R - 1, X[:i] + X[i + 1:], z + 1))
    return _mex(opts)

@lru_cache(maxsize=1_000_000)
def H_ordered_noBinc(R, X, z):
    if R == 0: return 0
    opts = set()
    for i, w in enumerate(X):
        if w > 1:
            opts.add(H_ordered_noBinc(R - 1, X[:i] + (w - 1,) + X[i + 1:], z))
        else:
            opts.add(H_ordered_noBinc(R - 1, X[:i] + X[i + 1:], z))
    if z >= 1:
        opts.add(1 ^ H_ordered_noBinc(R - 1, X, z - 1))
    return _mex(opts)

def q_odd_mut(k):
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
        print(('CAUGHT' if bad > 0 else 'TAMPER-MISSED') + ': ' + name +
              ' bad=' + str(bad))
        return bad
    total_bad = 0
    # mut1: K1269 anchor parent flip ({1}^3@(1,3) expected 1)
    hc = H_canonical(3, (1, 1, 1), 1)
    total_bad += rec('mut1 K1269 anchor parent flip ({1}^3@(1,3) exp 1)',
                     0 if hc == 1 else 1)
    # mut2: M2 widened to min=1 ({1}^t at z=0 and z=1, R=3)
    bad = 0
    for t in range(3, 9):
        xs = tuple([1] * t)
        if H_canonical(3, xs, 0) != single_token(t, 0, 3): bad += 1
        if H_canonical(3, xs, 1) != single_token(t, 1, 3): bad += 1
    total_bad += rec('mut2 M2 widened to min=1 claim ({1}^t R3 z0/z1)', bad)
    # mut3: M2 widened to z=2, m=2 (published frontier witness)
    bad = 0
    if H_canonical(5, (2, 2), 2) != single_token(4, 2, 5): bad += 1
    total_bad += rec('mut3 M2 widened to z=2 m=2 claim (frontier witness)', bad)
    # mut4: ordered engine without C-move
    bad = 0
    for z in range(1, 13):
        for R in range(1, z + 6):
            if H_ordered_noC(R, (3, 2), z) != H_canonical(R, (3, 2), z): bad += 1
    total_bad += rec('mut4 ordered engine without C-move', bad)
    # mut5: corrupted q_odd closed form
    bad = 0
    for x in range(2, 41):
        for z in range(1, 21):
            for R in range(0, min(x + z + 1, 40) + 1):
                if single_token_mut(x, z, R) != vC(x, z, R): bad += 1
    total_bad += rec('mut5 corrupted q_odd closed form', bad)
    # mut6: LW B-move value flip (v(u-1,2,2)==1 for u>=3)
    bad = 0
    for u in range(3, 16):
        # flipped claim asserts value==1; the real closed form gives 0,
        # so every u is a catch (deterministic).
        if single_token(u - 1, 2, 2) != 1: bad += 1
    total_bad += rec('mut6 LW B-move value flip (v(u-1,2,2)==1 claim)', bad)
    # mut7: B-move without z-increment
    bad = 0
    for t in range(2, 7):
        for z in range(0, 3):
            for R in range(1, 6):
                if H_ordered_noBinc(R, tuple([1] * t), z) != H_canonical(R, tuple([1] * t), z): bad += 1
    total_bad += rec('mut7 ordered engine without B z-increment', bad)
    results.append({'mutation': 'TOTAL', 'bad': total_bad})
    missed = [r['mutation'] for r in results
              if r['mutation'] != 'TOTAL' and r['bad'] == 0]
    print('TAMPER BATTERY:', 'ALL CAUGHT' if not missed else 'MISSED: ' + str(missed))
    if missed: sys.exit(1)
    sys.exit(0)

# ------------------------------------------------------------------
def run_audit():
    res = {}
    res['D0'] = check_D0()
    clear_engines()
    res['D0b'] = check_D0b()
    clear_engines()
    res['D0c'] = check_D0c()
    clear_engines()
    res['D1'] = check_D1()
    clear_engines()
    res['D2'] = check_D2()
    clear_engines()
    res['D3'] = check_D3()
    clear_engines()
    res['D3b'] = check_D3b()
    clear_engines()
    res['D4'] = check_D4()
    clear_engines()
    total_bad = sum(res[k]['bad'] for k in res)
    res['summary'] = {
        'declaration': 'research/log/2026-11-23-ones-multiset-t2-lowz-banded-single-owner-note.md (commit 9ceb96d0)',
        'total_bad': total_bad,
        'theorem_M1': 'M1/K1269: {1}^t separates at (z,R)=(1,3) for all t>=3 (parent 2 vs single 0); t=2 collapses; engine-checked t=2..24',
        'theorem_M2': 'M2/K1270: low-z banded window extension: min(X)=m>=2 => H(m+1;X;0)=v(sum,0,m+1) and H(m+2;X;1)=v(sum,1,m+2) (all shapes, all arity)',
        'verifier_sha256': SELF_SHA,
    }
    return res, total_bad

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else 'audit'
    if mode == 'tamper':
        tamper(); return
    res, bad = run_audit()
    with open('output/audit.json', 'w') as f:
        f.write(json.dumps(res, indent=1, sort_keys=True, ensure_ascii=True) + '\n')
    comp_tot = sum(res[k].get('comparisons', 0) for k in res if k != 'summary')
    print('TOTAL comparisons:', comp_tot, 'bad:', bad)
    print('D2 beyond separations:', res['D2']['beyond_separations'],
          '/', res['D2']['beyond_points'])
    print('D3 beyond separations:', res['D3']['beyond_separations'],
          '/', res['D3']['beyond_points'])
    print('D3 m=2 extension all-one:', res['D3']['m2_extension_all_one'])
    if bad:
        print('AUDIT FAIL: bad =', bad); sys.exit(1)
    print('AUDIT PASS'); sys.exit(0)

if __name__ == '__main__':
    main()
