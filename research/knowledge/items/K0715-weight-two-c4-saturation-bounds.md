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
- path: research/log/2026-11-12-c4-three-leaf-false-lemma-counterexample.md
  role: source
  note: 3葉補題の反例とそれに依存する一般下界の証明の破綻
- path: research/experiments/binary-cube-coplanar-midpoint-theorem-20261109/verify_three_leaf_counterexample.py
  role: verifier
  note: 明示された8頂点3葉グラフのC4不在と全欠辺追加の独立検査
- path: research/experiments/binary-cube-coplanar-midpoint-theorem-20261109/three-leaf-counterexample-audit.json
  role: data
  note: 70四点集合と19欠辺の検査結果
- path: research/experiments/binary-cube-coplanar-midpoint-theorem-20261109/c4-saturation-n-plus-two-corrected.md
  role: proof
  note: 正しい葉高々3個を用いるn>=9のn+2下界と有限核の排除
- path: research/experiments/binary-cube-coplanar-midpoint-theorem-20261109/audit_bicyclic_boundary.py
  role: verifier
  note: 8・9頂点の二重閉路核を四角形と欠辺追加で直接検査
- path: research/experiments/binary-cube-coplanar-midpoint-theorem-20261109/bicyclic-boundary-audit.json
  role: data
  note: 8頂点12核・9頂点16核の直接検査結果
- path: research/experiments/binary-cube-coplanar-midpoint-theorem-20261109/audit_bicyclic_diameters.py
  role: verifier
  note: 10頂点21核の直径をFloyd-Warshall法で照合
scope: 二値立方体の重み2層、実アフィン共面四点禁止、包含極大安全集合の最小サイズ。全立方体や正方形格子には適用しない。
evidence: 単閉路分類、葉高々3個と二重閉路の構造分類による下界、偶奇別の明示構成による上界。9頂点16核と10頂点21核を有限直接検査。
---

# 重み2層における極小極大配置

二値立方体 `{0,1}^n` の重み2頂点を `K_n` の辺とみなすと、共面四点を含まない包含極大集合は、`C4` を含まず任意の欠辺の追加で `C4` が生じるグラフに対応する。その最小辺数を `s_n^(2)` と書く。

`n≥7` では `n+1 ≤ s_n^(2) ≤ floor((3n−5)/2)`。下界は、極大グラフの連結性と、辺数が頂点数以下のグラフの単閉路分類から従う。上界は中心で交わる三角形に葉を付ける偶奇別の明示構成による。

葉を持つ配置に限れば、この上界がすべての `n≥5` で厳密な最小値となる（K0742）。上界より小さい極大配置の探索は葉を持たないグラフに限ってよい。

以前ここに記載した `n≥10` の下界 `n+2` の証明は、3葉を持つC4飽和グラフは6頂点に限るという誤った補題に依存していたため撤回した。8頂点9辺・3葉の明示的な反例がある。これは `n+2` 下界自体の反例を意味しない。

その後、**`n≥9` では `n+2 ≤ s_n^(2)`** と修正された根拠で示せる。C4飽和グラフの葉は高々3個で、葉を持つ `n+1` 辺グラフには少なくとも `n−5` 個の葉が必要。`n≥9` では4個以上となり矛盾する。葉のない場合は二重閉路に分類され、9頂点の16核を直接排除できる。`n≥10` は10頂点21核からの辺の細分と直径の単調性で排除する。8頂点の3葉反例はこの修正版と矛盾しない。

さらに三重閉路核の12頂点への縮約と有限直径検査により、**`n≥11` では `n+3 ≤ s_n^(2)`**（K0744）。この強化も有限の核検査に依存する。

下界と構成が一致するため、**`s_7^(2)=8`、`s_8^(2)=9`、`s_9^(2)=11`、`s_10^(2)=12`**。また、単閉路分類とその構成から `s_4^(2)=4`、`s_5^(2)=5`、`s_6^(2)=6`。`s_9^(2)` と `s_10^(2)` はK0716・K0717の独立な全グラフ有限列挙とも一致する。`s_11^(2)=14` と `s_12^(2)=15` はK0743・K0744の構造縮約と有限検査による。一般の `n≥13` で上界が最適とは主張しない。

構成の安全性と極大性を独立に確かめるため、`n=5..20` で全四点上の三種類の四角形を調べ、さらに各欠辺を追加したときに四角形が生じることを直接確認した。これは有限検算であり、全次元の結論は記載した分類と構成の証明に依存する。
