# Completion log: n11 eighteenth ladder-top k03 adoption reaudit (flip-census/refresh)

Completion of the Part declared in
`research/log/2026-11-28-n11-eighteenth-ladder-top-k03-adoption-reaudit-declaration.md`
(declaration commit `b841063a`, single owner, publish-then-execute,
HEAD pin `86cec4cd`). Kit:
`research/experiments/n11-eighteenth-ladder-top-k03-adoption-reaudit-20261128/`
(commit `6ee6e212`; fetch-back byte-identical against the kit
MANIFEST.txt via commit-pinned raw CDN + sha256).

## Measured (prediction holds EXACTLY, zero deviation)

BASE = seventeenth k02 head of record `e56ca5ca...` (6,902 rows
WIN 220 / LOSS 6,682) -> SCEN = eighteenth k03 head of record
`3abecf8b...` (6,903 rows WIN 221 / LOSS 6,682); the adoption
consumes exactly the single published eighteenth k03 15M escalation
row (1 WIN: k03 `1155173441859489792:131072`, s5 index 605961,
serving class 20421, legal 73, nodes 5,266,012; increment
`c208891e`).

- **Status flips: exactly the 3 non-pre-excluded owner classes
  [18136, 18143, 20128] flip unknown -> excluded_now.** Census:
  unknown 34,360 -> 34,357 / excluded_now 160 -> 163 / free_now 39
  (Board-verified both sides) / excluded 390. The declaration's
  naive THREE-flip prediction holds with zero deviation; the
  standing shared-owner pre-exclusion caveat materialises on the
  serving class.
- **Serving class 20421 STAYS in the closure ladder: 798 -> 798
  rows, entered [], left [] (NO exit), rank churn 0 cells; it keeps
  rank 1 and its unknown_now drops 3 -> 2** (k04
  `1153062242096250880:540672`, k05
  `1152921642046849024:68719477248` remain stage-1 2M UNKNOWN).
  It is already excluded_now at BASE and does not flip.
- Per-root coverage: free_now/uncovered identical on all 20 roots;
  two individual greedy re-routes (root 12 drops 2,841 -> 2,840,
  root 37 drops 3,632 -> 3,631); **joint greedy MEASURES
  43,145 -> 43,185 (a +40 scheduling re-route churn, NOT a coverage
  claim)**; probing worklist 64,255 -> 64,254 (SCEN regen pin
  `115e3c60...` / 3,714,209 B unpublished per size policy; BASE
  pin `6d3cf3ad` / 3,714,268 B reproduced).
- update8: the adopted s5 index 605961 sits INSIDE the frozen
  baseline requirement (resolved 288 -> 289, remaining_now 31,332
  unchanged, groups_free_now 131); win-hit group set unchanged
  35 -> 35, every group entry byte-identical; the three flipping
  owner classes are NOT update8 plan group classes; the serving
  class 20421 IS a plan group class on BOTH sides, untouched.

## Gates (fail-closed)

- Refresh: 3-region byte-clone of the published seventeenth k02
  reaudit refresh (docstring, CACHE path, expected cache sha
  `3abecf8b`); 3 sequential runs byte-identical (~65 s/run):
  summary `23561801`, closure `77521463`, per-root `340e5a9c`.
- BASE-side pin reproduction (disclosed standing anchor, executed
  BEFORE the declaration, reads BASE bytes only): 1 run of the
  published seventeenth k02 refresh (unchanged bytes, CACHE
  `e56ca5ca`) reproduces the published seventeenth k02 reaudit
  outputs byte-for-byte (summary `e22be6db`, closure `32f0e4f1`,
  per-root `b1aae491`, BASE worklist regen pin `6d3cf3ad`).
- Measurer: structural adaptation of the seventeenth k02 measurer
  (count-asserted replacements); 3 runs byte-identical (census
  json `3e0be91a`).
- External tamper battery 4/4 fail-closed (MT1 SCEN-cache verdict
  flip -> SCEN cache sha pin, MT2 BASE closure csv byte-tamper ->
  BASE closure pin, MT3 adoption-manifest byte-tamper -> manifest
  pin, MT4 SCEN worklist row deletion -> SCEN worklist pin), each
  aborted at its own pin BEFORE the census json was written; census
  json sha snapshot `3e0be91a` unchanged throughout; clean control
  re-PASS byte-identical.

## Honest disclosures

- The first refresh invocation attempt used `/usr/bin/time`
  (absent on this host, rc=127, no run happened, no output
  produced); redone with shell timestamps, all runs rc=0.
- The joint greedy union increases by 40 in this adoption
  (43,145 -> 43,185) while both measured individual greedy
  re-routes drop; this is a greedy-ordering re-route churn
  (scheduling quantity), not a coverage claim, and not a
  deviation from the declared prediction (which pre-registered
  only the flip census and the standing caveat).
- During execution an unrelated parallel lane published a
  five-row q4 declaration (`86eb9df6`, HEAD pin `b841063a` =
  this Part's declaration); the kit push proceeded after
  re-confirming HEAD (no conflict, unrelated path).
- This lane runs without access to the user's computer (scheduled
  task); publication is via the GitHub API only.

## Status guard / next

NO verdict consumed. Class-status flips and the ladder stay are
census bookkeeping, not class closures and not root verdicts.
Class 20421 is NOT complete (k04-k05 remain stage-1 2M UNKNOWN; no
ladder exit). The standard 11x11 empty board, the 19 central-reply
roots, the two-stone root {60,27} and its remaining third moves
100/108 stay UNKNOWN. Nodes are bookkeeping, never verdicts.

Next (separate declared Part): either the class-20421 k04/k05
escalation continuation (fresh declaration needed; k04 legal 83 /
k05 legal 78) or the nineteenth ladder-top selection after this
reaudit's closure ladder recomputation.
