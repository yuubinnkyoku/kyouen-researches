# 2026-11-15：cost70f / cost70g / cost71c の証明書間D4重複監査

監査時点のmain: `8a567006fcdf902a42b493568d02f5c1885e91d1`。canonical frontier headはcost71c fold後の **1235 / 6612 / 521,988 / 4,882 / 385,711**。同headにはcost72cの新しいin-flight claim（edge cost 72、c1=0,c2=2,c4=0）が追加されたが、今回の監査対象manifestは変わっていない。AGENTS.md、research/knowledge/README.md、K0783、K0023、cost70f/70g/71cの証明書manifestと直近logを確認した。

## 発見：cost70f bit84 と cost70g bit29 は同じ7石rootのD4軌道

raw bitboardは異なるが、11×11のD4正準化で一致した。

- cost70f bit84 root: `00000000001000801202000002200000`
- cost70g bit29 root: `00000000000100809002000020000800`
- 共通D4正準形: `00000000000100809002000020000800`

cost70gの8 rootは同lane内では8軌道だが、cost70fの4 rootと横断照合すると1軌道が重複する。raw hex検索だけではこの重複を検出できない。両certificateは各manifest内で独立検証済みだが、bit29はbit84と同じゲーム局面の別表現であり、新しいroot軌道を増やさない。

## 親S6軌道の重複

各7石rootから1石を削除して6石親を作り、8個のD4変換をBigIntで正準化した。

| lane | 証明書 | 親lift延べ | 異なる親軌道 | 延べ重複 |
|---|---:|---:|---:|---:|
| cost70f | 4 | 28 | 25 | 3 |
| cost70g | 8 | 56 | 49 | 7 |
| cost71c | 2 | 14 | 13 | 1 |

cost70fとcost70gの親軌道集合は **8軌道**で交差する。内訳は、D4重複root（70f bit84 / 70g bit29）の7親軌道がすべて一致し、さらに `00000000000000c09002000000000800` が1軌道共有される。後者はcost70f bit72とcost70g bit70の親liftに現れる。

一方、cost71cの13親軌道はcost70f・cost70gのどちらとも交差しない。3 laneの親軌道和集合は79軌道、root軌道和集合は13軌道。

## fold順への含意

cost70fを先にfoldすると、cost70gのchild `00000000000100809002000000000800` はcost70f bit84の7親liftの一つとして既に被覆される。したがってcost70gの後続foldでは、同childを新規被覆として二重計上してはいけない。

cost70fの後にcost70gを置いた場合、cost70gの追加分は、D4 root軌道で7、親lift軌道で41。ただし41はcost70f集合との差であり、canonical head 1235のmanifest未被覆数・marginal数ではない。既存headや他laneが既に覆った親軌道を差し引くには、fold scriptでbaselineの完全な被覆集合と再照合する必要がある。

これは証明書manifest間のD4集合監査であり、frontier foldではない。solved数・未解決class数・勝敗statusは変更しない。cost70f/70gの実際のfoldは、head 1235からの再基準化と、cost65l等の並走receipt確認後に行う。

## 再現

- script: [audit_cost70f_70g_71c_cross_lane_d4_overlap_20261115.mjs](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_cost70f_70g_71c_cross_lane_d4_overlap_20261115.mjs)
- output: [cost70f-70g-71c-cross-lane-d4-overlap-20261115.json](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/cost70f-70g-71c-cross-lane-d4-overlap-20261115.json)
- 入力manifest: cost70f / cost70g / cost71cの各WIN7 certificate manifest

検査器は公開manifestのroot・bit・parent liftを再計算する。証明書本体の再読込や戦略木の再検証は行わず、各manifestに記録された独立検証結果を前提としている。標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class1・class2・class4は引き続き **UNKNOWN**。
