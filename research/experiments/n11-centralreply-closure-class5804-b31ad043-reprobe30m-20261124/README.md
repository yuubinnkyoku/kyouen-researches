# batch-31 (closure class 5804) last-remaining-EXHAUSTED 1-row (ad043) higher-budget (30M) reprobe — Part DI (2026-11-24)

Part DI (publish-then-execute・単一オーナー・宣言
`research/log/2026-11-24-part-di-b31ad043-reprobe30m-declaration.md`)。
batch-31 (closure class 5804) の EXHAUSTED 最終1行 **ad043**
(published batch-31 status.log `c69c2fec…`・Part CY drive-2 takeover C
commit `70d79714`・55キー集計 LOSS 51・WIN 3 (ad024/ad028/ad055)・
EXHAUSTED 1 (ad043) のEXHAUSTED行集合は機械抽出で{ad043}のみ) を、
**新条件 budget 30,000,000** で2-pass fresh-cold再probeする (Part CT先行例
(batch-28 aa050 30M再probe) の設計をbyte-for-byteで踏襲)。
**verdict不消費** (WIN/LOSSのprobe行はhonest labelのまま・canonical
adoptionは別adoption Part (pinned fail-closed merger `90711961…`) 経由のみ・
WIN行はさらに scrutiny owner C++第二実装 gate `9193f5b6…` 待ち)。
**published 15M条件の同一条件再probeは行わない** (COMPLETED exhaustion行の
no-same-condition-re-search規約は無傷)。閉鎖・被覆・secured・root勝敗の主張は
しない。結果0 (30M枯渇) はhonest UNKNOWN (same-condition再probeなし)。

## 30M回収設計 (事前登録)

published 15M exhaustion pass wall は108s (batch-31 raw実測) のため30M単発pass
推定~216sで260s inner window内に収まるが、**p1+p2 (=~432s) は260s inner window
を超える**。よって**cross-invocation p1/p2 resume** を事前登録: published
runnerのfile-existence + truncated-sidecar guard (Part CS/CTで実働実証済み) が
pass境界を運び、1-3 invocation/キーで完走する。バックアップ規則
(WINDOW-EXCEEDED・事前登録): 同一passのTRUNCATED-RETRY 2回でskipしhonest
unresolvedとして監査に記録 (silent dropなし)。

## kit (byte-pins・全て published bytesから復元)

- scripts byte-pins:
  - `jsreplay.js` `84585617…` (published batch-31 kernel byte-clone・変更なし)
  - `runbatch.sh` `f591f8c2…` (published runner byte-clone・参照用・本Partでは
    実行に使わない)
  - **`runbatch_b31ad043-30m.sh`** `3b5083b4…` (**published runnerの最小派生・
    `diff` は EXACTLY 1行**: `BUDGET=15000000` → `BUDGET=30000000` のみ・
    **published Part CT 30M runnerとbyte-identical**)
  - `make_reprobe_keys_di.py` `1ffd2554…` (fail-closed maker・solver非実行・
    鍵選定なし: 鍵集合はpublished b31 status.logのEXHAUSTED行集合のpin
    そのまま・G1-G7 gates・byte-stable 2回一致・宣言前tamper battery
    4/4 fail-closed)
  - `di_local_step.sh` `0f935350…` (published CT `ct_local_step.sh`
    `854daf1e…` の最小派生: kit-root path・script名・headerのみ変更・
    WIN-CONTINUE・`if rem`空キーガード・WINDOW-EXCEEDED規則・timeout 260
    inner / 290 outer すべて同一)
  - `audit_di.py` `72fc4dda…` (fail-closed row/anchor/val-gate/rules audit・
    schema `n11-centralreply-c5804-b31ad043-reprobe30m-audit-v1`)
- input: 3 CSV (1 target ad043 + 2 anchors ad054/ad055) はpublished batch-31
  packetのbyte-clone (`fda5d01d…` / `9bf500fb…` / `cad75b29…`)・
  `batch-keys.json` `d058fddc…` (published b31 packet byte-clone・budget
  15000000・class_index 5804)・`reprobe-keys.json` `6fbf61eb…` (maker生成の
  reprobe registry・budget 30000000・published 15M exhaustion事実 (raw sha込み)・
  base-cache不在検証 (0/1 hits vs Part DB canonical 6,354行 `04b0a239…`) を記録)
- sources: exh15m/ad043.p{1,2}.out (published b31 drive-2 raw 15M exhaustion
  基準・`5f3bf5bc…`/`1feacf0c…`) + anchor-15m/ad054.p{1,2}.out・ad055.p{1,2}.out
  (published b31 raw・`c2d1500b…`/`61704c55…`) + b31-status.log (`c69c2fec…`・
  published byte-clone) + canonical-cache-db-merged-b29loss37.cache (`04b0a239…`
  ・6,354行・Part DH A2b source byte-clone)
- val-gate: published 4組 (at2m×2 budget 2,000,000 / 15m×2 budget
  15,000,000・input CSV + published baselines byte-clone) + 本host fresh
  `.di-host.out` 4 (宣言後実行・出版)
- anchors (宣言後にderived runner 30Mで実行): ad054 (published LOSS・nodes
  1,644,957) / ad055 (published WIN・nodes 3,364,655) — 解決済み行の
  higher-budget flagでの再実行は探索決定性上 nodes/resultがpublished値と
  完全一致しなければならない (budgetは上限のみ。30M派生runnerのend-to-end
  妥当性gateとして事前登録)。
- output: status.log (append-only・runner書込のみ) + raw/
  (`ad043.p{1,2}.out`・truncated sidecar `.truncated.HHMMSS.out`はpublished
  runner guardがrename) + audit.json (audit_di.py生成)。

## 実行記録 (2026-11-24 UTC・protocol順)

- 宣言: commit `b3f068ab` (observed HEAD `7abca71f`・対抗宣言なし直近100コミット
  機械走査)・fetch-back byte-identical検証済み。
- A scaffold: commit `a5e32648` (observed HEAD `c9e534f4`) — kit 28 files・
  fetch-back 28/28 blob sha一致 (cache 262,326Bはpush前chunked-read再構成の
  byte-identical検証後、remote blob sha一致)。
- val-gate fresh 4 (07:10-07:12Z): **4/4 NODE-EXACT vs published baselines**
  (budget/result/nodes/legal/lo/hi全一致・wall_sは許容差分) — at2m×2
  (result 0・nodes 2,000,000)・first-15m (result 2・nodes 3,651,923)・
  second-15m (result 2・nodes 5,040,200)。quads header (95670) と
  `# replay_done` は4文件すべてに存在。
- anchors (derived 30M runner `runbatch_b31ad043-30m.sh`): ad054 PASS
  result 2 (LOSS)・nodes **1,644,957** (published 15M値とnodes完全一致・p1==p2)・
  ad055 PASS result 1 (WIN)・nodes **3,364,655** (同・p1==p2・WIN-HALT rc=45は
  事前登録どおり runnerの正常終了)。30M派生runnerのend-to-end妥当性gate PASS。
- target ad043 (`di_local_step.sh` invocation 1・07:14-07:16Z): 2-pass fresh-cold
  budget 30,000,000 完走 — **PASS result 1 (WIN)・nodes 18,247,029**・
  wall ~102s/pass (p1==p2 node-exact・本hostではp1+p2が単一invocationの260s
  inner windowに収まった・truncated sidecarなし・cross-invocation resume設計は
  不用起動に終わった)。invocation 2: remaining=0 ALL-DONE。
- audit ×3 byte-identical (audit.json sha `8415f48a…`) PASS: probed 1/1・win 1・
  loss 0・exhausted @30M 0・window-exceeded 0・unprobed 0・anchors 2・val-gate 4。
- tamper電池 4/4 fail-closed (kit全体のscratch copy上で実行・本番output非破壊):
  T1 p2 nodes +1 → p1/p2 row mismatch捕捉・T2 p1 WIN→LOSS反転 → 同捕捉・
  T3 replay_done削除 → truncated fragment捕捉・T4 registry budget 29999999 →
  A registry gate捕捉。clean control rc=0 (audit.json sha同一)・restore後再確認も同一。
- B outputs: commit `487eacd3` (observed HEAD `a5e32648`) — files **12**
  (status.log 1 + raw 6 + audit.json 1 + val-gate `.di-host.out` 4)。
  **コミットメッセージの「11 files」は誤記 (実際は12 files)** — fetch-back
  12/12 blob sha一致で件数・内容とも検証済み (Part CY B3計数誤記と同種の
  誠実訂正記録)。
- C: 本README実行記録追記 + MANIFEST-sha256 (40 entries・path-sorted)。
  fetch-back検証は完了logに記載。

## 結果 (honest label・verdict不消費)

- **ad043: budget 30,000,000で result 1 (WIN) が2-pass fresh-cold一致**
  (nodes 18,247,029 < 30,000,000・p1==p2 node-exact・fresh-cold・決定的探索)。
  published 15M条件 (nodes 15,000,000 exhaustion) に対する**新条件30Mでの
  解決**であり、同一条件再probeは一度も行っていない。
- これによりbatch-31 (closure class 5804) 55キーのprobe-level honest label
  集計は **LOSS 51・WIN 4 (ad024/ad028/ad043/ad055)・EXHAUSTED 0** となった
  (55/55キーがhonest labelを持つ状態に初到達)。
- **verdict不消費**: 本PartのWIN/LOSSはprobe-level honest labelのみ。canonical
  adoption は pinned fail-closed merger `90711961…` 経由の別adoption Part専権
  (ad043の30M行もbatch-31 55行と同様にadoption候補としてmergerに渡るのみ)。
  WIN行はscrutiny owner C++第二実装 gate `9193f5b6…` 待ち。
- nodes数 (18,247,029) は探索打刻であり距離でも証明サイズでもない。
- **標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・
  S2 {59,60}・class 1/2/4・class 5804 (55キーすべて・ad043の30M WIN labelを
  含む) はこの時点で UNKNOWN のまま。**

## 結果の解釈 (interpretation guard)

- ad043の結果 (WIN/LOSS/EXHAUSTEDいずれも) は **probe-level honest label
  のみ**。verdict不消費: canonical adoptionは別宣言のadoption Part (pinned
  fail-closed merger `90711961…`) 経由のみ・WIN行はscrutiny owner C++第二実装
  gate `9193f5b6…` 通過まで採用されない。本Partはいかなるadoptionも行わない。
- 30M EXHAUSTED の場合は ad043 は30M条件でもhonest UNKNOWNのまま
  (再びの同一条件再probeはしない・さらなる高budgetは別Partの対象)。
- **標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・
  S2 {59,60}・class 1/2/4・class 5804 (55キーすべて・本実験の結果行を含む)
  はこの時点で UNKNOWN**。nodes数・wall秒数を勝敗や距離として読まない。
