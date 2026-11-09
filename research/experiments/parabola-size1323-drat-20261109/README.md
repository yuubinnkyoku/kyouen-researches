# サイズ1323の監査と変数衝突の反例

サイズh=1323を4形状 `(x,c,e)=(0,0,0),(0,1,1),(1,0,1),(1,1,2)` に分け、
既存ソルバ記録をDRATへ進める過程で、一般形状builderの変数衝突を発見した。
不具合の現在の知識は [K0713](../../knowledge/items/K0713-shape-cnf-auxiliary-variable-aliasing.md)、
監査済み範囲は [K0711](../../knowledge/items/K0711-p2647-safe-lower-bound-1292.md) を参照する。

## 反例と修正

`input/legacy-p5-000.cnf` は禁止四点を一つも入れていないp=5・形状000・2点のCNFなのにUNSAT。
旧builderはCardEnc.equals(...,bound=0)のnvを次の確保位置に使い、最後の選択変数7,8と
点選択補助変数7,8を重複させる。CNF自身のUNSATはDRATでも受理されるが、
本来4通り存在する安全な2点の配置を表していない。
SATソルバやDRAT検査器の誤判定ではなく、入力への写像の不具合である。

共有 `search_shape_class.py` を修正し、各counter後に、それまでに予約した全変数範囲とnvのmaxを保持した。
修正版は `input/fixed-p5-000.cnf` と保存モデルでSAT。
`encoding_snapshot.py` は旧コード、`encoding_fixed.py` は修正後のスナップショットとして保持する。
原ソルバ記録や原DRATを、後から正しい形状の証拠として書き換えない。

## 実入力と監査状態

| 形状 | 採用する入力 | 修正前との差 | 状態（qualification-final） |
|---|---|---|---|
| 000 | `output/fixed/shape-000` | 異なる | DRAT VERIFIED |
| 011 | `output/shape-011` | byte一致 | DRAT VERIFIED |
| 101 | `output/fixed/shape-101` | 異なる | 再検査300秒上限でVERIFIED（実測184.5秒） |
| 112 | `output/shape-112` | byte一致 | ソルバUNSAT、DRAT検査120秒で未完了 |

旧 `output/shape-000` と `output/shape-101` のDRAT受理は、誤った変数割当のCNFへの受理記録であり、
幾何命題の根拠には使わない。011/112は修正版入力とbyte単位で一致したので、既存証明を再利用できる。
`generate.py` / `audit.py` は当初の実行コードとして保持し、修正後の000/101には
`generate_fixed.py` / `audit_fixed.py` を使った。各入力・証明・ソースのhashはinit/solver/auditに保存する。
使用辺は前回の監査済み53886四点を共有し、全辺列挙の完全性は上界の前提にしない。

112では617.2秒でUNSAT・2127240行のDRATを得たが、検査は未完了。
圧縮証明107007249 bytesはローカルの `output/shape-112/proof.drat.gz` に保持してGitから除外し、
追跡する `output/shape-112/proof-manifest.json` に圧縮・展開後SHA-256を記録した。
Gitだけを取得した別checkoutにはこの生証明はない。監査再開時はmanifest通りのローカル証明を復元するか、
実入力・凍結ソースから証明を再生成する必要がある。このmanifest自体は受理証拠ではない。
採用する監査済み上界1323の証明は前実験で全てGit管理されており、このローカル証明へは依存しない。

## 再現と再開

反例・修正・小例の全照合（大きな探索を起動しない）:

```sh
uv run --locked --with python-sat==1.9.dev21 python research/experiments/parabola-size1323-drat-20261109/regression.py
```

p=3,5,7,11,13,17の11896配置で修正版CNFと独立整数幾何の判定が一致。
原p=2647の入力も、000/101は修正で変化し、011/112はbyte一致することを確認した。

証拠レベルの新しいスナップショットを作る（既存のsnapshotは上書きしない）:

```sh
uv run --locked --with python-sat==1.9.dev21 python research/experiments/parabola-size1323-drat-20261109/qualify.py --output D:/tmp/size1323-qualification-new.json
```

生証明がローカルにある場合のみ、残るDRATを新しい出力先へ再検査する:

```sh
uv run --locked --with python-sat==1.9.dev21 python research/experiments/parabola-size1323-drat-20261109/recheck.py --shape 112 --timeout 900 --output research/experiments/parabola-size1323-drat-20261109/output/recheck-112-900s.json
```

同じ120秒上限の再試行や617秒のソルバ再実行は優先しない。`qualify.py` は修正版CNFとのbyte一致と
証明・入力・検査器hashを確認し、4件揃わなければ上界1322を返さない。
原実験の履歴を保持し、UNKNOWN・ソルバUNSAT・正しいCNFのDRAT受理・幾何上界を区別する。
