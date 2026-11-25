# 2026-11-15：cost-84a + cost-62a fold第二独立検証 — sweepを最初から再実行して公開raw batchとnode-exact一致・両foldを2回実行でbyte-identical再現

開始時main: `03eee4a6`（監査v8/agreement v5着地後）。並走laneがこの時間帯に**cost-84a sweep+fold着地**（head 1314→**1318**/6530/515822/4800/379545）と**cost-62a sweep+fold着地**（head 1318→**1326**/6522/515251/4792/378974・commit `f3abc8b3`）を相次いで実施した。本レーンは[83d fold第二独立検証](./2026-11-15-n11-class2-lane-cost83d-fold-second-verification.md)（`def2ddd1`）と[監査v8+agreement v5再現検証](./2026-11-15-n11-published-audit-v8-agreement-v5-reproduction.md)（`6d52031a`）の着地後、collision protocolに従い新2 endpointの第二独立検証に着手した。

## 発見した再現性ギャップと並走による同時修理（独立収束）

着手時点で `recompute_frontier_cost62a_receipts_20261116.py` は**新規cloneから実行不能**だった: 要求する `output/class2-lane-cost62a-raw-batch{1..8}-20261116.jsonl` がmainに一切存在せず（mainの `…-20261114.jsonl` は別child・pilot 5949・WIN 11件の別sweep）、`tmp-cost62a/`・`tmp-cost84a/` も未公開だった。本レーンがこの修理（batch再生成・repair script作成）を独立に進めている最中に、landing laneが同じ修理を着地させた: raw batch 8件（`a7244ae2`）・repair script 2本（62a: `f050254b`+`3c639ce3`・84a: `c3c5d785`+`94283c72`）。**landing laneの公開bytesを正**として以後の検証入力に使い、本レーンが独立に書いたrepair scriptはROOTS・検証器呼び出しロジックまで完全一致（docstringのみ相違）していたことを記録する。両導出が一致したことで、foldはpublished bytesのみで end-to-end 実行可能になった。

## 第二独立検証の内容

1. **62a sweep完全再実行**: pinned engine `class4_child1_runner_v16.ts`（blob `0a4a86f6`・node v22.20.0）をclaimのbatch layout（8 batch・62候補・depth 10・cap 1e9・andclose 1・per-batch d6 pilot）で**最初から全実行**（約2分）。再生成8 batchは**公開raw batchと全意味フィールドで行単位完全一致**（bit順・loss・nodes・capped・terminalStoneRange・andclose・pilot 3402×8・62候補・WIN7-D10 6件 [7,15,35,76,81,98]・REFUTED 56・capped 0・総nodes 46,968,169）。相違は壁時計`ms`のみ（どこでもassert対象外）。batch-5の8 bitは公開determinism rerunともnode-exact、v15 crosscheck（pilot 5949・6 WIN+3 REFUTED anchor）とも一致。
2. **公開repair scriptをそのまま実行**: `reconstruct_tmp_cost84a_20261116.py`・`reconstruct_tmp_cost62a_20261116.py` をtmp dir全削除後、main bytesから改変なく実行。84a 4/4・62a 6/6とも BigInt + TS-Bareiss 両検証器 **union 0/0 PASS**（fold内で再assert）。
3. **両foldを公開入力で各2回隔離実行**:

| 対象 | 統制 | 結果 |
| --- | --- | --- |
| cost-84a fold | runpy鎖（83d→83c→…→1227 baseline）再実行込み2回 | head **1318/6530/515822/4800/379545** 再現・head JSON（`f5624e99`・7,935B）+ ranking CSV（`41fe1225`）+ top-candidates CSV（`c00f7306`）が2回間・publishedともbyte-identical・証明書4件 208,335 rows / 7,518,339 bytes / 249 sub-roots・第二target S5 4行/293→3行/209 |
| cost-62a fold | 84a fold・全鎖を内包して2回 | head **1326/6522/515251/4792/378974** 再現・head JSON（`3989e9dd`・9,434B）+ ranking CSV（`f99c7561`）+ top-candidates CSV（`cec2b833`）が2回間・publishedともbyte-identical・marginal 32/8・zero-mim [35]・childはbit7で閉鎖・第二候補S5 39行/2708→34行/2368・第2開親 52行/3875→48行/3582 |

使用したpublished入力（84a/62a証明書6+6件・head JSON・CSV・claim・crosscheck・raw batch・repair script）はすべてfetch時に**git blob shaで照合**した。

機械可読記録: [class2-lane-cost84a-62a-fold-second-verification-20261115.json](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost84a-62a-fold-second-verification-20261115.json)（6,129 bytes）

## 意義

- 83dに続き**84a・62aも第二独立検証済み**となり、fold chainの全末端が「着地 + 独立再実行による検証」体制に揃った。84a/62a分はlanding sessionの状態を一切使わず、**sweep自体を別環境で最初から再実行して公開batchとnode-exact一致**を確認した点が、batchの再読取のみの検証より強い。
- repair scriptを2 laneが独立に導出して論理一致したことは、構成の自明性（「公開証明書→公開検証器でtmp再構成」以外の選択肢がない）の傍証ともなっている。

## 解釈境界（重要）

- foldは公開済みreceiptの帳簿更新であり、いかなる局面の勝敗判定でもない。solved 1326はmanifest被覆の計数。
- WIN7証明書は各7石rootから深さ10以内の先手勝ちのみを証明する。REFUTED-D10はLOSS証明ではない。
- 第二target S5 `00000000000000801202000000200000` は3行/209で、全残行がREFUTED-D10のためdepth-10 receiptでは閉鎖不能（より深い探索か別証明が必要）。
- **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class1・class2・class4は引き続きUNKNOWN**。

## 今後

- frontier baselineはhead **1326**。第二候補S5 `00000000000000801202000040000000` は残34行、第2開親 `00000000000000003800000008001000` は48行/3582、best class-4 blocker S5は18行/1460。
- 84a/62a endpointを含む**監査v9機械拡張**（双実装・agreement v6）の着手可否を最新mainで確認。fold chain末端の検証体制が揃ったため拡張条件は揃っている。
- 以後のfoldはhead 1326へのrebaseが必須。
