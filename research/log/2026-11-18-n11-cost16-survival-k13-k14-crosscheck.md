# n11 cost-16 survival curve k=13/k=14 extension - independent arithmetic cross-check

Date: 2026-11-18
Lane: verification (n11 long-term lane)
Commits verified: `3a1b9481` (k=13, exact A/B split + full-singleton-ban mixed points), `dc8cb4a4` (k=14, first non-hub root (0,15) activating A-type 3-way joint formulas)

## Scope

The parallel lane extended the exact cost-16 ban-survival curve to k=13 and k=14.
This entry records an independent arithmetic verification of those two publications
from the verification lane. No recomputation was performed: every check is exact
BigInt arithmetic over the published JSON values, plus git-blob-sha1 pinning of the
inputs. The verification script is
`cost16_survival_k13_k14_crosscheck_20261118.py` (same experiment directory);
it re-fetches both pinned JSONs and reruns all checks.

## Inputs (git blob sha1 pinned)

- `output/cost16-survival-k13-20261118.json` - `bcf680f7529a119223f362099ed89685b9e37db6` (byte-verified after fetch)
- `output/cost16-survival-k14-20261118.json` - `1f0b64b1d0587333be30b412e87178dd28afec6a` (byte-verified after fetch)

## Checks (16, all PASS)

1. Grand-total identity: `A_survive(k) + B_survive(k) + kill(k) == 2,966,450,341,680,481,356` for every k=1..14 (constant).
2. `B_survive(0) == B16 == 660,663,050,386,546,968` (k0 anchor), and the published k0 share 22.271165% is consistent.
3. `kill` strictly monotone k=1..14; `A_survive`, `B_survive` strictly decreasing.
4. Marginal chain: `kill(k)-kill(k-1)` reproduces all 12 published marginals `k2_minus_k1..k13_minus_k12` exactly; `k14_minus_k13 == 70,505,656,058,846,061` matches the published value and is <= `m14 == 125,210,807,225,999,160`.
5. Survive totals at k=4/8/10 (`A_survive + B_survive`) equal the independently recomputed per-d-slice totals published in commit `33abfdb8`: 2,453,842,390,618,094,434 / 2,001,925,712,552,127,087 / 1,789,978,398,755,093,008. This extends the 3-point two-method cross-validation from `kill` to the survive decomposition (both lanes agree on A+B for the same k).
6. A/B split identity: `kill_A(k) + kill_B(k) == kill(k)` for all k=1..14; both components monotone.
7. B share percentages consistent to <5e-6 relative for k=0..14.
8. Mixed full-singleton-ban endpoint: `full_singleton_ban_survive_k14 == B_survive(14) == 307,687,702,837,177,515` (10.372252%).
9. The k13 JSON's own `survival.reproduce_k1_k10` check reproduces the published direct-mode `kill(10) == 1,176,471,942,925,388,348` (`k10_mine == k10_pub`), so cross-referencing between the two lanes is bidirectional.

Curve headline values (cover-plan combinatorics, not game outcomes):
`kill(13) = 1,465,153,639,713,678,205` (49.3908%),
`kill(14) = 1,535,659,295,772,524,266` (51.7676%).

## Notes

- `raw.githubusercontent.com` served transient 404s for both output paths during
  this verification while the files were confirmed present on main (GitHub API
  directory listing); content was recovered byte-exact via the jsdelivr mirror
  and pinned by git blob sha1. No repository content was affected. The
  cross-check script therefore tries the jsdelivr mirror first with a raw CDN
  fallback and pins both files by sha1.
- Indexing convention: published marginal keys `kN_minus_k(N-1)` hold
  `kill(N)-kill(N-1)`. An initial off-by-one in the verification script's
  comparison was corrected before recording; with the corrected convention all
  12 points match exactly and no discrepancy remains.
- k=14 activates the first non-hub root (0,15); A-type 3-way joint formulas
  first appear there. Quad and quintuple terms are structurally zero by the
  13-hub-root pigeonhole (their checks `quads.census_99b_187z`,
  `quints.all_zero_2002`), consistent with the published structural analysis.

## Status

Cover-plan combinatorics only. Survival points count minimum cover plans
containing at least one banned root; they are not search costs and imply
nothing about the outcome of the game. Standard 11x11 empty board remains
UNKNOWN; two-stone roots {49,60}/{59,60}, S2 {59,60}, and class 1/2/4 all
remain UNKNOWN.
