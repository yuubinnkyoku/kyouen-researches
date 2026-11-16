# 2026-11-16 n11: corpus全体 raw-vs-audit node合計一貫性監査 — 29監査・273 rawバッチ・471チェック・0不一致

## 背景

69h race修復（前ログ `2026-11-16-n11-class2-lane-cost69h-race-repair-raw-restore.md`・commit `4885d75e`）で判明した通り、bit集合照合だけではrace clobber（batch1のnode drift +611,900）を検出できない。この検出ギャップを埋めるため、**main出版済みの全sweep-audit JSON（29件）に対して、現mainのraw batchファイルから独立に再導出したnode合計・bit集合・候補数・WIN7 bit集合・記録済みgit blob sha1を突き合わせる監査**を実施した。

## やったこと

1. **監査script `audit_corpus_raw_vs_audit_nodes_20261116.py`**（stdlibのみ・json/hashlib/os/sys/collections・engine不使用・`bytes([0])`でpaste転写事故を回避）を新規作成し、**5世代のaudit schema**を全部処理:
   - **A**: `.batches[]`がfile/nodes/candidate_bitsを持つ（60c・62b・63f・64c・65k・69h・70d・70e・70f・70j・71c・72c・73f・73g・73h・74f・74h・82b・84・87の20監査・188バッチ）
   - **B**: input_path/candidate_nodes（69f・9バッチ・aggregate total込み）
   - **B'**: input_pathのみ+`.aggregate`総計（74d=101,848,441・76a=131,329,581・78a=184,253,822）
   - **C**: input_path/git_blob_sha+`.sweep_totals.node_sum`（75e・76d・**記録済みgit blob sha1をsha1("blob len\0"+bytes)で再計算照合**）
   - **D**: `.raw_sweep`総計（70c・total 100,935,666・unique 70 bits・WIN7 bits 13個一致）
   - **E**: `.raw_batches[]`+`.candidate_nodes_total`（63g=75,637,935・67c=41,942,979）
2. **結果: 29監査・273 rawバッチ・471チェック・0不一致**。69h復元済みbatch1/2/3も含めて、**現mainのsweep corpusに他のrace clobberは存在しない**。75eの10バッチは記録済みgit blob sha1とも全一致（byte-level検証）。
3. **出版**（commit `f44f9f3a`・2ファイル・着地後commitピンrawでmd5照合 byte-exact: script `d5126775…`・JSON `d261b571…`・**出版版scriptの再実行PASS・出力byte-identical**）: scripts/`audit_corpus_raw_vs_audit_nodes_20261116.py` + output/`corpus-raw-vs-audit-node-sum-audit-20261116.json`。

## 意味

- 69hの3ファイルがrace corpus全体で唯一のclobberだったことが確定（修復済み）。
- 今後のsweepでは、raw出版時にaudit集計（batch nodes / candidate_nodes / sweep_totals）を必ず添付し、本監査script（schema追加で拡張）を回すことで同種事故を即座に検出できる。
- **verdictへの影響なし**。REFUTED-D10はLOSS証明ではない。STERILEもLOSS証明ではない。

## レジューム

- canonical head **1410不変**。次回の大工事は65j fold（fold chain再構築→`recompute_frontier_cost65j_receipts_20261116.py`新規作成→cover mapの34行×remaining set交差で閉鎖見込み確定）。69a着地監視（K0863予測: bit 109 REFUTED-D10）。76d/77e fold着地時は1410 headとのreconciliation必須。
- **solved 1410はmanifest被覆の簿記。11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class1/class2/class4はいずれもUNKNOWN**。
