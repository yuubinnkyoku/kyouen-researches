# 2026-11-15：cost-83c receipts foldのtmp再構成+第二独立検証 — head 1313がmain単独から再現・2証明書が第三幾何系で再検証

開始時状況: canonical head **1313/6534/516144/4804/379867**（cost-83c fold着地後・commit `e255a9cc`）。並走laneが着地したcost-83c fold（cost-83bで残った第二coverable class-2 target S5 `00000000000000801201202000000200000`系child `00000000200000003800000000400200`・2 WIN7-D10 bits [16,82]・head 1312→1313）について、**tmp-cost83c/はmainに一切存在せず**（83aと同じ形状のギャップ）、fold scriptが読む9ファイル（legal-moves.json + bits 16/82のcert-receipt/bigint/tsverify/consumed）が全て欠落していた。本セッションは83c成果物（fold script・claim・11 raw batches・v15/v16・証明書2件・head JSON・両CSV）をmain raw CDNからmirrorにfetchしてgit blob shaで照合した上で、83a検証（[83a検証log](./2026-11-15-n11-class2-lane-cost83a-fold-second-verification-and-tmp-reconstruction.md)）と同じパターンで再構成+第二独立検証を行った。

## 成果1：tmp-cost83c/9ファイルの再構成 — published検証器のみで全PASS

`reconstruct_tmp_cost83c_20261115.py` を作成し、main成果物のみから9ファイルを再生:

- **legal-moves.json**: 83c laneはtmpを1つも公開していないため**完全自前生成**（exact-integer Bareiss 4x4 determinantで合法loser初手を計算・bit16 61手 / bit82 60手 == published sub_roots_pass）
- **cert-receipt 2件**: 証明書bytes（2件とも単一ファイル・raw読み込み）から直接算出・md5/rowsはpublished head JSONの `cost83c_addition` 記録と一致（bit16 47,205行 / bit82 42,939行）
- **bigint.json**: published BigInt verifier（`verify_win7_certificate_bigint_independent.mjs`）をfresh runし2/2 PASS（union 0/0・terminal_range [13,17]）
- **tsverify.json + consumed.txt**: published TS-Bareiss verifier（`verify_bit7_win7_cert.ts`・--root-check + --subroots + --consumed-out）をfresh run（bit16 61・bit82 60 sub-roots・全sub-root range [13,17]内・consumed 90,144 keysの集合 == 証明書全行集合）
- 実行約40秒・全stepでcross-assert・総計 **90,144 rows / 3,257,864 bytes / 121 sub-roots** == published head JSON totals

## 成果2：published fold scriptのend-to-end再現 — head 1313・3成果物byte-identical

再構成tmpに対し `recompute_frontier_cost83c_receipts_20261115.py`（blob `9d25d201`）を隔離mirrorで2回実行（2回とも全統制PASS）:

- runpy鎖でcost-83b baseline 1312/6535/516227/4805/379950を83b head JSON（blob `b089bd95`）+両CSVとともにblob一致で再現（83b鎖は1309の83a head再現まで再帰的に含む）
- child genuinely remaining（両開親 6/459・65/5330がchild行を保持・demand c1=0,c2=2,c4=0）・sweep再統制・2証明書union 0/0・601-root disjointness・fold後のchild閉鎖とset等式
- **3成果物すべてmainとbyte-identical**: head JSON `fc7832ed` 6,811B・ranking CSV `08f0d715` 7,537B・top-candidates CSV `6a40509d` 6,899B（2回の実行間でも一致）

## 成果3：第二独立検証 — 8統制すべてPASS・2回実行byte-identical

`verify_cost83c_fold_second_independent_20261115.py` を作成・実行（約5分/回・2回実行で検証JSON byte-identical）:

1. **published blob pins**: fold script `9d25d201`・claim `6fdd0e63`・head JSON `fc7832ed`・ranking `08f0d715`・top-cand `6a40509d`
2. **tmp再構成をsubprocessで実行**（本検証の前提を自前で再現）
3. **fold script 2回の隔離subprocess実行**: 3成果物がpublished blobとbyte-identical
4. **sweep再集計（独自コード）**: 11 raw batchesから83候補を一度ずつ（== claim列挙）・2 WIN7-D10 [16,82] / 81 REFUTED-D10 / 0 capped・総nodes 132,219,127（win sum 2,357,798）・pilots 3402×11・determinism rerun node-exact（8 bits）・v15 cross-engine 2/2 WIN + 3/3 refuted anchors（bits 0/1/2・pilot 5949）
5. **2証明書の第三幾何系（rational）再検証**: 新規コードで読み込み（bytes/md5/sha256/git blob == receipts・rows sorted-unique）し、published第三系 `verify_cost75d_win7_rational_independent.py`（exact Fraction circumcentre・iterative replay）で2/2 PASS・**90,144 rows / 3,257,864 bytes / 121 sub-roots**・union 0/0・terminal [13,17]内・consumed winner-row集合 == 再構成TS consumed files（2/2）
6. **独立D4 + 逐次marginal算術**: per-bit marginal / in-manifest / hexes がpublished addition recordsと**全field一致**（総marginal 9・in-manifest 1・zero-mim [82]）・child orbit closureはbit16（公開順最初）の1回のみ・set等式 `s_1313 == s_1312 ∪ covers(2 roots)` 成立・**第二target S5 6行/459 → 5行/376**（parent1喪失はchild行のみ）・第2開親（83c固有のclass-2 S5 `00000000000000801202000000000100`）65行/5330 → 64行/5247（喪失はchild行のみ）
7. **603-root在庫の軌道解析**: 601既存 + 2新規 = 603 roots・**592 distinct orbits**（590+2）・11 twin pairs（新twinなし）・2新rootは601在庫とraw-hex・D4ともdisjoint
8. **completed claim fold record**: head 1312→1313・publication order [16,82]・totals 9/1・zero-mim [82]・child closed by bit16・parents_after 5行/376・64行/5247・lost rows（両parentともchildのみ）・output blob shas・head_json_bytes 6,811と全field一致

機械可読検証記録: [class2-lane-cost83c-fold-second-verification-20261115.json](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost83c-fold-second-verification-20261115.json)（4,648 bytes・md5 `ce10c6d3`・git blob `7cbc21a6`・2回実行byte-identical）

これによりcost-75d/80d/82c/83a/83b/83cの全6 fold endpointが「並走lane実装 + 本レーン第二独立実装」の二重検証体制となり、83a/83b/83cは第三幾何系（rational verifier）による証明書再検証も付く。

## main反映

- 再構成script + 第二検証script + 検証JSON + tmp-cost83c小ファイル7件（legal-moves・receipts/bigint/tsverify×2bit）+ 本logをpush（consumed.txtは再構成scriptで再生可能なためsize上限から除外）。push直前の最新main再取得で競合・兄弟の83c検証着地なしを確認
- 全ファイルraw CDN照合byte-identical

## 解釈境界（重要）

- solved 1313はmanifest被覆の簿記であり、いかなる局面のgame-theoretic値も意味しない。REFUTED-D10はLOSS証明ではない。WIN7証明書は個々の7石rootからdepth-10以内の先手勝ちのみを証明する。
- 83c foldはchild orbit `00000000200000003800000000400200` を閉じ、第二target S5の残行を6→5に減らすが、S5自体は解決しない。
- **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class1・class2・class4は引き続きUNKNOWN**。

## 今後

- 次のfold baselineはhead **1313**（`class-frontier-cost83c-receipts-recompute-20261115.json`・blob `fc7832ed`）。第二target S5は5行/376。
- **cost-83d IN FLIGHT**（並走・commit `3ba611fc`・14:03:54Z）に着手禁止。着地後は本logの再構成+第二検証パターンを適用可能（tmp-cost83dの有無をまず確認）。
- audit v7機械拡張（83b/83c endpoint・head 1313）とagreement v4が次回候補。着手前に必ず最新mainを再取得し、83d着地状況を確認すること。

詳細: [83c fold head JSON](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-cost83c-receipts-recompute-20261115.json)、[83c fold script](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_cost83c_receipts_20261115.py)、[83c completed claim](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost83c-inflight-20261115.json)、[83b検証log（前回）](./2026-11-15-n11-class2-lane-cost83b-fold-second-verification.md)、[83a検証log（tmp再構成の先例）](./2026-11-15-n11-class2-lane-cost83a-fold-second-verification-and-tmp-reconstruction.md)。
