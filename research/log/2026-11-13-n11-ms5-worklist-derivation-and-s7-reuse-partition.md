# 2026-11-13 n11 S2 {59,60} milestone-5: full independent worklist derivation + S7 reuse partition

Baseline main at start: `5af484bb2411`? no — `5af484bb241cd776af2eda5e26eda4e97595baee` (the full geometry cost audit). Read AGENTS.md, research/knowledge/README.md, the milestone-5 experiment README, and both prior ms5 audit logs.

## What was done

1. **Full independent worklist derivation.** From the K0675 oracle hex inputs alone (78 FW + 16 SW 5-stone bases, 14 LOSS sweep keys), a fresh TypeScript implementation (4x32-bit masks, D4 permutation tables, forbidden-set memo capped and cleared at 5,000 entries to bound memory, canonical hex via BigInt minimization over the 8 board symmetries) rebuilt the whole milestone-5 accounting: sweep 3,868; S5 orbits 196; obligatory instances 17,524; judged 479; judged-LOSS 13; settled S5 10; unique reduced S6 7,867; cost 615,497. The re-derived hex,cost,classes table sorted lexicographically is byte-identical (md5 `0e95a438dbcb486368393de9c73fc21e`) to the six published manifest parts. Unlike the 2026-11-13 geometry audit, this also covers the key set and the classes column; the 213-row sample audit is now fully superseded.

2. **S7 certificate-reuse partition.** For every worklist S6 and every oracle base O with exactly one stone outside S6 and the completing move x legal, the candidate S7 = S6 + x was classified against the certified pools: 0 direct WIN7 hits, 396 known-LOSS (62-cert LOSS7 subset or child of a LOSS sweep S6), 8,367 possible-win-pool (a 6-subset lies in the judged 3,868 sweep), 0 unclassified. 8,763 candidates over 6,276 S6s; 1,591 S6s have no oracle-completing candidate. Full table in three CSV parts; the cat=2 rows are the external-lane lookup targets against the local win-child pool.

## Notes for reproduction

- The derivation program is memory-bounded (sandbox 16 MiB); the forbidden-memo cap of 5,000 and per-run output chunking (~2,900 rows) are implementation details, not part of the math.
- Implementation gotchas that were fixed during this session: the legal mask must invert the banned mask (and chunk 3 masks with 0x01FFFFFF, bits 96..120); a BigInt-keyed version was too slow and memory-hungry; large single write operations exhausted the sandbox memory limit.

## Status

Verification and conditional bookkeeping only. **11x11 empty root, two-stone root {49,60}, and S2 {59,60} remain UNKNOWN.** No verdict was produced or changed; every win/loss count above is conditioned on the K0675 oracles.
