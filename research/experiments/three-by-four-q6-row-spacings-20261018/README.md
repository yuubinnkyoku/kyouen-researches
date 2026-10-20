# 3×4・q=6・非等間隔行の完全分類

水平方向の列 `0,1,2,3` を共有する3行を `y=0,a,a+b`（`a,b>0`）とした共円ゲームの禁止集合と全安全局面Grundyを分類。

- `proof.md`: 全実数間隔の代数証明と75型の完全mex表
- `verify.py`, `audit-python.json`: 有理数行列式、4096局面mex、群占有数による独立照合
- `verify_independent.cpp`, `audit-cpp.txt`: 整数行列式＋反復mexの独立実装

再現（リポジトリ根から）：

```sh
python research/experiments/three-by-four-q6-row-spacings-20261018/verify.py
c++ -std=c++17 -O2 research/experiments/three-by-four-q6-row-spacings-20261018/verify_independent.cpp -o /tmp/q6_3x4
/tmp/q6_3x4
```

本結果は標準整数格子の固定幅安定化長 `M_{3,6}=9` の変更ではない。行ごとの横座標を自由に動かした場合は未分類。
