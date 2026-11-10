# p2531 d=182..300の未監査113件

開始mainはd2b4a7fe。前段238 d台帳との差から対象を選び、既監査の201,221,241,261,268,281を除いた。
現在の命題・statusは[K0702](../../../../knowledge/items/K0702-p2531-no-parabola-equality-witness.md)を参照する。

全113件がsolver UNSAT、固定DRAT-trimのRUP限定検査、空節処理修正版LRATの別実装で受理された。
提供38160辺の整数幾何、新113入力の独立投影schemaと全節集合の一致を確認した。
保存したCNF・圧縮LRATの別処理での実再生も113件すべて終了コード0だった。
sourceと証拠hash、前段台帳のhash連鎖、原DRAT113件のローカルhashを照合した。

前段238 dと新113 dは重複なしで351/1265 d、残り914 d。内訳は修正版DRAT143 d、LRAT208 d。
このbatchの未完了・失敗・UNKNOWNは0だが、全数監査・正確な最大サイズ・検証器の一般健全性の形式証明は主張しない。

```sh
uv run --locked --with python-sat==1.9.dev21 python research/experiments/parabola-p2531-lrat-batches-20261110/audit.py --prior research/experiments/parabola-p2531-lrat-batches-20261110/output/batch142-180/coverage.json --edges research/experiments/parabola-p2531-lrat-20261110/input/edges.txt --ds 182-200,202-220,222-240,242-260,262-267,269-280,282-300 --output FRESH-batch182-300 --workers 4 --budget 100000
uv run --locked python research/experiments/parabola-p2531-lrat-batches-20261110/verify_saved.py --saved research/experiments/parabola-p2531-lrat-batches-20261110/output/batch182-300 --output FRESH-verification182-300.json --manifest FRESH-certificates182-300.json --workers 4
```

採用CNF gzipとLRAT gzipはGit管理し、元DRAT gzipとraw LRATは各dのディレクトリにローカル保持する。
226原ファイルが存在してGit除外され、raw LRAT113個が配布用gzipの展開bytesに一致することを確認した。
原証明と採用証拠の所在・hashは親outputのcertificates182-300.json、実再生結果はverification182-300.jsonに記録した。
原DRATのない別checkoutでも採用CNF・LRATだけで再生できる。再生成時は新しい出力先を使う。
