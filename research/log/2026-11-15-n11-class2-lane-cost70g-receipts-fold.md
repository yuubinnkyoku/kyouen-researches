# 2026-11-15：cost-70g receipts fold — canonical head 1249 → 1254（warm-hygiene fold）

開始時main: HEAD `1822850f`（取得後に並走が進みpush直前は `e2750cb`・いずれも本実験dirには無影響）。canonical baseline 1249（`class-frontier-cost73g-receipts-recompute-20261115.json`・blob `e4fb98dc8670fbb85786ab02f017a0a95e357648`）。直前までのセッションでsweep・証明書8件・claim v2/v3・fold fence（`class2-lane-cost70g-fold-inflight-20261115.json`・commit `a5f0d7be`）まで完了済み。本セッションはfold実行・claim v4・fence v2 closureまで実施した。

## このfoldの特殊事情：warm hygiene（childは既に閉鎖済み）

cost-70gのchild `00000000000100809002000000000800`（edge cost 70・stones [11,49,60,63,71,80]）は**baseline 1249の時点で既に閉鎖済み**である。70f fold（head 1235→1239）のbit-84 receipt（root `00000000001000801202000002200000`）のcross-coverに含まれており、manifest内でsolved済み。両開親（parent1 `00000000000000801202000000200000` 19行/1463・parent2 `00000000000000801202010000000000` 58行/4203）ともchild行を残していない。したがって本foldはcost-62a/63a/71b band hygieneの先行例に従い、**child閉鎖を伴わない**「warm-hygiene fold」として実行した: per-receipt marginalはすべて拡張unionから再導出し、zero-marginal receiptは正の重複として簿記する。fold前の需要は開親のみから再導出し c1=0,c2=2,c4=0（lift: del80→parent1・del11→parent2・残り4削除は閉行）を再確認した。

さらに**bit-29 receiptは既fold済みrootのD4重複**である: root `00000000000100809002000020000800` は70f bit-84 root `00000000001000801202000002200000` とD4 canonical（`00000000000100809002000020000800`）で同一。これは公開済みcross-lane監査 `cost70f-70g-71c-cross-lane-d4-overlap-20261115.json`（blob `ba32c51b`）に記録済みの事実であり、bit-29のmarginalは厳密に0になる（fold7==fold8統制で確認: bit-29を除く7 receiptだけで同一状態に到達）。

## 成果1：cost-70g receipts fold（head 1249 → 1254）

`recompute_frontier_cost70g_receipts_20261115.py`（73g fold scriptの統制構造を70g入力・warm-hygieneに適合）を書き、**4回連続実行すべてbyte-identical**を確認した。統制はすべてPASS:

- **baseline再構成**: 73g fold scriptをrunpy鎖（73g→72c→70f→71c→前期鎖全体）で再現し、1249/6598/520956/4868/384679 head（73g head JSON blob `e4fb98dc`・両CSVともblob-identical）を再生成。fold済みroot集合は**520個**（512 through cost-73gの前段 + 8 cost-73g）。runpy鎖全体の所要は約1.3秒。
- **入力検証**: 19 published input files（sweep record・certificate manifest・cross-lane D4 overlap audit・9 raw batches・determinism rerun・v15 crosscheck・5 scripts）をgit blob shaでbyte-exact検証。claimとfold fenceは内容検証のみ（blob pinning廃止の運用継続・cost-72b repairの教訓）。
- **child既閉鎖の統制**: childがmanifest内・solved集合内・`covers(70f bit-84 root)`内であること、両開親の残行にchildがないこと、需要 c1=0,c2=2,c4=0 の開lift親からの再導出、をすべてassert。
- **sweep再導出**: 9 raw batch JSONLsから70候補を一度ずつ（claim列挙と一致）・**8 WIN7-D10 [9,20,29,34,62,70,76,119]・62 REFUTED-D10・0 capped・総nodes 63,592,195**（win sum 15,922,270）・pilot 3402×9・determinism rerun（batch5・bits [58,59,61,62,64,65,67,69]）node-exact（WIN bit62 586,769）・v15交差（8 WIN node-matched [9:10273907, 20:1523082, 29:10750468, 34:10250857, 62:4821985, 70:1408183, 76:9482275, 119:7787565]・refutedアンカー [6,86,98] loss=false・pilot 5949×11）。
- **証明書検証**: 8証明書を単一ファイルの実bytesで直接検証（git blob sha == manifest・header + root行・rows sorted-unique・root == child|1<<bit・sub-roots == loser mobility（合計434）・terminal 13..17・union 0/0）・manifest totals再総和（**302,270 rows / 10,905,613 bytes / 31,812,232 extraction nodes**）。
- **root-orbit簿記**: 8新rootは520 fold済みrootとraw-hexでdisjoint・**7つの新D4 orbit** + 記録済みcross-lane重複1つ（bit-29 == 70f bit-84・canonical `00000000000100809002000020000800`・公開監査JSONを再読込して突合）。
- **fold**: 公開順 [9, 20, 29, 34, 62, 70, 76, 119]でper-record marginalを拡張unionから再導出。**総marginal 33・in-manifest 5**（bit20/34/70/76/119が各1）・zero-mim receipts [9, 29, 62]・zero-marginal receipts [29]（記録済みD4重複）・set等式 `s_after == s_1249 UNION covers(8 roots)`・**fold7==fold8統制**（bit-29除外で同一状態）。

**fold後 frontier: solved 1254 / unique 6593 / cost 520,600 / open 4,863 / open_cost 384,323**。parent1（第2 coverable target S5）**19行/1463（不変）**・parent2 **53行/3847**（5行喪失: `00000000000000801202010000000002`・`00000000000000801202110000000000`・`00000000000000801206010000000000`・`00000000000040809002001000000000`・`00000000000100003800000008100000`・すべてcovers(8 roots)内）。in-manifest 5行が閉じたが**child orbitは本foldでは閉じておらず**（70f bit-84 cross-coverにより既に閉鎖）、どちらのS5親も解決していない。top-candidates CSVは73g版とbyte-identical（スポットライト4候補はいずれも行を喪失しなかった; 別名で再公開）。

## 成果2：claim v4 + fence v2 closureの運用

claim v3→**v4**（status "completed (sweep + certificates + receipts fold)"・fold block: chain_head_before 1249…/after 1254…・receipts [9,20,29,34,62,70,76,119]・per-receipt marginal + hex・bit29_d4_duplicate_note・erratum・parents_after/parents_lost_rows・出力3 blob sha + bytes・fold script blob `18b13fa9`・fold_runs_byte_identical 4）に更新。fold fenceも**v2 status completed**に更新（landed_head 1254・head JSON blob `73890fe3`・以降のfoldはhead 1254へのrebase必須と明記）。fold scriptのsection 9（completed-claim control）がclaim v4と再計算の一致（head string・3出力blob再assert）を検証済み。

pushは単一コミット（fold script + 出力3件 + claim v4 + fence v2・commit `bc4ff54d`）とし、push前に最新main（`e2750cb`）を再取得して本実験dirへの新コミットがないこと（= chain head 1249不変・70g fold未着地・fence無改変）を確認した。push後、6ファイルすべてremote raw CDNから再取得し**git blob shaでbyte-exact照合**（script `18b13fa9`・head JSON `73890fe3`・ranking `7397c805`・top-candidates `2da64221`・claim `b605ffe3`・fence `6c56f622`）。

**erratum（claim v4に記録）**: sweep recordのduplicate_root_checkはraw-hex検索のみ（8/8 roots 0 hits → "new coverage"）であり、D4意味でのbit-29重複を見逃していた。claimのsweep_results.certificatesの"8/8 new coverage"も同じ限界。どのchain headの被覆計数にも影響なし（bit-29のmarginalはいずれにせよ0）。証明書自体は独立検証済みの有効なWIN7-D10証明のまま。

## 解釈境界（重要）

- solved数はmanifest被覆の簿記であり、いかなる局面のgame-theoretic値も意味しない。
- **REFUTED-D10はLOSS証明ではない**（depth-10以内の先手勝ちが無いことのみ）。
- 8つのWIN7証明書は個別7石rootからdepth-10以内の先手勝ちのみを証明する。本foldはchild orbitを1つも閉じず（70f foldが閉鎖済み）、S5親も解決しない。
- **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class1・class2・class4は引き続きUNKNOWN**。

## 今後

- 次のfold baselineは本head **1254**（`class-frontier-cost70g-receipts-recompute-20261115.json`・blob `73890fe34580ec2f869a97a00b3e6400eda30c0a`）。fold前に必ず最新mainを再取し、並走laneのfold着地（cost-73h 4 receipts・65l 2 receiptsのrebase・69g/65j/74e/74g）をチェックすること。
- parent2 `00000000000000801202010000000000` は53行/3847が残存。次点class-2候補は変わらずthird target `00000000000000809102000000000000`（2行/143）。
- warm-hygiene foldの統制セット（child既閉鎖assert・zero-marginal正の簿記・D4重複の明示）は以降の重複可能性のあるfold（70f/70g/71c重複の教訓）で再利用する。

詳細: [fold head JSON](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-cost70g-receipts-recompute-20261115.json)、[ranking CSV](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-s5-ranking-after-cost70g-receipts-20261115.csv)、[top-candidates CSV](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-top-candidates-s6-after-cost70g-receipts-20261115.csv)、[fold script](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_cost70g_receipts_20261115.py)、[claim v4](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost70g-inflight-20261115.json)、[fold fence v2](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost70g-fold-inflight-20261115.json)。
