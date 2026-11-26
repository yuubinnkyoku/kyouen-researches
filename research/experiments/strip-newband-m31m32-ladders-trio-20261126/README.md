# newband m31/m32 frontier first contacts + m19..m32 ladder continuation + trio lifecycle + m26 hole + m13/15/17 trio mid-slice probes + m29/m30 below-frontier windows pre-declaration exploration kit (frozen)

This directory is the publish-then-execute PRIMARY RECORD for the
pre-declaration census of the REGISTERED kit-7 frozen section (d)
constants (commit a62c5d2e): the 28 binding candidate rows (the ladder
continuation / birth / death rows of m=19..m=28, the m=29 / m=30
mini-ladder rows, and the frontier first contacts m=31@z=61 / m=32@z62,
the registered 19th / 20th K1268 parity datum candidates, FIRST-EVER
rows for those m), the TRIO-TRACKER rows at m=19 z=56 / z=57 (kit-7 log
S5 item 10, NON-BINDING: the stacked trio {19,19,19}@S=57 tracked
beside the binding seats, outcome the datum either way), the m=26 z=25
HOLE ROW (kit-7 log S5 item 11, the single unmeasured slice of the
m=26 line, registered candidate 0 separations), the TRIO MID-SLICE
PROBES m=13@z=37 / m=15@z=43 / m=17@z=49 (kit-7 log S5 item 12
proposals, counter-probed 0-hit at this build, registered at the
ENGINE-FREE derived slices z=z*(m)+2d=3m-2; DATED DISCLOSURE: the
kit-7 log prose z values 42/48 for m=15/m=17 are off-by-one typos, the
m=13 value 37 matches the derivation; binding birth-template
candidates + NON-BINDING trio mimic candidates), and the WINDOW SWEEPS
m=29 z in {49..56} / m=30 z in {50..57} (kit-7 frozen section (d) items
29/30, register-before-measure satisfied by this freeze; FIRST-EVER
below-frontier rows for m=29/m=30), plus 180 published anchor rechecks
(the 141 kit-7-era anchors VERBATIM + the 39 kit-7 separation spots,
machine-extracted from the published kit-7 frozen .out and
machine-verified 39/39 BEFORE the first run of this kit by
verify_new_anchors_kit8.py, independent pre-freeze script). No K slot
is claimed and no claim is made here: everything below is machine
observation; the only PROVED statement remains the K0832 closed form.

## Files

- `engine_block.py` — byte-clone of the published chain engine, sha256
  `582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8841d3a6610d5c0`
  (byte-identical to the kit-4/kit-5/kit-6/kit-7 chain); embedded
  ENGINE_BLOCK startup pin `bd5f22e4…` asserted (engine_gate PASS in
  the frozen output).
- `explore_m31m32_ladders_trio.py` — frozen pre-declaration explorer,
  sha256 `c6f2dda907163f51251b0481433c24ecf18a02b81ab407045da61c25cc2af349`
  (71,430 bytes; assembled programmatically from the published kit-7
  explorer — ENGINE_BLOCK, parts/row_record/row_record_x0 helpers and
  the 141-entry anchor_spec copied verbatim, byte-fidelity asserted by
  the assembler — plus the machine-derived kit8_spec.json). Every
  registered literal was machine-regenerated engine-free by
  `derive_kit8.py` (370 structural asserts, 0 failures; the regenerated
  prediction TEXT of all 28 binding rows byte-matches the kit-7 frozen
  constants — stick-slice occupancy z=S(d-1), death-slice occupancy
  z=S(d-1)+1, co-token/S/R arithmetic and every collapse v() literal
  machine-recomputed, per the kit-6 lifecycle-shift lesson).
- `explore_m31m32_ladders_trio.out` — the frozen stdout, sha256
  `5723304c58416ea9a858439a813b972a2c1bc6133eb239718b583c39795bc8c0`
  (137,126 bytes). Deterministic — the published run plus FIVE
  verification runs are all byte-identical (default x2, PYTHONHASHSEED
  =random, env -i isolated x2, ~42 s per run), plus the push-time
  rerun disclosed in the log.
- `derive_kit8.py` — the engine-free derivation checker (pre-freeze):
  regenerates the 28 binding predictions from the K0832 closed form +
  seat-lifecycle scaffold (0 text mismatches vs the kit-7 frozen
  constants), derives the probe slices 37/43/49 and the kit-9 future
  constants, and emits the battery triple union (1,004 triples).
- `verify_new_anchors_kit8.py` — the pre-freeze anchor verifier: the
  39 kit-7 separation spots re-measured 39/39 with the canonical
  engine against the published kit-7 .out values, and the embedded
  anchor table asserted to be 141 byte-identical inherited entries
  + exactly 39 new (transcription 39/39), BEFORE the first census run.
- `audit_kit8.py` — the post-run INDEPENDENT ordered-engine audit:
  re-executes every row with H_ordered instead of the canonical sweep
  (48 rows, 763 shapes, 54 separations, 0 mismatches), re-anchors all
  180 spots with the ordered engine (180/180), re-checks the battery
  (1,004/1,004 closed==canonical==ordered), and classifies the binding
  rows against the registered candidate texts.

## Registered targets taken by this kit (before the fact)

1. kit-7 frozen section (d) items 1-28, verbatim binding candidates.
2. kit-7 log S5 item 10: the trio-tracker rows (NON-BINDING).
3. kit-7 log S5 item 11: the m=26 z=25 hole row (candidate 0 separations).
4. kit-7 log S5 item 12: the trio mid-slice probes m=13/15/17 (binding
   birth-template candidates + NON-BINDING trio mimic candidates,
   registered at the derived z=3m-2 slices with the dated disclosure of
   the kit-7 prose off-by-one).
5. kit-7 frozen section (d) items 29/30: the window sweeps m=29
   z in {49..56}, m=30 z in {50..57} (registered at this build).
6. The anchor chain: 141 inherited verbatim + 39 kit-7 spots.

SWEEP-DOMAIN RULE (frozen in the docstring): every depth row sweeps
S in {m..max(m+38, z+2)} — the kit-7 cap m+38 stops covering the NEW
birth seats S(d)=z+2 from d=10 onward for m in {19,20}; the extension
is the minimal domain covering every registered named seat.

## Measured outcome (machine observation, no claim)

- Anchors: 180/180 exact (141 inherited + 39 kit-7 spots, the latter
  also pre-freeze verified 39/39). Battery: 1,004/1,004 literals
  closed==canonical==ordered (the cumulative kit-era union: no
  prior datum lost; layout disclosed in the docstring).
- Registered binding rows: 28 executed, shapes 407 seat-triples with
  54 total separations. **26/28 FULL HIT** (the measured separating
  2-token seats are exactly the registered named seats of each
  candidate), **2 REGISTERED-CANDIDATE MEASUREMENT DEVIATIONS — the
  2nd and 3rd of the kit series**: item 2 (m=19 z=57, birth slice
  d=10) and item 4 (m=20 z=58, birth slice d=10). Both registered
  named-seat pairs measured EXACT HITS (stick + NEW); the deviations
  are UNREGISTERED separating stack shapes at the seats' S values:
  at m=19 z=57 the THREE-token shapes {19,19,21}@59 and {19,20,20}@59
  (2v0 UP, exact numeric mimics of the NEW birth seat {19,40}@59 UP
  2v0 they split the co-token of), one of which ({19,20,20}} is
  beyond the kit-7 sweep cap and only visible through this kit's
  domain extension; at m=20 z=58 the stack {20,20,20}@60 (2v1 UP,
  exact mimic of the NEW birth seat (20,40)@60 UP 2v1). The named-seat
  scaffold survived 40/40 seat hits across the 28 rows.
- TRIO-TRACKER outcomes (explicit, as registered): m=19 z=56 trio
  {19,19,19}@57 = **1v0 UP, the EXACT MIMIC of the registered mimic
  candidate** (like the birth seat one-past {19,38}@57 UP 1v0); m=19
  z=57 trio = **1v2 DOWN, the EXACT MIMIC** (like the stick {19,38}@57
  DOWN 1v2). The trio at S=57 follows the S=57 seat-class lifecycle
  slice by slice so far (birth 2v0 -> one-past 1v0 -> stick 1v2).
- TRIO MID-SLICE PROBES: all three FIRST-EVER rows measured the
  binding birth-template seats EXACT (stick 1v2 + NEW 2v0 UP), and
  all three trios measured **2v0 UP at S=3m — the mimic candidate
  HIT 3/3** ({13,13,13}@39, {15,15,15}@45, {17,17,17}@51). The
  stacked-trio mid-ladder shadow GENERALIZES to all in-sweep odd
  m (13/15/17/19 now observed); the even analogue appeared at m=20
  d=10 ({20,20,20}, the mid-ladder depth d=m/2 for even m).
- FRONTIER: the 19th datum m=31@z=61 measured {31,32}@S=63 UP 2v0
  (collapse v(63,61,93)=0) and the 20th m=32@z=62 measured
  (32,32)@S=64 UP 2v1 (collapse v(64,62,95)=1), both EXACT HITS; the
  frontier parity scaffold is now 20/20 (m=13..32, per-row
  observations). FIRST-EVER rows for m=31 and m=32.
- Deaths witnessed this run (first datum for each): m=19/m=20 deaths
  of d=8 (z=56/z=57), m=21/m=22 deaths of d=4, m=23/m=24 deaths of
  d=3, m=25/m=26 deaths of d=2, m=29/m=30 deaths of d=0 (z=60/z=61,
  the first m=29/m=30 deaths). The m=27/m=28 one-past/death rows
  re-measured kit-7's own item-21/item-24 slices (a redundancy of the
  kit-7 future list, disclosed in the log) and agreed exactly.
- Ladder depths after kit-8: m=19/m=20 births through d=10 (deepest
  measured yet); m=21/m=22 through d=6; m=23/m=24 through d=5;
  m=25/m=26 through d=4; m=27/m=28 through d=2; m=29/m=30 through
  d=1. One-past d=0 decay counts: odd 34 (m in {13..29}, the m=29
  2->1 measured here), even 33 (m in {14..30}, the m=30 2->0 here).
- m=26 z=25 HOLE ROW: CLEAN (14 shapes, 0 separations) — the m=26
  line is the series-second FULLY SWEPT measured line,
  z in {25..56}, after m=25.
- WINDOW SWEEPS: m=29 z in {49..56} and m=30 z in {50..57},
  16 rows, 154 shapes, 0 separations — ALL CLEAN; the below-frontier
  bands of the two newest odd/even pairs begin their measured
  history clean, matching the in-band-clean precedent.

## Verification

- Pre-freeze: derive_kit8.py (370 checks, 0 errors; 28 binding texts
  byte-match kit-7's frozen constants; probe slices derived, kit-7
  prose off-by-one disclosed); verify_new_anchors_kit8.py (39/39
  canonical re-measurement + 141+39 table byte-fidelity + 39/39
  transcription).
- Determinism: published run + 5 verification runs byte-identical,
  plus the push-time rerun (disclosed in the log).
- Independent ordered-engine audit (audit_kit8.py): 48 rows, 763
  shapes, 54 ordered-separations, 0 mismatches; anchors ordered
  180/180; battery 1,004/1,004; classification 26 FULL HIT +
  2 DEVIATION reproduced independently.
- No universal claim is made. K0832 remains the only PROVED
  statement. The standard 11x11 cell remains UNKNOWN at all times;
  this kit does not touch it. No K slot is claimed. No residual
  verdict is consumed.

## Next-kit handoff

The frozen output section `future_slice_registration_constants`
registers the kit-9 binding candidates (ladder continuation of every
line measured here, the m=29/m=30 d=2/d=3 rows, the CONTINGENT
m=31/m=32 mini-ladders, and the 21st / 22nd frontier datum
candidates m=33@z=65 / m=34@z=66), plus the window proposals for
m=31/m=32 and the trio-tracker continuation. The kit-8 log S5 adds
the STACK-SHADOW registration rule and the explicit stack candidates
for the kit-9 birth rows (observed shadow census to date: 6 measured
birth slices with in-sweep stack-split seats — m=19 d=9 (kit-7),
m=13 d=6, m=15 d=7, m=17 d=8, m=19 d=10, m=20 d=10 — hosting 7
shadow separations {19,19,19}@57, {13,13,13}@39, {15,15,15}@45,
{17,17,17}@51, {19,19,21}@59, {19,20,20}@59, {20,20,20}@60, every
one an exact numeric mimic of its host seat, 0 conforming stacks),
the m=13/15/17 lifecycle continuation
rows, and the probe-derived one-past rows. See
`research/log/2026-11-26-m31m32-ladders-trioprobe-predecl-microkit.md`.
