# p2531 d=142..160,162..180の独立監査

汎用ドライバを変更せず、前回の200 d台帳をpriorへ指定した別batch。既監査の141,161は対象外とした。
実行時点のmainはa21cd69c。現在の命題・statusは[K0702](../../../../knowledge/items/K0702-p2531-no-parabola-equality-witness.md)を参照する。

全38件がsolver UNSAT、固定DRAT-trimのRUP限定検査、空節処理修正版LRATの別実装で受理された。
独立投影schemaと入力全節集合が一致し、提供38160辺の整数幾何を検査した。
保存した圧縮CNF・LRATの別処理による実再生も38件すべて終了コード0だった。
台帳hash連鎖、source hash、原DRAT38件のローカルhashも照合した。

前段200 dと新38 dは重複なしで238/1265 d、残り1027 d。
修正版DRAT143 dとLRAT95 dを区別する。全数監査・検証器の一般健全性の形式証明・正確な最大サイズは主張しない。
UNKNOWN・失敗・未完了はいずれも0。計算を再起動する場合は実行中プロセスと既存planを確認し、異なる出力先を使う。

```sh
uv run --locked --with python-sat==1.9.dev21 python research/experiments/parabola-p2531-lrat-batches-20261110/audit.py --prior research/experiments/parabola-p2531-lrat-batches-20261110/output/batch102-140/coverage.json --edges research/experiments/parabola-p2531-lrat-20261110/input/edges.txt --ds 142-160,162-180 --output FRESH-batch142-180 --workers 4 --budget 100000
uv run --locked python research/experiments/parabola-p2531-lrat-batches-20261110/verify_saved.py --saved research/experiments/parabola-p2531-lrat-batches-20261110/output/batch142-180 --output FRESH-verification142-180.json --manifest FRESH-certificates142-180.json --workers 4
```

採用CNF gzipとLRAT gzipをGit管理し、原DRAT gzipとraw LRATは各dのディレクトリへローカル保持する。
採用証明・原証明の所在とhashは親outputのcertificates142-180.json、再生結果はverification142-180.jsonに記録した。
原DRATがない別checkoutでも採用CNFとLRATだけで検査できる。
