---
id: K0538
title: 多項式行列式版は同列三点の吸収性から次数3以上の勝敗と初手を構成できる
kind: proposition
status: proved
topics: [variants, geometry, rules, first-moves, rectangles]
aliases: []
relations:
- type: depends_on
  target: K0537
  note: 同列三点が吸収集合となることから完成戦略を適用
artifacts:
- path: research/experiments/absorbing-subsets-20261024/proof.md
  role: proof
  note: 同列三行の階数2から吸収性と次数偶奇の勝敗を証明
- path: research/experiments/absorbing-subsets-20261024/polynomial.py
  role: verifier
  note: 整数Bareiss・有理数消去の全行列式と二方式の全安全局面mex
- path: research/experiments/absorbing-subsets-20261024/polynomial.json
  role: data
  note: 9盤・9187個のq点組・14089安全局面の独立照合
solution:
  board: 多項式持ち上げ行列式版・各列3候補以上
  level: weak
  outcome: conditional
  classification: [root, first-moves]
  coverage: 全d≥3・総点数N≥d+1の対象盤の空盤と全初手
  conditions: q=d+2、det[x^d,x^(d−1),...,x,y,1]=0を禁止、退化を含む
  verification: [mathematical-proof]
  certificate: 同列三点を先手5手目・後手4手目までに完成し終局をd+1石へ固定する戦略
  independent_check: 9有限盤の二方式行列式・全局面mex。無界性は別途数学的証明
  note: 偶数dは全初手勝ち、奇数dは全初手負け。全安全局面の強解決ではない
scope: d≥3、q=d+2、正方行列det[x^d,x^(d−1),...,x,y,1]=0のq点を禁止する有限平面実数点盤、N≥d+1、通常プレイ。退化を含む。
evidence: 同列三点の行が高々二次元を張ることとK0537の構成戦略による全称数学的証明。
---

# 多項式持ち上げ行列式版の構成的な勝敗

q=d+2点の `det[x^d,x^(d−1),...,x,y,1]=0` を禁止する。
同じx座標の三点は行列の階数が高々2なので、その三点を含む全q点集合が禁止される。

N≥d+1のとき、次の条件が十分である。

- d偶数、d≥4：同列三点が一組でもあれば先手必勝。三点以上ある列上の任意の点を初手にできる。
- d奇数、d≥3：全点が三点以上の列に属せば後手必勝。

特に全列三候補以上なら、d偶数で全初手が勝ち手、d奇数で全初手が負け手となる。
先手は遅くとも5手、後手は初手点を利用して遅くとも4手で同列三点を完成させ、
終局をd+1石に固定する。長盤・等間隔・整数座標は仮定しない。

**ルールの境界**：退化した行列式零も禁止する。
同じxの複数点は関数グラフには載らないので、厳密な共多項式グラフだけを禁止する版とは異なる。
d=2のλ=0四点版には手数条件が足りず適用できない。
標準共円ゲームや、共球・共面の別規則の結論でもない。
