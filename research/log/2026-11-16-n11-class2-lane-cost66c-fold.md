# 2026-11-16：cost-66c fold着地 — WIN7-D10 receipts 7本（bits 73/75/79/87/96/97/112）をhead 1444へfold・**新canonical head 1450/174/6398/506297/4671/370211** — 独立basis再構築+prereg全フィールド一致（16/16 checks PASS）+conflict census 0・証明書7本byte再検証（11.2MB）・11×11はUNKNOWN

開始時main: 並走レーンのcost-65n fold着地済み（commits `109cea3f`/`d99014af`・新head **1444**）で、本レーンはcost-66c foldの**事前登録**（`class2-lane-cost66c-fold-preregistration-20261116.json`・git blob `809ad05e`・commit `aca9d762`・projection artifact `da8cab2f`）を出版済み。65o sweepは並走IN FLIGHT（着手禁止）。本foldは同preregの全machine-checkableフィールドと突合して着地させた。

## foldの全容（独立basis再構築 + sweep再導出 + 証明書7本再検証）

1. **head 1444独立再構築**: 公開済みreceipt群から764 roots（101 class-frontier recompute JSON群・cost-64g fold JSON経由のbit-89 root・**cost-65n fold JSON経由のbit-90/bit-117 roots**込み・26 WIN7-only base証明書ファイル・6 named frontier recompute）を収集しD4 canonical **749 canons**、MS5 manifest 6 parts（7,867 S6）+ 498 sweep winnersと合わせてfrontier再計算（`recompute_frontier_full.py`のsemanticsをverbatim移植）。head 6数値 **1444/174/6404/506746/4677/370660** とdemand histがpublish済みchain head（65n fold JSON `frontier_after_cost65n`）ともprereg `basis_summary`（blob `809ad05e`）とも完全一致。
2. **sweep再導出**: 8 raw batch JSONL（v16・全blob pin照合）から59 open候補を再集計 — **WIN bits [73, 75, 79, 87, 96, 97, 112]（nodes 1,380,970 / 2,092,539 / 1,078,921 / 2,016,731 / 2,363,101 / 689,724 / 12,574,920）・REFUTED swept 52 + transferred 7（bits 5/25/70/81/84/115/119・root canon再導出一致）= 66/66・0 capped（解決後）・84,180,263 definitive nodes**（as-run 81,605,344・pilots 3,402×8別）・terminal [13,17]・andclose全。bit-112 cap eventはraised cap 80,000,000で解決（capped attempt 10,000,001 → 12,574,920 nodes WIN7-D10・determinism rerun node-exact）。determinism rerun batch5 8 bits node-exact・v15 crosscheck両方向一致（anchors [30,73,83,96]・WIN bits 73/96はv15でもloss=true 3,128,502 / 5,027,518 nodes・REFUTED 30/83は 16,840,620 / 653,399 nodes）。claim v2（blob `ed21be88`）の全計数・`legal_candidates` 66 bits・`open_candidates_to_sweep` 59 bits・`planned_batch_bit_lists`・`win7_d10_root_hexes`・`transferred_refuted_d10_bits`のroot canonを恒等式ごとassert。
3. **census v4再assert**: presweep（blob `3dcb7cb6`・rows CSV blob pin）のbit tableでopen 59 == swept set・7 transferred root canons再導出一致・shared family 29/2017（child行 cost 66・demand c1=0,c2=1,c4=0・census receipt_win 0 / harvested_refuted 7 / open 59・open_after_census 59）。
4. **証明書7本のbyte再検証**: split certs bit-73 **1,260,573 B（parts 2）**・bit-75 **1,457,491 B（parts 2）**・bit-87 **1,514,876 B（parts 2）**・bit-96 **1,973,437 B（parts 2）**・bit-112 **2,774,034 B（parts 3・初の3-part split）**はparts join == whole・md5/sha256/whole git blob再計算一致。whole certs bit-79 **1,107,891 B**・bit-97 **1,130,350 B**はblob pin照合。全7本：header/root行・310,129行sorted-unique・BigInt union 0/0（bigint_recordのverdict/rows_sorted_unique/subroots_passed 44/53/45/50/51/45/58 = 計348・winner/loser/terminal counts）・Bareiss all_subroots_pass true・root mobility照合・win7 manifest totals（rows 310,129 / extraction 42,779,918 / cert_bytes 11,218,652）一致。
5. **conflict census**: 66候補（59 swept + 7 transferred）のD4 orbit全てが互いにdistinctで、head 1444時点のfolded roots（764 roots・749 canons）と**重複0**。WIN 7 rootsもraw-hex・D4両方で全folded rootとdisjoint。**WIN/LOSS conflict 0**。
6. **childの残存確認**: child `00000000000000003800000008002008`（stones [3,13,27,59,60,61]）はhead 1444で唯一直接開親（shared `…03800000008002000` 27/1883・class-2）にedge cost 66・demand c1=0,c2=1,c4=0で残存。
7. **fold（公開順 bit 73 → 75 → 79 → 87 → 96 → 97 → 112）**: childは**bit 73でちょうど1回閉鎖**（marginal 7・うちmanifest内1行=child）。per-bit marginal/mim: 73:7/1・75:4/0・79:5/1・87:5/1・96:4/0・97:4/1・112:6/2。計**marginal 35・manifest内6行**（child + collateral 5行 `…8012020100000000 80`系）・set-equality control（s_after == s_1444 ∪ covers(7 roots)）PASS。閉鎖6行は全てc1=0の開行（hist変化: c2=1,c4=0: 212→208・c2=1,c4=2: 9→8・c2=2,c4=0: 798→797）。全結果がprereg（blob `809ad05e`）のreceipts（marginal/mim/marginal_hexes/manifest_hexes/covers/D4 canon hex・d4_orbit_distinct）・projected head・demand deltas・affected parentsと**フィールド単位で完全一致**。
8. **prereg一致チェック**: 66c版check script（65n版からの機械変換・EXPECTED 1450 head・66c child・blob `809ad05e`/commit `aca9d762`）を本fold receiptに対して実行し**16/16 checks PASS**（projected head 6数値・hist・total marg/mim 35/6・rows_closed 6行・child closed・affected parents 6親before/after・lost rows per parent・incidences 8・edge cost delta 596・per-root marg/mim 7本）。agreement record（all_pass true）を出版。

## 新headとper-parent

- **新canonical head: 1450/174/6398/506297/4671/370211**（1444+6行・unique 6404→6398・sum cost 506746→506297・needed 4677→4671 / 370660→370211）。receipts 7本でmim 6 — bit-79/87/97/112の証明書がchildの他に計5つのopen行も覆い、prereg見込み通りのcollateral効果。
- per-parent（6親・8 incidences・edge cost delta 596）: shared `…03800000008002000` (c2) **27/1883→25/1748**（child 66 + collateral 69）・`…8012020100000000 0080` (c2) **53/4003→52/3929**・`…80120201000000080000` (c2) **66/5066→65/4988**・`…80120201000020000000` (c2) **46/3497→45/3420**・`…80120201000100000000` (c2) **71/5912→69/5758**・`…20801002000000080000` (c2) **88/7439→87/7361**。唯一直接開親はchild行を保持しなくなった。
- fold後のbest coverable class-2 3/209（`00000000000000801202000000200000`）・second 5/364・best class-4 18/1460（`00000000020000003800000080000000`）・best class-1=audit-blocked 10/698は不変で、**top-candidates CSVは64f/64g/65n版とbyte-identical**（blob `838d98a3`）。

## 実装メモ（実験事実として記録）

本セッションでscriptを生成して初回実行した際、3箇所のassert仕様のズレで停止し修正した（claim v2 `win7_d10_root_hexes` がdict形式・bigint-verify JSONが`bigint_record`ラッパー持ち・bareiss変数名）。最終版（出版blob `898cfa61`）で全assert PASS。修正はすべて入力ファイルの実構造にassertを合わせるもので、pinned値そのものの変更は無し。

## 解釈上の注意

**solved 1450はmanifest被覆の簿記。WIN7証明書は7 roots単体のfirst-player win（depth 10以内）のみを証明。REFUTED-D10 59件（52 swept + 7 transferred）はLOSS証明ではなく該当rootの深さ10内的反証のみ。NOT-STERILEも行の勝敗を意味しない。標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class1・class2・class4、6 affected parent・残り6,398行は引き続きUNKNOWN。**

## 成果物

- fold script: [recompute_frontier_cost66c_receipts_20261116.py](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_cost66c_receipts_20261116.py)（blob `898cfa61`・82,449B・独立basis再構築+全入力blob pin+全assert PASS）
- checker script: [check_cost66c_fold_receipt_vs_preregistration_20261116.py](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/check_cost66c_fold_receipt_vs_preregistration_20261116.py)（blob `4a5e020c`・8,115B）
- fold JSON: [class-frontier-cost66c-receipts-recompute-20261116.json](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-cost66c-receipts-recompute-20261116.json)（blob `8783999e`・18,061B）
- ranking CSV: [class-frontier-s5-ranking-after-cost66c-receipts-20261116.csv](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-s5-ranking-after-cost66c-receipts-20261116.csv)（blob `53332293`・7,535B）
- top-candidates CSV: [class-frontier-top-candidates-s6-after-cost66c-receipts-20261116.csv](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-top-candidates-s6-after-cost66c-receipts-20261116.csv)（blob `838d98a3`・4,717B・64f/64g/65n版と同一内容）
- claim v3: [class2-lane-cost66c-inflight-20261116.json](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost66c-inflight-20261116.json)（blob `6dd30913`・15,172B・schema `n11-class2-lane-cost66c-fold-complete-20261116-v3`・v2 blob `ed21be88`全欄保存・v2 byte-identical復元可能（claimファイルround-trip検査内蔵）・65n v3出版時のshallow-copy aliasing問題は本scriptでは新規キー追加のみで構造的に回避）
- prereg agreement record: [class2-lane-cost66c-fold-preregistration-agreement-20261116.json](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost66c-fold-preregistration-agreement-20261116.json)（blob `16d36921`・4,378B・16/16 checks PASS）

## 次の候補（着手前に最新main・orbit重複確認が必須）

- **cost-66d claim-prep**: fold後rankingで次点open行を確認してから（best coverable 3/209 `00000000000000801202000000200000` が最有力・second 5/364）。
- 並走のcost-65o（IN FLIGHT・着手禁止）: **cross-row watch item** — 66c bit-83 root canon `00000000000000a09002080080000000` は65o claim v1のopen bit-43候補とD4同一（REFUTED-D10 verdict here）。65o完了更新時にこのverdictを転送するかWIN/LOSS conflict調査を要する（claim v2 `cross_row_watch`に記載済み・両レーンの完了時に要対応）。
