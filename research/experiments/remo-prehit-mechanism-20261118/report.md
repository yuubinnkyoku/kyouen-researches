# K0956: Pre-tail hit mechanism: universal HIT-GAP, SPLIT, SEAM (proved) + deterministic audit up to M<=2000

Continues K0950 (hit arithmetics HIT-ARITH, P-KILL, first-hit growth), K0952
(tail branch decomposition BRANCH/e-forms, seam bound max(M,3)), K0954 (from-start
BH model and its failure modes). All fixed-M modular statements use prime M,
main regime K = (M+1)t + kappa, t >= 1, 0 <= kappa <= M-2, (t,kappa) != (1,0);
Y = K+1, k0 = Mt + kappa - 1, N = MY - 1, C = gcd(M+1, kappa+2). "Window" means
the divisor interval [M, k0]. A state is a HIT iff sigma_Z(M,K) = 1.

## 1. HIT-GAP (universal, proved)

In the main regime with k0 >= sqrt(N):

  sigma_Z(M,K) = 1  <=>  [Y prime or Y = M^2]  and  D*(N) < M,

where D*(N) is the largest divisor of N not exceeding sqrt(N) (D*(1)=1).

Proof. K0950 HIT-ARITH: sigma_Z = 1 iff [Y ok] and the window [M, k0] is empty.

(=>) Window empty and k0 >= sqrt(N) force every divisor d <= sqrt(N) to lie
below M, hence D*(N) < M.

(<=) Assume [Y ok] and D*(N) < M. Suppose some d in [M, k0] divides N. If
d <= sqrt(N) then d <= D*(N) < M, contradiction; so d > sqrt(N). Then N/d
is itself a divisor of N with N/d <= sqrt(N), hence N/d <= D*(N) < M.
Then N = d*(N/d) < M*d <= M*k0. But N - (M+1)*k0 = 2M - kappa > 0
(kappa <= M-2), so N > (M+1)*k0 > M*k0, contradiction. Hence the window is
empty and HIT-ARITH gives sigma_Z = 1. QED.

The key inequality N > (M+1)*k0 (equivalently 2M > kappa) is independent of t.

Regime extent (k0 >= sqrt(N)), proved by f(kappa) = k0^2 - N increasing in
kappa with f(0) = M^2 t(t-1) - 3Mt - M + 2: the condition holds for every
kappa in [0,M-2] whenever [M >= 4, t >= 2], or M = 3, t >= 3, or M = 3,
t = 2, kappa >= 1, or M = 2, t >= 3; it fails only at (M,t,kappa) = (3,2,0),
at t = 1 with small kappa, and at M = 2, t = 2. Remark: at (3,2,0) (Y = 9 =
M^2, N = 26, D* = 2) the HIT-GAP equivalence still holds, by direct check;
the failure is only of the regime hypothesis, not of the gap statement.

## 2. SPLIT (universal, proved)

Same hypotheses (main regime, k0 >= sqrt(N), prime M). Every HIT satisfies
exactly one of:

(i) BRANCH: N has a divisor d <= M-1 with C | d and N/d prime. This is
    precisely K0952's branch-hit form: writing d = C*e, the identities
    C*A = M(M+1), C*B = M(kappa+1)-1 make e | Q and t = t_e (mod e)
    equivalent, so no extra condition is needed.

(ii) SMOOTH: N is (M-1)-smooth and N <= (M-1)^3.

Proof. Let the state be a HIT; by Section 1, [Y ok] and D*(N) < M, so every
divisor of N lies in [1, M-1] or [k0+1, N] (a divisor in [M, k0] would also
contradict the HIT-GAP converse direction argument since the window is empty).
Note N = MY - 1 gives M does not divide N, and N > (M+1)*k0. In regime,
t >= 2 (or t = 1, kappa >= 4) gives N >= 2M^2 + 3M - 1 > (M+1)^2, hence
sqrt(N) > M+1 and k0 >= sqrt(N) > M+1 >= C.

Set D* = D*(N) <= M-1 and B1 = N/D*; then B1 > sqrt(N), and B1 <= k0 would put
B1 in the window, so B1 > k0 > M+1 >= C.

Step 1 (B1 prime => branch). C | N = D* * B1; every prime p | C satisfies
p <= C < B1, so v_p(B1) = 0 and v_p(C) <= v_p(D*). Hence C | D*, and
d = D* <= M-1, N/d = B1 prime: BRANCH.

Step 2 (B1 composite). Write B1 = u*v with 2 <= u <= v. Then u <= sqrt(B1) <=
sqrt(N), so u is a divisor <= k0, hence u <= M-1.

  (i) If v <= sqrt(N): v is a divisor <= k0, so v <= M-1. Any prime factor
  p0 of N exceeding sqrt(N) would divide one of D*, u, v, all < p0:
  impossible. So N = D* * u * v with all prime factors <= M-1 and
  N <= (M-1)^3: SMOOTH.

  (ii) If v > sqrt(N): v <= k0 would put v (>= M) inside the window,
  contradiction; so v > k0. Since v > k0, its cofactor m = N/v satisfies
  m < N/k0 < M+1, and m divides N with m != M, so m <= M-1.
    (a) If v is prime: C | N = m*v and every p | C satisfies p <= C < v,
    so v_p(C) <= v_p(m); hence C | m, and d = m <= M-1, N/d = v prime:
    BRANCH.
    (b) If v is composite: write v = u2*v2 with 2 <= u2 <= v2; u2 <=
    sqrt(v) <= sqrt(N) gives u2 <= M-1, and v2 = v/u2 >= sqrt(v) > sqrt(k0).
    If v2 <= sqrt(N) then v2 <= M-1 (window) and N = m*u2*v2 with all prime
    factors <= M-1 (same p0 argument) and N <= (M-1)^3: SMOOTH. Otherwise
    v2 > sqrt(N) forces (window) v2 > k0 and we recurse on v2 in place of v.

The recursion terminates because the large cofactor strictly decreases
(v_{j+1} <= v_j / 2). QED.

Corollary (branch characterization of the far tail): for M >= 7, every HIT
with t >= M-3 is of BRANCH type; for M = 5 every HIT with t >= 3 is BRANCH;
for M = 3 every HIT with t >= 2 is BRANCH; for M = 2 (t >= 3) every HIT is
BRANCH. See SEAM below.

## 3. SEAM (universal, proved)

In the SMOOTH case, N >= M(M+1)t + M - 1 (kappa >= 0) and N <= (M-1)^3 give

  t <= (M-1)(M-2)/(M+1) < M-3   for M >= 7,
  t <= 2 for M = 5,  no smooth HITs at all for M = 2 and M = 3.

This improves K0952's seam bound max(M,3) to M-3 (M >= 7). Consequence: the
K0952 branch characterization of all hits holds throughout the far tail
t >= M-3 (M >= 7); the M = 3 statement agrees with the published PAIR-3
(all-hit branch law at M = 3).

## 4. Deterministic machine audit (finite enumeration, not a proof)

All code is in this directory (audit_build.py, prehit_core.py, pinned cores);
rerun produces byte-identical outputs (verified twice cold). Distinguish:
finite enumerations below are checks, not universal statements.

- GAP-GRID-A/B: engine sigma_Z == 1 vs raw-window predicate vs HIT-GAP over
  30,502 states (all primes M <= 61, t <= 50; M <= 23, t in [51,120]; all
  kappa incl. dead classes; K <= 7440): 0 mismatches (raw-window hits 1,460 +
  280). This extends K0950's engine anchoring (previously K <= 1500).
- SPLIT-GRID: primes M <= 199, live kappa classes, t in [2, M-2]: 24,763
  hits = 24,734 BRANCH + 29 SMOOTH-only; 0 SPLIT violations, 0 SEAM
  violations (also checked the analytic bound t <= (M-1)(M-2)/(M+1):
  0 violations), 0 hits in nonlive classes (consistent with P-KILL).
- T1-CHANNEL: t = 1 hits over primes M <= 199 (532 hits, 741 live classes):
  all require Y(1) = M + kappa + 2 prime (72% of live classes; 209 classes
  have Y(1) composite and never hit at t = 1); 435 branch, 97 smooth.
- FIRSTHIT: primes M <= 2000 (303 primes, 103,185 live kappa classes), scan
  capped at t_cap = 7*ln^2(M+1) + 100: every class hits within the cap
  (n_nohit = 0), so recorded first hits are genuine. Per-class first-hit type:
  branch-type first hits in 96,837/103,185 = 93.8% of classes (smooth-type
  6,348 = 6.1%); F(M) (worst first hit) is always branch-type. Crosschecks:
  tier3 (M <= 199) first/max_first_K 0 mismatch vs K0950 tier3;
  firsthit_pred 1,546 rows 0 mismatch.
  F-fit: M <= 199 (46 pts) F ~ 1.767*M^1.5088, R^2 = 0.8991, reproducing
  K0950's published 1.767*M^1.509 exactly; extended to M <= 2000 (303 pts):
  F ~ 2.977*M^1.3861, R^2 = 0.9249 (exponent flattens to 1.280 over
  M in [200,2000], R^2 = 0.745, suggesting slower-than-M^1.5 growth in the
  far range; finite observation).
- FIRSTHIT-PRED (heuristic, BH-conditional): corrected from-start BH model
  (K0954's divergence bug fixed via per-branch integration domains
  n_min(e) = 2 if (e = 1, t_e = 0, kappa = 0) excluding the special state
  K = M+1, else 1 if t_e = 0, else 0; integer n integrated over [n, n+1)).
  Pooled Spearman t* vs t_first = 0.1614 (old t_hat: 0.0758); within-M mean
  0.0087 (class ordering remains noise-dominated). Calibration: over the
  1,014 classes with t_first >= 2, median Lambda*(t_first) = 0.755, close to
  the theoretical ln 2 = 0.693 of a Poisson race; distribution calibration
  holds.
- RATE-PROFILE: per-t census for M in {7,13,23,53,101,199}: observed/expected
  BH hit ratio 0.88-1.01 at M = 23, 1.2-1.35 at M = 199 (heuristic).
- SMOOTH-LAW: all 29 smooth-only hit states recorded in output/audit.json
  (smooth_law.per_M), e.g. M = 61, kappa = 6, t = 8: N = 30682 = 2*23^2*29,
  D* = 58 < 61; M = 199, kappa = 152, t = 10: N = 428446. Max smooth N =
  428446 << 198^3. Smooth hits concentrate at t far below the SEAM bound
  (max t over the census is 10 at M = 199; bound allows t <= 195).

## 5. Status summary

- HIT-GAP, SPLIT, SEAM: universal, proved (pen-and-paper), machine-checked
  on the grids above.
- GAP-GRID / SPLIT-GRID / T1-CHANNEL / FIRSTHIT / SMOOTH-LAW: deterministic
  finite enumerations with byte-identical reruns.
- FIRSTHIT-PRED / RATE-PROFILE: heuristics conditional on the BH ansatz;
  the corrected from-start model is monotone and finite (K0954's Simpson-grid
  dependence removed).
- uv check / build test: not performed (same handling as prior remo items;
  flag for the long lane).

## 6. Files

- prehit_core.py: hit predicate toolkit + corrected BH model.
- audit_build.py: deterministic audit builder (all grids above).
- output/audit.json, output/firsthit_rows.json: machine outputs
  (audit.json also records sha256 pins of the inputs).
- Pinned inputs: composite_core.py, sievegen_core.py, branch_density_core.py,
  hitpair_core.py (copies included in this directory, sha256 in
  audit.json pin section); firsthit_pred.json
  (research/experiments/remo-branch-density-20261118/output/) and
  pkill_tight_tier3.json
  (research/experiments/remo-hit-prime-pair-20261118/output/) are referenced
  by sha256 pin without copying (byte-identical originals remain in the
  publishing experiments).
