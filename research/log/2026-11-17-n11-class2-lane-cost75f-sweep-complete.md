# n11 class2-lane cost75f sweep完了: 75 bit全REFUTED-D10・勝ち7手目なし (2026-11-17)

## 背景

head-1473 presweep census v10（commit `cad0b982` + 修復commit `6de8f127`）が選定した
rank-1行`00000000020000003800020080000000`（cost 75・parent
`00000000020000003800000080000000`・stones [31,41,59,60,61,89]・demand
{c1:0, c2:0, c4:3}・legal 75 bits・71 open + 4 confirmation [27, 90, 93, 115]）を
cost-75fとしてclaim（claim v1・commit `1c234a02`・push直前のmain head
`6de8f127`で同childへのclaim/raw batch/auditの不在を確認済み）し、同セッションで
fresh v17 depth-10 sweepを実行した。75ラベルのb/c/d/eは使用済みのためf。

## 実行

- driver: `scripts/ev75f_batches_20261117.sh`（74iと同一形状: 71 open bitsを
  7×9 + 1×8、confirmation 4 bitsを別batch。engineはv17 blob `c132cc64`、
  depth 10・cap 1e9/bit・andclose 1・fresh engine per bit）。
- 9 batchを順に実行（batch 1〜8がopen bits、batch 9がconfirmation）。
  pilot_d6制御は9/9で期待値 {loss=false, nodes=3402, capped=false} と完全一致。
- 決定性: batch 1とbatch 8を別プロセスで再実行し、非ms全フィールドで
  field-identical。
- v15 cross-engine: 独立v15 engine（blob `8744fc65`）でconfirmation 4 bits +
  最重5 bits [7, 15, 66, 86, 105] を再探索。9/9 verdict一致（全てloss=false）・
  2/2 pilot 5949・0 capped。v15 nodes合計 57,511,014。

## 結果: 0 WIN7-D10 / 75 REFUTED-D10 / 0 capped

- 全75 candidate bit（= legal 75 bits全て）がREFUTED-D10。capなし。
  candidate nodes合計 76,432,898（pilot込み 76,482,218）。最重bit 66
  （7,160,326 nodes）。terminal stone range は全bit [13,17]・例外なし。
- **このchildには先手の勝ち7手目（depth 10以内）が1つも存在しない。**
  よって証明書抽出・BigInt再検証・receipt foldはすべて不要。行はaudit強度で
  完全確定。**74iに続き2行連続の全滅行**（STERILE候補はcensus上これで3行目:
  64a, 74i, 75f）。
- confirmation 4 bits [27, 90, 93, 115] は予測どおり全てREFUTED-D10で、
  独立D4 canon再導出で両側検証（4/4）: 27 = cost74i bit 41（raw同一・両側
  nodes 680,730一致）、90 = cost73f bit 79、93 = cost74i bit 79、
  115 = cost74f bit 79（いずれもcanon等価のみ）。出典の生バッチ行から
  verdictを再読み出し（0 capped）。
- raw sweep auditは2回実行でbyte-identical（md5 `0480cf1b`・blob `0951327a`）。

## 成果物

- `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/ev75f_batches_20261117.sh`
- `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_cost75f_raw_batches_20261117.py`
- raw 9 batch + det 2 + v15 crosscheck 2 の13 JSONL（git blob pinはclaim v2に記録）
- `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost75f-raw-sweep-audit-20261117.json`（blob `0951327a`）
- `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost75f-inflight-20261117.json`（claim v2）

## 制限

- これらは個別7石rootのengine検索verdictのみ。REFUTED-D10はloss証明ではなく
  「depth 10以内の先手勝ちなし」。manifest行は本sweepでは閉じない。
- solved 1473の簿記は不変（head 1473/174/6375/504596/4648/368510）。
- 11x11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4はいずれも
  **UNKNOWN** のまま。

## 次の一手

- census v11で75f行をswept除外（0 WIN7-D10 + 75 REFUTED-D10・証明書なし・
  fold不要）として14番目のmapに追加し、次ターゲット（census v10 runner-up
  `00000000000000403800000008000008`, cost 78, open 66）を選定する。
- 並走管轄のまま手を出さないもの: 66i receipt fold、73i証明書の出版、
  cost73k hybrid seed union / 8-way worker split memo merge measurementの追従。
