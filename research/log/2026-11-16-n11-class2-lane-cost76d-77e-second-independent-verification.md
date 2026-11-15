# 2026-11-16：cost-76d・cost-77e 並走sweep成果の第二独立検証 — 4 WIN7-D10証明書（bits 19/49/37/69）をpublished files限定で再検証、sweep totals・claim baseline・legal candidates全再現・VERIFICATION PASSED

開始時main: `2d00e01b`（K0832 z=1残余証明群）。対象は、並走レーンが21:25〜21:49に着地させた**第二coverable class-2 candidate S5 `00000000000000801202000040000000` の残2行のsweep成果** — cost-76d（2番目のcost-76行・child `00000000040000003800080008000000`・76候補・sweep完了+証明書公開・claim status=completed）と cost-77e（cost-77行・child `00000000040000809002000000004000`・77候補・sweep完了+証明書公開・claim上はin-flightのまま）。両fold onto canonical head 1405は本log時点で未着地。本レーンはfold（並走のin-flight作業）に着手せず、**出版済み成果の第二独立検証**を実施した。

## 検証内容（`scripts/verify_cost76d_77e_second_independent_20261116.py`・純stdlib+published verifier再実行・出力 `output/class2-lane-cost76d-77e-second-independent-verification-20261116.json`・2回実行byte-identical md5 `65ed4ad5…`・全チェックPASS）

### claim baseline（v12監査で確立したstale-baseline検査の適用）
- 76d・77e両claimとも `chain_head_at_claim` がreconciled canonical head **1405/6443/509457/4713/373180**（blob `b3ad19d7…`・commit `ca0e8c42`）を直接pin。**stale-baseline quoteなし**（67d/70gで見つかった旧型の異常は今回の両claimには存在しないことを機械確認）。

### 77e証明書（bits 37/69）の再構成と再検証
- parts 4本を連結したwhole証明書がreceipt（`bit37/bit69.cert-receipt.json`）のpart git blob sha 2本ずつ・whole bytes/md5/sha256全件と一致（bit37: 1,695,679B md5 `5bf6a67f…`・bit69: 1,964,949B md5 `1e738110…`）。consumed winner-state list 4本も連結してlines/distinct全一致（bit37: 64,971/47,018・bit69: 71,945/54,491）。**part境界は行途中で切れており、per-part splitlinesは過大計上する**（bytes連結→splitlinesが正しい。検証script実装中に発見・修正）。
- published BigInt独立検証器（`verify_win7_certificate_bigint_independent.mjs`）を両証明書に再実行し、**出力recordがpublished `bit37/bit69.bigint.json` とrecord完全一致**（57/57 sub-roots・strategy rows 47,018/54,491・union 0/0・terminal [13,17]・winner_states 64,971/71,945等全項目）。

### 76d証明書（bits 19/49）のpin照合と再検証
- manifest `class2-lane-cost76d-win7-certificates-20261116.json` の自己pin全照合: sweep audit blob `a57af016…`・両cert {bytes 1,618,698/1,215,488・md5・sha256・git blob sha}・両bareiss-verify blob全一致。
- BigInt検証器を両証明書に再実行: verdict/root/stones/safety・root mobility 55/54（manifest root_check loserMobilityと一致）・strategy rows 44,810/33,648・sub-roots 55/54・union 0/0・terminal [13,17]・terminal count 15,404/11,853全一致。**manifest totals（rows 78,458/sub_roots 109/winner_states 109,726/loser_states 32,979/terminal_count 27,257）を再実行から再合成して完全再現**。

### sweep receiptsからの独立再導出（両sweep・raw batch 10本ずつ）
- 76d: 76候補・bits==claimのlegal list==swept set・WIN bits [19,49]・REFUTED 74・capped 0・node_sum 96,246,915・terminal [13,17]・andclose全・pilot_d6 10本（nodes 3402・loss=false uncapped）— published sweep auditと全一致。
- 77e: 77候補・WIN bits [37,69]（nodes 1,819,936/2,623,346）・REFUTED 75・capped 0・total_nodes 116,019,458・win_node_sum 4,443,282・refuted_node_sum 111,576,176・heaviest bits [33:11,599,283/110/68/44/31]・terminal [13,17]・andclose全・pilot 10本 — published sweep JSONのaggregateと全一致。
- 77e determinism rerun: batch 4/6（WIN bitsを含むbatch）がoriginalsとnode-exact（verdict/nodes/capped/terminalRange同一）。v15 cross-engine: 両sweepとも pilot 5949・WIN bits全てloss=true（77eはrefuted anchor bit 0 loss=false 11,578,726 nodes も一致）・verdicts 3/3一致を再確認。
- legal_candidates.py（exact Bareiss 4x4）による候補再列挙: 76d 76候補・77e 77候補、**claimのlegal_candidates配列とbit-exact一致・swept setと一致**（候補の過不足なし）。

## 意義

1. 並走レーンの4枚のWIN7-D10証明書（bits 19/49/37/69）が**第三の環境でpublished filesのみから再検証可能**であることを確定（並走はBigInt+Bareissの二重独立検証済み、本検証がその再現）。以後の76d/77e foldとv13監査はこのrecordをpinできる。
2. 両claimが1405 baselineを正しく引用していることを機械確認 — fold着地時のfork（67d/70g型のnon-nested fork）が発生しない見通しを裏付け。
3. 第二候補S5 6行/439のうち5行までsweep完了・証明書公開済み（64a/71d STERILE・76d/77e本検証済み）。**残る未完了は75e（artifacts未公開・4 WIN7-D10 bits 6/10/11/37はメモ扱い）と76c（in-flight）と両foldのみ**。
4. 検証過程の副産物: 77e consumed listのpart分割は行途中で切れているため、**再構成時はbytes連結→splitlinesでなければlines/distinctが1件過大になる**（receiptの値が正しい。検証scriptに反映済み・今後のparts再構成の注意点）。

## 解釈境界（重要）

- WIN7-D10証明書は各7石rootから深さ10以内の先手勝ちのみを証明する。REFUTED-D10はLOSS証明ではない。STERILE行は閉鎖不能の表明でLOSS証明ではない。
- solved 1405はmanifest被覆の簿記であり、76d/77e fold着地まではchain bookkeepingも不変。
- **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class1・class2・class4は引き続きUNKNOWN**。

## 今後

- 76d/77e fold onto 1405は並走レーンのin-flight作業（着手禁止）。着地検知→v13監査拡張（両実装+agreement v10・76d/77e fold endpoint・本verification recordをpin）。
- 75e: raw artifacts公開待ち。公開されたら同様の第二独立検証→1405 re-base fold評価。
- 76c: in-flight・着手禁止。
