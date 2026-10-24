# 有理二線型の全実数第三線被覆を有限認証

[証明と範囲](proof.md)。九段{0,...,8}からの外線5点二組・全8001型について、
任意の線間距離・第三線位置・安全な高々四石が禁止する空点は高々8個と認証する。
全実数の外線高さB,Cへの外挿や、ゲームの一様閾値改善は行わない。

```sh
uv run --locked python research/experiments/q6-rational-third-line-blockers-20261024/generate.py
uv run --locked python research/experiments/q6-rational-third-line-blockers-20261024/check.py
```

* 生成器：三円Cramer計算、判別式の整数平方判定、全有理根グラフ。
* 独立検査器：三元Gaussian消去、全特異組の実数排除、二次式の根軸による高次数頂点。
* `certificate.json`：全8001型と全11624個の正のパラメータ・上界。
* `audit.json`：全558238三円組の分類、全被覆上界、3種類の改変拒否。

どちらも標準ライブラリの整数・Fractionだけを使う。浮動小数点・外部ライブラリ・未知盤探索は使用しない。
