# 2026-11-17：cost64d・cost64g両行のv17全行再検査（過去lane再検査キュー第3弾）— 64+59 bit全フィールド一致・完全非飽和・verdict反転0

開始時の最新mainは `427e29fa450482dc5572cdc33a66527a4040f1e9`。cost65n（`cee2fdc8`）・cost66c（`96b323c0`）に続き、fbt飽和欠陥logが挙げた過去lane再検査キューのうち、head-1452構成行で未実施だった **cost-64d**（head-1419最良own-closable行）と **cost-64g**（head-1438 census最安open行）の2行を、fbt修復済みv17 engineで初めて全行再検査した。cost64h fold receiptは本エントリ時点でも未着地（並走claim済み・着手禁止）。

## 出発点

64dはchild `00000000000000403800000008002000`・64 swept bit（WIN7-D10 23 bits〔manifest `244e4b61`で証明書二重検証済み〕・REFUTED-D10 41・capped 0・総nodes 64,291,757）。64gはchild `00000000000100003800000008080000`・59 swept bit（D4転写5 bits含む・WIN7-D10 bit 89〔証明書検証済み〕・REFUTED-D10 58・capped 0・総nodes 33,505,865）。2行ともper-bit最大nodesは64d bit 98の3,457,163・64g bit 89の3,672,017で、76c bit 113（~8.2M・飽和）より大幅に小さいが、66c bit 117（3.12M・軽微飽和）と同規模のため検査対象とした。

## 実施内容

fbt修復済みv17 engine（blob `c132cc64`）で両行の全swept bit（64d 64 bits・64g 59 bits）を出版時と同一のbatch分割（各8バッチ）・depth 10・cap 1e9（出版行は2行とも0 capped・cap不発動）・`--andclose 1`・候補ごとengine完全reset・pilot_d6制御付きで再実行し、出版raw batches 1-8（blob SHA pin照合済み: 64d 8本・64g 8本）と全フィールド（loss・nodes・capped・terminalStoneRange・andclose）比較した。監査script `verify_cost64d64g_v17_full_row_rechecks_20261117.py`（stdlibのみ・43 checks）を2回実行し、監査JSONがbyte-identicalであることを確認した。

## 結果

- **64d: 64/64 bit全フィールド一致**。WIN 23 bits（0/1/2/11/16/30/32/43/53/66/69/75/79/86/92/95/98/106/107/109/111/113/120）全不変。nodes総和64,291,757完全一致。
- **64g: 59/59 bit全フィールド一致**。WIN bit 89不変。nodes総和33,505,865完全一致。
- **verdict反転0件・capped 0・pilot 16/16（3402・両行×8バッチ）**。node数不一致0のため飽和検出の必要なし: 両行とも**完全fb非飽和**と確定。
- 43 checks全PASS・2回実行決定的。

## 含意

1. 64dのREFUTED-D10 41 bit・64gのREFUTED-D10 58 bitはplanning証拠として有効（engine-consistencyの簿記確定）。
2. 64d fold（head 1419→1435）・64g fold（head 1438→1441）の基盤は無影響。head-1452構成行のうち本2行のv17裏付けが完了。
3. 非飽和実績のしきい値情報: 65n（5,654,046 nodes/bit非飽和）・66c bit 30（8.8M非飽和）に加え、64d/64gは全bit一致で非飽和。3.4M未満の行はnode数不一致なし、という傾向データが増えたが、node数による事前飽和判定は不可能というfbt logの結論は不変（検出器はv17 node数不一致のみ）。
4. 過去lane再検査キューの残りは76d・77e（バッチ実行中）・64f（未着手）・65f/65j/60c（v15由来のためnode-exact比較不能、別方式が必要）。

## 保存物

- 監査script: `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/verify_cost64d64g_v17_full_row_rechecks_20261117.py`（stdlibのみ・入力blob SHA pin照合・engine blob pin照合・43 checks・2回実行byte-identical）
- 監査JSON: `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost64d64g-v17-full-row-rechecks-20261117.json`
- v17生記録: 同output/配下 `class2-lane-cost64d-v17-recheck-batch{1..8}-20261117.jsonl`・`class2-lane-cost64g-v17-recheck-batch{1..8}-20261117.jsonl`（計16本）
- 入力（出版済み・blob pin照合済）: `class2-lane-cost64d-raw-batch{1..8}-20261116.jsonl`（`0f93456c`/`c41d88f1`/`d45d8cfa`/`bba937a0`/`12a379c4`/`a0d86791`/`6d34099b`/`ce86d0fb`）・`class2-lane-cost64g-raw-batch{1..8}-20261116.jsonl`（`873807ad`/`e9b0b41b`/`f22888df`/`a8ba871f`/`07809fd4`/`13088f70`/`fcc2786d`/`1f2ea9d8`）
- 運用注記: 初回push（`ad26ac69`）で誤ってroot `output/`・root `scripts/` に配置されたため、同日中に上記experiments配下へ移設しroot側は削除した（内容はbyte-identical）。

## 信頼境界

v17自体の健全性は経験的証拠による（非飽和領域でv16一致・pilot不変・76c両順序安定）。本再検査はengine-consistencyの簿記確定であり、REFUTED-D10はLOSS証明ではない。WIN7-D10証明書は個別7石rootのfirst-player win（depth 10以内）のみを証明する。NOT-STERILEも行の勝敗を意味しない。

**標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4 はすべてUNKNOWN。**
