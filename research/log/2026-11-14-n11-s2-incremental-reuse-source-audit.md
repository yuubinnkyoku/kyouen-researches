# 2026-11-14 n11 S2 {59,60}: incremental WIN7 reuse の独立監査

Audit base: `main` = `24b89f40b73622be83acc1d013ecd6d11500217a` (2026-11-14 21:09 JST 時点)。

`AGENTS.md`、`research/knowledge/README.md`、SCHEMA / VOCABULARY、K0023、K0783、milestone-5 reuse experiment README、incremental reuse script / JSON、関連receiptを確認した。

## 独立再計算

S6 worklist part 1..6、4つの新規WIN7 manifest、baselineの3 receiptを読み、D4の8変換と整数座標の4点共線・共円判定を別実装で再計算した。大きな `s6sweep/verified.json` と `sweep_results.json` はGitHubファイル取得関数が本文を返さなかったが、rawファイル取得では全内容を読み取れた。以前の「0 byte」という判定は取得器の制限による誤りであり、ここで訂正する。

### K0675 baseline

- `sweep_results.json`: **3,868 S6**、WIN-for-mover **3,854**、LOSS-for-mover **14**、timeout **0**、試行 **29,680**、勝ち子を持つS6 **3,854**。
- `s6sweep/verified.json`: **4,288 receipt**（WIN7 **3,401** / LOSS7 **887**）、fails **0**。
- focus2154 / frontier2140を合わせた全baseline receipt union: WIN7 **4,052** / LOSS7 **2,699**、相互conflict **0**。

### 23新規WIN7 rootの親への再利用

- S6 worklist: **7,867行・重複なし・合法七石目候補cost 615,497**。
- 新規WIN7 manifest: **23件**（cost-69c:1、70b:1、71:2、75:19）。D4正規化後も23 rootすべて相異なり、7石で、独立整数幾何判定を通過。
- 新規rootとbaseline WIN7 / LOSS7 receiptの重複・conflict: **0 / 0**。
- baseline WIN7から閉じるS6親: **498**、削減cost **38,387**、残 **7,369親・cost577,110**。
- 新規23 rootからの親子incidence: **70組・48親**。うちbaselineで既に閉じていた親 **5**、増分 **43親**。
- 増分43親のcost **3,275**、class内訳 **1:3 / 2:35 / 3:5**。
- union後: **541親**、残 **7,326親・cost573,835**。

保存JSONの48 parent record、各子root集合、43件の `incremental_parent_hex`、cost/class集計は再計算結果と一致した。したがって、前回記録した43親・cost3,275の増分はbaselineを含めて再現できた。

## 残る再現性の注意

現在の `audit_incremental_class2_win7_reuse.py` と保存JSONは出力schemaが一致しない。スクリプトは `inputs`、`already_covered_by_baseline` を書くが、保存JSONは `input`、`already_in_baseline` を持ち、さらに `checks.worklist_unique` を含む。数値と親子集合は独立再計算で一致したものの、保存JSONが現在のスクリプトからそのまま生成されたことは確認できない。再現器と出力schemaを次回統一する余地がある。

証明書本体23件は今回再実行していない。WIN7判定は公開manifestと既存独立検証記録を前提にし、今回新たに検査したのはrootの幾何安全性、D4正規形、baselineとの重複/conflict、親への再利用である。

この監査はS6 worklistの閉鎖数を更新するもので、S2 {59,60}、二石root {49,60}、標準11×11空盤の勝敗を決めない。これらは引き続き **UNKNOWN**。
