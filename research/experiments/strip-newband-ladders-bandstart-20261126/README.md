# newband-ladders-bandstart pre-declaration exploration kit (frozen)

This directory is the publish-then-execute PRIMARY RECORD for the
pre-declaration census of the LADDER CONTINUATION of the NEW m=19 /
m=20 residual bands (the registered one-past + d=2-birth rows
m=19@z=40 / z=41 and m=20@z=41 / z=42, plus the kit-added
second one-past + d=3-birth rows m=19@z=42 / z=43 and m=20@z=43 /
z=44 — carrying the FIRST m=19/m=20 DEATH datums of the series) and
the BAND-START window rows (the first-ever x0-style row records at
the below-window slices with no published engine value: m=19 z in
{25..28}, m=20 z in {27..29}), plus 40 published anchor rechecks.
No K slot is claimed and no claim is made here: everything below is
machine observation. The declaration lane (a later run) picks up the
slot claims if any.

## Files

- `engine_block.py` — byte-clone of the published chain engine (sha256
  `582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0`);
  the embedded ENGINE_BLOCK startup pin `bd5f22e4…` is asserted by the
  machinery (engine_gate PASS in the frozen output).
- `explore_newband_ladders.py` — frozen pre-declaration explorer, sha256
  `621073f017a2f14076b87e2979180b4013bc383c88767352baa85e60b506bb46`
  (32,785 bytes, 590 lines; structure adapted from the published kit-1
  `explore_inband_m19m20.py` `3f4eeb22…` by replacing the docstring and
  the main() body with the disclosed new scope; the ENGINE_BLOCK, parts,
  row_record and row_record_x0 helpers are byte-preserved). The full
  registration provenance, counter-probe, overlap census and honest
  disclosure are in the file docstring, frozen BEFORE the first run.
- `explore_newband_ladders.out` — the frozen stdout, sha256
  `6c85f8c2b8649b558f4833dca2bdfd4b901c3c17c2d5cec5a79e6396a39ed3c4`
  (29,937 bytes). Deterministic — SIX runs all byte-identical (first
  frozen run + default ×2 + PYTHONHASHSEED=random same-cwd + env -i
  isolated directories ×2), rc 0, ~7.5 s per run, no randomness, no
  wall-clock, no hash-order dependence.

## Registered targets taken by this kit (before the fact)

1. The four rows m=19@z=40 / z=41, m=20@z=41 / z=42: the published kit-1
   log section 5 items (1)-(4) (commit `6057ed51`) and its frozen
   section (g) future-slice constants, verbatim binding candidates.
2. The band-start pinning (kit-1 log S5 item (5)) — taken here
   AMENDED by the build-time overlap census: the x0-style rows at
   m=19 z in {21..24} and m=20 z in {21..26} are contained
   position-by-position in the published co-token strip sweeps of the
   z21-min16 / z22 / z23-floor17 / z24-floor18 / z25-min20 /
   z26-floor20 census kits (base token m, R=m+z+1, S in {m..m+39},
   arity <= 4 TOTAL, all published 0 violations), hence
   derivable-clean and NOT re-swept (duplicate avoidance). The
   genuinely-unmeasured window slices measured here: m=19 z in
   {25,26,27,28}, m=20 z in {27,28,29}.
3. The four rows m=19@z=42 / z=43, m=20@z=43 / z=44: kit-added
   scaffold-derived binding candidates registered in the frozen
   docstring before the first run and measured in the same run (the
   kit-1 one-past/two-past precedent).

## Headline results (all finite observations, no universal claim)

1. **ALL EIGHT LADDER ROWS FULL HIT, zero surprises.** Registered:
   m=19@z=40 EXACTLY ONE {19,22}@S=41 UP 1v0 (value 1 vs collapse
   v(41,40,60)=0), {19,20} conform-DEAD at birth+3; m=19@z=41
   EXACTLY TWO: stick {19,22} DOWN 1v2 (vs v(41,41,61)=2 — the
   z==x collapse jump) + NEW birth {19,24}@S=43 UP 2v0 (gap 5);
   m=20@z=41 EXACTLY ONE (20,22)@S=42 DOWN 0v1; m=20@z=42 EXACTLY
   TWO: stick (20,22) DOWN 0v2 + NEW birth (20,24)@S=44 UP 2v1
   (gap 4). Kit-added: m=19@z=42 EXACTLY ONE {19,24}@S=43 UP 1v0
   (odd decay 2->1 of the d=2 birth); m=19@z=43 EXACTLY TWO: stick
   {19,24} DOWN 1v2 + NEW birth {19,26}@S=45 UP 2v0 (gap 7);
   m=20@z=43 EXACTLY ONE (20,24)@S=44 DOWN 0v1; m=20@z=44 EXACTLY
   TWO: stick (20,24) DOWN 0v2 + NEW birth (20,26)@S=46 UP 2v1
   (gap 6). Every measured value equals the pre-declared candidate.
2. **The FIRST m=19/m=20 DEATH datums (4)**: the death-at-birth+3
   class (the shape's value EQUALS the collapse from the birth+3
   slice on, witnessed by absence from the separation list with the
   collapse equal to the stuck parity value): m=19 d=0 shape
   {19,20} at z=40 (collapse v(39,40,60)=1), m=19 d=1 {19,22} at
   z=42 (v(41,42,62)=1), m=20 d=0 (20,20) at z=41 (v(40,41,62)=0),
   m=20 d=1 (20,22) at z=43 (v(42,43,64)=0). The new bands' death
   class is now observed for d in {0,1} of each parity.
3. **Life-cycle scaffold status (m=19 odd / m=20 even), candidates:
   each 4/4 through d=3** — birth seats (m, m+2d+1) / (m, m+2d) at
   slices z*(m)+2d born UP 2v0 / 2v1 (d=0..3: frontier + z=39/40 +
   z=41/42 + z=43/44), one-past decays 2->1 (odd) / 2->0 (even),
   birth+2 sticks (value stays, collapse jumps to 2), birth+3
   deaths. Cumulative one-past decay class counts: odd 2->1 now 17
   observations (15 published incl. kit-1 + 2 here: m=19@z=40,
   z=42), even 2->0 now 16 (14 published + 2 here: m=20@z=41,
   z=43); stick class gains 2 odd (m=19@z=41, z=43) + 2 even
   (m=20@z=42, z=44). Frontier parity law unchanged at 8/8 (m=13..20;
   the m=21/m=22 datum candidates are REGISTERED below for the next
   execution, not measured here).
4. **ALL SEVEN BAND-START WINDOW ROWS CLEAN (0 separations):**
   m=19@z in {25,26,27,28} (22 shapes each) and m=20@z in
   {27,28,29} (20 shapes each). The measured m=19 in-band window is
   now z in {25..36} = z*(19)-12..z*(19)-1 (12 slices: 4 here + 8
   kit-1), m=20 z in {27..37} = z*(20)-11..z*(20)-1 (11 slices).
   With the strip-derived clean slices (m=19 z in {21..24}, m=20 z
   in {21..26}) the candidate clean window extends to z=21 for both
   new bands — the band-start conventions belong to the future
   T-Z19/T-Z20 declaration lanes. The 2 published in-row base spots
   reproduce exactly: H(45;(19,19);25)=0, H(46;(19,19);26)=0.
5. **Verification battery**: 40/40 published anchors reproduced
   exactly (the 30 kit-1 anchors + the 8 kit-1 new-band separation
   spots of `6057ed51` + the 2 base spots); K0832 closed-form vs
   canonical vs ordered engine 156/156; determinism 6/6 runs
   byte-identical; ordered-engine independent audit (outside the
   frozen artifact): all 15 rows re-enumerated and re-evaluated with
   H_ordered — 316 shapes, separation lists value-exact 15/15 rows,
   anchors 40/40.

## Honest record

- Every collapse constant was computed on paper (engine-free, the
  PROVED K0832 closed form), drafted twice, before the freeze; the
  anchor values are verbatim citations of published logs read before
  the freeze. No engine recursion on any section (b)-(d) position was
  evaluated before the frozen first run; the only pre-published values
  are the 40 anchor spots.
- Timestamp erratum (disclosed here, the frozen file is NOT edited):
  the docstring counter-probe note reads 09:02Z; the probe executions
  actually ran at ~08:57-08:59Z (before the file assembly), with HEAD
  `6057ed51` confirmed unchanged both then and at push time. The
  probes were re-run at push time against the then-current main.
- The m19@z42 / z43 and m20@z43 / z44 rows are same-kit
  registrations (the kit-1 one-past/two-past precedent), disclosed as
  such in the docstring and in the kit log.
- No file was edited after any run; the frozen stdout is the
  published artifact.

## Standard caveats

Everything here is a FINITE machine observation against the pinned
raw engine. Nothing here is a theorem, nothing universal is claimed,
and no verdict of any game position (11x11 standard board,
two-stone roots, S2, class 1/2/4 — all UNKNOWN) is consumed. The
strip-derivation of the covered window slices is a set-containment
argument over published artifacts, not a new measurement. Section
(d) is a pure closed-form pre-computation using no engine recursion.
