---
id: K0742
title: 葉を持つC4飽和グラフの最小辺数はfloor((3n-5)/2)
kind: proposition
status: proved
topics: [variants, geometry, maximal-safe]
aliases: []
relations:
- type: depends_on
  target: K0715
  note: 偶奇別のC4飽和明示構成と重み2層の対応
artifacts:
- path: research/experiments/binary-cube-coplanar-midpoint-theorem-20261109/leaf-saturation-exact.md
  role: proof
  note: 葉の支持点の近傍・葉数上限・辺数式を用いる下界と明示構成による達成
- path: research/experiments/binary-cube-coplanar-midpoint-theorem-20261109/audit_leaf_saturation_bound.py
  role: verifier
  note: n=4..6の全グラフとn=5..20の明示構成で下界・達成・極大性を照合
- path: research/experiments/binary-cube-coplanar-midpoint-theorem-20261109/leaf-saturation-bound-audit.json
  role: data
  note: 小次元の列挙数と明示構成の辺数・葉数
- path: research/experiments/binary-cube-coplanar-midpoint-theorem-20261109/weight-two-odd-dimension-improved-saturation-20261110.md
  role: certificate
  note: 奇数n>=5で葉を持ち下界を達成する明示構成
- path: research/experiments/binary-cube-coplanar-midpoint-theorem-20261109/weight-two-even-dimension-improved-saturation-20261110.md
  role: certificate
  note: 偶数n>=6で葉を持ち下界を達成する明示構成
- path: research/experiments/binary-cube-coplanar-midpoint-theorem-20261109/d11-c4-saturation-sat-20261111/result.json
  role: data
  note: 11頂点13辺・固定辺SAT試行の50万衝突結果はUNKNOWN
scope: n>=5頂点の少なくとも1個の葉を持つC4飽和単純グラフ。葉なしグラフを含む一般の飽和数の厳密値は主張しない。
evidence: 葉支持点の近傍マッチングと葉高々3個からの辺数下界、および偶奇別の明示構成による全称証明。n=4..6の全グラフとn=5..20の構成を直接検算。
---

# 葉を持つC4飽和グラフの最小辺数

`n≥5` について、少なくとも1個の葉を持つ `n` 頂点 C4 飽和単純グラフの最小辺数は **`floor((3n−5)/2)`** である。

葉の支持点の次数を `2k+1`、その閉近傍外の誘導辺数を `e` とすると、近傍マッチングと閉近傍外の各点の一意な接続から `m=n+k−1+e`。葉は高々3個で、そのうち支持点の葉1個を除き、閉近傍外の辺に接しない点も葉だから `n−2k−2−2e≤2`。従って `2m≥3n−6`。既存の偶奇別構成は葉を持ち、整数下界 `floor((3n−5)/2)` を達成する。

よって、この数より少ない辺のC4飽和グラフが存在するとすれば、それは葉を持たない。これは葉なし候補の存在・不存在を決めるものではない。

例えば11頂点13辺の候補は葉を持ちえない。全候補を扱う固定辺SAT符号化の50万衝突試行はUNKNOWNだったが、その後の葉なし候補の構造縮約と有限検査で、一般の場合も14辺が最小と決まった（K0743）。

独立検算として `n=4..6` の全部分グラフで葉を持つ飽和例の下界を確かめ、`n=5..20` で構成の葉・辺数・全欠辺追加を直接検査した。奇数次元構成の旧監査文にある「5頂点の構成はC5」という説明は誤りで、実際は三角形に2葉を付けたグラフである。
