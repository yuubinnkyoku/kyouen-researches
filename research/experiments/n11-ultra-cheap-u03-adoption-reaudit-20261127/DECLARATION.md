# n11 ultra-cheap u03 adoption flip-census/reaudit: single-owner declaration

**Declaration (publish-then-execute).** This lane declares the
adoption follow-up reaudit Part for the ultra-cheap u03 WIN-row
canonical adoption (kit
`research/experiments/n11-ultra-cheap-u03-win-adoption-20261127`,
adoption commit `ab50c3ca`, new head of record
`merged-exact-s5-chain-plus-ultra-cheap-u03-20261127.cache` sha256
`c5082866c1bb61e9cbcb86b80b29c3b2a141b4b5e93a0b8d4b46e04151b631c8`,
6,893 rows WIN 211 / LOSS 6,682).  Kit:
`research/experiments/n11-ultra-cheap-u03-adoption-reaudit-20261127`.

## Protocol

1. **Refresh**: `scripts/refresh_adoption_ultra_cheap_u03.py`
   (sha256 `84304650fd365c9c3a58dbc0a0efc85fe2c76056b167eaa4c59fcac60fb8fe2e`)
   is a byte-clone of the published ultra-cheap u02 refresh
   (`525a130d...`, u02 reaudit declaration line) differing in EXACTLY
   three regions (docstring, CACHE path, expected cache sha); the
   computation region is machine-verified byte-identical (line diff =
   only the two CACHE/SHA config lines).  It is run three times
   sequentially (fresh cold) against ROOT inputs pinned by sha256:
   dependency graph `54f9c364...`, update8 plan `b658290a...`,
   independent Board `954d3a10...`, evidence policy `78655e94...`,
   quarantine `81d23160...`, SCEN cache `c5082866...`.  The three
   output sets (`refresh-summary.json`, `closure-classes.csv`,
   `per-root-coverage.csv`) must be mutually byte-identical.
2. **Census measurement**: a measurer structurally adapted from the u02
   measurer (`e3df6a73...`) computes the class-status census deltas
   BASE (u02 head `82b52577...`, BASE side = the published u02 reaudit
   outputs) vs SCEN (`c5082866...`) plus a tamper battery.  Three fresh
   cold passes, byte-identical outputs, fail-closed.
3. Nothing else runs in this Part.

## Pre-registered expectation (disclosed before execution)

The single adopted row is a u03 WIN (serving class 16371, key
`1153202979851993088:272`, s5 index 550879).  BEFORE execution the
owner class union of the adopted key was derived mechanically from the
frozen dependency graph `54f9c364...` (`550879 in s4_cost[ci]`): the
WIN key has exactly THREE owner classes, 16371 (the serving class
`1153202979851993088:16`), 16404 (`1154047404580798464:64`) and 16930
(`1152921504875282432:272`).  Graph-derived prediction: each flips
`unknown` -> `excluded_now`, so unknown 34,382 -> 34,379,
excluded_now 138 -> 141, free_now 39 unchanged, excluded 390 unchanged
(BASE census = the published u02 reaudit values 34,382/138/39/390).
Closure ladder 802 -> 801 rows (the serving class 16371, BASE rank 1
unknown_now 1, leaves the ladder); unknown_now churn expected at 16930
(52 -> 51) and 16404; probing worklist 64,268 -> 64,267 (the adopted
key's probe row leaves).  **Caveat pre-disclosed**: the u01 and u02
adoptions both measured the 3-owner pattern after naive single-owner
predictions; here the prediction is graph-derived, but any deviation
is recorded as an experimental fact, not silently adjusted; the
official numbers are the MEASURED ones.

## Standing UNKNOWN notice

The adopted row is an S5 solver-trusted WIN and transfers nothing to
any root or class verdict.  The standard 11x11 empty board and every
one of the 19 central-reply roots remain UNKNOWN.
