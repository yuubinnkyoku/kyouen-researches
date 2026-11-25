# 2026-11-15：cost-65l/74g/69i 3-way fork解消 — 統合head 1277/6570/518896/4840/382619・第三target S5 0/0閉鎖を維持・65l-vs-69i・74g-vs-69iクロスroot disjointness raw+D4で初検証・11×11はUNKNOWN

開始時main: `dde42161`直前（本merge script着地時）。head 1257（cost-73h）を共通forkとする**3本の並走receipt fold**がmainに着地し、canonical chainがforkしていた:

- **chain A（自レーン）**: cost-65l（2 WIN7-D10 receipts bits [21,48]・child `00000000220000003800000000000200`）→ head **1261**/6586/520097/4856/383820（commit `97d99a11`）
- **chain B（並走）**: cost-74g（10 WIN7-D10 receipts bits [4,11,20,44,69,95,100,108,109,116]・第三target S5のcost-74行child `00000000000000809142000000000000`）→ head **1266**/6581/519710/4851/383433
- **chain C（並走）**: cost-69i（4 WIN7-D10 receipts bits [21,29,97,100]・第三target S5の**最終行** child `00000000000000809102000000002000`・1266ベースでfold）→ head **1273**/6574/519179/4844/382902（commit `79d866f8`・**第三target S5 1/69 → 0/0閉鎖**）

A+Bは前回 `5ac44005` で2-way merge済み（head **1270**）。しかしCは1266 fork脚から着地したため65lの2 receiptsを含まず、**1270 vs 1273のfork**が残っていた（69i lane自身が「cost65l must be merged with this 1266-based chain by the next unified fold」とhead JSONに明記）。

## 3-way merge script（`recompute_frontier_merged_cost65l_74g_69i_20261115.py`）

78a+69h前例・65l/74g merge scriptの方式を3-wayに拡張:

1. **fork 1257をrunpyで1回だけbyte-identical再現**（73h head JSON blob `71f79b4b`検証・532 folded roots）。
2. **4つの出版head JSONをgit blob shaで検証**: 65l `0b523e70`（9,260B）・74g `fce4ce77`（12,590B）・69i `8692a7a6`（9,103B）・2-way merged-AB `02109530`（12,459B・head 1270数値を再assert）。
3. **16 receipt roots（2+10+4）の相互disjointness raw+D4**: **65l-vs-69iと74g-vs-69iはどの出版foldも共通baselineからは検証できなかったペア**（69iは自身のbaseline 542 roots＝532+74g分に対してのみ検証しており65l rootsを含まない）。全ペア（A-B/A-C/B-C）raw・D4とも重複なし・532 folded rootsとも重複なし・16 D4 orbit distinct。
4. **3 chainをforkから正確再導出**: A → 1261（per-bit marginals published一致）・B → 1266（同）・CはBの上にreplay → **1273**（per-bit marginals published一致・child bit21閉鎖・第三target 0/0制御・parent2 69/5265・parent3 79/6427行再現）。
5. **pairwise covers overlapを列挙**: A-B 0・**A-C 0**・**B-C 3**（`00000000000000809102000000001000`・`00000000000000809102000000200000`・`00000000000000809102000020000000`）。B-C重複の3行はいずれも**74g foldで既にsolved済み**の行であり、69iのpublished marginals（sB基準で計算）には元々含まれない — したがって**chain-C marginal deltas vs published: none**（統合replayでも65l→74g→69i順で69iの全4 receiptのmarginalがpublishedと完全一致）。重複はunion簿記として正しく一重計上される。
6. **統合逐次replay（65l → 74g → 69i）**: total marginal 78（=65l 10 + 74g 49 + 69i 19）・marginal_in_manifest 20（=4+9+7）。3 child closures（65l bit21・74g bit4・69i bit21）各1回ずつ。set等式: `s_merged == union(s_1261, s_1266, s_1273) == s_1257 ∪ covers(16 roots)`。
7. **逆順replay（69i → 74g → 65l）同一集合**（commutativity control）。
8. **merged head per-parent行会計**: 第二target 17/1325・class-4 lift親 75/5519・**第三target 0/0（CLOSED）**・74g第2親 55/4143・69i第2親 69/5265・69i第3親（class-4）79/6427。

## 統合head

**solved 1277 / unique 6570 / cost 518,896 / open 4840 / open_cost 382,619**（1257 + 4 + 9 + 7 = 1277）。head JSON [class-frontier-merged-cost65l-74g-69i-recompute-20261115.json](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-merged-cost65l-74g-69i-recompute-20261115.json)・ranking/top-candidates CSVs・merge scriptをpush（commit `dde42161`・4ファイルremote raw CDN cmp照合OK）。**3回連続実行で全出力byte-identical**。

branch head 3個（1261・1266・1273）と2-way merged head 1270はいずれも1257 forkの有効な独立foldのまま残るが、**正準継続は1277のみ**。以後のfoldはすべて1277 baselineをassertしてからrebaseすること。

## 第三target S5閉鎖の意味と限界

69i receiptsにより第三coverable class-2 target S5 `00000000000000809102000000000000`の残行が0となった。標準even-OR/odd-AND規約のもとで「6石childrenがすべて先手WIN」ならS5自身が先手WINであり、**class-2 blockerが条件付きで閉鎖**される — これはmanifest被覆簿記に基づく条件付きclosureであり、blocker全体の独立証明ではない。REFUTED-D10はLOSS証明でなく、WIN7証明書は個別7石rootの深さ10以内の先手勝ちのみを証明する。solved 1277はmanifest被覆の簿記であり勝敗ではない。

次のtarget: **第二coverable class-2 target S5 `00000000000000801202000000200000`（17行/1325・best coverable class-2）**の次行cost-75 `00000000000040801202000000200000`（c1=0, c2=1, c4=0）、およびclass-4 blocker S5（18行/1460）のcost-80行2本。cost-69g/65j/74eの並走claimは未着地のまま要再確認。

**標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class1・class2・class4はすべてUNKNOWN**。

## 成果物

- merge script: [recompute_frontier_merged_cost65l_74g_69i_20261115.py](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_merged_cost65l_74g_69i_20261115.py)
- 統合head JSON: [class-frontier-merged-cost65l-74g-69i-recompute-20261115.json](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-merged-cost65l-74g-69i-recompute-20261115.json)
- ranking CSV: [class-frontier-s5-ranking-after-merged-cost65l-74g-69i-20261115.csv](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-s5-ranking-after-merged-cost65l-74g-69i-20261115.csv)
- top-candidates CSV: [class-frontier-top-candidates-s6-after-merged-cost65l-74g-69i-20261115.csv](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-top-candidates-s6-after-merged-cost65l-74g-69i-20261115.csv)
