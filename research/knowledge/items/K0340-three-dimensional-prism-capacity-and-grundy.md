---
id: K0340
title: 三次元の平行格子列では高qでも二列容量が残り、列数の偶奇が全Grundy0/1を決める
kind: proposition
status: proved
topics: [variants, geometry, grundy, maximal-safe]
aliases: []
relations:
- type: depends_on
  target: K0305
  note: 全極大同偶奇と全Grundy0/1の同値
artifacts:
- path: research/experiments/prism-hyperplane-2026-10-05/proof.md
  role: proof
  note: 超平面分類、全極大分類、全称Grundy式と奇数列のnimber2
- path: research/experiments/prism-hyperplane-2026-10-05/verify.py
  role: verifier
  note: 占有数mexと独立の有理数lifted-rank subset検算
- path: research/experiments/prism-hyperplane-2026-10-05/output.json
  role: data
  note: 12長盤・120全長境界の占有数全検算と3小盤全subset検算
---

# 三次元の平行格子列では高qでも二列容量が残る

3点共線のない相異なる整数底面点B、列数w≥3について、三次元盤
`B×{0,...,m−1}`を考える。超平面または超球面上のq点を禁止する通常プレイで
`q>2w`, `r=q−1`, `m≥1`とする。これは標準二次元盤とは異なる変種。

安全性は占有数の全ペア条件`x_i+x_j≤r`と同値。
2m≤rなら全極大は全点占有のみ。それ以外の全極大の降順占有数は
`(a,r−a,...,r−a)`, `ceil(r/2)≤a≤min(m,r)`に完全分類される。
終局長は`(w−1)r−(w−2)a`で、任意に長い盤でも全行容量wrへ安定化しない。

w偶数では全安全局面で`g(S)=(min(2m,r)−|S|) mod2`。
w奇数ではm≤ceil(r/2)と「全Grundy0/1」が同値。
m≥ceil(r/2)+1なら`a=ceil(r/2)`として占有数`(a,r−a−1,...,r−a−1)`の全局面がg=2。
特に長さm≥rの族では「全Grundy0/1」はw偶数と正確に同値。

具体的に2×2×mの全三次元格子点、q=10、m≥9は空盤先手勝ちで、
終局サイズ9,11,13,15,17を持つ。二次元4×m・q10の全終局36石・空盤後手勝ちと異なる。
K0025の二次元行分離を高次元へそのまま適用することはできない。

根拠は超球面・超平面と鉛直列の交点数、全極大占有数分類、mex帰納による全称証明。
保存した占有数DPと有理数lifted行列からの小盤全subset DPは独立の有限検算である。
奇数wの長盤空盤勝敗と奇数rの全Grundy公式はK0341で確定した。
本項目の全長分類から二次元標準盤のGrundy無界性や11×11勝敗は推論しない。
