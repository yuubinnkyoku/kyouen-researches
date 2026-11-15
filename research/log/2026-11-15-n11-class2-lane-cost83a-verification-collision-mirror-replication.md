# 2026-11-15：cost-83a 第二独立検証の並走衝突とmirror再現 — 着地版が別環境でbyte-identicalに再現・非公開twin実装が全統制で一致

## 経緯（collision protocolの実績2件目）

本セッション（長期レーン）は前回レジュームどおり、並走が着地したcost-83a fold（head 1306→1309・4 WIN7-D10 bits [12,58,72,95]）の第二独立検証を、mainとは独立に構築したcodeload tarball全体展開mirror（3.3GB・着地sessionの状態は不使用）で開始した。

1. **tmp-cost83a再現性ギャップの検出**: fold script `recompute_frontier_cost83a_receipts_20261115.py`（blob `70fc5d12`）は `output/tmp-cost83a/bit{b}.cert-receipt.json` / `.bigint.json` / `.tsverify.json` / `.consumed.txt`（b ∈ {12,58,72,95}の16ファイル）を読むが、83a laneはこれらをpushしておらず、fold scriptはmain単独では `bit12.cert-receipt.json` で停止した（cost-69iと同一の障害形状。bit95の `.rows` は約2.1MBで単発push上限超過も確認）。
2. **自前修復の実装**: `reconstruct_tmp_cost83a_20261115.py`（自前版・非公開）を書き、published検証器（BigInt・TS-Bareiss）のみで16ファイルを再生して全PASS。続けて自前の第二独立検証script（非公開）を書いて実行し、全統制PASS・2回実行byte-identicalを確認した。
3. **push直前の最新main再取得で衝突を検出**: 並走が同一ファイル名の `reconstruct_tmp_cost83a_20261115.py` と `verify_cost83a_fold_second_independent_20261115.py` を着地済み（`69df8402`・13:19Z）。**着地済みファイルは一切変更せず**、自前版の公開を取りやめ、着地版の第三者再現に転換した（collision protocol・監査v3レースと同じ手順）。

## 成果1：着地版修復+検証鎖がfresh mirrorで完全再現

並走の着地成果物（修復script・再生成16 tmpファイルのうち公開分12件+bit72.consumed.txt witness・検証script）をmainから取得し、本セッションの隔離mirrorで実行:

- **修復script**: 16ファイルがmain成果物のみから再生・BigInt 4/4・TS-Bareiss 4/4 PASS・consumed集合 == 証明書行集合
- **検証script 2回実行**: 8統制すべてPASS（head 1306→1309・3成果物 blob `74e35f22`/`70eab6c4`/`fad56f79` byte-identical・sweep再集計 83候補/4 WIN/79 REFUTED/0 capped/152,978,839 nodes・4証明書 176,791 rows の第三幾何系検証・独立D4 marginal 19/3・zero-mim [58,95]・child bit12閉鎖・**596 roots / 585 orbits / 11 twins**・claim closure）
- **検証JSONがpublished版とbyte-identical**: md5 `88510d8c69e0bee6ecf73f562996d47c`・4,518 bytes（`2d90488f`で公開されたものと同一）。着地sessionと本セッションの**無関係な2環境で機械出力が一致**したことで、83a foldの第二独立検証は環境をまたいで再現可能と確定した。

## 成果2：非公開twin実装が全統制で一致

着地版を見る前に書いた自前の修復+検証実装（scriptsともに非公開）は、実質的な全統制で着地版と同じ値に到達していた: legal-moves Bareiss照合 60/58/57/68・証明書 rows 40,417/41,891/36,293/58,190（総計176,791 rows / 6,386,515 bytes / 243 sub-roots・union 0/0・rational verifier 4/4 すべて terminal {13,15,17}）・sweep 83/4/79/0（win sum 10,308,522・pilots 3402×11・determinism rerun node-exact・v15 anchors 4/4+3/3）・per-bit marginals がpublished addition records とhex集合単位で全field一致（19/3・zero-mim [58,95]・child はbit12でちょうど1回閉鎖）・set等式・parents_after 7行/542・67行/5509・596-root在庫 585 orbits/11 twins・claim closure。差分は配線と文言のみ（自前版は修復script自体もpin tableに含める点が追加）。

機械可読記録: [class2-lane-cost83a-fold-verification-mirror-replication-20261115.json](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost83a-fold-verification-mirror-replication-20261115.json)。

## 運用（今回確立）

- **同じギャップを両レーンが同時に修復する衝突が2度目**（tmp-cost69iに続きtmp-cost83a）。修復系ファイル名は定型（`reconstruct_tmp_<lane>_20261115.py`）なので衝突しやすい。修復着手前に最新mainの該当パスを必ず確認し、着地済みなら上書きせず再現検証に転換する。
- fold logの「再現」欄に「mainから1〜2分で再実行可能」とある場合は、tmp依存の実在ファイル一式がmainにあるか実際に再実行してから記述を信頼する（83a fold logの当該記述は修復着地までは不正確だった。修復script・README着地で解消済み）。

## 解釈境界（重要）

- solved 1309はmanifest被覆の簿記であり、いかなる局面のgame-theoretic値も意味しない。REFUTED-D10はLOSS証明ではない。WIN7証明書は個別7石rootからdepth-10以内の先手勝ちのみを証明する。
- 第二target S5 `00000000000000801202000000200000` は7行/542で未解決（並走がcost-83b child `00000000000000801202000000200010` をIN FLIGHT）。
- **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class1・class2・class4は引き続きUNKNOWN**。

## 今後

- 両audit script（第一実装v5・第二実装v5）のcost-83a endpoint（1309/596 roots/585 orbits）へのv6機械拡張と、dual implementation agreement v3拡張を本セッションで続行する。

詳細: [並走の83a第二独立検証log](./2026-11-15-n11-class2-lane-cost83a-fold-second-verification-and-tmp-reconstruction.md)、[83a fold log](./2026-11-15-n11-class2-lane-cost83a-sweep-certificates-and-fold.md)、[監査v3衝突の先例](./2026-11-15-n11-class2-lane-published-chain-roots-audit-v4-second-independent.md)。
