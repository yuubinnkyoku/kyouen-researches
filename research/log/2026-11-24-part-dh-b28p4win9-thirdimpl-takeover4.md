# Part DH takeover-4 宣言: b28 P4パッケージ9行第三実装交叉検証 (takeover-3 lane停滞の継承)

- 出版: 2026-11-24T22:55Z台 (takeover単一オーナー宣言・4代目takeover・publish-then-execute)
- 原宣言: `research/log/2026-11-24-part-dh-b28p4win9-thirdimpl-declaration.md` (`f63c1654`・2026-11-24T06:07:31Z)
- 第1次takeover: `2026-11-24-part-dh-b28p4win9-thirdimpl-takeover.md` (`a4e00aa3`・09:40:53Z・D5開始時outage中断・interim `076e05c1`)
- 第2次takeover: `...takeover2.md` (`8699b203`・13:22:07Z・B wave1 `68483d7d` 13:26:22Z = D1-D4 outputs: rules-gate quads 95,670/mismatches 0・val-gate fresh 4/4 node-exact・negatives fail-closed・anchors k02a/l1a exp/ttH pin一致)
- 第3次takeover: `...takeover3.md` (`a67a12f5`・17:14:55Z)
- 第3次takeover laneの停滞: `a67a12f5` (17:14:55Z) を最初で最後の出版とし、
  それ以降のDH出版物ゼロ (kit復元・D1-D8 fresh再実行はいずれも未出版・
  本宣言時点で5時間41分超)。takeover-3宣言自体は「D1-D8を本hostですべて
  fresh再実行し成果物を出版する」方針 (takeover-2が第1次takeoverの未出版
  D1-D4に対したのと同一方針) を宣言済みであり、停滞中に実行が再開した
  形跡はない (下記機械確認)。
- earliest_takeover: 現owner laneの最終出版 17:14:55Z + 3.5h =
  **20:44:55Z経過後**に本宣言を出版した (anchorは最終出版時刻・時刻逸脱なし)。

## 競合・停滞の機械確認 (本宣言出版直前)

- 最新main再取得: HEAD `635488d0` (2026-11-24T22:35:55Z・K1308 cleanup・非接触)。
- GitHub commit search「Part DH」(committer-date降順): 最新 = `a67a12f5`
  (17:14:55Z)。以降のDH関連commit 0件。
- DH実験dir `research/experiments/n11-centralreply-closure-b28p4win9-thirdimpl-20261124`
  へのcommit: 最終 = `68483d7d` (13:26:22Z・takeover-2 B wave1)。以降0件。
- `research/log` の17:14:55Z以降のcommit走査: DH関連 (takeover-3宣言以降の
  宣言・amendment・interim・完了) 0件 (DW/DV/DU-b/K130x/DK等は全て直交レーン)。
- 対抗takeover-4・第3次lane再開なし。出版後に観測した対抗があればamendmentで誠実対処
  (hourly並走注意)。

## 継承の範囲と本laneの方針

- protocol (D1-D9) は原宣言・takeover-2・takeover-3から**変更なし**で引き継ぐ。
- 本laneは D1-D8 を本hostですべて fresh 再実行し成果物を出版する
  (自己完結のevidence chain)。D1-D4 fresh値とtakeover-2 published値
  (`68483d7d`) の交差照合 (rules-gate byte-identical想定・negatives文言一致想定・
  anchors exp/ttH exact想定 (wall_sのみ差)・val-gate node-exact想定 (wall_sのみ差))
  を実行記録に含める。
- val-gate host sidecarは audit pin suffix `.dh-host.out` で本host fresh走行により
  再生成・出版する。takeover-2 host sidecarの出版bytesはcommit `68483d7d` の
  git historyに保存され、本lane走行値とnon-wall全field一致を交差照合後に上書きする
  (honest記録)。
- 本host 2並列上限 (2 core)。長時間計算 (D5/D6) は1 call 1 pass (または
  1 call 1 key区切り) で進め、増分出版を優先する (環境reset対策)。

## kit復元 (published evidenceのみを正本として再構築・本lane)

- 実験dir 74ファイルをcommit指定raw fetchで復元: A1 `f8db8d87` (scripts 7 +
  input 14 + val-gate 8 + README) / A2a `de650462` (sources 38) / A2b `871af8cf`
  (CO/DB cache 2 + increment 2 + manifest 2)。takeover-3宣言のpin表
  (scripts 7: `8036d0e5`/`88e25e0e`/`4dae72ac`/`a0b77d83`/`08ea958f`/`c8c52528`/`84585617`・
  rows.json `6a0e4012`・raw 18 (aa034/aa050はp1==p2)・status 4種・
  batch-keys `af19208f`・queue-registry rev3 `334f6209`・CO cache `854800f3`等・
  DB cache `04b0a239`等) と全ファイルsha照合 (mismatch 0を確認してから実行する)。
- B wave1 (`68483d7d`: rules-gate.txt・status.log・anchors/・negative/・val-gate 4
  `.dh-host.out`) も取得して交差照合基準とする。

## 実行protocol (原宣言D1-D8・takeover-3と同一)

- D1 rules-gate: `node scripts/verify_tbl.js` (quads 95,670 / triples 195,044 /
  mismatches 0 → `output/rules-gate.txt`)。
- D2 val-gate fresh 4 (2M/2M/15M/15M): `node scripts/jsreplay.js
  --exact-replay=val-gate/<k>.input.csv --exact-replay-budget=<budget>` →
  `.dh-host.out` (baseline node-exact期待)。
- D3 negatives ng1/ng2 (期待fail-closed)・D4 anchors k02a/l1a
  (`run_thirdimpl.sh` a/b・exp 9,106,337 / 7,660,202・ttHits 4,991,527 /
  3,951,175 pin一致期待)。
- D5 replica 18 pass (9キー×p1/p2・**1 call 1 pass**・`run_replica_dh.sh <key> <pass>`・
  per-key budget 15M×5 / 25M×3 / 30M×1・inner timeout 260/288/295)。
  audit G2bで p1==p2 + published raw node-exact。
- D6 thirdimpl 18 run (9キー×a/b・wallcap 240・est pass-one最大 aa050 ~30M・
  runlimit時はWALL-INCONCLUSIVEとしてhonest記録しverdictとはしない)。2並列上限。
- D7 audit `audit_dh.py` ×3 (stdout byte-identical + summary・全gate PASS必須)。
  FAIL→成果FAILとして記録・出版 (押し通さない)。
- D8 tamper battery (4種: replica nodes+1 → verdict-vs-published / target result反転 →
  det-pair or verdict-agree / anchor expansions改竄 → anchor gate /
  rows.json replica_nodes改竄 → verdict-vs-published。全部捕捉 + byte-exact復元 +
  復帰green期待)。
- D9 出版: B outputs (進捗に応じた分割出版可) → C README最終 + MANIFEST-sha256 →
  完了log → queue registry bookkeepingは実行時点の最新registry状態に基づく
  (本宣言時点の想定: rev5 published状態で P4 9行 open・DH完了なら done_win 37→46・
  open_win 9→0・packages.P4 done・thirdimpl_publications.DH追記・rev6として出版・
  競合時は見送り記録して次回へ)。

## 停止条件 (原宣言・takeover-2/3宣言と同一)

- いずれかのgateで FAIL/MISMATCH → 実行停止・誠実記録・verdict不消費。
- 第三実装verdictがpublished WIN (rc=1) と一致しない場合 → 採用も被覆も一切行わず
  divergence証拠として記録。
- 実験中の環境reset等 → published scaffoldからkit復元・sha検証の上やり直し
  (published evidenceだけが証拠)。
- push競合・同時書き込み・取得失敗 → 無理に押し進めず記録して次回実行に回す。
- **verdicts不消費**: 対象9行 (aa011/aa054/aa022/aa034/aa037/aa032/aa028/aa021/aa050)
  は unadopted honest WIN labels のまま。adoptionは scrutiny owner C++第二実装
  gate `9193f5b6…` 通過後・pinned merger `90711961…` 経由の別adoption Part 専権。
- **標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2 {59,60}・
  class 5343 (全54キー) は本Partの前後を通じてすべてUNKNOWNのまま。**
  nodes数・expansions数・ttHits数を勝敗や距離として読まない。
- 非接触: Part DW (b35loss26・完了済み)・Part DK (ac013 25M再probe・完了済み)・
  Part DP canonical chain・ scrutiny owner専権事項・各published dir。

## observed

- HEAD-before-push (本宣言出版時): 直近の機械確認では `635488d0`
  (2026-11-24T22:35:55Z)。push直前に再度最新main取得をして記録する
  (変わっていた場合は本宣言の「観測」行としてamendment対象)。
- 対象9行 (per-key decisive budgets・原宣言表と同一): aa011 15M 12,424,953 /
  aa054 15M 13,227,570 / aa022 15M 14,044,375 / aa034 15M 14,097,048 /
  aa037 15M 14,239,714 / aa032 25M 20,312,294 / aa028 25M 21,563,925 /
  aa021 25M 22,942,323 / aa050 30M 25,541,199 (pinned合計 158,393,401)。
