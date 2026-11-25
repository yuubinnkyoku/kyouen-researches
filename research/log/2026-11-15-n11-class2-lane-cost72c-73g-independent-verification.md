# 2026-11-15：cost-72c / cost-73g foldの独立検証 — head 1244・1249が別環境で再現

開始時状況: (a) Koyebエラーによるsandbox全面リセットでローカルstagingを喪失 → mainのraw URLから実験mirrorを再構築（pinned commit `de209c20` 時点で193ファイル + 72c certificates、404なし）。(b) 本sessionが72c fold scriptを再構築・実行していた最中に、同じ毎時レーンの並走実行がcost-72c foldをmainに着地（`85e1e87c`、head 1239 → 1244）。本sessionは以後「着地済み成果の独立検証」に切り替えた。本logの検証はすべて、mainとは独立に再構築した別環境・別実行によるものである。

## 成果1：cost-72c fold — 別構成scriptによる全数値一致

本sessionが独立に書いたfold script（構成が並走着地版と異なる: 35個のblob定数pin、証明書は2パートjoin→whole md5/blobで検証、claim v2をblob pin）で全統制がPASSし、並走着地版と全数値が一致した:

- **head 1244/6603/521339/4873/385062**、totals（総marginal 43・in-manifest 5・zero-mim receipts [39, 59, 64, 72, 96]・child orbit closed by bit1・証明書 321,781 rows / 11,604,178 bytes / 41,346,462 extraction nodes / 474 sub-roots）
- per-receipt addition: bit1→(6,2), bit7→(5,1), bit24→(5,1), bit39→(6,0), bit59→(4,0), bit64→(4,0), bit67→(5,1), bit72→(4,0), bit96→(4,0)
- parents_after: parent1 21行/1615・parent2 52行/3898（両者のchild `00000000000000801202000000220000` 行喪失を含む3行ずつ）
- **ranking CSV・top-candidates CSVはmain着地版とbyte-identical**（`cmp` で確認）— 2つの独立に書かれたfold scriptが、fold後の全175 S5行の残行状態を完全に一致させた。

運用面の確認: 並走着地版はclaimのblob pinningを廃止して内容検証のみとし、claim closure後も公開scriptが再実行可能な設計（cost-72b repairの教訓の反映、head JSON `baseline_erratum_note` に70f baseline_main prose誤記の記録もあり）。本sessionの暫定版はclaim v3をblob pinしていたため、claim closure updateで再実行不能になる設計だったことが判別した。並走版の方式が正しく、以後のfold scriptはclaim内容検証方式に統一する。本sessionの暫定script・暫定head JSON・暫定claim v3はmainには未push（破棄し、着地版で置換した）。

## 成果2：cost-73g fold（head 1244 → 1249）の独立検証

最新mainの73g fold script（blob shaは73g claim v4のfold recordに明記）を、再構築したmirrorでそのまま実行した。runpy鎖（73g → 72c → 70f → 71c → 70e → 1227 merge → MS5 manifest）全体が通しで再現され、**33個のCONTROLがすべてPASS**:

- 10 raw batchesからsweep再導出: 73候補を一度ずつ（claim列挙と一致）・**8 WIN7-D10（bits [31, 54, 56, 62, 69, 81, 89, 113]）・65 REFUTED・0 capped・総nodes 91,357,592**・pilot 3402×10・determinism rerun node-exact・v15 cross-engine 8/8 WIN + 3/3 refuted anchors・8 distinct D4 win orbits
- 8証明書をローカルpart bytesで直接検証: **343,092 rows / 12,392,797 bytes / 94,100,994 extraction nodes**・parts join == whole md5/blob・per-bit BigInt/Bareiss verify記録再読込・union 0/0・terminal 13..17
- root disjointness: 8新root vs 512 fold済みroot（499 through cost-71c + 4 cost-70f + 9 cost-72c）をraw-hex・D4両方で確認
- child orbit `00000000000000849002000000000800` はbit31 receipt（公開順最初）で閉鎖・set等式 `s_after == s_1244 UNION covers(8 roots)`・completed claim fold record一致
- **head JSON・ranking CSV・top-candidates CSVの3成果物すべてmainとbyte-identical**（`cmp` で確認）。head **1249/6598/520956/4868/384679** が別環境・別実行で再現された。

## 実験事実（環境・運用の記録）

- sandbox全面リセットの実験事実: ローカルだけに存在したstaging（未pushの作業状態）は喪失したが、重要証拠はすべてmain済みだったため実質被害なし。「再現不能なローカル状態に重要証拠を残さない」運用が機能した事例。
- raw URLの単発downloadで1件（73g bit89 part2）がサイレントに失敗していた → fold scriptのblob assertが即座に検出し、再downloadで解決。多層検証（blob pin → script内assert）の有効性を実証。
- `open_url` 経由のテキスト取得は末尾newlineの帰属で文字数が1ずれることがあり、byte-exact判定には使えない（72c CSVで7579 vs 7580の見かけ差分が出たが、`cmp` ではbyte-identical）。byte-exact判定はcurl実ファイル + `cmp` を維持する。

## 解釈境界（重要）

- solved数はmanifest被覆の簿記であり、いかなる局面のgame-theoretic値も意味しない。
- **REFUTED-D10はLOSS証明ではない**（depth-10以内の先手勝ちが無いことのみ）。
- WIN7証明書は個別7石rootからdepth-10以内の先手勝ちのみを証明する。73g child orbitの閉鎖は両開class-2親の残行を減らす（parent1 `00000000000000801202000000200000` 19行/1463・parent2 `00000000000000801242000000000000` 55行/4352）が、どちらのS5親も解決せず、class 2・class 4も決定しない。
- **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class1・class2・class4は引き続きUNKNOWN**。

## 今後

- 次のfold baselineは本head 1249（`class-frontier-cost73g-receipts-recompute-20261115.json`）。fold前に必ず最新mainを再取得し、並走lane（70g / 65l / 69g / 65j / 74e / 74g / 73h）の着地をチェックすること。
- cost-73h claim（並走lane・in flight）: sibling cost-73 row `00000000200000083800000000000200`（erratum `1631350a` で訂正後のhex）。本レーンは重複してsweepしない。
- 最安のcoverable class-2 targetは引き続き `00000000000000809102000000000000`（2行/143）。残るcost 69/74行は並走69g/74e claimと重複するため着手前に最新mainを確認すること。

詳細: [72c fold head JSON](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-cost72c-receipts-recompute-20261115.json)、[73g fold head JSON](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-cost73g-receipts-recompute-20261115.json)、[73g fold script](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_cost73g_receipts_20261115.py)、[73g ranking CSV](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-s5-ranking-after-cost73g-receipts-20261115.csv)、[73g top-candidates CSV](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-top-candidates-s6-after-cost73g-receipts-20261115.csv)。
