# 2026-10-29: N11第18回、証明限定8石WIN 5,803類・未証明辺44本

最新main、AGENTS.md、research/knowledge/README.md、K0023、11×11関連の実験・研究記録を確認した。第17回の証明限定8石WIN 5,795類、固定14根計画の未証明辺45本から再開。branch / PRを作らずmainへ直接反映した。

第17回後の固定再計画では9石候補116類から支配関係を削除し14類を選択。合法10石子381本はすべて異なる。第18回の固定終局証明書は**1 WIN9 / 13 LOSS9**。独立整数幾何検証CI [40807028929](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40807028929)と、別実装Pythonによる42個の終局義務の再検証CI [40807254582](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40807254582)が成功した。勝敗は9石局面に限る。

第18回WIN9から異なる9類のWIN8親を導出。証明済みとの重複1類を除く**8類が純増**。伝播CI [40807139359](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40807139359)の成功と成果物12868404730を確認し、`research/experiments/n11-s9-post-round17-round18-20261029/lift.json`に固定した。成果物ZIPのSHA-256は `3ec379ba927aa806638c6637ed48a7c3adb61c0d0f27ac0f5098a6c7e777a164`。証明限定WIN8は**5,795→5,803類**、固定14根計画の証明済み辺は**503→504/548**、未証明辺は**45→44本**。WIN/LOSS衝突0、新規二石root閉鎖0。

第9〜18回の証明書を再利用する第18回後の再計画を `research/experiments/n11-s9-post-round18-replan-20261029/replan.js` に実装。第18回の独立検証・上位伝播を再実行し、10石LOSS証人由来の9石LOSS親、回をまたぐWIN/LOSS衝突、既存WIN8伝播、残り44本への接続を監査する。候補選択は支配関係削減と被覆最適化による。CI [40807697423](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40807697423)を起動したが、この記録時点では実行中。選択結果・削減数は検証完了まで未確定とする。

固定14根の44本は空盤解決までの全証明義務を意味しない。未完探索、pn/dn、潜在被覆を勝敗に読み替えない。

**標準11×11空盤の勝敗はUNKNOWN。**
