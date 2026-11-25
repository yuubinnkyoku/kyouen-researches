# 2026-10-29: N11第19回の証明限定12候補を固定し、独立幾何監査

最新main、AGENTS.md、research/knowledge/README.md、K0023、11×11の第18回までの証明・実験・logを確認した。空盤勝敗はUNKNOWNのまま。

第18回後の再計画CI [40807697423](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40807697423)は成功。成果物 `n11-round18-replan`（artifact 12869540624、ZIP SHA-256 `1ff023be55065ca65cf17345225dd610d7db293de484a92dfe0613092d53e420`）を取得し、`research/experiments/n11-s9-post-round18-replan-20261029/next-plan.json` に固定した。前回の未証明9石候補116類から、第18回証明と10石LOSS証人由来の親閉包で18類を除外し98類、残り44本の未証明辺に接続しない5類を除外して**93類**。支配関係を除くと**12類**、選択数12、潜在被覆12。WIN/LOSS衝突0。選択鍵のSHA-256は `564a47bb41339d9fb665536faccd697ed7ce7fac6ec83b3ccbe5e616f3dace2c`。

別実装の `preflight_independent.py` で、12局面が安全な9石・D4正規代表であることを検査。各空点の合法性を3×3差分行列式と独立した4×4整数行列式（24項の置換展開）で照合した。4点判定114,408件、合法10石子**329本**、D4で異なる10石子**329類**、候補間重複0。内訳は25,25,27,27,27,27,28,28,28,29,29,29。検査結果は `preflight.json` に固定。計算を独立に再現するCIは [N11 round19 independent boundary preflight](https://github.com/yuubinnkyoku/kyouen-researches/actions/workflows/n11-s9-post-round18-preflight.yml)。

本回の確定した改善は、次の証明探索候補を116→93→12類へ絞り、12類の合法境界を独立整数幾何で照合したこと。これは候補選択と合法手の証明であり、9石WIN/LOSSの新証明ではない。証明限定8石WINは5,803類、固定14根計画の未証明辺は44本、新規二石root閉鎖0。新たな終局探索を漫然と起動していない。

**標準11×11空盤の勝敗はUNKNOWN。**
