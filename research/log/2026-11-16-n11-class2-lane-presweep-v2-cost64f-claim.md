# 2026-11-16：head-1435 pre-sweep census v2（cost-64e STERILE verdicts収集込み）+ cost-64f claim v1 — 次対象行 `0000000000000080120a000000800000`（59 open bits）・11×11はUNKNOWN

開始時main: `c277a616`（cost-64e completed STERILE直後・並走の新着なし）。本レーンはcost-64e sweep完了（60/60 REFUTED-D10・STERILE・head 1435不変）を受け、**census再計算（v2）と次行claim**を着地した。

## census v2（`next_target_presweep_head1435_v2_20261116.py`）

1. **harvest拡張**: v1のprotocol-2親census（`next_target_presweep_head1435_20261116.py`）は64e raw batchをharvest対象に含めていなかった（スクリプト作成時点で存在しなかった）。v2では**cost-64e raw batch 8本（claim v2 blob `55c51c92`のbatch bit lists・60 swept bits・4 pre-sweep transfersとbit-exact検証）をharvestに追加**。結果: **harvest 4,182 distinct canon（WIN 426 / REFUTED 3,756 / conflict 0）**（v1比 +60 canon、全REFUTED-D10）。
2. **検証**: 64e raw batch 60 canonは他ソース（claim v2 JSON harvest経由）と**60/60 cross-agree・conflict 0**。runpy fold chain再現（head 1435・全assert再実行）と`legal_candidates.py`独立候補列挙のbit-exact assertも全て再実行。
3. **census結果**: 完全確定行は**3行**（v1比 +1）: cost-64c STERILE行 `00000000000000003800000008002020`・**cost-64e STERILE行 `0000000000000000380000000a002000`（今回確定追加）**・cost-65転送行 `00000000020000801202000000200000`。family: class-2 target `00000000000000403800000008000000` 18行/1287 occ → **open 1,131 distinct canon**（v1と同数）・shared `00000000000000003800000008002000` 31行/2145 occ → **open 1,473 distinct canon**（v1 1,533から−60）。
4. **新ランキング**: 最安open行は**`0000000000000080120a000000800000`（class-2 target parent・cost 64・demand c1=0,c2=2,c4=0・64候補中59 open・5 REFUTED転送済み [21,35,55,64,109]）**。次点 `00000000000100003800000008080000`（59 open・同cost）・cost-65 2行（各60 open）が続く。

## cost-64f claim v1

- child `0000000000000080120a000000800000`（stones [23,49,51,57,60,71]）・**既存claim/raw batch/audit/certificate/fold receiptとの重複なし**（`80120a`系inflightは62aの別child・近傍分析`sterile-rows-neighbor-analysis`では65k STERILE行の最安近傍として言及のみ）。
- 5 transfer bits [21,35,55,64,109]はD4-canonical identityによるREFUTED-D10転送（再sweep対象外・cost-64eと同規約）。
- protocol: v16 engine（depth 10・cap 10,000,000・pilot_d6 control 3402・8bit×7+3bit×1の8 batch・raw batch JSONL出版・determinism rerun・v15 crosscheck・WIN7があれば証明書抽出→fold、REFUTEDのみならSTERILE記録）。

## 解釈上の注意

**censusは探索計画の簿記であり、本作業でengine探索は実行していない（claim v1出版時点）。WIN7-D10証明書は個別7石rootのfirst-player win（depth 10以内）のみを証明。REFUTED-D10はLOSS証明ではなく、STERILEもLOSS証明ではない。solved 1435はmanifest被覆の簿記。標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class1・class2・class4、両開親は引き続きUNKNOWN。**

## 成果物

- census v2 script: [next_target_presweep_head1435_v2_20261116.py](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/next_target_presweep_head1435_v2_20261116.py)
- census v2 JSON: [class2-lane-next-target-presweep-1435-v2-20261116.json](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-next-target-presweep-1435-v2-20261116.json)（blob `e2d12b5b`）
- census v2 rows CSV: [class2-lane-next-target-rows-1435-v2-20261116.csv](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-next-target-rows-1435-v2-20261116.csv)（blob `0a3bab02`）
- cost-64f claim v1: [class2-lane-cost64f-inflight-20261116.json](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost64f-inflight-20261116.json)

## 次回

- cost-64f sweep（8 batch・v16）の実行・raw batch出版・claim v2更新。WIN7があれば証明書抽出（`cert_driver65j.ts`パターン）→fold→head前進。REFUTEDのみならSTERILE確定を記録。
- 並走in-flight着手禁止: 76c `00000000010000809092000001000000`・69a `00000000000000801222000000800000`。
