# 三次元の平行格子列とq点超平面・超球面ゲーム

この実験は二次元固定幅定理の三次元への適用境界を調べる。
現在の結論は対応するknowledge項目に置き、ここには証明・再現物を保存する。

- [proof.md](proof.md): 全称証明、ルール、二次元との差、検証範囲。
- [verify.py](verify.py): 占有数DPと独立の有理数lifted-rank subset DP。
- [output.json](output.json): 再現可能な有限検算。
- [odd-root-proof.md](odd-root-proof.md): 奇数列の長盤空盤mod4則と奇数rの全Grundy公式。
- [odd_root_verify.py](odd_root_verify.py): 独立のラベル付きmexとgapゲーム全検算。
- [odd-root-output.json](odd-root-output.json): 続編の実行済み検算。

repo rootで実行:

```sh
python research/experiments/prism-hyperplane-2026-10-05/verify.py
python research/experiments/prism-hyperplane-2026-10-05/odd_root_verify.py
```

標準ライブラリのみ。出力はこの実験のoutput.jsonに保存する。
長時間の未知盤探索や11×11の勝敗判定は行わない。
