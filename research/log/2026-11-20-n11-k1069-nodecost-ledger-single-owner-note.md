# n11 長期レーン: K1069 nodeコスト台帳の完全再導出: 単一オーナー宣言ノート（2026-11-20）

K1069 39-live witness depth-10掃引は正本で要約統計（総nodes 169,615,508・最大probe 14,249,420・
WIN 1/REFUTED 38/CAPPED 0・順序矛盾0）とroot→ラベル分類のみを出版しており、**per-probe node数の
台帳は出版されていない**。二石rootへ向かう供給判断（root別コスト分布・depth延長見積・証明掃引の
順序設計）にはroot別node数が必要である。本レーンが以下を単一オーナーとして実行することを宣言する:

1. 対象: K1069正本（SHA-256 22953ae1…）のclassification全39根（38 REFUTED-D10 + 1 WIN7-D10）。
   各根の(child, bit)は生child hex規約（child=root−最小セットビット）で機械再導出する。
2. プロトコル: runner v17固定コピー（git blob c132cc64…）・cap 30M・timeout 280s・両AND順序・
   pilot_d6制御必須・逐次・depth 10・計78 probe。**判定は一切行わない**（全根のdepth-10判定は
   K1069で出版済み）。
3. gate: (a) K1069正本SHA pin・membershi 39根・(b) 78 probe完走・pilot_d6制御・(c) 出版済み
   per-probe値（max_probe root=00000000…のandclose0 14,249,420・WIN両順序1,576,372/2,544,178）の
   厳密一致・(d) 3根×2順序の再測定がdepth-11測定標本拡張正本（8a584be6…）とも一致・
   (e) **再導出総和nodesがK1069 summaryの169,615,508と厳密一致**・(f) loss値が分類ラベル
   （REFUTED-D10は両順序loss=false・WIN7-D10は両順序loss=true）と全根で一致。
   いずれかの不一致はfail-closed（その場合は不一致の内容自体が知見として記録される）。
4. 出力: `research/experiments/n11-k1069-nodecost-ledger-20261120/`（per-probe台帳正本+統計）。

この再導出は出版済み判定の検証とコスト台帳生成であり、REFUTED-D10の意味を変えない。
36-root fresh witness掃引本体（掃引オーナーレーン実行中）・fresh-unsafe census（宣言済み）には
着手しない。**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて
UNKNOWN のまま。REFUTED-D10 は LOSS 証明ではない。**（確認時HEAD: 2db12bdcc0）
