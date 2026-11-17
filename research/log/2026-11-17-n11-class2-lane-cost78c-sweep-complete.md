# n11 class2-lane cost78c sweep完了: 11 WIN7-D10 / 67 REFUTED-D10・初のWIN付き行 (2026-11-17)

## 背景

head-1473 presweep census v11（commit `cea8c4fb`）が選定したrank-1行
`00000000000000403800000008000008`（cost 78・parent
`00000000000000403800000008000000`・stones [3,27,59,60,61,70]・demand
{c1:0, c2:1, c4:0}・legal 78 bits・66 open + 12 confirmation [5, 13, 14, 20,
34, 46, 97, 103, 108, 110, 115, 118]）をcost-78cとしてclaim（claim v1・
commit `fb9aeb7d`・push直前のmain head `cea8c4fb`で同childへのclaim/raw
batch/auditの不在を確認済み）。78ラベルのa/bは使用済みのためc。census v11
runner-up（cost 79・open 69）は次候補。

## 実行

- driver: `scripts/ev78c_batches_20261117.sh`（74i/75fと同一形状: 66 open
  bitsを7×9 + 1×3、confirmation 12 bitsを別batch。engineはv17 blob
  `c132cc64`、depth 10・cap 1e9/bit・andclose 1・fresh engine per bit）。
- 9 batchを順に実行（batch 1〜8がopen bits、batch 9がconfirmation）。
  pilot_d6制御は9/9で期待値 {loss=false, nodes=3402, capped=false} と完全一致。
- 2回のサンドボックスインフラリセットを跨いだ実行になった。1回目はbatch 6
  出版後で、batches 1-6はmainからbyte-exact再取得、batches 7-9とdet/v15
  制御runsはリセット後に再実行した。リセット前の実行も同一の11 WIN bitsと
  同一の78-bit総node数（238,626,461）を観測済み（WIN bit 114 = 5,630,090・
  bit 116 = 9,489,167も同一node数）。
- 決定性: det batch 1（bits 1,2,4,9,10,16,17,18,19・第1セッション産）と
  batch 8（bits 117,119,120・リセット後セッション産）を再実行し、非ms全
  フィールドでfield-identical（cross-session determinism）。さらに本log出版
  時に、リセットで喪失したdriverとaudit scriptを再構築し、再構築driverで
  batch 8を第3セッションとして再実行したところ、これもfield-identical。
- v15 cross-engine: 独立v15 engine（blob `8744fc65`）でconfirmation 12 bits +
  最重5 bits [34, 116, 41, 25, 99] を再探索。17/17 verdict一致（16 loss=false +
  1 loss=true at WIN bit 116）・2/2 pilot 5949・0 capped。v15 nodes合計
  150,314,380。

## 結果: 11 WIN7-D10 / 67 REFUTED-D10 / 0 capped

- 78 candidate bits（= legal 78 bits全て）が確定。capなし。candidate nodes合計
  238,626,461（pilot込み 238,675,781）。terminal stone rangeは全bit [13,17]・
  例外なし。最重bit 34（11,476,946 nodes）。78 root canonは78/78でunique、
  WIN canonsとconfirmation canonsはdisjoint。
- **WIN7-D10 bits: [1, 4, 9, 30, 49, 69, 75, 79, 100, 114, 116]**
  （nodes: 1 = 7,264,656 / 4 = 7,292,768 / 9 = 5,853,782 / 30 = 2,011,603 /
  49 = 1,818,616 / 69 = 1,161,282 / 75 = 1,264,941 / 79 = 1,982,518 /
  100 = 2,234,336 / 114 = 5,630,090 / 116 = 9,489,167）。
- **74i・75fに続きpresweep-1473 band 3行目だが、両行（全滅）と違い初の
  WIN付き行**（band全体では73l以来のWIN7-D10）。この行のreceipt foldには
  11証明書の抽出・独立検証・出版が先に必要になる。
- confirmation 12 bitsは予測どおり全てREFUTED-D10で、独立D4 canon再導出で
  両側検証（12/12）。6転送（bits 5/13/14/20/34/46 = cost69j/cost64d/
  cost72d/cost64h/cost73j/cost73i bit 3）はraw同一・両側nodes一致、
  6転送（bits 97/103/108/110/115/118 = cost71e bit 87・cost66i bit 33・
  cost66j bit 87・cost73k bit 33・cost70b bit 48・cost73l bit 87）は
  canon等価のみ。出典の生バッチ行からverdictを再読み出し（0 capped）。
- 並走セッションがbatches 1-6の独立audit（`class2-lane-cost78c-raw-
  batches-1-6-audit-20261118.json`・blob `d8e5f9b7`・all_pass、WIN 9 bitsは
  bit-exact一致）とclaim v2（PARTIAL・archived）を出版済み。claim v3は
  v2を完成形に更新し、batches 7-9（`a8cd1012`）とdet/v15（`867a131c`）を
  取り込む。
- 再構築したaudit script（`audit_cost78c_raw_batches_20261117.py`）は、
  出版済み監査JSONをbyte-identicalに再現（blob `8e3ee7aa` 一致）。

## 成果物

- `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/ev78c_batches_20261117.sh`（リセット後再構築・第3セッションbatch 8再実行で検証）
- `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_cost78c_raw_batches_20261117.py`（リセット後再構築・出版監査JSONをbyte-identical再現）
- raw 9 batch + det 2 + v15 crosscheck 2 の13 JSONL（git blob pinはclaim v3に記録）
- `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost78c-raw-sweep-audit-20261117.json`（blob `8e3ee7aa`）
- `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost78c-inflight-20261117.json`（claim v3・blob `d3105b3a`）

## 制限

- WIN7-D10は個別7石rootからのdepth 10内先手勝ちのみ。REFUTED-D10はloss
  証明ではなく「depth 10以内の先手勝ちなし」。manifest行は本sweepでは閉じない。
- 11 WIN rootsは証明書抽出・独立検証・出版が完了するまで確定扱いにしない。
  receipt foldは66i/66j/69j/71e/72d/73i/73j/73k/73l fold完了後。
- 11x11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4はいずれも
  **UNKNOWN** のまま。

## 次の一手

- 11 WIN bitsの証明書抽出（73l-band pipeline: 抽出 → 独立検証 → 出版）。
  bit単位で分割実行し、逐次出版。
- census v12で78c行をswept扱い（11 WIN7-D10・証明書出版待ち）として更新。
- 並走管轄のまま手を出さないもの: 66i receipt fold、73i証明書の出版、
  cost73k測定系（fixB 8-way worker split memo merge追従）。
