# cost-72b 13 receipt foldのcross-lane独立検証 — head 1,188は両系統で一致

自レーン（長期class2レーン、毎時実行）はcost-72b foldを**並走レーンとほぼ同時に独立に実施**し、全計算量で一致した。並走fold（コミット `40e03194`、2026-11-14T22:56:48Z着地）が先にmainへ公開されたため、自レーンのfold成果物（同一ファイル名のJSON/CSV/スクリプト）は**重複pushを回避して未公開**とし、本entryでcross-lane検証の事実のみを記録する。この取り扱いは「push前に必ず最新mainを取り直し、競合時は無理に押し進げない」の運用規約に従う。

## 自レーンの実施内容（並走foldと独立に実行）

1. **baseline再現**: MS5 manifest入力から30スクリプトのrunpy鎖でcost-74d receipts head **1,179/6,668/526,075/4,938/389,798** を再現。head JSON（git blob sha `06724afe0698ce93319d092521c5887da6eec0f0`、11,449 bytes）とranking CSV 2件がmainとbyte-identicalであることを確認。
2. **13証明普のbyte検証**: 19 part（bytes×md5×git blob sha）＋結合whole 13件（md5×sha256×git blob sha）を `class2-lane-cost72b-win7-certificates-20261115.json` の記録値と照合。**13/13 OK**。
3. **13証明普の完全戦略再検証（新規の検証イベント）**: repo-verbatimの独立検証器 `verify_bit7_win7_cert.ts`（整数Bareiss 4x4、verdict cache不使用、engine不使用）を13証明普全件に再実行。各rootの敵の合法初手すべて（47〜64手）についてsub-rootごとに全戦略を再生し、**消費winner-stateの和集合が証明普の行集合と各bitで完全一致**（636,225/636,225行、union missing/extra 0/0）、sub-root **729/729 PASS**、root mobility == sub-root数、端末石数範囲 [13,17] 全件。landed foldのcontrol群はbyte/digest検証が中心のため、**全証明普の完全再生による再検証としては本実行が記録上最初**となる。
4. **foldの独立計算**: 独立に実装したfold scriptで、同じく1179 baselineから13 receiptを公閊bit順 (2,11,21,30,31,36,47,66,85,95,97,100,106) でfold（per-record marginalは拡大和集合から再導出）。子軌道 `00000000000000809102000002000000` は1179 baselineで既にsolved（74d bit91 receiptの交差被覆）であることを自前で確認し、provenance-completion foldとして計算継続。

## 一致の内容（landed fold vs 自レーン計算）

- **head**: 1,179 → **1,188/6,659/525,437/4,929/389,160**（両系統で完全一致）。
- **per-receipt marginal**: 全13 receiptのmarginal/marginal_in_manifest/marginal_manifest_hexesが受領順に完全一致。total marginal **57**、marginal_in_manifest **+9**（bits 2/30/31/36/47/95/97/100/106が各+1）。
- **zero-mim receipts**: bits **11/21/66/85**（85は74d bit91と同一D4軌道）。
- **+9軌道の帰属**: 9軌道すべてが共有open親S5 `00000000000000801202000020000000` のremaining行削減（56軌道 → 47軌道・4,199 → 3,561）。
- 子のpre-closureの解釈も一致（landed foldのrebase_noteにおけるD4軌道等価 72b bit85 == 74d bit91、canonical `00000000000080811202000020000000`）。

## 競合処理の記録（実験事実）

- 自レーンは22:50過ぎにfold claim `class2-lane-cost72b-fold-inflight-20261115.json`（コミット `1429ee68`、予測 +9 mim・新head 1,188を記載済み）をpushしてスコープ確保を図ったが、並走レーンのfoldは既に実行中で**数分後に着地**した。claimの存在は並走側の実行を停止させなかった（毎時並走の想定どおり）。
- 成果物push直前のmain再取得で着地を検出し、**重複するfold成果物（同一ファイル名3点＋fold script）のpushを中止**。未公開に留めた自レーン実装のfold script・出力JSON/CSVは、landed版と同じ入力・同じbaselineから独立に導かれた一致確認の証拠として本entryにのみ要數を記録する。
- 自レーンのclaimファイルは本コミットで `status: superseded-by-parallel-fold-cross-verified` に更新した（staleなin-flight残置を防ぐ）。

## 位置づけ

- head 1,188は**S6 manifest被覆の帳簿前進**であり、盤全体の勝敗ではない。WIN7証明普は個別7石rootの深さ10以内のWINのみを証明し、REFUTED-D10は「深さ10以内の先手勝ち不存在」であって子の反証ではない。**標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class2・class4はいずれもUNKNOWN。**
- 次の候補はlanded foldのoutstanding記録に従う: 親S5 `00000000000000809102000000000000` 残4子（cost-69子=69g並走in flight・cost-74第二子 `00000000000000809142000000000000` 未claim・cost-76子・cost-78子）、class-2次位 `00000000000000809082000000000000`（10軌道・698、audit要確認）。

成果物: [fold claim更新（status: superseded-by-parallel-fold-cross-verified）](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost72b-fold-inflight-20261115.json)、[並走foldのfrontier JSON](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-cost72b-receipts-recompute-20261115.json)、[並走fold log](2026-11-15-n11-class2-lane-cost72b-receipts-fold.md)、[13証明普manifest](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost72b-win7-certificates-20261115.json)、[独立検証器](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/verify_bit7_win7_cert.ts)。
