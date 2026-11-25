# 2026-11-16 n11 class2-lane cost-66c independent re-run verification (59/59 + bit-112 resolution node-exact)

## Start state

- Start main: `aca9d762` (cost-66c fold pre-registration at the post-cost65n head 1444,
  projected head 1450/174/6398/506297/4671/370211). The cost-66c fold receipt was still
  in flight; the cost-65o sweep was still in flight.
- Inputs verified (all blob-pinned pre-fold artifacts published by the parallel lane
  in commits `64e83dff` (claim v1) and `b17e978e` (claim v2 completed NOT-STERILE,
  raw batches 1-8, bit-112 cap-raise resolution, determinism reruns, v15 crosscheck,
  stdlib audit)): child `00000000000000003800000008002008` (cost 66, third-ranked
  cheapest open row at head 1441, shared class-2 parent
  `00000000000000003800000008002000`), 66 legal candidates, 59 open bits swept,
  7 transferred REFUTED-D10.

## Method

- This lane re-ran the entire sweep independently in a fresh environment: the
  repo-verbatim v16 runner (`class4_child1_runner_v16.ts`, fetched from main),
  Node 22, depth 10, cap 1e7, `--andclose 1`, engine state fully reset per candidate,
  pilot_d6 control 3402 nodes per batch invocation (9 invocations: 8 batches + the
  bit-112 cap-80M resolution run).
- No engine modification of any kind; the runner is byte-identical to main
  (`scripts/class4_child1_runner_v16.ts`).

## Results

- **59/59 swept bits node-exact**: bit / loss / nodes / capped /
  terminalStoneRange / andclose identical to the published raw batches 1-8.
  Mismatches: **0**.
- **Bit-112 cap-raise resolution reproduced node-exact**: at the protocol cap 1e7
  the run caps at exactly 10,000,001 nodes (as published in raw batch 7), and at the
  raised cap 80,000,000 it resolves as **WIN7-D10 at exactly 12,574,920 nodes**
  (identical to `class2-lane-cost66c-bit112-cap80m-resolution-20261116.jsonl`).
- All 7 WIN7-D10 verdicts reproduced at the sweep level: bits 73 (1,380,970),
  75 (2,092,539), 79 (1,078,921), 87 (2,016,731), 96 (2,363,101), 97 (689,724),
  112 (12,574,920 resolution). 52 swept REFUTED-D10 reproduced. 0 capped after the
  resolution.
- Totals reproduced exactly: raw-as-run 81,605,344 nodes; definitive
  84,180,263 nodes (matches claim v2 `total_definitive_swept_nodes`).
- Pilots: 9/9 invocations pilot_d6 = 3402 nodes, loss=false, identical.
- Throughput in this environment: ~450-520k nodes/s (single process), consistent
  with the previous sessions' v16 measurements.

## Process notes (experiment facts)

- Batch 2 was inadvertently executed twice (two full invocations, ~1 min apart,
  same environment); both executions produced byte-identical records, which was
  then trimmed to a single copy in the published file. This is an unplanned
  additional determinism observation (same-day, same-binary, fresh-process).
- The verification script was executed twice end-to-end; the verification JSON is
  byte-identical on re-run.

## Position

- This verifies the **sweep verdict layer** of cost-66c (which feeds the in-flight
  fold) with a third implementation instance of the same published binary. The
  published certificate layer (7 WIN7-D10 certificates, dual-verified BigInt +
  Bareiss by the publishing lane) is unchanged and not re-extracted here.
- Head 1444 unchanged by this verification; the 66c fold receipt (projected head
  1450) is still in flight at publication time.

## Interpretation guard

- Bookkeeping verification only. WIN7-D10 proves a first-player win within depth
  10 from the individual 7-stone roots only. REFUTED-D10 is not a LOSS proof.
  NOT-STERILE is not a game resolution. The 11x11 empty board, the two-stone roots
  {49,60} and {59,60}, S2 {59,60}, and classes 1/2/4 all remain **UNKNOWN**.
