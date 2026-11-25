# p=2647の1292点安全証人

保存済みのp=2647,d=1323の等号CNFを、重みなしの確率的局所探索で近似した。
100万flip・seed=20261109の1試行（9.144秒、壁時計上限60秒）で、
元53,886節のうち41節だけに違反する割当を得た。
違反節の選択点支持をgreedyに被覆し、1325点のテンプレートから33点を除いて1292点を残した。
独立な整数幾何検査を通過し、**A(2647)>=1292**。
監査済み上界と合わせた現在の結論は [K0711](../../knowledge/items/K0711-p2647-safe-lower-bound-1292.md)。

## 一次資料

`output/walk-1000000-seed20261109/`:

- `model.json`: native探索が保存した正変数、違反数、最良step、完了step。
- `trace.txt` / `stderr.txt`: 生出力。最良モデルはstep 408536、100万stepまで完了。
- `assessment.json`: Pythonによる全元節の再評価41違反、除去33点、候補のパラメータ。
- `candidate.txt`: `p n`とソート済み1292パラメータ。点は `(t,t² mod p)`。
- `geometry.json`: 独立generic 4×4検証器の受理出力、入力とソースのSHA-256。
- `geometry_initial.json`: 初回の受理出力。対応ソースは `verify_subset_initial.cpp` に保存。

元CNFは前のRC2実験の保存入力をそのまま用いた:
`../parabola-cnf-deletion-distance-20261109/output/rc2-p2647-d1323-20261108T184724Z.cnf`。
SHA-256は `0f09fc6efce1ba1b3df795eef24e4bb014fcfad836f31d4e6ba7e99b242ff0b3`。
RC2のUNKNOWNを再実行したのではなく、同じ目的関数への別方式で、割当の上界を得た。

実際の探索ソースは `walk_initial.cpp`（SHA-256 `fcfd3f57e73f310c95b57fc439661b447c741f4719d58de2edeecdfe6968c3bb`）。
現在の `walk.cpp` は、restart直後にSATを発見した一般入力にも対応するcheckpointを追加した版。
当初の実行ソースを保持し、修正版を当時の実行コードと混同しない。

## 独立検証と範囲

`verify_subset.cpp` は既存の `frontier-geometry-2026-10-05/verify_witnesses.cpp` をもとに、
等号サイズの制限を外し、少数点・重複・欠損入力等を扱うようにした。
探索コード、CNF、edge cacheは読まず、整数座標から24項の4×4行列式を計算する。
全115,563,355,055組を、証明済みの必要合同式によって漏れなく絞り、
残る43,730,623組で行列式0件だった（初回32.160秒）。
その後、空入力・不完全なヘッダの拒否と、大きな点数の四点組数を128bit中間値で計算する修正を加えた。
最終版でも同じ1292点を再検査し、同じ検査数で受理した（32.095秒）。入力・出力と各版のsource hashを区別する。
行列式が0ならmod pでも0で、異なるパラメータのVandermonde積が非零なので和が0 mod pとなる。
選択三点から第四点を復元して最大点だけを検査するため、対象四点を重複なく被覆する。

最大性・最適性は主張しない。41は当該CNF節削除距離の検査済み上界、
33はこの割当からの除去点数であり、どちらも最小と証明した値ではない。
下界証人の安全性は最終の整数幾何検査から従い、CNF還元や局所探索の正しさには依存しない。
計算機・コンパイラ・検証器と必要合同式の証明への依存は残る。

## 再現

repo rootで、小規模回帰のみ:

```sh
uv run --locked python research/experiments/parabola-local-repair-20261109/verify.py
```

4つの玩具CNFを全割当最適値と照合し、96小集合についてPython整数行列式・
C++全四点検査・C++合同式フィルタの判定を比較した。7種の不正入力、保存証拠のhashと
元CNFに対する保存モデルの41違反も検査する。
このコマンドは大きな証人の幾何検査を再実行しない。

明示的に1292点証人の検査を再現する場合:

```sh
uv run --locked python research/experiments/parabola-local-repair-20261109/verify.py --audit research/experiments/parabola-local-repair-20261109/output/walk-1000000-seed20261109/candidate.txt --receipt D:/tmp/parabola-subset-audit-reproduction.json
```

探索自体の再現は、新しい出力先を使う:

```sh
uv run --locked python research/experiments/parabola-local-repair-20261109/run.py --source research/experiments/parabola-local-repair-20261109/walk_initial.cpp --steps 1000000 --seed 20261109 --output research/experiments/parabola-local-repair-20261109/output/reproduction
```

同じseed・予算を自動再試行しない。次に改善するなら、現在の41違反モデルを出発点として
別の近傍・点除去目的・大きな空対を扱う方法を具体化する。正確値の決定は未完了。
