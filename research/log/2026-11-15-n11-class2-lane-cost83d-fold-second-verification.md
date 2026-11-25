# 2026-11-15：cost-83d receipts foldの第二独立検証 — head 1314がmain単独から再現・3証明書（6 partファイル）が第三幾何系で再検証

開始時状況: canonical head **1314/6533/516061/4803/379784**（cost-83d fold着地後・commit `1c89d19e`・14:38:26Z）。並走laneが着地したcost-83d fold（第二coverable class-2 target S5 `00000000000000801202000000200000`系child `00000000200000003800100000000200`・3 WIN7-D10 bits [16,51,82]・head 1313→1314・第二target S5 5行/376→4行/293）について、**tmp-cost83d/はmainに一切存在せず**（83a/83cと同じ形状のギャップ）。ただし今回は並走lane自身がrepair script `reconstruct_tmp_cost83d_20261115.py`（commit `59025a50`）を公開済みであり、本セッションはそれをそのまま実行して第二独立検証を行った。なお証明書は**6つのpartファイル（各bit 2分割）として公開**されており（83a/83b/83cの単一ファイル形式と異なる新形式）、part-joinからreceipts算出までを検証側で新規実装した。

また本セッションの副次的発見: 83d fold scriptのrunpy鎖はtmp-cost83cの`bit16/bit82.consumed.txt`を必要とするが、これらは83cのsize上限でmain未pushであるため、**83d検証の前にpublished 83c再構成script `reconstruct_tmp_cost83c_20261115.py`の実行が前提**となる（83cのconsumedは同scriptで再生可能なためmain単独再現性は保たれる）。この依存関係をlogとして明記する。

## 成果1：tmp-cost83d/13ファイルの再生 — published repair scriptで全PASS

published `reconstruct_tmp_cost83d_20261115.py`（blob `591716b8`・2,520B）をfresh mirrorで実行:

- **legal-moves.json**: published `legal_candidates` enumerationから生成（bit16 62手 / bit51 58手 / bit82 68手 == published sub_roots_pass 62/58/68）
- **cert-receipt 3件**: 6 partファイルのplain連結bytesから算出・md5/rowsはpublished head JSONの `cost83d_addition` 記録と一致（bit16 67,775行 / bit51 58,094行 / bit82 90,769行）
- **bigint.json**: published BigInt verifier fresh run 3/3 PASS（union 0/0・terminal_range [13,17]）
- **tsverify.json + consumed.txt**: published TS-Bareiss verifier fresh run（3 bitとも全sub-root range [13,17]内・consumed集合 == 証明書全行集合）
- 実行約40秒・総計 **216,638 rows / 7,830,260 bytes / 188 sub-roots** == published head JSON totals

## 成果2：published fold scriptのend-to-end再現 — head 1314・3成果物byte-identical

再構成tmp（+83c consumed再生）に対し `recompute_frontier_cost83d_receipts_20261115.py`（blob `a07540cf`）を隔離mirrorで2回実行（2回とも全統制PASS・約2分/回）:

- runpy鎖でcost-83c baseline 1313/6534/516144/4804/379867を83c head JSON（blob `fc7832ed`）+両CSVとともにblob一致で再現
- child genuinely remaining（両開親 5/376・72/6019がchild行を保持・demand c1=0,c2=2,c4=0）・sweep再統制・3証明書union 0/0・603-root disjointness・fold後のchild閉鎖とset等式
- **3成果物すべてmainとbyte-identical**: head JSON `49cb8022` 7,407B・ranking CSV `d8adfb7e` 7,537B・top-candidates CSV `454568f2` 6,813B（2回の実行間でも一致）

## 成果3：第二独立検証 — 8統制すべてPASS・2回実行byte-identical

`verify_cost83d_fold_second_independent_20261115.py`（31,446B・83c検証scriptの機械変換+83d固有統制追加）を作成・実行（約5分/回・2回実行で検証JSON byte-identical）:

1. **published blob pins**: fold script `a07540cf`・reconstruction script `591716b8`・claim `e88ea50d`・head JSON `49cb8022`・ranking `d8adfb7e`・top-cand `454568f2`、**加えて6証明書partファイルのblob pins**（`44176845d5`/`adb6daf529`/`6a00807a4b`/`0837825303`/`14559e5787`/`126b0a5f56`）
2. **tmp再生をsubprocessで実行**（published repair scriptを検証内で再実行）
3. **fold script 2回の隔離subprocess実行**: 3成果物がpublished blobとbyte-identical
4. **sweep再集計（独自コード）**: 11 raw batchesから83候補を一度ずつ（== claim列挙・順序も一致）・3 WIN7-D10 [16,51,82] / 80 REFUTED-D10 / 0 capped・総nodes 153,125,301（win sum 17,873,557）・pilots 3402×11・determinism rerun node-exact（bits 42..50の8件）・v15 cross-engine 3/3 WIN + 3/3 refuted anchors（bits 0/1/2・pilot 5949・anchor nodes 9,879,365 / 6,821,378 / 13,232,449 == published v15_anchor_nodes）
5. **3証明書の第三幾何系（rational）再検証**: 6 partファイルを新規コードでjoin（bytes/md5/sha256 == receipts・part blob pins照合・rows sorted-unique）し、published第三系 `verify_cost75d_win7_rational_independent.py`（exact Fraction circumcentre・iterative replay）で3/3 PASS・**216,638 rows / 7,830,260 bytes / 188 sub-roots**・union 0/0・terminal [13,17]内・consumed winner-row集合 == 再構成TS consumed files（3/3）
6. **独立D4 + 逐次marginal算術**: per-bit marginal / in-manifest / hexes がpublished addition recordsと**全field一致**（bit16 5/1・bit51 4/0・bit82 4/0・総marginal 13・in-manifest 1・zero-mim [51,82]）。**bit16のin-manifest marginalはchild自身（`00000000200000003800100000000200`）のみ**であり、child orbit closureはbit16（公開順最初）の1回のみ。set等式 `s_1314 == s_1313 ∪ covers(3 roots)` 成立・**第二target S5 5行/376 → 4行/293**（parent1喪失はchild行のみ）・第2開親（83d固有のclass-2 S5 `00000000000000043800000008000000`）72行/6019 → 71行/5936（喪失はchild行のみ）
7. **606-root在庫の軌道解析**: 603既存 + 3新規 = 606 roots・**595 distinct orbits**（592+3）・11 twin pairs（新twinなし）・3新rootは603在庫とraw-hex・D4ともdisjoint
8. **completed claim fold record**: head 1313→1314・publication order [16,51,82]・totals 13/1・zero-mim [51,82]・child closed by bit16・parents_after 4行/293・71行/5936・lost rows（両parentともchildのみ）・output blob shas・**head JSON totals block（v15_crosscheck_nodes_sum 29,933,192・v16_sweep_win_nodes_sum 17,873,557等）も全field一致**

機械可読検証記録: [class2-lane-cost83d-fold-second-verification-20261115.json](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost83d-fold-second-verification-20261115.json)（5,046 bytes・md5 `43975fcf`・2回実行byte-identical）

これによりcost-75d/80d/82c/83a/83b/83c/**83d**の全7 fold endpointが「並走lane実装 + 本レーン第二独立実装」の二重検証体制となり、83a以降は第三幾何系（rational verifier）による証明書再検証も付く。

## main反映

- 第二検証script + 検証JSON + 本log + tmp-cost83d小ファイル10件（legal-moves・receipts/bigint/tsverify×3bit）を1コミットでpush（consumed.txt 3件はsize上限から除外・published repair scriptで再生可能。join済み証明書全体ファイルも6 partから再生可能なため除外）。push直前の最新main再取得で兄弟の83d検証着地なしを確認
- 全ファイルraw CDN照合byte-identical

## 解釈境界（重要）

- solved 1314はmanifest被覆の簿記であり、いかなる局面のgame-theoretic値も意味しない。REFUTED-D10はLOSS証明ではない。WIN7証明書は個々の7石rootからdepth-10以内の先手勝ちのみを証明する。
- 83d foldはchild orbit `00000000200000003800100000000200` を閉じ、第二target S5の残行を5→4に減らすが、S5自体は解決しない。
- **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class1・class2・class4は引き続きUNKNOWN**。

## 今後

- 次のfold baselineはhead **1314**（`class-frontier-cost83d-receipts-recompute-20261115.json`・blob `49cb8022`）。第二target S5は4行/293（best coverable class-2・残行はcost-84行が最安）。
- **cost-84a sweep IN FLIGHT**（並走・claim `59025a50`・child `00000000000040809002000000000800`・84候補）と**cost-62a IN FLIGHT**（並走・claim `64aa3938`・15:18:06Z）に着手禁止。着地後は本logの第二検証パターンを適用（tmpの有無をまず確認）。
- push直前の最新main確認で、兄弟が**監査v8両実装（第一実装104 pins・第二実装新version file）+agreement v5（83d endpoint pair追加）を着地済み**（`98f750b9`/`6b73f1cf`/`2294c403`/`ea748af0`/`bf3c46f1`・15:22-15:23Z）であることを確認した。これにより83d endpointは「fold着地 + 本第二検証 + 双実装監査v8 + agreement v5」の三重体制となった。次回候補は兄弟のv8/v5着地の再現検証（fresh mirrorで両audit script再実行・byte-identical照合）。着手前に必ず最新mainを再取得し、84a/62a着地状況を確認すること。

詳細: [83d fold head JSON](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-cost83d-receipts-recompute-20261115.json)、[83d fold script](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_cost83d_receipts_20261115.py)、[83d completed claim](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost83d-inflight-20261115.json)、[83c検証log（前回・consumed再依存の源）](./2026-11-15-n11-class2-lane-cost83c-fold-second-verification.md)、[83b検証log](./2026-11-15-n11-class2-lane-cost83b-fold-second-verification.md)。
