# 純三点七辺の全核計算

全六辺核4279型からの完全辺追加生成を、独立母関数の辺ラベル付き署名総数で監査する。
生成器は六辺実験のgenerate.cppをEDGE_COUNT=7でコンパイルする。
全ゲーム値をcell占有数のC++再帰と、別C++の生占有subset DPで比較し、さらにPython標本を確認する。

```sh
uv run --locked python research/experiments/pure-triple-seven-edge-complete-20261108/audit.py
```

全53,340型の計算が完了し、独立総数193,926,796とも一致した。
通常値は核で8以下、g8核は十一点の一型のみ。任意自由点込みでg≤9が鋭い。
`misere.py`では自由点両偶奇106,680根の通常値・終局1補助値を二実装で全件照合し、h≤9も鋭い。
hはxorではなく自由点二個周期で任意点数へ帰着する。
[証明・全称範囲](proof.md)、通常全表`output/audit.json`、補助値全配列`output/misere.json`を保存した。
現行結論はK0687とK0699に記録する。
