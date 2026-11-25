# 二最大値による全長Grundy縮約

現在の正本はK0347。数学的証明は[proof.md](proof.md)、独立監査は[audit.md](audit.md)。
有限検算は全称証明とは区別する。

```sh
python research/experiments/prism-two-maxima-20261005/verify.py
```

[kernel.py](kernel.py)は二変数のDAG再帰のみで表を構築する。
[verify.py](verify.py)は別のラベル付き全座標mexで、各手の全ペア制約を検査する。
全合法ベクトルが空盤から到達可能であることと、閉式の状態数を用いて
完了範囲を確認する。有限gapの補助ゲームも別DPで全範囲を検査する。
保存した[verified.json](verified.json)にはパラメータ・全状態数・値の分布を含む。

長さm、禁止数q、列数wを混同しない。三次元格子へ適用する場合は
K0340の幾何条件が必要であり、標準二次元盤の11×11勝敗の証拠にはならない。
