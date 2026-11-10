---
id: K0715
title: 二値立方体の重み2層における極小極大配置の上下界
kind: proposition
status: proved
topics: [variants, geometry, maximal-safe]
aliases: []
relations:
- type: depends_on
  target: K0713
  note: 重み2層の共面四点禁止と完全グラフ上のC4禁止の同値
artifacts:
- path: research/experiments/binary-cube-coplanar-midpoint-theorem-20261109/weight-two-c4-saturation-unicyclic-classification-20261110.md
  role: proof
  note: n辺以下の極大C4禁止グラフの分類とn>=7でのn+1下界
- path: research/experiments/binary-cube-coplanar-midpoint-theorem-20261109/weight-two-odd-dimension-improved-saturation-20261110.md
  role: proof
  note: 奇数次元の構成と全欠辺の極大性の証明
- path: research/experiments/binary-cube-coplanar-midpoint-theorem-20261109/weight-two-even-dimension-improved-saturation-20261110.md
  role: proof
  note: 偶数次元の構成と全欠辺の極大性の証明
- path: research/experiments/binary-cube-coplanar-midpoint-theorem-20261109/audit_saturated_constructions.py
  role: verifier
  note: n=5..20で四点上の閉路と全欠辺追加後の閉路を直接照合
- path: research/experiments/binary-cube-coplanar-midpoint-theorem-20261109/saturated-constructions-audit.json
  role: data
  note: 偶奇それぞれの構成の有限検算結果
scope: 二値立方体の重み2層、実アフィン共面四点禁止、包含極大安全集合の最小サイズ。全立方体や正方形格子には適用しない。
evidence: C4禁止極大グラフの単閉路分類による下界と、偶奇別の明示構成による上界。n=5..20で全四点・全欠辺追加を直接検算。
---

# 重み2層における極小極大配置

二値立方体 `{0,1}^n` の重み2頂点を `K_n` の辺とみなすと、共面四点を含まない包含極大集合は、`C4` を含まず任意の欠辺の追加で `C4` が生じるグラフに対応する。その最小辺数を `s_n^(2)` と書く。

`n≥7` では `n+1 ≤ s_n^(2) ≤ floor((3n−5)/2)`。下界は、極大グラフの連結性と、辺数が頂点数以下のグラフの単閉路分類から従う。上界は中心で交わる三角形に葉を付ける偶奇別の明示構成による。

下界と構成が一致するため、**`s_7^(2)=8`、`s_8^(2)=9`**。また、単閉路分類とその構成から `s_4^(2)=4`、`s_5^(2)=5`、`s_6^(2)=6`。一般の `n≥9` で上界が最適とは主張しない。

構成の安全性と極大性を独立に確かめるため、`n=5..20` で全四点上の三種類の四角形を調べ、さらに各欠辺を追加したときに四角形が生じることを直接確認した。これは有限検算であり、全次元の結論は記載した分類と構成の証明に依存する。
