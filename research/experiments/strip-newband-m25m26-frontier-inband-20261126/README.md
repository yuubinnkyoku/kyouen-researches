# newband m25/m26 frontier + m23/m24 in-band pre-declaration exploration kit (frozen)

This directory is the publish-then-execute PRIMARY RECORD for the
pre-declaration census of the LADDER CONTINUATION rows of the new
m=19..m=24 residual bands (the registered kit-4 S5 items m=19@z=50 /
z=51, m=20@z=51 / z=52, m=21@z=46 / z=47, m=22@z=47 / z=48,
m=23@z=48 / z=49, m=24@z=50), the FIRST-EVER m=25 / m=26 rows (the
registered 13th / 14th parity datum candidates), and the REGISTERED
in-band window sweeps m=23 z in {36..43} and m=24 z in {38..45},
plus 93 published anchor rechecks (the 72 kit-era anchors verbatim +
the 21 kit-4 separation spots, first re-anchored here). No K slot is
claimed and no claim is made here: everything below is machine
observation.

## Files

- `engine_block.py` — byte-clone of the published chain engine (sha256
  `582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0`,
  byte-identical to the kit-4 publication); embedded ENGINE_BLOCK
  startup pin `bd5f22e4…` asserted (engine_gate PASS in the frozen
  output).
- `explore_m25m26_frontier.py` — frozen pre-declaration explorer, sha256
  `08974974ded39b8c8d7447d792813086a34acff9c54f041a20c461baed804aa8`
  (39,954 bytes; structure adapted from the published kit-4 explorer
  by replacing the docstring and the main() body with the disclosed
  new scope; ENGINE_BLOCK and the row-record helpers are
  byte-published-chain). Full registration provenance, the TWO dated
  erratum/build-fix disclosures, counter-probe, overlap/coverage
  census and honest disclosure frozen in the docstring BEFORE the
  published run.
- `explore_m25m26_frontier.out` — the frozen stdout, sha256
  `9d32f5fcd5cfb1209868e2e3773704d47b59e45a92829e047f807b7e769fd9fb`
  (59,488 bytes). Deterministic — the published run plus FIVE
  verification runs are all byte-identical (default ×2 +
  PYTHONHASHSEED=random + env -i isolated ×2), rc 0, ~18 s per run,
  plus a push-time rerun.

## Registered targets taken by this kit (before the fact)

1. kit-4 log S5 items (1)-(11) (commit `fe0a2d01`): the eleven ladder
   continuation rows m=19@z=50 / z=51, m=20@z=51 / z=52, m=21@z=46 /
   z=47, m=22@z=47 / z=48, m=23@z=48 / z=49 and m=24@z=50, verbatim
   binding candidates (the m=22 pair quoted with the CORRECTED R
   annotations R=70/71 of the disclosed kit-4 (f) slip; values
   unchanged, both annotation triples battery-checked).
2. kit-4 log S5 item (12): the frontier datum candidates m=25@z=49
   and m=26@z=50 (z* arithmetic re-derived and double-asserted at this
   build: z*(25)=49, z*(26)=50 per K1268).
3. kit-4 log S5 item (13): the in-band window sweeps m=23 z in
   {36..43} and m=24 z in {38..45} (candidates 0 separations each).
   The strip-coverage caveat was re-probed at this build (no
   z=36..45 census kit exists on main; see Honest record).

## Headline results (all finite observations, no universal claim)

1. **ALL 29 ROWS FULL HIT, zero surprises.** The eleven ladder rows:
   m=19@z=50 EXACTLY ONE {19,32}@S=51 UP 1v0 with {19,30}
   conform-DEAD (the first m=19 d=5 death datum); m=19@z=51 EXACTLY
   TWO (stick {19,32} DOWN 1v2 + NEW birth {19,34}@S=53 UP 2v0,
   d=7 seat gap 15) — the m=19 ladder is now measured COMPLETE
   through the d=7 birth (8 birth seats, d=0..7); m=20@z=51 EXACTLY
   ONE (20,32)@S=52 DOWN 0v1 with (20,30) conform-DEAD (first m=20
   d=5 death); m=20@z=52 EXACTLY TWO (stick + birth (20,34)@S=54 UP
   2v1, d=7 gap 14) — the m=20 ladder COMPLETE through d=7;
   m=21@z=46 EXACTLY ONE {21,26}@S=47 UP 1v0 with {21,24}
   conform-DEAD (first m=21 d=1 death); m=21@z=47 EXACTLY TWO (stick
   1v2 + {21,28}@S=49 UP 2v0, d=3 gap 7); m=22@z=47 EXACTLY ONE
   (22,26)@S=48 DOWN 0v1 with (22,24) conform-DEAD (first m=22 d=1
   death, corrected R annotation); m=22@z=48 EXACTLY TWO (stick 0v2
   + (22,28)@S=50 UP 2v1, d=3 gap 6); m=23@z=48 EXACTLY ONE
   {23,26}@S=49 UP 1v0 with {23,24} conform-DEAD at z=48=S+1 — the
   FIRST m=23 death datum (d=0); m=23@z=49 EXACTLY TWO (stick 1v2 +
   {23,28}@S=51 UP 2v0, d=2 gap 5); m=24@z=50 EXACTLY TWO (stick
   (24,26)@S=50 DOWN 0v2 + birth (24,28)@S=52 UP 2v1, d=2 gap 4,
   stick seat coincides S(d1)=50=z).
2. **FRONTIER PARITY LAW 14/14 through m=26** (was 12/12): 13th datum
   m=25@z=49 EXACTLY ONE {25,26}@S=51 UP 2v0 (collapse v(51,49,75)=0);
   14th datum m=26@z=50 EXACTLY ONE (26,26)@S=52 UP 2v1 (collapse
   v(52,50,77)=1) — the first-ever m=25 / m=26 rows, both
   value-exact. The 15th / 16th datum candidates (m=27@z=53,
   m=28@z=54) are REGISTERED below for the next execution.
3. **IN-BAND WINDOW SWEEPS 16/16 CLEAN**: m=23 z in {36..43} (8 rows,
   17 shapes each, R=60..67) and m=24 z in {38..45} (8 rows, 16
   shapes each, R=63..70), all 0 separations. Measured in-band
   coverage is now m=23 z in {36..49} contiguous (window + kit-4
   z=44..47 + this kit's ladder rows) plus z in {25,26} strip-derived,
   and m=24 z in {38..50} plus strip.
4. Cumulative class counts (observation counts, published + this kit):
   one-past decays odd 2->1 now 26 observations (23 + m=19@z=50,
   m=21@z=46, m=23@z=48 here), even 2->0 now 25 (23 + m=20@z=51,
   m=22@z=47 here); sticks +3 odd (m19@z51, m21@z47, m23@z49) +3
   even (m20@z52, m22@z48, m24@z50); deaths +5 here (m=19 d=5,
   m=20 d=5, m=21 d=1, m=22 d=1, m=23 d=0) — the death class is now
   witnessed for m=19/m=20 d in {0..5} plus d in {0,1} of m=21, m=22
   and d=0 of m=23, m=24.
5. Shapes (measured counts per row, unchanged convention): m=19 rows
   22, m=20 20, m=21 19, m=22 18, m=23 17, m=24 16, m=25 15, m=26
   14 (the quadratic shape-count guess stays refuted and is not
   used).
6. **Verification battery**: 93/93 published anchors reproduce
   exactly (72 kit-era + 21 kit-4 separation spots first re-anchored
   here); K0832 closed-form vs canonical vs ordered 331/331 (both
   corrected R annotation triples of the kit-4 (f) slip kept on
   record in the battery); candidate-vs-measured hit check 29/29;
   ordered-engine independent audit (outside the frozen artifact):
   29/29 rows separation-value-exact over 501 shapes, anchors 93/93;
   determinism 6/6 byte-identical plus push-time rerun.

## Honest record

- TWO dated disclosures, both in the frozen docstring BEFORE the
  published run:
  (i) the kit-4 frozen section (f) R-ANNOTATION slip for its two
  m=22 entries (values unaffected, collapse parity-constant in both
  annotation windows; this kit quotes corrected R=70/71 and
  battery-checks BOTH triples);
  (ii) THIS BUILD's anchor-table splice fix: the 21 kit-4-sourced
  anchor entries were first assembled with the separation seat S in
  the R slot; an internal pre-publication check run (kept locally as
  `*.out.run1`, NOT a datum, NOT published) surfaced exactly 15
  false-conform mismatches, all kit-4-entry spots; the 21 first
  fields were corrected to the mechanical R=m+z+1 and pre-verified to
  reproduce all 21 published values EXACTLY (21/21). The 29
  measurement sections of the internal run and of the published run
  are byte-identical (29/29), demonstrating that no candidate,
  engine or measurement code changed. The published .out is from
  the corrected file.
- Counter-probe: at build (~09:15Z, head `fe0a2d01`, this kit's own
  predecessor) ALL kit-specific content queries returned no
  measurement record ("frontier_m25", "m25_z49", "m26_z50",
  "inband_m23", "_m23_z36"/"m24_z38", "ladder_m19_z50", "m23_z48");
  re-run at push time against then-current main (head `fe0a2d01`
  unchanged): 8/8 queries 0 hits, target paths absent, no new
  commits after kit-4.
- All constants are K0832 closed-form paper derivations,
  machine-derived and double-asserted at this build (60 constants
  including z*(25)=49, z*(26)=50, z*(27)=53, z*(28)=54); no engine
  recursion before the frozen published run.
- The 24 future-slice registrations of the frozen section (f) are
  pre-computations for the next execution, not measurements.

## Standard caveats

Finite machine observations against the pinned raw engine only; no
theorem, no universal claim (the 26/25 decay-class counts are
observation counts over published + this kit's data); the 11x11
standard board, two-stone roots, S2, class 1/2/4 and all
central-reply roots remain UNKNOWN, unchanged; no verdict consumed.
Section (f) is a pure closed-form pre-computation with no engine
recursion. No K slot claimed; the future T-Z19..T-Z22 declaration
lanes own their band conventions.
