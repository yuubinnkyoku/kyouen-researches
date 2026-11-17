# 2026-11-17 n11 class2-lane: boundary-respecting 4-worker split memo merge (K0909, independent measurement)

Lane: 11x11 class2-lane long-term (cost73k). Kind: measurement + verification.
Outcome: all soundness/correctness/reproduction gates pass; two expectation
gates are falsified by measurement and recorded as findings; the merged
4-way table is measured NOT to be a superset of the published 2-way seed
(merge non-closure, 262 keys / 0.0061%); full pipeline executed twice with
byte-identical outputs. No verdict change; 11x11 remains UNKNOWN.

## Context and relation to the parallel node-balanced measurement

K0909 (commit f9e3acf8) proved the 2-worker split merge safe (zero
conflicts) and beneficial (seedrun at 80.2% of band ms24). A parallel
session of this lane published the node-balanced 4-way extension
(commit b38b9f3d: 7/6/5/4 split, heapq N-way merge, incidence histogram,
fault-injection validation of the conflict detector; 112,741,501 worker
nodes, merge occupied_after 4,985,986, seedrun 76,903,818).

This measurement was designed and executed independently and concurrently
in a separate environment instance, with a different split: the
BOUNDARY-RESPECTING 4-way split, which cuts at the same bit boundaries the
published 2-way split used (39/41, 73/76, 97/98). This makes the merged
4-way table directly comparable to the published 2-way seed key-by-key,
which the node-balanced split is not. Its two distinctive deliverables are
(1) an in-pipeline exact reproduction of the published 2-way measurement
(the 2-way workers are re-run as anchors inside the same orchestrator) and
(2) the key-set comparison of the 4-way merged table against the 2-way
merged table, which quantifies merge non-closure. All numbers that overlap
with the parallel measurement agree (see Cross-validation below).

An earlier attempt of this same measurement in this environment instance
was lost to an environment reset after w0/w1 completed; the rebuilt
run re-derived and re-measured the recorded anchors exactly.

## Design

- Workers (verbatim engine blob 52bcaf50, both known memo bugs in place -
  K0907; MS=1<<23, band-wide memo within each worker, per-bit snapshot +
  clearRows with byte-compare against the published certificates):
  W0 = bits 0,7,11,15,35,39; W1 = 41,44,58,62,73; W2 = 76,87,89,94,95,97;
  W3 = 98,103,105,112,117.
- Reproduction anchors: workerA (bits 0..73) and workerB (bits 76..117)
  are re-run with the published 2-way pipeline in the same orchestrator;
  gates require per-bit nodes and per-bit occupancy series equal to the
  published K0909 output JSON, totals 48,482,011 / 71,480,136, and the
  merged 2-way seed byte-identical to the published md5
  e7c2c17e7a91d8ea17f433f3bb482f29.
- Offline merge (sort-based, streaming, no sqlite): per-worker distinct
  pass (win=min, lose=min, nowin=max, nolose=max, 255 = unbound) with
  sentinel-aware internal conflict counting; all SIX pairwise merges
  among W0..W3 (cross conflicts); cascade M01 = merge(W0,W1),
  M23 = merge(W2,W3), FINAL4 = merge(M01,M23). Every merge executed
  twice; passes must be byte-identical.
- FINAL4 vs the reproduced 2-way seed: key-set and monotone comparison
  (subset prediction only_in_seed2 == 0; monotone prediction: value
  violations 0 under win<=, lose<=, nowin>=, nolose>= with 255-sentinel
  rules).
- Seedrun: verbatim engine at MS=1<<24 seeds from FINAL4 through the
  engine's own memoEntry() (verbatim probe semantics), then extracts all
  22 bits band-wide. Gates: 22/22 certificates byte-identical, seed insert
  failure rate < 0.1%, record identity of the final dump against FINAL4.
- Determinism: the complete pipeline is executed twice (independent work
  directories, fresh processes); the two output JSON documents must be
  byte-identical (wall-ms excluded by design).

## Results

- 2-way reproduction anchors: workerA 48,482,011 nodes / final occupied
  5,263,320 / 11 certs byte-identical, per-bit nodes and occupancy series
  EXACTLY the published values; workerB 71,480,136 / 6,242,804 / 11
  likewise; merged 2-way seed shared 882,089, occupied_after 4,291,899,
  md5 e7c2c17e7a91d8ea17f433f3bb482f29 == published (byte-identical),
  second pass byte-identical.
- 4-way workers (certificates byte-identical 6/5/6/5):
  W0 27,424,708 nodes / occ 3,705,871 (per-bit == workerA prefix exactly);
  W1 20,252,951 / 3,180,413; W2 36,575,507 / 4,869,649 (per-bit ==
  workerB prefix exactly); W3 27,700,017 / 3,916,795.
  workers4 total 111,953,183 = 0.9332 x the 2-way workers total and
  0.9238 x band ms23 - cheaper than both the 2-way split (as expected)
  and the node-balanced 7/6/5/4 split (112,741,501; -0.7%).
- Per-bit occupancy-harm quantified (fresh restart vs the same bits
  carried in the 2-way workers): W1 bits 41..73 cost 20,252,951 fresh vs
  21,057,303 carried (-804,352); only the first bit of a fresh worker is
  more expensive (bit41 1,868,639 vs 1,768,864: the fresh table lacks the
  previous bits' entries). W3 bits 98..117 cost 27,700,017 fresh vs
  33,712,244 carried (-6,012,227, -17.8%; bit117 alone 7,739,551 vs
  10,008,242). The verbatim memo's late-run occupancy harm (K0907
  mechanism) dominates; keeping the 73/76 boundary and cutting inside the
  2-way workers' ranges preserves most of the fine-split saving.
- distinct pass: W0 3,705,871 records -> 1,869,417 distinct; W1
  3,180,413 -> 1,480,715; W2 4,869,649 -> 1,823,669; W3 3,916,795 ->
  1,780,518. Duplicate keys all high-bit (signed-key bug, max 64 copies).
  Internal conflicts 0 in all four.
- Six pairwise merges: shared 472,945 (W0-W1), 452,527 (W0-W2), 386,260
  (W0-W3), 359,726 (W1-W2), 318,937 (W1-W3), 368,177 (W2-W3); cross
  conflicts 0 in all six. Cross-worker sharing (~20% of keys) does not
  collapse with the finer split.
- Cascade: M01 occupied_after 2,877,187; M23 3,236,010; FINAL4
  occupied_after 4,975,265 (+15.9% vs the 2-way seed's 4,291,899),
  final-merge shared 1,137,932, cross conflicts 0, both passes
  byte-identical (md5 35ccec0eb01e9b1b3719fa7e0c6ff4e9).
- FINAL4 vs the reproduced 2-way seed: shared 4,291,637 keys with
  equal-or-stronger combined values (violations 0); only_in_final4
  683,628; only_in_seed2 262.
- seedrun (MS=1<<24, FINAL4 seed, all 22 bits): seeded 4,975,265,
  inserted 4,960,608, failed 14,657 (0.295%); 76,599,320 nodes =
  0.8933 x the published 2-way seedrun (85,747,496), 0.717 x unseeded
  band ms24 (106,861,135); final occupied 10,525,071 (load 62.7%);
  22/22 certificates byte-identical.
- record identity: present 4,960,608 (every inserted seed key survives),
  missing exactly the 14,657 failed inserts, value violations 0.
- determinism: run1 and run2 (independent work directories, all fresh
  processes) produced byte-identical output JSON documents. The
  document-type schema label was adjusted from
  ...-worker-split4-memo-merge-... to
  ...-worker-split4-boundary-memo-merge-... in both files (identically)
  before publication, to disambiguate from the parallel node-balanced
  measurement's schema label; it is a label and affects no measured value.

## Falsified expectation gates (recorded as findings)

gates_all_pass is FALSE for exactly two gates; every soundness,
correctness, reproduction, conflict-detection and determinism gate passes.

1. final4_superset (prediction only_in_seed2 == 0; measured 262).
   The boundary-preserving 4-way merged table does NOT contain 262 keys
   (0.0061% of 4,291,899) that the 2-way merged table contains. Root
   cause: the verbatim memo's search and insertion are path-dependent -
   a split worker's table state differs from the unsplit worker's, so a
   position the unsplit worker visited and memoized can be never reached
   under the split's different pruning, or its local memoEntry() probe
   can fail. MERGE IS NOT CLOSED UNDER RE-SPLITTING: merging finer-split
   workers' tables does not recover the coarser split's table, even
   though the finer union is much larger overall (+683,628 net). This
   nuances the parallel measurement's "the merged table is more complete"
   (true in cardinality, NOT in set inclusion). Cost-only, soundness
   unaffected (all certificates byte-identical); the seedrun recomputes
   the missed positions. A coordinator must treat any merged worker
   cache as an approximation, never as a substitute for a coarser
   configuration's cache.
2. seed_insert_failure_rate_below_0.1pct (prediction < 0.1%;
   measured 0.295%). FINAL4 is 15.9% larger than the 2-way seed, seeding
   load rises from 25.6% to 29.6%, and clumped-hash probe failures grow
   superlinearly: 14,657 vs the 2-way's 1,448 (10.1x, rate 8.7x).
   Independent confirmation of the parallel measurement's 0.324% at a
   16.2% larger seed: the failure rate scales faster than seed size in
   both measurements; the 0.1% constant is not the right budget for
   larger seeds.

## Cross-validation with the parallel node-balanced measurement

All overlapping quantities agree across the two independent measurements
(different environment instances, different split geometries, both against
the same published anchors): conflicts 0 everywhere; certificate
byte-identity 22/22; record identity closed (missing == failed inserts,
violations 0); the seed-insert failure rate falsifies the same 0.1%
expectation (0.295% here, 0.324% there); seedrun totals are within 0.4%
(76,599,320 vs 76,903,818) and both are ~0.72 of unseeded band ms24; the
4-way union grows ~16% over the 2-way seed in both (4,975,265 / 4,985,986).
The boundary-respecting split is the cheaper of the two by 0.7% on worker
nodes and 0.4% on the seedrun.

## Interpretation guard

Measurement only. No new WIN/LOSS verdicts, no manifest row opened or
closed, certificate bytes unchanged. The repo-verbatim extractor is
unmodified in the repo (published determinism chains). WIN7-D10 proves a
first-player win within depth 10 from the individual 7-stone roots only;
REFUTED-D10 is not a LOSS proof. The 11x11 empty board, both two-stone
roots {49,60} and {59,60}, S2 {59,60} and classes 1/2/4 all remain UNKNOWN.

## Resume pointers

- Best measured configuration for the band so far: boundary-respecting
  4-way split (111.95M worker nodes) + merged seed (4,975,265 records,
  reusable for future band runs at MS=1<<24) + seedrun (76.60M nodes).
- The merged-seed table files themselves are not published (size); the
  orchestrator regenerates them deterministically from the pinned inputs.
- 8-way measurement: change the BITS_W* lists; watch the first-bit
  penalty (bit41-style +5.6%) against the carried-run harm, and re-budget
  the seed-failure gate for the larger union.
- The merge non-closure residual (262 keys) is a phenomenon of the
  verbatim memo's path-dependence; the fixed engine (K0907 fixB) removes
  the clumping and should make merge closure exact - measurable if the
  fix lane ever modifies an extractor in-repo.
- The fold chain (76c->66i->66j->69j->71e->72d->73i) remains under the
  parallel claim lane's management; do not touch until published.
