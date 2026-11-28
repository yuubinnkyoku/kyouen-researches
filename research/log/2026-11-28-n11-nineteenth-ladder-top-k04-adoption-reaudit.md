# Completion log: n11 nineteenth ladder-top k04 adoption reaudit (flip-census/refresh)

Completion of the Part declared in
`research/log/2026-11-28-n11-nineteenth-ladder-top-k04-adoption-reaudit-declaration.md`
(declaration commit `0c912e89`, single owner, publish-then-execute).
Kit: `research/experiments/n11-nineteenth-ladder-top-k04-adoption-reaudit-20261128/`
(commit `2041489d`; fetch-back 11/11 byte-identical against the kit
MANIFEST.txt via commit-pinned raw CDN + sha256; the 3.7 MB probe
worklist stays unpublished per size policy, pinned by sha256 only).

## Measured (prediction holds EXACTLY, zero deviation)

BASE = eighteenth k03 head of record `3abecf8b...` (6,903 rows
WIN 221 / LOSS 6,682) -> SCEN = nineteenth k04 head of record
`8cc87263...` (6,904 rows WIN 222 / LOSS 6,682); the adoption
consumes exactly the single published nineteenth k04 15M escalation
row (1 WIN: k04 `1153062242096250880:540672`, serving class 20421,
s5 index 620742, legal 83, nodes 6,877,739; increment
`7cc20141`).

- **Status flips: exactly the 3 non-pre-excluded owner classes
  [18534, 18554, 19885] flip unknown -> excluded_now.** Census:
  unknown 34,357 -> 34,354 / excluded_now 163 -> 166 / free_now 39
  (Board-verified both sides) / excluded 390. The declaration's
  naive THREE-flip prediction holds with zero deviation; the standing
  shared-owner pre-exclusion caveat materialises on the serving
  class.
- **Serving class 20421 STAYS in the closure ladder: 798 -> 798
  rows, entered [], left [] (NO exit), rank churn 0 cells; it keeps
  rank 1 and its unknown_now drops 2 -> 1** (k05
  `1152921642046849024:68719477248` remains stage-1 2M UNKNOWN).
  It is already excluded_now at BASE and does not flip.
- Per-root coverage: free_now/uncovered identical on all 20 roots;
  one individual greedy re-route (root 12 RISES 2,840 -> 2,932, a
  +92 scheduling re-route churn, NOT a coverage claim); joint greedy
  MEASURES 43,185 -> 43,184; probing worklist 64,254 -> 64,253
  (SCEN regen pin `7e3c73d4...` / 3,714,150 B unpublished per size
  policy; BASE pin `115e3c60` / 3,714,209 B reproduced).
- update8: the adopted s5 index 620742 sits INSIDE the frozen
  baseline requirement (resolved 289 -> 290, remaining_now 31,332
  unchanged, groups_free_now 131); win-hit group set unchanged
  35 -> 35, every group entry byte-identical; the three flipping
  owner classes are NOT update8 plan group classes; the serving
  class 20421 IS a plan group class on BOTH sides, untouched.

## Gates (fail-closed)

- Refresh: 3-region byte-clone of the published eighteenth k03
  reaudit refresh (docstring, CACHE path, expected cache sha
  `8cc87263...`); 3 sequential runs byte-identical (~65 s/run):
  summary `d4b8099b`, closure `877b5f52`, per-root `0fccacec`.
- BASE-side pin reproduction (disclosed standing anchor, executed
  BEFORE the declaration, reads BASE bytes only): 1 run of the
  published eighteenth k03 refresh (unchanged bytes, CACHE
  `3abecf8b...`) reproduces the published eighteenth k03 reaudit
  outputs byte-for-byte (summary `23561801`, closure `77521463`,
  per-root `340e5a9c`, BASE worklist regen pin `115e3c60`).
- Measurer: structural adaptation of the eighteenth k03 measurer
  (count-asserted replacements); 3 runs byte-identical (census
  json `7c0d1649...`).
- External tamper battery 4/4 fail-closed (MT1 SCEN-cache verdict
  flip -> SCEN cache sha pin, MT2 BASE closure csv byte-tamper ->
  BASE closure pin, MT3 adoption-manifest byte-tamper -> manifest
  pin, MT4 SCEN worklist row deletion -> SCEN worklist pin), each
  aborted at its own pin BEFORE the census json was written; census
  json sha snapshot unchanged throughout; clean control re-PASS
  byte-identical.

## Honest disclosures

- The first SCEN refresh invocation attempt wrote to a not-yet-
  created reaudit/output directory and failed closed (rc=1,
  FileNotFoundError at the summary write, no partial output); the
  directory was created and all 3 runs completed rc=0
  byte-identical.
- The root-12 individual greedy union INCREASES by 92 while the
  joint greedy union DECREASES by 1 and the worklist drops by 1;
  these are scheduling re-route churns, not coverage claims and not
  deviations from the declared prediction.
- This lane runs without access to the user's computer (scheduled
  task); publication is via the GitHub API only.

## Status guard / next

NO verdict consumed. Class-status flips and the ladder stay are
census bookkeeping, not class closures and not root verdicts.
Class 20421 is NOT complete (k05 remains stage-1 2M UNKNOWN; no
ladder exit). The standard 11x11 empty board, the 19 central-reply
roots, the two-stone root {60,27} and its remaining third moves
100/108 stay UNKNOWN. Nodes are bookkeeping, never verdicts.

Next (separate declared Part): either the class-20421 k05
escalation (fresh declaration needed; k05
`1152921642046849024:68719477248`, s5 index 625899, legal 78, the
last cost-unknown of the rank-1 ladder class) or the twentieth
ladder-top selection after this reaudit's closure ladder
recomputation.
