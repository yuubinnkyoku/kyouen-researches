---
id: K0600
title: 格子状共円盤の全安全局面母関数・唯一の最短最長極大配置・二行型の連続終局欠番
kind: proposition
status: proved
topics: [geometry, maximal-safe, maximum-safe, residual-games, statistics, variants, strategy-length]
aliases: []
relations:
- type: depends_on
  target: K0599
  note: 任意m,nの格子状禁止四点組の整数平面実現と極小横断集合の分類
artifacts:
- path: research/experiments/grid-circle-spectrum-20261101/proof.md
  role: proof
  note: 安全局面の全石数別母関数、終局長の両極値と唯一性、二行型の全終局長、漸近密度の全称証明
- path: research/experiments/grid-circle-spectrum-20261101/verify.py
  role: verifier
  note: 四盤の全安全局面・極大配置完全列挙と十五組の独立極小横断集合検算
scope: 任意m,n>=2のK0599格子状円交差配置を整数平面上で実現する共円・共線4点禁止ゲーム。標準正方形全格子盤の勝敗・s_nは対象外。
evidence: K0599の幾何実現に基づく無界m,nの組合せ論的全称証明。四盤の点別完全列挙と十五組の極小横断集合独立検算で不一致0。
---

# 格子状共円盤では最短極大配置が平方根規模、最長はほぼ全点

K0599 の整数点構成を使う。点は O、m 個の行点 R_i、n 個の列点 C_j、mn 個の専用点 P_ij、総点数 N=(m+1)(n+1)。禁止4点組は E_ij={O,R_i,C_j,P_ij} の mn 個だけである。

**全安全局面の石数別母関数**は

\[
A_{m,n}(u)=(1+u)^{N-1}
+u\sum_{a=0}^{m}\sum_{b=0}^{n}
\binom ma\binom nb u^{a+b}(1+u)^{mn-ab}.
\]

従って全安全局面数は

\[
A_{m,n}(1)=2^{N-1}
+\sum_{a=0}^{m}\binom ma(2^m+2^{m-a})^n.
\]

**最短極大石数と最大安全石数**は、任意 m,n>=2 に対して

\[
\boxed{s=m+n+1,\qquad K=N-1=mn+m+n}.
\]

どちらも達成配置は唯一である。最短は O とすべての行点・列点だけを選んだ配置、最長は O 以外の全点を選んだ配置。特に m=n=k とすれば N=(k+1)^2、s=2\sqrt N-1、K=N-1 で、**任意整数点配置族では s/K→0** が全称的に実現される。

**二行型 m=2 の全終局長**は n>=2 に対し厳密に

\[
\boxed{\{n+3,n+4,\ldots,2n+3\}\cup\{3n+1,3n+2\}}.
\]

n>=4 なら **2n+4,...,3n の連続 n-3 個が欠番**となる。母関数の全係数も

\[
P_{2,n}(u)=u^{3n+2}+u^{3n+1}+u^{2n+3}
+\sum_{b=0}^{n-1}\binom nb u^{n+3+b}
+2(2^n-1)u^{2n+2}
\]

で決まる。n=3 では K0599 の12点・6禁止円例の終局長6〜11を再現し、n=4 では7〜11・13・14石だけで12石が欠番になる。

**安全集合の密度** p=A_mn(1)/2^N は

\[
\frac12\le p\le\frac12+\frac12(7/8)^{\min(m,n)}
\]

であり、m,n がともに無限大になると 1/2 に収束する。固定 m で n→∞ の極限は 1/2+2^{-m-1}。

全称証明は O の選択による安全集合の分類、および K0599 の極小横断集合分類からの代数的導出。独立検証器では2x2・2x3・2x4・3x3の全部分集合を点別列挙し、さらに2xn (n=2..10)・kxk (k=2..7) の15組で極小横断集合を一点ずつ削除して直接検査した。**不一致0**。

これは標準 n×n の全格子点を使う問題 K0147 の s_n=o(n) を証明しない。整数点を自由に配置できる盤に関する結果であり、11×11の全121点盤の勝敗も未確定のままである。
