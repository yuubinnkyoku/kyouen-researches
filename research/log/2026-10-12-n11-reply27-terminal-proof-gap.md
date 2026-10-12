# 2026-10-12: `{60,27}` のterminal-only proof依存数とpilot順

K0414の119/119 LOSS witness tableで使用した32 S4 LOSS classの全S5境界を独立Boardで再生成した。3,297 edgesは2,995 unique S5 LOSS rootsに集約され、現行exact cacheでは65行にdirect `nodes>0`（合計388,074,801 nodes）、2,930行に `nodes=0` が記録されていた。

K0378の終局only 6-root DAGと交差する対象rootは3。従って別root2,992件は今回調べた既存証明DAGには閉じられていない。K0375/K0377の現S4配下三根と、K0372の独立10,407-node S6 WIN証明・validator資産の適用範囲を分けて記録した。

巨大proof captureは起動せず、direct solver node数の低・中・高3根と `nodes=0` の合法手数70/94/110の3根をpilot候補として順位付けした。次段階でproof node/edge/terminal、RSS、bytesを実測するための選定であり、node数から証明容量を外挿しない。

再現結果とSHAは [terminal proof experiment](../experiments/n11-reply27-terminal-proof-priority-20261012/README.md) に保存した。現119/119結論はsolver-trusted leavesを使用し、terminal-only independent minimax DAGには未到達。
