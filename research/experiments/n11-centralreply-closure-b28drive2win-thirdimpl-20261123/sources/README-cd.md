# batch-28 drive-2 continuation: fileless 52 keys aa003..aa054 (Part CD, 2026-11-23)

Part CD (publish-then-execute・単一オーナー・宣言はnote amendment `0ae99cf0…`)。
batch-28 (class 5343・54キー・Part CB drive-1のWIN-HALT状態: completed WIN行
aa001/aa002 + fileless 52キー aa003..aa054) のpublished kitをbyte-clone継続し、
残り52キーをpinned replicaで2-pass fresh-cold probeする drive-2 waveの実験dir。
**verdict不消費**。閉鎖・被覆・secured・root勝敗の主張はしない。

## kit (published batch-28 kitのbyte-clone・68 filesをpublished MANIFEST pinsと全件byte照合済み)

- scripts byte-pin再利用 (一切変更なし): runbatch.sh `f591f8c2…` (pre-registered
  stop rules: WIN rc=45 / MISMATCH rc=42 / p1/p2 fail rc=43/44・budget 15M・
  TRUNCATED passはevidenceでなくfresh-cold retry・`# replay_done`なしのpassは
  再実行)・jsreplay.js `84585617…`・drive_batch28.sh `08dc059c…`・
  row_audit_batch28.py `656cac31…`・row_audit_batch28_win_halt.py
  `96867282…`・make_batch28_keys.py `d1ffe72f…`・runwave.sh `8efd78c2…`。
- scripts/drive2_local_step.sh: session-local orchestration記録 (pinned kitの
  一部ではない・solver変更なし・実行再現のための補助driver。後述の実行上の
  事情による直接runbatch.sh起動ヘルパー)。
- input 55 files (54 CSV + batch-keys.json `af19208f…`・published pinsそのまま)。
- output seeds: published status.log `e98b5d23…` (drive-1の4行) + published raw
  outs aa001/aa002 (4 files・published pins)。**drive-1のcompleted行 (aa001/aa002)
  は再probeしていない** (残りキー計算はstatus.logから機械導出)。
- val-gate: sanctioned 4キー (at2m×2 budget 2M・15m×2 budget 15M) input CSV +
  published baselines (published pins) + 本host fresh `.cd2-host.out` 4 files。

## 実行記録 (宣言protocol・逐次)

1. val-gate 4/4 本host node-exact (published baseline比較・wall_s比較外)。
2. wave 1 (drive_batch28.sh 1回・16:03:47-16:08:07Z): aa003 PASS (result 2 =
   LOSS行・nodes 4,070,373)・aa004 p1完走 (207s)・aa004 p2/aa005 p1 は260s窓で
   truncated (TRUNCATED-RETRY行はstatus.logどおり)。
3. **実行上の正直な開示 (orchestration偏移)**: aa004 (legal 91・EXHAUSTED
   15,000,000) は1 pass 207sであり、drive_batch28.shのworker当たり`timeout 260`
   窓ではp2が完了できない (完了passは再実行されないが truncated pass は永遠に
   retryになる)。よってdrive_batch28.shの反復を断念し、**pinned runner
  `runbatch.sh` (`f591f8c2…`・変更なし) を「未完キー1個ずつ」`timeout 285`
   で直接起動するsession-local orchestration (scripts/drive2_local_step.sh) に
   切り替えた (2 solver並列上限・odd/even 2 workers相当・runner内部guard・
   stop rule変更なし)。すべてのverdict行はrunner自身の記録。
4. 結果: aa004 EXHAUSTED (honest UNKNOWN)・aa005 EXHAUSTED (同) → **aa006
   WIN-HALT (result 1・nodes 14,303,810)・aa007 WIN-HALT (result 1・nodes
   13,483,540)**。両workerのrc=45観測で事前登録stop ruleによりwave終了。
   残り47キー (aa008..aa054) はfileless UNPROBEDのまま。

## 状態 (row-audit-winhalt・機械導出)

- row-audit(winhalt) PASS: **probed 7 (aa001..aa007) = WIN 4 (aa001, aa002,
  aa006, aa007)・LOSS 1 (aa003)・EXHAUSTED 2 (aa004, aa005)・fragment 0・
  fileless 47・mismatch 0**。truncated sidecar 4 files
  (aa004.p2/aa005.p1/aa006.p2/aa007.p2 `.truncated.*.out`) はevidenceでない
  bookkeepingとしてpublish (runnerがrenameした実行記録・内容いずれも
  `# replay_done`なし)。
- tamper battery 4/4検出 (scratch copy上: T1 aa006 p1 result 1→2 → p1/p2 row
  mismatch gate fail (初回はsed置換不発動の無操作だったため実効性assert込みで
  再実施・T1'としてGATE FAILED確認)・T2 status.log aa006 nodes +1 →
  WIN-HALT record incomplete fail・T3 seed aa001 status nodes +1 → 同fail・
  T4 aa003 raw legal 86→87 → published packet legal不一致fail)・battery後の
  実験dir全file sha256不変を検証。

## 解釈ガード

- nodes数・wall秒数を勝敗として読まない。WIN行 (aa006/aa007を含む) はhonest
  labels only (adoption候補としてmerger `90711961…` 経由の別adoption Partの
  み消費)。LOSS行 (aa003) はadoption候補のみ。EXHAUSTED行はhonest UNKNOWN
  (same-condition再probeなし)。scrutiny owner C++第二実装 gate `9193f5b6` は
  継続。**標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2
  {59,60}・class 1/2/4・class 10968・class 23964・class 5343 (54キーすべて) は
  本実験の前後を通じてUNKNOWNのまま。**
