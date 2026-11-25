# 2026-11-18 n11 cost76c記録 parent B エントリのadditive amendment

## 背景

fold-chain ledger crosscheck(commit `aa3af62b`、`fold-chain-ledger-1410-1476-crosscheck-20261118.json` blob `e8785d509e8a11a37c0d03cc450455a14708c34d`)は、歴史fold記録 `class-frontier-cost76c-receipts-recompute-20261117.json` の parent B(`00000000000000801202000000040000`)エントリが77e行(`00000000040000809002000000004000`・cost76d77e foldでhead-1452に閉鎖済み)をpost-cost64h baselineに対して再度lostとして計上していることを検出した(前回の検証側logに提案のみ記録し、並走の対応待ちとしていた)。

今回mainを確認した結果、並走は head-1476 census log(commit `658597f0`)で当該誤記を認識し「本再計算では誤記されたBのafter値を使わず」と対応したが、**記録ファイル自体は2026-11-17T03:58Zの初回出版以降未修正のまま**だった。よって検証側がadditive amendmentとして修正値を同ファイルに添付した。

## amendmentの内容

- top-level に `amendment_20261118` を追加し、元記録の全fieldは**一字も変更していない**(歴史記録の保存)。
- 修正値(corrected_entry): B は cost64d(2行)→cost76d77e(77e行)→cost64h(1行)の後、**本foldでは行を失わない**。chain-correct な値は `rows_after` 70 / `edge_cost_after` 5,802 / `lost_rows` 0 / `lost_edge_cost` 0(出版記録は 69 / 5,725 / 1 / 77)。76c WIN行のD4 childrenは parent P(`00000000000000003800000208000000`)と E(`00000000000000801202000100000000`)のみで、Bは含まれない(ledger crosscheckの直接計算による)。
- aggregate fieldの読み替えも同amendmentに明記: `parent_edge_cost_delta` 458 は spurious 77を含むので chain-correct な76c marginal per-parent値は **381**、`parent_row_incidences` 6 → **5**。
- 大域head算術(1473/6,375/504,596)への影響なし(foldは1行をちょうど1回閉じる。ledger crosscheck 57/57 checksで確認済み)。

## 実験的事実

- hex定数の転記はrepr/len込みの機械注入で行った(parent B key 32文字・rank-1 parent とは1ビット配置が異なる別parentであり、目視比較は不可)。
- amendment挿入は書式保存(textual insert)で行い、元ファイルの全行がverbatimで残ることを機械検証した。amendment後のJSONは `json.loads` で正常にparseし、元fieldの値(誤記込み)が保存されていることを確認。

## 解釈境界

- REFUTED-D10はLOSS証明ではない。STERILEもLOSS証明ではない。
- 標準11×11空盤、二石root `{49,60}` / `{59,60}`、S2 `{59,60}`、class 1/2/4はすべて**UNKNOWN**のまま。
