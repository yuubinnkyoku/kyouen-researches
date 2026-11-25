---
id: K0689
title: 純三点Berge森は六辺以下でGrundy3以下、八辺以下で7以下となり全て鋭い
kind: proposition
status: proved
topics: [grundy, residual-games, variants]
aliases: []
relations:
- type: depends_on
  target: K0108
  note: 残余ゲームと連結成分・自由点のxor分離
- type: depends_on
  target: K0683
  note: 達成する抽象三点族を指定有限整数点盤に移す
artifacts:
- path: research/experiments/pure-triple-hyperforests-20261107/proof.md
  role: proof
  note: 葉辺削除による全型生成完全性、有限核と任意自由点、鋭さ
- path: research/experiments/pure-triple-hyperforests-20261107/audit.py
  role: verifier
  note: 所属木生成・残余木mexと別C++生subset DPの比較
- path: research/experiments/pure-triple-hyperforests-20261107/output/audit.json
  role: certificate
  note: 全209連結型、7562646安全状態比較、成分xor全スペクトル
- path: research/log/2026-11-08-grundy-mobility-gap-and-hyperforests.md
  role: log
  note: 森の完全分類と合法点数上界を調べた記録
scope: 純三点極小禁止族の所属二部グラフが森、辺数h<=8、合法点数と自由点数と連結成分数は任意、通常プレイ。
evidence: 全連結所属木の葉辺追加生成と木同型code、全209型のPython/C++根値一致、全成分分解と自由点偶奇のxor。h<=5では独立Venn生成からの抽出とも型集合一致。
---

純三点Berge森は「頂点と辺の所属二部グラフが無閉路」という意味で用いる。
単なる二辺の交点数制限ではない。
自由点と任意個の成分を許すと、厳密にh辺の全Grundyスペクトルは

|h|全スペクトル|
|---:|---|
|0..3|0,1|
|4..6|0,1,2,3|
|7..8|0,1,2,3,4,5,6,7|

従ってg=2,3に必要な辺数は最少4、g=4,5,6,7に必要な辺数は最少7。
例えば七辺・十五点の連結木mask族
`7,25,98,388,1544,6176,25088`はg=6で、自由点一個を加えればg=7。
閉路がなくてもg≤1にはならない。

h辺の連結所属木は2h+1頂点を持ち、葉辺を消す帰納で全型を有限生成できる。
h=1..8の連結型数は1,1,2,4,8,19,48,126、連結型のみの最大値は
0,1,1,3,2,3,6,7。全209型を別のC++占有subsetで検査した。
h=6..8で生成そのものを二方式比較したとは主張せず、完全性は葉辺削除証明による。

[証明・再現資料](../../experiments/pure-triple-hyperforests-20261107/proof.md)を参照。
九辺以上の上界や標準全正方形格子盤での達成は未主張。
