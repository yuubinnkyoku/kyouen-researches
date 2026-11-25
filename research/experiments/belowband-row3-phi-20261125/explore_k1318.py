#!/usr/bin/env python3
"""explore_k1318: frozen measurement battery for the below-band row-3
(m,W)-Phi ladder-geometry packet (K1315 next-task 2; provisional slot
K1318; observation packet, extends K1315 OBS-BBL3).

The exploration session of the handoff log (research/log/
2026-11-25-belowband-row3-phi-tables-exploration.md) left the following
plan for this machine, section "次回実行の凍結・出版計画":
 (i)   tier battery (m=6/m=7 full words, j-shift included);
 (ii)  2-recursion pairs, fresh recompute of every measured pair;
 (iii) base-family tables m=8..12 (every D4/D5 row = 51 rows, embedded
       filler table, minimal zmax per suppression arithmetic);
 (iv)  D6 pre-registration rows, fresh re-run (12);
 (v)   suppression-arithmetic rows (D7, 6 rows + 1 new declared row);
 (vi)  synthesis agreement: machine cross-check of A = eta(n)+2j-2Phi(m,W)
       on every measured row, with declared-exception accounting.

Plus the handoff's unfinished-measurement list 1-6 (WH), plus the
deep-tier probes (WI): kappa <= -1 pure [3^b] rows (linear-tier reading
Phi = m-6), the []-family deep floor, the small-m [4] family rows, and
the direct []@11 measurement (Phi = 15 predicted, previously OOM).

Coordinates (K1311/K1315): descending heap multiset X, n = |X|,
S = sum(X), E := 2*max(X)-S, j := #1-heaps, m := n-j (# heaps >= 2),
row k = z+n-5 (third below-band row), R = S+z+n-5.
A family anchor line: the in-window single-2 position z2, A := E+z2.
Synthesis (D1, family-level observation):
   A(n,j,W) = eta(n) + 2j - 2*Phi(m,W),  eta(n) = -5(n-4), m = n-j.
W := the {2,3,4}-part of X (word, by counts a:=#2, b:=#3, c:=#4);
fillers are heaps = F (literal, 5 <= F <= 17 per row table), inert per
D1/WB; cf := m-a-b-c.
Phi law (conjecture-grade prediction function, validity zones declared):
   strip 2s: Phi(a,b,c,m) := Phi(0,b,c,m-a) when a >= 1;
   empty family: m'>=8: T_{m'-6}; m' in {6,7}: m'-6; m'<=5: open zone;
   [4^c] family c>=1: base = (m'-6 if m'<=7 else T_{m'-7}+2),
       wall: -sum_{i<c-1} (m'-9-i)_+;
   [3^b] family b>=1 (pure or mixed with c>=1):
       base = (T_{kappa}+b for b<=m'-5, kappa=m'-6-b>=-1, T_{-1}:=-1;
               m'-6 for b>=m'-4), wall: q=c, t=8+b,
       wall: -sum_{i<q} (m'-t-i)_+.
Tier rules (D2, handoff claims, tested as stated): m=6: Phi=0 all words;
m=7: Phi=0 if a>=1 else 1.  The sweep also measures words whose stripped
target lies in the open zone (m'<6); those Phi values are recorded as
deep-zone observations (WZ empty-floor table), not as law cells.

Waves:
  WA  engine sanity: single_token cross-check slice;
  WB  filler/j invariance pairs (D1 pairs + deep-support pairs);
  WC  tier battery: m=6/m=7 full word sweeps x {j=0,j=1}, F=6,
      + n=10 j=4 witnesses (7 words, F=8);
  WD  2-recursion pairs fresh recompute (17 pairs, host+target);
  WE  base-family tables: every D4/D5 row (51 rows), embedded F table;
  WF  D6 pre-registration m12 battery fresh re-run (12 rows);
  WG  wall-suppression arithmetic rows (6 D7 rows + [4444]@12 F=7 new);
  WH  handoff pending rows p1..p6b (explicit constructions);
  WI  deep-tier probes: pure [3^b] kappa<=-1 linear-tier rows,
      []-family deep floor probes, [4] family small-m rows, []@11;
  WJ  synthesis agreement across every measured row;
  WZ  refined deep summary (pure [3^b] linear table vs []-family
      zero-floor table).

Construction rule (fresh freeze, deterministic): each row's filler F is
the smallest value in 5..17 whose predicted anchor z2 = A_pred - E lies
in [0..3] (fallback: z2 in [0..10]); WH rows and WG decls keep the
handoff's explicit constructions.  Exceptions are declared here:
  - WD pair ([2,2,3],11): target m=9 (see revision note (b));
  - WB []@11 pair: j-invariance @F=8 (the F=9 second leg OOMs in the
    ~1GB sandbox; honest incident, not retried);
  - WI [3^6]@9 F=13 / [3^7]@10 F=17: the only visible constructions
    at z2=0 (fillers >= 5 inert per WB/D1 support pairs in WB).

Revision note (vs the first, superseded run of this same battery,
whose outputs were discarded with a workspace loss before any
publication; the superseded run never left the sandbox):
 (a) tier/pair/WG visibility tests used the strict inequality A > E;
     the correct spec is A >= E (A == E is the visible z2 = 0 boundary
     line; in the superseded run every flagged row had vals[0] == 2 at
     z2 = 0), so its 22 supp_inconsistent and 23 jshift_bad entries
     were boundary false positives;
 (b) the handoff log's D3 pair listing ([2,2,3],11)->([3],10) contains
     a typo caught faithfully by the superseded run (measured
     Phi([3],10) = 7 vs host Phi = 4): the 2-recursion law and the
     log's own "( =4)" annotation both give the target m = 9;
     the frozen spec here uses m = 9;
 (c) WZ deep summary splits the pure [3^b] linear-tier probes from
     the []-family deep floor probes (measured Phi([]) = 0 on stripped
     m' in {3,4,5} inside the m=6 tier sweep: flat zero floor, not
     linear, not T_{-2} = 1);
 (d) the superseded run was reconstructed from the published handoff
     log + kit templates after the workspace loss; every row of this
     freeze predry-passed 2 identical runs before publication, and
     the official publish chain re-runs this exact frozen file;
 (e) predry discovery folded into the freeze: the family formulas
     ([3^b] linear tier, [4^c] base) continue to NEGATIVE values for
     stripped targets m' <= 5, but every measured tier row there sits
     at Phi = 0 (44 rule rows + 12 jshift boundary rows of the first
     post-reconstruction predry); the formula zone is closed at
     m' >= 6 and m' <= 5 is open, with the flat deep floor recorded
     as the WZ floor-probe observation (generalizes the handoff's
     []-family floor note to all word families);
 (f) predry protocol notes: rows whose swept window holds TWO 2s are
     recorded as multi2 observations (tier grade is single-2 anchors
     only); witness [333] (n=10,j=4,F=8) has z2_pred = -1, so its
     no-2 sweep is suppression-consistent, not an anchor hit.

Every row is a fresh engine measurement (byte-clone engine_block chain,
pin bd5f22e4 startup gate).  All values in the frozen .out are
observation grade over the swept z-windows; no universal theorem is
claimed here.  11x11 stays UNKNOWN; no verdicts consumed.

Determinism: fixed iteration orders, json sort_keys; lru_cache does not
affect values; PYTHONHASHSEED-independent.
"""
import hashlib
import json
import sys
from functools import lru_cache
from itertools import combinations_with_replacement  # noqa: F401 (kept: k1315 lineage)

sys.setrecursionlimit(100000)

ENGINE_BLOCK = '''def mex(values):
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
'''

PIN = 'bd5f22e415a78368c9b798296bc84948d5637decbf3c21a92404d45fb12e3a92'
sha = hashlib.sha256(ENGINE_BLOCK.encode('utf-8')).hexdigest()
assert sha == PIN, sha
exec(ENGINE_BLOCK)

REPORT = {'engine_sha': sha}

# ------------------------------------------------------------------
# Law helpers (embedded, conjecture grade; validity zones declared).
# ------------------------------------------------------------------


def T(x):
    return x * (x + 1) // 2


def etaf(n):
    return -5 * (n - 4)


def phi_pred(a, b, c, m):
    """The (m,W)-Phi prediction; None in the open/unknown zone.

    Open-zone boundary (fresh-freeze decision, superseding the run's
    discovery): after stripping the 2s (m' = m - a), every family
    formula would continue to negative values for m' <= 5; the tier
    sweeps instead measure Phi = 0 there (WZ floor probes).  The
    formula zone therefore ends at m' = 6; m' <= 5 is open and the
    tier rules govern the unstripped m in {6,7} rows.
    """
    if a >= 1:
        return phi_pred(0, b, c, m - a)
    if m <= 5:
        return None
    if b == 0 and c == 0:
        if m >= 8:
            return T(m - 6)
        if m in (6, 7):
            return m - 6
        return None
    if b == 0:
        base = (m - 6) if m <= 7 else (T(m - 7) + 2)
        return base - sum(max(0, m - 9 - i) for i in range(c - 1))
    base = (m - 6) if b >= m - 4 else \
        ((T(m - 6 - b) if m - 6 - b >= 0 else -1) + b)
    q = c
    t = 8 + b
    return base - sum(max(0, m - t - i) for i in range(q))


def tier_expected(a, b, c, m):
    """Tier rules as stated in the handoff D2."""
    if m == 6:
        return 0
    if m == 7:
        return 0 if a >= 1 else 1
    return None


def build_X(a, b, c, m, j, F):
    cf = m - a - b - c
    return tuple([F] * cf + [4] * c + [3] * b + [2] * a + [1] * j)


def E_of(a, b, c, m, j, F):
    X = build_X(a, b, c, m, j, F)
    return 2 * X[0] - sum(X)


def pick_F(a, b, c, m, j=0):
    """Fresh-freeze construction rule: smallest F in 5..17, z2 in [0..3];
    fallback smallest F with z2 in [0..10]; None if never visible."""
    pp = phi_pred(a, b, c, m)
    if pp is None:
        return None
    A = etaf(m + j) + 2 * j - 2 * pp
    fb = None
    for F in range(5, 18):
        E = E_of(a, b, c, m, j, F)
        z2 = A - E
        if 0 <= z2 <= 3:
            return F
        if fb is None and 0 <= z2 <= 10:
            fb = F
    return fb


def measure(X, zwin):
    S = sum(X)
    n = len(X)
    vals = []
    for z in range(zwin + 1):
        R = S + z + n - 5
        vals.append(H_canonical(R, X, z) if R >= 0 else None)
    H_canonical.cache_clear()
    twos = [z for z, v in enumerate(vals) if v is not None and v == 2]
    return vals, twos


def row_of(a, b, c, m, j, F, zwin, tag):
    """Measure a row and extract the single-2 anchor if present."""
    X = build_X(a, b, c, m, j, F)
    n = len(X)
    E = 2 * X[0] - sum(X)
    vals, twos = measure(X, zwin)
    etan = etaf(n)
    A = (E + twos[0]) if len(twos) == 1 else None
    Phi = None
    parity_odd = None
    if A is not None:
        num = etan + 2 * j - A
        if num % 2 == 0:
            Phi = num // 2
        else:
            parity_odd = True
    pp = phi_pred(a, b, c, m)
    A_pred = etan + 2 * j - 2 * pp if pp is not None else None
    conform_bad = bool(A is not None and A_pred is not None and A != A_pred)
    status = ('measured' if A is not None
              else ('multi2' if twos else 'no2'))
    return {'tag': tag, 'X': list(X), 'n': n, 'j': j, 'm': m, 'F': F,
            'W': [a, b, c], 'E': E, 'zwin': zwin, 'vals': vals,
            'twos': twos, 'A': A, 'Phi': Phi, 'parity_odd': parity_odd,
            'A_pred': A_pred, 'Phi_pred': pp, 'conform_bad': conform_bad,
            'status': status}


# ------------------------------------------------------------------
# WA: engine sanity (single-token slice, canonical engine == K0832 form).
# ------------------------------------------------------------------
wa = {'cells': 0, 'mismatch': []}
for x in range(1, 13):
    for z in range(0, 13):
        R = x + z - 4
        if R < 0:
            continue
        wa['cells'] += 1
        if H_canonical(R, (x,), z) != single_token(x, z, R):
            wa['mismatch'].append([x, z, R])
H_canonical.cache_clear()
wa['pass'] = (wa['cells'] == 150 and not wa['mismatch'])
REPORT['WA_sanity'] = wa

all_rows = []

# ------------------------------------------------------------------
# WB: filler / j invariance pairs.  Each pair measures the SAME (m,W)
# Phi at two constructions; A is construction-dependent, Phi is not.
# Pair 7's second leg is a j-shift (the F=9 leg OOMs in the ~1GB
# sandbox; honest incident, superseded: the j-shift is the equivalent
# D1 claim and was freshly feasible).
# ------------------------------------------------------------------
WB_PAIRS = [
    (('w001m10F6', (0, 0, 1), 10, 0, 6), ('w001m10F7', (0, 0, 1), 10, 0, 7)),
    (('w002m10F7', (0, 0, 2), 10, 0, 7), ('w002m10F8', (0, 0, 2), 10, 0, 8)),
    (('w010m10F6', (0, 1, 0), 10, 0, 6), ('w010m10F7', (0, 1, 0), 10, 0, 7)),
    (('w012m10F7', (0, 1, 2), 10, 0, 7), ('w012m10F8', (0, 1, 2), 10, 0, 8)),
    (('w040m8F6', (0, 4, 0), 8, 0, 6), ('w040m8F7', (0, 4, 0), 8, 0, 7)),
    (('w060m10F10', (0, 6, 0), 10, 0, 10), ('w060m10F12', (0, 6, 0), 10, 0, 12)),
    (('w000m11j0F8', (0, 0, 0), 11, 0, 8), ('w000m11j1F8', (0, 0, 0), 11, 1, 8)),
]


def run_pair_side(spec):
    tag, w, m, j, F = spec
    pp = phi_pred(*w, m)
    A = etaf(m + j) + 2 * j - 2 * pp
    E = E_of(*w, m, j, F)
    zwin = max(2, A - E + 2)
    r = row_of(*w, m, j, F, zwin, tag)
    all_rows.append(r)
    return r


wb_rows = []
wb_bad = []
for s1, s2 in WB_PAIRS:
    r1 = run_pair_side(s1)
    r2 = run_pair_side(s2)
    wb_rows.append((r1, r2))
    if r1['Phi'] is None or r2['Phi'] is None or r1['Phi'] != r2['Phi']:
        wb_bad.append({'pair': [s1[0], s2[0]],
                       'Phi1': r1['Phi'], 'Phi2': r2['Phi']})
    else:
        pp = phi_pred(*s1[1], s1[2])
        if pp is not None and r1['Phi'] != pp:
            wb_bad.append({'pair': [s1[0], s2[0]], 'Phi': r1['Phi'],
                           'law': pp, 'reason': 'law-mismatch'})
REPORT['WB_invariance'] = {
    'rows': [r for pair in wb_rows for r in pair],
    'n_pairs': len(WB_PAIRS), 'bad': wb_bad}

# ------------------------------------------------------------------
# WC: tier battery.  m=6 / m=7 full word sweeps with j in {0,1}, F=6;
# boundary spec: A_rule >= E is the visible z2=0 line (only A_rule < E
# is suppressed).  j-shift note: z2(j+1) = z2(j) - 2, so a j0 row with
# z2 in {0,1} legitimately suppresses at j=1.
# ------------------------------------------------------------------
wc = {'m6': [], 'm7': [], 'rule_bad': [], 'supp_inconsistent': [],
      'jshift_bad': [], 'multi2_obs': []}


def words_upto(s):
    out = []
    for a in range(s + 1):
        for b in range(s + 1 - a):
            for c in range(s + 1 - a - b):
                out.append((a, b, c))
    return out


def tier_row(w, m, j, tag):
    a, b, c = w
    exp = tier_expected(a, b, c, m)
    A_rule = etaf(m + j) + 2 * j - 2 * exp
    E = E_of(a, b, c, m, j, 6)
    # boundary spec: A_rule == E is the z2 = 0 visible line
    if A_rule >= E:
        zwin = max(2, A_rule - E + 2)
        r = row_of(a, b, c, m, j, 6, zwin, tag)
        if r['Phi'] is not None:
            if r['Phi'] != exp:
                wc['rule_bad'].append({'tag': tag, 'Phi': r['Phi'],
                                       'exp': exp, 'row': r})
            elif r['A_pred'] is not None and r['A'] != r['A_pred']:
                wc['rule_bad'].append({'tag': tag, 'reason': 'law-disagree',
                                       'row': r})
        else:
            wc['rule_bad'].append({'tag': tag, 'reason': 'expected-visible'
                                   '-but-no-single-2', 'row': r})
        all_rows.append(r)
        return r
    # suppressed under the rule (A_rule < E): window must be 2-free
    X = build_X(a, b, c, m, j, 6)
    vals, twos = measure(X, 2)
    rec = {'tag': tag, 'X': list(X), 'n': len(X), 'j': j, 'm': m, 'F': 6,
           'W': [a, b, c], 'E': E, 'zwin': 2, 'vals': vals, 'twos': twos,
           'A': None, 'Phi': None, 'parity_odd': None,
           'A_pred': A_rule, 'Phi_pred': phi_pred(a, b, c, m),
           'conform_bad': False,
           'status': ('rule_suppressed_consistent' if not twos
                      else 'RULE_SUPPRESSION_INCONSISTENT')}
    if twos:
        wc['supp_inconsistent'].append(rec)
    all_rows.append(rec)
    return rec


for m, mmin in ((6, 'm6'), (7, 'm7')):
    for w in words_upto(m - 1):
        t0 = f't_m{m}_w{w[0]}{w[1]}{w[2]}_j0'
        r0 = tier_row(w, m, 0, t0)
        wc[mmin].append(r0)
        t1 = f't_m{m}_w{w[0]}{w[1]}{w[2]}_j1'
        r1 = tier_row(w, m, 1, t1)
        wc[mmin].append(r1)
        # real-anchor z2: measured A when present (tier grade), else the
        # rule-line arithmetic; boundary rows (z2 <= 1) legitimately
        # suppress at j=1 because z2(j+1) = z2(j) - 2.
        if r0['A'] is not None:
            z2_j0 = r0['A'] - r0['E']
        elif r0['A_pred'] is not None:
            z2_j0 = r0['A_pred'] - r0['E']
        else:
            z2_j0 = None
        multi2 = (len(r0['twos']) > 1) or (len(r1['twos']) > 1)
        if multi2:
            wc['multi2_obs'].append({'tag': t0, 'j0_twos': r0['twos'],
                                     'j1_twos': r1['twos'],
                                     'j0_zwin': r0['zwin'],
                                     'j1_zwin': r1['zwin'],
                                     'j0_vals': r0['vals'],
                                     'j1_vals': r1['vals']})
        elif (r0['Phi'] is not None) != (r1['Phi'] is not None):
            # legitimate only when the j0 anchor sits at the boundary
            if not (r0['Phi'] is not None and z2_j0 is not None
                    and z2_j0 <= 1):
                wc['jshift_bad'].append({'tag': t0,
                                         'reason': 'supp-mismatch',
                                         'j0': r0['Phi'],
                                         'j1': r1['Phi']})
        elif r0['Phi'] is not None and r0['Phi'] != r1['Phi']:
            wc['jshift_bad'].append({'tag': t0, 'j0_phi': r0['Phi'],
                                     'j1_phi': r1['Phi']})

# handoff D2 witnesses: n=10, j=4 (m=6), F=8, A = -22, z2 = 14
wc['witness_n10j4'] = []
for (a, b, c) in [(0, 0, 0), (0, 1, 0), (0, 0, 1), (0, 2, 0), (0, 0, 2),
                  (0, 0, 3), (0, 3, 0)]:
    X = build_X(a, b, c, 6, 4, 8)
    S = sum(X)
    E = 2 * X[0] - S
    vals, twos = measure(X, 16)
    A = E + twos[0] if len(twos) == 1 else None
    Phi = (etaf(10) + 8 - A) // 2 if A is not None else None
    # z2 arithmetic of the declared (-22) line in THIS construction:
    # [333] (w030) sits at z2 = A_pred - E = -1, i.e. its line is one
    # step below the window and the no-2 sweep is the consistent
    # outcome (recorded as such, not as an anchor hit).
    z2_pred = etaf(10) + 8 - E
    if A is not None:
        st = 'measured'
    elif z2_pred < 0 and not twos:
        st = 'suppressed_consistent'
    else:
        st = 'no2'
    rec = {'tag': f'wit_w{a}{b}{c}', 'X': list(X), 'E': E, 'vals': vals,
           'twos': twos, 'A': A, 'Phi': Phi,
           'A_pred': etaf(10) + 8, 'Phi_pred': 0,
           'z2_pred': z2_pred,
           'W': [a, b, c], 'm': 6, 'j': 4, 'F': 8, 'n': 10, 'zwin': 16,
           'parity_odd': None,
           'conform_bad': bool(A is not None and A != etaf(10) + 8),
           'status': st}
    wc['witness_n10j4'].append(rec)
    all_rows.append(rec)
REPORT['WC_tier'] = {'m6_n': len(wc['m6']), 'm7_n': len(wc['m7']),
                      'rule_bad': wc['rule_bad'],
                      'supp_inconsistent': wc['supp_inconsistent'],
                      'jshift_bad': wc['jshift_bad'],
                      'multi2_obs': wc['multi2_obs'],
                      'witness_n10j4': wc['witness_n10j4'],
                      'm6': wc['m6'], 'm7': wc['m7']}

# ------------------------------------------------------------------
# WD: 2-recursion pairs (fresh recompute, host + target).
# Targets use target m' = host m - a (strip rule).  Pair 13 is the
# handoff's D3 listing with the corrected target m (revision note b).
# ------------------------------------------------------------------
WD_PAIRS = [
    ([2, 3], 9, [3], 8), ([2, 3], 10, [3], 9), ([2, 3], 11, [3], 10),
    ([2, 4], 9, [4], 8), ([2, 4], 10, [4], 9),
    ([2, 4, 4], 9, [4, 4], 8), ([2, 4, 4], 10, [4, 4], 9),
    ([2, 4, 4], 12, [4, 4], 11),
    ([2, 3, 3], 10, [3, 3], 9), ([2, 3, 3], 11, [3, 3], 10),
    ([2, 3, 3], 12, [3, 3], 11),
    ([2, 2, 3, 3], 10, [3, 3], 8),
    ([2, 2, 3], 11, [3], 9),   # D3 typo (target m=10) corrected to 9
    ([2], 11, [], 10), ([2, 2], 12, [], 10), ([2, 2, 2], 12, [], 9),
    ([2, 2, 2, 2, 2], 12, [], 7),
]


def pair_side(word, m, tag):
    a = sum(1 for v in word if v == 2)
    b = sum(1 for v in word if v == 3)
    c = sum(1 for v in word if v == 4)
    F = pick_F(a, b, c, m)
    assert F is not None, (word, m)
    pp = phi_pred(a, b, c, m)
    A = etaf(m) - 2 * pp
    E = E_of(a, b, c, m, 0, F)
    zwin = max(2, A - E + 2)   # boundary spec: A == E visible at z2=0
    r = row_of(a, b, c, m, 0, F, zwin, tag)
    all_rows.append(r)
    return r


wd_rows = {'pairs': [], 'recursion_bad': []}
for idx, (hw, hm, tw, tm) in enumerate(WD_PAIRS, 1):
    rh = pair_side(hw, hm, f'wd{idx:02d}_host')
    rt = pair_side(tw, tm, f'wd{idx:02d}_target')
    wd_rows['pairs'].append({'idx': idx, 'host': rh, 'target': rt})
    if not (tm == hm - sum(1 for v in hw if v == 2)):
        wd_rows['recursion_bad'].append({'idx': idx,
                                         'reason': 'spec-strip-mismatch'})
        continue
    if rh['Phi'] is None or rt['Phi'] is None:
        wd_rows['recursion_bad'].append({'idx': idx, 'host': rh['Phi'],
                                         'target': rt['Phi'],
                                         'reason': 'unmeasured-side'})
    elif rh['Phi'] != rt['Phi']:
        wd_rows['recursion_bad'].append({'idx': idx, 'host': rh['Phi'],
                                         'target': rt['Phi']})
REPORT['WD_recursion'] = wd_rows

# ------------------------------------------------------------------
# WE: base-family tables (every D4/D5 row, 51 rows) with the embedded
# frozen construction table (word, m, F).
# ------------------------------------------------------------------
WE_SPEC = [((0, 1, 0), 8, 5), ((0, 1, 0), 9, 5), ((0, 1, 0), 10, 6),
           ((0, 1, 0), 11, 7), ((0, 1, 0), 12, 8),
           ((0, 2, 0), 8, 5), ((0, 2, 0), 9, 5), ((0, 2, 0), 10, 6),
           ((0, 2, 0), 11, 7),
           ((0, 3, 0), 9, 6), ((0, 3, 0), 10, 6),
           ((0, 4, 0), 9, 7), ((0, 5, 0), 10, 8),
           ((0, 6, 0), 11, 9), ((0, 6, 0), 12, 9),
           ((0, 0, 1), 8, 5), ((0, 0, 1), 9, 6), ((0, 0, 1), 10, 6),
           ((0, 0, 1), 11, 7), ((0, 0, 1), 12, 8),
           ((0, 1, 1), 8, 5), ((0, 1, 1), 9, 6), ((0, 1, 1), 10, 6),
           ((0, 1, 1), 11, 7), ((0, 1, 1), 12, 8),
           ((0, 0, 2), 8, 5), ((0, 0, 2), 9, 6), ((0, 0, 2), 10, 6),
           ((0, 0, 2), 11, 7), ((0, 0, 2), 12, 8),
           ((0, 0, 3), 10, 7), ((0, 0, 3), 11, 7), ((0, 0, 3), 12, 8),
           ((0, 0, 4), 10, 7),
           ((0, 2, 1), 8, 5), ((0, 2, 1), 9, 6), ((0, 2, 1), 10, 6),
           ((0, 2, 1), 11, 7), ((0, 2, 1), 12, 8),
           ((0, 1, 2), 8, 5), ((0, 1, 2), 9, 6), ((0, 1, 2), 10, 7),
           ((0, 1, 2), 11, 7), ((0, 1, 2), 12, 8),
           ((0, 2, 2), 9, 6), ((0, 2, 2), 10, 7), ((0, 2, 2), 12, 8),
           ((0, 4, 1), 10, 8),
           ((0, 2, 0), 9, 5), ((0, 2, 0), 10, 6), ((0, 2, 0), 11, 7)]
we_rows = []
we_mismatch = []
for w, m, F in WE_SPEC:
    pp = phi_pred(*w, m)
    A = etaf(m) - 2 * pp
    E = E_of(*w, m, 0, F)
    zwin = max(2, A - E + 2)   # boundary spec
    tag = f'we_w{w[0]}{w[1]}{w[2]}_m{m}'
    r = row_of(*w, m, 0, F, zwin, tag)
    we_rows.append(r)
    all_rows.append(r)
    if r['Phi'] is not None and pp is not None and r['Phi'] != pp:
        we_mismatch.append({'tag': tag, 'Phi': r['Phi'], 'law': pp})
REPORT['WE_tables'] = {'n_rows': len(we_rows), 'rows': we_rows,
                       'phi_mismatch': we_mismatch}

# ------------------------------------------------------------------
# WF: D6 pre-registration battery, fresh re-run (12 rows; m12 unless
# noted).  Predicted values were pre-registered in the handoff.
# ------------------------------------------------------------------
WF_SPEC = [((0, 1, 0), 12, 8, 16), ((0, 0, 1), 12, 8, 17),
           ((0, 0, 2), 12, 8, 14), ((0, 1, 1), 12, 8, 13),
           ((0, 0, 3), 12, 8, 12), ((0, 1, 2), 12, 8, 11),
           ((0, 2, 1), 12, 8, 10), ((0, 4, 0), 12, 8, 7),
           ((0, 6, 0), 12, 10, 6),
           ((1, 0, 2), 12, 8, 10),   # [244]@12 = Phi([44],11) = 10
           ((1, 2, 0), 12, 7, 8),     # [233]@12 = Phi([33],11) = 8
           ((2, 1, 0), 11, 7, 4)]     # [223]@11 = Phi([3],9) = 4
wf_rows = []
wf_bad = []
for w, m, F, pred in WF_SPEC:
    pp = phi_pred(*w, m)
    A = etaf(m) - 2 * pp
    E = E_of(*w, m, 0, F)
    zwin = max(2, A - E + 2)
    tag = f'wf_w{w[0]}{w[1]}{w[2]}_m{m}'
    r = row_of(*w, m, 0, F, zwin, tag)
    wf_rows.append(r)
    all_rows.append(r)
    if r['Phi'] is None:
        wf_bad.append({'tag': tag, 'reason': 'unmeasured'})
    elif r['Phi'] != pred:
        wf_bad.append({'tag': tag, 'Phi': r['Phi'], 'prereg': pred})
    elif pp is not None and r['Phi'] != pp:
        wf_bad.append({'tag': tag, 'Phi': r['Phi'], 'law': pp})
REPORT['WF_prereg'] = {'n_rows': len(wf_rows), 'rows': wf_rows,
                       'bad': wf_bad}

# ------------------------------------------------------------------
# WG: wall-suppression arithmetic rows (predicted A < E => no 2 in
# the swept [0,2] window; plateau expected: v = E mod 2 complement as
# declared: constant = 1 if E odd else 0 on the swept band).
# Six D7 rows + one new declared row ([4444]@12 at F=7).
# ------------------------------------------------------------------
WG_SPEC = [((0, 0, 0), 12, 8), ((0, 5, 0), 12, 7), ((0, 6, 0), 11, 8),
           ((0, 7, 0), 11, 10), ((0, 7, 0), 12, 10), ((0, 4, 0), 9, 6),
           ((0, 0, 4), 12, 7)]
wg_rows = []
wg_bad = []
for w, m, F in WG_SPEC:
    pp = phi_pred(*w, m)
    A_pred = etaf(m) - 2 * pp
    X = build_X(*w, m, 0, F)
    E = 2 * X[0] - sum(X)
    vals, twos = measure(X, 2)
    plateau = 1 if E % 2 == 1 else 0
    rec = {'tag': f'wg_w{w[0]}{w[1]}{w[2]}_m{m}_F{F}', 'X': list(X),
           'n': len(X), 'j': 0, 'm': m, 'F': F, 'W': list(w), 'E': E,
           'zwin': 2, 'vals': vals, 'twos': twos, 'A': None, 'Phi': None,
           'parity_odd': None, 'A_pred': A_pred, 'Phi_pred': pp,
           'status': ('suppressed_consistent' if not twos
                      else 'SUPPRESSION_VIOLATION')}
    # boundary spec: A_pred == E would be a visible z2=0 line (not
    # expected here, but handled honestly rather than assumed away)
    if A_pred >= E:
        rec['status'] = 'PREDICTED-SUPPRESSED-BUT-VISIBLE'
    pb = [z for z, v in enumerate(vals) if v is not None and v != plateau]
    if pb:
        rec['plateau_bad'] = pb
    wg_rows.append(rec)
    if rec['status'] != 'suppressed_consistent' or pb:
        wg_bad.append({'tag': rec['tag'], 'status': rec['status'],
                       'plateau_bad': pb})
REPORT['WG_supp'] = {'n_rows': len(wg_rows), 'rows': wg_rows,
                     'bad': wg_bad}

# ------------------------------------------------------------------
# WH: handoff pending rows p1..p6b (explicit constructions; the log's
# p3 E value -57 is a misprint for the true E = -55 of X=(8^7,3^5),
# and p6a's listed X=(7^7,4,4,4,3,3) is inconsistent with its claimed
# (m=11) parameters, corrected here to X=(8^6,4,4,4,3,3); both
# corrections are recorded openly).
# ------------------------------------------------------------------
WH_SPEC = [
    ('p1', (0, 2, 0), 12, 1, 8, 12),    # [33]@(m12) j-shift witness
    ('p2', (0, 2, 2), 11, 0, 7, 7),     # [3344]@11 z2=0 boundary
    ('p3', (0, 5, 0), 12, 0, 8, 6),     # [3^5]@12 (log E=-57 misprint)
    ('p4', (0, 7, 0), 12, 0, 11, 6),    # [3^7]@12 kappa=-1
    ('p5', (0, 7, 0), 11, 0, 13, 5),    # [3^7]@11 kappa=-2 linear tier
    ('p6a', (0, 2, 3), 11, 0, 8, 7),    # corrected construction
    ('p6b', (0, 3, 2), 12, 0, 8, 8),    # [33344]@12 prereg
]
wh_rows = []
wh_bad = []
for tag, w, m, j, F, pred in WH_SPEC:
    pp = phi_pred(*w, m)
    A = etaf(m + j) + 2 * j - 2 * pp
    E = E_of(*w, m, j, F)
    zwin = max(2, A - E + 2)   # boundary spec (p2 is exactly z2=0)
    r = row_of(*w, m, j, F, zwin, f'wh_{tag}')
    wh_rows.append(r)
    all_rows.append(r)
    if r['Phi'] is None:
        wh_bad.append({'tag': tag, 'reason': 'unmeasured'})
    elif r['Phi'] != pred:
        wh_bad.append({'tag': tag, 'Phi': r['Phi'], 'pred': pred})
REPORT['WH_pending'] = {'n_rows': len(wh_rows), 'rows': wh_rows,
                        'bad': wh_bad,
                        'notes': {
                            'p3_E': 'handoff log lists E=-57 misprint; '
                                    'true E of X=(8^7,3^5) is -55 (z2=3)',
                            'p6a': 'handoff listed X=(7^7,4,4,4,3,3) '
                                   'with m=11 params, which is n=12; '
                                   'corrected X=(8^6,4,4,4,3,3) (n=11)',
                            'p5_second': 'the handoff declared '
                                    '[3^6]@10 unreachable via j-shift; '
                                    'measured here in WI at F=10 '
                                    'construction'}}

# ------------------------------------------------------------------
# WI: deep-tier probes.  Pure [3^b] kappa <= -1 rows (linear tier
# reading Phi = m-6), plus [3^6]@10 (log-declared unreachable, now
# measured), the [4] small-m rows, and the direct []@11 row
# (Phi = 15, previously OOM).
# ------------------------------------------------------------------
WI_SPEC = [
    ((0, 4, 0), 8, 6, 'linear2'), ((0, 5, 0), 9, 8, 'linear3'),
    ((0, 6, 0), 10, 10, 'linear4'), ((0, 8, 0), 12, 14, 'linear6'),
    ((0, 6, 0), 9, 13, 'linear3b'), ((0, 7, 0), 10, 17, 'linear4b'),
    ((0, 0, 1), 6, 5, 'pure4_m6'), ((0, 0, 1), 7, 5, 'pure4_m7'),
    ((0, 0, 2), 7, 5, 'pure44_m7'), ((0, 0, 0), 11, 8, 'empty_m11')]
wi_rows = []
wi_bad = []
for w, m, F, tag0 in WI_SPEC:
    pp = phi_pred(*w, m)
    A = etaf(m) - 2 * pp
    E = E_of(*w, m, 0, F)
    zwin = max(2, A - E + 2)
    r = row_of(*w, m, 0, F, zwin, f'wi_{tag0}')
    wi_rows.append(r)
    all_rows.append(r)
    if r['Phi'] is None:
        wi_bad.append({'tag': tag0, 'reason': 'unmeasured'})
    elif pp is not None and r['Phi'] != pp:
        wi_bad.append({'tag': tag0, 'Phi': r['Phi'], 'law': pp})
REPORT['WI_deep'] = {'n_rows': len(wi_rows), 'rows': wi_rows,
                     'bad': wi_bad}

# ------------------------------------------------------------------
# WJ: synthesis agreement across every measured row (machine
# cross-check of A = eta(n)+2j-2Phi(m,W) and Phi==law where the law
# zone is declared).
# ------------------------------------------------------------------
synth = {'rows_seen': 0, 'measured': 0, 'agree': 0, 'law_open': 0,
         'suppressed': 0, 'violations': [], 'conform_bad': 0,
         'parity_odd': 0}
for r in all_rows:
    synth['rows_seen'] += 1
    pp = r.get('Phi_pred')
    if r['Phi'] is None:
        if pp is None:
            synth['law_open'] += 1
        else:
            synth['suppressed'] += 1
        continue
    synth['measured'] += 1
    if r.get('parity_odd'):
        synth['parity_odd'] += 1
    if pp is None:
        synth['law_open'] += 1
        continue
    if r['Phi'] == pp:
        synth['agree'] += 1
    else:
        synth['violations'].append({'tag': r['tag'], 'm': r['m'],
                                    'W': r['W'], 'j': r.get('j', 0),
                                    'Phi': r['Phi'], 'Phi_pred': pp})
    if r.get('conform_bad'):
        synth['conform_bad'] += 1
REPORT['WJ_synth'] = synth

# ------------------------------------------------------------------
# WZ: refined deep-tier summary, split by family:
#  (1) pure [3^b] deep probes (b >= m-4, c=0, a=0, kappa <= -2, plus
#      the kappa=-1 seam rows): linear-tier reading Phi = m-6;
#  (2) []-family deep floor probes through the m=6 tier sweep rows
#      with b=c=0, a>=1: strip targets m'=m-a <= 5, measured Phi
#      (recorded; standing flat-zero observation in this freeze).
# ------------------------------------------------------------------
deep3 = []
deepE = []
for r in all_rows:
    a, b, c = r['W']
    m = r['m']
    if a == 0 and b >= 1 and c == 0 and (m - 6 - b) <= -1:
        deep3.append({'tag': r['tag'], 'W': r['W'], 'm': m,
                      'kappa': m - 6 - b, 'Phi': r['Phi'],
                      'linear_pred': m - 6,
                      'linear_ok': (r['Phi'] == m - 6)})
    if a >= 1 and (m - a) <= 5:
        # every family's stripped target lands in the open zone m' <= 5;
        # the family formulas would go NEGATIVE there (e.g. [24]@6 ->
        # Phi([4],5) = -1 by formula) but the measured tier rows sit at
        # Phi = 0: the flat deep floor across families.
        deepE.append({'tag': r['tag'], 'W': r['W'], 'm': m,
                      'm_stripped': m - a, 'Phi': r['Phi'],
                      'floor0_ok': (r['Phi'] == 0)})
REPORT['WZ_deep_linear'] = {
    'pure3_probes': deep3,
    'pure3_n': len(deep3),
    'pure3_measured': sum(1 for d in deep3 if d['Phi'] is not None),
    'pure3_linear_ok': sum(1 for d in deep3 if d['linear_ok']),
    'empty_floor_probes': deepE,
    'empty_floor_n': len(deepE),
    'empty_floor_measured': sum(1 for d in deepE if d['Phi'] is not None),
    'empty_floor0_ok': sum(1 for d in deepE if d['floor0_ok']),
}

print(json.dumps(REPORT, sort_keys=True))
