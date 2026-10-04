# 三次整数曲線と反転による故障耐性の無界族

現在の正本はK0346。[proof.md](proof.md)に全rの構成・安全性・極大性・
故障耐性と全Grundyの数学的証明を保存する。

```sh
python research/experiments/geometry-frontier-followup-20261005/verify_cubic_fault_family.py
```

[verify_cubic_fault_family.py](verify_cubic_fault_family.py)は既存整数幾何coreと
別のgeneric Leibniz行列式、削除集合、全安全集合mexを検査する。
三次恒等式は有限代入に加え、整数多項式環の全係数展開でも照合する。
[audit.json](audit.json)に各範囲の入力・全状態数・整数座標・解除証人を保存する。

点盤は構成した有限整数点集合だけである。包含する全格子正方形盤の極大性を
主張しないため、K0328はOPENのまま。有限計算を無界証明の代わりにはしない。
