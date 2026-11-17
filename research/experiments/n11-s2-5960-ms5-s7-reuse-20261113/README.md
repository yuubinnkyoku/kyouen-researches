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
