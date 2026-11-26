# d-shift two-supply family: UNIVERSAL closed-form theorem (case analysis over the published single-token closed form)

Kit: `research/experiments/dshift-supply-family-theorem-20261126/`
(verify_dshift_theorem.py sha256 `15040ba4…` 17092 B / engine_block.py
`582c93c1…` pin `bd5f22e4…` / frozen .out `87f0c951…` 8397 B / this README).

Executed answer to the OPEN STRUCTURAL QUESTION (a) registered by
`research/log/2026-11-26-single-token-tail-supply-identity-theorem.md`
(handoff item 3): "the same treatment for the two-supply family
v(s,k+2,k+2) vs v(s,k,k+2) and general d-shifts — do they admit
closed-form k-universal patterns too?" Answer: YES, in closed form
for ALL d >= 1, not just d = 2.

Slot check (pre-claim, at kit-build time): latest main head `e76b8c27`
(n11 sixth-cost k12 checkpoint). Repo-wide code search at build time:
"dshift" 0 files, "d-shift" only the registering theorem log, the
two-supply text matches only the registering theorem log and the z18
kit README's unrelated two-supply-CHAIN picture (census deviant
triplets). The published single-token theorem kit and K1334 cover the
d=1 pair (A = v(s,k+1,k+1), B = v(s,k,k+1)) only; no published engine
value or knowledge item covers any seat pair
(v(s,k+d,k+d), v(s,k,k+d)) with d >= 2. Every position in the frozen
audit was first evaluated by the frozen first run (pure closed form +
raw-engine spot battery, no prior kit output involved).

## The theorem

Notation: v = published single-token closed form
v(x,z,R) = H(R;(x);z) (transcription pinned `bd5f22e4…`, embedded
byte-identically in every strip kit and in this kit's engine_block.py),
q(t) = q_odd(t) = t if t odd else t-1, and the branch decomposition

- (E0) x <= 0 or R = 0 -> 0
- (E1) z = 0 -> min(R,x) % 2
- (E2) z = x -> [R odd & R <= 2x-1: 2 | R even & R <= x-1: 0 | else x%2]
- (E3) 1 <= z <= x-1 -> m = q(z): [R <= m: 2 if R odd else 0 |
  m < R < x+z: (R+z)%2 | R >= x+z: x%2]
- (E4) z >= x+1 -> m = q(x): [R <= m: 2 if R odd else 0 | else x%2].

For every integer k >= 1, every shift d >= 1 and every s >= 1, put

    A = v(s, k+d, k+d)     (advance seat: z and R both advanced by d)
    B = v(s, k,   k+d)     (lagging seat: z stays at k, R advanced by d).

**A-part (hold then k+d-parity constant, no cap in s).**

1. 1 <= s <= k+d-1:  A = s mod 2.
2. s >= k+d:  A = 2 if k+d is odd, 0 if k+d is even (s-independent).

**B-part (four pieces, no cap in s).**

1. 1 <= s <= k-1:  B = s mod 2.
2. s = k:  B = 2 if (k+d odd AND d <= k-1), else B = k mod 2.
3. k+1 <= s <= d (this interval exists iff d >= k+1):  B = s mod 2.
4. s >= max(k+1, d+1):  B = d mod 2 (s-independent forever).

**Identity region (the d-shift two-supply identity A = B).** The hold
set is exactly the union

- (I1) [1..k-1]                                    (always)
- (I2) {k} iff k+d is even OR d >= k               (otherwise lag break)
- (I3) [k+1..d]                                    (iff d >= k+1)
- (I4) {s in [max(k+1,d+1) .. k+d-1] : s = d mod 2} (striped)
- (I5) [k+d..infinity) iff k even AND d even        (uniform tail hold),

and the break pairs are

- s = k (iff k+d odd AND d <= k-1):            (k%2, 2)
- I4 points with s = d+1 mod 2:                ((d+1)%2, d%2)
- I5 when k,d both odd:                        (0, 1)
- I5 when k+d odd, d even:                     (2, 0)
- I5 when k+d odd, d odd:                      (2, 1).

## Proof (engine-free case analysis on the published closed form)

A-part. Fix k,d.

- 1 <= s <= k+d-1: then z = k+d >= s+1 = x+1, so (E4) applies with
  m = q(s) <= s <= k+d-1 < R = k+d, so the R <= m sub-branch is
  excluded and A = x%2 = s%2.
- s = k+d: z = x, so (E2) applies with R = x = k+d. R <= x-1 is
  impossible. If R is odd then R <= 2x-1 holds (R = x <= 2x-1), so
  A = 2. If R is even the final sub-branch gives A = x%2 = 0.
- s >= k+d+1: then 1 <= z = k+d <= x-1 = s-1, so (E3) applies with
  m = q(k+d). If k+d is odd, m = k+d = R, so the first sub-branch gives
  2 (R odd). If k+d is even, m = k+d-1 < R and R < x+z (because
  R = k+d < s+k+d for s >= 1), so the middle sub-branch gives
  A = (R+z)%2 = (k+d+k+d)%2 = 0.

So A is s%2 on [1..k+d-1] and the parity constant 2/0 beyond,
s-independent. &#9632;

B-part. Fix k,d.

- 1 <= s <= k-1: then z = k >= x+1, so (E4) applies with m = q(s) <=
  s <= k-1 < R = k+d, excluding R <= m, and B = s%2.
- s = k: z = x, so (E2) applies with R = k+d and x = z = k. R <= x-1
  would need k+d <= k-1, impossible for d >= 1. If R is odd (k+d odd)
  and R <= 2x-1 (i.e. k+d <= 2k-1, i.e. d <= k-1) then B = 2.
  Otherwise the final sub-branch gives B = k%2.
- s >= k+1: then 1 <= z = k <= x-1 = s-1, so (E3) applies with
  m = q(k) <= k < R = k+d (d >= 1), excluding R <= m; the middle
  sub-branch m < R < x+z is selected iff R < s+k iff s > d, giving
  B = (R+z)%2 = (k+d+k)%2 = d%2 there, and the final sub-branch
  B = x%2 = s%2 exactly on k+1 <= s <= d (endpoints inclusive: at
  s = d, R = x+z and the final sub-branch gives s%2 = d%2, the same
  value the middle branch would assign, so the two pieces glue).

So B has the four pieces above, the last one uniform forever. &#9632;

Identity. Compare per zone: on I1 both are s%2; at s = k the A-side
still sits in its hold (d >= 1), so the point holds iff B(k) = k%2 iff
NOT(k+d odd AND d <= k-1), else the pair is (k%2, 2); on I3 both are
s%2; on the striped zone [max(k+1,d+1)..k+d-1] (nonempty iff
d >= 2, resp. k >= 2 when d >= k+1) A = s%2 is still in its hold while
B = d%2 is already uniform, so the identity holds precisely at the
points s = d mod 2 and fails as ((d+1)%2, d%2) elsewhere; on the
uniform tail s >= k+d both sides are constants, 2/0 by k+d parity vs
d%2, so the tail holds iff 0 = d%2 and k+d even (k,d both even) and
otherwise breaks with the pairs (0,1) (k,d both odd), (2,0) (k+d odd,
d even), (2,1) (k+d odd, d odd). &#9632;

The d = 1 instantiation is EXACTLY the published single-token tail
supply identity theorem (and K1334 Theorem A): A = s%2 on [1..k] then
2 (k even) / 0 (k odd) forever; B = s%2 on [1..k-1], B(k) = 1 (k odd) /
2 (k even, k >= 2), B = 1 forever past k+1. Machine-checked
point-by-point against the published case analysis (frozen audit
section d1_instantiation_audit, 98,200 points).

## The d = 2 family (the literal open question (a) pair)

With d = 2 the identity region collapses to:

- k EVEN: holds [1..k] with s%2, single striped break at s = k+1 with
  pair (1,0), then holds (0,0) FOREVER from s = k+2 on — the identity
  fails at exactly ONE point of the whole line.
- k ODD, k >= 3: holds [1..k-1], breaks (1,2) at s = k, holds the
  ISOLATED single point s = k+1 with (0,0) (an island between two
  break regions), breaks (2,0) from s = k+2 on.
- k = 1: holds [1..2], breaks (2,0) from s = 3 on.

The frozen d2_family_record section draws these rows from the measured
closed form (k in {1,2,3,4,5,10,15,30,44}, s in [1..k+9]).

Consistency with K1334 Lemma S: the B-uniform part B = d%2 on
s >= max(k+1,d+1) is exactly the (E3) middle branch on the lattice
line R = (d-1) + k + 1 (Lemma S's m = d-1), value (m+1)%2 = d%2; the
present theorem extends that lattice fact to the full two-seat profile
comparing against the advance seat.

## Frozen corroboration audit (verify_dshift_theorem.py)

- engine_gate: embedded engine block sha256 == pin `bd5f22e4…` PASS.
- closed_form_grid_audit: k in {1..400} x d in {1..12} x
  s in {1..k+d+45}: 1,209,600 points, 0 mismatches vs the derived
  case analysis (pure closed form, engine-free).
- identity_region_audit: independent region classifier (I1-I5 zone
  labels derived from the region claims, not from the pair formula) vs
  measured pairs on the same 1,209,600-point grid: 0 mismatches; label
  counts I1_hold_low 957,600 / lag_break 2,364 / I2_hold_k 2,436 /
  I3_hold_mid 286 / I4_striped_hold 13,039 / I4_striped_break 13,075 /
  I5_uniform_hold 55,200 / I5_uniform_break_deven 55,200 /
  I5_uniform_break_dodd 55,200 / I5_uniform_break_oddodd 55,200.
- large_s_extension_audit: d in {2,3,4,5,8,13,21} x
  k in {1,2,3,44,45,99,100,101,199,200}, s in
  {k+d+46..k+d+300 step 7} + k+d+5000: 2,660 points, 0 mismatches.
- engine_spot_audit: canonical AND ordered raw engines on both seats,
  complete k in {1..8} x d in {1,2,3,5} x s in {1..k+d+6} plus sampled
  k in {10,12,15,20,25,31,44} x d in {2,3,4,5,9} x
  s in {k-1,k,k+1,d-1,d,d+1,k+d-1,k+d,k+d+1,2k}: 764 seats, 0
  mismatches (closed-form == engine transfer on d-shift seats).
- d1_instantiation_audit: 98,200 points, 0 mismatches vs the published
  single-token theorem case analysis (verbatim transcription).
- degenerate_s0_boundary_record: inherited convention — at s = 0 both
  raw engines return 1 on both seats (identity A = B still holds
  engine-side) while the closed form returns 0 by its x <= 0
  convention; NO strip-kit measurement involves x = 0 (row scans use
  parts >= m >= 13).
- Determinism: 6/6 runs byte-identical (default x2 in the kit dir,
  PYTHONHASHSEED=random, env -i same cwd, env -i isolated dir copy,
  env -i + PYTHONHASHSEED=1 isolated dir copy), all sha256
  `87f0c951…`, rc 0 each run, ~1 s per run.

FINITE audits corroborate only; the universal claim is the written
case analysis over the published closed form. 有限計算を全称性の根拠
にはしていない。

## Caveats

- The universal claim is over the PUBLISHED single-token closed form
  (the same scope discipline as K1334 and the single-token theorem
  kit); transfer to the raw engines is sample-verified here (764
  seats) and by every strip-kit battery to date, not re-proved.
- The degenerate s = 0 convention divergence is inherited and
  recorded; no measurement is affected.
- Finite observations + one written universal case analysis of the
  published closed form; no claim beyond that closed form's validity
  regime; no K slot claimed (1 experiment != 1 K).
- 11x11 empty board, two-stone roots, S2, class 1/2/4, 19
  central-reply roots and all closure classes: UNKNOWN unchanged; no
  verdict consumed; nodes are bookkeeping and no board-level claim is
  made.
