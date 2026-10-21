---
id: K0456
title: 独立行容量ゲームの勝敗別合法手数分布と条件付き平均の厳密公式
kind: proposition
status: proved
topics:
- variants
- grundy
- statistics
aliases: []
relations: []
artifacts:
- path: research/experiments/game-structure/reports/independent-row-mobility-distribution-20261016.md
  role: proof
  note: 二変数母関数・勝敗別平均・漸近式の全称証明
- path: research/experiments/game-structure/scripts/verify_mobility_20261016.py
  role: verifier
  note: 物理的ビット集合の直接列挙と多項式畳み込みの独立比較
- path: research/experiments/game-structure/output/mobility-audit-20261016.txt
  role: data
  note: 95条件・317253局面の完全有限検算結果
- path: research/experiments/knowledge-audit-20261021/README.md
  role: log
  note: 証明の論理監査・再実行範囲・判定
scope: 各行の占有上限以外に禁止集合がないw行m点の容量ゲーム、w,m,r>=1
evidence: '2026-10-21監査。二変数母関数・平均差の正値性・境界を確認し95条件317253局面を再検査。 監査記録: research/experiments/knowledge-audit-20261021/README.md。'
---


# 勝敗別の合法手数の完全分布

行容量a=min(m,r)の独立行ゲームで、不足数d=wa−|S|、合法手数ell(S)とする。

```
F(z,t)=C(m,a)+sum_{k=0}^{a-1} C(m,k) z^(a-k)t^(m-k)
```

このとき `[z^d t^ell] F(z,t)^w` は対応する安全石集合の厳密な個数。
Grundy値はd mod2であり、勝ち側・負け側の合法手数分布はそれぞれ
`(F(1,t)^w−F(−1,t)^w)/2` と `(F(1,t)^w+F(−1,t)^w)/2`。

m>rでは勝ち局面の平均合法手数は負け局面の平均より**厳密に大きい**。
固定w,rでm→∞なら、勝ち確率wr/m+O(m^-2)、勝ち側平均m-r+1+O(m^-1)、
負け側平均wr(wr-1)/m+O(m^-2)。
m<=r,wm>=2では勝敗別平均はともにwm/2。

全称証明と厳密閉公式は上記report。有限検算は95条件・317253局面。
**共円ゲームへの適用は行間の禁止集合がないと証明された領域に限定する。**

取込時の未統合状態は解消済み。現行項目の検査・生成索引再構築は2026-10-21監査で実施。
