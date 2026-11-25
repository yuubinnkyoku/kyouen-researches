# 純三点禁止・六点の完全Grundy分類

2026-11-07の一次資料。現在の知識はK0686。

```sh
uv run --locked python research/experiments/pure-triple-maximum-grundy-six-20261107/audit.py
```

Python標準ライブラリとC++17のg++を使う。コンパイル生成物・全根値列は専用の一時ディレクトリに作り、
PythonとC++の全1048576個の根値をbyte単位で比較する。

* `scan.py`: 既証明の五点核表を用いる初手分解。
* `independent.cpp`: 全占有subsetだけを使う別アルゴリズム。
* `audit.py`: 全件比較、六軌道、最小点数、具体幾何証人の監査。
* `proof.md`: 完全分類の根拠と範囲。
* `output/`: 決定的な全数集計と座標証人。
