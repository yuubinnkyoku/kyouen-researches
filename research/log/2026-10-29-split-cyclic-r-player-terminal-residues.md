# 2026-10-29 高速研究：分割グラフの全終局長と巡回 r 人の最終着手者

作業開始時に main、AGENTS.md、research/knowledge/README.md、generated/summary.md を確認。既存の split-graph-parity-classification-20261029、K0305、K0336、positive-private-leaves-arbitrary-missing-20261028 等を調べ、二人通常プレイのGrundy二値性と重複しない r 人終局同余問題を選択した。

分割グラフの全極大独立集合を中心 c ごとの M_c と、条件付きの独立集合 I に分類することで、終局手数の集合・度数分布・最小最大を数学的に完全決定。r≥2 の巡回着手・最終着手者のみ勝ちという明示ルールでは、全ての進行で勝者が固定される条件が「全中心の独立側次数が1 mod r」または「全中心の独立側次数が0 mod rで零次数中心が存在」の二場合に限られると証明した。r=2 は既存のGrundy二値性定理の条件と一致するが、r≥3 の結論は別の一般化である。

独立の二方式（全部分集合の極大独立集合判定と閉近傍削除による全終局手数再帰）を実装し、k,m≤4 と (3,5),(5,3) のラベル付き140,499構成を全件照合。r=2..6 の判定不一致0。r=3 で異なる終局長3,6を持ちながら最終着手者が同じになる9頂点証人も確認。

一次資料: research/experiments/game-structure/split-cyclic-r-player-terminal-residues-20261029/README.md と verify.py。長時間11×11 root探索なし。これは抽象二点禁止ゲームに限り、r人の最善戦略や格子実現を含まない。knowledge正本への昇格は生成器と全体検査を実行できる環境で後日検討する。
