# 2026-11-05 11x11 角代表 v=0（--memo=30・7200s）のタイムアウト実績

対象: 標準 q=4・完全指摘・通常プレイの 11x11 空盤、角初手 v=0。
実行: `cpp/solvers/kyouen_solver_11_root.cpp`, `/tmp/kys11 --reps --memo=30 --only=0 --budget=7200`
環境: WSL Ubuntu, 16 cores, RAM 19GiB, D: 空き約 945GB

## 結果（7200s 天井到達）
- outcome: done=0 timeout=1（TIME_BUDGET、勝敗未確定）
- visited total 1,282,408,448（約1.28B、中央60の --memo=29 377M から約 3.4 倍、d14-d15 で 690M 集中）
- memo 1,065,861,580/1,073,741,824、hit率 24.82%、avgprobe 7.58、evict 216,546,854
- loss_cut_cached 481,534,658 / loss_cut_rec 400,436,888、cached_cut_frac 54.60%

## 解釈
角初手でも全11x11（21 D4代表）中で中でも軽くない（中央よりは軽いが240s では 57.7M visited）。
7200s でも勝敗は決まらず、memo はほぼ一杯（1,065M）まで進んだが depth 21 まで枯渇した。
memowise 余裕度は --memo=31（約2B スロット）が必要で、WSL 19GiB + swap 5.0GB で逼迫する。
後続案として、RAMの他用途を落とした状態で --memo=31・7200s を1プロセスで全力実行するか、
実行する初手の数を減らす（影響なし）かになる。
