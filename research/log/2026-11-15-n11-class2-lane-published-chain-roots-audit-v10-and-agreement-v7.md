# 2026-11-15：published chain roots audit v10（両実装）+ agreement v7 — cost-58c/cost-63h endpoint組み込みでpinned chainを1362まで拡張

開始時main: `a5b6c4f7`（高速レーン F_n延長直後）。本レーンは同日早くに**cost-63h sweep+fold着地**（commit `0d5639cf`/`24572765`/`2c083b87`・head 1360→**1362**/6486/512653/4756/376376）を済ませており、並走laneの**cost-58c fold**（`dcd2ead`・head 1326→**1360**/6488/512785/4758/376508）も63h sweep中に着地済み。両foldの公開成果物を監査体系に組み込む「次回定型」（[監査v9両実装](./2026-11-15-n11-class2-lane-published-chain-roots-audit-v9-first-implementation.md)から機械拡張）を実施した。

## 変更内容

### 第一実装 v9→v10（in-place: `audit_published_chain_roots_independent_20261115.py`、`76c65fa3`→更新）

- POST70E_PINSに **58c head `62a411bb…`（26,118B）** と **63h head `647498b9…`（6,852B）** を追加（pins 106→**108**・post-70e 28→**30**）
- own_claimに58c 616+33=**649**・63h 649+1=**650**、own_baselineに58c←62a・63h←58cを追加
- CANONICAL_LINEに `cost58c_addition`（mim 34）と `cost63h_addition`（mim 2）を追記 → canonical-line hex-level exactly-onceが**1233..1362・mim 129/distinct 129/multi 0**に拡張
- 新section **8k（58c）**: head frontier (1360,6488,512785,4758,376508)・`totals.receipts`=34（static sweep count）とaddition 33件の区別を明示的に保持・bit76除外（BigInt verifier terminal guard 13..17 vs 証明書terminal 11..17）をclaim publication_order文字列とともにassert・証明書34ファイル（folded 33+excluded bit76）のbit集合整合・claim fold記録（before 1326→after 1360・receipts_folded 33・marginal 166/34・zero-mim [42,44,56,91,99,105,109,118]・child bit1・parents_after 21/1454, 27/1915）とbyte-exact照合
- 新section **8l（63h）**: head frontier (1362,6486,512653,4756,376376)・単一bit-89 receipt（mim 2・child+bonus orbit）・証明書はbit89の1件のみ・claim fold記録（opened at 1326 head・re-based before 1360→after 1362・receipts_folded 1・marginal 5/2・child bit89・parents_after 20/1391, 68/5202, 75/5416）とbyte-exact照合・**rebase二重裏付け**（head JSON `rebase_note` と claim fold `rebase_note` の両方にre-based 1360 baselineが記録されていることをassert）
- own_labelのrecompute接頭辞処理に `-recompute-20261116.json` を追加（58c用）

### 第二実装 v9→v10（新規file: `audit_published_chain_roots_second_independent_v10_20261115.py`、v9 `3216df36`から拡張）

- POST70E_PINS 24→**26**（n_pins 102→**104**）・POST70E_ORDER/own_claim/own_baseline/CANONICAL_LINEに同様の追記
- section **8k/8l** を第一実装と同じ実質内容で追加（endpoint recordのkey setは第一実装と完全一致させ、agreementの全record比較がそのまま成立）
- v9のmethod textにあった **"100 git blob pins"の過少記述**（実際の`controls.pins_checked`は102）をv10では正しく104と記述し、v9の過少を明示的に注記

### agreement v6→v7（in-place: `audit_dual_implementation_agreement_20261115.py`、`223c420a`→更新）

- AUDIT_PINS 14→**16**（v10両JSONをpin）・第九endpoint pair `pair_58c63h` を追加
- pins統制: post-70e差は引き続き正確に4（第一実装30 vs 第二実装26・71c/70f/73g/70gの4 pin proposals）

## 実行結果（全て2回実行でbyte-identical）

| 成果物 | 統制 | 結果 |
| --- | --- | --- |
| 第一実装 v10 | mirror上2回実行 | **AUDIT PASSED**・108 pins (26+52+30)・650 roots / **639 D4 orbits / 11 twin pairs**・receipt records 527・geometry anomalies 0・arith heads 82 / anomalies 0・child-closure heads 37・canonical line 1233..**1362** mim 129/distinct 129/multi 0・出力 `class2-lane-published-chain-roots-independent-audit-v10-20261115.json`（114,836B・blob `b4c4348d`） |
| 第二実装 v10 | mirror上2回実行 | **AUDIT PASSED**・104 pins (26+52+26)・同一の650/639/11・527 records・0 anomalies・canonical 1233..1362・出力 `…second-independent-audit-v10-20261115.json`（114,790B・blob `8b2b5428`） |
| agreement v7 | mirror上2回実行 | **AGREEMENT CONFIRMED**・九endpoint pair全部一致（58c/63h pair: 30 heads / 650 roots / 639 orbits / 11 twins / canon 1233..1362 mim 129）・bit-78 root hex全9 pair一致・出力 `…dual-implementation-agreement-v7-20261115.json`（33,356B・blob `49e8d217`） |

58c/63h endpoint recordは両実装で**全フィールド完全一致**（`endpoint_cost58c`==`endpoint_58c`・`endpoint_cost63h`==`endpoint_63h`）。cumulative_by_post70e_head（30 head分の全行）・convention-external receipts・child-closure・base/chain inventoryも全一致。v9第一実装はmirror上での再実行でpublished bytesとbyte-identicalであることも再確認済み。

## 意義

- これにより **cost-58cとcost-63hの両foldの全簿記（receipts・marginals・child closure・head遷移・claim fold record）が二重の独立実装で検証済み**となった。63hのsweep/certificate部分は着地時にtsverify+BigIntで検証済み、fold部分はrunpy鎖CONTROL PASSで検証済みであり、今回の拡張で「公開成果物のみからの独立監査」体制にも組み込まれた。
- 58cの `totals.receipts: 34`（fold scriptがsweep WIN数からstatic copyした値）と実際の33 fold receiptsの不一致は、**両監査が明示的に区別して保持**することになった（bug fixではなく文書化された事実として固定）。
- canonical-line exactly-onceが**129 manifest hexes（1233..1362）**まで拡張された。chain末端のどのhexも単一receiptからのみclaimされることが双実装で確認されている。

## 解釈境界（重要）

- 監査は公開receiptの帳簿検証であり、いかなる局面の勝敗判定でもない。solved 1362はmanifest被覆の計数。
- WIN7証明書は各7石rootから深さ10以内の先手勝ちのみを証明する。63h sweepの62件のREFUTED-D10はLOSS証明ではない。
- **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class1・class2・class4は引き続きUNKNOWN**。

## 今後

- frontier baselineはhead **1362/6486/512653/4756/376376**。以後のfoldはこのheadへのrebaseが必須。
- 次の未sweep cost-63候補 `00000000040000003800000048000000`（c1=0,c2=2,c4=0・63i claim対象外）のsweep+claimが次候補。63i（別lane claimed `d284456d`）には引き続き着手しない。
- 監査は次のfold着地ごとにv11機械拡張（両実装+agreement v8）で追従する。
