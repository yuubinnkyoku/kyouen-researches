# 2026-11-17：cost66c行のv17全行再検査（過去lane再検査キュー第2弾）— bit 117に飽和検出（22 nodes・verdict不変）・bit 30/112は非飽和・WIN 7 bits全不変

開始時の最新mainは `4f49879805820e6d7a33d7f966ef79bcf4ea6c91`。cost65n再検査log（同日）に続き、fbt飽和欠陥logが挙げた過去lane再検査キューの最優先残件であるcost-66c（head-1441第3位最安open行・child `00000000000000003800000008002008`・共有class-2親 `00000000000000003800000008002000`）を再検査した。cost64h fold receiptは本エントリ時点でも未着地（並走claim済み・着手禁止）。

## 出発点

66cは既出版行の中で**最大級のper-bit探索**を持つ: bit 30が8,806,920 nodes・bit 112がcap-raise解決で12,574,920 nodes（cap 1e7でcapped後80Mまで引き上げてWIN確定）。76c bit 113（~8.2M nodes・396k drops）の飽和反転事例と同規模であり、52 swept REFUTED-D10 bitの証拠有効性が焦点。WIN 7 bits（73/75/79/87/96/97/112）は全て証明書二重検証済み（manifest `39665854`・盲再抽出byte-identical `b41027e1`）で不動。

## 実施内容

fbt修復済みv17 engine（blob `c132cc64`）で59 swept bit全部を出版時と同一のbatch分割（8バッチ）・depth 10・cap 1e7・`--andclose 1`（bit 112はcap 80000000を追加）・候補ごとengine完全reset・pilot_d6制御付きで再実行し、出版raw batches 1-8（blob pin照合済）+ bit-112 cap-raise解決記録と全フィールド比較した。

## 結果

- **58/59 bitが全フィールド一致**（loss・nodes・capped・terminalStoneRange・andclose）。
- **bit 117に飽和検出**: v16の3,121,390 nodesに対しv17は3,121,368 nodes（**−22 nodes**）。verdictは両engineともREFUTED-D10で不変。order-matrix（v16/v17 × andclose 1/0の4構成）で**全構成REFUTED-D10**。c0 traversalは両engineでnode-exact（1,341,675）で、飽和はclose-first順序でのみ軽微に発生した。v17の決定性あるnode数3,121,368がengine-corrected値として確定。
- **bit 112（12,574,920 nodes WIN・cap 80M）はnode-exact一致**。fb非飽和。証明書（2,774,034 bytes・3分割出版）と完全整合。
- **bit 30（8,806,920 nodes）もnode-exact一致**でfb非飽和。**12.57M nodes/bitの非飽和実測**はnode数だけでは飽和判定できないことの決定的な実例（76c bit 113の8.2M飽和と対比。飽和はfb unique tripleの多様性依存）。
- **WIN bits 7個（73/75/79/87/96/97/112）全て不変**・verdict反転0件。capped 0（bit 112はcap-raise記録と同一）。
- nodes総和: v16出版81,605,344 + bit112解決12,574,920 = **84,180,263に対しv17は84,180,241**（差はbit 117の−22のみ）。pilot 8/8（3402）。
- **決定性**: 全8バッチ+cap80Mの2回実行で全bit+全pilotが完全一致（msのみ相違）。

## 含意

1. 66c行のREFUTED-D10 52 bit（bit 117を含む）はplanning証拠として有効。bit 117のengine-corrected node数は3,121,368。
2. 66c fold（head 1444→1450・7 WIN receipts）の基盤は無影響（WIN 7 bitsが証明書+v17の双方で確認）。
3. 66cからD4転写で伝播したverdictも裏付けられた。
4. **node数による飽和の事前判定は不可能**というfbt logの結論を、12.57M nodes非飽和（bit 112）と3.12M nodes軽微飽和（bit 117）の対比で補強した。検出器はv17でのnode数不一致のみ。
5. 過去lane再検査キューの残りは、head-1452構成行のうち64d/64f/64g/65f/65j/76d/77e等（未実施）。

## 保存物

- 監査script: `scripts/verify_cost66c_v17_full_row_recheck_20261117.py`（stdlibのみ・入力blob SHA pin照合・29 checks・2回実行byte-identical）
- 監査JSON: `output/class2-lane-cost66c-v17-full-row-recheck-20261117.json`
- v17生記録: `output/class2-lane-cost66c-v17-recheck-batch{1..8}-20261117.jsonl` + `class2-lane-cost66c-v17-recheck-bit112-cap80m-20261117.jsonl`
- bit 117 order-matrix: `output/class2-lane-cost66c-v17-bit117-order-matrix-20261117.jsonl`（4構成）
- 入力（出版済み・blob pin照合済）: `class2-lane-cost66c-raw-batch{1..8}-20261116.jsonl`（`1ee1146d`/`b598d6cc`/`c3a85aca`/`5ff20e15`/`5899ba17`/`8d84f6cb`/`a805e410`/`ec9adcd2`）+ `class2-lane-cost66c-bit112-cap80m-resolution-20261116.jsonl`（`317876ad`）

## 信頼境界

v17自体の健全性は経験的証拠による（非飽和領域でv16一致・pilot不変・76c両順序安定）。本再検査はengine-consistencyの簿記確定であり、REFUTED-D10はLOSS証明ではない。WIN7-D10証明書は個別7石rootのfirst-player win（depth 10以内）のみを証明する。NOT-STERILEも行の勝敗を意味しない。

**標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4 はすべてUNKNOWN。**
