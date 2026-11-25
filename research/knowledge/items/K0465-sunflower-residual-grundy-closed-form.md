---
id: K0465
title: ヒマワリ型残余禁止集合の全Grundy値は閉形式で高々3
kind: proposition
status: proved
topics:
- grundy
- residual-games
- search-methods
aliases: []
relations:
- type: depends_on
  target: K0305
  note: 奇数本の場合の極大集合同偶奇性から全局面の二値性を得る
- type: depends_on
  target: K0108
  note: 標準盤への適用には包含極小の残余禁止集合を正確に構成する
artifacts:
- path: research/experiments/sunflower-grundy-20261019/README.md
  role: proof
  note: 任意本数のヒマワリ型禁止集合に対する全称帰納証明と適用範囲
- path: research/experiments/sunflower-grundy-20261019/verify.py
  role: verifier
  note: 残数再帰と独立した全占有部分集合mexの照合
- path: research/experiments/sunflower-grundy-20261019/audit.json
  role: data
  note: 334構造・579915安全局面の照合結果
- path: research/experiments/game-structure/reports/sunflower_grundy_20261018.md
  role: proof
  note: 任意個のsunflower禁止集合の全称証明、極大数と安全局面数
- path: research/experiments/game-structure/scripts/sunflower_grundy_20261018.py
  role: verifier
  note: 実際のビット集合を使った全安全局面の独立mex再帰
- path: research/experiments/game-structure/output/sunflower_grundy_20261018.json
  role: data
  note: 12点以下1470盤・2580974安全局面の完全検証結果
- path: research/experiments/knowledge-audit-20261021/README.md
  role: log
  note: 証明の論理監査・再実行範囲・判定
scope: 任意有限ヒマワリ型禁止集合族 E_i=C∪P_i、各P_i非空で互いに素、Cは空でもよい。通常プレイの一点追加、自由点を許す。
evidence: '2026-10-21監査。花芯・最短花弁の大小別mex帰納と任意安全局面への帰着を確認。334構造579915安全局面の独立照合を再実行。 監査記録: research/experiments/knowledge-audit-20261021/README.md。'
---


# ヒマワリ型残余ゲームの閉形式

`h≥1` 個の禁止集合が `E_i=C∪P_i` で、花芯Cと非空の花弁P_iが互いに素であるとする。`c=|C|`, `p_i=|P_i|`, `P=Σp_i`, `N=c+P`, `m=min_i p_i`。自由点fを除いた空局面のGrundy値Gは

* h奇数：`G=(N−1) mod 2`。
* h偶数：`c<m` なら `G=N mod 2`、`c>m` なら `G=(N−1) mod 2`、`c=m` なら `G=2+(P mod 2)`。

自由点f個があれば `g=G xor (f mod 2)`。したがって全hについて `g≤3`。奇数hでは全安全局面が二値であり、偶数hでは任意のhについて `c=1, p_1=...=p_{h−1}=1, p_h=2` が `g=3` を達成する。

全称性は花芯・花弁への手のmex帰納法、および奇数hの極大安全集合サイズ `N−1,N−h` の同偶奇性から証明した。独立した占有部分集合mexで334個の有限構造・579915安全局面を検算した。詳細はproof artifact。

**限界**：抽象的な禁止集合ゲームに関する結果。標準整数格子の任意の残余集合がこの型になるという主張ではない。11×11の探索時間改善も未検証。

追加の同一命題資料: `K0465-sunflower-forbidden-grundy.md`。詳細と独立証人・検算範囲は追加artifactを参照。原文は取込元ZIPに保存。
