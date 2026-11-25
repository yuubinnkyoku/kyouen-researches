# 2026-11-16：cost-64g bit-89 foldの独立投影・並走fold receiptとの完全一致 — head-1438 solved集合の全出版物からの再構成 761 roots・投影head 1441/174/6407/506945/4680/370859・mim 3・5親delta一致・AGREEMENT PASSED

開始時main: `6c2693f3`（本レーン直前のverification JSON fix再出版）。作業中、並走レーンが**cost-64g fold receipt（bit 89）を `f14f8bdb`（2026-11-16 08:05:57Z）で着地**させた。本レーンの計算設計・入力収集は並走fold receiptの公開に先立ち準備され、全入力はblob-pinnedな**fold前**成果物のみで並走fold成果物を一切読まない。ただし最終完全実行は並走着地後に完了したため、本成果は厳密なtiming事前登録ではなく**独立投影・一致検証（independent-projection agreement check）**として位置づける。script名・schemaから「preregistration」の語を除去し「independent-agreement」に改めたのはこのため。

## 検証内容（出力 `output/class2-lane-cost64g-bit89-fold-independent-agreement-20261116.json`・schema `...-independent-agreement-20261116-v1`・git blob `f74df27e`・決定性2回byte-identical確認済み）

### head-1438 solved集合の全出版物からの独立再構成
- solved集合 = winners 498 ∪ covers(全出版receipt roots **761** = base 194 [26個のWIN7-only base certificate files] + chain 567 [91 chain-head JSONs: 52 pinned pre-70e + 35 pinned post-70e + 4 unpinned first-generation 71c `61af2eb3`/70f `4d0f130e`/73g `e4fb98dc`/70g初世代 `73890fe3`] + 5 later fold heads 75e/60c/65j/64d/64f)。manifest rows 7867・incidences 14558。
- frontier semantics（images/canon/covers/frontier/summary_state）はpublished `recompute_frontier_full.py` からverbatim移植した**別実装**で再構成。並走のfold receipt内部再現はpublished fold scriptのrunpy再実行（同一script）だが、本レーンはroot収集経路そのものが独立（114+4ファイルからの直接抽出 vs fold script系列の内部累積）。
- **head-1438完全一致**: 1438/174/6410/507143/4683/371057・demand histogram全バケット一致・cost-64g child `00000000000100003800000008080000` の両open class-2親 30/2081・50/3631完全一致。roots 761 → D4 canons **746**。

### bit-89 fold投影と並走fold receipt `f14f8bdb` との完全一致
- WIN7-D10 receipt root bit 89 `00000000020100003800000008080000`（証明書 git blob `1d2cc167`・本レーンの前回logでbyte-identical盲抽出・BigInt/Bareiss両PASS済み）をfold。
- **全項目が並走fold receipt（`class-frontier-cost64g-receipts-recompute-20261116.json`）と完全一致**:
  - marginal 6 / **marginal_in_manifest 3**: child + cross-class open rows `00000000000000801202010000080000` + `00000000020000801002010000080000`（並走 `totals.rows_closed_hexes` と同一集合）
  - **投影head 1441/174/6407/506945/4680/370859**（並走 `frontier_after_cost64g` 6数値と同一）
  - demand histogram deltas: `c2=0,c4=2`/`c2=2,c4=0`/`c2=2,c4=2` 各 -1
  - 5 open parentsのdelta完全一致: `00000000000000003800000008002000` 30→29/2081→2017・`00000000000000801202010000000000` 50→48/3631→3498・`00000000000000003800001000800000` 66→64/4719→4585・`00000000000000801202000000080000` 67→66/5135→5066・`00000000020000003800000000080000` 60→59/4288→4223（並走 `parents_after` と同一）
  - parent-row incidences 7（lost rows per parent 1/2/1/2/1）・parent edge cost delta 465（64+134+69+133+65）— 並走 `totals.parent_row_incidences=7`/`parent_edge_cost_delta=465` と同一
  - D4 orbit独立: folded canons 746 + bit89 canonで747、全folded rootsとD4-canonicalにdisjoint — 並走のconflict census zero overlapsと整合

### 簿記差の記録（被覆への影響なし）
- 本レーン再構成761 receipt roots vs 並走内部再現760 receipt roots。**D4 canonsは両者746で一致**し、head-1438全数値・histogram・fold投影が完全一致するため、被覆solved集合は同一。差は同canon orbit内のhex数え上げの経路差（本レーンのglob収集はmerged/unified/warm系recompute JSONを含む一方、並走fold系列はreceipts系の内部累積）と推定されるが、並走の内部root hexリストが成果物に保存されていないため確定はできない。以後の照合はcanon数（746）とhead 6数値を基準にする。

## 意義

1. **cost-64g fold receipt `f14f8bdb` のfrontier再計算が、別実装・別root収集経路（114+4ファイルからの独立抽出）で完全再現**された。並走のrunpy再現（同一script再実行）とは独立の第二証拠であり、fold receiptのauditに本record（blob `f74df27e`）をpinできる。
2. 新canonical head **1441/174/6407/506945/4680/370859** への遷移が二重に独立確認された。以後の次target選定・censusはこのheadを基準とする。
3. solved集合再構成の入力ファイル群（26 base + 91 chain-head + 4 unpinned heads + 5 fold heads、全blob-pinned）がrepo公開物のみでhead-1438を再現できることを確定 — solved 1438（→fold後1441）の独立性検証可能性が完全に閉じた。

## 解釈境界（重要）

- solved 1441はmanifest被覆の簿記であり、どの位置のgame-theoretic valueも示さない。WIN7-D10証明書は7石root `00000000020100003800000008080000` から深さ10以内の先手勝ちのみを証明する。REFUTED-D10はLOSS証明ではない。
- **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class1/class2/class4は引き続きUNKNOWN**。
- 本レーンはfold claimを作っていない。foldの着地とrunpy再現は並走 `f14f8bdb` のものであり、本recordは独立投影による一致検証のみ。

## 今後

- 次target選定は並走のcost-64g fold後ranking（`class-frontier-s5-ranking-after-cost64g-receipts-20261116.csv`・fold receiptのbest_class2 `00000000000000801202000000200000` 3 rows/209等）依存。重複回避のため本レーンは新規claimを作らない。
- 並走の次fold着地時は、本recordの再構成法（761 roots・verbatim移植frontier semantics）で同様の独立投影・一致検証を行う。
