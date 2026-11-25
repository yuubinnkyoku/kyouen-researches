---
id: K0545
title: 四次元二値立方体の5点共超平面禁止版の強解決と二値超立方体の共面四点数
kind: proposition
status: proved
topics: [variants, geometry, grundy, maximal-safe, maximum-safe, statistics]
aliases: []
relations:
- type: depends_on
  target: K0544
  note: d石極大のアフィン階数判定
- type: depends_on
  target: K0305
  note: 全極大同偶奇のGrundy帰結
artifacts:
- path: research/experiments/coplanar-4cube-q5-20261024/proof.md
  role: proof
  note: 任意次元の共面四点数の全称証明と有限完全列挙の根拠
- path: research/experiments/coplanar-4cube-q5-20261024/verify.py
  role: verifier
  note: 直接整数行列式と全局面mex
- path: research/experiments/coplanar-4cube-q5-20261024/independent.cpp
  role: verifier
  note: Gram行列式による独立完全列挙
- path: research/experiments/coplanar-4cube-q5-20261024/rectangle_formula.py
  role: verifier
  note: d=2..6の3×3小行列式による独立検算
- path: research/experiments/coplanar-4cube-q5-20261024/results.md
  role: data
  note: 全局面・極大配置・Grundyの計数結果
scope: d≥2の二値超立方体の共面四点数、四次元二値立方体の5点共超平面禁止版の全安全局面
evidence: 共面四点の全称組合せ証明。四次元の全65536部分集合を独立した整数方式で完全列挙、全極大同偶奇から帰納的にGrundy式を証明
solution:
  board: 2×2×2×2・5点共超平面禁止
  level: strong
  outcome: second-player-win
  classification: [root, first-moves, all-safe-win-loss, all-safe-grundy]
  coverage: 全6613安全局面、通常・misère
  conditions: 四次元二値立方体・5点が同一アフィン超平面にあると禁止
  verification: [mathematical-proof, exhaustive-enumeration, independent-enumeration]
  certificate: 全5点組4368個・全65536部分集合の二方式完全列挙と偶奇帰納
  independent_check: Pythonの4×4直接行列式、C++のGram行列式・別方式安全判定で一致
  note: 通常版後手必勝、misère版先手必勝。全局面g(S)=|S| mod2、h(S)=1-g(S)
---

# 四次元二値立方体の強解決と共面四点の公式

四次元盤 V={0,1}^4 で、5点のアフィン次元が3以下なら禁止（退化を含む）。全6613安全局面で

    g(S)=|S| mod 2,  h(S)=1-g(S).

極大安全配置は4石100個または6石1088個だけ。K=6、s=4。空盤は通常版後手必勝、misère版先手必勝。全16初手後の値は(g,h)=(1,0)。

任意d≥2の二値超立方体の共面四点は、互いに素な非空座標集合を反転して得られる長方形に限られ、その個数は

    R_d=2^(d−3)(3^d−2^(d+1)+1).

この計数公式は全称証明。四次元の全局面分類は有限完全列挙に依存し、他次元の勝敗へ拡張しない。

証明・再現手順は同名実験ディレクトリのproof.md、検算表はresults.md。
