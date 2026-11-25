#!/usr/bin/env python3
"""K1098 audit: H(R;(x,3);19), all x>=3, R>=0.
Two raw engines, K1052/K1078 anchors, exact A/B/C signature bands
(static rows x=3..24, affine x>=25), induction closure, low-R
single-token collapse and sharpness, tail.
"""
import hashlib, json, random, sys
from functools import lru_cache
from pathlib import Path
sys.setrecursionlimit(1_000_000)

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

def qo(n): return n if n % 2 else n - 1
def qe(n): return n if n % 2 == 0 else n - 1

# K1052: z=19, y=2 (published verifier transcription)
def k1052_T(x, r):
    if x == 2: return r in (1, 3)
    if x in (3, 4): return 1 <= r <= 5 and r % 2 == 1
    if x in (5, 6): return 1 <= r <= 7 and r % 2 == 1
    if x in (7, 8): return 1 <= r <= 9 and r % 2 == 1
    if x in (9, 10): return 1 <= r <= 11 and r % 2 == 1
    if x in (11, 12): return 1 <= r <= 13 and r % 2 == 1
    if x in (13, 14): return 1 <= r <= 15 and r % 2 == 1
    if x in (15, 16): return 1 <= r <= 17 and r % 2 == 1
    if x == 17: return 1 <= r <= 21 and r % 2 == 1
    if x == 21: return (1 <= r <= 19 and r % 2 == 1) or r == 23
    if x == 22: return r % 2 == 1 and (1 <= r <= 19 or 23 <= r <= 43)
    if x >= 23: return (1 <= r <= 19 and r % 2 == 1) or r == 23
    return 1 <= r <= 19 and r % 2 == 1

def k1052_P(x, r):
    if x % 2 == 0 and x <= 16: return False
    if x % 2 == 1 and x <= 15: return r >= x + 3
    if x == 17: return r >= 20 and r != 21
    if x == 18: return r == 20
    if x == 19: return r in (20, 22) or r >= 23
    if x == 20: return r in (20, 22)
    if x == 21: return r in (20, 22) or r >= 24
    if x == 22: return r in (20, 22)
    if x % 2 == 1:
        return (r in (20, 22) or (r % 2 == 1 and 25 <= r <= x + 21) or r >= x + 22)
    return r in (20, 22) or (r % 2 == 1 and 25 <= r <= x + 21)

def k1052(x, R):
    assert not (k1052_T(x, R) and k1052_P(x, R)), ('k1052 overlap', x, R)
    if R == 0: return 0
    if k1052_T(x, R): return 2
    return 1 if k1052_P(x, R) else 0

# K1078: z=18, y=3 (published verifier transcription)
def k1078_T(x, r):
    if r % 2 == 0: return False
    if x <= 14: return r <= 2 * (x // 2) + 3
    if x == 15: return r <= 21
    if 16 <= x <= 18: return r <= 17
    if x == 19: return r <= 17 or r == 23
    if x in (20, 21): return r <= 17
    if x == 22: return r <= 17 or 25 <= r <= 43
    return r <= 17 or r == 25

def k1078_P(x, r):
    if x <= 15: return x >= 4 and x % 2 == 0 and r >= x + 4
    if x == 16: return r in (19, 21) or r >= 22
    if x == 17: return r in (19, 21)
    if x in (18, 20): return r in (19, 21) or r >= 23
    if x == 19: return r in (19, 21)
    if x == 21: return r in (19, 21, 23)
    if x == 22: return (r in (19, 21, 23) or (r % 2 == 0 and 26 <= r <= 42) or r >= 44)
    upper = x + 20 if x % 2 == 0 else x + 21
    return (r in (19, 21, 23) or (r % 2 == 0 and 26 <= r <= upper)
            or (x % 2 == 0 and r >= x + 22))

def k1078(x, r):
    if r == 0: return 0
    if r >= x + 22: return (x + 3) % 2
    if k1078_T(x, r): return 2
    if k1078_P(x, r): return 1
    return 0

# Target T/P predicates, R-space.
def T(x, R):
    if x <= 15: return R % 2 == 1 and R <= 2 * (x // 2) + 3
    if x == 16: return R % 2 == 1 and R <= 21
    if x in (17, 19, 20, 21): return R % 2 == 1 and R <= 19
    if x == 18: return (R % 2 == 1 and R <= 19) or R == 23
    if x == 22: return (R % 2 == 1 and R <= 19) or R == 25
    if x == 23: return (R % 2 == 1 and R <= 19) or (R % 2 == 1 and 25 <= R <= 45)
    return (R % 2 == 1 and R <= 19) or R == 25

def P(x, R):
    if x % 2 == 1 and x <= 15: return False
    if x % 2 == 0 and x <= 14: return R >= x + 4
    if x == 16: return R == 20 or R >= 22
    if x == 17: return R in (20, 22)
    if x == 18: return R in (20, 22) or R >= 24
    if x == 19: return R in (20, 22)
    if x == 20: return R in (20, 22) or R >= 24
    if x == 21: return R in (20, 22, 24)
    if x == 22: return R in (20, 22, 24) or R >= 26
    if x == 23: return R in (20, 22, 24)
    band = R % 2 == 1 and 27 <= R <= qo(x + 22)
    tail = x % 2 == 0 and R >= x + 23
    return R in (20, 22, 24) or band or tail

def F(x, R):
    if R == 0: return 0
    if R >= x + 23: return (x + 3) % 2
    t, p = T(x, R), P(x, R)
    assert not (t and p), ('TP overlap', x, R)
    return 2 if t else (1 if p else 0)

# Independently encoded set form.
def Tset(x):
    if x <= 15: return set(range(1, 2 * (x // 2) + 4, 2))
    if x == 16: return set(range(1, 22, 2))
    if x in (17, 19, 20, 21): return set(range(1, 20, 2))
    if x == 18: return set(range(1, 20, 2)) | {23}
    if x == 22: return set(range(1, 20, 2)) | {25}
    if x == 23: return set(range(1, 20, 2)) | set(range(25, 46, 2))
    return set(range(1, 20, 2)) | {25}

def Pset(x, L):
    if x % 2 == 1 and x <= 15: return set()
    if x % 2 == 0 and x <= 14: return set(range(x + 4, L + 1))
    if x == 16: return {20} | set(range(22, L + 1))
    if x == 17: return {20, 22}
    if x == 18: return {20, 22} | set(range(24, L + 1))
    if x == 19: return {20, 22}
    if x == 20: return {20, 22} | set(range(24, L + 1))
    if x == 21: return {20, 22, 24}
    if x == 22: return {20, 22, 24} | set(range(26, L + 1))
    if x == 23: return {20, 22, 24}
    out = {20, 22, 24} | set(range(27, qo(x + 22) + 1, 2))
    if x % 2 == 0: out |= set(range(x + 23, L + 1))
    return out

# Static signature bands (R-space), derived from the anchors and the
# x-outer mex recurrence; every row tiles its parity class up to x+22.
BANDS = {
    3:  ([(1,5,'01'),(7,25,'1')], [(2,6,'23'),(8,24,'1')]),
    4:  ([(1,7,'01'),(9,25,'0')], [(2,6,'23'),(8,8,'03'),(10,26,'0')]),
    5:  ([(1,7,'01'),(9,27,'1')], [(2,8,'23'),(10,26,'1')]),
    6:  ([(1,9,'01'),(11,27,'0')], [(2,8,'23'),(10,10,'03'),(12,28,'0')]),
    7:  ([(1,9,'01'),(11,29,'1')], [(2,10,'23'),(12,28,'1')]),
    8:  ([(1,11,'01'),(13,29,'0')], [(2,10,'23'),(12,12,'03'),(14,30,'0')]),
    9:  ([(1,11,'01'),(13,31,'1')], [(2,12,'23'),(14,30,'1')]),
    10: ([(1,13,'01'),(15,31,'0')], [(2,12,'23'),(14,14,'03'),(16,32,'0')]),
    11: ([(1,13,'01'),(15,33,'1')], [(2,14,'23'),(16,32,'1')]),
    12: ([(1,15,'01'),(17,33,'0')], [(2,14,'23'),(16,16,'03'),(18,34,'0')]),
    13: ([(1,15,'01'),(17,35,'1')], [(2,16,'23'),(18,34,'1')]),
    14: ([(1,17,'01'),(19,35,'0')], [(2,16,'23'),(18,18,'03'),(20,36,'0')]),
    15: ([(1,17,'01'),(19,37,'1')], [(2,18,'23'),(20,22,'13'),(24,36,'1')]),
    16: ([(1,21,'01'),(23,37,'0')], [(2,18,'23'),(20,38,'0')]),
    17: ([(1,19,'01'),(21,39,'1')], [(2,18,'23'),(20,22,'02'),(24,38,'1')]),
    18: ([(1,19,'01'),(21,21,'1'),(23,23,'01'),(25,39,'0')], [(2,18,'23'),(20,20,'02'),(22,40,'0')]),
    19: ([(1,19,'01'),(21,41,'1')], [(2,18,'23'),(20,20,'02'),(22,22,'0'),(24,24,'123'),(26,40,'1')]),
    20: ([(1,19,'01'),(21,23,'1'),(25,41,'0')], [(2,18,'23'),(20,20,'02'),(22,42,'0')]),
    21: ([(1,19,'01'),(21,43,'1')], [(2,18,'23'),(20,20,'02'),(22,22,'0'),(24,24,'02'),(26,42,'1')]),
    22: ([(1,19,'01'),(21,23,'1'),(25,25,'01'),(27,43,'0')], [(2,18,'23'),(20,20,'02'),(22,22,'0'),(24,24,'02'),(26,44,'023')]),
    23: ([(1,19,'01'),(21,23,'1'),(25,45,'01')], [(2,18,'23'),(20,20,'02'),(22,22,'0'),(24,24,'02'),(26,26,'123'),(28,44,'1')]),
    24: ([(1,19,'01'),(21,23,'1'),(25,25,'01'),(27,45,'0')], [(2,18,'23'),(20,20,'02'),(22,22,'0'),(24,24,'02'),(26,26,'123'),(28,46,'12')]),
}

def expected_bands(x, p):
    if x <= 24: return BANDS[x][0] if p == 1 else BANDS[x][1]
    if p == 1: return [(1,19,'01'),(21,23,'1'),(25,25,'01'),(27,qo(x+22),'0')]
    return [(2,18,'23'),(20,20,'02'),(22,22,'0'),(24,24,'02'),(26,26,'123'),(28,qe(x+22),'1')]

def sig(x, R):
    r = R - 1
    if x == 3: a = b = k1052(3, r)
    else: a = F(x-1, r); b = k1052(x, r)
    c = 1 ^ k1078(x, r)
    return ''.join(map(str, sorted({a, b, c})))

MEX = {'01':2,'23':0,'03':1,'0':1,'1':0,'12':0,'13':0,'023':1,'123':0,'02':1}

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

HROW_MAX = {16:22, 17:23, 18:22, 19:23, 20:24, 21:25}

def run():
    c = {}
    n = 0
    for x in range(3, 42):
        for R in range(x + 33):
            a = H_ordered(R, (x,3), 19); b = H_canon(R, (x,3), 19); d = F(x, R)
            assert a == b == d, ('parent', x, R, a, b, d); n += 1
    c['parent_two_raw_engines_vs_formula'] = n
    n = 0
    for x in range(2, 42):
        for R in range(x + 31):
            a = H_ordered(R, (x,2), 19); b = H_canon(R, (x,2), 19); d = k1052(x, R)
            assert a == b == d, ('B', x, R, a, b, d); n += 1
    c['K1052_B_anchor'] = n
    n = 0
    for x in range(3, 42):
        for R in range(x + 31):
            a = H_ordered(R, (x,3), 18); b = H_canon(R, (x,3), 18); d = k1078(x, R)
            assert a == b == d, ('C', x, R, a, b, d); n += 1
    c['K1078_C_anchor'] = n
    n = 0
    for x in range(3, 101):
        for p in (1, 0):
            row = expected_bands(x, p)
            assert row[0][0] == (1 if p == 1 else 2)
            prev = None
            for lo, hi, s in row:
                assert lo % 2 == p and hi % 2 == p and lo <= hi and s in MEX
                if prev is not None: assert lo == prev + 2, ('gap', x, p, row)
                prev = hi
                for R in range(lo, hi + 1, 2):
                    got = sig(x, R)
                    assert got == s, ('band', x, R, s, got)
                    assert MEX[s] == F(x, R), ('mex', x, R, s)
                    n += 1
            top = x + 22 if (x + 22) % 2 == p else x + 21
            assert prev == top, ('top', x, p, prev, top)
    c['signature_band_coverage_identity_mex'] = n
    n = 0
    for x in range(4, 501):
        for R in range(1, x + 23):
            assert MEX[sig(x, R)] == F(x, R), ('closure', x, R)
            n += 1
    c['induction_closure_sweep'] = n
    n = 0
    for x in range(3, 201):
        ts = Tset(x); ps = Pset(x, x + 85)
        assert ts.isdisjoint(ps), ('overlap', x)
        for R in range(x + 86):
            assert (R in ts) == T(x, R), ('Tset', x, R)
            assert (R in ps) == P(x, R), ('Pset', x, R)
            n += 1
    c['set_vs_predicate'] = n
    n = 0
    for x in range(3, 16):
        for R in range(x + 91):
            assert F(x, R) == single(x + 3, 19, R), ('lowfull', x, R)
            n += 1
    for x in range(16, 22):
        for R in range(HROW_MAX[x] + 1):
            assert F(x, R) == single(x + 3, 19, R), ('lowrow', x, R)
            n += 1
    for x in range(22, 201):
        for R in range(25):
            assert F(x, R) == single(x + 3, 19, R), ('lowuniform', x, R)
            n += 1
    c['height_only_initial_intervals'] = n
    witnesses = {16:(23,1,2),17:(24,0,1),18:(23,2,0),19:(24,0,1),20:(25,1,0),
                 21:(26,0,1),22:(25,2,0),25:(25,2,0),50:(25,2,0),200:(25,2,0)}
    for x,(R,a,b) in witnesses.items():
        assert F(x, R) == a and single(x + 3, 19, R) == b, ('witness', x, R)
    c['height_only_sharpness_witnesses'] = len(witnesses)
    n = 0
    for x in range(3, 41):
        for R in range(x + 23, x + 31):
            a = H_ordered(R, (x,3), 19); b = H_canon(R, (x,3), 19)
            assert a == b == (x + 3) % 2, ('tail', x, R, a, b)
            n += 1
    c['tail_direct'] = n
    n = 0
    for x in range(25, 30001):
        for p in (1, 0):
            for lo, hi, s in expected_bands(x, p):
                m = (lo + hi) // 2
                m += (p - m) % 2
                for R in {lo, hi, m}:
                    if lo <= R <= hi:
                        assert sig(x, R) == s and MEX[s] == F(x, R), ('deep', x, R)
                        n += 1
        for R in (x + 23, x + 24, x + 25, x + 30):
            assert F(x, R) == (x + 3) % 2, ('deep_tail', x, R)
            n += 1
    c['deep_affine_band_and_tail_samples'] = n
    rng = random.Random(20261121); n = 0
    for _ in range(3000):
        x = rng.randint(3, 10000); R = rng.randint(0, x + 60); v = F(x, R)
        assert v in (0, 1, 2) and not (T(x, R) and P(x, R))
        if R >= x + 23: assert v == (x + 3) % 2
        elif R >= 1: assert MEX[sig(x, R)] == v
        n += 1
    c['fixed_seed_scatter'] = n
    c['total_checks'] = sum(c.values())
    c['claim'] = 'H(R;(x,3);19), all x>=3 and R>=0'
    c['proof_status'] = 'proved_by_x_outer_induction_and_complete_symbolic_signature_bands'
    c['finite_audit_scope'] = {'parent':'3<=x<=41, 0<=R<=x+32, ordered/canonical/formula',
                               'B':'2<=x<=41, 0<=R<=x+30','C':'3<=x<=41, 0<=R<=x+30',
                               'bands':'3<=x<=100, complete 1<=R<=x+22',
                               'closure':'4<=x<=500, complete 1<=R<=x+22',
                               'sets':'3<=x<=200, 0<=R<=x+85',
                               'low_R':'x<=15 full rows to R<=x+90; x=16..21 exact prefixes; x>=22 R<=24',
                               'tail':'3<=x<=40, x+23<=R<=x+30',
                               'deep':'25<=x<=30000, band endpoints/midpoints and tail samples',
                               'scatter_seed':20261121}
    c['ordered_states'] = H_ordered.cache_info().currsize
    c['canonical_states'] = H_canon.cache_info().currsize
    c['height_only'] = {'x<=15':'all R (window R<=x+90, constant tail identity)',
                        'row_max':{str(k):v for k,v in HROW_MAX.items()},
                        'x>=22':24,
                        'sharpness':'pin R=25=2y+z gives F=2 vs single=0 for every x>=22'}
    c['sharpness_first_mismatch'] = {str(k):list(v) for k,v in witnesses.items()}
    c['verifier_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    out = Path(__file__).resolve().parent / 'output' / 'audit.json'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(c, ensure_ascii=False, sort_keys=True, indent=2) + '\n', encoding='utf-8')
    return c

if __name__ == '__main__':
    print(json.dumps(run(), ensure_ascii=False, sort_keys=True, indent=2))
