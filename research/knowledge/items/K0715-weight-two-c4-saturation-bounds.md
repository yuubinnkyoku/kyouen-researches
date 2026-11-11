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
- path: research/log/2026-11-11-c4-saturated-n-plus-one-leaf-free.md
  role: proof
  note: n>=8かつn+1辺のC4飽和グラフに葉がないことの証明
- path: research/log/2026-11-11-c4-saturated-n-plus-one-all-n-ge-ten.md
  role: proof
  note: 二重閉路の構造分類と細分によりn>=10でn+1辺を排除
- path: research/log/2026-11-11-c4-saturated-ten-eleven-bicyclic-diameter-exclusion.md
  role: proof
  note: 一般下界の基礎となる10頂点21核の分類と直径の検査
- path: research/experiments/binary-cube-coplanar-midpoint-theorem-20261109/audit_bicyclic_diameters.py
  role: verifier
  note: 10頂点21核の直径をFloyd-Warshall法で独立照合し11..20頂点も有限検算
- path: research/experiments/binary-cube-coplanar-midpoint-theorem-20261109/bicyclic-diameter-audit.json
  role: data
  note: 二重閉路の基礎21ケースと11..20頂点の検算結果
scope: 二値立方体の重み2層、実アフィン共面四点禁止、包含極大安全集合の最小サイズ。全立方体や正方形格子には適用しない。
evidence: 単閉路分類と二重閉路分類・細分による下界、偶奇別の明示構成による上界。10頂点の21核の直径を独立計算し、構成はn=5..20で全四点・全欠辺追加を直接検算。
---

# 重み2層における極小極大配置

二値立方体 `{0,1}^n` の重み2頂点を `K_n` の辺とみなすと、共面四点を含まない包含極大集合は、`C4` を含まず任意の欠辺の追加で `C4` が生じるグラフに対応する。その最小辺数を `s_n^(2)` と書く。

`n≥7` では `n+1 ≤ s_n^(2) ≤ floor((3n−5)/2)`。下界は、極大グラフの連結性と、辺数が頂点数以下のグラフの単閉路分類から従う。上界は中心で交わる三角形に葉を付ける偶奇別の明示構成による。

さらに `n≥10` では **`n+2 ≤ s_n^(2)`**。葉を持つ `n+1` 辺の候補は葉の支持頂点の近傍構造と葉数上界から除外できる。葉のない候補は二重閉路の3種類に分類でき、辺の細分で10頂点11辺の21核から得られる。各核の直径は4以上で、細分は元の頂点間の距離を縮めない。一方、C4飽和グラフの直径は高々3なので矛盾する。21核の直径は元の幅優先探索に加え、Floyd-Warshall法でも独立に確認した。11〜20頂点の核の検算は全称証明の代替ではない。

下界と構成が一致するため、**`s_7^(2)=8`、`s_8^(2)=9`、`s_10^(2)=12`**。また、単閉路分類とその構成から `s_4^(2)=4`、`s_5^(2)=5`、`s_6^(2)=6`。`s_9^(2)=11` はK0716の有限全数列挙による。一般の `n≥11` で上界が最適とは主張しない。

構成の安全性と極大性を独立に確かめるため、`n=5..20` で全四点上の三種類の四角形を調べ、さらに各欠辺を追加したときに四角形が生じることを直接確認した。これは有限検算であり、全次元の結論は記載した分類と構成の証明に依存する。
