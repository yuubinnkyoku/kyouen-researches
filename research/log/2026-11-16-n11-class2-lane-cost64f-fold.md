# 2026-11-16：cost-64f fold着地 — 3 WIN7-D10 receiptsをhead 1435へfold・**新canonical head 1438/174/6410/507143/4683/371057** — 全chain再現+証明書3枚再検証+conflict census 0・並走のclaim v4（REFUTED計数訂正）をv5で継承・11×11はUNKNOWN

開始時main: `d660f89d`。本レーンの作業中に並走レーンがcost64f系の修正コミット（`139c6e0b` REFUTED-D10計数訂正・`fd109d3a`/`dd5d6af0` counter & cross-row cache audit・`63c5443a` audit出版修繕・`bc0740d1`/`60b926c2` audit再生成）を着地させたため、fold出版の直前に最新main（`60b926c21a`）を取り直し、**公開済みclaim v4（blob `b9d0f9fa7`・`results.refuted_d10_count` 64→61 = 56 swept + 5 transferred 訂正）をベースにv5（blob `b43303e8`・fold complete）を作成**した。v5はv4の全欄を保存し、top-level `fold` recordのみを追加。raw batch・det rerun・v15 crosscheck・presweep v2・parent-and-marginal audit・win3 manifestの全blobは最新mainと照合のうえ全て同一（`d9f5f377`/`29aedffc`/`59d42a6b`等）であることを確認済み。

## foldの全容（runpy chain reproduction）

1. **head 1435再現**: 13本の`reconstruct_tmp_*`前提を含む全chainを、公開済み`recompute_frontier_cost64d_receipts_20261116.py`のrunpyで再現（canonical 1405→75e 1407→60c 1410→65j 1419→64d 1435・全出力blob byte-identical・win23証明書23枚の再検証も内部でPASS）。
2. **sweep再導出**: 8 raw batch（blob pin全一致）から59 sweep候補を再集計し、presweep v2 bit tableの5 transferred（bits 21/35/55/64/109・harvested_refuted）と合わせて64候補全部の判定を再構成 — WIN bits [39,72,107]・REFUTED swept 56 + transferred 5 = **REFUTED-D10 61**（claim v4の訂正計数と恒等式ごとassert）・0 capped・54,905,391 nodes（pilots 3402×8別）・terminal [13,17]・andclose全。determinism rerun batch2（bits [14,18,22,26,31,32,33,39]・WIN bit 39含む最重batch）node-exact・v15 crosscheck（pilot 5949・anchors [0,32,39,118]）両方向一致。
3. **presweep v2 bit table再主張**: 64候補のD4 canon全てが再導出canonと一致・transferred 5本はharvested_refuted・swept 59本はopen・receipt roots 757/743 canons・harvest conflicts 0。
4. **parent-and-marginal audit再主張**: blob `d9f5f377`の`receipt_marginals_in_order`（publication順の**逐次**in-manifest marginals 1/0/2 — 全receiptが石経由でchildをcoverするため、bit 39がchildを閉じるまでbit 72/107のbaseline marginalはchildを含む点に注意）・3新規行（child cost 64 + `…a09002000000002000` cost 67 + `…20002801002000000080000` cost 63・unique cost delta 194）・7 parent-row incidences / 5 affected parents（edge cost delta 455）・投影head 1438/174/6410/507143/4683/371057とhistogramを、covers機構による逐次再導出と突き合わせ全一致。
5. **証明書3枚のbyte再検証**: win3 manifest（blob `29aedffc`）どおり、bit 107はwhole cert（1,007,877B・blob `98a3a9da`）、bits 39/72はpart1of2+part2of2+join receipt（39: `d53c3e00`+`cd495bcb`→whole 1,589,881B、72: `45c79099`+`2531c3b2`→whole 1,599,747B）のgit blob pin・md5・sorted-unique rows・root行・**root mobility == legal_candidates.py（3/3）**・BigInt union 0/0 + Bareiss sub-roots 50/51/41 all PASS・fbt_drops 0・fatal nullを再assert。totals 116,367 rows / 9,709,419 extraction nodes / 142 sub-roots / 4,197,505 cert bytes。
6. **conflict census**: 64候補のD4 orbit全てが1435時点のfolded roots（734@1419 + 64d receipts 23 = 757 receipt roots・743 distinct canons）と**重複0**。3 WIN rootsは3 distinct D4 orbitsで、全folded rootに対しraw-hex・D4両方でdisjoint。**WIN/LOSS conflict 0**。
7. **childの残存確認**: child `0000000000000080120a000000800000`（stones [23,49,51,57,60,71]）はhead 1435で両直接開親（shared `00000000000000003800000008002000` 31/2145・`0000000000000080120a000000000000` 43/3167・いずれもclass-2）にedge cost 64・dual demand c1=0,c2=2,c4=0で残存。
8. **fold（publication order = bits昇順・per-receipt marginals全pin）**: **childはbit 39でちょうど1回閉鎖**。zero-marginal receipt 1本（bit 72）。**total marginal 15 / marginal_in_manifest 3**・set-equality control（s_after == s_1435 ∪ covers(3 roots)）PASS。閉鎖3行はauditのnew_marginal_rowsと完全一致し、全行がc1=0（child c2=2,c4=0・a090 c2=2,c4=2・200028 c2=0,c4=2）。

## 新headとper-parent

- **新canonical head: 1438/174/6410/507143/4683/371057**（1435+3行・6413→6410・507337−194・4686−3・371251−194）。hist変化はc2=0,c4=2: 3013→3012・c2=2,c4=0: 803→802・c2=2,c4=2: 52→51のみ。
- per-parent（5親・7 incidences・edge cost delta 455）: shared `…03800000008002000` **31/2145→30/2081**・`…03800002080000000` **78/5837→76/5707**・`…8012020000000080000` **68/5202→67/5135**・`…80120a000000000000` **43/3167→41/3036**・`…020000003800000000080000` **61/4351→60/4288**。published auditの`affected_parent_deltas`と全一致。両直接開親ともchild行を保持しなくなった（childはmanifest内で閉鎖）。
- fold後のbest coverable class-2 3/209（K0863でdepth-10 receipt閉鎖不能のSTERILE行構成・不変）・second 5/364・best class-4 18/1460・audit-blocked 10/698は全て不変で、**top-candidates CSVは64d版とbyte-identical**（blob `838d98a3`）。

## 解釈上の注意

**solved 1438はmanifest被覆の簿記。WIN7証明書は個別7石rootのfirst-player win（depth 10以内）のみを証明。REFUTED-D10 61件はLOSS証明ではなく該当rootの深さ10内的反証のみ。標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class1・class2・class4、両開親・5 affected parentは引き続きUNKNOWN。**

## 成果物

- fold script: [recompute_frontier_cost64f_receipts_20261116.py](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_cost64f_receipts_20261116.py)（複数回実行で出力3ファイルbyte-identical・全assert PASS）
- fold JSON: [class-frontier-cost64f-receipts-recompute-20261116.json](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-cost64f-receipts-recompute-20261116.json)（blob `e11f31f3`）
- ranking CSV: [class-frontier-s5-ranking-after-cost64f-receipts-20261116.csv](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-s5-ranking-after-cost64f-receipts-20261116.csv)（blob `5d08ef27`）
- top-candidates CSV: [class-frontier-top-candidates-s6-after-cost64f-receipts-20261116.csv](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-top-candidates-s6-after-cost64f-receipts-20261116.csv)（blob `838d98a3`・64d版と同一内容）
- claim v5: [class2-lane-cost64f-inflight-20261116.json](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost64f-inflight-20261116.json)（blob `b43303e8`・並走v4 `b9d0f9fa7`〔計数訂正+cache audit〕をsupersede・全欄保存）

## 次の候補（着手前に最新census・orbit重複確認が必須）

- 次の最安open行は**census再計算**（64fの61 REFUTED-D10と3 WIN7-D10 verdictsをharvestへ追加した上で）で決定: runner-up cost-64行 `00000000000100003800000008080000`（claim target_context記載・59 open見込み）と、ranking上のcost-64/65帯の行が候補。orbit共有転送（presweep harvest）を確認してからsweep着手。
- 並走レーンの時間毎実行とバッティングしない範囲で、presweep v2方式のbit table事前生成（transferred候補の特定）を先回りして用意するとsweep開始が早まる。
