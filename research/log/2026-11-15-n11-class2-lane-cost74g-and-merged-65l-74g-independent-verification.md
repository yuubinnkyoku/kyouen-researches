# 2026-11-15：cost-74g foldと65l/74g統合foldの第二独立検証 — 分岐の独立検出とmerged head 1270再現

開始時状況: 同日のcost-65l fold第二独立検証（[別log](./2026-11-15-n11-class2-lane-cost65l-fold-independent-verification.md)）に続き、同じ再構築mirror（codeload tarballから独立に構築・mainとは別環境・別実行）でcost-74g foldを検証した。検証中に、74g fold（`c3a8d104`・head 1257→1266）が65l fold（`97d99a11`・head 1257→1261）と**同一baseline 1257から分岐した着地**であることをpublished成果物のみから独立に検出した。その後、並走laneがcollision protocolにより統合foldを着地済み（script+成果物 `5ac44005`・log `eae89730`）であることを確認した。本logは(1) 74g fold scriptの第二独立検証、(2) 統合fold scriptの第二独立検証、(3) 付随するerratum・baseline fence状況を記録する。

## 成果1: 74g foldの第二独立検証 — 全統制PASS・3成果物byte-identical

main版script（git blob `5ce9dd31`・API取得テキストとmirror版でblob一致）を再構築mirrorでend-to-end再実行し、全CONTROL PASS:

- **baseline再構成**: runpy鎖で73h chain head **1257/6590/520380/4860/384103**（head JSON blob `71f79b4b`・10,965B）を再現
- **child remaining統制**: child `00000000000000809142000000000000` はhead 1257でgenuinely remaining・両開親（第三target S5 `00000000000000809102000000000000` 2行/143・parent2 `00000000000000003800000008000010` 66行/4964）がchild行を保持・demand c1=0,c2=2,c4=0再導出
- **sweep再導出**: 74候補を一度ずつ・10 WIN7-D10 bits [4,11,20,44,69,95,100,108,109,116]・64 REFUTED・0 capped・総nodes **179,966,455**・pilot 3402×10・determinism rerun node-exact・v15 cross-engine WIN 10/10 node-matched
- **証明書検証**: 10証明書をjoined LF bytesで検証（**639,189 rows / 23,085,545 bytes / 600 sub-roots**・BigInt+Bareiss 10/10・union 0/0）
- **fold**: head **1266/6581/519710/4851/383433**・総marginal 49・in-manifest 9・zero-mim [11,20]・childはbit4（公開順最初）で閉鎖・第三target 2/143→**1/69**・parent2 →55行/4143
- **3成果物ともmainとbyte-identical**: head JSON `fce4ce77`（12,590B）・ranking CSV `d3c24ddc`（7,579B）・top-candidates CSV `cd6d395e`（4,662B）
- completed claim（`class2-lane-cost74g-inflight-20261115.json`・status completed）のfold record全field一致（PASS）

## 成果2: 1257分岐の独立検出

74g再実行の過程で、74g fold scriptのbaselineが65l foldと同一の73h head 1257であり、両branch head JSONが互いのreceiptsを含まない（74g fold recordの`outstanding_not_folded`は65lをfold-in-flightのまま記録）ことを検出した。この分岐はpublished artifactsのみから再構築可能であり、本検証は分岐が第三者からも検出可能であったことを実証した。並走laneは同様に検出し、前例（cost-78a+69h統合）に従うcollision protocolで統合foldを着地済みだったため、追加の介入は不要と判断した。

## 成果3: 統合foldの第二独立検証 — merged head 1270再現・3成果物byte-identical

`recompute_frontier_merged_cost65l_74g_20261115.py`（git blob `bd694237`）をmirrorで再実行し、全統制PASS:

- **fork再現**: head 1257（`71f79b4b`）・両branch head blob検証（65l `0b523e70`・74g `fce4ce77`）
- **12 rootの相互disjointness**: 65l-vs-74gのクロス組を含めraw+D4とも無重複（cross-chain組はどちらの単独foldでも検証されていなかった組）
- **両鎖の再導出**: 65l head 1261・74g head 1266ともpublished per-bit marginalsと完全一致
- **addition/overlap**: addA=10・addB=49・raw overlap=0・covers overlap=0（完全疎）
- **逐次replay**（65l公開順→74g公開順）: 74g-stage marginalsは統合stateに対する再計算でもpublishedと完全一致（cross-chain二重被覆なし）・**逆順replay（74g先）も同一集合**（可換性統制PASS）
- **set等式**: `s_merged == s_1261 UNION s_1266 == s_1257 UNION covers(12 roots)`
- **統合head**: **1270/6577/519427/4847/383150**（= 1257+4+9・unique 6590−13・cost 520380−953）・総marginal 59・in-manifest 13
- **per-parent行会計一致**: 第二target S5 `00000000000000801202000000200000` **17行/1325**・class-4 lift親 `00000000020000003800000000000200` **75行/5519**・第三target S5 `00000000000000809102000000000000` **1行/69**・74g parent2 `00000000000000003800000008000010` **55行/4143**（parent2は65l段階でmarginal行の共有により2行減る66→64行、74g段階でさらに9行。単独74g鎖の1257起点66→55と統合後の55行はset等式により同一集合）
- **3成果物ともmainとbyte-identical**: merged head JSON `02109530`（12,459B・git blob直接照合）・ranking CSV `5d88b9c1`（7,579B）・top-candidates CSV `7de39cf8`（4,576B）・両CSVはget_file_contents APIのSHAで照合

## prose erratum（74g script・本logで新規記録）

74g fold scriptのresult dict内`baseline_main`欄は「class-frontier-cost72c-receipts-recompute-20261115.json … blob `42dbb92e`」と73h head数値「1257/6590/520380/4860/384103」が混在している。これはclaim作成時baseline（72c head 1244・blob `42dbb92e`）とfold実行時baseline（73h head 1257・head JSON blob `71f79b4b`）の取り違えであり、実際のassert（head JSON blob `71f79b4b`・10,965B）は正しい。proseのみの誤記で数値・計算への影響なし。なおhead JSON control key `root_disjointness_vs_512_roots`（assertは正しく532）は統合log側で記録済み。

## claim baselineのfence状況

- 69h claim（`44ed8003`）は分岐済みbranch head 1266/6581/519710/4851/383433を参照したまま → fold着地時はmerged head **1270**へのrebaseが必須（child行・marginal・parent残行の再導出が必要）
- 74h claim（`ea458c63`）はmerged head 1270を正しく使用中

## 解釈境界（重要）

- solved 1270はmanifest被覆の簿記であり、いかなる局面のgame-theoretic値も意味しない。REFUTED-D10はLOSS証明ではない。WIN7証明書は個別7石rootからdepth-10以内の先手勝ちのみを証明する。
- 両foldともchild orbitの閉鎖と親S5の残行削減のみで、どのS5親も未解決（第三targetは残り1行）。
- **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class1・class2・class4はすべてUNKNOWN**。

## 今後

- 次のfold baselineは統合head **1270**（`class-frontier-merged-cost65l-74g-recompute-20261115.json`・blob `02109530`）。
- 第三target S5の残り1行（cost-69行 `00000000000000809102000000002000`）が69h laneでIN FLIGHT（rebase必要）。
- 第二target S5 17行/1325の最安未sweep行（child `00000000000000889002000000000800`・cost 74）が74h laneでv16 d10 sweep IN FLIGHT。
- 並走laneと重複してsweepせず、着手前に必ず最新mainを再取得すること。

詳細: [merged head JSON](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-merged-cost65l-74g-recompute-20261115.json)、[merge script](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_merged_cost65l_74g_20261115.py)、[74g fold script](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_cost74g_receipts_20261115.py)、[74g claim](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost74g-inflight-20261115.json)、[merged ranking CSV](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-s5-ranking-after-merged-cost65l-74g-20261115.csv)、[merged top-candidates CSV](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-top-candidates-s6-after-merged-cost65l-74g-20261115.csv)、[統合fold log](./2026-11-15-n11-merged-fold-cost65l-74g-fork-resolution.md)。
