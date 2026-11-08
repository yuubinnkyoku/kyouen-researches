# 固定dのCNF節削除距離: RC2試行とモデル投影の回帰

p=2647, d=1323 の等号CNFを全節重み1のMaxSATとして一度だけ試した。
53,886節の入力作成後、壁時計60秒で **UNKNOWN**。モデルは得られず、
節削除距離、A(2647)の下界・正確値には進展なし。ソルバの未完了をUNSATと解釈しない。
現在の数学的・計算的結論は [K0706](../../knowledge/items/K0706-p2647-no-parabola-equality-witness.md) を参照する。

## 一次資料

`output/rc2-p2647-d1323-20261108T184724Z` を共通prefixとするファイル:

- `.cnf`: 固定した元の無重みCNF（1,323変数、53,886節）。変数dは不使用。
- `.init.json`: 入力、edge cache、encoderのSHA-256と依存版。
- `.run.json`: 実測60.056秒、UNKNOWN、モデルファイルなし。
- `.cleanup.json`: 終了後にこの試行の子プロセスが残らないことを確認した記録。

実際に使ったworkerは `initial_probe_worker.py` に保持した。
当初は親の `subprocess.run(..., timeout=60)` から起動した。
現在の `run_probe.py` はWindowsのvenvリダイレクタを避けてbase interpreterを直接起動し、
現在のworkerは保存CNFからも入力できる。実試行後の変更を当時の実行コードと混同しない。

CNF SHA-256: `0f09fc6efce1ba1b3df795eef24e4bb014fcfad836f31d4e6ba7e99b242ff0b3`。
外部のedge cacheがなくても同じ目的関数を再現できるよう入力CNFを保存した。
`--cnf`の場合は幾何学的安全性を判定しない。モデルが得られれば元の全節で違反数を再計算するが、
それは節削除距離の上界であり、RC2が返す最適性の独立証明ではない。
`--edges`の場合の検査も入力edge集合への依存があり、大素数の独立整数幾何検査とは区別する。

## 再現と次の手順

repo rootから、回帰のみ:

```sh
uv run --locked --with python-sat==1.9.dev21 python research/experiments/parabola-cnf-deletion-distance-20261109/test_projection.py
```

未完了試行を明示的に再開する場合のコマンド（自動再試行はしない）:

```sh
uv run --locked --with python-sat==1.9.dev21 python research/experiments/parabola-cnf-deletion-distance-20261109/run_probe.py --prime 2647 --double 1323 --cnf research/experiments/parabola-cnf-deletion-distance-20261109/output/rc2-p2647-d1323-20261108T184724Z.cnf --timeout 60
```

同じ予算の再実行を優先せず、保存CNFへの別方式または上界モデルの構成に具体的根拠ができた時に進める。
1違反モデルが得られれば、監査済み元CNF UNSATの下界1と合わせてそのdの節削除距離が1となる。
対応する点を一つ除いた1324点候補の独立整数幾何検査が通れば、K0706の上界と合わせて
A(2647)の正確値を決定できる。現時点ではモデルも候補も得られていない。

## SATモデル解釈の修正

既存 `parabola-p2207-no-equality-witness-20261107/maxsat_probe.py` のSAT後処理に、
負リテラル評価、選択点の上下、負リテラルに対応する除去点の符号の誤りがあった。
正の変数iは高側p-iを選ぶ。違反した正リテラル+iの支持点はi、負リテラル-iはp-i。
今回修正し、元の出力・歴史資料は変更しない。UNSAT/UNKNOWNという既存返値には影響しない。
SATの旧違反数・候補解釈はこの修正で再検査する必要がある。

`test_projection.py` はp=5,7,11,13,17の全1312等号テンプレートについて、元CNF評価と
24項の整数4×4行列式による全四点組検査を照合する。
旧helperと新workerの両修復後の点集合も、整数幾何で検査する。
p=17では192テンプレートが違反を持ち、この修復分岐も検査できた。
負リテラル単位例、保存CNFの完全一致、RC2を親から起動する玩具例も含む。
玩具例はp=2647の最適化の再試行でも幾何的証人でもない。
