# 木の三点辺の周期的効果と整数幾何実現

2026-11-07の研究記録。現在の知識は
[K0680（全長周期分類）](../../knowledge/items/K0680-tree-triple-broom-grundy-periodicity.md)と
[K0681（整数幾何実現）](../../knowledge/items/K0681-graph-plus-independent-triple-geometric-realization.md)を参照。

* `proof.md`: 箒木の正確なmex再帰、有限窓からの全称周期証明、非局所性の系。
* `geometry.md`: 任意グラフ＋一つの独立三点辺の有限整数点盤への全状態実現。
* `verify_period.py`: 周期の有限証明書と別の占有subsetゲーム・閉近傍ゲームとの照合。
* `verify_geometry.py`: 有理円構成と別の整数4×4行列式・全安全局面の監査。
* `output/`: 整数の有限証明書と座標証人。

repo rootから実行する（どちらも標準ライブラリのみ）：

```sh
uv run --locked python research/experiments/tree-triple-broom-periodicity-20261107/verify_period.py
uv run --locked python research/experiments/tree-triple-broom-periodicity-20261107/verify_geometry.py
```

既知の道の周期性そのものを新規成果とは扱わない。
箒の三点制約付きゲームは、全長への帰納証明と有限証明書の組合せで扱う。
正方形全格子盤や11×11空盤の勝敗への主張は含まない。
