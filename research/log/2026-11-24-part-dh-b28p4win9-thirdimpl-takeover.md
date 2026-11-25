# Part DH takeover宣言: b28 P4パッケージ9行 第三実装交叉検証 (原宣言 f63c1654 の停滞解除)

- 出版時刻: 2026-11-24T09:4xZ (commit timestampはGitHub側・takeover単一オーナー宣言)
- 原宣言: `research/log/2026-11-24-part-dh-b28p4win9-thirdimpl-declaration.md` (出版 `f63c1654`・2026-11-24T06:07:31Z・publish-then-execute)
- 原オーナーの最終出版: `879ae475` (2026-11-24T06:32:38Z・env outage記録「出版 (宣言 f63c1654/A1 f8db8d87/A2a de650462/A2b 871af8cf・fetch-back byte検証済み) 後のローカル実行中にsandbox reset」)。以降の停滞 observed。
- earliest_takeover (原宣言06:07:31Z + 3.5h) = **2026-11-24T09:37:31Z**。本takeover宣言は**同時刻経過後**に出版した (Part DFの教訓を適用: 先行出版ではなく経過後出版・したがって時刻逸脱amendment不要)。
- 対抗takeover・原オーナー再開の機械確認: 出版直前に最新main再取得 (`e56c8cce` — のちに本宣言push時に変化があれば再取得)・GitHub commit search `repo:… "Part DH takeover"` total_count **0**・DH実験dirはscaffold 3 commits (`f8db8d87`/`de650462`/`871af8cf`) のまま (outputs未出版・09:14Z時点のpath listで確認) を機械確認済み。

## 実験dir・kit (本takeover laneでの復元・検証)

- `research/experiments/n11-centralreply-closure-b28p4win9-thirdimpl-20261124/` (scaffold 74 files: scripts 7 + input 14 + val-gate 8 + sources 44 + README)。
- kit復元: latest mainから全74ファイルをraw fetch復元し、**各ファイルをその出版commit (A1 `f8db8d87` / A2 `871af8cf`) 指定のraw fetchとbyte比較して全件一致 (mismatch 0)** であることを機械確認 (scaffoldは出版後不変)。
- pin照合: 原宣言のsha等のうち機械照合可能な37 prefix/script pin (raw 16・status logs 4・batch-keys・queue-registry rev3 `334f6209…`・README-queue `4b20c6a0…`・CO/DB出版物6・rows.json `6a0e4012…`・scripts 7) すべて一致 (mismatch 0)。
- rules-gate用 lane-kit (`_class1297036830122704896-lane-kit/inv/jsreplay.js` = pinned `84585617…`) は既定位置に配置済み (Part DF takeover時と同一配置・Knowledge durable領域のため今回の実行環境resetを通じて存続確認済み)。
- honest記録: 本takeover準備中 (09:0x-09:1xZ) に実行環境resetが1回発生し、準備中のローカルkit復元・宣言draftを消失した。published evidenceのみを正本として再復元し、上記の機械検証で再構築した (設計思想どおり・誤出版なし)。

## 実行protocol (原宣言の検証計画 D1-D8を引き継ぐ)

- D1 rules-gate: `node scripts/verify_tbl.js > output/rules-gate.txt 2>&1` (quads 95,670 / triples 195,044 mismatches 0 期待)。
- D2 val-gate fresh 4 (2M/2M/15M/15M): `node scripts/jsreplay.js --exact-replay=val-gate/<k>.input.csv --exact-replay-budget=<budget> > val-gate/<k>.dh-host.out` (baseline node-exact期待)。
- D3 negatives ng1/ng2 (期待fail-closed)・D4 anchors k02a/l1a (`run_thirdimpl.sh` a/b)。
- D5 replica 18 pass (9キー×p1/p2・**1 pass 1 invocation**・per-key budget 15M×5/25M×3/30M×1・`run_replica_dh.sh <key> <pass>`・inner timeout 260/288/295) → audit G2b p1==p2 + published raw node-exact。
- D6 thirdimpl 18 run (9キー×a/b・wallcap240・WALL-INCONCLUSIVE時はhonest記録しverdictとしない)。
- D7 audit `audit_dh.py` ×3 (stdout byte-identical + summary) 全gate PASS 必須。FAIL→成果FAILとして記録・出版 (押し通さない)。
- D8 (executor側補強・原宣言の事前11/11捕捉に加えて host出力への4種tamper battery: replica raw nodes+1 → verdict-vs-published / target result反転 → det-pair or verdict-agree / anchor expansions改竄 → anchor gate / rows.json改竄 → verdict gate・全部捕捉+byte-exact復元+復帰green)。
- D9 出版: B outputs (進捗に応じて分割出版可・環境reset対策で早期出版を優先) → C README最終+MANIFEST → 完了log → queue registry bookkeepingは**実行時点の最新registry状態**に基づく (rev5 `4734f13f…` 時点では P4 9行 open・DH完了なら done_win 37→46・open_win 9→0・packages.P4 done・thirdimpl_publications.DH追記・rev6として出版・競合時は見送り記録して次回へ)。

## 停止条件 (原宣言のstop rulesを引き継ぐ)

- いずれかのgateで FAIL/MISMATCH → 実行停止・誠実記録・verdict不消費。
- 対象9行の第三実装verdictがpublished WIN (rc=1) と一致しない場合 → 採用も被覆も一切行わず divergence証拠として記録。
- 実験中の環境reset等 → published scaffoldからkit復元・sha検証の上やり直し (published evidenceだけが証拠)。
- push競合・同時書き込み・取得失敗 → 無理に押し進めず記録して次回実行に回す。
- **verdicts不消費**: 対象9行は unadopted honest WIN labels のまま。adoptionは scrutiny owner C++第二実装 gate `9193f5b6…` 通過後・pinned merger `90711961…` 経由の別adoption Part 専権。
- **標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2 {59,60}・class 5343 (全54キー) は本Partの前後を通じてすべてUNKNOWNのまま。** nodes数・expansions数・ttHits数を勝敗や距離として読まない。

## observed

- HEAD-before-push (takeover宣言出版時): `e56c8cce` (2026-11-24T09:26:09Z・Part K1286 README repair)。
- 対象9行 (per-key decisive budgets): aa011 15M 12,424,953 / aa054 15M 13,227,570 / aa022 15M 14,044,375 / aa034 15M 14,097,048 / aa037 15M 14,239,714 / aa032 25M 20,312,294 / aa028 25M 21,563,925 / aa021 25M 22,942,323 / aa050 30M 25,541,199 (pinned合計 158,393,401)。
