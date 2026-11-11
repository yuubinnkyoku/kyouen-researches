---
id: K0717
title: 二値立方体重み2層の10次元最小極大配置は12石
kind: computation
status: computed
topics: [variants, geometry, maximal-safe]
aliases: []
relations:
- type: depends_on
  target: K0715
  note: 重み2層のC4対応、10次元の11石下界と12石構成
artifacts:
- path: research/experiments/binary-cube-coplanar-midpoint-theorem-20261109/search_sparse_c4_n10.cpp
  role: verifier
  note: 連結可能性で枝刈りする固定辺・11辺の安全配置列挙
- path: research/experiments/binary-cube-coplanar-midpoint-theorem-20261109/enumerate_sparse_unpruned_n10.cpp
  role: verifier
  note: 連結性枝刈りなしの再列挙。C4判定は共有する
- path: research/experiments/binary-cube-coplanar-midpoint-theorem-20261109/enumerate_sparse_masks_n10.cpp
  role: verifier
  note: 別の四角形マスク方式による全固定辺候補の独立列挙
- path: research/experiments/binary-cube-coplanar-midpoint-theorem-20261109/audit_c4_enumerators.py
  role: verifier
  note: 隣接集合方式と四角形マスク方式の小次元・各辺数の差分照合
- path: research/experiments/binary-cube-coplanar-midpoint-theorem-20261109/c4-enumerator-small-audit.json
  role: data
  note: 次元4..6の各辺数と次元7の既知ケース計94442候補の照合
- path: research/experiments/binary-cube-coplanar-midpoint-theorem-20261109/d10-eleven-edge-enumeration.json
  role: data
  note: 2回の列挙の集計、検査器のhashと証拠上の制約
- path: research/experiments/binary-cube-coplanar-midpoint-theorem-20261109/saturation_sat.py
  role: verifier
  note: 四角形禁止・欠辺ごとの長さ3の道・辺数を用いる別のSAT符号化
- path: research/experiments/binary-cube-coplanar-midpoint-theorem-20261109/audit_saturation_sat.py
  role: verifier
  note: n=4..6の固定辺を含む全小グラフとSAT符号化の照合
- path: research/experiments/binary-cube-coplanar-midpoint-theorem-20261109/saturation-sat-small-audit.json
  role: data
  note: 小グラフ16925件について直接検査とSATの一致
- path: research/experiments/binary-cube-coplanar-midpoint-theorem-20261109/d10-c4-saturation-sat-20261110/result.json
  role: data
  note: 別SAT符号化の30万衝突探索はUNKNOWN
- path: research/experiments/binary-cube-coplanar-midpoint-theorem-20261109/d10-c4-saturation-sat-20261110/input.cnf.gz
  role: data
  note: 上記試行の固定辺・11辺のCNF
- path: research/experiments/binary-cube-coplanar-midpoint-theorem-20261109/d10-c4-saturation-sat-2m-20261110/result.json
  role: data
  note: 同一CNFの200万衝突探索もUNKNOWN
- path: research/experiments/binary-cube-coplanar-midpoint-theorem-20261109/weight-two-even-dimension-improved-saturation-20261110.md
  role: certificate
  note: 10次元12辺の包含極大C4禁止構成
- path: research/log/2026-11-11-c4-saturated-ten-eleven-bicyclic-diameter-exclusion.md
  role: source
  note: 二重閉路21核の直径計算。葉あり候補を除外する部分は誤った補題に依存
- path: research/log/2026-11-12-c4-three-leaf-false-lemma-counterexample.md
  role: source
  note: 葉なし補題の根拠となった3葉補題への反例
- path: research/experiments/binary-cube-coplanar-midpoint-theorem-20261109/audit_bicyclic_diameters.py
  role: verifier
  note: 基礎21核の直径をFloyd-Warshall法で独立照合
scope: 二値立方体の重み2層、共面四点禁止、10次元の包含極大安全配置の最小サイズ。有限計算に依存し、全立方体や正方形格子には適用しない。
evidence: 固定辺を含む11辺グラフの隣接集合による列挙と、全2481256778候補を走査する四角形マスク方式が、安全配置506030448個と極大配置0件で一致。SATによる独立証明は未完了。
---

# 10次元重み2層の最小極大配置

二値立方体 `{0,1}^10` の重み2層で、共面四点を禁止した場合の包含極大安全配置の最小サイズは、**有限全数列挙によれば12石**。

以前ここに記載した葉なし補題を使う構造的証明は、その根拠となる3葉補題に反例が見つかったため撤回する。10頂点の最小次数2以上という条件付きでは21核の直径はいずれも4以上と独立検算できるが、これだけでは葉を持つ候補を排除できない。以下の全数列挙は葉を持つ候補も対象としており、結論の根拠はこの有限計算と12辺構成である。

K0715の一般下界は11石、偶数次元の構成は12石を与える。11辺グラフは頂点の付け替えにより辺 `{0,1}` を含められるため、固定辺を含む `binom(44,10)=2481256778` 候補を対象にした。四角形を作る辺の追加を除外する再帰探索は、C4を含まない506030448配置のいずれも極大でないと判定した。連結可能性による枝刈りを追加した再実行でも、連結なC4禁止配置398428800個のうち極大なものは0個だった。よって同列挙が正しければ11石は不可能で、構成の12石が最小となる。

さらに、四角形ビットマスクを直接使う別実装で `binom(44,10)=2481256778` 候補を一つずつ走査し、安全配置506030448個、極大配置0個で隣接集合方式と一致した。両方式は `n=4..6` の各辺数と `n=7` の既知ケースでも照合済み。

**証拠の限界**：連結性枝刈りの有無を変えた2回の隣接集合探索はC4判定と極大性判定を共有する。四角形マスクによる独立走査も有限計算であり、一般次元の証明ではない。別途作成したSAT符号化は `n=4..6` の固定辺を含む全16925グラフで直接判定と一致したものの、10次元11辺の30万・200万衝突試行はいずれもUNKNOWN。SATの独立したUNSAT証明は得ていない。

再現は各C++ソースを `g++ -std=c++17 -O3` でコンパイルし、実行ファイルに `10 11` を渡す。隣接集合方式はC4を作る部分集合や連結不能な部分集合を枝刈りし、マスク方式は固定サイズの全候補を走査する。
