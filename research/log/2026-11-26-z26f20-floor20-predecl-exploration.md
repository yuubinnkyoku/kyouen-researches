# 2026-11-26 — z=26 floor-20 (z−6, SUB-CRITICAL, EVEN) pre-declaration census: derived head row 20/20 value-exact (even chain 6/6), 11-entry lattice registered table value-exact (+2-shift identity 11/11 vs z24f18), m=14 FRONTIER exactly-one separation {14,14}@S=28 UP 2v1 (PARITY datum: the naive frontier-law formulation refuted, the K1268-aligned parity formulation confirmed), m=13 ONE-PAST-FRONTIER value drop 2→1, 25th-tail (k=34) even form 8/8 candidate CONFIRMED, four first-ever z=27 touches all conform

Slot check (pre-claim, per registered handoffs): at kit-build time
the latest main (head `ec7acda6`, 2026-11-26T04:22:47Z Part EM
completion, re-verified again before the push) contained NO z=26
census kit (`filename:explore_z26` → 0 hits, `z26f20` → 0 hits, the
kit path nonexistent), NO T-Z26 declaration, and the only published
z=26 engine values were the four z25f20 handoff spots h1..h4. The
slot this kit claims is therefore the registered pre-declaration
lane: the z=26 floor-20 (z−6) EVEN sub-critical census, executing
the z25f20 kit log S5 item #1 (the z=26 kit itself, incl. the
m=14-row NO-CANDIDATE frontier record), S5 item #4 (the k=34
pre-computation), and the z=27-touch blind-table registration —
leaving the T-Z24/T-Z25/T-Z26 proof lanes untouched.

## §1 Context and kit role

The floor-(z−6) sub-critical census series builds the per-z cell
ladder (F,G,E,D,C,B,A,A2..) one step BELOW the next critical slice,
pre-surveying exactly the material a future T-Z26 declaration lane
consumes: strip segments m ∈ {21..26} (would-be claim positions,
plus the even-chain m=20 floor segment), the in-band row records
(m=18 T-Z24-band second entry through the m=14 AT-FRONTIER record),
base and spot tables, the below-band child slice, the extended
supply-identity table, and the cross-slice z=27 handoff. Every
z=26 (and z=27) value in this kit was touched by the engine for the
FIRST time at the frozen first run — the sole exceptions being
re-verification anchors of the four published z25f20 handoff
values.

This edition is the FIRST z=26 slice census of any kind on main
(the z25f20 kit's four z=26 handoff spots were single-point
probes). Its head (s=20) row was hand-DERIVED in-session from
published inputs only — the single observational dependency is the
published z25f20 s=20 row (reducible to its three measured deviant
cells C/B/A = {1,0,2}), disclosed per rung — and its s ≥ 21 rows
were pre-declared as BLIND structural candidates from the measured
even chain (z=16/18/20/22/24, all value-exact at
{z−6,z−4,z−2,z}).

## §2 Kit construction and discipline (executed before the first run)

- Files: `explore_z26f20.py` (frozen, sha256
  `7a5bd75c2ee682bcdb889af1656105c6dd7c9a6e48ae22362bb1bcdfb41c5676`,
  42,441 bytes), `engine_block.py` (byte-clone sha256
  `582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0`,
  pin `bd5f22e4…` asserted at startup, engine_gate PASS in the
  frozen output), frozen stdout `explore_z26f20.out` (sha256
  `73797c1c759e9ebe35579ba6729af667368d26357e853799c6e5a86f50845408`,
  68,633 bytes). SIX runs all byte-identical (frozen + default ×2 +
  PYTHONHASHSEED=random same-cwd + env -i isolated dirs ×2 via
  /usr/local/bin/python3), rc 0, ~42–44 s per run.
- Structure (per the frozen docstring): (a) cell census j=1..20
  (F..A14; j=1..19 stair-derivable with the EXACT K1264 window
  equality R = 26+j at the (19,j) children; j=20 A14 derived via
  the coinciding-decrease structure X=(20,20) → both B-children =
  Cell_19(20)), s-domain {0}∪{20..51}, arity ≤ 4, 75 shapes per
  cell = 1,500 census points; (b) tail spots s ∈ {52..59}; (c)
  strip m ∈ {20..26} at R=m+27; (d) row records m=18 (arity≤4 ext
  too) / 17 / 16 / 15 / 14 FRONTIER / 13 ONE-PAST; (e) strip spots
  m ∈ {27..30} + base spots m=20/m=19 + 4 published recheck
  anchors; (f) below-band H(27;Y;27), Y ≥ 20; (g) supply table k ∈
  {23..34} over {0}∪{12..68} (engine-free); (h) z=27 cross-slice
  handoff h1..h4; (i) K0832 battery (95 literals).
- Head derivation (s=20 row, 20 rungs): written in-session from
  published inputs ONLY — the published z25f20 census s=20 row
  (finite observations; the dependency reduces to the three
  measured deviant cells C/B/A = {1,0,2} at j=5/6/7, every other
  C-child input a PROVED K0832 closed-form constant), the PROVED
  K0832 closed form, the PROVED K1264 stair equality at the
  floor-token decrease, and the left-to-right in-head cascade.
  The drafting scratch (K1344-D6 discipline) cross-checked ONLY
  the published z=25 input literals against the engine (20/20
  exact) BEFORE the freeze; it evaluated NO z=26/z=27 position.
  The pre-declared heads: the registered even head trio {B DOWN
  0v2, A UP 1v0, A2 UP 2v1} at s=z−6=20 (even chain candidate
  6/6, the mirror of the odd head-empty rule 5/5), all other
  rungs conform (A RANK stays dead at even z).
- Structural candidates (s ≥ 21, blind, frozen before the run):
  the registered 11-entry lattice at positions {22,24,26}:
  @s=22 {C UP 1v0, B UP 2v1, D DOWN 0v2}, @s=24 {E UP 1v0, D UP
  2v1, G DOWN 0v2}, @s=26 {F UP 1v0, G UP 2v1}; NO other deviant
  in {21..51}; NO F persistent tail (even signature); sub-floor
  block s ∈ {40..51} clean; 0 multivalue. Total predicted deviant
  rows 11 = 3 + 8.
- Registered blind picks executed: z25f20 S5 #1 (the m=14 FRONTIER
  record with explicitly NO candidate — first contact, both
  outcomes new data, the §5-item-#2 non-binding structural
  expectation recorded before the run), S5 #4 (k=34 both
  components predeclared), and the z=27 touch as frozen option
  tables (values NOT predicted, only option-set resolution tables
  registered). PLUS THIS KIT'S OWN new sections registered before
  the run: the m=13 ONE-PAST-FRONTIER record (NO candidate, extra
  section added by this kit, not required by the handoff) and the
  m=20/m=19 base spots (paper-derived conforming candidates with
  disclosed premises, same composite-honesty structure as the
  published z25f20 e1/e2).
- m=20 base-spot derivation carried one UNMEASURED premise (the
  m=19-strip z=26 position (19,20)@R=46 conform candidate 
  v(39,26,46)=0 — no published kit measured it), disclosed and
  tested together with the spot; the premise's octave is the same
  composite-honesty structure the z25f20 kit used at its own e1.
- No file edited after any run.

## §3 Results (finite observations)

All pre-declared candidates HIT; the two NO-CANDIDATE sections
delivered the two headline data points. 

1. Head row (s=20): 20/20 rungs value-exact vs the raw engine —
   the registered trio {B j=6 DOWN 0v2, A j=7 UP 1v0 (exotic A
   option set {0,2,3}), A2 j=8 UP 2v1}; even chain candidate 6/6;
   A13 closes conform 0 = v(39,26,46); A14
   coinciding-decrease conform 1 = v(40,26,47).
2. Blind block {21..51}: deviant histogram {20:3, 22:3, 24:3,
   26:2} — the 11-entry lattice value-exact at every position and
   value; NO other deviant; NO F tail; sub-floor block clean; 0
   multivalue over all 1,500 census points.
3. +2-shift structural crosscheck vs the published z24-f18
   frozen census (post-run, both published artifacts): 11/11
   deviants value-exact under (cell, s+2), zero mismatches, zero
   extras — the consecutive-even structural identity chain
   z=16/18/20/22/24/26 now carries 5 consecutive value-exact +2
   shift comparisons.
4. Tail spots {52..59}: 160/160 MATCH (even signature; the odd F
   8/8 value-2 signature absent, as pre-declared).
5. Strip m ∈ {20..26}: cumulative 20/39/57/74/90/105/119 shapes,
   0 violations; the T-Z26 would-be claim positions m ∈ {21..26}
   measured clean for the first time.
6. Row records: m=18 R=45 26/0 (T-Z24 band m=18 z∈{25..33} SECOND
   entry; the S=36 shape X=(18,18) re-verifies the published
   z25f20 h3 value 1 in-record); m=17 R=44 32/0 (T-Z22 band FOURTH
   entry; in-record re-verification of h1 (17,18)@S=35=0 and h4
   (17,17)@S=34=0); m=16 R=43 40/0 (T-Z21 band entry; in-record
   re-verification of h2 (16,17)@S=33=1); m=15 R=42 50/0 (K1335
   band SIXTH entry).
7. **FRONTIER m=14 R=41: 62 shapes, EXACTLY ONE SEPARATION —
   X={14,14} @S=28, UP, value 2 vs collapse 1.** At z = z*(14) =
   26 exactly (K1268), the second at-frontier record of the
   series. The registered non-binding expectation inherited from
   the z25f20 S5-item-#2 law candidate (separations BEGINNING at
   the first co-token X={m,m+1}, S=2m+1, UP 2v0 — the exact
   m=13@z=25 shape) is REFUTED at this datum: X={14,15}@S=29
   CONFORMS; the actual unique separation is the CO-EQUAL pair
   {14,14} at S=2m=28 with value 2 vs collapse 1. The datum
   matches the published K1268 parity witness split EXACTLY
   (K1268 E6: even m separates at X=(m,m) with parent 2 vs single
   1 — and K1268's frontier cells (26, m≤8) were swept only for
   m ≤ 8, so cells (26,13)/(26,14) are new). Combined with the
   m=13 datum (odd m → X={m,m+1}@S=2m+1, UP 2v0), the frontier
   record law is now a TWO-DATUM PARITY-SPLIT candidate — see §5
   item #1.
8. **ONE-PAST-FRONTIER m=13 R=40: 76 shapes, EXACTLY ONE
   SEPARATION — X={13,14} @S=27, UP, value 1 vs collapse 0.** The
   FIRST datum of the one-past regime (no candidate registered,
   extra section added by this kit): the unique separation
   PERSISTS at the same shape as the z=25 at-frontier record but
   the value DROPS 2→1 (UP 1v0 instead of UP 2v0). Recorded as
   found.
9. Spot checks: strip spots m ∈ {27..30} 12/12; base spots m=20
   H(47;(20,20);26)=1 CONFORM (paper-derived candidate hit; the
   unmeasured m=19-strip premise tested true), m=19
   H(46;(19,19);26)=0 CONFORM (candidate hit; premises: the
   in-kit m=18 record + the published z25f20 m=19 base spot);
   published recheck anchors 4/4 (0,1,1,0 — the published z25f20
   z=26 handoff values reproduced exactly).
10. Below-band z'=27 (floor 20 = z'−7): 75 shapes, 0 deviants,
    0 multivalue — the NINTH z'−7 empty-datum candidate of the
    series confirmed.
11. Supply table k ∈ {23..34} ({0}∪{12..68}): every published
    constant reproduced (14th..24th tails); k=34 (TWENTY-FIFTH
    tail) REGISTERED candidate CONFIRMED — hold {0}∪{12..33},
    break 0v2 at s=34, UNIFORM 2v1 for ALL s ∈ {35..68} (34 break
    points, exactly one 0v2) — the even-z supply chain graduates
    to candidate 8/8 (k=20/22/24/26/28/30 measured + k=32
    closed-form published + k=34 closed-form here); the z=34-slice
    supply datum is precomputed for the future z=34 declaration
    lane.
12. z=27 handoff: h1 H(45;{17,18};27)=0, h2 H(44;{16,17};27)=1
    (both first co-token members conform), h3 H(46;(18,18);27)=1,
    h4 H(45;(17,17);27)=0 — ALL FOUR blind candidates CONFORM
    through their frozen option tables. m=18 base-spot z-sequence
    12 published + 1 new member: z ∈ {16..27} =
    0,1,0,1,0,1,0,1,1,1,1,1 (the post-z=23 1-run reaches FIVE
    consecutive slices); m=17 sequence z ∈ {16..27} =
    0,0,0,0,0,0 (six members).
13. K0832 battery 95/95; engine gate PASS.

## §4 Honest record

- The head derivation input literals were cross-checked against
  the engine at published z=25 positions only (20/20). Every
  z=26/z=27 value is first-contact at the frozen run. The s ≥ 21
  candidates are structural predictions from the measured even
  chain, not derivations; the measured value-exact hits upgrade
  the even lattice chain to 6/6 candidate instances and the +2
  shift structural identity to 5 consecutive value-exact pairs,
  nothing more.
- Every pre-declared candidate hit; the two NO-CANDIDATE sections
  are the designed honesty probes and both recorded real
  structure (the frontier parity split with the naive formulation
  refuted — X={14,15}@S=29 conforms, the separation is {14,14}
  instead; the one-past value drop 2→1), recorded as found. The
  K1268 alignment stated in §3.7 is a POST-run observation of the
  datum matching the ALREADY-PUBLISHED K1268 E6 parity table
  (K1268 is published `observed` status; its E6 parity split was
  measured on different sweeps — the two-token R*=W+1 scans — so
  the alignment is a cross-artifact consistency note, not a
  proof and not a new K claim).
- The m=13 one-past section was NOT required by any registered
  handoff; it was added by this kit and disclosed in the frozen
  docstring before the run.
- No file edited after any run; determinism six-run
  byte-identical.

## §5 Handoff (new registrations, all BEFORE any measurement, for future executions)

Ranked next targets for the fast lane:

1. **PARITY-CORRECTED FRONTIER-RECORD LAW candidate (supersedes the
   z25f20 S5-item-#2 formulation; two data points)**: at z = z*(m)
   exactly (K1268), the m-row x0 record (R=m+z+1, all parts ≥ m,
   co-token allowed, arity ≤ 3) shows EXACTLY ONE separation —
   ODD m: X={m,m+1} @S=2m+1, UP 2v0 (datum m=13@z=25); EVEN m:
   X={m,m} @S=2m, UP 2v1 (datum m=14@z=26, NEW). Aligned with the
   published K1268 L1/L2 parity witness split (X=(m+1,m) parent 2
   vs single 0 / X=(m,m) parent 2 vs single 1), now carried into
   the x0-record sweep style (K1268 swept two-token d-scans at
   R*=W+1; the x0 records add arity ≤ 3 parts-≥-m coverage and
   count-exact band entry). Next test data: the m=15 row at z=29
   (z*(15)=29, odd → predicted unique separation {15,16}@S=31 UP
   2v0), the m=16 row at z=30 (z*(16)=30, even → predicted unique
   separation {16,16}@S=32 UP 2v1), the m=17 row at z=33, the
   m=18 row at z=34. Any kit measuring a row at its own frontier
   should register the parity-corrected prediction and record the
   separation list verbatim, whatever it is.
2. **ONE-PAST-FRONTIER datum type (NEW, one datum)**: at z =
   z*(m)+1, the unique frontier separation PERSISTS at the same
   shape but the value DROPS 2→1 (m=13: {13,14}@S=27, UP 2v0 at
   z=25 → UP 1v0 at z=26). Second datum candidates: m=13@z=27 and
   m=14@z=27 (both fall inside a future z=27-slice kit or
   micro-kit); no formulation beyond the single observation.
3. **z=26 floor-21 (z−5, CRITICAL) pre-declaration census kit —
   the natural next CRITICAL edition (the analog of z23-min18 for
   K1344)**: its head (s=21) row is NOT derivable from published
   data (the z=25 floor-21 census row does not exist; no T-Z25
   proof), so its head row candidates are BLIND structural
   predictions and must be registered as such before any
   measurement: the two published CRITICAL-floor editions at
   even/odd z (z22f17 EVEN `115c0bb9`, z23f18 ODD K1344) plus the
   CONFIRMED z25f20 odd-critical profile are the disclosure
   material; no strong head-layout candidate should be registered
   until the even-critical same-floor profile is re-derived from
   the z22f18 publication. The supply side is complete (K1334
   theorem A k=34 even instance CONFIRMED here = even-z supply
   chain candidate 8/8; the z=26-slice supply datum k=26 was
   precomputed by the z20f14 kit); the next supply
   pre-computation is the TWENTY-SIXTH tail (k=35, ODD form):
   hold {0}∪{12..35}, UNIFORM 0v1 for ALL s ∈ {36..69}, over
   {0}∪{12..69} (odd-z supply chain candidate 9/9 after k=33;
   K0832 closed-form, engine-free).
4. **m=18 base-spot z-sequence next extension (z=28 touch)**:
   register the blind option tables BEFORE measuring — the
   pattern is now fully concrete because this kit PUBLISHES the
   z=27 values (h1=0, h2=1, h3=1, h4=0): the z=28 table is
   h1=(46;{17,18};28) [m=17 first co-token, R=46, blind],
   h2=(45;{16,17};28) [m=16 first co-token, R=45, blind], h3=(47;(18,18);28)
   [m=18 base on-line member, frozen table {B-child = h1 (in-kit
   premise), C-child 1^H(46;(18,18);27) = 1^1 = 0 PUBLISHED by
   this kit} → mex{h1,0}], h4=(46;(17,17);28) [m=17 base member,
   frozen table {B-child = h2, C-child 1^H(45;(17,17);27) = 1^0 =
   1 PUBLISHED by this kit} → mex{h2,1}].
5. **11×11 UNKNOWN: unchanged. No action.**

## §6 Caveats

Finite machine observations only, plus disclosed hand derivations
whose candidate status is stated per section; no universal claim;
no K slot claimed (1 experiment ≠ 1 K). Raw engine pinned at
`bd5f22e4…` (embedded, engine_gate PASS in the frozen output).
11×11 empty board, two-stone roots, S2, class 1/2/4 and all
central-reply roots: all UNKNOWN, unchanged; no verdict consumed.
