# 共通pivotを加えた純四点Berge木liftの有限probe

K0689の八辺以下の全209連結純三点Berge木に、一つの新pivotを全辺へ追加した。
生成された純四点族をC++の生占有subset mexで計算した。
25824958安全状態の有限probeで、根値の最大観測値は3、値0は現れなかった。

[実行器](scan.py)、[全入力と結果](output/scan.json)を保存する。

```sh
uv run --locked python research/experiments/common-pivot-four-uniform-forest-lift-20261108/scan.py
```

九辺以上の上界、全rank四共通pivot族、独立実装による全値照合、
具体的整数座標への移送は未検証。この段階では新しい全称K項目にしていない。
