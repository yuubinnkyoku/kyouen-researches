---
id: K0425
title: 4行8点円の非局所型は単調で隣接弦長差が10以上
kind: proposition
status: proved
topics: [geometry, rectangles, variants]
aliases: []
relations:
- type: depends_on
  target: K0073
  note: 共通二根和と弦長平方の二階差分を使用
- type: depends_on
  target: K0317
  note: Pell族の初項が下界10と最初の非局所幅73を達成
artifacts:
- path: research/experiments/fixed-width/reports/q48-chord-gap-rigidity-20261015.md
  role: proof
  note: 無界の間隔定理と74列初出の短い算術証明
- path: research/experiments/fixed-width/scripts/q48_chord_gap_verify_20261015.py
  role: verifier
  note: 小間隔候補・幅73候補の全約数検査、独立平方根列挙
- path: research/experiments/fixed-width/scripts/q48_chord_gap_independent_20261015.cpp
  role: verifier
  note: 中央二弦長からの別方式の整数完全列挙
- path: research/experiments/fixed-width/output/q48_chord_gap_audit_20261015.txt
  role: data
  note: Python検証結果
- path: research/experiments/fixed-width/output/q48_chord_gap_independent_20261015.txt
  role: data
  note: C++独立検証結果
scope: 標準整数格子の四連続行を各2点ずつ通る全8点円、全盤長
---

## 命題・範囲

4連続整数行の各行で2個ずつ相異なる格子点を通る円の水平弦長列は、局所型 `(1,3,3,1)` か、隣接差が全て絶対値10以上の厳密単調列である。下界10は鋭い。非局所型の8点の横座標は全て異なり、任意の連続4列には高々2点しか含まれない。

さらに、水平全幅73以下の非局所型は `(35,51,63,73)` とその上下反転だけである。したがって最初の非局所8点円は4×74に現れる。この初出結果は既知だが、今回の証明は従来の大きな弦長対列挙を使わない独立した約数・判別式の有限排除である。

## 現在の根拠と限界

無界の単調性と差10下界は、弦長平方の二階差分 -8、奇数平方、半差 `(a,b,c)` の連立整数式から全称的に証明。`c<=4` は4候補の判別式で排除する。最初の幅73の完全分類は `c<=11` の約数候補6件からの厳密排除。Pythonの `d_0,d_1<=3000` 完全列挙と、中央2弦長から逆算する独立C++有限列挙が一致する。**有限検算を無界命題の証明と混同しない**。K0077のゲーム安定化長は変更しない。
