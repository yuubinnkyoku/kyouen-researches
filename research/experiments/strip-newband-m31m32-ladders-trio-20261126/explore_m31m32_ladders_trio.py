"""
explore_m31m32_ladders_trio: FROZEN PRE-DECLARATION census for:

1. the TWENTY-EIGHT binding candidate rows of the kit-7 frozen output
   section future_slice_registration_constants (commit a62c5d2e): the
   ladder continuation / birth / death rows of m=19..m=28 (items 1-20),
   the m=29 / m=30 MINI-LADDER rows (items 21-26: one-past of the d=0
   seat, birth d=1, one-past-of-d=1 / death-of-d=0), and the frontier
   first contacts m=31@z=61 / m=32@z=62 (items 27-28, the registered
   19th / 20th K1268 parity datum candidates, FIRST-EVER rows for those
   m). Every candidate literal is machine-regenerated engine-free from
   the K0832 closed form + the seat-lifecycle scaffold by derive_kit8.py
   (370 structural asserts, 0 failures; the regenerated prediction TEXT
   of all 28 rows byte-matches the kit-7 frozen constants, proving the
   generator AND the transcription, the way the kit-6 lifecycle-shift
   lesson prescribes: stick-slice occupancy z=S(d-1), death-slice
   occupancy z=S(d-1)+1, co-token/S/R and every collapse v() literal
   machine-recomputed BEFORE any measurement by this file).
2. the TRIO-TRACKER rows (kit-7 log S5 item 10, NON-BINDING observation
   candidates; any outcome is the datum): at m=19 z=56 and z=57 the
   stacked trio {19,19,19}@S=57 (the kit-7 deviation shadow seat) is
   tracked beside the binding seat candidates and must be reported
   explicitly either way: z=56 mimic candidate UP 1v0 like the birth
   seat one-past, or conform (collapse v(57,56,76)=0), or other;
   z=57 mimic candidate DOWN 1v2 like the stick, or conform (collapse
   v(57,57,77)=2), or other.
3. the m=26 z=25 HOLE ROW (kit-7 log S5 item 11, registered candidate:
   0 separations; the published z=25 floor strip covered m in {20..25}
   only, so m=26@z=25 was never measured; if clean this closes the m=26
   measured line to z in {25..56}).
4. the TRIO MID-SLICE PROBES (kit-7 log S5 item 12 proposals,
   counter-probed 0-hit at this build BEFORE registering): the full x0
   row records m=13@z=37, m=15@z=43, m=17@z=49. DATED DISCLOSURE: the
   kit-7 log S5 prose listed the probe slices as m=13 z=37, m=15 z=42,
   m=17 z=48; the derived slices are z=z*(m)+2d with d=(m-1)/2, i.e.
   z=3m-2: 37/43/49. The m=13 value 37 matches; the m=15/m=17 prose
   values 42/48 are off-by-one typos in the kit-7 log prose (the kit-7
   FROZEN section (d), the SSOT, contains none of these rows, so no
   frozen byte is affected). This kit registers the derived values
   37/43/49 with binding birth-row candidates (stick + NEW seats, same
   template as the binding items) plus the NON-BINDING trio probe
   candidate {m,m,m}@S=3m UP 2v0 mimic (the m=19 z=55 precedent
   datum), or conform, or other; the trio lifecycle beyond z=55 is the
   primary open question (kit-7 S6 item 1) and the probes test whether
   the mid-ladder trio shadow generalizes to the in-sweep odd m<19.
5. the WINDOW SWEEPS m=29 z in {49..56} and m=30 z in {50..57} (kit-7
   frozen section (d) items 29/30 window proposals; register before
   measuring satisfied by THIS FREEZE; candidates 0 separations each
   per the in-band-clean precedent; FIRST-EVER below-frontier rows for
   m=29/m=30, no strip-derivation claim made - m=29/m=30 are NOT
   strip-covered).
6. THE ANCHOR CHAIN: the 141 kit-7-era published anchors VERBATIM
   (inherited anchor_spec block, byte-copied from the kit-7 explorer
   and re-measured here) PLUS the 39 kit-7 separation spots
   (38 named seat separations + the stacked-trio deviation seat),
   machine-extracted from the published kit-7 frozen .out and
   machine-verified 39/39 BEFORE the first run of this file by
   verify_new_anchors_kit8.py (canonical engine, published values
   only).
7. the K0832 battery: the UNION of the kit-7 737 battery literal
   triples (no prior datum lost; layout change disclosed: the battery
   rows are now a sorted-unique triple set instead of an insertion-order
   multiset, the checked property is unchanged: closed==canonical==
   ordered per triple) PLUS the kit-8 literals: stair rows of every
   measured row, the registered candidate collapse literals, the new
   anchor collapse literals, and the kit-9 future constants.

SWEEP-DOMAIN RULE (frozen here, disclosed): every depth row sweeps
S in {m..max(m+38, z+2)} with the published x0 convention (parts>=m,
arity<=3 TOTAL, X[0]=m, co-token m allowed). The kit-7 convention
smax=m+38 covered all registered seats through the kit-7 depths, but
from d=10 onward the NEW birth seat S(d)=z+2 exceeds m+38 for
m in {19,20}; the extension to max(m+38, z+2) is the minimal domain
covering every registered named seat (m=19 z=56/57 -> 57/58->59,
m=20 z=57/58 -> 58/59->60). Any separation found inside the extended
domain beyond the registered seats is a deviation = the datum.

Counter-probe at this build (2026-11-26, head a62c5d2e): 10 kit-specific
content queries (explore_m31m32, frontier_m31, trio-tracker/trio_tracker,
"m=31 z=61", kit-8, mid-slice trio, "z=25 hole", "m=19 z=56",
inband_m29_z49, stacked-trio) returned 0 measurement records, and no
experiment directory or log for any of this kit's rows exists on main.
Re-run at push time against then-current main and disclosed in the push
commit body.

NO K slot is claimed by this file; the 28 binding candidate rows, the
hole row, the 3 probe rows and the 16 window rows in this docstring were
frozen BEFORE the first run of this file (the trio-tracker statuses are
NON-BINDING and their outcome is the datum). The only edit performed
after any run must be disclosed here in dated form (verifier-table or
docstring fixes only; no candidate, engine, or measurement code was
edited at any time).
"""

import hashlib, json, sys
from functools import lru_cache

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
ns = {'lru_cache': lru_cache}
exec(ENGINE_BLOCK, ns)
H = ns['H_canonical']
v = ns['single_token']


def parts(s, lo, arity):
    """all multisets (nondecreasing tuples) of tokens >= lo, sum s, 1..arity tokens"""
    out = []

    def rec(rem, k, cur):
        if rem == 0:
            if 1 <= len(cur) <= arity:
                out.append(tuple(cur))
            return
        if k == arity:
            return
        for t in range(lo, rem + 1):
            if cur and t < cur[-1]:
                continue
            cur.append(t)
            rec(rem - t, k + 1, cur)
            cur.pop()

    rec(s, 0, [])
    return out


def row_record(sec, rlabel, extra, R, z, m, smin, smax, min_tok):
    """co-token style sweep: X = (m,) U parts >= min_tok (arity up to 4 total)."""
    H.cache_clear()
    sep = []
    scnt = 0
    for S in range(smin, smax + 1):
        for X in parts(max(S - m, 0), min_tok, 3):
            XX = tuple(sorted((m,) + X, reverse=True))
            if sum(XX) != S:
                continue
            hv = H(R, XX, z)
            ev = v(S, z, R)
            scnt += 1
            if hv != ev:
                sep.append({'X': list(XX), 'S': S, 'value': hv,
                            'collapse': ev,
                            'direction': 'UP' if hv > ev else 'DOWN'})
    return {'section': sec, 'label': rlabel, 'R': R, 'z': z, 'min': m,
            **extra, 'shapes': scnt, 'separations': sep}


def row_record_x0(sec, rlabel, extra, R, z, m, smin, smax):
    """published residual-band record style: X = parts(S, m, 3) with
    X[0] == m, i.e. all parts >= m with co-token m allowed, arity <= 3
    TOTAL. Shape-for-shape comparable with the published entries."""
    H.cache_clear()
    sep = []
    scnt = 0
    for S in range(smin, smax + 1):
        for X in parts(S, m, 3):
            if not X or X[0] != m:
                continue
            hv = H(R, X, z)
            ev = v(S, z, R)
            scnt += 1
            if hv != ev:
                sep.append({'X': list(X), 'S': S, 'value': hv,
                            'collapse': ev,
                            'direction': 'UP' if hv > ev else 'DOWN'})
    return {'section': sec, 'label': rlabel, 'R': R, 'z': z, 'min': m,
            **extra, 'shapes': scnt, 'separations': sep}





K8_BINDING_JSON = "[\n {\n  \"item\": 1,\n  \"m\": 19,\n  \"z\": 56,\n  \"kind\": \"one-past-of-d=9 / death-of-d=8\",\n  \"cand\": \"EXACTLY ONE: {19,38}@S=57 UP 1v0 (collapse v(57,56,76)=0); {19,36} conform-DEAD at z=56=S+1 (collapse v(55,56,76)=1); death-of-d=8; any deviation is the datum\",\n  \"tracker\": [\n   {\n    \"m\": 19,\n    \"z\": 56,\n    \"X\": [\n     19,\n     19,\n     19\n    ],\n    \"S\": 57,\n    \"cand\": \"mimic: UP 1v0 (value 1) like the birth seat one-past {19,38}@S=57, or conform (value 0 = collapse v(57,56,76)), or other; NON-BINDING observation candidate, any outcome is the datum\"\n   }\n  ]\n },\n {\n  \"item\": 2,\n  \"m\": 19,\n  \"z\": 57,\n  \"kind\": \"birth slice d=10\",\n  \"cand\": \"EXACTLY TWO: stick {19,38} DOWN 1v2 (collapse v(57,57,77)=2) + NEW {19,40}@S=59 UP 2v0 (collapse v(59,57,77)=0), d=10 seat gap 21 (stick seat coincides z=S(d-1)); any deviation is the datum\",\n  \"tracker\": [\n   {\n    \"m\": 19,\n    \"z\": 57,\n    \"X\": [\n     19,\n     19,\n     19\n    ],\n    \"S\": 57,\n    \"cand\": \"mimic: DOWN 1v2 (value 1, collapse 2) like the stick {19,38}@S=57, or conform (value 2 = collapse v(57,57,77)), or other; NON-BINDING observation candidate, any outcome is the datum\"\n   }\n  ]\n },\n {\n  \"item\": 3,\n  \"m\": 20,\n  \"z\": 57,\n  \"kind\": \"one-past-of-d=9 / death-of-d=8\",\n  \"cand\": \"EXACTLY ONE: (20,38)@S=58 DOWN 0v1 (collapse v(58,57,78)=1); (20,36) conform-DEAD at z=57=S+1 (collapse v(56,57,78)=0); death-of-d=8; any deviation is the datum\"\n },\n {\n  \"item\": 4,\n  \"m\": 20,\n  \"z\": 58,\n  \"kind\": \"birth slice d=10\",\n  \"cand\": \"EXACTLY TWO: stick (20,38) DOWN 0v2 (collapse v(58,58,79)=2) + NEW (20,40)@S=60 UP 2v1 (collapse v(60,58,79)=1), d=10 seat gap 20 (stick seat coincides z=S(d-1)); any deviation is the datum\"\n },\n {\n  \"item\": 5,\n  \"m\": 21,\n  \"z\": 52,\n  \"kind\": \"one-past-of-d=5 / death-of-d=4\",\n  \"cand\": \"EXACTLY ONE: {21,32}@S=53 UP 1v0 (collapse v(53,52,74)=0); {21,30} conform-DEAD at z=52=S+1 (collapse v(51,52,74)=1); death-of-d=4; any deviation is the datum\"\n },\n {\n  \"item\": 6,\n  \"m\": 21,\n  \"z\": 53,\n  \"kind\": \"birth slice d=6\",\n  \"cand\": \"EXACTLY TWO: stick {21,32} DOWN 1v2 (collapse v(53,53,75)=2) + NEW {21,34}@S=55 UP 2v0 (collapse v(55,53,75)=0), d=6 seat gap 13 (stick seat coincides z=S(d-1)); any deviation is the datum\"\n },\n {\n  \"item\": 7,\n  \"m\": 22,\n  \"z\": 53,\n  \"kind\": \"one-past-of-d=5 / death-of-d=4\",\n  \"cand\": \"EXACTLY ONE: (22,32)@S=54 DOWN 0v1 (collapse v(54,53,76)=1); (22,30) conform-DEAD at z=53=S+1 (collapse v(52,53,76)=0); death-of-d=4; any deviation is the datum\"\n },\n {\n  \"item\": 8,\n  \"m\": 22,\n  \"z\": 54,\n  \"kind\": \"birth slice d=6\",\n  \"cand\": \"EXACTLY TWO: stick (22,32) DOWN 0v2 (collapse v(54,54,77)=2) + NEW (22,34)@S=56 UP 2v1 (collapse v(56,54,77)=1), d=6 seat gap 12 (stick seat coincides z=S(d-1)); any deviation is the datum\"\n },\n {\n  \"item\": 9,\n  \"m\": 23,\n  \"z\": 54,\n  \"kind\": \"one-past-of-d=4 / death-of-d=3\",\n  \"cand\": \"EXACTLY ONE: {23,32}@S=55 UP 1v0 (collapse v(55,54,78)=0); {23,30} conform-DEAD at z=54=S+1 (collapse v(53,54,78)=1); death-of-d=3; any deviation is the datum\"\n },\n {\n  \"item\": 10,\n  \"m\": 23,\n  \"z\": 55,\n  \"kind\": \"birth slice d=5\",\n  \"cand\": \"EXACTLY TWO: stick {23,32} DOWN 1v2 (collapse v(55,55,79)=2) + NEW {23,34}@S=57 UP 2v0 (collapse v(57,55,79)=0), d=5 seat gap 11 (stick seat coincides z=S(d-1)); any deviation is the datum\"\n },\n {\n  \"item\": 11,\n  \"m\": 24,\n  \"z\": 55,\n  \"kind\": \"one-past-of-d=4 / death-of-d=3\",\n  \"cand\": \"EXACTLY ONE: (24,32)@S=56 DOWN 0v1 (collapse v(56,55,80)=1); (24,30) conform-DEAD at z=55=S+1 (collapse v(54,55,80)=0); death-of-d=3; any deviation is the datum\"\n },\n {\n  \"item\": 12,\n  \"m\": 24,\n  \"z\": 56,\n  \"kind\": \"birth slice d=5\",\n  \"cand\": \"EXACTLY TWO: stick (24,32) DOWN 0v2 (collapse v(56,56,81)=2) + NEW (24,34)@S=58 UP 2v1 (collapse v(58,56,81)=1), d=5 seat gap 10 (stick seat coincides z=S(d-1)); any deviation is the datum\"\n },\n {\n  \"item\": 13,\n  \"m\": 25,\n  \"z\": 56,\n  \"kind\": \"one-past-of-d=3 / death-of-d=2\",\n  \"cand\": \"EXACTLY ONE: {25,32}@S=57 UP 1v0 (collapse v(57,56,82)=0); {25,30} conform-DEAD at z=56=S+1 (collapse v(55,56,82)=1); death-of-d=2; any deviation is the datum\"\n },\n {\n  \"item\": 14,\n  \"m\": 25,\n  \"z\": 57,\n  \"kind\": \"birth slice d=4\",\n  \"cand\": \"EXACTLY TWO: stick {25,32} DOWN 1v2 (collapse v(57,57,83)=2) + NEW {25,34}@S=59 UP 2v0 (collapse v(59,57,83)=0), d=4 seat gap 9 (stick seat coincides z=S(d-1)); any deviation is the datum\"\n },\n {\n  \"item\": 15,\n  \"m\": 26,\n  \"z\": 57,\n  \"kind\": \"one-past-of-d=3 / death-of-d=2\",\n  \"cand\": \"EXACTLY ONE: (26,32)@S=58 DOWN 0v1 (collapse v(58,57,84)=1); (26,30) conform-DEAD at z=57=S+1 (collapse v(56,57,84)=0); death-of-d=2; any deviation is the datum\"\n },\n {\n  \"item\": 16,\n  \"m\": 26,\n  \"z\": 58,\n  \"kind\": \"birth slice d=4\",\n  \"cand\": \"EXACTLY TWO: stick (26,32) DOWN 0v2 (collapse v(58,58,85)=2) + NEW (26,34)@S=60 UP 2v1 (collapse v(60,58,85)=1), d=4 seat gap 8 (stick seat coincides z=S(d-1)); any deviation is the datum\"\n },\n {\n  \"item\": 17,\n  \"m\": 27,\n  \"z\": 56,\n  \"kind\": \"one-past-of-d=1 / death-of-d=0\",\n  \"cand\": \"EXACTLY ONE: {27,30}@S=57 UP 1v0 (collapse v(57,56,84)=0); {27,28} conform-DEAD at z=56=S+1 (collapse v(55,56,84)=1); death-of-d=0; any deviation is the datum\"\n },\n {\n  \"item\": 18,\n  \"m\": 27,\n  \"z\": 57,\n  \"kind\": \"birth slice d=2\",\n  \"cand\": \"EXACTLY TWO: stick {27,30} DOWN 1v2 (collapse v(57,57,85)=2) + NEW {27,32}@S=59 UP 2v0 (collapse v(59,57,85)=0), d=2 seat gap 5 (stick seat coincides z=S(d-1)); any deviation is the datum\"\n },\n {\n  \"item\": 19,\n  \"m\": 28,\n  \"z\": 57,\n  \"kind\": \"one-past-of-d=1 / death-of-d=0\",\n  \"cand\": \"EXACTLY ONE: (28,30)@S=58 DOWN 0v1 (collapse v(58,57,86)=1); (28,28) conform-DEAD at z=57=S+1 (collapse v(56,57,86)=0); death-of-d=0; any deviation is the datum\"\n },\n {\n  \"item\": 20,\n  \"m\": 28,\n  \"z\": 58,\n  \"kind\": \"birth slice d=2\",\n  \"cand\": \"EXACTLY TWO: stick (28,30) DOWN 0v2 (collapse v(58,58,87)=2) + NEW (28,32)@S=60 UP 2v1 (collapse v(60,58,87)=1), d=2 seat gap 4 (stick seat coincides z=S(d-1)); any deviation is the datum\"\n },\n {\n  \"item\": 21,\n  \"m\": 29,\n  \"z\": 58,\n  \"kind\": \"one-past of the d=0 seat\",\n  \"cand\": \"EXACTLY ONE: {29,30}@S=59 UP 1v0 (collapse v(59,58,88)=0); one-past of the d=0 seat (frontier decay 2->1); any deviation is the datum\"\n },\n {\n  \"item\": 22,\n  \"m\": 29,\n  \"z\": 59,\n  \"kind\": \"birth slice d=1\",\n  \"cand\": \"EXACTLY TWO: stick {29,30} DOWN 1v2 (collapse v(59,59,89)=2) + NEW {29,32}@S=61 UP 2v0 (collapse v(61,59,89)=0), d=1 seat gap 3 (stick seat coincides z=S(d-1)); any deviation is the datum\"\n },\n {\n  \"item\": 23,\n  \"m\": 29,\n  \"z\": 60,\n  \"kind\": \"one-past-of-d=1 / death-of-d=0\",\n  \"cand\": \"EXACTLY ONE: {29,32}@S=61 UP 1v0 (collapse v(61,60,90)=0); {29,30} conform-DEAD at z=60=S+1 (collapse v(59,60,90)=1); death-of-d=0; any deviation is the datum\"\n },\n {\n  \"item\": 24,\n  \"m\": 30,\n  \"z\": 59,\n  \"kind\": \"one-past of the d=0 seat\",\n  \"cand\": \"EXACTLY ONE: (30,30)@S=60 DOWN 0v1 (collapse v(60,59,90)=1); one-past of the d=0 seat (frontier decay 2->0); any deviation is the datum\"\n },\n {\n  \"item\": 25,\n  \"m\": 30,\n  \"z\": 60,\n  \"kind\": \"birth slice d=1\",\n  \"cand\": \"EXACTLY TWO: stick (30,30) DOWN 0v2 (collapse v(60,60,91)=2) + NEW (30,32)@S=62 UP 2v1 (collapse v(62,60,91)=1), d=1 seat gap 2 (stick seat coincides z=S(d-1)); any deviation is the datum\"\n },\n {\n  \"item\": 26,\n  \"m\": 30,\n  \"z\": 61,\n  \"kind\": \"one-past-of-d=1 / death-of-d=0\",\n  \"cand\": \"EXACTLY ONE: (30,32)@S=62 DOWN 0v1 (collapse v(62,61,92)=1); (30,30) conform-DEAD at z=61=S+1 (collapse v(60,61,92)=0); death-of-d=0; any deviation is the datum\"\n },\n {\n  \"item\": 27,\n  \"m\": 31,\n  \"z\": 61,\n  \"kind\": \"frontier first contact proposal (FIRST-EVER m=31 row)\",\n  \"cand\": \"EXACTLY ONE: {31,32}@S=63 UP 2v0 (collapse v(63,61,93)=0); z*(31)=2*31-2+1=61 per K1268 (derive_check double-checked); R=93; any deviation is the datum\",\n  \"frontier\": true,\n  \"nth\": \"19th\"\n },\n {\n  \"item\": 28,\n  \"m\": 32,\n  \"z\": 62,\n  \"kind\": \"frontier first contact proposal (FIRST-EVER m=32 row)\",\n  \"cand\": \"EXACTLY ONE: (32,32)@S=64 UP 2v1 (collapse v(64,62,95)=1); z*(32)=2*32-2+0=62 per K1268 (derive_check double-checked); R=95; any deviation is the datum\",\n  \"frontier\": true,\n  \"nth\": \"20th\"\n }\n]"
K8_PROBES_JSON = "[\n {\n  \"m\": 13,\n  \"z\": 37,\n  \"kind\": \"trio mid-slice probe (d=(m-1)/2 birth row; binding birth template + NON-BINDING trio probe)\",\n  \"cand\": \"EXACTLY TWO: stick {13,24} DOWN 1v2 (collapse v(37,37,51)=2) + NEW {13,26}@S=39 UP 2v0 (collapse v(39,37,51)=0), d=6 seat gap 13\",\n  \"trio\": \"trio {13,13,13}@S=39 UP 2v0 mimic candidate (the m=19 z=55 precedent datum), or conform, or other; NON-BINDING probe, any outcome is the datum\"\n },\n {\n  \"m\": 15,\n  \"z\": 43,\n  \"kind\": \"trio mid-slice probe (d=(m-1)/2 birth row; binding birth template + NON-BINDING trio probe)\",\n  \"cand\": \"EXACTLY TWO: stick {15,28} DOWN 1v2 (collapse v(43,43,59)=2) + NEW {15,30}@S=45 UP 2v0 (collapse v(45,43,59)=0), d=7 seat gap 15\",\n  \"trio\": \"trio {15,15,15}@S=45 UP 2v0 mimic candidate (the m=19 z=55 precedent datum), or conform, or other; NON-BINDING probe, any outcome is the datum\"\n },\n {\n  \"m\": 17,\n  \"z\": 49,\n  \"kind\": \"trio mid-slice probe (d=(m-1)/2 birth row; binding birth template + NON-BINDING trio probe)\",\n  \"cand\": \"EXACTLY TWO: stick {17,32} DOWN 1v2 (collapse v(49,49,67)=2) + NEW {17,34}@S=51 UP 2v0 (collapse v(51,49,67)=0), d=8 seat gap 17\",\n  \"trio\": \"trio {17,17,17}@S=51 UP 2v0 mimic candidate (the m=19 z=55 precedent datum), or conform, or other; NON-BINDING probe, any outcome is the datum\"\n }\n]"
BATTERY_TRIPLES_JSON = "[[13, 37, 51], [15, 37, 51], [15, 43, 59], [17, 43, 59], [17, 49, 67], [19, 49, 67], [19, 54, 74], [19, 55, 75], [19, 56, 76], [19, 57, 77], [20, 55, 76], [20, 56, 77], [20, 57, 78], [20, 58, 79], [21, 50, 72], [21, 51, 73], [21, 52, 74], [21, 53, 75], [21, 54, 74], [21, 55, 75], [21, 56, 76], [21, 57, 77], [22, 51, 74], [22, 52, 75], [22, 53, 76], [22, 54, 77], [22, 55, 76], [22, 56, 77], [22, 57, 78], [22, 58, 79], [23, 50, 72], [23, 51, 73], [23, 52, 74], [23, 52, 76], [23, 53, 75], [23, 53, 77], [23, 54, 78], [23, 55, 79], [24, 51, 74], [24, 52, 75], [24, 53, 76], [24, 53, 78], [24, 54, 77], [24, 54, 79], [24, 55, 80], [24, 56, 81], [25, 27, 53], [25, 28, 54], [25, 29, 55], [25, 30, 56], [25, 31, 57], [25, 32, 58], [25, 33, 59], [25, 34, 60], [25, 35, 61], [25, 36, 62], [25, 37, 63], [25, 38, 64], [25, 39, 65], [25, 40, 66], [25, 52, 76], [25, 53, 77], [25, 53, 79], [25, 54, 78], [25, 54, 80], [25, 55, 79], [25, 55, 81], [25, 56, 82], [25, 57, 83], [26, 25, 52], [26, 27, 54], [26, 28, 55], [26, 29, 56], [26, 30, 57], [26, 31, 58], [26, 32, 59], [26, 33, 60], [26, 34, 61], [26, 35, 62], [26, 36, 63], [26, 37, 51], [26, 37, 64], [26, 38, 65], [26, 39, 66], [26, 40, 67], [26, 41, 68], [26, 42, 69], [26, 53, 78], [26, 54, 79], [26, 54, 81], [26, 55, 80], [26, 55, 82], [26, 56, 81], [26, 56, 83], [26, 57, 84], [26, 58, 85], [27, 27, 41], [27, 27, 53], [27, 28, 54], [27, 29, 55], [27, 30, 56], [27, 31, 57], [27, 32, 58], [27, 33, 59], [27, 34, 60], [27, 35, 61], [27, 36, 62], [27, 37, 51], [27, 37, 63], [27, 38, 64], [27, 39, 65], [27, 40, 66], [27, 45, 73], [27, 46, 74], [27, 47, 75], [27, 48, 76], [27, 49, 77], [27, 50, 78], [27, 51, 79], [27, 52, 80], [27, 53, 79], [27, 54, 80], [27, 54, 82], [27, 55, 81], [27, 55, 83], [27, 56, 82], [27, 56, 84], [27, 57, 83], [27, 57, 85], [28, 25, 52], [28, 27, 54], [28, 28, 55], [28, 29, 56], [28, 30, 57], [28, 31, 58], [28, 32, 59], [28, 33, 60], [28, 34, 61], [28, 35, 62], [28, 36, 63], [28, 37, 64], [28, 38, 65], [28, 39, 66], [28, 40, 67], [28, 41, 68], [28, 42, 69], [28, 46, 75], [28, 47, 76], [28, 48, 77], [28, 49, 78], [28, 50, 79], [28, 51, 80], [28, 52, 81], [28, 53, 82], [28, 54, 81], [28, 55, 82], [28, 55, 84], [28, 56, 83], [28, 56, 85], [28, 57, 84], [28, 57, 86], [28, 58, 85], [28, 58, 87], [29, 27, 41], [29, 45, 73], [29, 46, 74], [29, 47, 75], [29, 48, 76], [29, 49, 77], [29, 49, 79], [29, 50, 78], [29, 50, 80], [29, 51, 79], [29, 51, 81], [29, 52, 80], [29, 52, 82], [29, 53, 83], [29, 54, 82], [29, 54, 84], [29, 55, 83], [29, 55, 85], [29, 56, 84], [29, 56, 86], [29, 57, 85], [29, 57, 87], [29, 58, 88], [29, 59, 89], [29, 60, 90], [30, 43, 59], [30, 46, 75], [30, 47, 76], [30, 48, 77], [30, 49, 78], [30, 50, 79], [30, 50, 81], [30, 51, 80], [30, 51, 82], [30, 52, 81], [30, 52, 83], [30, 53, 82], [30, 53, 84], [30, 54, 85], [30, 55, 84], [30, 55, 86], [30, 56, 85], [30, 56, 87], [30, 57, 86], [30, 57, 88], [30, 58, 87], [30, 58, 89], [30, 59, 90], [30, 60, 91], [30, 61, 92], [31, 29, 45], [31, 30, 46], [31, 43, 59], [31, 49, 79], [31, 50, 80], [31, 51, 81], [31, 52, 82], [31, 53, 83], [31, 54, 84], [31, 55, 85], [31, 56, 86], [31, 57, 87], [31, 58, 88], [31, 59, 89], [31, 60, 90], [31, 61, 93], [32, 30, 47], [32, 31, 48], [32, 50, 81], [32, 51, 82], [32, 52, 83], [32, 53, 84], [32, 54, 85], [32, 55, 86], [32, 56, 87], [32, 57, 88], [32, 58, 89], [32, 59, 90], [32, 60, 91], [32, 61, 92], [32, 62, 95], [33, 28, 45], [33, 29, 46], [33, 30, 47], [33, 31, 48], [33, 32, 49], [33, 33, 47], [33, 61, 93], [34, 28, 46], [34, 29, 47], [34, 30, 48], [34, 31, 49], [34, 32, 50], [34, 49, 67], [34, 62, 95], [35, 28, 46], [35, 29, 47], [35, 30, 48], [35, 31, 49], [35, 32, 50], [35, 33, 47], [35, 35, 53], [35, 49, 67], [36, 28, 47], [36, 29, 48], [36, 30, 49], [36, 31, 50], [36, 32, 51], [37, 35, 53], [37, 37, 51], [38, 25, 45], [38, 26, 46], [38, 54, 74], [38, 55, 75], [38, 56, 76], [38, 57, 77], [39, 37, 51], [39, 37, 57], [39, 38, 58], [39, 39, 59], [39, 54, 74], [39, 55, 75], [39, 56, 76], [39, 57, 77], [40, 38, 59], [40, 39, 60], [40, 40, 61], [40, 55, 76], [40, 56, 77], [40, 57, 78], [40, 58, 79], [41, 39, 59], [41, 40, 60], [41, 41, 61], [41, 55, 76], [41, 56, 77], [41, 57, 78], [41, 58, 79], [42, 40, 61], [42, 41, 62], [42, 42, 63], [42, 50, 72], [42, 51, 73], [42, 52, 74], [42, 53, 75], [43, 41, 61], [43, 41, 63], [43, 42, 62], [43, 42, 64], [43, 43, 59], [43, 43, 63], [43, 43, 65], [43, 50, 72], [43, 51, 73], [43, 52, 74], [43, 53, 75], [44, 42, 63], [44, 42, 65], [44, 43, 64], [44, 43, 66], [44, 44, 65], [44, 44, 67], [44, 51, 74], [44, 52, 75], [44, 53, 76], [44, 54, 77], [45, 43, 59], [45, 43, 63], [45, 43, 65], [45, 44, 64], [45, 44, 66], [45, 45, 65], [45, 45, 67], [45, 46, 68], [45, 51, 74], [45, 52, 75], [45, 53, 76], [45, 54, 77], [46, 44, 65], [46, 44, 67], [46, 45, 66], [46, 45, 68], [46, 46, 67], [46, 46, 69], [46, 47, 68], [46, 47, 70], [46, 52, 76], [46, 53, 77], [46, 54, 78], [46, 55, 79], [47, 45, 65], [47, 45, 67], [47, 45, 69], [47, 46, 66], [47, 46, 68], [47, 46, 70], [47, 47, 67], [47, 47, 69], [47, 47, 71], [47, 48, 70], [47, 48, 72], [47, 52, 76], [47, 53, 77], [47, 54, 78], [47, 55, 79], [48, 46, 67], [48, 46, 69], [48, 46, 71], [48, 47, 68], [48, 47, 70], [48, 47, 72], [48, 48, 69], [48, 48, 71], [48, 48, 73], [48, 49, 72], [48, 53, 78], [48, 54, 79], [48, 55, 80], [48, 56, 81], [49, 47, 67], [49, 47, 69], [49, 47, 71], [49, 48, 68], [49, 48, 70], [49, 48, 72], [49, 49, 67], [49, 49, 69], [49, 49, 71], [49, 49, 73], [49, 50, 70], [49, 50, 74], [49, 53, 78], [49, 54, 79], [49, 55, 80], [49, 56, 81], [50, 27, 53], [50, 28, 54], [50, 29, 55], [50, 30, 56], [50, 31, 57], [50, 32, 58], [50, 33, 59], [50, 34, 60], [50, 35, 61], [50, 36, 62], [50, 37, 51], [50, 37, 63], [50, 38, 64], [50, 39, 65], [50, 40, 66], [50, 48, 69], [50, 48, 71], [50, 48, 73], [50, 49, 70], [50, 49, 72], [50, 49, 74], [50, 50, 71], [50, 50, 73], [50, 50, 75], [50, 51, 72], [50, 51, 76], [50, 53, 79], [50, 54, 80], [50, 55, 81], [50, 56, 82], [50, 57, 83], [51, 27, 53], [51, 28, 54], [51, 29, 55], [51, 30, 56], [51, 31, 57], [51, 32, 58], [51, 33, 59], [51, 34, 60], [51, 35, 61], [51, 36, 62], [51, 37, 51], [51, 37, 63], [51, 38, 64], [51, 39, 65], [51, 40, 66], [51, 49, 67], [51, 49, 69], [51, 49, 71], [51, 49, 73], [51, 49, 75], [51, 50, 70], [51, 50, 72], [51, 50, 74], [51, 50, 76], [51, 51, 71], [51, 51, 73], [51, 51, 75], [51, 51, 77], [51, 52, 72], [51, 52, 74], [51, 52, 76], [51, 52, 78], [51, 53, 79], [51, 54, 80], [51, 55, 81], [51, 56, 82], [51, 57, 83], [52, 25, 52], [52, 27, 54], [52, 28, 55], [52, 29, 56], [52, 30, 57], [52, 31, 58], [52, 32, 59], [52, 33, 60], [52, 34, 61], [52, 35, 62], [52, 36, 63], [52, 37, 64], [52, 38, 65], [52, 39, 66], [52, 40, 67], [52, 41, 68], [52, 42, 69], [52, 43, 59], [52, 50, 71], [52, 50, 73], [52, 50, 75], [52, 50, 77], [52, 51, 72], [52, 51, 74], [52, 51, 76], [52, 51, 78], [52, 52, 73], [52, 52, 75], [52, 52, 77], [52, 52, 79], [52, 53, 74], [52, 53, 76], [52, 53, 78], [52, 53, 80], [52, 54, 81], [52, 55, 82], [52, 56, 83], [52, 57, 84], [52, 58, 85], [53, 25, 52], [53, 27, 54], [53, 28, 55], [53, 29, 56], [53, 30, 57], [53, 31, 58], [53, 32, 59], [53, 33, 60], [53, 34, 61], [53, 35, 62], [53, 36, 63], [53, 37, 64], [53, 38, 65], [53, 39, 66], [53, 40, 67], [53, 41, 68], [53, 42, 69], [53, 43, 59], [53, 51, 71], [53, 51, 73], [53, 51, 75], [53, 51, 77], [53, 52, 72], [53, 52, 74], [53, 52, 76], [53, 52, 78], [53, 53, 73], [53, 53, 75], [53, 53, 77], [53, 53, 79], [53, 54, 74], [53, 54, 76], [53, 54, 78], [53, 54, 80], [53, 54, 81], [53, 55, 82], [53, 56, 83], [53, 57, 84], [53, 58, 85], [54, 45, 73], [54, 46, 74], [54, 47, 75], [54, 48, 76], [54, 49, 67], [54, 49, 77], [54, 50, 78], [54, 51, 79], [54, 52, 73], [54, 52, 75], [54, 52, 77], [54, 52, 79], [54, 52, 80], [54, 53, 74], [54, 53, 76], [54, 53, 78], [54, 53, 80], [54, 54, 75], [54, 54, 77], [54, 54, 79], [54, 54, 81], [54, 54, 82], [54, 55, 76], [54, 55, 78], [54, 55, 80], [54, 55, 82], [54, 55, 83], [54, 56, 84], [54, 57, 85], [55, 45, 73], [55, 46, 74], [55, 47, 75], [55, 48, 76], [55, 49, 67], [55, 49, 77], [55, 50, 78], [55, 51, 79], [55, 52, 80], [55, 53, 73], [55, 53, 75], [55, 53, 77], [55, 53, 79], [55, 53, 81], [55, 54, 74], [55, 54, 76], [55, 54, 78], [55, 54, 80], [55, 54, 82], [55, 55, 75], [55, 55, 77], [55, 55, 79], [55, 55, 81], [55, 55, 83], [55, 56, 76], [55, 56, 80], [55, 56, 82], [55, 56, 84], [55, 57, 85], [56, 46, 75], [56, 47, 76], [56, 48, 77], [56, 49, 78], [56, 50, 79], [56, 51, 80], [56, 52, 81], [56, 53, 82], [56, 54, 74], [56, 54, 75], [56, 54, 77], [56, 54, 79], [56, 54, 81], [56, 54, 83], [56, 55, 75], [56, 55, 76], [56, 55, 78], [56, 55, 80], [56, 55, 82], [56, 55, 84], [56, 56, 76], [56, 56, 77], [56, 56, 79], [56, 56, 81], [56, 56, 83], [56, 56, 85], [56, 57, 77], [56, 57, 78], [56, 57, 82], [56, 57, 84], [56, 57, 86], [56, 58, 87], [57, 46, 75], [57, 47, 76], [57, 48, 77], [57, 49, 78], [57, 50, 79], [57, 51, 80], [57, 52, 81], [57, 53, 82], [57, 54, 74], [57, 55, 75], [57, 55, 76], [57, 55, 77], [57, 55, 79], [57, 55, 81], [57, 55, 83], [57, 55, 84], [57, 56, 76], [57, 56, 77], [57, 56, 80], [57, 56, 82], [57, 56, 84], [57, 56, 85], [57, 57, 77], [57, 57, 78], [57, 57, 81], [57, 57, 83], [57, 57, 85], [57, 57, 86], [57, 58, 78], [57, 58, 79], [57, 58, 84], [57, 58, 86], [57, 58, 87], [58, 49, 79], [58, 50, 72], [58, 50, 80], [58, 51, 73], [58, 51, 81], [58, 52, 74], [58, 52, 82], [58, 53, 75], [58, 53, 83], [58, 54, 84], [58, 55, 76], [58, 55, 85], [58, 56, 77], [58, 56, 79], [58, 56, 81], [58, 56, 83], [58, 56, 85], [58, 56, 86], [58, 57, 78], [58, 57, 82], [58, 57, 84], [58, 57, 86], [58, 57, 87], [58, 58, 79], [58, 58, 83], [58, 58, 85], [58, 58, 87], [58, 58, 88], [58, 59, 80], [58, 59, 86], [58, 59, 88], [58, 59, 89], [58, 60, 90], [59, 49, 79], [59, 50, 72], [59, 50, 80], [59, 51, 73], [59, 51, 74], [59, 51, 81], [59, 52, 74], [59, 52, 75], [59, 52, 82], [59, 53, 75], [59, 53, 76], [59, 53, 83], [59, 54, 77], [59, 54, 84], [59, 55, 85], [59, 56, 86], [59, 57, 77], [59, 57, 81], [59, 57, 83], [59, 57, 85], [59, 57, 87], [59, 58, 78], [59, 58, 84], [59, 58, 86], [59, 58, 88], [59, 59, 79], [59, 59, 85], [59, 59, 87], [59, 59, 89], [59, 60, 90], [60, 50, 81], [60, 51, 74], [60, 51, 82], [60, 52, 75], [60, 52, 76], [60, 52, 83], [60, 53, 76], [60, 53, 77], [60, 53, 84], [60, 54, 77], [60, 54, 78], [60, 54, 85], [60, 55, 79], [60, 55, 86], [60, 56, 87], [60, 57, 88], [60, 58, 79], [60, 58, 83], [60, 58, 85], [60, 58, 87], [60, 58, 89], [60, 59, 80], [60, 59, 86], [60, 59, 88], [60, 59, 90], [60, 60, 81], [60, 60, 87], [60, 60, 89], [60, 60, 91], [60, 61, 92], [61, 50, 81], [61, 51, 82], [61, 52, 76], [61, 52, 83], [61, 53, 77], [61, 53, 78], [61, 53, 84], [61, 54, 78], [61, 54, 79], [61, 54, 85], [61, 55, 79], [61, 55, 80], [61, 55, 86], [61, 56, 81], [61, 56, 87], [61, 57, 88], [61, 58, 89], [61, 59, 79], [61, 59, 85], [61, 59, 87], [61, 59, 89], [61, 59, 90], [61, 60, 90], [61, 60, 91], [61, 61, 91], [61, 61, 92], [61, 62, 92], [62, 27, 53], [62, 28, 54], [62, 29, 55], [62, 30, 56], [62, 31, 57], [62, 32, 58], [62, 33, 59], [62, 34, 60], [62, 35, 61], [62, 36, 62], [62, 37, 63], [62, 38, 64], [62, 39, 65], [62, 40, 66], [62, 53, 78], [62, 53, 79], [62, 54, 79], [62, 54, 80], [62, 55, 80], [62, 55, 81], [62, 56, 81], [62, 56, 82], [62, 57, 83], [62, 60, 81], [62, 60, 87], [62, 60, 89], [62, 60, 91], [62, 61, 92], [62, 61, 93], [62, 62, 93], [62, 63, 94], [63, 25, 52], [63, 27, 53], [63, 27, 54], [63, 28, 54], [63, 28, 55], [63, 29, 55], [63, 29, 56], [63, 30, 56], [63, 30, 57], [63, 31, 57], [63, 31, 58], [63, 32, 58], [63, 32, 59], [63, 33, 59], [63, 33, 60], [63, 34, 60], [63, 34, 61], [63, 35, 61], [63, 35, 62], [63, 36, 62], [63, 36, 63], [63, 37, 63], [63, 37, 64], [63, 38, 64], [63, 38, 65], [63, 39, 65], [63, 39, 66], [63, 40, 66], [63, 40, 67], [63, 41, 68], [63, 42, 69], [63, 53, 79], [63, 54, 80], [63, 54, 81], [63, 55, 81], [63, 55, 82], [63, 56, 82], [63, 56, 83], [63, 57, 83], [63, 57, 84], [63, 58, 85], [63, 61, 91], [63, 61, 93], [63, 62, 92], [63, 62, 94], [63, 63, 93], [63, 63, 95], [63, 64, 96], [64, 25, 52], [64, 27, 54], [64, 28, 55], [64, 29, 56], [64, 30, 57], [64, 31, 58], [64, 32, 59], [64, 33, 60], [64, 34, 61], [64, 35, 62], [64, 36, 63], [64, 37, 64], [64, 38, 65], [64, 39, 66], [64, 40, 67], [64, 41, 68], [64, 42, 69], [64, 45, 73], [64, 46, 74], [64, 47, 75], [64, 48, 76], [64, 49, 77], [64, 50, 78], [64, 51, 79], [64, 52, 80], [64, 54, 81], [64, 54, 82], [64, 55, 82], [64, 55, 83], [64, 56, 83], [64, 56, 84], [64, 57, 84], [64, 57, 85], [64, 58, 85], [64, 62, 93], [64, 62, 95], [64, 63, 94], [64, 63, 96], [64, 64, 95], [64, 64, 97], [64, 65, 98], [65, 45, 73], [65, 46, 74], [65, 46, 75], [65, 47, 75], [65, 47, 76], [65, 48, 76], [65, 48, 77], [65, 49, 77], [65, 49, 78], [65, 50, 78], [65, 50, 79], [65, 51, 79], [65, 51, 80], [65, 52, 80], [65, 52, 81], [65, 53, 82], [65, 54, 82], [65, 55, 83], [65, 55, 84], [65, 56, 84], [65, 56, 85], [65, 57, 85], [65, 57, 86], [65, 58, 87], [65, 62, 95], [65, 63, 93], [65, 63, 95], [65, 64, 96], [66, 46, 75], [66, 47, 76], [66, 48, 77], [66, 49, 78], [66, 49, 79], [66, 50, 79], [66, 50, 80], [66, 51, 80], [66, 51, 81], [66, 52, 81], [66, 52, 82], [66, 53, 82], [66, 53, 83], [66, 54, 84], [66, 55, 84], [66, 55, 85], [66, 56, 85], [66, 56, 86], [66, 57, 86], [66, 57, 87], [66, 58, 87], [66, 58, 88], [66, 59, 89], [66, 60, 90], [66, 64, 95], [66, 64, 97], [66, 65, 98], [67, 49, 79], [67, 50, 80], [67, 50, 81], [67, 51, 81], [67, 51, 82], [67, 52, 82], [67, 52, 83], [67, 53, 83], [67, 53, 84], [67, 54, 84], [67, 54, 85], [67, 55, 85], [67, 55, 86], [67, 56, 86], [67, 56, 87], [67, 57, 87], [67, 57, 88], [67, 58, 88], [67, 58, 89], [67, 59, 89], [67, 59, 90], [67, 60, 90], [67, 60, 91], [67, 61, 92], [67, 65, 99], [68, 50, 81], [68, 51, 82], [68, 52, 83], [68, 53, 84], [68, 54, 85], [68, 55, 86], [68, 56, 87], [68, 57, 88], [68, 58, 89], [68, 59, 90], [68, 60, 91], [68, 61, 92], [68, 61, 93], [68, 66, 101], [69, 61, 93], [69, 62, 95], [70, 62, 95]]"

def main():
    out = []
    out.append({'section': 'engine_gate', 'engine_sha': sha, 'pin': PIN,
                'gate': 'PASS'})
    vC = ns['vC']
    vO = ns['vO']

    anchor_spec = [
        # ---- 29 kit-6 separation spots, first re-anchored here ----
        (72, (19, 34), 52, 1, 'kit-6 (76c461da) kit5 S5 item1 one past of d7 death of d6 -- one-past-of-d=7 separation (death-of-d=6: {19,32} conform-DEAD)'),
        (73, (19, 34), 53, 1, 'kit-6 (76c461da) kit5 S5 item2 birth slice d8 -- d=8 birth slice'),
        (73, (19, 36), 53, 2, 'kit-6 (76c461da) kit5 S5 item2 birth slice d8 -- d=8 birth slice'),
        (74, (20, 34), 53, 0, 'kit-6 (76c461da) kit5 S5 item3 one past of d7 death of d6 -- one-past-of-d=7 separation (death-of-d=6)'),
        (75, (20, 34), 54, 0, 'kit-6 (76c461da) kit5 S5 item4 birth slice d8 -- d=8 birth slice'),
        (75, (20, 36), 54, 2, 'kit-6 (76c461da) kit5 S5 item4 birth slice d8 -- d=8 birth slice'),
        (70, (21, 28), 48, 1, 'kit-6 (76c461da) kit5 S5 item5 one past of d3 death of d2 -- one-past-of-d=3 separation (first m=21 d=2 death row)'),
        (71, (21, 28), 49, 1, 'kit-6 (76c461da) kit5 S5 item6 birth slice d4 -- d=4 birth slice'),
        (71, (21, 30), 49, 2, 'kit-6 (76c461da) kit5 S5 item6 birth slice d4 -- d=4 birth slice'),
        (72, (22, 28), 49, 0, 'kit-6 (76c461da) kit5 S5 item7 one past of d3 death of d2 -- one-past-of-d=3 separation (first m=22 d=2 death row)'),
        (73, (22, 28), 50, 0, 'kit-6 (76c461da) kit5 S5 item8 birth slice d4 -- d=4 birth slice'),
        (73, (22, 30), 50, 2, 'kit-6 (76c461da) kit5 S5 item8 birth slice d4 -- d=4 birth slice'),
        (74, (23, 28), 50, 1, 'kit-6 (76c461da) kit5 S5 item9 one past of d2 death of d1 -- one-past-of-d=2 separation (first m=23 d=1 death row)'),
        (75, (23, 28), 51, 1, 'kit-6 (76c461da) kit5 S5 item10 birth slice d3 -- d=2 birth slice'),
        (75, (23, 30), 51, 2, 'kit-6 (76c461da) kit5 S5 item10 birth slice d3 -- d=2 birth slice'),
        (76, (24, 28), 51, 0, 'kit-6 (76c461da) kit5 S5 item11 one past of d2 death of d1 -- one-past-of-d=2 separation (first m=24 d=1 death row)'),
        (77, (24, 28), 52, 0, 'kit-6 (76c461da) kit5 S5 item12 birth slice d3 -- d=3 birth slice'),
        (77, (24, 30), 52, 2, 'kit-6 (76c461da) kit5 S5 item12 birth slice d3 -- d=3 birth slice'),
        (81, (27, 28), 53, 2, 'kit-6 (76c461da) frontier record m27 z53 K1268 15th datum candidate -- FRONTIER separation (the 15th parity datum, FIRST-EVER m=27 row)'),
        (83, (28, 28), 54, 2, 'kit-6 (76c461da) frontier record m28 z54 K1268 16th datum candidate -- FRONTIER separation (the 16th parity datum, FIRST-EVER m=28 row)'),
        (76, (25, 26), 50, 1, 'kit-6 (76c461da) kit5 S5 item13 one past of the d0 seat -- one-past-of-d=0 decay separation (2->1)'),
        (77, (25, 26), 51, 1, 'kit-6 (76c461da) kit5 S5 item14 birth slice d1 stick coincides -- d=1 birth slice (stick seat coincides z=S(d0))'),
        (77, (25, 28), 51, 2, 'kit-6 (76c461da) kit5 S5 item14 birth slice d1 stick coincides -- d=1 birth slice (stick seat coincides z=S(d0))'),
        (78, (25, 28), 52, 1, 'kit-6 (76c461da) kit5 S5 item15 one past of d1 death of d0 first m25 death -- one-past-of-d=1 separation (THE FIRST m=25 death datum, d=0)'),
        (78, (26, 26), 51, 0, 'kit-6 (76c461da) kit5 S5 item16 one past of the d0 seat -- one-past-of-d=0 decay separation (2->0)'),
        (79, (26, 26), 52, 0, 'kit-6 (76c461da) kit5 S5 item17 birth slice d1 stick coincides -- d=1 birth slice (stick seat coincides z=S(d0))'),
        (79, (26, 28), 52, 2, 'kit-6 (76c461da) kit5 S5 item17 birth slice d1 stick coincides -- d=1 birth slice (stick seat coincides z=S(d0))'),
        (80, (26, 28), 53, 0, 'kit-6 (76c461da) kit5 S5 item18 one past of d1 death of d0 first m26 death -- one-past-of-d=1 separation (THE FIRST m=26 death datum, d=0)'),
        (77, (26, 26), 50, 2, 'kit-6 (76c461da) frontier recheck m26 z50 published 14th datum blind reverification -- blind re-verification of the kit-5 published 14th frontier datum'),
        (46, (17, 18), 28, 0, 'lifecycle kit z=28 handoff h1'),
        (45, (16, 17), 28, 1, 'lifecycle kit z=28 handoff h2'),
        (47, (18, 18), 28, 1, 'lifecycle kit z=28 handoff h3'),
        (46, (17, 17), 28, 0, 'lifecycle kit z=28 handoff h4'),
        (47, (17, 18), 29, 0, 'decay kit z=29 touch u1'),
        (46, (16, 17), 29, 1, 'decay kit z=29 touch u2'),
        (48, (18, 18), 29, 1, 'decay kit z=29 touch u3'),
        (47, (17, 17), 29, 0, 'decay kit z=29 touch u4'),
        (48, (17, 18), 30, 0, 'wavetrain kit z=30 touch w1'),
        (47, (16, 17), 30, 1, 'wavetrain kit z=30 touch w2'),
        (49, (18, 18), 30, 1, 'wavetrain kit z=30 touch w3'),
        (48, (17, 17), 30, 0, 'wavetrain kit z=30 touch w4'),
        (49, (17, 18), 31, 0, 'fifthwave kit z=31 touch x1'),
        (48, (16, 17), 31, 1, 'fifthwave kit z=31 touch y1'),
        (50, (18, 18), 31, 1, 'fifthwave kit z=31 touch x3'),
        (49, (17, 17), 31, 0, 'fifthwave kit z=31 touch x4'),
        (50, (17, 18), 32, 0, 'sixthwave kit z=32 touch x1'),
        (49, (16, 17), 32, 1, 'sixthwave kit z=32 touch y1'),
        (51, (18, 18), 32, 1, 'sixthwave kit z=32 touch x3'),
        (50, (17, 17), 32, 0, 'sixthwave kit z=32 touch x4'),
        (45, (15, 16), 29, 2, 'frontier m=15@z=29 separation (lifecycle kit + d49b480a blind replication)'),
        (47, (16, 16), 30, 2, 'frontier m=16@z=30 separation (lifecycle kit + d49b480a)'),
        (46, (15, 16), 30, 1, 'one-past m=15@z=30 separation (lifecycle kit + d49b480a)'),
        (48, (16, 16), 31, 0, 'one-past m=16@z=31 separation (lifecycle kit + d49b480a)'),
        (41, (13, 14), 27, 1, 'two-past m=13@z=27 stick separation (d49b480a)'),
        (41, (13, 16), 27, 2, 'two-past m=13@z=27 d=1 birth separation (d49b480a)'),
        (53, (17, 18), 35, 1, 'two-past m=17@z=35 stick separation (fifthwave kit)'),
        (53, (17, 20), 35, 2, 'two-past m=17@z=35 d=1 birth separation (fifthwave kit)'),
        (47, (13, 20), 33, 1, 'm=13@z=33 stick separation (fifthwave kit)'),
        (47, (13, 22), 33, 2, 'm=13@z=33 d=4 birth separation (fifthwave kit)'),
        (57, (19, 20), 37, 2, 'kit-1 (6057ed51) frontier m=19@z=37 d=0 birth separation UP 2v0'),
        (58, (19, 20), 38, 1, 'kit-1 (6057ed51) one-past m=19@z=38 separation UP 1v0 (odd decay 2->1)'),
        (59, (19, 20), 39, 1, 'kit-1 (6057ed51) two-past m=19@z=39 stick separation DOWN 1v2'),
        (59, (19, 22), 39, 2, 'kit-1 (6057ed51) two-past m=19@z=39 d=1 birth separation UP 2v0'),
        (59, (20, 20), 38, 2, 'kit-1 (6057ed51) frontier m=20@z=38 d=0 birth separation UP 2v1'),
        (60, (20, 20), 39, 0, 'kit-1 (6057ed51) one-past m=20@z=39 separation DOWN 0v1 (even decay 2->0)'),
        (61, (20, 20), 40, 0, 'kit-1 (6057ed51) two-past m=20@z=40 stick separation DOWN 0v2'),
        (61, (20, 22), 40, 2, 'kit-1 (6057ed51) two-past m=20@z=40 d=1 birth separation UP 2v1'),
        (45, (19, 19), 25, 0, 'z25-min20 kit base spot H(45;(19,19);25)=0 published CONFORM'),
        (46, (19, 19), 26, 0, 'z26-floor20 kit base spot H(46;(19,19);26)=0 published CONFORM'),
        (60, (19, 22), 40, 1, 'kit-2 (637d15e1) ladder m=19@z=40 one-past-of-d=1 separation UP 1v0'),
        (61, (19, 22), 41, 1, 'kit-2 (637d15e1) ladder m=19@z=41 stick separation DOWN 1v2'),
        (61, (19, 24), 41, 2, 'kit-2 (637d15e1) ladder m=19@z=41 d=2 birth separation UP 2v0'),
        (62, (19, 24), 42, 1, 'kit-2 (637d15e1) ladder m=19@z=42 one-past-of-d=2 separation UP 1v0'),
        (63, (19, 24), 43, 1, 'kit-2 (637d15e1) ladder m=19@z=43 stick separation DOWN 1v2'),
        (63, (19, 26), 43, 2, 'kit-2 (637d15e1) ladder m=19@z=43 d=3 birth separation UP 2v0'),
        (62, (20, 22), 41, 0, 'kit-2 (637d15e1) ladder m=20@z=41 one-past-of-d=1 separation DOWN 0v1'),
        (63, (20, 22), 42, 0, 'kit-2 (637d15e1) ladder m=20@z=42 stick separation DOWN 0v2'),
        (63, (20, 24), 42, 2, 'kit-2 (637d15e1) ladder m=20@z=42 d=2 birth separation UP 2v1'),
        (64, (20, 24), 43, 0, 'kit-2 (637d15e1) ladder m=20@z=43 one-past-of-d=2 separation DOWN 0v1'),
        (65, (20, 24), 44, 0, 'kit-2 (637d15e1) ladder m=20@z=44 stick separation DOWN 0v2'),
        (65, (20, 26), 44, 2, 'kit-2 (637d15e1) ladder m=20@z=44 d=3 birth separation UP 2v1'),
        (64, (19, 26), 44, 1, 'kit-3 (6554de44) ladder m=19@z=44 one-past-of-d=3 separation UP 1v0'),
        (65, (19, 26), 45, 1, 'kit-3 (6554de44) ladder m=19@z=45 stick separation DOWN 1v2'),
        (65, (19, 28), 45, 2, 'kit-3 (6554de44) ladder m=19@z=45 d=4 birth separation UP 2v0 seat gap 9'),
        (66, (19, 28), 46, 1, 'kit-3 (6554de44) ladder m=19@z=46 one-past-of-d=4 separation UP 1v0'),
        (67, (19, 28), 47, 1, 'kit-3 (6554de44) ladder m=19@z=47 stick separation DOWN 1v2'),
        (67, (19, 30), 47, 2, 'kit-3 (6554de44) ladder m=19@z=47 d=5 birth separation UP 2v0 seat gap 11'),
        (66, (20, 26), 45, 0, 'kit-3 (6554de44) ladder m=20@z=45 one-past-of-d=3 separation DOWN 0v1'),
        (67, (20, 26), 46, 0, 'kit-3 (6554de44) ladder m=20@z=46 stick separation DOWN 0v2'),
        (67, (20, 28), 46, 2, 'kit-3 (6554de44) ladder m=20@z=46 d=4 birth separation UP 2v1 seat gap 8'),
        (68, (20, 28), 47, 0, 'kit-3 (6554de44) ladder m=20@z=47 one-past-of-d=4 separation DOWN 0v1'),
        (69, (20, 28), 48, 0, 'kit-3 (6554de44) ladder m=20@z=48 stick separation DOWN 0v2'),
        (69, (20, 30), 48, 2, 'kit-3 (6554de44) ladder m=20@z=48 d=5 birth separation UP 2v1 seat gap 10'),
        (63, (21, 22), 41, 2, 'kit-3 (6554de44) frontier m=21@z=41 d=0 birth separation UP 2v0'),
        (64, (21, 22), 42, 1, 'kit-3 (6554de44) one-past m=21@z=42 separation UP 1v0 (odd decay 2->1)'),
        (65, (21, 22), 43, 1, 'kit-3 (6554de44) two-past m=21@z=43 stick separation DOWN 1v2'),
        (65, (21, 24), 43, 2, 'kit-3 (6554de44) two-past m=21@z=43 d=1 birth separation UP 2v0 seat gap 3'),
        (65, (22, 22), 42, 2, 'kit-3 (6554de44) frontier m=22@z=42 d=0 birth separation UP 2v1'),
        (66, (22, 22), 43, 0, 'kit-3 (6554de44) one-past m=22@z=43 separation DOWN 0v1 (even decay 2->0)'),
        (67, (22, 22), 44, 0, 'kit-3 (6554de44) two-past m=22@z=44 stick separation DOWN 0v2'),
        (67, (22, 24), 44, 2, 'kit-3 (6554de44) two-past m=22@z=44 d=1 birth separation UP 2v1 seat gap 2'),
        (68, (19, 30), 48, 1, 'kit-4 (fe0a2d01) ladder m=19@z=48 one-past-of-d=5 separation UP 1v0'),
        (69, (19, 30), 49, 1, 'kit-4 (fe0a2d01) stick m=19@z=49 separation DOWN 1v2'),
        (69, (19, 32), 49, 2, 'kit-4 (fe0a2d01) birth m=19@z=49 d=6 separation UP 2v0 seat gap 13'),
        (70, (20, 30), 49, 0, 'kit-4 (fe0a2d01) one-past m=20@z=49 separation DOWN 0v1'),
        (71, (20, 30), 50, 0, 'kit-4 (fe0a2d01) stick m=20@z=50 separation DOWN 0v2'),
        (71, (20, 32), 50, 2, 'kit-4 (fe0a2d01) birth m=20@z=50 d=6 separation UP 2v1 seat gap 12'),
        (66, (21, 24), 44, 1, 'kit-4 (fe0a2d01) one-past m=21@z=44 separation UP 1v0 (first m=21 death row: {21,22} conform-DEAD)'),
        (67, (21, 24), 45, 1, 'kit-4 (fe0a2d01) stick m=21@z=45 separation DOWN 1v2'),
        (67, (21, 26), 45, 2, 'kit-4 (fe0a2d01) birth m=21@z=45 d=2 separation UP 2v0 seat gap 5'),
        (68, (22, 24), 45, 0, 'kit-4 (fe0a2d01) one-past m=22@z=45 separation DOWN 0v1 (first m=22 death row: (22,22) conform-DEAD at z=45=S+1)'),
        (69, (22, 24), 46, 0, 'kit-4 (fe0a2d01) stick m=22@z=46 separation DOWN 0v2'),
        (69, (22, 26), 46, 2, 'kit-4 (fe0a2d01) birth m=22@z=46 d=2 separation UP 2v1 seat gap 4'),
        (69, (23, 24), 45, 2, 'kit-4 (fe0a2d01) frontier m=23@z=45 separation UP 2v0 (the 11th datum, corrected registration)'),
        (70, (23, 24), 46, 1, 'kit-4 (fe0a2d01) one-past m=23@z=46 separation UP 1v0'),
        (71, (23, 24), 47, 1, 'kit-4 (fe0a2d01) stick m=23@z=47 separation DOWN 1v2'),
        (71, (23, 26), 47, 2, 'kit-4 (fe0a2d01) birth m=23@z=47 d=1 separation UP 2v0 seat gap 3'),
        (71, (24, 24), 46, 2, 'kit-4 (fe0a2d01) frontier m=24@z=46 separation UP 2v1 (the 12th datum)'),
        (72, (24, 24), 47, 0, 'kit-4 (fe0a2d01) one-past m=24@z=47 separation DOWN 0v1'),
        (73, (24, 24), 48, 0, 'kit-4 (fe0a2d01) stick m=24@z=48 separation DOWN 0v2'),
        (73, (24, 26), 48, 2, 'kit-4 (fe0a2d01) birth m=24@z=48 d=1 separation UP 2v1 seat gap 2'),
        (74, (24, 26), 49, 0, 'kit-4 (fe0a2d01) one-past-of-d=1 m=24@z=49 separation DOWN 0v1 (first m=24 death row: (24,24) conform-DEAD at z=49=S+1)'),
        (70, (19, 32), 50, 1, 'kit-5 (d52f2be7) ladder m=19@z=50 one-past-of-d=6 separation UP 1v0 (first m=19 d=5 death row: {19,30} conform-DEAD)'),
        (71, (19, 32), 51, 1, 'kit-5 (d52f2be7) stick m=19@z=51 separation DOWN 1v2'),
        (71, (19, 34), 51, 2, 'kit-5 (d52f2be7) birth m=19@z=51 d=7 separation UP 2v0 seat gap 15 (m=19 ladder COMPLETE d=7)'),
        (72, (20, 32), 51, 0, 'kit-5 (d52f2be7) ladder m=20@z=51 one-past-of-d=6 separation DOWN 0v1 ((20,30) conform-DEAD, first m=20 d=5 death row)'),
        (73, (20, 32), 52, 0, 'kit-5 (d52f2be7) stick m=20@z=52 separation DOWN 0v2'),
        (73, (20, 34), 52, 2, 'kit-5 (d52f2be7) birth m=20@z=52 d=7 separation UP 2v1 seat gap 14 (m=20 ladder COMPLETE d=7)'),
        (68, (21, 26), 46, 1, 'kit-5 (d52f2be7) ladder m=21@z=46 one-past-of-d=2 separation UP 1v0 ({21,24} conform-DEAD, first m=21 d=1 death row)'),
        (69, (21, 26), 47, 1, 'kit-5 (d52f2be7) stick m=21@z=47 separation DOWN 1v2'),
        (69, (21, 28), 47, 2, 'kit-5 (d52f2be7) birth m=21@z=47 d=3 separation UP 2v0 seat gap 7'),
        (70, (22, 26), 47, 0, 'kit-5 (d52f2be7) ladder m=22@z=47 one-past-of-d=2 separation DOWN 0v1 ((22,24) conform-DEAD, first m=22 d=1 death row)'),
        (71, (22, 26), 48, 0, 'kit-5 (d52f2be7) stick m=22@z=48 separation DOWN 0v2'),
        (71, (22, 28), 48, 2, 'kit-5 (d52f2be7) birth m=22@z=48 d=3 separation UP 2v1 seat gap 6'),
        (72, (23, 26), 48, 1, 'kit-5 (d52f2be7) ladder m=23@z=48 one-past-of-d=1 separation UP 1v0 (THE FIRST m=23 death datum: {23,24} conform-DEAD)'),
        (73, (23, 26), 49, 1, 'kit-5 (d52f2be7) stick m=23@z=49 separation DOWN 1v2'),
        (73, (23, 28), 49, 2, 'kit-5 (d52f2be7) birth m=23@z=49 d=2 separation UP 2v0 seat gap 5'),
        (75, (24, 26), 50, 0, 'kit-5 (d52f2be7) stick m=24@z=50 separation DOWN 0v2 (stick seat coincides S(d1)=50=z)'),
        (75, (24, 28), 50, 2, 'kit-5 (d52f2be7) birth m=24@z=50 d=2 separation UP 2v1 seat gap 4'),
        (75, (25, 26), 49, 2, 'kit-5 (d52f2be7) frontier m=25@z=49 separation UP 2v0 (the 13th datum, first-ever m=25 row)'),
        (77, (26, 26), 50, 2, 'kit-5 (d52f2be7) frontier m=26@z=50 separation UP 2v1 (the 14th datum, first-ever m=26 row)'),
        (74, (36, 19), 54, 1, 'kit-7 (a62c5d2e) frozen section (d) item 1 m=19 z=54  -- seat separation [19, 36] 1 v 0 (S=55) UP'),
        (75, (36, 19), 55, 1, 'kit-7 (a62c5d2e) frozen section (d) item 2 m=19 z=55  -- seat separation [19, 36] 1 v 2 (S=55) DOWN'),
        (75, (19, 19, 19), 55, 2, 'kit-7 (a62c5d2e) STACKED-TRIO SHADOW SEAT datum {19,19,19}@S=57 UP 2v0 (the kit series FIRST registered-candidate deviation, unregistered third separation at the m=19 z=55 d=9 birth slice)'),
        (75, (38, 19), 55, 2, 'kit-7 (a62c5d2e) frozen section (d) item 2 m=19 z=55  -- seat separation [19, 38] 2 v 0 (S=57) UP'),
        (76, (36, 20), 55, 0, 'kit-7 (a62c5d2e) frozen section (d) item 3 m=20 z=55  -- seat separation [20, 36] 0 v 1 (S=56) DOWN'),
        (77, (36, 20), 56, 0, 'kit-7 (a62c5d2e) frozen section (d) item 4 m=20 z=56  -- seat separation [20, 36] 0 v 2 (S=56) DOWN'),
        (77, (38, 20), 56, 2, 'kit-7 (a62c5d2e) frozen section (d) item 4 m=20 z=56  -- seat separation [20, 38] 2 v 1 (S=58) UP'),
        (72, (30, 21), 50, 1, 'kit-7 (a62c5d2e) frozen section (d) item 5 m=21 z=50  -- seat separation [21, 30] 1 v 0 (S=51) UP'),
        (73, (30, 21), 51, 1, 'kit-7 (a62c5d2e) frozen section (d) item 6 m=21 z=51  -- seat separation [21, 30] 1 v 2 (S=51) DOWN'),
        (73, (32, 21), 51, 2, 'kit-7 (a62c5d2e) frozen section (d) item 6 m=21 z=51  -- seat separation [21, 32] 2 v 0 (S=53) UP'),
        (74, (30, 22), 51, 0, 'kit-7 (a62c5d2e) frozen section (d) item 7 m=22 z=51  -- seat separation [22, 30] 0 v 1 (S=52) DOWN'),
        (75, (30, 22), 52, 0, 'kit-7 (a62c5d2e) frozen section (d) item 8 m=22 z=52  -- seat separation [22, 30] 0 v 2 (S=52) DOWN'),
        (75, (32, 22), 52, 2, 'kit-7 (a62c5d2e) frozen section (d) item 8 m=22 z=52  -- seat separation [22, 32] 2 v 1 (S=54) UP'),
        (76, (30, 23), 52, 1, 'kit-7 (a62c5d2e) frozen section (d) item 9 m=23 z=52  -- seat separation [23, 30] 1 v 0 (S=53) UP'),
        (77, (30, 23), 53, 1, 'kit-7 (a62c5d2e) frozen section (d) item 10 m=23 z=53  -- seat separation [23, 30] 1 v 2 (S=53) DOWN'),
        (77, (32, 23), 53, 2, 'kit-7 (a62c5d2e) frozen section (d) item 10 m=23 z=53  -- seat separation [23, 32] 2 v 0 (S=55) UP'),
        (78, (30, 24), 53, 0, 'kit-7 (a62c5d2e) frozen section (d) item 11 m=24 z=53  -- seat separation [24, 30] 0 v 1 (S=54) DOWN'),
        (79, (30, 24), 54, 0, 'kit-7 (a62c5d2e) frozen section (d) item 12 m=24 z=54  -- seat separation [24, 30] 0 v 2 (S=54) DOWN'),
        (79, (32, 24), 54, 2, 'kit-7 (a62c5d2e) frozen section (d) item 12 m=24 z=54  -- seat separation [24, 32] 2 v 1 (S=56) UP'),
        (79, (28, 25), 53, 1, 'kit-7 (a62c5d2e) frozen section (d) item 13 m=25 z=53  -- seat separation [25, 28] 1 v 2 (S=53) DOWN'),
        (79, (30, 25), 53, 2, 'kit-7 (a62c5d2e) frozen section (d) item 13 m=25 z=53  -- seat separation [25, 30] 2 v 0 (S=55) UP'),
        (80, (30, 25), 54, 1, 'kit-7 (a62c5d2e) frozen section (d) item 14 m=25 z=54  -- seat separation [25, 30] 1 v 0 (S=55) UP'),
        (81, (30, 25), 55, 1, 'kit-7 (a62c5d2e) frozen section (d) item 15 m=25 z=55  -- seat separation [25, 30] 1 v 2 (S=55) DOWN'),
        (81, (32, 25), 55, 2, 'kit-7 (a62c5d2e) frozen section (d) item 15 m=25 z=55  -- seat separation [25, 32] 2 v 0 (S=57) UP'),
        (81, (28, 26), 54, 0, 'kit-7 (a62c5d2e) frozen section (d) item 16 m=26 z=54  -- seat separation [26, 28] 0 v 2 (S=54) DOWN'),
        (81, (30, 26), 54, 2, 'kit-7 (a62c5d2e) frozen section (d) item 16 m=26 z=54  -- seat separation [26, 30] 2 v 1 (S=56) UP'),
        (82, (30, 26), 55, 0, 'kit-7 (a62c5d2e) frozen section (d) item 17 m=26 z=55  -- seat separation [26, 30] 0 v 1 (S=56) DOWN'),
        (83, (30, 26), 56, 0, 'kit-7 (a62c5d2e) frozen section (d) item 18 m=26 z=56  -- seat separation [26, 30] 0 v 2 (S=56) DOWN'),
        (83, (32, 26), 56, 2, 'kit-7 (a62c5d2e) frozen section (d) item 18 m=26 z=56  -- seat separation [26, 32] 2 v 1 (S=58) UP'),
        (82, (28, 27), 54, 1, 'kit-7 (a62c5d2e) frozen section (d) item 19 m=27 z=54  -- seat separation [27, 28] 1 v 0 (S=55) UP'),
        (83, (28, 27), 55, 1, 'kit-7 (a62c5d2e) frozen section (d) item 20 m=27 z=55  -- seat separation [27, 28] 1 v 2 (S=55) DOWN'),
        (83, (30, 27), 55, 2, 'kit-7 (a62c5d2e) frozen section (d) item 20 m=27 z=55  -- seat separation [27, 30] 2 v 0 (S=57) UP'),
        (84, (30, 27), 56, 1, 'kit-7 (a62c5d2e) frozen section (d) item 21 m=27 z=56 one-past-of-d=1 / death-of-d=0 -- seat separation [27, 30] 1 v 0 (S=57) UP'),
        (84, (28, 28), 55, 0, 'kit-7 (a62c5d2e) frozen section (d) item 22 m=28 z=55  -- seat separation [28, 28] 0 v 1 (S=56) DOWN'),
        (85, (28, 28), 56, 0, 'kit-7 (a62c5d2e) frozen section (d) item 23 m=28 z=56  -- seat separation [28, 28] 0 v 2 (S=56) DOWN'),
        (85, (30, 28), 56, 2, 'kit-7 (a62c5d2e) frozen section (d) item 23 m=28 z=56  -- seat separation [28, 30] 2 v 1 (S=58) UP'),
        (86, (30, 28), 57, 0, 'kit-7 (a62c5d2e) frozen section (d) item 24 m=28 z=57 one-past-of-d=1 / death-of-d=0 -- seat separation [28, 30] 0 v 1 (S=58) DOWN'),
        (87, (30, 29), 57, 2, 'kit-7 (a62c5d2e) frontier m=29@z=57 separation (the 17th parity datum, FIRST-EVER m=29 row)'),
        (89, (30, 30), 58, 2, 'kit-7 (a62c5d2e) frontier m=30@z=58 separation (the 18th parity datum, FIRST-EVER m=30 row)'),
    ]
    # (a) K0832 battery: the UNION of the kit-7 737 literal triples
    #     (sorted-unique layout; property checked unchanged) plus the
    #     kit-8 literals below (stair rows, candidate literals, new
    #     anchor collapses, kit-9 future constants).
    battery_lits = json.loads(BATTERY_TRIPLES_JSON)
    battery = []
    bad_bat = 0
    for (x, z2, R2) in battery_lits:
        cf = v(x, z2, R2)
        cn = vC(x, z2, R2)
        od = vO(x, z2, R2)
        ok = (cf == cn == od)
        if not ok:
            bad_bat += 1
        battery.append({'x': x, 'z': z2, 'R': R2, 'closed': cf,
                        'vC': cn, 'vO': od, 'match': ok})
    out.append({'section': 'k0832_battery', 'literals': len(battery),
                'all_match': bad_bat == 0, 'bad': bad_bat,
                'rows': battery})

    # (b) the 28 binding candidate rows (kit-7 frozen section (d),
    #     verbatim; machine-regenerated byte-identical at this build).
    K8_BINDING = json.loads(K8_BINDING_JSON)

    def emit_k8_row(r):
        m = r['m']
        z = r['z']
        R = m + z + 1
        smax = max(m + 38, z + 2)
        extra = {'co_token_%d_allowed' % m: True,
                 's_domain': '{%d..%d}' % (m, smax), 'arity_max': 3,
                 'style': 'x0 published residual-band style',
                 'registered_by': r['provenance'],
                 'candidate': r['cand'],
                 'seat_kind': r['kind']}
        for tr in r.get('tracker', []):
            extra['trio_tracker_%s' % tr['z']] = tr['cand']
        secname = r['secname']
        return row_record_x0(secname, r['label'], extra, R, z, m, m, smax)

    def triref(item):
        return item

    for r in K8_BINDING:
        m = r['m']
        z = r['z']
        if r.get('frontier'):
            r['secname'] = 'frontier_m%d_z%d_row_record' % (m, z)
            r['label'] = ('registered_frontier_record_m%d_z%d_K1268_%s_datum_candidate'
                          % (m, z, r['nth']))
        else:
            r['secname'] = 'ladder_m%d_z%d_row_record' % (m, z)
            r['label'] = 'registered_kit7_S5_item%d_%s' % (r['item'], r['kind'])
        prov = ('kit-7 frozen output section (d) item %d (commit a62c5d2e)' % r['item'])
        if r['m'] == 19 and r['z'] in (56, 57):
            prov += '; kit-7 log S5 item 10 trio-tracker (NON-BINDING, tracked beside the binding seats)'
        r['provenance'] = prov
        out.append(emit_k8_row(r))

    # (b2) the m=26 z=25 HOLE ROW (kit-7 log S5 item 11)
    out.append(row_record_x0(
        'hole_m26_z25_row_record',
        'm26_z25_hole_row_first_measurement',
        {'co_token_26_allowed': True,
         's_domain': '{26..64}', 'arity_max': 3,
         'style': 'x0 published residual-band style',
         'registered_by': 'kit-7 log S5 item 11 (commit a62c5d2e): the kit-7 S6 item-3 dated correction found the single unmeasured slice z=25 of the m=26 line; register-before-measure satisfied by this freeze',
         'candidate': '0 separations (registered candidate); if clean this closes the m=26 measured line to z in {25..56}',
         'band': 'm=26 measured-line bookkeeping: z in {26..56} measured by kit-6/kit-7 chain + this z=25 row; the published z=25 floor strip covered m in {20..25} only'},
        26 + 25 + 1, 25, 26, 26, 64))

    # (b3) the TRIO MID-SLICE PROBES (kit-7 log S5 item 12 proposals,
    #      counter-probed 0-hit at this build; z DERIVED z=z*(m)+2d=3m-2;
    #      the kit-7 prose z 42/48 for m=15/m=17 are off-by-one typos,
    #      disclosed in the docstring; registered at the derived slices
    #      37/43/49).
    K8_PROBES = json.loads(K8_PROBES_JSON)
    for r in K8_PROBES:
        m = r['m']
        z = r['z']
        R = m + z + 1
        extra = {'co_token_%d_allowed' % m: True,
                 's_domain': '{%d..%d}' % (m, m + 38), 'arity_max': 3,
                 'style': 'x0 published residual-band style',
                 'registered_by': ('kit-7 log S5 item 12 trio mid-slice probe proposal '
                                   '(commit a62c5d2e), counter-probed 0-hit at this build; '
                                   'z derived z=z*(m)+2d=3m-2=%d (kit-7 prose z off-by-one typos '
                                   'disclosed in the docstring)' % z),
                 'candidate': r['cand'] + '; any deviation is the datum',
                 'trio_probe_%d' % m: r['trio'],
                 'seat_kind': r['kind']}
        out.append(row_record_x0('trio_mid_slice_m%d_z%d_row_record' % (m, z),
                                 'trio_mid_slice_probe_m%d_z%d' % (m, z),
                                 extra, R, z, m, m, m + 38))

    # (b4) the WINDOW SWEEPS m=29 z in {49..56}, m=30 z in {50..57}
    #      (kit-7 frozen section (d) items 29/30; registered at this
    #      build: register-before-measure satisfied by this freeze).
    for z in range(49, 57):
        R = 29 + z + 1
        out.append(row_record_x0(
            'inband_m29_z%d_row_record' % z,
            'inband_window_m29_z%d' % z,
            {'co_token_29_allowed': True,
             's_domain': '{29..67}', 'arity_max': 3,
             'style': 'x0 published residual-band style',
             'registered_by': 'kit-7 frozen output section (d) window proposal item 29 (commit a62c5d2e), rows z in {49..56} = z*(29)-8..-1; register-before-measure satisfied by this freeze; m=29 is NOT strip-covered',
             'candidate': '0 separations each (in-band-clean precedent); FIRST-EVER below-frontier m=29 rows, no strip-derivation claim made',
             'band': 'm=29 window pinning: z in {49..56} here + frontier {57} + mini-ladder {58,59,60} (kit-7); z in {25..48} remains unmeasured, unregistered'},
            R, z, 29, 29, 67))

    for z in range(50, 58):
        R = 30 + z + 1
        out.append(row_record_x0(
            'inband_m30_z%d_row_record' % z,
            'inband_window_m30_z%d' % z,
            {'co_token_30_allowed': True,
             's_domain': '{30..68}', 'arity_max': 3,
             'style': 'x0 published residual-band style',
             'registered_by': 'kit-7 frozen output section (d) window proposal item 30 (commit a62c5d2e), rows z in {50..57} = z*(30)-8..-1; register-before-measure satisfied by this freeze; m=30 is NOT strip-covered',
             'candidate': '0 separations each (in-band-clean precedent); FIRST-EVER below-frontier m=30 rows, no strip-derivation claim made',
             'band': 'm=30 window pinning: z in {50..57} here + frontier {58} + mini-ladder {59,60,61} (kit-7); z in {25..49} remains unmeasured, unregistered'},
            R, z, 30, 30, 68))

    # (c) future-slice registration constants (engine-free, NOT measured)
    # (c) future-slice registration constants (engine-free, NOT measured)
    out.append({'section': 'future_slice_registration_constants',
                'label': 'engine_free_paper_only_K0832_closed_form_next_slice_predictions_NOT_measured_here',
                'registered_for_next_execution_kit_log_S5': [[
 {
  "kind": "one-past",
  "m": 19,
  "z": 58,
  "prediction": "EXACTLY ONE: {19,40}@S=59 UP 1v0 (collapse v(59,58,78)=0); {19,38} conform-DEAD at z=58=S+1 (collapse v(57,58,78)=1); death-of-d=9"
 },
 {
  "kind": "birth",
  "m": 19,
  "z": 59,
  "prediction": "EXACTLY TWO: stick {19,40} DOWN 1v2 (collapse v(59,59,79)=2) + NEW {19,42}@S=61 UP 2v0 (collapse v(61,59,79)=0), d=11 seat gap 23"
 },
 {
  "kind": "one-past",
  "m": 20,
  "z": 59,
  "prediction": "EXACTLY ONE: (20,40)@S=60 DOWN 0v1 (collapse v(60,59,80)=1); (20,38) conform-DEAD at z=59=S+1 (collapse v(58,59,80)=0); death-of-d=9"
 },
 {
  "kind": "birth",
  "m": 20,
  "z": 60,
  "prediction": "EXACTLY TWO: stick (20,40) DOWN 0v2 (collapse v(60,60,81)=2) + NEW (20,42)@S=62 UP 2v1 (collapse v(62,60,81)=1), d=11 seat gap 22"
 },
 {
  "kind": "one-past",
  "m": 21,
  "z": 54,
  "prediction": "EXACTLY ONE: {21,34}@S=55 UP 1v0 (collapse v(55,54,76)=0); {21,32} conform-DEAD at z=54=S+1 (collapse v(53,54,76)=1); death-of-d=5"
 },
 {
  "kind": "birth",
  "m": 21,
  "z": 55,
  "prediction": "EXACTLY TWO: stick {21,34} DOWN 1v2 (collapse v(55,55,77)=2) + NEW {21,36}@S=57 UP 2v0 (collapse v(57,55,77)=0), d=7 seat gap 15"
 },
 {
  "kind": "one-past",
  "m": 22,
  "z": 55,
  "prediction": "EXACTLY ONE: (22,34)@S=56 DOWN 0v1 (collapse v(56,55,78)=1); (22,32) conform-DEAD at z=55=S+1 (collapse v(54,55,78)=0); death-of-d=5"
 },
 {
  "kind": "birth",
  "m": 22,
  "z": 56,
  "prediction": "EXACTLY TWO: stick (22,34) DOWN 0v2 (collapse v(56,56,79)=2) + NEW (22,36)@S=58 UP 2v1 (collapse v(58,56,79)=1), d=7 seat gap 14"
 },
 {
  "kind": "one-past",
  "m": 23,
  "z": 56,
  "prediction": "EXACTLY ONE: {23,34}@S=57 UP 1v0 (collapse v(57,56,80)=0); {23,32} conform-DEAD at z=56=S+1 (collapse v(55,56,80)=1); death-of-d=4"
 },
 {
  "kind": "birth",
  "m": 23,
  "z": 57,
  "prediction": "EXACTLY TWO: stick {23,34} DOWN 1v2 (collapse v(57,57,81)=2) + NEW {23,36}@S=59 UP 2v0 (collapse v(59,57,81)=0), d=6 seat gap 13"
 },
 {
  "kind": "one-past",
  "m": 24,
  "z": 57,
  "prediction": "EXACTLY ONE: (24,34)@S=58 DOWN 0v1 (collapse v(58,57,82)=1); (24,32) conform-DEAD at z=57=S+1 (collapse v(56,57,82)=0); death-of-d=4"
 },
 {
  "kind": "birth",
  "m": 24,
  "z": 58,
  "prediction": "EXACTLY TWO: stick (24,34) DOWN 0v2 (collapse v(58,58,83)=2) + NEW (24,36)@S=60 UP 2v1 (collapse v(60,58,83)=1), d=6 seat gap 12"
 },
 {
  "kind": "one-past",
  "m": 25,
  "z": 58,
  "prediction": "EXACTLY ONE: {25,34}@S=59 UP 1v0 (collapse v(59,58,84)=0); {25,32} conform-DEAD at z=58=S+1 (collapse v(57,58,84)=1); death-of-d=3"
 },
 {
  "kind": "birth",
  "m": 25,
  "z": 59,
  "prediction": "EXACTLY TWO: stick {25,34} DOWN 1v2 (collapse v(59,59,85)=2) + NEW {25,36}@S=61 UP 2v0 (collapse v(61,59,85)=0), d=5 seat gap 11"
 },
 {
  "kind": "one-past",
  "m": 26,
  "z": 59,
  "prediction": "EXACTLY ONE: (26,34)@S=60 DOWN 0v1 (collapse v(60,59,86)=1); (26,32) conform-DEAD at z=59=S+1 (collapse v(58,59,86)=0); death-of-d=3"
 },
 {
  "kind": "birth",
  "m": 26,
  "z": 60,
  "prediction": "EXACTLY TWO: stick (26,34) DOWN 0v2 (collapse v(60,60,87)=2) + NEW (26,36)@S=62 UP 2v1 (collapse v(62,60,87)=1), d=5 seat gap 10"
 },
 {
  "kind": "one-past",
  "m": 27,
  "z": 58,
  "prediction": "EXACTLY ONE: {27,32}@S=59 UP 1v0 (collapse v(59,58,86)=0); {27,30} conform-DEAD at z=58=S+1 (collapse v(57,58,86)=1); death-of-d=1"
 },
 {
  "kind": "birth",
  "m": 27,
  "z": 59,
  "prediction": "EXACTLY TWO: stick {27,32} DOWN 1v2 (collapse v(59,59,87)=2) + NEW {27,34}@S=61 UP 2v0 (collapse v(61,59,87)=0), d=3 seat gap 7"
 },
 {
  "kind": "one-past",
  "m": 28,
  "z": 59,
  "prediction": "EXACTLY ONE: (28,32)@S=60 DOWN 0v1 (collapse v(60,59,88)=1); (28,30) conform-DEAD at z=59=S+1 (collapse v(58,59,88)=0); death-of-d=1"
 },
 {
  "kind": "birth",
  "m": 28,
  "z": 60,
  "prediction": "EXACTLY TWO: stick (28,32) DOWN 0v2 (collapse v(60,60,89)=2) + NEW (28,34)@S=62 UP 2v1 (collapse v(62,60,89)=1), d=3 seat gap 6"
 },
 {
  "kind": "birth",
  "m": 29,
  "z": 61,
  "prediction": "EXACTLY TWO: stick {29,32} DOWN 1v2 (collapse v(61,61,91)=2) + NEW {29,34}@S=63 UP 2v0 (collapse v(63,61,91)=0), d=2 seat gap 5"
 },
 {
  "kind": "one-past",
  "m": 29,
  "z": 62,
  "prediction": "EXACTLY ONE: {29,34}@S=63 UP 1v0 (collapse v(63,62,92)=0); {29,32} conform-DEAD at z=62=S+1 (collapse v(61,62,92)=1); death-of-d=1"
 },
 {
  "kind": "birth",
  "m": 29,
  "z": 63,
  "prediction": "EXACTLY TWO: stick {29,34} DOWN 1v2 (collapse v(63,63,93)=2) + NEW {29,36}@S=65 UP 2v0 (collapse v(65,63,93)=0), d=3 seat gap 7"
 },
 {
  "kind": "birth",
  "m": 30,
  "z": 62,
  "prediction": "EXACTLY TWO: stick (30,32) DOWN 0v2 (collapse v(62,62,93)=2) + NEW (30,34)@S=64 UP 2v1 (collapse v(64,62,93)=1), d=2 seat gap 4"
 },
 {
  "kind": "one-past",
  "m": 30,
  "z": 63,
  "prediction": "EXACTLY ONE: (30,34)@S=64 DOWN 0v1 (collapse v(64,63,94)=1); (30,32) conform-DEAD at z=63=S+1 (collapse v(62,63,94)=0); death-of-d=1"
 },
 {
  "kind": "birth",
  "m": 30,
  "z": 64,
  "prediction": "EXACTLY TWO: stick (30,34) DOWN 0v2 (collapse v(64,64,95)=2) + NEW (30,36)@S=66 UP 2v1 (collapse v(66,64,95)=1), d=3 seat gap 6"
 },
 {
  "kind": "one-past",
  "m": 31,
  "z": 62,
  "prediction": "EXACTLY ONE: {31,32}@S=63 UP 1v0 (collapse v(63,62,94)=0); one-past of the d=0 seat (frontier decay 2->1); CONTINGENT: registered under the assumption the kit-8 frontier first contact m=31@z=61 measures the 19th parity datum; any deviation is the datum"
 },
 {
  "kind": "birth",
  "m": 31,
  "z": 63,
  "prediction": "EXACTLY TWO: stick {31,32} DOWN 1v2 (collapse v(63,63,95)=2) + NEW {31,34}@S=65 UP 2v0 (collapse v(65,63,95)=0), d=1 seat gap 3"
 },
 {
  "kind": "one-past",
  "m": 31,
  "z": 64,
  "prediction": "EXACTLY ONE: {31,34}@S=65 UP 1v0 (collapse v(65,64,96)=0); {31,32} conform-DEAD at z=64=S+1 (collapse v(63,64,96)=1); death-of-d=0"
 },
 {
  "kind": "one-past",
  "m": 32,
  "z": 63,
  "prediction": "EXACTLY ONE: (32,32)@S=64 DOWN 0v1 (collapse v(64,63,96)=1); one-past of the d=0 seat (frontier decay 2->0); CONTINGENT: registered under the assumption the kit-8 frontier first contact m=31@z=61 measures the 19th parity datum; any deviation is the datum"
 },
 {
  "kind": "birth",
  "m": 32,
  "z": 64,
  "prediction": "EXACTLY TWO: stick (32,32) DOWN 0v2 (collapse v(64,64,97)=2) + NEW (32,34)@S=66 UP 2v1 (collapse v(66,64,97)=1), d=1 seat gap 2"
 },
 {
  "kind": "one-past",
  "m": 32,
  "z": 65,
  "prediction": "EXACTLY ONE: (32,34)@S=66 DOWN 0v1 (collapse v(66,65,98)=1); (32,32) conform-DEAD at z=65=S+1 (collapse v(64,65,98)=0); death-of-d=0"
 },
 {
  "kind": "frontier first contact proposal (FIRST-EVER m=33 row)",
  "m": 33,
  "z": 65,
  "prediction": "EXACTLY ONE: {33,34}@S=67 UP 2v0 (collapse v(67,65,99)=0); z*(33)=2*33-2+1=65 per K1268 (derive_check double-checked); R=99"
 },
 {
  "kind": "frontier first contact proposal (FIRST-EVER m=34 row)",
  "m": 34,
  "z": 66,
  "prediction": "EXACTLY ONE: (34,34)@S=68 UP 2v1 (collapse v(68,66,101)=1); z*(34)=2*34-2+0=66 per K1268 (derive_check double-checked); R=101"
 },
 {
  "kind": "in-band window sweep proposal",
  "m": 31,
  "z": "53..60",
  "prediction": "0 separations each (candidate); z*(31)-8..-1; m=31 is NOT strip-covered; register before measuring"
 },
 {
  "kind": "in-band window sweep proposal",
  "m": 32,
  "z": "54..61",
  "prediction": "0 separations each (candidate); z*(32)-8..-1; m=32 is NOT strip-covered; register before measuring"
 },
 {
  "kind": "trio-tracker continuation proposal (NON-BINDING, log-level)",
  "m": 19,
  "z": "58,59",
  "prediction": "track the stacked trio {19,19,19}@S=57 beside the binding m=19 rows; any outcome is the datum"
 },
 {
  "kind": "probe continuation proposals (contingent on probe outcomes, NON-BINDING, log-level)",
  "prediction": "if the m=13/15/17 probe rows measure their trios UP 2v0, register the trio lifecycle rows (one-past z=3m-1, stick z=3m, next birth) for those m; if conform-or-other, register the observed status either way; the row records here are the provenance"
 },
 {
  "kind": "hollow-row conditional (pre-declared)",
  "prediction": "if the m=26 z=25 hole row measures clean, the m=26 line becomes FULLY SWEPT z in {25..56}; any deviation voids the conditional and is the datum"
 }
]]})

    # (h) published anchor rechecks (180 spots, verbatim published values)
    rechecks = []
    H.cache_clear()
    for (R, X, z2, expected, role) in anchor_spec:
        XX = tuple(sorted(X, reverse=True))
        hv = H(R, XX, z2)
        S = sum(X)
        ev = v(S, z2, R)
        rechecks.append({'R': R, 'X': list(XX), 'z': z2, 'value': hv,
                         'collapse': ev, 'published_value': expected,
                         'match': hv == expected,
                         'conform': hv == ev,
                         'role': role})
    out.append({'section': 'published_anchor_rechecks',
                'label': 'one_hundred_eighty_published_spots_reproduce_exactly_match_field_is_value_equality_with_published',
                'rows': rechecks,
                'note': 'the separation spots are separations by construction (value != collapse BY DESIGN); the match criterion is equality with the PUBLISHED value'})

    res = {'result': 'EXPLORE-DONE', 'sections': out}
    print(json.dumps(res, sort_keys=True, separators=(',', ':')))


if __name__ == '__main__':
    main()
