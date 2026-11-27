#!/usr/bin/env python3
"""
explore_inband_m19m20: FROZEN PRE-DECLARATION census for the IN-BAND
z=29..33 row records of the m=16/17/18 residual bands (the T-Z21 /
T-Z22 / T-Z24 band COMPLETIONS), the FIRST-EVER m=19 / m=20 rows
(the full new in-band residual-band sweeps z in {29..36} and
{30..37}, the FRONTIER first-contact rows at z=37 / z=38, the
ONE-PAST companion rows at z=38 / z=39, and the TWO-PAST birth-slice
rows at z=39 / z=40), plus 30 published anchor rechecks. NO K slot
is claimed by this file; the constants below were frozen into this
docstring BEFORE the first run of this file and the file has not
been edited after any of its runs.

Registered provenance (all BEFORE any measurement by this kit):
- The in-band rows m=16@z=29, m=17@z in {29..32}, m=18@z in
  {29..33} are the REGISTERED items of the published
  frontier-lifecycle kit log section 5 item (2) (commit dc7f36e1,
  research/log/2026-11-26-frontier-lifecycle-z27z28-rows-and-tail26.md):
  "m=16@z=29 (R=46) = T-Z21 band completion entry (3rd band), then
  m=17 z in {29..32} (T-Z22 6/10), m=18 z in {29..33} (T-Z24 4/9)".
- The FRONTIER rows m=19@z=37 and m=20@z=38 are the REGISTERED
  items of the same log section 5 item (1): "frontier parity rule
  candidate next points: m=19@z=37 (prediction {19,20}@S=39 UP 2v0,
  collapse v(39,37,57)=0) and m=20@z=38 ({20,20}@S=40 UP 2v1)".
  Both also follow the published six-band separation life-cycle
  scaffold (wavetrain/fifthwave/sixthwave logs section 3): births
  at slices z*(m)+2d at shapes (m, m+2d+1) for ODD m / (m, m+2d)
  for EVEN m (K1268: z*(m)=2m-2+(m mod 2); z*(19)=37, z*(20)=38),
  born UP 2v0 (odd) / UP 2v1 (even).
- The ONE-PAST and TWO-PAST m=19/m=20 rows are KIT-ADDED here,
  derived BEFORE the freeze from the published six-band life-cycle
  scaffold (one-past parity decay odd 2->1, even 2->0; two-past =
  birth slice: previous stuck + newborn; the m=13@z=26/z=27 and
  m=14@z=27/z=28 measured analogues). They are registered binding
  candidates, spelled out in full below; any deviation is itself
  the datum and is recorded verbatim.
- The FULL in-band residual-band sweeps for the NEW bands m=19
  (z in {29..36} = z*-8..z*-1, 8 entries) and m=20 (z in
  {30..37}, 8 entries) are KIT-ADDED first coverage: NO published
  m=19 or m=20 row exists anywhere in main at kit-build time
  (verified by content search_code probe, not only guessed paths;
  the wave-lane kits strip-wavetrain / strip-fifthwave /
  strip-sixthwave published ONLY past slices z >= z*(m) of the
  bands m=13..18, per their own slot-check paragraphs). Registered
  candidate: 0 separations at every entry, by the in-band-clean
  precedent (all six bands m=13..18, every measured in-band
  slice, published 0 separations). Any deviation is the datum.

Counter-probe (content-based, per the registered lesson; re-run at
push time against the then-current main): at kit-build time
(2026-11-26T08:33Z, main head 28ed2d9c) the content queries
"inband_m17_z29", "m16_z29", "m19_z37", "frontier_m19", "explore_z29"
return NO measurement record; the only published z=29..33 engine
values are the z=29..32 touch QUADS u1..u4 / w1..w4 / x1..x4
(0,1,1,0 each, decay/wavetrain/fifthwave/sixthwave kits — rechecked
here as in-record anchors), the frontier / one-past / two-past
m=13..18 row records at their own slices (per the wave-lane slot
checks; fully disjoint from the m=19/m=20 rows measured here), and
the four z=28 handoff spots (lifecycle kit). No published engine
value exists for ANY m=19 or m=20 position, and none for the
in-band rows m=16@z=29 / m=17@z in {29..32} / m=18@z in {29..33}
(only m=15@z=29 frontier / m=16@z=30 frontier / m=17@z in
{33,...} past-side rows are published, all outside this kit's
in-band scopes).

HONEST DISCLOSURE (paper arithmetic, before the freeze): every
collapse constant stated below is the PROVED K0832 single-token
closed form computed on paper (engine-free), re-derived twice (draft
+ numeric sample check with the closed form only, no engine
recursion); the quoted published touch / anchor values are verbatim
citations of the published logs read BEFORE the freeze. NO engine
recursion on ANY position listed below was evaluated before the
freeze — every engine value in the sections (b)..(g) is touched for
the FIRST time at the frozen first run; the sole exceptions are the
30 published anchor spots of section (h), which must reproduce
their published values exactly.

Scope (this file measures and reports; it proves nothing by
itself):

  (a) K0832 battery: every single-token literal used by this
      file's candidate constants, derivations, staircase samples
      (row edges and co-token seats for every measured row), the
      future-slice registration constants, and the anchor
      collapses — checked closed-form vs canonical-engine vs
      ordered-engine. Candidate: all match.
  (b) IN-BAND row records, published residual-band x0 style
      (X = parts(S, m, 3) with X[0] == m, all parts >= m, co-token
      m allowed, arity <= 3 TOTAL, S in {m..m+38}, R = m+z+1),
      recorded against the collapse v(S,z,R):
      - m=16 @ z=29, R=46, 40 shapes: the EIGHTH and LAST entry of
        the future T-Z21 residual band m=16 z in {22..29} (7
        published entries 40/0 at z=22..28) — the BAND COMPLETION.
        Candidate 0 separations.
      - m=17 @ z=29..32, R=47..50, 32 shapes each: the SEVENTH
        through TENTH entries of the future T-Z22 residual band
        m=17 z in {23..32} (6 published entries 32/0 at z=23..28)
        — z=32 is the BAND COMPLETION. Candidate 0 separations each.
      - m=18 @ z=29..33, R=48..52, 26 shapes each: the FIFTH
        through NINTH entries of the future T-Z24 residual band
        m=18 z in {25..33} (4 published entries 26/0 at z=25..28)
        — z=33 is the BAND COMPLETION; its clean entry would also
        derivative-confirm the registered z=33 touch candidate x3
        (a clean row proves H(52;(18,18);33) = v(36,33,52) = 1).
        Candidate 0 separations each.
      - m=19 @ z=29..36, R=49..56, 22 shapes each: the FIRST-EVER
        m=19 rows — the NEW m=19 in-band residual band sweep, 8
        entries (z*(19)=37; window z*-8..z*-1, band-start
        convention at declaration time TBD). Candidate 0
        separations each; any deviation is the datum.
      - m=20 @ z=30..37, R=51..58, 20 shapes each: the FIRST-EVER
        m=20 rows — the NEW m=20 in-band residual band sweep, 8
        entries (z*(20)=38; window z*-8..z*-1). Candidate 0
        separations each.
  (c) ARITY<=4 co-token extension sweeps (published ext style,
      X = (m,) + parts(S-m, m, 3), arity up to 4 TOTAL): m=16@z=29
      and m=17@z=32 and m=18@z=29..33 at the completion-band
      slices (first exts for m=16/m=17; m=18 exts continue the
      published z=24..z=28 ext series); candidate 0 separations.
      PLUS the first-ever exts for m=19/m=20 at their frontier
      slices (d).
  (d) FRONTIER first-contact rows (REGISTERED binding candidates,
      frontier-lifecycle log S5 item (1); the parity-corrected
      frontier-record law, 6 published data points m=13..18 all
      HIT):
      - m=19 @ z=37, R=57, S in {19..57}, 22 shapes: candidate
        EXACTLY ONE separation X={19,20} @S=39, UP 2v0 (value 2 vs
        collapse v(39,37,57)=0 on paper); all other 21 shapes
        conform.
      - m=20 @ z=38, R=59, S in {20..58}, 20 shapes: candidate
        EXACTLY ONE separation X=(20,20) @S=40, UP 2v1 (value 2 vs
        collapse v(40,38,59)=1 on paper); all other 19 shapes
        conform.
  (e) ONE-PAST rows (KIT-ADDED, scaffold-derived binding
      candidates, measured in the same run as the frontier rows):
      - m=19 @ z=38, R=58: candidate EXACTLY ONE separation
        {19,20} @S=39, UP 1v0 (odd decay 2->1; collapse
        v(39,38,58)=0 on paper); no other separation.
      - m=20 @ z=39, R=60: candidate EXACTLY ONE separation
        (20,20) @S=40, DOWN 0v1 (even decay 2->0; collapse
        v(40,39,60)=1 on paper); no other separation.
  (f) TWO-PAST birth-slice rows (KIT-ADDED scaffold-derived binding
      candidates — the d=1 birth seats of the new bands):
      - m=19 @ z=39, R=59: candidate EXACTLY TWO separations:
        stick {19,20} @S=39 DOWN 1v2 (stuck value 1 vs collapse
        v(39,39,59)=2 — the z==x collapse jump, paper) + NEW birth
        {19,22} @S=41 UP 2v0 (collapse v(41,39,59)=0 on paper),
        d=1 seat gap 3 (odd law shape (m, m+2d+1)).
      - m=20 @ z=40, R=61: candidate EXACTLY TWO separations:
        stick (20,20) @S=40 DOWN 0v2 (stuck value 0 vs collapse
        v(40,40,61)=2 on paper) + NEW birth (20,22) @S=42 UP 2v1
        (collapse v(42,40,61)=1 on paper), d=1 seat gap 2 (even
        law shape (m, m+2d)).
  (g) FUTURE-SLICE REGISTRATION CONSTANTS (paper-only section,
      engine-free, K0832 closed form; battery-checked but NOT
      measured): the next two slices of each new band — m=19@z=40
      one-past prediction EXACTLY ONE {19,22}@S=41 UP 1v0
      (collapse v(41,40,60)=0) with {19,20} conform-DEAD at its
      birth+3 slice (collapse v(39,40,60)=1; death datum for the
      m=19 d=0 shape); m=19@z=41 birth slice EXACTLY TWO: stick
      {19,22} DOWN 1v2 (collapse v(41,41,61)=2) + NEW {19,24}@S=43
      UP 2v0 (collapse v(43,41,61)=0), d=2 seat gap 5; m=20@z=41
      one-past-of-d=1 / three-past-of-d=0 prediction EXACTLY ONE
      (20,22)@S=42 DOWN 0v1 (collapse v(42,41,62)=1) with (20,20)
      conform-DEAD at its birth+3 (collapse v(40,41,62)=0); m=20
      @z=42 birth slice EXACTLY TWO: stick (20,22) DOWN 0v2
      (collapse v(42,42,63)=2) + NEW (20,24)@S=44 UP 2v1 (collapse
      v(44,42,63)=1), d=2 seat gap 4. Registered in the kit log
      section 5 for the next execution.
  (h) published anchor rechecks (30 spots, all values verbatim
      from the published logs): the four z=28 handoff spots (0,1,
      1,0 — lifecycle kit), the z=29..z=32 touch quads u/w/x
      (0,1,1,0 each — decay/wavetrain/fifthwave/sixthwave kits),
      the frontier m=15@z=29 / m=16@z=30 separations (2,2), the
      one-past m=15@z=30 / m=16@z=31 separations (1,0), the
      two-past-with-birth m=13@z=27 separations (1,2), and the
      m=17@z=35 / m=13@z=33 two-past sticks+births (1,2 / 1,2) —
      must all reproduce exactly.

Everything is a pure function of the pinned engine bytes; no
randomness, no hash-seed dependence, no wall-clock in the output.
stdout is the frozen artifact (explore_inband_m19m20.out).
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
    for (m, z) in [(16, 29), (17, 29), (17, 30), (17, 31), (17, 32),
                   (18, 29), (18, 30), (18, 31), (18, 32), (18, 33),
                   (19, 29), (19, 30), (19, 31), (19, 32), (19, 33),
                   (19, 34), (19, 35), (19, 36), (19, 37), (19, 38),
                   (19, 39),
                   (20, 30), (20, 31), (20, 32), (20, 33), (20, 34),
                   (20, 35), (20, 36), (20, 37), (20, 38), (20, 39),
                   (20, 40)]:
        R = m + z + 1
        for S in (m, m + 2, 2 * m, 2 * m + 1, m + 37, m + 38):
            battery_lits.append((S, z, R))
        rows_stair.append((m, z, R))
    # candidate collapse constants (frontier / one-past / birth)
    for (x, z2, R2) in [
            (39, 37, 57), (40, 38, 59),
            (39, 38, 58), (40, 39, 60),
            (39, 39, 59), (41, 39, 59), (40, 40, 61), (42, 40, 61)]:
        battery_lits.append((x, z2, R2))
    # future-slice registration constants (section (g), NOT measured)
    for (x, z2, R2) in [
            (41, 40, 60), (39, 40, 60), (41, 41, 61), (43, 41, 61),
            (42, 41, 62), (40, 41, 62), (42, 42, 63), (44, 42, 63)]:
        battery_lits.append((x, z2, R2))
    # anchor collapse literals (section (h))
    anchor_spec = [
        (46, (17, 18), 28), (45, (16, 17), 28), (47, (18, 18), 28),
        (46, (17, 17), 28),
        (47, (17, 18), 29), (46, (16, 17), 29), (48, (18, 18), 29),
        (47, (17, 17), 29),
        (48, (17, 18), 30), (47, (16, 17), 30), (49, (18, 18), 30),
        (48, (17, 17), 30),
        (49, (17, 18), 31), (48, (16, 17), 31), (50, (18, 18), 31),
        (49, (17, 17), 31),
        (50, (17, 18), 32), (49, (16, 17), 32), (51, (18, 18), 32),
        (50, (17, 17), 32),
        (45, (15, 16), 29), (47, (16, 16), 30),
        (41, (13, 14), 27), (41, (13, 16), 27),
        (53, (17, 18), 35), (53, (17, 20), 35),
        (47, (13, 20), 33), (47, (13, 22), 33),
        (46, (15, 16), 30), (48, (16, 16), 31)]
    for (R, X, z2) in anchor_spec:
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

    # (b) IN-BAND row records
    ib = [('m16', 16, 29, 'eighth_last_tz21_band_completion',
           'future T-Z21 residual band m=16 z in {22..29} (frontier z*(16)=30 per K1268); published entries 40/0 at z=22..28 (z22f16..z28 lifecycle kits); REGISTERED candidate (frontier-lifecycle kit dc7f36e1 log S5 item (2)): 0 separations — this entry COMPLETES the band (third fully-swept band of the series after K1330 m=14 and K1335 m=15)'),
          ]
    # m=16 z=29
    out.append(row_record_x0(
        'inband_m16_z29_row_record',
        'tz21_band_completion_eighth_last_m16_z29',
        {'co_token_16_allowed': True,
         's_domain': '{16..54}', 'arity_max': 3,
         'style': 'x0 published residual-band style',
         'registered_by': 'frontier-lifecycle kit log S5 item (2) (commit dc7f36e1)',
         'candidate': '0 separations',
         'band': ib[0][4]},
        46, 29, 16, 16, 54))
    out.append(row_record(
        'inband_m16_z29_row_record_ext_arity4',
        'arity_le4_extension_cotoken_style_first_m16_ext',
        {'co_token_16_allowed': True,
         's_domain': '{16..54}', 'arity_max': 4,
         'registered_by': 'kit-added first m=16 ext (published ext precedent is m=18-only)'},
        46, 29, 16, 16, 54, 16))
    # m=17 z=29..32
    for i, z in enumerate(range(29, 33)):
        R = 17 + z + 1
        comp = 'this entry COMPLETES the future T-Z22 residual band (fourth fully-swept band candidate)' if z == 32 else (
            'the remaining in-band slice(s) after this are {%s} (T-Z22 %d/10)' % (
                ','.join(str(t) for t in range(z + 1, 33)), 7 + i))
        out.append(row_record_x0(
            'inband_m17_z%d_row_record' % z,
            'tz22_residual_band_m17_z%d_entry_%d' % (z, 7 + i),
            {'co_token_17_allowed': True,
             's_domain': '{17..55}', 'arity_max': 3,
             'style': 'x0 published residual-band style',
             'registered_by': 'frontier-lifecycle kit log S5 item (2) (commit dc7f36e1)',
             'candidate': '0 separations',
             'band': 'future T-Z22 residual band m=17 z in {23..32} (frontier z*(17)=33); published entries 32/0 at z=23..28; ' + comp},
            R, z, 17, 17, 55))
    out.append(row_record(
        'inband_m17_z32_row_record_ext_arity4',
        'arity_le4_extension_cotoken_style_first_m17_ext_band_completion_slice',
        {'co_token_17_allowed': True,
         's_domain': '{17..55}', 'arity_max': 4,
         'registered_by': 'kit-added first m=17 ext at the band-completion slice'},
        50, 32, 17, 17, 55, 17))
    # m=18 z=29..33
    for z in range(29, 34):
        R = 18 + z + 1
        comp = 'this entry COMPLETES the future T-Z24 residual band (fifth fully-swept band candidate); a clean row also derivative-confirms the registered z=33 touch candidate x3 = 1 (clean row proves H(52;(18,18);33) = v(36,33,52) = 1)' if z == 33 else (
            'remaining in-band slices after this: z in {%s} (T-Z24 %d/9)' % (
                ','.join(str(t) for t in range(z + 1, 34)), z - 24))
        out.append(row_record_x0(
            'inband_m18_z%d_row_record' % z,
            'tz24_residual_band_m18_z%d_entry_%d' % (z, z - 24),
            {'co_token_18_allowed': True,
             's_domain': '{18..56}', 'arity_max': 3,
             'style': 'x0 published residual-band style',
             'registered_by': 'frontier-lifecycle kit log S5 item (2) (commit dc7f36e1)',
             'candidate': '0 separations',
             'band': 'future T-Z24 residual band m=18 z in {25..33} (frontier z*(18)=34); published entries 26/0 at z=25..28; ' + comp},
            R, z, 18, 18, 56))
        out.append(row_record(
            'inband_m18_z%d_row_record_ext_arity4' % z,
            'arity_le4_extension_cotoken_style_published_m18_ext_series',
            {'co_token_18_allowed': True,
             's_domain': '{18..56}', 'arity_max': 4,
             'registered_by': 'published m=18 ext series continuation (z24f18..lifecycle kits measured z=24..28 exts)'},
            R, z, 18, 18, 56, 18))
    # m=19 z=29..36 (first-ever m=19 rows; new band sweep)
    for z in range(29, 37):
        R = 19 + z + 1
        out.append(row_record_x0(
            'inband_m19_z%d_row_record' % z,
            'first_ever_m19_row_new_band_sweep_entry_z%d' % z,
            {'co_token_19_allowed': True,
             's_domain': '{19..57}', 'arity_max': 3,
             'style': 'x0 published residual-band style',
             'registered_by': 'kit-added full new-band sweep (no prior registration needed: no published m=19 value exists; discovered free slot by content probe at kit-build)',
             'candidate': '0 separations (in-band-clean precedent: all six bands m=13..18, every measured in-band slice, published 0 separations)',
             'band': 'NEW m=19 in-band residual band, z in {29..36} = z*(19)-8..z*(19)-1 (z*(19)=37 per K1268); 8 entries, band-start convention at declaration time TBD'},
            R, z, 19, 19, 57))
    # m=20 z=30..37 (first-ever m=20 rows; new band sweep)
    for z in range(30, 38):
        R = 20 + z + 1
        out.append(row_record_x0(
            'inband_m20_z%d_row_record' % z,
            'first_ever_m20_row_new_band_sweep_entry_z%d' % z,
            {'co_token_20_allowed': True,
             's_domain': '{20..58}', 'arity_max': 3,
             'style': 'x0 published residual-band style',
             'registered_by': 'kit-added full new-band sweep (no published m=20 value exists; free slot by content probe)',
             'candidate': '0 separations (in-band-clean precedent, six bands m=13..18)',
             'band': 'NEW m=20 in-band residual band, z in {30..37} = z*(20)-8..z*(20)-1 (z*(20)=38 per K1268); 8 entries, band-start convention TBD'},
            R, z, 20, 20, 58))

    # (d) FRONTIER first-contact rows (REGISTERED candidates)
    out.append(row_record_x0(
        'frontier_m19_z37_row_record',
        'frontier_record_m19_z37_registered_parity_candidate_odd_K1268_L7th_datum',
        {'co_token_19_allowed': True,
         's_domain': '{19..57}', 'arity_max': 3,
         'style': 'x0 published residual-band style',
         'registered_by': 'frontier-lifecycle kit log S5 item (1) (commit dc7f36e1): m=19@z=37 prediction {19,20}@S=39 UP 2v0, collapse v(39,37,57)=0',
         'candidate': 'EXACTLY ONE separation X={19,20} @S=39, UP 2v0 (value 2 vs collapse v(39,37,57)=0 on paper); all other 21 shapes conform; parity law through m=18 is 6/6 HIT; any deviation (extra/missing/different separation) is the datum and is recorded verbatim',
         'z_star': 'z*(19)=2*19-2+1=37 EXACTLY (K1268)'},
        57, 37, 19, 19, 57))
    out.append(row_record(
        'frontier_m19_z37_row_record_ext_arity4',
        'arity_le4_extension_cotoken_style_first_m19_ext_at_frontier',
        {'co_token_19_allowed': True,
         's_domain': '{19..57}', 'arity_max': 4,
         'registered_by': 'kit-added first m=19 ext at the frontier slice'},
        57, 37, 19, 19, 57, 19))
    out.append(row_record_x0(
        'frontier_m20_z38_row_record',
        'frontier_record_m20_z38_registered_parity_candidate_even_K1268_L8th_datum',
        {'co_token_20_allowed': True,
         's_domain': '{20..58}', 'arity_max': 3,
         'style': 'x0 published residual-band style',
         'registered_by': 'frontier-lifecycle kit log S5 item (1) (commit dc7f36e1): m=20@z=38 prediction {20,20}@S=40 UP 2v1, collapse v(40,38,59)=1',
         'candidate': "EXACTLY ONE separation X=(20,20) @S=40, UP 2v1 (value 2 vs collapse v(40,38,59)=1 on paper); all other 19 shapes conform; any deviation is the datum",
         'z_star': 'z*(20)=2*20-2+0=38 EXACTLY (K1268)'},
        59, 38, 20, 20, 58))
    out.append(row_record(
        'frontier_m20_z38_row_record_ext_arity4',
        'arity_le4_extension_cotoken_style_first_m20_ext_at_frontier',
        {'co_token_20_allowed': True,
         's_domain': '{20..58}', 'arity_max': 4,
         'registered_by': 'kit-added first m=20 ext at the frontier slice'},
        59, 38, 20, 20, 58, 20))

    # (e) ONE-PAST rows (kit-added scaffold-derived binding candidates)
    out.append(row_record_x0(
        'onepast_m19_z38_row_record',
        'one_past_frontier_record_m19_z38_scaffold_candidate_odd_decay',
        {'co_token_19_allowed': True,
         's_domain': '{19..57}', 'arity_max': 3,
         'style': 'x0 published residual-band style',
         'registered_by': 'kit-added (six-band life-cycle scaffold one-past parity decay odd 2->1, 14 observations; measured in the same run as the frontier row)',
         'candidate': 'EXACTLY ONE separation {19,20} @S=39, UP 1v0 (value 1 vs collapse v(39,38,58)=0 on paper); no other separation; any deviation is the datum'},
        58, 38, 19, 19, 57))
    out.append(row_record_x0(
        'onepast_m20_z39_row_record',
        'one_past_frontier_record_m20_z39_scaffold_candidate_even_decay',
        {'co_token_20_allowed': True,
         's_domain': '{20..58}', 'arity_max': 3,
         'style': 'x0 published residual-band style',
         'registered_by': 'kit-added (six-band life-cycle scaffold one-past parity decay even 2->0, 13 observations; measured in the same run as the frontier row)',
         'candidate': 'EXACTLY ONE separation (20,20) @S=40, DOWN 0v1 (value 0 vs collapse v(40,39,60)=1 on paper); no other separation; any deviation is the datum'},
        60, 39, 20, 20, 58))

    # (f) TWO-PAST birth-slice rows (kit-added scaffold-derived binding candidates)
    out.append(row_record_x0(
        'twopast_m19_z39_row_record',
        'two_past_birth_slice_record_m19_z39_scaffold_candidate_d1_seat',
        {'co_token_19_allowed': True,
         's_domain': '{19..57}', 'arity_max': 3,
         'style': 'x0 published residual-band style',
         'registered_by': 'kit-added (six-band life-cycle scaffold: birth slices z*(m)+2d, d=1 here; odd law shape (m, m+2d+1) = {19,22})',
         'candidate': 'EXACTLY TWO separations: stick {19,20} @S=39 DOWN 1v2 (stuck value 1 vs collapse v(39,39,59)=2 on paper — the z==x collapse jump) + NEW birth {19,22} @S=41 UP 2v0 (collapse v(41,39,59)=0 on paper), d=1 seat gap 3; any deviation is the datum'},
        59, 39, 19, 19, 57))
    out.append(row_record_x0(
        'twopast_m20_z40_row_record',
        'two_past_birth_slice_record_m20_z40_scaffold_candidate_d1_seat',
        {'co_token_20_allowed': True,
         's_domain': '{20..58}', 'arity_max': 3,
         'style': 'x0 published residual-band style',
         'registered_by': 'kit-added (six-band life-cycle scaffold: birth slices z*(m)+2d, d=1 here; even law shape (m, m+2d) = (20,22))',
         'candidate': 'EXACTLY TWO separations: stick (20,20) @S=40 DOWN 0v2 (stuck value 0 vs collapse v(40,40,61)=2 on paper) + NEW birth (20,22) @S=42 UP 2v1 (collapse v(42,40,61)=1 on paper), d=1 seat gap 2; any deviation is the datum'},
        61, 40, 20, 20, 58))

    # (g) future-slice registration constants (engine-free, NOT measured)
    out.append({'section': 'future_slice_registration_constants',
                'label': 'engine_free_paper_only_K0832_closed_form_next_slice_predictions_NOT_measured_here',
                'registered_for_next_execution_kit_log_S5': [
                    {'m': 19, 'z': 40, 'kind': 'one-past-of-d=1 / death-of-d=0',
                     'prediction': 'EXACTLY ONE: {19,22}@S=41 UP 1v0 (collapse v(41,40,60)=0); {19,20} conform-DEAD at its birth+3 slice (collapse v(39,40,60)=1) — first m=19 death datum (d=0 shape)'},
                    {'m': 19, 'z': 41, 'kind': 'birth slice d=2',
                     'prediction': 'EXACTLY TWO: stick {19,22}@S=41 DOWN 1v2 (collapse v(41,41,61)=2) + NEW {19,24}@S=43 UP 2v0 (collapse v(43,41,61)=0), d=2 seat gap 5'},
                    {'m': 20, 'z': 41, 'kind': 'one-past-of-d=1 / death-of-d=0',
                     'prediction': 'EXACTLY ONE: (20,22)@S=42 DOWN 0v1 (collapse v(42,41,62)=1); (20,20) conform-DEAD at its birth+3 (collapse v(40,41,62)=0) — first m=20 death datum (d=0 shape)'},
                    {'m': 20, 'z': 42, 'kind': 'birth slice d=2',
                     'prediction': 'EXACTLY TWO: stick (20,22)@S=42 DOWN 0v2 (collapse v(42,42,63)=2) + NEW (20,24)@S=44 UP 2v1 (collapse v(44,42,63)=1), d=2 seat gap 4'}]})

    # (h) published anchor rechecks (30 spots, verbatim published values)
    anchors = [
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
    ]
    rechecks = []
    H.cache_clear()
    for (R, X, z2, expected, role) in anchors:
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
                'label': 'thirty_published_spots_reproduce_exactly_match_field_is_value_equality_with_published',
                'rows': rechecks,
                'note': 'the frontier/one-past/two-past anchor spots are separations by construction (value != collapse BY DESIGN); the match criterion is equality with the PUBLISHED value'})

    res = {'result': 'EXPLORE-DONE', 'sections': out}
    print(json.dumps(res, sort_keys=True, separators=(',', ':')))


if __name__ == '__main__':
    main()
