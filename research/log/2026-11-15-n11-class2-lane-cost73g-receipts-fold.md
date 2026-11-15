# 2026-11-15：cost-73g receipts fold — canonical head 1244 → 1249

開始時main: HEAD `784b1969`（本レーンのK0783追記push）。canonical baseline 1244（`class-frontier-cost72c-receipts-recompute-20261115.json`・blob `42dbb92e1505d05389e840e3368974b1c613b750`）。直前セッションでsweep・証明書8件・独立監査・claim v2・K0783追記まで完了済み。本セッションはclaim v3（fold IN FLIGHT fence）→ fold → claim v4の流れで実施した。

## fenceと並走確認

claim v3（schema v3・`fold_in_flight`キー・receipts_to_fold [31,54,56,62,69,81,89,113]・baseline head 1244 + blob `42dbb92e`再assert）を先頭にpush（commit `b41d9a1d`）。fold成果物のpush前に最新mainを再取得したところfive-row-q7レーンの新コミット（K0726 anchor verification・5301-5599 census・m36-class-split claim）が着地していたが、いずれも本チェーンの対象外で72c head JSONは不変・claim v3も無改変であることを確認した（rebase不要）。

## 成果1：cost-73g receipts fold（head 1244 → 1249）

`recompute_frontier_cost73g_receipts_20261115.py`（624行・72c fold scriptの統制構造を73g入力に適合）を書いて実行した。すべての統制がPASS:

- **baseline再構成**: 72c fold scriptをrunpy鎖（72c→70f→71c→78a+69h merge込みの前期鎖全体）で再現し、1244/6603/521339/4873/385062 head（72c head JSON blob `42dbb92e`・両CSVともblob-identical）をローカルで再生成。fold済みroot集合は**512個**（499 through cost-71c + 4 cost-70f + 9 cost-72c）。runpy鎖全体の所要は約1秒（純幾何・簿記計算のみ）。
- **入力検証**: 37 published input files（sweep audit・certificate manifest・10 raw batches・determinism rerun・4 v15 crosschecks・16 per-bit verify records・3 scripts・certificates README）をgit blob shaでbyte-exact検証。claimは内容検証のみ（blob pinning廃止の運用継続・cost-72b repairの教訓）。
- **childの残存確認**: parent1 `00000000000000801202000000200000` 21行/1615・parent2 `00000000000000801242000000000000` 59行/4656がchild `00000000000000849002000000000800`（edge cost 73・需要 c1=0,c2=2,c4=0・stones [11,49,60,63,66,71]）を行として持ち、開親はこの2つのみ。D4 lift: del66=parent1 bit-exact・del11=parent2 bit-exact・残り4削除は閉行。
- **sweep再導出**: 10 raw batch JSONLsから73候補を一度ずつ（claim列挙と一致）・**8 WIN7-D10（bits [31,54,56,62,69,81,89,113]）・65 REFUTED-D10・0 capped・総nodes 91,357,592**・pilot 3402×10・batch5 determinism rerun node-exact・v15 cross-engine（8 WIN node-matched・アンカー0/100/117 loss=false・pilot 5949×4）・8 distinct D4 win orbits。
- **証明書検証**: 8証明書16パートすべてpart bytesで直接検証（part bytes/md5/blob sha → join == whole md5・whole blob sha）・rows sorted-unique・sub-roots == loser mobility（合計450）・terminal 13..17（BigInt）/ 13,15,17（Bareiss）・per-bit verify記録16件の再読込・union 0/0・manifest totals再総和（**343,092 rows / 12,392,797 bytes / 94,100,994 extraction nodes**）。
- **root disjointness**: 8新root vs **512 folded roots**をraw-hex・D4両方で確認。
- **fold**: 公開順 [31, 54, 56, 62, 69, 81, 89, 113]でper-record marginalを拡張unionから再導出。**総marginal 39・in-manifest 5**・zero-mim receipts [56, 62, 69, 81, 113]・child orbit closureはbit31（公開順最初・全8 rootが自石削除でchildを被覆）・set等式 `s_after == s_1244 UNION covers(8 roots)`・**3回連続実行byte-identical**（head JSON md5 `4f36b505`）。

**fold後 frontier: solved 1249 / unique 6598 / cost 520,956 / open 4,868 / open_cost 384,679**。parent1（第2 coverable target S5）**19行/1463**（2行喪失: child + `00000000020000809002000000000800`）・parent2 **55行/4352**（4行喪失: child + `00000000000000801242000080000000` + `00000000000000841242000000000000` + `00000000000000849002000080000000`）。in-manifest計5行が閉じた（child + 4行）が、どちらのS5親も解決していない。次点class-2候補は変わらずthird target `00000000000000809102000000000000`（2行/143）。

## 成果2：claim v3 fence → v4 closureの運用

- claim v3（fold IN FLIGHT）push後にfoldを実施・claim v4（fold record: chain_head_before 1244…/after 1249…・receipts_folded・marginals・parents_after・parents_lost_rows・出力3 blob sha・controls・outstanding）に更新して成果物と同時pushした。fold scriptのsection 9（completed-claim control）がclaim v4と再計算の一致（head string・3出力blob再assert）を検証済み。
- push後のremote照合: head JSON（blob `e4fb98dc`）・ranking CSV（`5760754d`）・top-candidates CSV（`2da64221`）・fold script（`386b0666`）はdirectory listingのblob shaで、claim v4はraw CDN md5（`d6722677`）でbyte-exactを確認。
- 並走との衝突は一度もなし（fold成果物push時のHEAD移動はfive-row-q7レーンのみで本チェーン無影響）。

## 解釈境界（重要）

- solved数はmanifest被覆の簿記であり、いかなる局面のgame-theoretic値も意味しない。
- **REFUTED-D10はLOSS証明ではない**（depth-10以内の先手勝ちが無いことのみ）。
- 8つのWIN7証明書は個別7石rootからdepth-10以内の先手勝ちのみを証明する。child orbitの閉鎖は両開class-2親の残行を減らすが、どちらのS5親も解決せず、class 2・class 4も決定しない。
- **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class1・class2・class4は引き続きUNKNOWN**。

## 今後

- 次のfold baselineは本head 1249（`class-frontier-cost73g-receipts-recompute-20261115.json`・blob `e4fb98dc8670fbb85786ab02f017a0a95e357648`）。fold前に必ず最新mainを再取得し、並走laneのfold着地をチェックすること。**70g（8証明書）・65l（2 receipts）のfoldは本head 1249へのrebaseが必須**。
- 次のsweep候補: third target `00000000000000809102000000000000`の残り2行（cost 69: `00000000000000809102000000002000`・cost 74: `00000000000000809142000000000000`）が最安だが、69g/74e/74gの並走claimとの重複に注意。兄弟行 `00000000200000083800000000000200`（cost 73・第2開親 `00000000000000003800200008000000` 67行/5182）も未着手のまま残置。

**prose誤記の記録（70f baseline_mainと同じ運用）**: claim v2のno_prior_sweep_note（以降の版でも無修正）と本fold head JSONの `outstanding_not_folded.sibling_cost73_row` が兄弟行を `00000000220000083800000000000200` と引用しているが、正しいhexは `00000000200000083800000000000200`（機械生成のranking・top-candidates CSVs・fold再現で確認）。誤記hexはmanifest行ではなく、いかなるassert値・fold算術・証明成果物にも影響しない。公開済みhead JSONはbyte-unmodifiedとし、claim v4の `fold.erratum_sibling_hex` に記録した。次回のsweep/foldは正しいhexを対象にすること。

詳細: [fold head JSON](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-cost73g-receipts-recompute-20261115.json)、[ranking CSV](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-s5-ranking-after-cost73g-receipts-20261115.csv)、[top-candidates CSV](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-top-candidates-s6-after-cost73g-receipts-20261115.csv)、[fold script](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_cost73g_receipts_20261115.py)、[claim v4](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost73g-inflight-20261115.json)。
