---
id: K0448
title: 4行8点円には相異なる実現可能な既約傾きが無限種類ある
kind: proposition
status: needs-review
topics:
- geometry
- rectangles
- variants
aliases: []
relations:
- type: depends_on
  target: K0432
  note: 傾きの定義と整数弦長からの円の復元を用いる
artifacts:
- path: research/experiments/fixed-width/reports/q48-infinite-distinct-slopes-20261016.md
  role: proof
  note: Pell型二次形式の自己同型による相異なる傾きの無限構成と任意法の合同保存
- path: research/experiments/fixed-width/scripts/q48_infinite_distinct_slopes_20261016.py
  role: verifier
  note: 5世代の整数検算、350個の独立4点行列式、8種類の法の帰還周期
- path: research/experiments/fixed-width/output/q48_infinite_distinct_slopes_audit_20261016.txt
  role: data
  note: 独立検証器の実行結果
scope: 標準4連続整数行の非局所8点円。異なる既約傾きの無限性および任意固定法での無限同余部分列。
evidence: 2026-10-20添付統合。元資料では proved または computed と報告（個別の元statusは保存ZIPを参照）。本項目の全量化範囲に対する証明・計算の再監査は未完了。有限検証の実行範囲は統合実験のVALIDATION.mdを参照。
---


> 統合監査: 以下は取込元の主張・報告。全称証明・完全列挙の監査が未完了のため、現在の採用状態は needs-review。本文中の「証明」「一致」は元資料での報告を表す。


標準4連続整数行に各2点を持つ非局所8点円の既約傾きは無限種類ある。明示的な傾き列は9から厳密に減少し、3√(325/37)に収束する。各傾きは実際の整数8点円を持つ。さらに任意の法Nで分子9・分母1と合同な実現傾きが無限種類存在し、対応する円の全8点の正規化座標も最初の円と法Nで一致する。

これはK0431・K0432の固定傾き内のPell延長とは異なり、傾きの種類そのものが無限であるという全称結果。最小の次傾きや傾き計数関数の真の漸近は未解決。有限検算は無限性の証明とは区別する。
