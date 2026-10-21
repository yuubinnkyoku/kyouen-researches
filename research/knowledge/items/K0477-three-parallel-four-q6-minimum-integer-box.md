---
id: K0477
title: 3整数水平行・各4点の6点円3本を実現する最小包囲格子は7×4
kind: proposition
status: proved
topics:
- geometry
- variants
aliases: []
relations: []
artifacts:
- path: research/experiments/geometry/reports/three-parallel-four-q6-minimum-integer-box-20261018.md
  role: proof
  note: 有限帰着・全列挙の監査範囲・7×4の明示構成と円の完全性
- path: research/experiments/geometry/scripts/three_parallel_four_q6_minbox_primary.cpp
  role: verifier
  note: 二点和・二点積による有限完全列挙
- path: research/experiments/geometry/scripts/three_parallel_four_q6_minbox_independent.cpp
  role: verifier
  note: 独立した整数行列式による有限完全列挙
- path: research/experiments/geometry/output/three_parallel_four_q6_minbox_counts.txt
  role: data
  note: 二方式で一致した全5長方形の完全集計と全達成配置
- path: research/experiments/knowledge-audit-20261021/README.md
  role: log
  note: 証明の論理監査・再実行範囲・判定
scope: 相異なる3本の整数水平行に各4個の相異なる整数格子点を置く12点集合。非退化実円の6点共円を数える。包囲格子の面積WHを最小化。
evidence: '2026-10-21監査。面積28以下の候補長方形の完全被覆を確認。独立2方式の全2186661配置を再走査し文字単位で一致。 監査記録: research/experiments/knowledge-audit-20261021/README.md。'
---


# 最小包囲格子面積は28

3本の相異なる整数水平行に各4個の整数格子点を選ぶとき、6点を通る円が3本存在する配置の包囲格子面積 `WH` の最小値は28。等号は `W=7,H=4` に限られ、平行移動正規化後の達成配置は4個、すべて左右・上下反射で同値。

具体例は `y=0: {0,3,4,5}`, `y=1: {0,2,5,6}`, `y=3: {2,3,4,6}`。6点円は `x²+y²−8x−4y+15=0`, `x²+y²−7x−3y+12=0`, `x²+y²−5x−y=0` のちょうど3本。各行の二点和の共通部分が `{5,7,8}` で、各和につき各行の点対がただ一組なので、これ以外の6点円はない。

面積28未満の任意の包囲格子は `9×3`, `6×4`, `5×5`, `4×7` のいずれかに含まれる。各長方形について `C(H,3)C(W,4)^3` 配置を漏れなく調べ、3円配置が0個と独立に確認した。面積28で残る `7×4` には4配置、`4×7` には0配置。数学的な有限帰着と整数完全列挙による計算機援用証明であり、無限探索の外挿ではない。

この主張は整数水平行・整数横座標に限定される。任意実数座標・傾いた平行線には拡張しない。達成例上の通常プレイの空盤Grundy値は0（12点の有限完全列挙）だが、これは全整数配置の勝敗を分類したものではない。
