# p2531 d=302..500の未監査188件

開始時のmainは4c1a6a1e。前段351 d台帳との差から対象を選び、既被覆の321,341,361,381,393,395,401,421,441,461,481を除いた。
現在の命題・statusは[K0702](../../../../knowledge/items/K0702-p2531-no-parabola-equality-witness.md)を参照する。

全188件がsolver UNSAT、固定DRAT-trimのRUP限定検査、空節処理修正版LRATの別実装で受理された。
提供38160辺の整数幾何、新188入力の独立投影schemaと全節集合の一致を確認した。
保存したCNF・圧縮LRATの別処理での実再生も188件すべて終了コード0だった。
sourceと証拠hash、前段台帳のhash連鎖、原DRAT188件のローカルhashを照合した。

前段351 dと新188 dは重複なしで539/1265 d、残り726 d。内訳は修正版DRAT143 d、LRAT396 d。
この和はd=1..500を全て含む。このbatchの未完了・失敗・UNKNOWNは0だが、全数監査・正確な最大サイズ・検証器の一般健全性の形式証明は主張しない。

```sh
uv run --locked --with python-sat==1.9.dev21 python research/experiments/parabola-p2531-lrat-batches-20261110/audit.py --prior research/experiments/parabola-p2531-lrat-batches-20261110/output/batch182-300/coverage.json --edges research/experiments/parabola-p2531-lrat-20261110/input/edges.txt --ds 302-320,322-340,342-360,362-380,382-392,394,396-400,402-420,422-440,442-460,462-480,482-500 --output FRESH-batch302-500 --workers 4 --budget 100000
uv run --locked python research/experiments/parabola-p2531-lrat-batches-20261110/verify_saved.py --saved research/experiments/parabola-p2531-lrat-batches-20261110/output/batch302-500 --output FRESH-verification302-500.json --manifest FRESH-certificates302-500.json --workers 4
```

採用CNF gzipとLRAT gzipはGit管理し、原DRAT gzipとraw LRATは各dのdirectoryにローカル保持する。
376原ファイルの存在とGit除外、raw LRAT188個と配布用gzip展開bytesの一致も確認した。
採用証拠・原証明の所在とhashは親outputのcertificates302-500.json、実再生結果はverification302-500.jsonに記録した。
原DRATのない別checkoutでも採用CNFとLRATだけで再生できる。再生成時は新しい出力先を使う。
