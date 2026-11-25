# 2026-11-15：cost-65l foldの第二独立検証 — head 1261が再構築mirrorで再現

開始時状況: 同日のcost-73h fold第二独立検証（[別log](./2026-11-15-n11-class2-lane-cost73h-fold-independent-verification.md)）に続き、並走laneが着地したcost-65l fold（`97d99a11`、head 1257→1261）を同じ再構築mirrorで検証した。本logの検証は、mainとは独立にcodeload tarballから再構築した別環境・別実行によるもの。65lのsweep入力（8 raw batches・determinism rerun・v15 crosscheck・extraction summaries 2件・BigInt cert-verify records 2件・parent-lift analysis）・証明書2件（single files）・sweep claim・fold claim v1はmirror構築時点でmain済みだった。fold script（blob `01a73f2f`）とclaim v2（blob `dea8bd08`）のみをmainから追加取得して実行した。

## 成果：published fold scriptの再構築mirrorでの再実行 — 全統制PASS・3成果物byte-identical

`recompute_frontier_cost65l_receipts_20261115.py`をそのまま実行し、全CONTROL PASS:

- **baseline再構成**: 73h fold script（blob `ce4f7d9a`・本mirrorで同一検証済み）をrunpyで再現し、1257 head JSON `71f79b4b`・両CSV（`ee4cc2ff`・`122803ea`）ともblob一致（それ以前のfold鎖は73h script内でchain-internallyにassert）
- **入力検証**: 17 published cost-65l input filesをgit blob shaでbyte-exact検証（claim 2件は内容検証）
- **rebase control**: child `00000000220000003800000000000200` はhead 1257でgenuinely remaining・class-2 lift親 `00000000000000801202000000200000` は18行/1390（1227以来31→18行に縮小してもchild行を保持）・class-4 lift親 `00000000020000003800000000000200` は77行/5655（無傷）・demand c1=0,c2=1,c4=1再導出（stone-89 D4-canon → class-2親 / stone-93 D4-canon → class-4親）
- **sweep再導出**: 65候補を一度ずつ（claim列挙と一致）・2 WIN7-D10 [21,48]（nodes 712,251 / 882,679）・63 REFUTED-D10・0 capped・総nodes 44,268,335・pilot 3402×8・determinism rerun（batch-2・WIN bit 21込み）node-exact・v15 cross-engine 2/2 WIN node-matched（1,772,664 / 2,492,516）+ refuted anchor bit54 raw verdict一致
- **証明書検証**: 2証明書を実bytesで検証（git blob sha == claim receipts `6cdd6d0d`/`06bc8da7`・rows sorted-unique 28,523+31,817 = 60,340・extraction nodes 3,110,330+4,694,247 = 7,804,577再総和・sub-roots 51+50 == root mobility・BigInt verify records union 0/0・per-move terminal [13,17]部分集合・fbt_drops 0・parent-lift analysis cross-check）
- **root-orbit簿記**: 2新root vs 532 fold済みroot（528 through 73h baseline + 4 73h）、raw-hex・D4ともdisjoint
- **fold結果**: **head 1261/6586/520097/4856/383820**・総marginal 10・in-manifest 4（zero-mim/zero-marginal receiptsなし）・per-receipt marginals bit21→(5,2)・bit48→(5,2)・childはbit21（公開順最初）で閉鎖・set等式 `s_after == s_1257 UNION covers(2 roots)`・class-2親 18行/1390 → 17行/1325（child行のみ喪失）・class-4親 77行/5655 → 75行/5519（child + bit48 marginal由来1行喪失）
- **3成果物すべてmainとbyte-identical**: head JSON `0b523e70` 9260B・ranking CSV `af64bbe3` 7580B・top-candidates CSV `1b2b66fe` 4663B（git blob sha照合）
- 着地済みclaim v2 fold record（chain_head_before/after・receipts・per_receipt_marginals・zero_mim/zero_marginal・child_closed_by_bit・parents_after・parents_lost_rows・output_blob_shas）とsection 9で全field一致（PASS）

## 解釈境界（重要）

- solved 1261はmanifest被覆の簿記であり、いかなる局面のgame-theoretic値も意味しない。REFUTED-D10はLOSS証明ではない。WIN7証明書は個別7石rootからdepth-10以内の先手勝ちのみを証明する。
- 65l foldはchild orbit `00000000220000003800000000000200`（bit21）を閉じ、class-2/class-4両lift親の残行を減らすが、どちらのS5親も解決しない。
- **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class1・class2・class4は引き続きUNKNOWN**。

## 今後

- 次のfold baselineはhead **1261**（`class-frontier-cost65l-receipts-recompute-20261115.json`・blob `0b523e70`）。
- 第2 coverable class-2 target S5 `00000000000000801202000000200000` は17行/1325・class-4 S5 `00000000020000003800000000000200` は75行/5519・73h parent2 `00000000000000003800200008000000` は64行/4962、いずれも未解決。
- 並走lane状況: cost-74g sweepが着地済み（`c3a8d104`・74候補・10 WIN7-D10 bits 4/11/20/44/69/95/100/108/109/116・64 REFUTED）でfold待ち。69g / 65j / 74eも並走中。重複してsweepせず、着手前に必ず最新mainを再取得すること。

詳細: [65l fold head JSON](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-cost65l-receipts-recompute-20261115.json)、[65l fold script](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_cost65l_receipts_20261115.py)、[65l claim v2](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost65l-fold-inflight-20261115.json)、[65l ranking CSV](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-s5-ranking-after-cost65l-receipts-20261115.csv)、[65l top-candidates CSV](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-top-candidates-s6-after-cost65l-receipts-20261115.csv)、[65l fold log](./2026-11-15-n11-class2-lane-cost65l-receipts-fold.md)。
