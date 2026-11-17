# 2026-11-17 n11 class2-lane: 8-way worker split memo merge (K0909 resume item)

Lane: 11x11 class2-lane long-term (cost73k). Kind: measurement only.
Outcome: the K0909 N-way worker-split line is extended from 4 to 8
workers. Workers total 110,639,931 nodes (0.913 of band ms23, cheaper
than every published split); the 8-way heapq merge yields a 5,243,408-key
seed with zero conflicts; the seed-capacity design rule holds one notch
beyond its calibration point (load 0.156 at MS=1<<25, 383 failed inserts
== simulator prediction exactly); the MS=1<<25 seedrun is the cheapest
measured band run on this band (70,538,916 nodes, 0.9172 of the nb4
seedrun24). All 15 gates pass. No verdict change; 11x11 remains UNKNOWN.

## Context

The K0909 line had published, on the cost-73k band and the repo-verbatim
engine: the 2-way split (119,962,147 worker nodes, merged seed 4,291,899
keys), the node-balanced 4-way (112,741,501, seed 4,985,986), the
boundary-preserving 4-way (111,953,183, seed 4,975,265, with the bit-41
head-bit reversal +5.6% and the merge non-closure 262 keys), the seed
capacity design (knee at S~4.1-4.2M keys at MS=1<<24; design rule seed at
load <= ~0.15, i.e. MS=1<<25 for ~5M-key seeds, cross-validated 28 ==
28 at the design point), and the hybrid seed union (4,975,527 keys,
72,761,010 nodes at MS=1<<25, published by a concurrent lane at 1299412a
with docs at e0c13af3). Two questions were left open and are targeted by
this resume item: (a) does the split keep paying at N=8, and is the
head-bit restart penalty structural (bit 41 was the only observed
reversal); (b) where does the failure knee sit for a ~5.24M-key seed,
and does the 0.15 design line hold at MS=1<<25. This lane claimed the
item at b8c76a4d (14:18Z) before any compute; the concurrently completed
cost74i sweep (claimed 7153fe58, completed 874c5327) and the in-progress
fixB worker-split claim (dcfdcb25) belong to other lanes and were not
touched.

## Design

1. Rebuild all inputs from raw-CDN pinned blobs with git blob sha
   verification (extractor 52bcaf50, driver 2a95d952, legal 8e97082c,
   manifest 0892aed0) and md5-verify all 22 published certificates
   before any compute.
2. Contiguous DP min-max 8-way split of the 22 band bits by the
   published band ms23 per-bit node counts: V1 = 0,7,11 (the band ms23
   prefix anchor), V2 = 15,35, V3 = 39,41,44,58, V4 = 62,73,76,
   V5 = 87,89,94, V6 = 95,97, V7 = 98,103,105, V8 = 112,117.
3. Eight fresh worker processes at MS=1<<23 with band-carried memo and
   per-bit snapshots. Gates: split is an exact partition; V1 per-bit
   nodes / total / final occupancy equal the band ms23 prefix; every
   other worker's head bit equals the published fresh per-bit anchor;
   all certificates byte-identical per worker (22 in total).
4. Distinct passes (internal conflicts), 8-way heapq merge-join
   (incidence histogram up to 8, cross conflicts), merge determinism
   (byte-identical repeat merge).
5. Light occupancy simulator (the seed-capacity lane's anchored design)
   MS sweep 1<<24 / 1<<25 / 1<<26 on the merged seed8, extending the
   published knee curve (4.29M -> 1,448, 4.99M -> 16,137) with a third
   point at ~5.24M keys.
6. Engine seedrun at the design point MS=1<<25 (hardened fsync dumpMemo
   variant, cap 200): certificates 22/22 byte-identical, seed failure
   == simulator prediction, record identity closed (violations 0,
   missing == failed).

## Findings

1. **Workers (2 -> 4 -> 8 monotone, diminishing returns)**: V1
   12,253,371 / V2 13,181,331 / V3 13,007,357 / V4 13,387,472 /
   V5 15,825,310 / V6 16,061,843 / V7 14,904,737 / V8 12,018,510,
   total **110,639,931 nodes** = 0.9130 of band ms23 (121,186,659),
   0.9223 of the published 2-way (119,962,147), 0.9814 of the
   node-balanced 4-way (112,741,501), 0.9883 of the boundary 4-way
   (111,953,183). The split pays monotonically on every published
   variant (2-way -> nb4 -6.0%, nb4 -> 8-way -1.9%). V1 equals the band
   ms23 per-bit prefix exactly (final occupancy 1,882,289 ==
   BAND23_OCC[11]). Certificates 22/22 byte-identical (3/2/4/3/3/2/3/2
   per worker).
2. **Head-bit reverse penalty is not structural at N=8**: all 7
   non-prefix worker head bits reproduce the published fresh per-bit
   anchors exactly (gate). The fresh-vs-band-carried node ratios are
   V2 0.9937 (bit 15), V3 1.0362 (bit 39, the ONLY reversal), V4 0.7903
   (bit 62), V5 0.8171 (bit 87), V6 1.0000 (bit 95, memo-state
   invariant), V7 0.8788 (bit 98), V8 0.7731 (bit 112). Most fresh heads
   are CHEAPER than the band-carried cost, consistent with the fresh
   ms23 battery total being below the band ms23 total; the boundary
   4-way's bit-41 reversal is an instance, not a law.
3. **8-way merge**: distinct totals V1 994,999 / V2 1,008,503 /
   V3 1,141,457 / V4 959,286 / V5 1,005,753 / V6 808,798 / V7 1,030,415
   / V8 965,398 (sum 7,914,609); heapq 8-way merge-join gives
   **occupied_after 5,243,408** (+22.2% vs the 2-way seed 4,291,899,
   +5.2% vs the nb4 seed 4,985,986), shared_total 1,980,110, incidence
   histogram {1: 3,263,298, 2: 1,422,024, 3: 441,397, 4: 101,479,
   5: 14,142, 6: 1,030, 7: 38, 8: 0} - no key is memoized by all 8
   workers. Internal conflicts 0, cross conflicts 0, merge
   deterministic (byte-identical repeat), seed8 md5
   8d07cd7b82a3befc07cc775ea883e2e0. Union growth continues to flatten
   (2 -> 4-way +16.2%, 4 -> 8-way +5.2%).
4. **Simulator MS sweep on seed8 (third knee point)**: MS=1<<24 ->
   39,409 failed (0.7516%, load 0.3102; own-cluster 7,019 + spill-over
   32,390; max cluster 130 keys, 563 bases >= 64 keys); the knee curve
   4.29M -> 1,448 / 4.99M -> 16,137 / 5.24M -> 39,409 confirms the
   superlinear growth beyond the published two points. MS=1<<25 ->
   383 (0.0073%, load 0.1563). MS=1<<26 -> 0 (load 0.0781, no base
   >= 64 keys). The 5.24M-key seed slightly exceeds the 0.15 design
   line at MS=1<<25, but the knee moves with MS: the failure rate
   stays two orders below the 0.1% gate.
5. **Engine seedrun at MS=1<<25**: seeded 5,243,408 / inserted
   5,243,025 / **failed 383 == simulator prediction exactly** (0.0073%
   < 0.1% gate); certificates 22/22 byte-identical; record identity
   closed (present 5,243,025, missing == 383, value violations 0);
   total **70,538,916 nodes** = 0.9697 of the nb4 seedrun25
   (72,745,351), 0.9172 of the nb4 seedrun24 (76,903,818), 0.9695 of
   the concurrently published hybrid seedrun25 (72,761,010); final
   occupancy 14,053,298 (load 0.4188); bit 95 = 11,857,737 nodes
   (fifth independent confirmation of the memo-state-invariant root).
   The larger 8-way union buys the cheapest measured band run on this
   band to date: at fixed MS the merged-seed size and the band-run cost
   are inversely related through memo completeness, and the sim ==
   engine agreement extends one notch past the design calibration
   point.

## Environment facts (recorded as experiment facts)

- Full workspace rebuild from pinned raw-CDN blobs after an
  environment reset (same class as the previous K0909 measurements);
  git blob shas verified, 22/22 published certificate md5s verified
  before compute.
- Background jobs must be detached with a setsid nohup wrapper
  (< /dev/null > log 2>&1, disown); the orchestrator's
  Popen(start_new_session=True) survives bash command returns.
- Engine throughput ~365k nodes/s in this cgroup; the full 8-way
  pipeline (8 workers, 8 distinct passes, merge x2, sim sweep, MS=1<<25
  seedrun with the hardened fsync dumpMemo at cap 200, record identity)
  completes in ~35 minutes.
- All long bash invocations need an explicit timeout_seconds; blocking
  device reads must be avoided.

## Gates (output/worker-split8-memo-merge-73k-20261117.json, 15/15 pass)

- split_exact_partition - True
- workerV1_per_bit_equals_band23_prefix - True
- workerV1_total - True
- workerV1_final_occupied - True
- first_bit_fresh_anchors - True
- worker_byte_identical - True
- internal_conflicts_zero - True
- cross_conflicts_zero - True
- merge_deterministic - True
- seedrun_byte_identical - True
- seedrun_seed_failed_equals_sim25 - True
- seed_failure_rate_below_0.1pct - True
- record_identity_no_violations - True
- record_identity_missing_equals_seed_failed - True
- bit95_memo_state_invariant - True

## Interpretation guard

Measurement only. No new WIN/LOSS verdicts, no manifest row opened or
closed, certificate bytes unchanged, repo-verbatim extractor unmodified
(published determinism chains). WIN7-D10 proves a first-player win
within depth 10 from the individual 7-stone roots only; REFUTED-D10 is
not a LOSS proof. The 11x11 empty board, both two-stone roots {49,60}
and {59,60}, S2 {59,60} and classes 1/2/4 all remain UNKNOWN.
