---
id: K0458
title: 四行8点円には新しい既約傾き181273/40152の無限Pell族がある
kind: proposition
status: proved
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
- path: research/experiments/knowledge-audit-20261021/README.md
  role: log
  note: 証明の論理監査・再実行範囲・判定
scope: 標準4連続整数行を各2点通る非局所8点円の既約傾き181273/40152
evidence: '2026-10-21監査。明示整数円・新傾き・Pellノルムと既存無限延長定理の条件を確認。独立行列式・ガウス積検査を再実行。 監査記録: research/experiments/knowledge-audit-20261021/README.md。'
---


非局所8点円の弦長列 `(5371183,43796547,61704339,75476575)` は整数円の必要十分条件を満たす。既約傾きは `181273/40152`、Pell正規形は `g=1,L=223,M=291,P=31247717425,Q=18350252593` で `QM²−PL²=8`。K0431の全称無限延長定理により、同じ既約傾きの相異なる整数8点円が無限に存在する。有限列挙が無限性の証明ではなく、明示証人と既存定理が根拠。全傾きの分類は未解決。
