---
id: K0346
title: 任意有限整数点盤では三共線なし・唯一最大配置でも故障耐性が無界
kind: proposition
status: proved
topics: [geometry, maximal-safe, maximum-safe, variants, grundy]
aliases: []
relations:
- type: depends_on
  target: K0328
  note: 元から空だった点の最小解除石数という故障耐性の定義を有限点盤へ使う
- type: depends_on
  target: K0339
  note: 終局サイズ差から多人数の策略非依存敗者を判定する帰結
artifacts:
- path: research/experiments/geometry-frontier-followup-20261005/proof.md
  role: proof
  note: 整数三次行列式・反転・全rの故障耐性と全Grundyの数学的証明
- path: research/experiments/geometry-frontier-followup-20261005/verify_cubic_fault_family.py
  role: verifier
  note: 共有幾何coreとgeneric Leibniz、全削除集合、非圧縮全safe mexで独立検査
- path: research/experiments/geometry-frontier-followup-20261005/audit.json
  role: data
  note: r≤8の整数証人・削除完全検査、r≤6全436848安全局面の完全mex検査
scope: 全r≥1、明示構成した3r+1個の整数点だけを盤にする標準q=4およびcircle-only。全格子正方形盤のK0328は含まない。
evidence: 全称数学的証明。有限検査は独立した支持監査。
---

# 円だけによる故障耐性の無界族

全整数r≥1について、3r+1点の整数盤B_rと安全極大3r石S_rを明示構成でき、
元の空点はp一つだけで、故障耐性ρ(S_r)=rとなる。
B_r全体に三共線はなく、禁止四点はpを共有するr本の円だけ。
各円の残る三石は互いに素なブロックC_iをなす。
標準circle-and-lineとcircle-onlyは同じゲーム。
r≥2ではS_rはこの有限点盤の唯一最大配置でもある。
従って任意有限整数点盤の一様故障耐性上界は存在しない。

構成の起点は、整数tの点(t,2t³)。四パラメータのVandermondeをV、
基本対称式をe_jとするとlifted determinantは
2V{1−4(e₁²e₂−e₂²−e₁e₃+e₄)}で零にならない。
三共線はパラメータ和0と同値。
100^i{1,10,−11}のr組を選ぶと、最大levelの絶対値比較により各組だけが三共線。
原点反転・分母払いで指定三点直線をpを通る4点円へ移す。
全円を壊すには各C_iから一石が必要十分なのでρ=r。

全極大配置はS_r一つと、pおよび各C_iの二石からなる3^r配置のみ。
最大は3r、最小極大は2r+1。
この有限点盤の通常プレイは全局面Grundy閉式も持つ。
p占有時はg=(2r−Σx_i) mod2、p不在で満杯ブロックがあればg=(3r−Σx_i) mod2。
p不在で満杯がなければa,b,cを占有0,1,2のブロック数として、
r奇数ではg=(3r−Σx_i) mod2、r偶数はc>0でg=2+(b mod2)、c=0でg=(a+1) mod2。
空盤g=1、全3r+1初手がg=0に移る。r偶数≥2の最大Grundyはちょうど3。
循環ℓ人で最初に着手不能となる一人を敗者にする規則なら、
全合法プレイで同じ敗者となる必要十分条件はℓ|(r−1)。

この結果は**B_rの選択点だけを盤とする**。
S_rを含む正方形全格子盤では他の空点の被覆を証明していないため極大ともρ=rとも言わない。
K0328の標準正方形盤の一様上界はOPENのまま。
一般に円・直線の局所幾何だけから定数故障耐性を導くことはできず、
正方形の全格子点を使う条件が必要になることを示す。
