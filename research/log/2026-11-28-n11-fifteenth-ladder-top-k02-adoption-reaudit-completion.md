# Completion log: n11 fifteenth k02 adoption reaudit (flip-census/refresh)

Completion of the Part declared in
`research/log/2026-11-28-n11-fifteenth-ladder-top-k02-adoption-reaudit-declaration.md`
(commit `68b18052`, single owner, publish-then-execute). Kit:
`research/experiments/n11-fifteenth-ladder-top-k02-adoption-reaudit-20261128/`
(commit `c40b2648`, 10 files; fetch-back 9/9 byte-identical against
the kit MANIFEST via commit-pinned raw CDN + sha256).

## Measured result (prediction holds EXACTLY; zero deviation)

- **Status flips: exactly [5788, 5815, 7678] flip unknown ->
  excluded_now** - the declaration's naive THREE-flip prediction
  (the non-pre-excluded members of the owner union [5788, 5804,
  5815, 7678]). Census: unknown 34,368 -> 34,365 / excluded_now
  152 -> 155 / free_now 39 (Board-verified both sides) / excluded
  390.
- **Serving class 5804 EXITS the closure ladder: 799 -> 798 rows,
  left [5804], entered []** - it was the rank-1 ladder row holding
  its LAST cost-unknown child (k02, unknown_now 1 at BASE); the
  adoption drops its cost-unknown 1 -> 0. Its status is unchanged
  (already excluded_now since the fourteenth Part). Ladder rank
  churn 798 cells. The owner classes sit outside the ladder on both
  sides. The ladder exit is a scheduling statement measured here,
  NOT a class closure claim and NOT a root verdict.
- Per-root: free_now/uncovered identical on all 20 roots; greedy
  re-routes root 38 (2,876 -> 2,875) and root 49 (2,690 -> 2,689);
  joint greedy 43,148 -> 43,147; probing worklist 64,259 -> 64,258
  (SCEN regen pin `a8ebeffc...` / 3,714,446 B unpublished per size
  policy; BASE pin `e165cf36` / 3,714,501 B reproduced).
- update8: adopted s5 index 212115 outside the frozen baseline
  requirement (resolved 286 -> 286, remaining_now 31,332,
  groups_free_now 131); win-hit groups 35 -> 35 unchanged.

## Gates

- Refresh (3-region byte-clone of the published k03 reaudit refresh
  `b02869ef...`: docstring, CACHE path, expected sha `58110025...`):
  3 sequential runs byte-identical (~66s/run; summary `df5e7607`,
  closure `e10b5765`, per-root `f2d5d2a7`).
- BASE-side pin reproduction (pre-declaration disclosed anchor): 1
  run of the published k03 reaudit refresh (unchanged bytes, CACHE
  `3a527d39...`) reproduced the published k03 reaudit outputs
  (summary `8e37ad17`, closure `01dd4d85`, per-root `fc771d82`)
  byte-for-byte plus the BASE worklist regen pin `e165cf36`.
- Measurer (structural adaptation of the k03 measurer `4a2680aa...`,
  expected values pinned from the first measured run, sha
  `8afedb6c...`): 3 runs byte-identical (census json `b089b269...`).
- External tamper battery 4/4 fail-closed (MT1 SCEN-cache verdict
  flip caught by the sha-pin gate, MT2 BASE closure byte-tamper
  caught by the BASE closure pin, MT3 manifest byte-tamper caught
  by the manifest pin, MT4 SCEN worklist row deletion caught by the
  SCEN worklist pin - all aborted before the census json was
  written) + clean control re-PASS byte-identical.

## Disclosures

- One transient raw-CDN failure during the MT2 restore: the first
  clean control correctly FAILED CLOSED on the stale BASE closure
  pin (`9eb5924a...`) and wrote no output; the pin was re-fetched
  from the commit-pinned raw CDN, sha-verified (`01dd4d85...`), and
  the clean control re-run PASSed byte-identical.
- This lane runs without access to the user's computer (scheduled
  task); publication is via the GitHub API only.

## Status guard / next

Measurement bookkeeping only: NO verdict consumed. The standard
11x11 empty board, all 19 central-reply roots, the two-stone root
{60,27} and its remaining third moves 100/108 stay UNKNOWN. The
fifteenth class 5804 sequence (k01/k03/k02) is now fully adopted;
the closure ladder's new rank-1 serving class is 20421 (unknown_now
5) with 34269 (11) behind it - the next ladder-top selection Part
(single-owner declaration required) picks from these. Nodes are
bookkeeping, never verdicts.
