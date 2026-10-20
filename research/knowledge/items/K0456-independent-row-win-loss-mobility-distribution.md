---
id: K0456
title: 独立行容量ゲームの勝敗別合法手数分布と条件付き平均の厳密公式
kind: proposition
status: needs-review
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
scope: 各行の占有上限以外に禁止集合がないw行m点の容量ゲーム、w,m,r>=1
evidence: 2026-10-20添付統合。元資料では proved または computed と報告（個別の元statusは保存ZIPを参照）。本項目の全量化範囲に対する証明・計算の再監査は未完了。有限検証の実行範囲は統合実験のVALIDATION.mdを参照。
---


> 統合監査: 以下は取込元の主張・報告。全称証明・完全列挙の監査が未完了のため、現在の採用状態は needs-review。本文中の「証明」「一致」は元資料での報告を表す。


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

K0440は未統合の仮番号。mainへの書き込みが安全検査で拒否され、
knowledgeチェック・生成索引再構築・リポジトリ全体の回帰は未実施。
