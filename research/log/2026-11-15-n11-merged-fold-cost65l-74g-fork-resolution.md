# 2026-11-15：cost-65l/74g 並行fold分岐の統合解決 — canonical head 1257 fork → 統合head 1270/6577/519427/4847/383150（74g fold独立検証込み）

開始時main: HEAD `e94f6b56`（自分の65l foldコミット `3ee9adc2` の後に並走のcost-74g sweep+証明書+foldが着地済み）。**問題の検出**: 並走の74g fold（`recompute_frontier_cost74g_receipts_20261115.py`・commit `c3a8d104`・head **1257→1266/6581/519710/4851/383433**）と本レーンの65l fold（commit `97d99a11`・head **1257→1261/6586/520097/4856/383820**）は**同一baseline 1257から分岐した並行fold**で、どちらのbranch head JSONも相手のreceiptsを含まない（74g foldの`outstanding_not_folded`は65lを「fold in flight」のまま記録・65l foldは74g着地前に確定済み）。このままではchain headが2つに分岐したまま後続foldのbaselineが不定になるため、cost-78a+69h統合の前例（`recompute_frontier_merged_cost78a_69h_20261115.py`）に従い統合foldで解決した。

## 74g foldの完全独立検証（統合の前提）

74g fold scriptの全入力（claim `class2-lane-cost74g-inflight-20261115.json`〔status completed〕・raw batches 10件〔再集計: 74候補・179,966,455 nodes〕・v16 determinism rerun・v15 crosscheck・`tmp-cost74g/` 51ファイル・証明書19ファイル合計23,085,545 bytes）をmainから再取得し、`recompute_frontier_cost74g_receipts_20261115.py` を本セッションのmirrorでend-to-end再実行:

- **全統制PASS**: runpy鎖（73h→70g→…）による1257 head再現（blob `71f79b4b`）・child genuinely remaining（第三target 2行/143 + 第2親 `00000000000000003800000008000010` 64行/4813がchild行を保持・demand c1=0,c2=2,c4=0再導出）・sweep再導出（74候補一度ずつ・10 WIN7-D10 [4,11,20,44,69,95,100,108,109,116]・64 REFUTED・0 capped・179,966,455 nodes・pilot 3402×10・determinism rerun node-exact・v15 10 WIN + アンカーbits 0/1/2）・証明書10件のjoined LF bytes検証（639,189 rows/23,085,545 bytes/600 sub-roots・BigInt+Bareiss 10/10 union 0/0）・root disjointness vs 532 folded roots（raw+D4）・fold（総marginal 49・in-manifest 9・zero-mim [11,20]・child bit4閉鎖・第三target 2/143→**1/69**・第2親 64/4813→55/4143）・completed-claim closure control（claim fold recordの全fieldと出力3 blob再assert）。
- **再生成3出力はmainとbyte-identical**: head JSON blob `fce4ce77`（12,590B）・ranking CSV `d3c24ddc`・top-candidates CSV `cd6d395e`（cmp照合）。
- **prose erratum記録**: 74g head JSONのcontrol key `root_disjointness_vs_512_roots` は「512」と記載しているが、fold scriptのassertは正しく `len(prev) == 532`（528+4の73h鎝までの折り畳みroot数）。proseのみの誤記で数値・計算への影響なし。本統合で真の532-root集合に対するdisjointnessを改めて検証した。

## 統合fold（`recompute_frontier_merged_cost65l_74g_20261115.py`）

78a+69h統合の構成を踏襲し、以下を1プロセスで実行（**3回連続実行すべてbyte-identical**）:

1. **fork再現**: 73h fold scriptをrunpyしhead **1257/6590/520380/4860/384103**（head JSON blob `71f79b4b`・fold済みroot 532個）を再現。
2. **両branch head JSONのblob検証**: 65l `0b523e70`（9,260B）・74g `fce4ce77`（12,590B）。rootsは両head JSONのaddition recordから取得（65l [21,48]・74g [4,11,20,44,69,95,100,108,109,116]）。
3. **12 rootの相互disjointness（raw+D4）**: 65l-vs-74gの**クロス組を含む**（両branch foldはそれぞれ532-root集合に対してのみassertしており、この組はどちらにも検証されていなかった）。PASS・532-root集合とも無重複。
4. **両chainのforkからの正確な再導出**: 65l（per-bit marginals 5/2・5/2 == published・child bit21閉鎖・head 1261/6586/520097/4856/383820）・74g（per-bit marginals == published・child bit4閉鎖・head 1266/6581/519710/4851/383433）。
5. **分岐addition・overlap**: addA=10・addB=49・**raw overlap=0・covers overlap=0**（完全疎）。
6. **統合逐次replay**（65l公開順→74g公開順）: 74g-stageのmarginalsを統合stateに対して再計算してもpublishedと完全一致（**cross-chain二重被覆なし**・deltas none）。両child閉鎖はbit21（65l stage）・bit4（74g stage）で各1回。
7. **set等式**: `s_merged == s_1261 UNION s_1266 == s_1257 UNION covers(12 roots)`。**reverse-order replay（74g先）も同一集合**（可換性統制PASS）。
8. **統合head: solved 1270 / unique 6577 / cost 519,427 / open 4,847 / open_cost 383,150**（= 1257 + 4 + 9・unique 6590−13・cost 520380−953）。per-parent行会計: 第二coverable target S5 `00000000000000801202000000200000` **17行/1325**・class-4 lift親 `00000000020000003800000000000200` **75行/5519**・第三coverable target S5 `00000000000000809102000000000000` **1行/69**・74g第2親 `00000000000000003800000008000010` **55行/4143**。両child行は全親のremaining rowsから消滅をassert。

出力4ファイル（merge script blob `bd694237`・merged head JSON `02109530`〔12,459B〕・ranking CSV `5d88b9c1`・top-candidates CSV `7de39cf8`）をcommit `5ac44005` でpush・remote raw CDNでcmp照合一致（4/4）。

## 統合後の前線

- **best coverable class-2: 第三target S5 `00000000000000809102000000000000` 残り1行/69**（cost-69行 `00000000000000809102000000002000`）。この行がWIN7 receiptで閉じれば第三target S5の全行が閉鎖され、class-2 blockerが条件付きで閉じる。並走がIN FLIGHT claim済み（commit `44ed8003`）。
- best class-4 blocker S5 `00000000020000003800000080000000` 18行/1460（不変・最安行73f/74f/74cはすべてsterile sweep済み）。
- audit-blocked class-2 `00000000000000809082000000000000` 10行/698。
- 第二coverable target S5 17行/1325（最安未sweep行はcost-70 `00000000000000801282000000200000` だが70dとしてsterile sweep済み・次はcost-74/75/76/77帯）。

## 信頼境界

- foldは公開済みreceiptの帳簿更新であり、いかなる局面の勝敗判定でもない。solved 1270はmanifest被覆のみを測る。
- WIN7証明書は各7石rootから深さ10以内の先手勝ちのみを証明する。REFUTED-D10はLOSS証明ではない。
- 両child orbitの閉鎖は親S5の残行からchildを除くが、どのS5親も未解決のまま（第三targetは残り1行）。
- **標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class1・class2・class4はすべてUNKNOWN**。次のfold baselineは統合head **1270**（`class-frontier-merged-cost65l-74g-recompute-20261115.json`・blob `0210953083309c1dd2d8f1cf036ec1f91e88f267`）。

詳細: [merged head JSON](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-merged-cost65l-74g-recompute-20261115.json)、[merge script](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_merged_cost65l_74g_20261115.py)、[ranking CSV](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-s5-ranking-after-merged-cost65l-74g-20261115.csv)、[top-candidates CSV](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-top-candidates-s6-after-merged-cost65l-74g-20261115.csv)。
