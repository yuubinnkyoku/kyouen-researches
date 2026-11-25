# 2026-11-15：cost-77d / merged 75d+77d / cost-79a / cost-80d の4 fold第二独立検証 — 全統制PASS・12成果物byte-identical・bit-78重複root同一性と77d予測brief全数値一致を独立確認

開始時状況: canonical head **1305/6542/516793/4812/380516**（cost-80d receipts fold・head JSON blob `289c9337`）。当レーンが事前予測brief（`class2-lane-cost77d-fold-prediction-20261115.json`）を公開した後、並走laneが cost-77d receipts fold（head 1290→1299・lane-local）・merged cost-75d+77d warm-hygiene fold（1296→1302）・cost-79a receipts fold（1302→1304）・cost-80d receipts fold（1304→1305）を着地させた。本logの検証はcodeload tarballから再構築した隔離mirror（80d成果物50ファイルはmainからfetchしgit blob sha照合済み）による別環境・別実行で、着地セッションの状態は一切再利用していない。

## 成果1：4つのpublished fold scriptをend-to-endで2回ずつ再実行 — 全統制PASS・12成果物byte-identical

`recompute_frontier_cost77d_receipts_20261115.py`（445行）・`recompute_frontier_merged_cost75d_77d_20261115.py`（416行）・`recompute_frontier_cost79a_receipts_20261115.py`（436行）・`recompute_frontier_cost80d_receipts_20261115.py`（437行）をそのまま2回ずつ実行（全体で各回約28.5秒・2回とも全出力byte-identical）。各scriptは独立の短命サブプロセスで実行: runpy鎖はdel+gcでもプロセス内に状態が残り、同一インタプリタで4 script×2回を実行すると1回目は全PASSするのに2回目の途中でcgroup約1GB上限を超えてOOM kill（RC=137）することを実測した。プロセス分離で解決（各scriptのピークRSSは約150-200 MB）。全CONTROL PASS:

- **77d fold**: 77c head 1290/6557/517923/4827/381646 runpy再現（head JSON `7f2badce`+両CSV blob一致）・child genuinely remaining（両開親 13/1018・66/5192・lift stones {92},{21}）・sweep再導出（77候補・12 WIN7-D10 / 65 REFUTED / 0 capped・152,577,045 nodes・pilot 3402×10・det rerun node-exact・v15 12/12 WIN+3/3 refuted anchors）・証明書12件 581,661行 / 20,629,247 bytes / 703 sub-roots・12 root vs 565 folded roots raw+D4 disjoint・child閉鎖bit7・**head 1299/6548/517249/4818/380972**
- **merged 75d+77d warm-hygiene fold**: 75d head 1296/6551/517468/4821/381191再現（`c801e605`+両CSV）・warm-hygiene（77d childは1296 baselineで既解決・両開親のremaining rowsに不在 11/866・64/5036・child closure不主張）・11 receipts fold（bit78除外）・**head 1302/6545/517025/4815/380748**（marginal 51 / in-manifest 6・zero-mim 7/39/58/64/108・第二target 11/866不変・第2開親64/5036→58/4593）
- **79a fold**: merged head 1302再現（`97130384`+両CSV）・child genuinely remaining（11/866・73/5750・lift {52},{21}）・sweep再導出（79候補・3 WIN7-D10 bits 9/50/64 / 76 REFUTED / 0 capped・131,934,659 nodes）・証明書3件 165,209行 / 5,977,942 bytes / 178 sub-roots・3 root vs 580 folded roots raw+D4 disjoint・child閉鎖bit9・**head 1304/6543/516873/4813/380596**（第二target 11/866→10/787・第2開親73/5750→71/5598）
- **80d fold**: 79a head 1304再現（`7dea99ff`+両CSV）・child genuinely remaining（両開親 10/787・55/4417・lift {10},{99}）・sweep再導出（80候補・4 WIN7-D10 bits 48/61/81/96 / 76 REFUTED / 0 capped・131,430,976 nodes・det rerun node-exact・v15 4/4 WIN+3/3 refuted anchors）・証明書4件 202,272行 / 7,309,967 bytes / 243 sub-roots・BigInt+Number Bareiss 4/4 PASS・4 root vs 583 folded roots raw+D4 disjoint・child閉鎖bit48・**head 1305/6542/516793/4812/380516**（marginal 18 / in-manifest 1・zero-mim 61/81/96・第二target 10/787→9/707 でbest coverable class-2に・第2開親55/4417→54/4337）
- **12成果物すべてmainとbyte-identical**（git blob sha照合）: 77d head JSON `d19c96b7` 13,128B・77d ranking `a69f5e7a`・77d top-cand `49b7f378`・merged head JSON `97130384` 12,460B・merged ranking `aba88980`・merged top-cand `49b7f378`・79a head JSON `7dea99ff` 7,452B・79a ranking `d31201b1`・79a top-cand `34efacb3`・80d head JSON `289c9337` 8,033B・80d ranking `723e1e1e` 7,537B・80d top-cand `a38f1563` 7,243B

機械可読検証記録: [class2-lane-cost77d-merged75d77d-79a-folds-second-verification-20261115.json](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost77d-merged75d77d-79a-folds-second-verification-20261115.json)（10,662 bytes・md5 `2eda6d91…`・2回実行byte-identical・検証script [verify_cost77d_merged_79a_folds_second_independent_20261115.py](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/verify_cost77d_merged_79a_folds_second_independent_20261115.py)・540行）

## 成果2：bit-78重複rootの同一性とzero-marginalを独立確認（fold scriptに欠けていた統制）

予測briefが指摘した重点項目。merged fold scriptはbit-78を「root == 75d bit92 root」のcomment付きでreceiptsから除外しているが、**その同一性とzero-marginal性をassertする統制がscript内にない**（disjointness assertは11 rootのみに効く）。本検証で独立に確認:

- 77d bit-78 root `00000000100040801202000000200000` は **75d bit-92 receipt rootとraw-hex完全一致**（1296 inventoryにraw含む）
- 独立D4実装によるbit-78 rootの7つのdeletion orbitは**すべてhead 1296で既解決**（zero marginal）→ 11-receipt set等式と仮想12-receipt版が一致し、除外は算術的に正当

## 成果3：77d fold事前予測brief vs 着地merged fold — 全数値一致

fold前に公開した予測（blob `97db3dec`・script `4808dd64`）と着地merged foldの全数値照合:

- **head 5数値すべて一致**: 予測1302/6545/517025/4815/380748 == 着地merged head
- **totals一致**: union marginal 51 / in-manifest 6
- **per-bit 11/11一致**: 各bitのmarginal・in-manifest数・marginal hex集合まで完全一致（bit7: 4/0・bit12: 5/1・bit39: 5/0・bit58: 4/0・bit62: 5/1・bit64: 4/0・bit66: 5/1・bit94: 5/1・bit96: 5/1・bit108: 4/0・bit111: 5/1）
- **parent effects一致**: 第二target S5 11→11（喪失なし）・第2開親 `00000000000000003800400008000000` 64→58（同じ6行喪失）
- **zero-mimの簿記規約差のみ**: 予測[7,39,58,64,78,108]（bit-78をzero-marginal receiptとして計上）に対し着地[7,39,58,64,108]（bit-78を除外済み重複rootとして非計上）。寄与0で意味は同一
- 予測の`already_folded_root_duplicate`フラグ（bit-78 = true）は着地扱いと整合

## 成果4：独立D4・Bareissによる追加統制

- **独立8要素D4群**で12+3+4=19新rootを再正準化: 12 77d rootsは12 distinct orbitで565-root 1290 inventoryとraw+D4 disjoint・11 folded rootsは569-root 1296 inventoryとD4 disjoint（bit-78はinventory内=重複で正しい）・3 79a rootsは580-root 1302 inventoryとraw+D4 disjoint・4 80d rootsは583-root 1304 inventoryとraw+D4 disjoint・全19 rootがchild | 1<<bit・popcount 7
- **独立Bareiss候補列挙**: 77d child・79a child・80d childのlegal候補をscratchesから再導出し、77/79/80件ともclaimとbit-exact
- **独立marginal算術**: 11 merged receipts・3 79a receipts・4 80d receiptsのper-bit covers/marginalsを独立D4で再計算しpublished recordsとhex集合単位で一致・unionが1302・1304・1305状態を正確に再現
- **top-candidates CSV同一性の説明**: 77d後とmerged後のtop-candidates CSVがbyte-identical（`49b7f378`）は、両fold経路がスポートライト候補の残行集合（第二target 11/866等）を同じ状態に収束させるためで、両scriptの再実行によるbyte-identical再生成で正当性確認

## erratum（published blobは不変のまま本logに記録）

1. merged fold scriptのprose（published head JSONのmethod欄・section 6 print）は「the 12 roots asserted disjoint … the 12 receipts folded in publication order [7,12,39,58,62,64,66,78,94,96,108,111]」「set_equality_after_12: covers(12 cost-77d roots)」と記載するが、**codeは11 receiptsをfoldし（bit-78除外）disjointness assertも11 rootに作用**。bit-78 rootのcoversは1296 baselineで全解決（zero marginal・本検証で独立確認）のため算術には無影響。proseのみ。
2. 同script section 4のprint「CONTROL 12 published certificates asserted … 11/11 PASS」は11 certificatesが正。proseのみ。

## 解釈境界（重要）

- solved 1305はmanifest被覆の簿記であり、いずの局面のgame-theoretic値も意味しない。REFUTED-D10はLOSS証明ではない。WIN7証明書は個別7石rootからdepth-10以内の先手勝ちのみを証明する。
- 80d以降も並走laneがさらにsweep/foldを着地させる可能性がある。着手前に必ず最新mainを再取得すること。
- **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class1・class2・class4は引き続きUNKNOWN**。

## 今後

- 次のfold baselineはhead **1305**（`class-frontier-cost80d-receipts-recompute-20261115.json`・blob `289c9337`）。80dは着地済みで本検証が全範囲をカバー（child genuinely remaining・sweep・証明書4件・disjointnessすべてPASS）。
- 両audit script（`audit_published_chain_roots_independent_20261115.py` v3系・`audit_published_chain_roots_second_independent_20261115.py`）の77d/merged/79a/80d endpointへのv4拡張（PINS/ORDER・own_claim・own_baseline・CANONICAL_LINE・endpoint各エントリ）は次回以降の課題。bit-78重複rootのexactly-once簿記（1296 inventoryと77d receiptsの二重計上なし）を重点確認。

詳細: [merged head JSON](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-merged-cost75d-77d-receipts-recompute-20261115.json)、[79a head JSON](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-cost79a-receipts-recompute-20261115.json)、[80d head JSON](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-cost80d-receipts-recompute-20261115.json)、[77d head JSON](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-cost77d-receipts-recompute-20261115.json)、[予測brief](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost77d-fold-prediction-20261115.json)、[merge log](./2026-11-15-n11-class2-merged-cost75d-77d-warm-hygiene.md)、[79a fold log](./2026-11-15-n11-class2-lane-cost79a-sweep-certificates-and-fold.md)、[75d fold第二検証（前回）](./2026-11-15-n11-class2-lane-cost75d-fold-second-verification.md)。
