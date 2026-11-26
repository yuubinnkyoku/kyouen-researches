# 2026-11-26 — d-shift two-supply family: UNIVERSAL closed-form theorem (case analysis) closes open structural question (a) of the single-token theorem log — the general-d pair (v(s,k+d,k+d), v(s,k,k+d)) fully characterized for ALL k>=1, d>=1, s>=1; the d=1 instantiation machine-matches the published theorem/K1334 Theorem A on 98,200 points; d=2 (the literal question pair v(s,k+2,k+2) vs v(s,k,k+2)) collapses to: even k a single-break line (holds forever (0,0) from s=k+2), odd k an ISOLATED hold island at s=k+1 between the (1,2) lag break and the (2,0) uniform tail; frozen audit 1,209,600 + 2,660 + 764 + 98,200 points ALL MATCH, determinism 6/6 byte-identical

Experiment: `research/experiments/dshift-supply-family-theorem-20261126/`
(verify_dshift_theorem.py sha256 `15040ba4…` 17092 B / engine_block.py
`582c93c1…` pin `bd5f22e4…` (published chain byte-clone) / frozen
.out `87f0c951…` 8397 B / README with the full written proof).

## Position and slot check (pre-claim, at kit-build time)

This kit executes the OPEN STRUCTURAL QUESTION (a) registered by
`research/log/2026-11-26-single-token-tail-supply-identity-theorem.md`
handoff item 3 (a): "the same treatment for the two-supply family
v(s,k+2,k+2) vs v(s,k,k+2) and general d-shifts — do they admit
closed-form k-universal patterns too?"

Slot probes at build time (latest main head `e76b8c27`, the n11
sixth-cost k12 checkpoint): repo-wide code search "dshift" 0 files;
"d-shift" only the registering theorem log itself; the two-supply
text matches only the registering log and the z18 kit README's
unrelated two-supply-CHAIN deviant-triplet picture; no knowledge
item covers any (v(s,k+d,k+d), v(s,k,k+d)) seat pair with d >= 2
(K1334 and the single-token theorem kit cover d=1 only). Every
position in the frozen audit was first evaluated by the frozen first
run; no prior kit output is involved beyond the pinned engine bytes.

## Derivation order (paper-first, per the K1320/K1321/K1325/K1334
discipline)

The complete case analysis (A-part / B-part / identity region) was
derived by hand from the published closed-form branch structure
(E0)-(E4) BEFORE any machine run: drafting scratch checked only the
branch arithmetic on paper; the first machine contact of every
audited position happened at the frozen first run. The proof is the
written case analysis in the kit README; the frozen audit is a
corroboration and transcription-error defense, NOT the basis of
universality.

## The theorem (full statement and proof: kit README)

For all k >= 1, d >= 1, s >= 1, seats A = v(s,k+d,k+d) and
B = v(s,k,k+d):

- **A-part**: A = s mod 2 on [1..k+d-1]; A = 2 (k+d odd) / 0
  (k+d even) for ALL s >= k+d (no cap).
- **B-part**: B = s mod 2 on [1..k-1]; B(k) = 2 iff (k+d odd AND
  d <= k-1), else k mod 2; B = s mod 2 on [k+1..d] (iff d >= k+1);
  B = d mod 2 for ALL s >= max(k+1, d+1) (no cap).
- **Identity region**: hold exactly on [1..k-1] ∪ ({k} iff k+d even
  OR d >= k) ∪ [k+1..d] ∪ (striped points s = d mod 2 in
  [max(k+1,d+1)..k+d-1]) ∪ ([k+d..∞) iff k even AND d even); break
  pairs (k%2,2) at the lag break, ((d+1)%2,d%2) in the striped gaps,
  and (0,1)/(2,0)/(2,1) in the three uniform-tail break shapes.

Key structural findings (all finite-restatement-free, from the
universal claim): the identity line for even k and even d FAILS
NOWHERE except the striped zone and the lag break; for d=2 even k it
fails at exactly ONE point of the whole infinite line (s = k+1,
pair (1,0)) and holds (0,0) forever beyond; for d=2 odd k >= 3 the
hold set contains an ISOLATED single point s = k+1 (island (0,0)
between the (1,2) lag break at s=k and the (2,0) uniform break from
s=k+2 on) — a hold-set topology that never occurs in the d=1 family.
The B-uniform piece is the K1334 Lemma S lattice fact at m = d-1;
the present theorem extends it to the full two-seat profile.

## d=1 instantiation (machine cross-check against the published theorem)

The general-d case analysis instantiated at d=1 was machine-checked
point-by-point against a verbatim transcription of the published
single-token theorem's derived(s,k) (frozen audit section
d1_instantiation_audit): k in {1..400} x s in {1..k+45}, 98,200
points, 0 mismatches. So the new theorem provably-specializes to the
published theorem (= K1334 Theorem A) as written.

## Frozen corroboration audit (verify_dshift_theorem.py, ~1 s per run)

- engine_gate: pin assert PASS.
- closed_form_grid: k in {1..400} x d in {1..12} x s in {1..k+d+45}:
  1,209,600 / 0.
- identity_region: independent classifier (I1-I5 zone labels derived
  from the region claims, not from the pair formula) vs measured
  pairs on the same grid: 0 mismatches, label counts I1 957,600 /
  lag_break 2,364 / I2_hold_k 2,436 / I3_hold_mid 286 /
  I4_striped_hold 13,039 / I4_striped_break 13,075 / I5_uniform_hold
  55,200 / I5_uniform_break_deven 55,200 / I5_uniform_break_dodd
  55,200 / I5_uniform_break_oddodd 55,200.
- large_s: d in {2,3,4,5,8,13,21} x k in {1,2,3,44,45,99,100,101,199,
  200}, s to k+d+5000: 2,660 / 0.
- engine spots (canonical AND ordered raw engines, both seats):
  complete k in {1..8} x d in {1,2,3,5} x s in {1..k+d+6} plus
  sampled boundary rows: 764 / 0.
- d1_instantiation: 98,200 / 0.
- degenerate s=0 boundary record (inherited convention, 5 rows):
  engines give 1 on both d-shift seats at s=0 (identity A=B holds
  engine-side), closed form 0 by its x<=0 convention; no strip-kit
  measurement involves x=0.
- d2_family_record: the measured closed-form rows drawing the d=2
  corollary (9 k-rows).
- Determinism: 6/6 byte-identical (default x2 in the kit dir,
  PYTHONHASHSEED=random, env -i same cwd, env -i isolated dir copy,
  env -i + PYTHONHASHSEED=1 isolated dir copy); all sha256
  `87f0c951…`; rc 0 each run.

## §5 Handoff (registrations, all BEFORE any further measurement)

1. **Open structural question (b) of the single-token theorem log
   REMAINS OPEN** and is the natural next case-analysis target: the
   m-row supply analogues of the strip bands (R = m+z+1, m in
   {13..18}) where the published separation life-cycle scaffold
   lives (births at z*(m)+2d, death at birth+3, "exactly two at
   birth slices / exactly one in between", the periodic-2 wave
   profile of the sixth-wave log S3) — is that scaffold also a
   closed-form case analysis over the published shape-vs-collapse
   comparison (two-token collapse v(sumX; z; R) vs the closed-form
   family derived here and in K1334/Lemma S)? The present theorem
   fixes BOTH seats of that comparison in closed form whenever the
   comparison seats are single-token lattices; the missing piece is
   the two-token H side. No claim made here.
2. Future kits registering d-shift supply identities should cite
   this theorem (experiment dir + this log) instead of per-(k,d)
   grids, at most keeping a small battery spot-check (the same
   corollary-citation discipline the single-token theorem log
   prescribed for per-k tails).
3. The lag-break edge (B(k) = 2 only when d <= k-1) means the d > k
   regime has NO lag break at s = k and the s%2 hold extends through
   d; kits scanning "wide-supply" chains (d of order k) should
   expect the three-glide profile hold/hold-tail/flat rather than
   the d=1 break family. Finite restatement of the universal claim;
   no additional measurement registered here.
4. 11x11: no action. Standard 11x11 empty board, 19 central-reply
   roots, two-stone root {60,27}, third moves {100,108}, S2, class
   1/2/4 and all closure classes remain UNKNOWN; no verdict
   consumed; no board-level claim made.

## §6 Caveats

Finite machine observations + one written universal case analysis of
the PUBLISHED single-token closed form; no claim beyond that closed
form's validity regime; engine transfer sample-verified (764 seats +
every strip-kit battery) and per the lane's published equivalence
claim, not re-proved here; degenerate s=0 convention divergence
inherited and recorded; no K slot claimed by this log (1 experiment
!= 1 K, promotion is a separate integrator step); nodes are
bookkeeping.
