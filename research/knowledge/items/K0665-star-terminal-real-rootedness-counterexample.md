---
id: K0665
title: 木型中心付き終局長多項式の実根性は星K1,3で破れ、星型では次数2以下に限る
kind: proposition
status: proved
topics: [geometry, maximal-safe, statistics, strategy-length, variants]
aliases: []
relations:
- type: depends_on
  target: K0602
  note: 中心付き極大配置の許容削除集合と重みの公式を使用
- type: contrasts
  target: K0664
  note: 道型で成立する実根性は一般の木へ拡張できない
artifacts:
- path: research/experiments/tree-terminal-real-roots-counterexample-20261103/proof.md
  role: proof
  note: 星型の全称母関数と全根の分類
- path: research/experiments/tree-terminal-real-roots-counterexample-20261103/verify.py
  role: verifier
  note: d=2..10、r=1..7の63条件の独立完全列挙
scope: K0602のグラフ星型整数共円構成で元グラフが星K1,d、d>=2、q>=4、中心点を含む極大配置の終局長差。標準全格子盤は対象外。
evidence: 許容削除集合の二場合分けによる全称証明。63条件の独立完全列挙で確認。
---

# 星型では中心付き終局長分布の実根性が一般に破れる

r=q-3>=1、d>=2とすると、中心付き極大配置の最短終局からの差の多項式は

\[
\boxed{F_{K_{1,d},r}(u)=(r+1)^d+u^{d-1}.}
\]

したがって **全根が負の実数であることとd=2は同値**。d>=3では非実根を持つ。最小の反例は木K1,3、q=4で、F(u)=8+u²、根は±2sqrt(2)i。

K0664の道型の実根性を一般の木に拡張する予想は反証された。なお星K1,3の終局長の欠番はK0647の既知結果とも整合する。ここでの新しい帰結は実根性の全称的な失敗と星型での完全分類である。

証明: [proof.md](../../experiments/tree-terminal-real-roots-counterexample-20261103/proof.md)。検証: [verify.py](../../experiments/tree-terminal-real-roots-counterexample-20261103/verify.py)。
