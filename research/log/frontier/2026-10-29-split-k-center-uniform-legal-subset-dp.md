# 高速レーン：分割グラフ k 中心の一様合法着手（2026-10-29）

- 最新 main の AGENTS.md、research/knowledge/README.md、generated/summary.md、関連する二中心一様合法着手・終局列計数・多人数終局の研究を確認。11×11 の重い root 探索は行っていない。
- 二中心の交差数による公式を、任意の中心数 k に一般化。中心近傍の全部分集合和集合サイズ U(S) だけから、中心 c を選ぶ確率と中心を選ばない確率を O(k²2^k) 回の厳密有理数演算で求める部分集合再帰を導出。
- 乱順列の貪欲独立集合と逐次一様合法着手の同分布性、中心 c が採用されるための E_c 事象、優先順位積分、包除原理を用いて全称証明。証明は有限実験に依存しない。
- 三中心の構成で、中心次数・全ての二中心共通近傍数が同じでも、三重交差が違うと中心なし終局確率が 1/3 と 12/35 に分かれることを厳密に示した。
- 独立した閉近傍削除再帰で全11,535構成、全優先順位順列による貪欲再帰で1,295構成、二中心既存閉形式で1,365構成を照合。不一致0。実行コマンド：python3 research/experiments/game-structure/split-k-center-uniform-legal-subset-dp-20261029/verify.py。
- 証明・再現コード：research/experiments/game-structure/split-k-center-uniform-legal-subset-dp-20261029/README.md、同ディレクトリ verify.py。branch / PR なしで main に直接追加。
- 限界：抽象分割グラフの確率モデルであり、共円格子残局での実現可能性と多人数の最適戦略は未確定。knowledge 正本への昇格、生成物更新、全体CIは未実施。
