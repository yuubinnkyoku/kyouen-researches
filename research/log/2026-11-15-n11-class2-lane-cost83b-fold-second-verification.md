# 2026-11-15：cost-83b receipts foldの第二独立検証 — head 1312がmain単独から再現・5証明書が第三幾何系で再検証

開始時状況: canonical headは並走laneのcost-83b fold（commit `54f89d49`・head 1309→1312）とcost-83c fold（`e255a9cc`・head 1312→1313）着地後。cost-83b（第二coverable class-2 target S5 `00000000000000801202000000200000` のcost-83 child `00000000000000801202000000200010`・5 WIN7-D10 bits [9,12,58,64,96]）について、**tmp-cost83b/はmain上に完全存在**（34ファイル: bits 9/12/58/64/96のcert-receipts/bigint/tsverify/consumed/rows/summaries + bits 9/58/96のsplit + legal-moves.json）しており、cost-83a（[83a検証log](./2026-11-15-n11-class2-lane-cost83a-fold-second-verification-and-tmp-reconstruction.md)）と違って**再構成stepが不要**だった。83a第二検証script（blob `a4abde75`）を機械変換し、fresh codeload-tarball mirror（HEAD `e5673851`）・landing sessionの状態を一切使わずにmain公開bytesのみでfold全体を再検証した。

## 成果：第二独立検証 — 8統制すべてPASS・複数回実行で検証JSON byte-identical

`verify_cost83b_fold_second_independent_20261115.py` を作成・実行（約4分/回・実行JSONは2回byte-identical・本文言語修正版での再実行1回も同一md5）:

1. **published blob pins**: fold script `4239b520`（22,552B）・completed claim `a34ef154`（6,503B）・head JSON `b089bd95`（8,651B）・ranking CSV `c06ab3bb`（7,537B）・top-candidates CSV `13670c6a`（6,985B）
2. **tmp-cost83b在庫確認**: 34ファイル全存在・legal-moves.jsonが5 WIN bit全てをカバー
3. **fold script 2回の隔離subprocess実行**: runpy鎖でcost-83a baseline 1309/6538/516477/4808/380200を83a head JSON+両CSVとともにblob一致で再現し、3成果物がpublished blobとbyte-identical（2回の実行間でも一致）
4. **sweep再集計（独自コード）**: 11 raw batchesから83候補を一度ずつ（== claim列挙）・5 WIN7-D10 [9,12,58,64,96] / 78 REFUTED-D10 / 0 capped・総nodes 147,896,427（win sum 16,656,056）・pilots 3402×11・determinism rerun node-exact（8 bits）・v15 cross-engine 5/5 WIN + 3/3 refuted anchors（bits 0/1/2・pilot 5949）
5. **5証明書の第三幾何系（rational）再検証**: 新規コードでpart-join（bytes/md5/sha256/git blob == receipts・rows sorted-unique）し、published第三系 `verify_cost75d_win7_rational_independent.py`（exact Fraction circumcentre・iterative replay）で5/5 PASS・**275,648 rows / 9,968,222 bytes / 317 sub-roots**・union 0/0・terminal [13,17]内・consumed winner-row集合 == 公開TS consumed files（5/5）
6. **独立D4 + 逐次marginal算術**: 8 affine行列の独立実装でper-bit marginal / in-manifest / hexes がpublished addition recordsと**全field一致**（総marginal 23・in-manifest 3・zero-mim [58,64,96]）・child orbit closureはbit9（公開順最初）の1回のみ・set等式 `s_1312 == s_1309 ∪ covers(5 roots)` 成立・**第二target S5 7行/542 → 6行/459**（parent1喪失はchild行のみ）・第2開親 70行/5822 → 67行/5572（child + in-manifest 2行喪失）
7. **601-root在庫の軌道解析**: 596既存 + 5新規 = 601 roots・**590 distinct orbits**（585+5）・11 twin pairs（新twinなし）・5新rootは596在庫とraw-hex・D4ともdisjoint
8. **completed claim fold record**: head 1309→1312・publication order [9,12,58,64,96]・totals 23/3・zero-mim [58,64,96]・child closed by bit9・parents_after 6行/459・67行/5572・lost rows（parent2 = child + `00000000000000003800100008001000` + `00000000000000801202000000000210`）・output blob shas・head_json_bytes 8,651と全field一致

機械可読検証記録: [class2-lane-cost83b-fold-second-verification-20261115.json](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost83b-fold-second-verification-20261115.json)（4,271 bytes・md5 `e2da7162`・git blob `09f89855`・複数回実行byte-identical）

これによりcost-75d/80d/82c/83a/83bの全5 fold endpointが「並走laneの実装 + 本レーンの第二独立実装」の二重検証体制となり、うち82c/83a/83bは第三幾何系（rational verifier）による証明書再検証も付く。

## main反映

- 検証script + 検証JSON + 本logをpush（push直前の最新main再取得で兄弟の83b検証着地なし・競合なしを確認。並走はcost-83c fold着地後、cost-83d IN FLIGHT claim `3ba611fc` まで進行）
- 全ファイルraw CDN照合byte-identical

## 解釈境界（重要）

- solved 1312はmanifest被覆の簿記であり、いかなる局面のgame-theoretic値も意味しない。REFUTED-D10はLOSS証明ではない。WIN7証明書は個々の7石rootからdepth-10以内の先手勝ちのみを証明する。
- 83b foldはchild orbit `00000000000000801202000000200010` を閉じ、第二target S5の残行を7→6に減らすが、S5自体は解決しない（83cでさらに5→…に減った後も未解決）。
- **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class1・class2・class4は引き続きUNKNOWN**。

## 今後

- cost-83c fold（head 1312→1313・commit `e255a9cc`）の第二独立検証が次候補。ただし**83c成果物の一部がmirror（HEAD `e5673851`・13:47Z時点）に未着地**のため、raw batches 11件・証明書2件・claim・head JSON等のCDN fetchから始める必要がある。
- **cost-83d IN FLIGHT**（並走・commit `3ba611fc`・14:03:54Z）に着手禁止。
- audit v7機械拡張（83b/83c endpoint・head 1313）とagreement v4が次回候補。着手前に必ず最新mainを再取得し、83c検証・83d着地状況を確認すること。

詳細: [83b fold head JSON](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-cost83b-receipts-recompute-20261115.json)、[83b fold script](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_cost83b_receipts_20261115.py)、[83b completed claim](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost83b-inflight-20261115.json)、[tmp-cost83b checkpoint](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/tmp-cost83b/)、[83a検証log（前回・tmp再構成を含む）](./2026-11-15-n11-class2-lane-cost83a-fold-second-verification-and-tmp-reconstruction.md)。
