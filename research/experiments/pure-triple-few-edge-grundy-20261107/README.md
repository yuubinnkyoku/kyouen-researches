# 純三点辺h≤5の全署名型

2026-11-07の一次資料。現在の命題はK0687。

```sh
uv run --locked python research/experiments/pure-triple-few-edge-grundy-20261107/audit.py
```

Python標準ライブラリとC++17のg++を使う。主生成はVenn cellの行和3、
独立生成は辺の追加。主mexはcell占有数、別のC++は個別頂点subset。
全型を両生成法で集合一致させ、全527型の根値を個別照合する。
一時コンパイル生成物は専用temporary directoryだけに置く。

`proof.md`は頂点数無制限への帰着、`output/audit.json`は全署名型と度数・証人を保存する。
