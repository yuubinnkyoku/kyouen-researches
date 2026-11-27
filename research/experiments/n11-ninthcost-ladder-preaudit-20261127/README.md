# n11 ninth-cost ladder pre-audit kit (2026-11-27)

Independent verification harness for the ninth-cost (第9コスト) ladder of the
11x11 two-stone-root campaign, after the parked-3 L50M escalation completed
(wave A declaration `59db0d52`, wave B raw publication `41b331d1`).

## What this kit contains

- `scripts/audit_ninth_ladder.py` — fresh third-stage auditor for the ninth
  ladder. Multi-stage modeling (byte-level manifest check, per-key pair
  identity, ledger==raw cross-check, head census, provenance pins), 527 gates.
- `output/ninth-preaudit-run1.json` — full gate-by-gate result of the clean
  run (sha256 `a3ff228d558fc9e123f16d2f9b1e2b2c4c31feae16adf629cd39bf97d6df3fc1`).
  Three cold passes produced byte-identical JSON (deterministic).
- `output/stdout-run{1,2,3}.txt` — stdout of the three clean passes
  (byte-identical to each other).
- `output/preaudit-summary.json` — summary of the clean run and the tamper
  battery (T1..T5), each tamper expected to fail-closed.
- `MANIFEST-sha256.txt` — sha256 of every file in this kit.

## Inputs (published elsewhere in this repo, not duplicated here)

- Raw pair outputs and ledgers:
  `research/experiments/n11-ninthcost-class-s5-exclusive-probe-1297036692683751424-20261127/`
  (raw 116 + 6 points, `MANIFEST-raw-sha256.txt` 122 lines).
- Head of record: `head.cache` at commit `0935c94c` (6875 lines, WIN203/LOSS6672).
- jsreplay engine pin `84585617...`; node v22.20.0.

## How to run

```bash
python3 scripts/audit_ninth_ladder.py <kit9-dir> <head-cache-file> <out.json>
```

where `<kit9-dir>` is a local checkout of the probe experiment directory
(`output/raw/...`, ledgers, `MANIFEST-raw-sha256.txt`).

## Results

- Clean run: rc=0, overall PASS, 527 gates, byte-identical across 3 passes.
- Tamper battery (all fail-closed as expected):
  - T1 k02 50m raw nodes 18123017->18123018: rc=1, FAIL
    `P1:manifest-sha-all`, `P3:k02:50m-pair-identity`, `P4:k02:50m-ledger==raw`.
  - T2 phantom k13 50m raw file: rc=1, FAIL `P1:manifest-sha-all`.
  - T3 batch-summary-l50m result flip (byte-verified flip, not sed):
    rc=1, FAIL `P5:batch-summary==ledger`.
  - T4 head.cache append: rc=1, FAIL `P0:head-census` (first).
  - T5 k12 15m WIN flip: rc=1, FAIL `P3:k12:15m-pair-identity` (first).

## Disclosure

- The 3 newly solved rows (k02 WIN 18123017, k04 LOSS 24309957, k07 WIN
  27621128) come from a single implementation and transfer nothing until
  third-implementation corroboration and C++ gate declaration are complete.
- The standard 11x11 empty board, 19 central-reply roots, two-stone root
  {60,27}, third move {100,108}, and all closure classes remain UNKNOWN.
  Verdicts are not consumed; node counts are bookkeeping only.
