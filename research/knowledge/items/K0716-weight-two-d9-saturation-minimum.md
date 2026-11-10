---
id: K0716
title: 二値立方体重み2層の9次元最小極大配置は11石
kind: computation
status: computed
topics: [variants, geometry, maximal-safe]
aliases: []
relations:
- type: depends_on
  target: K0715
  note: 重み2層のC4対応、9次元の10石下界と11石構成
artifacts:
- path: research/experiments/binary-cube-coplanar-midpoint-theorem-20261109/enumerate_sparse_c4.cpp
  role: verifier
  note: 隣接ビット集合によるC4生成判定と安全な辺集合の再帰列挙
- path: research/experiments/binary-cube-coplanar-midpoint-theorem-20261109/enumerate_sparse_masks.cpp
  role: verifier
  note: 四角形ビットマスクと固定サイズ部分集合走査による独立列挙
- path: research/experiments/binary-cube-coplanar-midpoint-theorem-20261109/sparse-c4-enumeration.json
  role: data
  note: 2実装で一致した安全配置と極大配置の集計・ソースhash
- path: research/experiments/binary-cube-coplanar-midpoint-theorem-20261109/weight-two-odd-dimension-improved-saturation-20261110.md
  role: certificate
  note: 9次元11辺の包含極大C4禁止構成
scope: 二値立方体の重み2層、共面四点禁止、9次元の包含極大安全配置の最小サイズ。有限計算に依存し、全立方体や正方形格子には適用しない。
evidence: 固定辺を含む全70607460個の10辺グラフを異なる2実装で列挙し、14113575個のC4禁止グラフに極大なものがないことを照合。別途11辺の明示構成と10辺の理論下界を使用。
---

# 9次元重み2層の最小極大配置

二値立方体 `{0,1}^9` の重み2頂点のみを使い、共面四点を禁止すると、包含極大な安全配置の最小サイズは **11石**。これは有限全数列挙に依存する結論である。

K0715の下界により、極大配置には少なくとも10石が必要。11石の明示構成がある。そこで10辺のグラフを調べる。どの10辺グラフも頂点を付け替えて辺 `{0,1}` を含められるため、これを固定した `binom(35,9)=70607460` 候補の検査で不存在を判定できる。

隣接集合からC4を判定する再帰列挙と、固定サイズの部分集合を走査して四角形マスクを照合する別実装は、それぞれC4を含まない候補14113575個、極大候補0個と一致した。後者は全候補数も直接検査する。したがって10石の極大配置は存在せず、11石が最小である。

両実装は5次元5辺、6次元6辺、7次元8辺、8次元9辺でも一致し、先行する5〜7次元の全列挙結果と整合する。8次元9辺では固定辺を含む極大配置が3240個。ラベル付き配置を「配置に含まれる辺」で二重計数すると、総数は `3240·binom(8,2)/9=10080` 個である。

再現は各C++ソースを `g++ -std=c++17 -O3` でコンパイルし、実行ファイルに `9 10` を渡す。マスク版は高速化のため実行環境が対応する場合に `-mpopcnt` を追加できる。通常プレイ・misèreの勝敗や、他の次元の最小値はこの列挙からは決まらない。
