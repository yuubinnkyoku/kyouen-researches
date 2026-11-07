# 八点純三点族でGrundy 6を合成

seed20261108のC++ランダム探索で481番目に八点・六辺g=6を得た。
辺maskは `22,38,41,49,88,146`。自由点追加で九点g=7。
K0690の任意rank上界g≤μ−2と合わせ、両値の最少点数は8,9と確定する。
K0687により辺数六本も最少である。現在の正本はK0691。

## 証拠と再現

- [C++有界探索](random.cpp)、[出力](output/random_n8.json)
- [別Python計算と幾何監査](audit.py)、[整数座標・全初手値](output/witness_audit.json)
- [先行SMT合成](search.py)、[60秒timeout](output/n8_g6_eNone.json)

```sh
uv run --locked python research/experiments/pure-triple-grundy-synthesis-20261108/audit.py
```

上の検査にz3は不要。14点・15点の整数座標盤を構成し、全共円四点組が
指定した六辺だけであることと、全安全占有状態でゲーム値が一致することを確かめる。
C++探索を再現する場合はC++17でrandom.cppをコンパイルし、試行上限500000を
引数に与える。最初のg≥6発見で停止する。乱数生成器はstd::mt19937_64を使い、
標準配布への依存を避けてrng()%56で辺番号を選ぶ。

SMTは追加依存を本体lockに導入せず、次で再現できる。

```sh
uv run --locked --with z3-solver python research/experiments/pure-triple-grundy-synthesis-20261108/search.py
```

SMT結果unknownは不存在の証拠ではない。今回の最小値の証明はSAT/UNSAT判定ではなく、
独立検査できる達成例とK0690/K0687の下界を組み合わせたもの。
ソルバのtime limitはZ3の[公式Parameters](https://microsoft.github.io/z3guide/programming/Parameters/)
に従いミリ秒で設定した。世界初性、六辺族の最大値、全正方形格子盤の達成は未主張。

`random_larger.cpp`の十点500000標本は最大観測値7だった。
`output/random_n10.json`を保存し、その達成例はaudit.pyで別Python計算も行う。
値8が十点で不可能という意味ではない。
