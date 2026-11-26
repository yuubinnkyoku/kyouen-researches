# newband m23/m24 frontier + below-window pre-declaration exploration kit (frozen)

This directory is the publish-then-execute PRIMARY RECORD for the
pre-declaration census of the LADDER CONTINUATION rows of the new
m=19..m=22 residual bands (the registered kit-3 S5 items m=19@z=48 /
z=49, m=20@z=49 / z=50, m=21@z=44 / z=45, m=22@z=45 / z=46), the
FIRST-EVER m=23 / m=24 rows (the frontier datum candidates, TAKEN
TOGETHER WITH THE DISCLOSED z*(23) REGISTRATION ERRATUM of kit-3 S5
item (9): the registered "z*(23)=2*23-2+1=44" is an arithmetic slip —
the K1268 formula z*(m)=2m-2+(m mod 2) gives z*(23)=45 EXACTLY; the
misregistered row m=23@z=44 was measured as registered with the
corrected expectation stated before the freeze, and the CORRECTED
frontier m=23@z=45 was registered kit-added in the same run), the
kit-added one-past / birth mini-ladder rows of m=23 / m=24, and the
REGISTERED below-window band-start rows m=21 z in {27..32} and
m=22 z in {27..33}, plus 72 published anchor rechecks. No K slot is
claimed and no claim is made here: everything below is machine
observation.

## Files

- `engine_block.py` — byte-clone of the published chain engine (sha256
  `582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0`);
  embedded ENGINE_BLOCK startup pin `bd5f22e4…` asserted (engine_gate
  PASS in the frozen output).
- `explore_m23m24_frontier.py` — frozen pre-declaration explorer, sha256
  `759233d1f07aa9ab6a6f92dc1d6a76d48ef7a3202d6f1d4181db3521bce40124`
  (41,365 bytes; structure adapted from the published kit-3 explorer
  by replacing the docstring and the main() body with the disclosed
  new scope; ENGINE_BLOCK and the row-record helpers are
  byte-published-chain). Full registration provenance, erratum
  disclosure, counter-probe, overlap/coverage census and honest
  disclosure frozen in the docstring BEFORE the first run.
- `explore_m23m24_frontier.out` — the frozen stdout, sha256
  `4d433267b88791e322c34861b4e981f372be2a07af5ec45f7c1e483160f2dda3`
  (51,406 bytes). Deterministic — SEVEN runs all byte-identical
  (frozen first run + default ×2 + PYTHONHASHSEED=random + env -i
  isolated directories ×2 + push-time rerun), rc 0, ~15 s per run.

## Registered targets taken by this kit (before the fact)

1. kit-3 log S5 items (1)-(8) (commit `6554de44`): the rows
   m=19@z=48 / z=49, m=20@z=49 / z=50, m=21@z=44 / z=45 and
   m=22@z=45 / z=46, verbatim binding candidates.
2. kit-3 log S5 item (9): the frontier datum candidates — the
   misregistered m=23@z=44 (discharged here with the corrected
   expectation, see below) and m=24@z=46 (arithmetic verified at this
   build: z*(24)=2*24-2+0=46).
3. Kit-added same-run registrations (the kit-1 precedent, disclosed):
   the CORRECTED frontier m=23@z=45 (the erratum discharge), and the
   m=23@z=46 / z=47 and m=24@z=47 / z=48 / z=49 mini-ladder rows.
   The m=24@z=49 row candidate was CORRECTED BY THE BUILD CHECK
   before the freeze (disclosed in the docstring): at z=49=S+1 the
   d=0 seat is on its death slice (conform), so the candidate is
   EXACTLY ONE (24,26)@S=50 DOWN 0v1.
4. kit-3 log S5 item (10): the below-window band-start rows
   m=21 z in {27..32} and m=22 z in {27..33} (candidates
   0 separations). The strip-coverage caveat was re-probed at this
   build (docstring): no z=27..33 census kit exists; every published
   z=27..33 engine value belongs to m<=22 rows with a part < 21
   except kit-3's own m=21/m=22 rows themselves — disjoint slices.

## Headline results (all finite observations, no universal claim)

1. **ALL 29 ROWS FULL HIT, zero surprises.** The eight registered
   ladder rows: m=19@z=48 EXACTLY ONE {19,30}@S=49 UP 1v0 with
   {19,28} conform-DEAD (the first m=19 d=4 death datum); m=19@z=49
   EXACTLY TWO (stick {19,30} DOWN 1v2 + NEW birth {19,32}@S=51 UP
   2v0, d=6 seat gap 13); m=20@z=49 EXACTLY ONE (20,30)@S=50 DOWN
   0v1 with (20,28) conform-DEAD (first m=20 d=4 death); m=20@z=50
   EXACTLY TWO (stick + birth (20,32)@S=52 UP 2v1, d=6 gap 12);
   m=21@z=44 EXACTLY ONE {21,24}@S=45 UP 1v0 with {21,22}
   conform-DEAD (the FIRST m=21 death datum); m=21@z=45 EXACTLY TWO
   (stick 1v2 + {21,26}@S=47 UP 2v0, d=2 gap 5); m=22@z=45 EXACTLY
   ONE (22,24)@S=46 DOWN 0v1 with (22,22) conform-DEAD (the FIRST
   m=22 death); m=22@z=46 EXACTLY TWO (stick 0v2 + (22,26)@S=48 UP
   2v1, d=2 gap 4). The m=19 / m=20 ladders are now measured
   COMPLETE through the d=6 birth (7 birth seats each, d=0..6).
2. **z*(23) ERRATUM DISCHARGED (resolved as predicted).** The
   misregistered m=23@z=44 row measured EXACTLY ZERO separations —
   the corrected expectation (frontier-minus-one precedent) held, so
   the m=13..23 frontier-minus-one rows are now all published clean;
   the registered EXACTLY ONE prediction written at kit-3 for z=44
   is voided by the slip and was not re-asserted (docstring-first
   disclosure, before the freeze). The CORRECTED frontier m=23@z=45
   hit EXACTLY ONE {23,24}@S=47 UP 2v0 (collapse v(47,45,69)=0).
3. **FRONTIER PARITY LAW 12/12 through m=24** (was 10/10): 11th
   datum m=23@z=45 EXACTLY ONE {23,24}@S=47 UP 2v0; 12th datum
   m=24@z=46 EXACTLY ONE (24,24)@S=48 UP 2v1 (collapse
   v(48,46,71)=1) — the first-ever m=23 / m=24 rows, both
   value-exact. The 13th / 14th datum candidates (m=25@z=49,
   m=26@z=50) are REGISTERED below for the next execution.
4. **m=23 / m=24 mini-ladders hit** (kit-added, same-run): one-past
   decays m=23@z=46 UP 1v0 (odd 2->1) and m=24@z=47 DOWN 0v1 (even
   2->0); birth slices m=23@z=47 EXACTLY TWO (stick {23,24} DOWN
   1v2 + {23,26}@S=49 UP 2v0, gap 3) and m=24@z=48 EXACTLY TWO
   (stick (24,24) DOWN 0v2 + (24,26)@S=50 UP 2v1, gap 2); and
   m=24@z=49 EXACTLY ONE (24,26)@S=50 DOWN 0v1 with (24,24)
   conform-DEAD at z=49=S+1 (the FIRST m=24 death datum, d=0).
   Cumulative one-past decay class counts: odd 2->1 now 23
   observations (20 + m=19@z=48, m=21@z=44, m=23@z=46 here), even
   2->0 now 23 (19 + m=20@z=49, m=22@z=45, m=24@z=47, z=49 here).
   Death class now witnessed for m=19/m=20 d in {0..4} plus d=0 of
   m=21, m=22, m=24 (m=23 d=0 death is REGISTERED below).
5. **BELOW-WINDOW BAND-START 13/13 CLEAN**: m=21 z in {27..32}
   (19 shapes each, R=49..54) and m=22 z in {27..33} (18 shapes each,
   R=50..56), all 0 separations. Measured in-band coverage is now
   m=21 z in {25..40} (z=25/26 strip-derived) and m=22 z in {25..41}.
6. Shapes: m=23 rows carry 17 shapes, m=24 rows 16 (measured counts;
   the quadratic shape-count guess stays refuted and is not used).
7. **Verification battery**: 72/72 published anchors (52 kit-3 +
   20 separation spots of `6554de44`); K0832 closed-form vs
   canonical vs ordered 297/297; determinism 7/7 byte-identical;
   ordered-engine independent audit (outside the frozen artifact):
   29/29 rows separation-value-exact over 530 shapes, anchors 72/72.

## Honest record

- Paper arithmetic disclosure as in the docstring (all constants
  K0832 closed-form, derived twice, no engine recursion before the
  frozen first run; anchors are verbatim published values). The
  counter-probe ran at ~09:12Z against head `6554de44` (this kit's
  own predecessor) with the content queries
  "frontier_m23", "m23_z44", "m23_z45", "m24_z46", "m19_z48",
  "m20_z49", "m21_z44", "m22_z45", "inband_m21_z27", "inband_m22_z27"
  returning NO measurement record, and was re-run at push time
  against then-current main (head `0f2440c8`: the target paths are
  absent, the only commits after kit-3 belong to the n11 lane).
- FROZEN-FILE TYPOS (disclosed; frozen files NOT edited, the kit-2
  timestamp-erratum precedent): (i) the docstring's first paragraph
  reads "the registered 11th / 10th parity datum candidates" — the
  intent, per kit-3 S5 item (9) itself, is the 11th (m=23) and 12th
  (m=24) datum candidates; no constant is affected (all constants
  battery-checked 297/297). (ii) the frozen future-slice section's
  m=23 window proposal is labelled "z*(23)-8..-1" but lists the rows
  z in {36..43} — the LISTED rows {36..43} are the binding proposal
  (z=44 was measured clean by this kit's erratum row, z=45/46/47 by
  its frontier/mini-ladder rows, so {36..43} are exactly the free
  slices).
- The 7 kit-added rows are same-kit registrations (kit-1 precedent),
  disclosed in the docstring and in the kit log; the m=24@z=49
  candidate correction by the build check was disclosed BEFORE the
  freeze in the docstring.
- No file was edited after any run; the frozen stdout is the
  published artifact.

## Standard caveats

Finite machine observations against the pinned raw engine only; no
theorem, no universal claim (the 23/23 decay-class counts are
observation counts over published + this kit's data); the 11x11
standard board, two-stone roots, S2, class 1/2/4 and all
central-reply roots remain UNKNOWN, unchanged; no verdict consumed.
Section (f) is a pure closed-form pre-computation with no engine
recursion. No K slot claimed; the future T-Z19..T-Z22 declaration
lanes own their band conventions.
