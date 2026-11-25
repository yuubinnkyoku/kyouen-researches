# 2026-10-26：14根計画の8石WINを終局証明し、未証明義務を1類削減

開始時main `9b820a6770c7b1caf0b73fbab75ff6dfea00adfd`。AGENTS.md、knowledge README、K0023・K0417・K0426、直近の5石27子／7石14根計画、独立8石終局証明、既存df-pn・s5 cache・s4 manifestの信頼境界を確認。標準11×11・元先手固定視点、空盤UNKNOWN。

最適化済み14根 `s7-plan14-remaining.keys` の合法8石子から、合法9石子が19類と比較的少ない根 `00000000000000821090a00000000020` を選んだ。元先手WINの9石証人 `000000000000408210a8400000000020` を発見。合法10石子13類をすべて終局まで再計算し、13類すべて元先手WINだったため、8石根の元先手WINが成立する。

証明書は `research/experiments/n11-s8-plan14-win13-20261026/s10-win13.keys`。独立3×3・4×4整数幾何で8→9→10の合法性・全称境界と13葉の終局minimaxを再計算し、両実装とも各葉の状態数 [57,68,23,41,17,40,22,39,28,13,36,21,59]、合計464で一致。改変拒否4件も成功。旧cacheを終局葉として信用していない。

この8石根は現行14根のうち7石候補 `00000000000000821090200000000020` に属する。既存証明限定8石WIN2,176類には含まれず、既知8石LOSSとも衝突しないことを新しいNode.js監査で確認する。**固定済み14根計画**の未証明7→8辺は536→535、相異なる未証明8石子は536→535へ1減る。再最適化後の最適値は未検証であり、535を厳密最適値とは呼ばない。

再現：
```sh
python3 research/experiments/n11-s8-plan14-win13-20261026/verify.py --negative
node research/experiments/n11-s8-plan14-win13-20261026/audit_plan_progress.js --negative
```

新規8石WIN証明1件、7石WIN閉鎖0件、5石閉鎖0件、二石root閉鎖0件。**標準11×11空盤UNKNOWN**。

専用CI [40338497955](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40338497955) は **success**（Pythonの二独立整数幾何・終局minimax・改変拒否、Node.jsの既存証明限定集合との非重複・衝突拒否・535辺への減少を検査）。
