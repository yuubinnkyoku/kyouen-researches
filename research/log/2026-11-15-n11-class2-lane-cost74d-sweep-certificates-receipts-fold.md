# cost-74d子sweep完結・bit118証明書・15 receipt fold — chain head 1,179

自レーン（class2 lane）が第三class-2 coverableターゲットS5 `00000000000000809102000000000000` の未sweep子 `00000000000000809102020000000000`（cost 74、需要c1=0,c2=2,c4=0）をclaim・sweepし、15 WIN7-D10 receiptをchain head 1,163の上にfoldした。

## sweep（10 raw batch）

独立Bareiss 4x4列挙で74候補がmanifest edge cost 74とbit-exact一致（claim `class2-lane-cost74d-inflight-20261115.json`）。repo-verbatim v16 engineで**WIN7-D10 15件（bits 2,12,28,66,68,69,80,91,92,100,102,109,112,116,118）・REFUTED-D10 59件・打切り0・候補節点101,848,441**（pilot d6制御3,402 nodesは10/10 batchで一致、終局石数 [13,17]）。

交叉検査:
- 決定性再実行（`class2-lane-cost74d-det-rerun-20261115.jsonl`）: bits 2/102/118がraw batchとnode-exact一致（1,887,907 / 17,056,910 / 456,245、全loss=true）
- v15 cross-engine（`class2-lane-cost74d-v15-crosscheck-20261115.jsonl`）: 15 WIN7 bits全件loss=true（bit2 6,793,780 / bit12 8,136,371 / … / bit118 3,163,638）、REFUTEDアンカーbits 25/103はloss=false（16,147,976 / 8,529,979）、pilot 5,949×5
- 純Python+Bareiss行列式の監査スクリプト `audit_cost74d_raw_sweep.py` が74候補を幾何学的に再導出しclaimと完全一致。d4正規形はcost-69f監査公表値9件で検証、15 win rootはすべて別個のd4 orbit。監査JSON `class2-lane-cost74d-sweep-audit-20261115.json`（blob 2cf2c426ede5c5a720206bb65a84862fc2b1cbeb）

## bit118 WIN7証明書

root `00400000000000809102020000000000`（= child | 1<<118、敵合法初手50）の戦略証明書をrepo-verbatim抽出器（FBS 1<<20・fbt_drops 0・行LC_ALL=C整列一意化）で抽出: **5,030,722節点・28,719行・50/50 sub-root ok**。BigInt独立検証器で**PASS**（union missing/extra 0/0、終局石数 [13,17]、行sorted-unique、root安全性・全敵初手展開）。証明書は `output/class2-lane-cost74d-certificates/bit118-root-00400000000000809102020000000000.cert`（1,034,744 bytes、git blob sha `b96de16ac906721d9f7cdf82fed45bb032d57c1a`、md5 c99abba056adb3c4e1f8747c1a5b0ea5、sha256 9f4b9ce73e20f53fb616153a3a28ab77a4df0cfa817df68cdcb320c729d7ee7c）、記録JSON `class2-lane-cost74d-cert-bit118-record-20261115.json`（blob e411dcf6418a7d78c181d925392b6e997214ca8b）。残り14 WIN7 bitsの証明書抽出は未了（foldはraw sweep receipt+v15 anchorで実施）。

## 15 receipt fold — chain head 1,179

`recompute_frontier_cost74d_receipts_20261115.py` で以下をすべてassertしてからfoldした:

1. cost-70c warm batch-3 chain head 1,163をrunpyでbyte-identical再現（1163/684/527280/4954/391003、head JSON blob sha 50735896…照合）
2. 74d子がbaselineで本当に残存すること（parent 7行中、cost 74、child == parent | 1<<41）
3. sweep auditを10 raw batchから再導出（候補bit列・pilot 3402・判定・節点和101,848,441・batch blob sha・root == child|1<<bit全件）
4. v15アンカー・v16決定性rerunを公開JSONLからassert
5. bit118証明書をbytes×md5×sha256×git blob sha×行sorted-unique×sub-roots 50×union 0/0×fbt_drops 0で、記録JSONのblob sha込みで検査
6. 15 receiptを公開bit順（2,12,28,66,68,69,80,91,92,100,102,109,112,116,118）でfold。per-record marginalは拡大和集合から再導出。最初のreceipt（bit2）がchild軌道を閉鎖すること、fold後にchildが親のremainingから消えることをassert

結果: **+16 manifest軌道**（zero-mim receiptはbits 69/118 — 両者のmarginalは既存receiptで被覆済み。bit118がmim 0なのはfold順序上の帰属であり、証明書の価値を損なわない）。**chain headは解消S6 1,179・unique残り6,668・費用526,075・open需要4,938/389,798**（残りS5軌道175、c2=2,c4=0バケットは1,025→1,009）。2回実行でbyte-identical、push 4ファイルのremote git blob sha照合済み。

## 親S5の縮小と並走レーンへの影響（重要）

foldは74d子に加えて**2個の兄弟S6軌道も閉じた**:

- **cost-72b子 `00000000000000809102000002000000`（並走レーンがclaim・sweep・13証明書公開済み）は、74d bit91のWIN7 receiptの交差軌道lift（D4対称性による1石削除親被覆）で閉鎖された**
- cost-76子 `00000000000000809102000000004000` はbit102のliftで閉鎖

これにより親S5 `00000000000000809102000000000000` は**7軌道・519 → 4軌道・297**（残り: cost-69子 `00000000000000809102000000002000`〔69g、並走in flight〕・cost-74第二子 `00000000000000809142000000000000`〔未claim〕・cost-76子 `00000000000000809102000000000001`・cost-78子 `00000000000000809102000000400000`）。

**並走cost-72b foldへの指針**: 13 receiptのfoldはこの新しいhead 1,179をbaselineにして再実行すること（1,163基準のままfoldすると72b子の閉鎖が二重計上される）。72b子自体はbit91のreceiptで既に被覆済みのため、72b receiptのchildに対するmarginalは0になるが、各receiptの他のlift軌道は通常通りmarginalを持ちうる。fold慣行どおり拡大和集合からper-record marginalを再導出すれば帳簿は自動的に正しい。

## 未fold material・次の作業

- 残り14 WIN7 bitsの証明書抽出（候補: bit91 1,178,026節点 / bit68 1,283,700 / bit66 1,428,442 / bit92 1,445,828 / bit12 1,699,411が安価）
- cost-69g sweep（並走in flight、child `00000000000000809102000000002000`）
- cost-72b 13 receipt fold（並走、head 1,179へのrebase必要）
- cost-74第二子 `00000000000000809142000000000000` は未claim

解消計数はmanifest被覆の前進であり、盤全体の勝敗ではない。WIN7証明書は個別7石rootの深さ10以内のWINのみを証明し、REFUTED-D10は「深さ10以内の先手勝ち不存在」であって子の反証ではない。**標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class2・class4はいずれも引き続きUNKNOWN。**

成果物: [frontier再計算JSON](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-cost74d-receipts-recompute-20261115.json)、[ranking CSV](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-s5-ranking-after-cost74d-receipts-20261115.csv)、[top-candidates CSV](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-top-candidates-s6-after-cost74d-receipts-20261115.csv)、[foldスクリプト](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_cost74d_receipts_20261115.py)、[sweep audit](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost74d-sweep-audit-20261115.json)、[bit118証明書](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost74d-certificates/bit118-root-00400000000000809102020000000000.cert)、[bit118記録JSON](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost74d-cert-bit118-record-20261115.json)、[claim](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost74d-inflight-20261115.json)。raw batch 1–10・determinism rerun・v15 crosscheckは同output/の `class2-lane-cost74d-*`。
