# 2026-11-15：cost-83a receipts foldのtmp再構成+第二独立検証 — head 1309がmain単独から再現・4証明書が第三幾何系で再検証

開始時状況: canonical head **1309/6538/516477/4808/380200**（cost-83a receipts fold・[fold log](./2026-11-15-n11-class2-lane-cost83a-sweep-certificates-and-fold.md)）。並走laneが着地したcost-83a fold（第二coverable class-2 target S5 `00000000000000801202000000200000` のcost-83 child `00000000000000801202000000200008`・4 WIN7-D10 bits [12,58,72,95]・head 1306→1309）について、fold script・claim・11 raw batches・4証明書はmain済みだったが、**tmp-cost83a/は部分的**（bit12/58/72の .rows + .rows.summary.json + legal-moves.jsonのみ・commit 477a5199）で、fold scriptが読む `bit{b}.cert-receipt.json` / `bit{b}.bigint.json` / `bit{b}.tsverify.json` / `bit{b}.consumed.txt` の16ファイルが欠落しており、main単独ではend-to-end再実行不可能だった。これはcost-69i（[reconstruct log](./2026-11-15-n11-merged-fold-1277-and-cost69i-second-verification-and-repair.md)）と同じ形状のギャップである。

## 成果1：tmp-cost83a/16ファイルの再構成 — published検証器のみで全PASS

`reconstruct_tmp_cost83a_20261115.py`（blob `65d58526`）を作成し、main成果物のみから16ファイルを再生:

- **cert-receipt 4件**: 証明書bytesから直接算出（bit12/58/72は単一ファイル・bit95は行境界2分割をfold scriptと同じ規約でper-part CRLF→LF結合）・md5/rowsはpublished head JSONの `cost83a_addition` 記録と一致（rows 40,417/41,891/36,293/58,190・総計176,791 rows / 6,386,515 bytes / 243 sub-roots）
- **legal-moves.json**: lane公開ファイルをそのまま保持し、Bareiss 4x4 exact-integerで再計算した合法loser初手が完全一致（mobility 60/58/57/68 == sub_roots_pass）
- **公開済み部分 .rows のcross-check**: bit12/58/72の .rows行集合 == 証明書行集合・summary nRows一致（bit95.rowsはmain未公開だがfold scriptは読まない）
- **bigint.json**: published BigInt verifier（`verify_win7_certificate_bigint_independent.mjs`）をfresh runし4/4 PASS（union 0/0・terminal_range [13,17]）
- **tsverify.json + consumed.txt**: published TS-Bareiss verifier（`verify_bit7_win7_cert.ts`）をfresh run（--root-checkのloserMobility == sub_roots_pass・全sub-root range [13,17]内・consumed 36,293+41,891+40,417+58,190 keysの集合 == 証明書全行集合）
- 実行約1分・全stepでcross-assert

## 成果2：published fold scriptのend-to-end再現 — head 1309・3成果物byte-identical

再構成tmpに対し `recompute_frontier_cost83a_receipts_20261115.py`（blob `70fc5d12`）を隔離mirrorで2回実行（各回約1.5分・2回とも全統制PASS）:

- runpy鎖でcost-82c baseline 1306/6541/516711/4811/380434を82c head JSON（blob `4ee6aaab`）+両CSVとともにblob一致で再現
- child genuinely remaining（両開親 8/625・70/5743がchild行を保持・demand c1=0,c2=2,c4=0）・sweep再統制（83候補・4 WIN/79 REFUTED/0 capped・152,978,839 nodes・pilots 3402×11・determinism rerun・v15 anchors）・4証明書のbytes/md5/rows/sorted-unique/sub-roots/union 0/0・592-root disjointness・fold後のchild閉鎖とset等式
- **3成果物すべてmainとbyte-identical**: head JSON `74e35f22` 8,068B・ranking CSV `70eab6c4` 7,537B・top-candidates CSV `fad56f79` 7,071B（2回の実行間でも一致）

## 成果3：第二独立検証 — 8統制すべてPASS・2回実行byte-identical

`verify_cost83a_fold_second_independent_20261115.py`（blob `a4abde75`）を作成・実行（約2.5分/回・2回実行で検証JSON byte-identical）:

1. **published blob pins**: fold script `70fc5d12`・claim `02e7aa09`・head JSON `74e35f22`・ranking `70eab6c4`・top-cand `fad56f79`
2. **tmp再構成をsubprocessで実行**（本検証の前提を自前で再現）
3. **fold script 2回の隔離subprocess実行**: 3成果物がpublished blobとbyte-identical
4. **sweep再集計（独自コード）**: 11 raw batchesから83候補を一度ずつ（== claim列挙）・4 WIN7-D10 [12,58,72,95] / 79 REFUTED-D10 / 0 capped・総nodes 152,978,839（win sum 10,308,522）・pilots 3402×11・determinism rerun node-exact・v15 cross-engine 4/4 WIN + 3/3 refuted anchors（bits 0/1/2・pilot 5949）
5. **4証明書の第三幾何系（rational）再検証**: 新規コードでpart-join（bytes/md5/sha256/git blob == receipts・rows sorted-unique）し、published第三系 `verify_cost75d_win7_rational_independent.py`（exact Fraction circumcentre・iterative replay）で4/4 PASS・**176,791 rows / 6,386,515 bytes / 243 sub-roots**・union 0/0・terminal [13,17]内・consumed winner-row集合 == 再構成TS consumed files（4/4）
6. **独立D4 + 逐次marginal算術**: 8 affine行列の独立実装でper-bit marginal / in-manifest / hexes がpublished addition recordsと**全field一致**（総marginal 19・in-manifest 3・zero-mim [58,95]）・child orbit closureはbit12の1回のみ・set等式 `s_1309 == s_1306 ∪ covers(4 roots)` 成立・**第二target S5 8行/625 → 7行/542**（parent1喪失はchild行のみ）・第2開親 70行/5743 → 67行/5509（child + in-manifest 2行喪失）
7. **596-root在庫の軌道解析**: 592既存 + 4新規 = 596 roots・**585 distinct orbits**（581+4）・11 twin pairs（新twinなし）・4新rootは592在庫とraw-hex・D4ともdisjoint
8. **completed claim fold record**: head 1306→1309・publication order [12,58,72,95]・totals 19/3・zero-mim・child closed by bit12・parents_after・output blob shas・head_json_bytes 8,068と全field一致

機械可読検証記録: [class2-lane-cost83a-fold-second-verification-20261115.json](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost83a-fold-second-verification-20261115.json)（4,518 bytes・md5 `88510d8c…`・git blob `857d9040`・2回実行byte-identical）

## main反映

- scripts 2件（再構成+第二検証）→ commit `69df8402`
- tmp小ファイル12件（receipts/bigint/tsverify×4bit）→ commit `8cf9f5d8`
- **bit72.consumed.txt（1,757,415B）をformat witnessとして公開** → commit `3370ab2f`（raw CDNでbyte-identical確認）。bit12/58/95のconsumed（1.77/1.96/2.48MB）は再構成scriptで再生（69iと同じ運用）。なお1.76MB級の単一ファイルpushは今回toolchainの16MiB program memory制限に引っかかったが、**push自体は着地済み**であることを事後CDN照合で確認した（失敗と記録すべきは戻り値の確認のみでなく着地照合まで）
- tmp README + 検証JSON + 本log → 本commit
- 全15ファイルraw CDN照合byte-identical。push直前の最新main再取得で、並走のfiber lane（`1fa66b18`/`e0d4df7a`）とK0827 docs sync（`6404863a`）の着地を確認・競合なし

## 解釈境界（重要）

- solved 1309はmanifest被覆の簿記であり、いかなる局面のgame-theoretic値も意味しない。REFUTED-D10はLOSS証明ではない。WIN7証明書は個々の7石rootからdepth-10以内の先手勝ちのみを証明する。
- 83a foldはchild orbit `00000000000000801202000000200008` を閉じ、第二target S5の残行を8→7に減らすが、S5自体は解決しない。
- **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class1・class2・class4は引き続きUNKNOWN**。

## 今後

- 次のfold baselineはhead **1309**（`class-frontier-cost83a-receipts-recompute-20261115.json`・blob `74e35f22`）。第二target S5は7行/542（残行cost: 65, 70, 74, 83, 83, 83, 84）。
- **cost-83b IN FLIGHT**（並走・commit `fe7c785c`・child `00000000000000801202000000200010`）に着手禁止。着地後は本logの再構成+第二検証パターン（`reconstruct_tmp_cost83b_*` + `verify_cost83b_fold_second_independent_*`）を適用可能。
- audit v6拡張（両実装・83a endpoint: pins +1〔blob `74e35f22`〕・own_claim 592+4・own_baseline 83a→82c・CANONICAL_LINE +cost83a_addition〔mim 76/distinct 76/multi 0・1309-1233=76〕・ENDPOINT_CHECKS +83a entry〔nrec 4・closebit 12・order [12,58,72,95]・8,068B〕）+ agreement v3が次回候補。着手前に必ず最新mainを再取得し、83b着地状況を確認すること。

詳細: [83a fold head JSON](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-cost83a-receipts-recompute-20261115.json)、[83a fold script](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_cost83a_receipts_20261115.py)、[83a completed claim](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost83a-inflight-20261115.json)、[tmp README](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/tmp-cost83a/README.md)、[83a fold log](./2026-11-15-n11-class2-lane-cost83a-sweep-certificates-and-fold.md)、[82c fold第二独立検証（前回）](./2026-11-15-n11-class2-lane-cost82c-fold-second-verification.md)、[69i tmp再構成の先例](./2026-11-15-n11-merged-fold-1277-and-cost69i-second-verification-and-repair.md)。
