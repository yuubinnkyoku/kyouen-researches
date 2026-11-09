# 空対を許した点選択と1296点証人

固定原点・完全対d=1323のもとで、残り各対を低側・高側・空対から選ぶ。
元の等号CNFの各節を点選択の否定節へ変換し、空対の総数を制約する。
厳密な命題と全称証明は [K0712](../../knowledge/items/K0712-parabola-empty-pair-ternary-sat-reduction.md)、
現在の数値境界は [K0711](../../knowledge/items/K0711-p2647-safe-lower-bound-1292.md) を参照する。
一般の二値同値CNFへ簡約した後の変換は正しくない場合があるため、禁止四点の直接投影節を使う。

## 保存した2試行

| 出力ディレクトリ | 要求点数 | 空対上限 | 結果 |
|---|---:|---:|---|
| `output/target1300-budget100000` | 1300以上 | 25 | 壁時計60秒でUNKNOWN、モデルなし |
| `output/target1293-budget100000` | 1293以上 | 32 | SAT、空対29・1296点を構成 |
| `output/target1322-budget100000` | 1322以上 | 3 | 衝突予算100000を使い切りUNKNOWN（solve 14.3秒、モデルなし） |

いずれもconflict budgetは100000、Python-SAT 1.9.dev21のCadical195。
1292点の既存証人からphaseを設定したが、点を固定するassumptionは置いていない。
SAT試行は142992節・45249変数、solve 11.233秒（入力構築を含む親14.164秒）。
1300点試行のUNKNOWNは不存在の証明ではない。

各試行の `input.cnf.gz` は実際のCNFを保存し、`init.json` に展開後SHA-256、
元CNF・起点証人・workerソースのSHA-256と依存版を記録する。
`run.json` は壁時計上限を持つ親の記録。UNKNOWNでは `result.json` がない。
SAT側には全変数の `model.json`、選択結果 `result.json`、パラメータ `candidate.txt` がある。
`geometry.json` は探索コードを使わないgeneric整数4×4検査器の別の受理記録。

## 1296点の検査

保存CNFを再生成して実入力とbyte単位で照合し、保存モデルで全142992節の充足を確認した。
選択点数1296・空対29を直接数え、原点と固定完全対を含むことを確認した。
独立整数幾何検査では、全117002820060四点を必要合同式と44277012候補の行列式検査で被覆し、
禁止四点0件だった（28.903秒）。ソルバのSAT主張、モデルの全節検査、幾何安全性を区別する。

元入力は前の実験の保存CNF:
`../parabola-cnf-deletion-distance-20261109/output/rc2-p2647-d1323-20261108T184724Z.cnf`。
起点は前の1292点証人であり、いずれも内容hashを検査する。
点削除を直接最適化する今回の目的は、前の元CNFの違反節数の最小化とは異なる。

## 再現

repo rootから、探索を再実行せずに符号化と保存証拠を検査:

```sh
uv run --locked --with python-sat==1.9.dev21 python research/experiments/parabola-ternary-selection-20261109/regression.py
```

p=5,7,11,13,17の19392三値割当、444 cardinalityケース、無効one-hot、
任意の二値簡約の反例、起点1292点と現在の1296点の実入力・モデル・幾何receiptを照合する。
大きな点集合の幾何検査を再実行する場合:

```sh
uv run --locked python research/experiments/parabola-local-repair-20261109/verify.py --audit research/experiments/parabola-ternary-selection-20261109/output/target1293-budget100000/candidate.txt --receipt D:/tmp/parabola-1296-reproduction.json
```

探索自体の再現は、同じ予算の自動再試行にせず、明示的に新しい出力先を選ぶ:

```sh
uv run --locked --with python-sat==1.9.dev21 python research/experiments/parabola-ternary-selection-20261109/run.py --target 1293 --budget 100000 --timeout 60 --output research/experiments/parabola-ternary-selection-20261109/output/reproduction
```

入力生成は原点と完全対を固定した部分族を扱う。仮にこのCNFでUNSATが出ても、
他のd・原点のない形・完全対のない形を含む全Q_pの上界にはそのまま拡張しない。
正確値・最適性・他素数への一般化は未確定。
