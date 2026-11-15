# 2026-11-16：published chain roots audit v11（両実装）+ agreement v8 — cost-63i/merged 63h+63i endpoint組み込みでpinned chainを1369まで拡張

開始時main: `3dd753a2`（merged 63h+63i fold `c3bd5b4f` + all-ones erratum修正2コミット）。本レーン対象は、並走していた二枝（cost-63h: 1360→1362・cost-63i: 1360→1367）を**merged head 1369/6479/512163/4749/375886**（blob `c3ff5036`）にreconcileしたmerged foldの全簿記を監査体系に組み込む「次回定型」（[監査v10両実装+agreement v7](./2026-11-15-n11-class2-lane-published-chain-roots-audit-v10-and-agreement-v7.md)から機械拡張）。作業前にv10第一実装・v10第二実装・agreement v7の3出力がpublished版とbyte-identical再現することを各2回実行で再確認済み。

## 変更内容

### 第一実装 v10→v11（in-place: `audit_published_chain_roots_independent_20261115.py`・25+13 edits）

- POST70E_PINSに **63i head `db0288f1…`** と **merged head `c3ff5036…`** を追加（pins 108→**110**・post-70e 30→**32**）。両blobともローカル実測。
- POST70E_ORDER末尾に63i・mergedを追加・own_claim 667@63i/668@merged・own_baseline 63i←58c・merged←63i
- head_roots_all/records_of/section6のkey filterを `re.fullmatch(r'[a-z0-9]+_addition_on_[0-9]+', k)` に拡張 — merged headの `cost63h_addition_on_1367`（63h枝のbit-89 receiptを1367にrefoldしたaddition）を拾うため
- head_arithmeticにfork branch新設: 分類 **'fork-merge-rebase'**。merged headはbaseline_mainを持たないためfork_record.common_baselineのslash形式5整数をparseし、**delta 9 = own 2 + external 7**（externalは63i headのrecords_ofのmim和と照合）
- CANONICAL_LINE: **63h head（1362）をlineから外し**lane-local化（77d precedentと同じ扱い）し、63i head（mim 7）とmerged head（mim 2）を追加 → canonical-line hex-level exactly-onceが**1233..1369・mim 136/distinct 136/multi 0**に拡張（129−2+7+2=136）
- child-closureにmerged headの明示entry追加（child = 63h headのtarget・bit-89で閉鎖）
- 新section **8m（63i）**: endpoint frontier (1367,6481,512295,4751,376018)・claim publication_order（18候補 [30,32,41,45,54,61,62,66,77,81,99,105,107,112,114,116,119,120]・mim 7・zero-mim 11件）・child bit-30・parents_after 17/1185+24/1704・head_json_bytes 16455のbyte-exact照合
- 新section **8n（merged）**: merged headのendpoint record・63h claimのreconciliation欄（merged head 1369 quoteとblob sha込み）とのcrosscheck
- fork63_entry（`fork_merge_head_63h_63i` controls entry）: baseline_quote [1360,6488,512785,4758,376508]・delta 9・sum/union mim 2・external 7をassert

### 第二実装 v10→v11（新規file: `audit_published_chain_roots_second_independent_v11_20261115.py`・37 edits）

- v10から複製+拡張。POST70E_PINS 26→**28**（n_pins 104→**106**）・POST70E_ORDER/own_claim/own_baseline/CANONICAL_LINE/endpoint record（`endpoint_63i`・`endpoint_merged_63h_63i`同名キー）に同様の追記
- 8m/8nと等価なsectionを追加し、fork_merge_head_63h_63i controls entryも同一実質で生成

### agreement v7→v8（in-place: `audit_dual_implementation_agreement_20261115.py`・27 edits）

- AUDIT_PINS 16→**18**（v11両JSONのblob pin）・第十endpoint pair `pair_63i_merged` を追加
- endpoint照合: `endpoint_cost63i`==`endpoint_63i`・`endpoint_merged_63h_63i`同名キー・fork_merge_head_63h_63i全レコード一致・bit78 root hex一致
- progression sanity: roots 668・canon endpoint 1369・cumulative_heads 32・child_closure_heads 39・orbits = roots−11
- result schema v8・date 2026-11-16・supersedes v7文面

## 実行結果（全て2回実行でbyte-identical）

| 成果物 | 統制 | 結果 |
| --- | --- | --- |
| 第一実装 v11 | mirror上2回実行 | **AUDIT PASSED**・110 pins (26+52+32)・668 roots / **657 D4 orbits / 11 twin pairs**・receipt records 546 / group records 40 / anomalies 0・arith 84 heads / anomalies 0・child-closure heads 39・canonical line 1233..**1369** mim 136/distinct 136/multi 0・published hex errata 1（従来通り）・convention-external 1・出力 `class2-lane-published-chain-roots-independent-audit-v11-20261115.json`（120,223B・blob `63d808d4`） |
| 第二実装 v11 | mirror上2回実行 | **AUDIT PASSED**・106 pins (26+52+28)・同一の668/657/11・546/40・84 heads/0 anomalies・39・canonical 1233..1369 mim 136・出力 `…second-independent-audit-v11-20261115.json`（120,190B・blob `e43ef238`） |
| agreement v8 | mirror上2回実行 | **AGREEMENT CONFIRMED**・十endpoint pair全部一致（63i/merged pair: 32 heads / 668 roots / 657 orbits / 11 twins / canon 1233..1369 mim 136）・fork-merge-rebase算術（delta 9 = own 2 + external 7）とmerged endpoint recordが両実装で完全一致・bit-78 root hex全pair一致・出力 `…dual-implementation-agreement-v8-20261115.json`（38,364B・blob `4970a8d0`） |

63i/merged endpoint recordは両実装で**全フィールド完全一致**。cumulative_by_post70e_head（32 head分の全行）・convention-external receipts・child-closure・base/chain/baseline inventoryも全一致。運用面: mirror内のv10第一実装出力が途中テスト実行で上書きされていたため、退避済みpublished版（ref/）のblob shaがpublished pin `b4c4348d…`と一致することを確認のうえmirrorに復元してからagreement v8を実行した（重要証拠はrepo側published版で不変）。

## 意義

- **二枝fork（63h/63i）のreconciliationを含むmerged foldの全簿記が、二重の独立実装+機械agreementで検証済み**となった。merged headのdelta分解（own 63i枝 2 + external 63h枝 7）は外部寄与を63i headのrecords_ofのmim和と直接照合しており、単なる自己申告のquoteに依存しない。
- canonical-line exactly-onceが**136 manifest hexes（1233..1369）**まで拡張。chain末端のどのhexも単一receiptからのみclaimされることが双実装で確認。63h head（1362）はlane-local化され、canonical lineは 58c(1360)→63i(1367)→merged(1369) を通る。
- 63i sweep・merged foldの着地時検証（tsverify+BigInt・runpy鎖）に加え、「公開成果物のみからの独立監査」体制に組み込まれた。

## 解釈境界（重要）

- 監査は公開receiptの帳簿検証であり、いかなる局面の勝敗判定でもない。solved 1369はmanifest被覆の計数。
- WIN7証明書は各7石rootから深さ10以内の先手勝ちのみを証明する。REFUTED-D10はLOSS証明ではない。
- **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class1・class2・class4は引き続きUNKNOWN**。

## 今後

- frontier baselineはmerged head **1369/6479/512163/4749/375886**。以後のfoldはこのheadへのrebaseが必須。
- 並走laneの**cost-63j sweep着地済み**（commit `50e6a1b3`・child `00000000040000003800000048000000`・63候補 29 WIN7-D10 / 45 REFUTED-D10）。ただし63j fold head `class-frontier-cost63j-receipts-recompute-20261116.json` は**63i枝head 1367 baselineのまま**であり、merged head 1369へのre-baseが未実施 → 次回は63j foldの1369へのre-base（merged recompute）と**監査v12（両実装+agreement v9）**が必要。並走laneのmerged fold fresh-mirror reproduction（`daf30032`・logのみ）も着地済みで本監査結果と整合。
- 監査は次のfold着地ごとに機械拡張で追従する。次の未sweep行: cost-64 `00000000000000801202000050000000`（c1=0,c2=2,c4=0）・`00000000000000801282000040000000`（c1=1,c2=1,c4=0）。
