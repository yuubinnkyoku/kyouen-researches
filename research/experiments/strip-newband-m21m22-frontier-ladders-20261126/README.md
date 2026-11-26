# newband m21/m22 frontier + ladders pre-declaration exploration kit (frozen)

This directory is the publish-then-execute PRIMARY RECORD for the
pre-declaration census of the LADDER CONTINUATION of the new m=19 /
m=20 residual bands (the registered kit-2 S5 items m=19@z=44 / z=45
and m=20@z=45 / z=46, plus the kit-added m=19@z=46 / z=47 and
m=20@z=47 / z=48) and the FIRST-EVER m=21 / m=22 rows (the registered
FRONTIER candidates m=21@z=41 / m=22@z=42 — the parity frontier law
9th / 10th datum candidates — the kit-added one-past and d=1-birth
mini-ladder rows, and the registered in-band window sweeps
m=21 z in {33..40} / m=22 z in {34..41}), plus 52 published anchor
rechecks. No K slot is claimed and no claim is made here: everything
below is machine observation.

## Files

- `engine_block.py` — byte-clone of the published chain engine (sha256
  `582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0`);
  embedded ENGINE_BLOCK startup pin `bd5f22e4…` asserted (engine_gate
  PASS in the frozen output).
- `explore_frontier_m21m22.py` — frozen pre-declaration explorer, sha256
  `311ed6a20b2f7496136a93e0bb6faf8842308598e6a3f9c1e9b39583b0c6318c`
  (37,704 bytes; structure adapted from the published kit-1
  `explore_inband_m19m20.py` by replacing the docstring and the main()
  body with the disclosed new scope; ENGINE_BLOCK and the row-record
  helpers are byte-preserved from the published chain). Full
  registration provenance, counter-probe, overlap/coverage census and
  honest disclosure frozen in the docstring BEFORE the first run.
- `explore_frontier_m21m22.out` — the frozen stdout, sha256
  `c4ef061023ead9dec65be335a82e418c88463b1767c7468921455a005aed5d63`
  (49,871 bytes). Deterministic — SIX runs all byte-identical (frozen
  first run + default ×2 + PYTHONHASHSEED=random + env -i isolated
  directories ×2), rc 0, ~16 s per run.

## Registered targets taken by this kit (before the fact)

1. kit-2 log S5 items (1)-(4) (commit `637d15e1`): the rows
   m=19@z=44 / z=45 and m=20@z=45 / z=46, verbatim binding candidates.
2. kit-2 log S5 item (5): the FIRST-EVER m=21 / m=22 rows — the
   frontier candidates m=21@z=41 ({21,22}@S=43 UP 2v0,
   v(43,41,63)=0) and m=22@z=42 ((22,22)@S=44 UP 2v1,
   v(44,42,65)=1), and the in-band windows m=21 z in {33..40} /
   m=22 z in {34..41} (candidates 0 separations). The registered
   strip-coverage caveat was re-probed at this build: the z=33..41
   census kits do not exist; every published z=33..41 engine value
   belongs to m<=20 rows / quad spots with a part < 21 — disjoint.
3. Kit-added same-run registrations (the kit-1 precedent, disclosed):
   m=19@z=46 / z=47, m=20@z=47 / z=48 (ladder), m=21@z=42 / z=43 and
   m=22@z=43 / z=44 (frontier one-past + d=1-birth mini-ladders).

## Headline results (all finite observations, no universal claim)

1. **ALL 30 ROWS FULL HIT, zero surprises.** Ladder: m=19@z=44
   EXACTLY ONE {19,26}@S=45 UP 1v0; m=19@z=45 EXACTLY TWO (stick
   {19,26} DOWN 1v2 + NEW birth {19,28}@S=47 UP 2v0, gap 9);
   m=19@z=46 EXACTLY ONE {19,28} UP 1v0; m=19@z=47 EXACTLY TWO
   (stick + birth {19,30}@S=49 UP 2v0, gap 11); m=20@z=45 EXACTLY
   ONE (20,26) DOWN 0v1; m=20@z=46 EXACTLY TWO (stick + birth
   (20,28)@S=48 UP 2v1, gap 8); m=20@z=47 EXACTLY ONE (20,28) DOWN
   0v1; m=20@z=48 EXACTLY TWO (stick + birth (20,30)@S=50 UP 2v1,
   gap 10). The m=19 / m=20 life-cycle ladders are now measured
   COMPLETE through the d=5 birth (6 birth seats each, d=0..5);
   4 more death datums witnessed (m19 d=2@z44, d=3@z46; m20 d=2@z45,
   d=3@z47).
2. **FRONTIER PARITY LAW 10/10 through m=22** (was 8/8): m=21@z=41
   EXACTLY ONE {21,22}@S=43 UP 2v0 and m=22@z=42 EXACTLY ONE
   (22,22)@S=44 UP 2v1 — both registered candidates hit value-exact;
   the m=23 (@z=44) / m=24 (@z=46) datum candidates are REGISTERED
   below for the next execution.
3. **m=21 / m=22 mini-ladders hit** (kit-added, same-run): one-past
   decays m=21@z=42 UP 1v0 (odd 2->1), m=22@z=43 DOWN 0v1 (even
   2->0); d=1 birth slices m=21@z=43 EXACTLY TWO (stick 1v2 +
   {21,24}@S=45 UP 2v0, gap 3) and m=22@z=44 EXACTLY TWO (stick 0v2
   + (22,24)@S=46 UP 2v1, gap 2). Cumulative one-past decay class
   counts: odd 2->1 now 20 observations (17 published + m19@z44,
   z46 + m21@z42 here), even 2->0 now 19 (16 published + m20@z45,
   z47 + m22@z43 here).
4. **IN-BAND WINDOWS 16/16 CLEAN**: m=21 z in {33..40} (19 shapes
   each, R=55..62) and m=22 z in {34..41} (18 shapes each, R=57..64),
   all 0 separations. NOTE (disclosed): the kit-2 S5 registration
   guessed "20 shapes" for m=21 by the m19/m20 quadratic shape
   pattern; the MEASURED count is 19 (m=21) / 18 (m=22) — the guess
   was non-binding (counts are measured, per series convention) and
   the deviation is recorded here. The m=21 / m=22 z in {25,26}
   equivalents are contained in the published z25-min20 (strips m in
   {20..25}) / z26-floor20 (m in {20..26}) sweeps — derivable-clean;
   the below-window slices m=21 z in {27..32} / m=22 z in {27..33}
   are REGISTERED for the next execution.
5. **Verification battery**: 52/52 published anchors (40 kit-2 + 12
   kit-2 ladder separation spots of `637d15e1`); K0832 closed-form vs
   canonical vs ordered 274/274; determinism 6/6 byte-identical;
   ordered-engine independent audit (outside the frozen artifact):
   30/30 rows separation-value-exact over 575 shapes, anchors 52/52.

## Honest record

- Paper arithmetic disclosure as in the docstring (all constants
  K0832 closed-form, derived twice, no engine recursion before the
  frozen first run; anchors are verbatim published values). The
  counter-probe ran at ~08:57Z against head `7fc6727e` (the n11
  sixth-cost batch publications sitting on top of this kit's
  predecessor `637d15e1`, intact in history) and was re-run at push
  time; the strip-coverage re-probe for the m=21/m=22 windows is
  described in the docstring and passed.
- The 8 kit-added rows are same-kit registrations (kit-1 precedent),
  disclosed in the docstring and in the kit log.
- No file was edited after any run; the frozen stdout is the
  published artifact.

## Standard caveats

Finite machine observations against the pinned raw engine only; no
theorem, no universal claim (the 20/19 decay-class counts are
observation counts over published + this kit's data); the 11x11
standard board, two-stone roots, S2, class 1/2/4 and all
central-reply roots remain UNKNOWN, unchanged; no verdict consumed.
Section (f) is a pure closed-form pre-computation with no engine
recursion. No K slot claimed; the future T-Z19..T-Z22 declaration
lanes own their band conventions.
