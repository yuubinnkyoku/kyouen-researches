# 2026-10-29: 分割グラフの全終局着手列の計数と鋭い交差辺数別上下界

[直前の終局長集合・r人最終着手者分類](../experiments/game-structure/split-cyclic-r-player-terminal-residues-20261029/README.md)は、到達可能な終局長を分類していたが、同じ長さに到達する着手順序の数は未分類だった。極大独立集合 M_c={c}∪(I\N(c)) と、存在条件付きの I を用い、各集合の全順列がちょうど終局着手列となることから、長さ別母関数を全称証明した。

さらに交差辺数 E を固定し、全終局着手列総数の**鋭い最小・最大**を、中心次数0の有無で2クラスに分けて離散凸性から導出した。辺追加による総着手列数の非増加も証明。多人数の「全着手列を等確率とした最終着手者の分布」まで計算できるが、各局面での一様ランダム着手や最適戦略を表すものではない。

[定理・証明・実行手順](../experiments/game-structure/split-terminal-sequence-extrema-20261029/README.md)と[全着手再帰C++検証器](../experiments/game-structure/split-terminal-sequence-extrema-20261029/verify.cpp)、[極大集合直接列挙Python検証器](../experiments/game-structure/split-terminal-sequence-extrema-20261029/verify_independent.py)を追加。

- C++: k,m≤5、km≤16、k+m≤10の142,613個を全列挙。長さ別係数一致、187交差辺数階級の厳密最小最大一致、全件の終局列数総和15,848,017。g++ -O2 -Wall -Wextra -Werror -pedantic でコンパイルし実行成功。
- Python: 別方式で1,439個のラベル付きグラフを照合し、不一致0。
- 証明は有限検証に依存しない。共円盤の幾何学的実現性と一般r人最適戦略は未確定。
- 長期11×11のroot探索は実行していない。knowledge正本への昇格と全体CIは未実施。AGENTS.mdに従い生成物は手編集していない。
