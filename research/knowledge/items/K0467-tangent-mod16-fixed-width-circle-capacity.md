---
id: K0467
title: 接線行の法16制約による固定幅円点数の上界と5〜16行の厳密値
kind: proposition
status: proved
topics:
- geometry
- rectangles
- variants
- grundy
aliases: []
relations:
- type: depends_on
  target: K0072
  note: 連続整数行における二重点行数の全称上界を利用
artifacts:
- path: research/experiments/fixed-width/reports/tangent-mod16-circle-capacity-20261016.md
  role: proof
  note: 無界証明・法16有限補題・最大点数の証人
- path: research/experiments/fixed-width/scripts/tangent_mod16_separation_20261016.py
  role: verifier
  note: 法16の独立2実装と有限格子の三点円直接列挙
- path: research/experiments/fixed-width/output/tangent_mod16_separation_20261016.txt
  role: data
  note: 監査結果
- path: research/experiments/knowledge-audit-20261021/README.md
  role: log
  note: 証明の論理監査・再実行範囲・判定
solution:
  board: 標準整数格子 w×m・q点版
  level: strong
  outcome: conditional
  classification:
  - root
  - first-moves
  - all-safe-win-loss
  - all-safe-grundy
  coverage: 全m≥1・全安全局面
  conditions: w=5..16かつq>P(w)、またはw≥15かつ本文の合同別十分条件
  verification:
  - mathematical-proof
  - independent-enumeration
  certificate: K0072の二重点行数定理と接線行のmod16全剰余証明
  independent_check: 有限6盤の三点円列挙、法16の独立2方式
  note: g(S)=(w min(m,q−1)−|S|) mod2、M=q−1
evidence: '2026-10-21監査。二重点行上界達成時に限る縦係数整数性とmod16周期補題・容量帰着を確認。付属検査を再実行。 監査記録: research/experiments/knowledge-audit-20261021/README.md。'
---


# 接線行の法16制約による固定幅円点数の上界と5〜16行の厳密値

非退化円が標準整数格子の連続するw行に持てる整数点数の最大値 P(w) は、w=5..16 で順に

`8,8,10,12,12,12,14,16,16,16,16,16`

である。全称上界とそれを達成する具体的な円は証明資料に記録した。

さらに w≥15 では、w mod 8 が 0,1,5,7 のとき `P(w)≤2 ceil(w/2)`、それ以外では `P(w)≤2 ceil(w/2)+2`。これは全整数横幅についての全称定理であるが、後者の上界の達成可能性は主張しない。

q>P(w) が証明された範囲では q 点円と非水平 q 点直線がなく、全 m≥1 の安全局面 S で `g(S)=(w min(m,q−1)−|S|) mod 2`。真の満容量安定化長は `M_{w,q}=q−1`。特に 6×m・q=9 は M=8。

数学的根拠は K0072 の二重点行数上界、Vieta の整数性による単一点行=水平接線の補題、および法16の平方剰余必要条件の全剰余検査である。有限格子の直接円列挙は独立支持資料であって無界証明の代替ではない。
