# 2026-11-15：cost-76a receipts fold 完成（chain head 1188 → 1195）と cost-72b 再実行不能の透明修復

開始時main: `7fcc8945`（cost-72b chain head `1188/6659/525437/4929/388160` 掲載済み）。AGENTS.md、research/knowledge/README.md、cost-72b/76a関連のclaim・manifest・audit、直近の11×11実験・logを確認した。

## 成果1：cost-72b recompute script の透明修復（commit b4d655f9）

`recompute_frontier_cost72b_receipts_20261115.py` はclaimファイル `class2-lane-cost72b-inflight-20261115.json` の公開時点blob sha（`e8ede675…`）をassertしていた。その後の正当なclosure追記でclaimのblob shaが `b1c135c539e20c0ae94cdc2e66d769911af5eb7d` に変わり、**公開済みのchainが再実行不能**（assert失敗）になっていた。

- 修正はembedされたsha 1点のみ。算術・出力は無変更。
- 修復後、1188 head JSON・両CSVがmain掲載版とbyte-identicalに再現（remote blob sha照合済み: script `6c4b8a4f…`）。
- docstringに修復noteを明記し、claim closure追記が再実行を壊す経緯を記録した。
- **運用教訓**：以後のfold scriptは「closure後のclaim blob sha」をassertする（cost-76a fold scriptは `7922a02a…` をassertし、無期限に再実行可能）。claim側をclosure後に更新する運用でもよい。

## 成果2：cost-76a 6-receipt fold 完成（commit 753c01b1）

`recompute_frontier_cost76a_receipts_20261115.py`（37,783 bytes、remote blob `9090e4c86795f96864c0d83bd66db18b35ea88e2` 照合済み）で、cost-76a sweep の証明書付きWIN7-D10 receipts 6件（bits 11/29/66/80/92/96）を1188 headにfoldした。

**新canonical chain head: `1195/6652/524884/4922/388607`**（`class-frontier-cost76a-receipts-recompute-20261115.json`、remote blob `efd83f2637f83c0e1c5c477dcb0cc42162cda534`）。remaining S5 orbits 175。

- total marginal 31 / marginal_in_manifest +7。zero-mim receipts なし。
- bit11 receiptが子orbit `00000000000000809102000000000001` 本体＋交差被覆 `00000000000000801202000000200400` を閉鎖。bits 29/66/80/92/96 が各1件（`…8012020000020004 00` 系5件）を閉鎖。
- 第3target class-2 S5 `00000000000000809102000000000000` は残り4行（69/74/76/78 = 297）→3行（221）。残る69（cost-69g）/74（cost-74e）/78（cost-78a）はすべて並走レーンでin flight。
- 両open parentからchild行が落ちたことをbit-exactで検証。set-equality管理 `s_after == s_1188 ∪ covers(6 roots)` 成立。
- 統制: 72b chain head のrunpy全再現（1188 byte-identical）、16入力ファイルのgit blob sha照合、sweep auditをraw 10 batchから再導出（76候補、6 WIN7-D10 / 70 REFUTED / 0 capped、131,329,581 nodes）、v15 cross-engine anchors（6 WIN node一致、3 REFUTED、pilots 5949×6）、証明書6件のbytes再検証（md5×sha256×git blob、8 parts + 6 wholes、union 0/0、terminal 13..17）、第三独立audit JSON全項目一致、root disjointness（90既fold roots、raw + D4両方）。4回実行すべてbyte-identical。

## 並走衝突の記録

自claim（c1f3028f、00:48:12Z）pushの約1分後、並走実行が同fold claim（c4767883、00:49:28Z）をstale-fetchで上書きした。c00b4543（00:51:19Z）で自版を復元し、衝突をclaimのclosureに `concurrent_claim_note` として記録した。並走が独立に算出したfoldは同一算術になるはずであり、公開された場合は衝突プロトコル（cost-72b precedent）に従って相互検証する。

## 次への指示

- **cost-78a fold（並走、証明書公開中）は新head `1195/6652/524884/4922/388607` にrebase必須**。以後のrecompute/claimはこのheadをassertして拡張する。
- cost-69g / cost-65j / cost-74e レーンは並走in flight。次回の統一fold前に各receiptの最新を再確認する。
- 第3targetの残り3行（69/74/78）はすべて並走が担当中のため、こちらからは触れない。

## 勝敗status

標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class 2、class 4 はすべて **UNKNOWN**。本foldはmanifest被覆のbookkeepingであり、いかなる局面のgame-theoretic valueも確定しない。REFUTED-D10 sweepはWIN7-D10不在のみを証明し、WIN7証明書は個々の7石rootからdepth 10以内の勝ちのみを証明する。
