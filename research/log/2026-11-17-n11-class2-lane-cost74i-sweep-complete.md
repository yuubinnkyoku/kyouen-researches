# n11 class2-lane cost74i sweep完了: 74 bit全REFUTED-D10・勝ち7手目なし (2026-11-17)

## 背景

head-1473 presweep census v9（commit `7153fe58`）が選定したrank-1行
`00000000020000003800000088000000`（cost 74・parent `00000000020000003800000080000000`・
demand {c1:0, c2:1, c4:2}・legal 74 bits）をcost-74iとしてclaimし、同セッションで
fresh v17 depth-10 sweepを実行した。実行前にmain head `b8c76a4d`を再取得し、
同childへのclaim/raw batch/auditの不在を確認済み。

## 実行

- driver: `scripts/ev74i_batches_20261117.sh`（73lと同一形状: 69 open bitsを
  7×9 + 1×6、confirmation 5 bitsを別batch。engineはv17 blob `c132cc64`、
  depth 10・cap 1e9/bit・andclose 1・fresh engine per bit）。
- 9 batchを順に実行（batch 1〜8がopen bits、batch 9がconfirmation）。
  pilot_d6制御は9/9で期待値 {loss=false, nodes=3402, capped=false} と完全一致。
- 決定性: batch 1とbatch 8（最重bit 116を含む）を別プロセスで再実行し、
  非ms全フィールドでfield-identical。
- v15 cross-engine: 独立v15 engine（blob `8744fc65`）でconfirmation 5 bits +
  最重5 bits [4, 35, 88, 116, 120] を再探索。10/10 verdict一致
  （全てloss=false）・2/2 pilot 5949・0 capped。v15 nodes合計 64,022,261。

## 結果: 0 WIN7-D10 / 74 REFUTED-D10 / 0 capped

- 全74 candidate bit（= legal 74 bits全て）がREFUTED-D10。capなし。
  candidate nodes合計 56,125,895（pilot込み 56,156,513）。最重bit 116
  （5,970,739 nodes）。terminal stone range は全bit [13,17]・例外なし。
- **このchildには先手の勝ち7手目（depth 10以内）が1つも存在しない。**
  よって証明書抽出・BigInt再検証・receipt foldはすべて不要。行はaudit強度で
  完全確定（STERILE、64aと同種の全滅行）。
- confirmation 5 bits [30, 71, 72, 90, 115] は予測どおり全てREFUTED-D10で、
  独立D4 canon再導出で両側検証（5/5）: 30 = cost73f bit 27（raw同一・両側
  nodes 264011一致）、71 = cost58b bit 107、72 = cost71e bit 107、
  90 = cost73f bit 93、115 = cost74f bit 93（いずれもcanon等価のみ）。
  出典の生バッチ行からverdictを再読み出し（0 capped）。

## 成果物

- `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/ev74i_batches_20261117.sh`
- `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_cost74i_raw_batches_20261117.py`
- raw 9 batch + det 2 + v15 crosscheck 2 の13 JSONL（git blob pinはclaim v2に記録）
- `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost74i-raw-sweep-audit-20261117.json`（blob `e5c803ed`・2回実行でbyte-identical）
- `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost74i-inflight-20261117.json`（claim v2・blob `d915e120`）

## 制限

- これらは個別7石rootのengine検索verdictのみ。REFUTED-D10はloss証明ではなく
  「depth 10以内の先手勝ちなし」。manifest行は本sweepでは閉じない。
- solved 1473の簿記は不変（head 1473/174/6375/504596/4648/368510）。
- 11x11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4はいずれも
  **UNKNOWN** のまま。

## 次の一手

- census v10で74i行をswept除外（0 WIN7-D10 + 74 REFUTED-D10・証明書なし・
  fold不要）として13番目のmapに追加し、次ターゲット（census v9 runner-up
  `00000000020000003800020080000000`, cost 75, open 73）を選定する。
- 並走管轄のまま手を出さないもの: 66i receipt fold、73i証明書の出版、
  cost73k hybrid seed union / 8-way worker split memo merge measurement。
