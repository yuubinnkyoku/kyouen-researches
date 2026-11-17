# n11 S2 {59,60} milestone-5: full independent worklist derivation + S7 certificate-reuse partition

## 後続監査の注意
`scripts/ms5_s7_reuse_analysis.ts` はコメントのみで実行本体がなく、下記の再導出・分類を再実行できない。`scripts/audit_published_candidates.py` は公開済み行の安全性・親子関係・件数を検査するが、網羅性や分類を検証しない。現在の評価は K0783 を参照。

後続の全列挙 `scripts/audit_candidate_completeness.py` により、下記の8,763件は完全ではなく、94オラクルの全対称像を使うと15,072件あることが判明した。追加6,309件は `output/additional-candidates.csv.gz` に収録し、その安全性は別の行列式検査でも確認した。候補のない親は下記の1,591個ではなく611個。

さらに `scripts/audit_win7_reuse.py` でリポジトリ内のWIN7監査記録を照合すると、534親子対・498親に勝ち子が見つかり、残りは7,369親となる。監査記録を前提にした結果で、別保管の証明書本体は再検証していない。照合表は `output/win7-reuse-hits.csv.gz` を参照。

候補CSVの `move` は正規化済み `s6_hex` にそのまま適用できるとは限らない。親の対称像を試し、空き位置 `move` を加えた子の正規形が `s7_hex` に一致する像を選ぶ。part2とpart3にはCSVヘッダーがない。

Baseline main: `5af484bb241cd776af2eda5e26eda4e97595baee` (includes the full S6 geometry cost audit of 2026-11-13, which verified the cost column of all 7,867 published rows but explicitly not the key set or classes column).

## Part 1: full independent worklist derivation (keys + classes + cost)

A fresh TypeScript routine (independent of the milestone-5 generator) re-derived the entire milestone-5 accounting from the K0675 oracle inputs (78 FW + 16 SW base hex positions, 14 LOSS sweep keys):

- sweep (judged 6-stone children of the oracle bases): **3,868**
- S5 worklist orbits: **196**
- obligatory (S5, child) instances: **17,524**; judged instances **479**; judged-LOSS instances **13**
- S5 orbits settled by a judged-LOSS child: **10**
- reduced unique S6 worklist orbits: **7,867**; total S7 legal-edge cost: **615,497**

The re-derived `hex,cost,classes` table, sorted lexicographically, is **byte-identical (md5 `0e95a438dbcb486368393de9c73fc21e`)** to the concatenation of the six published `ms5_s6_manifest_part*.csv` files. This closes the gap left by the geometry-only audit: the key set and the classes column are now independently reproduced as well.

## Part 2: S7 certificate-reuse partition of the 7,867-row worklist

Every worklist S6 is a 6-stone position; its 7th move x produces a 7-stone position S7 = S6 + x. An S7 can only belong to the existing certified pool if it contains one of the 94 oracle base positions (78 FW + 16 SW, 5 stones each) as a subset; since a worklist S6 never contains an oracle base in full, the only candidates have exactly one oracle stone outside S6 (|O \ S6| = 1) with x legal for S6.

Result (deduplicated by canonical S7 hex, all under the K0675 oracle conditioning):

- oracle-completing candidates: **8,763** across **6,276** distinct worklist S6s (1,591 S6s have no candidate)
- direct hits against the 62 focus2154 certificates: **0 WIN7**, and every LOSS7 of the 62 that arises this way is counted below
- known-LOSS candidates: **396** (in the 35 certified LOSS7 set, or in the LOSS7 pool = legal children of the 14 LOSS sweep S6, pool size 907)
- possible-win-pool candidates: **8,367** (the S7 has some 6-stone subset inside the judged 3,868-position sweep, so it *may* be a recorded win-child witness)
- unclassified candidates: **0** — the candidate set is completely partitioned.

Per-S6: **6,073** S6s have at least one possible-win-pool candidate; **374** have at least one known-LOSS candidate.

## External-lane action

Intersect the `s7_hex` column of `ms5_s7_reuse_candidates_part1..3.csv` (cat=2 rows) with the local win-child key pool (e.g. `/mnt/d/kyouen-focus-certs`). Each hit certifies its parent S6 as WIN (player to move), under the K0675 oracle conditioning, without any new search.

## Output files

- `output/ms5_s7_reuse_stats.json` — the counts above.
- `output/ms5_s7_reuse_candidates_part1..3.csv` — header `s7_hex,s6_hex,move,cat`; cat: 1 = known LOSS child, 2 = possible-win-pool. move is the 7th stone index (row-major, 0..120).
- `output/ms5_s7_knownloss_candidates.csv` — the 396 known-LOSS rows.
- `scripts/ms5_s7_reuse_analysis.ts` — regenerates everything deterministically, including the manifest derivation check.

## Status

This is verification and bookkeeping only. **No game verdict is established**: 11x11 empty root, two-stone root {49,60}, and S2 {59,60} all remain **UNKNOWN**. All win/loss statements above are conditioned on the K0675 oracles (78 FW + 16 SW positions).


## 2026-11-14 incremental reuse from later class2-lane certificates

The baseline 498-parent S7 reuse audit was extended with the cost-69c, cost-70b, cost-71, and cost-75 WIN7 certificate manifests. The 23 new roots are distinct and exactly safe; they yield 70 S6-parent incidences over 48 distinct worklist parents. After removing the five parents already covered by the baseline, **43 additional D4-canonical S6 worklist orbits** are covered. The remaining worklist falls from 7,369 to 7,326 rows, and the remaining legal seventh-move candidate cost falls from 577,110 to 573,835 (a reduction of 3,275).

This is certificate-reuse bookkeeping, not closure of S2 or the empty root. Certificate bodies were not re-run in this audit; see [the run log](../../log/2026-11-14-n11-s2-class2-win7-incremental-reuse.md), [the reproducible audit script](scripts/audit_incremental_class2_win7_reuse.py), and [the JSON result](output/class2-win7-reuse-incremental-20261114.json).

## 2026-11-14 v16 runner: signed transposition-key repair

The original `class4_child1_runner.ts` is retained as v15 for reproducibility. Its memo keys are stored in `Uint32Array`, while the live bitwise occupancy words are signed 32-bit values; strict equality therefore misses states whenever a word's high bit is set. The negative-bound arrays also used sentinel 255 with update conditions that could never succeed at search depths up to 10.

Use the separate `scripts/class4_child1_runner_v16.ts` for future sweeps after any already-claimed v15 job has completed. It compares keys as unsigned words and writes `mNoWin` / `mNoLose` bounds when the 255 sentinel is still empty.

Regression command (Node 22):

```sh
node --experimental-strip-types research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/class4_child1_runner_v16.test.ts
```

The fixed pilot is `loss=false` at 3,402 nodes. On child `00000000020000003800000280000000`, bit 15 at depth 8 with close-first AND, v15 used 146,514 nodes and v16 used 56,791; both returned `loss=false` and terminal range [13,15]. This is a bounded implementation regression, not a game verdict. A second case exercises the sign bit in the next word: on child `00000000000000809102000001000000` plus bit 0 at depth 8, v15 reached the 200,000-node cap while v16 completed in 121,837 nodes with `loss=false` and terminal range [13,15].

The in-flight cost-86c and cost-62a claims still use v15. Do not combine their raw batches with v16 results. Other copies of the signed-key pattern (sweep engine, chunk prover, certificate extractors, and FBT-saturation runners) still require separate audit before reuse.

## 2026-11-17 certificate extractor memo-key audit (K0907)

The 2026-11-14 v16 repair note above anticipated that the certificate extractor copies carry the same signed-key and dead-sentinel defects. `class4_child1_cert_extractor_exact.ts` (blob `52bacf509ea12fad4c936501d30d26b5b66c0085`) was audited and both defects confirmed; they are performance-only (the memo can miss but never produce a wrong hit), so every published certificate, node count and verdict remains valid.

A dump-only instrumentation of the verbatim engine (bit 0, first 12 loser moves, MS=1<<23, 834,262 nodes) quantified the duplicate-insertion mechanism: 216,719 stored records over 112,731 distinct keys; 16,417 keys have 2..64 copies and ALL of them are high-bit (bit 31 of words 0/1/2, i.e. positions on cells 31/63/95); no non-high-bit key is stored twice; 7 keys own their complete 64-slot probe window; every record keeps nowin=nolose=255 (the negative bounds never fire).

Measured on the published cost-73k band with fresh per-bit processes at MS=1<<23 and byte-identity gates against all 22 published certificates (split files concatenated): fixing the key sign alone (fixA) gives 75,108,849 nodes (69.23% of the verbatim fresh ms23 battery, -30.8%); fixing both defects (fixB) gives 28,290,025 nodes (26.07%, -73.9%; 18.14% of the published ms18 baseline, -81.9%). Per-bit memo occupancy is identical between fixA and fixB. Deterministic: fixB bit 0 = 1,277,392 nodes on repeated runs and the verifier reproduces its audit JSON byte-identically across two full runs.

The verbatim extractor is deliberately left unchanged (published determinism chains); see item K0907, the [run log](../../log/2026-11-17-n11-class2-lane-extractor-memo-sign-bug-and-fixed-battery-73k.md), [verifier](scripts/verify_extractor_memo_sign_bug_73k_20261117.py), [battery script](scripts/measure_fresh_battery_fixed_memo_73k_20261117.py), and the audit JSONs in `output/`. The remaining copies (sweep engine, chunk prover, FBT-saturation runners) are still unaudited. No verdict change: 11x11 empty root, two-stone roots, S2 {59,60}, classes 1/2/4 all remain UNKNOWN.

## 2026-11-17 worker-split memo merge measurement (K0909)

Two workers split the published cost-73k band at the natural gap of the bit list (A: bits 0..73, B: bits 76..117, 11 bits each, fresh process, band-wide memo within each worker, repo-verbatim engine at MS=1<<23 including its two known memo bugs) and dump their full memo tables (KYOENWM1). The tables merge offline (sort-based, streaming): per-key value combination (win=min, lose=min, nowin=max, nolose=max, 255=unbound), internal conflicts within each worker and cross conflicts between workers counted with sentinel-aware rules, and the merged table (KYOENWM2) re-seeds a single MS=1<<24 band run over all 22 bits.

Measured: workers total 119,962,147 nodes (0.9899 of the band ms23 single-process total 121,186,659; worker A reproduces the band ms23 per-bit prefix exactly, 48,482,011 nodes, final occupancy 5,263,320 - the two-worker split is slightly BETTER than one process at ms23 because it avoids the late-bit pollution of the 85%-load single table while keeping within-worker sharing). Distinct keys: A 2,619,833 / B 2,554,155 (duplicate keys are all high-bit, up to 64 copies - the signed-key duplicate-insertion mechanism quantified in K0907); merged occupied_after 4,291,899 with 882,089 keys shared across workers. Internal conflicts 0, cross conflicts 0: the verbatim memo values are globally consistent across workers, so worker caches merge safely and any WIN/LOSS contradiction would be detected immediately at merge time.

Merged-seed band run at MS=1<<24: 4,291,899 records seeded, 4,290,451 inserted, 1,448 (0.034%) failed because their 64-slot probe window was already full (verbatim hash clustering at 25.6% initial load; performance-only). The run extracted all 22 bits in 85,747,496 nodes (80.2% of the unseeded band ms24 106,861,135, 79.0% of the fresh ms23 battery), final occupancy 10,614,912 (load 63.3%). All 22 certificates byte-identical to the published bytes. Record-identity gate on the final dump: every inserted seed key is present with equal-or-stronger combined values (0 violations); missing keys are exactly the 1,448 failed inserts. The merge itself is deterministic (byte-identical on a second pass).

See item K0909, the [run log](../../log/2026-11-17-n11-class2-lane-worker-split-memo-merge-73k.md), the [orchestrator](scripts/measure_worker_split_memo_merge_73k_20261117.py), the [driver](scripts/measure_worker_split_memo_73k.ts) and the [measurement JSON](output/worker-split-memo-merge-73k-20261117.json). Measurement only: no verdict change, no manifest row opened or closed, certificate bytes unchanged; 11x11 empty root, two-stone roots, S2 {59,60}, classes 1/2/4 all remain UNKNOWN.

## 2026-11-17 4-worker N-way extension and fault-injection validation of the conflict detector (K0909 update)

The 2-worker measurement above left two gaps: the conflict detector had never fired (zero natural conflicts), and only N=2 was measured. This session closes both on the same band and verbatim engine.

4-way split, node-count balanced from the published per-bit values (W1 = bits 0,7,11,15,35,39,41 = the band ms23 prefix, W2 = 44,58,62,73,76,87, W3 = 89,94,95,97,98, W4 = 103,105,112,117), band-wide memo within each worker at MS=1<<23: workers total 112,741,501 nodes (0.940 of the 2-worker total, 0.930 of band ms23; W1 equals the band ms23 per-bit prefix exactly; certificates 7/6/5/4 byte-identical per worker). Distinct keys W1 1,979,858 / W2 1,793,658 / W3 1,544,867 / W4 1,565,935; internal conflicts 0 everywhere. Streaming heapq N-way merge-join of the sorted distinct tables: occupied_after 4,985,986 (+694,087 = +16.2% vs the 2-way union; the union GROWS because the finer split lowers per-worker table load and fewer keys are lost to 64-slot probe-window saturation in the dumps - a more complete merged table), shared_total 1,592,504, incidence histogram {1: 3,393,482, 2: 1,306,914, 3: 265,352, 4: 20,238}, cross conflicts 0, deterministic.

Merged-seed band run at MS=1<<24 (seed = the 4,985,986-record merged table): 76,903,818 nodes = 0.897 of the 2-way seedrun, 0.720 of the unseeded band ms24, 0.709 of the fresh ms23 battery; final occupancy 10,526,730 (load 62.7%); 22/22 certificates byte-identical; bit95 = 11,857,737 nodes again unchanged in every configuration (memo-state-invariant root). Seed insertion: 4,985,986 seeded, 4,969,849 inserted, 16,137 failed (0.324% at 29.7% initial load, vs 0.034% for the smaller 2-way seed - probe-window saturation grows superlinearly with seed size). The pre-registered <0.1% gate therefore fails (13/14 gates); the record-identity gate still closes: every inserted key survives with equal-or-stronger values (0 violations) and the missing keys are exactly the 16,137 failed inserts. Performance-only, soundness unaffected.

Fault-injection validation (7/7 gates): deterministic synthetic corruptions in copies of the real dump/distinct tables are detected EXACTLY - F1 (duplicate record with lose=3 appended to a copy of W2's raw dump) fires exactly 2 internal win_and_lose through the full sort+distinct pipeline; F2/F3 (cross lose/win injections on shared keys) fire exactly 4 cross win_and_lose; F4 (nowin:=win on a W4-only incidence-1 key) fires exactly 2 win_le_nowin; samples equal the injected keys, zero false positives. F5 (nowin:=4 / nolose:=2 injected into W3 records on W1&W3 shared keys) does NOT fire: the other workers' unbound 255 sentinels absorb the negative bound under the max-combine, and the fault-merged records are byte-identical to the clean merged records. The fault merge keeps the clean structural counts exactly. The merge-time detection catchment is thereby characterized: logical contradictions in the COMBINED values are detected exactly; a single worker's negative bound absorbed under others' sentinels is by design not a contradiction.

See item K0909, the [run log](../../log/2026-11-17-n11-class2-lane-worker-split4-memo-merge-73k.md), the [4-way orchestrator](scripts/measure_worker_split4_memo_merge_73k_20261117.py), the [fault-injection script](scripts/fault_inject_worker_merge_conflicts_20261117.py), the [4-way measurement JSON](output/worker-split4-memo-merge-73k-20261117.json) and the [fault-injection JSON](output/fault-inject-worker-merge-conflicts-73k-20261117.json). Measurement and synthetic-corruption tests only: no verdict change, no manifest row opened or closed, certificate bytes unchanged; 11x11 empty root, two-stone roots, S2 {59,60}, classes 1/2/4 all remain UNKNOWN.


## 2026-11-17 boundary-respecting 4-worker split memo merge (K0909, independent measurement)

Executed independently and concurrently with the node-balanced measurement above, in a separate environment instance, with a split that cuts at the same bit boundaries as the published 2-way split (39/41, 73/76, 97/98): W0 = bits 0,7,11,15,35,39, W1 = 41,44,58,62,73, W2 = 76,87,89,94,95,97, W3 = 98,103,105,112,117. The published 2-way workers are re-run inside the same orchestrator as anchors and reproduce the published measurement exactly (per-bit nodes and occupancy series, workers total 119,962,147, merged 2-way seed md5 e7c2c17e7a91d8ea17f433f3bb482f29 byte-identical).

4-way workers total 111,953,183 nodes (0.9332 of the 2-way total, 0.9238 of band ms23; 0.7% below the node-balanced split; W0/W2 equal the 2-way per-bit prefixes exactly; certificates 6/5/6/5 byte-identical per worker). All six pairwise merges and the cascade (M01, M23, FINAL4) have zero cross conflicts; FINAL4 occupied_after 4,975,265 (+15.9% vs the 2-way seed). Merged-seed band run at MS=1<<24: 76,599,320 nodes (0.8933 of the 2-way seedrun, 0.717 of the unseeded band ms24), final occupancy 10,525,071 (load 62.7%), 22/22 certificates byte-identical, seed insertion 4,975,265 seeded / 4,960,608 inserted / 14,657 failed (0.295%, independently confirming the superlinear probe-window saturation at the larger seed), record identity closed (0 violations, missing == failed inserts exactly). The complete pipeline ran twice with byte-identical output JSON.

Distinctive finding (merge non-closure): the 4-way merged table is NOT a superset of the 2-way merged table - 262 keys (0.0061%) that the 2-way workers memoized are absent from the 4-way union, while 683,628 keys are new. The verbatim memo's search and insertion are path-dependent, so merging finer-split workers' tables does not recover the coarser split's table; a coordinator must treat any merged cache as an approximation. Cardinality-wise the union is larger; set-inclusion-wise it is not. Cost-only, soundness unaffected. Two pre-registered expectation gates are falsified by measurement (superset; <0.1% seed-failure rate) and recorded as findings; all soundness, reproduction, conflict-detection and determinism gates pass.

See item K0909, the [run log](../../log/2026-11-17-n11-class2-lane-worker-split4-boundary-memo-merge-73k.md), the [boundary 4-way orchestrator](scripts/measure_worker_split4_boundary_memo_merge_73k_20261117.py) and the [measurement JSON](output/worker-split4-boundary-memo-merge-73k-20261117.json). Measurement only: no verdict change, no manifest row opened or closed, certificate bytes unchanged; 11x11 empty root, two-stone roots, S2 {59,60}, classes 1/2/4 all remain UNKNOWN.

## 2026-11-17 N-way merge seed capacity design (K0909 follow-up: gate-constant redesign)

Both 4-way measurements above broke the pre-run gate "seed insertion failure < 0.1%" at MS=1<<24 (node-balanced 16,137 = 0.324%; boundary-preserving 14,657 = 0.295%), while the 2-way seed (4,291,899 keys) passed at 1,448 = 0.034% - with record identity closed in every case. This measurement establishes the seed-capacity design rule. The published 4-way pipeline was rebuilt from pinned blobs (orchestrator 50b60247, extractor 52bcaf50, manifest 0892aed0, legal 8e97082c) and re-reproduced every published value exactly (workers, distincts, merge, merged seed md5 7b098aeb..., seedrun4 76,903,818 nodes with 16,137 seed failures, record identity); the 2-way pipeline was rebuilt likewise (workers A 48,482,011 / B 71,480,136 nodes, distincts 2,619,833 / 2,554,155, raw seed md5 1599c496..., published-header substitution reproducing the published md5 e7c2c17e... exactly).

A light occupancy-only simulator (light_sim_seed_73k.mjs: verbatim mHash + 64-slot linear probe window, per-base counters only) is exact for distinct-key seeding (the engine's key-match branch is unreachable) and matches both engine anchors at MS=1<<24 exactly (16,137 and 1,448). MS sweep of the 4-way seed: MS=1<<24 -> 16,137 failed (load 0.296), **MS=1<<25 -> 28 failed (0.00056%, load 0.149)**, MS=1<<26 -> 0. The MS=1<<24 failure knee in seed size S (real keys, merged insertion order): 1M/2M -> 0, 3M -> 26, 3.5M -> 256, 4M -> 2,017, 4.29M -> 5,969, 4.5M -> 8,233, 4.75M -> 11,410, 4.99M -> 16,137; the 0.1% gate boundary sits at S~4.1-4.2M keys, quantitatively explaining why the 2-way seed passed and both 4-way seeds failed. Failure mechanism: verbatim-hash clustering (largest base index carries 109 distinct keys; 250 of 1,224,783 non-empty bases hold >=64 keys; 2,278 own-cluster saturations + 13,859 spill-overs).

Design point MS=1<<25, full band, verbatim engine: seeded 4,985,986 / inserted 4,985,958 / **failed 28 = simulator prediction exactly**; certificates 22/22 byte-identical; record identity closed (missing == 28, violations 0). The design point is also cheaper: **72,745,351 nodes = 0.9459 of the MS=1<<24 seedrun (76,903,818)** - at MS=1<<24 the probe windows saturate during the band search itself, silently discarding ~3.5M memo entries (final occupancy 10,526,730 = load 0.627 vs 14,073,139 = 0.419 at MS=1<<25) and forcing re-expansion; every bit except the memo-state-invariant bit 95 (11,857,737 nodes at both MS, ratio exactly 1.0 - third independent confirmation) is cheaper. Design rule: seed N-way merged tables at load <= ~0.15 (MS=1<<25 for ~5M-key seeds); evaluate gates on seed load vs the knee, not a fixed failure rate at a fixed MS. All 16 gates pass; MS>=1<<26 engine runs are infeasible in this cgroup and are carried by the anchored simulator.

See item K0909, the [run log](../../log/2026-11-17-n11-class2-lane-seed-capacity-design-73k.md), the [design orchestrator](scripts/measure_seed_capacity_design_73k_20261117.py), the [light simulator](scripts/light_sim_seed_73k.mjs) and the [measurement JSON](output/seed-capacity-design-73k-20261117.json). Measurement only: no verdict change, no manifest row opened or closed, certificate bytes unchanged; 11x11 empty root, two-stone roots, S2 {59,60}, classes 1/2/4 all remain UNKNOWN.
## 2026-11-17 hybrid seed union measurement (K0909 follow-up: covering the 262-record merge non-closure)

The published hybrid seed union design (DESIGN_DERIVED_NOT_MEASURED, blob `8ec64f21`) is converted into a full measurement. The boundary-preserving FINAL4 seed (4,975,265 keys, md5 `35ccec0e`) and the published 2-way seed (4,291,899 keys, md5 `e7c2c17e`) are rebuilt from pinned blobs; the 262 only-in-2way records (md5 `1d97a0d2167506168faae5f3898ff952`, 13,356 bytes; deterministic re-extraction byte-identical) are reconstructed and appended after the FINAL4 records under the single published header, giving the hybrid seed: **4,975,527 records, 253,874,013 bytes, md5 `d24198ea37b31ffbd85ead4ba230560b`**, byte-prefix-identical to the published FINAL4 seed file (extra bytes exactly 13,356; FINAL4 prefix strictly key-sorted). Initial load factor at MS=1<<25 is 0.1482822597026825, equal to the design prediction to the last digit.

Simulator prediction (light_sim_seed_73k.mjs): MS=1<<24 -> 14,657 failed (exactly the published boundary FINAL4 anchor, under the design upper bound 14,919 - the appended records add no failure), MS=1<<25 -> 20, MS=1<<26 -> 0.

Engine measurement at MS=1<<25, full band, repo-verbatim engine: seeded 4,975,527 / inserted 4,975,507 / **failed 20 == simulator prediction** (0.00040%, the <0.1% gate passes with two orders of margin); **22/22 certificates byte-identical**; total **72,761,010 nodes**, final occupancy 14,065,965 (load 0.419). Ratios: 1.00022 of the node-balanced 4-way seedrun25 (72,745,351) - the hybrid seed buys coverage of the 262-record merge non-closure for +0.022% over the cheapest measured seed; 0.9499 of the boundary FINAL4 seedrun24 (76,599,320); 0.8485 of the published 2-way seedrun24 (85,747,496). bit 95 = 11,857,737 nodes unchanged (fourth independent confirmation of the memo-state-invariant root). Record identity closes: present 4,975,507 / missing == failed == 20 / value violations 0.

New verification pitfall (documented as experimental fact): the hybrid seed file is a FINAL4-sorted prefix with an unordered 262-record tail appended; a naive single sorted merge join mis-reads the tail and reports missing 282 (= 20 true + 262 tail). Run A fixed this by sorting the seed records before the external sort merge; run B implemented it structurally from the start (prefix merge join: present 4,975,245 / missing 20; tail hash join: present 262 / missing 0). Any future concatenated-seed record-identity gate must handle the unordered tail.

Execution and provenance: the measurement was executed to completion twice independently by concurrent hourly-lane sessions in the shared durable scratch (two independently written orchestrators, 824 and 957 lines, outputs finalized 14:10:02Z and 14:10:41Z, gates_all_pass=True in both; run B also re-ran the published boundary MS=1<<24 FINAL4 seedrun in-pipeline as an anchor, 76,599,320 nodes / 14,657 failed / 22/22 byte-identical). The claim-holding session's own run completed all six workers byte-identically to the published values before an environment reset destroyed its volatile workspace (recorded as experimental fact); it then independently verified both completed runs' artifacts (file hashes and structure, tail byte identity, 22/22 certificates against the published split parts, record identity recomputed with an independent implementation, per-bit sums, full cross-run agreement) and publishes the measurement on behalf of the claim.

See item K0909, the [run log](../../log/2026-11-17-n11-class2-lane-hybrid-seed-union-measurement-73k.md), the [run A orchestrator](scripts/measure_hybrid_seed_union_73k_20261117.py), the [run B orchestrator](scripts/measure_hybrid_seed_union_73k_independent_20261117.py), the [run A JSON](output/hybrid-seed-union-73k-20261117.json), the [run B JSON](output/hybrid-seed-union-measurement-73k-20261117.json) and the [independent verification JSON](output/hybrid-seed-union-independent-verification-73k-20261117.json). Measurement only: no verdict change, no manifest row opened or closed, certificate bytes unchanged; 11x11 empty root, two-stone roots, S2 {59,60}, classes 1/2/4 all remain UNKNOWN.

## 2026-11-17 8-way worker split memo merge (K0909 resume item)

The N-way worker-split line is extended from 4 to 8 workers on the same band and repo-verbatim engine. The 22 band bits are partitioned contiguously by DP min-max on the published band ms23 per-bit node counts (V1 = bits 0,7,11 = the band ms23 prefix anchor; V2 = 15,35; V3 = 39,41,44,58; V4 = 62,73,76; V5 = 87,89,94; V6 = 95,97; V7 = 98,103,105; V8 = 112,117), each worker a fresh process at MS=1<<23 with band-carried memo and per-bit snapshots.

Measured: workers total 110,639,931 nodes (0.9130 of band ms23 121,186,659, 0.9223 of the published 2-way 119,962,147, 0.9814 of the node-balanced 4-way 112,741,501, 0.9883 of the boundary 4-way 111,953,183) - the 2 -> 4 -> 8 progression is monotone on every published variant, with diminishing returns (2-way -> nb4 -6.0%, nb4 -> 8-way -1.9%). V1 equals the band ms23 per-bit prefix exactly (12,253,371 nodes, final occupancy 1,882,289 = BAND23_OCC[11]); every other worker's head bit reproduces the published fresh per-bit anchor exactly (gate). Head-bit fresh-vs-band-carried ratios: V2 0.9937, V3 1.0362 (the only reversal, bit 39), V4 0.7903, V5 0.8171, V6 1.0000 (bit 95), V7 0.8788, V8 0.7731 - at N=8 most fresh heads are CHEAPER than band-carried (consistent with the fresh ms23 battery total being below the band ms23 total), so the boundary 4-way's bit-41 reversal is an instance, not a law.

8-way heapq merge-join: distinct totals sum 7,914,609; occupied_after 5,243,408 (+22.2% vs the 2-way seed 4,291,899, +5.2% vs the nb4 seed 4,985,986; union growth flattens: 2->4-way +16.2%, 4->8-way +5.2%), shared 1,980,110, incidence histogram {1: 3,263,298, 2: 1,422,024, 3: 441,397, 4: 101,479, 5: 14,142, 6: 1,030, 7: 38, 8: 0} (no key is memoized by all 8 workers), internal conflicts 0, cross conflicts 0, merge deterministic (byte-identical repeat), seed8 md5 8d07cd7b82a3befc07cc775ea883e2e0.

Simulator MS sweep on seed8: MS=1<<24 -> 39,409 failed (0.7516%, load 0.3102; own-cluster 7,019 + spill-over 32,390, max cluster 130 keys, 563 bases >= 64 keys) - the third knee point 4.29M -> 1,448 / 4.99M -> 16,137 / 5.24M -> 39,409 confirms the superlinear growth; MS=1<<25 -> 383 (0.0073%, load 0.1563, slightly above the 0.15 design line but two orders below the 0.1% gate); MS=1<<26 -> 0 (load 0.0781, no base >= 64 keys).

Engine seedrun at MS=1<<25 (hardened fsync dump, cap 200): seeded 5,243,408 / inserted 5,243,025 / failed 383 == simulator prediction exactly (0.0073% < 0.1% gate); 22/22 certificates byte-identical; record identity closed (present 5,243,025, missing == 383, value violations 0); total 70,538,916 nodes (0.9697 of the nb4 seedrun25 72,745,351, 0.9172 of the nb4 seedrun24 76,903,818, 0.9695 of the concurrently published hybrid seedrun25 72,761,010); final occupancy 14,053,298 (load 0.4188); bit 95 = 11,857,737 nodes unchanged (fifth independent confirmation of the memo-state-invariant root). The larger 8-way union buys the cheapest measured band run on this band to date, and the sim == engine agreement extends one notch past the seed-capacity design calibration point.

See item K0909 (addendum 4), the [run log](../../log/2026-11-17-n11-class2-lane-worker-split8-memo-merge-73k.md), the [8-way orchestrator](scripts/measure_worker_split8_memo_merge_73k_20261117.py) and the [measurement JSON](output/worker-split8-memo-merge-73k-20261117.json). Measurement only: no verdict change, no manifest row opened or closed, certificate bytes unchanged; 11x11 empty root, two-stone roots, S2 {59,60}, classes 1/2/4 all remain UNKNOWN.
