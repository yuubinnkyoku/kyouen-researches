# 2026-11-15：cost-74g sweep・WIN7証明書10件・receipt fold — head 1249→1258（第3 target S5が残り1行に）

開始時main: `a8354d68`（cost-72c fold後のhead 1244/6603/521339/4873/385062）。第三coverable class-2 target S5 `00000000000000809102000000000000` のcost-74 child `00000000000000809142000000000000`（stones [49,54,56,60,63,71]・需要 c1=0,c2=2,c4=0）をcost-74gとしてsweepした。既存のcost-74e claim（head 1188・planのみ・raw/証明書/foldなし）は実行上staleとして扱い、名前衝突を避けて74gとした（claimのcoordination_noteに明記）。fold実行中に並走cost-73g fold（1244→1249）が着地したため、本foldは**head 1249にrebase**した。

## sweep（v16 d10・cap 1e9・andclose 1・10バッチ・pilot 3402×10全PASS）

**74/74候補・WIN7-D10 10件（bits 4,11,20,44,69,95,100,108,109,116）・64 REFUTED-D10・0 capped・総nodes 179,966,455**。全候補 terminal [13,17]。batch-5 determinism rerun node-exact、v15交差エンジンで10 WIN loss=true（sum 159,009,591）・REFUTEDアンカーbits 0/1/2 loss=false・pilot 5949。

## 証明書10件（blind抽出・二重独立検証PASS）

| bit | mobility | rows | extraction nodes |
|---|---:|---:|---:|
| 4 | 65 | 99,948 | 63,769,232 |
| 11 | 58 | 56,032 | 17,678,255 |
| 20 | 59 | 52,615 | 19,828,636 |
| 44 | 58 | 42,594 | 10,783,636 |
| 69 | 62 | 64,865 | 22,399,084 |
| 95 | 61 | 80,597 | 37,604,127 |
| 100 | 60 | 67,934 | 19,856,779 |
| 108 | 59 | 57,582 | 13,893,370 |
| 109 | 57 | 60,340 | 18,376,728 |
| 116 | 61 | 56,682 | 17,197,650 |

全move `ok:true`・`fbt_drops:0`・terminal [13,17]。合計**639,189行・23,085,545 bytes・241,387,497 extraction nodes・600 sub-roots**。bit44のみ単一ファイル、他9件は行境界2分割。**BigInt 3x3 + Number Bareiss 4x4**の二独立検証器で**10/10 PASS**（union missing/extra 0/0・consumed union == 証明書行集合 0/0）。

## receipt fold（head 1249 → 1258）

`recompute_frontier_cost74g_receipts_20261115.py` はcost-73g fold scriptをrunpyで再実行してhead 1249/6598/520956/4868/384679をbyte-identicalに再現し、公開順 [4,11,20,44,69,95,100,108,109,116] で10 receiptをfoldした。

- 新canonical head: **`1258/6589/520286/4859/384009`**（solved 1249→1258、in-manifest marginal 9、raw marginal 49、zero-mim bits 11/20）。
- child `00000000000000809142000000000000` は**bit4**で閉鎖。
- **第三target S5: 2行/143 → 1行/69**（残るはcost-69 row `00000000000000809102000000002000` のみ）。
- 第2開親 `00000000000000003800000008000010`: **65行/4885 → 56行/4215**（child+8親orbit喪失）。
- set等式 `s_after == s_1249 ∪ covers(10 roots)`、520 folded rootsとのraw/D4 disjointness、sweep再導出、証明書bytes検証をassert。
- 出力: head JSON（blob `307e7ad8f45b9a11e73653c0314aae18634f50c6`・12,592 B）、ranking CSV（`062dcb6068a2bc98784da1f50be8f2f645b9c0d0`・7,579 B）、top-candidates CSV（`1eac1ca1f121bc8930b26030fc6b9e774f74fffc`・4,748 B）。claimはcompletedへretireし、fold記録・出力blob・再現コマンドを記載。completed claim後の再実行で3出力のbyte-identityとfold数値を再assertする制御付き。

## 信頼境界

- foldは公開済みreceiptの帳簿更新であり、いかなる局面の勝敗判定でもない。solved数はmanifest被覆のみを測る。
- WIN7証明書は各7石rootから深さ10以内の先手勝ちのみを証明する。REFUTED-D10はLOSS証明ではない。
- child orbitの閉鎖は両S5親の残り行からchildを除くが、どちらのS5も未解決のまま。**第三target S5は残り1行（cost-69）**で、これがWIN7 receiptで閉じれば第三target S5が先手WINとなりclass-2 blockerが条件付きで閉鎖される。
- 証明書木そのものの再走査は本foldの範囲外。公開receiptの二重独立検証に依拠し、foldはjoined LF bytes・root同定・sub-roots・終端範囲・親orbit・D4正準性を再検証した。

## 並走・次の一手

- cost-70g（8 WIN7証明書・fold待ち）は新head 1258へのrebaseが必須。70f bit84と70g bit29のD4重複に注意。
- cost-73g（fold済み・head 1249）と本74g fold（head 1258）の順序でcanonical chainが進んだ。
- **cost-69 row `00000000000000809102000000002000` のsweepが第三target S5閉鎖への最後の一手**（staleなcost-69g claimはhead 1163でartifactsなし）。

## 勝敗

標準11×11空盤、二石root `{49,60}`・`{59,60}`、S2 `{59,60}`、class1・class2・class4はすべて **UNKNOWN**。今回のfoldは勝敗判定を変更しない。

## 再現

```sh
python research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_cost74g_receipts_20261115.py
```

cost-73g baselineを再実行し、head 1249のbyte-identical再現から全制約を再検証した上でfoldする。実行時間は約1〜2分。
