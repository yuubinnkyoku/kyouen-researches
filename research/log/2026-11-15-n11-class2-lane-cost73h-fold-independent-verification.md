# 2026-11-15：cost-73h foldの第二独立検証 — head 1257が別構成scriptと再構築mirrorの両方で再現

開始時状況: (a) sandbox環境リセットが2回連続し、ローカル検証ツリーを喪失 → codeload tarball 1リクエスト（約2.8GBストリーム、実験dirのみtar wildcards抽出・約270秒）で実験mirrorを再構築（MS5 manifest 6 CSV・73h入力27ファイル+証明書parts 8個、全blob照合、欠落なし）。(b) 本sessionがhead-1249ベースでfold導出を終えclaim v4 draftまで作成した直後に、同じ毎時レーンの並走実行がcost-70g fold（`bc4ff54d`、head 1249→1254）とcost-73h fold（`a422f2d8`、head 1254→1257）を連続してmainに着地した。本sessionはfence_note provision（70g先着時はその時点のcanonical headにrebaseして再導出）に従い1254ベースで全数値を再導出し、以後「着地済み成果の第二独立検証」に切り替えた。本logの検証はすべて、mainとは独立に再構築した別環境・別実行によるものである。

## 成果1：cost-73h fold（head 1254 → 1257）— 別構成scriptによる全数値一致

本sessionが並走着地前に独立に書き、1254 rebase対応を施したfold script（構成が着地版と異なる: zero-marginal receiptsの追跡をmarginal値の再計算に置換、出力は正規成果物pathに一切書かずsecond-independentファイル名に隔離、claim v4は内容検証方式）で全統制がPASSし、着地済みclaim v4 fold recordとfield単位で一致した:

- runpy鎖で着地済みcost-70g fold scriptから1254 headを再現（70g head JSON `73890fe3`・ranking `7397c805`・top-candidates `2da64221` ともblob一致）
- 41個のpublished cost-73h入力ファイルをgit blob shaでbyte-exact検証（sweep audit・証明書manifest・10 raw batches・determinism rerun・2 v15 crosscheck・8 per-bit verify records・証明書README・8 part files・7 scripts、claimは内容検証）
- sweep再導出（73候補を一度ずつ・4 WIN7-D10 [45,48,82,96]・69 REFUTED-D10・0 capped・76,012,796 nodes・pilot 3402×10・determinism rerun node-exact・v15 cross-engine 4/4 WIN node-matched + refuted anchors一致）・4証明書をpart bytesから直接検証（parts join→whole md5/blob・176,451 rows / 6,384,415 bytes / 28,144,763 extraction nodes・sub-roots 56/56/59/63）・root disjointness（4新root vs 528 fold済みroot、raw-hex・D4両方）
- fold結果: **head 1257/6590/520380/4860/384103**、per-receipt marginals bit45→(6,2)・bit48→(5,1)・bit82→(4,0)・bit96→(4,0)、総marginal 19・in-manifest 3・zero-mim [82,96]・zero-marginal receiptsなし、child orbit `00000000200000083800000000000200` はbit45（公開順最初）で閉鎖、set等式 `s_after == s_1254 UNION covers(4 roots)`、parents_after parent1 18行/1390（child含む1行喪失）・parent2 64行/4962（child含む3行喪失）
- **ranking CSV（blob `ee4cc2ff`）・top-candidates CSV（blob `122803ea`）ともmain着地版とbyte-identical** — 2つの独立に書かれたfold scriptが、fold後の全175 S5行の残行状態を完全に一致させた
- 着地済みclaim v4 fold record（chain_head_before/after・receipts・per_receipt_marginals・zero_mim/zero_marginal receipts・child_closed_by_bit・parents_after・parents_lost_rows・output_blob_shas）とsection 9で全field一致をassert（PASS）

運用面の修正: 初回runで本sessionのscriptが正規head JSON path（`class-frontier-cost73h-receipts-recompute-20261115.json`・blob `71f79b4b`）をローカルで上書きしてしまった → 第二検証scriptは正規成果物に一切書かない設計に修正し、正規head JSONをmainから復元（blob `71f79b4b`・10965B再検証）。72c precedent（`d4ceb255`）と同様、本sessionの第二scriptはmainには未push（着地済み公開scriptが正規であり、両者の完全一致が本logの記録）。

## 成果2：着地済み公開fold scriptの再構築mirrorでの再実行

並走着地版の公開fold script（claim v4 fold recordに明記・blob `ce4f7d9a`・39049B）を再構築mirrorでそのまま実行し、全CONTROL PASS・3成果物すべてmainとbyte-identical（head JSON `71f79b4b` 10965B・ranking `ee4cc2ff` 7580B・top-candidates `122803ea` 4749B）。head **1257/6590/520380/4860/384103** が別環境・別実行で再現された。73h段階の3成果物は、その後のcost-65l fold着地（`97d99a11`）後もmain上で無変更（正規head JSONをmainから再取得しblob一致で確認済み）。

## 実験事実（環境・運用の記録）

- sandboxリセット2回の実験事実: 未pushのローカル導出（claim v4 draft含む）は喪失したが、再導出で全数値が再現可能だったため実被害なし。ただし「リセット後のmirror再構築はcodeload tarball 1リクエスト + tar wildcards抽出が正攻法」を確立した（egressリクエスト数制限（約10/window）下ではraw CDNの一括downloadは失敗しやすい）。
- `tools.file_system.read_file`の約64KB/呼び出し制限によるbyte切り詰めで、並走sessionがK0783.md（約260KB）をclobberした事故（`568575d6`で修復）→ 大ファイルpushはchunked read連結 + push後remote照合を必須とする運用は妥当（本logのpushは1ファイル・約3KBのため対象外だが遵守）。

## 解釈境界（重要）

- solved数はmanifest被覆の簿記であり、いかなる局面のgame-theoretic値も意味しない。REFUTED-D10はLOSS証明ではない（depth-10以内の先手勝ちが無いことのみ）。WIN7証明書は個別7石rootからdepth-10以内の先手勝ちのみを証明する。
- 73h foldはchild orbit `00000000200000083800000000000200`（bit45）を閉じ、両開class-2親（parent1 `00000000000000801202000000200000`・parent2 `00000000000000003800200008000000`）の残行を減らすが、どちらのS5親も解決しない。
- **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class1・class2・class4は引き続きUNKNOWN**。

## 今後

- 次のfold baselineはhead **1261**（cost-65l fold `97d99a11`着地後。本logは73h段階の第二検証であり、65l fold（総marginal 10・in-manifest 4・child `00000000220000003800000000000200` bit21閉鎖）の数値検証は本sessionでは未実施 — 次回の検証候補）。
- 第2 coverable class-2 target S5 `00000000000000801202000000200000` は73h fold時点18行/1390 → 65l fold後17行/1325（65l log記載）。73h parent2 `00000000000000003800200008000000` は64行/4962のまま未解決。
- 並走lane（69g / 65j / 74e / 74g）の着地を重複してsweepしない。着手前に必ず最新mainを再取得すること。

詳細: [73h fold head JSON](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-cost73h-receipts-recompute-20261115.json)、[73h fold script](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_cost73h_receipts_20261115.py)、[73h ranking CSV](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-s5-ranking-after-cost73h-receipts-20261115.csv)、[73h top-candidates CSV](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-top-candidates-s6-after-cost73h-receipts-20261115.csv)、[73h fold log](./2026-11-15-n11-class2-lane-cost73h-receipts-fold.md)。
