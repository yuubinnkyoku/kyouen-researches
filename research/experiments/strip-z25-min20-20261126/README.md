# strip-z25-min20 — z=25 floor-20 (z−5, CRITICAL) pre-declaration census kit

THIRD edition of the floor-(z−5) CRITICAL census series (z=22
`115c0bb9`, z=23 `25522d56`), and the FIRST z=25 slice work of any
kind on main. This kit is a FINITE machine census against the pinned
raw engine plus engine-free closed-form pre-computations plus a
disclosed hand derivation written BEFORE the first run. NO K slot is
claimed, NO universal statement is claimed; the declaration lane (a
future T-Z25) picks up from here, exactly as the z22-min17 and
z23-min18 kits did for K1339/K1344.

Counter-probe (required before claiming, per the registered
handoffs; re-run at push time, HEAD `c77e79ab` unchanged since
kit-build): NO T-Z25 declaration exists on main (the only
`T-Z25` hits are handoff references in the published m18spot log);
no z=25 census kit exists (`filename:explore_z25` → 0 hits); no
z=24 floor-19 critical kit exists (`z24f19` → 0 hits).

## Files

- `explore_z25f20.py` — frozen pre-declaration explorer, sha256
  `4886cea4cc4329286a8cf803ab7a373fc25ac579f78af6e77baaa7c644349e90`
  (38,623 bytes). Structure adapted from the published
  `explore_z24f18.py` (z24-floor18 census kit, commit `35f7fe59`) by
  the disclosed parameter diff (slice z 24→25, floor 18→20, cell
  s-domain {0}∪{20..51} arity≤4, rungs j=1..20 incl. the disclosed
  beyond-bottom A14 extension, strip m ∈ {20..25} at R=m+26 — ALL
  segments NEW (no T-Z25), row records m=18..13 at R=m+26 incl. the
  registered m=15/m=14 band entries and the m=13 FRONTIER first
  contact, strip spots m ∈ {26..29}, new base spots m=20/m=19,
  below-band z'=26, supply sections 14th..24th-consolidated + the
  NEW k=32/k=33 pre-computations over {0}∪{12..67}, and the z=26
  cross-slice handoff h1..h4). The full hand derivation of the
  s=20 head row (20 points) and every structural candidate are
  frozen in the docstring BEFORE the first run.
- `engine_block.py` — byte-clone of the published chain engine
  (sha256 `582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0`),
  identical to the z22-floor16 / z20-floor14 / z21-floor15 /
  z23-floor17 / z24-floor18 kit bytes; the embedded ENGINE_BLOCK
  startup pin `bd5f22e4…` is asserted by the machinery (engine_gate
  PASS in the frozen output).
- `explore_z25f20.out` — frozen stdout, sha256
  `80f1617d38e57026345645ac2eb3dcb8e3d6fa51e4604c957cf564382ec885ba`
  (65,789 bytes). Determinism: SIX runs all byte-identical (first
  frozen run + default ×2 at freeze time + PYTHONHASHSEED=random
  same-cwd + env -i isolated directories ×2 via
  /usr/local/bin/python3), rc 0, ~39 s per run.

## Registered targets taken by this kit (before the fact)

The published m18spot kit log §5 (commit `b8146415`) registered,
BEFORE this kit ran:

1. (item #1) "TWENTY-THIRD-tail (k=32, even form) registered
   candidate: hold {0}∪{12..31}, break 0v2 at s=32, then UNIFORM
   2v1 for ALL s ∈ {33..66}" — executed here (g).
2. (item #3) "Base-spot z-sequence z=26 blind picks: m=18 on-line
   12th member H(45;(18,18);26), m=17 5th member H(44;(17,17);26)"
   — executed here (h), as blind first-ever z=26 engine touches
   with full frozen option tables.
3. (item #4) "z=25 residual-band record entries: m=15 (K1335)
   z=25 entry and the m=14 (K1330) z=25 entry = band COMPLETION" —
   executed here (d), together with the first-ever m=18/m=17/m=16
   z=25 row records and the m=13 frontier first contact.

Item #2 of that §5 (the z=26 floor-20 11-entry structural
lattice) is NOT taken here: its head-row derivation depends on this
kit's own s=20 row, so it belongs to the next execution once these
bytes are published (disclosed in the docstring).

## Headline results (all finite observations, no universal claim)

1. **The derived s=20 HEAD ROW hit VALUE-EXACT, 20/20 rungs**:
   the hand-derived option-set cascade (disclosed per rung,
   input literals c_j cross-checked 20/20 against the published
   z24f18 frozen row BEFORE the freeze) reproduced the raw engine
   exactly, including the ODD-CRITICAL STATION TRIPLET
   {C(j=5) DOWN 1v2, B(j=6) DOWN 0v1, A(j=7) UP 2v0} at s=z−5=20 —
   the **A RANK BREAK REBIRTH candidate CONFIRMED (5th odd
   instance, after z=17/19/21/23)** — the A2(j=8)
   rebirth-absorption conform, and the j=9..20 re-locked cascade
   conform. The odd critical station rule reaches candidate
   **4/4** editions (z=19/21/23 proved + z=25 candidate here).
2. **The BLIND structural candidates hit with zero surprises**:
   at s=22 the mirror triplet {E DOWN 1v2, D DOWN 0v1, C UP 2v0},
   at s=24 {F DOWN 1v2, G DOWN 0v1, E UP 2v0}; F HOLE at s=25
   conform (0 = v(26,25,27)); the F PERSISTENT TAIL UP 2v0 for ALL
   s ∈ {26..51} (26 rows); NO other deviant row in {21..51};
   **0 multivalue rows anywhere**. Total deviant rows
   **35 = 9 point + 26 tail, exactly as pre-declared**. The
   F-family HOLE+TAIL typology (odd = HOLE+TAIL) reaches candidate
   **10th consecutive slice**. Census scope: 20 cells × 75 shapes
   = 1,500 deviant-census points.
3. **Tail spots s ∈ {52..59}: 160/160 as declared** — F 8/8 spot
   values 2 vs collapse 0 (the persistent tail past the census
   domain), the other 19 cells 152/152 CONFORM (odd-edition
   signature; the even editions show no F tail).
4. **Strip m ∈ {20..25} at R=m+26 (ALL NEW; no T-Z25)**: 105
   cumulative shapes, **0 violations** — the m ∈ {21..25} segments
   are the would-be T-Z25 claim positions, measured clean for the
   first time; the m=20 head-floor segment measured 20 shapes 0
   violations. Per-m cumulative: 20/39/57/74/90/105.
5. **Row records at z=25 (x0 published residual-band style), SIX
   sections**: m=18-row (R=44) **26/0 + arity≤4 ext 25/0 — the
   FIRST-EVER z=25 m=18 row record** (first of the future T-Z24
   declaration band m=18 z∈{25..33}); m=17-row (R=43) 32/0 (third
   entry of the future T-Z22 band); m=16-row (R=42) 40/0 (fourth
   entry, incl. the m18spot first co-token members covered);
   m=15-row (R=41) 50/0 (K1335 band FIFTH entry);
   **m=14-row (R=40) 62/0 — the K1330 band SIXTH AND FINAL entry =
   BAND COMPLETION, the first fully-swept residual band of the
   series (z ∈ {20..25} all 62/0)**; m=13-row (R=39) 76 shapes
   with **EXACTLY ONE SEPARATION: X={13,14} at S=27, collapse 0
   vs value 2, UP — the FIRST-EVER observed FRONTIER datum of the
   series** (z*(13)=25 EXACTLY, K1268 formula; no candidate was
   predeclared, first contact, and the separation is recorded
   whatever it is: the K1328 band m=13 z∈{19..24} is complete
   76/0 at each entry, and the very first frontier slice shows
   the single co-token separation {m,m+1} at S=2m+1, UP 2v0).
6. **Spot checks**: strip spots m ∈ {26..29} 12/12 conform; the NEW
   base spots both HIT their paper-derived candidates:
   m=20 H(46;(20,20);25) = 1 CONFORM (premises measured
   conforming by this kit's own (c)/(d2) sections) and m=19
   H(45;(19,19);25) = 0 CONFORM; published recheck anchors 8/8
   (1,0,1,0,0,1,1,1 — the m18spot constants reproduced).
7. **Below-band z'=26 (floor 20 = z'−6)**: 75 shapes, 0 deviants,
   0 multivalue rows — the j=1 removal-child supply source of the
   future T-Z25 lane measured clean.
8. **Supply identities (engine-free K0832 closed form) over the
   EXTENDED domain {0}∪{12..67}, consolidated 14th..24th table**:
   every published k=23..31 constant REPRODUCED (hold domains
   0 violations; breaks exactly at the published positions:
   odd k uniform 1v0 at s ≥ k+1, even k 0v2 at s=k then uniform
   2v1); **k=32 (TWENTY-THIRD, REGISTERED): CONFIRMED** — hold
   {0}∪{12..31} (21 rows), 0v2 at s=32, UNIFORM 2v1 for ALL
   s ∈ {33..67} — the even-z supply chain graduates to candidate
   **7/7**; **k=33 (TWENTY-FOURTH, NEW registration made by this
   file before the run): CONFIRMED** — hold {0}∪{12..33} (23 rows),
   UNIFORM 0v1 for ALL s ∈ {34..67} — the odd-z supply chain
   graduates to candidate **8/8**; the z=33-slice supply datum
   precomputed for the future z=33 declaration lane.
9. **z=26 CROSS-SLICE HANDOFF: four FIRST-EVER z=26 engine touches,
   all four CONFORM to the frozen option tables**: h1
   H(44;{17,18};26) = 0, h2 H(43;{16,17};26) = 1, h3
   H(45;(18,18);26) = 1, h4 H(44;(17,17);26) = 0. The m=18
   base-spot z-sequence extends to its 12th member: z ∈ {16..26} =
   **0,1,0,1,0,1,0,1,1,1,1** (the post-z=23 1-run continues
   through z=24/25/26); the m=17 sequence 5th member 0
   (0,0,0,0,0).
10. **K0832 closed-form-vs-engine battery: 96/96** (every
    single-token literal used by the derivations, closed form ==
    canonical engine == ordered engine); engine gate PASS
    (pin `bd5f22e4…`).

## Honest record

- The s=20 head row was DERIVED BY HAND in-session from published
  inputs ONLY (z24f18 frozen census finite observations, published
  zero-violation record constants v(38,24,43)=1, v(39,24,44)=0,
  v(40,24,45)=1, the PROVED K0832 closed form, the PROVED K1264
  stair equality, the left-to-right cascade), and the drafting
  scratch machine cross-checked ONLY these published z=24 input
  literals against the engine (20/20 exact) BEFORE the freeze; it
  evaluated NO z=25/z=26 position. Every z=25/z=26 value was
  touched by the engine for the first time at the frozen first
  run. The s ≥ 21 rows are structural candidates (blind) from the
  PROVED odd critical-chain profile K1330 z=19 / K1337 z=21 /
  K1344 z=23.
- Every pre-declared candidate hit with zero surprises (head row,
  station triplet, A rebirth and A2 absorption, s=22/s=24 mirrors,
  F hole+tail, multivalue census, strip segments, m=15/m=14 band
  entries, spot checks, base spots, supply constants, z=26
  handoff). The single NO-CANDIDATE section (m=13 frontier first
  contact) recorded its datum as declared, whatever it is.
- No file was edited after any run; the frozen stdout is the
  published artifact.
- No wall-clock, no randomness, no hash-order dependence (6-run
  byte-identical determinism incl. PYTHONHASHSEED=random and
  env -i isolation).

## Standard caveats

Everything here is FINITE machine observation against the pinned raw
engine, plus pure closed-form pre-computations, plus disclosed hand
derivations whose candidate status is stated per section. Nothing
here is a theorem; no universal statement is claimed. Standard
11×11 empty board, two-stone roots, S2, class 1/2/4 and all
central-reply roots: all UNKNOWN, unchanged; no verdict consumed.
