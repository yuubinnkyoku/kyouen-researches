#!/usr/bin/env python3
"""verify_unified_window_sharpness.py -- machine audit for:
(1) T1 (theorem, proved on paper in report.md): {1}^t separates at (z,R)=(0,3)
    for every t>=3 (parent H=0 vs single v=1); {1}^2 collapses (K1265).
(2) Unified-window max(z+min(X),2) CELL-SHARPNESS census (observed):
    per cell (z,m): minimal separating two-token witness X=(m+d,m) at
    R*=W+1, W:=max(z+m,2); negative cells get d-extension and an arity>=3
    battery; all findings recorded as census (NOT failures).
(3) Diagonal-line checks L1/L2 (published witnesses m<=6; parent-2 is a
    PRE-REGISTERED prediction; refutation is recorded, not an error).
(4) K1264 C4 boundary census recount over the published domain
    (y 1..8, d 0..24, z 0..26, Rb=z+y+1) -> must equal published
    180/37/32/31/26/25/20/19 (fail-closed).

Fail-closed rules (rc=1 on any bad): window-edge equalities (both engines vs
published closed form), engine mutual agreement, published anchor values,
C4 recount vs published. Separations at boundary+1 are census records.

Engines + closed form: byte-exact block machine-extracted from the published
K1264 verifier (see build_unified_verifier.py; sha-gated).
--tamper runs the mutation battery (each mutation MUST be caught).
"""
import sys, json, hashlib
from functools import lru_cache

sys.setrecursionlimit(1_000_000)

# === ENGINE BLOCK (machine-extracted from published K1264 verifier) ===
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

# ---------------------------------------------------------------
# unified window W(z,m) = max(z+m, 2)   (K1264 staircase + K0832 R<=2 clause)
# ---------------------------------------------------------------
def W_of(z, m):
    return max(z + m, 2)

def clear_engines():
    # value-transparent memo reset (sandbox memory cap ~1.0 GiB):
    # bounds live cache entries; pure deterministic recursion is unaffected.
    H_ordered.cache_clear()
    H_canonical.cache_clear()

# ---------------------------------------------------------------
# E0: closed-form x dual-engine anchor grid
# ---------------------------------------------------------------
def check_E0():
    bad = pts = 0
    for x in range(1, 61):
        if x % 20 == 0:
            clear_engines()
        for z in range(0, 31):
            rmax = min(x + z + 2, 50)
            for R in range(0, rmax + 1):
                s = single_token(x, z, R)
                pts += 1
                if vC(x, z, R) != s: bad += 1
                if vO(x, z, R) != s: bad += 1
    return {'label': 'E0 closedform x dual-engine anchor grid',
            'points': pts, 'comparisons': pts * 2, 'bad': bad}

# ---------------------------------------------------------------
# E1: published witness anchors (K1264 C5 x11 + K1265 D5 x6;
#     (2,1)@z=1,R=3 appears in both -> counted twice, as declared)
# spec: (X, z, R, expected_parent, expected_single, src)
#   expected_parent None -> expect Hc==Ho==closedform (control point)
# ---------------------------------------------------------------
ANCHORS = [
    ((12, 6), 17, 24, 0, 1, 'K1087 z=17 witness (K1264 C5)'),
    ((12, 6), 18, 25, 0, 2, 'K1259 z=18 witness (K1264 C5)'),
    ((14, 6), 19, 26, 0, 1, 'K1261 z=19 witness (K1264 C5)'),
    ((16, 6), 20, 27, 2, 1, 'K1262 z=20 witness (K1264 C5)'),
    ((2, 1), 1, 3, 2, 0, 'staircase sharpness (2,1) (K1264 C5)'),
    ((1, 1, 1), 1, 3, 2, 0, 'staircase sharpness {1}^3 (K1264 C5)'),
    ((2, 2), 2, 5, 2, 1, 'staircase sharpness (2,2) (K1264 C5)'),
    ((4, 3), 5, 9, 2, 0, 'staircase sharpness (4,3) (K1264 C5)'),
    ((4, 4), 6, 11, 2, 1, 'staircase sharpness (4,4) (K1264 C5)'),
    ((6, 5), 9, 15, 2, 0, 'staircase sharpness (6,5) (K1264 C5)'),
    ((6, 6), 10, 17, 2, 1, 'staircase sharpness (6,6) (K1264 C5)'),
    ((1, 1), 0, 1, 1, 1, 'K1265 D5 (1,1)@0,1 collapse'),
    ((1, 1), 0, 2, 0, 0, 'K1265 D5 (1,1)@0,2 collapse'),
    ((1, 1, 1), 0, 3, 0, 1, 'K1265 D5 {1}^3@0,3 separation'),
    ((1, 1, 1), 1, 3, 2, 0, 'K1265 D5 {1}^3@1,3 (K1264 published)'),
    ((2, 1), 1, 3, 2, 0, 'K1265 D5 (2,1)@1,3 (K1264 published)'),
    ((1, 1), 1, 3, 0, 0, 'K1265 D5 (1,1)@1,3 boundary+1 collapse control'),
]

def check_E1():
    bad = comp = 0
    details = []
    for (X, z, R, ep, es, src) in ANCHORS:
        xs = tuple(X)
        hc = H_canonical(R, xs, z); ho = H_ordered(R, xs, z)
        s = single_token(sum(xs), z, R)
        comp += 5
        if hc != ho: bad += 1
        if ep is None:
            if not (hc == s and ho == s): bad += 1
        else:
            if hc != ep or ho != ep: bad += 1
            if s != es: bad += 1
        # window edge equality at W(z,min)
        Rw = W_of(z, min(xs))
        cw = single_token(sum(xs), z, Rw)
        if H_canonical(Rw, xs, z) != cw or H_ordered(Rw, xs, z) != cw: bad += 1
        details.append({'X': list(xs), 'z': z, 'R': R, 'parent': hc,
                        'single': s, 'src': src})
    return {'label': 'E1 published witness anchors (17)', 'comparisons': comp,
            'bad': bad, 'details': details}

# ---------------------------------------------------------------
# E2: T1 theorem anchors (paper mex chain; engine check)
# ---------------------------------------------------------------
def check_E2():
    bad = comp = 0
    rec = []
    # {1}^t @ (z=0, R=3): t=3..12 parent 0 vs single 1; t=2 collapse 0=0
    for t in list(range(3, 13)) + [2]:
        xs = tuple([1] * t)
        hc = H_canonical(3, xs, 0); ho = H_ordered(3, xs, 0)
        s = single_token(t, 0, 3)
        comp += 3
        if hc != ho: bad += 1
        if hc != 0 or ho != 0: bad += 1
        exp_s = 1 if t >= 3 else 0
        if s != exp_s: bad += 1
        rec.append({'t': t, 'parent': hc, 'single': s,
                    'separates': (hc != s)})
    # (2,1) @ (z=0, R=3): parent 2 vs single 1; window edge W=2 equality
    hc = H_canonical(3, (2, 1), 0); ho = H_ordered(3, (2, 1), 0)
    s = single_token(3, 0, 3)
    comp += 5
    if hc != ho or hc != 2: bad += 1
    if s != 1: bad += 1
    cw = single_token(3, 0, 2)
    if H_canonical(2, (2, 1), 0) != cw or H_ordered(2, (2, 1), 0) != cw: bad += 1
    rec.append({'X': [2, 1], 'z': 0, 'R': 3, 'parent': hc, 'single': s,
                'src': 'cell (0,1) two-token witness (paper)'})
    return {'label': 'E2 T1 theorem anchors', 'comparisons': comp,
            'bad': bad, 'details': rec}

# ---------------------------------------------------------------
# E3: two-token census (z<=24, m<=10, d<=60) + E3b (z=25,26 for m<=8, d<=24)
# + C4 recount vs published
# ---------------------------------------------------------------
def census_point(z, m, d, cell):
    x = m + d
    Rw = W_of(z, m)
    Rs = Rw + 1
    X = (x, m)
    S = x + m
    cw = single_token(S, z, Rw)
    hc_w = H_canonical(Rw, X, z); ho_w = H_ordered(Rw, X, z)
    bad = 0
    if hc_w != cw: bad += 1
    if ho_w != cw: bad += 1
    hc = H_canonical(Rs, X, z); ho = H_ordered(Rs, X, z)
    if hc != ho: bad += 1
    sc = single_token(S, z, Rs)
    sep = (hc != sc)
    if sep:
        cell['n_sep'] += 1
        if cell['min_d'] is None or d < cell['min_d']:
            cell['min_d'] = d
            cell['witness'] = {'X': [x, m], 'parent': hc, 'single': sc}
        if len(cell['sep_d']) < 25:
            cell['sep_d'].append(d)
    return bad

C4_PUBLISHED = {1: 180, 2: 37, 3: 32, 4: 31, 5: 26, 6: 25, 7: 20, 8: 19}

def check_E3():
    cells = []
    bad = pts = comp = 0
    for z in range(0, 25):
        for m in range(1, 11):
            cell = {'z': z, 'm': m, 'n_sep': 0, 'min_d': None,
                    'witness': None, 'sep_d': [], 'ext_found': False,
                    'arity_witness': None}
            for d in range(0, 61):
                bad += census_point(z, m, d, cell)
                pts += 1; comp += 4
            clear_engines()
            cells.append(cell)
    # E3b: z=25,26 slice for m<=8, d<=24 (completes the K1264 C4 domain)
    cells_b = []
    for z in (25, 26):
        for m in range(1, 9):
            cell = {'z': z, 'm': m, 'n_sep': 0, 'min_d': None,
                    'witness': None, 'sep_d': [], 'ext_found': False,
                    'arity_witness': None, 'source': 'E3b'}
            for d in range(0, 25):
                bad += census_point(z, m, d, cell)
                pts += 1; comp += 4
            cells_b.append(cell)
    # C4 recount (published semantics: Rb = z+y+1) over full published domain
    recount = {}
    for y in range(1, 9):
        c = 0
        for d in range(0, 25):
            x = y + d
            for z in range(0, 27):
                Rb = z + y + 1
                if H_canonical(Rb, (x, y), z) != single_token(x + y, z, Rb):
                    c += 1
        recount[y] = c
        clear_engines()
    c4_bad = 0
    for y, c in recount.items():
        if c != C4_PUBLISHED[y]: c4_bad += 1
    bad += c4_bad
    clear_engines()
    return {'label': 'E3 two-token census (+E3b, +C4 recount)',
            'points': pts, 'comparisons': comp, 'bad': bad,
            'c4_recount': recount, 'c4_published': C4_PUBLISHED,
            'c4_recount_bad': c4_bad, 'cells': cells, 'cells_e3b': cells_b}

# ---------------------------------------------------------------
# E4: negative-cell d-extension (61..200) + arity>=3 battery
# ---------------------------------------------------------------
def arity_battery(m):
    b = [(m, m, m), (m, m, m, m), (m, m, m, m, m), (m, m, m + 1),
         (m, m, m + 2), (m, m, 2 * m), (m, m, m, m + 1)]
    if m == 1:
        for t in range(9, 13):
            b.append(tuple([1] * t))
    return b

def check_E4(e3):
    bad = pts = comp = 0
    ext_cells = []
    ar_cells = []
    for cell in e3:
        if cell['n_sep'] > 0:
            continue
        z, m = cell['z'], cell['m']
        clear_engines()
        found = False
        for dd in range(61, 201):
            # census points only (window equality included per point)
            bad_pt = census_point(z, m, dd, cell)
            bad += bad_pt
            pts += 1; comp += 4
            if dd % 50 == 0:
                clear_engines()
            if cell['min_d'] is not None and not found:
                found = True
                cell['ext_found'] = True
        if not found:
            # arity battery
            for X in arity_battery(m):
                Rwp = W_of(z, m)
                cw = single_token(sum(X), z, Rwp)
                hcw = H_canonical(Rwp, X, z); how = H_ordered(Rwp, X, z)
                bad += (0 if hcw == cw else 1) + (0 if how == cw else 1)
                Rs = Rwp + 1
                hc = H_canonical(Rs, X, z); ho = H_ordered(Rs, X, z)
                if hc != ho: bad += 1
                sc = single_token(sum(X), z, Rs)
                comp += 4; pts += 1
                clear_engines()
                if hc != sc and cell['arity_witness'] is None:
                    cell['arity_witness'] = {'X': list(X), 'parent': hc,
                                             'single': sc}
        if cell['ext_found']:
            ext_cells.append((z, m, cell['min_d']))
        elif cell['arity_witness'] is not None:
            ar_cells.append((z, m, cell['arity_witness']['X']))
    H_ordered.cache_clear(); H_canonical.cache_clear()
    return {'label': 'E4 negative-cell extension + arity battery',
            'points': pts, 'comparisons': comp, 'bad': bad,
            'n_negative_cells': sum(1 for c in e3 if c['n_sep'] == 0),
            'ext_resolved': sorted(ext_cells),
            'arity_resolved': sorted(ar_cells),
            'n_open_cells': sum(1 for c in e3 if c['n_sep'] == 0
                                and c['min_d'] is None
                                and c['arity_witness'] is None)}

# ---------------------------------------------------------------
# E5: {1}^t row census t=3..8, z=0..24 (min=1 arity map)
# ---------------------------------------------------------------
def check_E5():
    bad = pts = comp = 0
    rows = []
    for t in range(3, 9):
        for z in range(0, 25):
            xs = tuple([1] * t)
            Rw = W_of(z, 1)
            cw = single_token(t, z, Rw)
            hcw = H_canonical(Rw, xs, z); how = H_ordered(Rw, xs, z)
            if hcw != cw: bad += 1
            if how != cw: bad += 1
            Rs = Rw + 1
            hc = H_canonical(Rs, xs, z); ho = H_ordered(Rs, xs, z)
            if hc != ho: bad += 1
            sc = single_token(t, z, Rs)
            pts += 1; comp += 4
            if hc != sc:
                rows.append({'t': t, 'z': z, 'parent': hc, 'single': sc})
    clear_engines()
    return {'label': 'E5 {1}^t row census t=3..8 z=0..24',
            'points': pts, 'comparisons': comp, 'bad': bad,
            'separating_rows': rows,
            'n_separating_rows': len(rows)}

# ---------------------------------------------------------------
# E6: diagonal lines L1/L2 (parent-2 pre-registered prediction)
# ---------------------------------------------------------------
def check_E6():
    bad = comp = 0
    L = []
    L1_ok = L2_ok = L1_par_ok = L2_par_ok = True
    for m in range(11, 21):  # L1: X=(m+1,m), z=2m-1, R*=3m
        z = 2 * m - 1; R = 3 * m; X = (m + 1, m)
        hc = H_canonical(R, X, z); ho = H_ordered(R, X, z)
        s = single_token(2 * m + 1, z, R)
        Rw = z + m
        cw = single_token(2 * m + 1, z, Rw)
        if H_canonical(Rw, X, z) != cw or H_ordered(Rw, X, z) != cw: bad += 1
        comp += 5
        par_ok = (hc == 2 and ho == 2)
        if not par_ok: L1_par_ok = False
        if s != (5 * m - 1) % 2: L1_ok = False
        L.append({'line': 'L1', 'm': m, 'parent': hc, 'single': s,
                  'parent2_holds': par_ok,
                  'single_formula_holds': s == (5 * m - 1) % 2})
        clear_engines()
    for m in range(11, 23):  # L2: X=(m,m), z=2m-2, R*=3m-1
        z = 2 * m - 2; R = 3 * m - 1; X = (m, m)
        hc = H_canonical(R, X, z); ho = H_ordered(R, X, z)
        s = single_token(2 * m, z, R)
        Rw = z + m
        cw = single_token(2 * m, z, Rw)
        if H_canonical(Rw, X, z) != cw or H_ordered(Rw, X, z) != cw: bad += 1
        comp += 5
        par_ok = (hc == 2 and ho == 2)
        if not par_ok: L2_par_ok = False
        if s != (5 * m - 3) % 2: L2_ok = False
        L.append({'line': 'L2', 'm': m, 'parent': hc, 'single': s,
                  'parent2_holds': par_ok,
                  'single_formula_holds': s == (5 * m - 3) % 2})
        clear_engines()
    H_ordered.cache_clear(); H_canonical.cache_clear()
    return {'label': 'E6 diagonal lines L1 (m=11..20) L2 (m=11..22)',
            'comparisons': comp, 'bad': bad,
            'L1_parent2_holds': L1_par_ok, 'L2_parent2_holds': L2_par_ok,
            'L1_single_formula_holds': L1_ok,
            'L2_single_formula_holds': L2_ok, 'points': L}

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
    # T8: B-move without the z-increment (token removal keeps z)
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
    total = 0
    def rec(name, bad):
        nonlocal total
        results.append({'mutation': name, 'bad': bad})
        print(('CAUGHT' if bad > 0 else 'TAMPER-MISSED') + ': ' + name +
              ' bad=' + str(bad))
        total += bad
        return bad
    # T1: window+1 collapse claim (two-token y<=6 subdomain)
    bad = 0
    for y in range(1, 7):
        for d in range(0, 12):
            for z in range(0, 16):
                if H_canonical(z + y + 1, (y + d, y), z) != single_token(2 * y + d, z, z + y + 1):
                    bad += 1
    rec('T1 window+1 claimed collapse (y<=6)', bad)
    # T2: T1-anchor parent flip ({1}^3@(0,3) expected 1)
    hc = H_canonical(3, (1, 1, 1), 0)
    rec('T2 T1-anchor parent flip', 0 if hc == 1 else 1)
    # T3: C-move removed from ordered engine (anchor recheck)
    bad = 0
    for z in range(1, 15):
        for R in range(1, z + 8):
            if H_ordered_noC(R, (3, 2), z) != H_canonical(R, (3, 2), z): bad += 1
    rec('T3 ordered engine without C-move', bad)
    # T4: corrupted q_odd closed form
    bad = 0
    for x in range(2, 60):
        for z in range(1, 40):
            for R in range(0, min(x + z + 1, 50) + 1):
                if single_token_mut(x, z, R) != vC(x, z, R): bad += 1
    rec('T4 corrupted q_odd closed form', bad)
    # T5: boundary+1 always-equal claim (y=1 row)
    bad = 0
    for d in range(0, 25):
        for z in range(0, 27):
            if H_canonical(z + 2, (1 + d, 1), z) != single_token(2 + d, z, z + 2): bad += 1
    rec('T5 boundary+1 equality claim (y=1 row)', bad)
    # T6: published E1 anchor value flip ((4,4)@z=6 expected parent 0)
    rec('T6 E1 anchor parent flip ((4,4)@6)', 0 if H_canonical(11, (4, 4), 6) == 0 else 1)
    # T7: min/max window swap claim (published set, K1264 T6 analog)
    bad = 0
    for (X, z) in [((2, 1), 1), ((2, 1), 2), ((3, 1), 1), ((5, 2), 3), ((1, 1, 3), 1)]:
        mx = max(X)
        for R in range(0, z + mx + 1):
            if H_canonical(R, X, z) != single_token(sum(X), z, R): bad += 1
    rec('T7 max-token window claim', bad)
    # T8: B-move without z-increment ({1}^t z-row recheck)
    bad = 0
    for t in range(2, 7):
        for z in range(0, 3):
            for R in range(1, 6):
                if H_ordered_noBinc(R, tuple([1] * t), z) != H_canonical(R, tuple([1] * t), z):
                    bad += 1
    rec('T8 ordered engine without B z-increment', bad)
    missed = [r['mutation'] for r in results if r['bad'] == 0]
    print('TAMPER BATTERY:', 'ALL CAUGHT' if not missed else 'MISSED: ' + str(missed))
    if missed: sys.exit(1)
    sys.exit(0)

# ---------------------------------------------------------------
def run_audit():
    res = {}
    res['E0'] = check_E0()
    clear_engines()
    res['E1'] = check_E1()
    clear_engines()
    res['E2'] = check_E2()
    clear_engines()
    e3 = check_E3()
    res['E3_meta'] = {k: v for k, v in e3.items() if k not in ('cells', 'cells_e3b')}
    # snapshot per-cell census state (post-E3) BEFORE E4 mutates cells
    cells = e3['cells']
    sharp_two_token = [(c['z'], c['m'], c['min_d']) for c in cells if c['n_sep'] > 0]
    negative = [(c['z'], c['m']) for c in cells if c['n_sep'] == 0]
    res['E4'] = check_E4(cells)
    res['E5'] = check_E5()
    res['E6'] = check_E6()
    # census summary tables for the report
    res['census_cells'] = cells
    res['census_cells_e3b'] = e3['cells_e3b']
    res['summary'] = {
        'n_cells': len(cells) + len(e3['cells_e3b']),
        'n_sharp_two_token': len(sharp_two_token),
        'n_negative_after_E3': len(negative),
        'negative_cells': negative,
        'sharp_two_token': sharp_two_token,
        'meta': {
            'verifier_sha256': SELF_SHA,
            'theorem': 'T1: {1}^t separates at (0,3) for all t>=3 (paper mex chain; engine-checked t<=12)',
            'census': 'unified window W=max(z+m,2) cell sharpness; separations at W+1 are census records',
        },
    }
    total_bad = res['E0']['bad'] + res['E1']['bad'] + res['E2']['bad'] \
        + e3['bad'] + res['E4']['bad'] + res['E5']['bad'] + res['E6']['bad']
    res['summary']['total_bad'] = total_bad
    res['points_totals'] = {
        'E0': res['E0']['points'], 'E1': len(ANCHORS), 'E2': len(res['E2']['details']),
        'E3': e3['points'], 'E4': res['E4']['points'], 'E5': res['E5']['points'],
        'E6': len(res['E6']['points'])}
    return res, total_bad

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else 'audit'
    if mode == 'tamper':
        tamper(); return
    res, bad = run_audit()
    with open('output/audit.json', 'w') as f:
        f.write(json.dumps(res, indent=1, sort_keys=True, ensure_ascii=True) + '\n')
    pts = sum(res['points_totals'].values())
    comp_tot = (res['E0']['comparisons'] + res['E1']['comparisons'] +
                res['E2']['comparisons'] + res['E3_meta']['comparisons'] +
                res['E4']['comparisons'] + res['E5']['comparisons'] +
                res['E6']['comparisons'])
    print('TOTAL points:', pts, 'comparisons:', comp_tot, 'bad:', bad)
    print('sharp cells (two-token):', res['summary']['n_sharp_two_token'],
          'negative:', res['summary']['n_negative_after_E3'],
          'open after E4:', res['E4']['n_open_cells'])
    if bad:
        print('AUDIT FAIL: bad =', bad); sys.exit(1)
    print('AUDIT PASS'); sys.exit(0)

if __name__ == '__main__':
    main()
