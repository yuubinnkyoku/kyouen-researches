# K0958: Smooth-hit census: Lemma S3/S3', EXCLUSIVE, YSQR (proved) + complete enumeration up to M<=2000

Continues K0956 (HIT-GAP, SPLIT, SEAM, HIT-ARITH/P-KILL of K0950).
All fixed-M modular statements use prime M, main regime
K = (M+1)t + kappa, t >= 1, 0 <= kappa <= M-2, (t,kappa) != (1,0);
Y = K+1, k0 = Mt + kappa - 1, N = MY - 1, C = gcd(M+1, kappa+2),
live: gcd(kappa+1, M+1) = 1. "Window" = divisor interval [M, k0].
HIT-ARITH (K0950): in the main regime, sigma_Z(M,K) = 1 iff [Y ok]
and the window is empty, where [Y ok] means "Y prime or Y = M^2".

## 1. Lemma S3 (universal, proved)

If N is (M-1)-smooth with Omega(N) <= 3 (Omega = number of prime
factors with multiplicity), then every divisor d <= sqrt(N) of N
satisfies d <= M-1.

Proof. Write N = p1 p2 ... with primes p1 <= p2 <= ... <= M-1.
Omega <= 2: divisors <= sqrt(N) are among {1, p1}: p1 <= sqrt(N)
<= M-1.
Omega = 3, N = abc, a <= b <= c <= M-1 (each a prime factor, so
each <= M-1 by smoothness): a divisor d <= sqrt(N) other than 1,
a, b must be ab, ac, bc or c. ac <= sqrt(abc) forces ac <= b, but
ac >= 2c >= 2b > b (a >= 2): impossible; bc <= sqrt(abc) forces
bc <= a <= c, hence b <= 1: impossible. So d in {ab, c}. If
ab <= sqrt(abc) then ab <= c, so ab <= M-1. If c <= sqrt(abc)
then c <= ab, and c <= M-1 anyway. QED

## 2. Corollary S3' (universal, proved)

Main-regime state with prime M, [Y ok], N (M-1)-smooth and
Omega(N) <= 3  =>  sigma_Z(M,K) = 1. No window test is needed,
and no regime hypothesis (k0 >= sqrt(N)) is needed.

Proof. By S3 every divisor d <= sqrt(N) is < M. Suppose a divisor
d lies in the window [M, k0]. If d <= sqrt(N) then d < M,
contradiction; if d > sqrt(N) then N/d is a divisor <= sqrt(N),
hence N/d <= M-1, and N = d(N/d) <= k0(M-1). But N - (M+1)k0 =
2M - kappa > 0 (kappa <= M-2), so N > (M+1)k0 > k0(M-1),
contradiction. The window is empty and HIT-ARITH applies. QED

(The d > sqrt(N) branch is the HIT-GAP complement-window argument,
which uses only 2M > kappa, valid throughout the main regime.)

## 3. Lemma EXCLUSIVE (universal, proved)

No main-regime state can satisfy both SPLIT cases at once: if N
is (M-1)-smooth then N has no divisor d <= M-1 with C | d and
N/d prime. Hence SPLIT's dichotomy BRANCH / SMOOTH is disjoint,
and every smooth hit is smooth-only.

Proof. If N/d = p is prime and N is (M-1)-smooth then p <= M-1,
so N = d*p <= (M-1)^2. But Y >= M+2 in the main regime (equality
only at the excluded special state (1,0)), so N = MY - 1 >=
M(M+2) - 1 = (M-1)^2 + 4M - 2 > (M-1)^2. Contradiction. QED

## 4. Lemma YSQR (universal, proved)

No smooth hit has Y = M^2 (prime M). In fact for the state
t = M-1, kappa = 0 (the only one with Y = M^2): N = M^3 - 1 =
(M-1)(M^2+M+1), k0 = M^2 - M - 1. If M^2+M+1 is not
(M-1)-smooth, neither is N. If it is (M-1)-smooth, let p <= M-1
be any prime factor of M^2+M+1 (one exists since M^2+M+1 > 1);
then d = (M-1)p divides N and M <= 2M-2 <= d <= (M-1)^2 <=
M^2 - M - 1 = k0 (all for M >= 2), so d is a window divisor and
the state is not a hit. QED

## 5. Census completeness (finite, machine)

Theorem (deterministic enumeration, prime 5 <= M <= 1000): the
census below lists exactly the main-regime states of prime M in
[5, 1000] with N (M-1)-smooth and sigma_Z(M,K) = 1; and, for
primes 1000 < M <= 2000, exactly those with t <= 60.

Completeness argument. Let a smooth hit be given.
(i) [Y ok] holds by HIT-ARITH. Y = M^2 is impossible by YSQR,
so Y is prime, and kappa = (Y-1) mod (M+1) lands in [0, M-2]
with (t,kappa) != (1,0).
(ii) If the state is in the k0 >= sqrt(N) regime (all t >= 2
for M >= 4), SPLIT applies: by EXCLUSIVE the hit is SMOOTH-typed,
so N <= (M-1)^3. If not (t = 1 for M >= 5), N = M(M+kappa+2) - 1
<= M(M+4) - 1 < (M-1)^3 for M >= 5. Either way Y <= (M-1)^3/M.
(iii) Conversely a candidate (prime Y <= (M-1)^3/M in a valid
class) is a hit iff its window is empty, by HIT-ARITH.
The candidate set is finite and is exhausted by the sieve-walk
below. M = 2, 3 have no smooth hits at all (SEAM, K0956);
M = 5 is included in the walk (Y <= 12).

Sieve-walk. For each prime p <= M-1, the candidates N = MY-1
divisible by p are exactly the prime Y with Y = M^{-1} (mod p);
walking that residue class and dividing out all powers of p
factors every candidate simultaneously (cost sum_p 1/p per
candidate). A candidate is smooth iff its leftover reaches 1.
Deterministic; reruns are byte-identical (verified twice cold).

## 6. Census results (finite enumeration, not universal claims)

CENSUS-FULL (166 primes, 5 <= M <= 1000, complete):
- 4,067,641 candidates, 374,408 (M-1)-smooth, 2,609 hits,
  371,799 smooth-but-window-blocked states.
- Every blocked candidate has Omega >= 4: 0 violations of S3'
  over 374,408 smooth candidates (machine check of Sec. 2).
- 0 dead-class candidates (expected: p | kappa+1 forces p | Y,
  and Y = p < M+2 is below the candidate range) - a machine
  confirmation of the P-KILL/Y-prime interplay over 5.2M states.
- 0 BRANCH-and-SMOOTH overlaps (machine check of EXCLUSIVE over
  all 2,609 hits); all 2,609 hits are smooth-only.
- 0 SEAM violations (every hit has t <= (M-1)(M-2)/(M+1)).
- Engine: all 126 hits with M <= 199 plus every 29th beyond
  verified sigma_Z = 1 (288 checks, 0 failures); 101 sampled
  blocked candidates verified sigma_Z != 1 (0 failures).
- YSQR machine check: over the 301 primes, 62 have
  (M-1)-smooth M^3 - 1, and none of those 62 states is a hit.

CENSUS-STRIP (135 primes, 1000 < M <= 2000, complete for t <= 60):
- 1,150,823 candidates, 210,874 smooth, 7,441 hits (t = 60 is
  reached by 20 hits; smooth hits beyond t = 60, if any, are
  outside this strip).
- All 4,543 published smooth-first classes of these M are inside
  the strip (0 shortfall vs K0956's FIRSTHIT n_smooth_first).

Crosschecks vs K0956 outputs (pinned by sha256):
- The 29 published smooth-only states (SPLIT-GRID) match the
  census exactly, field by field.
- The 97 t=1 smooth hits (T1-CHANNEL) match exactly.
- All 109 smooth-type rows of firsthit_rows.json appear in the
  census with the same t.
- Independent recompute of all 1,546 per-class first hits
  (primes M <= 199): 0 mismatches vs firsthit_rows.json.
- Per M, census hit-class count >= published n_smooth_first
  everywhere (and equal for only 36/166 primes: later smooth
  hits after a branch first hit are common at larger M).

## 7. Structure of the smooth-hit locus (finite observations)

- Omega spectrum of hits: Omega = 3 in 28 + 50 cases, mode
  Omega = 4 (1,237 + 3,571), long tail to Omega = 16; omega
  (distinct primes) up to 6. S3' (Omega <= 3) is sharp but covers
  only a small minority: the mass sits at Omega = 4..7.
- Two populations. (a) t = 1: 4,904/10,050 hits, Omega up to 16,
  2-power-rich factorizations (all 119 hits with Omega >= 10 are
  t = 1; e.g. M = 647: N = 532480 = 2^13*5*13). (b) t >= 40:
  547/547 hits have exactly three odd prime factors <= M-1 with
  2-adic valuation <= 2 (522 with v2 = 1, 25 with v2 = 2, all of
  the latter within the strip's t <= 60 band); the odd primes
  concentrate near M/2 (e.g. M = 983, t = 220: N = 212977762 =
  2*449*487^2, the census maximum).
- t-concentration: max hit t = 220 at M = 983 vs SEAM bound 979
  (22.5%); N <= 0.225*(M-1)^3 in the full range. Deep smooth hits
  exist far beyond the old max t = 10 (K0956's M <= 199 census).
- Per-M hit counts grow roughly like M/25 on average (averages
  1.4, 5.9, 14.4, 28.5 over M in (2,100], (100,300], (300,600],
  (600,1000]); the seam bound (M-1)(M-2)/(M+1) is never tight.
- Multiplicity: 86 classes with two smooth hits in the full range
  (89 extra hits), 366 in the strip; so a class can have several
  smooth hits, and a smooth hit need not be the class's first hit.

## 8. Status summary

- S3, S3', EXCLUSIVE, YSQR: universal, proved (pen-and-paper,
  three to six lines each), machine-checked on all census states.
- CENSUS-FULL / CENSUS-STRIP: deterministic finite enumerations,
  byte-identical reruns; completeness as in Sec. 5.
- Population structure (Sec. 7): finite observations, no
  universal claims.
- 11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60},
  classes 1/2/4: unchanged, still UNKNOWN.
- uv check / build test: not performed (same handling as prior
  remo items; flagged for the long lane).

## 9. Files

- smooth_core.py: sieve-walk census + window DFS + classification.
- audit_build.py: deterministic builder (all sections above).
- output/audit.json: aggregates, checks, crosschecks, pins.
- output/hits_full.json, output/hits_strip.json: compact hit rows
  [M, kappa, t, K, Y, N, Omega, omega, is_branch_and_smooth].
- Pinned copies: prehit_core.py, composite_core.py,
  sievegen_core.py, branch_density_core.py, hitpair_core.py
  (sha256 as in K0956's pin section); K0956 outputs
  (audit.json, firsthit_rows.json) referenced by relative path
  with sha256 pins recorded in output/audit.json.
