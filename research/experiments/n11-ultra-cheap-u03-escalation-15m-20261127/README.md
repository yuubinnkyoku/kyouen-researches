# n11 ultra-cheap u03 escalation (15M, WIN-stopped)

Execution kit of the escalation declared in
`research/log/2026-11-27-n11-ultra-cheap-u03u04-escalation-declaration.md`
(commit `fd41e986`), covering the two remaining one-unknown
class-completion S5 keys left UNKNOWN at 2M by the ultra-cheap batch
(`research/experiments/n11-ultra-cheap-batch-stage1-2m-20261127`) and
escalation-suppressed at the u02 escalation
(`research/experiments/n11-ultra-cheap-u02-escalation-15m-20261127`),
under the canonical head of record `82b52577...` (6,892 rows WIN 210 /
LOSS 6,682, fetched and sha-verified; both keys verified fresh/absent).

## Results

- Declared order u03 -> u04, 15M budget, cold pair per key,
  WIN-stop rule active.
- **u03 `1153202979851993088:272` (class 16371, legal 78, s5 index
  550879) resolves WIN(1) at nodes 2,909,040** (cold pair
  node-identical; both passes byte-identical incl. wall_s 13).
  Raw: `raws/at15m-u03-p1.raw`, `raws/at15m-u03-p2.raw`.
- The WIN-stop rule fired at u03: **u04
  (`1152921505747697664:1032`) is escalation-suppressed and stays
  UNKNOWN at 2M** (parking/L50M only under a future declaration).
- No overreach: no suppressed key was run at any budget in this Part.

## Pillar status (single implementation only)

The u03 WIN row is single-implementation (Node.js replica jsreplay.js
sha256 `84585617...`, byte-verified at assembly; not republished
here).  Before any adoption it requires the C++
second-implementation scrutiny gate and a third-implementation
corroboration (separate Parts); a u03 adoption would additionally
require the standing WIN-side flip-census review (class 16371
completion would be Board-verified free_now at adoption time).  The
verdict is NOT consumed: the u03 row is cache bookkeeping, not a
class closure, not a root verdict, and transfers nothing.

## Calibration (pre-declaration, disclosed in the declaration)

One 2M cold run of u01 (`1153485622925590528:0`) reproducing the
published stage-1 raw exactly (result 0, nodes 2,000,000, forbidden
quadruples 95,670); published as `raws/cal-u01-at2m.raw`.  The
declaration disclosed wall_s 10 from the pre-declaration observation;
the published raw records wall_s 9 from the kit-assembly rerun (same
result/nodes) - host wall-clock variance, disclosed in
batch-summary.json.

## Files

- batch-summary.json - machine summary (schema
  n11-ultra-cheap-u03-escalation-summary-v1).
- input/u03.input.csv - the u03 probe input row (byte-verified against
  the published batch kit input).
- raws/at15m-u03-p1.raw, raws/at15m-u03-p2.raw - the u03 cold pair.
- raws/cal-u01-at2m.raw - the disclosed calibration run.
- MANIFEST-sha256.txt - sha256 of every published file (excluding
  itself).

## Status guard

Scheduling/batch bookkeeping only; NO verdict consumed.  The standard
11x11 empty board, the two-stone root {60,27} and its remaining
third moves 100/108 stay UNKNOWN.
