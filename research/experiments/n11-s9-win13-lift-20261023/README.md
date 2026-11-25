# 11×11：13終局WIN葉から9石WINを独立証明し、8石WINを9局面へ伝播

対象は標準11×11・完全指摘・通常プレイ、元先手固定視点。

9石局面 `00040000400000821084000002000020` は **WIN**。この局面からの合法な正準10石子は **13件**で、すべて終局まで独立に計算してWINと確認した。9石は奇数石ANDなので、全子WINから9石WINを導く。石を一つ除いた正準8石親は **9件**で、各8石は偶数石ORなので、この9石WIN子が一つあればWINと導ける。

9件中8件は既存 `n11-targeted-terminal-lift-20261015/data/lifted_s8_win_51571.txt`（13,501件、Git blob `80859e805287d55d3c43effa850f0629d44cb4c0`）には未収録。残る1件 `00040000400000821080000002000020` は既収録。既存 `all_s8_loss_294.txt`（Git blob `dd069f2800a7c803c7deab211e6af817399b5a93`）との重複は0。これは指定した旧一覧との差分であり、全研究資産との未重複を保証しない。

## 再現

repoルートから：

```sh
python3 research/experiments/n11-s9-win13-lift-20261023/verify.py
python3 -O research/experiments/n11-s9-win13-lift-20261023/verify.py
g++ -std=c++17 -O2 research/experiments/n11-targeted-terminal-lift-20261015/scripts/solve_s10_candidates.cpp -o /tmp/n11-s10-check
/tmp/n11-s10-check research/experiments/n11-s9-win13-lift-20261023/s10-keys.txt /tmp/n11-s10-check.tsv
diff -u research/experiments/n11-s9-win13-lift-20261023/s10-cpp.tsv /tmp/n11-s10-check.tsv
```

Pythonは既存 `n11-s8-to-s7-lift238-20261020/terminal_geometry.py` の3×3整数行列式・全合法境界・終局minimaxを使用。C++は独立した4×4整数行列式。solver/cacheの勝敗は使用しない。13葉の個別終局再帰状態数合計は557（共有表状態数ではない）。

この証明だけで7石WIN、二石root、空盤勝敗は閉じない。**11×11空盤はUNKNOWN。**
