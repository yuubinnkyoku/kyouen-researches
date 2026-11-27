# 2026-11-27 — z=24 min≥19 floor-19 (z−5, CRITICAL) pre-declaration census: ALL predeclared candidates FULL HIT (cell ladder 18/18, even form 6/6 graduates, K1328 m=13 band CLOSES at z=24)

Slot check (pre-claim, per registered handoffs): at kit-build time the
latest main (head `96dc2b08` at probe, kit published at wave A commit
`2f46b967`) contained NO T-Z24 declaration, NO z=24 floor-19 critical
census, and no `explore_z24f19` (code probes `explore_z24f19` / `T-Z24`
/ `z24-min19` → 0 kit hits; only handoff references in the published
z24-floor18 / m18spot / z25min20 / inband-completions kits). The
z25min20 kit's own counter-probe had additionally recorded "no z=24
floor-19 critical kit exists (`z24f19` → 0 hits)". The slot this kit
claims is the registered highest-information next target of the
published z=24 floor-18 census kit log §5 item 1 — the T-Z24 critical
lane material — which the m18spot and z25min20 kits explicitly did NOT
take.

## §1 Context and kit role

The floor-(z−5) CRITICAL census series builds the per-z cell ladder one
step AT the critical floor, pre-surveying exactly the material a future
T-Z24 declaration lane consumes: the 18-rung floor-19 cell census, the
tail spots, the strip would-be claim positions, the in-band row records
(base child + residual bands), the base spot, the below-band child
shape set, and the K1345-corollary supply battery. Editions of the
series: z=22 (`115c0bb9`), z=23 (`25522d56`), z=25 (floor-20, published
out of order by the z25min20 kit) — this edition (z=24, floor-19) fills
the gap the declaration chain actually needs next, since T-Z24's
C-hand children land on the PROVED K1344 floor-18 cells (co-floor
18 ⊆ 19 subset argument) and its j=18 base-child C-hand lands on the
PROVED T-Z23 m=18-row claim position itself.

## §2 Kit construction and discipline (executed before the first run)

- Base file: the published `research/experiments/strip-z23-min18-20261125/explore_z23f18.py`
  (sha `eddd5e90…`) — parameter diff ONLY, per the series discipline:
  slice z 23→24, cell budget j+24→j+25, floor 18→19, rungs 17→18 with
  the provisional 18th-rank label `A12`, s domain {0}∪{19..49}, tail
  spots {50..57}, strip m∈{19..23}, row records m=18..13, base spot
  m=19, below-band H(25;Y;25), section (g) reduced to the prescribed
  K1345-corollary battery (per the published K1345 log §5 handoff item
  2 — NO new tail pre-computation; the k=27..32 chain is already
  published by the z23-floor17 / z24-floor18 / m18spot / tail22 kits).
- Engine: embedded block byte-identical to the K1282..K1345 chain
  (`engine_block.py` sha256 `582c93c1…`, startup pin `bd5f22e4…`
  asserted in-file, engine_gate PASS in the frozen output).
- Predeclared candidates: written in the frozen docstring BEFORE the
  first run. Primary derivation: the PROVED z=22 K1339 cell profile
  shifted +2 (consecutive-even structural identity chain), with the
  z=23 odd-form s=18 triplet EXCLUDED below the floor-19 domain
  (third odd→even oldest-station death / sixth definition-domain
  exclusion event) and NO newborn at s=19 (A-break position z−5=19 is
  an odd s at even z). The published z24-floor18 kit's measured
  11-entry lattice at {18,20,22,24} is a DISCLOSED consistency anchor,
  NOT a premise (the s-only premise is itself a candidate here: this
  kit's shape set at floor-19 differs from the floor-18 shapes for
  every s).
- No drafting scratch engine check was needed: every predeclared
  constant is either a PROVED z=22+2 value or a published measured
  constant; no file edited after any run.
- Freeze: `explore_z24f19.py` sha256
  `fb95f5a82a13ee0ea1c1e0973f5207403e5f239b69be41b177d99f6458cf57dd`
  (30,675 bytes). Publish-then-execute: wave A (kit + README +
  engine_block) pushed as commit `2f46b967` BEFORE the first run of
  the frozen file.
- Determinism: SIX runs, all byte-identical (frozen stdout sha256
  `713ea3e2bc00e97549bd9a1aef2d3d223aa2b5c94ce542532dda8609ac681758`,
  24,807 bytes): default run, its exact duplicate,
  `PYTHONHASHSEED=random` same-cwd, `PYTHONHASHSEED=1` same-cwd, and
  two `env -i` clean runs in fresh scratch dirs (one with
  `PYTHONHASHSEED=1`), /usr/local/bin/python3 all, rc 0, ~30 s each.

## §3 Results (finite observations) — ALL predeclared candidates HIT

Full frozen data in `explore_z24f19.out`. Headlines:

1. Cell ladder 18/18 at floor-19, z=24 — deviant position set
   {20,22,24} EXACTLY as predeclared, value-exact against BOTH the
   proved z=22+2 profile and the published z24-floor18 lattice:
   F24f19 {24: UP 1v0} (single@(even z), no hole, no tail — the
   single/hole+tail typology alternation reaches TEN consecutive
   consistent slices z15..z24, even-z single form 6/6);
   G24f19 {22: DOWN 0v2, 24: UP 2v1}; E24f19 {22: UP 1v0};
   D24f19 {20: DOWN 0v2, 22: UP 2v1}; C24f19 {20: UP 1v0};
   B24f19 {20: UP 2v1}; A..A12 (12 rungs) FULLY COLLAPSED — the
   A-break extinction at even z graduates to 6/6 (z=14/16/18/20/22/24;
   the z=23 A-rank rebirth class at s=18 falls below the floor-19
   domain, the THIRD odd→even oldest-station death after z=19→20 s=14
   and z=21→22 s=16); head row s=19 ALL-CONFORMING; station structure
   {D,C,B}@20 and {G,E,D}@22 both the even-form triplet
   {DOWN 0v2, UP 1v0, UP 2v1} (the parity mirror of the z=23 odd
   triplet), lattice head {F,G}@24 = {UP 1v0, UP 2v1}; multivalue
   rows 0 over all 18 cells (the s-only premise holds on every
   measured row).
2. Tail spots {50..57}: 144/144 ALL MATCH (even signature; the z=23
   odd-form 8/8 F value-2 tail signature absent, as predeclared).
3. Strip m∈{19..23} at R=m+25 (T-Z24 would-be claim positions):
   97 shapes 0 violations, per-m deltas 23/20/19/18/17 — cross-artifact
   identical to the published z24-floor18 strip segments.
4. Row records: m=18-row z=24 (R=43) 26/0 + arity≤4 ext 25/0 — the
   FIRST entry of the K1344-registered T-Z23 residual band m=18
   z∈{24..33} AND the T-Z24 base m=19 a=19 child (TENTH consecutive
   in-band base child); m=17 32/0 (T-Z22 band third entry);
   m=16 40/0 (fourth); m=15 50/0 (fifth, K1335 band); m=14 62/0
   (sixth, K1330 band); m=13 76/0 (SIXTH AND FINAL, K1328 band
   m=13 z∈{19..24} — the band CLOSES at z=24, the
   closest-to-frontier row record of the series: z*(13)=25 > 24 by one
   point). All cross-artifact identical to the published z24-floor18
   entries; every separation list empty.
5. Strip spots m∈{24..27}: 12/12 match (recheck of the published 12/12).
6. Base spots: the m=19 base spot H(44;(19,19);24)=0 CONFORMING
   (= v(38,24,44)=0) — the NINTH base-spot z-parity point
   (0,1,0,1,0,1,0,1,0), never measured before; the published-anchor
   recheck H(43;(18,18);24)=1 reproduced exactly (the z24-floor18 kit's
   m=18-row spot, the §5-item-3 alternation-anomaly point).
7. Below-band child census H(25;Y;25) at the FLOOR-19 shape set
   (Y tokens ≥ 19, 74 shapes — a different shape set from the published
   floor-18 version 89/0): 74/74 full collapse, 0 multivalue — the
   TENTH consecutive below-band full collapse; the collapse proof
   belongs to the declaration lane (BB-lemma stair R=25 ≤ 25+min(Y)).
8. Supply battery (engine-free, K0832): FIFTEENTH tail
   v(s,25,25)=v(s,24,25) holds on {0}∪{12..23}, 0v2 at s=24, uniform
   2v1 for all s∈{25..61}; SIXTEENTH tail v(s,26,26)=v(s,25,26) holds
   on {0}∪{12..25}, uniform 0v1 for all s∈{26..61} — both exactly as
   anchored, now battery spot-checks of the identities PROVED
   universal by the published K1345 d-shift theorem (d=1 slice).

## §5 Handoff

1. **T-Z24 declaration lane**: every supply-side input the paper proof
   needs is now PROVED or measured — the C-hand children of rungs
   j=1..17 land on the PROVED K1344 floor-18 cells, the j=18 C-hand
   child (42;{18}∪Y;23) is the PROVED T-Z23 m=18-row claim position,
   the j=1 B-hand below-band child collapses at H(25;Y;25) (this kit's
   section (f)) with the FIFTEENTH-tail identity (PROVED universal by
   K1345), and the cell ladder constants are frozen here
   value-exact. The z=24 head trio for the future z=25 floor-19 kit's
   head derivation still needs the z=24 floor-18 lattice PROVED (i.e.
   the T-Z24 chain extension first) — unchanged from the published
   z24f18 §5 assessment.
2. The even-form A-break extinction is now a 6/6 finite pattern
   (z=14..24 even) and the station-triplet parity-mirror rule is 5/5
   even slices; both remain finite observations (no universal claim).
3. The K1328 m=13 residual band is the second band to CLOSE at z=24;
   the m=14 (K1330) and m=15 (K1335) bands close at z=25/28 per their
   registered ranges — the z=25 and z=28 row-record entries are the
   natural next band-completion measurements (already scheduled by the
   published frontier-lifecycle / inband-completions lanes).
4. 11×11: no action. Standard 11×11 empty board, 19 central-reply
   roots, two-stone root {60,27}, third moves {100,108}, S2, class
   1/2/4 and all closure classes remain UNKNOWN; no verdict consumed;
   no board-level claim made.

## §6 Caveats

Finite machine observations only; no K slot claimed (promotion is a
separate integrator step); the predeclared candidates were derived
from PROVED z=22 constants and published measured z24-floor18
constants (the latter disclosed as anchor, not premise); the s-only
cell premise is confirmed on every measured row but is a census
observation, not a theorem; raw engine pinned at `bd5f22e4…`
(engine_gate PASS in the frozen output); nodes are bookkeeping.
