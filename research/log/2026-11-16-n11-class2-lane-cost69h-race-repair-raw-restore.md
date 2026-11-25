# 2026-11-16 n11 class2-lane: cost-69h concurrent-run race repair — raw batch1/2/3 byte-exact restore + pinned-v16 independent re-run verification

## やったこと

1. **race事故の全容確定**。第二独立検証（`7c99621f`）が指摘した69h raw出版ギャップ（batch2のbit集合不一致・batch3欠落）の原因をgit履歴調査で特定した: **commit `10b054ef`（2026-11-15T06:45:34Z・parabola-p2207レーンのコミット「re-verify the 5059 (0,1,0) certificate … and record the concurrent-run race」）が69hレーンの foreign file 3本を巻き込んでいた**（batch1 modified +8 -8・batch2 modified +8 -8・batch3 removed +0 -9）。コミット自身が記録している concurrent-run race が機構と推定される。
2. **batch1の新規検出（第二検証のX6では見えていなかった缺陷）**。X6はraw/auditのcandidate bit集合照合のみで、batch1はbit集合が変わっていなかったためok判定になっていた。しかし**node合計でbatch1だけがaudit集計と+611,900漂移**していた（clobber版 11,645,338 vs audit 11,033,438）。batch4-9は全てauditと一致（diff 0）。verdictは全行loss=falseで矛盾なし・WIN bits 58/96はbatch5/7で無事。
3. **復元は再実行ではなく歴史からのbyte-exact restore**。本来の出版コミット（batch1=`7b753f73` 03:01:21Z・batch2=`79892475` 03:01:26Z・batch3=`706d2aaa` 03:01:31Z）から2独立経路（raw CDN・GitHub contents API resource）で取得し一致確認。**clobber版batch2のbits 17/19/20/21は非合法bit**（第二検証X4/X5で機械検証済み・bit21 loss:trueもinert engine entryでlegal root canonと衝突しない）。
4. **pinned v16による全24 bit独立再実行でnode-exact検証**（`class4_child1_runner_v16.ts` main md5一致・depth 10・cap 1e9・andclose 1・pilot d6 3,402 nodes ×3 PASS・child `0000000000000080120a000000200000`）。**3バッチとも復元正本と9/9行一致（bit/loss/nodes/capped/terminalStoneRange/andclose・ms除く）**・audit集計再照合 batch1 11,033,438 / batch2 7,756,242 / batch3 12,707,969 全一致・69候補総合計 83,542,525 一致。
5. **出版**（commit `4885d75e`・7ファイル）: raw batch1/2/3復元（git blob `11bc5881…`/`f73da762…`/`b56c811c…`・着地後raw再取得+blob sha再計算でbyte-exact照合済み）+ 再実行アーティファクト `class2-lane-cost69h-race-repair-rerun-batch{1,2,3}-20261116.jsonl` + 検証記録 `class2-lane-cost69h-race-repair-verification-20261116.json`。

## 影響評価

- **verdict・fold・headへの影響なし**。復元24 bitはすべてREFUTED-D10（loss=false・非capped）で、clobber版batch1のverdictともauditとも一致。WIN7-D10 bits 58/96のrawはrace対象外。foldはaudit集計とWIN証明書を使っており無影響。scan engine map（8,964 verdicts）も restoration で不変。
- 第二検証の `data_quality_observations.cost_69h_publication_gap` はpin時点（post-race main）の観察として歴史的に正しいまま。本修復によりraw batch2のbit集合はaudit計画と一致し、batch3はmainに再存在する。
- claim v4の「raw batch1..9 all pushed」記述は修復後に正しくなる。

## 運用教訓（実験事実）

- **並走セッションのmixed commitが最大のデータ汚染リスク**: 他レーンのコミットが自レーンの raw ファイルを巻き込む事故はbit集合照合（X6）では検出できない場合がある（batch1のnode drift）。**rawアーティファクト出版後はaudit集計とのnode合計照合を独立チェックとして入れるべき**。
- **git履歴は最良のバックアップ**: race事故で上書き/削除されたrawファイルでも元出版コミットからbyte-exact復元でき、git blob sha照合で完全性を機械検証できる。

## レジューム

- canonical head **1410不変**（本修復はbookkeeping・verdict不変）。
- 69h batch2/3 raw再出版の残課題は**本修復で解消**（再実行ではなく復元+検証で、より強い形: node-exact再実行付き）。
- 69a（並走in-flight）は着手禁止。K0863予測（bit 109 REFUTED-D10）着地待ち。76d/77e fold着地時は1410 headとのreconciliation必須。
- 次回の大工事は65j fold（前ログのレジューム参照）。
- **solved 1410はmanifest被覆の簿記。REFUTED-D10はLOSS証明ではない。STERILEもLOSS証明ではない。11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class1/class2/class4はいずれもUNKNOWN**。
