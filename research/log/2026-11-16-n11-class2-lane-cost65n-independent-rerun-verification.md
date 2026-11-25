# 2026-11-16：cost-65n sweep独立再実行検証 59/59 node-exact・WIN bits 90/117独立再現 — 2 WIN rootsのfold投影を**並走fold receipt着地前に事前登録**（投影head 1444/174/6404/506746/4677/370660・mim 1+2・3親delta）

開始時main: `a7ac1757`（本レーンのfold投影ツール出版）。対象は並走レーンが08:18-08:20Zに出版した**cost-65n sweep raw batches 1-8**（child `00000000000000801202010000800000`・claim v1 `7dcd9767`・batches 1-4 `60c97b93`・batches 5-8 `e728c47e`）: **2 WIN7-D10（bits 90, 117）+ 57 REFUTED-D10・0 capped・総nodes 92,530,349・sweep complete NOT-STERILE**。本レーンは並走のsweep開始前にclaim v1の構造検証（21/21 PASS・`9888e42c`）を出版済み。本検証は並走と完全に独立な同一runner再実行による全bit照合であり、**fold receipt（並走が証明書抽出後に出版予定）の内容は一切読まない**。

## 検証内容

### 独立並行sweep再実行（出力 `output/class2-lane-cost65n-independent-rerun-verification-20261116.json`・git blob `304e1331`・独立raw 8ファイル併せ出版）
- **repo-verbatim runner v16**（`class4_child1_runner_v16.ts`・Node 22・`--andclose 1`・depth 10・cap 10⁷・engine状態はバッチごと完全リセット）で59 open bitsを8バッチ構成（claim v1のplanned_batch_bit_listsと同一）で独立sweep。
- **59/59 bitがbit/loss/nodes/capped/terminalStoneRange/andclose全項目でnode-exact完全一致**（過不足・不一致0件）。総nodes 92,530,349（並走のbatches 1-4 46,251,266 + 5-8 46,279,083と同一）。pilot_d6 8/8 = 3402 nodes・loss=false全一致。
- **WIN7-D10 bits 90（1,562,274 nodes）と117（388,910 nodes）が第三者環境で再現** — loss=true・capped=false。REFUTED 57・capped 0。
- 本レーンの独立raw 8ファイル（`class2-lane-cost65n-independent-rerun-batch{1..8}-20261116.jsonl`）を併せて出版し、第三者が並走raw batchとのdiffを直接検証可能。

### cost-65n fold投影の事前登録（出力 `output/class2-lane-cost65n-fold-preregistration-20261116.json`・git blob `da2b2292`）
- **出版済みfold投影ツール**（`fold_projection_head1441_tool_20261116.py`・commit `a7ac1757`・bit-89でagreement recordとbit-exact検証済み）を、独立再構成したbasis head **1441**（761 receipt roots + bit-89 + winners 498・6数値assert済み）で実行し、2 WIN roots `00000000040000801202010000800000`（child|1<<90）と `00200000000000801202010000800000`（child|1<<117）をfold。
- **事前登録値**:
  - root90: marginal 5・mim 1（child `00000000000000801202010000800000`〔manifest cost 65・classes 2〕のみ閉鎖）・D4 canon `00000000000100003800000048002000`
  - root117: marginal 6・mim 2（`00000000000020003800000008080000`〔manifest cost 69・classes 2〕と `00000000000100809002000000000008`〔manifest cost 65・classes 2〕）・D4 canon `00000000001020003800000008080000`
  - **投影head 1441→1444/174/6404/506746/4677/370660**
  - demand histogram delta: `c2=2,c4=0` −3 のみ（閉鎖3行すべて同バケット）
  - 3 affected parents: SH親 `00000000000000003800000008002000` 29→27/2017→1883（child+`00000000000020003800000008080000`の2行・134 = 65+69）・`00000000000000801202000000000080`（class-2・55 rows）55→53/4137→4003（2行・134）・第2親 `00000000000000801202010000000000` 48→46/3498→3368（2行・130）— 計6 parent-row incidences（3親×2行: childはSH親+第2親の2親・row2はSH親+`00000000000801202000000000080`の2親・row3は`00000000000801202000000000080`+第2親の2親）・edge cost delta 398
  - 両WIN rootのD4 orbitはfold済み762軌道（747 canons）とdisjoint（ツールの衝突assert内蔵）
- **本事前登録は並走fold receiptの公開前にmainへ出版する**（証明書抽出が並走の次工程のため）。着地時に並走receiptの全対応フィールドと照合する。

## 意義

1. cost-65n行の全確定（59/59: WIN7-D10 bits 90/117 + REFUTED 57）が**並走と独立の第三者環境でnode-exactに再現可能**であることを確定。以後の65n fold着地と監査は本verification record（blob `304e1331`）をpinできる。
2. **fold投影がreceipt公開前に事前登録された** — 並走fold receipt着地時に、投影head 1444/174/6404/506746/4677/370660・mim 1+2・3親delta・hist deltaが一致するはず。不一致の場合は実験事実として記録する。
3. bit-89（mim 3・5親）と異なり、65nは**同一childの2 WIN roots**で閉鎖3行・3親という構造。1 rootあたりのmimが小さく閉鎖がchild中心であることは、class-2 laneの最安行の典型構造として記録に値する。

## 解釈境界（重要）

- WIN7-D10証明書はroot `00000000040000801202010000800000` と `00200000000000801202010000800000` から深さ10以内の先手勝ちのみを証明する（証明書抽出は並走が実施中・本レーンは抽出しない）。REFUTED-D10はLOSS証明ではない。NOT-STERILEは勝敗決着ではない。
- solved 1441（→事前登録後1444は投影に過ぎない）はmanifest被覆の簿記。
- **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class1/class2/class4は引き続きUNKNOWN**。

## 今後

- 並走のcost-65n証明書・fold receipt着地時: (1) 証明書の盲抽出・byte-identical照合（bit-89と同じ手順）、(2) fold receiptとの本事前登録（blob `da2b2292`）の全フィールド照合、を実施する。
- 次target（cost-66帯 `00000000000000801226000000000000` 等のcensus v4 ranking）は並走依存。本レーンは新規claimを作らない。
