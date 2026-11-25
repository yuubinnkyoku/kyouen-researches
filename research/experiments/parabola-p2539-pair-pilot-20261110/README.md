# p2539の有限pilot・修復・固定証人監査

現在の結論は[K0723](../../knowledge/items/K0723-p2539-safe-bound-and-maximal-witness.md)を参照する。
このexperimentは2026-11-10の入力・出力を凍結する。既存出力を上書きしない。
生成した出力directoryとreceiptの出力pathには未使用の名前を指定する。
rootのlocked uv環境とg++を使う。SAT依存は--withで実行時のpython-sat 1.9.dev21を指定する。

## 再現

```sh
uv run --locked --with python-sat==1.9.dev21 python research/experiments/parabola-p2539-pair-pilot-20261110/pilot.py --edges research/experiments/parabola-p2539-pair-pilot-20261110/output/edges.txt.gz --output FRESH-pilot
uv run --locked python research/experiments/parabola-p2539-pair-pilot-20261110/local.py --saved research/experiments/parabola-p2539-pair-pilot-20261110/output --output FRESH-local
uv run --locked python research/experiments/parabola-p2539-pair-pilot-20261110/augment.py --saved research/experiments/parabola-p2539-pair-pilot-20261110/output --repaired research/experiments/parabola-p2539-pair-pilot-20261110/local-output --output FRESH-augmented
uv run --locked python research/experiments/parabola-p2539-pair-pilot-20261110/verify_saved.py --saved research/experiments/parabola-p2539-pair-pilot-20261110/augmented-output --output FRESH-replay.json
uv run --locked python research/experiments/parabola-p2539-pair-pilot-20261110/regression.py --saved research/experiments/parabola-p2539-pair-pilot-20261110/augmented-output --output FRESH-regression.json
uv run --locked python research/experiments/parabola-p2539-pair-pilot-20261110/projection_controls.py --output FRESH-projection-controls.json
```

保存証拠と符号化の再監査には最後の三コマンドを使い、SAT探索を再実行する必要はない。
新しいpilot結果から続きを行う場合はlocal.pyの--savedをその出力へ、
augment.pyの--savedと--repairedを対応する出力へ変更する。
pilotの既定値は12固定対、各10万衝突。localはd=1,631,1237の各100万step、seed=20261110+d。

## 保存した探索結果

元cacheはD:/tmp/kyouen-parabola/edges_2539.txt、843414四点であり、所在とhashをplan.jsonに記録した。
完全対を含む辺（この場合二完全対）を除いた38868辺を圧縮してGit管理する。
固定完全対を一つだけ含む等号templateでは、除去辺の節は恒真となる。
小素数で完全辺集合と除去後のCNFを全数比較したが、大素数cacheの完全列挙自体を独立監査したとは扱わない。
提供38868辺が実際に禁止四点であることはgeometry-edges.jsonで独立検査した。

12ケースの結果は11 UNKNOWN、d=1237のソルバUNSAT 1件。等号証人は得なかった。
各CNF gzip、ソルバ統計とhashを保存する。solver-proof.drat.gzはローカルに保持してGit除外し、
result.jsonに解凍後hash・行数・完了フラグを残す。UNKNOWNの証明は不完全であり、
UNSATの証明も未独立検査。どれも非達成の証拠には採用しない。

局所探索後の修復はd=1,631で1251点、d=1237で1253点となった。
後者の違反節99件は共有頂点を18点削除すれば被覆できた。
違反節21件の前二者より修復後サイズが大きく、違反節数だけで修復の良さは順位づけできない。
修復最良1253点は汎用整数幾何検査を通した。
三集合を各三順序で拡張し、1254点を三通り得た。採用した降順trialは点2533を追加した。
他trialは探索辺に対する暫定結果であり、独立検査対象は採用集合とその全追加阻止証拠だけ。

## 信頼境界

augmented-output/candidate.txtは1254点、blockers.txtは未選択1285点それぞれへの明示禁止四点。
全選択四点を完全な合同式フィルタとgeneric整数4x4 Leibniz検査で被覆した。
verify_saved.pyはCNF・局所モデル・辺cacheを読まず同じ集合を再検査し、
各阻止四点を別のPython Bareiss整数消去法で検査する。
安全三点の受理、禁止四点・重複・入力打切り・合成数の拒否も実行する。
regression.pyはp=5,7,11の192割当て全数照合、修復制御、五種類の破損阻止証拠の拒否を行う。
この三素数の非自明辺は空なので、projection_controls.pyでp=17,19の6656割当ても全数照合し、
非空節が安全・禁止の両側を正しく分類することを確認する。

明示した各追加点tがS内三点と禁止四点を作るのでS∪{t}は安全でない。
全補集合を覆うため包含極大性が従う。探索辺cacheの完全性を根拠にする必要はない。
最大性、点交換不能、検査器一般の形式的健全性、未調査素数の結論は主張しない。
