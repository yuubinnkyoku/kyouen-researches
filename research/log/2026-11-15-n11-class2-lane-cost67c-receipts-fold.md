# 2026-11-15：cost-67c receipts fold 完成（chain head 1216 → 1219）

開始時main: canonical chain head `1216/6631/523382/4901/387105`（cost-63g fold済み・`class-frontier-cost63g-receipts-recompute-20261115.json`）。AGENTS.md、research/knowledge/README.md、K0783、cost-67c関連のclaim（v3 `fold_in_flight`）・sweep audit・証明書manifest・第三独立監査、並走レーン（65l/78a/69g/65j/74e）の着地状況を確認した。65l foldを含め新たなfold着地はなし（rebase不要）。

## 成果1：cost-67c 2-receipt fold 完成

`recompute_frontier_cost67c_receipts_20261115.py`（42,661 bytes）で、cost-67c sweep の証明書付きWIN7-D10 receipts 2件（bits 64/96）を1216 headにfoldした。親はrunpyでcost-63g chain head 1216をbyte-identical再現（head JSON・両CSVのgit blob sha照合、chain内部で1199 headも再現）。

**新canonical chain head: `1219/6628/523173/4898/386896`**（`class-frontier-cost67c-receipts-recompute-20261115.json`、remote blob `6d187f48420a9b66d527c3c0fb2764ad5f63235a`・9,323 bytes）。remaining S5 orbits 175不変。

- total marginal 9 / marginal_in_manifest +3。zero-mim receipts なし。
- child `00000000000000801202000000202000`（混合demand c1=0,c2=1,c4=1・両開親の行）は **bit-64 receipt（公開順最初）で閉鎖**。root 2件は112既fold receipt roots（98 pre-63g + 14 cost-63g）とraw・D4正準形の両方でdisjoint、2 distinct D4 orbits。
- bit-64 receipt: covers 7 / marginal 4 / in-manifest 1（childのみ）。bit-96 receipt: covers 7 / marginal 5 / in-manifest 2。
- **両開親の行喪失をbit-exact検証**: 第二coverable class-2 target S5 `00000000000000801202000000200000` 33行/2470 → **32行/2403**（child行のみ喪失）。開class-4 S5 `00000000000000801002000000080800` 76行/5703 → **74行/5560**（child行＋`00000000020000003800000040000002`）。
- bit-96 receiptの交差被覆はさらに2開親の行を削減: class-2 S5 `00000000000000801202000040000000` 45/3119→44、class-4 S5 `00000000020000003800000040000000` 85/6497→84（`00000000040000003800000088000000`閉鎖）。
- 統制: 14入力ファイル＋claimのgit blob sha byte-exact照合、sweep auditをraw 9 batchから再導出（67候補==claim列挙、2 WIN7-D10 / 65 REFUTED / 0 capped、41,942,979 nodes、batch-5 determinism rerun node-exact）、v15 cross-engine anchors（2 WIN node一致 sum 7,504,416、3 REFUTED anchors、pilots 5949×5）、証明書2件のbytes再検証（4 parts + 2 wholes、parts-join-whole md5一致、md5×sha256×git blob、rows 70,480 / bytes 2,546,005 / extraction 11,554,974 / sub-roots 106、terminal 13..17、sub-roots==loser mobility==53）、第三独立監査JSON全項目一致（13 covered orbits・worklist parents・proven_win [64,96]）、set-equality管理 `s_after == s_1216 ∪ covers(2 roots)` 成立。2回実行byte-identical。
- 出力: ranking CSV blob `fa04928a15c62d56fcceae3ce1ef5d670d5365a1`（7,580 bytes）、top-candidates CSV blob `52872558ff4e1d5a0d972a840fedc776fcba460c`（6,039 bytes）。

## 成果2：claim retire v4 と script の恒久再実行化

claim `class2-lane-cost67c-inflight-20261115.json` をv4（status `completed`・fold record: chain_head_after `1219/6628/523173/4898/386896`、total_marginal 9、total_marginal_in_manifest 3、child_orbit_closed_by_bit 64、parents_after 32行/2403・74行/5560、receipts_folded [64,96]、output blob shas、head_json_bytes 9323）にretireした。remote blob `728f929d999fba6d0bed8e037b573d528f99616e`（10,852 bytes）。

fold scriptはclaimのretire後blobをassertする運用（cost-72b再実行不能事故の教訓・cost-76a基準）に従い、初回push（`17f36faa…`）後にCLAIM_BLOBSをretire後の実blobで差し替えて再push（remote blob `01d3ceabd9487e1e3a8da440c08dafea018b55df`）。差し替え後に**retired claim v4のfold record全項目と再計算の一致、head JSON byte-identicalを含む再実行**を確認（`CONTROL retired claim v4 fold record matches this recomputation`）。以後このscriptはclaim修正なしに恒久的に再実行可能。

## fold後frontierと次への指示

- 第三target class-2 S5 `00000000000000809102000000000000` は3行/221のまま（69/74/78行はすべて並走レーン担当: 69g/74e/78a in flight）。こちらからは触れない。
- 第二coverable class-2 target（32行/2403）の次の最安未sweep行は、公開済みsterile（65k等）・in-flight（65l）との照合の上で選定すること。候補はcost-65（`00000000020000801202000000200000`・c2=2）から順に、head-1219のtop-candidates CSV参照。
- **65l/78a/69g/65j/74e の各foldは新head `1219/6628/523173/4898/386896` にrebase必須**。以後のrecompute/claimはこのheadをassertして拡張する。
- best class-4 blocker S5 `00000000020000003800000080000000` は18行/1460不変（73f/74fで連続STERILE済み）。

## 勝敗status

標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class 2、class 4 はすべて **UNKNOWN**。本foldはmanifest被覆のbookkeepingであり、いかなる局面のgame-theoretic valueも確定しない。REFUTED-D10 sweepはWIN7-D10不在のみを証明し、WIN7証明書は個々の7石rootからdepth 10以内の勝ちのみを証明する。child軌道の閉鎖は両開親の残行を減らすが、どちらのS5親も解決していない。
