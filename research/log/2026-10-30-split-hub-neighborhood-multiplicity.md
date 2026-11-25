# 2026-10-30: 同一近傍の特別中心の個数圧縮

作業開始時に最新 `main`（開始時 `be7f326`）、`AGENTS.md`、`research/knowledge/README.md`、`research/knowledge/generated/summary.md`、直前の `split-marked-hub-subset-polynomial-dp-20261030` と `split-marked-hub-terminal-law-20261030` を確認した。固定幅の既知の真の閾値（3×m q=5, q=4、4×m q=8）との重複を避けた。

前回の未解決点「特別中心数 $k$ に対する指数依存」のうち、同じ独立点側近傍を持つ中心が多数ある場合を解決した。中心を近傍の種類 $r$ 個にまとめ、各種類の最小優先順位の密度 $c_i(1-u)^{c_i-1}$ を使うことで、中心数 $k$ に対する $2^k$ 再帰を種類数 $r$ に対する $2^r$ 再帰へ置き換えた。種類ごとの選択確率、指定された一中心の選択確率、終局長の完全分布を厳密に求める全称公式を証明。

別方式の検証器は実際に全中心を展開したグラフの閉近傍削除による有理数再帰。小構成からの固定乱数抽出280件、追加乱数79件、指定例3件を全照合し、不一致0。$c=7$ の同一近傍の中心と2独立点の例で中心選択確率 $7/9$（無重み縮約では $1/3$）を確認。これは確率計算の重み付き縮約であり、既存のGrundy用双子縮約と混同しない。

一次資料：[定理・証明](../experiments/game-structure/split-hub-neighborhood-multiplicity-20261030/README.md)、[独立検証器](../experiments/game-structure/split-hub-neighborhood-multiplicity-20261030/verify.py)。

残る問題：異なる近傍種類数 $r$ が大きい場合の指数依存、整数格子の共円ゲーム残局としての実現性、実盤面での圧縮効果。11×11 root探索は実行していない。全称性は数学的証明による。knowledge正本への昇格・生成索引再構築・全体CIは未実施。
