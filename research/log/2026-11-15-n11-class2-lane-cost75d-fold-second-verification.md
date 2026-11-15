# 2026-11-15：cost-75d receipts foldの第二独立検証 — head 1296が再構築mirrorで再現

開始時状況: 同日のpublished-fold chain全監査v3（[別log](./2026-11-15-n11-published-fold-chain-roots-independent-audit.md)）に続き、並走laneが着地したcost-75d receipts fold（`81707a4c`・`a63ea0bb`・`ef0765a3`、head 1290→1296）を、mainとは独立にcodeload tarballから再構築した隔離mirrorで検証した。本logの検証は別環境・別実行によるもの。75dのsweep入力（10 raw batches・determinism rerun・v15 crosscheck・extraction summaries・BigInt/Bareiss verify records・split manifests）・証明書4件（bit12/bit40 single files・bit92 2分割・bit111 3分割）・sweep claim・fold claim v2はmirror構築時点でmain済みだった。fold script（blob `a9664368`）はmainから取得して実行した。証明書4件の第三幾何系（rational）による第二検証は[別JSON](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost75d-certificates-second-verification-20261115.json)として先に着地済みで、本検証はその"to-follow"項目（fold本体＋fold script内の全root簿記。head 1277の548-rootに代わるhead 1290の565 fold済みrootとのdisjointnessを含む）に対応する。

## 成果：published fold scriptの再構築mirrorでのend-to-end再実行 — 全統制PASS・3成果物byte-identical

`recompute_frontier_cost75d_receipts_20261115.py`をそのまま2回実行し（約3.3秒/回・2回とも全出力byte-identical）、全CONTROL PASS:

- **baseline再構成**: 77c fold scriptをrunpyで再現し、head 1290/6557/517923/4827/381646のhead JSON `7f2badce`（10,558B）・ranking CSV `9ada5dfc`（7,539B）・top-candidates CSV `8d5583e0`（7,589B）ともmainとblob一致（それ以前のfold鎖は77c script内でchain-internallyにassert済み）
- **child genuinely remaining**: 唯一のopen lift親（第二target S5）がhead 1290でchild行 13行/1018を保持・demand c1=0,c2=1,c4=0再導出・lift stone 78がparent1を正確に再現・残り5つのdeletion orbitは閉鎖維持
- **sweep再導出**: 10 raw batch JSONLsから75候補を一度ずつ・4 WIN7-D10 bits [12,40,92,111] / 71 REFUTED-D10 / 0 capped・総nodes 143,552,593・pilot 3402×10・determinism rerun node-exact・v15 pinned record 4/4 WIN（nodes 1,406,438 / 7,087,163 / 16,644,786 / 10,234,430）＋refuted anchors 5/5 bits 0/2/4/6/86（pilot 5949×3）
- **証明書bytes検証**: 4証明書を実bytesで検証 — 239,868 rows / 8,654,219 bytes / 242 sub-roots・bit92（2分割）とbit111（3分割）はpart-join == whole・split manifests・receipts md5/sha256/blob・BigInt + Number Bareiss verifier records 4/4 PASS（union 0/0）
- **root-orbit簿記**: 4新root vs 565 fold済みroot（head 1290時点）がraw-hex・D4ともdisjoint・4 distinct D4 orbits
- **fold結果**: **head 1296/6551/517468/4821/381191**・総marginal 22・in-manifest 6（zero-mim/zero-marginal receiptsなし）・child orbitはbit12（公開順最初）で閉鎖・set等式control成立・第二target S5 13行/1018 → 11行/866（喪失行 = child行とcost-77行 `00000000100000801202000000200000`。後者はbit-92 cross-coverで閉鎖 — 進行中の77d foldにwarm-hygiene必須）
- **3成果物すべてmainとbyte-identical**: head JSON `c801e605` 8,992B・ranking CSV `25b7fc1b` 7,538B・top-candidates CSV `d6782837` 7,416B（git blob sha照合）
- 着地済みclaim v2 fold record（chain_head_before/after・receipts・per_receipt_marginals・zero_mim/zero_marginal・child_closed_by_bit・parents_after・parents_lost_rows・output_blob_shas）と全field一致（PASS）

機械可読検証記録: [class2-lane-cost75d-fold-second-verification-20261115.json](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost75d-fold-second-verification-20261115.json)

## 解釈境界（重要）

- solved 1296はmanifest被覆の簿記であり、いかなる局面のgame-theoretic値も意味しない。REFUTED-D10はLOSS証明ではない。WIN7証明書は個別7石rootからdepth-10以内の先手勝ちのみを証明する。
- 75d foldはchild orbitを閉じ、第二target S5の残行を13→11に減らすが、S5自体は解決しない。
- **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class1・class2・class4は引き続きUNKNOWN**。

## 今後

- 次のfold baselineはhead **1296**（`class-frontier-cost75d-receipts-recompute-20261115.json`・blob `c801e605`）。
- 第二coverable class-2 target S5 `00000000000000801202000000200000` は11行/866・best class-4 blocker `00000000020000003800000080000000` 18行/1460、いずれも未解決。
- 並走lane状況: cost-77d sweepがIN FLIGHT（77c head 1290基準で実行中）。着地時はhead 1296へのrebaseとwarm-hygiene統制（77d child行が75d bit-92 cross-coverで既に閉鎖）が必須 — K0783とv3監査logに記載済み。重複してsweep/foldせず、着手前に必ず最新mainを再取得すること。

詳細: [75d fold head JSON](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-cost75d-receipts-recompute-20261115.json)、[75d fold script](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_cost75d_receipts_20261115.py)、[75d claim v2](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost75d-inflight-20261115.json)、[75d ranking CSV](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-s5-ranking-after-cost75d-receipts-20261115.csv)、[75d top-candidates CSV](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-top-candidates-s6-after-cost75d-receipts-20261115.csv)、[75d fold log](./2026-11-15-n11-class2-lane-cost75d-receipts-fold.md)、[75d certificates第二検証JSON](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost75d-certificates-second-verification-20261115.json)。
