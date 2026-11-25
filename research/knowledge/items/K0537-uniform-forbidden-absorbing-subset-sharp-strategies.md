---
id: K0537
title: q点禁止ゲームは小さい吸収集合から勝敗を構成でき、集合サイズ条件は鋭い
kind: proposition
status: proved
topics: [variants, rules, grundy, first-moves]
aliases: []
relations:
- type: depends_on
  target: K0002
  note: 通常プレイの最後の合法手と勝ち初手の規約
artifacts:
- path: research/experiments/absorbing-subsets-20261024/proof.md
  role: proof
  note: 吸収集合完成の手数戦略と、偶数・奇数両方の全称的な鋭さ反例
- path: research/experiments/absorbing-subsets-20261024/verify.py
  role: verifier
  note: 吸収条件の全上位集合検査と二方式の全安全局面mex
- path: research/experiments/absorbing-subsets-20261024/results.json
  role: data
  note: q=2..12の22族・32637安全局面の個別値照合
scope: 有限盤N≥q−1、禁止辺が全て厳密にq点の共通占有通常プレイ。偶数q≥2、奇数q≥3。
evidence: 先手の2|T|−1手・後手の2(|T|−1)手の完成戦略による数学的証明。サイズ条件の一つ緩い反例を全qで構成。
---

# 小さい吸収集合による勝敗の構成

Tを含むすべてのq点集合が禁止されるとき、Tを吸収集合と呼ぶ。
盤点数N≥q−1なら、Tの完成後はq−1石で必ず終局する。

- q=2r：r点以下の吸収集合が一つあれば先手必勝。T上の任意の点を初手にできる。
- q=2r+1：各点vが、それを含むr+1点以下の吸収集合T_vを持てば後手必勝で、全初手が負け手。

先手はTを遅くとも2|T|−1手、後手は初手点を含むT_vを遅くとも2(|T_v|−1)手で完成できる。
完成までq点未満なので、選ぶ手の合法性も保証される。

両方の集合サイズ条件は鋭い。
q+1点のV=A⊔F、禁止族 `{V\{f}:f∈F}` に対して、
偶数qで|A|=r+1,|F|=rなら後手勝ち、奇数qで|A|=|F|=r+1なら先手勝ち。
後者ではr+2点の吸収集合が全点を覆うため、被覆サイズ条件を一つ緩められない。

Grundy値の具体的な値までは保証しない。
小辺が混在する禁止族、N<q−1、misèreにはそのまま適用しない。
