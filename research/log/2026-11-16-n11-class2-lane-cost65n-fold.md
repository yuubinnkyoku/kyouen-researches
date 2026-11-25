# 2026-11-16：cost-65n fold着地 — WIN7-D10 receipts 2本（bits 90・117）をhead 1441へfold・**新canonical head 1444/174/6404/506746/4677/370660** — 独立basis再構築（fold-projection方式）+prereg全フィールド一致（16/16 checks PASS）+conflict census 0・証明書2本byte再検証・11×11はUNKNOWN

開始時main: 65n sweep完了済み（claim v2 `257e7093` "completed NOT-STERILE"、foldは"deferred per protocol"で未着手）。並走レーンが**fold事前登録**（`class2-lane-cost65n-fold-preregistration-20261116.json`・git blob `da2b2292`・commit `0c237017`）と検証用check script（`check_cost65n_fold_receipt_vs_preregistration_20261116.py`）を事前出版済みであり、本foldは同preregの全machine-checkableフィールドと突合して着地させた。runpyによるcost-64f/64g chain再現は必要なfetch（約1.5GB）が本セッションの環境リセットで2回失敗したため、並走レーン出版済みの**fold-projection方式**（`fold_projection_head1441_tool_20261116.py`・commit `a7ac1757`）でhead 1441のbasis solved setを独立再構築するprotocol adaptとして実行した（fold JSONの`baseline_record`に経緯を明記）。

## foldの全容（独立basis再構築 + sweep再導出 + 証明書再検証）

1. **head 1441独立再構築**: 公開済みreceipt群から762 roots（100 class-frontier recompute JSON群・cost-64g fold JSON経由のbit-89 root込み・26 WIN7-only base証明書ファイル・6 named frontier recompute）を収集しD4 canonical 747 canons、MS5 manifest 6 parts（7,867 S6）+ 498 sweep winnersと合わせてfrontier再計算（`recompute_frontier_full.py`のsemanticsをverbatim移植）。head 6数値 **1441/174/6407/506945/4680/370859** とdemand hist（c2=2,c4=0: 801ほか）がpublish済みchain head（claim v2の`chain_head_at_claim`）ともpreregの`basis_summary`（blob `da2b2292`）とも完全一致。roots数762 vs census v4の761は同一D4 orbit内のhex差（coverage等価・cost-64g independent-agreement log commit `6719f0c6`記載のbookkeeping差異）。
2. **sweep再導出**: 8 raw batch JSONL（v16・全blob pin照合）から59 open候補を再集計 — **WIN bits [90, 117]（1,562,274 / 388,910 nodes）・REFUTED swept 57 + transferred 6（bits 35/50/51/55/64/109・root canon再導出一致）= 65/65・0 capped・92,530,349 nodes**（pilots 3,402×8別）・terminal [13,17]・andclose全。determinism rerun batch5/batch7 node-exact・v15 crosscheck両方向一致（anchors [9,90,94,117]・WIN bitsはv15でもloss=true 3,204,116 / 865,824 nodes）。claim v2（blob `257e7093`・v1 `c16ba5c9`をsupersede）の全計数・`legal_candidates` 65 bits・`open_candidates_to_sweep` 59 bits・`batch_bit_lists`・`transferred_refuted_d10_bits`のroot canonを恒等式ごとassert。
3. **census v4再assert**: presweep（blob `3dcb7cb6`・rows CSV `4ede6c25`）のbit tableでopen 59 == swept set・6 transferred root canons再導出一致・shared family 29/2017（child行 cost 65・demand c1=0,c2=2,c4=0・census receipt_win 0 / harvested_refuted 6 / open 59）。
4. **証明書2本のbyte再検証**: bit-90はparts 2枚join == whole **1,285,412 bytes**（md5 `616b15e7`・sha256再計算一致・whole git blob `c2460e59`）・35,627行sorted-unique・sub_roots 51・extraction 2,770,239 nodes・BigInt union 0/0 + Bareiss all PASS・root mobility == legal_candidates。bit-117はwhole **721,989 bytes**（git blob `ac0ea37d`）・20,047行・sub_roots 49・extraction 769,616 nodes・BigInt/Bareiss PASS。win2 manifest（blob `e2e4e3f5`）totals一致・**第二独立検証記録 byte_identical true** を再assert。
5. **conflict census**: 65候補のD4 orbit全てがhead 1441時点のfolded roots（762 roots・747 canons）と**重複0**。WIN 2 rootもraw-hex・D4両方で全folded rootとdisjoint。**WIN/LOSS conflict 0**。
6. **childの残存確認**: child `00000000000000801202010000800000`（stones [23,40,49,57,60,71]）はhead 1441で両直接開親（shared `…03800000008002000` 29/2017・第2親 `…8012020100000000 00` 48/3498・いずれもclass-2）にedge cost 65・dual demand c1=0,c2=2,c4=0で残存。
7. **fold（公開順 bit 90 → bit 117）**: childは**bit 90でちょうど1回閉鎖**（marginal 5・うちmanifest内1行=child）。bit-117 receiptはmarginal 6・うちmanifest内2行（`00000000000020003800000008080000`・`00000000000100809002000000000008`）。計**marginal 11・manifest内3行**・set-equality control（s_after == s_1441 ∪ covers(both roots)）PASS。閉鎖3行は全てc1=0の開行（hist変化はc2=2,c4=0: 801→798のみ）。全結果がprereg（blob `da2b2292`）のreceipts（marginal/mim/covers/D4 canon hex）・projected head・demand deltas・affected parentsと**フィールド単位で完全一致**。
8. **prereg一致チェック**: 並走レーン出版の`check_cost65n_fold_receipt_vs_preregistration_20261116.py`を本fold receiptに対して実行し**16/16 checks PASS**（projected head 6数値・hist・total marg/mim・rows_closed・child closed・affected parents before/after・lost rows per parent・incidences 6・edge cost delta 398・per-root marg/mim）。agreement record（all_pass true）を出版。

## 新headとper-parent

- **新canonical head: 1444/174/6404/506746/4677/370660**（1441+3行・unique 6407→6404・sum cost 506945−199・needed 4680−3 / 370859−199）。receipts 2本でmim 3 — bit-117の証明書がchildの他に2つのopen行も覆い、1本あたりの閉鎖効率はprereg見込み通り。
- per-parent（3親・6 incidences・edge cost delta 398）: shared `…03800000008002000` (c2) **29/2017→27/1883**（child 65 + collateral 132）・`…8012020000000000 80` (c2) **55/4137→53/4003**・第2親 `…8012020100000000 00` (c2) **48/3498→46/3368**。両直接開親ともchild行を保持しなくなった。
- fold後のbest coverable class-2 3/209・second 5/364・best class-4 18/1460・audit-blocked 10/698は全て不変で、**top-candidates CSVは64f/64g版とbyte-identical**（blob `838d98a3`）。

## 並走66cへの影響（orbit重複事前確認・実験事実）

本foldで閉じた3行（child・collateral 2行）と、並走レーンがsweep完了・証明書出版済みのcost-66c receipt roots 7本（child `00000000000000003800000008002008`のbits 73/75/79/87/96/97/112）は**raw-hex・D4 orbit両方で重複なし**。66c foldは新head 1444をbaselineにmarginal再計算が必要（本foldでchild 66c行は閉じていない）。

## 決定論性（再現性）

- 2回実行で出力4ファイル（fold JSON・ranking・top-cand・claim v3）ともbyte-identical。2回目はclaim v3のfold record `v2_fields`からv2を復元しblob `257e7093`と一致することを確認してから再foldする経路で、出版後の再実行（repo上でv3のみが存在する状態）でも全assertが通り同一出力になることを実証済み。script内のv2復元検査はv2 claimファイル自体のround-trip（blob `257e7093`）で行う。

## 解釈上の注意

**solved 1444はmanifest被覆の簿記。WIN7証明書はbits 90/117 roots `00000000040000801202010000800000`・`00200000000000801202010000800000` 単体のfirst-player win（depth 10以内）のみを証明。REFUTED-D10 63件（57 swept + 6 transferred）はLOSS証明ではなく該当rootの深さ10内的反証のみ。NOT-STERILEも行の勝敗を意味しない。標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class1・class2・class4、両開親・3 affected parent・66c行は引き続きUNKNOWN。**

## 成果物

- fold script: [recompute_frontier_cost65n_receipts_20261116.py](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_cost65n_receipts_20261116.py)（独立basis再構築+全入力blob pin+全assert PASS・2回実行byte-identical）
- fold JSON: [class-frontier-cost65n-receipts-recompute-20261116.json](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-cost65n-receipts-recompute-20261116.json)（blob `7390c540`・9,308B）
- ranking CSV: [class-frontier-s5-ranking-after-cost65n-receipts-20261116.csv](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-s5-ranking-after-cost65n-receipts-20261116.csv)（blob `da17bfec`・7,535B）
- top-candidates CSV: [class-frontier-top-candidates-s6-after-cost65n-receipts-20261116.csv](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-top-candidates-s6-after-cost65n-receipts-20261116.csv)（blob `838d98a3`・4,717B・64f/64g版と同一内容）
- claim v3: [class2-lane-cost65n-inflight-20261116.json](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost65n-inflight-20261116.json)（blob `ae35e76c`・16,760B・v2 `257e7093`全欄保存・v2 byte-identical復元可能。初回出版blob `137b9c56`では`results.fold`欄にv2の`deferred per protocol`文言がshallow-copy aliasingで残っていたため、`results.fold`を`complete...`に修正した上で出版し直した（script側もv2復元検査をv2 claim自体のround-tripに変更・修正版で2回実行byte-identicalを再確認））
- prereg agreement record: [class2-lane-cost65n-fold-preregistration-agreement-20261116.json](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost65n-fold-preregistration-agreement-20261116.json)（blob `684219f6`・3,846B・16/16 checks PASS）

## 次の候補（着手前に最新main・orbit重複確認が必須）

- **cost-66c fold**（並走レーンがsweep完了・証明書7本出版済み・claim v2 `b17e978e`系）: 新head 1444をbaselineにfold scriptを実行。receipt roots 7本とのD4 orbit重複は本log記載の通り現時点で0だが、fold時のconflict census・marginal再計算が必須。
- 並走のcost-65o（receipt-overlap audit出版済み commit `138bef70`）もfold待ち候補。本foldで閉じた3行と65o receiptsのorbit重複は同auditをhead 1444に対して再実行して確認すること。
