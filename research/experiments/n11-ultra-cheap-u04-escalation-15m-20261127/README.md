# n11 ultra-cheap u04 escalation (15M, single key)

Execution kit of the escalation declared in
`research/log/2026-11-27-n11-ultra-cheap-u04-escalation-declaration.md`
(commit `236db1b7`), covering the last remaining one-unknown
class-completion S5 key left UNKNOWN at 2M by the ultra-cheap batch
(`research/experiments/n11-ultra-cheap-batch-stage1-2m-20261127`) and
escalation-suppressed at the u03 escalation
(`research/experiments/n11-ultra-cheap-u03-escalation-15m-20261127`),
under the canonical head of record `c5082866...` (6,893 rows WIN 211 /
LOSS 6,682, fetched and sha-verified; the key verified fresh/absent).

## Results

- Declared scope: exactly one key, 15M budget, cold pair.
- **u04 `1152921505747697664:1032` (class 23101, legal 85, s5 index
  745184) resolves WIN(1) at nodes 9,149,084** (cold pair
  node-identical; both passes byte-identical incl. wall_s 49).
  Raw: `raws/at15m-u04-p1.raw`, `raws/at15m-u04-p2.raw`.
- This closes the four-key ultra-cheap family: u01 WIN(1) nodes
  4,893,014, u02 WIN(1) nodes 3,167,121, u03 WIN(1) nodes 2,909,040,
  u04 WIN(1) nodes 9,149,084 (all single-implementation until their
  pillars complete).
- No overreach: no other key was run at any budget in this Part.

## Pillar status (single implementation only)

The u04 WIN row is single-implementation (Node.js replica jsreplay.js
sha256 `84585617...`, byte-verified at assembly; not republished
here).  Before any adoption it requires the C++
second-implementation scrutiny gate and a third-implementation
corroboration (separate Parts); a u04 adoption would additionally
require the standing WIN-side flip-census review.  The verdict is NOT
consumed: the u04 row is cache bookkeeping, not a class closure, not
a root verdict, and transfers nothing.

## Calibration (pre-declaration, disclosed in the declaration)

One 2M cold run of u01 (`1153485622925590528:0`) reproducing the
published values exactly: result 0, nodes 2,000,000, forbidden
quadruples 95,670, wall_s 9; published as `raws/cal-u01-at2m.raw`,
which is byte-identical to the u03 escalation kit's published
calibration raw.

## Files

- batch-summary.json - machine summary (schema
  n11-ultra-cheap-u04-escalation-summary-v1).
- input/u04.input.csv - the u04 probe input row (byte-verified against
  the published batch kit input, sha256
  e09332d76bd506e7a6613e29411fbd06b55135389c02260727336375c3fb6479).
- raws/at15m-u04-p1.raw, raws/at15m-u04-p2.raw - the u04 cold pair.
- raws/cal-u01-at2m.raw - the disclosed calibration run.
- MANIFEST-sha256.txt - sha256 of every published file (excluding
  itself).

## Status guard

Scheduling/batch bookkeeping only; NO verdict consumed.  The standard
11x11 empty board, the two-stone root {60,27} and its remaining
third moves 100/108 stay UNKNOWN.
