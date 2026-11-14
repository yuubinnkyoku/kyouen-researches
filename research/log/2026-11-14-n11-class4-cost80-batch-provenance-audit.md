# 2026-11-14 n11 class4 cost-80 raw-batch provenance audit

Latest main at audit start: `d09238c958bc2f9865c3476e0774704112e5371e`.
Read `AGENTS.md`, `research/knowledge/README.md`, K0023, K0783, the cost-80 log, the summary JSON and all five raw JSONL batches.

## Independently recomputed from published raw rows

- Each of `class4-lane-cost80-raw-batch1..5-20261114.jsonl` has **17 lines**: one `pilot_d6` control and **16** candidate results.
- The combined 80 candidate records contain **80 distinct bits**, all present in the summary JSON, with exact agreement of per-bit node counts.
- Sum of the 80 raw node counts: **290,092,122**, exactly the summary value. Controls are excluded from this total.
- The 80 candidate verdicts remain `REFUTED-D10`, with no capped runs and no `WIN7-D10` in the published summary.

## Provenance discrepancy (documentation only)

The summary JSON `method` field and the cost-80 log both describe batches as `20+20+20+20`, but the committed raw batch files and the JSON `raw_jsonl_batches` field establish **five batches of 16 candidates each**. The cost-80 log itself also correctly describes five raw batch files. For reproducibility, use the actual five raw files rather than the stale 20×4 narrative. This audit does not alter historical records.

## Evidence boundary

This is an independent **cross-file consistency check**, not an independent solver rerun or certificate verification. `REFUTED-D10` excludes only depth-10 winning witnesses for the tested seven-stone roots, not deeper wins or a parent/root verdict. The 11×11 empty board and two-stone roots `{59,60}`, `{49,60}` remain **UNKNOWN**.
