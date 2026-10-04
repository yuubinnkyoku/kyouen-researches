# 残余hypergraphの双子偶奇圧縮

同一の全hypergraph linkを持つ点を、奇数classなら一つ、偶数classなら二つへ
減らしてもGrundy数が一致する全称定理と、格子終盤での独立検査。
現在の結論は [K0336](../../knowledge/items/K0336-independent-residual-twins-parity-compression.md)、
証明・標本選択・限界は [report](reports/twin-parity.md) を参照。
11×11空盤の勝敗はUNKNOWN。実df-pn速度改善は未測定。

```sh
g++ -std=c++17 -O3 -Wall -Wextra -Wpedantic \
  research/experiments/n11-residual-twins/scripts/sample_residual_twins.cpp \
  -o /tmp/sample_residual_twins
/tmp/sample_residual_twins 200 \
  > research/experiments/n11-residual-twins/output/geometry-samples.json
python research/experiments/n11-residual-twins/scripts/verify_twins.py
```

標本生成は共有128-bit geometry、証人監査はPython整数行列式・共有最小R core、
mex確認は残余更新と直接占有subsetの別定式化を使う。追加パッケージは不要。
