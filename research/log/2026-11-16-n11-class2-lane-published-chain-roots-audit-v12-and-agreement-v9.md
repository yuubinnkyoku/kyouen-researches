# 2026-11-16：published chain roots audit v12（両実装）+ agreement v9 — 第二 receipts fork（63j/65m/67d/70g・merged-4/merged-5/reconciled）組み込みでpinned chainをreconciled canonical-1405まで拡張

開始時main: `6c7955f6`（three-token transient band K0832群）。本レーン対象は、63i head 1367で分岐した**第二 receipts fork** — branch B（63j 1367→1394・65m 1394→1396）・branch C（63h bit-89 receiptを65m head 1396にrefoldするmerged-4）・branch D（67d bit-97 receiptを65m head 1396にfold）・**merged-5 canonical-1400 head**・branch-D 1398 headにfoldされた7 receiptのcost-70g fork head 1403を**reconciled canonical-1405 head**（`1405/6443/509457/4713/373180`・blob `b3ad19d7`）にreconcileした全簿記を監査体系に組み込む「次回定型」（[監査v11両実装+agreement v8](./2026-11-16-n11-class2-lane-published-chain-roots-audit-v11-and-agreement-v8.md)から機械拡張）。作業前にv11第一実装・v11第二実装・agreement v8の3出力がpublished版とbyte-identical再現することを各2回実行で再確認済み（第一実装出力blob `63d808d4`・第二実装出力blob `e43ef238`・agreement blob `4970a8d0`）。

## 変更内容

### 第一実装 v11→v12（in-place: `audit_published_chain_roots_independent_20261115.py`）

- POST70E_PINSに7 head追加（63j `35236daf`・65m `9798a9fc`・**merged-4 `a4cc8e95`（measured pin — 後続JSONからのquoteなし）**・67d `304c6afe`・merged-5 `777474fa`・70g-20261116 `8eb71c91`・reconciled `b3ad19d7`）。pins 110→**117**・post-70e 32→**39**
- own_claim/own_baseline: 696@63j（63i枝系）・704@65m・705@merged-4/705@67d・706@merged-5・712@70g-fork（lane-local）・**713@reconciled**
- key filter regexを `[a-z0-9]+_addition_on_[a-z0-9]+` に拡張（3箇所）— `cost63h_addition_on_1396`・`cost67d_addition_on_1396`・`cost70g_addition_on_canonical1400` を拾うため
- geometryに **symmetric_covers_exceptions** 新設: 非自明D4 stabilizerを持つroot（63j bit-93 root `00000000240000003800000048000000`）は7 deletion coversが4 D4 orbitに落ちる。record宣言covers値との一致を再導出で検証し、covers7規則からは例外リストに回す（corpus初の対称例外）
- head_arithmetic: fork path一般化 — FORK_BRANCH_HEADS表（merged-63h-63i←[63i]・merged-4←[63i,63j,65m]・merged-5←[]・reconciled←[]）でexternal枝寄与を名前付き枝headのrecords_of mim和から再導出。分類 **fork-reconcile**（reconciled head）新設。fr_text = fork_record値から最初の5-slash tuple
- **stale-baseline-quote** 分類新設: 67d/70g headのbaseline_mainは63j headの1394 quoteのstale copy。STALE_BASELINE表（67d←65m head・70g←67d head）で補正baseline（claimのchain_head_before・section 8でcross-assert）を再導出し、**補正delta == sum == union** を検証（67d: 1396→1398 delta 2・70g: 1398→1403 delta 5）。stale_baseline_errataとして出力
- CANONICAL_LINE += 4（63j・65m・merged-5の67d record・reconciledの70g records）→ canonical-line exactly-once **1233..1405・mim 172/distinct 172/multi 0**（136+27+2+2+5=172）。merged-4は65m head以降新marginalなし・70g fork head 1403はline外（77d precedent）
- 新sections: **8o**（63j/65m/67d/70g sweep claim fold-detail crosscheck — V12_SWEEP_CLAIMS表: publication_order・head totals zero-mim・certificates dir照合【70gは旧20261115 sweep 8枚と共存し15ファイル】・67d/70gはclaim chain_head_beforeがarith補正baselineと一致）・**8p**（merged-4: 1398/6450/509983/4720/373706・receipts_folded_here 1・merged total 56 = 63i 18+63j 29+65m 8+63h 1・fork_recordの枝head stateとblob sha quote・parents_at_merged_head・7265B）・**8q**（merged-5: 1400/6448/509842/4718/373565・両children bit 89/97閉鎖・57 receipts・reconciled headのcanonical_1400 quoteが7460B pinned fileとbyte-exact）・**8r**（reconciled: 1405/6443/509457/4713/373180・7 receipts（mim 5・zero-mim bit59/89/112・mim shrink 0）が70g fork headのrecordsとper-bit同一・fork_recordの両superseded head quote・coordinationの75e/76c re-base要求・11352B・published second-independent-verification record（blob sha+bytes+両CSV blob sha 26fa720b/c3433eee）との照合）・**8s**（**v12_method_prose_errata**: 4 sweep headのmethod/controls proseが63j fold scriptからのtemplate copyで、sweep数字・"set_equality_after_18"・bit-1 closure誤記・1394 baseline誤記などが各headのstructured recordと矛盾 — arith anomalyではなく出版prose erratumとして記録）

### 第二実装 v11→v12（新規file: `audit_published_chain_roots_second_independent_v12_20261115.py`）

- v11から複製+拡張（同一のcorpus事実を、第二実装自身の構造 — table駆動でない明示block — で検証する形で実装し、8oはendpoint recordとclaim fold双方を1表で照合する第二実装固有の構成）。POST70E_PINS 28→**35**（n_pins 106→**113**）・ORDER/own_claim/own_baseline/regex×3/cumulative 713×3/orbits 713−11に同様の追記
- 同じsymmetric_covers_exceptions・STALE_BASELINE・FORK_BRANCH_HEADS（fr_text一般化・fork-reconcile分岐・external_branch_heads entry）・stale_baseline_errata・fork4/fork5/reconciled/stale67d/stale70g entry asserts
- sections 8o（V12_SWEEP_ENDPONTS表: endpoint record + claim fold双方照合・child closure receipt照合・70g共有certificates dir 15ファイル）・8p/8q/8r（endpoint_m4/endpoint_m5/endpoint_rc + mrec63/hrec63h とのrecord一致 + second-independent-verification record + 両CSV sha実測照合）・8s（同一事実のprose errata）

### agreement v8→v9（in-place: `audit_dual_implementation_agreement_20261115.py`）

- AUDIT_PINS 18→**20**（v12両JSONのblob pin `2011009e`/`d788e238`）・第十一endpoint pair `pair_reconciled_canonical1405` を追加
- endpoint照合: 63j/65m/67d/70gは第一実装 `endpoint_heads`（claim_fold_details_checkedを分離して比較）と第二実装 `v12_sweep_endpoint_crosschecks` が完全一致・merged-4/merged-5/reconciled endpoint record同名キー完全一致・fork4/fork5/reconciled_head全レコード一致・**stale_baseline_quote_errataとv12_method_prose_errataがrecord-for-record一致**・bit78 root hex一致
- progression sanity: roots 713・canon endpoint 1405・cumulative_heads 39・child_closure_heads 46・orbits = roots−11
- result schema v9・supersedes v8文面・出力 `…dual-implementation-agreement-v9-20261115.json`

## 実行結果（全て2回実行でbyte-identical）

| 成果物 | 統制 | 結果 |
| --- | --- | --- |
| 第一実装 v12 | mirror上2回実行 | **AUDIT PASSED**・117 pins (26+52+39)・713 roots / **702 D4 orbits / 11 twin pairs**・receipt records 601 / anomalies 0・arith **91 heads** / anomalies 0（classification: cross-head-merge 1・fork-merge-rebase 3・fork-reconcile 1・no_numeric_baseline_quote 7・own-label-recompute 1・parallel-batch-union 11・sequential-fold-union 65・stale-baseline-quote 2）・canonical line 1233..**1405** mim 172/distinct 172/multi 0・出力 `class2-lane-published-chain-roots-independent-audit-v12-20261115.json`（152,696B・blob `2011009e`） |
| 第二実装 v12 | mirror上2回実行 | **AUDIT PASSED**・113 pins (26+52+35)・同一の713/702/11・601 records・91 heads/0 anomalies（classification counts同一）・canonical 1233..1405 mim 172・出力 `…second-independent-audit-v12-20261115.json`（149,854B・blob `d788e238`） |
| agreement v9 | mirror上2回実行 | **AGREEMENT CONFIRMED**・十一endpoint pair全部一致（reconciled-1405 pair: 39 heads / 713 roots / 702 orbits / 11 twins / canon 1233..1405 mim 172）・4 sweep + 2 merged + 1 reconciled endpoint record・fork算術・stale errata・prose errata全一致・bit-78 root hex全pair一致・出力 `…agreement-v9-20261115.json`（55,746B・blob `96dbe42c`） |

## 監査で確定した新規の出版事実（v12 sweep headのerrata）

1. **67d/70g headのbaseline_mainはstale quote**（63j head 1394のcopy）。実際のbaselineはclaimのchain_head_beforeが正しく（65m head 1396・67d branch-D head 1398）文書しており、補正baselineでのdelta算術は各head自身のreceipt recordsと完全に一致する。arith anomalyではない。
2. **4 sweep head（63j/65m/67d/70g）のmethod/controls proseが63j fold scriptからのtemplate copy**で、"18 roots vs 649"・`set_equality_after_18`・bit-1 closure誤記（実際は21/97/18）・63jのsweep数字流用などがstructured record（target/totals/addition records/claim）と矛盾。structured側は内部的に整合し全監査統制を支えるため、proseを出版erratum（`v12_method_prose_errata`）として記録した。
3. **70g certificates dirは新旧sweepで共有**（旧20261115: bits 9/20/29/34/62/70/76/119・新: bits 18/24/28/59/89/112/120 → 計15ファイル・受領bit集合はdisjoint）。
4. **63j bit-93 rootがcorpus初の非自明D4 stabilizer record**: 7 deletion coversが4 D4 orbitに縮退し、recordの宣言covers値4と監査再導出が一致（`symmetric_covers_exceptions`）。

## 意義

- **第二 receipts fork（4枝+2 merge+1 reconciliation）の全簿記が二重の独立実装+機械agreementで検証済み**。merged-4のexternal枝寄与36（=63i 7+63j 27+65m 2）は名前付き枝headのrecords_of mim和から直接再導出され、自己申告quoteに依存しない。
- canonical-line exactly-onceが**172 manifest hexes（1233..1405）**まで拡張。chain末端のどのhexも単一receiptからのみclaimされることが双実装で確認。canonical lineは 58c(1360)→63i(1367)→merged(1369)→63j(1394)→65m(1396)→merged-5(1400)→reconciled(1405) を通る。merged-4（lane-local）と70g fork head 1403（superseded）はline外。
- stale-baseline・prose errataを「異常」ではなく「分類+erratum」として簿記に組み込んだことで、**head quoteとclaim/structured recordの乖離が機械検出可能**になった。

## 解釈境界（重要）

- 監査は公開receiptの帳簿検証であり、いかなる局面の勝敗判定でもない。solved 1405はmanifest被覆の計数。
- WIN7証明書は各7石rootから深さ10以内の先手勝ちのみを証明する。REFUTED-D10はLOSS証明ではない。
- **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class1・class2・class4は引き続きUNKNOWN**。

## 今後

- frontier baselineはreconciled head **1405/6443/509457/4713/373180**（canonical）。以後のfoldはこのheadへのrebaseが必須（in-flight 75e/76c claimはcoordination noteでre-base要求済み）。
- 監査は次のfold着地ごとに機械拡張で追従する（次回: 76d fold onto 1405着地後にv13両実装+agreement v10）。
- 次の未sweep行: second-candidate S5 6/439 worklist（64/71 STERILE・75e artifacts unpublished・76c in-flight・76/77 unclaimed）。
