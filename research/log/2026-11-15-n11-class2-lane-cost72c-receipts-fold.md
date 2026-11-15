# 2026-11-15：cost-72c receipts fold — canonical head 1239 → 1244・claim blob pinningの廃止

開始時main: HEAD `ebe9cdca`（本レーンのclaim v3 push）。canonical baseline 1239（`class-frontier-cost70f-receipts-recompute-20261115.json`・blob `4d0f130e975b6a7bec4759387bd6d54dfe2b6a18`）。fold直前に最新mainを再取得し、並走の70g/65l foldいずれも着地していないこと・claimがまだv3（blob `2162d7bf`）であること・70f head JSONが不変であることをSHA headerで確認した（rebase不要）。

## 成果1：cost-72c receipts fold（head 1239 → 1244）

`recompute_frontier_cost72c_receipts_20261115.py`を書いて実行した。すべての統制がPASS:

- **baseline再構成**: 70f fold scriptをrunpy鎖で再現し、1239/6608/521701/4878/385424 head（70f head JSON・両CSVともblob-identical）を再生成。71c→70fのrunpy鎖全体がローカルで完結。
- **childの残存確認**: parent1 `00000000000000801202000000200000` 24行/1836・parent2 `00000000000000083800000008000000` 55行/4111がchild `00000000000000801202000000220000`（edge cost 72・需要 c1=0,c2=2,c4=0）を行として持ち、開親はこの2つのみ。D4 lift: del17=parent1 bit-exact・del21=parent2 bit-exact・残り4削除は閉行。
- **sweep再導出**: 9 raw batch JSONLsから72候補を一度ずつ（claim列挙と一致）・**9 WIN7-D10（bits [1,7,24,39,59,64,67,72,96]）・63 REFUTED・0 capped・総nodes 61,297,942**・pilot 3402×9・batch5 determinism rerun node-exact・v15 cross-engine（9 WIN node-matched・アンカー0/43/117 loss=false・pilot 5949×3）・9 distinct D4 win orbits。
- **証明書検証**: 9証明書18パートすべてpart bytesで直接検証（part bytes/md5/blob sha → join == whole md5・whole blob sha）・rows sorted-unique・sub-roots == loser mobility・terminal 13..17（BigInt）/ 13,15,17（Bareiss）・per-bit verify記録18件の再読込・union 0/0・manifest totals再総和（**321,781 rows / 11,604,178 bytes / 41,346,462 extraction nodes**）。
- **root disjointness**: 9新root vs 503 fold済みroot（499 through cost-71c + 4 cost-70f）をraw-hex・D4両方で確認。
- **fold**: 公開順 [1, 7, 24, 39, 59, 64, 67, 72, 96]でper-record marginalを拡張unionから再導出。**総marginal 43・in-manifest 5**・zero-mim receipts [39, 59, 64, 72, 96]・child orbit closureはbit1（公開順最初）・set等式 `s_after == s_1239 UNION covers(9 roots)`・3回連続実行byte-identical。

**fold後 frontier: solved 1244 / unique 6603 / cost 521,339 / open 4,873 / open_cost 385,062**。parent1 21行/1615（3行喪失: child + `00000000000000801202000000200002` + `00000000000000881202000000200000`）・parent2 52行/3898（3行喪失: child + `00000000000000083800000009000000` + `00000000000000801202000000020080`）。third target `00000000000000809102000000000000`（2行/143）が引き続き不変最安のcoverable class-2候補。

## 成果2：cost-70f head JSONのbaseline_main prose誤記の記録

fold中に、公開済み70f head JSONの`baseline_main`文が**cost-70eのhead数字（1235/6614/522131/4884/385854）と70e head blob（`a0171d4b`）を引用している**（実際にassertしているのは71c head 1235/6612/521988/4882/385711・blob `61af2eb3`）ことを検出した。prose-onlyのcopy-paste誤記で、70f fold scriptのassertは正しく、いかなる公開数値にも影響しない。履歴ファイルはbyte-unmodifiedとし、本fold head JSONの`baseline_erratum_note`（controls内）に記録した（bit112 md5誤記と同じ運用）。

## 成果3：claim blob pinningの廃止（運用変更）

cost-72b repairの教訓（claim closure updateがfold scriptのblob参照を壊し再実行不能になる循環）に対処するため、**fold scriptからclaimのINPUT_BLOBS pinningを外し、claimは内容検証のみ**とする70f方式に統一した。これにより公開済みscriptはclaimのclosure update後も無条件に再実行可能になる。代償としてfold head JSONの`published_inputs_byte_exact_vs_main`は37（claim分を除く）となり、claimのfoldレコード側にscript blob `144b41c6` を明記して相互参照を担保した。

## 解釈境界（重要）

- solved数はmanifest被覆の簿記であり、いかなる局面のgame-theoretic値も意味しない。
- **REFUTED-D10はLOSS証明ではない**（depth-10以内の先手勝ちが無いことのみ）。
- 9つのWIN7証明書は個別7石rootからdepth-10以内の先手勝ちのみを証明する。child orbitの閉鎖は両開class-2親の残行を減らすが、どちらのS5親も解決せず、class 2・class 4も決定しない。
- **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class1・class2・class4は引き続きUNKNOWN**。

## 今後

- 次のfold baselineは本head 1244（`class-frontier-cost72c-receipts-recompute-20261115.json`・blob `42dbb92e`）。fold前に必ず最新mainを再取得し、並走lane（70g/65l/69g/65j/74e）のfold着地をチェックすること。**70g（8証明書）・65l（2 receipts）のfoldは本head 1244へのrebaseが必須**。
- 次のsweep候補: third target `00000000000000809102000000000000`の残り2行（cost 69: `00000000000000809102000000002000`・cost 74: `00000000000000809142000000000000`）が最安だが、69g/74eの並走claimとの重複に注意。

詳細: [fold head JSON](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-cost72c-receipts-recompute-20261115.json)、[ranking CSV](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-s5-ranking-after-cost72c-receipts-20261115.csv)、[top-candidates CSV](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-top-candidates-s6-after-cost72c-receipts-20261115.csv)、[fold script](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_cost72c_receipts_20261115.py)、[claim v4](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost72c-inflight-20261115.json)。
