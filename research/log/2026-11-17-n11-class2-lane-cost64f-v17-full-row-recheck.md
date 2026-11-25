# 2026-11-17：cost64f行のv17全行再検査（過去lane再検査キュー第4弾）— 59 bit全フィールド一致・完全非飽和・WIN 3 bits不変

開始時の最新mainは `427e29fa450482dc5572cdc33a66527a4040f1e9`（作業中の移設・他レーンの進行を挟り現在は並走コミットが継続）。cost65n・cost66c・cost64d/64gに続き、過去lane再検査キューの未実施行だった **cost-64f**（head-1438第2行・child `0000000000000080120a000000800000`・59 swept bits・WIN7-D10 3 bits〔39/72/107・win3 manifestで証明書二重検証済み〕・REFUTED-D10 56・capped 0・総nodes 54,905,391）を再検査した。cost64h fold receiptは本エントリ時点でも未着地（並走claim済み・着手禁止）。

## 実施内容

fbt修復済みv17 engine（blob `c132cc64`）で59 swept bit全部を出版時と同一のbatch分割（8バッチ）・depth 10・cap 1e9（出版行は0 capped・max per-bit 2,994,208でcap不発動）・`--andclose 1`・候補ごとengine完全reset・pilot_d6制御付きで再実行し、出版raw batches 1-8（blob SHA pin照合済み・repoとのbyte照合済み）と全フィールド比較した。さらに独立の2回目全行実行（ms以外byte-identical）で決定性を確認した。

## 結果

- **59/59 bit全フィールド一致**（loss・nodes・capped・terminalStoneRange・andclose）。nodes総和54,905,391完全一致。
- **WIN 3 bits（39/72/107）全不変**・verdict反転0件・capped 0・pilot 8/8（3402）。
- **完全fb非飽和**と確定（node数不一致0）。2回目実行とも全bit一致。

## 含意

1. 64fのREFUTED-D10 56 bitはplanning証拠として有効（engine-consistencyの簿記確定）。
2. 64f fold（head 1438→1441）の基盤は無影響。head-1452構成行のうち65n/66c/64d/64g/64fのv17裏付けが完了。
3. 非飽和しきい値情報: 2,994,208 nodes/bitまでの行で全bit一致事例が累積（65n 5.65M・66c bit 30 8.8Mも非飽和）。node数による事前飽和判定は不可能という結論は不変。

## 保存物

- 監査script: `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/verify_cost64f_v17_full_row_recheck_20261117.py`（stdlibのみ・入力blob SHA pin照合・engine blob pin照合・決定性2回実行照合）
- 監査JSON: `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost64f-v17-full-row-recheck-20261117.json`
- v17生記録: 同output/配下 `class2-lane-cost64f-v17-recheck-batch{1..8}-20261117.jsonl`（8本）
- 入力（出版済み・blob pin照合済）: `class2-lane-cost64f-raw-batch{1..8}-20261116.jsonl`（`e33817e9`/`6dd3db9b`/`44ad9e80`/`1b62bb8a`/`5a89767c`/`c598100f`/`0d5ed3ad`/`6b29c182`）

## 信頼境界

v17自体の健全性は経験的証拠による（非飽和領域でv16一致・pilot不変・76c両順序安定）。本再検査はengine-consistencyの簿記確定であり、REFUTED-D10はLOSS証明ではない。WIN7-D10証明書は個別7石rootのfirst-player win（depth 10以内）のみを証明する。NOT-STERILEも行の勝敗を意味しない。

**標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4 はすべてUNKNOWN。**
