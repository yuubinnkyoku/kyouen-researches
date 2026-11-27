# 2026-11-27 Six-row q=7, 6x22: complete two-edit surgery — NEGATIVE

## Status

Complete, published. Kit: `research/experiments/six-row-q7-m22-two-edit-surgery-20261127/` (20 files, MANIFEST-sha256.txt verified by fetch-back).

## What was run

Complete two-edit neighborhood surgery on the 6x22 board (bx=22, by=6, q=7) around the published 6x21 K0815 dai-7 witness (35 stones, rows [6,6,5,6,6,6], `six-row-q7-m21-class-split-20261114/output/w67_21.json`), targeting the unique uncovered cell T=(21,2) (the witness is one-stone-short on 6x22; T-curve census c4=3, c5=1). Engine: the published q-generalized surgery engine (`scripts/surgery_general.py`, byte-identical to the 6x26 kit engine, sha256 `8ae82dde4b4959c1e0cfdc388f619d32508623befb29b0c91968bab25d3b6b6a`), q=7 parameterization (safety >= 7, blocking >= 6, deficiency via row-capacity 6 and final size <= 35).

## Result

**692,655 unique candidates, 0 safe, 0 safe-maximal witnesses. NEGATIVE.**

Local negative only: no 6x22 witness within edit distance <= 2 of the m=21 seed. NOT an absence claim for 6x22 (K0815 class {2} kissat 280s, 5,038,264 conflicts INDET remains the frontier status; other classes unswept). **M_{6,7} stays in [22, 402]** (lower K0815, upper K0318 substitution U=402). Frontier stays 6x22.

## Verification

- Declaration `ab8134bc` published before all recorded runs (HEAD pinned `81703981`; preliminary probe disclosed).
- Determinism: run1 = run2 byte-identical (sha256 `1ac7c6d84d7865e31cd6b18f87a4b4d42a53225cf154d2730d4fd5e66ff51d86`).
- Calibration: published 7x32 q=6 m=31 surgery reproduced exactly (2,224,675 / 0; T-curve census c4=1 c3=10).
- Independent method-disjoint integer-conic spot-check of 300 engine-rejected candidates: 300/300 rejections confirmed.
- Tamper battery: T1 blocked-target fail-closed, T2 unsafe-seed fail-closed, T3b weakened blocking gate fail-loud (84,806 spurious).
- Disclosure: no rediscovery positive control possible (m=20 -> m=21 symmetric difference 40 over all flip images x translations).
- 11x11 empty board / two-stone roots / third move / S2 / closure classes: UNKNOWN at all times; no verdicts consumed.

## Next tasks (fast lane candidates)

1. (6,7) 6x22: three-edit surgery, or SAT-side class split of the remaining classes on 6x22 (class {2} already 280s INDET; other classes unswept).
2. (8,10) 8x26 two-edit surgery: m=25 witness (71 stones) from the eight-row-bands kit; witness-free band 40..138 known; untouched and the natural next q-family data point.
