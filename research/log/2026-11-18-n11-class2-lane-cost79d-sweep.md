# 2026-11-18 n11 class2-lane cost79d: fresh v17 sweep完了・全79 bit反証 (2026-11-18)

## 背景

cost79d claim v1（`class2-lane-cost79d-inflight-20261118.json`・blob `84f32d13`・census v13は
`fdb94e31`・census v13 script `9976d8ce`）は、census v13 rank-1行
`00000000020000003800400080000000`（S6・石bits [31,46,59,60,61,89]・edge cost 79・
demand {c1:0, c2:0, c4:3}・法候補79 == edge cost）のfresh 79-bit depth-10 sweepを計画し、
長期レーンの同じセッションがdriver `ev79d_batches_20261118.sh` で実行して完走した。
79c（20 WIN7-D10）と異なり、本行は**全79 bitがREFUTED-D10**に確定し、
74i・75fに次ぐ3つ目の完全反証行となった。

## 実行: fresh v17 depth-10 sweep（raw commit `1371465c`）

- 72 open bits（8×9）+ 7 confirmation bitsの9バッチ。engine v17
  （blob `c132cc64`）・depth 10・cap 1e9/bit・andclose 1・pilot_d6管理。
- 79/79 verdicts確定: **0 WIN7-D10 / 79 REFUTED-D10 / 0 capped**。
  candidate nodes **49,103,515** + pilot 9×3,402。実行環境: node v22.20.0・2 vCPU
  （約101k nodes/s、単一runnerプロセス）。
- 9/9バッチがpilot_d6管理 loss=false・ちょうど3,402 nodesで開始（v17管理・全合格）。
- 確認batch 9（bits [5,27,41,79,90,93,115]）はcensus v13 overlay予測と**7/7完全一致**
  （全REFUTED-D10・衝突0）。転移元は pre-64h harvest×3・cost74i行×2・cost75f行×2。
- 決定性: det1/det8再実行はmsのみ差でfield同一
  （`class2-lane-cost79d-det-batch1-20261118.jsonl` blob `53e83a4f`・
  `class2-lane-cost79d-det-batch8-20261118.jsonl` blob `35678125`）。
- v15 cross-engine: 独立v15 runner（blob `8744fc65`）で確認batch 7 bitを再チェック、
  **7/7 REFUTED-D10一致**（pilot_d6 5,949・blob `733cc40a`）・衝突0。
- 生バッチ監査（`audit_cost79d_raw_batches_20261118.py`・blob `d4a5c6cf`・
  出力 `class2-lane-cost79d-raw-batches-1-9-audit-20261118.json`・blob `cfc6fbe3`）:
  全batchのpilot 3402・bit列計画一致・andclose全true・capped 0・terminal石数範囲[13,17]・
  verdict意味論の適用・**per-bit D4 root canonの独立再計算**（確認7 bitのroot canonは
  census v13転移canonと一致）・node合計49,103,515・12 rawファイルのsha1 pin。

## 出版

- 12 raw JSONL（9 batch + det2 + v15 crosscheck）+ audit JSON + audit scriptの14ファイルを
  commit `1371465c` で出版。全ファイルのgit blob SHAを本logとclaim v2にpin。
- claim v2（`class2-lane-cost79d-inflight-20261118.json`）で完了状態を記録
  （batches_run 9・actual_execution・confirmation_outcome・raw blob pins）。

## 制限

- 本sweepが証明するのは「このchildの79個の7石rootのそれぞれについてdepth 10以内に
  先手勝ちが存在しない（REFUTED-D10）」のみ。**REFUTED-D10はLOSS証明ではない**。
  行のreceipt foldは不要（win bit 0のため、74i/75fと同様）。
- 11x11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4はいずれも
  **UNKNOWN** のまま。

## 次の一手

- census v14で本行をswept（79 REFUTED-D10・完全反証・証明書なし・fold不要）として記録し、
  census v13 ranking_top10のrunner-up `00000000020000003800000880000000`
  （cost 79・open 74）を次ターゲット候補として選定する。
- 並走管轄のまま手を出さないもの: 66i receipt fold残り、66j/69j/71e/72d/73i/73j/73k/73l
  fold、K09xx系、cost73k測定系。
