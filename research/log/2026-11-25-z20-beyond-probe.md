# 2026-11-25 z=20 beyond/frontier spot-probe — log

Lane: high-speed lane (this run), the direct follow-up of the z19-min14
pre-declaration census kit published earlier in the same session. Document
type: PRIMARY RECORD log of the frozen spot-probe
`research/experiments/strip-z20-beyond-probe-20261125/`. No K slot
claimed, no universal statement. All content is finite machine observation
against the pinned raw engine plus engine-free closed-form
pre-computations.

## 1. Why this probe, and why now

The published observation series had reached, at z=19:
- the even-m beyond arc with 2/2 flip-at-+1 data points ((8,8), (10,10)),
  with the m=10 +2 slice unmeasured — does the flipped diagonal persist
  DOWN at +2 like (8,8) did, or reabsorb early?
- the odd-m beyond arc fully sketched at z=19: (9,10) flipped UP->DOWN
  at +2 AND a new (9,12) gap+3 birth at +2 — the (8,8) analogy
  predicted (9,10) reabsorption around +3, untested at z=20;
- the m=8 beyond set EMPTY at both z=18 and z=19, with the recorded
  candidate "no re-emergence has ever been observed" — the stability of
  terminal emptiness untested past +4;
- the K1322 residual band m=11 z∈{17..20} one entry from closure;
- the z-parity base-spot alternation at four data points;
- the supply-identity parity structure with the odd-z form at 2/2 and
  the z=21 (twelfth-tail) identity unmeasured: the z=20 slice's own
  supply datum (the eleventh-tail identity) freshly pre-computed by the
  z19 census kit section (g2), needing a frozen cross-artifact recheck.

The z=20 slice is exactly where all of these discriminate. The probe
freezes them in the IDENTICAL published enumerations
(170/234/362/110/92/76+75 shapes), at ~10.4 s per run.

## 2. Determination and verification

- Adaptation basis: the pinned engine (byte-clone from the published
  chain, sha256 `582c93c1…`, startup pin `bd5f22e4…` asserted at
  engine_gate) + the published enumeration forms of the z18-min13 /
  z19-beyond / z19-min14 records. No other source.
- FIVE runs: default, default re-run, PYTHONHASHSEED=1 same cwd,
  env -i isolated dirs ×2 (explicit `/usr/local/bin/python3`): ALL
  BYTE-IDENTICAL (sha256
  `281311e87db85da3b608d80f5b5f79843e40ff5fcc8bb792ba0217654d19094c`,
  rc 0 each).
- Independent ordered-engine cross-check (outside the frozen artifact,
  re-executed IN FULL in this session after the environment reset):
  - all 1,119 record shapes (170+234+362+110+92+76+75) re-enumerated
    and re-evaluated with `H_ordered` against the canonical engine:
    0 mismatches; every record's shape count and separation list
    MATCHES the frozen rows exactly;
  - the 15 strip spots, the base spot and both supply identities
    re-derived from the closed forms: byte-exact against the frozen
    rows (9/37 hold/break for the eleventh; 11/36 for the twelfth).
- The kit files and this log are pushed to main in a single commit;
  the fetch-back byte verification of every pushed file follows
  immediately after the push (same session; any mismatch would be
  recorded as an incident in the next lane entry).

## 3. Findings (observational)

1. **Even-m beyond arc at +2 (2/2)**: m=10 at z=20: the flipped
   diagonal (10,10) PERSISTS DOWN (0 vs 2) at S=20 — the same +2
   persistence as (8,8) at z=16 — AND a NEW separation (10,12)
   (S=22, UP 2v1) is born at +2 past the frontier at gap +2, matching
   the (8,10) birth (gap +2, +2 past the frontier). The even-m +2
   pattern (persist DOWN + gap+2 birth) now reads 2/2 (m=8, m=10).
   The predeclared REABSORB candidate is counterexampleed.
2. **Odd-m beyond arc at +2->+3 (fully resolved for m=9)**: (9,10)
   REABSORBS at +3, exactly the (8,8)-analogy prediction from the
   z19 probe handoff; the (9,12) birth PERSISTS with value decay 2->1
   (UP 1v0 at S=21). Odd-m gap+3 births live longer than even-m gap+2
   births on this data (1 event each; no law claimed).
3. **FIRST OBSERVED RE-EMERGENCE**: the m=8 beyond set, EMPTY at
   z=18 AND z=19, is NON-EMPTY at z=20: X=(8,12) DOWN 0v2 at S=20 and
   X=(8,14) UP 2v1 at S=22 — neither position is a reabsorbed old
   position. The predeclared candidate "remains empty" is
   counterexampleed, and the z19 probe's recorded reading "total
   reabsorption is a stable terminal state / no re-emergence has ever
   been observed" is falsified at its next test. Note the S-lock
   observation: the m=8 and m=10 z=20 separation multisets coincide
   position-wise in S ((DOWN at S=20, UP 2v1 at S=22)) while their
   gaps differ ((8,12)/(8,14) vs (10,10)/(10,12)) — one event,
   recorded for the next slice's discriminating measurement.
4. **K1322 residual band m=11 CLOSED 4/4**: the z=20 entry measures
   110 shapes, 0 separations (identical enumeration); with the
   published z=17/z=18/z=19 entries also 110/0 each, the band m=11
   z∈{17..20} is fully measured. z*(11)=21: the m=11 frontier is the
   next slice's headline event (odd-m → off-diagonal (11,12) candidate
   by the frontier parity rule, 1/1 so far on odd m).
5. **K1325/K1328 in-band entries**: m=12-row z=20: 92/0 (THIRD entry
   of m=12 z∈{18..21}); m=13-row z=20: 76/0 + arity<=4 ext 75/0
   (SECOND entry of m=13 z∈{19..24}) — both cross-artifact consistent
   with the z19 census kit's same-band entries at z=19.
6. **z=20 provisional claim spots**: 15/15 match at R=m+21 for
   m∈{14..18} — no surprise ahead of the T-Z19 declaration and the
   future z=20 census, as expected at this depth.
7. **Base-spot alternation 5/5**: 0 (z16), 1 (z17), 0 (z18), 1 (z19),
   0 (z20) — the z-parity candidate held as predeclared.
8. **Supply identities (engine-free)**: the ELEVENTH-tail identity
   rechecks exactly as published by the z19 census kit section (g2):
   hold {0}∪{12..19}, 0v2 break at s=20, uniform 2v1 for s∈{21..56}
   (the exact z=18 even-z shape — the z=20 slice's supply datum, and
   the even-z newest form now 2/2). The NEW TWELFTH-tail identity
   (z=21): hold {0}∪{12..21}, UNIFORM 0v1 break for ALL s∈{22..57} —
   the predeclared odd-z candidate confirmed; the odd-z identity form
   is now 3/3 (z=17, z=19, z=21 pre-computed). The z=21 slice's
   census F-cell supply story is thereby available before that
   census runs.

## 4. Honest record

- The probe was built AFTER the z19 census kit was frozen locally, from
  the published enumerations and the pinned engine only. Predeclared
  candidate outcomes for ALL sections were written into the frozen
  script's docstring BEFORE the first run — three candidates were
  RESOLVED AGAINST: the m=10 reabsorb candidate (result: persist DOWN
  + new birth), the m=8 "remains empty" candidate (result: first
  re-emergence), and note that the re-emergence also falsifies the
  persisted "no re-emergence ever" reading carried in the published
  z19 probe README/log. The (9,10)-reabsorb-at-+3 prediction
  CONFIRMED; the m=11/m=12/m=13 shape predictions (110/92/76+75),
  the base-spot 0 and the twelfth-identity form CONFIRMED as
  predeclared.
- All seven records reuse EXACT published enumeration forms, so shape
  counts are forced and machine-checked (170/234/362/110/92/76/75).
- Environment incident, pre-push: the FIRST cross-check attempt (a
  combined in-process verifier holding the ordered-engine cache across
  records) was OOM-killed (rc 137) in this sandbox — resolved by
  per-record invocation with per-S `cache_clear()` (the census kit's
  lesson applied); the frozen `.out` was never touched, and the full
  cross-check was then re-executed cleanly from scratch after the
  session's environment reset (all MATCH, section 2 above). The sandbox
  memory ceiling is a real constraint of the check environment, not of
  the frozen artifact.
- The environments for the five determinism runs and the frozen output
  were re-populated after a sandbox reset within the same session; all
  kit bytes were sha-verified against the frozen pins
  (`17974ab0…`/`281311e8…`/`582c93c1…`) before the re-executed runs,
  and the five fresh runs reproduced the frozen sha byte-identically.
- The m=8 re-emergence strengthens the case for keeping ALL beyond-row
  enumerations identical slice-over-slice: a "cleaner" probe that
  dropped the m=8 row after two empty slices would have missed the
  event entirely. Recorded as a lane practice rule (observation, one
  event).

## 5. Handoff

- The T-Z19 declaration lane is NOT affected: this probe touches only
  z=20 data beyond the published z=19 slice; the z=19 census kit
  (`strip-z19-min14-20261125`, same session) carries the T-Z19
  declaration dossier (13-rung ladder, base child A719f14 collapse,
  strip 230/0, residual-band band + base dossier, tenth/eleventh
  identity supply).
- Natural next measurements after this probe, in information-value
  order:
  1. the m=11 z=21 FRONTIER record (z*(11)=21, odd-m → (11,12) by the
     frontier parity rule candidate 1/1) — the last small odd-m
     frontier before the m=12 z=22 frontier; belongs to the z=21
     slice's kit (also the first beyond slices for the m=12/m=13
     rows' next moves and the re-emergent m=8 arc's z=21 fate);
  2. the z=20 census kit (floor-15): the F-cell even-z single-point
     question at s=20 against the eleventh-tail identity datum
     (0v2@20 + 2v1@21+); the m=11-row z=20 record is already
     published HERE (band closed 4/4);
  3. the m=10 z=21 record (+3: does (10,10) reabsorb at +3 like
     (8,8), and does the (10,12) birth decay like (9,12)?) and the
     m=9/m=8 z=21 records (the (9,12) arc's third slice; the
     re-emergence's next move).
  The declaration lane should recompute all z*(m) values from the
  published K1268 statement rather than trusting this log's inline
  arithmetic.
- The z-parity device candidates after this probe: base-spot
  alternation (5/5), odd-z supply identity form (3/3), odd-z F-cell
  hole+tail typology (3/3 with the z=19 census), even-z newest
  identity form (2/2). Each stays a candidate series until the
  corresponding census/declaration absorbs them.

## 6. Standard caveats

Finite machine observation only. No theorem, no universal claim, no
verdict consumed. Standard 11×11 empty board, two-stone roots, S2,
classes 1/2/4 and all central-reply roots: all UNKNOWN, unchanged.
Battery/spot counts are engine cross-checks, not proof substitutes.
