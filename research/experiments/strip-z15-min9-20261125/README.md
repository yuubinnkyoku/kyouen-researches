# Kit: strip-z15-min9 (floor-9 z=15 pre-declaration exploration census)

This kit is the FROZEN pre-declaration exploration census for the **z=15
min>=9 (floor-9) cell ladder F15f9..A315f9 and the prospective m=9-row z=15
line** — the next slice registered by the K1320 declaration note §7 (and
K1319 §5). No K slot is claimed by this kit; publish-then-execute.

Received handoff: `research/experiments/strip-z15-min10-20261125/` was
published by the same fast lane at `f547c174`; the published K1320
machines verify the min>=10 slice and its lemmas (`bb22f304…` README,
verify_k1320.py `081fe719…`). This kit registers no conflict with the
belowband-row3-phi lane (K1318 declaration `2026-11-25-belowband-row3-phi`,
orthogonal axes; the below-band measurement here is H(16;Y;16) at the
floor-9 domain, a different object from the (m,W)-Φ ladder geometry).

## Files

- `engine_block.py` — sha256
  `582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0`,
  byte-identical to the K1282..K1319 chain (pin
  `bd5f22e415a78368c9b798296bc84948d5637decbf3c21a92404d45fb12e3a92`).
- `explore_z15m9.py` — frozen exploration machine (sha256 see log/embedded
  docstring; startup pin gate asserts the embedded engine block bytes).
- `explore_z15m9.out` — frozen stdout artifact, determinism 3/3 runs
  byte-identical (sha256 `52a9808e7d0f43db69e13f083c1c0b7626d003f011d340319583e9d6f67821f9`).

## Machine provenance (full disclosure)

`explore_z15m9.py` is a text-diff modification of the published frozen
machine `research/experiments/strip-z15-min10-20261125/explore_z15pre.py`
(sha256 `3e2a8ab8…`). The engine block, PIN assert, `parts`, `cell_sweep`
machinery, and all section drivers are UNCHANGED bytes except for the
following exact differences (both endpoints published in-repo, so
`diff explore_z15pre.py explore_z15m9.py` reproduces everything):

1. Docstring fully rewritten for the floor-9 scope (sections (a)-(f)
   below; machine-provenance paragraph retained by construction of this
   README). No executable byte touched.
2. `cell_sweep`: s domain `{0}∪{9..smax}` (was 10) and `parts(s, 9, 4)`
   (was 10); per-cell dict `'floor': 9` (was 10); labels `15f9` (was
   `15f10`).
3. Strip sweep driver: `for m in range(9, 15)` (was `range(10, 15)`); the
   output section renamed `strip_z15_m9_14` (was `strip_z15_m10_14`).
4. Below-band census (f): floor-9 domain `s in {0}∪{9..40}` +
   `parts(s, 9, 4)` (was 10), `'floor': 9`, label
   `observational_only_belowband_floor9_domain_supply_source`,
   s_domain string `{0} U {9..40}`.
5. NEW section `m9_claim_position_spots` added (6 named witnesses at the
   m=9-row claim position R=25).
6. Sections (b) tail spots, (d) m=9-row in-band record, (e) strip spots
   m∈{15..18}, m10_base_spot: UNCHANGED (continuity re-measurements;
   labels 15f9 substituted consistently where the cell tags appear).

## Measured sections (frozen output)

- (a) **Cell census (9 cells × 312 floor-9 shapes each, s∈{0}∪{9..40},
  arity(Y) 0..4, engine = embedded pinned block)**:
  **multivalue rows 0 for ALL cells and ALL s** — every Cell_j value is
  s-only, decomposition-independent, over the extended floor-9 domain.
  Deviants from the Σ-collapse v(s+j,15,j+16):
  - **F15f9**: DOWN 1<2 at s=14, HOLE at s=15 (conforms), constant-2 UP
    tail 2>0 for ALL s>=16 (through tail spots s=41..48, unbroken);
    the F-family SIXTH tail form of K1320 SURVIVES the floor drop
    unchanged.
  - **G15f9**: single DOWN 0<1 at s=14 (absorbs the F tail; no tail of
    its own).
  - **E15f9**: DOWN 1<2 at s=12 + UP 2>0 at s=14.
  - **D15f9**: DOWN 0<1 at s=12.
  - **C15f9**: DOWN 1<2 at s=10 + UP 2>0 at s=12.
  - **B15f9**: DOWN 0<1 at s=10.
  - **A15f9**: UP 2>0 at s=10.
  - **A215f9**: ZERO deviants — FULL COLLAPSE (the prospective m=9-row
    base cell, the a=9 child of the claim position).
  - **A315f9**: ZERO deviants over the whole floor-9 domain — the
    m=9-row claim position census itself: H(25;{9}∪Y;15)=v(s+9,15,25)
    for all 312 swept shapes.
  **Floor-insensitivity observation**: each cell's floor-9 deviant list
  is IDENTICAL to its published floor-10 counterpart (same positions,
  same directions, same values). The z=15 cell values did not change a
  single point when the floor dropped from 10 to 9; the newly admitted
  min(Y)=9 / small-piece shapes all conform.
- (b) **Tail spots** (s∈{41..48}, single-token Y=(s,), 9 cells): exactly
  the 8 F15f9 rows mismatch at 2 vs 0 (the constant-2 tail, consistent
  with the F lemmas; no other cell deviates past s=40).
- (c) **Strip sweep m∈{9..14}** (S∈{m..m+39}, Y parts >= m,
  arity(Y)<=3, claim positions H(m+16;X;15) vs v(S,15,m+16)):
  **m=9: 265 shapes, 0 violations** (the prospective new claim
  positions). m∈{10..14}: cumulative 594 shapes, 0 violations — exact
  re-measurement of the published predecl kit's 594.
- (d) **m=9-row in-band record** ((25;X;15), parts>=9, co-token 9
  allowed, arity<=3, S∈{9..47}): **152 shapes, 0 separations** —
  continuity re-measurement, byte-level numbers match the published
  predecl kit section (d).
- (e) **m=9 claim position spots** (named witnesses): (9), (9,9), (9,10),
  (9,11), (9,9,9), (9,9,10) — all 6 MATCH v(S,15,25). Strip spots
  m∈{15..18} 12/12 match; m=10 base spot (26;(10,10);15)=1=v(20,15,26)
  continuity ✓.
- (f) **Below-band bottom-rung child census at the FLOOR-9 domain**
  ((16;Y;16) vs v(s,16,16), Y>=9 — min(Y)=9 and single-piece shapes
  like (9,) enter for the first time): **312 shapes, 0 deviants, 0
  multivalue** — the K1320 lemma-BB collapse EXTENDS to the floor-9
  domain over the whole sweep.

Everything above is OBSERVATION (census), not a claim: no universality
is asserted by this kit. The m=9-row line statement
H(m+16;X;15)=v(ΣX,15,m+16) for min(X)>=9 remains OPEN pending a
declaration-lane paper proof (prospective skeleton: rungs j=1..8 with
C children = the published z=14 floor-9 cells F14f9..A214f9 — an exact
domain fit — base a=9 child = A215f9 fully collapsed with stair children
at R=24=z+min (K1264), bottom B child below-band at the measured floor-9
collapse, m>=10 step inherited from the published T-Z15).

The standard 11x11 empty board, two-stone root, S2, and class 1/2/4
remain UNKNOWN at all times; no verdict is consumed.
