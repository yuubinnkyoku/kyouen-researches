# n11 eleventh-cost batch stage-1 sweep (2M cold pairs + 15M escalation, WIN-stopped)

Execution kit of the eleventh-cost batch declared in
`research/log/2026-11-27-n11-eleventhcost-batch-stage1-sweep-declaration.md`
(commit 8fbccf0b), for class `1297036696978718720:0` (46 exclusive
S5 keys, selected under canonical head of record 16b34014..., kit
research/experiments/n11-eleventhcost-class-s5-exclusive-probe-20261127).

## Results

- Stage-1 sweep: 46/46 keys UNKNOWN at the 2,000,000-budget cold pair
  (result 0, nodes 2,000,000; 46/46 cold pairs node-identical).
- 15M escalation (interleaved key order, WIN-stopping rule active):
  **k01 `1297036696978718720:64` resolves WIN(1) at nodes 12,755,963**
  (cold pair node-identical; raws at15m-k01-p1/p2.raw).  The WIN
  stopping rule fired: k02..k46 are escalation-suppressed and stay
  UNKNOWN at 2M (L50M parking candidates only if a future wave
  re-declares them; this batch claims nothing further).
- No overreach: no suppressed key was run at any higher budget.

## Pillar status (single implementation only)

All rows are single-implementation (Node.js replica jsreplay.js,
byte-clone of the published 84585617..., pinned in the selection kit).
The k01 WIN row requires the C++ second-implementation scrutiny gate
and a third-implementation corroboration (both separate future Parts)
before any adoption, and an adoption requires a WIN-side flip-census
review per the k12/k02/k07/k02-tenth precedent.  The verdict is NOT
consumed: the k01 row is cache bookkeeping, not a class closure, not
a root verdict, and transfers nothing.

## Files

- batch-summary.json - machine summary (schema
  n11-eleventhcost-batch-stage1-summary-v1), per-key at2m pairs and
  the k01 at15m pair, WIN-stop bookkeeping, disclosures, guards.
- raws/at2m-k01..k46-p1/p2.raw - 92 stage-1 raws (2M cold pairs).
- raws/at15m-k01-p1/p2.raw - the k01 15M escalation cold pair (WIN).
- MANIFEST-sha256.txt - sha256 of all 97 kit files.

## Meaning and non-meaning

Scheduling/batch bookkeeping only: NO verdict is claimed or implied.
Nodes are bookkeeping, never evidence of WIN or LOSS.  The standard
11x11 empty board, the two-stone root {60,27} and its remaining third
moves 100/108 stay UNKNOWN.
