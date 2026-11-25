# K0959: First-hit extremes: F identity, the "flattening" as a fitting artifact, BH extreme-value identification

Continues K0956 (FIRSTHIT table F_by_M, 303 primes M <= 2000;
firsthit_rows.json, 1,546 live kappa classes of primes M <= 199
with corrected-BH t_star).  Everything below is a finite
observation on that pinned data unless explicitly marked proved.
Notation: F(M) = (M+1) t* + kappa* is the worst first hit of M,
F_t = t*, F_kappa = kappa*, F_C = gcd(M+1, kappa*+2).

## 1. F identity and parity (machine checks, 303/303)

- F = (M+1) F_t + F_kappa holds on all 303 rows.
- F_type = branch on all 303 rows (no M has a smooth worst class;
  consistent with the smooth census of K0958: smooth hits
  concentrate at small t).
- F_kappa is even on all 303 rows (corollary of K0949 PARITY:
  for odd M, K even forces kappa even; M = 2 has kappa* = 0).
- F_t = 2 only for M in {2, 3, 17}; kappa* = 0 for 6 primes;
  median kappa*/M = 0.564, max 0.991.
- F is NOT monotone in M: 137/302 adjacent-prime pairs decrease
  (e.g. M = 1511: F = 118798 vs M = 1523: F = 56950).  Max
  F = 220140.  Any asymptotic statement about F must be
  statistical, not pointwise.

## 2. The exponent "flattening" is a fitting artifact (finite)

K0956 reported power fits F ~ a M^beta with beta drifting
1.5088 (M <= 199, R^2 = 0.8991) -> 1.3861 (M <= 2000, R^2 =
0.9249) -> 1.2798 (M in [200,2000], R^2 = 0.7454) and read this
as "flattening".  Surrogate recovery: power-fitting the pure
deterministic law g_d(M) = M ln^d M on the same grids gives

  grid            observed beta   surrogate beta (d=1.5 / 1.8)
  M <= 199          1.5088           1.5235   / 1.6282
  M <= 2000         1.3861           1.3250   / 1.3900
  [200,2000]        1.2798           1.2280   / 1.2736

A single logarithmic law, power-fitted on these grids, produces
the same apparent decay of beta with grid range (for d = 1.8 the
two larger grids match the observed beta within 0.006; for
d = 1.5 the small grid matches within 0.016).  The drift of the
fitted exponent therefore carries no information about a regime
change; it is a grid artifact.  Conversely no fixed (alpha, d)
describes all three grids (log-space slope-1 fits of M ln^d M
reach R^2 = 0.886/0.924/0.745 at best, on par with the power
fits), so on this range F is not asymptotic to alpha M ln^d M
for a fixed d either.  The stable quantity is the bucket median
of F_t / ln^2 M, which stays in [0.856, 0.976] over the buckets
M in [2,50), [50,100), [100,200), [200,500), [500,1000),
[1000,2001] (medians 0.8696, 0.9761, 0.8949, 0.9126, 0.9351,
0.8560) - i.e. F_t ~ ln^2 M to within a slowly drifting factor,
and F ~ (M+1) F_t + kappa* inherits the M ln^2 M shape.

## 3. Worst-class structure (finite)

F_C = 2 in 68/303 cases; the rest spread over many C values with
55 cases of C > 100 and 20 cases of C = (M+1)/2.  There is no
dominant worst class; the worst class is not characterized by
its C alone.

## 4. BH identifies the extreme, not the order (finite)

Over the 43 primes M <= 199 with at least 3 class rows:
- pooled Spearman(t_first, t_star) = 0.1619 (replicates K0956's
  0.1614): global class ordering is noise-dominated.
- top-decile Spearman = 0.5633: within the slowest 10% of classes
  the model orders much better.
- top-3 overlap = 0.9302: on average 2.79 of the observed 3
  worst classes are in the model's top 3.
- argmax agreement 9/43; the observed worst class sits at
  normalized BH-rank median 0.273, mean 0.399 (0.5 would be
  chance).

Interpretation (heuristic): the corrected from-start BH model is
an extreme-value model, not an ordering model - usable to
predict which classes will be slow, not to rank the bulk.

## 5. Extreme-value amplification (finite, M <= 199)

For each M the observed ratio t*/median(t_first) exceeds the
iid-exponential baseline ln(2n)/ln(2) (n = number of live
classes) by a median factor 1.363 (mean 1.61; for M >= 50 the
median is 1.385).  Extremes: M = 181: t* = 81 vs median 2
(excess 5.66); M = 137: t* = 10 vs median 3 (excess 0.52).
Class-rate heterogeneity amplifies the worst case beyond the
homogeneous-Poisson prediction by a typical factor ~1.4.

## 6. Engine anchor on F (machine check)

sigma_Z(M, F) = 1 verified directly by the pinned engine for
all 303 F rows (0 failures, 3.4 s total).  This anchors the
worst first hits up to K = 220140, far beyond K0956's GAP-GRID
engine anchor (K <= 7440).

## 7. Status summary

- All statements in this item are finite observations/heuristics
  on pinned K0956 data; none is universal.
- The artifact explanation (Sec. 2) resolves the K0956 open note
  about exponent flattening; it is a methodological remark, not
  a theorem about F.
- 11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60},
  classes 1/2/4: unchanged, still UNKNOWN.
- uv check / build test: not performed (same handling as prior
  remo items; flagged for the long lane).

## 8. Files

- extr_core.py: fits, ranks, medians, Spearman.
- audit_build.py: deterministic builder, byte-identical reruns
  (verified twice cold).
- output/audit.json: all tables above with pins.
- Pinned copies: prehit_core.py, composite_core.py,
  sievegen_core.py, branch_density_core.py, hitpair_core.py
  (sha256 as in K0956's pin section); K0956 outputs
  (audit.json, firsthit_rows.json) referenced by relative path
  with sha256 pins recorded in output/audit.json.
