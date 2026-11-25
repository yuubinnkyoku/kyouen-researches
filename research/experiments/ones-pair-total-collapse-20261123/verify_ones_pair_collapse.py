#!/usr/bin/env python3
"""
verify_ones_pair_collapse.py -- machine audit for the ones-pair total collapse.

THEOREM (ones-pair total collapse, universal structural induction; see report.md):
  For every z>=0 and every R>=0:   H(R;(1,1);z) = v(2, z, R)

i.e. the {1,1} row of the kappa=1 residual game collapses to the single token
(sum 2) residual for ALL residual R, not only inside the K1264 staircase
window R<=z+min(X)=z+1. This closes K1264's open problem 2 (the {1,1}
no-separation observation).

Proof (report.md): Lemma V1 (full characterization of the x=1 single-token
residual: v(1,z,n)=0 at n=0; 2 at n=1 with z>=1; 1 otherwise) via induction on
n, then strong induction on R: z>=1 -> option sets identical because
v(1,z+1,R-1)=v(1,z,R-1) for all n; z=0 -> the B-child {v(1,1,R-1)} and the
A-child {v(1,0,R-1)} differ only at n=1 (2 vs 1) where both mexes are 0.

The universal claim rests on the written induction in report.md. This machine
provides: dual raw engines cross-checked pointwise against the published K0832
closed form, Lemma V1 exhaustives, {1,1} theorem sweeps (exhaustive + fixed-
seed random deep), {1}^t separation census, and witness anchors (including
published K1264 witnesses). Fail-closed: any bad point => rc=1. Deterministic
output: sorted JSON. --tamper runs the mutation battery (each MUST be caught).
"""
import sys, json, hashlib, random
from functools import lru_cache

sys.setrecursionlimit(1_000_000)

def mex(values):
    values = set(values)
    m = 0
    while m in values:
        m += 1
    return m

# ------------------------------------------------------------------
# Raw engines + single-token wrappers: byte-exact transcription from the
# published K1264 verifier verify_min_token_staircase.py
# (SHA-256 108fdd65...; provenance chain K1138 -> y22 machine K1257 ->
#  K1264 machine -> this machine). Extracted mechanically by
#  build_verifier.py (assembler kept in the experiment dir).
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
# Published K0832 single-token closed form: byte-exact transcription from
# the published K1264 verifier (same source, mechanically extracted).
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

def char1(z, n):
    """Lemma V1 characteristic function of the x=1 single-token residual:
    v(1,z,n) = 0 (n=0) / 2 (n=1, z>=1) / 1 (n>=1 with n>=2 or z=0)."""
    if n == 0:
        return 0
    if n == 1:
        return 2 if z >= 1 else 1
    return 1

def check_D0():
    # provenance anchor: raw single-token engines vs published closed form
    bad1 = bad2 = pts = 0
    for x in range(1, 41):
        for z in range(0, 22):
            rmax = min(x + z + 2, 40)
            for R in range(0, rmax + 1):
                s = single_token(x, z, R)
                pts += 2
                if vC(x, z, R) != s: bad1 += 1
                if vO(x, z, R) != s: bad2 += 1
    return {'label': 'D0 raw-vs-closedform anchor', 'points': pts,
            'bad_canonical': bad1, 'bad_ordered': bad2}

def check_D1():
    # Lemma V1 exhaustive: raw x=1 residuals + closed form vs characteristic
    bad = pts = 0
    for z in range(0, 51):
        for n in range(0, z + 17):
            c = char1(z, n)
            pts += 3
            if vC(1, z, n) != c: bad += 1
            if vO(1, z, n) != c: bad += 1
            if single_token(1, z, n) != c: bad += 1
    return {'label': 'D1 Lemma V1 characterization', 'points': pts, 'bad': bad}

def check_D2():
    # {1,1} theorem sweep: z 0..30, R 0..min(z+13,43), 3-way
    bad = pts = 0
    for z in range(0, 31):
        for R in range(0, min(z + 13, 43) + 1):
            s = single_token(2, z, R)
            go = H_ordered(R, (1, 1), z)
            gc = H_canonical(R, (1, 1), z)
            pts += 3
            if gc != s: bad += 1
            if go != s: bad += 1
            if go != gc: bad += 1
    return {'label': 'D2 ones-pair theorem sweep', 'points': pts, 'bad': bad}

def check_D3(seed=20261124):
    # fixed-seed random deep: 400 shallow-deep + 100 beyond-window
    rng = random.Random(seed)
    bad = pts = 0
    for _ in range(400):
        z = rng.randint(0, 60)
        R = rng.randint(0, z + 16)
        s = single_token(2, z, R)
        go = H_ordered(R, (1, 1), z)
        gc = H_canonical(R, (1, 1), z)
        pts += 3
        if gc != s: bad += 1
        if go != s: bad += 1
        if go != gc: bad += 1
    for _ in range(100):
        z = rng.randint(0, 40)
        R = rng.randint(z + 17, z + 28)
        s = single_token(2, z, R)
        go = H_ordered(R, (1, 1), z)
        gc = H_canonical(R, (1, 1), z)
        pts += 3
        if gc != s: bad += 1
        if go != s: bad += 1
        if go != gc: bad += 1
    return {'label': 'D3 ones-pair random deep (fixed seed)',
            'points': pts, 'bad': bad}

def check_D4():
    # {1}^t census t=2..6: t=2 must be bad 0 (corollary); t>=3 break census
    bad2 = pts = 0
    breaks = {}
    first_break = {}
    for t in range(2, 7):
        b = 0
        for z in range(0, 17):
            for R in range(0, z + 11):
                s = single_token(t, z, R)
                gc = H_canonical(R, (1,) * t, z)
                pts += 1
                if gc != s:
                    b += 1
                    if t not in first_break:
                        first_break[t] = [z, R, gc, s]
        breaks[t] = b
        if t == 2:
            bad2 = b
    return {'label': 'D4 ones^t census', 'points': pts, 'bad_t2': bad2,
            'breaks_by_t': {str(k): v for k, v in sorted(breaks.items())},
            'first_break': {str(k): v for k, v in sorted(first_break.items())}}

def check_D5():
    # witness anchors; each: 2 parent-engine comps + 1 single comp + 2 window-row comps
    anchors = [
        ((1, 1), 0, 1, 'ones-pair z=0,R=1 equality anchor'),
        ((1, 1), 0, 2, 'ones-pair z=0,R=2 equality anchor'),
        ((1, 1, 1), 0, 3, 'ones^3 z=0,R=3 separation anchor (pre-declaration probe)'),
        ((1, 1, 1), 1, 3, 'published K1264 witness ones^3 z=1,R=3'),
        ((2, 1), 1, 3, 'published K1264 sharpness witness (2,1) z=1,R=3'),
        ((1, 1), 1, 3, 'ones-pair z=1,R=3 boundary+1 collapse counterpoint'),
    ]
    published_expect = {
        ((1, 1, 1), 1, 3): (2, 0),   # parent 2, single 0 (published)
        ((2, 1), 1, 3): (2, 0),      # parent 2, single 0 (published)
        ((1, 1, 1), 0, 3): (0, 1),   # pre-declaration probe: parent 0, single 1
    }
    bad = pts = 0
    details = []
    for (X, z, R, src) in anchors:
        xs = tuple(X)
        go = H_ordered(R, xs, z)
        gc = H_canonical(R, xs, z)
        s = single_token(sum(xs), z, R)
        pts += 3
        if go != gc: bad += 1
        if (X, z, R) in published_expect:
            ep, es = published_expect[(X, z, R)]
            pts += 1
            if gc != ep or s != es: bad += 1
            equal = (gc == s)
        else:
            equal = (gc == s)
            if xs == (1, 1) and not equal: bad += 1
        # window row equality R=z+min
        Rw = z + min(xs)
        eW = single_token(sum(xs), z, Rw)
        pts += 2
        if H_canonical(Rw, xs, z) != eW: bad += 1
        if H_ordered(Rw, xs, z) != eW: bad += 1
        details.append({'X': list(xs), 'z': z, 'R': R, 'parent': gc,
                        'single': s, 'equal': equal, 'src': src})
    return {'label': 'D5 witness anchors', 'points': pts, 'bad': bad,
            'details': details}

def run_audit():
    res = {}
    res['D0'] = check_D0()
    H_ordered.cache_clear(); H_canonical.cache_clear()
    res['D1'] = check_D1()
    H_ordered.cache_clear(); H_canonical.cache_clear()
    res['D2'] = check_D2()
    H_ordered.cache_clear(); H_canonical.cache_clear()
    res['D3'] = check_D3()
    H_ordered.cache_clear(); H_canonical.cache_clear()
    res['D4'] = check_D4()
    H_ordered.cache_clear(); H_canonical.cache_clear()
    res['D5'] = check_D5()
    total_bad = 0
    for k in sorted(res):
        v = res[k]
        total_bad += sum(x for kk, x in v.items()
                         if kk == 'bad' or kk.startswith('bad_'))
    res['meta'] = {
        'verifier_sha256': SELF_SHA,
        'total_bad': total_bad,
        'theorem': 'ones-pair total collapse: H(R;(1,1);z)=v(2,z,R) for all z>=0, R>=0',
        'proof': 'structural strong induction on R (report.md); Lemma V1 characterizes v(1,z,n)',
    }
    return res, total_bad

# =====================================================================
# Tamper battery (--tamper): each mutation MUST be caught (bad>0).
# =====================================================================
@lru_cache(maxsize=2_000_000)
def H_ordered_noC(R, X, z):
    if R == 0: return 0
    opts = set()
    for i, v in enumerate(X):
        if v > 1:
            opts.add(H_ordered_noC(R - 1, X[:i] + (v - 1,) + X[i + 1:], z))
        else:
            opts.add(H_ordered_noC(R - 1, X[:i] + X[i + 1:], z + 1))
    return mex(opts)

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
        print(f"{'CAUGHT' if bad > 0 else 'TAMPER-MISSED'}: {name} bad={bad}")
        return bad

    total = 0
    # M1: theorem falsely extended to {1,1,1} -- break must exist.
    bad = 0
    for z in range(0, 9):
        for R in range(0, z + 9):
            if H_canonical(R, (1, 1, 1), z) != single_token(3, z, R): bad += 1
    total += rec('M1 collapse claimed for ones^3', bad)
    # M2: Lemma V1 z=0 case flipped (n=1 claimed 2 at z=0).
    bad = 0
    for z in range(0, 31):
        for n in range(0, min(z + 10, 40) + 1):
            c = 2 if n == 1 else char1(z, n)
            if vC(1, z, n) != c or vO(1, z, n) != c: bad += 1
    total += rec('M2 Lemma V1 z=0 case flipped', bad)
    # M3: Lemma V1 n>=2 corrupted to (z+n)%2.
    bad = 0
    for z in range(0, 31):
        for n in range(0, min(z + 10, 40) + 1):
            c = (z + n) % 2 if n >= 2 else char1(z, n)
            if vC(1, z, n) != c: bad += 1
    total += rec('M3 Lemma V1 n>=2 parity corrupted', bad)
    # M4: corrupted q_odd closed form -- anchor must find bads.
    bad = 0
    for x in range(2, 51):
        for z in range(1, 31):
            for R in range(0, min(x + z, 40) + 1):
                if single_token_mut(x, z, R) != vC(x, z, R): bad += 1
    total += rec('M4 corrupted q_odd closed form', bad)
    # M5: C-move removed from ordered engine (for the {1,1} row).
    bad = 0
    for z in range(1, 13):
        for R in range(1, z + 9):
            if H_ordered_noC(R, (1, 1), z) != H_canonical(R, (1, 1), z): bad += 1
    total += rec('M5 ordered engine without C-move', bad)
    # M6: z=0 option values falsely claimed equal (v(1,1,1) vs v(1,0,1)).
    b_val, a_val = vC(1, 1, 1), vC(1, 0, 1)
    bad = 0 if b_val == a_val else 1
    total += rec('M6 z=0 option-value equality claim', bad)
    # M7: published witness parent flip ({1}^3@z=1,R=3 expected 2 -> 0).
    bad = 0 if H_canonical(3, (1, 1, 1), 1) == 0 else 1
    total += rec('M7 published witness parent flip', bad)
    # M8: (1,1)@z=0,R=1 anchor parent flip (1 -> 0).
    bad = 0 if H_canonical(1, (1, 1), 0) == 0 else 1
    total += rec('M8 ones-pair z=0 anchor parent flip', bad)

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
            pts += res[k].get('points', 0)
        print('TOTAL points checked:', pts)
        if bad:
            print('AUDIT FAIL: bad =', bad)
            sys.exit(1)
        print('AUDIT PASS')
        sys.exit(0)

if __name__ == '__main__':
    main()
