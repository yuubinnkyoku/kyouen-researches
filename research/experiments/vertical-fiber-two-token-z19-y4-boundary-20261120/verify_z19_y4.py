#!/usr/bin/env python3
"""K1100 audit: H(R;(x,4);19), all x>=4, R>=0.
Two raw engines, K1098/K1083 anchors, exact A/B/C signature bands
(static rows x=4..25, affine x>=26), induction closure, low-R
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
        while i + 1 < len(X) and X[i+1] == a: i += 1
        i += 1
    if z: opts.add(1 ^ H_canon(R-1, X, z-1))
    m = 0
    while m in opts: m += 1
    return m

def qo(n): return n if n % 2 else n - 1
def qe(n): return n if n % 2 == 0 else n - 1

# ---- B anchor: K1098 (z=19, y=3, all x>=3) ----
def k1098_T(x, r):
    if x <= 15: return r % 2 == 1 and r <= 2 * (x // 2) + 3
    if x == 16: return r % 2 == 1 and r <= 21
    if x in (17, 19, 20, 21): return r % 2 == 1 and r <= 19
    if x == 18: return (r % 2 == 1 and r <= 19) or r == 23
    if x == 22: return (r % 2 == 1 and r <= 19) or r == 25
    if x == 23: return (r % 2 == 1 and r <= 19) or (r % 2 == 1 and 25 <= r <= 45)
    return (r % 2 == 1 and r <= 19) or r == 25

def k1098_P(x, r):
    if x % 2 == 1 and x <= 15: return False
    if x % 2 == 0 and x <= 14: return r >= x + 4
    if x == 16: return r == 20 or r >= 22
    if x == 17: return r in (20, 22)
    if x == 18: return r in (20, 22) or r >= 24
    if x == 19: return r in (20, 22)
    if x == 20: return r in (20, 22) or r >= 24
    if x == 21: return r in (20, 22, 24)
    if x == 22: return r in (20, 22, 24) or r >= 26
    if x == 23: return r in (20, 22, 24)
    band = r % 2 == 1 and 27 <= r <= qo(x + 22)
    tail = x % 2 == 0 and r >= x + 23
    return r in (20, 22, 24) or band or tail

def k1098(x, r):
    if r == 0: return 0
    if r >= x + 23: return (x + 3) % 2
    if k1098_T(x, r): return 2
    if k1098_P(x, r): return 1
    return 0

# ---- C anchor: K1083 (z=18, y=4, all x>=4) ----
def k1083_T(x, r):
    odd = lambda r, a, b: a <= r <= b and r % 2 == 1
    if x == 4: return odd(r, 1, 7)
    if x in (5, 6): return odd(r, 1, 9)
    if x in (7, 8): return odd(r, 1, 11)
    if x in (9, 10): return odd(r, 1, 13)
    if x in (11, 12): return odd(r, 1, 15)
    if x == 13: return odd(r, 1, 17)
    if x == 14: return odd(r, 1, 21)
    if x == 16: return odd(r, 1, 17) or r == 23
    if x == 20: return odd(r, 1, 17) or r == 25
    if x == 23: return odd(r, 1, 17) or odd(r, 27, 45)
    if x >= 24: return odd(r, 1, 17) or r == 27
    return odd(r, 1, 17)

def k1083_P(x, r):
    if x == 5: return r >= 10
    if x == 7: return r >= 12
    if x == 9: return r >= 14
    if x == 11: return r >= 16
    if x == 13: return r >= 18
    if x == 15: return r in (19, 21, 23) or r >= 24
    if x == 16: return r in (19, 21)
    if x == 17: return r in (19, 21, 23) or r >= 24
    if x == 18: return r in (19, 21, 23)
    if x == 19: return r in (19, 21, 23) or r >= 25
    if x == 20: return r in (19, 21, 23, 25)
    if x == 21: return r in (19, 21, 23) or r >= 25
    if x == 22: return r in (19, 21, 23, 25)
    if x >= 23:
        base = r in (19, 21, 23, 25)
        band = r % 2 == 0 and 28 <= r <= qe(x + 22)
        tail = bool(x & 1) and r >= x + 23
        return base or band or tail
    return False

def k1083(x, r):
    if r == 0: return 0
    if r >= x + 23: return (x + 4) % 2
    if k1083_T(x, r): return 2
    if k1083_P(x, r): return 1
    return 0

# ---- closed form: parent H(R;(x,4);19) ----
def T(x, R):
    if x <= 14: return R % 2 == 1 and R <= qo(x + 4)
    if x == 15: return R % 2 == 1 and R <= 23
    if x in (16, 17, 18, 20, 21, 22): return R % 2 == 1 and R <= 19
    if x == 19: return (R % 2 == 1 and R <= 19) or R == 25
    if x == 23: return (R % 2 == 1 and R <= 19) or R == 27
    if x == 24: return (R % 2 == 1 and R <= 19) or (R % 2 == 1 and 27 <= R <= 47)
    return (R % 2 == 1 and R <= 19) or R == 27

def P(x, R):
    if x <= 14:
        if x % 2 == 1: return R >= x + 5
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
    band = R % 2 == 1 and 29 <= R <= qo(x + 23)
    tail = x % 2 == 1 and R >= x + 24
    return R in (20, 22, 24, 26) or band or tail

def F(x, R):
    if R == 0: return 0
    if R >= x + 24: return (x + 4) % 2
    t, p = T(x, R), P(x, R)
    assert not (t and p), ('TP overlap', x, R)
    return 2 if t else (1 if p else 0)

# Independently encoded set form.
def Tset(x):
    if x <= 14: return set(range(1, qo(x + 4) + 1, 2))
    if x == 15: return set(range(1, 24, 2))
    if x in (16, 17, 18, 20, 21, 22): return set(range(1, 20, 2))
    if x == 19: return set(range(1, 20, 2)) | {25}
    if x == 23: return set(range(1, 20, 2)) | {27}
    if x == 24: return set(range(1, 20, 2)) | set(range(27, 48, 2))
    return set(range(1, 20, 2)) | {27}

def Pset(x, L):
    if x <= 14:
        if x % 2 == 1: return set(range(x + 5, L + 1))
        return set()
    if x == 15: return set(range(20, L + 1)) - {21, 23}
    if x == 16: return {20, 22}
    if x == 17: return set(range(20, L + 1)) - {21, 23}
    if x == 18: return {20, 22, 24}
    if x == 19: return set(range(20, L + 1)) - {21, 23, 25}
    if x == 20: return {20, 22, 24}
    if x == 21: return set(range(20, L + 1)) - {21, 23, 25}
    if x == 22: return {20, 22, 24, 26}
    if x == 24: return {20, 22, 24, 26}
    if x == 23: return set(range(20, L + 1)) - {21, 23, 25, 27}
    out = {20, 22, 24, 26} | set(range(29, qo(x + 23) + 1, 2))
    if x % 2 == 1: out |= set(range(x + 24, L + 1))
    return out

# Static signature bands (R-space), derived from the anchors and the
# x-outer mex recurrence; every row tiles its parity class up to x+23.
BANDS = {
    4:  ([(1,7,'01'),(9,27,'1')], [(2,8,'23'),(10,26,'1')]),
    5:  ([(1,9,'01'),(11,27,'0')], [(2,8,'23'),(10,10,'03'),(12,28,'0')]),
    6:  ([(1,9,'01'),(11,29,'1')], [(2,10,'23'),(12,28,'1')]),
    7:  ([(1,11,'01'),(13,29,'0')], [(2,10,'23'),(12,12,'03'),(14,30,'0')]),
    8:  ([(1,11,'01'),(13,31,'1')], [(2,12,'23'),(14,30,'1')]),
    9:  ([(1,13,'01'),(15,31,'0')], [(2,12,'23'),(14,14,'03'),(16,32,'0')]),
    10: ([(1,13,'01'),(15,33,'1')], [(2,14,'23'),(16,32,'1')]),
    11: ([(1,15,'01'),(17,33,'0')], [(2,14,'23'),(16,16,'03'),(18,34,'0')]),
    12: ([(1,15,'01'),(17,35,'1')], [(2,16,'23'),(18,34,'1')]),
    13: ([(1,17,'01'),(19,35,'0')], [(2,16,'23'),(18,18,'03'),(20,36,'0')]),
    14: ([(1,17,'01'),(19,37,'1')], [(2,18,'23'),(20,22,'13'),(24,36,'1')]),
    15: ([(1,23,'01'),(25,37,'0')], [(2,18,'23'),(20,38,'0')]),
    16: ([(1,19,'01'),(21,39,'1')], [(2,18,'23'),(20,22,'02'),(24,24,'123'),(26,38,'1')]),
    17: ([(1,19,'01'),(21,23,'1'),(25,39,'0')], [(2,18,'23'),(20,20,'02'),(22,40,'0')]),
    18: ([(1,19,'01'),(21,41,'1')], [(2,18,'23'),(20,20,'02'),(22,22,'0'),(24,24,'02'),(26,40,'1')]),
    19: ([(1,19,'01'),(21,23,'1'),(25,25,'01'),(27,41,'0')], [(2,18,'23'),(20,20,'02'),(22,42,'0')]),
    20: ([(1,19,'01'),(21,43,'1')], [(2,18,'23'),(20,20,'02'),(22,24,'0'),(26,26,'123'),(28,42,'1')]),
    21: ([(1,19,'01'),(21,25,'1'),(27,43,'0')], [(2,18,'23'),(20,20,'02'),(22,44,'0')]),
    22: ([(1,19,'01'),(21,45,'1')], [(2,18,'23'),(20,20,'02'),(22,24,'0'),(26,26,'02'),(28,44,'1')]),
    23: ([(1,19,'01'),(21,25,'1'),(27,27,'01'),(29,45,'0')], [(2,18,'23'),(20,20,'02'),(22,24,'0'),(26,26,'02'),(28,46,'023')]),
    24: ([(1,19,'01'),(21,25,'1'),(27,47,'01')], [(2,18,'23'),(20,20,'02'),(22,24,'0'),(26,26,'02'),(28,28,'123'),(30,46,'1')]),
    25: ([(1,19,'01'),(21,25,'1'),(27,27,'01'),(29,47,'0')], [(2,18,'23'),(20,20,'02'),(22,24,'0'),(26,26,'02'),(28,28,'123'),(30,48,'12')]),
}

def expected_bands(x, p):
    if x <= 25: return BANDS[x][0] if p == 1 else BANDS[x][1]
    if p == 1: return [(1,19,'01'),(21,25,'1'),(27,27,'01'),(29,qo(x+23),'0')]
    return [(2,18,'23'),(20,20,'02'),(22,24,'0'),(26,26,'02'),(28,28,'123'),(30,qe(x+23),'1')]

def sig(x, R):
    r = R - 1
    if x == 4: a = b = k1098(4, r)
    else: a = F(x-1, r); b = k1098(x, r)
    c = 1 ^ k1083(x, r)
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

HROW_MAX = {15:24, 16:23, 17:24, 18:25, 19:24, 20:25, 21:26, 22:27}

def run():
    c = {}
    n = 0
    for x in range(4, 42):
        for R in range(x + 33):
            a = H_ordered(R, (x,4), 19); b = H_canon(R, (x,4), 19); d = F(x, R)
            assert a == b == d, ('parent', x, R, a, b, d); n += 1
    c['parent_two_raw_engines_vs_formula'] = n
    n = 0
    for x in range(3, 42):
        for R in range(x + 31):
            a = H_ordered(R, (x,3), 19); b = H_canon(R, (x,3), 19); d = k1098(x, R)
            assert a == b == d, ('B', x, R, a, b, d); n += 1
    c['K1098_B_anchor'] = n
    n = 0
    for x in range(4, 42):
        for R in range(x + 31):
            a = H_ordered(R, (x,4), 18); b = H_canon(R, (x,4), 18); d = k1083(x, R)
            assert a == b == d, ('C', x, R, a, b, d); n += 1
    c['K1083_C_anchor'] = n
    n = 0
    for x in range(4, 101):
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
            top = x + 23 if (x + 23) % 2 == p else x + 22
            assert prev == top, ('top', x, p, prev, top)
    c['signature_band_coverage_identity_mex'] = n
    n = 0
    for x in range(5, 501):
        for R in range(1, x + 24):
            assert MEX[sig(x, R)] == F(x, R), ('closure', x, R)
            n += 1
    c['induction_closure_sweep'] = n
    n = 0
    for x in range(4, 201):
        ts = Tset(x); ps = Pset(x, x + 85)
        assert ts.isdisjoint(ps), ('overlap', x)
        for R in range(x + 86):
            assert (R in ts) == T(x, R), ('Tset', x, R)
            assert (R in ps) == P(x, R), ('Pset', x, R)
            n += 1
    c['set_vs_predicate'] = n
    n = 0
    for x in range(4, 15):
        for R in range(x + 91):
            assert F(x, R) == single(x + 4, 19, R), ('lowfull', x, R)
            n += 1
    for x in range(15, 23):
        for R in range(HROW_MAX[x] + 1):
            assert F(x, R) == single(x + 4, 19, R), ('lowrow', x, R)
            n += 1
    for x in range(23, 201):
        for R in range(27):
            assert F(x, R) == single(x + 4, 19, R), ('lowuniform', x, R)
            n += 1
    c['height_only_initial_intervals'] = n
    witnesses = {15:(25,1,2),16:(24,0,1),17:(25,1,0),18:(26,0,1),19:(25,2,0),
                 20:(26,0,1),21:(27,1,0),22:(28,0,1),23:(27,2,0),25:(27,2,0),50:(27,2,0),200:(27,2,0)}
    for x,(R,a,b) in witnesses.items():
        assert F(x, R) == a and single(x + 4, 19, R) == b, ('witness', x, R)
    c['height_only_sharpness_witnesses'] = len(witnesses)
    n = 0
    for x in range(4, 41):
        for R in range(x + 24, x + 31):
            a = H_ordered(R, (x,4), 19); b = H_canon(R, (x,4), 19)
            assert a == b == (x + 4) % 2, ('tail', x, R, a, b)
            n += 1
    c['tail_direct'] = n
    n = 0
    for x in range(26, 30001):
        for p in (1, 0):
            for lo, hi, s in expected_bands(x, p):
                m = (lo + hi) // 2
                m += (p - m) % 2
                for R in {lo, hi, m}:
                    if lo <= R <= hi:
                        assert sig(x, R) == s and MEX[s] == F(x, R), ('deep', x, R)
                        n += 1
        for R in (x + 24, x + 25, x + 26, x + 31):
            assert F(x, R) == (x + 4) % 2, ('deep_tail', x, R)
            n += 1
    c['deep_affine_band_and_tail_samples'] = n
    rng = random.Random(20261122); n = 0
    for _ in range(3000):
        x = rng.randint(4, 10000); R = rng.randint(0, x + 60); v = F(x, R)
        assert v in (0, 1, 2) and not (T(x, R) and P(x, R))
        if R >= x + 24: assert v == (x + 4) % 2
        elif R >= 1: assert MEX[sig(x, R)] == v
        n += 1
    c['fixed_seed_scatter'] = n
    c['total_checks'] = sum(c.values())
    c['claim'] = 'H(R;(x,4);19), all x>=4 and R>=0'
    c['proof_status'] = 'proved_by_x_outer_induction_and_complete_symbolic_signature_bands'
    c['finite_audit_scope'] = {'parent':'4<=x<=41, 0<=R<=x+32, ordered/canonical/formula',
                               'B':'3<=x<=41, 0<=R<=x+30',
                               'C':'4<=x<=41, 0<=R<=x+30',
                               'bands':'4<=x<=100, complete 1<=R<=x+23',
                               'closure':'5<=x<=500, complete 1<=R<=x+23',
                               'deep':'26<=x<=30000, band endpoints/midpoints and tail samples',
                               'low_R':'x<=14 full rows to R<=x+90; x=15..22 exact prefixes; x>=23 R<=26',
                               'sets':'4<=x<=200, 0<=R<=x+85',
                               'parent_scope_x0':'x=4 is the multiset-collapse base row (A=B=K1098 x=4)',
                               'tail':'4<=x<=40, x+24<=R<=x+30',
                               'scatter_seed':20261122}
    c['ordered_states'] = H_ordered.cache_info().currsize
    c['canonical_states'] = H_canon.cache_info().currsize
    c['height_only'] = {'x<=14':'all R (window R<=x+90, constant tail identity)',
                        'row_max':{str(k):v for k,v in HROW_MAX.items()},
                        'x>=23':26,
                        'sharpness':'pin R=27=2y+z gives F=2 vs single=0 for every x>=23'}
    c['sharpness_first_mismatch'] = {str(k):list(v) for k,v in witnesses.items()}
    c['verifier_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    out = Path(__file__).resolve().parent / 'output' / 'audit.json'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(c, ensure_ascii=False, sort_keys=True, indent=2) + '\n', encoding='utf-8')
    return c

if __name__ == '__main__':
    print(json.dumps(run(), ensure_ascii=False, sort_keys=True, indent=2))
