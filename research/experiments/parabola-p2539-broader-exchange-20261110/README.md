# p2539の削除上限拡張・完全対変更・完全対なしの有限探索

現在の独立結論は[K0723](../../knowledge/items/K0723-p2539-safe-bound-and-maximal-witness.md)と
[K0724](../../knowledge/items/K0724-p2539-fixed-pair-four-deletion-local-exclusion.md)を参照する。
このexperimentは2026-11-10の有限探索と入力監査を凍結する。
種はSHA-256 `454f0e293fd846aa6616dd45500dbaf9b325834408ec7f69234852e3e35e22fb` の1258点集合。
前回の独立排除の範囲を越えたケースだけを選び、同じ条件の探索は再実行しなかった。

## 保存した実行

全ケースは原点を保ち、1259点を要求し、衝突予算10万で実行した。

| ケース | 削除上限 | 変数 | 節 | 結果 | 秒 |
|---|---:|---:|---:|---|---:|
| 完全対6を固定 | 5 | 25129 | 89073 | UNKNOWN | 42.34 |
| 完全対を6以外へ変更 | 3 | 42812 | 128281 | SOLVER_UNSAT | 4.64 |
| 完全対を6以外へ変更 | 4 | 44062 | 130779 | SOLVER_UNSAT | 14.12 |
| 完全対なし | 4 | 40302 | 123259 | SOLVER_UNSAT | 10.21 |

新形状の三実行は子プロセス終了値0。固定対・削除上限5の実行はUNKNOWNとresult.jsonを書き出した後、
子プロセスが0xC0000409で異常終了した（launch.json）。正常終了とは扱わない。
SATモデル・候補はなく、新しい安全下界を得ていない。
固定対の最初のケースは凍結済みsearch.pyをそのまま使用した。
他の三ケースは、K0721で修正済みのencoding_fixed.pyを読み、
point変数の否定への削除counterを追加する。完全対変更では元のBOTH変数を偽にする。
完全対なしではBOTH数を0とし、trivialなcounterの返すnvを予約上限より小さくしない凍結builderを使う。
これらの新形状入力はexact targetであり、ソルバ出力を最大値の上界や交換不能と解釈しない。
証人探索用にproofを無効化したため、三つのSOLVER_UNSATにDRATはない。

## 再現

rootのuv環境、python-sat 1.9.dev21を使い、出力には未使用directoryを指定する。

```sh
uv run --locked --with python-sat==1.9.dev21 python research/experiments/parabola-p2539-exchange-20261110/search.py --seed research/experiments/parabola-p2539-exchange-20261110/output/target1258-remove3/candidate.txt --edges research/experiments/parabola-p2539-pair-pilot-20261110/output/edges.txt.gz --target 1259 --max-removed 5 --budget 100000 --output FRESH-fixed-pair-remove5
uv run --locked --with python-sat==1.9.dev21 python research/experiments/parabola-p2539-broader-exchange-20261110/change_pair.py --seed research/experiments/parabola-p2539-exchange-20261110/output/target1258-remove3/candidate.txt --edges research/experiments/parabola-p2539-pair-pilot-20261110/output/edges.txt.gz --target 1259 --max-removed 3 --budget 100000 --output FRESH-changed-pair-remove3
uv run --locked --with python-sat==1.9.dev21 python research/experiments/parabola-p2539-broader-exchange-20261110/change_pair.py --seed research/experiments/parabola-p2539-exchange-20261110/output/target1258-remove3/candidate.txt --edges research/experiments/parabola-p2539-pair-pilot-20261110/output/edges.txt.gz --target 1259 --max-removed 4 --budget 100000 --output FRESH-changed-pair-remove4
uv run --locked --with python-sat==1.9.dev21 python research/experiments/parabola-p2539-broader-exchange-20261110/no_pair.py --seed research/experiments/parabola-p2539-exchange-20261110/output/target1258-remove3/candidate.txt --edges research/experiments/parabola-p2539-pair-pilot-20261110/output/edges.txt.gz --target 1259 --max-removed 4 --budget 100000 --output FRESH-no-pair-remove4
uv run --locked --with python-sat==1.9.dev21 python research/experiments/parabola-p2539-broader-exchange-20261110/audit_saved.py --saved research/experiments/parabola-p2539-broader-exchange-20261110/output --edges research/experiments/parabola-p2539-pair-pilot-20261110/output/edges.txt.gz --output FRESH-input-audit
uv run --locked --with python-sat==1.9.dev21 python research/experiments/parabola-p2539-broader-exchange-20261110/regression.py --output FRESH-regression.json
```

保存入力の検査には最後の二コマンドを使い、探索を再起動する必要はない。
各launch.jsonへ引数・終了値・標準出力・標準エラーを保存した。
audit_saved.pyは四入力をbyte再生成し、source・種・辺hash、result/init一致、候補・モデルの不在を確認する。
負のソルバ結果の独立証明検査ではない。

## 回帰と次の課題

新しい二つのbuilderはp=5,7,17の65925選択割当てで、整数幾何・点数・削除上限と充足性を照合した。
完全対変更の小例では変更先の対を標本化し、その自由対の三値状態は全数検査した。
完全対なしの小例は全三値状態を検査し、削除上限0と非trivialな上限も含めた。
これは有限回帰であり、実入力全体の独立schemaや数学的な一般健全性証明ではない。

固定対の除去上限5は未確定のまま。完全対変更・完全対なしの除去上限4も独立排除ではない。
次に負の三ケースを採用するには、保存CNFの証明生成と、4値選択・point定義・削除counterを
探索builderから独立に確認するschemaが必要になる。
探索継続なら原点変更、削除上限を広げるなど別の条件を選び、同じ予算を繰り返さない。
