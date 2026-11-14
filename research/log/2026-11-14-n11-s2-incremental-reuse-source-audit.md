# 2026-11-14 n11 S2 {59,60}: incremental WIN7 reuse の再現性監査

Audit base: `main` = `24b89f40b73622be83acc1d013ecd6d11500217a` (2026-11-14 21:09 JST 時点)。

`AGENTS.md`、`research/knowledge/README.md`、K0023、K0783、milestone-5 reuse experiment README、incremental reuse script / JSON、関連 receipt を確認した。

## 独立に再計算できた範囲

入力は現在 main の S6 manifest part 1..6、cost-69c / 70b / 71 / 75 の4つの WIN7 manifest、incremental reuse JSON。D4 の8変換と整数座標の4点共線・共円判定を別実装で再計算した。

- S6 worklist: **7,867行・重複なし・合法七石目候補コスト615,497**。
- 新規WIN7 manifest: **23件**（1 + 1 + 2 + 19）。D4正規化後も23 rootすべて相異なり、7石で、整数幾何判定を通過。
- 23 root からの親子 incidence: **70組・48個の異なるS6 worklist親**。
- 保存済み `new_parent_records` は、再計算した48親と各親の子root集合に完全一致。cost / classes もworklistと一致。
- JSONで baseline 未被覆と記された43親は、`incremental_parent_hex` と完全一致し、cost合計 **3,275**、class内訳 **1:3 / 2:35 / 3:5**。
- 残っている baseline receipt 2ファイル（focus2154: 62鍵、frontier2140: 2,401鍵）との照合では、新規23 rootの重複・LOSS7 conflictは **0件**。

ここまでは独立再計算できた。ただし「43親が本当にbaseline未被覆」という分類は、次の欠落により完全には再検証できない。

## 再現性の欠落

1. `research/experiments/n11-central-19-cover-20261031/output/s6sweep/verified.json` は現在 main で **0 byte**（Git blob SHA `a60a7881001c762be3ca604096a9357115f796ab`）。同じ `s6sweep/sweep_results.json` も0 byte。K0675と `win7-reuse-audit.json` は前者を4,288件（WIN7 3,401 / LOSS7 887）の監査receiptとして参照し、その非空内容のSHA-256を `f647a6c2837328b054a3a691ae0da6668ea3063177ea02bc5877dc76df88674f` と記録しているが、現checkoutからその内容を取得できない。
2. 残るfocus2154 / frontier2140のreceiptは合計2,463鍵（WIN7 651 / LOSS7 1,812）にとどまり、baseline全体として記録されたWIN7 4,052 / LOSS7 2,699を再構成できない。したがって48親のうち5親を「baselineで既に被覆」とした判定、baseline 498親、合計541親、残7,326親・cost573,835は今回独立に再確定していない。
3. 現在の `audit_incremental_class2_win7_reuse.py` は空の `s6sweep/verified.json` を `json.loads` するため、clean checkoutでは先へ進めない。また、現スクリプトは出力に `inputs`（複数形）を書き、`checks.worklist_unique` を出さない一方、保存JSONは `input`（単数形）と `worklist_unique` を含む。保存JSONが現在のスクリプトからそのまま生成されたことも確認できない。

## 評価と次の要件

- **確認済み**: 23新規rootの幾何安全性、70 incidence、48親、保存JSONの親・子対応、43件の「新規」フラグとcost/class集計の内部整合性。
- **未再確認**: baseline receiptとの重複5件、541親・残7,326親・cost573,835という全体差分。43件の分類は保存JSONのbaselineフラグを入力としている。
- **未実施**: 23個のWIN7証明書本体の再実行。WIN7 verdictは既存manifest・検証記録を前提にした。
- 次に全体差分を確定するには、4,288件の元receiptを復元するか、K0675のS6 sweep結果から同じ鍵集合を再生成し、SHA-256を照合してからincremental auditを現main上で再実行する必要がある。

この監査はworklist accountingと再現性の評価であり、S2 {59,60}、二石root {49,60}、11×11空盤の勝敗を決めない。これらは引き続き **UNKNOWN**。
