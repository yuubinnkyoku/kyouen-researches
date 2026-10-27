# 2026-10-27：19子9石WIN55類の第三独立C++終局検証

開始時main `256863cd7717a2a5eab3494acdee873c99cead72`。AGENTS.md、research/knowledge/README.md、K0023、11×11の19子・20子9石証明、14根再最適化、直近研究記録を確認。既知の証明限定8石WINは4,089類、保存14根の証明済み298/548辺、条件付き最小未証明250辺。**標準11×11空盤勝敗UNKNOWN**。

既存 `n11-s9-n19-terminal-20261027/certificate.tsv` の9石WIN55類を、第三の独立実装 `independent_terminal.cpp` で終局まで再計算。整数4×4行列式の余因子展開、独立D4正準化、9石根の安全性、8石逆親の合法性、全9→10石合法手、10石以降の禁止2・3・4点組を用いた通常プレイの完全再帰を実装。既存のJavaScript幾何・凍結勝敗表・未完探索は参照しない。

結果は9石WIN55類、8石WIN逆親477類、9→10石着手1,045本、相異なる10石WIN葉1,026類、終局探索状態数83,884。既存の3×3差分行列式と4×4 Bareiss法による結果と一致。証明書の根、状態数、UNKNOWNヘッダ、行数を改変した4件を拒否した。

`.github/workflows/n11-s9-n19-terminal.yml` に第三C++検証と改変拒否を追加し、[専用CI 40465471579](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40465471579) のジョブ `verify` で、二種類の既存幾何検証・第三C++終局検証・C++改変拒否がすべて成功。再現手順は `research/experiments/n11-s9-n19-terminal-20261027/README.md`。

今回の新規WIN/LOSS証明0件、7石・5石・二石root閉鎖0件。全4,089類の8石WIN集合や上流の他証明をC++で一括再証明したわけではない。条件付き14根計画の未証明辺は250本のまま。**標準11×11空盤UNKNOWN**。
