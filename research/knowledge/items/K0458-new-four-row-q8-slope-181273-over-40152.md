---
id: K0458
title: 四行8点円には新しい既約傾き181273/40152の無限Pell族がある
kind: proposition
status: needs-review
topics:
- geometry
- rectangles
- variants
aliases: []
relations:
- type: depends_on
  target: K0431
  note: 任意の非局所8点円のPell無限延長定理
artifacts:
- path: research/experiments/fixed-width/reports/q48-gaussian-circle-census-100m-20261015.md
  role: proof
  note: 明示的な8格子点円・Pell正規形・整数恒等式
- path: research/experiments/fixed-width/scripts/q48_gaussian_census_independent_audit_20261015.py
  role: verifier
  note: 4点円行列式1050件と新傾きの整数監査
scope: 標準4連続整数行を各2点通る非局所8点円の既約傾き181273/40152
evidence: 2026-10-20添付統合。元資料では proved または computed と報告（個別の元statusは保存ZIPを参照）。本項目の全量化範囲に対する証明・計算の再監査は未完了。有限検証の実行範囲は統合実験のVALIDATION.mdを参照。
---


> 統合監査: 以下は取込元の主張・報告。全称証明・完全列挙の監査が未完了のため、現在の採用状態は needs-review。本文中の「証明」「一致」は元資料での報告を表す。


非局所8点円の弦長列 `(5371183,43796547,61704339,75476575)` は整数円の必要十分条件を満たす。既約傾きは `181273/40152`、Pell正規形は `g=1,L=223,M=291,P=31247717425,Q=18350252593` で `QM²−PL²=8`。K0431の全称無限延長定理により、同じ既約傾きの相異なる整数8点円が無限に存在する。有限列挙が無限性の証明ではなく、明示証人と既存定理が根拠。全傾きの分類は未解決。
