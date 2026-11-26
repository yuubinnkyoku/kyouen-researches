"""
explore_m23m24_frontier: FROZEN PRE-DECLARATION census for the LADDER
CONTINUATION of the new bands (the registered kit-3 S5 items m=19@z
=48 / z=49, m=20@z=49 / z=50, m=21@z=44 / z=45, m=22@z=45 / z=46),
the FRONTIER rows m=23 and m=24 (the registered 11th / 10th parity
datum candidates, WITH THE DISCLOSED z*(23) REGISTRATION ERRATUM:
the kit-3 S5 item (9) wrote z*(23)="2*23-2+1=44", which is an
arithmetic slip — the K1268 formula z*(m)=2m-2+(m mod 2) gives
z*(23)=45 EXACTLY; both slices are measured here: the misregistered
m=23@z=44 (in-band one-below-frontier row) with the corrected
expected clean, and the CORRECTED frontier m=23@z=45), the kit-added
one-past / d=1-birth mini-ladders of m=23 / m=24, and the
REGISTERED below-window band-start rows m=21 z in {27..32} and
m=22 z in {27..33}, plus 72 published anchor rechecks. NO K slot is
claimed by this file; the constants below were frozen into this
docstring BEFORE the first run of this file and the file has not
been edited after any of its runs.

Registered provenance (all BEFORE any measurement by this kit):
- The four rows m=19@z=48 / z=49, m=20@z=49 / z=50, m=21@z=44 /
  z=45, m=22@z=45 / z=46 are the REGISTERED binding candidates of
  the published m21m22 kit log section 5 items (1)-(8) and of its
  frozen output section future_slice_registration_constants
  (commit 6554de44, research/log/2026-11-26-m21m22-frontier-ladders-
  predecl-microkit.md), verbatim (one-past rows EXACTLY ONE with the
  previous seat conform-DEAD at its birth+3; birth rows EXACTLY TWO
  stick + new birth).
- The ERRATUM (disclosed here, first): kit-3 S5 item (9) and its
  frozen section (f) registered the m=23 frontier at z=44 with the
  claim "z*(23)=2*23-2+1=44 per K1268" — the formula evaluates to
  45; the registration's intent was the next frontier datum
  (the 11th). This kit DISCHARGES the misregistration by measuring
  m=23@z=44 (R=68) as registered — with the CORRECTED expectation
  stated before the freeze: the m=13..21 frontier-minus-one rows
  are all published clean, so the candidate for m=23@z=44 is
  0 separations (the registered EXACTLY ONE prediction is
  understood to be voided by the slip and is NOT re-asserted) —
  and by measuring the CORRECTED frontier m=23@z=45 (R=69,
  KIT-ADDED corrected registration, measured in the same run):
  candidate EXACTLY ONE {23,24}@S=47 UP 2v0 (collapse
  v(47,45,69)=0 on paper). If m=23@z=44 measures any separation,
  that is the datum, recorded verbatim.
- The frontier row m=24@z=46 (z*(24)=2*24-2+0=46 EXACTLY) is the
  REGISTERED 12th datum candidate (kit-3 S5 item (9), arithmetic
  verified at this build): EXACTLY ONE (24,24)@S=48 UP 2v1
  (collapse v(48,46,71)=1).
- The kit-added mini-ladder rows of m=23 / m=24 (the kit-1
  precedent, registered in this docstring before the freeze,
  measured in the same run):
  * m=23@z=46 (two-past of the d=0 seat, one-below its stick):
    candidate EXACTLY ONE {23,24}@S=47 UP 1v0 (value 1 vs collapse
    v(47,46,70)=0 on paper).
  * m=23@z=47 (birth slice d=1, stick coincides: S(d0)=47=z):
    candidate EXACTLY TWO: stick {23,24}@S=47 DOWN 1v2 (collapse
    v(47,47,71)=2 — the z==x collapse jump) + NEW birth
    {23,26}@S=49 UP 2v0 (collapse v(49,47,71)=0), d=1 seat gap 3.
  * m=24@z=47 (one-past of the d=0 seat): candidate EXACTLY ONE
    (24,24)@S=48 DOWN 0v1 (collapse v(48,47,72)=1 on paper).
  * m=24@z=48 (birth slice d=1, stick coincides: S(d0)=48=z):
    candidate EXACTLY TWO: stick (24,24)@S=48 DOWN 0v2 (collapse
    v(48,48,73)=2) + NEW birth (24,26)@S=50 UP 2v1 (collapse
    v(50,48,73)=1), d=1 seat gap 2.
  * m=24@z=49 (two-past of the d=0 seat, one-below its stick):
    candidate EXACTLY ONE (24,24)@S=48 ... CORRECTED BEFORE THE
    FREEZE BY THE BUILD CHECK: at z=49 the seat S=48 has x=48,
    z=49=x+1: collapse v(48,49,74)=0 (the death slice = stick+1),
    expected value 0 = conform — so the m=24@z=49 row candidate is
    0 separations (the d=0 shape dies at z=49 = S+1); the d=1 seat
    (24,26)@S=50 at z=49: value 0 (even one-past decay of the
    birth value 2), collapse v(50,49,74)=1 on paper -> candidate
    EXACTLY ONE separation (24,26)@S=50 DOWN 0v1.
- The below-window band-start rows m=21 z in {27..32} (R=49..54)
  and m=22 z in {27..33} (R=50..56) are the REGISTERED kit-3 S5
  item (10) proposals, strip-coverage re-probed at this build: no
  z=27..33 census kit exists (the census series stops at z=26; the
  z=27 census is only a registered future lane), and every
  published z=27..33 engine value belongs to m<=22 row records /
  quad-spot / handoff families with a part < 21 except the kit-3
  m=21/m=22 rows themselves (z=33..44, disjoint slices) — free
  slices; the z in {25,26} equivalents remain strip-derived clean
  (z25-min20 strips m in {20..25}, z26-floor20 m in {20..26}).
  Candidate 0 separations each (in-band-clean precedent).

Counter-probe (content-based; re-run at push time against the
then-current main): at kit-build time (2026-11-26T09:12Z, main head
6554de44 — this kit's own predecessor) the content queries
"frontier_m23", "m23_z44", "m23_z45", "m24_z46", "m19_z48",
"m20_z49", "m21_z44", "m22_z45", "inband_m21_z27", "inband_m22_z27"
return NO measurement record; the registered constants exist only
as registrations in the published kit-3 log S5 and frozen section.

HONEST DISCLOSURE (paper arithmetic, before the freeze): every
collapse constant stated below is the PROVED K0832 single-token
closed form computed on paper (engine-free), re-derived twice, and
the full candidate list of every measured row was re-checked at
build time against the seat-life-cycle algebra (birth at z*(m)+2d,
seat value 2; one-past z+1 decay (odd 2->1 / even 2->0); the
collapse z==x jump at z=S (stick) with the value stuck at the decay
parity value; death (conform) at z=S+1) — the check that caught
the m=23 z*(23) registration slip and corrected the m=24@z=49
candidate before the freeze. The quoted published anchor values are
verbatim citations read BEFORE the freeze. NO engine recursion on
ANY position listed below was evaluated before the freeze — every
engine value in the sections (b)..(g) is touched for the FIRST
time at the frozen first run; the sole exceptions are the 72
published anchor spots of section (h) (the 52 kit-3 anchors + the
20 kit-3 separation spots of commit 6554de44), which must
reproduce their published values exactly.

Scope (this file measures and reports; it proves nothing by
itself):

  (a) K0832 battery: every single-token literal used by this
      file's candidate constants, the staircase samples for every
      measured row, the future-slice registration constants, and
      the anchor collapses — closed-form vs canonical-engine vs
      ordered-engine. Candidate: all match.
  (b) LADDER rows, x0 published residual-band style (X = parts(S,
      m, 3), X[0] == m, co-token m allowed, arity <= 3 TOTAL,
      S in {m..m+38}, R = m+z+1): m=19@z in {48,49} (R=68,69),
      m=20@z in {49,50} (R=70,71), m=21@z in {44,45} (R=66,67),
      m=22@z in {45,46} (R=68,69) — REGISTERED binding candidates;
      m=23@z in {44,45,46,47} (R=68,69,70,71) and m=24@z in
      {46,47,48,49} (R=71,72,73,74) — the frontier / erratum /
      kit-added rows as spelled out above.
  (c) BELOW-WINDOW band-start rows, same x0 style: m=21 z in
      {27..32} and m=22 z in {27..33}, candidates 0 separations.
  (d) FUTURE-SLICE REGISTRATION CONSTANTS (paper-only,
      engine-free, battery-checked, NOT measured): m=19@z=50
      (one-past-of-d=6: EXACTLY ONE {19,32}@S=51 UP 1v0, collapse
      v(51,50,70)=0; {19,30} conform-DEAD at z=50 = S+1, collapse
      v(49,50,70)=1) and m=19@z=51 (birth d=7: EXACTLY TWO: stick
      {19,32} DOWN 1v2, v(51,51,71)=2, + NEW {19,34}@S=53 UP 2v0,
      v(53,51,71)=0, seat gap 15); m=20@z=51 (one-past-of-d=6:
      EXACTLY ONE (20,32)@S=52 DOWN 0v1, v(52,51,72)=1; (20,30)
      conform-DEAD, v(50,51,72)=0) and m=20@z=52 (birth d=7:
      EXACTLY TWO: stick (20,32) DOWN 0v2, v(52,52,73)=2, + NEW
      (20,34)@S=54 UP 2v1, v(54,52,73)=1, seat gap 14); m=21@z=46
      (one-past-of-d=2: EXACTLY ONE {21,26}@S=47 UP 1v0,
      v(47,46,68)=0; {21,24} conform-DEAD, v(45,46,68)=1) and
      m=21@z=47 (birth d=3: EXACTLY TWO: stick {21,26} DOWN 1v2,
      v(47,47,69)=2, + NEW {21,28}@S=49 UP 2v0, v(49,47,69)=0,
      seat gap 7); m=22@z=47 (one-past-of-d=2: EXACTLY ONE
      (22,26)@S=48 DOWN 0v1, v(48,47,68)=1; (22,24) conform-DEAD,
      v(46,47,68)=0) and m=22@z=48 (birth d=3: EXACTLY TWO: stick
      (22,26) DOWN 0v2, v(48,48,69)=2, + NEW (22,28)@S=50 UP 2v1,
      v(50,48,69)=1, seat gap 6); m=23@z=48 (one-past-of-d=1:
      EXACTLY ONE {23,26}@S=49 UP 1v0, v(49,48,72)=0; {23,24}
      conform-DEAD at z=48=S+1, v(47,48,72)=1) and m=23@z=49
      (birth d=2: EXACTLY TWO: stick {23,26} DOWN 1v2, v(49,49,73)
      =2, + NEW {23,28}@S=51 UP 2v0, v(51,49,73)=0, seat gap 5);
      m=24@z=50 (birth d=2 — stick coincides: S(d1)=50=z:
      EXACTLY TWO: stick (24,26)@S=50 DOWN 0v2, v(50,50,75)=2, +
      NEW (24,28)@S=52 UP 2v1, v(52,50,75)=1, seat gap 4); PLUS
      the frontier proposals m=25@z=49 (z*(25)=2*25-2+1=49,
      R=75): EXACTLY ONE {25,26}@S=51 UP 2v0 (collapse
      v(51,49,75)=0) — the 13th datum candidate; m=26@z=50
      (z*(26)=50, R=77): EXACTLY ONE (26,26)@S=52 UP 2v1
      (collapse v(52,50,77)=1) — the 14th.
  (h) published anchor rechecks (72 spots): the 52 kit-3 anchor
      spots verbatim + the 20 kit-3 separation spots (commit
      6554de44) — must all reproduce exactly.

Everything is a pure function of the pinned engine bytes; no
randomness, no hash-seed dependence, no wall-clock in the output.
stdout is the frozen artifact (explore_m23m24_frontier.out).
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
    meas_rows = [(19, 48), (19, 49), (20, 49), (20, 50),
                 (21, 44), (21, 45), (22, 45), (22, 46),
                 (23, 44), (23, 45), (23, 46), (23, 47),
                 (24, 46), (24, 47), (24, 48), (24, 49)] + \
                [(21, z) for z in range(27, 33)] + \
                [(22, z) for z in range(27, 34)]
    for (m, z) in meas_rows:
        R = m + z + 1
        for S in (m, m + 2, 2 * m, 2 * m + 1, m + 37, m + 38):
            battery_lits.append((S, z, R))
        rows_stair.append((m, z, R))
    # registered kit-3 S5 items (1)-(8) candidate constants
    for (x, z2, R2) in [
            (49, 48, 68), (47, 48, 68), (49, 49, 69), (51, 49, 69),
            (50, 49, 70), (48, 49, 70), (50, 50, 71), (52, 50, 71),
            (45, 44, 66), (43, 44, 66), (45, 45, 67), (47, 45, 67),
            (46, 45, 68), (44, 45, 68), (46, 46, 69), (48, 46, 69)]:
        battery_lits.append((x, z2, R2))
    # m=23/m=24 frontier + erratum + kit-added candidate constants
    for (x, z2, R2) in [
            (47, 44, 68), (47, 45, 69), (47, 46, 70), (47, 47, 71),
            (49, 47, 71), (48, 46, 71), (48, 47, 72), (48, 48, 73),
            (50, 48, 73), (50, 49, 74), (48, 49, 74)]:
        battery_lits.append((x, z2, R2))
    # future-slice registration constants (section (d), NOT measured)
    for (x, z2, R2) in [
            (51, 50, 70), (49, 50, 70), (51, 51, 71), (53, 51, 71),
            (52, 51, 72), (50, 51, 72), (52, 52, 73), (54, 52, 73),
            (47, 46, 68), (45, 46, 68), (47, 47, 69), (49, 47, 69),
            (48, 47, 68), (46, 47, 68), (48, 48, 69), (50, 48, 69),
            (49, 48, 72), (47, 48, 72), (49, 49, 73), (51, 49, 73),
            (50, 50, 75), (52, 50, 75), (51, 49, 75), (52, 50, 77)]:
        battery_lits.append((x, z2, R2))
    # anchor collapse literals (section (h))
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
        (67, (22, 24), 44, 2, 'kit-3 (6554de44) two-past m=22@z=44 d=1 birth separation UP 2v1 seat gap 2')]
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

    # (b) LADDER rows: registered kit-3 S5 items (1)-(8)
    out.append(row_record_x0(
        'ladder_m19_z48_row_record',
        'registered_kit3_S5_item1_one_past_of_d5_death_of_d4',
        {'co_token_19_allowed': True,
         's_domain': '{19..57}', 'arity_max': 3,
         'style': 'x0 published residual-band style',
         'registered_by': 'kit-3 log S5 item (1) + frozen section (commit 6554de44)',
         'candidate': 'EXACTLY ONE separation {19,30}@S=49 UP 1v0 (value 1 vs collapse v(49,48,68)=0 on paper); {19,28} conform-DEAD at its birth+3 (collapse v(47,48,68)=1); any deviation is the datum'},
        68, 48, 19, 19, 57))
    out.append(row_record_x0(
        'ladder_m19_z49_row_record',
        'registered_kit3_S5_item2_birth_slice_d6',
        {'co_token_19_allowed': True,
         's_domain': '{19..57}', 'arity_max': 3,
         'style': 'x0 published residual-band style',
         'registered_by': 'kit-3 log S5 item (2) + frozen section (commit 6554de44)',
         'candidate': 'EXACTLY TWO separations: stick {19,30}@S=49 DOWN 1v2 (collapse v(49,49,69)=2) + NEW {19,32}@S=51 UP 2v0 (collapse v(51,49,69)=0), d=6 seat gap 13; any deviation is the datum'},
        69, 49, 19, 19, 57))
    out.append(row_record_x0(
        'ladder_m20_z49_row_record',
        'registered_kit3_S5_item3_one_past_of_d5_death_of_d4',
        {'co_token_20_allowed': True,
         's_domain': '{20..58}', 'arity_max': 3,
         'style': 'x0 published residual-band style',
         'registered_by': 'kit-3 log S5 item (3) + frozen section (commit 6554de44)',
         'candidate': 'EXACTLY ONE separation (20,30)@S=50 DOWN 0v1 (value 0 vs collapse v(50,49,70)=1 on paper); (20,28) conform-DEAD at its birth+3 (collapse v(48,49,70)=0); any deviation is the datum'},
        70, 49, 20, 20, 58))
    out.append(row_record_x0(
        'ladder_m20_z50_row_record',
        'registered_kit3_S5_item4_birth_slice_d6',
        {'co_token_20_allowed': True,
         's_domain': '{20..58}', 'arity_max': 3,
         'style': 'x0 published residual-band style',
         'registered_by': 'kit-3 log S5 item (4) + frozen section (commit 6554de44)',
         'candidate': 'EXACTLY TWO separations: stick (20,30)@S=50 DOWN 0v2 (collapse v(50,50,71)=2) + NEW (20,32)@S=52 UP 2v1 (collapse v(52,50,71)=1), d=6 seat gap 12; any deviation is the datum'},
        71, 50, 20, 20, 58))
    out.append(row_record_x0(
        'ladder_m21_z44_row_record',
        'registered_kit3_S5_item5_one_past_of_d1_death_of_d0_first_m21_death',
        {'co_token_21_allowed': True,
         's_domain': '{21..59}', 'arity_max': 3,
         'style': 'x0 published residual-band style',
         'registered_by': 'kit-3 log S5 item (5) + frozen section (commit 6554de44)',
         'candidate': 'EXACTLY ONE separation {21,24}@S=45 UP 1v0 (value 1 vs collapse v(45,44,66)=0 on paper); {21,22} conform-DEAD at its birth+3 (collapse v(43,44,66)=1) — the FIRST m=21 death datum (d=0 shape); any deviation is the datum'},
        66, 44, 21, 21, 59))
    out.append(row_record_x0(
        'ladder_m21_z45_row_record',
        'registered_kit3_S5_item6_birth_slice_d2',
        {'co_token_21_allowed': True,
         's_domain': '{21..59}', 'arity_max': 3,
         'style': 'x0 published residual-band style',
         'registered_by': 'kit-3 log S5 item (6) + frozen section (commit 6554de44)',
         'candidate': 'EXACTLY TWO separations: stick {21,24}@S=45 DOWN 1v2 (collapse v(45,45,67)=2) + NEW {21,26}@S=47 UP 2v0 (collapse v(47,45,67)=0), d=2 seat gap 5; any deviation is the datum'},
        67, 45, 21, 21, 59))
    out.append(row_record_x0(
        'ladder_m22_z45_row_record',
        'registered_kit3_S5_item7_one_past_of_d1_death_of_d0_first_m22_death',
        {'co_token_22_allowed': True,
         's_domain': '{22..60}', 'arity_max': 3,
         'style': 'x0 published residual-band style',
         'registered_by': 'kit-3 log S5 item (7) + frozen section (commit 6554de44)',
         'candidate': 'EXACTLY ONE separation (22,24)@S=46 DOWN 0v1 (value 0 vs collapse v(46,45,68)=1 on paper); (22,22) conform-DEAD at its birth+3 (collapse v(44,45,68)=0) — the FIRST m=22 death datum (d=0 shape); any deviation is the datum'},
        68, 45, 22, 22, 60))
    out.append(row_record_x0(
        'ladder_m22_z46_row_record',
        'registered_kit3_S5_item8_birth_slice_d2',
        {'co_token_22_allowed': True,
         's_domain': '{22..60}', 'arity_max': 3,
         'style': 'x0 published residual-band style',
         'registered_by': 'kit-3 log S5 item (8) + frozen section (commit 6554de44)',
         'candidate': 'EXACTLY TWO separations: stick (22,24)@S=46 DOWN 0v2 (collapse v(46,46,69)=2) + NEW (22,26)@S=48 UP 2v1 (collapse v(48,46,69)=1), d=2 seat gap 4; any deviation is the datum'},
        69, 46, 22, 22, 60))

    # (b2) FRONTIER rows m=23 / m=24 with the disclosed ERRATUM
    out.append(row_record_x0(
        'frontier_m23_z44_row_record',
        'kzstar_erratum_row_discharged_corrected_candidate_in_band_one_below_frontier',
        {'co_token_23_allowed': True,
         's_domain': '{23..61}', 'arity_max': 3,
         'style': 'x0 published residual-band style',
         'registered_by': 'kit-3 S5 item (9) registered this slice BY ARITHMETIC SLIP (z*(23)=45, not 44); discharged here with the corrected expectation stated before the freeze',
         'candidate': '0 separations (the frontier-minus-one rows of m=13..21 are all published clean; the registered EXACTLY ONE prediction is VOIDED by the slip and not re-asserted); any separation is the datum, recorded verbatim'},
        68, 44, 23, 23, 61))
    out.append(row_record_x0(
        'frontier_m23_z45_row_record',
        'corrected_frontier_record_m23_z45_registered_K1268_11th_datum_candidate',
        {'co_token_23_allowed': True,
         's_domain': '{23..61}', 'arity_max': 3,
         'style': 'x0 published residual-band style',
         'registered_by': 'corrected registration (kit-added, disclosed): the CORRECTED next frontier datum after kit-3 measured m=21/m=22; z*(23)=2*23-2+1=45 EXACTLY (K1268)',
         'candidate': 'EXACTLY ONE separation X={23,24} @S=47, UP 2v0 (value 2 vs collapse v(47,45,69)=0 on paper); all other shapes conform; the parity frontier law is 10/10 through m=22; any deviation is the datum and is recorded verbatim',
         'z_star': 'z*(23)=2*23-2+1=45 EXACTLY (K1268); the kit-3 S5 item (9) z=44 registration is an arithmetic slip, disclosed here'},
        69, 45, 23, 23, 61))
    out.append(row_record_x0(
        'frontier_m24_z46_row_record',
        'registered_frontier_record_m24_z46_K1268_12th_datum_candidate',
        {'co_token_24_allowed': True,
         's_domain': '{24..62}', 'arity_max': 3,
         'style': 'x0 published residual-band style',
         'registered_by': 'kit-3 log S5 item (9) + frozen section (commit 6554de44), arithmetic verified at this build',
         'candidate': 'EXACTLY ONE separation X=(24,24) @S=48, UP 2v1 (value 2 vs collapse v(48,46,71)=1 on paper); all other shapes conform; any deviation is the datum',
         'z_star': 'z*(24)=2*24-2+0=46 EXACTLY (K1268)'},
        71, 46, 24, 24, 62))

    # (b3) kit-added mini-ladder rows m=23 / m=24
    out.append(row_record_x0(
        'onepast_m23_z46_row_record',
        'kit_added_two_past_of_d0_seat_m23_z46_up_1v0',
        {'co_token_23_allowed': True,
         's_domain': '{23..61}', 'arity_max': 3,
         'style': 'x0 published residual-band style',
         'registered_by': 'kit-added (seat-life-cycle algebra: the d=0 seat {23,24}@S=47 holds its decayed value 1 one-below its stick slice z=S=47; registered before the freeze, measured in the same run)',
         'candidate': 'EXACTLY ONE separation {23,24} @S=47, UP 1v0 (value 1 vs collapse v(47,46,70)=0 on paper); any deviation is the datum'},
        70, 46, 23, 23, 61))
    out.append(row_record_x0(
        'twopast_m23_z47_row_record',
        'kit_added_birth_slice_record_m23_z47_d1_seat_stick_coincides',
        {'co_token_23_allowed': True,
         's_domain': '{23..61}', 'arity_max': 3,
         'style': 'x0 published residual-band style',
         'registered_by': 'kit-added (six-band life-cycle scaffold: birth slice d=1 with the stick coinciding at z=S(d0)=47; registered before the freeze, measured in the same run)',
         'candidate': 'EXACTLY TWO separations: stick {23,24} @S=47 DOWN 1v2 (value 1 vs collapse v(47,47,71)=2 on paper — the z==x collapse jump) + NEW birth {23,26} @S=49 UP 2v0 (collapse v(49,47,71)=0 on paper), d=1 seat gap 3; any deviation is the datum'},
        71, 47, 23, 23, 61))
    out.append(row_record_x0(
        'onepast_m24_z47_row_record',
        'kit_added_one_past_frontier_record_m24_z47_even_decay',
        {'co_token_24_allowed': True,
         's_domain': '{24..62}', 'arity_max': 3,
         'style': 'x0 published residual-band style',
         'registered_by': 'kit-added (six-band life-cycle scaffold one-past parity decay even 2->0; kit precedent, registered before the freeze, measured in the same run)',
         'candidate': 'EXACTLY ONE separation (24,24) @S=48, DOWN 0v1 (value 0 vs collapse v(48,47,72)=1 on paper); no other separation; any deviation is the datum'},
        72, 47, 24, 24, 62))
    out.append(row_record_x0(
        'twopast_m24_z48_row_record',
        'kit_added_birth_slice_record_m24_z48_d1_seat_stick_coincides',
        {'co_token_24_allowed': True,
         's_domain': '{24..62}', 'arity_max': 3,
         'style': 'x0 published residual-band style',
         'registered_by': 'kit-added (six-band life-cycle scaffold: birth slice d=1 with the stick coinciding at z=S(d0)=48; registered before the freeze, measured in the same run)',
         'candidate': 'EXACTLY TWO separations: stick (24,24) @S=48 DOWN 0v2 (value 0 vs collapse v(48,48,73)=2 on paper) + NEW birth (24,26) @S=50 UP 2v1 (collapse v(50,48,73)=1 on paper), d=1 seat gap 2; any deviation is the datum'},
        73, 48, 24, 24, 62))
    out.append(row_record_x0(
        'onepast_m24_z49_row_record',
        'kit_added_one_past_of_d1_death_of_d0_m24_z49',
        {'co_token_24_allowed': True,
         's_domain': '{24..62}', 'arity_max': 3,
         'style': 'x0 published residual-band style',
         'registered_by': 'kit-added (seat-life-cycle algebra: the d=0 seat dies at z=S+1=49 and the d=1 seat decays 2->0; corrected at the build check, disclosed; registered before the freeze, measured in the same run)',
         'candidate': 'EXACTLY ONE separation (24,26) @S=50 DOWN 0v1 (value 0 vs collapse v(50,49,74)=1 on paper); (24,24) conform-DEAD at z=49=S+1 (collapse v(48,49,74)=0); any deviation is the datum'},
        74, 49, 24, 24, 62))

    # (c) BELOW-WINDOW band-start rows (REGISTERED kit-3 S5 item (10),
    #     strip coverage re-probed at this build: free slices)
    for z in range(27, 33):
        R = 21 + z + 1
        out.append(row_record_x0(
            'inband_m21_z%d_row_record' % z,
            'below_window_bandstart_m21_z%d' % z,
            {'co_token_21_allowed': True,
             's_domain': '{21..59}', 'arity_max': 3,
             'style': 'x0 published residual-band style',
             'registered_by': 'kit-3 log S5 item (10) (commit 6554de44), strip coverage re-probed at this build',
             'candidate': '0 separations (in-band-clean precedent)',
             'band': 'm=21 below-window band-start pinning: measured windows now z in {27..32} here + {33..40} kit-3; z in {25,26} strip-derived clean'},
            R, z, 21, 21, 59))
    for z in range(27, 34):
        R = 22 + z + 1
        out.append(row_record_x0(
            'inband_m22_z%d_row_record' % z,
            'below_window_bandstart_m22_z%d' % z,
            {'co_token_22_allowed': True,
             's_domain': '{22..60}', 'arity_max': 3,
             'style': 'x0 published residual-band style',
             'registered_by': 'kit-3 log S5 item (10) (commit 6554de44), strip coverage re-probed at this build',
             'candidate': '0 separations (in-band-clean precedent)',
             'band': 'm=22 below-window band-start pinning: measured windows now z in {27..33} here + {34..41} kit-3; z in {25,26} strip-derived clean'},
            R, z, 22, 22, 60))

    # (d) future-slice registration constants (engine-free, NOT measured)
    out.append({'section': 'future_slice_registration_constants',
                'label': 'engine_free_paper_only_K0832_closed_form_next_slice_predictions_NOT_measured_here',
                'registered_for_next_execution_kit_log_S5': [
                    {'m': 19, 'z': 50, 'kind': 'one-past-of-d=6 / death-of-d=5',
                     'prediction': 'EXACTLY ONE: {19,32}@S=51 UP 1v0 (collapse v(51,50,70)=0); {19,30} conform-DEAD at z=50=S+1 (collapse v(49,50,70)=1)'},
                    {'m': 19, 'z': 51, 'kind': 'birth slice d=7',
                     'prediction': 'EXACTLY TWO: stick {19,32} DOWN 1v2 (collapse v(51,51,71)=2) + NEW {19,34}@S=53 UP 2v0 (collapse v(53,51,71)=0), d=7 seat gap 15'},
                    {'m': 20, 'z': 51, 'kind': 'one-past-of-d=6 / death-of-d=5',
                     'prediction': 'EXACTLY ONE: (20,32)@S=52 DOWN 0v1 (collapse v(52,51,72)=1); (20,30) conform-DEAD at z=51=S+1 (collapse v(50,51,72)=0)'},
                    {'m': 20, 'z': 52, 'kind': 'birth slice d=7',
                     'prediction': 'EXACTLY TWO: stick (20,32) DOWN 0v2 (collapse v(52,52,73)=2) + NEW (20,34)@S=54 UP 2v1 (collapse v(54,52,73)=1), d=7 seat gap 14'},
                    {'m': 21, 'z': 46, 'kind': 'one-past-of-d=2 / death-of-d=1',
                     'prediction': 'EXACTLY ONE: {21,26}@S=47 UP 1v0 (collapse v(47,46,68)=0); {21,24} conform-DEAD at z=46=S+1 (collapse v(45,46,68)=1)'},
                    {'m': 21, 'z': 47, 'kind': 'birth slice d=3',
                     'prediction': 'EXACTLY TWO: stick {21,26} DOWN 1v2 (collapse v(47,47,69)=2) + NEW {21,28}@S=49 UP 2v0 (collapse v(49,47,69)=0), d=3 seat gap 7'},
                    {'m': 22, 'z': 47, 'kind': 'one-past-of-d=2 / death-of-d=1',
                     'prediction': 'EXACTLY ONE: (22,26)@S=48 DOWN 0v1 (collapse v(48,47,68)=1); (22,24) conform-DEAD at z=47=S+1 (collapse v(46,47,68)=0)'},
                    {'m': 22, 'z': 48, 'kind': 'birth slice d=3',
                     'prediction': 'EXACTLY TWO: stick (22,26) DOWN 0v2 (collapse v(48,48,69)=2) + NEW (22,28)@S=50 UP 2v1 (collapse v(50,48,69)=1), d=3 seat gap 6'},
                    {'m': 23, 'z': 48, 'kind': 'one-past-of-d=1 / death-of-d=0',
                     'prediction': 'EXACTLY ONE: {23,26}@S=49 UP 1v0 (collapse v(49,48,72)=0); {23,24} conform-DEAD at z=48=S+1 (collapse v(47,48,72)=1) — the first m=23 death datum (d=0 shape)'},
                    {'m': 23, 'z': 49, 'kind': 'birth slice d=2',
                     'prediction': 'EXACTLY TWO: stick {23,26} DOWN 1v2 (collapse v(49,49,73)=2) + NEW {23,28}@S=51 UP 2v0 (collapse v(51,49,73)=0), d=2 seat gap 5'},
                    {'m': 24, 'z': 50, 'kind': 'birth slice d=2 (stick coincides: S(d1)=50=z)',
                     'prediction': 'EXACTLY TWO: stick (24,26)@S=50 DOWN 0v2 (collapse v(50,50,75)=2) + NEW (24,28)@S=52 UP 2v1 (collapse v(52,50,75)=1), d=2 seat gap 4'},
                    {'m': 25, 'z': 49, 'kind': 'frontier first contact proposal (FIRST-EVER m=25 row)',
                     'prediction': 'EXACTLY ONE: {25,26}@S=51 UP 2v0 (collapse v(51,49,75)=0); z*(25)=2*25-2+1=49 per K1268 (arithmetic double-checked: 2*25-2+1=49); R=75; the 13th datum candidate'},
                    {'m': 26, 'z': 50, 'kind': 'frontier first contact proposal (FIRST-EVER m=26 row)',
                     'prediction': 'EXACTLY ONE: (26,26)@S=52 UP 2v1 (collapse v(52,50,77)=1); z*(26)=2*26-2+0=50 per K1268; R=77; the 14th datum candidate'},
                    {'m': 23, 'z': '36..43', 'kind': 'in-band window sweep proposal',
                     'prediction': '0 separations each (candidate); z*(23)-8..-1; strip-coverage probe at build time (no z=36..43 census kit exists yet, but the z=26 heavy-lane plans make future overlap possible: RE-PROBE before measuring)'},
                    {'m': 24, 'z': '38..45', 'kind': 'in-band window sweep proposal',
                     'prediction': '0 separations each (candidate); z*(24)-8..-1; re-probe strip coverage at build time'}]})

    # (h) published anchor rechecks (72 spots, verbatim published values)
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
                'label': 'seventy_two_published_spots_reproduce_exactly_match_field_is_value_equality_with_published',
                'rows': rechecks,
                'note': 'the separation spots are separations by construction (value != collapse BY DESIGN); the z=25/z=26 base spots are published CONFORM values; the match criterion is equality with the PUBLISHED value'})

    res = {'result': 'EXPLORE-DONE', 'sections': out}
    print(json.dumps(res, sort_keys=True, separators=(',', ':')))


if __name__ == '__main__':
    main()
