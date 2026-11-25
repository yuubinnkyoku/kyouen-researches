# p2539・原点を除く四点削除近傍

現在の結論は[K0726](../../knowledge/items/K0726-p2539-four-deletion-local-optimum.md)を参照する。
種はSHA-256 `454f0e293fd846aa6616dd45500dbaf9b325834408ec7f69234852e3e35e22fb` の1258点集合S。
K0725で原点保持の場合は排除済みなので、今回は原点を必ず除く二形状だけを調べた。

## 再現

rootのuv環境、gcc、g++を使用し、全出力には未使用pathを指定する。

```sh
uv run --locked python research/experiments/parabola-p2539-without-origin-20261111/greedy.py --seed research/experiments/parabola-p2539-exchange-20261110/output/target1258-remove3/candidate.txt --edges research/experiments/parabola-p2539-pair-pilot-20261110/output/edges.txt.gz --output FRESH-greedy
uv run --locked --with python-sat==1.9.dev21 python research/experiments/parabola-p2539-without-origin-20261111/search.py --seed research/experiments/parabola-p2539-exchange-20261110/output/target1258-remove3/candidate.txt --edges research/experiments/parabola-p2539-pair-pilot-20261110/output/edges.txt.gz --target 1259 --complete-pairs 0 --max-removed 4 --budget 100000 --output FRESH-B0
uv run --locked --with python-sat==1.9.dev21 python research/experiments/parabola-p2539-without-origin-20261111/search.py --seed research/experiments/parabola-p2539-exchange-20261110/output/target1258-remove3/candidate.txt --edges research/experiments/parabola-p2539-pair-pilot-20261110/output/edges.txt.gz --target 1259 --complete-pairs 1 --max-removed 4 --budget 100000 --output FRESH-B1
uv run --locked python research/experiments/parabola-p2539-without-origin-20261111/audit.py --output FRESH-audit --timeout 120
uv run --locked python research/experiments/parabola-p2539-without-origin-20261111/regression.py --output FRESH-regression.json
uv run --locked python research/experiments/parabola-p2539-without-origin-20261111/replay.py --saved research/experiments/parabola-p2539-without-origin-20261111/audit-output --output FRESH-replay.json
uv run --locked python research/experiments/parabola-p2539-without-origin-20261111/qualify.py --output FRESH-qualification.json
```

auditは保存output/B0-target1259-remove4とoutput/B1-target1259-remove4を読み、探索を起動しない。
別出力の探索を監査するときは保存版と同じ配置・hashを復元する。
replayは採用したCNF gzip・verified-proof.drat.gz・固定種と独立schemaを読む。
ソルバやローカルLRATを使わずGit管理された証拠だけで再生できる。
元DRAT gzipと大きいcore.lrat/raw gzipはローカル保持・Git除外し、manifestへ所在・hashを保存する。

## 探索と独立検査

原点のみを除く貪欲拡張は三順序とも1257点から追加できず、最良1257点集合を整数幾何で検査した。
この探索結果を改善不能の証明には使わない。
次の二SAT入力は原点なし・exact1259点・総削除数4以下。
原点を必ず失うため、非原点1257個の種点への削除counterは上限3である。

| 完全対数 | 空対数 | 変数 | 節 | 幾何節 | 元DRAT行 | 検査LRAT行 |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | 10 | 36556 | 115767 | 38866 | 23072 | 1277 |
| 1 | 11 | 40320 | 123294 | 38866 | 205896 | 22797 |

二つの探索は証明生成を有効にして実行し、ソルバUNSATと証明を保存した。両子プロセス終了値は0。
独立schemaはSATライブラリや探索builderをimportしない。
4値one-hot、BOTH数、NONEの二つのprefix counter、pointとBOTH∨sideの全三節同値、削除counterを全節照合する。
全幾何節は原点を含まない四点へ直接戻し、generic整数4x4行列式0を実検査した。
原点依存の三点節は受理しない。
安全なexact1259点Tから状態・point・prefix変数を構成すれば全節を満たすので、提供辺の完全性は不要。
両DRATを固定RUP限定検査で受理し、抽出LRATを空節修正版でも受理した。
採用圧縮DRATを別処理で再生し、独立schema・整数幾何・固定種も結び付けた。

## 全改善集合への論証

0∉T、|S∖T|≤4、|T|≥1259の安全なTを仮定する。原点を失うのでr=|S∖T|≥1。
完全対は高々一つである。
完全対なしならS∩Tを全て含む1259点部分集合T'を選べ、完全対なし・原点なし・削除数rを保てる。
完全対{d,2539−d}を持つならR=(S∩T)∪{d,2539−d}は|R|≤1258−r+2≤1259。
Rを含む1259点部分集合T'をTから選べ、新完全対・原点なし・削除数rを保てる。
いずれも安全性を受け継ぎ、対応するCNFの独立排除に反する。

従って原点を除く場合も4点以下の削除では改善できない。
原点を保つK0725の場合と合わせ、全ての安全な改善集合はSから少なくとも5点を失う必要がある。
これは固定Sの局所最適性であり、A(2539)=1258という全体の最大性ではない。

## 回帰と限界

二実入力の14改変を拒否し、point定義の128真理値割当てと、原点削除コスト・部分集合選択の縮小例152件を検査した。
三点の原点依存節や非原点削除counterの境界誤りも拒否する。
縮小例は一般証明の代替ではなく、全称論証は前節による。
検査器・コンパイラの一般健全性やLean形式証明、5点以上を失う改善の不存在は主張しない。
