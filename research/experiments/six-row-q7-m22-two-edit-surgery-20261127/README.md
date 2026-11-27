# Six-row q=7, 6x22: complete two-edit surgery, negative (2026-11-27 fast lane)

Single-owner lane declared in
`research/log/2026-11-27-six-row-q7-m22-two-edit-surgery-declaration.md`
(declaration-time HEAD `8170398137fa74710e9b5fb44fb6a8c596f839b8`; declaration
commit `ab8134bc`).

## Headline result

- The complete two-edit neighborhood (S' = seed - R + A, |R| <= 2, |A| <= 2,
  final size <= 35, A on empty cells, target occupied or blocked) of the
  published 6x21 K0815-7th witness (35 stones, rows [6,6,5,6,6,6],
  `six-row-q7-m21-class-split-20261114/output/w67_21.json`, sha256
  `5f01a133ab2d51ef1a02506ef3be8f655c2cf2e46e548bc77dc08603a3203168`) on the
  **6x22 board** targeting the unique uncovered cell **T=(21,2)** contains
  **no safe row-deficient maximal configuration**:
  - 692,655 unique candidates, 0 safe, 0 safe-maximal witnesses.
- The seed is one-stone-short on 6x22: the ONLY uncovered cell of the
  transplanted witness is (21,2). T-curve census c4=3, c5=1 (the c5 T-curve
  is the row-2 line y=2 carrying 5 stones; blocking threshold is 6).
- This is a **local negative only**: no 6x22 witness within edit distance
  <= 2 of the m=21 seed. NOT an absence claim for 6x22 (the K0815 class {2}
  280s kissat INDET stays the frontier status). **M_{6,7} stays in
  [22, 402]** (lower bound K0815, upper K0806/K0318 unchanged).
- Measured observation: the m=21 witness is at symmetric difference 40
  (>= 20 stone moves) from the m=20 witness over all 4 flip images x all
  translations, so no rediscovery control from m=20 is possible.

## Completeness argument

Same q-generalized case split as the 6x26 kit (q=7: safety >= 7, blocking
>= 6, T-curves with c in {4,5}, need = 6 - (c - t) <= 2 given |A| <= 2 and
|C n S'| >= 6 requiring >= 4 seed stones on the curve). Final size <= 35
keeps deficiency (36 = all rows at capacity 6 is non-deficient; 37+ needs a
7-stone row = unsafe). Full argument in the 6x26 kit README; the engine is
the same byte (sha-pinned in MANIFEST) with only the CLI parameters
differing.

## Engine, calibration, controls

- `scripts/surgery_general.py`: byte-identical to the engine published in
  `six-row-q6-m26-two-edit-surgery-20261127` (sha256 in MANIFEST; compare
  with that kit's MANIFEST entry `8ae82dde...`).
- **Calibration (exact, rerun in this kit)**: published 7x32 q=6 m=31
  configuration reproduces published `surgery-m32.json` counters exactly
  (candidates 2,224,675 / safe 0 / T-curve c4=1 c3=10)
  (`output/calib-m32.json`).
- **Determinism**: run1 = run2 byte-identical
  (`output/surgery-m22.run1.json` sha256
  `1ac7c6d84d7865e31cd6b18f87a4b4d42a53225cf154d2730d4fd5e66ff51d86`).
- **Independent spot-check**: `scripts/spotcheck_int.py` (byte-identical
  to the 6x26 kit's method-disjoint integer-conic re-checker) on a
  seeded-random sample of 300 engine-rejected candidates: 300/300
  rejections confirmed, 0 missed witnesses.
- **Tamper battery** (`output/tamper/tamper-summary.json`):
  T1 blocked-target -> fail-closed; T2 unsafe seed (stone added at (0,0)
  completing a 7-stone curve) -> fail-closed ("seed unsafe");
  T3b blocking gate weakened -> fail-loud (safe 84,806 / spurious
  witnesses 84,806, counters diverge from official; full spurious log
  elided, excerpt published).

## Honest disclosures

- A preliminary probe (uncovered-cell identification, preliminary
  enumeration with identical counts) ran before the declaration; the
  declaration discloses this; all recorded runs (determinism pair, sample
  dump, spot-check, tamper) ran after the declaration commit `ab8134bc`.
- No rediscovery positive control (m=20 -> m=21 sd = 40, disclosed).
- Standard 11x11 empty board, two-stone roots, third move, S2, closure
  classes remain UNKNOWN at all times; verdicts not consumed;
  candidates/safe counts are bookkeeping.

## Outputs

- `output/m21.witness.stones.json`: seed stones.
- `output/calib-m32.json` + stdout: calibration record.
- `output/surgery-m22.run1.json` (+ stdout + 300-line sample) and
  `output/surgery-m22.run2.json` (+ stdout): official runs.
- `output/spotcheck-summary.json`, `output/tamper/*`: control records.

## Reproduction

```sh
python3 scripts/surgery_general.py --bx 22 --by 6 --q 7 --target 21,2 \
  --seed output/m21.witness.stones.json --out run.json --sample 300
python3 scripts/spotcheck_int.py run.json run.json.sample.jsonl 300 0 100
# (chunks 100/100/100)
```
