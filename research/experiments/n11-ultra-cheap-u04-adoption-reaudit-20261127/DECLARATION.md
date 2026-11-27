# n11 ultra-cheap u04 adoption flip-census/reaudit: single-owner declaration

**Declaration (publish-then-execute).** This lane declares the
adoption follow-up reaudit Part for the ultra-cheap u04 WIN-row
canonical adoption (kit
`research/experiments/n11-ultra-cheap-u04-win-adoption-20261127`,
adoption commits `ed1aab54`/`04b8c23a`, new head of record
`merged-exact-s5-chain-plus-ultra-cheap-u04-20261127.cache` sha256
`beecb024a648d0ddb29eaf261b09326f9412328cd09f85cb180ee2ffd9ed4544`,
6,894 rows WIN 212 / LOSS 6,682).  Kit:
`research/experiments/n11-ultra-cheap-u04-adoption-reaudit-20261127`.

## Protocol

1. **Refresh**: `refresh_adoption_ultra_cheap_u04.py` (sha256
   `db61c8505b122c0e99cd6c51ed10ab6c2920ec79c590580911650d7f461c0d49`)
   is a byte-clone of the published ultra-cheap u03 refresh
   (`84304650...`) differing in EXACTLY the three regions (this
   docstring, the CACHE path, the expected cache sha
   `beecb024...`); the computation region is machine-verified
   byte-identical (line diff = only the two CACHE/SHA config lines).
   It is run three times sequentially (fresh cold) against ROOT
   inputs pinned by sha256: dependency graph `54f9c364...`, update8
   plan `b658290a...`, independent Board `954d3a10...`, evidence
   policy `78655e94...`, quarantine `81d23160...`, SCEN cache
   `beecb024...`.  The three output sets (`refresh-summary.json`,
   `closure-classes.csv`, `per-root-coverage.csv`) must be
   mutually byte-identical.
2. **Census measurement**: a measurer structurally adapted from the u03
   measurer (`a86cf188...`) computes the class-status census deltas
   BASE (u03 head `c5082866...`, BASE side = the published u03
   reaudit outputs) vs SCEN (`beecb024...`) plus a tamper battery.
   Three fresh cold passes, byte-identical outputs, fail-closed.
   All expectation constants are MEASURED from the first execution
   run before publication (u02/u03 precedent).
3. Nothing else runs in this Part.

## Pre-registered expectation (disclosed before execution)

The single adopted row is a u04 WIN (serving class 23101, key
`1152921505747697664:1032`, s5 index 745184).  BEFORE execution the
owner class union of the adopted key was derived mechanically from the
frozen dependency graph `54f9c364...` (`745184 in s4_cost[ci]`): the
WIN key has exactly FOUR owner classes (the first 4-owner pattern in
the ultra-cheap family) - 23092 (`1152921505747697664:8`), 23101
(`1152921504892059648:16`, the serving class), 23115
(`1152921505680588800:1032`) and 23938
(`1152921504673955840:1032`).  Graph-derived naive prediction: each
flips `unknown` -> `excluded_now`, so unknown 34,380 -> 34,376,
excluded_now 140 -> 144, free_now 39 unchanged, excluded 390
unchanged (BASE census = the published u03 reaudit values
34,380/140/39/390).  Closure ladder 801 -> 800 rows expected IF the
serving class 23101 is still on the ladder with its last unknown cost
child resolved; probing worklist 64,266 -> 64,262 (the adopted key's
four membership rows leave).  **Caveat pre-disclosed**: the u03
adoption measured only 2 of 3 graph-derived flips because its serving
class was ALREADY excluded_now on the BASE head (win-hit predating
the adoption); the same pre-exclusion may reduce the u04 flip count.
Any deviation is recorded as an experimental fact, not silently
adjusted; the official numbers are the MEASURED ones.

## Standing UNKNOWN notice

The adopted row is an S5 solver-trusted WIN and transfers nothing to
any root or class verdict.  The standard 11x11 empty board and every
one of the 19 central-reply roots remain UNKNOWN.
