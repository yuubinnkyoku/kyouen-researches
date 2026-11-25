#!/usr/bin/env python3
"""verify_ones_row_frontier.py -- machine audit for the declared claims of the
single-owner note 55e6b109 ({1}^t row window-edge frontier):
  M-RC   : closed form for A_j(k,z) = H(z+2-2j; {1}^k; z) (all j,k,z, R>=1)
  M-DIAG : the j=0 diagonal H(z+2;{1}^t;z)
  M-SEP  : window-edge separation set S(t) of the {1}^t row (all t, all z)
Declared checks (PUBLISH-THEN-EXECUTE, note 55e6b109):
  D1 A-family full-state sweep: j=0..7, k=0..44, all valid z
     (both raw engines vs CFG; 26,190 points / 78,570 comparisons predicted)
  D2 diagonal values: t=1..44 x z=1..50 vs CFG + z=0 column
     (2,244 points / 4,488 comparisons predicted)
  D3 separation law sweep: t=1..44 x z=0..54, separation iff z in S(t),
     single side closed-form/vC/vO triple engine agreement
     (2,420 points / 9,680 comparisons / 546 separating pairs predicted)
  D4 published anchors: mex-chain paragraphs (a)/(b)/(d), T1 (K1267 E2),
     T2 supplementary values (published uw report, t=2..16), K1265 row,
     K1268 E5 published sparse patterns (t=3,5,7)
     (225 points / 472 comparisons predicted)
  TOTAL declared: 31,079 points / 93,210 comparisons / bad 0.
Fail-closed: any bad>0 -> rc=1; declared-count mismatch -> rc=1 (honest
record requirement).  Finite machine audit is NOT the proof: the universal
claim rests on the paper induction in report.md (mex chains, strong
induction on the budget R).
--tamper runs the 10-mutation battery (every mutation MUST be caught).
"""
import sys, json, hashlib
from functools import lru_cache

sys.setrecursionlimit(1_000_000)

# === ENGINE BLOCK (machine-extracted; see build_engine_from_published.py) ===
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
# === END ENGINE BLOCK ===

SELF_SHA = hashlib.sha256(open(__file__, 'rb').read()).hexdigest()

def clear_engines():
    # value-transparent memo reset (bounds live cache entries only)
    H_ordered.cache_clear()
    H_canonical.cache_clear()

def ones(k):
    return tuple([1] * k)

# ---------------------------------------------------------------
# the declared closed form (M-RC)
# ---------------------------------------------------------------
def cfg_A(k, j, z):
    R = z + 2 - 2 * j
    if R < 1:
        raise ValueError((k, j, z))
    if k % 2 == 1:
        if z % 2 == 1 and z <= k + 2 * j - 2:
            return 2
        if z >= k + 2 * j - 1:
            return 1
        return 0
    if z % 2 == 1 and z <= k + 2 * j - 3:
        return 2
    return 0

def parent_d(t, z):
    # H(z+2;{1}^t;z) per M-DIAG (= cfg_A(t,0,z)), z>=1
    return cfg_A(t, 0, z)

def sep_set(t):
    # declared M-SEP law; returns the set of z's separating at window edge
    if t <= 2:
        return set()
    S = {0}
    if t % 2 == 0:
        S |= {z for z in range(1, t - 2, 2) if z <= t - 3}
    else:
        S |= {z for z in range(1, t - 1, 2) if z <= t - 2}
        S |= {t - 1, t}
    return S

def R_of(z):
    return 3 if z == 0 else z + 2

# ---------------------------------------------------------------
# D1: A-family full-state sweep
# ---------------------------------------------------------------
def check_D1():
    pts, comps, bad = 0, 0, 0
    details = []
    for j in range(0, 8):
        for k in range(0, 45):
            zmin = max(1, 2 * j - 1)
            for z in range(zmin, k + 2 * j + 50):
                R = z + 2 - 2 * j
                hc = H_canonical(R, ones(k), z)
                ho = H_ordered(R, ones(k), z)
                c = cfg_A(k, j, z)
                comps += 3
                if hc != c or ho != c or hc != ho:
                    bad += 1
                    if len(details) < 20:
                        details.append((k, j, z, hc, ho, c))
                pts += 1
    return {'points': pts, 'comparisons': comps, 'bad': bad,
            'details_mismatch': details}

# ---------------------------------------------------------------
# D2: diagonal values (j=0) + z=0 column
# ---------------------------------------------------------------
def check_D2():
    pts, comps, bad = 0, 0, 0
    details = []
    for t in range(1, 45):
        for z in range(1, 51):
            hc = H_canonical(z + 2, ones(t), z)
            ho = H_ordered(z + 2, ones(t), z)
            c = parent_d(t, z)
            comps += 2
            if hc != c or ho != c:
                bad += 1
                details.append(('diag', t, z, hc, ho, c))
            pts += 1
    for t in range(1, 45):
        exp = 1 if t == 1 else 0
        hc = H_canonical(3, ones(t), 0)
        ho = H_ordered(3, ones(t), 0)
        comps += 2
        if hc != exp or ho != exp:
            bad += 1
            details.append(('z0', t, hc, ho, exp))
        pts += 1
    return {'points': pts, 'comparisons': comps, 'bad': bad,
            'details_mismatch': details}

# ---------------------------------------------------------------
# D3: separation law sweep
# ---------------------------------------------------------------
SEP_POINTS_CLAIMED = 546

def check_D3():
    pts, comps, bad = 0, 0, 0
    sep_count = 0
    details = []
    for t in range(1, 45):
        S = sep_set(t)
        for z in range(0, 55):
            R = R_of(z)
            hc = H_canonical(R, ones(t), z)
            ho = H_ordered(R, ones(t), z)
            sin = single_token(t, z, R)
            sc = vC(t, z, R)
            so = vO(t, z, R)
            claimed_in = z in S
            actual_sep = (hc != sin)
            comps += 4
            if sin != sc or sin != so or hc != ho or actual_sep != claimed_in:
                bad += 1
                details.append((t, z, hc, sin, sc, so, claimed_in))
            if actual_sep:
                sep_count += 1
            pts += 1
    if sep_count != SEP_POINTS_CLAIMED:
        bad += 1
        details.append(('sep_count', sep_count, SEP_POINTS_CLAIMED))
    return {'points': pts, 'comparisons': comps, 'bad': bad,
            'sep_points': sep_count, 'sep_points_claimed': SEP_POINTS_CLAIMED,
            'details_mismatch': details}

# ---------------------------------------------------------------
# D4: published anchors
# ---------------------------------------------------------------
E5_ANCHORS = [(3, [0, 1, 2, 3]), (5, [0, 1, 3, 4, 5]), (7, [0, 1, 3, 5, 6, 7])]

def check_D4():
    pts, comps, bad = 0, 0, 0
    details = []
    # (a) H(1;{1}^j;z)=2 for j>=1, z>=2 (published chain para (a))
    for j in range(1, 13):
        for z in (2, 4, 6):
            hc = H_canonical(1, ones(j), z)
            ho = H_ordered(1, ones(j), z)
            comps += 2
            if hc != 2 or ho != 2:
                bad += 1
                details.append(('a', j, z, hc, ho))
            pts += 1
    # (b) H(2;{1}^k;z)=0 for k>=2, z>=2 (published chain para (b))
    for k in range(2, 13):
        for z in (2, 4, 6):
            hc = H_canonical(2, ones(k), z)
            ho = H_ordered(2, ones(k), z)
            comps += 2
            if hc != 0 or ho != 0:
                bad += 1
                details.append(('b', k, z, hc, ho))
            pts += 1
    # (d) H(2;{1}^t;0)=0 for t>=2 (published chain para (d))
    for t in range(2, 13):
        hc = H_canonical(2, ones(t), 0)
        ho = H_ordered(2, ones(t), 0)
        comps += 2
        if hc != 0 or ho != 0:
            bad += 1
            details.append(('d', t, hc, ho))
        pts += 1
    # T1 (K1267 E2): {1}^t @(0,3) parent 0 vs single 1, t=3..12
    for t in range(3, 13):
        hc = H_canonical(3, ones(t), 0)
        ho = H_ordered(3, ones(t), 0)
        sin = single_token(t, 0, 3)
        comps += 3
        if hc != 0 or ho != 0 or sin != 1:
            bad += 1
            details.append(('T1', t, hc, ho, sin))
        pts += 1
    # T2 published supplementary values: {1}^t @(1,3) parent 2 (t>=3),
    # t=2 collapse 0=0; both engines, t=2..16
    for t in range(2, 17):
        exp = 2 if t >= 3 else 0
        hc = H_canonical(3, ones(t), 1)
        ho = H_ordered(3, ones(t), 1)
        sin = single_token(t, 1, 3)
        comps += 3
        if hc != exp or ho != exp or sin != 0:
            bad += 1
            details.append(('T2', t, hc, ho, sin))
        pts += 1
    # K1265 row quotation: H(R;{1,1};z) == v(2,z,R) for z<=12, R<=8
    for z in range(0, 13):
        for R in range(0, 9):
            target = single_token(2, z, R)
            hc = H_canonical(R, (1, 1), z)
            ho = H_ordered(R, (1, 1), z)
            comps += 2
            if hc != target or ho != target:
                bad += 1
                details.append(('K1265', z, R, hc, ho, target))
            pts += 1
    # K1268 E5 published sparse patterns: S(t) cap [0,24] literal equality
    for (t, expected) in E5_ANCHORS:
        S = sep_set(t)
        got = sorted(z for z in range(0, 25) if z in S)
        comps += 1
        if got != expected:
            bad += 1
            details.append(('E5', t, got, expected))
        pts += 1
    return {'points': pts, 'comparisons': comps, 'bad': bad,
            'details_mismatch': details}

# =====================================================================
# tamper battery (10 mutations; every one must be caught, rc=1 otherwise)
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

@lru_cache(maxsize=1_000_000)
def H_ordered_noXOR(R, X, z):
    if R == 0: return 0
    opts = set()
    for i, w in enumerate(X):
        if w > 1:
            opts.add(H_ordered_noXOR(R - 1, X[:i] + (w - 1,) + X[i + 1:], z))
        else:
            opts.add(H_ordered_noXOR(R - 1, X[:i] + X[i + 1:], z + 1))
    if z >= 1:
        opts.add(H_ordered_noXOR(R - 1, X, z - 1))
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

def cfg_mut_thresholds(k, j, z):
    # M1: odd-k 2-band threshold -1 (effective; +1 is parity-protected as
    # k+2j-1 is even for odd k, so the band set is unchanged -- disclosed)
    R = z + 2 - 2 * j
    if R < 1: raise ValueError((k, j, z))
    if k % 2 == 1:
        if z % 2 == 1 and z <= k + 2 * j - 3: return 2
        if z >= k + 2 * j - 1: return 1
        return 0
    if z % 2 == 1 and z <= k + 2 * j - 3: return 2
    return 0

def cfg_mut_no1band(k, j, z):
    # M2: odd-k 1-region dropped
    R = z + 2 - 2 * j
    if R < 1: raise ValueError((k, j, z))
    if k % 2 == 1:
        if z % 2 == 1 and z <= k + 2 * j - 2: return 2
        return 0
    if z % 2 == 1 and z <= k + 2 * j - 3: return 2
    return 0

def cfg_mut_parity(k, j, z):
    # M3: 2-band parity flipped (both parities)
    R = z + 2 - 2 * j
    if R < 1: raise ValueError((k, j, z))
    if k % 2 == 1:
        if z % 2 == 0 and z <= k + 2 * j - 2: return 2
        if z >= k + 2 * j - 1: return 1
        return 0
    if z % 2 == 0 and z <= k + 2 * j - 3: return 2
    return 0

def cfg_mut_even_threshold(k, j, z):
    # M4: even-k 2-band threshold -2
    R = z + 2 - 2 * j
    if R < 1: raise ValueError((k, j, z))
    if k % 2 == 1:
        if z % 2 == 1 and z <= k + 2 * j - 2: return 2
        if z >= k + 2 * j - 1: return 1
        return 0
    if z % 2 == 1 and z <= k + 2 * j - 5: return 2
    return 0

def sep_set_mut(t):
    # M10: even-t staircase corrupted (z <= t-1 instead of t-3)
    if t <= 2: return set()
    S = {0}
    if t % 2 == 0:
        S |= {z for z in range(1, t, 2)}
    else:
        S |= {z for z in range(1, t - 1, 2) if z <= t - 2}
        S |= {t - 1, t}
    return S

def tamper():
    results = []

    def rec(name, bad):
        results.append({'mutation': name, 'bad': bad})
        print(('CAUGHT' if bad > 0 else 'TAMPER-MISSED') + ': ' + name +
              ' bad=' + str(bad))
        return bad

    # M1: CFG odd-k 2-band threshold -1 (+1 is a documented no-op:
    # k+2j-1 is even for odd k so the odd-z band is parity-protected)
    bad = 0
    for j in range(0, 6):
        for k in range(1, 40, 2):
            for z in range(max(1, 2 * j - 1), k + 2 * j + 20):
                R = z + 2 - 2 * j
                if H_canonical(R, ones(k), z) != cfg_mut_thresholds(k, j, z):
                    bad += 1
    rec('M1 CFG odd-k 2-band threshold -1 (+1 is a parity-protected no-op, disclosed)', bad)
    # M2: CFG odd-k 1-region dropped
    bad = 0
    for j in range(0, 6):
        for k in range(1, 40, 2):
            for z in range(max(1, 2 * j - 1), k + 2 * j + 20):
                R = z + 2 - 2 * j
                if H_canonical(R, ones(k), z) != cfg_mut_no1band(k, j, z):
                    bad += 1
    rec('M2 CFG odd-k 1-region dropped', bad)
    # M3: CFG 2-band parity flip
    bad = 0
    for (j, k, z) in [(0, 5, 4), (0, 7, 6), (1, 5, 4), (0, 4, 3), (0, 6, 5), (1, 4, 3)]:
        R = z + 2 - 2 * j
        if H_canonical(R, ones(k), z) != cfg_mut_parity(k, j, z):
            bad += 1
    rec('M3 CFG 2-band parity flip', bad)
    # M4: CFG even-k threshold -2
    bad = 0
    for j in range(0, 6):
        for k in range(2, 41, 2):
            for z in range(max(1, 2 * j - 1), k + 2 * j + 20):
                R = z + 2 - 2 * j
                if z % 2 == 1 and z <= k + 2 * j - 3:
                    if H_canonical(R, ones(k), z) != cfg_mut_even_threshold(k, j, z):
                        bad += 1
    rec('M4 CFG even-k threshold -2', bad)
    # M5: z=0 boundary claim flip (parent 2 for t>=3)
    bad = 0
    for t in range(3, 20):
        if H_canonical(3, ones(t), 0) != 2: bad += 1
    rec('M5 z=0 boundary flip claim', bad)
    # M6: engine without C-move
    bad = 0
    for t in range(2, 9):
        for z in range(0, 6):
            for R in range(1, 7):
                if H_ordered_noC(R, ones(t), z) != H_canonical(R, ones(t), z):
                    bad += 1
    rec('M6 ordered engine without C-move', bad)
    # M7: engine without B z-increment
    bad = 0
    for t in range(2, 9):
        for z in range(0, 6):
            for R in range(1, 7):
                if H_ordered_noBinc(R, ones(t), z) != H_canonical(R, ones(t), z):
                    bad += 1
    rec('M7 ordered engine without B z-increment', bad)
    # M8: C-move without the 1^ (nimber) flip
    bad = 0
    for t in range(1, 8):
        for z in range(0, 7):
            for R in range(1, 7):
                if H_ordered_noXOR(R, ones(t), z) != H_canonical(R, ones(t), z):
                    bad += 1
    rec('M8 C-move without 1^ flip', bad)
    # M9: corrupted q_odd closed form
    bad = 0
    for x in range(2, 41):
        for z in range(1, 31):
            for R in range(0, min(x + z, 31) + 1):
                if single_token_mut(x, z, R) != vC(x, z, R): bad += 1
    rec('M9 corrupted q_odd closed form', bad)
    # M10: S(t) law corruption (even-t)
    bad = 0
    for t in range(1, 45):
        S = sep_set_mut(t)
        for z in range(0, 55):
            R = R_of(z)
            actual = (H_canonical(R, ones(t), z) != single_token(t, z, R))
            if actual != (z in S): bad += 1
    rec('M10 S(t) even-t staircase corruption', bad)
    missed = [r['mutation'] for r in results if r['bad'] == 0]
    print('TAMPER BATTERY:', 'ALL CAUGHT' if not missed else 'MISSED: ' + str(missed))
    if missed: sys.exit(1)
    sys.exit(0)

# ---------------------------------------------------------------
DECLARED_TOTALS = {'points': 31079, 'comparisons': 93210}

def run_audit():
    res = {}
    res['D1'] = check_D1()
    clear_engines()
    res['D2'] = check_D2()
    clear_engines()
    res['D3'] = check_D3()
    clear_engines()
    res['D4'] = check_D4()
    total_bad = sum(res[k]['bad'] for k in ('D1', 'D2', 'D3', 'D4'))
    pts = sum(res[k]['points'] for k in ('D1', 'D2', 'D3', 'D4'))
    comps = sum(res[k]['comparisons'] for k in ('D1', 'D2', 'D3', 'D4'))
    count_bad = 0
    if pts != DECLARED_TOTALS['points']:
        count_bad += 1
    if comps != DECLARED_TOTALS['comparisons']:
        count_bad += 1
    res['summary'] = {
        'n_bad': total_bad + count_bad,
        'theorem': ('M-RC/M-DIAG/M-SEP: {1}^t row window-edge frontier '
                    '(published note 55e6b109). Universal claim proved on '
                    'paper in report.md; engines corroborate the declared grid.'),
        'declared_totals': DECLARED_TOTALS,
        'observed_totals': {'points': pts, 'comparisons': comps},
        'meta': {'verifier_sha256': SELF_SHA},
    }
    res['points_totals'] = {k: res[k]['points'] for k in ('D1', 'D2', 'D3', 'D4')}
    res['comparisons_totals'] = {k: res[k]['comparisons'] for k in ('D1', 'D2', 'D3', 'D4')}
    sep_sets = {}
    for t in range(1, 45):
        S = sep_set(t)
        sep_sets[t] = len(S)
    res['sep_set_sizes'] = sep_sets
    return res, total_bad + count_bad, pts, comps

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else 'audit'
    if mode == 'tamper':
        tamper(); return
    res, bad, pts, comps = run_audit()
    with open('output/audit.json', 'w') as f:
        f.write(json.dumps(res, indent=1, sort_keys=True, ensure_ascii=True) + '\n')
    print('TOTAL points:', pts, 'comparisons:', comps, 'bad:', bad)
    print('D3 sep points:', res['D3']['sep_points'],
          '(claimed', res['D3']['sep_points_claimed'], ')')
    if bad:
        print('AUDIT FAIL: bad =', bad); sys.exit(1)
    print('AUDIT PASS'); sys.exit(0)

if __name__ == '__main__':
    main()
