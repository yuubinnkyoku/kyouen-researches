# 2026-11-18 n11 class2-lane cost79c: 3 WIN7証明書のBigInt一般化円による独立検査

## 対象と方法

cost79cのraw sweepでWIN7-D10となり、証明書本体がmainに分割公開済みの3 root（bit 1・2・21）を検査した。各2分割ファイルはGit blob SHAで固定し、連結境界が行単位であることを確認した。

検査器はBigIntの3×3 Cramer係数から各3点が定める一般化円（円または退化直線）を構成し、盤上121セルを整数評価する。既存の探索器、verdict cache、4×4 Bareiss証明書検査器は呼び出さず、各rootで敗者側の合法な初手を全列挙し、その全てから先手の戦略手と敗者の全応手をたどった。各rootの戦略行集合と、実際に消費した先手局面集合が完全一致することを要求した。

## 結果

| bit | 戦略行 | rootの敗者合法手 | subroot訪問状態合計 | 終端状態 | 敗者応手辺 |
|---:|---:|---:|---:|---:|---:|
| 1 | 58,324 | 64 | 118,778 | 20,763 | 103,330 |
| 2 | 65,440 | 64 | 135,045 | 22,161 | 120,569 |
| 21 | 48,856 | 66 | 102,570 | 16,609 | 91,063 |
| 合計 | 172,620 | 194 | 356,393 | 59,533 | 314,962 |

3 rootはいずれも7石で安全。各subrootの終端石数はすべて13〜17。各証明書で戦略行の不足0・余分0。3 rootのD4正準形は相互に異なる。

bit21は公開済みrootcheck（7石・敗者合法手66）と一致し、公開済み66 subrootの訪問数・終端数・敗者応手辺・終端石数範囲も66/66すべて一致した。

## 境界と残件

これは個別の7石rootに対するWIN7戦略証明の独立検査であり、S6/S5 manifestへのreceipt foldではない。cost79cの他のWIN7 rootや、class frontierの閉鎖数は今回変更していない。REFUTED-D10は深さ10以内の反証であってLOSS証明ではない。

標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4はいずれもUNKNOWNのまま。

## 再現

Node.js 22、標準ライブラリのみ:

    node research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_cost79c_certificates_general_circle_bigint_20261118.mjs

出力JSONは同じ実験のoutput/class2-lane-cost79c-certificates-third-independent-audit-20261118.json。今回の監査計算は固定Git blobを取得して実行環境内の独立BigInt実装で行った。公開する再現スクリプト自体をcheckout上で実行したわけではない。
