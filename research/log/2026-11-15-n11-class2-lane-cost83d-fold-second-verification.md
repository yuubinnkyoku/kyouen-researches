# 2026-11-15：cost-83d receipts foldのtmp再構成（第二実装）+第二独立検証 — head 1314がmain単独から再現・3証明書（分割push）が第三幾何系で再検証・両再構成実装の一致確認

開始時状況: canonical head **1314/6533/516061/4803/379784**（cost-83d fold着地後・commit `1c89d19e`）。並走laneが着地したcost-83d fold（第二coverable class-2 target S5 `00000000000000801202000000200000`のcost-83 child `00000000200000003800100000000200`・3 WIN7-D10 bits [16,51,82]・head 1313→1314・第二target S5は5行/376→4行/293）について、**tmp-cost83d/はmainに存在せず**（404確認済み）、fold scriptが読む13ファイル（legal-moves.json + bits 16/51/82のcert-receipt/bigint/tsverify/consumed）が全て欠落していた。さらに本セッション中に並走が**第一再構成script**（`reconstruct_tmp_cost83d_20261115.py`・blob `591716b8`・2,520B・cost-84a in-flight claimと同commit `59025a50`で着地）を公開済みであることを確認したため、v6/v7監査と同じ「第一実装は不変・第二実装は新規file」パターンで対処した。

## 成果1：83d成果物のmirror回収と第二独立tmp再構成 — published検証器のみで全PASS

まず83d成果物（fold script・claim・11 raw batches・v15/v16・証明書6 part・head JSON・両CSV）をmain raw CDNからmirrorにfetchしgit blob shaで照合（head JSON `49cb8022` 7,407B・ranking `d8adfb7e` 7,537B・top-cand `454568f2` 6,813B・fold script `a07540cf` 22,448B・claim `e88ea50d` 6,413B・6 partは後述のpins）。次に `reconstruct_tmp_cost83d_second_independent_20261115.py`（blob `4ef976ce`・10,975B・新規file）を作成し、main成果物のみから13ファイルを再生:

- **legal-moves.json**: 完全自前生成（exact-integer Bareiss 4x4 determinant・bit16 62手 / bit51 58手 / bit82 68手 == published sub_roots_pass・第一実装の使うlegal_candidates moduleに依存しない独立実装）
- **cert-receipt 3件**: 証明書は**2分割push**（`.cert.part1of2` + `.part2of2`・連結時にCRLF→LF正規化・全partをmain git blob shaにpin: bit16 `44176845`/`adb6daf5`・bit51 `6a00807a`/`08378253`・bit82 `14559e58`/`126b0a5f`）し、連結bytesのmd5/rowsがpublished head JSONの `cost83d_addition` 記録と一致することを確認（bit16 67,775行 / bit51 58,094行 / bit82 90,769行・総計 **216,638 rows / 7,830,260 bytes / 188 sub-roots**）
- **bigint.json**: published BigInt verifierをfresh runし3/3 PASS（union 0/0・terminal_range [13,17]）
- **tsverify.json + consumed.txt**: published TS-Bareiss verifierをfresh run（--root-checkでloserMobility 62/58/68 == sub_roots_pass確認後・--subroots + --consumed-out・全sub-root range [13,17]内・consumed集合 == 証明書全行集合）
- 実行約32秒・全stepでpublished値とのcross-assert

## 成果2：両再構成実装の一致 — dual implementation agreement（tmp層）

第一実装（main着地済み・blob `591716b8`）と第二実装のtmp出力を交叉比較し**完全一致**を確認:

- **byte-identical**: legal-moves.json・3 consumed.txt・3連結証明書bytes（第一実装はunlinkなしで`bit{b}.cert`に書くがbytes同一）
- **field-identical（parse後）**: cert-receipt（bit/root_hex/rows/bytes/md5/sha256）・bigint.json・tsverify.json（subroots行）
- legal_candidates moduleとBareiss自前実装の候補列挙は順序含め完全一致

**実装上の重要発見（記録のみ・第一実装は不変）**: published TS verifier（`verify_bit7_win7_cert.ts`）は`--consumed-out`に**fs.appendFileSyncで追記する**。第一実装は対象fileをunlinkせずに再実行するため、tmp-cost83d残存状態での再実行はconsumed.txtに重複keyを追記し**file内容が実行履歴に依存する**（fold scriptのconsumed検証はset baseなのでfold自体は壊れないが、byte比較は不可能になる）。83c再構成script（`reconstruct_tmp_cost83c_20261115.py`）はunlinkしており、83d第一実装はこの保護が欠落している。第二実装はunlink後に書くため再実行安全。本検証では第一実装を**保証されたclean状態**（tmp-cost83d削除後）から実行し、両者のclean-state出力一致を確認した。

## 成果3：published fold scriptのend-to-end再現 — head 1314・3成果物byte-identical

再構成tmpに対し `recompute_frontier_cost83d_receipts_20261115.py`（blob `a07540cf`）を実行（1回約5秒・2回実行）:

- runpy鎖でcost-83c baseline 1313/6534/516144/4804/379867を83c head JSON（blob `fc7832ed`）+両CSVとともにblob一致で再現（83c鎖は83b/83a再帰を含む。**83c側のtmp再構成（consumed.txt欠落分）も本セッションで先に再生し、7ファイルがmain版とbyte-identicalであることを確認済み**）
- child genuinely remaining（両開親 5/376・72/6019がchild行を保持・demand c1=0,c2=2,c4=0・lift stones一致）・sweep再統制（83候補・3 WIN / 80 REFUTED・153,125,301 nodes・pilots 3402×11・determinism rerun 8 bits [42,43,45,46,47,48,49,50] node-exact・v15 3/3 WIN + anchors 0/1/2 refuted）・3証明書union 0/0・603-root disjointness（raw-hex・D4とも）・fold後のchild閉鎖（bit16・公開順最初）とset等式
- **3成果物すべてmainとbyte-identical**（2回の実行間でも一致）: head JSON `49cb8022` 7,407B・ranking `d8adfb7e` 7,537B・top-cand `454568f2` 6,813B

## 成果4：第二独立検証 — 8統制すべてPASS・2回実行byte-identical

`verify_cost83d_fold_second_independent_20261115.py`（blob `407ed2c4`・34,242B）を作成・実行（約4分/回・2回実行で検証JSON byte-identical）:

1. **published blob pins**: fold script `a07540cf`・claim `e88ea50d`・head JSON `49cb8022`・ranking `d8adfb7e`・top-cand `454568f2`・第一再構成 `591716b8`・**証明書6 part**
2. **dual tmp再構成**: 第一実装（clean状態から実行）と第二実装をsubprocessで実行し、上記の一致を全bitで確認
3. **fold script 2回の隔離subprocess実行**: 3成果物がpublished blobとbyte-identical（83c head 1313のrunpy再現込み）
4. **sweep再集計（独自コード）**: 83候補を一度ずつ（== claim列挙）・3 WIN7-D10 [16,51,82] / 80 REFUTED-D10 / 0 capped・総nodes 153,125,301（win sum 17,873,557）・pilots 3402×11・determinism rerun node-exact（8 bits 42..50）・v15 cross-engine 3/3 WIN（sum 29,933,192）+ 3/3 refuted anchors（bits 0/1/2・pilot 5949）
5. **3証明書の第三幾何系（rational）再検証**: 新規コードでpart連結から読み込み（bytes/md5/sha256/git blob == receipts・rows sorted-unique）し、published第三系 `verify_cost75d_win7_rational_independent.py`（exact Fraction circumcentre・iterative replay）で3/3 PASS・**216,638 rows / 7,830,260 bytes / 188 sub-roots**・union 0/0・terminal [13,17]内・consumed winner-row集合 == 再構成TS consumed files（3/3）
6. **独立D4 + 逐次marginal算術**: per-bit marginal / in-manifest / hexes がpublished addition recordsと全field一致（**marginals 5/4/4 = 総13・in-manifest 1・zero-mim [51,82]**）・child orbit closureはbit16の1回のみ・set等式 `s_1314 == s_1313 ∪ covers(3 roots)` 成立・**第二target S5 5行/376 → 4行/293**（parent1喪失はchild行のみ）・第2開親（class-2 S5 `00000000000000043800000008000000`）72行/6019 → 71行/5936（喪失はchild行のみ）
7. **606-root在庫の軌道解析**: 603既存 + 3新規 = 606 roots・**595 distinct orbits**（592+3新規orbit）・11 twin pairs（新twinなし）・3新rootは603在庫とraw-hex・D4ともdisjoint
8. **completed claim fold record**: head 1313→1314・publication order [16,51,82]・totals 13/1・zero-mim [51,82]・child closed by bit16・parents_after 4行/293・71行/5936・lost rows（両parentともchildのみ）・output blob shas・head_json_bytes 7,407と全field一致

機械可読検証記録: [class2-lane-cost83d-fold-second-verification-20261115.json](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost83d-fold-second-verification-20261115.json)（5,512 bytes・md5 `cd8314f6`・git blob `fe418cf2`・2回実行byte-identical）

これによりcost-75d/80d/82c/83a/83b/83c/83dの全7 fold endpointが「lane実装 + 本レーン第二独立実装」の二重検証体制となり、83a〜83dは第三幾何系（rational verifier）による証明書再検証も付く。83dはtmp再構成自体も二重実装で確認済み。

## main反映

- 第二再構成script（新規file）+ 第二検証script + 検証JSON + 本logをpush。第一再構成script（`591716b8`）はmain上不変。tmp-cost83d小ファイルはpushしない（83d laneの先例に従い、両再構成scriptで再生可能・consumed.txtはsize上限で元々push不可のためfoldのmain単独実行には再構成が必須）。push直前の最新main再取得で競合・83d検証の同時着地なしを確認
- 全ファイルraw CDN照合byte-identical

## 解釈境界（重要）

- solved 1314はmanifest被覆の簿記であり、いかなる局面のgame-theoretic値も意味しない。REFUTED-D10はLOSS証明ではない。WIN7証明書は個々の7石rootからdepth-10以内の先手勝ちのみを証明する。
- 83d foldはchild orbit `00000000200000003800100000000200` を閉じ、第二target S5の残行を5→4に減らすが、S5自体は解決しない。
- **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class1・class2・class4は引き続きUNKNOWN**。

## 今後

- 次のfold baselineはhead **1314**（`class-frontier-cost83d-receipts-recompute-20261115.json`・blob `49cb8022`）。第二target S5は4行/293。
- **cost-84a IN FLIGHT**（並走・commit `59025a50`・第二coverable class-2 target S5 cost-84 child `00000000000040809002000000000800`・demand c1=0,c2=1,c4=0・84候補）に着手禁止。着地後は本logの再構成+第二検証パターンを適用可能。
- 機械拡張候補: published fold-chain監査v8（83d endpoint追加・両実装+agreement v5）。着手前に必ず最新mainを再取得し、83d以降のfold・cost-84aの着地状況を確認すること。

詳細: [83d fold head JSON](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-cost83d-receipts-recompute-20261115.json)、[83d fold script](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_cost83d_receipts_20261115.py)、[83d completed claim](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost83d-inflight-20261115.json)、[第一再構成script（main着地）](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/reconstruct_tmp_cost83d_20261115.py)、[第二再構成script](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/reconstruct_tmp_cost83d_second_independent_20261115.py)、[83c検証log（前回）](./2026-11-15-n11-class2-lane-cost83c-fold-second-verification.md)。
