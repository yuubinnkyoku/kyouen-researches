#!/usr/bin/env python3
"""K1260 (provisional) audit: H(R;(x,5);19), all x>=5, R>=0.

Universal claim: Grundy values 0/1/2 of the two-token residual game at
height z=19 with second token y=5, for all x>=5 and R>=0, classified by
the T/P closed form below.

Proof skeleton (x-outer induction + complete symbolic signature bands):
  A-child = H(R-1;(x-1,5);19)   x-outer induction (x=5: multiset confluence)
  B-child = H(R-1;(x,4);19)     K1100 (published closed form, verbatim)
  C-child = 1 xor H(R-1;(x,5);18)  K1092 (published closed form, verbatim)
  tail: R>=x+25=S+z+1 => S mod 2 (K0832 general tail)

Transcription sources (published, sha256):
  K1100: research/experiments/vertical-fiber-two-token-z19-y4-boundary-20261120/verify_z19_y4.py
         sha256 09cc65208d4696a73354455ac348e2f4054fca34e74ecacbb9eaa5b434d56b3f
  K1092: research/experiments/vertical-fiber-two-token-z18-y5-boundary-20261120/verify_z18_y5.py
         sha256 2adda5706885290183f99db26d2fb5cc9114d8d30ec86ac403daac53c0f41143

Finite audit is not the universal proof: universality rests on the
x-outer induction and the complete symbolic band table below.
"""
import hashlib, json, os, random, sys
from functools import lru_cache
from pathlib import Path
sys.setrecursionlimit(1_000_000)

SMOKE = bool(os.environ.get('SMOKE'))
if SMOKE:
    PARENT_X, ANCHOR_X, BAND_X, CLOSURE_X, SET_X, DEEP, SCATTER = 12, 16, 30, 40, 30, 300, 500
else:
    PARENT_X, ANCHOR_X, BAND_X, CLOSURE_X, SET_X, DEEP, SCATTER = 40, 45, 100, 500, 200, 30000, 3000

@lru_cache(None)
def H_ordered(R, X, z):
    if R == 0: return 0
    opts = set()
    for i, a in enumerate(X):
        if a > 1: opts.add(H_ordered(R-1, X[:i]+(a-1,)+X[i+1:], z))
        else: opts.add(H_ordered(R-1, X[:i]+X[i+1:], z+1))
    if z: opts.add(1 ^ H_ordered(R-1, X, z-1))
    m = 0
    while m in opts: m += 1
    return m

@lru_cache(None)
def H_canon(R, X, z):
    X = tuple(sorted(X, reverse=True))
    if R == 0: return 0
    opts = set(); i = 0
    while i < len(X):
        a = X[i]
        if a > 1: opts.add(H_canon(R-1, tuple(sorted(X[:i]+(a-1,)+X[i+1:], reverse=True)), z))
        else: opts.add(H_canon(R-1, tuple(sorted(X[:i]+X[i+1:], reverse=True)), z+1))
        while i+1 < len(X) and X[i+1] == a: i += 1
        i += 1
    if z: opts.add(1 ^ H_canon(R-1, X, z-1))
    m = 0
    while m in opts: m += 1
    return m

def qo(n): return n if n % 2 else n-1
def qe(n): return n if n % 2 == 0 else n-1

# ---- B anchor: K1100 (z=19, y=4, all x>=4), transcribed from verify_z19_y4.py ----
def k1100_T(x, R):
    if x <= 14: return R % 2 == 1 and R <= qo(x+4)
    if x == 15: return R % 2 == 1 and R <= 23
    if x in (16, 17, 18, 20, 21, 22): return R % 2 == 1 and R <= 19
    if x == 19: return (R % 2 == 1 and R <= 19) or R == 25
    if x == 23: return (R % 2 == 1 and R <= 19) or R == 27
    if x == 24: return (R % 2 == 1 and R <= 19) or (R % 2 == 1 and 27 <= R <= 47)
    return (R % 2 == 1 and R <= 19) or R == 27

def k1100_P(x, R):
    if x <= 14:
        if x % 2 == 1: return R >= x+5
        return False
    if x == 15: return R >= 20 and R not in (21, 23)
    if x == 16: return R in (20, 22)
    if x == 17: return R >= 20 and (R % 2 == 0 or R >= 25)
    if x == 18: return R in (20, 22, 24)
    if x == 19: return R >= 20 and R not in (21, 23, 25)
    if x == 20: return R in (20, 22, 24)
    if x == 21: return R >= 20 and R not in (21, 23, 25)
    if x == 22: return R in (20, 22, 24, 26)
    if x == 23: return R >= 20 and R not in (21, 23, 25, 27)
    if x == 24: return R in (20, 22, 24, 26)
    band = R % 2 == 1 and 29 <= R <= qo(x+23)
    tail = x % 2 == 1 and R >= x+24
    return R in (20, 22, 24, 26) or band or tail

def k1100(x, R):
    if R == 0: return 0
    if R >= x+24: return (x+4) % 2
    if k1100_T(x, R): return 2
    if k1100_P(x, R): return 1
    return 0

# ---- C anchor: K1092 (z=18, y=5, all x>=5), transcribed from verify_z18_y5.py ----
def k1092_T(x, r):
    if 5 <= x <= 12: return r % 2 == 1 and 1 <= r <= qo(x+5)
    if x == 13: return r % 2 == 1 and r <= 23
    if 14 <= x <= 16 or x in (18, 19, 20, 22, 23): return r % 2 == 1 and r <= 17
    if x == 17: return (r % 2 == 1 and r <= 17) or r == 25
    if x == 21: return (r % 2 == 1 and r <= 17) or r == 27
    if x == 24: return (r % 2 == 1 and r <= 17) or (r % 2 == 1 and 29 <= r <= 47)
    return (r % 2 == 1 and r <= 17) or r == 29

def k1092_P(x, r):
    if x in (5, 7, 9, 11, 13): return False
    if x in (6, 8, 10, 12): return r >= x+6
    if x == 14: return r in (19, 21) or r >= 23
    if x == 15: return r in (19, 21, 23)
    if x == 16: return r in (19, 21, 23) or r >= 25
    if x == 17: return r in (19, 21, 23)
    if x == 18: return r in (19, 21, 23) or r >= 25
    if x == 19: return r in (19, 21, 23, 25)
    if x == 20: return r in (19, 21, 23, 25) or r >= 27
    if x == 21: return r in (19, 21, 23, 25)
    if x == 22: return r in (19, 21, 23, 25) or r >= 27
    if x == 23: return r in (19, 21, 23, 25, 27)
    if x == 24: return r in (19, 21, 23, 25, 27) or (r % 2 == 0 and 30 <= r <= 46) or r >= 48
    if x % 2: return r in (19, 21, 23, 25, 27) or (r % 2 == 0 and 30 <= r <= qe(x+23))
    return r in (19, 21, 23, 25, 27) or (r % 2 == 0 and 30 <= r <= qe(x+23)) or r >= x+24

def k1092(x, r):
    if r == 0: return 0
    if r >= x+24: return (x+5) % 2
    if k1092_T(x, r): return 2
    if k1092_P(x, r): return 1
    return 0

# ---- target closed form: H(R;(x,5);19) ----
def T(x, R):
    if x <= 13: return R % 2 == 1 and R <= qo(x+5)
    if x == 14: return R % 2 == 1 and R <= 23
    if x in (15, 17, 18, 19, 21, 22, 23): return R % 2 == 1 and R <= 19
    if x == 16: return (R % 2 == 1 and R <= 19) or R == 25
    if x == 20: return (R % 2 == 1 and R <= 19) or R == 27
    if x == 24: return (R % 2 == 1 and R <= 19) or R == 29
    if x == 25: return (R % 2 == 1 and R <= 19) or (R % 2 == 1 and 29 <= R <= 49)
    return (R % 2 == 1 and R <= 19) or R == 29

def P(x, R):
    if x in (5, 7, 9, 11, 13): return False
    if x in (6, 8, 10, 12): return R >= x+6
    if x == 14: return 20 <= R <= 38 and R not in (21, 23)
    if x in (15, 17): return R in (20, 22, 24)
    if x == 16: return R == 20 or (R % 2 == 0 and 22 <= R <= 40) or (R % 2 == 1 and 27 <= R <= 39)
    if x == 18: return R == 20 or (R % 2 == 0 and 22 <= R <= 42) or (R % 2 == 1 and 27 <= R <= 41)
    if x in (19, 21): return R in (20, 22, 24, 26)
    if x == 20: return R == 20 or (R % 2 == 0 and 22 <= R <= 44) or (R % 2 == 1 and 29 <= R <= 43)
    if x == 22: return R == 20 or (R % 2 == 0 and 22 <= R <= 46) or (R % 2 == 1 and 29 <= R <= 45)
    if x == 23: return R in (20, 22, 24, 26, 28)
    if x == 24: return R in (20, 22, 24, 26, 28) or 30 <= R <= 48
    if x == 25: return R in (20, 22, 24, 26, 28)
    if x == 26: return R in (20, 22, 24, 26, 28) or (R % 2 == 1 and 31 <= R <= 49)
    if x % 2 == 0:
        return R in (20, 22, 24, 26, 28) or (R % 2 == 1 and 31 <= R <= qo(x+24)) or R >= x+25
    return R in (20, 22, 24, 26, 28) or (R % 2 == 1 and 31 <= R <= qo(x+24))

def F(x, R):
    if R == 0: return 0
    if R >= x+25: return (x+5) % 2
    t, p = T(x, R), P(x, R)
    assert not (t and p), ('TP overlap', x, R)
    return 2 if t else (1 if p else 0)

# Independently encoded set form.
def Tset(x):
    if x <= 13: return set(range(1, qo(x+5)+1, 2))
    if x == 14: return set(range(1, 24, 2))
    if x in (15, 17, 18, 19, 21, 22, 23): return set(range(1, 20, 2))
    if x == 16: return set(range(1, 20, 2)) | {25}
    if x == 20: return set(range(1, 20, 2)) | {27}
    if x == 24: return set(range(1, 20, 2)) | {29}
    if x == 25: return set(range(1, 20, 2)) | set(range(29, 50, 2))
    return set(range(1, 20, 2)) | {29}

def Pset(x, L):
    if x in (5, 7, 9, 11, 13): return set()
    if x in (6, 8, 10, 12): return set(range(x+6, L+1))
    if x == 14: return set(range(20, min(38, L)+1)) - {21, 23}
    if x in (15, 17): return {20, 22, 24}
    def ranged(a, b, step=1):
        return set(range(a, min(b, L)+1, step))
    if x == 16: return {20} | ranged(22, 41, 2) | ranged(27, 40, 2)
    if x == 18: return {20} | ranged(22, 43, 2) | ranged(27, 42, 2)
    if x in (19, 21): return {20, 22, 24, 26}
    if x == 20: return {20} | ranged(22, 45, 2) | ranged(29, 44, 2)
    if x == 22: return {20} | ranged(22, 47, 2) | ranged(29, 46, 2)
    if x == 23: return {20, 22, 24, 26, 28}
    if x == 24: return {20, 22, 24, 26, 28} | set(range(30, min(48, L)+1))
    if x == 25: return {20, 22, 24, 26, 28}
    if x == 26: return {20, 22, 24, 26, 28} | ranged(31, 50, 2)
    if x % 2 == 0:
        return {20, 22, 24, 26, 28} | ranged(31, qo(x+24)+1, 2) | set(range(x+25, L+1))
    return {20, 22, 24, 26, 28} | ranged(31, qo(x+24)+1, 2)

# Complete symbolic A/B/C signature bands. Static rows x=5..26, affine x>=27.
ODD_ROWS = (
'1-9:01,11-29:1;1-11:01,13-29:0;1-11:01,13-31:1;1-13:01,15-31:0;1-13:01,15-33:1;'
'1-15:01,17-33:0;1-15:01,17-35:1;1-17:01,19-35:0;1-17:01,19-37:1;1-23:01,25-37:0;'
'1-19:01,21-39:1;1-19:01,21-23:1,25:01,27-39:0;1-19:01,21-41:1;1-19:01,21-25:1,27-41:0;'
'1-19:01,21-43:1;1-19:01,21-25:1,27:01,29-43:0;1-19:01,21-45:1;1-19:01,21-27:1,29-45:0;'
'1-19:01,21-47:1;1-19:01,21-27:1,29:01,31-47:0;1-19:01,21-27:1,29-49:01;'
'1-19:01,21-27:1,29:01,31-49:0')
EVEN_ROWS = (
'2-10:23,12-28:1;2-10:23,12:03,14-30:0;2-12:23,14-30:1;2-12:23,14:03,16-32:0;'
'2-14:23,16-32:1;2-14:23,16:03,18-34:0;2-16:23,18-34:1;2-16:23,18:03,20-36:0;'
'2-18:23,20-24:13,26-36:1;2-18:23,20-38:0;2-18:23,20-24:02,26-38:1;'
'2-18:23,20:02,22-40:0;2-18:23,20:02,22-24:0,26:123,28-40:1;2-18:23,20:02,22-42:0;'
'2-18:23,20:02,22-24:0,26:02,28-42:1;2-18:23,20:02,22-44:0;'
'2-18:23,20:02,22-26:0,28:123,30-44:1;2-18:23,20:02,22-46:0;'
'2-18:23,20:02,22-26:0,28:02,30-46:1;2-18:23,20:02,22-26:0,28:02,30-48:023;'
'2-18:23,20:02,22-26:0,28:02,30:123,32-48:1;'
'2-18:23,20:02,22-26:0,28:02,30:123,32-50:12')

def parse_row(s):
    out = []
    for part in s.split(','):
        span, sig = part.split(':')
        if '-' in span: a, b = map(int, span.split('-'))
        else: a = b = int(span)
        out.append((a, b, sig))
    return out

def expected_bands(x, p):
    if 5 <= x <= 26:
        rows = (ODD_ROWS if p else EVEN_ROWS).split(';')
        return parse_row(rows[x-5])
    if p: return [(1, 19, '01'), (21, 27, '1'), (29, 29, '01'), (31, qo(x+24), '0')]
    return [(2, 18, '23'), (20, 20, '02'), (22, 26, '0'), (28, 28, '02'), (30, 30, '123'), (32, qe(x+24), '1')]

def sig(x, R):
    r = R-1
    if x == 5: a = b = k1100(5, r)
    else: a = F(x-1, r); b = k1100(x, r)
    c = 1 ^ k1092(x, r)
    return ''.join(map(str, sorted({a, b, c})))

MEX = {'01': 2, '23': 0, '03': 1, '0': 1, '1': 0, '12': 0, '13': 0, '023': 1, '123': 0, '02': 1}

def single(s, z, r):
    if r == 0 or s <= 0: return 0
    if z == 0: return min(r, s) % 2
    if s == z:
        if r % 2 and r <= 2*s-1: return 2
        if r % 2 == 0 and r <= s-1: return 0
        return s % 2
    if 1 <= z <= s-1:
        m = qo(z)
        if r <= m: return 2 if r % 2 else 0
        if m < r < s+z: return (r+z) % 2
        return s % 2
    if z >= s+1:
        m = qo(s)
        if r <= m: return 2 if r % 2 else 0
        return s % 2
    raise ValueError((s, z, r))

ROWMAX = {14: 24, 15: 25, 16: 24, 17: 25, 18: 26, 19: 27, 20: 26, 21: 27, 22: 28, 23: 29}
WITNESSES = {14: (25, 1, 2), 15: (26, 0, 1), 16: (25, 2, 0), 17: (26, 0, 1), 18: (27, 1, 0),
             19: (28, 0, 1), 20: (27, 2, 0), 21: (28, 0, 1), 22: (29, 1, 0), 23: (30, 0, 1),
             24: (29, 2, 0), 26: (29, 2, 0), 50: (29, 2, 0), 200: (29, 2, 0)}

def run():
    c = {}
    n = 0
    for x in range(5, PARENT_X+1):
        for r in range(x+31):
            a = H_ordered(r, (x, 5), 19); b = H_canon(r, (x, 5), 19); d = F(x, r)
            assert a == b == d, ('parent', x, r, a, b, d); n += 1
    c['parent_two_raw_engines_vs_formula'] = n
    n = 0
    for x in range(4, ANCHOR_X+1):
        for r in range(x+29):
            a = H_ordered(r, (x, 4), 19); b = H_canon(r, (x, 4), 19); d = k1100(x, r)
            assert a == b == d, ('B', x, r, a, b, d); n += 1
    c['K1100_B_anchor'] = n
    n = 0
    for x in range(5, ANCHOR_X+1):
        for r in range(x+29):
            a = H_ordered(r, (x, 5), 18); b = H_canon(r, (x, 5), 18); d = k1092(x, r)
            assert a == b == d, ('C', x, r, a, b, d); n += 1
    c['K1092_C_anchor'] = n
    n = 0
    for x in range(5, BAND_X+1):
        for p in (1, 0):
            row = expected_bands(x, p)
            assert row[0][0] == (1 if p else 2)
            prev = None
            for lo, hi, s in row:
                assert lo % 2 == p and hi % 2 == p and lo <= hi and s in MEX
                if prev is not None: assert lo == prev+2, ('gap', x, p, row)
                prev = hi
                for r in range(lo, hi+1, 2):
                    got = sig(x, r)
                    assert got == s, ('band', x, r, s, got)
                    assert MEX[s] == F(x, r), ('mex', x, r, s)
                    n += 1
            top = x+24; want = top if top % 2 == p else top-1
            assert prev == want, ('top', x, p, prev, want)
    c['signature_band_coverage_identity_mex'] = n
    n = 0
    for x in range(6, CLOSURE_X+1):
        for r in range(1, x+25):
            s = sig(x, r); assert MEX[s] == F(x, r), ('closure', x, r, s)
            n += 1
    for r in range(1, 30):
        s = sig(5, r); assert MEX[s] == F(5, r), ('base', r, s); n += 1
    c['induction_closure_sweep'] = n
    n = 0
    for x in range(5, SET_X+1):
        ts = Tset(x); ps = Pset(x, x+80)
        assert ts.isdisjoint(ps), ('overlap', x)
        for r in range(x+81):
            assert (r in ts) == T(x, r), ('Tset', x, r)
            assert (r in ps) == P(x, r), ('Pset', x, r)
            n += 1
    c['set_vs_predicate'] = n
    n = 0
    for x in range(5, SET_X+1):
        upto = x+80 if x <= 13 else ROWMAX[x] if x <= 23 else 28
        for r in range(upto+1):
            assert F(x, r) == single(x+5, 19, r), ('low', x, r, F(x, r), single(x+5, 19, r)); n += 1
    c['height_only_initial_intervals'] = n
    for x, (r, a, b) in WITNESSES.items():
        assert F(x, r) == a and single(x+5, 19, r) == b, ('witness', x, r)
    c['height_only_sharpness_witnesses'] = len(WITNESSES)
    n = 0
    for x in range(5, ANCHOR_X+1):
        for r in range(x+25, x+32):
            a = H_ordered(r, (x, 5), 19); b = H_canon(r, (x, 5), 19); d = (x+5) % 2
            assert a == b == d, ('tail', x, r); n += 1
    c['tail_direct'] = n
    n = 0
    for x in range(27, DEEP+1):
        for p in (1, 0):
            for lo, hi, s in expected_bands(x, p):
                m = (lo+hi)//2; m += (p-m) % 2
                for r in {lo, hi, m}:
                    if lo <= r <= hi and r % 2 == p:
                        assert sig(x, r) == s and MEX[s] == F(x, r), ('deep', x, r)
                        n += 1
        for r in (x+25, x+26, x+31, x+42):
            assert F(x, r) == (x+5) % 2, ('deep_tail', x, r); n += 1
    c['deep_affine_band_and_tail_samples'] = n
    rng = random.Random(20261123); n = 0
    for _ in range(SCATTER):
        x = rng.randint(5, 10000); r = rng.randint(0, x+60); v = F(x, r)
        assert v in (0, 1, 2) and not (T(x, r) and P(x, r))
        if r >= x+25: assert v == (x+5) % 2
        elif r >= 1: assert MEX[sig(x, r)] == v
        n += 1
    c['fixed_seed_scatter'] = n
    c['total_checks'] = sum(c.values())
    c['claim'] = 'H(R;(x,5);19), all x>=5 and R>=0'
    c['proof_status'] = 'proved_by_x_outer_induction_and_complete_symbolic_signature_bands'
    c['finite_audit_scope'] = {'parent': f'5<=x<={PARENT_X}, 0<=R<=x+30, ordered/canonical/formula',
        'B': f'4<=x<={ANCHOR_X}, 0<=R<=x+28, raw z=19 y=4 vs K1100',
        'C': f'5<=x<={ANCHOR_X}, 0<=R<=x+28, raw z=18 y=5 vs K1092',
        'bands': f'5<=x<={BAND_X}, complete 1<=R<=x+24',
        'closure': f'6<=x<={CLOSURE_X}, complete 1<=R<=x+24 plus x=5 base',
        'sets': f'5<=x<={SET_X}, 0<=R<=x+80', 'low_R': 'x<=13 full window; x=14..23 exact prefixes; 24<=x<=SET_X R<=28',
        'tail': f'5<=x<={ANCHOR_X}, x+25<=R<=x+31', 'deep': f'27<=x<={DEEP}, band endpoints/midpoints and tail',
        'scatter_seed': 20261123}
    c['ordered_states'] = H_ordered.cache_info().currsize; c['canonical_states'] = H_canon.cache_info().currsize
    c['height_only_row_max'] = {'5..13': 'all R', **{str(k): v for k, v in ROWMAX.items()}, '24+ or 26+': 28}
    c['sharpness_first_mismatch'] = {str(k): list(v) for k, v in WITNESSES.items()}
    c['verifier_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    out = Path(__file__).resolve().parent/'output'/'audit.json'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(c, ensure_ascii=False, sort_keys=True, indent=2)+'\n', encoding='utf-8')
    return c

if __name__ == '__main__': print(json.dumps(run(), ensure_ascii=False, sort_keys=True, indent=2))
