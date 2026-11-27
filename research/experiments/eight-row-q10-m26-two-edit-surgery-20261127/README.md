# Eight-row q=10, 8x26: complete two-edit surgery, negative (2026-11-27 fast lane)

Single-owner lane declared in
`research/log/2026-11-27-eight-row-q10-m26-two-edit-surgery-declaration.md`
(declaration-time observed HEAD `a48a7d777ee3b8f1b9729d190ba3fc1d73c75dd8`;
declaration commit `17ddb2d5`). Preliminary census probe disclosed there.

## Headline result

- The complete two-edit neighborhood (S' = seed - R + A, |R| <= 2,
  |A| <= 2, final size <= 71 = 8x9 - 1, A on empty cells, target occupied
  or blocked) of the published 8x25 m=25 witness (71 stones, rows
  [9,9,9,8,9,9,9,9], `eight-row-bands-20261114/.../s8x25q10_none.witness.json`,
  sha256 `051be05c9c2c41a19a3cfe0fad0ad2fad63c15505df89fbe7b72f7fa54cfd9d`) on
  the **8x26 board** targeting the unique uncovered cell **T=(25,3)**
  contains **no safe row-deficient maximal configuration**:
  - **4,659,859 unique candidates, 0 safe, 0 safe-maximal witnesses.**
- The seed is one-stone-short on 8x26: the ONLY uncovered cell of the
  transplanted witness is (25,3). T-curve census c7=0, c8=1 (the c8
  T-curve is the row-3 line y=3 carrying the 8 stones of row 3;
  empty_on=17). Blocking threshold is 9.
- This is a **local negative only**: no 8x26 witness within edit distance
  <= 2 of the m=25 seed. NOT an absence claim for 8x26 (the published
  SAT encodings s8x26q10_none / rowY3 / rowY3lexH / rowY4 all remain
  INDET; m=27..39 probed INDET or unswept). **M_{8,10} stays in
  [26, 940]** (lower eight-row-bands m=25 witness; upper U_{8,10}=940
  curve-packing). Frontier stays 8x26.

## Engine (v2 streaming, disclosed adaptation)

- The published engine `scripts/surgery_general.py` (sha256 `8ae82dde...`,
  byte-identical to the 6x26 and 6x22 kit engines) materializes the global
  candidate set; on 8x26 q10 that set (~4.7M pairs) exceeds sandbox memory
  (the first official attempt with the published engine was killed by the
  OOM reaper at 36s; disclosed in the run stdout trail).
- `scripts/surgery_stream.py` (this kit, sha256 in MANIFEST) streams
  per-R: for each removal set R the additions A are collected in a small
  per-R set (exact dedup: a duplicate (R, A) can only arise within the
  same R), checked, and discarded. Candidate semantics identical; the
  only further differences are chunking (partitions the sorted R list)
  and the sample dump (deterministic reservoir sampling, seed 20261127).
  All other code (curve construction, thresholds, safe_and_max) is
  byte-copied from the published engine.
- **Calibration (exact)**: the streaming engine reproduces the published
  7x32 q=6 m=31 surgery counters exactly: 2,224,675 candidates / 0 safe /
  0 witnesses, 11s (`output/calib-m32-stream.json`).
- **Determinism**: official run1 = run2 byte-identical (sha256
  `c2d8b30af1835668d84bfdf3f4f1e2212734a2eb25e5d4ab01f705077f250348`
  for both `surgery-m26.run1.json` and `surgery-m26.run2.json`).

## Controls

- **Independent spot-check**: `scripts/spotcheck_int.py` (byte-identical
  to the published method-disjoint integer-conic re-checker, sha256
  `8f57d6b0...`) on the 300-candidate reservoir sample, chunks
  100/100/100: 300/300 engine rejections confirmed, 0 missed witnesses
  (`output/spotcheck-summary.json`).
- **Tamper battery** (`output/tamper/tamper-summary.json`): T1 blocked
  target -> fail-closed; T2 unsafe seed (stone at (0,0) completing a
  10-stone row-0 line) -> fail-closed; T3b weakened blocking gate
  (Q-1 -> Q-3, chunk 0:16, witness recording capped at 5) -> fail-loud
  (15,727 spurious in the chunk vs official 0). Honest note: an uncapped
  full-scan T3b attempt exhausted sandbox memory and forced an
  environment reset (recorded in the declaration-completion log); the
  published T3b is the bounded run.

## Honest disclosures

- Preliminary census probe (uncovered-cell identification, T-curve
  census, one OOM-killed enumeration attempt with the published engine)
  ran before the declaration and is disclosed there and here. All
  recorded runs (calibration, determinism pair, sample, spot-check,
  tamper) ran after the declaration commit `17ddb2d5`.
- No m=24 witness is published for this family, so no rediscovery
  positive control is available (disclosed in the declaration).
- 11x11 empty board, two-stone roots, third move, S2, closure classes:
  UNKNOWN at all times; verdicts not consumed; candidate/safe counts are
  bookkeeping.

## Outputs

- `output/m25.witness.stones.json`: seed stones (transplanted coordinates).
- `output/calib-m32-stream.json` + stdout: calibration record.
- `output/surgery-m26.run1.json` (+ stdout + 300-line reservoir sample) and
  `output/surgery-m26.run2.json` (+ stdout): official runs.
- `output/spotcheck.{0,1,2}.txt`, `output/spotcheck-summary.json`,
  `output/tamper/*`: control records.

## Reproduction

```sh
python3 scripts/surgery_stream.py --bx 32 --by 7 --q 6 --target 31,3 \
  --seed m31.stones.json --out calib.json          # must give 2224675/0/0
python3 scripts/surgery_stream.py --bx 26 --by 8 --q 10 --target 25,3 \
  --seed output/m25.witness.stones.json --out run1.json --sample 300
python3 scripts/spotcheck_int.py run1.json run1.json.sample.jsonl 300 0 100
# (chunks 0/100/100 and 100/100 and 200/100)
```
