# 2026-11-18 n11 class2-lane cost82d: fresh v17 sweep完了・全82 bit反証 (2026-11-18)

## 背景

cost82d claim v1（`class2-lane-cost82d-inflight-20261118.json`・blob `1f4484ed`・
census v18は`11306824`・census v18 script `99371f15`・driver commit `89aabc45`、
lane dir `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/`に直接着地）は、
census v18 rank-1行 `00000000020000003800000080000800`（S6・石bits
[11,31,59,60,61,89]・edge cost 82・open 65 + confirmation 17・demand
{c1:0, c2:0, c4:2}・法候補82 == edge cost）のfresh 82-bit depth-10 sweepを計画した。
band名cost82dはcost-82台では**class4-lane cost82・cost82b、class2-lane cost82cに次ぐ
最初の空き文字**（cost82aは不使用のためhighest+1のdを採用・repo検索0件）。
confirmation 17 bitのうちbits 15/105は**81行（cost81）swept化による初のcost81由来転移**。

## 実行: fresh v17 depth-10 sweep（2セッション分担）

- 65 open bits（7×9 + 1×2）+ 17 confirmation bitsの9バッチ。engine v17
  （blob `c132cc64`）・depth 10・cap 1e9/bit・andclose 1・pilot_d6管理。
- batch 1-5は並走セッションが実行・出版（commits `724cca8b`〜`02ff4596`）。
  並走がbatch 5で停止した後、**別セッション（本セッション）が全9バッチを
  独立に再実行**し、出版済みbatch 1-5との全ビット比較で
  **48/48行・non-msフィールド完全一致**を確認した上で、
  batch 6-9 + det1/det8 + v15 crosscheckを出版した（commit `4ac5fa29`）。
  これはcost81監査のdet1/det8相当の決定性検証を**全ビットに拡張**したものに等しい。
- 82/82 verdicts確定: **0 WIN7-D10 / 82 REFUTED-D10 / 0 capped**。
  candidate nodes **127,619,232** + pilot 9×3,402。実行環境: node v22.20.0・
  sandbox（約300-400k nodes/s・単一runnerプロセス）。per-batch:
  b1 17,199,294 / b2 13,329,438 / b3 23,060,651 / b4 7,145,097 / b5 13,891,750 /
  b6 13,840,230 / b7 13,201,034 / b8 5,383,680 / b9-conf 20,568,058 nodes。
- 9/9バッチがpilot_d6管理 loss=false・ちょうど3,402 nodesで開始（全合格）。
- 確認batch 9（bits [5,15,27,30,32,35,41,45,46,74,75,79,85,90,93,105,115]）は
  census v18 overlay予測と**17/17完全一致**（全REFUTED-D10・衝突0）。転移元は
  pre-64h harvest×4・cost81×2（bits 15/105・初のcost81由来）・cost74i×2・
  cost80e×1・cost79e×2・cost75f×2・cost79d×2・cost80f×2。
- 決定性: det1/det8再実行はmsのみ差でfield同一（det-batch1 blob `83b49a0f`・
  det-batch8 blob `77068322`）。
- v15 cross-engine: 独立v15 runner（blob `8744fc65`）で確認17 bitを再チェック、
  **17/17 REFUTED-D10一致**（pilot_d6 5,949・blob `6c8a273a`）・衝突0。
- 生バッチ監査（`audit_cost82d_raw_batches_20261118.py`・blob `5d612a36`・
  出力 `class2-lane-cost82d-raw-batches-1-9-audit-20261118.json`・blob `14a44c8b`・
  cost81監査からの機械変換）: 全batchのpilot 3402・bit列計画一致・andclose全true・
  capped 0・terminal石数範囲[13,17]・**per-bit D4 root canonの独立再計算**
  （確認17 bitのroot canonはcensus v18転移canonと一致）・v15 crosscheck 17/17・
  node合計127,619,232・12 rawファイルのsha1 pin。

## 出版

- 本コミットでaudit JSON + audit script + claim v2
  （`class2-lane-cost82d-inflight-20261118.json`・blob `cffeda69`）+ 本logを出版。
  全rawファイルのgit blob SHAをclaim v2にpin。
- raw batch 1-5（並走・5コミット）とbatch 6-9 + det + v15（本セッション・
  commit `4ac5fa29`）は出版済み。

## 制限

- 本sweepが証明するのは「このchildの82個の7石rootのそれぞれについてdepth 10以内に
  先手勝ちが存在しない（REFUTED-D10）」のみ。**REFUTED-D10はLOSS証明ではない**。
  行のreceipt foldは不要（win bit 0のため、74i/75f/79d/79e/80e/80f/81と同様）。
- 11x11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4はいずれも
  **UNKNOWN** のまま。

## 次の一手

- census v19で本行をswept（82 REFUTED-D10・8つ目の完全反証行・証明書なし・
  fold不要）として記録し、census v18 rankingのrunner-up
  `00000000020000003800000090000000`（cost 82・open 65）を次ターゲット候補として
  選定する。残り未swept poolは8行。
- 並走管轄のまま手を出さないもの: 66i receipt fold残り、66j/69j/71e/72d/73i/73j/
  73k/73l fold、K09xx系、cost73k測定系。