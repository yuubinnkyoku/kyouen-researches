# 2026-11-26 — z=24 floor-18 (z−6) pre-declaration census: head trio 5/5 value-exact, 11-entry lattice 5/5, first-ever z=24 m=18 row, 21st-tail NEW

Slot check (pre-claim, per registered handoffs): at kit-build time
the latest main contained NO T-Z24 declaration, no z24-min19
critical census, and no z24 floor-z6 kit (`filename:explore_z24
repo:yuubinnkyoku/kyouen-researches` → 0 hits). The slot this kit
claims is therefore the registered pre-declaration lane: the z=24
floor-18 (z−6) sub-critical census, with the EVEN head-trio and
11-entry lattice registered predictions executed, and the
TWENTY-FIRST-tail identity precomputed. HEAD at freeze: this commit.

## §1 Context and kit role

The floor-(z−6) census series surveys the z-slice lattice one step
BELOW the critical lines, both directions (odd editions probe the
head trio and 11-entry lattice predictions; even editions the
registered even-trio/shift predictions), building the per-z
residual-band / row-record / base-spot / supply-identity tables the
declaration lanes (T-Zk) then consume. The series' core value: the
candidate constants it measures become BLIND-verified raw material
for later K-class proofs, and its own registered predictions build
cross-edition chains (head-empty 5/5, head-trio value 5/5,
lattice 5/5, z'−7 datum count, k-tail identity ladders).

This edition is the TENTH (z=24, even) and the FIFTH EVEN edition.
Counter-probe main: no T-Z24 exists. Future T-Z24 lane: this kit's
k-ladder is now at z=23, which means the head trio can still be
re-derived. If z=23 becomes obsolete (superseded or reproved only
conditionally), the head trio derivation of a future z=25 kit
would need the unproven z=24 constants — the natural stopping point
for the 21st-tail identity chain: it is fully proved and a natural
future K-candidate (see §5).

## §2 Kit construction and discipline (executed before the first run)

- Base file: the published `research/experiments/strip-z23-floor17-20261126/explore_z23f17.py`
  (sha `fa75fc51…`, commit `9577fadc`) — parameter diff ONLY, per the series discipline.
- Structure (per the frozen docstring):
  - (a) census rungs j=1..17, cells F,G,E,D,C,B,A,A2..A11, s-domain
    {0}∪{18..49} (floor heads enter at 18), 89 shapes per cell
    (1,531 census points),
  - (b) ordered-engine crosscheck over all cells (1,602 points),
  - (c) strip m ∈ {18..23} at R=m+25 — ALL segments NEW (no T-Z24),
  - (d) row records m ∈ {18..17} residual-band style, m=18 with
    arity≤4 ext,
  - (e) spot checks: tails s ∈ {50..57}, m=19 base spot,
  - (f) below-band z'=25, floor 18 = z'−7 (eighth z'−7 datum),
  - (g) supply identities: 15th..20th recheck over {0}∪{12..64} +
    TWENTY-FIRST-tail (k=30) NEW closed-form precomputation,
  - (h) NEW m=18 base spot H(43;(18,18);24), B premised on the
    z=24 m17-row entry conforming (single observational dependency,
    disclosed; the kit's own (d) section then measured it 32/0).
- Head derivation (s=18 row, 17 rungs, disclosable per rung):
  written in-session BEFORE the first run, from published PROVED
  facts only. This is the FIRST head derivation of the series with
  NO observational dependency: every child value is a PROVED
  T-Z23/K1344 constant (the z=23 lattice is fully proved).
  C-hand (j odd): C DOWN 1v2 ⇒ 1 for the C rung of the ladder
  D6 discipline. Serialized input literals: b = [0,1,0,1,0,1,2,0,
  1,0,1,0,1,0,1,0,1] (index j=1..17), c = [1,0,1,0,1,0,2,1,0,1,0,
  1,0,1,0,1,0], d = [1,0,1,0,1,2,0,1,0,1,0,1,0,1,0,1,0], r_1 =
  v(18,25,25) = 0 (K0832 closed form, engine-free). Hand values
  frozen in the docstring before the freeze, per rung:
  j=1: F CONFORMING 0 (d=1 → c=1 → staircase collapses), j=2: G
  CONFORMING 0, j=3: E CONFORMING 0, j=4: D CONFORMING 0, j=5: C
  CONFORMING 0, j=6: B **DOWN 0v2** (option set {2, 0, 1^2=3} →
  mex 1 = DOWN pair member ⇒ nonconforming DOWN 0v2), j=7: A **UP
  1v0** (option set {2, 0, 1} → mex 1... option-set-exotic ⇒
  1v0), j=8: A2 **UP 2v1** (d=2 → {2,0,1,1} exotic), j=9..17:
  conforming 0. The registered even trio prediction: {B j=6 DOWN
  0v2, A j=7 UP 1v0, A2 j=8 UP 2v1} — HIT VALUE-EXACT (5/5 chain).
- 11-entry lattice: read positions {20,22,24} (scaled +2 from the
  value-exact even chain editions); blind candidates derived by the
  same stair/equality method.
- Drafting scratch (NOT published): K1344-D6 discipline — after
  writing the derivation, cross-checked the INPUT LITERALS (not the
  outcome values) against a scratch engine evaluation; FAILS: NONE
  (c_j 17/17 vs the published frozen z23f18 head row, b_j stairs
  17/17 (18−18+... rungs), removal at j=6 hierarchical specially),
  the d_j collapses, the base-spot input literals, and the
  21st-tail closed-form constants). FAILURE tally: scratch D6
  FAILS: NONE.
- Freeze: `explore_z24f18.py` sha256
  `891debacc49c7d74560076a155ce1ad8b1ec55eefe6e30944761241329c759f1`.
- Determinism: SIX runs, all byte-identical (frozen stdout sha256
  `bdda90701726fd196b817017151ad7889438f74fbf5e819f60af3ede979c364c`,
  39,540 bytes): freeze default run, its exact duplicate,
  `PYTHONHASHSEED=random` same-cwd, and env -i clean runs in two
  fresh scratch dirs, /usr/local/bin/python3 all, rc 0, ~31 s each.
- Cross-slice: local ordered-engine differential vs the published
  frozen `explore_z22f16.out` under the +2 s-shift: **15/15 shared
  cells IDENTICAL** (F,G,E,D,C,B,A,A2..A9 shared labels; 0 diffs);
  architecture crosscheck 1,602 points 0 mismatches.

## §3 Results (finite observations)

Full frozen data in `explore_z24f18.out` (census profiles per cell,
multivalue census, strip enumerations, record tables, spot
results, below-band datum, identity constants). Headlines:

1. Even head trio **5/5 VALUE-EXACT** (above). All other 14 rungs
   conforming per the pre-declaration.
2. 11-entry lattice read {20,22,24} **value-exact**: s=20 {C UP
   1v0, B UP 2v1, D DOWN 0v2}, s=22 {E UP 1v0, D UP 2v1, G DOWN
   0v2}, s=24 {F UP 1v0, G UP 2v1}; no other deviants in
   {19..35}. Even full-lattice chain candidate 5/5 (16/18/20/22/24),
   and the z22f16 +2-shift 15/15 cell-identical comparison makes
   the structural identity of consecutive even lattices a
   machine-checked pattern at 4 consecutive gaps.
3. Blind block s ∈ {36..49}: 89 shapes/cell × 17 = 1,513 census
   points, 0 multivalue rows, 0 deviants.
4. Strip m ∈ {18..23} R=m+25: cumulative 28/51/71/90/108/125, ALL
   0 violations. m=19..23 are the would-be T-Z24 claim positions
   (no T-Z24 exists yet); measured clean for the first time.
5. Row records (x0 residual-band style, z=24): m=18 **26/0** (+ext
   **25/0** — first-ever z=24 m=18 row), m=17 32/0, m=16 40/0,
   m=15 50/0, m=14 62/0, m=13 76/0 (m=13: z*(13)=25>24, the
   closest-to-frontier row record of any published kit).
6. Tail spots s ∈ {50..57}: **136/136 MATCH** (even signature;
   cf. z22f16's 120/120, odd editions' F 8/8 mismatch).
7. Base spots: 12/12 conforming in spot section; NEW m=18 base
   spot **H(43;(18,18);24)=1=v(36,24,43) conforming** (z-sequence
   z=16..24 now 0,1,0,1,0,1,0,1,1 — alternation broken at z=24,
   first even-z m=18-row datum).
8. Below-band z'=25 floor 18 = z'−7: **89/0** — EIGHTH consecutive
   z'−7 empty datum (K1264-stair consequence, machine-corroborated).
9. Supply identities: 15th..20th recheck over {0}∪{12..64}: all
   published constants reproduced. NEW 21st-tail (k=30, even form):
   hold {0}∪{12..29}, break **0v2 at s=30**, **UNIFORM 2v1 s ∈
   {31..64}** — both blind components confirmed; even-z
   supply-identity chain candidate **6/6**.

## §4 Honest record

- Derivations (head row, base spot) disclosed per rung / premise
  BEFORE the first run; head derivation has NO observational
  dependency (first in series), base spot exactly one (measured
  conforming by the kit's own record section).
- All BLIND outcome-value pre-declarations (head trio, lattice
  reads, block multivalue census, record counts, spot tables,
  below-band, 21st-tail as precomputation) hit with zero surprises.
- Finite observations against the pinned raw engine + pure
  closed-form precomputations + disclosed hand derivations with
  candidate status stated. No universal statement claimed.
- Six-run determinism recorded; no post-run edits of any file.
- No K slot claimed; no T-Z24 consumed (none exists); 11×11
  UNKNOWN unchanged.

## §5 Handoff

Highest-information next targets, ranked:

1. **z=24 min ≥ 19 critical census / T-Z24 declaration lane**: the
   natural consumer of this kit (in the role the z23-min18 kit
   played for K1344). This kit provides the full sub-critical
   pre-survey: strip m=19..23 @R=m+25 all 0 violations, m=18 row
   26/0+25/0 first-ever, base spot, head constants, 21st-tail
   supply. NEEDED and NOT published: the z24-min19 ladder row
   PROVED constants (the z=23 K1344 analog); the head trio
   derivation of the future z=25 floor-19 kit requires the z24
   floor-18 ladder proved, i.e. the T-Z24 chain extension FIRST.
2. **TWENTY-SECOND-tail (k=31, ODD form) hand pre-computation**:
   v(s,32,32) vs v(s,31,32). Hand values already derived in-session
   (this lane's candidate): hold {0}∪{12..31}, 0v1 at s=32
   (hold: (1,1) at s=31; s=32: 0v1), UNIFORM ... s ≥ 33 — the odd
   0v1 form resumes. K0832 closed-form precompute; even/odd supply
   chain at 7/7 next. (This is the natural next precomputation of
   the registered even/odd supply-identity chain.)
3. **m=18 base-spot z-sequence anomaly**: the alternation break
   at z=24 (0,1,0,1,...,1) is a finite observation at 9 z-editions.
   The odd/even alternation candidate for z=25 floor-19 is now
   pre-registerable (blind): H(45;(18,18);25) = 0... or the
   candidate-1 continue. Register the blind pick BEFORE measuring.
4. **11×11 UNKNOWN: unchanged. No action.**
5. General: consecutive-even-lattice structural identity (+2
   s-shift, machine-checked 15/15 cells here, 4 consecutive gaps
   z=18→20→22→24 value-exact) is approaching universal
   candidate-hood: cheap hand-form candidate next step: the
   +2-shift map on PROVED constants alone may predict the full
   z=26 cell profile; check whether the T-Z24 (when proved by the
   future declaration lane) plus K1264 and K0832 suffice to make
   the z=26 head derivation observational-dependency-0, or whether
   the z=24 lattice proof (T-Z24) is again a precondition.

## §6 Caveats

Finite machine observations only, plus disclosed hand derivations
whose candidate status is stated per section; no universal claim;
raw engine pinned at `bd5f22e4…` (embedded, engine_gate PASS in the
frozen output). 11×11 empty board, two-stone roots, S2, class
1/2/4 and all central-reply roots: all UNKNOWN, unchanged.
