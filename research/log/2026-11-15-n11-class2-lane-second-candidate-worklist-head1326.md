# 2026-11-15：head 1326の第二候補S5残34行のworklist分析 — 次sweep候補の需要導出・cost-63行4件が最小（58cはIN FLIGHT除外）・第二target S5残3行の内訳

published fold-chain監査v9両実装+agreement v6（[第一実装log](./2026-11-15-n11-class2-lane-published-chain-roots-audit-v9-first-implementation.md)・[第二実装log](./2026-11-15-n11-class2-lane-published-chain-roots-audit-v9-second-implementation.md)・[agreement v6 log](./2026-11-15-n11-published-fold-chain-dual-implementation-agreement-v6-84a-62a-pair.md)）の着地後、canonical head 1326（cost-62a receipts fold・blob `3989e9dd`）における**第二候補（second coverable class-2 candidate）S5 `00000000000000801202000040000000` の残34行**を機械分析した。分析はpublished fold script（`recompute_frontier_cost62a_receipts_20261116.py`・runpy全鎖）のnamespaceから純簿計で導出（sweepも候補列挙も実行せず）。tmp-cost83c/83d/84a/62aはpublished再構成script（83c `reconstruct_tmp_cost83c_20261115.py`・83d `reconstruct_tmp_cost83d_second_independent_20261115.py`（unlink安全の第二実装）・84a `reconstruct_tmp_cost84a_20261116.py`・62a `reconstruct_tmp_cost62a_20261116.py`）で全再生し、fold scriptはhead JSON・両CSVのblob一致を再assertした（head 1326/6522/515251/4792/378974の再現を兼ねる）。

## 成果1：残34行のcost histogramと次sweep候補の需要

- **parent1（第二候補S5・class 2）: 34 rows / 2,368 edge cost**（62a前は39/2708・foldでchild含む5行喪失）。**parent2（class-2 S5 `00000000000000003800000008001000`）: 48 rows / 3,582**。**両worklistの共有行は1行のみ**（`00000000000000801202000040001000`・cost 65・demand c1=0,c2=2,c4=0）——62a childの2開親構造は解消済みで、以後のsweepは2親で重複しない
- **cost histogram（34行）**: 58×1・63×4・64×2・65×1・66×1・67×3・68×2・69×1・70×2・71×4・72×2・73×2・74×2・75×2・76×4・77×1
- **cost-58行はIN FLIGHT**（並走claim commit `908716e1`・cost-58c・着手禁止）。**除外後の最小costは63の4行**: `00000000000000801202000040080000`（c1=0,c2=2,**c4=2**）・`00000000000000881202000040000000`（c2=2）・`00000000000000c09002000001000000`（c2=2）・`00000000040000003800000048000000`（c2=2）。4行中3行がclass-2専用需要・1行がclass-2+class-4複合需要（当該行のsweepはclass-4側の被覆にも波及する可能性）
- 出力: [worklist JSON](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-second-candidate-worklist-head1326-20261115.json)（10,080 bytes・md5 `f9d6f93ae1508ae8a1db20719afd50f2`・2回実行byte-identical）

## 成果2：第二target S5 `00000000000000801202000000200000` 残3行の内訳

- 残3行 / 209: **cost 65** `00000000020000801202000000200000`（c1=0,c2=2,c4=0）・**cost 70** `00000000000000801282000000200000`（c1=1,c2=1,c4=0）・**cost 74** `00000000000000889002000000000800`（c1=0,c2=2,c4=0）
- 84a/62a両fold時点でこの3行のdepth-10 sweepは全候補REFUTED-D10であり、**depth-10 receiptではこのS5は閉鎖不能**（深さ11以上か別証明手法が必要）。3行のcost合計209は不変

## 解釈境界（重要）

- 34行/48行/3行はすべてmanifest被覆の簿記であり、いずれのS6/S7の勝敗も意味しない。REFUTED-D10はLOSS証明ではない。
- **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class1・class2・class4は引き続きUNKNOWN**。cost-58c（IN FLIGHT・`908716e1`）には一切着手していない。

## 今後

- 次sweepはcost-63行4件（上記）が最小非IN FLIGHT対象。58c着地後はv10監査拡張+agreement v7が定型。

詳細: [分析script](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/analyze_second_candidate_worklist_head1326_20261115.py)（純簿計・runpy namespace由来・sweep/列挙なし）。
