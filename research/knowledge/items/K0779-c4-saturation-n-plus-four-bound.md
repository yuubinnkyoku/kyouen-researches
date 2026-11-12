---
id: K0779
title: C4飽和グラフはn>=13でn+4辺以上、重み2層の14次元最小値は18
kind: proposition
status: proved
topics: [variants, geometry, maximal-safe]
aliases: []
relations:
- type: depends_on
  target: K0715
  note: 重み2層のC4対応と偶数次元の構成
- type: depends_on
  target: K0742
  note: 葉を持つ候補の辺数下界
- type: depends_on
  target: K0744
  note: n>=11のn+3下界
- type: depends_on
  target: K0777
  note: 13頂点16辺の有限核排除
artifacts:
- path: research/experiments/binary-cube-coplanar-midpoint-theorem-20261109/tetracyclic-general-lower-bound.md
  role: proof
  note: 四重閉路核の14頂点への縮約と細分による直径単調性
- path: research/experiments/binary-cube-coplanar-midpoint-theorem-20261109/enumerate_tetracyclic_cores.cpp
  role: verifier
  note: 核を同型類ごとに生成し単純展開可能な道長を列挙
- path: research/experiments/binary-cube-coplanar-midpoint-theorem-20261109/tetracyclic-n14-candidates.txt.gz
  role: data
  note: 14頂点109249候補の核と道長
- path: research/experiments/binary-cube-coplanar-midpoint-theorem-20261109/audit_tetracyclic_cores.py
  role: verifier
  note: 独立な核・道長生成と四角形マスクによる候補の網羅性・判定照合
- path: research/experiments/binary-cube-coplanar-midpoint-theorem-20261109/tetracyclic-n14-audit.json
  role: data
  note: 候補数・核被覆・C4禁止候補数の照合結果
- path: research/experiments/binary-cube-coplanar-midpoint-theorem-20261109/audit_tetracyclic_diameter14.py
  role: verifier
  note: 3段階到達集合と長さ3以下の道による2方式の直径下界検査
- path: research/experiments/binary-cube-coplanar-midpoint-theorem-20261109/tetracyclic-n14-diameter-audit.json
  role: data
  note: 全109249候補の直径4以上を確認
- path: research/experiments/binary-cube-coplanar-midpoint-theorem-20261109/weight-two-even-dimension-improved-saturation-20261110.md
  role: certificate
  note: 14頂点18辺の明示構成
scope: n>=13頂点のC4飽和単純グラフと、二値立方体重み2層の包含極大配置。有限核検査に依存し、正方形格子や一般次元の厳密値は含まない。
evidence: 葉あり候補の辺数下界、四重閉路核の14頂点への縮約、14頂点109249候補の2種類の直径下界検査。n=13はK0777の有限核検査。
---

# C4飽和数の n+4 下界

`n≥13` の C4 飽和単純グラフは少なくとも **`n+4` 辺**を持つ。既存の偶数次元構成は14頂点18辺を与えるので、二値立方体の重み2層の最小極大配置は **`s_14^(2)=18`**。

`n+3` 辺候補はK0742の葉を持つ場合の下界により葉がなく、連結性から最小次数2以上。次数超過和6により、次数2の道を縮約した核の分岐頂点は1〜6個、核の辺数はその頂点数より3多い。ループと平行辺を含めて、単純性を保つ道長の下限和は高々17である。このため `n≥14` の候補は14頂点17辺の候補から辺の細分で得られる。

14頂点の場合、核と道長の全109249ケースで距離4以上の頂点対が見つかった。候補生成を別実装で照合し、各候補の直径下界も到達集合と長さ3以下の道の2方式で検査した。細分は元の頂点間距離を縮めない一方、C4飽和グラフの直径は高々3なので矛盾する。13頂点16辺はK0777で別途排除済み。

全称的な縮約と有限核の検査を組み合わせた結果であり、全数検査には保存した候補データを用いる。一般次元でこの下界が常に鋭いとは主張しない。
