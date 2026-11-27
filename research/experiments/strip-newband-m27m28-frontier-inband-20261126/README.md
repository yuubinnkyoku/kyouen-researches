# newband m27/m28 frontier + m25/m26 mini-ladder + m23..m26 windows pre-declaration exploration kit (frozen)

This directory is the publish-then-execute PRIMARY RECORD for the
pre-declaration census of the LADDER CONTINUATION rows of the
m=19..m=24 residual bands (the registered kit-5 S5 items m=19@z=52 /
z=53, m=20@z=53 / z=54, m=21@z=48 / z=49, m=22@z=49 / z=50,
m=23@z=50 / z=51, m=24@z=51 / z=52), the m=25 / m=26 MINI-LADDER
rows (the registered kit-5 S5 items (13)-(18), including the FIRST
m=25 / m=26 death datum candidates), the FIRST-EVER m=27 / m=28 rows
(the registered 15th / 16th parity datum candidates), the REGISTERED
in-band window sweeps m=25 z in {41..48} and m=26 z in {43..50}
(with the listed z=50 row executed as a disclosed blind
re-verification of the published kit-5 frontier 14th datum), plus 112
published anchor rechecks (the 93 kit-5-era anchors verbatim + the 19
kit-5 separation spots, first re-anchored here and machine-verified
19/19 before the first run). No K slot is claimed and no claim is
made here: everything below is machine observation.

## Files

- `engine_block.py` — byte-clone of the published chain engine (sha256
  `582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0`,
  byte-identical to the kit-4/kit-5 chain); embedded ENGINE_BLOCK
  startup pin `bd5f22e4…` asserted (engine_gate PASS in the frozen
  output).
- `explore_m27m28_frontier.py` — frozen pre-declaration explorer, sha256
  `2c7ac4a9a57c7f112808754cf68d3fee652b6775301dc946c40ca0496d1ca8d9`
  (48,354 bytes; structure assembled from the published kit-5 explorer
  by replacing the docstring, the anchor table, the battery literal
  list, the row section and the future section; ENGINE_BLOCK and the
  row-record helpers are byte-published-chain). Full registration
  provenance, the window label/list disclosure, the strip-coverage
  disclosure and the counter-probe record frozen in the docstring
  BEFORE the published run.
- `explore_m27m28_frontier.out` — the frozen stdout, sha256
  `4eda4e1e68bcb8b9645d775be2554504072b97438650efaf81be8b4919f0648e`
  (74,197 bytes). Deterministic — the published run plus FIVE
  verification runs are all byte-identical (default ×2 +
  PYTHONHASHSEED=random + env -i isolated ×2), rc 0, ~23 s per run,
  plus a push-time rerun.

## Registered targets taken by this kit (before the fact)

1. kit-5 log S5 items (1)-(12) (commit `d52f2be7`): the twelve ladder
   continuation rows m=19@z=52 / z=53, m=20@z=53 / z=54, m=21@z=48 /
   z=49, m=22@z=49 / z=50, m=23@z=50 / z=51, m=24@z=51 / z=52, verbatim
   binding candidates.
2. kit-5 log S5 items (13)-(18): the m=25 / m=26 mini-ladder rows
   m=25@z=50 / z=51 / z=52 and m=26@z=51 / z=52 / z=53, verbatim
   (including the FIRST m=25 / m=26 death datum candidates).
3. kit-5 log S5 items (21)/(22): the frontier datum candidates
   m=27@z=53 and m=28@z=54 (z* arithmetic re-derived and
   double-asserted at this build: z*(27)=53, z*(28)=54 per K1268).
4. kit-5 log S5 items (19)/(20): the in-band window sweeps m=25 z in
   {41..48} and m=26 z in {43..50}. DISCLOSED label/list resolution:
   item (20)'s prediction text reads "z*(26)-8..-1" (=42..49) while its
   row list reads 43..50; per the kit-4 label/list precedent the
   LISTED rows bind, so z in {43..49} were measured as plain window
   rows (candidates 0 separations) and the listed z=50 row — the
   ALREADY-PUBLISHED kit-5 frontier 14th datum — was executed as an
   explicit BLIND RE-VERIFICATION carrying the published candidate
   verbatim. The z=42 row of the label reading is NOT registered and
   NOT measured here (carried to the kit-7 proposals).

## Headline results (all finite observations, no universal claim)

1. **ALL 36 ROWS FULL HIT, zero surprises.** The twelve ladder rows:
   m=19@z=52 EXACTLY ONE {19,34}@S=53 UP 1v0 with {19,32}
   conform-DEAD (the first m=19 d=6 death datum); m=19@z=53 EXACTLY
   TWO (stick {19,34} DOWN 1v2 + NEW birth {19,36}@S=55 UP 2v0,
   d=8 seat gap 17) — the m=19 ladder is now measured COMPLETE
   through the d=8 birth (9 birth seats, d=0..8); m=20@z=53 EXACTLY
   ONE (20,34)@S=54 DOWN 0v1 with (20,32) conform-DEAD (first m=20
   d=6 death); m=20@z=54 EXACTLY TWO (stick + birth (20,36)@S=56 UP
   2v1, d=8 gap 16) — the m=20 ladder COMPLETE through d=8;
   m=21@z=48 EXACTLY ONE {21,28}@S=49 UP 1v0 with {21,26}
   conform-DEAD (first m=21 d=2 death); m=21@z=49 EXACTLY TWO (stick
   1v2 + {21,30}@S=51 UP 2v0, d=4 gap 9); m=22@z=49 EXACTLY ONE
   (22,28)@S=50 DOWN 0v1 with (22,26) conform-DEAD (first m=22 d=2
   death); m=22@z=50 EXACTLY TWO (stick 0v2 + (22,30)@S=52 UP 2v1,
   d=4 gap 8); m=23@z=50 EXACTLY ONE {23,28}@S=51 UP 1v0 with
   {23,26} conform-DEAD (first m=23 d=1 death); m=23@z=51 EXACTLY
   TWO (stick 1v2 + {23,30}@S=53 UP 2v0, d=2 gap 7); m=24@z=51
   EXACTLY ONE (24,28)@S=52 DOWN 0v1 with (24,26) conform-DEAD
   (first m=24 d=1 death); m=24@z=52 EXACTLY TWO (stick (24,28) DOWN
   0v2 + birth (24,30)@S=54 UP 2v1, d=3 gap 6).
2. **THE FIRST m=25 AND m=26 DEATHS WITNESSED** (registered candidates,
   both hit): m=25@z=52 EXACTLY ONE {25,28}@S=53 UP 1v0 with {25,26}
   conform-DEAD at z=52=S+1 (the FIRST m=25 death datum, d=0, the
   complete birth-stick-death cycle of the frontier-adjacent band);
   m=26@z=53 EXACTLY ONE (26,28)@S=54 DOWN 0v1 with (26,26)
   conform-DEAD at z=53=S+1 (the FIRST m=26 death datum, d=0). The
   m=25@z=50 / z=51 and m=26@z=51 / z=52 rows also hit verbatim
   (one-past UP 1v0 / DOWN 0v1; birth d=1 with the d=0 stick seat
   coinciding S(d0)=z, both parity-exact).
3. **FRONTIER PARITY LAW 16/16 through m=28** (was 14/14): 15th datum
   m=27@z=53 EXACTLY ONE {27,28}@S=55 UP 2v0 (collapse v(55,53,81)=0);
   16th datum m=28@z=54 EXACTLY ONE (28,28)@S=56 UP 2v1 (collapse
   v(56,54,83)=1) — the first-ever m=27 / m=28 rows, both value-exact.
   The 17th / 18th datum candidates (m=29@z=57, m=30@z=58) are
   REGISTERED below for the next execution.
4. **IN-BAND WINDOW SWEEPS 15/15 CLEAN + 1/1 BLIND RE-VERIFICATION**:
   m=25 z in {41..48} (8 rows, 15 shapes each, R=67..74, the z=48 row
   the frontier-minus-one precedent candidate) and m=26 z in {43..49}
   (7 rows, 14 shapes each, R=70..76), all 0 separations; the listed
   m=26 z=50 row reproduced the published frontier 14th datum
   EXACTLY (EXACTLY ONE (26,26)@S=52 UP 2v1). Measured in-band
   coverage is now m=25 z in {41..52} contiguous plus z in {25,26}
   strip-derived, and m=26 z in {43..53} plus strip.
5. Cumulative class counts (observation counts, published + this kit):
   one-past decays odd 2->1 now 31 observations (26 + m19@z52,
   m21@z48, m23@z50, m25@z50, m25@z52), even 2->0 now 30 (25 +
   m20@z53, m22@z49, m24@z51, m26@z51, m26@z53); sticks +4 odd +4
   even; deaths +8 here (m19 d=6, m20 d=6, m21 d=2, m22 d=2, m23 d=1,
   m24 d=1, m25 d=0, m26 d=0) — the death class is now witnessed for
   m=19/m=20 d in {0..6}, m=21/m=22 d in {0..2}, m=23/m=24 d in
   {0..1}, m=25/m=26 d=0 of the frontier-adjacent seats.
6. Shapes (measured counts per row): m=19 22, m=20 20, m=21 19,
   m=22 18, m=23 17, m=24 16, m=25 15, m=26 14, m=27 13, m=28 12
   (the quadratic shape-count guess stays refuted and is not used).
7. **Verification battery**: 112/112 published anchors reproduce
   exactly (the 19 new kit-5 separation spots machine-verified 19/19
   against the published values BEFORE the first run, R-first
   convention asserted for every entry: 112/112 immune to the kit-5
   S/R splice class); K0832 closed-form vs canonical vs ordered
   398/398 (all candOR and registration literals incl. the 44 kit-7
   future triples); candidate-vs-measured hit check 36/36;
   ordered-engine independent audit (outside the frozen artifact):
   36/36 rows separation-value-exact over 568 shapes, anchors 112/112;
   determinism 6/6 byte-identical plus push-time rerun; engine-free
   derive check: 77 collapse literals re-derived from the closed form,
   z* arithmetic (z*(25)..z*(30)), seat arithmetic S=sum(X), R=m+z+1,
   and UP/DOWN value-vs-collapse direction consistency for every
   parseable candidate claim.

## Honest record

- ALL ERRORS CAUGHT BEFORE THE FREEZE (build-time, disclosed): the
  engine-free derive check (derive_check_kit6) rejected the first
  draft's kit-7 registration constants for the m=25 / m=26
  post-mini-ladder rows — four collapse literals mis-derived from a
  seat-lifecycle offset slip (the d+1 seat's birth occupies the d
  seat's stick slice, shifting every later row by one slice). The
  corrected machine derivations are the published ones; no candidate
  text of the MEASURED rows was affected (all 36 measured candidates
  derive-checked PASS on the first attempt), and no published
  artifact was touched.
- Window label/list disclosure frozen in the docstring and executed as
  declared (see Registered targets 4); the listed z=50 blind
  re-verification HIT the published value exactly — which also
  re-proves the kit-5 frontier row inside the kit-6 frozen run.
- Counter-probe: at build (~09:37Z, head `d52f2be7`, this kit's own
  predecessor; unchanged) all 8 kit-specific content queries
  (frontier_m27, m27_z53, m28_z54, ladder_m19_z52, ladder_m25_z50,
  inband_m25_z41, inband_m26_z43, m27m28) returned 0 records; re-run
  at push time against then-current main and disclosed in the log.
- The kit-7 future-slice registrations of the frozen section (d) are
  pre-computations for the next execution, not measurements; the
  below-window rows (m=25 z in {27..40}, m=26 z in {27..42}, and the
  NOT strip-covered m=27 z in {25..44}, m=28 z in {25..45}) are NOT
  registered except the four window extension proposals.
- All constants are K0832 closed-form paper derivations,
  machine-derived and double-asserted at this build; no engine
  recursion before the frozen published run (the 19 anchor
  re-verifications are re-checks of already-published values, kit-5
  precedent).

## Standard caveats

Finite machine observations against the pinned raw engine only; no
theorem, no universal claim (the 31/30 decay-class counts are
observation counts over published + this kit's data); the 11x11
standard board, two-stone roots, S2, class 1/2/4 and all
central-reply roots remain UNKNOWN, unchanged; no verdict consumed.
Section (d) is a pure closed-form pre-computation with no engine
recursion. No K slot claimed; the future T-Z19..T-Z22 declaration
lanes own their band conventions.
