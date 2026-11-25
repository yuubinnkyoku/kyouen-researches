---
id: K0813
title: "幅2..5の円格子点数P(w)完全決定（4,6,8,8）・系としてw=5・q≥9の行分離 M_{5,q}=q−1"
kind: proposition
status: proved
topics: [rectangles, geometry, variants]
aliases: []
scope: "標準整数格子の固定幅w×m盤（w=2..5・全m≥1）について、盤内1円の格子点数の最大はP(2)=4・P(3)=6・P(4)=8（4×4盤で等号）・P(5)=8（いずれも等号達成）。系: q≥9の全(w=5,q)で行分離M_{5,q}=q−1・g(S)=(5·min(m,q−1)−|S|) mod2（全m≥1・全安全局面）"
evidence: "数学的証明（上界: 円と水平線の交点≤2によるP(w)≤2w〔w=2,3,4〕+単調性P(5)≤P(6)=8〔K0763〕。下界: witness円(2x−3)²+(2y−3)²=10が行0..3に各行2点・4×4盤に収まる）。独立な第2導出: K0767系の対偶と確定済みM_{2,4}=9・M_{3,6}=9・M_{4,8}=11・M_{5,8}=16からP(w)≥4,6,8,8。有限検証（行別点数・全点の整数方程式確認・x∈[−20,20]全円列挙で窓内最大4/6/8/8一致）は補強"
solution:
  board: 幅w=2..5固定長m可変の標準整数格子
  level: strong
  outcome: conditional
  classification: [all-safe-grundy]
  coverage: P(w)はw=2..5で全称決定・系は(w=5,q≥9)で全m≥1・全安全局面
  conditions: 連続整数行・円はa≠0の真円（直線は含めない）・系はq>P(5)=8かつq>5
  verification: [mathematical-proof, independent-enumeration]
  certificate: witness円(2x−3)²+(2y−3)²=10（整係数形x²+y²−3x−3y+2=0・行0..3各2点）とP(5)別witness円(2x−7)²+(2y−7)²=50
  independent_check: 対偶導出（K0069/K0070/K0077/K0331の確定M値とK0767系）がwitness下界と完全一致・全円列挙スクリプトで窓内最大一致
  note: "P(w)表はw=2..82で連続に。P(17)=P(18)=16はK0778で全称確定。"
relations:
- type: depends_on
  target: K0763
  note: P(6)=8（単調性によるP(5)≤8）とwitness円(2x−7)²+(2y−7)²=50の原形
- type: depends_on
  target: K0767
  note: 系「q>P(w)かつq>wなら行分離M_{w,q}=q−1」へのP(5)=8の代入と対偶
- type: depends_on
  target: K0778
  note: P(17)=P(18)=16の全称確定（K0767に残る旧open範囲を解消）
- type: depends_on
  target: K0331
  note: M_{5,8}=16の確定値（対偶によるP(5)≥8の第2導出）
- type: depends_on
  target: K0069
  note: M_{2,4}=9の確定値（対偶によるP(2)≥4の第2導出・K0796と併用）
- type: depends_on
  target: K0070
  note: M_{3,6}=9（対偶によるP(3)≥6の第2導出）
- type: depends_on
  target: K0077
  note: M_{4,8}=11（対偶によるP(4)≥8の第2導出）
- type: generalizes
  target: K0025
  note: 行分離公式の新規(w,q)領域（w=5・q=9,10。q≥11はK0025のq>2w帯と一致）
- type: supports
  target: K0332
  note: w=5の低q側帯の上界会計にP(5)=8を供給
artifacts:
- path: research/experiments/width2-5-circle-point-max-20261114/report.md
  role: proof
  note: 定理・系・証明・witness・検証の記録
- path: research/experiments/width2-5-circle-point-max-20261114/scripts/width2_5_circle_point_max.js
  role: verifier
  note: witness行別点数の整数検証・50円の再確認・全円列挙による補強
- path: research/experiments/width2-5-circle-point-max-20261114/output/width2_5_circle_point_max.json
  role: data
  note: 全数値の機械出力
- path: research/log/2026-11-14-width2-5-circle-point-max.md
  role: log
  note: 判断・経緯・レジューム
---

## 命題（証明済み・全称）

1. **P(w) 完全決定（w = 2..5・全 m ≥ 1）**:
   **P(2) = 4、P(3) = 6、P(4) = 8、P(5) = 8**（いずれも等号達成）。
   K0763..65（P(6)=8, P(7)=10, P(8)=12）と K0767（P(9..16)）の下側の空白 w=2..5 を閉じ、
   P(w) 表は w=2..82 で連続になった。
2. **witness**: 円 **(2x−3)² + (2y−3)² = 10**（整係数形 x²+y²−3x−3y+2=0）は
   行 0..3 の各行にちょうど2点〔y=0: (1,0),(2,0)・y=1: (0,1),(3,1)・y=2: (0,2),(3,2)・
   y=3: (1,3),(2,3)〕を持ち、y=4 に点を持たない。8点はすべて 4×4 盤に収まる。
   行 0..w−1 の窓で 4, 6, 8, 8 点（w=2,3,4,5）。
   P(5) には別 witness 円 (2x−7)²+(2y−7)²=50（行 0..4 で 8点・K0763/K0764 witness と同一円）もある。
3. **系（行分離公式の新規領域）**: K0767 の系「q > P(w) かつ q > w ⟹ M_{w,q} = q−1」に
   P(5)=8 を代入すると **w=5・q ≥ 9 の全 (w,q) で M_{5,q} = q−1**、
   すなわち **M_{5,9} = 8・M_{5,10} = 9**（新規）、全 m ≥ 1・全安全局面 S で
   g(S) = (5·min(m,q−1) − |S|) mod 2。
   q ≥ 11 は従来の K0025（q > 2w）帯に含まれ、本系で w=5 の分離帯が q ≥ 9 に拡大。

## 証明の骨子

- **上界（w=2,3,4）**: 円と水平格子線 y=c の交点は x の2次方程式の解として高々2点。
  行が w 本なので P(w) ≤ 2w。
- **上界（w=5）**: 単調性 P(w) ≤ P(w+1)（幅 w の盤に k 点を持つ円は同じ m の幅 w+1 の盤にも
  同じ k 点を持つ）と K0763 の P(6)=8 から P(5) ≤ 8。
- **下界**: witness 円（上記2）が 4, 6, 8, 8 点を構成性地達成。
- **独立な第2導出（対偶）**: K0767系の対偶により、確定済みの
  M_{2,4}=9（K0069/K0796）・M_{3,6}=9（K0070）・M_{4,8}=11（K0077）・M_{5,8}=16（K0331）は
  それぞれ P(w) ≥ 4, 6, 8, 8 を強制する（もし P(w) ≤ q−2 かつ q > w なら
  M_{w,q}=q−1 ≠ 記録値となり矛盾）。witness による下界と完全一致。
- **有限検証（補強）**: witness の行別点数・全点の整数方程式充足を整数演算で確認。
  x∈[−20,20]・行 0..w−1 の3点組を通る全円（w=5 で 937,609 円）を列挙し、
  窓内点数の最大が 4/6/8/8 で理論値と一致。

## 限界・注意

- 上界の根拠は数学的論証（行境界・単調性）であり、全円列挙は x が有界な補強にすぎない。
- 直線（a=0）は P(w) の定義に含めない（行分離の文脈では別扱い）。
- P(17)=P(18)=16 は K0778 で全称確定。K0767 の当時の未解決記述は後続結果で解消済み。
- 系は q ≤ 8 の (5,6)/(5,7)/(5,8) には適用されず、これらの境界・確定値は不変。
