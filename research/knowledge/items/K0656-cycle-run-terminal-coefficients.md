---
id: K0656
title: サイクル型グラフ星共円ゲームの全終局長係数は削除区間の二項和で閉じる
kind: proposition
status: proved
topics: [geometry, maximal-safe, statistics, strategy-length, variants]
aliases: []
relations:
- type: depends_on
  target: K0602
  note: グラフ星型整数共円構成の極大配置分類を使用
artifacts:
- path: research/experiments/cycle-terminal-run-formula-20261103/proof.md
  role: proof
  note: 削除区間の巡回二重計数による全称閉公式、支持集合、最大中心付き係数の証明
- path: research/experiments/cycle-terminal-run-formula-20261103/verify.py
  role: verifier
  note: 105条件の独立直接列挙・漸化式比較と6条件の禁止超辺全局面完全列挙
scope: K0602の整数平面グラフ星型構成でG=C_n（n>=3）、任意q>=4。標準全格子盤は対象外。
evidence: 削除区間と残存区間の巡回二重計数による全称証明。111条件の有限検査は独立監査。
---

# サイクル型構成の全終局長を二項係数で数える

グラフを単純サイクル C_n（n>=3）、禁止点数を q>=4、r=q-3、全点数を N=1+(r+1)n、最短極大石数を s=1+rn とする。極大安全配置の石数母関数は

\[
\boxed{P_{n,r}(u)=u^{N-1}+u^s\sum_{k=0}^{\lfloor n/2\rfloor}a_{n,k}(r)u^k,}
\]

\[
a_{n,0}(r)=r^n,\quad
\boxed{a_{n,k}(r)=\frac nk\sum_{j=0}^{\min(k,n-2k)}
\binom kj\binom{n-k-j-1}{k-1}r^{n-2k-j}.}
\]

**全称定理：** 中心点を含む極大配置の石数は正確に \(s,s+1,\ldots,s+\lfloor n/2\rfloor\) で、**途中に欠番はない**。中心なしの極大配置は \(N-1=s+n-1\) 石の一通りだけ。全終局長の欠番数は \(\lceil n/2\rceil-2\)。

中心付きの最長石数の係数は特に簡単で、偶数 \(n=2h\) なら **2通り**、奇数 \(n=2h+1\) なら **\(n(q-2)\) 通り**。前者は交互に削除する2通り、後者は一つの余分な位置を持つ巡回配置である。

証明は、削除頂点集合が長さ1または2の巡回区間に分解され、区間本数 \(k\) が最短からの石数差に一致することによる。区間の長さ2の本数 \(j\) を固定して巡回配置を数えれば上式になる。全称証明は[proof.md](../../experiments/cycle-terminal-run-formula-20261103/proof.md)、独立検証器は[verify.py](../../experiments/cycle-terminal-run-formula-20261103/verify.py)。105組の数値照合と6組の禁止超辺からの全局面列挙で不一致0。これはK0608の漸化式を明示係数に強化したもので、有限実験の外挿ではない。

**範囲：** K0602の自由な整数平面点配置であり、標準全格子盤の \(s_n\)、11×11の勝敗・Grundy値には直接適用できない。
