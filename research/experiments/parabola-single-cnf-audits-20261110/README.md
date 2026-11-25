# p2531・p3251の単一CNF独立監査

現在の結論は[K0702](../../knowledge/items/K0702-p2531-no-parabola-equality-witness.md)と[K0708](../../knowledge/items/K0708-p3251-no-parabola-equality-witness.md)を参照する。
既存のCNF・元DRAT・receiptを保持し、SAT探索は起動しない。
凍結したp2207独立schemaと共通検査関数を、source hashと既存意味検査receiptへ結び付けて再利用した。

```sh
uv run --locked python research/experiments/parabola-single-cnf-audits-20261110/check_case.py --p 2531 --output FRESH-p2531 --timeout 180
uv run --locked python research/experiments/parabola-single-cnf-audits-20261110/check_case.py --p 3251 --output FRESH-p3251 --timeout 180
uv run --locked python research/experiments/parabola-single-cnf-audits-20261110/regression.py --output FRESH-regression.json
uv run --locked python research/experiments/parabola-single-cnf-audits-20261110/replay.py --saved research/experiments/parabola-single-cnf-audits-20261110/output/p2531 --output FRESH-replay-p2531.json
uv run --locked python research/experiments/parabola-single-cnf-audits-20261110/replay.py --saved research/experiments/parabola-single-cnf-audits-20261110/output/p3251 --output FRESH-replay-p3251.json
```

既存出力は上書きしない。各素数の入力・証明・一時directoryは分離する。
採用CNF gzipとLRAT gzipをGit管理し、raw core.lratはローカル保持・Git除外する。
元DRAT gzipは元artifactに保持し、所在とhashをmanifestへ記録する。

## 形状の忠実性

任意の安全h+2点集合は原点あり・完全対一つ・空対なしに限られる（K0097）。
全CNFを対状態one-hot、BOTHの明示prefix counter、NONE単位節、点選択同値の構造節と残余幾何節に分ける。
このschemaは探索builderもCardEncもimportしない。各提供辺はgeneric整数4x4行列式で禁止四点と確認する。
安全集合から対状態・点選択・BOTH prefix ORを割り当てれば全節を満たすため、提供辺集合の完全性はUNSATによる排除に不要。
詳しいモデル構成は凍結したp2207監査のREADMEとschema.pyに記録している。

| p | 変数 | 構造節 | 幾何節 | 元DRAT行 | 採用LRAT行 | 独立上界 |
|---|---:|---:|---:|---:|---:|---:|
| 2531 | 8854 | 21502 | 38160 | 190979 | 57444 | 1266 |
| 3251 | 11374 | 27622 | 60266 | 229866 | 44623 | 1626 |

両方が固定DRAT-trim -Uと空節処理修正版LRATで受理された。圧縮CNF・LRATの別処理実再生と全bindingも成功。
素数の取り違えを含む10件の改変を拒否し、既存の小素数1104状態の意味検査へのsource bindingも確認した。
旧d別の被覆539/1265と84/1625は変更せず、全dを個別再生したとは扱わない。
正確な最大値、未調査素数への一般化、検査器の一般健全性の形式証明やLean形式化は主張しない。
