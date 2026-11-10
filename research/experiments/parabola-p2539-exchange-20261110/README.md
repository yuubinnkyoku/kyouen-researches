# p2539の固定完全対を保つ有界交換

現在の範囲と固定極大証人は[K0723](../../knowledge/items/K0723-p2539-safe-bound-and-maximal-witness.md)を参照する。
これは2026-11-10の独立experimentであり、先行pilotの入力・出力は保持する。
固定原点と完全対d=6、他の各対は低側・高側・空対の三値を使う（K0712）。
targetに対応する空対上限と、種に選ばれた点変数の否定へのAtMostで点数と削除数を制限する。
二つのcounterの各段階で予約上限とのmaxを保持する。形状CNFの旧alias問題（K0721）とは区別する。

## 保存した実行

| 種の点数 | target | 削除上限 | ソルバ | 秒 | 独立幾何 |
|---:|---:|---:|---|---:|---|
| 1254 | 1255 | 3 | SAT | 0.24 | 受理 |
| 1255 | 1256 | 3 | SAT | 2.35 | 受理 |
| 1256 | 1257 | 3 | SAT | 5.36 | 受理 |
| 1257 | 1258 | 3 | SAT | 1.87 | 受理 |
| 1258 | 1259 | 3 | SOLVER_UNSAT | 5.65 | 証明未監査 |
| 1258 | 1259 | 4 | SOLVER_UNSAT | 19.27 | 証明未監査 |

全ケースは10万衝突予算。SAT四ケースで完全モデルと候補を保存し、全節を再評価した。
audit.pyはsource・種・辺のhashを照合してCNFをbyte再生成し、別の点抽出で交換差分を再検査した。
幾何検査は探索辺やCNFを読まないgeneric整数4x4 Leibniz検査器を再コンパイルして行う。
1258点の採用入力はSHA-256 `454f0e293fd846aa6616dd45500dbaf9b325834408ec7f69234852e3e35e22fb`。

1258点集合の全未選択1281点に対する明示阻止四点をmaximal-outputに保存した。
生成は先行experimentのblocker関数を使うが、別のBareiss検査関数で全行列式0・所属・完全被覆を確認する。
安全性receiptと候補hashも結び付ける。提供辺の完全列挙を仮定する必要はない。

## 再現と保存証拠監査

rootのuv環境とg++を使う。python-satはlocked環境の依存に含まれないため--withで版を指定する。
全出力先は未使用directoryまたは未使用receipt pathを指定する。

```sh
uv run --locked --with python-sat==1.9.dev21 python research/experiments/parabola-p2539-exchange-20261110/search.py --seed research/experiments/parabola-p2539-pair-pilot-20261110/augmented-output/candidate.txt --edges research/experiments/parabola-p2539-pair-pilot-20261110/output/edges.txt.gz --target 1255 --max-removed 3 --budget 100000 --output FRESH-1255
uv run --locked --with python-sat==1.9.dev21 python research/experiments/parabola-p2539-exchange-20261110/audit.py --saved research/experiments/parabola-p2539-exchange-20261110/output --edges research/experiments/parabola-p2539-pair-pilot-20261110/output/edges.txt.gz --output FRESH-audit
uv run --locked --with python-sat==1.9.dev21 python research/experiments/parabola-p2539-exchange-20261110/certify_maximal.py --audit research/experiments/parabola-p2539-exchange-20261110/audit-output --saved research/experiments/parabola-p2539-exchange-20261110/output --edges research/experiments/parabola-p2539-pair-pilot-20261110/output/edges.txt.gz --output FRESH-maximal
uv run --locked --with python-sat==1.9.dev21 python research/experiments/parabola-p2539-exchange-20261110/regression.py --output FRESH-regression.json
```

次の探索は--seedへ直前の候補を渡しtargetを増やす。既存出力を上書きしない。
保存証拠の監査には後半三コマンドを使い、SAT探索を再起動する必要はない。
audit.pyの--savedはケースdirectoryを含む親directoryを指す。
--auditと--savedは対応する監査・探索出力を指定する。

proof-enabled SAT探索の初回ツール終了値は1、後続SAT三件の子プロセス終了値は0xC0000409だった。
いずれもresult.jsonまで保存された後の異常で、原因は未特定。
後続の実returncode・stdout・stderrはlaunch.jsonへ保持した。
正常終了の推測や再実行で原出力を置き換えず、保存された全モデルと候補を別処理で検査した。
audit.py・幾何・regressionは終了値0で成功した。

## 限界と次の監査

小素数p=5,7,17の13194三値割当てで、整数幾何・target・種からの削除上限とSATの存在が一致した。
trivialなcardinalityの予約上限、欠落・重複・偽節モデルの拒否も含む。
有限回帰は検査器の一般健全性証明ではない。

二つの負のケースはこの固定対・固定種・有限交換の入力に限られる。
proof.drat.gzはローカル保持・Git除外とし、result.jsonに解凍後hashと行数を記録する。
これは独立未監査のソルバ出力であり、交換不能や全体の最大値の上界には採用しない。
次回は特に除去上限4の保存228249行DRATを固定RUP/LRATで検査できる。
幾何学的な局所排除を主張するには、CNF反駁だけでなく形状・削除counterへの忠実性の独立監査も必要。
極大性は明示四点で独立に得られており、これらの負のソルバ判定に依存しない。
