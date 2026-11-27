# n11 twelfth-cost ladder pre-audit kit (2026-11-27)

Pre-registered independent audit instrument for the twelfth-cost
(第12コスト) exclusive S5 ladder of the 11x11 two-stone-root campaign.
Published BEFORE the batch stage-1 sweep raws (wave B of single-owner
declaration `f6d29d16`) exist, so that the content invariants the raws
will be held to are on record first. This lane does NOT run the sweep:
the 51-key batch remains owned by the declaring lane.

## What this kit contains

- `scripts/audit_twelfth_ladder.py` — fresh two-stage auditor.
  - Stage S (runnable now): byte pins of the selection kit
    (`n11-twelfthcost-class-s5-exclusive-probe-20261127`, commit
    `e588de1e`): selection json sha256 `1119d01b...`, selector
    `ea2b8331...`, jsreplay `84585617...`, kit README `74131df1...`,
    wave-A declaration log `395cbeac...`, head of record `1e2eeda2...`
    (6,890 rows WIN 208 / LOSS 6,682); selection content gates (schema,
    class `10376293541461626880:16777216`, 51 unique keys, first/last
    key, bands 5,041,585 x1 / 5,069,670 x1 / 5,234,938 x11 /
    5,932,112 x38, proxy_exclusive_sum 293,115,829 recomputed from
    entries); all 51 input CSVs verified against the kit MANIFEST and
    for order+legal fidelity against the authoritative
    exclusive_probe_order; head census + 51-key freshness (all absent).
  - Stage B (pre-registered, auto-activates when
    `<kit>/output/raw/` is populated): B1 raw keys subset of the 51,
    B2 stage-1 two 2M rows per key, B3 result semantics
    (result 0 requires nodes==budget; WIN=1 / exact LOSS=2 require
    nodes<=budget), B4 escalation only for stage-1 UNKNOWN keys,
    B5 WIN-stop content rule (no escalated rows after the first
    escalating WIN except ledger-marked overreach, ninth/eighth
    precedent), B6 cold-pair node identity per (key,budget).
- `output/twelfth-preaudit-run{1,2,3}.json` + `output/stdout-run{1,2,3}.txt`
  — three cold clean passes, byte-identical (deterministic).
- `output/preaudit-summary.json` — clean run, tamper battery T1..T5,
  and the synthetic batch-stage mock self-test results.
- `MANIFEST-sha256.txt` — sha256 of every file in this kit.

## Inputs (published elsewhere in this repo, not duplicated here)

- Selection kit: `research/experiments/n11-twelfthcost-class-s5-exclusive-probe-20261127/`
  (all 55 files sha-verified against its MANIFEST in-run).
- Head of record: `research/experiments/n11-eleventhcost-k01-win-adoption-20261127/output/merged/merged-exact-s5-chain-plus-eleventhcost-k01-20261127.cache`
  (sha256 `1e2eeda2...`, 288,584 B).
- Declaration: `research/log/2026-11-27-n11-twelfthcost-batch-stage1-sweep-declaration.md`
  (sha256 `395cbeac...`).

## How to run

```bash
python3 scripts/audit_twelfth_ladder.py <selkit-dir> <head.cache> <declaration.md> <out.json>
```

`<selkit-dir>` is a local copy of the selection experiment directory
(with its 51 input CSVs and MANIFEST). When the wave-B raws land, the
same command with the raws under `<selkit-dir>/output/raw/` activates
the six B-gates automatically.

## Results

- Clean run: rc=0, 34 gates (28 PASS + 6 batch gates PREREGISTERED
  because the wave-B raws are absent at publication time), three cold
  passes byte-identical. Run json sha256 `006760b4ca967c8d5dc62955e659f380dc3fadf9f02f4d036bb3df59f58d196d`.
- Tamper battery 5/5 fail-closed: T1 input CSV legal flip,
  T2 phantom head row, T3 declaration one-char edit, T4 selection json
  key digit flip, T5 k03/k04 CSV swap. Clean control re-PASS
  byte-identical. Disclosures: the first T1 attempt was a silent sed
  no-op (k07 legal is 97, not 88) redone with a byte-diff-verified
  edit; T4 exits rc=1 fail-closed but ungracefully (JSONDecodeError
  after the sha gate already failed, no gate JSON emitted).
- Batch-stage mock self-test (synthetic raws, NOT published as data):
  a WIN-stop violation (15M row for k03 after a 15M WIN at k02) is
  caught by B5 (rc=1); a clean mock passes all six B-gates (rc=0).
  The mock caught and fixed a real stage-B bug before publication
  (the escalation-order map was keyed by key string while the raw
  grouping is keyed by (lo,hi) tuple; fixed, stage-S output unchanged).

## Meaning and non-meaning

Audit bookkeeping only: NO verdict is claimed or consumed. Nodes and
proxy values are never evidence of WIN or LOSS. The standard 11x11
empty board: UNKNOWN. All 19 central-reply roots: UNKNOWN. The
two-stone root {60,27} and its remaining third moves 100/108: UNKNOWN.

## Honest disclosures

- This lane runs without access to the user's computer (scheduled
  task); publication is via the GitHub API only.
- All pinned inputs were fetched from main and byte-verified against
  the published sha256 pins before the runs (head cache 288,584 B
  included).
- The batch stage-1 sweep itself is NOT executed by this lane
  (single-owner declaration `f6d29d16` respected); the 51 twelfth-cost
  keys have not been run here.
