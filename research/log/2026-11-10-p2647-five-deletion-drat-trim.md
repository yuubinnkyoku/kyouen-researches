# Q_2647: 5点削除を許す固定対部分問題のDRAT検査

1303点証人、原点と完全対 `d=1323`、他の対から高々一側、証人から高々5点を削除、という条件で1304点以上を要求したCNFを再生成した。保存CNFと一致し、符号付き削除数制約の小規模1472ケースを照合した。

保存された1256894行の証明を、DRAT-trim commit `2e3b2dc0ecf938addbd779d42877b6ed69d9a985` で検査し、`VERIFIED` を得た。先頭100行で切った証明は `NOT VERIFIED` となった。入力・証明・検査器のhashと実行結果は `output/target1304-seed1303-delete5-budget1m/drat-trim-check.json` に記録した。

検査器ソースは https://github.com/marijnheule/drat-trim から取得し、`gcc -D_GNU_SOURCE -O2 -std=c99 drat-trim.c -o drat-trim` でコンパイルした。検査時は保存済み `input.cnf.gz` と `local-proof.drat.gz` を展開し、`./drat-trim input.cnf local-proof.drat` を実行した。独立の増分検査器でも検査を継続中。

結論は指定した固定対と証人の近傍に限られる。一般の1304点集合の不存在は示さない。
