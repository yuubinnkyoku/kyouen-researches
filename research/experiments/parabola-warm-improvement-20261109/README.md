# 1296点のphaseから1298点へ

現在の結論は[K0711](../../knowledge/items/K0711-p2647-safe-lower-bound-1292.md)、
符号化の数学的範囲は[K0712](../../knowledge/items/K0712-parabola-empty-pair-ternary-sat-reduction.md)を参照する。
固定原点と完全対d=1323の三値符号化を使い、1296点の保存済み証人をphaseにして次のサイズを要求した。
phaseはヒューリスティックな初期指定であり、点の固定や包含を要求するassumptionではない。

| 保存ディレクトリ | 起点 | 要求 | 結果 |
|---|---:|---:|---|
| output/target1297-warm1296-budget100000 | 1296点 | 1297点以上 | 7.76秒でSAT、1298点・空対27 |
| output/target1299-warm1298-budget100000 | 1298点 | 1299点以上 | 48.37秒、10万衝突予算でUNKNOWN |

Python-SAT 1.9.dev21のCadical195、各衝突予算100000、親の壁時計上限60秒。
初回SATの実入力は40201変数・132904節。保存した完全モデルが全節を満たすことを確認した。
1298点の独立整数幾何検査は `2647 1298 117727574580 44555181`、終了コード0。
全117727574580四点を合同式で被覆し44555181候補のgeneric 4×4整数行列式を検査して禁止四点0件だった。

`encoding_snapshot.py` は前実験のternary.pyのbyte一致コピー。
前実験で検査した三値19392割当・444 cardinalityケースの符号化は変更していない。
`verify_saved.py` はsnapshotのbyte一致、2実入力の再生成とhash、完全モデル・点抽出・幾何receiptを照合する。
UNKNOWNはモデルや不存在証明を返しておらず、固定dの族についても全体についても上界へ使わない。
1300点以上や1322点以上の以前の試行と同じ計算を繰り返していない。

保存証拠の検査（SAT探索は再実行しない）:

```sh
uv run --locked --with python-sat==1.9.dev21 python research/experiments/parabola-warm-improvement-20261109/verify_saved.py --output FRESH-verification.json
```

探索の再現は、同予算の定期再試行にせず、新しい出力先を指定する:

```sh
uv run --locked --with python-sat==1.9.dev21 python research/experiments/parabola-warm-improvement-20261109/run.py --target 1297 --warm research/experiments/parabola-ternary-selection-20261109/output/target1293-budget100000/candidate.txt --budget 100000 --timeout 60 --output FRESH-directory
```

独立幾何検査は既存verify.pyの--auditと--receiptを使い、receiptを新しい出力先へ保存する。

## 後続: 50万衝突予算で1300点へ

2026-11-09、1299点要求の衝突予算を10万から50万へ増やした。
同じwarm startと同じCNF（SHA-256 ec55b41a...）で83.515秒・190902衝突でSATとなり、1300点・空対25を得た。
保存先は `output/target1299-warm1298-budget500000`、親の壁時計上限300秒。
37665変数・127836節の完全モデルを検査し、実入力を再生成してbyte一致を確認した。
独立幾何検査は `2647 1300 118455690925 44831921`、禁止四点0件・終了コード0。
UNKNOWNだった入力が予算増加でSATになった事例として、両方の原記録を保持する。

続く `output/target1301-warm1300-budget100000` は1300点をphaseにした1301点以上の要求で、
10万衝突予算・52.79秒でUNKNOWN（親の壁時計上限90秒）。不存在の証明は得ていない。
`output/verification-budget500000.json` は旧2件と新2件を一緒に照合した結果。

新しい予算の探索を再現する場合も、既存の出力先は上書きしない:

```sh
uv run --locked --with python-sat==1.9.dev21 python research/experiments/parabola-warm-improvement-20261109/run.py --target 1299 --warm research/experiments/parabola-warm-improvement-20261109/output/target1297-warm1296-budget100000/candidate.txt --budget 500000 --timeout 300 --output FRESH-budget500000-directory
```

## 後続: 1301点要求も50万衝突へ

`output/target1301-warm1300-budget500000` は、1301点要求の予算を50万衝突へ増やしたもの。
同じCNF・同じ1300点phaseで269.43秒・500000衝突まで進めてもUNKNOWNだった（親上限300秒）。
モデル・証人はなく、1301点の不存在を意味しない。
`output/verification-1301-budget500000.json` に旧4件と新1件の照合を保存した。
