# 保存1300点集合の包含極大性

厳密な命題は[K0719](../../knowledge/items/K0719-p2647-saved-1300-witness-inclusion-maximal.md)を参照する。
現在の最大安全サイズの境界とは別に、保存した1300点集合へ1点も追加できないことを証明する。

`output/initial/blockers.txt` は先頭に `2647 1347`、以後は
`追加t q0 q1 q2 q3` の行を補集合の全点について持つ。
各四点はtと既存集合の3点からなり、正確な整数行列式が0である。

`audit.py` は非空対には二完全対の四点を提案し、空対25の50側には既存の直接投影CNFを候補生成に使う。
`verify_blockers.cpp` はCNF・SATソルバを使わず、明示四点の範囲・所属・相異性・整数幾何と
未選択1347点の完全被覆だけを検査する。既存verify_subset.cppのgeneric行列式をそのまま利用する。
元集合の安全性は、その同じinput hashに結び付いた独立幾何receiptから確認する。
両者が揃うので包含極大となる。最大サイズが1300という主張ではない。

再現は新しい出力先を指定する:

```sh
uv run --locked python research/experiments/parabola-maximal-1300-20261109/audit.py --output FRESH-blocker-audit
```

実行時に正例1347行の受理と7不正制御の拒否も確認する。
生成処理は保存証人の評価であり、新しいSAT探索や大きい四点全数検査は起動しない。

## 2026-11-09: 2点除去・3点追加による1301点証人

包含極大な上の1300点集合から `{1300,2262}` を除き、`{385,610,1723}` を加えると
1301点になる。`exchange.py` は固定原点・完全対d=1323を保ち、投影CNFの阻止支持を使って
2点以下の除去と1点多い追加を試した。6.21秒で候補を得た時点の原記録ではgeometryは未検査であり、
その記録は保持する。包含極大性は特定の1300点集合への単点追加不能で、交換による増加と矛盾しない。

後から独立のgeneric整数4×4検査器で全118821013025四点を合同式により被覆し、
44971096候補を実検査して禁止四点0件を確認した（30.88秒）。
`output/exchange-remove-at-most-two/candidate.txt` のSHA-256は
`1e02ea20ab61516d267887a7a31fa1b2aefd4aa9c305da403c60468da9bfc27b`。
現在の境界は[K0711](../../knowledge/items/K0711-p2647-safe-lower-bound-1292.md)を参照する。

さらに `verify_exchange.py` は以前UNKNOWNだった1301点要求の保存CNFを使い、3966個の点選択変数を
全てこの証人に固定して補助変数を補完した。35121変数の完全モデルが全122752節を満たし、
点抽出も一致する。衝突0、0.36秒。これは点を自由に探す探索の反復ではない。
元の10万・50万衝突UNKNOWNの試行は当時の記録のまま保持する。

`exchange_seeded.py` は入力証人を指定する版で、1301点からの次の試行では
36066除去候補・286追加候補で改善未発見（3.34秒）だった。
固定完全対の投影CNF近傍についての実装上の観測に限り、1302点の不存在や一般の局所最適性は主張しない。
同じ版を元の1300点で回帰実行し、元の交換とbyte単位で同じ1301点証人を再現した。

再現では毎回新しい出力先を使い、既存のraw evidenceを上書きしない:

```sh
uv run --locked python research/experiments/parabola-maximal-1300-20261109/exchange.py --seconds 60 --output FRESH-exchange
uv run --locked python research/experiments/parabola-local-repair-20261109/verify.py --audit research/experiments/parabola-maximal-1300-20261109/output/exchange-remove-at-most-two/candidate.txt --receipt FRESH-geometry.json
uv run --locked --with python-sat==1.9.dev21 python research/experiments/parabola-maximal-1300-20261109/verify_exchange.py --output FRESH-completion
uv run --locked python research/experiments/parabola-maximal-1300-20261109/exchange_seeded.py --seed research/experiments/parabola-maximal-1300-20261109/output/exchange-remove-at-most-two/candidate.txt --seconds 60 --output FRESH-next-exchange
uv run --locked python research/experiments/parabola-maximal-1300-20261109/exchange_seeded.py --seed research/experiments/parabola-warm-improvement-20261109/output/target1299-warm1298-budget500000/candidate.txt --seconds 60 --output FRESH-regression
uv run --locked python research/experiments/parabola-maximal-1300-20261109/audit_saved_exchange.py --output FRESH-saved-audit.json
```

最後の保存監査はSAT・符号化generatorをimportせず、保存モデルの全節と点状態を評価する。
モデル欠落・変数重複・点選択符号反転の3不正制御も拒否する。幾何については既存receiptとのhash照合であり、
その保存監査自体で行列式を再計算したとは扱わない。上界の証明や検証器の一般的健全性の証明とも区別する。
