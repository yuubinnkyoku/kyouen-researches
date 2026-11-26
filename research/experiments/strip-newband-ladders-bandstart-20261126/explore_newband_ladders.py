"""
explore_newband_ladders: FROZEN PRE-DECLARATION census for the LADDER
CONTINUATION of the NEW m=19 / m=20 residual bands past the published
kit-1 measurements (the registered one-past + d=2-birth rows m=19@z=40
and z=41, m=20@z=41 and z=42; the kit-added second one-past + d=3-birth
rows m=19@z=42 and z=43, m=20@z=43 and z=44 — each carrying the FIRST
m=19 / m=20 DEATH datums of the series), PLUS the BAND-START window
rows (the first-ever x0-style row records at the below-window slices
with NO published engine value at the row position: m=19 z in {25..28}
and m=20 z in {27..29}), plus 40 published anchor rechecks. NO K slot
is claimed by this file; the constants below were frozen into this
docstring BEFORE the first run of this file and the file has not been
edited after any of its runs.

Registered provenance (all BEFORE any measurement by this kit):
- The four rows m=19@z=40 and z=41, m=20@z=41 and z=42 are the
  REGISTERED binding candidates of the published in-band kit log
  section 5 items (1)-(4) and of its frozen output section
  future_slice_registration_constants (commit 6057ed51, research/log/
  2026-11-26-inband-completions-m19m20-newbands-predecl-microkit.md),
  verbatim:
  * m=19@z=40: EXACTLY ONE {19,22}@S=41 UP 1v0 (collapse
    v(41,40,60)=0) with {19,20} conform-DEAD at its birth+3 slice
    (collapse v(39,40,60)=1) — the FIRST m=19 death datum (d=0 shape).
  * m=19@z=41 (birth slice d=2): EXACTLY TWO: stick {19,22}@S=41
    DOWN 1v2 (collapse v(41,41,61)=2 — the z==x collapse jump) + NEW
    {19,24}@S=43 UP 2v0 (collapse v(43,41,61)=0), d=2 seat gap 5.
  * m=20@z=41: EXACTLY ONE (20,22)@S=42 DOWN 0v1 (collapse
    v(42,41,62)=1) with (20,20) conform-DEAD at its birth+3 (collapse
    v(40,41,62)=0) — the FIRST m=20 death datum (d=0 shape).
  * m=20@z=42 (birth slice d=2): EXACTLY TWO: stick (20,22)@S=42
    DOWN 0v2 (collapse v(42,42,63)=2) + NEW (20,24)@S=44 UP 2v1
    (collapse v(44,42,63)=1), d=2 seat gap 4.
- The four rows m=19@z=42 and z=43, m=20@z=43 and z=44 are KIT-ADDED
  here, derived BEFORE the freeze from the published six-band
  separation life-cycle scaffold (the exact kit-1 one-past/two-past
  precedent; the m=13..18 ladders published by the decay / wavetrain /
  fifthwave / sixthwave kits and the m=19/m=20 ladders through z=40 by
  kit-1). Binding candidates spelled out in full:
  * m=19@z=42: EXACTLY ONE {19,24}@S=43 UP 1v0 (collapse v(43,42,62)=0;
    the odd one-past decay 2->1 of the d=2 birth) with {19,22}
    conform-DEAD at its birth+3 slice (collapse v(41,42,62)=1) — the
    first m=19 death datum for a d=1 shape.
  * m=19@z=43 (birth slice d=3): EXACTLY TWO: stick {19,24}@S=43 DOWN
    1v2 (collapse v(43,43,63)=2) + NEW {19,26}@S=45 UP 2v0 (collapse
    v(45,43,63)=0), d=3 seat gap 7.
  * m=20@z=43: EXACTLY ONE (20,24)@S=44 DOWN 0v1 (collapse
    v(44,43,64)=1; the even one-past decay 2->0) with (20,22)
    conform-DEAD at its birth+3 (collapse v(42,43,64)=0) — the first
    m=20 death datum for a d=1 shape.
  * m=20@z=44 (birth slice d=3): EXACTLY TWO: stick (20,24)@S=44 DOWN
    0v2 (collapse v(44,44,65)=2) + NEW (20,26)@S=46 UP 2v1 (collapse
    v(46,44,65)=1), d=3 seat gap 6.
- The BAND-START window rows are executed here RESTRICTED to the
  slices at which NO published engine value exists at the row
  position, per the registered band-start pinning intent of the kit-1
  log section 5 item (5), amended by this build's overlap census:
  the published z-slice census kits measured co-token strip sweeps
  (base token m, R=m+z+1, S in {m..m+39}, arity <= 4 TOTAL) covering
  m=19 at z in {21..24} (z21-min16 strips m in {16..20}, the z=22
  kits' strips through m=21, z23-floor17 strips m in {17..22},
  z24-floor18 strips m in {18..23}) and m=20 at z in {21..26} (the
  same kits plus z25-min20 strips m in {20..25}, z26-floor20 strips
  m in {20..26}); every x0-style row position is CONTAINED in the
  corresponding strip sweep, so those window slices are
  derivable-clean from the published 0-violation strip results
  (position-by-position by determinism) and are NOT re-swept here
  (duplicate-avoidance). The genuinely-unmeasured window slices are
  m=19 z in {25,26,27,28} and m=20 z in {27,28,29}:
  * z=25/z=26: the published z25-min20 / z26-floor20 kits measured
    row records only for m in {13..18} and strips only for m >= 20;
    no m=19 row position at R=45/46 was measured EXCEPT the base
    spots H(45;(19,19);25)=0 and H(46;(19,19);26)=0 (z25-min20 /
    z26-floor20 base-spot sections, published CONFORM) — those two
    positions lie INSIDE the m=19@z=25 / z=26 window rows and are
    rechecked here as in-row published anchors (their conform status
    re-verified).
  * z=27/z=28: no z=27/z=28 census kit exists (the z26-floor20 kit
    registered the z=27 census as a future lane); the published
    z=27/z=28 engine values are the four-element handoff quads
    (m=16..18 pairs at R in {43..47}, z26-floor20 and
    frontier-lifecycle kits) — every such position has a part < 19,
    disjoint from the all-parts->=19 window rows m=19@z=27 (R=47),
    m=19@z=28 (R=48), m=20@z=27 (R=48), m=20@z=28 (R=49).
  * z=29: the published decay-kit touch quad lives at R in
    {45..48} with m=16..18 pairs — disjoint from m=20@z=29 (R=50).
  Registered candidate for every window row: 0 separations, by the
  in-band-clean precedent (all six bands m=13..18 at every measured
  in-band slice, plus kit-1's m=19 z in {29..36} and m=20 z in
  {30..37} sweeps, all published 0 separations). Any deviation is
  the datum and is recorded verbatim.

Counter-probe (content-based; re-run at push time against the
then-current main): at kit-build time (2026-11-26T09:02Z, main head
6057ed51, unchanged since kit-1's own publication) the content
queries "ladder_m19", "m19_z42", "m19_z25", "m20_z43", "m20_z27",
"m21_z41", "m22_z42" and 'death datum m19' return NO measurement
record; the "bandstart" hits are the unrelated 2026-11-15 five-row
q7 band-closure kit (different section namespace); the kit-1
registered candidates exist only as registrations (the published
log S5 items and the frozen section (g) constants list), not as
measured rows. No published engine value exists for ANY position of
the fifteen rows measured here except the 40 anchor spots of
section (e).

HONEST DISCLOSURE (paper arithmetic, before the freeze): every
collapse constant stated below is the PROVED K0832 single-token
closed form computed on paper (engine-free), re-derived twice
(draft planning + final assembly check, no engine recursion); the
quoted published anchor values are verbatim citations of the
published logs read BEFORE the freeze. NO engine recursion on ANY
position listed below was evaluated before the freeze — every
engine value in the sections (b)..(d) is touched for the FIRST time
at the frozen first run; the sole exceptions are the 40 published
anchor spots of section (e) (the 30 kit-1 anchors, the 8 kit-1
new-band separation spots of commit 6057ed51, and the 2 z25/z26
m=19 base spots inside the window rows), which must reproduce their
published values exactly.

Scope (this file measures and reports; it proves nothing by
itself):

  (a) K0832 battery: every single-token literal used by this
      file's candidate constants, the derivations, the staircase
      samples (row edges and co-token seats for every measured
      row), the future-slice registration constants, and the
      anchor collapses — checked closed-form vs canonical-engine
      vs ordered-engine. Candidate: all match.
  (b) LADDER rows, x0 published residual-band style (X = parts(S,
      m, 3) with X[0] == m, all parts >= m, co-token m allowed,
      arity <= 3 TOTAL, S in {m..m+38}, R = m+z+1):
      - m=19 @ z=40..43, R=60..63, 22 shapes each;
      - m=20 @ z=41..44, R=62..65, 20 shapes each.
      Registered binding candidates: EXACTLY ONE / EXACTLY TWO
      separation sets as spelled out above; any deviation
      (extra/missing/different value) is the datum, recorded
      verbatim. The rows carry the first m=19/m=20 DEATH datums
      (conform-at-birth+3) — a death is witnessed by the shape's
      ABSENCE from the separation list at its death slice with the
      collapse value equal to the scaffold's stuck value.
  (c) BAND-START window rows, same x0 style:
      - m=19 @ z in {25,26,27,28}, R=45..48;
      - m=20 @ z in {27,28,29}, R=48..50.
      Candidate 0 separations each; the two in-row base spots must
      reproduce their published conform values (0 each).
  (d) FUTURE-SLICE REGISTRATION CONSTANTS (paper-only,
      engine-free, K0832 closed form; battery-checked but NOT
      measured): the next two slices of each new band — m=19@z=44
      one-past-of-d=3 prediction EXACTLY ONE {19,26}@S=45 UP 1v0
      (collapse v(45,44,64)=0) with {19,24} conform-DEAD at its
      birth+3 (collapse v(43,44,64)=1); m=19@z=45 birth slice d=4
      prediction EXACTLY TWO: stick {19,26} DOWN 1v2 (collapse
      v(45,45,65)=2) + NEW {19,28}@S=47 UP 2v0 (collapse
      v(47,45,65)=0), d=4 seat gap 9; m=20@z=45 one-past-of-d=3
      prediction EXACTLY ONE (20,26)@S=46 DOWN 0v1 (collapse
      v(46,45,66)=1) with (20,24) conform-DEAD at its birth+3
      (collapse v(44,45,66)=0); m=20@z=46 birth slice d=4
      prediction EXACTLY TWO: stick (20,26) DOWN 0v2 (collapse
      v(46,46,67)=2) + NEW (20,28)@S=48 UP 2v1 (collapse
      v(48,46,67)=1), d=4 seat gap 8. PLUS the FIRST-EVER m=21 /
      m=22 row registrations for the next execution: m=21@z=41
      (z*(21)=2*21-2+1=41 per K1268, R=63) frontier candidate
      EXACTLY ONE {21,22}@S=43 UP 2v0 (collapse v(43,41,63)=0), the
      9th datum of the parity frontier law (8/8 through m=20);
      m=22@z=42 (z*(22)=42, R=65) frontier candidate EXACTLY ONE
      (22,22)@S=44 UP 2v1 (collapse v(44,42,65)=1), the 10th datum;
      and the in-band window sweeps m=21 z in {33..40} / m=22 z in
      {34..41} (candidates 0 separations) with the strip-coverage
      caveat (the z=33..41 census kits do not exist yet; the
      strip-overlap status must be re-probed at the next kit build
      exactly as done here for m=19/m=20). Registered in the kit
      log section 5 for the next execution.
  (e) published anchor rechecks (40 spots, all values verbatim
      from the published logs): the 30 kit-1 anchors (z=28 handoff
      spots, z=29..32 touch quads, frontier/one-past/two-past
      m=13..18 separation spots), the 8 kit-1 new-band separation
      spots (commit 6057ed51: frontier births, one-past decays,
      two-past sticks and d=1 births of m=19/m=20), and the 2
      published m=19 base spots inside the window rows — must all
      reproduce exactly.

Everything is a pure function of the pinned engine bytes; no
randomness, no hash-seed dependence, no wall-clock in the output.
stdout is the frozen artifact (explore_newband_ladders.out).
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
    # staircase samples for every measured row: (S=m, m+2, 2m, 2m+1,
    # m+37, m+38) at the row's (z, R)
    rows_stair = []
    for (m, z) in [(19, 25), (19, 26), (19, 27), (19, 28),
                   (20, 27), (20, 28), (20, 29),
                   (19, 40), (19, 41), (19, 42), (19, 43),
                   (20, 41), (20, 42), (20, 43), (20, 44)]:
        R = m + z + 1
        for S in (m, m + 2, 2 * m, 2 * m + 1, m + 37, m + 38):
            battery_lits.append((S, z, R))
        rows_stair.append((m, z, R))
    # ladder candidate collapse constants (sections (b))
    for (x, z2, R2) in [
            (41, 40, 60), (39, 40, 60), (41, 41, 61), (43, 41, 61),
            (42, 41, 62), (40, 41, 62), (42, 42, 63), (44, 42, 63),
            (43, 42, 62), (41, 42, 62), (43, 43, 63), (45, 43, 63),
            (44, 43, 64), (42, 43, 64), (44, 44, 65), (46, 44, 65)]:
        battery_lits.append((x, z2, R2))
    # future-slice registration constants (section (d), NOT measured)
    for (x, z2, R2) in [
            (45, 44, 64), (43, 44, 64), (47, 45, 65), (45, 45, 65),
            (46, 45, 66), (44, 45, 66), (48, 46, 67), (46, 46, 67),
            (43, 41, 63), (44, 42, 65)]:
        battery_lits.append((x, z2, R2))
    # anchor collapse literals (section (e))
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
        (45, (19, 19), 25, 0, 'z25-min20 kit base spot H(45;(19,19);25)=0 published CONFORM (inside the m=19@z=25 window row)'),
        (46, (19, 19), 26, 0, 'z26-floor20 kit base spot H(46;(19,19);26)=0 published CONFORM (inside the m=19@z=26 window row)')]
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
        'ladder_m19_z40_row_record',
        'registered_kit1_S5_item1_one_past_of_d1_death_of_d0_first_m19_death_datum',
        {'co_token_19_allowed': True,
         's_domain': '{19..57}', 'arity_max': 3,
         'style': 'x0 published residual-band style',
         'registered_by': 'kit-1 log S5 item (1) + frozen section (g) (commit 6057ed51)',
         'candidate': 'EXACTLY ONE separation {19,22}@S=41 UP 1v0 (value 1 vs collapse v(41,40,60)=0 on paper); {19,20} conform-DEAD at its birth+3 slice (collapse v(39,40,60)=1, value expected 1 = the stuck value, NOT a separation); any deviation is the datum'},
        60, 40, 19, 19, 57))
    out.append(row_record_x0(
        'ladder_m19_z41_row_record',
        'registered_kit1_S5_item2_birth_slice_d2_new_band_ladder',
        {'co_token_19_allowed': True,
         's_domain': '{19..57}', 'arity_max': 3,
         'style': 'x0 published residual-band style',
         'registered_by': 'kit-1 log S5 item (2) + frozen section (g) (commit 6057ed51)',
         'candidate': 'EXACTLY TWO separations: stick {19,22}@S=41 DOWN 1v2 (value 1 vs collapse v(41,41,61)=2 on paper — the z==x collapse jump) + NEW {19,24}@S=43 UP 2v0 (collapse v(43,41,61)=0), d=2 seat gap 5; any deviation is the datum'},
        61, 41, 19, 19, 57))
    out.append(row_record_x0(
        'ladder_m19_z42_row_record',
        'kit_added_one_past_of_d2_death_of_d1_second_m19_death_datum',
        {'co_token_19_allowed': True,
         's_domain': '{19..57}', 'arity_max': 3,
         'style': 'x0 published residual-band style',
         'registered_by': 'kit-added (six-band life-cycle scaffold + kit-1 ladder precedent, registered in this docstring before the freeze, measured in the same run)',
         'candidate': 'EXACTLY ONE separation {19,24}@S=43 UP 1v0 (value 1 vs collapse v(43,42,62)=0 on paper; odd one-past decay 2->1 of the d=2 birth); {19,22} conform-DEAD at its birth+3 slice (collapse v(41,42,62)=1, expected value 1); any deviation is the datum'},
        62, 42, 19, 19, 57))
    out.append(row_record_x0(
        'ladder_m19_z43_row_record',
        'kit_added_birth_slice_d3_new_band_ladder',
        {'co_token_19_allowed': True,
         's_domain': '{19..57}', 'arity_max': 3,
         'style': 'x0 published residual-band style',
         'registered_by': 'kit-added (six-band life-cycle scaffold + kit-1 ladder precedent, registered in this docstring before the freeze, measured in the same run)',
         'candidate': 'EXACTLY TWO separations: stick {19,24}@S=43 DOWN 1v2 (value 1 vs collapse v(43,43,63)=2 on paper) + NEW {19,26}@S=45 UP 2v0 (collapse v(45,43,63)=0), d=3 seat gap 7; any deviation is the datum'},
        63, 43, 19, 19, 57))
    out.append(row_record_x0(
        'ladder_m20_z41_row_record',
        'registered_kit1_S5_item3_one_past_of_d1_death_of_d0_first_m20_death_datum',
        {'co_token_20_allowed': True,
         's_domain': '{20..58}', 'arity_max': 3,
         'style': 'x0 published residual-band style',
         'registered_by': 'kit-1 log S5 item (3) + frozen section (g) (commit 6057ed51)',
         'candidate': 'EXACTLY ONE separation (20,22)@S=42 DOWN 0v1 (value 0 vs collapse v(42,41,62)=1 on paper); (20,20) conform-DEAD at its birth+3 (collapse v(40,41,62)=0, expected value 0 = the stuck value); any deviation is the datum'},
        62, 41, 20, 20, 58))
    out.append(row_record_x0(
        'ladder_m20_z42_row_record',
        'registered_kit1_S5_item4_birth_slice_d2_new_band_ladder',
        {'co_token_20_allowed': True,
         's_domain': '{20..58}', 'arity_max': 3,
         'style': 'x0 published residual-band style',
         'registered_by': 'kit-1 log S5 item (4) + frozen section (g) (commit 6057ed51)',
         'candidate': 'EXACTLY TWO separations: stick (20,22)@S=42 DOWN 0v2 (value 0 vs collapse v(42,42,63)=2 on paper) + NEW (20,24)@S=44 UP 2v1 (collapse v(44,42,63)=1), d=2 seat gap 4; any deviation is the datum'},
        63, 42, 20, 20, 58))
    out.append(row_record_x0(
        'ladder_m20_z43_row_record',
        'kit_added_one_past_of_d2_death_of_d1_second_m20_death_datum',
        {'co_token_20_allowed': True,
         's_domain': '{20..58}', 'arity_max': 3,
         'style': 'x0 published residual-band style',
         'registered_by': 'kit-added (six-band life-cycle scaffold + kit-1 ladder precedent, registered in this docstring before the freeze, measured in the same run)',
         'candidate': 'EXACTLY ONE separation (20,24)@S=44 DOWN 0v1 (value 0 vs collapse v(44,43,64)=1 on paper; even one-past decay 2->0 of the d=2 birth); (20,22) conform-DEAD at its birth+3 (collapse v(42,43,64)=0, expected value 0); any deviation is the datum'},
        64, 43, 20, 20, 58))
    out.append(row_record_x0(
        'ladder_m20_z44_row_record',
        'kit_added_birth_slice_d3_new_band_ladder',
        {'co_token_20_allowed': True,
         's_domain': '{20..58}', 'arity_max': 3,
         'style': 'x0 published residual-band style',
         'registered_by': 'kit-added (six-band life-cycle scaffold + kit-1 ladder precedent, registered in this docstring before the freeze, measured in the same run)',
         'candidate': 'EXACTLY TWO separations: stick (20,24)@S=44 DOWN 0v2 (value 0 vs collapse v(44,44,65)=2 on paper) + NEW (20,26)@S=46 UP 2v1 (collapse v(46,44,65)=1), d=3 seat gap 6; any deviation is the datum'},
        65, 44, 20, 20, 58))

    # (c) BAND-START window rows (first-ever x0 rows at the genuinely
    #     unmeasured below-window slices; covered slices disclosed as
    #     derivable-clean from the published strip sweeps and skipped)
    for z in range(25, 29):
        R = 19 + z + 1
        basenote = ('; the base spot H(%d;(19,19);%d)=0 published by the %s kit lies INSIDE this row and is rechecked in section (e)' % (R, z, 'z25-min20' if z == 25 else 'z26-floor20')) if z in (25, 26) else ''
        out.append(row_record_x0(
            'bandstart_m19_z%d_row_record' % z,
            'first_ever_m19_below_window_row_z%d_bandstart_pinning' % z,
            {'co_token_19_allowed': True,
             's_domain': '{19..57}', 'arity_max': 3,
             'style': 'x0 published residual-band style',
             'registered_by': 'kit-1 log S5 item (5) band-start pinning, restricted at build time by the strip-overlap census to the genuinely-unmeasured slices',
             'candidate': '0 separations (in-band-clean precedent: six bands m=13..18 every measured in-band slice + kit-1 m=19 z in {29..36} all clean)' + basenote,
             'band': 'm=19 in-band window extended below: published z in {29..36} (kit-1), this row z=%d; the z in {21..24} x0-equivalent rows are contained in the published z21-min16 / z22 / z23-floor17 / z24-floor18 strip sweeps (0 violations) and are derivable-clean, not re-swept' % z},
            R, z, 19, 19, 57))
    for z in range(27, 30):
        R = 20 + z + 1
        out.append(row_record_x0(
            'bandstart_m20_z%d_row_record' % z,
            'first_ever_m20_below_window_row_z%d_bandstart_pinning' % z,
            {'co_token_20_allowed': True,
             's_domain': '{20..58}', 'arity_max': 3,
             'style': 'x0 published residual-band style',
             'registered_by': 'kit-1 log S5 item (5) band-start pinning, restricted at build time by the strip-overlap census to the genuinely-unmeasured slices',
             'candidate': '0 separations (in-band-clean precedent: six bands m=13..18 + kit-1 m=20 z in {30..37} all clean)',
             'band': 'm=20 in-band window extended below: published z in {30..37} (kit-1), this row z=%d; the z in {21..26} x0-equivalent rows are contained in the published z21-min16 / z22 / z23-floor17 / z24-floor18 / z25-min20 / z26-floor20 strip sweeps (0 violations) and are derivable-clean, not re-swept' % z},
            R, z, 20, 20, 58))

    # (d) future-slice registration constants (engine-free, NOT measured)
    out.append({'section': 'future_slice_registration_constants',
                'label': 'engine_free_paper_only_K0832_closed_form_next_slice_predictions_NOT_measured_here',
                'registered_for_next_execution_kit_log_S5': [
                    {'m': 19, 'z': 44, 'kind': 'one-past-of-d=3 / death-of-d=2',
                     'prediction': 'EXACTLY ONE: {19,26}@S=45 UP 1v0 (odd decay 2->1; collapse v(45,44,64)=0); {19,24} conform-DEAD at its birth+3 (collapse v(43,44,64)=1) — the second m=19 death datum class (d=2 shape)'},
                    {'m': 19, 'z': 45, 'kind': 'birth slice d=4',
                     'prediction': 'EXACTLY TWO: stick {19,26}@S=45 DOWN 1v2 (collapse v(45,45,65)=2) + NEW {19,28}@S=47 UP 2v0 (collapse v(47,45,65)=0), d=4 seat gap 9'},
                    {'m': 20, 'z': 45, 'kind': 'one-past-of-d=3 / death-of-d=2',
                     'prediction': 'EXACTLY ONE: (20,26)@S=46 DOWN 0v1 (even decay 2->0; collapse v(46,45,66)=1); (20,24) conform-DEAD at its birth+3 (collapse v(44,45,66)=0) — the second m=20 death datum class (d=2 shape)'},
                    {'m': 20, 'z': 46, 'kind': 'birth slice d=4',
                     'prediction': 'EXACTLY TWO: stick (20,26)@S=46 DOWN 0v2 (collapse v(46,46,67)=2) + NEW (20,28)@S=48 UP 2v1 (collapse v(48,46,67)=1), d=4 seat gap 8'},
                    {'m': 21, 'z': 41, 'kind': 'frontier first contact (FIRST-EVER m=21 row proposal)',
                     'prediction': 'EXACTLY ONE: {21,22}@S=43 UP 2v0 (collapse v(43,41,63)=0); z*(21)=2*21-2+1=41 per K1268; the parity frontier law 9th datum candidate (8/8 through m=20)'},
                    {'m': 22, 'z': 42, 'kind': 'frontier first contact (FIRST-EVER m=22 row proposal)',
                     'prediction': 'EXACTLY ONE: (22,22)@S=44 UP 2v1 (collapse v(44,42,65)=1); z*(22)=42 per K1268; the parity frontier law 10th datum candidate'},
                    {'m': 21, 'z': '33..40', 'kind': 'in-band window sweep proposal',
                     'prediction': '0 separations each (candidate); strip-overlap status to be re-probed at the next kit build (the z=33..40 census kits do not exist yet)'},
                    {'m': 22, 'z': '34..41', 'kind': 'in-band window sweep proposal',
                     'prediction': '0 separations each (candidate); strip-overlap status to be re-probed at the next kit build'}]})

    # (e) published anchor rechecks (40 spots, verbatim published values)
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
                'label': 'forty_published_spots_reproduce_exactly_match_field_is_value_equality_with_published',
                'rows': rechecks,
                'note': 'the separation spots are separations by construction (value != collapse BY DESIGN); the z=25/z=26 base spots are published CONFORM values inside the window rows; the match criterion is equality with the PUBLISHED value'})

    res = {'result': 'EXPLORE-DONE', 'sections': out}
    print(json.dumps(res, sort_keys=True, separators=(',', ':')))


if __name__ == '__main__':
    main()
