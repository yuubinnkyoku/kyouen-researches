# 2026-11-17：cost65n行のv17全行再検査（fbtOR飽和欠陥・過去lane再検査キュー第1弾）— 59/59 bit全フィールド一致・行全体がfb非飽和と確定

開始時の最新mainは `4f49879805820e6d7a33d7f966ef79bcf4ea6c91`（cost64e v17再検査着地後）。作業前に `AGENTS.md`、`research/knowledge/README.md`、fbt飽和欠陥log（`2026-11-17-n11-class2-lane-cost76c-fbt-saturation-defect-v17-repair-and-resweep.md`）、cost65n claim v2（`6e85762f`）・raw batches・独立再実行検証（`0c237017`）を確認した。cost64h fold receiptは本エントリ時点でも未着地（並走claim済み・着手禁止）。

## 出発点

fbt飽和欠陥のlogは「**飽和探索のv16/v15 verdictは両方向に信用できない。過去laneのREFUTED-D10 verdict（特にnode数が大きいbit）は証拠として使う前にv17再スイープが必要**」と明記し、65n/66c等を再検査キューに挙げていた。本レーンはこのキューからcost-65n（head-1441最安open行・child `00000000000000801202010000800000`・共有class-2親 `00000000000000003800000008002000`・59 swept bits・総nodes 92,530,349・bit 9が5.08M・bit 26が5.65M nodesで当時の経験的非飽和しきい値3.5Mを超える）を最初の対象として選んだ。65nのWIN bits 90/117は証明書二重検証済み（BigInt+Bareiss・盲再抽出byte-identical `e01093dc`）であり、再検査の焦点はREFUTED-D10 57 bitの証拠としての有効性である。

## 実施内容

fbt修復済みv17 engine（`class4_child1_runner_v17.ts`・blob `c132cc64`・probe打ち切り時のcacheせず直接計算fallback）を用い、出版時と同一のbatch分割（8バッチ・bit構成不変）・depth 10・cap 1e7・`--andclose 1`・候補ごとのengine完全reset・pilot_d6制御付きで、59 bit全部を新規環境で再実行した。

## 結果

- **59/59 bitが出版v16記録と全フィールド一致**（loss・nodes・capped・terminalStoneRange・andclose。nodes総和も92,530,349で完全一致）。pilot_d6制御8/8（3402・loss=false）。
- **verdict反転0件**。WIN bits 90（1,562,274 nodes）・117（388,910 nodes）は不変。REFUTED 57 bit・capped 0も不変。
- **決定性**: 同一条件の全8バッチ2回実行で、全59 bit+8 pilotの verdict/nodes/capped/terminalStoneRange/andclose が完全一致（msのみ相違）。
- **解釈**: nodes一致はv17の「非飽和探索はv16とbyte-identical」性質により、**65n行全体がfb非飽和**であったことを機械的に確定する。65nの全verdict（WIN 2 + REFUTED 57・計59 bitのbit table・census harvest入力・65o/66c/64h等へのD4転写源）はfbt欠陥の影響を受けず、planning入力としてそのまま使用できる。
- **経験的非飽和しきい値の更新**: 非飽和実測しきい値は3.5M nodes/bit（64h/64e）から**5,654,046 nodes/bit（bit 26・bit 9の5,075,917も非飽和）**へ引き上げられた。76cの飽和事例（bit 113が~8.2M nodes・396k drops）と非飽和5.65Mの間に挟まった新データ点で、node数からの飽和判定は引き続き不可能（検出器はv17でのnodes不一致）だが、実務的な安心圏が拡大した。

## 含意

1. 65n行のREFUTED-D10 57 bitは以後のcensus・bit tableで引き続き有効なplanning証拠である。
2. 65nからD4転写で他行に伝播したverdict（`7074e276`の15件など転写系）も、転写元bitが非飽和確定したことで裏付けられた。
3. 過去lane再検査キューの残りは66c（bit 30が8.8M nodes・bit 112が12.57M nodesで飽和圏・WIN 7 bitは証明書で不動だがREFUTED 52 bitが焦点）が最優先で、本セッションで続けて実施する。

## 保存物

- 監査script: `scripts/verify_cost65n_v17_full_row_recheck_20261117.py`（stdlibのみ・入力blob SHA pin照合22 checks・2回実行byte-identical）
- 監査JSON: `output/class2-lane-cost65n-v17-full-row-recheck-20261117.json`
- v17生記録: `output/class2-lane-cost65n-v17-recheck-batch{1..8}-20261117.jsonl`（出版分割同一・pilot込み）
- 入力（出版済み・blob pin照合済）: `class2-lane-cost65n-raw-batch{1..8}-20261116.jsonl`（`8361a5be`/`4e2bbc51`/`c613f714`/`35b53b20`/`c4f810a2`/`32545b32`/`fe5a98c3`/`278e69ba`）

## 信頼境界

v17自体の健全性は「非飽和領域でv16一致・pilot不変・両順序でverdict不変（76c実績）」による強い証拠だが形式的検証ではない。本再検査はengine-consistencyの簿記確定であり、REFUTED-D10はもともとLOSS証明ではない。WIN7-D10証明書は個別7石rootのfirst-player win（depth 10以内）のみを証明する。

**標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4 はすべてUNKNOWN。**
