# 偶数ペア容量の三次元列ゲーム: 任意長の全Grundy

対象はK0340の奇数列数w≥3の占有ゲーム。偶数r=q−1と任意列長m≥1について、
最大列a・二番目b・残り総数の偶奇から全Grundyを閉公式にした。
現在の正本は [K0345](../../knowledge/items/K0345-even-capacity-odd-column-prism-all-lengths-grundy.md)。

- `even-capacity-proof.md`: 任意w,r,mの全称mex証明。空盤の真の安定化長rと、
  幾何条件下での全Grundy最大値1/3の境界も含む。
- `even_capacity_verify.py`: 全列対を直接判定する独立ラベル付きmex、既存ソート
  占有数DPとの照合、適用外反例と短盤補正の検査。
- `even-capacity-output.json`: 上記の再現出力。各有限範囲の完了全状態検算。

```sh
python research/experiments/prism-followup-20261005/even_capacity_verify.py
```

追加依存はなくPython標準ライブラリと既存実験の共通占有数DPを使う。
assertを有効にするためPythonの`-O`は使わない。
全称結果の根拠はmex証明であり、有限表を全称定理として扱わない。
標準二次元盤のGrundy上限や11×11勝敗は扱わない。
