# 2026-11-18 n11 class2-lane cost80e: fresh v17 sweep完了・全80 bit反証 (2026-11-18)

## 背景

cost80e claim v1（`class2-lane-cost80e-inflight-20261118.json`・blob `94ca870d`・
census v15は`dfb61db5`・census v15 script `5a53528f`・driver commit `c132463f`）は、
census v15 rank-1行`00000000020000003800000180000000`（S6・石bits
[31,32,59,60,61,89]・edge cost 80・demand {c1:0, c2:0, c4:2}・法候補80 ==
edge cost）のfresh 80-bit depth-10 sweepを計画し、長期レーンの同じセッションが
driver `ev80e_batches_20261118.sh` で実行して完走した。79e（完全反証）に続き、
**本行も全80 bitがREFUTED-D10**に確定し、74i・75f・79d・79eに次ぐ
**5つ目の完全反証行**となった。

## 実行: fresh v17 depth-10 sweep

- 68 open bits（7×9 + 1×5）+ 12 confirmation bitsの9バッチ。engine v17
  （blob `c132cc64`）・depth 10・cap 1e9/bit・andclose 1・pilot_d6管理。
- 80/80 verdicts確定: **0 WIN7-D10 / 80 REFUTED-D10 / 0 capped**。
  candidate nodes **87,301,907** + pilot 9×3,402。実行環境: node v22.20.0・
  2 vCPU（約400k nodes/s、単一runnerプロセス、foreground実行）。
- 9/9バッチがpilot_d6管理 loss=false・ちょうど3,402 nodesで開始（v17管理・全合格）。
- 確認batch 9（bits [5,27,30,35,41,46,74,79,85,90,93,115]）はcensus v15 overlay
  予測と**12/12完全一致**（全REFUTED-D10・衝突0）。転移元は pre-64h harvest×4・
  cost74i行×2・cost79e行×2・cost75f行×2・cost79d行×2。
- 決定性: det1/det8再実行はmsのみ差でfield同一
  （`class2-lane-cost80e-det-batch1-20261118.jsonl` blob `845a3ae1`・
  `class2-lane-cost80e-det-batch8-20261118.jsonl` blob `3549e2ea`）。
- v15 cross-engine: 独立v15 runner（blob `8744fc65`）で確認12 bitを再チェック、
  **12/12 REFUTED-D10一致**（pilot_d6 5,949・blob `e5ece402`）・衝突0。
- 生バッチ監査（`audit_cost80e_raw_batches_20261118.py`・blob `2c734748`・
  出力 `class2-lane-cost80e-raw-batches-1-9-audit-20261118.json`・blob `53007edc`）:
  全batchのpilot 3402・bit列計画一致・andclose全true・capped 0・terminal石数範囲[13,17]・
  verdict意味論の適用・**per-bit D4 root canonの独立再計算**（確認12 bitのroot canonは
  census v15転移canonと一致）・v15 crosscheck 12/12・node合計87,301,907・
  12 rawファイルのsha1 pin。

## 出版

- 12 raw JSONL（9 batch + det2 + v15 crosscheck）+ audit JSON + audit scriptの14ファイル、
  claim v2（`class2-lane-cost80e-inflight-20261118.json`・blob `9190341a`）、
  本logを出版。全ファイルのgit blob SHAをclaim v2にpin。
- band名cost80eはhighest+1（class2-lane cost80d・class4-lane cost80/80b/80cの次）で
  衝突なし（search検証済み）。

## 制限

- 本sweepが証明するのは「このchildの80個の7石rootのそれぞれについてdepth 10以内に
  先手勝ちが存在しない（REFUTED-D10）」のみ。**REFUTED-D10はLOSS証明ではない**。
  行のreceipt foldは不要（win bit 0のため、74i/75f/79d/79eと同様）。
- 11x11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4はいずれも
  **UNKNOWN** のまま。

## 次の一手

- census v16で本行をswept（80 REFUTED-D10・完全反証・証明書なし・fold不要）として記録し、
  census v15 ranking_top10のrunner-up `00000000020000003800200080000000`
  （cost 80・open 68）を次ターゲット候補として選定する。
- 並走管轄のまま手を出さないもの: 66i receipt fold残り、66j/69j/71e/72d/73i/73j/73k/73l
  fold、K09xx系、cost73k測定系。
