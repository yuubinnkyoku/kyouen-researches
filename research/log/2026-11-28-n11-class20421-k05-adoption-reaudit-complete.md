# Completion log: n11 class-20421 k05 adoption reaudit (flip-census/refresh)

Completion of the Part declared in
`research/log/2026-11-28-n11-class20421-k05-adoption-reaudit-declaration.md`
(declaration commit `2cad2042`, single owner, publish-then-execute).
Kit: `research/experiments/n11-class20421-k05-adoption-reaudit-20261128/`
(commit `868d8b39`; fetch-back 11/11 byte-identical against the kit
MANIFEST.txt via raw CDN + sha256; the 3.7 MB probe worklist stays
unpublished per size policy, pinned by sha256 only).

## Measured (prediction holds EXACTLY, zero deviation)

BASE = nineteenth k04 head of record `8cc87263...` (6,904 rows
WIN 222 / LOSS 6,682) -> SCEN = class-20421 k05 head of record
`e1a9cacc...` (6,905 rows WIN 223 / LOSS 6,682); the adoption
consumes exactly the single published class20421-k05 escalation
row (1 WIN: k05 `1152921642046849024:68719477248`, serving class
20421, s5 index 625899, legal 78, nodes 2,007,513; increment
`6b525957`).

- **Status flips: exactly the 2 non-pre-excluded owner classes
  [18683, 18710] flip unknown -> excluded_now.** Census: unknown
  34,354 -> 34,352 / excluded_now 166 -> 168 / free_now 39
  (Board-verified both sides) / excluded 390. The declaration's
  naive TWO-flip prediction holds with zero deviation; the standing
  shared-owner pre-exclusion caveat materialises on the serving
  class.
- **Serving class 20421 EXITS the closure ladder: 798 -> 797 rows,
  entered [], left [20421]** (the declaration's pre-registered EXIT
  prediction materialises). The adoption closes its LAST
  cost-unknown child (1 -> 0, exactly k05). It is already
  excluded_now at BASE and does not flip. Rank churn 769 cells:
  768 ladder cells shift by exactly -1 (the exit pulls the
  remaining rows up) plus one re-order cell - the flipping owner
  class 18683 sits INSIDE the ladder on both sides (unknown_now
  59 -> 58, rank 152 -> 123); 18710 sits OUTSIDE the ladder on
  both sides.
- Per-root coverage: free_now/uncovered identical on all 20 roots;
  two individual greedy re-routes (root 12 drops 2,932 -> 2,931 and
  root 37 rises 3,631 -> 3,634, scheduling re-route churns, NOT
  coverage claims); joint greedy MEASURES 43,184 -> 43,184
  (UNCHANGED); probing worklist 64,253 -> 64,251 (SCEN regen pin
  `09865553...` / 3,714,021 B unpublished per size policy; BASE pin
  `7e3c73d4` / 3,714,150 B reproduced).
- update8: the adopted s5 index 625899 sits INSIDE the frozen
  baseline requirement (resolved 290 -> 291, remaining_now 31,332
  unchanged, groups_free_now 131); win-hit group set unchanged
  35 -> 35, every group entry byte-identical; the two flipping
  owner classes are NOT update8 plan group classes; the serving
  class 20421 IS a plan group class on BOTH sides, untouched.

## Gates (fail-closed)

- Refresh: 3-region byte-clone of the published nineteenth k04
  reaudit refresh (docstring, CACHE path, expected cache sha
  `e1a9cacc...`); 3 sequential runs byte-identical (~65 s/run):
  summary `dae1f1b3`, closure `a33f0cb9`, per-root `ecfe4a0c`.
- BASE-side pin reproduction (disclosed standing anchor, executed
  BEFORE the declaration, reads BASE bytes only): 1 run of the
  published nineteenth k04 refresh (unchanged bytes, CACHE
  `8cc87263...`) reproduces the published nineteenth k04 reaudit
  outputs byte-for-byte (summary `d4b8099b`, closure `877b5f52`,
  per-root `0fccacec`, BASE worklist regen pin `7e3c73d4`).
- Measurer: structural adaptation of the nineteenth k04 measurer
  (count-asserted replacements); 3 runs byte-identical (census
  json `86c2f36b...`).
- External tamper battery 4/4 fail-closed (MT1 SCEN-cache verdict
  flip -> SCEN cache sha pin, MT2 BASE closure csv byte-tamper ->
  BASE closure pin, MT3 adoption-manifest byte-tamper -> manifest
  pin, MT4 SCEN worklist row deletion -> SCEN worklist pin), each
  aborted at its own pin BEFORE the census json was written; census
  json sha snapshot unchanged throughout; clean control re-PASS
  byte-identical.

## Honest disclosures

- The merger dependency (s5_union_merge.py, pin `90711961...`) was
  not present in the local working tree of this run; it was fetched
  read-only from the published sixthlossk38 reaudit kit and its
  sha re-verified against the pin before the measurer runs.
- The first tamper-battery harness draft reported "BATTERY FAILED"
  because its own pass criteria matched constant names against the
  Python traceback's `File` location line instead of the assert
  source text; re-running with the assert-location check showed
  all 4 tampers had in fact aborted at exactly the right pins
  (measurer lines 173/181/175/644: SCEN cache sha, BASE closure,
  manifest sha, SCEN worklist sha) with the census json unchanged
  throughout. The published tamper-battery-stdout.log documents the
  verified abort locations.
- Root 12's individual greedy union (raised to 2,932 by the
  nineteenth k04 adoption) drops back to 2,931 here while root 37
  rises 3,631 -> 3,634; the joint greedy union is UNCHANGED at
  43,184 and the worklist drops by 2 (the adopted key's own
  membership rows leave). These are scheduling re-route churns,
  not coverage claims and not deviations from the declared
  prediction.
- This lane runs without access to the user's computer (scheduled
  task); publication is via the GitHub API only.

## Status guard / next

NO verdict consumed. Class-status flips and the ladder EXIT are
census bookkeeping, not class closures and not root verdicts. The
serving class 20421 has left the closure ladder as a scheduling
quantity; it is NOT a completed class. The standard 11x11 empty
board, the 19 central-reply roots, the two-stone root {60,27} and
its remaining third moves 100/108 stay UNKNOWN. Nodes are
bookkeeping, never verdicts.

Next (separate declared Part): the ladder recomputation is already
measured in this kit's SCEN refresh (closure-classes.csv 797 rows);
the next class-20421-chain candidate is the new ladder rank-1
successor class 34269 (unknown_now 11), or the twentieth ladder-top
selection against the recomputed closure ladder.
