# 2026-10-27：20子9石WIN80類のC++第三独立終局検証と単独監査修正

最新main、AGENTS.md、knowledge README、K0023/K0105/K0329、11×11の9石証明・14根再最適化・研究記録を確認。開始時点の既知状況は証明限定8石WIN4,089類、保存14根の証明済み298/548辺、条件付き最小未証明250辺。標準11×11空盤勝敗はUNKNOWN。

`research/experiments/n11-s9-n20-terminal-20261027/independent_terminal.cpp` を追加。既存JavaScriptと異なるC++17の整数4×4余因子展開、独立D4正準化、9石根の安全性、8石逆親の合法性、全9→10石合法手、10石以降の禁止2・3・4点集合に基づく完全再帰を実装。保存済み勝敗表や未完探索は使わない。

検証結果は9石WIN80類、8石WIN逆親689類、9→10石着手1,600本、相異なる10石WIN葉1,573類、終局探索状態数157,557。既存の二種類の整数幾何と一致。証明書の根・状態数・UNKNOWNヘッダ・行数を改変した4件をすべて拒否。安全性検査追加後の専用CI [40459371257](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40459371257) 成功。

`research/experiments/n11-s5-post-n20-matching-20261027/audit.js` で新規9石証人を `terminal:false` のまま8石WINに逆伝播できた単独監査の信頼境界を修正し、`terminal:true` の終局再計算を必須化。再最適化CI [40459371394](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40459371394) でも成功。

これは80類の既存局所証明の独立検証と監査の重要修正であり、新規WIN/LOSS分類ではない。上流の全証明集合をC++で一括再証明したわけではない。証明限定8石WIN4,089類、条件付き14根の未証明辺250本、7石・5石・二石root新規閉鎖0件。**標準11×11空盤勝敗UNKNOWN**。
