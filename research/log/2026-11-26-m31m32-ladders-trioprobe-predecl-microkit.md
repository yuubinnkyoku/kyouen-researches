# m=31/m=32 frontier first contacts + m=19..m=28 ladder continuation + trio lifecycle + m=26 hole + m=13/15/17 trio mid-slice probes + m=29/m=30 below-frontier windows pre-declaration micro-kit (kit-8)

- kit id: kit-8 (hourly lane, session 2026-11-26, ~10:34Z build)
- runclass: publish-then-execute pre-declaration census, frozen before the
  literal push; candidate-vs-measured committee by machine observation only
- commit base: a62c5d2e (kit-7); main head at build a62c5d2e (no
  intervening commits at build; counter-probe at build: 10 code-collision
  queries over the kit-8 territory, 0 hits). At push time the head had
  advanced to 2db639d0 (the parallel part-ew lane's 10:37–10:39Z commits),
  none of which touches this kit's territory: the push-time counter-probe
  (10 queries re-run) returned 0 kit-8-territory hits and both target
  paths (this experiment directory and this log) did not exist on main.
- files:
  `research/experiments/strip-newband-m31m32-ladders-trio-20261126/{engine_block.py, explore_m31m32_ladders_trio.py, explore_m31m32_ladders_trio.out, derive_kit8.py, verify_new_anchors_kit8.py, audit_kit8.py, README.md}`
- engine: published chain clone, sha 582c93c1…, startup pin bd5f22e4… (PASS)
- explorer sha256: `c6f2dda907163f51251b0481433c24ecf18a02b81ab407045da61c25cc2af349`
- frozen output sha256: `5723304c58416ea9a858439a813b972a2c1bc6133eb239718b583c39795bc8c0` (137,126 bytes)
- status: EXECUTED, VERIFIED, PUSHED (run rc 0, ~42 s; see S4)

## S1. Anchor re-verification (180/180)

The 141 kit-7-era chain anchors verbatim, plus the 39 kit-7 separation
spots FIRST re-anchored here. The 39 spots were machine-extracted from
the published kit-7 frozen .out (fetched byte-identical, sha 5263c898…)
and derive-checked against its published values BEFORE the frozen census
(independent pre-freeze script `verify_new_anchors_kit8.py`, canonical
engine, published spots only): 39/39 canonical re-measurement, anchor
table byte-fidelity 141 inherited + exactly 39 new, transcription 39/39.
In the frozen run every anchor re-executed and hit exactly
(180/180 match, R-first convention asserted). Battery 1,004/1,004
all-match (K0832 closed-form vs canonical vs ordered, the cumulative
kit-era triple union including every registration literal used or
emitted by this kit). No prior datum lost; cumulative anchor count 180.

## S2. Registered vs measured (26/28 FULL HIT + 2 DEVIATIONS — the 2nd and 3rd registered-candidate deviations of the kit series)

28 binding rows executed (kit-7 frozen section (d) items 1–28; 407
binding-row seat-triples inside 763 total shapes and 54 total
separations across all 48 rows of this kit):

| row | registered candidate (binding) | verdict | measured |
|----|----|----|----|
| m=19 z=56 (item 1) | EXACTLY ONE {19,38}@S=57 UP 1v0; {19,36} dead; death-of-d=8 | HIT | as registered; first m=19 d=8 death; the NON-BINDING trio-tracker measured alongside (below) |
| m=19 z=57 (item 2) | EXACTLY TWO: stick {19,38} DOWN 1v2 + NEW {19,40}@S=59 UP 2v0 (d=10 birth, gap 21) | **DEVIATION** | both named separations HIT, plus TWO UNREGISTERED separating stack shapes {19,19,21}@59 UP 2v0 and {19,20,20}@59 UP 2v0 (exact numeric mimics of the NEW birth seat they share S=59 with); m=19 ladder COMPLETE through d=10 (deepest measured) |
| m=20 z=57 (item 3) | EXACTLY ONE (20,38)@S=58 DOWN 0v1; (20,36) dead; death-of-d=8 | HIT | first m=20 d=8 death |
| m=20 z=58 (item 4) | EXACTLY TWO: stick (20,38) DOWN 0v2 + NEW (20,40)@S=60 UP 2v1 (d=10, gap 20) | **DEVIATION** | both named separations HIT, plus ONE UNREGISTERED separating stack (20,20,20)@60 UP 2v1 (exact mimic of the NEW birth seat); m=20 ladder COMPLETE through d=10 |
| m=21 z=52 (item 5) | EXACTLY ONE {21,32}@S=53 UP 1v0; {21,30} dead; death-of-d=4 | HIT | first m=21 d=4 death |
| m=21 z=53 (item 6) | EXACTLY TWO: stick {21,32} DOWN 1v2 + NEW {21,34}@S=55 UP 2v0 (d=6 birth, gap 13) | HIT | as registered |
| m=22 z=53 (item 7) | EXACTLY ONE (22,32)@S=54 DOWN 0v1; (22,30) dead; death-of-d=4 | HIT | first m=22 d=4 death |
| m=22 z=54 (item 8) | EXACTLY TWO: stick (22,32) DOWN 0v2 + NEW (22,34)@S=56 UP 2v1 (d=6, gap 12) | HIT | as registered |
| m=23 z=54 (item 9) | EXACTLY ONE {23,32}@S=55 UP 1v0; {23,30} dead; death-of-d=3 | HIT | first m=23 d=3 death |
| m=23 z=55 (item 10) | EXACTLY TWO: stick {23,32} DOWN 1v2 + NEW {23,34}@S=57 UP 2v0 (d=5, gap 11) | HIT | as registered |
| m=24 z=55 (item 11) | EXACTLY ONE (24,32)@S=56 DOWN 0v1; (24,30) dead; death-of-d=3 | HIT | first m=24 d=3 death |
| m=24 z=56 (item 12) | EXACTLY TWO: stick (24,32) DOWN 0v2 + NEW (24,34)@S=58 UP 2v1 (d=5, gap 10) | HIT | as registered |
| m=25 z=56 (item 13) | EXACTLY ONE {25,32}@S=57 UP 1v0; {25,30} dead; death-of-d=2 | HIT | first m=25 d=2 death |
| m=25 z=57 (item 14) | EXACTLY TWO: stick {25,32} DOWN 1v2 + NEW {25,34}@S=59 UP 2v0 (d=4, gap 9) | HIT | as registered |
| m=26 z=57 (item 15) | EXACTLY ONE (26,32)@S=58 DOWN 0v1; (26,30) dead; death-of-d=2 | HIT | first m=26 d=2 death |
| m=26 z=58 (item 16) | EXACTLY TWO: stick (26,32) DOWN 0v2 + NEW (26,34)@S=60 UP 2v1 (d=4, gap 8) | HIT | as registered |
| m=27 z=56 (item 17) | EXACTLY ONE {27,30}@S=57 UP 1v0; {27,28} dead; one-past-of-d=1 / death-of-d=0 (REDUNDANT: kit-7's own S2 item 21 slice) | HIT | agrees exactly with kit-7's published measurement |
| m=27 z=57 (item 18) | EXACTLY TWO: stick {27,30} DOWN 1v2 + NEW {27,32}@S=59 UP 2v0 (d=2, gap 5) | HIT | m=27 through d=2 |
| m=28 z=57 (item 19) | EXACTLY ONE (28,30)@S=58 DOWN 0v1; (28,28) dead; one-past-of-d=1 / death-of-d=0 (REDUNDANT: kit-7's own S2 item 24 slice) | HIT | agrees exactly with kit-7's published measurement |
| m=28 z=58 (item 20) | EXACTLY TWO: stick (28,30) DOWN 0v2 + NEW (28,32)@S=60 UP 2v1 (d=2, gap 4) | HIT | m=28 through d=2 |
| m=29 z=58 (item 21) | EXACTLY ONE {29,30}@S=59 UP 1v0; one-past of the d=0 seat (frontier decay 2→1) | HIT | first m=29 one-past |
| m=29 z=59 (item 22) | EXACTLY TWO: stick {29,30} DOWN 1v2 + NEW {29,32}@S=61 UP 2v0 (d=1, gap 3) | HIT | as registered |
| m=29 z=60 (item 23) | EXACTLY ONE {29,32}@S=61 UP 1v0; {29,30} dead; death-of-d=0 | HIT | FIRST m=29 death |
| m=30 z=59 (item 24) | EXACTLY ONE (30,30)@S=60 DOWN 0v1; frontier decay 2→0 | HIT | as registered |
| m=30 z=60 (item 25) | EXACTLY TWO: stick (30,30) DOWN 0v2 + NEW (30,32)@S=62 UP 2v1 (d=1) | HIT | as registered |
| m=30 z=61 (item 26) | EXACTLY ONE (30,32)@S=62 DOWN 0v1; (30,30) dead; death-of-d=0 | HIT | FIRST m=30 death |
| m=31 z=61 (item 27) | EXACTLY ONE {31,32}@S=63 UP 2v0 (collapse v(63,61,93)=0); z*(31)=61 per K1268 | HIT | FIRST-EVER m=31 row; 19th parity datum |
| m=32 z=62 (item 28) | EXACTLY ONE (32,32)@S=64 UP 2v1 (collapse v(64,62,95)=1); z*(32)=62 per K1268 | HIT | FIRST-EVER m=32 row; 20th parity datum |

Frontier parity scaffold: 20/20 (m=13..32, per-row observations).
The named-seat scaffold survived 40/40 seat hits across the 28 rows.

### The item-2 and item-4 deviations: birth-slice co-token-split stack shadows

At the m=19 z=57 birth slice d=10, beyond the registered pair, TWO
unregistered three-token shapes separated: {19,19,21}@59 UP 2v0 and
{19,20,20}@59 UP 2v0. At the m=20 z=58 birth slice d=10, ONE unregistered
shape separated: (20,20,20)@60 UP 2v1. Facts established by these rows
(all machine observation):

- All three are exact numeric mimics of the NEW birth seat they share S
  with: same S (59 / 60), same value (2), same collapse, same direction,
  and they arise as SPLITS of the birth seat's co-token: at a birth slice
  the NEW seat is {m, co} with co = m+2d+1 (m odd) / m+2d (m even);
  a stack {m,x,y} with x+y = co, x,y ≥ m seats at the same S. m=19 d=10
  has co=40 and exactly two admissible splits with tokens ≥ 19: (19,21)
  and (20,20) — BOTH were measured separating. m=20 d=10 has co=40 and
  exactly one admissible split with tokens ≥ 20: (20,20) — measured
  separating. m=19 d=9 (kit-7) has co=38 and exactly one admissible
  split: (19,19) — kit-7's trio. The engine-free split arithmetic is
  full for the measured slices: every admissible co-token split of
  every measured birth slice has now been measured and separated.
- {19,20,20}@59 is OUTSIDE the kit-7 sweep cap (S ≤ m+38 = 57 at m=19):
  it is visible only through this kit's sweep-domain extension
  S ∈ {m..max(m+38, z+2)} (z=57 ⇒ cap 59), frozen in the docstring with
  the disclosure that the NEW birth seats S(d)=z+2 exceed m+38 from
  d=10 onward for m ∈ {19,20}.
- No stack at either birth slice conformed: every admissible stack seat
  measured at the d=10 slices separates as a mimic. The mid-ladder
  equistack arithmetic generalizes the observation family: at depth
  d=(m−1)/2 (odd) / d=m/2 (even) the birth S equals 3m and the
  admissible splits degenerate to the equistack {m,m,m}.

### TRIO-TRACKER outcomes (kit-7 log S5 item 10, NON-BINDING — both HIT as mimics)

- m=19 z=56: trio {19,19,19}@S=57 measured **UP 1v0** — the EXACT MIMIC
  of the birth seat's one-past {19,38}@57 UP 1v0 (the registered mimic
  candidate).
- m=19 z=57: trio {19,19,19}@S=57 measured **DOWN 1v2** — the EXACT
  MIMIC of the stick {19,38}@57 DOWN 1v2 (the registered mimic
  candidate).
- Lifecycle so far (machine observation): the trio seats at S=57 follow
  the S=57 seat-class slice by slice: birth 2v0 (kit-7 z=55), one-past
  1v0 (z=56), stick 1v2 (z=57). The trio has now tracked its host seat
  through the full birth→one-past→stick arc without deviation.

### TRIO MID-SLICE PROBES m=13@z=37 / m=15@z=43 / m=17@z=49 (kit-7 log S5 item 12)

Counter-probed 0-hit at this build, registered at the engine-free
derived mid-ladder birth slices z = z*(m)+2d with d=(m−1)/2
(z*(13)=25, z*(15)=29, z*(17)=33 ⇒ 37/43/49; see S6 item 2 for the
dated disclosure of the kit-7 log prose z values 42/48). All three
FIRST-EVER rows measured:

- Binding birth-template seats EXACT 3/3: stick {13,24}@37 DOWN 1v2 +
  NEW {13,26}@39 UP 2v0; stick {15,28}@43 DOWN 1v2 + NEW {15,30}@45 UP
  2v0; stick {17,32}@49 DOWN 1v2 + NEW {17,34}@51 UP 2v0.
- NON-BINDING trio mimic candidates HIT **3/3**: {13,13,13}@S=39,
  {15,15,15}@S=45, {17,17,17}@S=51, all UP 2v0 — exact numeric mimics
  of the NEW birth seats sharing their S=3m (the equistack splits of
  co-tokens 26/30/34).

The stacked-trio mid-ladder birth shadow now generalizes over every
measured odd m (13/15/17/19 + the kit-7 d=9 observation), with the even
analogue (20,20,20) measured at m=20 d=10.

### m=26 z=25 hole row (kit-7 log S5 item 11)

CLEAN: 14 shapes, 0 separations. The m=26 line is the series-second
FULLY SWEPT measured line, z ∈ {25..56}, after m=25. The kit-8 frozen
hollow-row conditional (future item 39) HELD.

### WINDOW SWEEPS m=29 z ∈ {49..56} / m=30 z ∈ {50..57} (kit-7 frozen section (d) items 29/30)

16 FIRST-EVER below-frontier rows, 154 shapes, 0 separations — ALL
CLEAN. The below-frontier bands of the newest odd/even pair begin
their measured history clean, matching the in-band-clean precedent
opened for m=27/m=28 by kit-7.

## S3. State after kit-8 (scaffolding bookkeeping, no claim)

- Ladder depths after kit-8: m=19/m=20 births through d=10 (the deepest
  measured yet, both COMPLETE through d=10); m=21/m=22 through d=6;
  m=23/m=24 through d=5; m=25/m=26 through d=4; m=27/m=28 through d=2;
  m=29/m=30 through d=1.
- Deaths witnessed this run (first datum for each): m=19/m=20 deaths of
  d=8; m=21/m=22 deaths of d=4; m=23/m=24 deaths of d=3; m=25/m=26
  deaths of d=2; m=29/m=30 deaths of d=0 (z=60/z=61, the first
  m=29/m=30 deaths). The m=27 z=56 / m=28 z=57 rows re-measured
  kit-7's own item-21/item-24 values exactly (redundancy disclosed in
  S6 item 3).
- Frontier: 19th/20th parity data taken (m=31/m=32 first contacts, both
  EXACT); scaffold 20/20 per-row observations (m=13..32).
- One-past d=0 decay counts: odd 34 (m ∈ {13..29}: the m=29 frontier
  decay 2→1 measured here, plus the redundant m=27 z=56 re-measure
  carrying the d=0 lifecycle terminus witness), even 33 (m ∈ {14..30}:
  the m=30 2→0 here, plus the redundant m=28 z=57 re-measure).
- Measured-line bookkeeping: m=26 z ∈ {25..56} COMPLETE (hole measured
  clean); m=25 z ∈ {25..55} stands from the chain. m=29/m=30 measured
  ranges now z ∈ {49..60} / {50..61}.
- Below-frontier bands: m=29 z{49..56} and m=30 z{50..57} opened clean.
- Mid-ladder: the odd mid-ladder birth slices are now measured for
  m = 13/15/17/19 and the even mid-ladder slice for m=20; every
  admissible stack seat at every measured birth slice has been measured
  and separated as an exact mimic (7 shadow separations at 6 birth
  slices, 0 conforming stacks).

## S4. Verification (all executed)

1. Pre-freeze derivation: `derive_kit8.py` — engine-free paper
   derivation of every registered literal from the K0832 closed form
   and the seat-lifecycle scaffold (z*(m)=2m−2+(m%2) per K1268; birth
   slice z=z*+2d, co-token m+2d+1 (odd)/m+2d (even), S=2m+2d+1 (odd) /
   2m+2d (even), one-past z=z*+2d+1, dead shape S=z−1, stick seat
   S=z, NEW birth S=z+2). 370 checks, 0 errors, run BEFORE the first
   row sweep. The regenerated prediction TEXT of all 28 binding rows
   byte-matches the kit-7 frozen section (d) constants. Also derived:
   the probe slices 37/43/49, the kit-9 future constants, and the
   1,004-triple battery union.
2. Pre-freeze anchor verification: `verify_new_anchors_kit8.py` — the
   39 kit-7 spots re-measured 39/39 on the published canonical engine,
   plus 141+39 anchor-table byte-fidelity and 39/39 transcription, all
   BEFORE any census row ran.
3. Frozen run: rc 0, ~42 s, stdout sha 5723304c…
   (`explore_m31m32_ladders_trio.out`).
4. Determinism: the published run plus FIVE build-time verification
   runs (default ×2, PYTHONHASHSEED=random, env -i isolated ×2) are all
   byte-identical, plus the push-time isolated-env rerun re-verified
   byte-identical (sha 5723304c…) immediately before the push — 7
   executions, one byte string.
5. Independent ordered-engine audit: `audit_kit8.py` re-executed every
   row with the ordered product instead of the canonical sweep dedup:
   48 rows, 763 shapes, 54 ordered-separations, 0 mismatches; anchors
   ordered 180/180; battery 1,004/1,004 closed==canonical==ordered;
   classification 26 FULL HIT + 2 DEVIATION reproduced independently.
   (The audit script's own pre-publication bugs are audit-tool-side
   only, disclosed in S6 item 4.)
6. Standard caveats: the K0832 closed form remains the only PROVED
   statement; every item above is a finite machine observation; the
   standard 11×11 cell remains UNKNOWN at all times; no K slot is
   claimed; no residual verdict is consumed.

## S5. Handoff: kit-9 registrations (34 binding rows + 2 frontier proposals frozen in the future section + log-level registrations)

Frozen in the kit-8 .out future section
(`future_slice_registration_constants`), verbatim-binding for the
next execution kit, all prediction literals engine-free derived and
derive-checked:

1. m=19 z=58 / z=59, m=20 z=59 / z=60 (one-past-of-d=10, birth d=11).
2. m=21 z=54 / z=55, m=22 z=55 / z=56 (one-past-of-d=6, birth d=7).
3. m=23 z=56 / z=57, m=24 z=57 / z=58 (one-past-of-d=5, birth d=6).
4. m=25 z=58 / z=59, m=26 z=59 / z=60 (one-past-of-d=4, birth d=5).
5. m=27 z=58 / z=59, m=28 z=59 / z=60 (one-past-of-d=2, birth d=3).
6. m=29 z=61 / z=62 / z=63 (birth d=2, one-past-of-d=2 / death-of-d=1,
   birth d=3), m=30 z=62 / z=63 / z=64 (same stages, m=30).
7. CONTINGENT m=31 z=62 / z=63 / z=64 (one-past of the d=0 first
   contact «decay 2→1», birth d=1, one-past-of-d=1 / death-of-d=0) —
   registered under the assumption the kit-8 first contact measured the
   19th parity datum (it did); m=32 z=63 / z=64 / z=65 (same stages).
8. m=33 z=65, m=34 z=66 (21st / 22nd frontier parity datum candidates,
   FIRST-EVER rows; z*(33)=65, z*(34)=66 double-derived per K1268).

Log-level registrations made by this kit's observations:

9. STACK-SHADOW registration rule (new, from the item-2/item-4
   deviations and the probe outcomes; engine-free arithmetic): at
   every birth slice the registered candidate must enumerate, beside
   the stick and NEW seats, EVERY admissible co-token-split stack
   {m,x,y} with x+y = co(d), x,y ≥ m, seating at the NEW seat's S, as
   explicit candidates (expected by the observation record: exact
   numeric mimic of the NEW seat; any deviation is the datum). The
   observed census this rule generalizes: 6 measured birth slices with
   admissible stacks, 7 shadow separations, all exact mimics
   ({19,19,19}@57 kit-7; {19,19,21}@59, {19,20,20}@59, {20,20,20}@60
   kit-8 d=10; the mid-ladder equistacks {13,13,13}@39, {15,15,15}@45,
   {17,17,17}@51 kit-8 probes), 0 conforming stacks. The domain is
   engine-free: admissible splits exist iff co(d) ≥ 2m, i.e. exactly at
   and beyond the mid-ladder depth d=(m−1)/2 (odd) / d=m/2 (even). For
   the kit-9 birth rows the enumeration is EMPTY at every depth below
   mid-ladder (co < 2m) and nonempty only for m=19/m=20 d=11 (co=42:
   splits (19,23),(20,22),(21,21) at m=19 — three candidates, the
   widest single-row stack registration yet; (20,22),(21,21) at m=20).
10. TRIO-TRACKER continuation (NON-BINDING, any outcome is the datum):
    track {19,19,19}@S=57 beside the binding m=19 z=58 / z=59 rows.
11. PROBE LIFECYCLE continuation (contingent, NON-BINDING): the probe
    trios measured UP 2v0, so register the m=13/15/17 trio lifecycle
    rows (one-past z=3m−1, stick z=3m, next birth z=3m+1) for those m.
12. WINDOW proposals below-frontier (register-before-measure at the
    next build): m=31 z ∈ {53..60}, m=32 z ∈ {54..61} (candidate 0
    separations each; neither m is strip-covered).
13. The hollow-row conditional (future item 39) is RESOLVED by this
    kit: the m=26 z=25 hole measured clean and the m=26 line is fully
    swept; no further conditional stands.

## S6. Honest record / caveats

1. The item-2 and item-4 DEVIATIONS are the kit series' 2nd and 3rd
   registered-candidate measurement deviations. The pre-declaration
   protocol did its job: the row-level templates "EXACTLY TWO" were
   falsified by observations the templates did not predict, while the
   named-seat scaffold itself survived 40/40. What the templates
   missed is the SHADOW seat class (co-token-split stacks at shared
   S), now codified as the S5 item-9 registration rule. No claim is
   upgraded or downgraded; the K0832 closed form is untouched (every
   shadow's collapse was computed by it and conformed to the
   measurement).
2. DATED DISCLOSURE: the kit-7 log S5 item 12 prose wrote the probe
   slices as m=15 z=42 and m=17 z=48. The engine-free derivation (and
   the kit-7 FROZEN .out constants, which the derive script matched
   byte-for-byte) give z = z*(m)+2d = 43 and 49 (the m=13 value 37
   matches). Kit-8 registered and measured at the derived slices
   37/43/49. Kit bytes are never edited; this is the dated correction
   of the kit-7 LOG PROSE only, no frozen constant is affected.
3. DATED DISCLOSURE (registration redundancy): the kit-7 log S5 item 6
   registered m=27 z=56 / m=28 z=57 (one-past-of-d=1 / death) as new
   rows, but those slices are exactly kit-7's own measured S2 items
   21/24 — a redundancy of the kit-7 future list, invisible to its
   build-time counter-probe because the candidates were its own.
   Kit-8 re-measured both; they agreed with the published values
   exactly. Kit-9's future list (S5 items 1–8 above) was checked
   against this kit's own measured rows before freezing: no such
   redundancy remains (every registered slice is either new depth or
   the contingent m=31/m=32 mini-ladder).
4. Pre-freeze build errors, caught and fixed BEFORE the freeze, all
   checker/assembler-side (the registration tables passed their first
   derivation and the frozen bytes were never edited after the first
   run): (a) `derive_kit8.py` depth-convention slips — the one-past
   rows take the slice's own d and the births the next d, initially
   written one-past-of-d as d+1 (the kit-6 lifecycle-shift lesson
   re-learned); (b) the explorer assembler emitted an unclosed
   triple-quote and a JSON `true` literal inside a docstring; (c) a
   docstring collapse typo v(57,56,76) written 1, corrected to 0
   (the frozen candidate text itself always carried 0); (d) two
   provenance-string slips; all fixed pre-freeze. (e) Post-run, the
   first draft of `audit_kit8.py` had parse bugs producing false
   mismatches; fixed before any publication claim — audit-tool-side
   only, disclosed here.
5. This kit measured 763 shapes across 48 rows and re-measured 180
   anchors without contradiction of any published datum, except the
   two row-level deviations, which contradict no prior observation
   and were invisible to every prior sweep (the m=19 z=57 / m=20 z=58
   birth slices had never been measured, and {19,20,20}@59 sits beyond
   every prior sweep cap).
6. SWEEP-DOMAIN DISCLOSURE: this kit's rows sweep S ∈ {m..max(m+38,
   z+2)}; the kit-7 cap m+38 stops covering the NEW birth seats
   S(d)=z+2 from d=10 onward. The extension is minimal (it adds only
   seats above the old cap up to the birth seat's S) and changes no
   published row: every re-measured kit-7-era row and anchor
   reproduced exactly, and the ordered-engine audit re-ran all 48
   rows at the extended domain with 0 mismatches.
7. No universal claim is made here. K0832 is the only PROVED
   statement. The 11×11 standard cell remains UNKNOWN at all times.
   No K slot is claimed. No residual verdict is consumed. The hourly
   lane may run concurrently; the push-time counter-probe and head
   record are in S4/the push commit body.
