# Part DH takeover-3 宣言: b28 P4パッケージ9行 第三実装交叉検証 (takeover-2 lane 停滞の継承)

- 出版: 2026-11-24T17:2xZ (takeover単一オーナー宣言・3代目takeover・publish-then-execute)
- 原宣言: `research/log/2026-11-24-part-dh-b28p4win9-thirdimpl-declaration.md` (出版 `f63c1654`・2026-11-24T06:07:31Z)
- 第1次takeover: `research/log/2026-11-24-part-dh-b28p4win9-thirdimpl-takeover.md` (`a4e00aa3`・09:40:53Z・D5開始時outageで中断・interim `076e05c1` 09:50:39Z)
- 第2次takeover: `research/log/2026-11-24-part-dh-b28p4win9-thirdimpl-takeover2.md` (`8699b203`・13:22:07Z・D1-D4 fresh再実行成果物をB wave1 `68483d7d` 13:26:22Zで出版: rules-gate・val-gate fresh `.dh-host.out` 4/4 node-exact・negatives fail-closed 2件・anchors k02a/l1a exp/ttH pin一致・status.log 6行)
- 第2次takeover laneの停滞: `68483d7d` (13:26:22Z) を最後に D5 (replica 18 pass) 以降の出版物なし (3時間49分超)。D5はper-key最大295sの独立18呼び出しで増分出版に適した構成であり、B wave出版後ただちに着手すべき工程であるにもかかわらず出版物ゼロ。
- earliest_takeover (本takeover-3): 現owner laneの最終出版 68483d7d 13:26:22Z + 3.5h = **16:56:22Z経過後**に本宣言を出版した (anchorは最終出版時刻・時刻逸脱なし)。
- 対抗takeover-3・原オーナー再開・第2次takeover lane再開の機械確認 (出版直前): 最新main再取得 HEAD `90732788` (2026-11-24T17:03:15Z・Part DQ kit wave C)・DH実験dir `research/experiments/n11-centralreply-closure-b28p4win9-thirdimpl-20261124` への13:26:23Z以降のcommit **0件**・`research/log` の13:26:23Z以降のcommit走査でDH関連 (declaration/takeover/takeover2 以外) **0件**・commit message走査で「Part DH」「takeover」の新規主張なし。対抗なし。出版後に観測した対抗があればamendmentで誠実対処 (hourly並走注意)。

## 継承の範囲と本laneの方針

- 第2次takeoverのD1-D4 (B wave1 `68483d7d`) は published evidence として参照 (本laneでbyte復元・pin照合済み)。本laneは **D1-D8 を本hostですべて fresh 再実行**し成果物を出版する (自己完結のevidence chain・takeover-2が第1次takeoverの未出版D1-D4に対したのと同一方針)。D1-D4 fresh値とtakeover-2 published値の交差照合 (rules-gate byte-identical想定・negatives文言一致想定・anchors exp/ttH exact想定 (wall_sのみ差)・val-gate node-exact想定 (wall_sのみ差)) を実行記録に含める。
- val-gate host sidecar は audit pin suffix `.dh-host.out` で本host fresh走行により再生成・出版する。takeover-2 host sidecarの出版bytesはcommit `68483d7d` のgit historyに保存され、本lane走行値とnon-wall全field一致を交差照合後に上書きする (honest記録)。
- 本laneは「長期レーン」の take duties として D5-D8 の長時間計算を担当する。本host 2並列上限 (2 core)。

## kit復元・検証 (published evidenceのみを正本として再構築・本lane)

- 実験dir 74ファイルを出版commit指定raw fetchで復元: A1 `f8db8d87` (scripts 7 + input 14 + val-gate 8 + README) / A2a `de650462` (sources 38: raw 18・published-input 9・published-input-bf 4・status 4・batch-keys-b28・queue-registry rev3・README-queue) / A2b `871af8cf` (CO/DB cache 2 + increment 2 + manifest 2)。注記: CO/DB系6ファイルはA2a commitのsources pathでは取得できずA2b `871af8cf` から取得した (74 = 1+7+14+8 + 44・目録整合)。
- 全pin照合 (原宣言pin表・mismatch 0): scripts 7 (`8036d0e5`/`88e25e0e`/`4dae72ac`/`a0b77d83`/`08ea958f`/`c8c52528`/`84585617`)・input/rows.json `6a0e4012…`・raw 18 (aa034 p1==p2 `42580df2…`・aa050 p1==p2 `aada66cf…` byte同一含む)・status-drive4 `59817444…`/drive5 `ca1e98cc…`/cs25m `cea47a0c…`/ct30m `efd18b3c…`・batch-keys `af19208f…`・queue-registry rev3 `334f6209…`・README-queue `4b20c6a0…`・CO cache `854800f3…`/increment `bd5ef7d7…`/manifest `b47e07ca…`・DB cache `04b0a239…`/increment `85bd4469…`/manifest `1b51f30d…`・val-gate baselines `6e902ab1`/`eeafe3ac`/`8035fe54`/`91dffdec`。
- maker gates PASS ×2・stdout byte-identical (sha256 `9a38606eed5451e…` = 原宣言pin prefix `9a38606e`)・input 14 file byte-stable。
- rules-gate用 lane-kit (`/home/user/knowledge/…` Knowledge durable領域 `_class1297036830122704896-lane-kit/inv/jsreplay.js`) sha `84585617…` 一致 (outageを通じて存続)。
- 環境smoke (本宣言前・unofficial・成果には含めない): verify_tbl.js quads 95,670 / triples 195,044 mismatches 0・jsreplay.js at2m 2M budget-exhausted node-exact vs published baseline (wall_sのみ差)・third_impl.js ng1 fail-closed文言一致。本host rate ~220k nodes/s (jsreplay)。

## 実行protocol (原宣言D1-D8・takeover-2 protocol を変更なく引き継ぐ)

- D1 rules-gate: `node scripts/verify_tbl.js` (quads 95,670 / triples 195,044 / mismatches 0 → `output/rules-gate.txt`)。
- D2 val-gate fresh 4 (2M/2M/15M/15M): `node scripts/jsreplay.js --exact-replay=val-gate/<k>.input.csv --exact-replay-budget=<budget>` → `.dh-host.out` (baseline node-exact期待)。
- D3 negatives ng1/ng2 (期待fail-closed)・D4 anchors k02a/l1a (`run_thirdimpl.sh` a/b・exp 9,106,337 / 7,660,202・ttHits 4,991,527 / 3,951,175 pin一致期待)。
- D5 replica 18 pass (9キー×p1/p2・**1 call 1 pass**・`run_replica_dh.sh <key> <pass>`・per-key budget 15M×5 / 25M×3 / 30M×1・inner timeout 260/288/295)。audit G2bで p1==p2 + published raw node-exact。2並列上限。
- D6 thirdimpl 18 run (9キー×a/b・wallcap240・est pass-one最大 aa050 ~30M・runlimit時はWALL-INCONCLUSIVEとしてhonest記録しverdictとはしない)。2並列上限。
- D7 audit `audit_dh.py` ×3 (stdout byte-identical + summary・全gate PASS必須)。FAIL→成果FAILとして記録・出版 (押し通さない)。
- D8 tamper battery (4種: replica nodes+1 → verdict-vs-published / target result反転 → det-pair or verdict-agree / anchor expansions改竄 → anchor gate / rows.json replica_nodes改竄 → verdict-vs-published。全部捕捉 + byte-exact復元 + 復帰green期待)。
- D9 出版: B outputs (進捗に応じた分割出版可・環境reset対策で早期出版優先) → C README最終+MANIFEST-sha256 → 完了log → queue registry bookkeeping は実行時点の最新registry状態に基づく (本宣言時点の想定: rev5 `4734f13f…` published状態で P4 9行 open・DH完了なら done_win 37→46・open_win 9→0・packages.P4 done・thirdimpl_publications.DH追記・rev6として出版・競合時は見送り記録して次回へ)。

## 停止条件 (原宣言・takeover-2宣言と同一)

- いずれかのgateで FAIL/MISMATCH → 実行停止・誠実記録・verdict不消費。
- 第三実装verdictがpublished WIN (rc=1) と一致しない場合 → 採用も被覆も一切行わず divergence証拠として記録。
- 実験中の環境reset等 → published scaffoldからkit復元・sha検証の上やり直し (published evidenceだけが証拠)。
- push競合・同時書き込み・取得失敗 → 無理に押し進めず記録して次回実行に回す。
- **verdicts不消費**: 対象9行 (aa011/aa054/aa022/aa034/aa037/aa032/aa028/aa021/aa050) は unadopted honest WIN labels のまま。adoptionは scrutiny owner C++第二実装 gate `9193f5b6…` 通過後・pinned merger `90711961…` 経由の別adoption Part 専権。
- **標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2 {59,60}・class 5343 (全54キー) は本Partの前後を通じてすべてUNKNOWNのまま。** nodes数・expansions数・ttHits数を勝敗や距離として読まない。
- 非接触: Part DQ (batch-33 class 34908・17:00Z宣言の単一オーナーlane、キー空間 af001..af054 は本Part対象aa*と無関係)・Part DP canonical chain・scrutiny owner専権事項・各published dir。

## observed

- HEAD-before-push (本宣言出版時): `90732788` (2026-11-24T17:03:15Z)。
- 対象9行 (per-key decisive budgets・原宣言表と同一): aa011 15M 12,424,953 / aa054 15M 13,227,570 / aa022 15M 14,044,375 / aa034 15M 14,097,048 / aa037 15M 14,239,714 / aa032 25M 20,312,294 / aa028 25M 21,563,925 / aa021 25M 22,942,323 / aa050 30M 25,541,199 (pinned合計 158,393,401)。
