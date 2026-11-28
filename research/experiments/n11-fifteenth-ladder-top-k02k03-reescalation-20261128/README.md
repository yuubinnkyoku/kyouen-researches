# n11 fifteenth class 5804 k02/k03 re-escalation (2026-11-28)

Execution kit of the re-escalation declared in
`research/log/2026-11-28-n11-fifteenth-ladder-top-k02k03-reescalation-declaration.md`
(publish-then-execute, declaration commit `88a24418`, single owner).
Re-escalates the two WIN-stop-suppressed keys of the published
fifteenth ladder-top escalation kit
(`research/experiments/n11-fifteenth-ladder-top-escalation-20261128`,
commit `a33217ca`) against the canonical head of record `b5f322dd...`
(6,898 rows WIN 216 / LOSS 6,682); both keys verified fresh to the
head before any run.

## Result

Declared order: k02 first; k03 only if k02 does not resolve WIN(1).

| key | stage-1 2M (published) | 15M re-escalation | pair |
|---|---|---|---|
| k02 `6052837899185946628:128` (s5_index 212115, legal 87) | UNKNOWN(0), nodes 2,000,000 | **UNKNOWN(0), nodes 15,000,000** (budget exhausted), wall_s 80/80 | node-identical |
| k03 `6053400849139367936:128` (s5_index 212536, legal 92) | UNKNOWN(0), nodes 2,000,000 | **WIN(1), nodes 3,364,655**, wall_s 15/15 | byte-identical |

The WIN-stop rule was re-affirmed but did NOT fire: k02 stayed
UNKNOWN at 15M, so k03 escalated per the declared order and
resolved WIN(1). k02 stays UNKNOWN (parking/L50M only under a
future declaration). Class 5804 was ALREADY excluded_now (k01 WIN
win-hit, measured by the published fifteenth reaudit kit
`3395d0ec`), so these results change no class-status bookkeeping;
the class is NOT complete (k02 remains unknown).

Calibration (after the declaration, before the 15M runs): u01
`1153485622925590528:0` at 2M reproduces the published fifteenth
escalation kit's calibration raw VALUES exactly (result 0, nodes
2,000,000, forbidden quadruples 95,670, wall_s 9); only stdout
footer line ordering differs (host buffering), so the raw file sha
differs while no values differ.

## Claim status

This kit is re-escalation bookkeeping only: NO verdict is
consumed. The k03 WIN(1) row is single-implementation (jsreplay
replica, cold pair) and requires the C++ second-implementation
scrutiny gate plus a third-implementation corroboration before
any adoption Part; a k03 adoption would additionally require the
standing WIN-side flip-census review. No free_now flip is claimed.
The standard 11x11 empty board, all 19 central-reply roots, the
two-stone root {60,27} and third moves 100/108 remain UNKNOWN.

## Files

- `DECLARATION.md` - mirror of the published declaration
  (commit `88a24418`).
- `batch-summary.json` - machine-readable summary (schema
  `n11-fifteenth-ladder-top-k02k03-reescalation-summary-v1`), head
  basis, runner pin (jsreplay sha256 `84585617...`), declared
  order, calibration, 15M results, WIN-stop non-firing,
  disclosures, status guard.
- `k02.input.csv`, `k03.input.csv`, `cal-u01.input.csv` - probe
  input rows, byte-verified copies of the published fifteenth
  escalation kit's input files.
- `raws/cal-u01-at2m.raw` - calibration raw (host footer order;
  values identical to the published calibration).
- `raws/at15m-k02-p1/p2.raw` - k02 15M cold pair,
  node-identical (wall_s 80/80).
- `raws/at15m-k03-p1/p2.raw` - k03 15M cold pair,
  byte-identical.
- `MANIFEST-sha256.txt` - sha256 of every kit file.
