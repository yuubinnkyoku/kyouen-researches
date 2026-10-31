---
id: K0586
title: 二担い手q点禁止ゲームは盤面総点数によらず定数状態で強解決できq≥5の空盤値とq≥6の全初手を決定できる
kind: proposition
status: proved
topics: [geometry, variants, grundy, residual-games, first-moves]
aliases: []
relations:
- type: generalizes
  target: K0583
  note: N=2qの七型から二担い手の任意の総点数へ拡張
- type: generalizes
  target: K0585
  note: N=2q+1の十二型から二担い手の任意の総点数へ拡張
- type: depends_on
  target: K0002
  note: 通常・misère補助mexの定義
artifacts:
- path: research/experiments/two-carrier-universal-20261031/proof.md
  role: proof
  note: 1505個の局所mex恒等式と帰納法による全称証明
- path: research/experiments/two-carrier-universal-20261031/verify.py
  role: verifier
  note: 72盤951327安全局面の独立点別再帰と根初手192条件
scope: q≥4、交差点数が高々2の二つのq点容量制約だけを持つ有限配置ゲームの全安全局面。空盤公式はq≥5、全初手同値はq≥6。
evidence: 12種類の有限代表で1505個のmex恒等式を検査し無界帰納法に接続する計算機援用全称証明、72盤951327局面の独立点別照合
---

# 二担い手の普遍的な定数状態強解決

二つの集合A,Bが|A|,|B|≥q、|A∩B|=c≤2を満たし、各集合にq点以上置けないゲームを考える。外部自由点は任意個許す。平面の共円・共線q点禁止ゲームで担い手がちょうど二本なら適用できる。

A,Bの残容量u,v、未占有共有点数T、外部自由点数の偶奇E mod2、|A|=q+aと|B|=q+bに対するa>0,b>0の真偽だけで全安全局面の通常Grundy値gとmisère補助値hが決まる。u,v≥6はそれぞれ4+(u mod2),4+(v mod2)に縮約でき、**0≤g,h≤3**。

**空盤**：q≥5なら (g,h)=((c+z) mod2,1−((c+z) mod2))（zはA∪Bの外部点数）。q≥6なら**全初手の子の値が同一**で、通常・misèreの勝ち初手はそれぞれ全点か空集合であり、両者は逆。q=4の根公式とq=5の初手同値性はともに一般には不成立。

**証拠の範囲**：1505個の局所mex恒等式の厳密検査と残容量の無界帰納法による計算機援用全称証明。独立の点別再帰で72盤951327安全局面を照合、不一致0。Lean形式検査なし。大盤残局で別の残余禁止集合が生じる場合や、第三の禁止曲線が存在する場合には適用しない。
