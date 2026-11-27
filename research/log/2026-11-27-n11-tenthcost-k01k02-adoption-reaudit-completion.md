# 2026-11-27 n11 tenth-cost k01/k02 adoption flip-census + reaudit completion

Completion log of the tenth-cost k01/k02 adoption flip-census /
reaudit Part (pre-declared in the adoption completion log b4cefa42
"flip-census reaudit Part is next (k02 WIN win-hit review per ninth
precedent)" and in the adoption manifest status_guard field). Commit
chain: adoption declaration fecb961a -> adoption kit 3128558c (+
thirdimpl MANIFEST correction 309ed661) -> adoption completion
b4cefa42 -> flip-census + reaudit kit
`research/experiments/n11-tenthcost-k01k02-adoption-reaudit-20261127/`
(a50dc1af, 8 files + unpublished worklist pin, fetch-back 8/8
byte-identical).

## What was done

- Reaudit refresh: byte-clone of the published ninth-cost 12-row
  refresh c9a7372a... (3-region change only: docstring, CACHE path,
  expected sha 16b34014...), run THREE times, all four outputs
  byte-identical each time (~71s/run): refresh-summary.json
  40268a5e..., closure-classes.csv d7ae77dd..., per-root-coverage.csv
  8cc804bb..., probe-worklist.csv b9f3f1a3... (3,715,222 bytes,
  unpublished per size policy).
- Measurer: fresh structural adaptation of the ninth-cost 12-row
  measurer d81113df... with fresh 2-row expectations, THREE runs
  byte-identical (census json 7cb90af4... x3), all fail-closed gates
  PASS. Tamper battery 5/5 fail-closed + clean control re-PASS
  byte-identical.

## Measured results (BASE 47280073 -> SCEN 16b34014)

- Class census: unknown 34,393 -> 34,391; excluded_now 127 -> 129;
  free_now 39 -> 39 (Board-verified both sides, zero rejections);
  excluded 390 -> 390.
- WIN-side flips MEASURED: exactly 2 classes, the owner-class union
  of the single adopted WIN row k02 (s5 index 95628), each unknown ->
  excluded_now: class 2310 (the tenth-cost serving class
  1297036692683751424:131072, cost-unknown 100 -> 98, owns both
  adopted rows) and class 16665 (1152921504607895552:96).  No other
  flip direction; no free_now change.
- The LOSS row k01 (s5 index 95304, owner classes 2287/2310/12891)
  flips nothing: its other owner classes 2287 and 12891 keep their
  unknown status; the closure ladder is BYTE-IDENTICAL to the BASE
  side (804 rows, no entered/left, no unknown_now churn, no rank
  churn) and so is the per-root coverage (all 20 roots, no greedy
  re-route) - unlike the ninth-cost 12-row adoption, this 2-row
  adoption re-ranks nothing.  Joint greedy 37,398 -> 37,398; probing
  worklist rows 64,272 -> 64,272 (regen sha b9f3f1a3... differs from
  the BASE pin 396c05ae..., same 3,715,222 bytes).
- update8 refresh: both adopted s5 indices (95304, 95628) sit OUTSIDE
  the frozen baseline requirement, so resolved 282 -> 282,
  remaining_now 31,444 -> 31,444, groups_free_now 131 -> 131; win-hit
  group set unchanged (25 groups; neither flipped class is an
  update8 plan group class).

## Honest disclosures

- Execution preceded kit publication (Part pre-declared in b4cefa42);
  matches the disclosed ninth-cost 12-row reaudit precedent.
- The first refresh launch was a three-way PARALLEL run and was
  OOM-killed twice on this host (rc=137); all published bytes come
  from the sequential re-runs only (disclosed in the kit README).
- The first T5 tamper harness attempt truncated the closure file to
  zero rows (a python one-liner write-order defect) and was caught
  by the 804-row count gate; redone properly with a byte-verified
  phantom append, caught by the closure byte-identity gate.
- Raw-CDN fetch-back: the 6 non-README files 404'd for the first
  minutes after push (propagation delay), then verified 8/8
  byte-identical.
- No measurer expectation was violated by a measurement this time
  (the measured churn sets are empty, unlike the ninth class-1792
  leapfrog case); expectations were machine-derived from the first
  measurement run before the determinism runs.

## Meaning and resume

Adopting the two published tenth-cost rows changes solver-trusted S5
cache bookkeeping ONLY: no root verdict is consumed, no root freed,
no root excluded, no coverage claim changed.  The standard 11x11
empty board, all 19 central-reply roots, the two-stone root {60,27},
its remaining third moves {100,108}, S2 and all closure classes stay
UNKNOWN.  Nodes are bookkeeping, never verdicts.

Resume (re-fetch latest main before starting; hourly parallelism):
(a) the next selection/adoption-lane BASE is the new head of record
16b34014 (6,889 rows WIN 207 / LOSS 6,682); the next Part is a FRESH
selector run (tenth selector 0a45a650... as template, head reference
16b34014) to pick the eleventh-cost class; (b) the 42
escalation-suppressed tenth-cost keys (k03-k44 at 2M UNKNOWN) remain
fresh to the head and may be re-selected by a future selector under
the same class or others; (c) the tenth-cost serving class 2310
(1297036692683751424:131072) is now excluded_now, not re-selectable;
(d) verdict NOT consumed, 11x11 UNKNOWN.
