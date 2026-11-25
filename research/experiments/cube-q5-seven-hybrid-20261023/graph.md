# 三角形を持たない共存グラフによる終盤短縮

有限共有盤の通常プレイで、合法集合族は遺伝的（合法集合のどの部分集合も合法）とする。
現在の合法集合Sの合法追加点集合をVとし、V上でpqを辺とする条件を
S∪{p,q}が合法であることと定義する。

このグラフが三角形を持たなければ、Sからは高々2手で終わる。もし3点を追加できた
なら、その各2点も共存でき、グラフに三角形があるからである。

- 孤立点pがあれば、pを置いた直後に合法手がなくなるのでSはN。
- 孤立点がなければ、どの初手pにも共存点qがあり、qを置くと終わる。
  各1手後の局面はNでありSはP。Vが空のときもSはP。

三角形がある場合は通常探索へ戻る。三角形の存在から3手を追加できるとは主張しない。

`graph.cpp`は候補数8以下の新規未確定局面にこの正確な規則を適用する。
辺は全三点組の差分幾何で判定する。Nには終端P子、Pには全N子と各子の終端P証人を
追加するため、証明書形式は変えず従来の独立検査器を使える。検査器が補題を
既知葉として信用することはなく、各局面の全合法子を実際に検査する。

既知3立方20根、中断再開の一致、tree上限40の置換、不正checkpoint拒否を確認した
（regression-graph.json）。固定seedの7立方合法履歴から得た24終盤も、従来df-pnと
全ての勝敗が一致し、各全証明書を独立Bareiss検査した（endgames-verified.json）。
最新の層分け版も同じ24終盤を独立検査した（endgames-current-verified.json）。
標本は全称補題の証明の代わりではなく、実装の有限回帰である。

```sh
g++ -O3 -std=c++17 -Wall -Wextra -Werror research/experiments/cube-q5-seven-hybrid-20261023/graph.cpp -o /tmp/q7-graph-repro
python research/experiments/cube-q5-seven-hybrid-20261023/regression.py /tmp/q7-graph-repro /tmp/q7-legacy /tmp/q7-verify-incremental
python research/experiments/cube-q5-seven-hybrid-20261023/regression_layers.py /tmp/q7-graph-repro /tmp/q7-legacy /tmp/q7-verify-incremental
python research/experiments/cube-q5-seven-hybrid-20261023/check_endgames.py /tmp/q7-graph-repro /tmp/q7-verify-incremental
```

Q5HYB1を読み、子一覧を再構築するQ5HYB2へ保存する。子の共存点cacheは保存しない。
engine.cppは先の保存方式の版として保持し、graph.cppで短縮を加えた。
layers.hppは追加確定候補を読み取り専用の層へ移し、作業用メモリを再利用する。
層の依存先fingerprint・行数・counterを束縛する。索引のBloom filterは不在判定にのみ
使い、一致候補は必ず元の全6ワードを比較する。全行・証人の索引照合も実施した。
小盤面では追加表の層への移動と未確定treeの引継ぎも独立証明で回帰確認した。
4石根・3石根・空盤の未確定性から勝敗を推測しない。
