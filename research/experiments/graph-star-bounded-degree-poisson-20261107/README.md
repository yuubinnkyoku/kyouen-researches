# 有界次数グラフの普遍的な終局長分布

研究時点: 2026-11-07。現在の命題と範囲は [K0679](../../knowledge/items/K0679-bounded-degree-terminal-poisson-universality.md)。

* `proof.md`: 有限誤差評価、正則族の臨界尺度、隣接対による一次補正の全称証明。
* `verify.py`: 標準ライブラリのみの有限独立監査。長時間探索や外部 solver は使わない。
* `output/audit.json`: 厳密監査集計と明示的に区別した浮動小数点診断。

repo root から再現する：

```sh
uv run --locked python research/experiments/graph-star-bounded-degree-poisson-20261107/verify.py
```

有限監査では n=3..6 の全ラベル付きグラフのうち最小次数2以上を全数処理する。
定理の無限範囲は有限外挿ではなく `proof.md` の組合せ論的証明による。
