# n11 ultra-cheap u02 adoption flip-census/reaudit: single-owner declaration

**Declaration (publish-then-execute).** This lane declares the
adoption follow-up reaudit Part for the ultra-cheap u02 WIN-row
canonical adoption (kit
`research/experiments/n11-ultra-cheap-u02-win-adoption-20261127`,
adoption commit `612cb3c2`, new head of record
`merged-exact-s5-chain-plus-ultra-cheap-u02-20261127.cache` sha256
`82b525777843ecb44c3857b034f7a135284c2587b42dbaa94aa295b01adc7509`,
6,892 rows WIN 210 / LOSS 6,682).  Kit:
`research/experiments/n11-ultra-cheap-u02-adoption-reaudit-20261127`.

## Protocol

1. **Refresh**: `scripts/refresh_adoption_ultra_cheap_u02.py`
   (sha256 `525a130d4597e3438baa41ea8802777cd2729edca6b841246ff5f7cf3c07a3db`)
   is a byte-clone of the published ultra-cheap u01 refresh
   (`d0fa1762...`, u01 reaudit kit `5ba55c96`) differing in EXACTLY
   three regions (docstring, CACHE path, expected cache sha); the
   computation region is machine-verified byte-identical (line diff =
   only the two CACHE/SHA config lines).  It is run three times
   sequentially (fresh cold) against ROOT inputs pinned by sha256:
   dependency graph `54f9c364...`, update8 plan `b658290a...`,
   independent Board `954d3a10...`, evidence policy `78655e94...`,
   quarantine `81d23160...`, SCEN cache `82b52577...`.  The three
   output sets (`refresh-summary.json`, `closure-classes.csv`,
   `per-root-coverage.csv`) must be mutually byte-identical.
2. **Census measurement**: a measurer structurally adapted from the u01
   measurer (`c5ff4883...`) computes the class-status census deltas
   BASE (u01 head `0ec4080d...`, BASE side = the published u01 reaudit
   outputs) vs SCEN (`82b52577...`) plus a tamper battery.  Three fresh
   cold passes, byte-identical outputs, fail-closed.
3. Nothing else runs in this Part.

## Pre-registered expectation (disclosed before execution)

The single adopted row is a u02 WIN (serving class 2251).  By the
standing win-hit mechanism the class-status census is expected to flip
the WIN key's owner classes from `unknown` to `excluded_now`.  Naive
single-owner prediction: unknown 34,385 -> 34,384, excluded_now 135 ->
136, free_now 39 unchanged (BASE census = the published u01 reaudit
values).  **Caveat pre-disclosed**: at the u01 adoption the WIN key
turned out to have THREE owner classes (measured unknown 34,388 ->
34,385, excluded_now 132 -> 135, a recorded deviation from the
single-owner prediction), so the official numbers are the MEASURED
ones; any deviation from this prediction is recorded as an
experimental fact, not silently adjusted.

## Standing UNKNOWN notice

The adopted row is an S5 solver-trusted WIN and transfers nothing to
any root or class verdict.  The standard 11x11 empty board and every
one of the 19 central-reply roots remain UNKNOWN.
