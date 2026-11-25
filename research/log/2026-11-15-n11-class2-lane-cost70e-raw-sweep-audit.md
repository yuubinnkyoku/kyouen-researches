# 2026-11-15：cost-70e raw sweep第三独立監査 — WIN7-D10 5 roots・D4重複0・証明書待ち・11×11はUNKNOWN

開始時main: `794f39c2`（本レーンのmerged 78a+69h第三独立検証追記直後）。並走がclaim `14970683`（head 1227/6620/522561/4890/386284基準・IN FLIGHT）で**第二coverable class-2 target S5 `00000000000000801202000000200000`（31行/2334）の最安未sweep cost-70 child `00000000000000801202000000200004`**（stones [2,21,49,57,60,71]・需要 c1=0,c2=2,c4=0・両開親がclass-2）をcost-70eとしてsweepし、raw batch 1–9（`26fd7d76`・sweep COMPLETE）・v16 determinism rerun（`9ef89e61`・batch5 node-exact）・v15 crosscheck（`f89ee535`・5 WIN + 3 REFUTED anchors）を出版済み。本レーンはこれら全11 rawファイルに対する**独立第三監査**（sweep実行とは別実装・別プロセス）を実施した。

## 監査手法

`audit_cost70e_raw_sweep_20261115.py`（Python標準ライブラリのみ・exact Bareiss整数行列式・浮動小数点なし・repo engine/solver/cache不使用）。geometry helpers（legal列挙・D4正準化）はmain出版済みのcost-70d監査スクリプトから流用（同一セッション系列）、raw-record parsing・集計再導出・batch-bit計画照合・WIN-root走査・一石削除再導出・CSV照合は70e用に新規実装。

## 監査結果（全assert合格・2回実行byte-identical）

- **独立legal再列挙70候補がclaim `legal_candidates` とbit-exact一致**、child 6石safe・stones [2,21,49,57,60,71]照合。
- **全batch bits 1–9がclaim engine `batch_bits` 計画と一致**・各bit 1回ずつ・pilot 3402×9（control行 nodes=3402 loss=false）。
- 集計再導出: **WIN7-D10 bits [0,8,24,66,79]**（nodes 4,596,984/1,333,433/2,197,162/1,763,979/1,765,453）・**REFUTED-D10 65件・capped 0件・総nodes 83,656,928**。全候補 terminalStoneRange [13,17]（深さ10境界内・distinct range 1種）。
- **determinism rerun（batch5 bits 64–75）node-exact一致**（verdicts/nodes/capped/terminal range・ms除く）。
- **v15交差エンジン一致**: 5 WIN bitsはすべてloss=true、REFUTEDアンカー bits 113/75/86はloss=false（nodes 13,605,564/6,262,124/6,426,703・pilots 5949×2）。
- **WIN 5 rootsのD4正準形は互いにdistinct**、かつ**公開win7証明書manifest 58ファイル・canonical roots 145個と重複0**（bit0 `00000000000000801202000000200005`・bit8 `00000000000000801202000000200104`・bit24 `00000000000000801202000001200004`・bit66 `00000000000000841202000000200004`・bit79 `00000000000080801202000000200004`・root mobility 60/63/56/49/52）→ **5 rootsはすべて新規fold材料候補**。
- **一石削除D4正準化6件を独立再導出**: del-2 = 第二coverable S5 `00000000000000801202000000200000` bit-exact（head 1227で31行/2334）・del-21 = class-2 S5 `00000000000000003800000008400000`（49行/3625）・del-49/57/60/71 はhead-1227 ranking CSV（175 open）に不在の閉行。parent2行は4つの第二開親候補中最少残行数（claim motivationの選定理由と整合）。
- head-1227 top-candidates CSVのchild行 demand `c1=0,c2=2,c4=0`・edge cost 70照合。
- 監査JSON `class2-lane-cost70e-sweep-audit-20261115.json`（2回実行byte-identical・md5 `a75a4dcc306b3a9fa17224fe1265cb05`）。

## 解釈上の注意

**証明書待ち**: 5 WIN rootsはfold材料候補だが、foldには blind抽出・独立検証済みWIN7証明書のmanifest出版が先決（78a/69hと同じ手順）。証明書が出版されるまで**head 1227/6620/522561/4890/386284 不変**。REFUTED-D10 65件はLOSS証明ではなく、child S6行は両開親の未解決行のまま。解消計数はmanifest被覆の前進であり、盤全体の勝敗ではない。標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class1・class2・class4は引き続き **UNKNOWN**。

## 並走状況（着手時点）

cost-65l receipts foldがIN FLIGHT（`6c6583d9`・bits 21/48・head 1227基準）。70eのchild行は65l foldと独立（65lのparentsは本childのparent1とclass-4 S5）。65l foldが先に着地した場合は70e証明書foldはその時点のcanonical headへのrebase必須。70e fold実行者は証明書manifest出版後に、claim `coordination_note` の衝突プロトコル（cost-72b/cost-76a/cost-63f precedent）に従うこと。

## 成果物

- sweep audit: [class2-lane-cost70e-sweep-audit-20261115.json](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost70e-sweep-audit-20261115.json)（再現: [audit_cost70e_raw_sweep_20261115.py](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_cost70e_raw_sweep_20261115.py)）
- source claim: [class2-lane-cost70e-inflight-20261115.json](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost70e-inflight-20261115.json)
- raw batches 1–9・determinism rerun・v15 crosscheck: 同output/ `class2-lane-cost70e-raw-batch{1..9}-20261115.jsonl` ほか（並走 commits `6e00fd29`…`26fd7d76`・`9ef89e61`・`f89ee535`）
