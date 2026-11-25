# 二平行線・各5点以下の一点共通円は高々4本、かつ鋭い

同和弦energyに条件を置かない[全称証明](proof.md)。
五円の共有点配置は二つのC5となり、二つの三次式から黄金比型へ帰着する。
要求される線間距離の二乗が負になるため五円を排除する。
四円は線間隔10・全点整数座標の明示例で実現し、別にenergy6・線間隔√71の例もある。
共有接続の整数上界と組み合わせ、各線2〜5点の全16サイズの最大円数も鋭く分類する。

```sh
uv run --locked python research/experiments/two-parallel-five-point-concurrency-20261024/verify.py
g++ -std=c++17 -O2 research/experiments/two-parallel-five-point-concurrency-20261024/witness.cpp -o /tmp/q6-four-witness
/tmp/q6-four-witness
```

`audit.json` は16個の多項式恒等式・改変拒否・9円中4円および6円中4円の明示証人の検査結果。
同じ整数5点×5点例の全676部分集合対から、全16サイズの達成例も収録する。
検査器はSymPyや浮動小数点を使用しない。バイナリはリポジトリ外に置く。
