# n11 ultra-cheap u02 escalation (15M, WIN-stopped)

Execution kit of the escalation declared in
`research/log/2026-11-27-n11-ultra-cheap-u02u03u04-escalation-declaration.md`
(commit `37f1e9f6`), covering the three remaining one-unknown
class-completion S5 keys left UNKNOWN at 2M by the ultra-cheap batch
(`research/experiments/n11-ultra-cheap-batch-stage1-2m-20261127`), under the
canonical head of record `0ec4080d...` (6,891 rows WIN 209 / LOSS 6,682,
fetched and sha-verified; all three keys verified fresh/absent).

## Results

- Declared order u02 -> u03 -> u04, 15M budget, cold pair per key,
  WIN-stop rule active.
- **u02 `1297036830121656320:131074` (class 2251, legal 80, s5 index
  93815) resolves WIN(1) at nodes 3,167,121** (cold pair node-identical;
  both passes byte-identical incl. wall_s 15).  Raw: `raws/at15m-u02-p1.raw`,
  `raws/at15m-u02-p2.raw`.
- The WIN-stop rule fired at u02: **u03 (`1153202979851993088:272`) and
  u04 (`1152921505747697664:1032`) are escalation-suppressed and stay
  UNKNOWN at 2M** (parking/L50M only under a future declaration).
- No overreach: no suppressed key was run at any budget in this Part.

## Pillar status (single implementation only)

The u02 WIN row is single-implementation (Node.js replica jsreplay.js,
byte-clone of the published `84585617...`, sha-verified at assembly; not
republished here).  Before any adoption it requires the C++
second-implementation scrutiny gate and a third-implementation
corroboration (separate Parts); a u02 adoption would additionally require
the standing WIN-side flip-census review (class 2251 completion would be
Board-verified free_now at adoption time).  The verdict is NOT consumed:
the u02 row is cache bookkeeping, not a class closure, not a root
verdict, and transfers nothing.

## Calibration (pre-declaration, disclosed in the declaration)

One 2M cold run of u01 (`1153485622925590528:0`) reproducing the
published stage-1 raw exactly (result 0, nodes 2,000,000, wall_s 9,
forbidden quadruples 95,670); published as `raws/cal-u01-at2m.raw`.

## Files

- batch-summary.json - machine summary (schema
  n11-ultra-cheap-u02-escalation-summary-v1).
- input/u02.input.csv - the u02 probe input row (byte-clone of the
  published batch kit input).
- raws/at15m-u02-p1.raw, raws/at15m-u02-p2.raw - the 15M escalation cold
  pair (WIN).
- raws/cal-u01-at2m.raw - pre-declaration calibration raw (disclosed).
- MANIFEST-sha256.txt - sha256 of every file in this kit.

## Meaning and non-meaning

Scheduling/batch bookkeeping only: NO verdict is claimed or implied.
Nodes are bookkeeping, never evidence of WIN or LOSS.  The standard 11x11
empty board, the two-stone root {60,27} and its remaining third moves
100/108 stay UNKNOWN.
