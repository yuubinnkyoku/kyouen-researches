# n11 ultra-cheap u01 adoption flip-census/reaudit: single-owner declaration

**Declaration (publish-then-execute).** This lane declares the
adoption follow-up reaudit Part for the ultra-cheap u01 WIN-row
canonical adoption (kit
`research/experiments/n11-ultra-cheap-u01-win-adoption-20261127`,
adoption commit `d4a9486f`, new head of record
`merged-exact-s5-chain-plus-ultra-cheap-u01-20261127.cache` sha256
`0ec4080da825a344a8dbbe0835da80dd506b06fa45f9f926b401d2387f3ed1e5`,
6,891 rows WIN 209 / LOSS 6,682).  Kit:
`research/experiments/n11-ultra-cheap-u01-adoption-reaudit-20261127`.

## Protocol

1. **Refresh**: `scripts/refresh_adoption_ultra_cheap_u01.py`
   (sha256 `d0fa17627705d816c248bbb28fb5c358dde79d11929bfffdcbb3eedd4199277c`)
   is a byte-clone of the published eleventh-cost k01 refresh
   (`0355d7fb...`, eleventh reaudit kit `2cd58330...`) differing in
   EXACTLY three regions (docstring, CACHE path, expected cache sha);
   the computation region is machine-verified byte-identical.  It is
   run three times sequentially (fresh cold) against ROOT inputs
   pinned by sha256: dependency graph `54f9c364...`, update8 plan
   `b658290a...`, independent Board `954d3a10...`, evidence policy
   `78655e94...`, quarantine `81d23160...`, SCEN cache `0ec4080d...`.
   The three output sets (`refresh-summary.json`,
   `closure-classes.csv`, `per-root-coverage.csv`) must be mutually
   byte-identical.
2. **Census measurement**: `scripts/measurer_adoption_ultra_cheap_u01.py`
   (structure-adapted from the eleventh measurer `f286f165...`) computes
   the class-status census deltas BASE (eleventh head `1e2eeda2...`)
   vs SCEN (`0ec4080d...`) plus a tamper battery.  Three fresh cold
   passes, byte-identical outputs, fail-closed.
3. Nothing else runs in this Part.

## Pre-registered expectation (disclosed before execution)

The single adopted row is a u01 WIN (owner class 1849).  By the
standing win-hit mechanism the class-status census is expected to
flip exactly one class from `unknown` to `excluded_now`:
unknown 34,388 -> 34,387, excluded_now 132 -> 133, free_now 39
unchanged (BASE census = the published eleventh reaudit values).  The
official numbers are the measured ones; a deviation is recorded as an
experimental fact, not silently adjusted.

## StandingUNKNOWN notice

The adopted row is an S5 solver-trusted WIN and transfers nothing to
any root or class verdict.  The standard 11x11 empty board and every
one of the 19 central-reply roots remain UNKNOWN.
