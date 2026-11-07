# rank3残余族の普遍的整数共円実現

2026-11-07の実験一次資料。現在の命題はK0683に置く。

* `proof.md`: 任意の二点・三点禁止族の全状態実現、ビット長、rank4での不可能性。
* `verify.py`: 将来の三点円も避ける有限除外構成と独立整数四点監査。
* `output/audit.json`: 130整数盤の全座標・全意図した四点組・検査集計。

```sh
uv run --locked python research/experiments/rank-three-residual-universality-20261107/verify.py
```

標準ライブラリと、既存K0681構成の有理円ヘルパーを使う。
独立監査は別の整数4×4行列式。有限検査と一般構成証明を区別する。
