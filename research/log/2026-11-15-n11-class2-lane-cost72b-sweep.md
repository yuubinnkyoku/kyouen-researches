# n11 class2: cost-72b子sweep完了（72候補・WIN7-D10 13件・打切り0）

2026-11-15 JST。第三class-2 coverableターゲットS5 `00000000000000809102000000000000` の次の未sweep子で、69g（並走in flight）を除く最安の子 `00000000000000809102000002000000`（cost 72、需要c1=0,c2=2,c4=0、open親2軌道: `00000000000000801202000020000000`(classes=2, rem 58) と `00000000000000809102000000000000`(classes=2, rem 7)）をclaimしてsweepした。claimは `class2-lane-cost72b-inflight-20261115.json`（main 50d2773c時点で未claimを確認）。

## 実行

- 候補列挙: `legal_candidates.py`（独立Bareiss 4x4整数行列式）で72候補。manifest edge cost 72とbit-exact一致。
- engine: repo-verbatim `class4_child1_runner_v16.ts`（blob sha 0a4a86f6…照合済み）、depth 10・cap 1e9・andclose=1。pilot d6制御 3,402 nodes は全10 batchでPASS。
- batch構成: claimでは9 batch×8を計画したが、実際はbit分割ミスで **10 batch（7+8×8+1）** になった。72候補は重複・欠落なく1回ずつ実行（集計スクリプトでbit集合の完全一致と重複0をassert）。

## 結果

**WIN7-D10 13件・REFUTED-D10 59件・打切り0、候補節点 117,444,772**（wall ~248s）。終局石数範囲は全行 [13,17]。

WIN7-D10 bits: **2, 11, 21, 30, 31, 36, 47, 66, 85, 95, 97, 100, 106**（v16 nodes: 3,579,035 / 662,882 / 1,490,927 / 1,465,190 / 2,481,547 / 1,674,157 / 2,272,166 / 2,387,057 / 1,027,754 / 5,701,307 / 833,113 / 4,134,068 / 4,655,532）。

### 交叉検査

- **v15 cross-engine**（`class4_child1_runner.ts`、pilot 5,949 nodes制御PASS）: 13 WIN bits全件 loss=true（v15 nodes 4,379,235〜18,036,593、計132,170,428）。REFUTEDアンカー bits 0/9/120 は loss=false（17,153,894 / 15,092,796 / 8,201,963）。
- **決定性再実行**: 別プロセスで13 WIN bits全件再実行、**13/13 node-exact**（`ms`のみ相違）。
- **D4軌道**: 13 rootは**13個の異なるD4軌道**（正準形hexはsweep recordに記録）。
- **先行公開チェック**: 13 root hexすべてGitHub code searchで0ヒット（main 50d2773c時点）。

## 意味と境界

- 13 WIN7-D10は**探索候補**であり証明書ではない。S6 frontierへの寄与は現時点で0。子軌道の被覆には証明書抽出（blind抽出器・FBS 1<<20・fbt_drops 0）とfrontier foldが必要。次回以降の作業。
- REFUTED-D10は「深さ10以内の先手勝ちなし」であって子の反証ではない。
- cost-72bは最初のcost-72子 `00000000000000803202000000000200`（bits 52/111、111は証明書済み）との混同を避ける命名。

## 成果物

- [sweep記録](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost72b-sweep-20261115.json)
- [claim（status更新済み）](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost72b-inflight-20261115.json)
- raw batch 1–10・v15 crosscheck 4件・determinism rerun: 同output/の `class2-lane-cost72b-*`

**標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class2・class4は引き続きUNKNOWN。**
