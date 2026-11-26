# m29/m30 frontier first contacts + m19..m26 ladders + m25/m26 scaffolds pre-declaration micro-kit (kit-7)

- kit id: kit-7 (hourly lane, session 2026-11-26, ~10:07Z build)
- runclass: publish-then-execute pre-declaration census, frozen before the
  literal push; committee by machine observation only
- commit base: 76c461da (kit-6); main head at build 52826b45
  (counter-probe at build: 9 code-collision queries over the kit-7
  territory, 0 hits, ~10:04Z)
- files:
  `research/experiments/strip-newband-m29m30-ladders-frontier-inband-20261126/{engine_block.py, explore_m29m30_frontier.py, explore_m29m30_frontier.out, README.md}`
- engine: published chain clone, sha 582c93c1…, startup pin bd5f22e4… (PASS)
- explorer sha256: `b9724059783942b7d60cb25e66c3f6604d8fc674d3e92f6c30aca7f3d15e04fd`
- frozen output sha256: `5263c898efa8eb39b3a09039dee647435bf78db413b6fc573a7bd6689b94c1e6` (126,668 bytes)
- status: EXECUTED, VERIFIED, PUSHED (run rc 0, ~41 s; see S4)

## S1. Anchor re-verification (141/141)

The 112 inherited chain anchors verbatim, plus the 29 kit-6
separation spots FIRST re-anchored here. The 29 spots were
derive-checked against the published kit-6 .out values and passed
29/29 BEFORE the frozen census (independent script
`verify_new_anchors.py`, canonical engine, published spots only),
then every anchor was re-executed in the frozen run and hit exactly
(R-first convention asserted). Battery 737/737 all-match (K0832
closed-form vs canonical vs ordered, the cumulative chain battery
including every registration literal used or emitted by this kit). No
prior datum lost; cumulative anchor count 141.

## S2. Registered vs measured (25/26 FULL HIT + 1 DEVIATION — the first registered-candidate deviation of the kit series)

26 registered rows executed (407 shapes, 38 seat separations + 1
unregistered trio separation):

| row | registered candidate (binding) | verdict | measured |
|----|----|----|----|
| m=19 z=54 (item 1) | EXACTLY ONE {19,36}@S=55 UP 1v0, {19,34} dead | HIT | as registered; first m=19 d=7 death |
| m=19 z=55 (item 2) | EXACTLY TWO: stick {19,36} DOWN 1v2 + NEW {19,38}@S=57 UP 2v0 (d=9 birth, gap 19) | **DEVIATION** | the two named separations HIT, plus an UNREGISTERED third separation {19,19,19}@S=57 UP 2v0 (trio, see below); m=19 ladder COMPLETE through d=9 |
| m=20 z=55 (item 3) | EXACTLY ONE (20,36)@S=56 DOWN 0v1, (20,34) dead | HIT | first m=20 d=7 death |
| m=20 z=56 (item 4) | EXACTLY TWO: stick + (20,38)@S=58 UP 2v1 (d=9 birth, gap 18) | HIT | m=20 ladder COMPLETE through d=9 |
| m=21 z=50 (item 5) | EXACTLY ONE {21,30}@S=51 UP 1v0, {21,28} dead | HIT | first m=21 d=3 death |
| m=21 z=51 (item 6) | EXACTLY TWO: stick 1v2 + {21,32}@S=53 UP 2v0 (d=5 birth, gap 13) | HIT | as registered |
| m=22 z=51 (item 7) | EXACTLY ONE (22,30)@S=52 DOWN 0v1, (22,28) dead | HIT | first m=22 d=3 death |
| m=22 z=52 (item 8) | EXACTLY TWO: stick 0v2 + (22,32)@S=54 UP 2v1 (d=5, gap 12) | HIT | as registered |
| m=23 z=52 (item 9) | EXACTLY ONE {23,30}@S=53 UP 1v0, {23,28} dead | HIT | first m=23 d=2 death |
| m=23 z=53 (item 10) | EXACTLY TWO: stick + {23,32}@S=55 UP 2v0 (d=4, gap 11) | HIT | as registered |
| m=24 z=53 (item 11) | EXACTLY ONE (24,30)@S=54 DOWN 0v1, (24,28) dead | HIT | first m=24 d=2 death |
| m=24 z=54 (item 12) | EXACTLY TWO: stick + (24,32)@S=56 UP 2v1 (d=4, gap 10) | HIT | as registered |
| m=25 z=53 (item 13) | EXACTLY TWO: stick {25,28} DOWN 1v2 (stick coincides z=S(d-1)) + NEW {25,30}@S=55 UP 2v0 (d=2, gap 9) | HIT | as registered |
| m=25 z=54 (item 14) | EXACTLY ONE {25,30}@S=55 UP 1v0, {25,28} dead | HIT | first m=25 d=1 death |
| m=25 z=55 (item 15) | EXACTLY TWO: stick + NEW {25,32}@S=57 UP 2v0 (d=3, gap 9→32) | HIT | as registered |
| m=26 z=54 (item 16) | EXACTLY TWO: stick (26,28) DOWN 0v2 (coincides) + NEW (26,30)@S=56 UP 2v1 (d=2, gap 8) | HIT | as registered |
| m=26 z=55 (item 17) | EXACTLY ONE (26,30)@S=56 DOWN 0v1, (26,28) dead | HIT | first m=26 d=1 death |
| m=26 z=56 (item 18) | EXACTLY TWO: stick + NEW (26,32)@S=58 UP 2v1 (d=3, gap 32) | HIT | as registered |
| m=27 z=54 (item 19) | EXACTLY ONE {27,28}@S=55 UP 1v0 (d=0 one-past decay 2→1) | HIT | odd decay count → 32 |
| m=27 z=55 (item 20) | EXACTLY TWO: stick {27,28} DOWN 1v2 (coincides) + NEW {27,30}@S=57 UP 2v0 (d=1, gap 5→30) | HIT | as registered |
| m=27 z=56 (item 21) | EXACTLY ONE {27,30}@S=57 UP 1v0, {27,28} dead | HIT | FIRST m=27 death (d=0) |
| m=28 z=55 (item 22) | EXACTLY ONE (28,28)@S=56 DOWN 0v1 (d=0 one-past decay 2→0) | HIT | even decay count → 31 |
| m=28 z=56 (item 23) | EXACTLY TWO: stick (28,28) DOWN 0v2 + NEW (28,30)@S=58 UP 2v1 (d=1, gap 28→30) | HIT | as registered |
| m=28 z=57 (item 24) | EXACTLY ONE (28,30)@S=58 DOWN 0v1, (28,28) dead | HIT | FIRST m=28 death (d=0) |
| m=29 z=57 (item 29) | EXACTLY ONE {29,30}@S=59 UP 2v0 (17th parity datum candidate, z*(29)=57) | HIT | FIRST-EVER m=29 row |
| m=30 z=58 (item 30) | EXACTLY ONE (30,30)@S=60 UP 2v1 (18th, z*(30)=58) | HIT | FIRST-EVER m=30 row |

Frontier parity scaffold: 18/18 (m=13..30, per-row observations).

### The item-2 deviation: the stacked-trio shadow seat

At the m=19 z=55 birth slice d=9, a THIRD separation measured beyond
the registered pair: {19,19,19}@S=57 UP 2v0 (value 2, collapse 0) —
numerically an exact mimic of the d=9 NEW birth seat {19,38} it shares
S=57 with (same S, same value, same collapse, direction UP). Facts
established by this row and its neighbors (all machine observation):

- The trio row conforms (not a separation) at every measured m=19
  slice z ≤ 54 (lifecycle kits through the kit-7 scaffold rows); it
  separates ONLY at the z=55 birth slice, and only in-scope here.
- Sweep membership: the x0 sweep at (m, z) covers X with sum S ≤
  z+2 ≤ m+38, so the trio is inside the sweep iff 3m ≤ m+38, i.e.
  m ≤ 19. m=19 is the largest in-sweep m; the trio shadow is not
  testable for m ≥ 20 under this convention.
- Engine-free lemma (arithmetic, not measurement): for odd m the
  birth-seat sum at depth d is S=2m+2d+1, which equals 3m exactly at
  d=(m−1)/2 — the mid-ladder slice. m=19@d=9 is the first (m,d)
  pair where the mid-ladder slice is both in-sweep and measured. The
  corresponding odd candidates below 19 are m=17@d=8 (z=48),
  m=15@d=7 (z=42), m=13@d=6 (z=37) — unmeasured (S5 proposals).
- The trio shares ONLY the numeric seat class, not the shape: the
  birth seat is {19,38} and the trio {19,19,19}; both collapse to 0
  at z=55 with value 2. No lifecycle fact about the trio beyond
  z=55 is known; it is the primary open question of the next kit.

## S3. State after kit-7 (scaffolding bookkeeping, no claim)

- Window sweeps (kit-6 items 1-4, registered here from the SSOT):
  m=25 z{33..40} and m=26 z{35..42}, 16 rows clean. The kit-6 label
  disclosure is now fully resolved on the label side (the list side
  was measured by kit-6: z{43..50} clean).
- Scaffold sweeps (kit-6 item 31, registered before measuring at
  this build): m=25 z{27..32} and m=26 z{27..34}, 14 rows clean.
- Below-frontier history opened for m=27 (z{45..52}) and m=28
  (z{46..53}): 16 rows clean.
- Measured-line bookkeeping (row records only):
  - m=25: z {25..55} COMPLETE (25/26 strips, 27..40 this kit,
    41..48 kit-6, 49..55 chain) — the first end-to-end measured
    m-line of the series, from the band floor to the d=3 birth.
  - m=26: z {26..56} measured, single hole at z=25 (the published
    z=25 floor strip covered m ∈ {20..25} only). Hole registered in
    S5. See S6 for the dated correction of this kit's docstring
    conditional.
- Ladder depths after kit-7: m=19/20 d=9 COMPLETE (the deepest
  measured yet); m=21/22 d=5; m=23/24 d=4; m=25/26 d=3; m=27/28
  d=1 with first deaths. Frontier m=29/30 first contacts taken.
- One-past d=0 decay counts: odd 32 (m ∈ {13..27}), even 31
  (m ∈ {14..28}).

## S4. Verification (all executed)

1. Pre-freeze derivation: `derive_kit7.py` — engine-free paper
   derivation of every registered literal from the K0832 closed form
   and the seat lifecycle arithmetic (z*(m)=2m−2+(m%2) per K1268;
   birth slice z=z*+2d, co-token m+2d+1 (m odd)/m+2d (m even),
   S=2m+2d+1 (odd)/2m+2d (even), one-past z=z*+2d+1, dead shape
   S=z−1, stick seat S=z, NEW birth S=z+2). 260 checks, 0 errors,
   run BEFORE the first row sweep. Also cross-checked the kit-6
   frozen .out section (d): all 30 measurable items' 48 collapse
   literals re-derived, 0 mismatch — and drew the kit-6 log S2
   prose/list discrepancy for m=25@z=51 into the daylight (S6).
2. Pre-freeze anchor verification: `verify_new_anchors.py` — the 29
   kit-6 spots re-measured 29/29 on the published canonical engine
   BEFORE any row of this kit ran.
3. Frozen run: rc 0, ~41 s, stdout sha 5263c89…
   (`explore_m29m30_frontier.out`).
4. Determinism: published run + default rerun + PYTHONHASHSEED=random
   + env -i isolated (×2): 5 local runs byte-identical; plus the
   push-time rerun disclosed in S6.
5. Independent ordered-engine audit: `audit_kit7.py` re-executed
   every row with the ordered product instead of the sweep dedup:
   72 rows, 1041 shapes, 39 ordered-separations, 0 bad; anchors
   ordered 141/141; classification 25 FULL HIT + 1 DEVIATION
   reproduced independently (the trio measured (2,0,55,75) both
   ways).
6. Standard caveats: the K0832 closed form remains the only PROVED
   statement; every item above is a finite machine observation; the
   standard 11×11 cell remains UNKNOWN at all times; no K slot is
   claimed; no residual verdict is consumed.

## S5. Handoff: kit-8 registrations (28 binding rows frozen in section (d) + 4 new log-level registrations)

Frozen in the kit-7 .out section (d)
(`future_slice_registration_constants`), all verbatim-binding for the
next execution kit:

1. m=19 z=56 (one-past-of-d=9 / death-of-d=8), m=19 z=57 (birth d=10).
2. m=20 z=57, m=20 z=58 (same stages, m=20).
3. m=21 z=52 / z=53, m=22 z=53 / z=54 (one-past-of-d=5, birth d=6).
4. m=23 z=54 / z=55, m=24 z=55 / z=56 (one-past-of-d=4, birth d=5).
5. m=25 z=56 / z=57, m=26 z=57 / z=58 (one-past-of-d=3, birth d=4).
6. m=27 z=56 / z=57, m=28 z=57 / z=58 (one-past-of-d=1 / death, birth d=2).
7. m=29 z=58 / z=59 / z=60 (one-past, birth d=1, one-past+death).
8. m=30 z=59 / z=60 / z=61 (same stages, m=30).
9. m=31 z=61, m=32 z=62 (19th / 20th frontier parity datum
   candidates, FIRST-EVER rows; z*(31)=61, z*(32)=62 double-derived).

New registrations made by this kit's observations (log-level,
registered for the next execution):

10. TRIO-TRACKER (single-datum provenance, NON-BINDING observation
    candidates; any outcome is the datum):
    m=19 z=56 — trio {19,19,19}@S=57 candidate (mimic): UP 1v0 like
    the birth seat's one-past, or conform / other. m=19 z=57 — trio
    candidate (mimic): DOWN 1v2 like the stick, or conform / other.
    The binding candidate for the SEAT separations of both rows
    remains frozen in section (d); the trio is tracked beside it and
    must be reported explicitly either way.
11. m=26 z=25 hole row (plain scan, registered candidate: 0
    separations; closes the m=26 measured line to {25..56} if
    clean).
12. TRIO MID-SLICE PROBES (proposals — COUNTER-PROBE BEFORE
    REGISTERING at the next build; none of these rows is in any
    published sweep as of this kit's build-time counter-probe):
    m=13 z=37, m=15 z=42, m=17 z=48 (the odd mid-ladder slices
    d=6/7/8 where S_birth=3m holds; full x0 row records).
13. Window proposals below-frontier (measurement suggested, not
    binding): m=29 z{49..56}, m=30 z{50..57} — the same
    below-frontier sweep pattern this kit opened for m=27/28.

## S6. Honest record / caveats

1. The item-2 DEVIATION is the kit series' first registered-candidate
   measurement deviation. The pre-declaration protocol did its job:
   the template "EXACTLY TWO" was falsified as a row-level candidate
   by an observation the template did not predict. The seat-scaffold
   itself (stick + NEW birth) survived 38/38 named-separation hits;
   what the template missed is a SHADOW seat class (stack trios at
   shared S) which the row-level "EXACTLY" bookkeeping must now
   audit for at every birth slice with an in-sweep trio (m ≤ 19).
   No claim is upgraded or downgraded by this deviation; the K0832
   closed form is untouched (the trio's collapse was computed by it
   and conformed to the measurement).
2. DATED DISCLOSURE: the kit-6 log S2 table row m=25@z=51 is a prose
   mis-statement of its own SSOT. The kit-5/kit-6 frozen .out
   registrations and the kit-6 measurement agree on "stick {25,26}
   DOWN 1v2 at S=51 + NEW {25,28}@S=53 UP 2v0"; the kit-6 log prose
   wrote "{25,26} UP + {25,28}@S=52". This kit measured
   m=25@z=53/z=54 independently and re-verified the SSOT reading
   (the .out literals that kit-7 registered its m=25 candidates
   from). Kit bytes are never edited; this is the dated correction.
3. DATED CORRECTION: this kit's frozen docstring pre-declared the
   m=26 conditional "FULLY SWEPT z in {25..56} iff the scaffold rows
   measure clean". That was wrong at the single slice z=25: the
   published z=25 floor strip covered m ∈ {20..25} only, so
   m=26@z=25 has never been measured. Corrected state: z {26..56}
   measured, hole registered (S5 item 11). The m=25 conditional held
   and the m=25 line is confirmed complete.
4. Pre-freeze build errors, caught and fixed BEFORE the freeze, all
   checker-side (registration tables passed their first derivation
   and were never edited): two `derive_check_kit7.py` bugs (a NEW-birth
   S off-by-one in the checker's expectation, and a stick-token @S
   parse omission); two first-draft `audit_kit7.py` false positives
   (key-order dependence and the same stick-token omission). No data
   blemish; the frozen bytes never changed after the freeze.
5. This kit measured 1041 shapes across 72 rows and re-measured 141
   anchors without any contradiction of any published datum, except
   the row-level deviation of item 2, which contradicts no prior
   observation and was invisible to every prior sweep
   (the m=19 z=55 slice had never been measured).
6. No universal claim is made here. K0832 is the only PROVED
   statement. The 11×11 standard cell remains UNKNOWN at all times.
   No K slot is claimed. No residual verdict is consumed. The
   hourly lane may run concurrently; the push-time counter-probe
   record is in the push commit body.
