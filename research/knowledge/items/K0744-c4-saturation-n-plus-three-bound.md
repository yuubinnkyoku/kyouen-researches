---
id: K0744
title: C4飽和グラフはn>=11でn+3辺以上、重み2層の12次元最小値は15
kind: proposition
status: proved
topics: [variants, geometry, maximal-safe]
aliases: []
relations:
- type: depends_on
  target: K0715
  note: n+2下界と重み2層のC4対応、偶数次元の構成
- type: depends_on
  target: K0742
  note: 葉を持つ候補の辺数下界
- type: depends_on
  target: K0743
  note: 11頂点13辺の有限核排除と三重閉路核の構造
artifacts:
- path: research/experiments/binary-cube-coplanar-midpoint-theorem-20261109/tricyclic-general-lower-bound.md
  role: proof
  note: 三重閉路核の12頂点への縮約と細分による直径単調性
- path: research/experiments/binary-cube-coplanar-midpoint-theorem-20261109/audit_tricyclic_diameters.py
  role: verifier
  note: 12頂点の核・道長18334ケースをFloyd-Warshall法で検査
- path: research/experiments/binary-cube-coplanar-midpoint-theorem-20261109/verify_tricyclic_diameters.py
  role: verifier
  note: 同じ全ケースの直径分布を幅優先探索で照合
- path: research/experiments/binary-cube-coplanar-midpoint-theorem-20261109/tricyclic-diameter-audit.json
  role: data
  note: 12頂点の直径分布と13頂点からの縮約可能性の有限検算
- path: research/experiments/binary-cube-coplanar-midpoint-theorem-20261109/tricyclic-n12-result.json
  role: data
  note: 12頂点14辺のC4飽和候補の核・道長列挙結果
- path: research/experiments/binary-cube-coplanar-midpoint-theorem-20261109/weight-two-even-dimension-improved-saturation-20261110.md
  role: certificate
  note: 12頂点15辺の明示構成
scope: n>=11頂点のC4飽和単純グラフと、二値立方体重み2層の包含極大配置。有限核検査に依存し、正方形格子や一般次元の厳密値は含まない。
evidence: 葉あり候補の辺数下界、三重閉路核の12頂点への縮約、12頂点18334候補の2種類の直径計算。n=11はK0743の有限核検査。
---

# C4飽和数の n+3 下界

`n≥11` の C4 飽和単純グラフは少なくとも **`n+3` 辺**を持つ。既存の偶数次元構成は12頂点15辺を与えるので、二値立方体の重み2層の最小極大配置は **`s_12^(2)=15`**。

`n+2` 辺候補はK0742の葉を持つ場合の下界により葉がなく、連結性から最小次数2以上。次数超過和4により、次数2の道を縮約した核の分岐頂点は1〜4個、核の辺数はその頂点数より2多い。ループと平行辺も含む全核について、単純性を保つ道長の下限和は高々12である。このため `n≥12` の候補は12頂点14辺の候補から辺の細分で得られる。

12頂点の場合、核と道長の全18334ケースで直径は4以上だった。Floyd-Warshall法と幅優先探索が直径分布でも一致した。細分は元の頂点間距離を縮めない一方、C4飽和グラフの直径は高々3なので矛盾する。11頂点13辺はK0743で別途排除済み。

全称的な縮約と有限核の検査を組み合わせた結果であり、両直径検査は候補生成器を共有する。一般次元でこの下界が常に鋭いとは主張しない。
