---
id: K0337
title: 奇数qの鏡映戦略の抽象十分条件と任意禁止族での最小q+1点反例
kind: proposition
status: proved
topics: [variants, grundy, residual-games]
aliases: []
relations:
- type: generalizes
  target: K0304
  note: 円・直線の鏡映定理を保証する抽象ブロック条件を明示する
artifacts:
- path: research/experiments/game-structure/reports/symmetry-scope-20261005.md
  role: proof
  note: 任意奇数qの最小反例と抽象ブロック十分条件の証明
- path: research/experiments/game-structure/scripts/symmetry_scope_20261005.py
  role: verifier
  note: 全安全集合のmex再帰と独立P/N再帰
- path: research/experiments/game-structure/output/symmetry_scope_20261005.json
  role: data
  note: q=3,5,7,9の有限照合
scope: 有限禁止ブロック配置ゲームと任意奇数q≥3
evidence: 数学的証明、有限例の独立再帰照合
---

# 奇数qの鏡映戦略の抽象十分条件と一般化の限界

固定点なし対合τが盤と禁止ブロック族を保ち、鏡像二点p,τ(p)を含む全ブロックがτ不変なら、
奇数q点禁止ゲームの任意の対称安全局面はPである。円・直線の真の鏡映はこの十分条件を満たす。
任意のq点禁止集合族へ、奇数qと対合不変性だけを使って拡張することはできない。

任意奇数q≥3に対し、V={0,…,q}、τ(i)=i xor 1、禁止辺V\{2},V\{3}という二辺族は
ルールを保つ固定点なし対合を持つが、対称安全局面S=V\{0,1}はg(S)=1となる。
0と1のどちらか一つだけが追加でき、一点追加後は終端だからである。空盤もg=1。
q+1頂点は、この種の奇数q点禁止反例を持つ最小頂点数である。

一般反証と十分条件は全称の数学的証明。q=3,5,7,9の全状態の二方式照合は独立確認である。
K0304の元の円・直線の幾何定理を反証する結果ではない。
