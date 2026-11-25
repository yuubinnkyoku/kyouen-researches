---
id: K0387
title: 異容量の列制約では偶数余裕でもGrundy値3が生じる
kind: proposition
status: proved
topics:
- variants
- grundy
aliases: []
relations:
- type: depends_on
  target: K0352
  note: 等容量の抽象ゲームを列別上限へ変更する際の適用境界を明確化する
artifacts:
- path: research/experiments/capacity-unequal-caps-20261010/README.md
  role: proof
  note: 具体的な2つの証人と全合法子のmex
- path: research/experiments/capacity-unequal-caps-20261010/certificates.json
  role: data
  note: 22局面と44局面の全後続局面証明書
- path: research/experiments/capacity-unequal-caps-20261010/verify_certificates.py
  role: verifier
  note: 証明書の閉包とmex等式の独立検証
- path: research/experiments/capacity-unequal-caps-20261010/verify_full_product.py
  role: verifier
  note: 全安全状態からの独立逆順mex計算
scope: 列上限が列ごとに異なる抽象容量ゲームにおける存在命題。h=2,r=4の具体的証人。
evidence: 全22/44後続局面の閉包・mex証明書と、62/124全安全局面の独立有限完全列挙
---

# 偶数容量余裕でもGrundy値3を実現

列ごとの上限を `c=(1,1,2,2,3)`、上位2列の占有数和の上限を `r=4` とし、ラベル付き局面 `x=(0,1,0,0,1)` を考える。`sum(top_2(x))=2` なので余裕 `sigma=2` は偶数。しかし全合法子のGrundy値集合は厳密に `{0,1,2}` であるため、`g(x)=3`。

また `c=(1,2,2,3),x=(1,0,0,1),h=2,r=4` では同じく `sigma=2` で `g(x)=2`。

いずれも根から到達する全後続局面のGrundy表を完全に列挙し、合法手の閉包とmexを独立検査した。証明書・別方式の全安全局面再帰は[実験記録](../../experiments/capacity-unequal-caps-20261010/README.md)を参照。

**量化の限界**：これは列上限が異なる場合に「偶数余裕ならGrundy0/1」が偽になることを示す**存在反例**であり、等容量版の全称定理に矛盾しない。異容量版での一様上界3の真偽は未解決。
