# m=33/m=34 frontier first contacts + m=19..m=32 ladder continuation + m13/15/17 probe lifecycles + even-mid trio probes + m=31/m=32 window sweeps pre-declaration micro-kit (kit-9)

- kit id: kit-9 (hourly lane, session 2026-11-26, ~11:56Z build)
- runclass: publish-then-execute pre-declaration census, frozen before the
  literal push; candidate-vs-measured committee by machine observation only
- commit base: 7af915fb (kit-8 publish-priority census); main head at build
  332ce273 (part-sm wave B, no kit-9 territory touched; counter-probe at
  build: 12 code-collision queries over the kit-9 territory, 0 hits). At
  push time the head had advanced to 44d8d90b (the parallel part-sm /
  parked4rest2 lanes' 11:44-12:01Z commits), none of which touches this
  kit's territory: the push-time counter-probe re-ran and returned 0
  kit-9-territory hits and both target paths (this experiment directory
  and this log) do not exist on main.
- files:
  `research/experiments/strip-newband-m33m34-frontier-ladders-20261126/{engine_block.py, explore_m33m34_frontier_ladders.py, explore_m33m34_frontier_ladders.out, derive_kit9.py, verify_new_anchors_kit9.py, audit_kit9.py, README.md}`
- engine: published chain clone, sha 582c93c1..., startup pin bd5f22e4... (PASS)
- explorer sha256: `d38af1b6e48708e643cd73c4ea9a3a85e2c3830fcb0ce3d1bd88227948d154a5` (127,224 bytes)
- frozen output sha256: `eb0c0c146c3d16090a604377a1aafc50bd56faee48a81cbdfa6d995df7db7a3f` (201,566 bytes)
- status: EXECUTED, VERIFIED, PUSHED (run rc 0, ~78 s; see S4)

## S1. Anchor re-verification (234/234)

The kit-8-era 180 chain anchors verbatim, plus the 54 kit-8 separation
spots FIRST re-anchored here. The 54 spots were machine-extracted from
the published kit-8 frozen .out and derive-checked against its
published values BEFORE the frozen census (independent pre-freeze
script `verify_new_anchors_kit9.py`, canonical engine, published spots
only): 54/54 canonical re-measurement, anchor-table byte-fidelity 180
inherited + exactly 54 new, transcription 54/54, and 54/54 agreement
with the second-census kit (680421eb/e9847712) values. In the frozen
run every anchor re-executed and hit exactly (234/234 match, R-first
convention asserted). Battery 1,454/1,454 all-match (K0832
closed-form vs canonical vs ordered, the cumulative kit-era union
including every registration literal used or emitted by this kit). No
prior datum lost; cumulative anchor count 234.

## S2. Registered vs measured (30/34 FULL HIT + 4 DEVIATIONS -- the 4th through 7th registered-candidate deviations of the kit series; all four the SAME shadow class)

34 binding rows executed (kit-8 frozen future constants items 1-34;
1,230 total shapes and 100 total separations across all 62 rows of
this kit):

| row | registered candidate (binding) | verdict | measured |
|----|----|----|----|
| m=19 z=58 (item 1) | EXACTLY ONE {19,40}@S=59 UP 1v0; {19,38} dead; death-of-d=9 | **DEVIATION** | the named seat HIT, plus TWO UNREGISTERED separating stack shadows {19,19,21}@59 and {19,20,20}@59, both UP 1v0 -- exact numeric mimics of the one-past seat {19,40} they share S=59 with (co=40 splits (19,21),(20,20), the full split enumeration) |
| m=19 z=59 (item 2) | EXACTLY TWO: stick {19,40} DOWN 1v2 + NEW {19,42}@S=61 UP 2v0 (d=11 birth, gap 23) + 3 registered NEW-seat co=42 split stacks | **DEVIATION** | every named seat and all 3 registered stacks HIT exactly ({19,19,23},{19,20,22},{19,21,21}@61 all UP 2v0 exact mimics), plus TWO UNREGISTERED stick-seat shadows {19,19,21},{19,20,20}@59 DOWN 1v2 (co=40 splits, exact mimics of the stick); m=19 ladder COMPLETE through d=11 -- the DEEPEST measured birth of the series |
| m=20 z=59 (item 3) | EXACTLY ONE (20,40)@S=60 DOWN 0v1; (20,38) dead; death-of-d=9 | **DEVIATION** | the named seat HIT, plus ONE UNREGISTERED shadow (20,20,20)@60 DOWN 0v1 -- exact mimic of the one-past seat (co=40 split (20,20), the full enumeration) |
| m=20 z=60 (item 4) | EXACTLY TWO: stick (20,40) DOWN 0v2 + NEW (20,42)@S=62 UP 2v1 (d=11, gap 22) + 2 registered NEW-seat co=42 split stacks | **DEVIATION** | every named seat and both registered stacks HIT exactly, plus ONE UNREGISTERED stick-seat shadow (20,20,20)@60 DOWN 0v2 (exact mimic of the stick); m=20 ladder COMPLETE through d=11 |
| m=21 z=54 / z=55 (items 5-6) | one-past-of-d=6 / birth d=7 | HIT (FULL) | as registered (first m=21 d=7 birth, gap 15) |
| m=22 z=55 / z=56 (items 7-8) | one-past-of-d=6 / birth d=7 | HIT (FULL) | as registered (co=34: no admissible split, no shadows -- consistent) |
| m=23 z=56 / z=57 (items 9-10) | one-past-of-d=5 / birth d=6 | HIT (FULL) | as registered |
| m=24 z=57 / z=58 (items 11-12) | one-past-of-d=5 / birth d=6 | HIT (FULL) | as registered |
| m=25 z=58 / z=59 (items 13-14) | one-past-of-d=4 / birth d=5 | HIT (FULL) | as registered |
| m=26 z=59 / z=60 (items 15-16) | one-past-of-d=4 / birth d=5 | HIT (FULL) | as registered |
| m=27 z=58 / z=59 (items 17-18) | one-past-of-d=2 / birth d=3 | HIT (FULL) | as registered (m=27 through d=3) |
| m=28 z=59 / z=60 (items 19-20) | one-past-of-d=2 / birth d=3 | HIT (FULL) | as registered (m=28 through d=3) |
| m=29 z=61 (item 21) | birth d=2: stick {29,32} DOWN 1v2 + NEW {29,34}@S=63 UP 2v0 | HIT (FULL) | as registered |
| m=29 z=62 (item 22) | one-past {29,34}@S=63 UP 1v0; death-of-d=1 | HIT (FULL) | as registered |
| m=29 z=63 (item 23) | birth d=3: stick {29,34} DOWN 1v2 + NEW {29,36}@S=65 UP 2v0 | HIT (FULL) | as registered (m=29 through d=3) |
| m=30 z=62 / z=63 / z=64 (items 24-26) | birth d=2 / one-past / birth d=3 | HIT (FULL) | as registered (m=30 through d=3) |
| m=31 z=62 (item 27, CONTINGENT) | one-past {31,32}@S=63 UP 1v0 (frontier decay 2->1) | HIT (FULL) | as registered; the kit-8 contingency resolved |
| m=31 z=63 (item 28, CONTINGENT) | birth d=1: stick {31,32} DOWN 1v2 + NEW {31,34}@S=65 UP 2v0 | HIT (FULL) | as registered; the first measured m=31 rows beyond the kit-8 first contact |
| m=31 z=64 (item 29, CONTINGENT) | one-past {31,34}@S=65 UP 1v0; {31,32} dead; death-of-d=0 | HIT (FULL) | as registered |
| m=32 z=63 / z=64 / z=65 (items 30-32, CONTINGENT) | one-past (frontier decay 2->0) / birth d=1 / one-past-of-d=1 | HIT (FULL) | as registered; m=32 mini-ladder COMPLETE |
| m=33 z=65 (item 33) | EXACTLY ONE {33,34}@S=67 UP 2v0 (collapse v(67,65,99)=0); z*(33)=65 per K1268 (derive_check double-checked), R=99 | HIT (FULL) | FIRST-EVER m=33 row; 21st parity datum EXACT |
| m=34 z=66 (item 34) | EXACTLY ONE (34,34)@S=68 UP 2v1 (collapse v(68,66,101)=1); z*(34)=66 per K1268 (derive_check double-checked), R=101 | HIT (FULL) | FIRST-EVER m=34 row; 22nd parity datum EXACT |

The named-seat scaffold survived 68/68 pair-seat hits across the 34
rows; the frontier parity scaffold now stands 22/22 per-row
observations (m=13..34).

### The items 1-4 deviations: the CO-SPLIT SHADOW rule generalizes beyond birth slices

Kit-8 codified (log S5 item-9) that at every BIRTH slice the
registration must enumerate the co-token-split stacks of the NEW seat.
Kit-9's registration followed that rule exactly (the co=42 split
stacks at m=19/m=20 were all registered and all HIT). The four
deviations are the rule's discovered TERRITORY GAP: the stick and
one-past seats {m,co=40} ALSO carry their admissible co-splits as
separating exact mimics at their own S (both at the one-past slice
AND at the stick slice). Facts established by these rows (all machine
observation):

- All six unregistered shapes (2+2+1+1) are exact numeric mimics of
  the 2-token seat they share S with: same S, same value, same
  collapse, same direction.
- COMPLETE enumeration: co=40 has exactly two admissible splits with
  tokens >= 19 ((19,21),(20,20)) and exactly one with tokens >= 20
  ((20,20)) -- every admissible split of every measured seat measured
  and separated; no conforming stack.
- RULE v2 (the registration rule generalization adopted at this log,
  engine-free): at EVERY slice, EVERY separating 2-token seat {m,co}
  carries, at the same S, every admissible co-split stack {m,x,y}
  (x+y=co, x,y >= m) as an exact numeric mimic (same value, same
  collapse, same direction); no 3-token separation occurs except as
  such a mimic. The audit machine-verified BOTH directions of rule v2
  across ALL 62 rows of this kit: every one of the 32 3-token
  separations is an exact mimic-split of a 2-token seat at the same
  S, and every admissible split of every one of the 68 pair seats is
  present -- 0 anomalies. (Finite verification over the rows of this
  kit; NOT a proved theorem.)
- Consequence: the kit-10 future registrations below are frozen per
  rule v2 (both the stick and the NEW seat split enumerations).

### TRIO-TRACKER outcome (m=19 z=58 / z=59, NON-BINDING)

- m=19 z=58: trio {19,19,19}@S=57 measured **CONFORM** (value =
  collapse, the GLIDE-DEAD expectation as registered: the S=57
  family's dead-shape collapse), and z=59: CONFORM again. The m=19
  trio lifecycle is COMPLETE end-to-end: birth 2v0 UP (kit-7 z=55),
  one-past 1v0 UP (kit-8 z=56, the exact mimic), stick 1v2 DOWN
  (kit-8 z=57, the exact mimic), glide-death CONFORM (kit-9 z=58/59).
  The L8 family-tracking observation bank gains its cleanest terminal
  witness: the trio dies WITH its host family, exactly as the
  one-past/stick mimics lived with it.
- m=20's own trio {20,20,20}@S=60 by contrast LIVES through this kit
  as the stick/one-past seat shadows (items 3-4 above): the host
  family {20,40}@S=60 has not died, so the mimic has not either. The
  two trios' divergent fates are both pure rule-v2 consequences
  (shadow follows host); the host is the only free variable.

### m=13/15/17 PROBE LIFECYCLES (9 rows, NON-BINDING scaffold; kit-8 log S5 item-11 continuation)

All 9 rows measured; the registered seats HIT 9/9 (stick + NEW birth
at the z=3m slices, one-past at z=3m-1 and z=3m+1):

- z=3m-1: one-past seat {m,2m}@S=3m UP 1v0 and the trio {m,m,m} UP
  1v0, its EXACT MIMIC (co=2m splits to (m,m) -- the trio IS the
  one-past seat's only admissible split). 3/3.
- z=3m: stick DOWN 1v2 (trio DOWN 1v2 mimic) + NEW birth seat
  {m,2m+2}@S=3m+2 UP 2v0 with BOTH registered co=2m+2 split stacks
  UP 2v0 exact mimics ({m,m,m+2},{m,m+1,m+1}). 6/6.
- z=3m+1: one-past of the NEW seat UP 1v0 with both split stacks UP
  1v0 exact mimics; the z=3m family's trio CONFORMS. 6/6.

The odd-m trio glide template (birth -> one-past -> stick -> death)
now has measured terminal rows at m=13/15/17 superposed on the
matching seat-class rows, and the kit-8 probe finding (UP 2v0 trio
equistacks) resolves into its lifecycle position: the mid-ladder
equistack is simply the birth-slice split of the co=2m NEW seat.

### EVEN-MID-SLICE PROBES m=14@z=40 / m=16@z=46 / m=18@z=52 (kit-8 log S5 second-census proposal)

Counter-probed 0-hit at this build; all three FIRST-EVER rows
measured at the engine-free even mid-ladder slices z=3m-2:

- Binding birth-template seats EXACT 3/3: stick {14,26}@40 /
  {16,30}@46 / {18,34}@52 DOWN 0v2 + NEW {14,28}@42 / {16,32}@48 /
  {18,36}@54 UP 2v1.
- The trio exact-mimic candidates HIT 3/3: {14,14,14}@S=42,
  {16,16,16}@S=48, {18,18,18}@S=54, all UP 2v1 -- exact numeric mimics
  of the NEW birth seats sharing their S (=3m; the equistack splits
  of co-tokens 28/32/36). The even-mid trio-shadow observation now
  covers m = 14/16/18/20 (the m=20 precedent generalized by this
  kit's three new firsts).
- No other separation at any of the three slices (full split
  enumerations are the single equistacks -- consistent with rule v2).

### WINDOW SWEEPS m=31 z in {53..60} / m=32 z in {54..61} (kit-8 log S5 item-12)

16 FIRST-EVER below-frontier rows, 136 shapes, 0 separations -- ALL
CLEAN. The below-frontier bands of m=31/m=32 begin their measured
history clean, matching the in-band-clean precedent (m=27/m=28
kit-7, m=29/m=30 kit-8). Measured-band bookkeeping after this kit:
m=31 z in {53..64} COVERED (the 8 window rows here + the kit-8 first
contact z=61 + the kit-9 contingent mini-ladder z=62/63/64); m=32
z in {54..65} COVERED (8+1+3, same decomposition). z in {25..52} /
{26..53} below those bands remains unmeasured and unregistered.

## S3. State after kit-9 (scaffolding bookkeeping, no claim)

- Ladder depths after kit-9: m=19/m=20 births through d=11 (the
  deepest measured yet, both COMPLETE through d=11, gaps 23/22);
  m=21/m=22 through d=7; m=23/m=24 through d=6; m=25/m=26 through
  d=5; m=27/m=28 through d=3; m=29/m=30 through d=3; m=31/m=32
  through d=1 (mini-ladders COMPLETE; the kit-8 CONTINGENT resolved).
- Deaths witnessed this run (first datum for each pair): m=19/m=20
  deaths of d=9; m=21/m=22 deaths of d=6; m=23/m=24 deaths of d=5;
  m=25/m=26 deaths of d=4; m=27/m=28 deaths of d=2; m=29/m=30
  deaths of d=1; m=31 deaths of d=0 (z=64); m=32 deaths of d=0
  (z=65).
- Frontier: 21st/22nd parity data taken (m=33/m=34 first contacts,
  both EXACT); scaffold 22/22 per-row observations (m=13..34).
- One-past d=0 decay counts: odd 35 (m in {13..31}), even 34
  (m in {14..32}), the two contingent decays measured here.
- Shadow census after kit-9: 32 three-token separations measured in
  this kit, ALL exact mimics under rule v2 (audit-verified 0
  anomalies); cumulative across kits 7 birth slices + 2 stick + 2
  one-past + 3 lifecycle-template + 3 even-mid + the m=19/m=20 d=11
  families -- 0 conforming stacks ever measured, 0 non-mimic shadows.
- Trio ledger: m=19 trio CLOSED-DEAD (glide-dead CONFIRMED); m=20
  trio LIVE (MIMIC following its living host, measured at z=59/60
  0v1/0v2 DOWN); m=13/15/17 trios in-mimic through their probe
  lifecycles (z=3m-1/3m terminals CONFORM); m=14/16/18 equistack
  trios measured UP 2v1 birth mimics (their lifecycle terminal rows
  are the kit-10 registrations below).

## S4. Verification (all executed)

1. Pre-freeze derivation: `derive_kit9.py` -- engine-free paper
   derivation of every registered literal (579 checks, 0 errors, run
   BEFORE the first row sweep; the regenerated prediction TEXT of all
   34 binding rows byte-matches the kit-8 frozen future constants).
2. Pre-freeze anchor verification: `verify_new_anchors_kit9.py` -- the
   54 kit-8 spots re-measured 54/54 canonical, 180+54 anchor-table
   byte-fidelity, 54/54 transcription, 54/54 second-census agreement,
   BEFORE any census row ran (ALL PASS).
3. Frozen run: rc 0, ~78 s, stdout sha eb0c0c14....
4. Determinism: the published run plus FIVE build-time verification
   runs (default x2, PYTHONHASHSEED=random, env -i isolated x2) are
   all byte-identical, plus the push-time isolated-env rerun
   re-verified byte-identical (sha eb0c0c14...) immediately before the
   push -- 7 executions, one byte string.
5. Independent ordered-engine audit: `audit_kit9.py` re-executed every
   row with the ordered product instead of the canonical sweep: 62
   rows, 1,230 shapes, 100 ordered-separations, 0 mismatches; anchors
   ordered 234/234; battery 1,454/1,454 closed==canonical==ordered;
   classification reproduced independently (30 FULL HIT + 4
   HIT-with-unregistered-shadow rows; the 6 unregistered shadows all
   confirmed exact mimics); lifecycle 9/9, probes 3/3, windows 16/16
   clean, trackers 2/2 conform reproduced; rule-v2 split check 0
   anomalies over 68 pair seats and 32 shadows.
6. Standard caveats: the K0832 closed form remains the only PROVED
   statement; every item above is a finite machine observation; the
   standard 11x11 cell remains UNKNOWN at all times; no K slot is
   claimed; no residual verdict is consumed.

## S5. Handoff: kit-10 registrations (36 binding rows frozen in the future section + rule-v2 amendment + log-level registrations)

Frozen in the kit-9 .out future section
(`future_slice_registration_constants`), verbatim-binding for the
next execution kit, all prediction literals engine-free derived and
derive-checked:

1. m=19 z=60 / z=61, m=20 z=61 / z=62 (one-past-of-d=11, birth d=12,
   co=44: the widest single-row split enumerations yet -- per RULE V2
   each birth row registers the stick-seat co=42 splits ALSO: m=19
   stick {19,42}@S=61 shadows {19,19,23},{19,20,22},{19,21,21}; NEW
   {19,44}@S=63 shadows {19,19,25},{19,20,24},{19,21,23},{19,22,22};
   m=20 stick (20,42)@S=62 shadows {20,20,22},{20,21,21}; NEW
   (20,44)@S=64 shadows {20,20,24},{20,21,23},{20,22,22}; the one-past
   rows register the co=42 shadows at z=60/61 similarly).
2. m=21/m=22 z=56/57, m=23/m=24 z=57/58, m=25/m=26 z=58/59+59/60,
   m=27/m=28 z=60/61 (one-past/birth of d small; split enumerations
   EMPTY below mid-ladder by the admissibility arithmetic co>=2m).
3. m=29 z=65 / z=66 / z=67 (birth d=3 stick, one-past, birth d=4),
   m=30 z=66 / z=67 / z=68 (same stages).
4. m=31 z=65 / z=66 (birth d=2 at z=65, one-past-of-d=2 at z=66),
   m=32 z=66 / z=67 (same stages). NOTE (dated): the frozen future
   section ALSO re-lists m=31 z=64 / m=32 z=65, byte-similar to kit-9
   items 29/32 JUST MEASURED here -- a registration redundancy of the
   kit-8-era future list (the kit-7 S5 item-6 precedent), disclosed in
   S6 item 3; kit-10 either skips or re-measures both (contract
   re-measure, agreement expected).
5. FRONTIER: m=35@z=69 EXACTLY ONE {35,36}@S=71 UP 2v0 (23rd parity
   datum candidate, FIRST-EVER m=35 row; z*(35)=69 per K1268,
   double-derived), m=36@z=70 EXACTLY ONE (36,36)@S=72 UP 2v1 (24th;
   z*(36)=70 per K1268, double-derived).
6. WINDOW proposals below-frontier (register-before-measure): m=33
   z in {57..64}, m=34 z in {58..65} (candidate 0 separations each;
   NEITHER m is strip-covered).

Log-level registrations made by this kit's observations:

7. RULE V2 AMENDMENT (supersedes the kit-8 S5 item-9 registration
   rule's scope; engine-free): every future registration enumerates
   the admissible co-split stacks of EVERY separating 2-token seat of
   the row (stick, one-past, NEW, decay alike), not of the NEW seat
   alone; observed census 32/32 shadows in this kit consistent, 0
   anomalies in the audit's both-directions machine check.
8. EVEN-M probe continuation (NON-BINDING): the m=14/16/18 mid-slice
   probes measured their equistacks as exact mimics (UP 2v1), so the
   m=13/15/17-style next-depth stack splits and the even-m lifecycle
   rows (one-past z=3m-1 analogues, where parity shifts the seat
   template by one slice) become registrable at the next build.
9. TRIO-TRACKER closure: the m=19 trio ledger is CLOSED (glide-dead
   witnessed); no further m=19 trio rows are registered. The m=20
   trio remains a LIVE host-follower (no separate registration
   needed: it is the co=40 split shadow of a binding seat).

## S6. Honest record / caveats

1. The items 1-4 DEVIATIONS are the kit series' 4th-7th
   registered-candidate measurement deviations, all of the SAME
   co-split-shadow class as kit-8's items 2/4 (which are now
   subsumed: kit-8's birth-slice shadows were the same rule at the
   NEW seats). The pre-declaration protocol again did its job: the
   row-level templates were falsified by observations the templates
   did not predict, while the named-seat scaffold survived 68/68 and
   the rule bank grew (rule v2). No claim is upgraded or downgraded;
   K0832 is untouched.
2. DATED DISCLOSURE (kit-8 future constants, not this kit's bytes):
   the kit-8 frozen handoff prose listed the m=19/m=20 one-past rows
   at z=58/59 with dead-seat d=9 collapse literals that this kit's
   derive re-checked and measured consistent; no constant changed.
3. DATED DISCLOSURE (registration redundancy): the kit-8 S5 handoff
   (and hence this kit's embedded future section) re-lists m=31 z=64
   / m=32 z=65 -- slices that ARE kit-9's own items 29/32, measured
   here (both HIT). The pre-build counter-probe cannot see this
   (the future constants were the registration source itself).
   Kit-10 skips or contract re-measures both rows; no datum is
   affected. (Same class as the kit-7 S5 item-6 redundancy disclosed
   by kit-8.)
4. Pre-freeze/pre-push build errors, caught and fixed BEFORE the
   freeze or before the push (the frozen bytes were never edited
   after the first successful run): (a) the explorer assembler's
   first build omitted the trailing commas of the 54 new anchor
   lines (a SyntaxWarning-class tuple-call proximity bug, caught by
   the AST parse before any run); (b) the independent audit script's
   first draft had a seat-format parser gap (stick-format candidates
   carry no inline @S) and a tuple-normalization slip in the split
   enumeration check, both fixed before any publication claim --
   audit-tool-side only, disclosed here.
5. The m=19 z=59 / m=20 z=60 rows measure stack shadows at S values
   beyond the old kit-7 sweep cap (S<=m+38); the sweep-domain
   extension S in {m..max(m+38, z+2)} (kit-8 precedent) covers them
   and was frozen in the docstring before the run.
6. This kit measured 1,230 shapes across 62 rows and re-measured 234
   anchors without contradiction of any published datum, except the
   four row-level deviations, which contradict no prior observation
   and were invisible to every prior sweep (the m=19/m=20 z=58..60
   slices had never been measured).
7. No universal claim is made here. K0832 is the only PROVED
   statement. The 11x11 standard cell remains UNKNOWN at all times.
   No K slot is claimed. No residual verdict is consumed. The hourly
   lane may run concurrently; the push-time counter-probe and head
   record are in S4/the push commit body.
