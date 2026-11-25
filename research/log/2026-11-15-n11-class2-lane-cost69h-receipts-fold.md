# 2026-11-15：cost-69h receipts fold 完成（chain head 1219 → 1221）

開始時main: canonical chain head `1219/6628/523173/4898/386896`（cost-67c fold済み・`class-frontier-cost67c-receipts-recompute-20261115.json`・remote blob `6d187f48420a9b66d527c3c0fb2764ad5f63235a`）。AGENTS.md、research/knowledge/README.md、K0783、cost-69h関連のclaim v2（sweep+証明書完成・fold pending）・sweep audit・証明書manifest・第三独立監査、並走レーン（65l/78a/69g/65j/74e）の着地状況を確認した。新たなfold着地はなし（rebase不要）。

## 成果1：cost-69h 2-receipt fold 完成

`recompute_frontier_cost69h_receipts_20261115.py`（42,226 bytes）で、cost-69h sweep の証明書付きWIN7-D10 receipts 2件（bits 58/96）を1219 headにfoldした。親はrunpy chainでcost-67c head 1219をbyte-identical再現（head JSON・両CSVのgit blob sha照合、chain内部で1216（cost-63g）・1199（cost-63f）headも再現）。

**新canonical chain head: `1221/6626/523035/4896/386758`**（`class-frontier-cost69h-receipts-recompute-20261115.json`、remote blob `1238cf8853595fbfabcc90856ec13502e7bbf6f6`・9,151 bytes）。remaining S5 orbits 175不変。

- total marginal 10 / marginal_in_manifest +2。zero-mim receipts なし。
- child `0000000000000080120a000000200000`（cost 69・demand c1=0,c2=2,c4=0・両開class-2親の行）は **bit-58 receipt（公開順最初）で閉鎖**。root 2件は114既fold receipt roots（98 pre-63g + 14 cost-63g + 2 cost-67c）とraw・D4正準形の両方でdisjoint、2 distinct D4 orbits。
- bit-58 receipt: covers 7 / marginal 5 / in-manifest 1（childのみ）。bit-96 receipt: covers 7 / marginal 5 / in-manifest 1。
- **両開親の行喪失をbit-exact検証**: 第二coverable class-2 target S5 `00000000000000801202000000200000` 32行/2403 → **31行/2334**（child行のみ喪失）。開class-2 S5 `0000000000000080120a000000000000` 49行/3593 → **47行/3455**（child行＋`00000000000000a09002000001000000` — bit-96証明書の交差被覆で2行目も閉鎖）。
- 統制: 14入力ファイル＋claimのgit blob sha byte-exact照合、sweep auditをraw 9 batchから再導出（69候補==claim列挙、2 WIN7-D10 / 67 REFUTED / 0 capped、83,542,525 nodes・win sum 3,786,857、pilots 3402×9、batch-5 determinism rerun node-exact）、v15 cross-engine anchors（2 WIN loss=true node一致 sum 7,553,969、3 REFUTED anchors bits 64/117/22、pilot 5949）、証明書2件のbytes再検証（4 parts→2 wholes parts-join-whole、md5×sha256×git blob、rows 90,646 / bytes 3,272,824 / extraction 12,100,785 / sub-roots 113、sub-roots==loser mobility==60/53、terminal 13..17）、第三独立監査JSON全項目一致（13 covered orbits・child共有・worklist parents・proven_win [58,96]）、childが1219 baselineでgenuinely remaining（両開親がchild行を保持・他の開親は保持しない・in-manifest未解決・demand c2=2再導出・lift stones 51/21）、set-equality管理 `s_after == s_1219 ∪ covers(2 roots)` 成立。2回実行byte-identical。
- 出力: ranking CSV blob `9898802912aeb040394bd0a8a53dcaa101e0bc76`（7,580 bytes）、top-candidates CSV blob `0bcdd84e0e83157876676a5fbf85ec79493307d0`（5,953 bytes）。

## 成果2：claim retire v3 と script の恒久再実行化

claim `class2-lane-cost69h-inflight-20261115.json` をv3（status `completed`・fold record: chain_head_after `1221/6626/523035/4896/386758`、total_marginal 10、total_marginal_in_manifest 2、child_orbit_closed_by_bit 58、parents_after 31行/2334・47行/3455、receipts_folded [58,96]、output blob shas、head_json_bytes 9151）にretireした。remote blob `7627d490683b01ad88f2f27c99e99ca75b6a0be2`（9,328 bytes）。

fold scriptはcost-67cと同じ恒久再実行化運用に従い、初回push（remote blob `45f4134137435af7c67871d09918c0f1d4d89654`）後にCLAIM_BLOBS_RETIREDへretire後の実blobを追記して再push（remote blob `623f97515055d792c58fca3bb7c0397fe38c7391`）。差し替え後に**retired claim v3のfold record全項目と再計算の一致、head JSON byte-identicalを含む再実行**を確認（`CONTROL retired claim v3 fold record matches this recomputation: head 1221/6626/523035/4896/386758`）。以後このscriptはclaim修正なしに恒久的に再実行可能。なおretire直後のscript再pushは並走のcost-70d claim着地（`bb44940e`）とのbranch-head raceで一度409となったが、同ファイル無変更を確認の上で再pushし解消した（並走はscriptに触れていない）。

## fold後frontierと次への指示

- 第三target class-2 S5 `00000000000000809102000000000000` は3行/221のまま（69/74/78行はすべて並走レーン担当: 69g/74e/78a in flight）。こちらからは触れない。
- 第二coverable class-2 target（31行/2334）の次の最安未sweep行は、公開済みsterile（65k/73f/74f等）・in-flight（65l等）との照合の上で選定すること。fold直後に並走がcost-70d claim（第二coverable class-2 S5のcost-70子・混合c1=1）を着地済みなので、**次回はclaim列挙で重複排除を必ず最初に**。head-1221のtop-candidates CSV参照。
- **65l/78a/69g/65j/74e/70d の各foldは新head `1221/6626/523035/4896/386758` にrebase必須**。以後のrecompute/claimはこのheadをassertして拡張する。
- audit-blocked class-2 S5 `00000000000000809082000000000000` 10行/698、best class-4 blocker S5 `00000000020000003800000080000000` 18行/1460不変（73f/74fで連続STERILE済み）。

## 追記：cost-78a fold着地に伴うrebase（head fork解消・canonical head 1227）

初回fold着地（commit `3d2faf3b`）の直前、03:07:50 UTCに並走cost-78a foldが同一baseline head 1219へ着地していた（commit `1691d9bbc1`・5 WIN7-D10 receipts bits 36/20/29/8/109・total marginal 26 / in-manifest 6・head JSON `class-frontier-cost78a-receipts-recompute-20261115.json` remote blob `3938bb16…` 10,629 bytes・completed claim remote blob `468b6d49…`）。そのため本レーンのfold（1219→1221）と78a fold（1219→1225）が同一baselineから並行着地し、canonical chainが分岐した（cost-70dのK0783追記もこのhead forkを指摘済み）。本レーンは78a laneがcost-67c時と同じrebase手順に従ってこのfoldを78a head 1225へrebaseし、分岐を解消した。

- **rebase後canonical chain head: `1227/6620/522561/4890/386284`**（= 1225+2・head JSON schema v2・remote blob `d25eb3a00f73cf9ca34fc2816d28045c1e23f3ae` 11,295 bytes）。set等式 `s_1227 == s_1219 ∪ covers(5×78a roots) ∪ covers(2×69h roots)` をassert。
- rebase版fold script（58,843 bytes・remote blob `a1eccdfc7d28fc20074bc822c4e7f6bdaab7294a`）は、78a公開4ファイル（head JSON・ranking CSV・top-candidates CSV・completed claim）のgit blob sha byte-exact照合の後、78a foldを純幾何（covers()/canon()のみ・repo engine不使用）で再導出する（per-receipt marginal counts・marginal hex lists 全一致、summary・parents・両CSVのbyte-identical再生成を確認）。続いて69h入力の全面検証（sweep audit再導出・証明書2件のparts-join-whole bytes・第三独立監査）、119 folded roots（98 pre-63g + 14 cost-63g + 2 cost-67c + 5 cost-78a）と69h 2 rootsのraw・D4正準形双方でのdisjointness、1225上でのfoldを実行する。78a証明書bytes（約12MB）は実行環境のcgroup 1GB制限のため再検証しておらず、78a lane自身のscript検証済みである旨をmethod文字列に明記した。
- marginal 10（78a分5 + 69h分5）/ in-manifest 2、child `0000000000000080120a000000200000` のbit-58閉鎖、marginal hex listsはすべてpre-rebaseの1219→1221 foldと同一（78a coversと69h coversの被覆重なり0）。parents_afterも同一で、第二coverable class-2 S5 `00000000000000801202000000200000` 31行/2334、開class-2 S5 `0000000000000080120a000000000000` 47行/3455（78a foldはこの2親の行に影響しない）。
- claimはv4としてretire（remote blob `31e3314118557cf5e14062e2931ecfd603445f3f` 10,399 bytes・chain_head_before `1225/6622/522699/4892/386422`・pre_rebase_chain_head_after `1221/6626/523035/4896/386758`・chain_head_after `1227/6620/522561/4890/386284`・total_marginal 10・total_marginal_in_manifest 2・child_orbit_closed_by_bit 58・parents_after 31行/2334・47行/3455・receipts_folded [58,96]・output blob shas・head_json_bytes 11295）。v3（1219-baseline fold record `1221/6626/523035/4896/386758`・output blobsは定数として記録保存）は歴史管理controlとしてscriptに残し、CLAIM_BLOBS_RETIREDにv3・v4両blobを登録したdual controlにより、scriptはclaim修正なしに恒久再実行可能。retire後の再実行で `CONTROL retired claim v4 fold record matches this rebased recomputation: head 1227/6620/522561/4890/386284, head JSON blob re-asserted byte-identical` がPASS、3出力の2回実行byte-identical（md5照合・git blob sha照合）も確認した。出力: ranking CSV remote blob `4eeca6155838169050804eb31a34db4a0681ec05` 7,580 bytes・top-candidates CSV remote blob `0f9905fcb9190cbbda3b6581466b50373308fe60` 5,867 bytes。
- これによりcost-70dが指摘した「78a（1225）と69h（1221）のマージrecompute必須」は完了した。以後のrecompute/claim（65l/69g/65j/74e等の未着地foldを含む）は新head **`1227/6620/522561/4890/386284`** をassertして拡張すること。fold後frontier: best coverable class-2 = 第三target S5 `00000000000000809102000000000000` 2行/143（残り69=69g担当・74=74e担当）・第二coverable 31行/2334・audit-blocked class-2 S5 `00000000000000809082000000000000` 10行/698・best class-4 blocker S5 `00000000020000003800000080000000` 18行/1460（73f/74f/74c/75/79/79b/70dすべてSTERILE）。なお並走five-row-q7-m29 batch-4も着地したが本chainとは無関係。

勝敗は変わらない。本rebaseはchain bookkeepingの統合であり、いかなる局面のgame-theoretic valueも確定しない。

## 勝敗status

標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class 2、class 4 はすべて **UNKNOWN**。本foldはmanifest被覆のbookkeepingであり、いかなる局面のgame-theoretic valueも確定しない。REFUTED-D10 sweepはWIN7-D10不在のみを証明し、WIN7証明書は個々の7石rootからdepth 10以内の勝ちのみを証明する。cost-69h child軌道の閉鎖は両開class-2親の残行を減らすが、どちらのS5親も解決していない。
