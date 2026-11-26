# newband m29/m30 frontier first contacts + m19..m26 ladder continuation + m25/m26 full-line scaffolds + in-band window sweeps pre-declaration exploration kit (frozen)

This directory is the publish-then-execute PRIMARY RECORD for the
pre-declaration census of the REGISTERED kit-6 S5 items: the ladder
continuation / birth / death rows of m=19..m=26 (items (1)-(18),
including the FIRST m=25 / m=26 death datum candidates at d=1, the
first m=19 / m=20 d=7 deaths, and the m=19 / m=20 birth slices at
d=9), the m=27 / m=28 mini-ladder rows (items (19)-(24), including
the FIRST-EVER m=27 / m=28 death datum candidates), and the frontier
first contacts m=29@z=57 / m=30@z=58 (the registered 17th / 18th
K1268 parity datum candidates, FIRST-EVER rows for those m), plus the
REGISTERED in-band window sweeps m=25 z in {33..40} and m=26 z in
{35..42} (the kit-6 items 1-4 with the disclosed z=42 label
resolution), plus the kit-6 item 31 scaffold sweeps m=25 z in {27..32}
and m=26 z in {27..34} (registered before measuring, as that item
requires), plus 141 published anchor rechecks (the 112 inherited
chain anchors verbatim + the 29 kit-6 separation spots, first
re-anchored here and machine-verified 29/29 before the first run). No
K slot is claimed and no claim is made here: everything below is
machine observation.

## Files

- `engine_block.py` — byte-clone of the published chain engine (sha256
  `582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0`,
  byte-identical to the kit-4/kit-5/kit-6 chain); embedded ENGINE_BLOCK
  startup pin `bd5f22e4…` asserted (engine_gate PASS in the frozen
  output).
- `explore_m29m30_frontier.py` — frozen pre-declaration explorer, sha256
  `b9724059783942b7d60cb25e66c3f6604d8fc674d3e92f6c30aca7f3d15e04fd`
  (53,329 bytes; structure assembled from the published kit-6 explorer
  by replacing the docstring, the anchor table, the battery literal
  list, the row section and the future section; ENGINE_BLOCK and the
  row-record helpers are byte-published-chain). Full registration
  provenance, the window label/list disclosure, the strip-coverage
  disclosure and the counter-probe record frozen in the docstring
  BEFORE the published run. DATED DISCLOSURE (2026-11-26, this
  README): the kit-6 log S2 table row "m=25@z=51" is a prose
  mis-translation of its own frozen .out registration (the registered
  pair was stick {25,26} DOWN 1v2 at S=51 + NEW {25,28}@S=53 UP 2v0;
  the prose wrote "{25,26} UP 1v2 + {25,28}@S=52 UP 2v1"); the
  registered-candidate literals used by this kit come from the kit-5 /
  kit-6 frozen .out files (the SSOT), and this kit measured both
  m=25@z=53 and m=25@z=54 and verified the SSOT reading. Kit bytes are
  not edited after the fact; this paragraph is the disclosure.
- `explore_m29m30_frontier.out` — the frozen stdout, sha256
  `5263c898efa8eb39b3a09039dee647435bf78db413b6fc573a7bd6689b94c1e6`
  (126,668 bytes). Deterministic — the published run plus FOUR
  verification runs are all byte-identical (default ×2 +
  PYTHONHASHSEED=random + env -i isolated), rc 0, ~41 s per run, plus
  a push-time rerun disclosed in the log.

## Registered targets taken by this kit (before the fact)

1. kit-6 log S5 items (1)-(12): the ladder continuation rows
   m=19@z=54 / z=55, m=20@z=55 / z=56, m=21@z=50 / z=51,
   m=22@z=51 / z=52, m=23@z=52 / z=53, m=24@z=53 / z=54, verbatim
   binding candidates (each a one-past/death row plus a birth slice
   row; the m=19 / m=20 birth d=9 slices and the m=19 / m=20 death
   of d=7 rows are the deepest ladder datums yet taken).
2. kit-6 log S5 items (13)-(18): the m=25 / m=26 ladder rows
   m=25@z=53 / z=54 / z=55 and m=26@z=54 / z=55 / z=56, verbatim
   (including the FIRST m=25 / m=26 death datum candidates at d=1).
3. kit-6 log S5 items (19)-(24): the m=27 / m=28 mini-ladder rows
   m=27@z=54 / z=55 / z=56 and m=28@z=55 / z=56 / z=57, verbatim
   (including the FIRST-EVER m=27 / m=28 death datum candidates).
4. kit-6 log S5 items 29/30 (the 17th / 18th K1268 parity datum
   candidates): the frontier first contacts m=29@z=57 and m=30@z=58
   (z* arithmetic re-derived and double-asserted at this build:
   z*(29)=57, z*(30)=58 per K1268).
5. kit-6 log S5 items 1-4 (the in-band window sweeps): m=25 z in
   {33..40} and m=26 z in {35..42}, plain window rows (registered
   candidate: 0 separations each). DISCLOSED label resolution: the
   kit-6 window label ended at z=42 while the kit-6 sweep list ended
   at z=50 — the m=26 z in {35..42} rows measured here close the
   label half of that disclosure, and the m=26 z in {43..50} measured
   by kit-6 close the other half.
6. kit-6 log S5 item 31 (the scaffold sweeps, registered BEFORE
   measuring at this build): m=25 z in {27..32} and m=26 z in
   {27..34}, plain scaffold rows (registered candidate: 0
   separations each).
7. Inherited anchor chain: 112 published anchors verbatim + the 29
   kit-6 separation spots re-anchored at this build (machine-verified
   29/29 against the published kit-6 .out BEFORE the row runs).

## Measured outcome (machine observation, no claim)

- Anchors: 141/141 exact (incl. 29/29 pre-freeze re-anchoring).
- k0832 battery literals: 737/737 all-match (the cumulative chain
  battery).
- Registered rows: 26 executed, shapes 407, separations 39.
  25/26 rows FULL HIT (measured separations exactly the registered
  candidates). ONE REGISTERED-CANDIDATE MEASUREMENT DEVIATION — the
  FIRST in the kit series: item 2, the m=19 z=55 birth slice d=9.
  The registered candidate said EXACTLY TWO (stick {19,36} DOWN 1v2
  + NEW {19,38}@S=57 UP 2v0); both named separations measured hit,
  AND an UNREGISTERED third separation measured: the stacked trio
  {19,19,19}@S=57 UP 2v0 (value 2, collapse 0) — numerically an
  exact mimic of the NEW birth seat it shares S=57 with. The trio
  row conforms (not a separation) at every m=19 slice z ≤ 54
  measured by this kit and separates only at this birth slice; the
  trio is inside the x0 sweep iff 3m ≤ m+38, i.e. m ≤ 19, so m=19 is
  the largest in-sweep m. Engine-free lemma (derivation, not
  measurement): for odd m the birth-seat S at ladder depth d is
  2m+2d+1, which equals 3m exactly at d=(m−1)/2 — the mid-ladder
  slice; m=19@d=9 is the first (m,d) pair where that slice is both
  in-sweep and measured. The trio's lifecycle beyond z=55 is
  UNKNOWN and is registered as the primary open question for the
  next kit (log S5).
- Frontier parity: the 17th datum m=29@z=57 measured {29,30}@S=59
  UP 2v0 and the 18th m=30@z=58 measured (30,30)@S=60 UP 2v1, both
  EXACT HITS of the registered candidates; the frontier parity
  scaffold is now 18/18 (m=13..30, K1268 z*(m) arithmetic, per-row
  observations only).
- First-ever rows measured for m=29 and m=30 (z=57 / z=58);
  first-ever below-frontier rows for m=27 (z=45..52) and m=28
  (z=46..53).
- Deaths witnessed this run (first datum for each): m=27 d=0 death
  (item 21), m=28 d=0 (item 24) — the first m=27 / m=28 deaths;
  m=25 d=1 / m=26 d=1 deaths (items 14 / 17); m=19 / m=20 deaths of
  d=7 (items 1 / 3); m=21 / m=22 deaths of d=3, m=23 / m=24 deaths
  of d=2 (items 5 / 7 / 9 / 11).
- Ladder depth achieved: m=19 / m=20 birth d=9 measured (COMPLETE
  through d=9); m=21 / m=22 to d=5, m=23 / m=24 to d=4, m=25 / m=26
  to d=3, m=27 / m=28 to d=1 (both with first deaths).
- One-past decay counts (registered-vs-measured, per-row
  observations): the d=0 one-past decays now stand at odd 32
  (m∈{13..27}, the m=27 2→1 UP 1v0 measured here) and even 31
  (m∈{14..28}, the m=28 2→0 DOWN 0v1 measured here).
- Window / scaffold outcome: 46 rows, 634 shapes, 0 separations —
  ALL CLEAN. Consequences for the measured-line bookkeeping (row
  records only, no claim):
  - m=25: every slice z in {25..55} now has a measured row record
    (z=25/26 by the published floor-20 strips, 27..32 here,
    33..40 here, 41..48 by kit-6, 49..55 by the chain). The m=25
    line is the first m-line to be measured end-to-end from its
    band floor z=25 through its d=3 birth z=55.
  - m=26: every slice z in {26..56} is measured (z=26 strip,
    27..34 here, 35..50 here+kit-6, 51..56 chain). DATED CORRECTION
    (2026-11-26, disclosed here): this kit's frozen docstring
    pre-declared the conditional "m=26 becomes FULLY SWEPT z in
    {25..56} iff the scaffold rows measure clean" — that
    conditional was WRONG at the single slice z=25: the published
    z=25 floor strip measured m ∈ {20..25} only, so m=26@z=25 was
    never measured. The honest state is z ∈ {26..56} measured, with
    the single hole at z=25. The hole row is registered for the
    next kit (log S5). Kit bytes are not edited; this paragraph is
    the correction.
  - Below-frontier vacuum rows: m=27 z ∈ {45..52} and m=28 z ∈
    {46..53} measured clean — the below-frontier band of the two
    newest m-lines starts its measured history with 16 clean rows.

## Verification

- Determinism: published run + 4 local verification runs
  byte-identical, plus a push-time rerun (disclosed in the log).
- Independent ordered-engine audit (`audit_kit7.py`, an INDEPENDENT
  re-derivation of every row with the published engine's ordered
  product rather than the sweep dedup): 72 rows, 1041 shapes, 39
  ordered-separations, 0 bad; anchors ordered 141/141; candidate
  classification 25 FULL HIT + 1 DEVIATION reproduced independently.
- Engine-free paper derivation (`derive_kit7.py` /
  `derived_kit7.json`): every registered literal re-derived from the
  K0832 closed form and the seat lifecycle arithmetic (260 checks,
  0 errors, run BEFORE the row runs; the checker itself needed two
  fixes during the pre-freeze build, disclosed in the log — the
  registration table passed on first derivation and was never
  edited).
- No universal claim is made. K0832 closed form remains the only
  PROVED statement. The standard 11×11 cell remains UNKNOWN at all
  times; this kit does not touch it. No K slot is claimed. No
  residual verdict is consumed.

## Next-kit handoff

The frozen output section `future_slice_registration_constants`
registers 28 binding rows for the next execution (ladder continuation
m=19..m=30, the m=29 / m=30 mini-ladders, the 19th / 20th frontier
datum candidates m=31@z=61 / m=32@z=62). The kit-7 log S5 adds the
trio-tracker registrations (m=19 z=56 / z=57 trio status candidates,
single-datum provenance, marked non-binding observations), the m=26
z=25 hole row, and the trio mid-slice probe proposals for m=13 / 15 /
17 (unregistered until their own counter-probe). See
`research/log/2026-11-26-m29m30-ladders-frontier-inband-predecl-microkit.md`.
