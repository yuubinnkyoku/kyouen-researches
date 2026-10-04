---
id: K0323
title: 7×7のGibbs分布は有限活動度で二つの最大相へ集中できる
kind: proposition
status: proved
topics: [statistics, maximum-safe, reconfiguration]
aliases: [B273]
relations:
- type: depends_on
  target: K0051
  note: 最大14石配置は二相各8個
- type: depends_on
  target: K0267
  note: 異なる最大配置間の一点移動には十二石以下が必要
artifacts:
- path: research/experiments/original-claims/reports/round69-b251-b300-original-scope-audit.md
  role: proof
  note: 有限λの重み上界による直接証明
---

# 7×7のGibbs分布は有限活動度で二つの最大相へ集中できる

標準7×7の全安全集合に確率比例λ^{|S|}を置く。最大14石集合はA/B各8個。λ=2^49とすると、各最大相の確率は8/17以上、十四石未満の全確率は1/17以下である。

安全集合は高々2^49個なのでλ≥1で低層重みR≤2^49λ^13。全重みは16λ^14+R。指定λではR≤λ^14より各相確率8λ^14/(16λ^14+R)≥8/17、低層確率R/(16λ^14+R)≤1/17。

K0267より各最大配置は十三石以上を保つ一点移動では他の最大へ移れない。最大層へ条件付けない有限分布に、分離したA/B両相の高い質量を保証する。二相が各一つの連結成分であること、連続秩序変数の局所最大数、無限盤の相転移や混合時間は主張しない。証明は現在の有限最大族分類を前提とする。

