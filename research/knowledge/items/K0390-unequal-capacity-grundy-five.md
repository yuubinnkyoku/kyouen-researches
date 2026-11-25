---
id: K0390
title: 異容量上位列和制約ゲームでGrundy値5が実現する
kind: proposition
status: proved
topics:
- variants
- grundy
aliases: []
relations: []
artifacts:
- path: research/experiments/capacity-unequal-grundy-five-20261010/certificates.json
  role: certificate
  note: 4列331局面・5列662局面の完全mex証明書
- path: research/experiments/capacity-unequal-grundy-five-20261010/verify.py
  role: verifier
  note: 証明書全辺検査と容量直積全安全局面の独立mex計算
- path: research/experiments/capacity-unequal-grundy-five-20261010/README.md
  role: source
  note: 定義・具体例・再現手順・計算境界
scope: 列ごとの上限が異なる抽象容量占有ゲーム、通常プレイ、上位h列の占有数和がr以下
evidence: 有限完全mex証明書・独立した全安全局面逆順計算
---

# 異容量ではGrundy値5が実現する

列上限 `c=(1,4,4,5,5)`、上位 `h=3` 列の占有数和上限 `r=12`、局面 `x=(0,2,1,1,0)` を考える。各手は任意の1列の占有数を1増やす。安全性は上位3列和が12以下であること。

この局面は上位3列和4、容量余裕 `σ=8` で、**`g(x)=5`**。列0,1,2,3,4への全5合法手の子Grundy値は順に **`4,2,3,1,0`** である。従って `mex{0,1,2,3,4}=5`。

さらに4列の `c=(4,4,5,5),h=3,r=12,x=(2,1,1,0)` でも `σ=8,g(x)=4` であり、全合法子の値は順に `3,2,0,1`。

**証明の完結性**：各根から到達可能な全331/662局面のmex値を証明書に列挙した。独立検証器は全合法辺・mex等式を照合し、別途容量直積内の全858/1716安全局面を石数の降順に再計算して証明書の全行と一致した。全局面は着手ごとに石数が増える有限非巡回グラフなので、各局面のmex等式の成立から帰納法で根の値が厳密に従う。

一般に幅 `w` の任意のこの種のゲームは一局面の合法手が高々 `w` 種なので `g(x)<=w`。5列の例はこの上界を達成する。**ただし任意の `w` で上界を達成できるとは主張しない。**

等容量ゲームの `g<=3` 全称定理（未統合のK0384候補）およびK0352の等容量の結論とは対象が異なり、矛盾しない。異容量版の `g<=3` は反証されたが、`h` 固定での一様上界や無界性は未解決。

再現コード・証明書・実行記録は [実験報告](../../experiments/capacity-unequal-grundy-five-20261010/README.md) を参照。
