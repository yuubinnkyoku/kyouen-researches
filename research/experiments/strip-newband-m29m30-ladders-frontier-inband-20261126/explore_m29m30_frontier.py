"""
explore_m29m30_frontier: FROZEN PRE-DECLARATION census for the LADDER
CONTINUATION rows of the m=19..m=24 residual bands (the registered
kit-6 S5 items 1-12), the m=25 / m=26 POST-MINI-LADDER rows (the
registered kit-6 S5 items 13-18), the m=27 / m=28 MINI-LADDER rows
(the registered kit-6 S5 items 19-24, including the FIRST m=27 / m=28
death datum candidates), the FRONTIER rows m=29 and m=30 (the
registered 17th / 18th parity datum candidates, the FIRST-EVER
m=29 / m=30 rows), the REGISTERED in-band window sweeps m=25 z in
{33..40}, m=26 z in {35..42} (resolving the kit-5 label z=42 row),
m=27 z in {45..52} and m=28 z in {46..53} (kit-6 S5 items 25-28), the
SCAFFOLD window extensions m=25 z in {27..32} and m=26 z in
{27..34} (kit-6 S5 item 31 deferral note: NOT registered by kit-6,
REGISTERED HERE AT THIS BUILD before the first run of this file —
the register-before-measure protocol is satisfied by this freeze;
candidates 0 separations each per the in-band-clean precedent), plus
141 published anchor rechecks (the 112 kit-6-era published anchors
verbatim + the 29 kit-6 separation spots, first re-anchored here and
machine-verified 29/29 against the published kit-6 frozen output
values BEFORE this file's first run, canonical engine only on
published spots).
NO K slot is claimed by this file; the 26 candidate measurement rows
and the 46 window/scaffold rows in this docstring were frozen BEFORE
the first run of this file. The only edit performed after any run
must be disclosed here in dated form (verifier-table or docstring
fixes only; no candidate, engine, or measurement code was edited at
any time).

Registered provenance (all BEFORE any measurement by this kit):
- The twenty-six binding candidate rows are the REGISTERED candidates
  of the published kit-6 frozen output section
  future_slice_registration_constants (commit 76c461da,
  research/experiments/strip-newband-m27m28-frontier-inband-20261126/),
  verbatim; the z* arithmetic z*(29)=2*29-2+1=57 and
  z*(30)=2*30-2+0=58 per K1268 was re-derived and double-asserted at
  this build by an engine-free derive check that ALSO machine-reproduced
  every published collapse literal of all 30 measurable kit-6
  registrations (48 literals, 0 mismatches) and the seat-lifecycle
  structure of every row (S=sum(X), R=m+z+1, stick-seat coincidence
  z=S(d-1) at birth slices, dead-shape z=S+1 at death slices,
  co-token=m+2d+1 odd / m+2d even, S=2m+2d+1 odd / 2m+2d even).
- The four window sweeps (kit-6 S5 items 25-28) are registered here
  verbatim: 0 separations each. Strip coverage re-probed at this
  build: m=25 and m=26 ARE strip-covered at z in {25,26} (published
  z25/z26 kits cover m in {20..26}); m=27 / m=28 are NOT strip-
  covered (z26-floor20 covers m in {20..26} only) — their window
  rows z in {45..52} / {46..53} are FIRST-EVER below-frontier rows
  for those m and no strip-derivation claim is made for them.
- The two scaffold extensions (kit-6 S5 item 31 deferral text:
  "below-window rows m=25 z in {27..32} and m=26 z in {27..34}: NOT
  registered by this kit") are REGISTERED HERE AT THIS BUILD, before
  the first run, candidates 0 separations each per the in-band-clean
  precedent; m=25/m=26 ARE strip-covered at z in {25,26}. If these
  measure clean, the measured m=25 line becomes the series-first
  FULLY SWEPT z in {25..55} row and m=26 the z in {25..56} row
  (strip {25,26} + scaffold {27..32}/{27..34} + window + kit-6
  window {41..48}/{43..49} + frontier/mini/post-mini seats) — this
  consequence is recorded here BEFORE the fact, as a pre-declared
  conditional.
- ANCHOR-TABLE PROVENANCE: the 112 inherited entries are the kit-6
  published anchor table verbatim; the 29 kit-6 separation spots were
  extracted by machine from the published kit-6 frozen output (R, X,
  z, value straight from the row records) and machine-verified to
  reproduce all 29 published values EXACTLY (29/29, canonical engine,
  BEFORE this file's first run).
- DATED DISCLOSURE AT THIS BUILD (2026-11-26, kit bytes untouched
  elsewhere): the kit-6 log S2 table line for m=25@z=51 renders the
  registered candidate as "{25,26} UP 1v2 + {25,28}@S=52 UP 2v1";
  the machine-registered kit-5 candidate (kit-5 frozen .out section
  (d)) and the kit-6 frozen .out measurement both read "stick
  {25,26} DOWN 1v2 (S=51) + NEW {25,28}@S=53 UP 2v0" (25+28=53; the
  log-table line is a prose transcription typo). The frozen kit-6
  .out (sha 4eda4e1e...) is the SSOT; this kit inherits its 29
  spot values from it; nothing in any frozen byte changes.
- Counter-probe at this build (2026-11-26T10:04Z head 52826b45):
  all 9 kit-specific content queries (frontier_m29, m29_z57,
  m30_z58, inband_m27_z45, inband_m28_z46, ladder_m19_z54,
  ladder_m27_z54, m29m30, kit-7) returned 0 measurement records,
  and no experiment directory or log for any of this kit's rows
  exists on main. Re-run at push time against then-current main and
  disclosed in the push commit body.
- Determinism claim: single JSON line stdout, no dict-ordering or
  hash-seed dependence (six-run byte-identical battery on the kit-6
  explorer; same code structure here).
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
    ]
    # (a) K0832 battery: every single-token literal used by this file
    # (cumulative: no prior kit datum lost; the kit-4/kit-5/kit-6 literal
    # groups inherited verbatim from the kit-6 explorer).
    battery_lits = []
    rows_stair = []
    meas_rows = [[19, 54], [19, 55], [20, 55], [20, 56], [21, 50], [21, 51], [22, 51], [22, 52], [23, 52], [23, 53], [24, 53], [24, 54], [25, 53], [25, 54], [25, 55], [26, 54], [26, 55], [26, 56], [27, 54], [27, 55], [27, 56], [28, 55], [28, 56], [28, 57], [29, 57], [30, 58], [25, 33], [25, 34], [25, 35], [25, 36], [25, 37], [25, 38], [25, 39], [25, 40], [26, 35], [26, 36], [26, 37], [26, 38], [26, 39], [26, 40], [26, 41], [26, 42], [27, 45], [27, 46], [27, 47], [27, 48], [27, 49], [27, 50], [27, 51], [27, 52], [28, 46], [28, 47], [28, 48], [28, 49], [28, 50], [28, 51], [28, 52], [28, 53], [25, 27], [25, 28], [25, 29], [25, 30], [25, 31], [25, 32], [26, 27], [26, 28], [26, 29], [26, 30], [26, 31], [26, 32], [26, 33], [26, 34]]
    for (m, z) in meas_rows:
        R = m + z + 1
        for S in (m, m + 2, 2 * m, 2 * m + 1, m + 37, m + 38):
            battery_lits.append((S, z, R))
        rows_stair.append((m, z, R))
    # registered kit-4 S5 items (1)-(11) candidate constants
    # (m=22 rows with the CORRECTED R annotations, disclosed in the
    # docstring: values identical to the slipped kit-4 triples)
    for (x, z2, R2) in [
            (51, 50, 70), (49, 50, 70), (51, 51, 71), (53, 51, 71),
            (52, 51, 72), (50, 51, 72), (52, 52, 73), (54, 52, 73),
            (47, 46, 68), (45, 46, 68), (47, 47, 69), (49, 47, 69),
            (48, 47, 70), (46, 47, 70), (48, 48, 71), (50, 48, 71),
            (49, 48, 72), (47, 48, 72), (49, 49, 73), (51, 49, 73),
            (50, 50, 75), (52, 50, 75)]:
        battery_lits.append((x, z2, R2))
    # the SLIPPED kit-4 (f) m=22 annotation triples (kept on record;
    # closed form is parity-constant between the two R windows, so
    # the values coincide — disclosed in the docstring)
    for (x, z2, R2) in [
            (48, 47, 68), (46, 47, 68), (48, 48, 69), (50, 48, 69)]:
        battery_lits.append((x, z2, R2))
    # frontier 13th/14th datum candidates
    for (x, z2, R2) in [(51, 49, 75), (52, 50, 77)]:
        battery_lits.append((x, z2, R2))
    # measured-row constants of THIS kit (the kit-5 frozen section (d)
    # registration list, verbatim; battery-checked again here)
    for (x, z2, R2) in [
            (53, 52, 72), (51, 52, 72), (53, 53, 73), (55, 53, 73),
            (54, 53, 74), (52, 53, 74), (54, 54, 75), (56, 54, 75),
            (49, 48, 70), (47, 48, 70), (49, 49, 71), (51, 49, 71),
            (50, 49, 72), (48, 49, 72), (50, 50, 73), (52, 50, 73),
            (51, 50, 74), (49, 50, 74), (51, 51, 75), (53, 51, 75),
            (52, 51, 76), (50, 51, 76), (52, 52, 77), (54, 52, 77),
            (51, 50, 76), (51, 51, 77), (53, 51, 77), (53, 52, 78),
            (51, 52, 78), (52, 51, 78), (52, 52, 79), (54, 52, 79),
            (54, 53, 80), (52, 53, 80), (55, 53, 81), (56, 54, 83)]:
        battery_lits.append((x, z2, R2))


    # the kit-6 frozen section (d) constants — the 46 candidate literal
    # triples of THIS kit's registered rows (verbatim; battery-checked
    # again here as measured-candidate constants)
    for (x, z2, R2) in [
            (55, 54, 74),
            (53, 54, 74),
            (55, 55, 75),
            (57, 55, 75),
            (56, 55, 76),
            (54, 55, 76),
            (56, 56, 77),
            (58, 56, 77),
            (51, 50, 74),
            (49, 50, 74),
            (51, 51, 75),
            (53, 51, 75),
            (52, 51, 76),
            (50, 51, 76),
            (52, 52, 77),
            (54, 52, 77),
            (53, 52, 76),
            (51, 52, 76),
            (53, 53, 77),
            (55, 53, 77),
            (54, 53, 78),
            (52, 53, 78),
            (54, 54, 79),
            (56, 54, 79),
            (53, 53, 79),
            (55, 53, 79),
            (55, 54, 80),
            (53, 54, 80),
            (55, 55, 81),
            (57, 55, 81),
            (54, 54, 81),
            (56, 54, 81),
            (56, 55, 82),
            (54, 55, 82),
            (56, 56, 83),
            (58, 56, 83),
            (55, 54, 82),
            (55, 55, 83),
            (57, 55, 83),
            (57, 56, 84),
            (55, 56, 84),
            (56, 55, 84),
            (56, 56, 85),
            (58, 56, 85),
            (58, 57, 86),
            (56, 57, 86),
            (59, 57, 87),
            (60, 58, 89),
        ]:
        battery_lits.append((x, z2, R2))
    # future-slice registration constants of THIS kit (section (d),
    # NOT measured here; kit-8 candidates; engine-free lifecycle derivation)
    for (x, z2, R2) in [
            (57, 56, 76),
            (55, 56, 76),
            (57, 57, 77),
            (59, 57, 77),
            (58, 57, 78),
            (56, 57, 78),
            (58, 58, 79),
            (60, 58, 79),
            (53, 52, 74),
            (51, 52, 74),
            (53, 53, 75),
            (55, 53, 75),
            (54, 53, 76),
            (52, 53, 76),
            (54, 54, 77),
            (56, 54, 77),
            (55, 54, 78),
            (53, 54, 78),
            (55, 55, 79),
            (57, 55, 79),
            (56, 55, 80),
            (54, 55, 80),
            (56, 56, 81),
            (58, 56, 81),
            (57, 56, 82),
            (55, 56, 82),
            (57, 57, 83),
            (59, 57, 83),
            (58, 57, 84),
            (56, 57, 84),
            (58, 58, 85),
            (60, 58, 85),
            (57, 56, 84),
            (55, 56, 84),
            (57, 57, 85),
            (59, 57, 85),
            (58, 57, 86),
            (56, 57, 86),
            (58, 58, 87),
            (60, 58, 87),
            (59, 58, 88),
            (59, 59, 89),
            (61, 59, 89),
            (61, 60, 90),
            (59, 60, 90),
            (60, 59, 90),
            (60, 60, 91),
            (62, 60, 91),
            (62, 61, 92),
            (60, 61, 92),
            (63, 61, 93),
            (64, 62, 95),
        ]:
        battery_lits.append((x, z2, R2))
    # anchor collapse literals (section (h))
    for (R, X, z2) in [t[:3] for t in anchor_spec]:
        battery_lits.append((sum(X), z2, R))
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

    # (b) the 26 registered candidate rows (kit-6 log S5 items 1-24 and
    #      29-30, verbatim binding candidates; machine-emitted call site)
    K7_ROWS = [
 {
  "item": 1,
  "m": 19,
  "z": 54,
  "kind": "one-past-of-d=8 / death-of-d=7",
  "cand": "EXACTLY ONE: {19,36}@S=55 UP 1v0 (collapse v(55,54,74)=0); {19,34} conform-DEAD at z=54=S+1 (collapse v(53,54,74)=1)"
 },
 {
  "item": 2,
  "m": 19,
  "z": 55,
  "kind": "birth slice d=9",
  "cand": "EXACTLY TWO: stick {19,36} DOWN 1v2 (collapse v(55,55,75)=2) + NEW {19,38}@S=57 UP 2v0 (collapse v(57,55,75)=0), d=9 seat gap 19"
 },
 {
  "item": 3,
  "m": 20,
  "z": 55,
  "kind": "one-past-of-d=8 / death-of-d=7",
  "cand": "EXACTLY ONE: (20,36)@S=56 DOWN 0v1 (collapse v(56,55,76)=1); (20,34) conform-DEAD at z=55=S+1 (collapse v(54,55,76)=0)"
 },
 {
  "item": 4,
  "m": 20,
  "z": 56,
  "kind": "birth slice d=9",
  "cand": "EXACTLY TWO: stick (20,36) DOWN 0v2 (collapse v(56,56,77)=2) + NEW (20,38)@S=58 UP 2v1 (collapse v(58,56,77)=1), d=9 seat gap 18"
 },
 {
  "item": 5,
  "m": 21,
  "z": 50,
  "kind": "one-past-of-d=4 / death-of-d=3",
  "cand": "EXACTLY ONE: {21,30}@S=51 UP 1v0 (collapse v(51,50,74)=0); {21,28} conform-DEAD at z=50=S+1 (collapse v(49,50,74)=1)"
 },
 {
  "item": 6,
  "m": 21,
  "z": 51,
  "kind": "birth slice d=5",
  "cand": "EXACTLY TWO: stick {21,30} DOWN 1v2 (collapse v(51,51,75)=2) + NEW {21,32}@S=53 UP 2v0 (collapse v(53,51,75)=0), d=5 seat gap 11"
 },
 {
  "item": 7,
  "m": 22,
  "z": 51,
  "kind": "one-past-of-d=4 / death-of-d=3",
  "cand": "EXACTLY ONE: (22,30)@S=52 DOWN 0v1 (collapse v(52,51,76)=1); (22,28) conform-DEAD at z=51=S+1 (collapse v(50,51,76)=0)"
 },
 {
  "item": 8,
  "m": 22,
  "z": 52,
  "kind": "birth slice d=5",
  "cand": "EXACTLY TWO: stick (22,30) DOWN 0v2 (collapse v(52,52,77)=2) + NEW (22,32)@S=54 UP 2v1 (collapse v(54,52,77)=1), d=5 seat gap 10"
 },
 {
  "item": 9,
  "m": 23,
  "z": 52,
  "kind": "one-past-of-d=3 / death-of-d=2",
  "cand": "EXACTLY ONE: {23,30}@S=53 UP 1v0 (collapse v(53,52,76)=0); {23,28} conform-DEAD at z=52=S+1 (collapse v(51,52,76)=1)"
 },
 {
  "item": 10,
  "m": 23,
  "z": 53,
  "kind": "birth slice d=4",
  "cand": "EXACTLY TWO: stick {23,30} DOWN 1v2 (collapse v(53,53,77)=2) + NEW {23,32}@S=55 UP 2v0 (collapse v(55,53,77)=0), d=4 seat gap 9"
 },
 {
  "item": 11,
  "m": 24,
  "z": 53,
  "kind": "one-past-of-d=3 / death-of-d=2",
  "cand": "EXACTLY ONE: (24,30)@S=54 DOWN 0v1 (collapse v(54,53,78)=1); (24,28) conform-DEAD at z=53=S+1 (collapse v(52,53,78)=0)"
 },
 {
  "item": 12,
  "m": 24,
  "z": 54,
  "kind": "birth slice d=4",
  "cand": "EXACTLY TWO: stick (24,30) DOWN 0v2 (collapse v(54,54,79)=2) + NEW (24,32)@S=56 UP 2v1 (collapse v(56,54,79)=1), d=4 seat gap 8"
 },
 {
  "item": 13,
  "m": 25,
  "z": 53,
  "kind": "birth slice d=2 (stick of the d=1 seat coincides: S({25,28})=53=z)",
  "cand": "EXACTLY TWO: stick {25,28} DOWN 1v2 (collapse v(53,53,79)=2) + NEW {25,30}@S=55 UP 2v0 (collapse v(55,53,79)=0), d=2 seat gap 5"
 },
 {
  "item": 14,
  "m": 25,
  "z": 54,
  "kind": "one-past-of-d=2 / death-of-d=1",
  "cand": "EXACTLY ONE: {25,30}@S=55 UP 1v0 (collapse v(55,54,80)=0); {25,28} conform-DEAD at z=54=S+1 (collapse v(53,54,80)=1)"
 },
 {
  "item": 15,
  "m": 25,
  "z": 55,
  "kind": "birth slice d=3",
  "cand": "EXACTLY TWO: stick {25,30} DOWN 1v2 (collapse v(55,55,81)=2) + NEW {25,32}@S=57 UP 2v0 (collapse v(57,55,81)=0), d=3 seat gap 7"
 },
 {
  "item": 16,
  "m": 26,
  "z": 54,
  "kind": "birth slice d=2 (stick of the d=1 seat coincides: S((26,28))=54=z)",
  "cand": "EXACTLY TWO: stick (26,28) DOWN 0v2 (collapse v(54,54,81)=2) + NEW (26,30)@S=56 UP 2v1 (collapse v(56,54,81)=1), d=2 seat gap 4"
 },
 {
  "item": 17,
  "m": 26,
  "z": 55,
  "kind": "one-past-of-d=2 / death-of-d=1",
  "cand": "EXACTLY ONE: (26,30)@S=56 DOWN 0v1 (collapse v(56,55,82)=1); (26,28) conform-DEAD at z=55=S+1 (collapse v(54,55,82)=0)"
 },
 {
  "item": 18,
  "m": 26,
  "z": 56,
  "kind": "birth slice d=3",
  "cand": "EXACTLY TWO: stick (26,30) DOWN 0v2 (collapse v(56,56,83)=2) + NEW (26,32)@S=58 UP 2v1 (collapse v(58,56,83)=1), d=3 seat gap 6"
 },
 {
  "item": 19,
  "m": 27,
  "z": 54,
  "kind": "one-past of the d=0 seat",
  "cand": "EXACTLY ONE: {27,28}@S=55 UP 1v0 (collapse v(55,54,82)=0)"
 },
 {
  "item": 20,
  "m": 27,
  "z": 55,
  "kind": "birth slice d=1 (stick coincides: S(d0)=55=z)",
  "cand": "EXACTLY TWO: stick {27,28} DOWN 1v2 (collapse v(55,55,83)=2) + NEW {27,30}@S=57 UP 2v0 (collapse v(57,55,83)=0), d=1 seat gap 3"
 },
 {
  "item": 21,
  "m": 27,
  "z": 56,
  "kind": "one-past-of-d=1 / death-of-d=0 \u2014 the FIRST m=27 death datum candidate",
  "cand": "EXACTLY ONE: {27,30}@S=57 UP 1v0 (collapse v(57,56,84)=0); {27,28} conform-DEAD at z=56=S+1 (collapse v(55,56,84)=1)"
 },
 {
  "item": 22,
  "m": 28,
  "z": 55,
  "kind": "one-past of the d=0 seat",
  "cand": "EXACTLY ONE: (28,28)@S=56 DOWN 0v1 (collapse v(56,55,84)=1)"
 },
 {
  "item": 23,
  "m": 28,
  "z": 56,
  "kind": "birth slice d=1 (stick coincides: S(d0)=56=z)",
  "cand": "EXACTLY TWO: stick (28,28) DOWN 0v2 (collapse v(56,56,85)=2) + NEW (28,30)@S=58 UP 2v1 (collapse v(58,56,85)=1), d=1 seat gap 2"
 },
 {
  "item": 24,
  "m": 28,
  "z": 57,
  "kind": "one-past-of-d=1 / death-of-d=0 \u2014 the FIRST m=28 death datum candidate",
  "cand": "EXACTLY ONE: (28,30)@S=58 DOWN 0v1 (collapse v(58,57,86)=1); (28,28) conform-DEAD at z=57=S+1 (collapse v(56,57,86)=0)"
 },
 {
  "item": 29,
  "m": 29,
  "z": 57,
  "kind": "frontier first contact proposal (FIRST-EVER m=29 row)",
  "cand": "EXACTLY ONE: {29,30}@S=59 UP 2v0 (collapse v(59,57,87)=0); z*(29)=2*29-2+1=57 per K1268 (derive_check double-checked); R=87; the 17th datum candidate"
 },
 {
  "item": 30,
  "m": 30,
  "z": 58,
  "kind": "frontier first contact proposal (FIRST-EVER m=30 row)",
  "cand": "EXACTLY ONE: (30,30)@S=60 UP 2v1 (collapse v(60,58,89)=1); z*(30)=2*30-2+0=58 per K1268 (derive_check double-checked); R=89; the 18th datum candidate"
 }
]

    def emit_k7_row(r):
        m = r['m']
        z = r['z']
        R = m + z + 1
        smax = m + 38
        extra = {'co_token_%d_allowed' % m: True,
                 's_domain': '{%d..%d}' % (m, smax), 'arity_max': 3,
                 'style': 'x0 published residual-band style',
                 'registered_by': ('kit-6 log S5 item (%d) + frozen section (d) '
                                   '(commit 76c461da)' % r['item']),
                 'candidate': r['cand'] + '; any deviation is the datum',
                 'seat_kind': r['kind']}
        secname = r['secname']
        return row_record_x0(secname, r['label'], extra, R, z, m, m, smax)

    for r in K7_ROWS:
        m = r['m']
        z = r['z']
        if r['item'] == 29 or r['item'] == 30:
            r['secname'] = 'frontier_m%d_z%d_row_record' % (m, z)
            r['label'] = ('registered_frontier_record_m%d_z%d_K1268_%s_datum_candidate'
                          % (m, z, '17th' if r['item'] == 29 else '18th'))
        else:
            r['secname'] = 'ladder_m%d_z%d_row_record' % (m, z)
            r['label'] = 'registered_kit6_S5_item%d_%s' % (r['item'], r['kind'])
        out.append(emit_k7_row(r))

    # (c) REGISTERED window sweeps (kit-6 S5 items 25-28) + the two
    #      SCAFFOLD extensions registered at this build (kit-6 S5 item 31
    #      deferral; register-before-measure satisfied by this freeze).
    #      Strip coverage re-probed at this build: m=25/m=26 strip-covered
    #      at z in {25,26}; m=27/m=28 NOT strip-covered.
    for z in range(33, 41):
        R = 25 + z + 1
        out.append(row_record_x0(
            'inband_m25_z%d_row_record' % z,
            'inband_window_m25_z%d' % z,
            {'co_token_25_allowed': True,
             's_domain': '{25..63}', 'arity_max': 3,
             'style': 'x0 published residual-band style',
             'registered_by': 'kit-6 log S5 item (25) (commit 76c461da), rows z in {33..40}; strip coverage re-probed at this build (m=25 strip-covered at z in {25,26})',
             'candidate': '0 separations each (in-band-clean precedent)',
             'band': 'm=25 in-band window pinning: z in {33..40} here (kit-6 window {41..48}, kit-6 mini-ladder {50,51,52}, kit-5 frontier {49}, kit-7 post-mini {53,54,55}); the scaffold z in {27..32} measured below closes the strip-to-window gap'},
            R, z, 25, 25, 63))

    for z in range(35, 43):
        R = 26 + z + 1
        out.append(row_record_x0(
            'inband_m26_z%d_row_record' % z,
            'inband_window_m26_z%d' % z,
            {'co_token_26_allowed': True,
             's_domain': '{26..64}', 'arity_max': 3,
             'style': 'x0 published residual-band style',
             'registered_by': 'kit-6 log S5 item (26) (commit 76c461da), rows z in {35..42} — this RESOLVES the kit-5 label z=42 row; strip coverage re-probed at this build (m=26 strip-covered at z in {25,26})',
             'candidate': '0 separations each (in-band-clean precedent)',
             'band': 'm=26 in-band window pinning: z in {35..42} here (kit-6 window {43..49} + z=50 blind recheck, kit-6 mini-ladder {51,52,53}, kit-7 post-mini {54,55,56}); the scaffold z in {27..34} measured below closes the strip-to-window gap'},
            R, z, 26, 26, 64))

    for z in range(45, 53):
        R = 27 + z + 1
        out.append(row_record_x0(
            'inband_m27_z%d_row_record' % z,
            'inband_window_m27_z%d' % z,
            {'co_token_27_allowed': True,
             's_domain': '{27..65}', 'arity_max': 3,
             'style': 'x0 published residual-band style',
             'registered_by': 'kit-6 log S5 item (27) (commit 76c461da), rows z in {45..52} = z*(27)-8..-1; m=27 is NOT strip-covered (z26-floor20 covers m in {20..26} only)',
             'candidate': '0 separations each (in-band-clean precedent); FIRST-EVER below-frontier m=27 rows, no strip-derivation claim made',
             'band': 'm=27 window pinning: z in {45..52} here + frontier {53} + mini-ladder {54,55,56} (kit-6/kit-7); z in {25..44} remains unmeasured, unregistered'},
            R, z, 27, 27, 65))

    for z in range(46, 54):
        R = 28 + z + 1
        out.append(row_record_x0(
            'inband_m28_z%d_row_record' % z,
            'inband_window_m28_z%d' % z,
            {'co_token_28_allowed': True,
             's_domain': '{28..66}', 'arity_max': 3,
             'style': 'x0 published residual-band style',
             'registered_by': 'kit-6 log S5 item (28) (commit 76c461da), rows z in {46..53} = z*(28)-8..-1; m=28 is NOT strip-covered',
             'candidate': '0 separations each (in-band-clean precedent); FIRST-EVER below-frontier m=28 rows, no strip-derivation claim made',
             'band': 'm=28 window pinning: z in {46..53} here + frontier {54} + mini-ladder {55,56,57} (kit-6/kit-7); z in {25..45} remains unmeasured, unregistered'},
            R, z, 28, 28, 66))

    for z in range(27, 33):
        R = 25 + z + 1
        out.append(row_record_x0(
            'inband_m25_z%d_row_record' % z,
            'inband_scaffold_m25_z%d' % z,
            {'co_token_25_allowed': True,
             's_domain': '{25..63}', 'arity_max': 3,
             'style': 'x0 published residual-band style',
             'registered_by': 'REGISTERED AT THIS BUILD (kit-6 log S5 item 31 deferral note, commit 76c461da: register before measuring — satisfied by freezing this file before its first run); candidate 0 separations per the in-band-clean precedent',
             'candidate': '0 separations (in-band-clean precedent); m=25 strip-covered at z in {25,26}',
             'band': 'm=25 SCAFFOLD extension z in {27..32}: closes the strip-to-window gap; if clean, the m=25 measured line becomes the series-first FULLY SWEPT z in {25..55} row (pre-declared conditional)'},
            R, z, 25, 25, 63))

    for z in range(27, 35):
        R = 26 + z + 1
        out.append(row_record_x0(
            'inband_m26_z%d_row_record' % z,
            'inband_scaffold_m26_z%d' % z,
            {'co_token_26_allowed': True,
             's_domain': '{26..64}', 'arity_max': 3,
             'style': 'x0 published residual-band style',
             'registered_by': 'REGISTERED AT THIS BUILD (kit-6 log S5 item 31 deferral note, commit 76c461da: register before measuring — satisfied by freezing this file before its first run); candidate 0 separations per the in-band-clean precedent',
             'candidate': '0 separations (in-band-clean precedent); m=26 strip-covered at z in {25,26}',
             'band': 'm=26 SCAFFOLD extension z in {27..34}: closes the strip-to-window gap; if clean, the m=26 measured line becomes the FULLY SWEPT z in {25..56} row (pre-declared conditional)'},
            R, z, 26, 26, 64))

    # (d) future-slice registration constants (engine-free, NOT measured)
    out.append({'section': 'future_slice_registration_constants',
                'label': 'engine_free_paper_only_K0832_closed_form_next_slice_predictions_NOT_measured_here',
                'registered_for_next_execution_kit_log_S5': [[
 {
  "kind": "one-past-of-d=9 / death-of-d=8",
  "m": 19,
  "z": 56,
  "prediction": "EXACTLY ONE: {19,38}@S=57 UP 1v0 (collapse v(57,56,76)=0); {19,36} conform-DEAD at z=56=S+1 (collapse v(55,56,76)=1); death-of-d=8"
 },
 {
  "kind": "birth slice d=10",
  "m": 19,
  "z": 57,
  "prediction": "EXACTLY TWO: stick {19,38} DOWN 1v2 (collapse v(57,57,77)=2) + NEW {19,40}@S=59 UP 2v0 (collapse v(59,57,77)=0), d=10 seat gap 21 (stick seat coincides z=S(d-1))"
 },
 {
  "kind": "one-past-of-d=9 / death-of-d=8",
  "m": 20,
  "z": 57,
  "prediction": "EXACTLY ONE: (20,38)@S=58 DOWN 0v1 (collapse v(58,57,78)=1); (20,36) conform-DEAD at z=57=S+1 (collapse v(56,57,78)=0); death-of-d=8"
 },
 {
  "kind": "birth slice d=10",
  "m": 20,
  "z": 58,
  "prediction": "EXACTLY TWO: stick (20,38) DOWN 0v2 (collapse v(58,58,79)=2) + NEW (20,40)@S=60 UP 2v1 (collapse v(60,58,79)=1), d=10 seat gap 20 (stick seat coincides z=S(d-1))"
 },
 {
  "kind": "one-past-of-d=5 / death-of-d=4",
  "m": 21,
  "z": 52,
  "prediction": "EXACTLY ONE: {21,32}@S=53 UP 1v0 (collapse v(53,52,74)=0); {21,30} conform-DEAD at z=52=S+1 (collapse v(51,52,74)=1); death-of-d=4"
 },
 {
  "kind": "birth slice d=6",
  "m": 21,
  "z": 53,
  "prediction": "EXACTLY TWO: stick {21,32} DOWN 1v2 (collapse v(53,53,75)=2) + NEW {21,34}@S=55 UP 2v0 (collapse v(55,53,75)=0), d=6 seat gap 13 (stick seat coincides z=S(d-1))"
 },
 {
  "kind": "one-past-of-d=5 / death-of-d=4",
  "m": 22,
  "z": 53,
  "prediction": "EXACTLY ONE: (22,32)@S=54 DOWN 0v1 (collapse v(54,53,76)=1); (22,30) conform-DEAD at z=53=S+1 (collapse v(52,53,76)=0); death-of-d=4"
 },
 {
  "kind": "birth slice d=6",
  "m": 22,
  "z": 54,
  "prediction": "EXACTLY TWO: stick (22,32) DOWN 0v2 (collapse v(54,54,77)=2) + NEW (22,34)@S=56 UP 2v1 (collapse v(56,54,77)=1), d=6 seat gap 12 (stick seat coincides z=S(d-1))"
 },
 {
  "kind": "one-past-of-d=4 / death-of-d=3",
  "m": 23,
  "z": 54,
  "prediction": "EXACTLY ONE: {23,32}@S=55 UP 1v0 (collapse v(55,54,78)=0); {23,30} conform-DEAD at z=54=S+1 (collapse v(53,54,78)=1); death-of-d=3"
 },
 {
  "kind": "birth slice d=5",
  "m": 23,
  "z": 55,
  "prediction": "EXACTLY TWO: stick {23,32} DOWN 1v2 (collapse v(55,55,79)=2) + NEW {23,34}@S=57 UP 2v0 (collapse v(57,55,79)=0), d=5 seat gap 11 (stick seat coincides z=S(d-1))"
 },
 {
  "kind": "one-past-of-d=4 / death-of-d=3",
  "m": 24,
  "z": 55,
  "prediction": "EXACTLY ONE: (24,32)@S=56 DOWN 0v1 (collapse v(56,55,80)=1); (24,30) conform-DEAD at z=55=S+1 (collapse v(54,55,80)=0); death-of-d=3"
 },
 {
  "kind": "birth slice d=5",
  "m": 24,
  "z": 56,
  "prediction": "EXACTLY TWO: stick (24,32) DOWN 0v2 (collapse v(56,56,81)=2) + NEW (24,34)@S=58 UP 2v1 (collapse v(58,56,81)=1), d=5 seat gap 10 (stick seat coincides z=S(d-1))"
 },
 {
  "kind": "one-past-of-d=3 / death-of-d=2",
  "m": 25,
  "z": 56,
  "prediction": "EXACTLY ONE: {25,32}@S=57 UP 1v0 (collapse v(57,56,82)=0); {25,30} conform-DEAD at z=56=S+1 (collapse v(55,56,82)=1); death-of-d=2"
 },
 {
  "kind": "birth slice d=4",
  "m": 25,
  "z": 57,
  "prediction": "EXACTLY TWO: stick {25,32} DOWN 1v2 (collapse v(57,57,83)=2) + NEW {25,34}@S=59 UP 2v0 (collapse v(59,57,83)=0), d=4 seat gap 9 (stick seat coincides z=S(d-1))"
 },
 {
  "kind": "one-past-of-d=3 / death-of-d=2",
  "m": 26,
  "z": 57,
  "prediction": "EXACTLY ONE: (26,32)@S=58 DOWN 0v1 (collapse v(58,57,84)=1); (26,30) conform-DEAD at z=57=S+1 (collapse v(56,57,84)=0); death-of-d=2"
 },
 {
  "kind": "birth slice d=4",
  "m": 26,
  "z": 58,
  "prediction": "EXACTLY TWO: stick (26,32) DOWN 0v2 (collapse v(58,58,85)=2) + NEW (26,34)@S=60 UP 2v1 (collapse v(60,58,85)=1), d=4 seat gap 8 (stick seat coincides z=S(d-1))"
 },
 {
  "kind": "one-past-of-d=1 / death-of-d=0",
  "m": 27,
  "z": 56,
  "prediction": "EXACTLY ONE: {27,30}@S=57 UP 1v0 (collapse v(57,56,84)=0); {27,28} conform-DEAD at z=56=S+1 (collapse v(55,56,84)=1); death-of-d=0"
 },
 {
  "kind": "birth slice d=2",
  "m": 27,
  "z": 57,
  "prediction": "EXACTLY TWO: stick {27,30} DOWN 1v2 (collapse v(57,57,85)=2) + NEW {27,32}@S=59 UP 2v0 (collapse v(59,57,85)=0), d=2 seat gap 5 (stick seat coincides z=S(d-1))"
 },
 {
  "kind": "one-past-of-d=1 / death-of-d=0",
  "m": 28,
  "z": 57,
  "prediction": "EXACTLY ONE: (28,30)@S=58 DOWN 0v1 (collapse v(58,57,86)=1); (28,28) conform-DEAD at z=57=S+1 (collapse v(56,57,86)=0); death-of-d=0"
 },
 {
  "kind": "birth slice d=2",
  "m": 28,
  "z": 58,
  "prediction": "EXACTLY TWO: stick (28,30) DOWN 0v2 (collapse v(58,58,87)=2) + NEW (28,32)@S=60 UP 2v1 (collapse v(60,58,87)=1), d=2 seat gap 4 (stick seat coincides z=S(d-1))"
 },
 {
  "kind": "one-past of the d=0 seat",
  "m": 29,
  "z": 58,
  "prediction": "EXACTLY ONE: {29,30}@S=59 UP 1v0 (collapse v(59,58,88)=0); one-past of the d=0 seat (frontier decay 2->1)"
 },
 {
  "kind": "birth slice d=1",
  "m": 29,
  "z": 59,
  "prediction": "EXACTLY TWO: stick {29,30} DOWN 1v2 (collapse v(59,59,89)=2) + NEW {29,32}@S=61 UP 2v0 (collapse v(61,59,89)=0), d=1 seat gap 3 (stick seat coincides z=S(d-1))"
 },
 {
  "kind": "one-past-of-d=1 / death-of-d=0",
  "m": 29,
  "z": 60,
  "prediction": "EXACTLY ONE: {29,32}@S=61 UP 1v0 (collapse v(61,60,90)=0); {29,30} conform-DEAD at z=60=S+1 (collapse v(59,60,90)=1); death-of-d=0"
 },
 {
  "kind": "one-past of the d=0 seat",
  "m": 30,
  "z": 59,
  "prediction": "EXACTLY ONE: (30,30)@S=60 DOWN 0v1 (collapse v(60,59,90)=1); one-past of the d=0 seat (frontier decay 2->0)"
 },
 {
  "kind": "birth slice d=1",
  "m": 30,
  "z": 60,
  "prediction": "EXACTLY TWO: stick (30,30) DOWN 0v2 (collapse v(60,60,91)=2) + NEW (30,32)@S=62 UP 2v1 (collapse v(62,60,91)=1), d=1 seat gap 2 (stick seat coincides z=S(d-1))"
 },
 {
  "kind": "one-past-of-d=1 / death-of-d=0",
  "m": 30,
  "z": 61,
  "prediction": "EXACTLY ONE: (30,32)@S=62 DOWN 0v1 (collapse v(62,61,92)=1); (30,30) conform-DEAD at z=61=S+1 (collapse v(60,61,92)=0); death-of-d=0"
 },
 {
  "kind": "frontier first contact proposal (FIRST-EVER m=31 row)",
  "m": 31,
  "z": 61,
  "prediction": "EXACTLY ONE: {31,32}@S=63 UP 2v0 (collapse v(63,61,93)=0); z*(31)=2*31-2+1=61 per K1268 (derive_check double-checked); R=93"
 },
 {
  "kind": "frontier first contact proposal (FIRST-EVER m=32 row)",
  "m": 32,
  "z": 62,
  "prediction": "EXACTLY ONE: (32,32)@S=64 UP 2v1 (collapse v(64,62,95)=1); z*(32)=2*32-2+0=62 per K1268 (derive_check double-checked); R=95"
 }

  , {"kind": "in-band window sweep proposal", "m": 29, "z": "49..56", "prediction": "0 separations each (candidate); z*(29)-8..-1; m=29 is NOT strip-covered; register before measuring"},
  {"kind": "in-band window sweep proposal", "m": 30, "z": "50..57", "prediction": "0 separations each (candidate); z*(30)-8..-1; m=30 is NOT strip-covered; register before measuring"},
  {"kind": "heavy below-window PROPOSAL (not registered, no strip coverage)", "prediction": "m=27 z in {25..44} and m=28 z in {25..45}: NOT strip-covered, unmeasured, unregistered (20/21-row sweeps; may be split; register before measuring)"},
  {"kind": "not registered here — derivable scaffold extensions, register before measuring", "prediction": "the m=25 z in {27..32} and m=26 z in {27..34} scaffold rows REGISTERED AND MEASURED by kit-7 (this kit); if any measured dirty, the fully-swept-line conditionals are void and recorded as datums"}
  ]]})


    # (h) published anchor rechecks (141 spots, verbatim published values)
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
                'label': 'one_hundred_forty_one_published_spots_reproduce_exactly_match_field_is_value_equality_with_published',
                'rows': rechecks,
                'note': 'the separation spots are separations by construction (value != collapse BY DESIGN); the z=25/z=26 base spots are published CONFORM values; the match criterion is equality with the PUBLISHED value'})

    res = {'result': 'EXPLORE-DONE', 'sections': out}
    print(json.dumps(res, sort_keys=True, separators=(',', ':')))


if __name__ == '__main__':
    main()
