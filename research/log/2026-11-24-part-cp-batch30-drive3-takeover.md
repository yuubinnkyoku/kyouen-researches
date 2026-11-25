# Part CP batch-30 (closure class 34269) drive-3 takeover宣言 — 単一オーナーtakeover (publish-then-execute)

原宣言 `6edbcf58` (2026-11-24T02:27:43Z・Part CP batch-30 drive-3・残25キー
ac030..ac054・2-pass fresh-cold budget 15M・WIN-CONTINUE) を、原オーナー停滞を
機械確認した上で本takeover宣言で継承する。**verdict不消費**。閉鎖・被覆・
secured・root勝敗の主張はしない。**標準11×11は本driveのどの時点でもUNKNOWNのまま**。

## takeover事由の機械確認 (2026-11-24T06:47Z時点)

- 原宣言: `6edbcf58` 2026-11-24T02:27:43Z (declarationノート出版・事前登録完了)。
- 原オーナーの最後の活動: scaffold A′ `cca29581` 2026-11-24T02:29:06Z
  (session script v3 `41c5719c…` 出版 + drive-3 host val-gate sidecar `.d3t-host.out` 4)。
- 以降、実験dir (research/experiments/n11-centralreply-closure-class34269-batch30-20261123/)
  へのcommitはゼロ (list_commits path filter で機械確認・最終touchは02:29:06Z)。
  status.logは出版済み44行のまま・ac030..ac054はfileless UNPROBEDのまま。
- 停滞 02:29:06Z → 06:47Z = 4時間18分 > takeover規約3.5h。
  earliest_takeover = 02:27:43Z + 3.5h = 05:57:43Z を47分超過。
- 対抗takeover宣言なし (research/log の02:29Z以降43 commitを機械走査・CP/batch30/drive3/ac0NN 関連0件)。
- observed HEAD-before-push: `4948f19a` (2026-11-24T06:44:53Z・K1283探査追録・非接触)。

## 継承kit (fetch-back sha256照合済み・本takeover host)

- scripts/runbatch.sh `f591f8c2b67326e53873f8ea70f8d04d18423e7c8ef8359838cbafe8264f3b84` (pinned runner byte-clone)
- scripts/jsreplay.js `845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df`
- scripts/drive3_local_step.sh `41c5719c8253a9e199786e5fd87e70cc71ba85e22b3b80249df2082964a2f6c1` (= v3宣言pinと完全一致・flock/orphan-liveness/incident-aware 3点deltaを含む)
- input/batch-keys.json `79fbd1664f4ad66ea62d9c8a8aa5aaff5d16bcdaa397895119ce4d8f47961232`
- input/ac030..ac054.input.csv 25 file 全て MANIFEST-sha256 (MANIFEST自体 `2b36d896…` pin一致) と一致
- output/status.log `07d839ab…` 44行 (drive-1 9 + drive-2 35・append-only base) をbaseとして複製して使用

実行はv3 session scriptそのまま (事前登録stop rules: WIN rc=45・MISMATCH rc=42・
p1/p2 fail 43/44・LOCK-BUSY rc=46・ORPHAN rc=47)。**「1 bash invocation = 1 wave」厳守**
(2キー x 2 worker・timeout 260内側wrap)。ac028/ac029は原宣言どおり出版済み
incident-area pairをそのまま採用し再probeしない。EXHAUSTED (result 0) は
honest UNKNOWNとして継続。

## takeover host val-gate (宣言後fresh実行)

- published baselines 4 (at2m x2・first-15m・second-15m) に対し本takeover host
  fresh 4走 (.d3u-host.out x4) を実行し node-exact (4/4) を出発点とする
  (drive-1/2/takeover規約と同一)。不一致ならhard-stop。

## 出版計画 (takeover分)

1. A: takeover host val-gate sidecar 4 (.d3u-host.out)。
2. B checkpoints: waves完了分のraw p1/p2 + status.log (append-only) を
   2-3 checkpointに分割出版。
3. C: README drive-3節追記 + MANIFEST-sha256拡張。
4. 完了log: research/log/2026-11-24-part-cp-batch30-drive3.md (原宣言分とtakeover分を併記)。

## UNKNOWN担保 (不変)

標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2 {59,60}・
class 1/2/4・class 10968・class 23964・class 5343・class 2251・**class 34269
(54キーすべて・EXHAUSTED行・incident-areaキー ac028/ac029・本takeoverで新たに
probeされるac030..ac054を含む)**・class 5804・class 34948 は本driveの実行・出版の
どの時点でもUNKNOWNのまま。nodes数・wall秒数を勝敗として読まない。
被覆・secured・root勝敗の主張をしない。WIN/LOSS採用はscrutiny owner C++
gate `9193f5b6…` 通過後の別adoption Part (pinned merger `90711961…` 経由) のみで、
本takeoverレーンは代行しない。
