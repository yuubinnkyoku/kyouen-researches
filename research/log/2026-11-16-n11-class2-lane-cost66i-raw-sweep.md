# 2026-11-16：cost66i掃引 完了（66bit中9 WIN7-D10・57 REFUTED-D10、capped 0、競合0）

開始時の最新mainは `8719c6ea5922ac1a37b10786b0dba5a172c058f8`（直前の自commit `0dab7917` 出版直後に再取得）。head-1452 presweep census v2で選定した cost-66i child `00000000000000801226000000000000` の掃引を、claim v1（git blob `9eb3991abe1ee32d7296607990218a4958a571f0`）出版後に実行した。

## 実行

- engine v17（blob `c132cc64...`、fbt飽和修復済み）、depth 10、cap 1e9、andclose 1。9 batch（8bit×8＋2bit×1）で66 legal bits 全てをfresh実行（63 open + 3 confirmation bits）。pilot d6=3402が全9 batchでexact。
- 実行環境は nproc=2 のため計画の4並列ではなく実質1-2並列で実行した（node数は負荷非依存であり、決定再実行で同一性を確認）。
- 総nodes: 候補74,232,744 + pilot 9×3,402 = 74,263,362。terminalStoneRange は全bit [13,17]。

## verdicts

- **WIN7-D10 9 bits: [19, 28, 29, 58, 88, 90, 99, 103, 112]**（各root_canonはclaim v2のwinner_rootsに記録、全てpresweep時点でopen）
- REFUTED-D10 57 bits、capped 0。
- confirmation bits 23/100/109 は3/3とも期待どおりREFUTED-D10（v1 harvest転送2件 + cost-64h orbit転送1件の交差一致）。

## コントロール（全て合格）

1. **決定再実行**: 最重のbatch 3（WIN bits 28/29を含む）を再実行し、ms以外全フィールド完全一致（`class2-lane-cost66i-det-batch3-20261116.jsonl`）。
2. **v15交差エンジン検証**: 独立v15エンジン（blob `8744fc65...`、pilot 5949 exact）で9 WIN bits全てを再実行、9/9 loss=true 一致（`class2-lane-cost66i-v15-crosscheck-a/b-20261116.jsonl`）。
3. **独立監査**: `audit_cost66i_raw_batches_20261116.py`（stdlibのみ、全入力blob pin検証）。pilot厳密性、66bit被覆一意性、capped 0、D4 canon再計算66/66（v1 bit table・claim転送3/3と一致）、内部canon衝突0、そして **cross-source conflict scan**（cost-64h 64bit / cost-76c v17 76bitのverdict mapと66 root canonを突合）で矛盾0。bit 100のcanon `00000000000000c89002000000100000` はcost-64h bit 103のREFUTED-D10と同一canonで一致（衝突ではなく一致として記録）。
   - 監査スクリプトの初期ドラフトにはverdict mapのキー型不一致（int vs hex string）によりconflict scanが自明に空になる欠陥があったが、出版前に発見・修復し、修復後に再実行して本物の突合で0 conflictを確認した。出版された成果物にこの欠陥は含まれない。
- 出力: `class2-lane-cost66i-raw-audit-20261116.json`（2回実行でbyte-identical）。

## 出版物

- raw batch 1-9、det-batch3、v15-crosscheck a/b、audit JSON、audit script、claim v2（git blob `738443c0d1076115d723029edac2de3cb67c3e86`、schema `n11-class2-lane-cost66i-sweep-complete-20261116-v2`）。

## 未完了（次回以降）

- 9 WIN rootのcandidate-manifest marginals監査（どのopen manifest行を閉じるか）→ 証明書抽出優先順位。証明書抽出はまだ1件も行っていない。
- receipt foldは保留。cost-64h・cost-76cの両foldが先に着地する必要がある（着手禁止維持）。

## 解釈上の注意

WIN7-D10証明書は個々の7石rootのdepth-10内先手勝ちのみを証明し、REFUTED-D10はLOSS証明ではない。solved数はmanifest被覆の簿記であって勝敗ではない。**11x11空盤はUNKNOWNのまま**。二石root {49,60}・{59,60}、S2 {59,60}、class 1/2/4もすべてUNKNOWN。
