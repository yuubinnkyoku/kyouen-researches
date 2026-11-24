# Part DH takeover-2 宣言: b28 P4パッケージ9行 第三実装交叉検証 (takeover lane a4e00aa3 停滞の継承)

- 出版時刻: 2026-11-24T13:2xZ (commit timestampはGitHub側・takeover単一オーナー宣言・2代目takeover)
- 原宣言: `research/log/2026-11-24-part-dh-b28p4win9-thirdimpl-declaration.md` (出版 `f63c1654`・2026-11-24T06:07:31Z・publish-then-execute)
- 第1次takeover: `research/log/2026-11-24-part-dh-b28p4win9-thirdimpl-takeover.md` (出版 `a4e00aa3`・2026-11-24T09:40:53Z・observed HEAD `e56c8cce`・earliest_takeover 09:37:31Z経過後出版・対抗0機械確認済み)
- 第1次takeover laneの最終出版: interim note `076e05c1` (2026-11-24T09:50:39Z「D5 replica 開始時に実行環境outage・D1-D4出力はhost上にあるが出版未済・環境復旧後に B wave出版して D5 resume」・非PASS主張)。以降publication停滞をobserved。
- earliest_takeover (本takeover-2): 現owner laneのtakeover宣言 09:40:53Z + 3.5h = 13:10:53Z、およびその最終出版 (interim note) 09:50:39Z + 3.5h = 13:20:39Z。両時刻経過後 (13:20:4xZ) に本宣言を出版した (anchorは保守的な後者・時刻逸脱なし)。
- 対抗takeover・原オーナー再開・第1次takeover lane再開の機械確認 (出版直前): 最新main再取得 HEAD `8a29c987` (2026-11-24T12:44:51Z・Part DN完了log)・DH実験dir `research/experiments/n11-centralreply-closure-b28p4win9-thirdimpl-20261124` への09:40Z以降のcommit **0件** (outputs未出版のまま)・`research/log` の09:55Z以降のDH関連log **0件**・commit search「Part DH takeover」該当は第1次takeover宣言のみ。対抗なし。
- 継承の範囲: 第1次takeover laneのD1-D4 (host上のみ・未出版) は published evidence がゼロのため、本laneで D1-D8 をすべて fresh 再実行する (publish-then-execute・規約どおり・D1-D4が済んでいる事実はinterim noteがhonest記録済み)。

## kit復元・検証 (本lane・published evidenceのみを正本として再構築)

- 実験dir 74ファイルを出版commit指定raw fetchで復元 (A1 `f8db8d87` scripts 7 + input 14 + val-gate 8 + README / A2a `de650462` sources 38 / A2b `871af8cf` 6)。
- 全pin照合 (原宣言pin表・machine check): scripts 7 (make_inputs_dh.py `8036d0e5…` / audit_dh.py `88e25e0e…` / run_replica_dh.sh `4dae72ac…` / run_thirdimpl.sh `a0b77d83…` / third_impl.js `08ea958f…` / verify_tbl.js `c8c52528…` / jsreplay.js `84585617…`)・input/rows.json `6a0e4012…`・raw 18 (aa034 p1==p2・aa050 p1==p2 byte同一含む)・status 4 (drive4 `59817444` / drive5 `ca1e98cc` / cs25m `cea47a0c` / ct30m `efd18b3c`)・batch-keys `af19208f`・queue-registry rev3 `334f6209`・README-queue `4b20c6a0`・CO/DB cache+increment+manifest 6 → すべて一致・mismatch 0。
- maker gates PASS ×2・stdout byte-identical (sha256 prefix `9a38606e` = 原宣言pin)・input 14 file byte-stable。
- rules-gate用 lane-kit (`_class1297036830122704896-lane-kit/inv/jsreplay.js` = pinned `84585617…`) はKnowledge durable領域に存在・sha一致 (outageを通じて存続)。
- 環境smoke (本宣言前・unofficial・成果には含めない): verify_tbl.js quads 95,670 / triples 195,044 mismatches 0・jsreplay.js 2M budget-exhausted node-exact (wall差のみ)・third_impl.js ng1 fail-closed文言一致。

## 誠実記録 (incident)

- 本lane準備中 (13:0x-13:2xZ) に実行環境の一次利用不可 (filesystem同期rollback失敗) が発生し、準備途中のローカルkit復元 (74ファイル・pin全照合済み) を消失した。published evidenceのみを正本として同74ファイルを再復元・再pin照合・maker再検証 (上記のとおり全部一致) のうえ本宣言を出版した。誤出版なし。第1次takeover laneの09:4xZ outage (interim note記載) と同一事象。

## 実行protocol (原宣言D1-D8を変更なく引き継ぐ)

- D1 rules-gate: `node scripts/verify_tbl.js` (quads 95,670 / triples 195,044 / mismatches 0)。
- D2 val-gate fresh 4 (2M/2M/15M/15M): `node scripts/jsreplay.js --exact-replay=val-gate/<k>.input.csv --exact-replay-budget=<budget>` → `.dh-host.out` (baseline node-exact期待)。
- D3 negatives ng1/ng2 (期待fail-closed)・D4 anchors k02a/l1a (`run_thirdimpl.sh` a/b・exp 9,106,337 / 7,660,202・ttHits 4,991,527 / 3,951,175 pin一致期待)。
- D5 replica 18 pass (9キー×p1/p2・**1 call 1 pass**・`run_replica_dh.sh <key> <pass>`・per-key budget 15M×5 / 25M×3 / 30M×1・inner timeout 260/288/295) → audit G2b p1==p2 + published raw node-exact。
- D6 thirdimpl 18 run (9キー×a/b・wallcap240・est pass-one最大 aa050 ~30M・runlimit時はWALL-INCONCLUSIVEとしてhonest記録しverdictとはしない)。
- D7 audit `audit_dh.py` ×3 (stdout byte-identical + summary・全gate PASS必須)。FAIL→成果FAILとして記録・出版 (押し通さない)。
- D8 tamper battery (4種: replica nodes+1 → verdict-vs-published / target result反転 → det-pair or verdict-agree / anchor expansions改竄 → anchor gate / rows.json改竄 → gate発火・全部捕捉+byte-exact復元+復帰green)。
- D9 出版: B outputs (進捗に応じて分割出版可・環境reset対策で早期出版を優先) → C README最終+MANIFEST-sha256 → 完了log → queue registry bookkeeping は**実行時点の最新registry状態**に基づく (rev5 `4734f13f…` published `5b9c6231` 時点で P4 9行 open・DH完了なら done_win 37→46・open_win 9→0・packages.P4 done・thirdimpl_publications.DH追記・rev6として出版・競合時は見送り記録して次回へ)。

## 停止条件 (原宣言・第1次takeover宣言と同一)

- いずれかのgateで FAIL/MISMATCH → 実行停止・誠実記録・verdict不消費。
- 第三実装verdictがpublished WIN (rc=1) と一致しない場合 → 採用も被覆も一切行わず divergence証拠として記録。
- 実験中の環境reset等 → published scaffoldからkit復元・sha検証の上やり直し (published evidenceだけが証拠)。
- push競合・同時書き込み・取得失敗 → 無理に押し進めず記録して次回実行に回す。
- **verdicts不消費**: 対象9行 (aa011/aa054/aa022/aa034/aa037/aa032/aa028/aa021/aa050) は unadopted honest WIN labels のまま。adoptionは scrutiny owner C++第二実装 gate `9193f5b6…` 通過後・pinned merger `90711961…` 経由の別adoption Part 専権。
- **標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2 {59,60}・class 5343 (全54キー) は本Partの前後を通じてすべてUNKNOWNのまま。** nodes数・expansions数・ttHits数を勝敗や距離として読まない。

## observed

- HEAD-before-push (本宣言出版時): `8a29c987` (2026-11-24T12:44:51Z)。
- 対象9行 (per-key decisive budgets・原宣言表と同一): aa011 15M 12,424,953 / aa054 15M 13,227,570 / aa022 15M 14,044,375 / aa034 15M 14,097,048 / aa037 15M 14,239,714 / aa032 25M 20,312,294 / aa028 25M 21,563,925 / aa021 25M 22,942,323 / aa050 30M 25,541,199 (pinned合計 158,393,401)。
