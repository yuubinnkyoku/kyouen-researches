# n11 fifteenth ladder-top k02 L50M escalation (2026-11-28)

Execution kit of the L50M escalation declared in
`research/log/2026-11-28-n11-fifteenth-ladder-top-k02-l50m-declaration.md`
(publish-then-execute, declaration commit `5cc8e1fb`, single owner).
Escalates the single remaining cost-unknown child of the rank-1
closure-ladder class 5804, k02 `6052837899185946628:128`
(s5_index 212115, legal 87), from its published 15M budget-exhausted
UNKNOWN (re-escalation kit `09358acd`) to a 50,000,000-node budget,
against the canonical head of record `3a527d39...` (6,899 rows
WIN 217 / LOSS 6,682, adoption `bc535153`, reaudit `e6ceb133` +
completion `d7a91957`).

## Result

| key | published 15M | L50M escalation | pair |
|---|---|---|---|
| k02 `6052837899185946628:128` (s5_index 212115, legal 87) | UNKNOWN(0), nodes 15,000,000 (budget exhausted) | **WIN(1), nodes 18,247,029**, wall_s 98/102 | node-identical |

**k02 resolves WIN(1) at the 50M budget** (well inside the budget:
18,247,029 of 50,000,000 nodes).  The cold pair is
node-identical (result 1, nodes 18,247,029 both runs); the raw
files differ only in the wall_s field (98 vs 102), the same
host-footprint pattern as the published k02 15M pair.

Calibration (after the declaration, before the 50M runs): u01
`1153485622925590528:0` at 2M reproduces the published fifteenth
escalation kit's calibration raw (`05ce2090...`) BYTE-FOR-BYTE on
this host (result 0, nodes 2,000,000, forbidden quadruples 95,670,
wall_s 9).

## Claim status

This kit is escalation bookkeeping only: NO verdict is consumed.
The k02 WIN(1) row is single-implementation (jsreplay replica,
cold pair) and requires the C++ second-implementation scrutiny
gate plus a third-implementation corroboration before any
adoption Part; a k02 adoption would additionally require the
standing WIN-side flip-census review.  Class 5804 is ALREADY
excluded_now (k01/k03 WIN win-hit, measured by the published
reaudit kits `3395d0ec`/`e6ceb133`), so this result changes no
class-status bookkeeping; if k02 is later adopted after the
3-pillar chain, class 5804 would have zero cost-unknown children
and its closure-ladder exit would be measured then.  No free_now
flip is claimed here.  The standard 11x11 empty board, all 19
central-reply roots, the two-stone root {60,27} and third moves
100/108 remain UNKNOWN.  Nodes are bookkeeping, never verdicts.

## Files

- `DECLARATION.md` - mirror of the published declaration
  (commit `5cc8e1fb`).
- `batch-summary.json` - machine-readable summary (schema
  `n11-fifteenth-ladder-top-k02-l50m-summary-v1`), head basis,
  runner pin (jsreplay sha256 `84585617...`), calibration, 50M
  result, disclosures, status guard.
- `k02.input.csv`, `cal-u01.input.csv` - probe input rows,
  byte-verified copies of the published re-escalation kit's input
  files (`fda5d01d...` / `52d79efc...`).
- `raws/cal-u01-at2m.raw` - calibration raw, byte-identical to the
  published fifteenth escalation kit calibration raw
  (`05ce2090...`).
- `raws/at50m-k02-p1/p2.raw` - k02 50M cold pair, node-identical
  (wall_s 98/102).
- `MANIFEST-sha256.txt` - sha256 of every kit file.
