# 固定完全対を保つ有界交換SAT

この実験は保存1301点から3点以下を除く交換で、より大きな安全集合を探索した。
現在の境界は[K0711](../../knowledge/items/K0711-p2647-safe-lower-bound-1292.md)を参照する。
以前の2点以下除去の投影近傍で改善未発見だった記録は変更しない。

`search.py` は既存の凍結三値符号化を使い、原点と完全対d=1323を固定する。
点数の下限を空対数の上限で表し、種で選択されていた低側・高側の変数の否定にAtMostを加える。
後者は実際に種から失う点の個数を制限する。先行counterの上限と3969の大きい方を保持して
次のcounterへ渡す。負のsolver結果はこの有界近傍に限られ、全体の最大サイズの上界には使わない。

## 1302点の構成

`output/target1302-remove3-budget100000` は1301点から3点以下除去、1302点以上の入力。
7.110秒・8180衝突でSATとなり、`{684,1430,1785}` を除き `{150,1217,1294,1963}` を加えた。
37731変数・129266節の完全モデルと入力を保存した。候補発見時のgeometry未検査という記録は保持する。

後から独立generic整数4×4検査を実行し、全119187179475四点を合同式により被覆して
45110020候補を実検査、禁止四点0件だった（29.495秒、終了コード0）。
証人のSHA-256は `5395d2326e08dfe8ac43b57103cc1d469ceddf68a0b522b4d7092e9db342000b`。

`audit.py` は保存入力のbyte再生成、全節の直接評価、独立に書いた点抽出と交換差分、幾何receiptのhashを確認する。
除去counterの768小規模真理値表、実際の補助変数領域の非衝突、3不正モデルの拒否も検査した。
全変数を保存モデルに固定したproof-enabled APIの再生も成功した。
幾何の安全性はCNFや探索器から独立しており、モデル検査や小規模回帰とは区別する。

初回探索のツール終了値は、完全なresult.jsonが出力された後に1と報告された。
その原因は未確定のため、プロセス終了値だけで成功扱いしていない。
保存証拠は全節検査と独立幾何検査を通り、同じproof-enabled APIの玩具例と全モデル固定再生は終了コード0だった。
自由探索を同じ条件で再実行して原出力を置き換えることはしていない。

## 次の1303点要求

1302点を種に、3点以下を除き1303点以上とする次のCNFを別出力に保存した。
`output/target1303-remove3-budget100000` は36457変数・126721節で、
20.802秒・22302衝突でSOLVER_UNSAT、325093行のDRATも保存した。
原記録の `independent_proof_audit: NOT_RUN` は発見当時の記録として保持する。
`audit_proof.py` はこの保存証明に既存の削除を無視するRUP-only検査器を適用し、独立receiptへ結果を記す。
受理した場合も、その特定CNFの反駁であり、全体の上界の改善や最大性を意味しない。

実際のRUP-only監査は120秒でtimeoutし、空節の受理には至らなかった。
`output/proof-audit-1303.json` に失敗・入力・証明・検査器のhashを保存した。
このUNSATは独立監査未完了のソルバ主張として扱う。同じ120秒条件の再実行はせず、
次回は削除対応の修正版DRAT検査器、証明縮約、またはRUP検査の伝播効率を検討する。

## 再現

rootのuv環境から、新しい出力先を指定する。既存の実入力・出力を上書きしない。

```sh
uv run --locked --with python-sat==1.9.dev21 python research/experiments/parabola-bounded-exchange-20261109/search.py --seed research/experiments/parabola-maximal-1300-20261109/output/exchange-remove-at-most-two/candidate.txt --target 1302 --max-removed 3 --budget 100000 --output FRESH-1302
uv run --locked python research/experiments/parabola-local-repair-20261109/verify.py --audit research/experiments/parabola-bounded-exchange-20261109/output/target1302-remove3-budget100000/candidate.txt --receipt FRESH-geometry.json
uv run --locked --with python-sat==1.9.dev21 python research/experiments/parabola-bounded-exchange-20261109/audit.py --saved research/experiments/parabola-bounded-exchange-20261109/output/target1302-remove3-budget100000 --output FRESH-audit
uv run --locked --with python-sat==1.9.dev21 python research/experiments/parabola-bounded-exchange-20261109/search.py --seed research/experiments/parabola-bounded-exchange-20261109/output/target1302-remove3-budget100000/candidate.txt --target 1303 --max-removed 3 --budget 100000 --output FRESH-1303
uv run --locked python research/experiments/parabola-bounded-exchange-20261109/audit_proof.py --saved research/experiments/parabola-bounded-exchange-20261109/output/target1303-remove3-budget100000 --output FRESH-proof-audit.json --timeout 120
uv run --locked python research/experiments/parabola-monotone-rup-20261109/regression.py --output FRESH-rup-regression.json
```

未知探索、ソルバ主張、実証明の独立検査、符号化の回帰、数学的な一般証明を区別する。
この実験はLean形式証明や、任意の素数に対する最大サイズ公式を与えない。

## 2026-11-09: 除去上限4の次の入力

保存1302点を種に、除去上限を3から4へ広げた別の1303点要求を実行した。
`output/target1303-remove4-budget100000` は37749変数・129303節、
77.497秒・100005衝突でUNKNOWN。候補・モデル・証明はなく、不存在や交換不能は主張しない。
初回ツールの終了値は原記録出力後に1と報告されたため、正常終了の推測で採用範囲を広げない。
`verify_unknown.py` は実入力をbyte再生成し、初期記録・source hash・変数予約と各出力の不在を確認する。
この検査は保存されたUNKNOWNの出典確認であり、SAT/UNSATを判定しない。

```sh
uv run --locked --with python-sat==1.9.dev21 python research/experiments/parabola-bounded-exchange-20261109/search.py --seed research/experiments/parabola-bounded-exchange-20261109/output/target1302-remove3-budget100000/candidate.txt --target 1303 --max-removed 4 --budget 100000 --output FRESH-remove4
uv run --locked --with python-sat==1.9.dev21 python research/experiments/parabola-bounded-exchange-20261109/verify_unknown.py --saved research/experiments/parabola-bounded-exchange-20261109/output/target1303-remove4-budget100000 --output FRESH-unknown-validation.json
```
