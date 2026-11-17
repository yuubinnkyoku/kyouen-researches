# 2026-11-18 n11 class2-lane cost82e: fresh v17 sweep完了・全82 bit反証・歴史的STERILE行のcross-version再検証 (2026-11-18)

## 背景

cost82e claim v1（`class2-lane-cost82e-inflight-20261118.json`・blob `5f9f3d95`・
census v19は`a0c6abaf`・census v19 script `8ba51a2d`・census v19 commit `122cb6c6`・
driver commit `43f9e07a`、lane dir `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/`に直接着地）は、
census v19 rank-1行 `00000000020000003800000090000000`（S6・石bits
[28,31,59,60,61,89]・edge cost 82・open 63 + confirmation 19・demand
{c1:0, c2:0, c4:3}・法候補82 == edge cost）のfresh 82-bit depth-10 sweepを計画した。
band名cost82eはcost-82台では**class4-lane cost82・cost82b、class2-lane cost82c・
cost82dに次ぐ最初の空き文字**（repo検索0件・highest+1のeを採用）。
confirmation 19 bitのうちbits 11/109は**82d行（cost82d）swept化による初のcost82d由来転移**。

## 実行: fresh v17 depth-10 sweep（単一セッション全実行）

- 63 open bits（7×9）+ 19 confirmation bitsの8バッチ。engine v17
  （blob `c132cc64`）・depth 10・cap 1e9/bit・andclose 1・pilot_d6管理。
- 82/82 verdicts確定: **0 WIN7-D10 / 82 REFUTED-D10 / 0 capped**。
  candidate nodes **70,583,627** + pilot 8×3,402。実行環境: node v22.20.0・
  sandbox（約300-400k nodes/s・単一runnerプロセス）。per-batch:
  b1 16,445,714 / b2 4,999,537 / b3 4,569,340 / b4 11,494,096 / b5 3,821,206 /
  b6 4,108,893 / b7 10,848,629 / b8-conf 14,296,212 nodes。
- 8/8バッチがpilot_d6管理 loss=false・ちょうど3,402 nodesで開始（全合格）。
- 確認batch 8（bits [5,11,15,30,32,35,41,45,46,74,75,79,85,88,90,93,105,109,115]）は
  census v19 overlay予測と**19/19完全一致**（全REFUTED-D10・衝突0）。転移元は
  pre-64h harvest×4・cost82d×2（bits 11/109・初のcost82d由来）・cost81×2・
  cost80e×2・cost79e×2・cost75f×2・cost80f×2・cost79d×2・cost74i×1。
- 決定性: det1/det7再実行はmsのみ差でfield同一（det-batch1 blob `0b1d9110`・
  det-batch7 blob `7df5d8c7`）。
- v15 cross-engine: 独立v15 runner（blob `8744fc65`）で確認19 bitを再チェック、
  **19/19 REFUTED-D10一致**（pilot_d6 5,949・blob `7dfff259`）・衝突0。
- 生バッチ監査（`audit_cost82e_raw_batches_20261118.py`・blob `42c9ecb7`・
  出力 `class2-lane-cost82e-raw-batches-1-8-audit-20261118.json`・blob `49757780`・
  cost82d監査（blob `5d612a36`）からの変換）: 全batchのpilot 3402・bit列計画一致・
  andclose全true・capped 0・terminal石数範囲[13,17]・**per-bit D4 root canonの独立再計算**
  （確認19 bitのroot canonはcensus v19転移canonと一致）・v15 crosscheck 19/19・
  det1/det7 field同一検証を監査script自体に含めて自己完結化・
  node合計70,583,627・11 rawファイルのsha1 pin。

## コーディネーター修正の承认（sweep完了後の着地）

- sweep完了後に並走がコーディネーター修正を出版（commits `1d05b0a1`/`e3db912a`/
  `4ffdf3b6`/`8c04f41e`）: K0865（head-1410 receipt-unclosability census）により、
  本childのS5 parent `00000000020000003800000080000000`（class 4・rem 18・edge cost 1460）は
  **all_remaining_sterile**（18/18 S6行がSTERILE）。census v18/v19の残pool全行が
  このSTERILE parent所属。
- **本sweepはclaim v1出版（`43f9e07a`）時点の正しいmain状態に基づいて起動し、
  修正の出版前に完了したもの**。コーディネーター指示
  「label it as revalidation and do not count it as a new receipt/coverage result」に従い、
  **本sweep成果は「歴史的STERILE行（K0863予測）のcross-version再検証」として明示ラベル**
  し、新規のreceipt/coverage進展としては数えない。claim v2
  （blob `de7de118`）のtitle・status・next_action・receipt_foldに再検証framingを反映。
- 82/82 REFUTED-D10の結果自体は、STERILE予測（D10内WIN7なし）のv17再実装・
  独立v15 cross-engine・独立監査scriptによる**cross-version整合の追加証拠**となる。
- census v19 script（blob `8ba51a2d`）内のcost82d claim pin（`cffeda69`）は
  main HEADではin-place修正により失効（claim v3化・現行blob `fcf44510`）。
  歴史的claim v2 blobはcommit `775277b5`で取得可能。repo慣行（claimのin-place修正）
  に従いcensus v19 script自体は変更しない。

## 出版

- 本コミットで11 rawファイル（batch 1-8 + det1/det7 + v15 crosscheck）+ audit script +
  audit JSON + claim v2（`class2-lane-cost82e-inflight-20261118.json`・blob `de7de118`）+
  本logを単一コミットで出版。全rawファイルのgit blob SHAをclaim v2にpin。
- push前に最新mainを再取得し、HEAD `8c04f41e`からの移動と82e関連ファイルの
  並走による先行出版を確認した上で着地する。

## 制限

- 本sweepが証明するのは「このchildの82個の7石rootのそれぞれについてdepth 10以内に
  先手勝ちが存在しない（REFUTED-D10）」のみ。**REFUTED-D10はLOSS証明ではない**。
  行のreceipt foldは不要（win bit 0のため、74i/75f/79d/79e/80e/80f/81/82dと同様）。
- STERILE parent所属のため、**本行の完全反証はD10 receiptによるfamily閉包の進展を
  意味しない**（K0863: 自前行からのD10 WIN7 receiptでは閉じられない）。
- 11x11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4はいずれも
  **UNKNOWN** のまま。

## 次の一手

- コーディネーター指示に従い、head-1473 worklistへK0865/K0863 STERILE-parent除外を
  適用したcensus再構築が次の選定前提。**これは並走管轄のため本レーンでは着手しない**。
  並走が出版したら検証側に回る。
- 残pool 8行の他行の再検証は、実施する場合も「revalidation」ラベルでのみ行う。
- partial-STERILE 57 parentのcross-cover価値分析は未着手領域。
- 並走管轄のまま手を出さないもの: 66i receipt fold残り、66j/69j/71e/72d/73i/73j/
  73k/73l fold、K09xx系、cost73k測定系、cost82d幾何監査系、STERILE filter census再構築。
