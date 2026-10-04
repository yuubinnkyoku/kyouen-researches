---
id: K0334
title: 剰余放物線の等号問題はsigned NAE3/4と原点由来2/3節へ厳密に分解できる
kind: proposition
status: proved
topics: [geometry, maximum-safe, search-methods]
aliases: []
relations:
- type: depends_on
  target: K0097
  note: 等号集合が原点・一完全対・残り各対の一側を含む形であること
- type: depends_on
  target: K0333
  note: Q_pの線上限2・円上限4と円方程式の原始係数
artifacts:
- path: research/experiments/frontier-geometry-2026-10-05/proof.md
  role: proof
  note: 完全対補題・四元和・反射によるNAE分解の全称証明
- path: research/experiments/frontier-geometry-2026-10-05/verify_polynomial_curves.py
  role: verifier
  note: 既存pair-CNFと新しいNAE分解を全double候補で比較する
- path: research/experiments/frontier-geometry-2026-10-05/polynomial-curve-audit.json
  role: data
  note: 全13素数p≤43の禁止四点完全検査と分解の比較記録
scope: 全奇素数p、Q_p={(t,t² mod p):0≤t<p}、標準q=4、等号h+2点の存在問題。
evidence: 全称証明。有限検査は同値変換を既存SAT実装と比較する支持検査。
---

# 剰余放物線の完全対とNAE制約

Q_pには三共線点も五共円点もない。任意の禁止四点のパラメータ和は0 mod p。
四点を含む円の原始整数方程式をmod pへ移すと、可逆な最高次係数を持つ
A t⁴+(A+C)t²+Bt+Dになるため、t³係数と四根の和から従う。
従って三点に対する禁止第四点は高々一つ。

禁止四点が完全対{d,p−d}を含めば、他の二点も完全対である。
逆に二完全対は全て共円なので、この種の辺の総数はC(h,2)、h=(p−1)/2。
残る辺は完全対を一つも含まず、原点を含まなければ異なる四対、含めば異なる三対から一側ずつを取る。

等号集合では原点と一つの完全対dを固定し、他の各対の一側を真偽変数で選ぶ。
二完全対の辺は最初から避けられる。
原点を含まない残りの辺とその反射辺をまとめると、dを含めばsigned NAE3、含めなければsigned NAE4。
原点を含む辺はdを含めば二リテラル、含めなければ三リテラルの通常節となる。
この制約系があるdで充足可能であることとA(p)=(p+3)/2は同値。

これは全素数で制約系が充足可能という証明ではない。K0101は未解決のままである。
四元和=0も整数共円性の十分条件としては使わない。
