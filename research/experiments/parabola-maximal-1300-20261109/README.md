# 保存1300点集合の包含極大性

厳密な命題は[K0715](../../knowledge/items/K0715-p2647-saved-1300-witness-inclusion-maximal.md)を参照する。
現在の最大安全サイズの境界とは別に、保存した1300点集合へ1点も追加できないことを証明する。

`output/initial/blockers.txt` は先頭に `2647 1347`、以後は
`追加t q0 q1 q2 q3` の行を補集合の全点について持つ。
各四点はtと既存集合の3点からなり、正確な整数行列式が0である。

`audit.py` は非空対には二完全対の四点を提案し、空対25の50側には既存の直接投影CNFを候補生成に使う。
`verify_blockers.cpp` はCNF・SATソルバを使わず、明示四点の範囲・所属・相異性・整数幾何と
未選択1347点の完全被覆だけを検査する。既存verify_subset.cppのgeneric行列式をそのまま利用する。
元集合の安全性は、その同じinput hashに結び付いた独立幾何receiptから確認する。
両者が揃うので包含極大となる。最大サイズが1300という主張ではない。

再現は新しい出力先を指定する:

```sh
uv run --locked python research/experiments/parabola-maximal-1300-20261109/audit.py --output FRESH-blocker-audit
```

実行時に正例1347行の受理と7不正制御の拒否も確認する。
生成処理は保存証人の評価であり、新しいSAT探索や大きい四点全数検査は起動しない。
