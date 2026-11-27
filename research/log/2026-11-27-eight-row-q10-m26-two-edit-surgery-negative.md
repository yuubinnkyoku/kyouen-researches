# 2026-11-27 Eight-row q=10, 8x26: complete two-edit surgery — NEGATIVE

## Status

Complete, published. Kit: `research/experiments/eight-row-q10-m26-two-edit-surgery-20261127/` (24 files, MANIFEST-sha256.txt verified by fetch-back).

## What was run

Complete two-edit neighborhood surgery on the 8x26 board (bx=26, by=8, q=10) around the published 8x25 m=25 witness (71 stones, rows [9,9,9,8,9,9,9,9], `eight-row-bands-20261114/output/w8q10-witness-search/s8x25q10_none.witness.json`), targeting the unique uncovered cell T=(25,3) (the seed is one-stone-short on 8x26; T-curve census c7=0, c8=1, the c8 T-curve being the row-3 line y=3).

## Result

**4,659,859 unique candidates, 0 safe, 0 safe-maximal witnesses. NEGATIVE.**

Local negative only: no 8x26 witness within edit distance <= 2 of the m=25 seed. NOT an absence claim for 8x26 (all four published SAT encodings for m=26 remain INDET; m=27..31 probed INDET; m=32..39 unswept). **M_{8,10} stays in [26, 940]**. Frontier stays 8x26.

## Engine adaptation (disclosed)

The published engine (`surgery_general.py`, sha256 `8ae82dde...`) OOM-killed at 36s on this instance (~4.7M candidates materialized in a set). A streaming v2 (`surgery_stream.py`, sha256 `de23dbe2...`) enumerates per-R with exact per-R dedup (globally equivalent, see kit README), calibrated EXACTLY against the published 7x32 q=6 m=31 surgery (2,224,675 / 0 / 0 reproduced, 11s).

## Verification

- Declaration `17ddb2d5` published before all recorded runs (observed HEAD `a48a7d77` at declaration time; preliminary census probe + the OOM-killed published-engine attempt disclosed there).
- Determinism: run1 = run2 byte-identical (both sha256 `c2d8b30af1835668d84bfdf3f4f1e2212734a2eb25e5d4ab01f705077f250348`).
- Independent method-disjoint integer-conic spot-check of the 300-candidate reservoir sample (chunks 100/100/100): 300/300 rejections confirmed, 0 missed witnesses.
- Tamper battery: T1 blocked target fail-closed, T2 unsafe seed fail-closed, T3b weakened blocking gate fail-loud (15,727 spurious in chunk 0:16 vs official 0; the uncapped full-scan T3b attempt exhausted sandbox memory and forced an environment reset — disclosed).
- No m=24 witness published for this family: no rediscovery control available (disclosed).
- 11x11 / roots / third move / S2 / closure classes: UNKNOWN at all times; verdicts not consumed.

## Next tasks (fast lane candidates)

1. (8,10) 8x26 three-edit surgery (two-edit is exhausted negative around the m=25 seed; T-curve census c8=1 keeps a three-edit attack small), or SAT-side class-split of the INDET encodings on 8x26 (precedent: six-row q7 class-split at 6x21).
2. (6,7) 6x22 three-edit surgery or class-split of the unswept classes.
3. Generalization data point: the one-stone-short transplant structure (unique uncovered cell at the wide edge) now holds for four independent families: 7x32 q6, 6x26 q6, 6x22 q7, 8x26 q10 — a candidate structural lemma worth stating precisely and testing on further (r,q) before any claim.
