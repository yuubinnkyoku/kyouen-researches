---
id: K0432
title: 非局所4行8点円の傾きは有限判定でき、各円型は任意法で無限延長する
kind: proposition
status: proved
topics: [geometry, rectangles, variants]
aliases: []
relations:
- type: supports
  target: K0317
  note: Pell正規形から実現可能傾きと固定傾きの円型数を細分する
artifacts:
- path: research/experiments/fixed-width/reports/q48-slope-reduction-congruence-20261015.md
  role: proof
  note: 厳密傾き下界、有限必要十分判定、合同保存と固定傾き漸近
- path: research/experiments/fixed-width/scripts/q48_slope_reduction_congruence_20261015.py
  role: verifier
  note: 有限逆変換・複数法の合同保存を監査
- path: research/experiments/fixed-width/scripts/q48_slope_scan_20261015.cpp
  role: verifier
  note: 指定された有限範囲の既約傾きを列挙
- path: research/experiments/fixed-width/reports/q48-fundamental-unit-parity-reduction-20261015.md
  role: proof
  note: Pell基本単元だけで偶奇を保ち有限帰着上界を改善
- path: research/experiments/fixed-width/scripts/q48_fundamental_unit_audit_20261015.py
  role: verifier
  note: 基本単元の偶奇保存と既知型への適用を監査
- path: research/experiments/fixed-width/output/q48_fundamental_unit_audit_20261015.txt
  role: data
  note: 既知型と488ノルム解の監査結果
- path: research/experiments/fixed-width/output/q48_slope_reduction_congruence_20261015.txt
  role: data
  note: 法保存と逆変換の有限監査結果
scope: 標準4連続整数行の非局所8点円。傾きA/Bは既約正整数比であり、有限判定と漸近は傾きを固定した場合に限る。
evidence: 実現可能傾きは A/B>sqrt(9+6sqrt(2))。各傾きの存在は Pell基本単元U0,V0から得る 1≤L≤floor(sqrt(8Q)V0) の有限区間で必要十分に判定できる。基本単元変換は正規形ノルム8解の各成分の偶奇を保つ。実現する固定傾きごとの弦長型数は最大弦長Xに対して κ log(X)/log(λ)+O(1)。
---

さらに、非局所円が一つ存在すれば任意の法Nで全8点の正規化座標を保つ円が無限にある。Pell行列が有限環 `GL₂(Z/(2N)Z)` 内で有限位数を持つことから従う。法27第四型の整数円の実在は、この合同保存命題からは導かれない。

平方したPell単元を使う以前の有限帰着上界に比べ、基本単元だけを使うと探索上界を厳密に `2U0` 倍縮小できる。数学的有限性の主張であり、多項式時間や全傾きの有限リスト化を保証しない。有限範囲のC++走査で見つかった傾き `9/1,47/6,53/12` は、その走査範囲外に他の傾きがないことを意味しない。
