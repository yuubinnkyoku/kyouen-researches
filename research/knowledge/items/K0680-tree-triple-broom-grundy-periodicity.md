---
id: K0680
title: 三葉三点制約付き箒木のGrundyは311以降34周期となり、効果は固定半径近傍と偶奇だけでは決まらない
kind: proposition
status: proved
topics: [residual-games, grundy, geometry, variants]
aliases: []
relations:
- type: depends_on
  target: K0108
  note: 二点グラフに三点辺を加えた全残余禁止族の通常ゲーム
- type: depends_on
  target: K0336
  note: 二点辺だけの三葉を一葉へ圧縮し道のGrundyへ還元
- type: depends_on
  target: K0344
  note: 三点辺付き三葉は内部容量2の縮約で二葉箒にGrundy同値となる別説明
- type: depends_on
  target: K0681
  note: 全長の抽象木＋三点辺を有限整数点盤の指定安全局面に実現
artifacts:
- path: research/experiments/tree-triple-broom-periodicity-20261107/proof.md
  role: proof
  note: 正確な二列mex再帰、有限窓からの全称周期帰納、34合同類と非局所性の系
- path: research/experiments/tree-triple-broom-periodicity-20261107/verify_period.py
  role: verifier
  note: 周期の整数証明書、原始禁止集合の独立subset mex38条件、閉近傍削除19条件
- path: research/experiments/tree-triple-broom-periodicity-20261107/output/period_audit.json
  role: certificate
  note: 必要な全prefix、311..657の比較、最小周期・開始位置の証拠と全34剰余表
- path: research/log/2026-11-07-tree-triple-broom-periodicity.md
  role: log
  note: 特殊木族の再帰発見から全長周期証明と整数幾何実現へ至る経緯
scope: 中心に三葉と長さL>=0の道を付けた木の全二点辺、および三葉上の三点辺1本を禁じる通常ゲーム。抽象残余族とK0681による有限整数点盤の指定安全局面。標準全正方形格子盤は含まない。
evidence: 二列mex再帰の手の全分類と有限窓からの全称周期帰納、0..691の整数証明書。独立subset mex38条件・全287525安全状態と閉近傍削除19条件で小サイズを監査。
---

## 命題と全長分類

中心c、三葉a,b,d、長さLの道 c−v₁−…−v_L からなる木を B_L とする。
全ての木の辺と三点集合{a,b,d}を禁止する一点追加通常ゲームのGrundyをb_L、
三点辺を無視した二点近似をh_L、n頂点の道のGrundyをp_nとする。

**全称定理：** h_L=p_{L+2}、b_Lは **L=311から周期34**。
最小の最終周期は34、周期34の最小開始位置は311。
L=0..310の明示prefixと34合同類で全長のGrundyを分類できる。

L≥311では、

* 値が変わらない必要十分条件は **L≡5,12 (mod34)**。
* 勝敗が反転する必要十分条件は **L≡2,6,13,18,22,26,32 (mod34)**。
* 値変更の長さの自然密度は16/17、勝敗反転は7/34。
* 全Lでb_L≤15、L≡3 (mod34), L≥311ならb_L=15。

完全な合同類表とprefixは[証明書](../../experiments/tree-triple-broom-periodicity-20261107/output/period_audit.json)にある。

## 固定半径による判定の不可能性

任意の固定半径Rに対し、十分大きいtを取り、L₁=34t+5、L₂=34t+13とする。
二つのマーク付き木は、三点間距離が全て2、Steiner木がK1,3、
中心から半径R以内の誘導球が同型で、長枝と頂点数の偶奇も同じ。
しかしL₁ではb=h=1、L₂ではb=0,h=5となる。

従って三点辺の効果は、三点間距離・Steiner木・任意の固定半径の近傍と
付加枝の偶奇だけからは判定できない。半径は競合グラフの距離である。
K0681により各木＋三点辺は、標準q=4の有限整数点盤の残局として全て実現できる。

## 証明と検証境界

b₀=2,b₁=1で、L≥2について

\[
 b_L=\operatorname{mex}\bigl(
 \{1\oplus p_L,p_{L-1},p_{L-2},b_{L-2}\}\cup
 \{b_i\oplus p_{L-3-i}:0\le i\le L-3\}\bigr).
\]

二列がN..2N+T+1で周期Tを満たせば、畳み込みの大きい添字にTを足し引きする
帰納法で全長に周期性が従う。N=311,T=34について値0..691だけでこの証明条件を満たす。
b₃₁₀=8≠14=b₃₄₄が開始位置の鋭さを、34項の全ての短い循環シフトの不一致が最小周期を保証する。
これは[全称帰納証明](../../experiments/tree-triple-broom-periodicity-20261107/proof.md)と
有限整数証明書を組み合わせた計算支援証明であり、長い標本からの外挿ではない。

L=0..18で、原始禁止族からの別subset mex38条件・287525安全状態と、
二点版の閉近傍削除19条件が一致した。道の既知周期性自体は新規成果とは扱わない。
任意の木の一般分類、標準全格子盤への実現、misère版は対象外。

## 構造上の別説明と先行文献

三葉の三点禁止は交換可能classの内部容量を2にする。
K0344により三葉を二葉へ縮めても商DAGとGrundyを保存するため、b_Lは二点辺だけの二葉箒にも等しい。
この二葉箒の周期34・開始311に対応する族は
[Songsuwan, Node-Kayles on Trees, Theorem 3.2](https://arxiv.org/html/2512.24221v1#S3)でも扱われている。
この数値周期自体を世界的に新規とは扱わず、本項は独立再証明・三点制約の効果分類・
有限整数点盤への移送として位置付ける。
より一般の5点以下の全核の全長分類はK0682にある。
