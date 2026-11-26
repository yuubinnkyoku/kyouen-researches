"""
explore_frontier_m21m22: FROZEN PRE-DECLARATION census for the LADDER
CONTINUATION of the NEW m=19 / m=20 residual bands (the registered
items m=19@z=44 / z=45 and m=20@z=45 / z=46, plus the kit-added
m=19@z=46 / z=47 and m=20@z=47 / z=48) AND the FIRST-EVER m=21 /
m=22 rows (the registered FRONTIER candidates m=21@z=41 and
m=22@z=42 — the parity frontier law 9th / 10th datum candidates —
plus the kit-added one-past and d=1-birth mini-ladder rows
m=21@z=42 / z=43 and m=22@z=43 / z=44, and the registered in-band
window sweeps m=21 z in {33..40} and m=22 z in {34..41}), plus 52
published anchor rechecks. NO K slot is claimed by this file; the
constants below were frozen into this docstring BEFORE the first
run of this file and the file has not been edited after any of its
runs.

Registered provenance (all BEFORE any measurement by this kit):
- The four rows m=19@z=44 and z=45, m=20@z=45 and z=46 are the
  REGISTERED binding candidates of the published newband-ladders
  kit log section 5 items (1)-(4) and of its frozen output section
  future_slice_registration_constants (commit 637d15e1,
  research/log/2026-11-26-newband-ladders-bandstart-predecl-
  microkit.md), verbatim:
  * m=19@z=44: EXACTLY ONE {19,26}@S=45 UP 1v0 (odd decay 2->1 of
    the d=3 birth; collapse v(45,44,64)=0) with {19,24}
    conform-DEAD at its birth+3 (collapse v(43,44,64)=1) — the
    second m=19 death datum class (d=2 shape).
  * m=19@z=45 (birth slice d=4): EXACTLY TWO: stick {19,26}@S=45
    DOWN 1v2 (collapse v(45,45,65)=2) + NEW {19,28}@S=47 UP 2v0
    (collapse v(47,45,65)=0), d=4 seat gap 9.
  * m=20@z=45: EXACTLY ONE (20,26)@S=46 DOWN 0v1 (even decay 2->0;
    collapse v(46,45,66)=1) with (20,24) conform-DEAD at its
    birth+3 (collapse v(44,45,66)=0) — the second m=20 death datum
    class (d=2 shape).
  * m=20@z=46 (birth slice d=4): EXACTLY TWO: stick (20,26)@S=46
    DOWN 0v2 (collapse v(46,46,67)=2) + NEW (20,28)@S=48 UP 2v1
    (collapse v(48,46,67)=1), d=4 seat gap 8.
- The FRONTIER rows m=21@z=41 and m=22@z=42 and the IN-BAND window
  sweeps m=21 z in {33..40} / m=22 z in {34..41} are the REGISTERED
  items (5) of the same published log section 5 (commit 637d15e1),
  verbatim binding candidates:
  * m=21@z=41 (z*(21)=2*21-2+1=41 per K1268, R=63): EXACTLY ONE
    {21,22}@S=43 UP 2v0 (collapse v(43,41,63)=0) — the parity
    frontier law 9th datum candidate (8/8 through m=20).
  * m=22@z=42 (z*(22)=42, R=65): EXACTLY ONE (22,22)@S=44 UP 2v1
    (collapse v(44,42,65)=1) — the 10th datum candidate.
  * window rows: 0 separations each (in-band-clean precedent), with
    the strip-coverage caveat registered there and re-probed at
    THIS build: verified by content probe that no z=33..41 census
    kit exists (the census series stops at z=26) and that every
    published z=33..41 engine value belongs to m<=20 row records /
    touch quads with a part < 21 (the decay-z29-z35, fifthwave and
    sixthwave kits published only m=13..18 past-side rows and
    m=16..18 quad spots at z=29..35, plus single-token supply
    closed forms; all disjoint from the all-parts->=21 rows
    measured here). The z=33 touch registered to the wave lane
    contains only tokens <= 18, disjoint.
- The four rows m=19@z=46 and z=47, m=20@z=47 and z=48 and the four
  m=21/m=22 one-past / d=1-birth rows m=21@z=42 and z=43, m=22@z=43
  and z=44 are KIT-ADDED here, derived BEFORE the freeze from the
  published six-band separation life-cycle scaffold (the exact
  kit-1/kit-2 one-past/two-past precedent). Binding candidates:
  * m=19@z=46: EXACTLY ONE {19,28}@S=47 UP 1v0 (collapse
    v(47,46,66)=0) with {19,26} conform-DEAD at its birth+3
    (collapse v(45,46,66)=1).
  * m=19@z=47 (birth slice d=5): EXACTLY TWO: stick {19,28}@S=47
    DOWN 1v2 (collapse v(47,47,67)=2) + NEW {19,30}@S=49 UP 2v0
    (collapse v(49,47,67)=0), d=5 seat gap 11.
  * m=20@z=47: EXACTLY ONE (20,28)@S=48 DOWN 0v1 (collapse
    v(48,47,68)=1) with (20,26) conform-DEAD at its birth+3
    (collapse v(46,47,68)=0).
  * m=20@z=48 (birth slice d=5): EXACTLY TWO: stick (20,28)@S=48
    DOWN 0v2 (collapse v(48,48,69)=2) + NEW (20,30)@S=50 UP 2v1
    (collapse v(50,48,69)=1), d=5 seat gap 10.
  * m=21@z=42: EXACTLY ONE {21,22}@S=43 UP 1v0 (odd decay 2->1;
    collapse v(43,42,64)=0).
  * m=21@z=43 (birth slice d=1): EXACTLY TWO: stick {21,22}@S=43
    DOWN 1v2 (collapse v(43,43,65)=2 — the z==x collapse jump) +
    NEW {21,24}@S=45 UP 2v0 (collapse v(45,43,65)=0), d=1 seat
    gap 3.
  * m=22@z=43: EXACTLY ONE (22,22)@S=44 DOWN 0v1 (even decay 2->0;
    collapse v(44,43,65)=1).
  * m=22@z=44 (birth slice d=1): EXACTLY TWO: stick (22,22)@S=44
    DOWN 0v2 (collapse v(44,44,67)=2) + NEW (22,24)@S=46 UP 2v1
    (collapse v(46,44,67)=1), d=1 seat gap 2.

Counter-probe (content-based; re-run at push time against the
then-current main): at kit-build time (2026-11-26T08:57Z, main head
7fc6727e — the unrelated n11 sixth-cost batch publications on top of
this kit's kit-2 predecessor 637d15e1, intact in history) the
content queries
"frontier_m21", "m21_z41", "m22_z42", "ladder_m19_z46", "m19_z46",
"m20_z47", "inband_m21_z33", "inband_m22_z34" return NO measurement
record; the registered constants exist only as registrations in the
published kit-2 log S5 and frozen section. The z=25 / z=26 strip
coverage of m=21 / m=22 (the z25-min20 kit strips m in {20..25}
and z26-floor20 strips m in {20..26}) means the m=21/m=22 rows at
z in {25,26} are derivable-clean and NOT measured here; the window
sweeps start at z=33 (m=21) / z=34 (m=22), with the below-window
slices z in {27..32} (m=21) / {27..33} (m=22) registered for the
next execution (probe at build time).

HONEST DISCLOSURE (paper arithmetic, before the freeze): every
collapse constant stated below is the PROVED K0832 single-token
closed form computed on paper (engine-free), re-derived twice;
the quoted published anchor values are verbatim citations of the
published logs read BEFORE the freeze. NO engine recursion on ANY
position listed below was evaluated before the freeze — every
engine value in the sections (b)..(f) is touched for the FIRST
time at the frozen first run; the sole exceptions are the 52
published anchor spots of section (g) (the 40 kit-2 anchors + the
12 kit-2 ladder separation spots of commit 637d15e1), which must
reproduce their published values exactly.

Scope (this file measures and reports; it proves nothing by
itself):

  (a) K0832 battery: every single-token literal used by this
      file's candidate constants, the staircase samples for every
      measured row, the future-slice registration constants, and
      the anchor collapses — closed-form vs canonical-engine vs
      ordered-engine. Candidate: all match.
  (b) LADDER rows m=19@z in {44,45,46,47} (R=64..67) and m=20@z
      in {45,46,47,48} (R=66..69), x0 published residual-band
      style (X = parts(S, m, 3), X[0] == m, co-token m allowed,
      arity <= 3 TOTAL, S in {m..m+38}). Registered candidates for
      z=44/45 (m=19) and z=45/46 (m=20); kit-added candidates for
      z=46/47 (m=19) and z=47/48 (m=20). Any deviation is the
      datum, recorded verbatim.
  (c) FRONTIER rows m=21@z=41 (R=63) and m=22@z=42 (R=65), same
      x0 style, S in {21..59} / {22..60}: REGISTERED candidates
      EXACTLY ONE each. These are the FIRST-EVER m=21 / m=22 rows.
  (d) FRONTIER one-past and d=1-birth rows m=21@z=42 / z=43 and
      m=22@z=43 / z=44 (KIT-ADDED, same-run, kit-1 precedent).
  (e) IN-BAND window sweeps m=21 z in {33..40} (R=m+z+1 each:
      R in {55..62}) and m=22 z in {34..41} (R in {57..64}),
      REGISTERED candidates 0 separations each.
  (f) FUTURE-SLICE REGISTRATION CONSTANTS (paper-only,
      engine-free, battery-checked, NOT measured): m=19@z=48
      one-past-of-d=5 EXACTLY ONE {19,30}@S=49 UP 1v0 (collapse
      v(49,48,68)=0) with {19,28} conform-DEAD (v(47,48,68)=1);
      m=19@z=49 birth d=6 EXACTLY TWO: stick {19,30} DOWN 1v2
      (v(49,49,69)=2) + NEW {19,32}@S=51 UP 2v0 (v(51,49,69)=0),
      gap 13; m=20@z=49 one-past-of-d=5 EXACTLY ONE (20,30)@S=50
      DOWN 0v1 (v(50,49,70)=1) with (20,28) conform-DEAD
      (v(48,49,70)=0); m=20@z=50 birth d=6 EXACTLY TWO: stick
      (20,30) DOWN 0v2 (v(50,50,71)=2) + NEW (20,32)@S=52 UP 2v1
      (v(52,50,71)=1), gap 12; m=21@z=44 one-past-of-d=1 EXACTLY
      ONE {21,24}@S=45 UP 1v0 (v(45,44,66)=0) with {21,22}
      conform-DEAD (v(43,44,66)=1); m=21@z=45 birth d=2 EXACTLY
      TWO: stick {21,24} DOWN 1v2 (v(45,45,67)=2) + NEW
      {21,26}@S=47 UP 2v0 (v(47,45,67)=0), gap 5; m=22@z=45
      one-past-of-d=1 EXACTLY ONE (22,24)@S=46 DOWN 0v1
      (v(46,45,68)=1) with (22,22) conform-DEAD (v(44,45,68)=0);
      m=22@z=46 birth d=2 EXACTLY TWO: stick (22,24) DOWN 0v2
      (v(46,46,69)=2) + NEW (22,26)@S=48 UP 2v1 (v(48,46,69)=1),
      gap 4; PLUS the frontier proposals m=23@z=44 (z*(23)=44,
      R=68): EXACTLY ONE {23,24}@S=47 UP 2v0 (collapse
      v(47,44,68)=0) — the 11th datum candidate; m=24@z=46
      (z*(24)=46, R=71): EXACTLY ONE (24,24)@S=48 UP 2v1 (collapse
      v(48,46,71)=1) — the 12th; AND the below-window proposals
      m=21 z in {27..32} / m=22 z in {27..33} (candidates 0
      separations; strip-derivation covers z in {25,26} via the
      z25-min20 / z26-floor20 strips; probe at build time).
  (g) published anchor rechecks (52 spots): the 40 kit-2 anchor
      spots verbatim + the 12 kit-2 ladder separation spots
      (commit 637d15e1) — must all reproduce exactly.

Everything is a pure function of the pinned engine bytes; no
randomness, no hash-seed dependence, no wall-clock in the output.
stdout is the frozen artifact (explore_frontier_m21m22.out).
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

    # (a) K0832 battery: every single-token literal used by this file.
    battery_lits = []
    rows_stair = []
    meas_rows = [(19, 44), (19, 45), (19, 46), (19, 47),
                 (20, 45), (20, 46), (20, 47), (20, 48),
                 (21, 33), (21, 34), (21, 35), (21, 36), (21, 37),
                 (21, 38), (21, 39), (21, 40), (21, 41), (21, 42),
                 (21, 43),
                 (22, 34), (22, 35), (22, 36), (22, 37), (22, 38),
                 (22, 39), (22, 40), (22, 41), (22, 42), (22, 43),
                 (22, 44)]
    for (m, z) in meas_rows:
        R = m + z + 1
        for S in (m, m + 2, 2 * m, 2 * m + 1, m + 37, m + 38):
            battery_lits.append((S, z, R))
        rows_stair.append((m, z, R))
    # ladder candidate collapse constants (registered + kit-added)
    for (x, z2, R2) in [
            (45, 44, 64), (43, 44, 64), (47, 45, 65), (45, 45, 65),
            (46, 45, 66), (44, 45, 66), (48, 46, 67), (46, 46, 67),
            (47, 46, 66), (45, 46, 66), (47, 47, 67), (49, 47, 67),
            (48, 47, 68), (46, 47, 68), (48, 48, 69), (50, 48, 69)]:
        battery_lits.append((x, z2, R2))
    # m=21/m=22 frontier + one-past + d=1-birth candidate constants
    for (x, z2, R2) in [
            (43, 41, 63), (44, 42, 65),
            (43, 42, 64), (43, 43, 65), (45, 43, 65),
            (44, 43, 65), (44, 44, 67), (46, 44, 67)]:
        battery_lits.append((x, z2, R2))
    # future-slice registration constants (section (f), NOT measured)
    for (x, z2, R2) in [
            (49, 48, 68), (47, 48, 68), (49, 49, 69), (51, 49, 69),
            (50, 49, 70), (48, 49, 70), (50, 50, 71), (52, 50, 71),
            (45, 44, 66), (43, 44, 66), (45, 45, 67), (47, 45, 67),
            (46, 45, 68), (44, 45, 68), (46, 46, 69), (48, 46, 69),
            (47, 44, 68), (48, 46, 71)]:
        battery_lits.append((x, z2, R2))
    # anchor collapse literals (section (g))
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
        (65, (20, 26), 44, 2, 'kit-2 (637d15e1) ladder m=20@z=44 d=3 birth separation UP 2v1')]
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

    # (b) LADDER rows (x0 published residual-band style)
    out.append(row_record_x0(
        'ladder_m19_z44_row_record',
        'registered_kit2_S5_item1_one_past_of_d3_death_of_d2',
        {'co_token_19_allowed': True,
         's_domain': '{19..57}', 'arity_max': 3,
         'style': 'x0 published residual-band style',
         'registered_by': 'kit-2 log S5 item (1) + frozen section (commit 637d15e1)',
         'candidate': 'EXACTLY ONE separation {19,26}@S=45 UP 1v0 (value 1 vs collapse v(45,44,64)=0 on paper); {19,24} conform-DEAD at its birth+3 (collapse v(43,44,64)=1, expected value 1); any deviation is the datum'},
        64, 44, 19, 19, 57))
    out.append(row_record_x0(
        'ladder_m19_z45_row_record',
        'registered_kit2_S5_item2_birth_slice_d4',
        {'co_token_19_allowed': True,
         's_domain': '{19..57}', 'arity_max': 3,
         'style': 'x0 published residual-band style',
         'registered_by': 'kit-2 log S5 item (2) + frozen section (commit 637d15e1)',
         'candidate': 'EXACTLY TWO separations: stick {19,26}@S=45 DOWN 1v2 (collapse v(45,45,65)=2) + NEW {19,28}@S=47 UP 2v0 (collapse v(47,45,65)=0), d=4 seat gap 9; any deviation is the datum'},
        65, 45, 19, 19, 57))
    out.append(row_record_x0(
        'ladder_m19_z46_row_record',
        'kit_added_one_past_of_d4_death_of_d3',
        {'co_token_19_allowed': True,
         's_domain': '{19..57}', 'arity_max': 3,
         'style': 'x0 published residual-band style',
         'registered_by': 'kit-added (six-band life-cycle scaffold + kit-1/kit-2 ladder precedent, registered in this docstring before the freeze, measured in the same run)',
         'candidate': 'EXACTLY ONE separation {19,28}@S=47 UP 1v0 (value 1 vs collapse v(47,46,66)=0 on paper); {19,26} conform-DEAD at its birth+3 (collapse v(45,46,66)=1, expected value 1); any deviation is the datum'},
        66, 46, 19, 19, 57))
    out.append(row_record_x0(
        'ladder_m19_z47_row_record',
        'kit_added_birth_slice_d5',
        {'co_token_19_allowed': True,
         's_domain': '{19..57}', 'arity_max': 3,
         'style': 'x0 published residual-band style',
         'registered_by': 'kit-added (six-band life-cycle scaffold + kit-1/kit-2 ladder precedent, registered in this docstring before the freeze, measured in the same run)',
         'candidate': 'EXACTLY TWO separations: stick {19,28}@S=47 DOWN 1v2 (collapse v(47,47,67)=2) + NEW {19,30}@S=49 UP 2v0 (collapse v(49,47,67)=0), d=5 seat gap 11; any deviation is the datum'},
        67, 47, 19, 19, 57))
    out.append(row_record_x0(
        'ladder_m20_z45_row_record',
        'registered_kit2_S5_item3_one_past_of_d3_death_of_d2',
        {'co_token_20_allowed': True,
         's_domain': '{20..58}', 'arity_max': 3,
         'style': 'x0 published residual-band style',
         'registered_by': 'kit-2 log S5 item (3) + frozen section (commit 637d15e1)',
         'candidate': 'EXACTLY ONE separation (20,26)@S=46 DOWN 0v1 (value 0 vs collapse v(46,45,66)=1 on paper); (20,24) conform-DEAD at its birth+3 (collapse v(44,45,66)=0, expected value 0); any deviation is the datum'},
        66, 45, 20, 20, 58))
    out.append(row_record_x0(
        'ladder_m20_z46_row_record',
        'registered_kit2_S5_item4_birth_slice_d4',
        {'co_token_20_allowed': True,
         's_domain': '{20..58}', 'arity_max': 3,
         'style': 'x0 published residual-band style',
         'registered_by': 'kit-2 log S5 item (4) + frozen section (commit 637d15e1)',
         'candidate': 'EXACTLY TWO separations: stick (20,26)@S=46 DOWN 0v2 (collapse v(46,46,67)=2) + NEW (20,28)@S=48 UP 2v1 (collapse v(48,46,67)=1), d=4 seat gap 8; any deviation is the datum'},
        67, 46, 20, 20, 58))
    out.append(row_record_x0(
        'ladder_m20_z47_row_record',
        'kit_added_one_past_of_d4_death_of_d3',
        {'co_token_20_allowed': True,
         's_domain': '{20..58}', 'arity_max': 3,
         'style': 'x0 published residual-band style',
         'registered_by': 'kit-added (six-band life-cycle scaffold + kit-1/kit-2 ladder precedent, registered in this docstring before the freeze, measured in the same run)',
         'candidate': 'EXACTLY ONE separation (20,28)@S=48 DOWN 0v1 (value 0 vs collapse v(48,47,68)=1 on paper); (20,26) conform-DEAD at its birth+3 (collapse v(46,47,68)=0, expected value 0); any deviation is the datum'},
        68, 47, 20, 20, 58))
    out.append(row_record_x0(
        'ladder_m20_z48_row_record',
        'kit_added_birth_slice_d5',
        {'co_token_20_allowed': True,
         's_domain': '{20..58}', 'arity_max': 3,
         'style': 'x0 published residual-band style',
         'registered_by': 'kit-added (six-band life-cycle scaffold + kit-1/kit-2 ladder precedent, registered in this docstring before the freeze, measured in the same run)',
         'candidate': 'EXACTLY TWO separations: stick (20,28)@S=48 DOWN 0v2 (collapse v(48,48,69)=2) + NEW (20,30)@S=50 UP 2v1 (collapse v(50,48,69)=1), d=5 seat gap 10; any deviation is the datum'},
        69, 48, 20, 20, 58))

    # (c) FRONTIER rows — the FIRST-EVER m=21 / m=22 rows (REGISTERED)
    out.append(row_record_x0(
        'frontier_m21_z41_row_record',
        'first_ever_m21_row_frontier_registered_parity_candidate_odd_K1268_9th_datum',
        {'co_token_21_allowed': True,
         's_domain': '{21..59}', 'arity_max': 3,
         'style': 'x0 published residual-band style',
         'registered_by': 'kit-2 log S5 item (5) (commit 637d15e1): m=21@z=41 prediction {21,22}@S=43 UP 2v0, collapse v(43,41,63)=0',
         'candidate': 'EXACTLY ONE separation X={21,22} @S=43, UP 2v0 (value 2 vs collapse v(43,41,63)=0 on paper); all other shapes conform; the parity frontier law is 8/8 through m=20; any deviation is the datum and is recorded verbatim',
         'z_star': 'z*(21)=2*21-2+1=41 EXACTLY (K1268)'},
        63, 41, 21, 21, 59))
    out.append(row_record_x0(
        'frontier_m22_z42_row_record',
        'first_ever_m22_row_frontier_registered_parity_candidate_even_K1268_10th_datum',
        {'co_token_22_allowed': True,
         's_domain': '{22..60}', 'arity_max': 3,
         'style': 'x0 published residual-band style',
         'registered_by': 'kit-2 log S5 item (5) (commit 637d15e1): m=22@z=42 prediction (22,22)@S=44 UP 2v1, collapse v(44,42,65)=1',
         'candidate': 'EXACTLY ONE separation X=(22,22) @S=44, UP 2v1 (value 2 vs collapse v(44,42,65)=1 on paper); all other shapes conform; any deviation is the datum',
         'z_star': 'z*(22)=2*22-2+0=42 EXACTLY (K1268)'},
        65, 42, 22, 22, 60))

    # (d) FRONTIER one-past and d=1-birth rows (kit-added, same-run)
    out.append(row_record_x0(
        'onepast_m21_z42_row_record',
        'kit_added_one_past_frontier_record_m21_z42_odd_decay',
        {'co_token_21_allowed': True,
         's_domain': '{21..59}', 'arity_max': 3,
         'style': 'x0 published residual-band style',
         'registered_by': 'kit-added (six-band life-cycle scaffold one-past parity decay odd 2->1; kit-1 precedent, measured in the same run)',
         'candidate': 'EXACTLY ONE separation {21,22} @S=43, UP 1v0 (value 1 vs collapse v(43,42,64)=0 on paper); no other separation; any deviation is the datum'},
        64, 42, 21, 21, 59))
    out.append(row_record_x0(
        'twopast_m21_z43_row_record',
        'kit_added_birth_slice_record_m21_z43_d1_seat',
        {'co_token_21_allowed': True,
         's_domain': '{21..59}', 'arity_max': 3,
         'style': 'x0 published residual-band style',
         'registered_by': 'kit-added (six-band life-cycle scaffold birth slices z*(m)+2d, odd law shape (m, m+2d+1) = {21,24}; kit-1 precedent, measured in the same run)',
         'candidate': 'EXACTLY TWO separations: stick {21,22} @S=43 DOWN 1v2 (value 1 vs collapse v(43,43,65)=2 on paper — the z==x collapse jump) + NEW birth {21,24} @S=45 UP 2v0 (collapse v(45,43,65)=0 on paper), d=1 seat gap 3; any deviation is the datum'},
        65, 43, 21, 21, 59))
    out.append(row_record_x0(
        'onepast_m22_z43_row_record',
        'kit_added_one_past_frontier_record_m22_z43_even_decay',
        {'co_token_22_allowed': True,
         's_domain': '{22..60}', 'arity_max': 3,
         'style': 'x0 published residual-band style',
         'registered_by': 'kit-added (six-band life-cycle scaffold one-past parity decay even 2->0; kit-1 precedent, measured in the same run)',
         'candidate': 'EXACTLY ONE separation (22,22) @S=44, DOWN 0v1 (value 0 vs collapse v(44,43,65)=1 on paper); no other separation; any deviation is the datum'},
        66, 43, 22, 22, 60))
    out.append(row_record_x0(
        'twopast_m22_z44_row_record',
        'kit_added_birth_slice_record_m22_z44_d1_seat',
        {'co_token_22_allowed': True,
         's_domain': '{22..60}', 'arity_max': 3,
         'style': 'x0 published residual-band style',
         'registered_by': 'kit-added (six-band life-cycle scaffold birth slices z*(m)+2d, even law shape (m, m+2d) = (22,24); kit-1 precedent, measured in the same run)',
         'candidate': 'EXACTLY TWO separations: stick (22,22) @S=44 DOWN 0v2 (value 0 vs collapse v(44,44,67)=2 on paper) + NEW birth (22,24) @S=46 UP 2v1 (collapse v(46,44,67)=1 on paper), d=1 seat gap 2; any deviation is the datum'},
        67, 44, 22, 22, 60))

    # (e) IN-BAND window sweeps (REGISTERED with probe caveat,
    #     re-probed at this build: the z=33..41 census kits do not
    #     exist; every published z=33..41 engine value has a part
    #     < 21, disjoint from these all-parts->=21 rows)
    for z in range(33, 41):
        R = 21 + z + 1
        out.append(row_record_x0(
            'inband_m21_z%d_row_record' % z,
            'first_ever_m21_in_band_window_sweep_entry_z%d' % z,
            {'co_token_21_allowed': True,
             's_domain': '{21..59}', 'arity_max': 3,
             'style': 'x0 published residual-band style',
             'registered_by': 'kit-2 log S5 item (5) in-band window proposal (commit 637d15e1), coverage probed at this build',
             'candidate': '0 separations (in-band-clean precedent: six bands m=13..18 + kit-1 m=19/m=20 sweeps)',
             'band': 'NEW m=21 in-band residual band window, z in {33..40} = z*(21)-8..z*(21)-1 (z*(21)=41 per K1268); the z in {25,26} x0-equivalents are contained in the published z25-min20 / z26-floor20 strips (0 violations), derivable-clean; the z in {27..32} slices are registered for the next execution'},
            R, z, 21, 21, 59))
    for z in range(34, 42):
        R = 22 + z + 1
        out.append(row_record_x0(
            'inband_m22_z%d_row_record' % z,
            'first_ever_m22_in_band_window_sweep_entry_z%d' % z,
            {'co_token_22_allowed': True,
             's_domain': '{22..60}', 'arity_max': 3,
             'style': 'x0 published residual-band style',
             'registered_by': 'kit-2 log S5 item (5) in-band window proposal (commit 637d15e1), coverage probed at this build',
             'candidate': '0 separations (in-band-clean precedent: six bands m=13..18 + kit-1 m=19/m=20 sweeps)',
             'band': 'NEW m=22 in-band residual band window, z in {34..41} = z*(22)-8..z*(22)-1 (z*(22)=42 per K1268); the z in {25,26} x0-equivalents are contained in the published z25-min20 / z26-floor20 strips (0 violations), derivable-clean; the z in {27..33} slices are registered for the next execution'},
            R, z, 22, 22, 60))

    # (f) future-slice registration constants (engine-free, NOT measured)
    out.append({'section': 'future_slice_registration_constants',
                'label': 'engine_free_paper_only_K0832_closed_form_next_slice_predictions_NOT_measured_here',
                'registered_for_next_execution_kit_log_S5': [
                    {'m': 19, 'z': 48, 'kind': 'one-past-of-d=5 / death-of-d=4',
                     'prediction': 'EXACTLY ONE: {19,30}@S=49 UP 1v0 (odd decay 2->1; collapse v(49,48,68)=0); {19,28} conform-DEAD at its birth+3 (collapse v(47,48,68)=1)'},
                    {'m': 19, 'z': 49, 'kind': 'birth slice d=6',
                     'prediction': 'EXACTLY TWO: stick {19,30} DOWN 1v2 (collapse v(49,49,69)=2) + NEW {19,32}@S=51 UP 2v0 (collapse v(51,49,69)=0), d=6 seat gap 13'},
                    {'m': 20, 'z': 49, 'kind': 'one-past-of-d=5 / death-of-d=4',
                     'prediction': 'EXACTLY ONE: (20,30)@S=50 DOWN 0v1 (even decay 2->0; collapse v(50,49,70)=1); (20,28) conform-DEAD at its birth+3 (collapse v(48,49,70)=0)'},
                    {'m': 20, 'z': 50, 'kind': 'birth slice d=6',
                     'prediction': 'EXACTLY TWO: stick (20,30) DOWN 0v2 (collapse v(50,50,71)=2) + NEW (20,32)@S=52 UP 2v1 (collapse v(52,50,71)=1), d=6 seat gap 12'},
                    {'m': 21, 'z': 44, 'kind': 'one-past-of-d=1 / death-of-d=0',
                     'prediction': 'EXACTLY ONE: {21,24}@S=45 UP 1v0 (collapse v(45,44,66)=0); {21,22} conform-DEAD at its birth+3 (collapse v(43,44,66)=1) — the first m=21 death datum (d=0 shape)'},
                    {'m': 21, 'z': 45, 'kind': 'birth slice d=2',
                     'prediction': 'EXACTLY TWO: stick {21,24} DOWN 1v2 (collapse v(45,45,67)=2) + NEW {21,26}@S=47 UP 2v0 (collapse v(47,45,67)=0), d=2 seat gap 5'},
                    {'m': 22, 'z': 45, 'kind': 'one-past-of-d=1 / death-of-d=0',
                     'prediction': 'EXACTLY ONE: (22,24)@S=46 DOWN 0v1 (collapse v(46,45,68)=1); (22,22) conform-DEAD at its birth+3 (collapse v(44,45,68)=0) — the first m=22 death datum (d=0 shape)'},
                    {'m': 22, 'z': 46, 'kind': 'birth slice d=2',
                     'prediction': 'EXACTLY TWO: stick (22,24) DOWN 0v2 (collapse v(46,46,69)=2) + NEW (22,26)@S=48 UP 2v1 (collapse v(48,46,69)=1), d=2 seat gap 4'},
                    {'m': 23, 'z': 44, 'kind': 'frontier first contact proposal (FIRST-EVER m=23 row)',
                     'prediction': 'EXACTLY ONE: {23,24}@S=47 UP 2v0 (collapse v(47,44,68)=0); z*(23)=2*23-2+1=44 per K1268; the parity frontier law 11th datum candidate (10/10 through m=22 if this kit confirms m=21/m=22)'},
                    {'m': 24, 'z': 46, 'kind': 'frontier first contact proposal (FIRST-EVER m=24 row)',
                     'prediction': 'EXACTLY ONE: (24,24)@S=48 UP 2v1 (collapse v(48,46,71)=1); z*(24)=46 per K1268; the 12th datum candidate'},
                    {'m': 21, 'z': '27..32', 'kind': 'below-window band-start proposal',
                     'prediction': '0 separations each (candidate); the z in {25,26} equivalents are strip-derived clean; probe strip coverage at the next kit build before measuring'},
                    {'m': 22, 'z': '27..33', 'kind': 'below-window band-start proposal',
                     'prediction': '0 separations each (candidate); probe strip coverage at the next kit build before measuring'}]})

    # (g) published anchor rechecks (52 spots, verbatim published values)
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
                'label': 'fifty_two_published_spots_reproduce_exactly_match_field_is_value_equality_with_published',
                'rows': rechecks,
                'note': 'the separation spots are separations by construction (value != collapse BY DESIGN); the z=25/z=26 base spots are published CONFORM values; the match criterion is equality with the PUBLISHED value'})

    res = {'result': 'EXPLORE-DONE', 'sections': out}
    print(json.dumps(res, sort_keys=True, separators=(',', ':')))


if __name__ == '__main__':
    main()
