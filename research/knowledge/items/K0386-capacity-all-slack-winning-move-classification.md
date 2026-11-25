---
id: K0386
title: 全容量余裕の容量占有ゲームにおける全勝ち手分類
kind: proposition
status: proved
topics:
- variants
- grundy
- strategy-length
aliases: []
relations:
- type: depends_on
  target: K0384
  note: 容量余裕に応じたGrundy署名を使う
- type: generalizes
  target: K0358
  note: 余裕1の勝ち手分類を一般化
artifacts:
- path: research/experiments/capacity-winning-moves-20261010/README.md
  role: proof
  note: 下位着手と上位着手の全称分類、物理列・盤上点数の厳密式
- path: research/experiments/capacity-winning-moves-20261010/check_winning_moves.py
  role: verifier
  note: 422953局面・2628542合法列着手の直接mex照合
- path: research/experiments/capacity-winning-moves-20261010/check_lower_ordered.py
  role: verifier
  note: 388006非整列局面・420945下位着手の署名非依存mex照合
scope: 抽象容量占有ゲームの全1≤h<w,m≥1,0≤r<hm、全安全局面。幾何盤への適用はK0352の条件に従う。
evidence: K0372の全称署名定理からの数学的帰結、独立の直接mex有限検証2方式
---

# 全容量余裕の勝ち手分類

降順局面 `x_1≥...≥x_w`、上位h列の最小値 `b=x_h`、容量余裕 `sigma=r−sum_{i≤h}x_i`、下位残量 `R=(w−h)b−sum_{i>h}x_i` とする。

**下位着手の全称定理：** `x_i<b` の列への合法着手は、親のGrundy値がちょうど1である場合に限り、**すべて**Grundy 0へ進む。親のGrundy値が2/3なら下位子は3/2、親が0なら下位子は1である。

**上位着手を含む完全分類：** 親が0なら勝ち手なし。親が1で余裕が奇数なら全合法手が勝ち手。親が1で余裕が偶数なら全下位着手と、上位着手子の署名がK0384の `single` 型であるものだけが勝ち手。親が2/3なら余裕は奇数・親署名は `mixed` で、勝ち手は上位着手だけである。上位子形 `v` の偶数余裕署名を `theta(v)`、元の上位形を `u`、余剰列数を `n=w−h` とすると、勝ち手となる上位子は

`(n*(v_h−u_h)+theta(v)) mod2 = R mod2`

を満たすものに限る。親が2/3のとき、この条件を満たす上位子と満たさない上位子がどちらも必ず存在する。

各物理列iの空き点数 `m−x_i` を勝ち手列について合計すれば、実際の盤上での勝ち手となる点数も厳密に求まる。

**証明と独立検証：** [全称証明・全列の分類・物理点数の区別](../../experiments/capacity-winning-moves-20261010/README.md) を参照。署名を用いる検査で422,953局面・2,628,542合法列着手を、署名を使わない別方式で388,006非整列局面・420,945下位着手を照合した。有限検査を無界の証明とは扱わない。

標準2次元共円ゲーム一般の勝ち手にこの定理を直接適用してはならない。
