---
id: K0428
title: 未出現の法27第四弦長型は全ての有限法で局所可解
kind: proposition
status: proved
topics: [geometry, rectangles, variants]
aliases: []
relations:
- type: depends_on
  target: K0427
  note: 法27の四つの必要弦長平方型のうち第四型を対象とする
artifacts:
- path: research/experiments/fixed-width/reports/q48-local-solubility-20261015.md
  role: proof
  note: Hensel持ち上げと中国剰余による全称構成
- path: research/experiments/fixed-width/scripts/q48_verify_local_solubility_20261015.py
  role: verifier
  note: 3冪平方根、CRT構成と円方程式の有限監査
- path: research/experiments/fixed-width/output/q48-local-solubility-audit-20261015.txt
  role: data
  note: 22法での座標合同監査
scope: 全正整数法Mにおける弦長平方の二階差分合同式、奇数性、厳密増加性。整数として厳密な四行8点円が存在するという主張ではない。
evidence: 任意のMに対し正の奇数 d0<d1<d2<d3 を構成し、二つの二階差分を -8 mod M、平方弦長を法27で (19,0,0,19) にできる。さらに円の整数係数方程式へ座標を代入する合同条件も、任意の有限法Nで満たせる。
---

`73` の平方根を法 `3^k` でHensel持ち上げし、3冪法では `(t_k,9,9,t_k)` を取る。3と互いに素な法では局所型 `(1,3,3,1)` を用い、中国剰余定理で貼り合わせた後、法の倍数を座標へ加えて正かつ厳密増加にする。この構成はどの固定有限法の合同篩も第四型を排除できないことを示す。

これは局所可解性だけの命題である。第四型の弦長方程式が整数として成立する解や、その型の実際の整数格子円の存在を含意しない。
