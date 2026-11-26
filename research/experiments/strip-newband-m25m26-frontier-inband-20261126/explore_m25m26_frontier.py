"""
explore_m25m26_frontier: FROZEN PRE-DECLARATION census for the LADDER
CONTINUATION of the new bands (the registered kit-4 S5 items m=19@z=
50 / z=51, m=20@z=51 / z=52, m=21@z=46 / z=47, m=22@z=47 / z=48,
m=23@z=48 / z=49, m=24@z=50), the FRONTIER rows m=25 and m=26 (the
registered 13th / 14th parity datum candidates, the FIRST-EVER m=25 /
m=26 rows), and the REGISTERED in-band window sweeps m=23 z in
{36..43} and m=24 z in {38..45}, plus 93 published anchor rechecks.
NO K slot is claimed by this file; the 29 registered measurement
candidates in this docstring were frozen BEFORE the first run of
this file. The only edit performed after any run is the anchor-table
build fix disclosed below (verifier table only; no candidate, engine,
or measurement code was edited at any time).

Registered provenance (all BEFORE any measurement by this kit):
- The eleven ladder rows are the REGISTERED binding candidates of
  the published kit-4 log S5 items (1)-(11) and of its frozen output
  section future_slice_registration_constants (commit fe0a2d01,
  research/log/2026-11-26-m23m24-frontier-belowwindow-predecl-microkit.md),
  verbatim.
- DISCLOSED AT THIS BUILD (dated correction; values unaffected): the
  kit-4 frozen section (f) R-ANNOTATIONS for its two m=22 rows carry
  slips — item (7) quoted collapse v(48,47,68)=1 / v(46,47,68)=0 where
  the mechanical R=m+z+1 gives v(48,47,70)=1 / v(46,47,70)=0, and
  item (8) quoted v(48,48,69)=2 / v(50,48,69)=1 where R=71 gives
  v(48,48,71)=2 / v(50,48,71)=1. The collapse VALUES coincide in both
  annotation windows (the closed form is parity-constant there), so
  the candidate PREDICTIONS are unchanged; this kit quotes the
  CORRECTED R annotations in its candidate texts and battery-checks
  BOTH annotation triples. The kit-4 published bytes are NOT edited
  (series convention).
- DISCLOSED AT THIS BUILD (anchor-table transcription fix, made BEFORE
  the published run; no published artifact and no candidate text is
  affected): the 21 kit-4-sourced anchor entries were first spliced
  into anchor_spec with the separation seat S placed in the R slot
  (the 72 kit-era entries are R-first; the kit-4 separation extraction
  produced S-first 5-tuples). An internal pre-publication check run
  (kept as explore_m25m26_frontier.out.run1, NOT a datum, not
  published) surfaced EXACTLY 15 anchor mismatches, all 15 kit-4-entry
  spots, all false-conform by misreading R; the 21 first fields were
  corrected to the mechanical R=m+z+1, and the corrected spots were
  pre-verified to reproduce all 21 published values EXACTLY (21/21).
  The 29 measurement sections of the internal run and of the published
  run are byte-identical (the audit checks this), and the base-72
  battery literal list and the engine pin are unchanged. The published
  .out is from the corrected file.
- The frontier rows m=25@z=49 ({25,26}@S=51 UP 2v0, collapse
  v(51,49,75)=0) and m=26@z=50 ((26,26)@S=52 UP 2v1, collapse
  v(52,50,77)=1) are the REGISTERED 13th / 14th datum candidates
  (kit-4 S5 item (12)); the z*(m)=2m-2+(m mod 2) arithmetic is
  asserted BEFORE the freeze this time (z*(25)=49, z*(26)=50,
  double-checked: hand once, engine-free derive_check once).
- The in-band window rows m=23 z in {36..43} (R=60..67) and m=24 z
  in {38..45} (R=63..70) are the REGISTERED kit-4 S5 item (13)
  proposals, strip-coverage re-probed at this build: all published
  m=23 / m=24 engine values belong to kit-4's own rows (m=23 z in
  {44..47}, m=24 z in {46..49}) — disjoint slices; the content probes
  returned NO record; the z in {25,26} equivalents remain
  strip-derived clean (z25-min20 strips m in {20..25}, z26-floor20
  m in {20..26}); the m=23 frontier-minus-one row z=44 is measured
  clean by kit-4 (erratum row). Candidate 0 separations each.
- NO kit-added rows are measured in this run; the next-slice
  constants (m=19..m=26 ladder continuations, the m=25 / m=26
  one-past / d=1-birth mini-ladder candidates incl. their FIRST death
  datum candidates, the m=25 / m=26 in-band windows z*(m)-8..-1, and
  the 15th / 16th frontier candidates m=27@z=53 / m=28@z=54) are
  REGISTERED in the frozen section (d) below for the next execution.
  All constants are engine-free paper derivations from the
  scaffolding algebra with R = m+z+1 computed mechanically, derived
  twice (hand + derive_check), battery-checked in this run.

Counter-probe (content-based; re-run at push time against the
then-current main): at kit-build time (2026-11-26T09:15Z, main head
fe0a2d01 — this kit's own predecessor) the content queries
"frontier_m25", "m25_z49", "m26_z50", "inband_m23", "_m23_z36",
"m24_z38", "ladder_m19_z50" return NO measurement record; the
registered constants exist only as registrations in the published
kit-4 log S5 and its frozen section.

(a) K0832 battery: every single-token literal used by this file
    (row stair literals + all candidate constants, including the
    corrected m=22 annotation triples AND the slipped kit-4 triples)
    is checked closed == canonical == ordered.
(b) the eleven registered ladder rows. (b2) the two frontier rows.
(c) the sixteen in-band window rows. (d) future-slice registration
    constants (engine-free, NOT measured here). (h) published anchor
    rechecks (93 spots): the 72 kit-4 anchor spots verbatim + the 21
    kit-4 separation spots (commit fe0a2d01) — must all reproduce
    exactly.

Everything is a pure function of the pinned engine bytes; no
randomness, no hash-seed dependence, no wall-clock in the output.
stdout is the frozen artifact (explore_m25m26_frontier.out).
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
        (74, (24, 26), 49, 0, 'kit-4 (fe0a2d01) one-past-of-d=1 m=24@z=49 separation DOWN 0v1 (first m=24 death row: (24,24) conform-DEAD at z=49=S+1)')
    ]
    # (a) K0832 battery: every single-token literal used by this file.
    battery_lits = []
    rows_stair = []
    meas_rows = [(19, 50), (19, 51), (20, 51), (20, 52),
                 (21, 46), (21, 47), (22, 47), (22, 48),
                 (23, 48), (23, 49), (24, 50), (25, 49), (26, 50)] + \
                [(23, z) for z in range(36, 44)] + \
                [(24, z) for z in range(38, 46)]
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
    # future-slice registration constants (section (d), NOT measured)
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

    # (b) LADDER rows: registered kit-4 S5 items (1)-(11)
    out.append(row_record_x0(
        'ladder_m19_z50_row_record',
        'registered_kit4_S5_item1_one_past_of_d6_death_of_d5',
        {'co_token_19_allowed': True,
         's_domain': '{19..57}', 'arity_max': 3,
         'style': 'x0 published residual-band style',
         'registered_by': 'kit-4 log S5 item (1) + frozen section (commit fe0a2d01)',
         'candidate': 'EXACTLY ONE separation {19,32}@S=51 UP 1v0 (value 1 vs collapse v(51,50,70)=0 on paper); {19,30} conform-DEAD at z=50=S+1 (collapse v(49,50,70)=1); any deviation is the datum'},
        70, 50, 19, 19, 57))
    out.append(row_record_x0(
        'ladder_m19_z51_row_record',
        'registered_kit4_S5_item2_birth_slice_d7',
        {'co_token_19_allowed': True,
         's_domain': '{19..57}', 'arity_max': 3,
         'style': 'x0 published residual-band style',
         'registered_by': 'kit-4 log S5 item (2) + frozen section (commit fe0a2d01)',
         'candidate': 'EXACTLY TWO separations: stick {19,32}@S=51 DOWN 1v2 (collapse v(51,51,71)=2) + NEW {19,34}@S=53 UP 2v0 (collapse v(53,51,71)=0), d=7 seat gap 15; any deviation is the datum'},
        71, 51, 19, 19, 57))
    out.append(row_record_x0(
        'ladder_m20_z51_row_record',
        'registered_kit4_S5_item3_one_past_of_d6_death_of_d5',
        {'co_token_20_allowed': True,
         's_domain': '{20..58}', 'arity_max': 3,
         'style': 'x0 published residual-band style',
         'registered_by': 'kit-4 log S5 item (3) + frozen section (commit fe0a2d01)',
         'candidate': 'EXACTLY ONE separation (20,32)@S=52 DOWN 0v1 (value 0 vs collapse v(52,51,72)=1 on paper); (20,30) conform-DEAD at z=51=S+1 (collapse v(50,51,72)=0); any deviation is the datum'},
        72, 51, 20, 20, 58))
    out.append(row_record_x0(
        'ladder_m20_z52_row_record',
        'registered_kit4_S5_item4_birth_slice_d7',
        {'co_token_20_allowed': True,
         's_domain': '{20..58}', 'arity_max': 3,
         'style': 'x0 published residual-band style',
         'registered_by': 'kit-4 log S5 item (4) + frozen section (commit fe0a2d01)',
         'candidate': 'EXACTLY TWO separations: stick (20,32)@S=52 DOWN 0v2 (collapse v(52,52,73)=2) + NEW (20,34)@S=54 UP 2v1 (collapse v(54,52,73)=1), d=7 seat gap 14; any deviation is the datum'},
        73, 52, 20, 20, 58))
    out.append(row_record_x0(
        'ladder_m21_z46_row_record',
        'registered_kit4_S5_item5_one_past_of_d2_death_of_d1',
        {'co_token_21_allowed': True,
         's_domain': '{21..59}', 'arity_max': 3,
         'style': 'x0 published residual-band style',
         'registered_by': 'kit-4 log S5 item (5) + frozen section (commit fe0a2d01)',
         'candidate': 'EXACTLY ONE separation {21,26}@S=47 UP 1v0 (value 1 vs collapse v(47,46,68)=0 on paper); {21,24} conform-DEAD at z=46=S+1 (collapse v(45,46,68)=1); any deviation is the datum'},
        68, 46, 21, 21, 59))
    out.append(row_record_x0(
        'ladder_m21_z47_row_record',
        'registered_kit4_S5_item6_birth_slice_d3',
        {'co_token_21_allowed': True,
         's_domain': '{21..59}', 'arity_max': 3,
         'style': 'x0 published residual-band style',
         'registered_by': 'kit-4 log S5 item (6) + frozen section (commit fe0a2d01)',
         'candidate': 'EXACTLY TWO separations: stick {21,26}@S=47 DOWN 1v2 (collapse v(47,47,69)=2) + NEW {21,28}@S=49 UP 2v0 (collapse v(49,47,69)=0), d=3 seat gap 7; any deviation is the datum'},
        69, 47, 21, 21, 59))
    out.append(row_record_x0(
        'ladder_m22_z47_row_record',
        'registered_kit4_S5_item7_one_past_of_d2_death_of_d1_R_annotation_corrected',
        {'co_token_22_allowed': True,
         's_domain': '{22..60}', 'arity_max': 3,
         'style': 'x0 published residual-band style',
         'registered_by': 'kit-4 log S5 item (7) + frozen section (commit fe0a2d01), R annotation CORRECTED at this build (disclosed in the docstring): collapse v(48,47,70), value unchanged; the kit-4 (f) quoted v(48,47,68) — an annotation slip, battery checks both triples',
         'candidate': 'EXACTLY ONE separation (22,26)@S=48 DOWN 0v1 (value 0 vs collapse v(48,47,70)=1 on paper — R corrected from the kit-4 (f) slip v(48,47,68), value unchanged); (22,24) conform-DEAD at z=47=S+1 (collapse v(46,47,70)=0); any deviation is the datum'},
        70, 47, 22, 22, 60))
    out.append(row_record_x0(
        'ladder_m22_z48_row_record',
        'registered_kit4_S5_item8_birth_slice_d3_R_annotation_corrected',
        {'co_token_22_allowed': True,
         's_domain': '{22..60}', 'arity_max': 3,
         'style': 'x0 published residual-band style',
         'registered_by': 'kit-4 log S5 item (8) + frozen section (commit fe0a2d01), R annotations CORRECTED at this build (disclosed): collapses v(48,48,71) / v(50,48,71), values unchanged; the kit-4 (f) quoted R=69 — an annotation slip',
         'candidate': 'EXACTLY TWO separations: stick (22,26)@S=48 DOWN 0v2 (collapse v(48,48,71)=2 — R corrected from the kit-4 (f) slip v(48,48,69), value unchanged) + NEW (22,28)@S=50 UP 2v1 (collapse v(50,48,71)=1 — corrected likewise), d=3 seat gap 6; any deviation is the datum'},
        71, 48, 22, 22, 60))
    out.append(row_record_x0(
        'ladder_m23_z48_row_record',
        'registered_kit4_S5_item9_one_past_of_d1_death_of_d0_first_m23_death',
        {'co_token_23_allowed': True,
         's_domain': '{23..61}', 'arity_max': 3,
         'style': 'x0 published residual-band style',
         'registered_by': 'kit-4 log S5 item (9) + frozen section (commit fe0a2d01)',
         'candidate': 'EXACTLY ONE separation {23,26}@S=49 UP 1v0 (value 1 vs collapse v(49,48,72)=0 on paper); {23,24} conform-DEAD at z=48=S+1 (collapse v(47,48,72)=1) — the FIRST m=23 death datum (d=0 shape); any deviation is the datum'},
        72, 48, 23, 23, 61))
    out.append(row_record_x0(
        'ladder_m23_z49_row_record',
        'registered_kit4_S5_item10_birth_slice_d2',
        {'co_token_23_allowed': True,
         's_domain': '{23..61}', 'arity_max': 3,
         'style': 'x0 published residual-band style',
         'registered_by': 'kit-4 log S5 item (10) + frozen section (commit fe0a2d01)',
         'candidate': 'EXACTLY TWO separations: stick {23,26}@S=49 DOWN 1v2 (collapse v(49,49,73)=2) + NEW {23,28}@S=51 UP 2v0 (collapse v(51,49,73)=0), d=2 seat gap 5; any deviation is the datum'},
        73, 49, 23, 23, 61))
    out.append(row_record_x0(
        'ladder_m24_z50_row_record',
        'registered_kit4_S5_item11_birth_slice_d2_stick_coincides',
        {'co_token_24_allowed': True,
         's_domain': '{24..62}', 'arity_max': 3,
         'style': 'x0 published residual-band style',
         'registered_by': 'kit-4 log S5 item (11) + frozen section (commit fe0a2d01)',
         'candidate': 'EXACTLY TWO separations: stick (24,26)@S=50 DOWN 0v2 (collapse v(50,50,75)=2) + NEW (24,28)@S=52 UP 2v1 (collapse v(52,50,75)=1), d=2 seat gap 4; any deviation is the datum'},
        75, 50, 24, 24, 62))

    # (b2) FRONTIER rows m=25 / m=26 (13th / 14th datum candidates,
    #      FIRST-EVER m=25 / m=26 rows)
    out.append(row_record_x0(
        'frontier_m25_z49_row_record',
        'registered_frontier_record_m25_z49_K1268_13th_datum_candidate',
        {'co_token_25_allowed': True,
         's_domain': '{25..63}', 'arity_max': 3,
         'style': 'x0 published residual-band style',
         'registered_by': 'kit-4 log S5 item (12) + frozen section (commit fe0a2d01), z* arithmetic double-checked at this build',
         'candidate': 'EXACTLY ONE separation X={25,26} @S=51, UP 2v0 (value 2 vs collapse v(51,49,75)=0 on paper); all other shapes conform; the parity frontier law is 12/12 through m=24; any deviation is the datum and is recorded verbatim',
         'z_star': 'z*(25)=2*25-2+1=49 EXACTLY (K1268; hand + derive_check double assertion at this build)'},
        75, 49, 25, 25, 63))
    out.append(row_record_x0(
        'frontier_m26_z50_row_record',
        'registered_frontier_record_m26_z50_K1268_14th_datum_candidate',
        {'co_token_26_allowed': True,
         's_domain': '{26..64}', 'arity_max': 3,
         'style': 'x0 published residual-band style',
         'registered_by': 'kit-4 log S5 item (12) + frozen section (commit fe0a2d01), z* arithmetic double-checked at this build',
         'candidate': 'EXACTLY ONE separation X=(26,26) @S=52, UP 2v1 (value 2 vs collapse v(52,50,77)=1 on paper); all other shapes conform; any deviation is the datum',
         'z_star': 'z*(26)=2*26-2+0=50 EXACTLY (K1268; hand + derive_check double assertion at this build)'},
        77, 50, 26, 26, 64))

    # (c) IN-BAND window rows (REGISTERED kit-4 S5 item (13),
    #     strip coverage re-probed at this build: free slices)
    for z in range(36, 44):
        R = 23 + z + 1
        out.append(row_record_x0(
            'inband_m23_z%d_row_record' % z,
            'inband_window_m23_z%d' % z,
            {'co_token_23_allowed': True,
             's_domain': '{23..61}', 'arity_max': 3,
             'style': 'x0 published residual-band style',
             'registered_by': 'kit-4 log S5 item (13) (commit fe0a2d01), strip coverage re-probed at this build',
             'candidate': '0 separations (in-band-clean precedent)',
             'band': 'm=23 in-band window pinning: z in {36..43} here; measured slices now z in {36..43} window + {44} frontier-minus-one (clean, kit-4 erratum row) + {45..47} frontier/mini-ladder (kit-4) + {48,49} here; z in {25,26} strip-derived clean'},
            R, z, 23, 23, 61))
    for z in range(38, 46):
        R = 24 + z + 1
        out.append(row_record_x0(
            'inband_m24_z%d_row_record' % z,
            'inband_window_m24_z%d' % z,
            {'co_token_24_allowed': True,
             's_domain': '{24..62}', 'arity_max': 3,
             'style': 'x0 published residual-band style',
             'registered_by': 'kit-4 log S5 item (13) (commit fe0a2d01), strip coverage re-probed at this build',
             'candidate': '0 separations (in-band-clean precedent)',
             'band': 'm=24 in-band window pinning: z in {38..45} here; measured slices now z in {38..45} window + {46..49} frontier/mini-ladder (kit-4) + {50} here; z in {25,26} strip-derived clean'},
            R, z, 24, 24, 62))

    # (d) future-slice registration constants (engine-free, NOT measured)
    out.append({'section': 'future_slice_registration_constants',
                'label': 'engine_free_paper_only_K0832_closed_form_next_slice_predictions_NOT_measured_here',
                'registered_for_next_execution_kit_log_S5': [
                    {'m': 19, 'z': 52, 'kind': 'one-past-of-d=7 / death-of-d=6',
                     'prediction': 'EXACTLY ONE: {19,34}@S=53 UP 1v0 (collapse v(53,52,72)=0); {19,32} conform-DEAD at z=52=S+1 (collapse v(51,52,72)=1)'},
                    {'m': 19, 'z': 53, 'kind': 'birth slice d=8',
                     'prediction': 'EXACTLY TWO: stick {19,34} DOWN 1v2 (collapse v(53,53,73)=2) + NEW {19,36}@S=55 UP 2v0 (collapse v(55,53,73)=0), d=8 seat gap 17'},
                    {'m': 20, 'z': 53, 'kind': 'one-past-of-d=7 / death-of-d=6',
                     'prediction': 'EXACTLY ONE: (20,34)@S=54 DOWN 0v1 (collapse v(54,53,74)=1); (20,32) conform-DEAD at z=53=S+1 (collapse v(52,53,74)=0)'},
                    {'m': 20, 'z': 54, 'kind': 'birth slice d=8',
                     'prediction': 'EXACTLY TWO: stick (20,34) DOWN 0v2 (collapse v(54,54,75)=2) + NEW (20,36)@S=56 UP 2v1 (collapse v(56,54,75)=1), d=8 seat gap 16'},
                    {'m': 21, 'z': 48, 'kind': 'one-past-of-d=3 / death-of-d=2',
                     'prediction': 'EXACTLY ONE: {21,28}@S=49 UP 1v0 (collapse v(49,48,70)=0); {21,26} conform-DEAD at z=48=S+1 (collapse v(47,48,70)=1)'},
                    {'m': 21, 'z': 49, 'kind': 'birth slice d=4',
                     'prediction': 'EXACTLY TWO: stick {21,28} DOWN 1v2 (collapse v(49,49,71)=2) + NEW {21,30}@S=51 UP 2v0 (collapse v(51,49,71)=0), d=4 seat gap 9'},
                    {'m': 22, 'z': 49, 'kind': 'one-past-of-d=3 / death-of-d=2',
                     'prediction': 'EXACTLY ONE: (22,28)@S=50 DOWN 0v1 (collapse v(50,49,72)=1); (22,26) conform-DEAD at z=49=S+1 (collapse v(48,49,72)=0)'},
                    {'m': 22, 'z': 50, 'kind': 'birth slice d=4',
                     'prediction': 'EXACTLY TWO: stick (22,28) DOWN 0v2 (collapse v(50,50,73)=2) + NEW (22,30)@S=52 UP 2v1 (collapse v(52,50,73)=1), d=4 seat gap 8'},
                    {'m': 23, 'z': 50, 'kind': 'one-past-of-d=2 / death-of-d=1',
                     'prediction': 'EXACTLY ONE: {23,28}@S=51 UP 1v0 (collapse v(51,50,74)=0); {23,26} conform-DEAD at z=50=S+1 (collapse v(49,50,74)=1)'},
                    {'m': 23, 'z': 51, 'kind': 'birth slice d=3',
                     'prediction': 'EXACTLY TWO: stick {23,28} DOWN 1v2 (collapse v(51,51,75)=2) + NEW {23,30}@S=53 UP 2v0 (collapse v(53,51,75)=0), d=3 seat gap 7'},
                    {'m': 24, 'z': 51, 'kind': 'one-past-of-d=2 / death-of-d=1',
                     'prediction': 'EXACTLY ONE: (24,28)@S=52 DOWN 0v1 (collapse v(52,51,76)=1); (24,26) conform-DEAD at z=51=S+1 (collapse v(50,51,76)=0)'},
                    {'m': 24, 'z': 52, 'kind': 'birth slice d=3',
                     'prediction': 'EXACTLY TWO: stick (24,28) DOWN 0v2 (collapse v(52,52,77)=2) + NEW (24,30)@S=54 UP 2v1 (collapse v(54,52,77)=1), d=3 seat gap 6'},
                    {'m': 25, 'z': 50, 'kind': 'one-past of the d=0 seat',
                     'prediction': 'EXACTLY ONE: {25,26}@S=51 UP 1v0 (collapse v(51,50,76)=0)'},
                    {'m': 25, 'z': 51, 'kind': 'birth slice d=1 (stick coincides: S(d0)=51=z)',
                     'prediction': 'EXACTLY TWO: stick {25,26} DOWN 1v2 (collapse v(51,51,77)=2) + NEW {25,28}@S=53 UP 2v0 (collapse v(53,51,77)=0), d=1 seat gap 3'},
                    {'m': 25, 'z': 52, 'kind': 'one-past-of-d=1 / death-of-d=0 — the FIRST m=25 death datum candidate',
                     'prediction': 'EXACTLY ONE: {25,28}@S=53 UP 1v0 (collapse v(53,52,78)=0); {25,26} conform-DEAD at z=52=S+1 (collapse v(51,52,78)=1)'},
                    {'m': 26, 'z': 51, 'kind': 'one-past of the d=0 seat',
                     'prediction': 'EXACTLY ONE: (26,26)@S=52 DOWN 0v1 (collapse v(52,51,78)=1)'},
                    {'m': 26, 'z': 52, 'kind': 'birth slice d=1 (stick coincides: S(d0)=52=z)',
                     'prediction': 'EXACTLY TWO: stick (26,26) DOWN 0v2 (collapse v(52,52,79)=2) + NEW (26,28)@S=54 UP 2v1 (collapse v(54,52,79)=1), d=1 seat gap 2'},
                    {'m': 26, 'z': 53, 'kind': 'one-past-of-d=1 / death-of-d=0 — the FIRST m=26 death datum candidate',
                     'prediction': 'EXACTLY ONE: (26,28)@S=54 DOWN 0v1 (collapse v(54,53,80)=1); (26,26) conform-DEAD at z=53=S+1 (collapse v(52,53,80)=0)'},
                    {'m': 25, 'z': '41..48', 'kind': 'in-band window sweep proposal',
                     'prediction': '0 separations each (candidate); z*(25)-8..-1; strip-coverage re-probe at build time; the z=48 frontier-minus-one row is included here (precedent: measured clean for m=13..23 one-below the frontier)'},
                    {'m': 26, 'z': '43..50', 'kind': 'in-band window sweep proposal',
                     'prediction': '0 separations each (candidate); z*(26)-8..-1; re-probe strip coverage at build time'},
                    {'m': 27, 'z': 53, 'kind': 'frontier first contact proposal (FIRST-EVER m=27 row)',
                     'prediction': 'EXACTLY ONE: {27,28}@S=55 UP 2v0 (collapse v(55,53,81)=0); z*(27)=2*27-2+1=53 per K1268 (derive_check double-checked); R=81; the 15th datum candidate'},
                    {'m': 28, 'z': 54, 'kind': 'frontier first contact proposal (FIRST-EVER m=28 row)',
                     'prediction': 'EXACTLY ONE: (28,28)@S=56 UP 2v1 (collapse v(56,54,83)=1); z*(28)=2*28-2+0=54 per K1268 (derive_check double-checked); R=83; the 16th datum candidate'},
                    {'kind': 'not registered here — derivable scaffold extensions, register before measuring',
                     'prediction': 'below-window rows m=25 z in {27..40} and m=26 z in {27..42}: NOT registered by this kit; m=25/m=26 z in {25,26} are strip-derived clean (z25-min20 strips m in {20..25}, z26-floor20 m in {20..26})'}]})

    # (h) published anchor rechecks (93 spots, verbatim published values)
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
                'label': 'ninety_three_published_spots_reproduce_exactly_match_field_is_value_equality_with_published',
                'rows': rechecks,
                'note': 'the separation spots are separations by construction (value != collapse BY DESIGN); the z=25/z=26 base spots are published CONFORM values; the match criterion is equality with the PUBLISHED value'})

    res = {'result': 'EXPLORE-DONE', 'sections': out}
    print(json.dumps(res, sort_keys=True, separators=(',', ':')))


if __name__ == '__main__':
    main()
