---
id: K0657
title: 道型グラフ星共円ゲームの全終局長係数は端点付き削除区間の二項和で閉じる
kind: proposition
status: proved
topics: [geometry, maximal-safe, statistics, strategy-length, variants]
aliases: []
relations:
- type: depends_on
  target: K0602
  note: グラフ星型整数共円構成の極大配置分類を使用
- type: depends_on
  target: K0609
  note: 道型の既知三項漸化式と照合し、その係数を閉形式に精密化
artifacts:
- path: research/experiments/path-run-coefficients-20261103/proof.md
  role: proof
  note: 端点削除と内部削除区間の正長分割による全称二項和・端係数の証明
- path: research/experiments/path-run-coefficients-20261103/verify.py
  role: verifier
  note: 75条件の三方式比較・21条件の大規模漸化式比較・12条件の禁止超辺全局面完全列挙
scope: K0602の整数平面グラフ星型構成でG=P_n（n>=2）、任意q>=4。標準全格子盤は対象外。
evidence: 削除区間の全単射と正長分割による全称証明。108条件の有限監査は独立検査。
---

# 道型構成の終局長係数の閉公式

\(n\ge2\)、\(q\ge4\)、\(r=q-3\)、\(N=1+n+r(n-1)\)、\(s=N-(n-1)\) とする。道 \(P_n\) に対応するK0602の極大安全配置の石数母関数は

\[
\boxed{P_{P_n,q}(u)=u^{N-1}+u^s\sum_{k=0}^{\lceil n/2\rceil-1}a_{n,k}(r)u^k},
\]
\[
\boxed{a_{n,k}(r)=\sum_{a,b\in\{0,1\}}\sum_{j=0}^{k}
\binom{k}{j}\binom{n-a-b-k-j-1}{k}r^{n-2k-j-a-b-1}.}
\]

ただし \(n-a-b-k-j<k+1\) の項は0とする（負指数は評価しない）。**中心付きの終局長は \(s,s+1,\ldots,s+\lceil n/2\rceil-1\) の全て**であり、係数は正整数。特に中心付き最長係数は

\[
\boxed{a_{2h+1,h}(r)=1\ (h\ge1),\qquad a_{2h,h-1}(r)=h(r+1)+1\ (h\ge2).}
\]

中心なしの一通りは \(N-1=s+n-2\) 石。\(n=2,3\) では中心付き終局長と重複し、\(n\ge4\) では別の長さとなる。\(n\ge4\) の全終局長の欠番数は \(\lfloor n/2\rfloor-2\)。最短係数は \(n\ge3\) で \(r^{n-3}(r+1)^2\)、\(n=2\) の中心付き最短係数は \(r+2\)（中心なしも加えると \(q\)）。

証明は、削除区間の長さが内部では1か2、両端では高々1であることと、残存頂点を \(k+1\) 個の正長区間に分割する二項係数の全単射による。[全称証明](../../experiments/path-run-coefficients-20261103/proof.md)と[独立検証器](../../experiments/path-run-coefficients-20261103/verify.py)を保存。75条件の直接削除集合列挙・既知漸化式比較、21条件の長い道の漸化式比較、12条件の禁止超辺からの全局面列挙で不一致0。

K0609 の三項漸化式を明示係数へ、K0647 の道の支持集合を配置数まで強化する。これはK0602の自由な整数点構成についての数学的定理であり、標準 \(n\times n\) 格子盤の \(s_n\) や11×11の勝敗には直接適用しない。
