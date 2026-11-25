---
id: K0599
title: 円の格子状交差で任意m×nの極大配置母関数を全称決定し6禁止円で全終局長を整数実現
kind: proposition
status: proved
topics: [geometry, maximal-safe, residual-games, variants, strategy-length]
aliases: []
relations:
- type: depends_on
  target: K0596
  note: 極大安全集合と包含極小横断集合の対応を利用
artifacts:
- path: research/experiments/grid-circle-terminal-polynomial-20261101/proof.md
  role: proof
  note: 格子状交差の任意整数m,nに対する有理円構成と母関数の全称証明
- path: research/experiments/grid-circle-terminal-polynomial-20261101/verify.py
  role: verifier
  note: 12整数点の全495四点組と4096部分集合、四種の抽象盤の全安全局面を独立検査
scope: 任意m,n>=2の整数平面上の任意有限点配置、共円または共線4点禁止。標準11×11全盤の勝敗は対象外。
evidence: 有理円の有限除外構成と包含極小横断集合の全称証明。12点495四点組と2x2、2x3、2x4、3x3の全安全局面を整数演算で独立完全列挙。
---

# 格子状の円の交差から終局長母関数を決定

任意の整数 m,n>=2 で N=(m+1)(n+1) 個の整数点を構成でき、禁止4点集合は正確に mn 個の E_ij={O,R_i,C_j,P_ij} となる。このとき極大安全集合の石数別母関数は

\[
P_{m,n}(u)=u^{N-1}+u^{N-m}+u^{N-n}
+\sum_{a=0}^{m-1}\sum_{b=0}^{n-1}\binom ma\binom nb
u^{N-a-b-(m-a)(n-b)}.
\]

m=2,n=3 では12点・6禁止4点組で P(u)=u^6+3u^7+17u^8+u^9+u^10+u^11。従って**6〜11石の連続した全6終局長**を、抽象超グラフではなく実際の整数平面の共円・共線ゲームで実現する。

証明は、補集合の包含極小横断集合を行・列・専用点で分類すること、および有理円上で有限個の不要な共円・共線条件を回避して整数化することによる。12点の明示座標を全495四点組の行列式で照合し、全4096部分集合と小さな格子状構成3種も独立検算した。**無界のm,nは数学的証明、具体係数は有限完全列挙であり、標準11×11全盤の勝敗は未解決。**
