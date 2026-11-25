# 2026-11-15：cost-82c receipts foldの第二独立検証 — head 1306が再構築mirrorで再現・5証明書が第三幾何系で再検証

開始時状況: canonical head **1306/6541/516711/4811/380434**（cost-82c receipts fold・head JSON blob `4ee6aaab`・[fold log](./2026-11-15-n11-class2-lane-cost82c-sweep-certificates-and-fold.md)）。並走laneが着地したcost-82c fold（第二coverable class-2 target S5 `00000000000000801202000000200000` のcost-82 child `00000000200040003800000000000200`・5 WIN7-D10 bits [16,37,47,71,82]・head 1305→1306）を、mainとは独立にcodeload tarball（3.3GB・全体展開）から再構築した隔離mirrorで検証した。本logの検証は別環境・別実行によるもので、着地sessionの状態は一切再利用していない。82cのsweep入力（11 raw batches・determinism rerun・v15 crosscheck）・証明書5件（bit16/bit71単一ファイル・bit37/bit47/bit82行境界2分割）・tmp-cost82c抽出記録・completed claimはすべてmirror構築時点でmain済み。

## 成果1：published fold scriptのend-to-end再実行 — 全統制PASS・3成果物byte-identical

`recompute_frontier_cost82c_receipts_20261115.py`（blob `d43fa6e5`）を独立した短命subprocessで2回実行（各回約4秒・全111 CONTROL PRINT・2回のstdout同一）し、続けて検証script内でin-process runpyにより同じ鎖を再実行:

- **baseline再構成**: runpy鎖でcost-80d chain head 1305/6542/516793/4812/380516をhead JSON `289c9337` + 両CSVとともにblob一致で再現（それ以前のfold鎖は80d script内でchain-internallyにassert済み）
- **child genuinely remaining**: head 1305で両開親（第二target S5 9行/707・class-2 S5 `00000000000000003800000408000000` 60行/4936）がchild行を保持・demand c1=0,c2=2,c4=0・lift stones {78}/{9}
- **sweep再集計（独自コード）**: 11 raw batch JSONLsから82候補を一度ずつ（== claim列挙）・5 WIN7-D10 [16,37,47,71,82] / 77 REFUTED-D10 / 0 capped・総nodes 151,736,232（win sum 12,653,956）・terminal range [13,17]内・pilots 3402×11・determinism rerun node-exact・v15 cross-engine 5/5 WIN + 3/3 refuted anchors（bits 0/1/2・pilot 5949）
- **3成果物すべてmainとbyte-identical**: head JSON `4ee6aaab` 8,587B・ranking CSV `cc89c52b` 7,537B・top-candidates CSV `6a1a2185` 7,157B（git blob sha照合・2回のsubprocess実行間でも一致）

## 成果2：5証明書の第三幾何系（rational）による再検証 — 5/5 PASS

証明書5件を新規コードでpart-join（bytes / md5 / sha256 / git blob == extraction receipts・rows sorted-unique）し、published第三系検証器 `verify_cost75d_win7_rational_independent.py`（exact Fraction circumcentre / cross-product collinearity・ iterative replay・着地laneのBigInt 3x3・Number Bareiss 4x4とは別系統）で幾何再検証:

- **289,911 rows / 10,488,172 bytes / 311 sub-roots・5/5 PASS**: root safe（7石・4点共円/共線なし）・union missing/extra 0/0・terminal rangeはすべて[13,17]内（bit16は{13,15,17}）・consumed winner-row集合がpublished TS consumed filesと完全一致
- bigint.json / tsverify.json抽出記録とも一致（union 0/0・subroots == loser mobility・terminal_range [13,17]）

## 成果3：独立D4・逐次marginal算術 — published addition recordsと全field一致

独自D4群実装（8つの明示的affine行列の最小像・chain内canon()とは別実装で101 rootにて動作照合済み）で:

- 5 root == child|1<<bit・popcount 7・7 deletion-orbit covers・childは自身が正準形
- **逐次marginal規約どおりpublication order [16,37,47,71,82]で**: per-bit marginal / in-manifest / marginal_manifest_hexes / marginal_non_manifest_hexesがpublished head JSON addition recordsと**hex集合単位で全field一致**（総marginal 21・in-manifest 1・zero-mim [37,47,71,82]）
- child orbit closureはbit16の1回のみ・set等式 `s_1306 == s_1305 ∪ covers(5 roots)`成立
- **第二target S5 9行/707 → 8行/625**（喪失はchild行のみ）・第2開親 60行/4936 → 59行/4854（同）・head arithmetic 1305+1=1306
- **592-root在庫の軌道解析**: 587既存 + 5新規 = 592 roots・581 distinct orbits（576+5）・11 twin pairs（新twinなし）・5新rootは587在庫とraw-hex・D4ともdisjoint
- completed claim fold record（chain_head_before/after・publication order・totals 21/1・zero-mim・child closed by bit16・parents_after 8/625・59/4854・parents_lost_rows・output blob shas）と全field一致

機械可読検証記録: [class2-lane-cost82c-fold-second-verification-20261115.json](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost82c-fold-second-verification-20261115.json)（3,810 bytes・md5 `78f8d21d…`・2回実行byte-identical・検証script [verify_cost82c_fold_second_independent_20261115.py](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/verify_cost82c_fold_second_independent_20261115.py)・約2分26秒/回）

## 解釈境界（重要）

- solved 1306はmanifest被覆の簿記であり、いかなる局面のgame-theoretic値も意味しない。REFUTED-D10はLOSS証明ではない。WIN7証明書は個別7石rootからdepth-10以内の先手勝ちのみを証明する。
- 82c foldはchild orbitを閉じ、第二target S5の残行を9→8に減らすが、S5自体は解決しない。
- **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class1・class2・class4は引き続きUNKNOWN**。

## 今後

- 次のfold baselineはhead **1306**（`class-frontier-cost82c-receipts-recompute-20261115.json`・blob `4ee6aaab`）。
- 第二coverable class-2 target S5は8行/625（最安はcost-83の3行）・best class-4 blocker S5 `00000000020000003800000080000000` 18行/1460、いずれも未解決。
- 両audit script（v1系v4・第二実装v4・endpoint 80d/587 roots）のcost-82c endpoint（1306/592 roots）へのv5機械拡張（pins追加・own_claim/own_baseline・CANONICAL_LINE・endpoint）が次回以降の課題。着手前に必ず最新mainを再取得すること。

詳細: [82c fold head JSON](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-cost82c-receipts-recompute-20261115.json)、[82c fold script](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_cost82c_receipts_20261115.py)、[82c completed claim](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost82c-inflight-20261115.json)、[82c fold log](./2026-11-15-n11-class2-lane-cost82c-sweep-certificates-and-fold.md)、[80d fold第二独立検証](./2026-11-15-n11-class2-lane-cost77d-merged75d77d-79a-folds-second-verification.md)、[75d fold第二検証（前回）](./2026-11-15-n11-class2-lane-cost75d-fold-second-verification.md)。
