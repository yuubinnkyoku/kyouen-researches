---
id: K0451
title: 4行8点円の実現可能な既約傾き数R(H)はO(H²/(log H)²)以下
kind: proposition
status: proved
topics:
- geometry
- rectangles
- variants
- statistics
aliases: []
relations:
- type: depends_on
  target: K0432
  note: Pell正規形を用いる
artifacts:
- path: research/experiments/fixed-width/reports/q48-slope-dimension-two-sieve-20261016.md
  role: proof
  note: 大篩とTauber定理による全称証明・明示的主係数
- path: research/experiments/fixed-width/scripts/q48_sieve_dimension2_20261015.py
  role: verifier
  note: 有限剰余篩監査
- path: research/experiments/fixed-width/scripts/q48_sieve_constant_independent_20261016.py
  role: verifier
  note: 有理数による独立有限監査
- path: research/experiments/fixed-width/scripts/q48_sieve_interval_audit_20261016.py
  role: verifier
  note: 傾き下界で短縮した区間の大篩を独立検査
- path: research/experiments/fixed-width/output/q48_sieve_explicit_constant_20261016.json
  role: data
  note: 実行出力
- path: research/experiments/fixed-width/reports/q48-slope-dimension-two-sieve-20261015.md
  role: proof
  note: 四剰余類障害と一変数大篩による全称上界
- path: research/experiments/fixed-width/output/q48_sieve_dimension2_20261015.json
  role: data
  note: H=80,160,320,640の有限監査結果
- path: research/experiments/knowledge-audit-20261021/README.md
  role: log
  note: 証明の論理監査・再実行範囲・判定
evidence: '2026-10-21監査。大篩の除外剰余・平均補正・Karamata・Euler積定数・短縮区間のAbel和を確認。付属3監査を再実行。 監査記録: research/experiments/knowledge-audit-20261021/README.md。'
---


# 4行8点円の実現可能な既約傾き数は対数二乗の上界を持つ

非局所8点円の既約傾き A/B のうち 1<=A,B<=H の種類数 R(H) は
R(H)=O(H²/(log H)²)。さらに篩定数の明示的 Euler 積 E,F に対して
limsup R(H)(log H)²/H² <= 4π²F/(αE) が成立する（α=√(9+6√2)）。

証明は四つの排除剰余類に一変数大篩を適用し、非負係数 Dirichlet 級数の
Tauber 定理を用いる。有限監査は全称証明の代わりではない。

この命題は円型総数の上界ではなく、実現可能な傾きの種類数の上界である。

追加の同一命題資料: `K0426-four-row-q8-slope-log-squared-upper-bound.md`。詳細と独立証人・検算範囲は追加artifactを参照。原文は取込元ZIPに保存。
