# 2026-11-16：cost-64g fold着地 — WIN7-D10 receipt 1本（bit 89）をhead 1438へfold・**新canonical head 1441/174/6407/506945/4680/370859** — 全chain再現+bit 89証明書byte再検証+conflict census 0・並走のindependent rerun verification（`1b0bd2cf`）を継承・11×11はUNKNOWN

開始時main: `4ecadd43`（64g sweep + win1証明書出版済み）。本レーンの作業中に並走レーンが**independent parallel-rerun verification**（commit `1b0bd2cf`・59/59 node-exact vs published raw batches・bit 89 cert byte-identical・BigInt/Bareiss both PASS・census v3 transfer effects reproduced）を着地させたため、foldのbaseline_recordに同commitを明記して継承した。raw batch 8本・det rerun 2本・v15 crosscheck・claim v2（`c899b52d`）・sweep audit（`fc45acbd`）・win1 manifest（`e30be681`）・whole cert（`1d2cc167`）・BigInt/Bareiss verify records・census v3（`47174799`・rows CSV `89b11c4c`）の全blobを最新mainと照合し全て同一であることを確認済み。

## foldの全容（runpy chain reproduction）

1. **head 1438再現**: 公開済み`recompute_frontier_cost64f_receipts_20261116.py`（blob `522069ff`）をrunpyで全assert再実行し、1435 baseline→64f fold→head 1438/174/6410/507143/4683/371057を再現。5出力blob（fold JSON `e11f31f3`・ranking `5d08ef27`・top-cand `838d98a3`・claim v5 `b43303e8`・win3 manifest `29aedff8`…`29aedffc`）byte-identical。folded roots 760 / 746 D4 canons（census v3の`receipt_roots`とも一致）。
2. **sweep再導出**: 8 raw batch（blob pin全一致）から59 open候補を再集計し、census v3 bit tableの5 transferred（bits 5/29/104/111/119・harvested_refuted・root canon再導出一致）と合わせて64候補全部の判定を再構成 — **WIN bit [89]（690,457 nodes）・REFUTED swept 58 + transferred 5 = 64/64・0 capped・33,505,865 nodes**（pilots 3402×8別）・terminal [13,17]・andclose全。determinism rerun batch3/batch5 node-exact（msのみ相違）・v15 crosscheck（pilot 5949・anchors [1,43,89,118]）両方向一致（bit 89はv15でもloss=true 1,760,287 nodes）。claim v2の全計数・`batch_bit_lists`・`legal_candidates` 64 bits・`open_candidates_to_sweep` 59 bitsと恒等式ごとassert。
3. **bit 89証明書のbyte再検証**: whole cert 1,096,891B（blob `1d2cc167`）・30,373行のsorted-unique・root行・md5/sha256再計算一致・BigInt union 0/0 + subroots 45 PASS・Bareiss all PASS（45/45・winner 44,932・loser 14,916・terminal 9,172・range [13,17]）・**root mobility 45 == legal_candidates.py**・perMove 45手全ok・合計1,278,418 extraction nodes・win1 manifest totals一致。sweep audit（`fc45acbd`）のbatches・transfers・lift parents（SH 30/2081・第2親 50/3631）・independent enumerationも再assert。
4. **conflict census**: 64候補のD4 orbit全てが1438時点のfolded roots（760 roots・746 canons）と**重複0**。WIN rootもraw-hex・D4両方で全folded rootとdisjoint。**WIN/LOSS conflict 0**。
5. **childの残存確認**: child `00000000000100003800000008080000`（stones [19,27,59,60,61,80]）はhead 1438で両直接開親（shared `00000000000000003800000008002000` 30/2081・第2親 `00000000000000801202010000000000` 50/3631・いずれもclass-2）にedge cost 64・dual demand c1=0,c2=2,c4=0で残存。
6. **fold**: childは**bit 89でちょうど1回閉鎖**。receiptは7 S6 boardsをcoverし、1438 baselineで**marginal 6・うちmanifest内3行**（child + `00000000000000801202010000080000` cost 69 + `00000000020000801002010000080000` cost 65）。set-equality control（s_after == s_1438 ∪ covers(root)）PASS。閉鎖3行は全てc1=0（child c2=2,c4=0・他2行も開行）。hist変化はc2=0,c4=2: 3012→3011・c2=2,c4=0: 802→801・c2=2,c4=2: 51→50のみ。

## 新headとper-parent

- **新canonical head: 1441/174/6407/506945/4680/370859**（1438+3行・unique 6410→6407・sum cost 507143−198・needed 4683−3 / 371057−198）。レシート1本でmim 3 — 事前見込み（mim 1・head 1439）を上回る成果: bit 89の証明書はchildの他に2つのopen行（class-4/class-6親が保持）も覆った。
- per-parent（5親・7 incidences・edge cost delta 465）: shared `…03800000008002000` (c2) **30/2081→29/2017**・`…03800001000800000` (c4) **66/4719→64/4585**・`…8012020000000080000` (c2+c4) **67/5135→66/5066**・第2親 `…801202010000000000` (c2) **50/3631→48/3498**・`…020000003800000000080000` (c4) **60/4288→59/4223**。内訳: child 64×2（SH・第2親）・`…8012020100000080000` 69×3・`…20000801002010000080000` 65×2。両直接開親ともchild行を保持しなくなった。
- fold後のbest coverable class-2 3/209・second 5/364・best class-4 18/1460・audit-blocked 10/698は全て不変で、**top-candidates CSVは64f版とbyte-identical**（blob `838d98a3`）。

## 決定論性（再現性）

- 2回実行で出力4ファイル（fold JSON・ranking・top-cand・claim v3）ともbyte-identical。1回目はclaim v2入力、2回目は**claim v3入力からfold recordの`v2_fields`でv2を復元しblob `c899b52d`と一致することを確認してから再fold**する経路で、出版後の再実行（repo上でv3のみが存在する状態）でも全assertが通り同一出力になることを実証済み。

## 解釈上の注意

**solved 1441はmanifest被覆の簿記。WIN7証明書はbit 89 root `00000000020100003800000008080000` 単体のfirst-player win（depth 10以内）のみを証明。REFUTED-D10 63件（58 swept + 5 transferred）はLOSS証明ではなく該当rootの深さ10内的反証のみ。NOT-STERILEも行の勝敗を意味しない。標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class1・class2・class4、両開親・5 affected parentは引き続きUNKNOWN。**

## 成果物

- fold script: [recompute_frontier_cost64g_receipts_20261116.py](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_cost64g_receipts_20261116.py)（runpy chain込み・全assert PASS・2回実行byte-identical）
- fold JSON: [class-frontier-cost64g-receipts-recompute-20261116.json](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-cost64g-receipts-recompute-20261116.json)（blob `aff79002`・7,136B）
- ranking CSV: [class-frontier-s5-ranking-after-cost64g-receipts-20261116.csv](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-s5-ranking-after-cost64g-receipts-20261116.csv)（blob `ec52dc36`）
- top-candidates CSV: [class-frontier-top-candidates-s6-after-cost64g-receipts-20261116.csv](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-top-candidates-s6-after-cost64g-receipts-20261116.csv)（blob `838d98a3`・64f版と同一内容）
- claim v3: [class2-lane-cost64g-inflight-20261116.json](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost64g-inflight-20261116.json)（blob `125a728e`・15,226B・v2 `c899b52d`全欄保存・v2 byte-identical復元可能）

## 次の候補（着手前に最新census・orbit重複確認が必須）

- 次の最安open行は**census再計算**（64gの58 REFUTED-D10 swept・1 WIN7-D10・5 transferred verdictsをharvestへ追加した上でpresweep v4をhead 1441に対して生成）で決定する。見込みはSH親のcost-65行 `00000000000000801202010000800000`（census v3時点で59 open・6 transfers → 64g fold後はtransfers増加見込み）だが、bit tableの実測が正。
- ranking上はcost-64帯の次位行（`00000000000000801202000000080000` 系・`…03800001000800000` 系のclass-4行もfold後に相対上昇）が候補。presweep v4のbit table事前生成（transferred候補特定）を先回りして用意するとsweep開始が早まる。
