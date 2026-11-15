# 2026-11-15：cost-77d receipts foldの独立事前予測 — bit-78候補が75d bit-92 receiptと同一root、fold後headは1302と予測

開始時状況: 同日のcost-75d receipts fold第二独立検証（[別log](./2026-11-15-n11-class2-lane-cost75d-fold-second-verification.md)）に続けて、並走laneがIN FLIGHTで掃引中のcost-77d（第二coverable class-2 target S5 `00000000000000801202000000200000` のcost-77 child `00000000100000801202000000200000`・77候補）について、公開済みの10 raw batches（77候補すべて完了・152,577,045 nodes・0 capped）から**foldの事前予測表**を独立に計算した。fold本体・証明書抽出は並走laneの領域であり、本logはfoldを実行しない・manifestを変更しない・claimしない予測のみ。

## 成果1：77d掃引の12 WIN候補のうちbit 78は75d bit-92 receiptと同一root（重複発見）

- raw batches再導出: 77候補一度ずつ・**12 WIN7-D10 bits [7, 12, 39, 58, 62, 64, 66, 78, 94, 96, 108, 111]**・65 REFUTED・0 capped・総nodes 152,577,045・pilot 3402×10
- **bit-78候補root `00000000100040801202000000200000` は、75d child `00000000000040801202000000200000` | 1<<92 とraw+D4完全一致** — すなわちhead 1296時点で既にfold済みの75d bit-92 receipt root（当時marginal 6/mim 2）。75d child（lift石78）と77d child（lift石92）が互いの相手のlift石を候補に加えた対称的な合成で同一7石配置に到達した
- このrootのcoversはhead 1296で全解決済み（予測marginal 0・検証assert済み）
- **77d foldへの含意**: 同foldのreceiptsにroot重複が含まれる初の事例。root在庫は11新規+1重複（新規12と数えるとauditのexactly-once簿記と衝突する）。75d側のbit-92 cross-coverでchild行が既に閉鎖（warm-hygiene）に加え、**bit-78 receiptはzero-marginalの重複receiptとして扱うか除外するか、fold scriptは明示的な処理を要する**

## 成果2：head 1296基準のfold完全予測表

`recompute_frontier_cost75d_receipts_20261115.py`のrunpy鎖でhead **1296/6551/517468/4821/381191**を再現（prev 569 roots）し、12 WIN rootの幾何（covers = 7石rootの各1石削除のD4正準S6 orbit）から:

- **新規root 11個**（bit 78を除く）: raw・D4とも相互distinct・fold済み569 rootとraw+D4 disjoint
- **union marginal 51・union in-manifest 6** → 予測fold後head **1302/6545/517025/4815/380748**
- **parent-A `00000000000000003800400008000000`（del-21側・64行/5036）は6行喪失** → 58行。ほか6 parentが各1行喪失
- **第二target S5（parent-B・11行/866）はさらに0行喪失** — 77d receiptsのdeletion orbitは第二targetの残行（cost 65〜84）をCoverしない。77d claimの動機（「第二targetを12行に減らす」）はhead 1290時点の記述であり、75d bit-92 cross-cover後のhead 1296では77d foldは第二targetの行数を減らさない
- **第二target S5の残11行の完全列挙**（fold後に残る行でもある）: cost 65 `00000000020000801202000000200000`・70 `00000000000000801282000000200000`・74 `00000000000000889002000000000800`・79 `00000000000000801212000000200000`・80 `00000008000000809002000000000400`・82 `00000000200040003800000000000200`・83×4（`...08000000200008` / `...08000000200010` / `...00000000400200` / `...00100000000200`）・84 `00000000000040809002000000000800`。**最安はcost-65行**で、77d後に次のsweep候補として最有力

## 解釈境界（重要）

- 12 WIN recordsはin-flight掃引のraw出力であって証明書ではない。予測は「全WIN候補が検証済みWIN7証明書として抽出される」ことを仮定した幾何のみの計算であり、determinism rerunやcross-engine不整合がWIN列表を修正する可能性は残る
- 予測head 1302はmanifest被覆の簿記であり、いかなる局面のgame-theoretic値も意味しない。REFUTED-D10はLOSS証明ではない。**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class1・class2・class4は引き続きUNKNOWN**
- 並走laneのfold scriptとcompleted claimが権威。予測との不一致が生じた場合はどちらかを強制せず、実験事実として記録する

## 再現

機械可読予測: [class2-lane-cost77d-fold-prediction-20261115.json](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost77d-fold-prediction-20261115.json)・予測script [predict_cost77d_fold_20261115.py](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/predict_cost77d_fold_20261115.py)（2回実行で出力byte-identical・md5 `c3572b07007267dc97f21e597f72ee4c`・9,929B）。

詳細: [77d claim](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost77d-inflight-20261115.json)、[75d fold head JSON](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-cost75d-receipts-recompute-20261115.json)、[75d fold第二検証log](./2026-11-15-n11-class2-lane-cost75d-fold-second-verification.md)。
