# cost-72b 13 WIN7 receipt fold — chain head 1,179 → 1,188（cost-74dへのrebase）

自レーン（class2 lane）が第三class-2 coverableターゲットS5 `00000000000000809102000000000000` の子 `00000000000000809102000002000000`（cost 72、需要c1=0,c2=2,c4=0）について、公開済み・独立検証済みの**13 WIN7-D10証明書**をreceiptとしてchainにfoldした。並走レーンのcost-74d fold（head 1,163 → 1,179）が先に着地し、そのbit91 receiptが本72b子軌道をD4等価liftで閉鎖済みだったため、claim記載の `rebase_required` 指針どおり**head 1,179をbaselineにrebaseして**foldを実施した。

## rebaseの経緯（実験事実）

- 本foldの1163基準版は総marginal 64 / mim +12（新head 1,175）まで実行済みだったが、main再取得で並走レーンのcost-74d fold（コミットf07e316c、15 receipt・bit118証明書付き、head 1,179）が先に公開されていたことが判明。1,175は兄弟分岐になるため公開せず、**1179基準に全面的に書き直した**（1,163版の成果物は未公開・破棄、出力3ファイルはrebase版で上書き）。
- 並走レーンはclaimをmain上で更新し `rebase_required` ブロック（baseline_head 1179）を追記していたため、それに従った。
- **D4重複の判明**: cost-72b bit85 root `00000000002000809102000002000000` と cost-74d bit91 root `00000000080000809102020000000000` は**同一D4軌道**（canonical `00000000000080811202000020000000`、変換 (x,y)->(x,10-y)）。chain内部の `canon()` で両rootの同一正規形をassertし、**別軌道として二重計上していない**。bit85証明書は74d側raw receipt（証明書抽出pending）の証明強化として機能する。

## Controls（すべてPASS、2回実行で出力3ファイルbyte-identical）

1. **baseline再現**: runpy鎖（full → bands → merged → 69e/70c → 75b/75c → multiband → 68d → unified 1154 → 69f 1163 → warm3 1163 → 74d 1179）でcost-74d chain head **1179/6668/526075/4938/389798** をbyte-identical再現し、head JSONのgit blob sha `06724afe0698ce93319d092521c5887da6eec0f0`（11,449 bytes）をmainと照合。warm3 1163（blob sha 50735896…）とunified 1154もchain内部でassert。
2. **入力のmain照合**: 72b材料18ファイル（sweep・raw batch 10件・v15 crosscheck・determinism rerun・claim・証明書manifest）すべてgit blob shaでmainとbyte-exactであることをassert。
3. **子の残存制御**: 1163基準（claim baseline）では親のremaining行に子（cost 72）がgenuinely残存することをchain内部のwarm3 remaining集合から歴史制御としてassert。1179では74d bit91の交差被覆で両open親から既にchild行が消滅していることをassert。
4. **sweep再導出**: 10 raw batchから72候補が重複なく1回ずつ、pilot 3402制御10/10、13 WIN7-D10 / 59 REFUTED / 0 capped / 117,444,772節点、win root == child|1<<bit、13 distinct D4 orbits。
5. **v15 cross-engine anchors**: 13 WIN bits全件 loss=true（nodesはsweep記録と全件一致）、REFUTED anchors bits 0/9/120 loss=false、pilot 5949×4。**v16 determinism rerun**: 13 bits全件 node-exact、pilot 3402。
6. **13証明書のbyte検証**: 19 part（bytes×md5×git blob sha）＋結合whole 13件（md5×sha256×git blob sha）、rows sorted-unique、header/root整合、sub_roots == loser mobility、union 0/0、terminal 13..17、fbt_drops 0、v15/v16 anchor node一致。manifest totals再集計: **636,225 rows / 729 sub-roots / 200,029,509 extraction nodes**。
7. **root disjointness**: 13新root vs 77個のfold済みreceipt root（62 + cost-74d 15）でraw-hex交差空。既知のD4軌道等価はbit85==74d bit91の1件のみで、`canon()` 照合により軌道としての重複を明示。
8. **fold**: 公開bit順 (2,11,21,30,31,36,47,66,85,95,97,100,106) で13 receiptをfold、per-record marginalを拡大和集合から再導出。**全receiptが子軌道に対してnon-marginal**（子は1179でpre-closed）、set-equality s == s_1179 ∪ covers(13 roots) 成立。

## 結果 — chain head 1,188

- **total marginal = 57、marginal_in_manifest = +9** → 解消S6 manifest 1,179 → **1,188**、unique remaining 6,668 → 6,659、sum cost 526,075 → 525,437、open需要 4,938 → 4,929 / 389,798 → 389,160。残りS5軌道175（不変）、c2=2,c4=0バケット 1,009 → 1,000。
- zero-mim receipts: **bits 11/21/66**（manifest内で完全に既被覆）＋**bit 85**（74d bit91と同一D4軌道のため）。
- **mim +9はすべて共有open親S5 `00000000000000801202000020000000` のremaining行削減**（56軌道・4,199 → 47軌道・3,561、bits 2/30/31/36/47/95/97/100/106のlift）。
- 親S5 `00000000000000809102000000000000`（第3class-2 coverableターゲット）: **4軌道・297で不変**（72b子とbit85軌道は74d foldで既閉鎖）。
- per-record marginal: bit2/30/31/36/47/95/97/100/106 = +1、bit11/21/66 = 0、bit85 = 0（D4 dedup）。

## Incident記録（実験事実）

- fold準備中に実行環境がリセットされ、ローカルのworkdir（`/home/user/kr`、抽出成果物・cache一式）が消失した。**mainに公開済みの成果物のみで環境を再構築**（chain scripts 39本の再帰fetch、参照input 253件、72b材料18件＋19 part、6分割証明書はpart結合でwhole再現）してfoldを完遂した。失われたのはローカル中間ファイルのみで、再現不能な重要証拠は残っていない。
- 欠落入力の動的fetch中に1件のtransient curl失敗（bit105 part）があったが再fetchで解消。main上に存在しない11件の参照（chainが読まないもの）は404のまま無視。
- 1163基準foldの実装に由来する2件の実行時エラー（NameError: 未定義変数参照）を修正後に完走。失敗実行も含め、成果はmain公開物から独立に再現・検証可能。

## 位置づけ・次の作業

- 本foldの+9は**S6 manifest被覆の前進**であり、親S5（残4軌道）・S2 {59,60}・11×11空盤の勝敗は不変。WIN7証明書は個別7石rootの深さ10以内のWINのみを証明する。**標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class2・class4はいずれもUNKNOWN。**
- 次の候補: 親S5 `00000000000000809102000000000000` の残る4子のうち、cost-69子（69g、並走in flight）とcost-74第二子 `00000000000000809142000000000000` は未claim。class-2次位は `00000000000000809082000000000000`（10軌道・698、audit要確認）。
- cost-74d側の残り14 WIN7 bitsの証明書抽出は並走レーンが継続中（bit12 1/19が公開済み）。cost-69f bits 2/94/109/119の証明書抽出も未了。

成果物: [frontier再計算JSON](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-cost72b-receipts-recompute-20261115.json)、[ranking CSV](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-s5-ranking-after-cost72b-receipts-20261115.csv)、[top-candidates CSV](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-top-candidates-s6-after-cost72b-receipts-20261115.csv)、[foldスクリプト](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_cost72b_receipts_20261115.py)、[claim更新（status: folded-into-chain-head-1188）](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost72b-inflight-20261115.json)。
