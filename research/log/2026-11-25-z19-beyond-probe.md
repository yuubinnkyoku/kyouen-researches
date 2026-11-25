# 2026-11-25 z=19 beyond/frontier spot-probe — log

Lane: high-speed lane (this run), the direct follow-up of the z18-min13
census kit published earlier in the same session (kit commit `f152a6f5`).
Document type: PRIMARY RECORD log of the frozen spot-probe
`research/experiments/strip-z19-beyond-probe-20261125/`. No K slot
claimed, no universal statement. All content is finite machine observation
against the pinned raw engine plus one engine-free closed-form
pre-computation.

## 1. Why this probe, and why now

The z18-min13 census measured, among other things:
- the first even-m frontier data point: m=10 at z=18 = z*(10) with
  EXACTLY one separation X=(10,10) UP 2v1 (the diagonal), giving the
  frontier parity rule candidate even-m → (m,m), odd-m → (m,m+1);
- the odd-m beyond arc: (9,10) persisted one slice beyond the frontier
  with value decay 2→1, NO reabsorption, NO direction flip;
- the m=8 beyond set EMPTY for the first time (z=18), after the SHRINK
  event at z=17;
- three candidate regularities (F-tail typology alternation, supply
  identity break structure, base-spot alternation) each needing one
  more discriminating data point.

The z=19 slice is exactly where these series branch: first beyond slice
for m=10 (does the diagonal flip at +1 like (8,8)?), second beyond slice
for m=9 (does (9,10) reabsorb / flip / persist?), first re-emergence test
for the empty m=8 set, and the tenth-tail supply identity pre-computation
for the z=19 census lane. The probe freezes all of them in 766 shapes of
IDENTICAL published enumerations (position-by-position cross-slice
comparability), at ~6.5 s per run.

## 2. Determination and verification

- Adaptation basis: the pinned engine (byte-clone from the z18 kit,
  sha256 `582c93c1…`, startup pin `bd5f22e4…` asserted at engine_gate)
  + the published enumeration forms of the z18-min13 records. No other
  source.
- FIVE runs: default, PYTHONHASHSEED=1 same cwd, env -i isolated
  directories x2 (explicit `/usr/local/bin/python3`), plus the frozen
  default run: ALL BYTE-IDENTICAL (sha256
  `045df5208318c7628c1cb705d44e2be95a9a8b2c8ee9f1f76417934d1a1ffc03`).
- Independent ordered-engine cross-check (outside the frozen artifact):
  ALL 766 shapes of the three row records re-evaluated with H_ordered:
  0 mismatches.
- The kit files and this log are pushed to main in a single commit;
  the fetch-back byte verification of every pushed file against the
  commit sha follows immediately after the push (same session; any
  mismatch would be recorded as an incident in the next lane entry).

## 3. Findings (observational)

1. **Even-m beyond-arc rule strengthened to 2/2**: m=10 at z=19
   (first beyond slice): (10,10) FLIPS UP->DOWN (0 vs 1) at S=20 — the
   same flip-at-+1 as (8,8) at z=14 -> z=15. Candidate rule: even-m
   diagonal frontier separations flip DOWN at +1. m=8 also persisted
   DOWN at +2 before reabsorbing at +3; the m=10 +2 slice record
   belongs to the (future) z=20 probe or the z=19 census extensions.
2. **Odd-m beyond arc is genuinely different and now fully sketched**:
   (9,10) does NOT reabsorb at +2 — it FLIPS UP->DOWN (1 vs 2 — note
   the collapse value also flipped to 2, so the DOWN is against a
   HIGHER collapse), AND a NEW separation (9,12) (gap +3, S=21, UP 2v0)
   is born at +2. The odd-m pattern candidate: flip of the (m,m+1)
   separation at +2 (vs +1 for even m) with a same-slice birth of a new
   gap-(m,m+3) separation (vs (m,m+2) for even m at +2). Every one of
   these numbers is a single series data point; no law is claimed.
3. **Empty beyond sets are stable**: m=8 at z=19 remains 0 separations
   (two consecutive empty slices). No position has ever re-emerged
   after reabsorption anywhere in the series so far.
4. **Supply identity parity structure (engine-free)**: v(s,20,20)=
   v(s,19,20) holds on {0}∪{12..19}, breaks uniformly 0v1 for all
   s>=20 — the odd-z identity shape (hold through s=z, uniform 0v1
   break from z+1) now has 2/2 odd data points (z=17, z=19), while the
   even-z identities break AT s=z (z=16 published, z=18 with its
   0v2/2v1 double profile rechecked over the extended domain in this
   probe's frozen output). This is consistent with the F-tail
   typology alternation (hole+tail at odd z needs the identity intact
   through the hole; single point at even z needs the break AT z).
5. **Base-spot alternation 4/4**: 0 (z16), 1 (z17), 0 (z18), 1 (z19).
6. **z=19 provisional claim spots**: 15/15 match at R=m+20 for
   m∈{13..17} — no surprise ahead of the z=19 census, as expected at
   this depth.

## 4. Honest record

- The probe was built AFTER the z18 census was published, from the
  published z18 enumerations and the pinned engine only. Predeclared
  candidate outcomes for (a)/(b) were written into the frozen script's
  docstring BEFORE the first run (flip-vs-vanish for (10,10);
  reabsorb/persist/decay for (9,10)) — the script bytes assert this
  ordering structurally (the docstring was written before execution;
  the runs then froze stdout).
- All three records reuse the EXACT published enumeration forms, so
  shape counts are forced (170/234/362) and appear unchanged — a
  machine-checked comparability property, not an assertion.
- The (9,12) separation is NEW relative to the published z=17/z=18
  records (the same S=21 shape was enumerated there and matched its
  collapse); this is visible in the published .out files of the z16-min9
  and z18-min13 kits, which record no (9,12) entry.

## 5. Handoff

- The z=19 census kit (floor-14) remains the entry point for the T-Z19
  declaration; this probe does not replace it. The probe's identity
  pre-computation (hold {0,12..19}, 0v1 break from s=20) is the supply
  input its F-cell derivation should use.

- Natural next probes after this one: the m=10 z=20 record (+2 past
  the frontier; does the flipped (10,10) persist DOWN like (8,8) did,
  or reabsorb early?); the m=9 z=20 record (+3 past the frontier; the
  (8,8) analogy predicts (9,10) reabsorbs around +3, and the (9,12)
  birth's next move is unmeasured); the m=11 frontier at z=21 (=z*(11),
  odd m → off-diagonal (11,12) predicted by the frontier parity rule,
  1/1 so far on odd m). The m=11 row residual band entries z∈{19,20}
  (in-band) belong to the z=19/z=20 census kits, not to this probe
  series. The declaration lane should recompute all z*(m) values from
  the published K1268 statement rather than trusting this log's inline
  arithmetic.
- F-family: the typology alternation predicts the z=19 F-cell has the
  hole+tail profile (single DOWN @ s=18, hole @ s=19, tail @ s>=20 —
  the +2-shifted z=17 profile); the z=19 census decides.

## 6. Standard caveats

Finite machine observation only. No theorem, no universal claim, no
verdict consumed. Standard 11×11 empty board, two-stone roots, S2,
classes 1/2/4 and all central-reply roots: all UNKNOWN, unchanged.
