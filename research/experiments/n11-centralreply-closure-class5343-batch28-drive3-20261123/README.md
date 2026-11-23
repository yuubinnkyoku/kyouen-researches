# batch-28 drive-3 continuation: fileless 47 keys aa008..aa054 (Part CJ, 2026-11-23)

Part CJ (publish-then-execute・単一オーナー・宣言 `research/log/2026-11-23-part-cj-batch28-drive3-declaration.md`・
commit `42cecf36…`)。batch-28 (class 5343・54キー・Part CD drive-2終了時点: completed
aa001..aa007 + fileless 47キー aa008..aa054) のpublished kitをbyte-clone継続し、
残り47キーをpinned replicaで2-pass fresh-cold probeする drive-3 waveの実験dir。
**verdict不消費**。閉鎖・被覆・secured・root勝敗の主張はしない。

## kit (published batch-28 drive-2 dirのbyte-clone・96ファイルをcommit-pinned raw URLで取得しsha256 96/96照合済み)

- scripts byte-pin再利用 (一切変更なし): runbatch.sh `f591f8c2…` (pre-registered
  stop rules: WIN rc=45 / MISMATCH rc=42 / p1/p2 fail rc=43/44・budget 15M・
  TRUNCATED passはevidenceでなくfresh-cold retry・`# replay_done`なしのpassは再実行)・
  jsreplay.js `84585617…`・drive_batch28.sh `08dc059c…`・row_audit_batch28.py
  `656cac31…`・row_audit_batch28_win_halt.py `96867282…`・make_batch28_keys.py
  `d1ffe72f…`・runwave.sh `8efd78c2…`。
- scripts/drive3_local_step.sh: session-local orchestration記録 (pinned kitの一部では
  ない・Part CD drive2_local_step.shと同型の実行tree path差のみ・solver/runner/stop
  rulesはbyte-identical・実行は反復每に未完キー最大2個を `timeout 285` でpinned
  runbatch.shへ直接渡す)。
- input 55 files (54 CSV + batch-keys.json `af19208f…`・published pinsそのまま)。
- output seeds: published drive-2 status.log `343097c2…` (17行) + published raw outs
  aa001..aa007 (18 files・truncated sidecars 4つ含む・published pins)。**drive-1/2の
  completed行 (aa001..aa007) は再probeしていない** (残りキー計算はstatus.logから機械導出)。
- val-gate: published 12 files (sanctioned 4キー: at2m×2 budget 2M・15m×2 budget 15M・
  input CSV + published baselines + Part CD `.cd2-host.out`) + 本host fresh
  `.cj-host.out` 4 files。

## 実行記録 (宣言protocol・逐次)

1. val-gate fresh 4/4 本host node-exact (at2m nodes 2,000,000 ×2 EXHAUSTED・15m行
   result 2 nodes 3,651,923 / 5,040,200・wall_s比較外・禁止四角 95,670・
   `# replay_done` x4)。
2. wave 1 (drive3_local_step.sh 1回・17:35〜17:36Z・2 worker): **aa008 WIN-HALT
   (result 1・nodes 5,270,340・legal 85・2-pass node-exact)・aa009 WIN-HALT
   (result 1・nodes 7,319,605・legal 91・2-pass node-exact)**。両worker rc=45観測で
   事前登録stop rule「本driveで2 WIN行観測でwave halt」(batch-28 drive-1/2と同じ
   設計)によりdrive-3終了。残り45キー (aa010..aa054) はfileless UNPROBEDのまま。

## 状態 (row-audit-winhalt・機械導出)

- row-audit(winhalt) PASS: **probed 9 (aa001..aa009) = WIN 6 (aa001, aa002, aa006,
  aa007, aa008, aa009)・LOSS 1 (aa003)・EXHAUSTED 2 (aa004, aa005)・fragment 0・
  fileless 45・mismatch 0** (pinned `row_audit_batch28_win_halt.py` x3 byte同一・
  row-audit-winhalt.json sha256 `eb1d1e98…`)。truncated sidecar 4 files
  (aa004.p2/aa005.p1/aa006.p2/aa007.p2 `.truncated.*.out`) はPart CDからのseed
  bookkeeping (runnerがrenameした実行記録・内容いずれも `# replay_done`なし)。
- tamper battery 4/4検出 (scratch copy上: T1 aa008 p1 result反転 1→2 → p1/p2 row
  mismatch gate fail・T2 status.log aa008 nodes +1 → WIN-HALT record incomplete
  fail・T3 seed aa003 status nodes +1 → node count mismatch fail・T4 raw aa003
  legal 86→87 (p1/p2両方) → published packet legal不一致fail)。**正直開示: T1の初回
  probeはharness側no-opだった** (sedパターンがval-gate行のlegal 98を流用して
  aa008行 legal 85に不動作・かつ実効性検証が `grep -c` の「0」出力を非emptyと
  誤判定する設計) → 有効性assert (count閾値) と実際のaa008行に合わせたT1'で再実施し
  DETECTED。T2/T3/T4は初回から有効変異でDETECTED。battery後の実験dir全104ファイル
  sha256不変を検証。
- aa008/aa009の意味は **route statementのみ**: unconsumed closure WIN候補34/35番目
  (Part CB/S 19prior + l系 + aa001/aa002/aa006/aa007に続く)。verdict不消費・採用は
  別adoption Part (pinned merger `90711961…`) 経由のみ。

## 解釈ガード

- nodes数・wall秒数を勝敗として読まない。WIN行 (aa008/aa009を含む) はhonest
  labels only (adoption候補としてmerger `90711961…` 経由の別adoption Partのみ消費)。
  LOSS行 (aa003) はadoption候補のみ。EXHAUSTED行はhonest UNKNOWN
  (same-condition再probeなし)。scrutiny owner C++第二実装 gate `9193f5b6` は継続。
  **標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2 {59,60}・
  class 1/2/4・class 10968・class 23964・class 5343 (54キーすべて) は本実験の前後を
  通じてUNKNOWNのまま。** canonical cache (Part CH merged 6,294行 `3124461b…`) への
  書込は一切ない (adoptionは別adoption宣言のみ)。
