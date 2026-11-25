# batch-33 (closure class 34908) remaining-EXHAUSTED 5行 (af003/af023/af034/af039/af048) higher-budget (30M) reprobe — Part EA (2026-11-25)

Part EA (publish-then-execute・単一オーナー・宣言
`research/log/2026-11-25-part-ea-b33exh5-reprobe30m-declaration.md`)。
batch-33 (closure class 34908) の EXHAUSTED 5行 **af003/af023/af034/af039/af048**
(published batch-33 status.log `1f663fc8…`・Part DS full-batch completion commit
`72877473`・54キー集計 LOSS 45・WIN 4 (af029/af047/af050/af053)・EXHAUSTED 5
(上記5行) のEXHAUSTED行集合は機械抽出で{af003, af023, af034, af039, af048}のみ)
を、**新条件 budget 30,000,000** で2-pass fresh-cold再probeする (Part CT/DI先行例
(batch-28 aa050・batch-31 ad043 30M再probe) の設計をbyte-for-byteで踏襲)。
**verdict不消費** (WIN/LOSSのprobe行はhonest labelのまま・canonical
adoptionは別adoption Part (pinned fail-closed merger `90711961…`) 経由のみ・
WIN行はさらに scrutiny owner C++第二実装 gate `9193f5b6…` 待ち)。
**published 15M条件の同一条件再probeは行わない** (COMPLETED exhaustion行の
no-same-condition-re-search規約は無傷)。閉鎖・被覆・secured・root勝敗の主張は
しない。結果0 (30M枯渇) はhonest UNKNOWN (same-condition再probeなし)。

## 30M回収設計 (事前登録)

published 15M exhaustion pass wall は88-130s (batch-33 raw実測・af003 p1 130s /
p2 88s ほか) のため30M単発pass推定~176-260s。**p1+p2 は単一invocationの260s
inner windowを超える**可能性が高いため**cross-invocation p1/p2 resume**を事前登録:
published runnerのfile-existence + truncated-sidecar guard (Part CS/CT/DIで実働
実証済み) がpass境界を運び、1-3 invocation/キーで完走する (1キー/invocation・
WIN-CONTINUE設計なのでWIN行観測でもorchestrationは継続)。バックアップ規則
(WINDOW-EXCEEDED・事前登録): 同一passのTRUNCATED-RETRY 2回でskipしhonest
unresolvedとして監査に記録 (silent dropなし)。

## kit (byte-pins・全て published bytesから復元)

- scripts byte-pins:
  - `jsreplay.js` `84585617…` (published kernel byte-clone・変更なし)
  - `runbatch.sh` `f591f8c2…` (published runner byte-clone・参照用・本Partでは
    実行に使わない)
  - **`runbatch_afexh5-30m.sh`** `3b5083b4…` (**published runnerのbyte-clone・
    `BUDGET=30000000`版・published Part CT/DI 30M runnerとbyte-identical**)
  - `make_reprobe_keys_ea.py` `97b28dd4…` (fail-closed maker・solver非実行・
    鍵選定なし: 鍵集合はpublished b33 status.logのEXHAUSTED行集合のpin
    そのまま・G1-G7 gates・byte-stable 2回一致・宣言前tamper battery
    4/4 fail-closed)
  - `ea_local_step.sh` `0e210e90…` (published DI `di_local_step.sh`
    `0f935350…` の最小派生: kit-root path・registry/script名・headerのみ変更・
    WIN-CONTINUE・`if rem`空キーガード・WINDOW-EXCEEDED規則・timeout 260
    inner すべて同一)
  - `audit_ea.py` `452cd817…` (fail-closed row/anchor/val-gate/rules audit・
    schema `n11-centralreply-c34908-b33exh5-reprobe30m-audit-v1`)
- input: 7 CSV (5 targets af003/af023/af034/af039/af048 + 2 anchors af001/af029)
  はpublished batch-33 packetのbyte-clone (`1ab3277e…` / `0ba31256…` /
  `a4bff566…` / `e51a3c9d…` / `d619dcd7…` / `b2ef3588…` / `b5500b8d…`)・
  `batch-keys.json` `8a863381…` (published b33 packet byte-clone・budget
  15000000・class_index 34908)・`reprobe-keys.json` `3744b522…` (maker生成の
  reprobe registry・budget 30000000・published 15M exhaustion事実 (raw sha込み)・
  base-cache不在検証 (5 targets 0 hits vs Part DZ merged canonical 6,660行
  `4a30b88d…`) を記録)
- sources: exh15m/{af003,af023,af034,af039,af048}.p{1,2}.out (published b33
  raw 15M exhaustion基準・p1/p2 sha pinsはG4で検証) + anchor-15m/af001.p{1,2}.out
  (`6adb122c…`×2)・af029.p{1,2}.out (`6bd7a2ac…` / `b6abaa63…`) +
  b33-status.log (`1f663fc8…`・published byte-clone・commit `72877473`) +
  canonical-cache-dz-merged-b4loss1-b36loss40-b37loss46-20261125.cache
  (`4a30b88d…`・6,660行・Part DZ outputs byte-clone・commit `01f1fcc9`)
- val-gate: published 4組 (at2m×2 budget 2,000,000 / 15m×2 budget
  15,000,000・input CSV + published baselines byte-clone) + 本host fresh
  `.ea-host.out` 4 (宣言後実行・出版)
- anchors (宣言後にderived runner 30Mで実行): af001 (published LOSS・nodes
  2,952,432・s5 900507) / af029 (published WIN・nodes 4,862,485・s5 900646) —
  解決済み行のhigher-budget flagでの再実行は探索決定性上 nodes/resultが
  published値と完全一致しなければならない (budgetは上限のみ。30M派生runnerの
  end-to-end妥当性gateとして事前登録)。
- output: status.log (append-only・runner書込のみ) + raw/
  (`af*.p{1,2}.out`・truncated sidecar `.truncated.HHMMSS.out`はpublished
  runner guardがrename) + audit.json (audit_ea.py生成)。

## 実行記録 (2026-11-25 UTC・protocol順)

- ① 宣言 push `a280180d` (observed HEAD `04c132fd`) → scaffold A1–A3b
  (59588a30 / 369b8d18 / bd6616c5 / 04c132fd・kit 40ファイル)。
- ② **B1-fix (honest deviation・DU-b先例)**: scaffold fetch-back で
  **commit `bd6616c5` (A3a) の sources/ 15ファイル
  (b33-status.log + exh15m 10 raw + anchor-15m 4 raw) が push 時に
  mojibake 化していたことを検出** (b33-status.log 実測 sha256 `1b5d96a9`
  ≠ pin `1f663fc8`、exh15m/anchor raws 全て pin 不一致)。published
  batch-33 正本 (commit `72877473` 出版物) から 15ファイルを再取得し
  **全て pin と一致 (`1f663fc8` / G4 pins / `6adb122c`×2 /
  `6bd7a2ac` / `b6abaa63`)** を確認のうえ kit 修復 commit `f9420860`
  として B1-fix 出版 (content直渡しpush・fetch-back は API git blob sha1
  15/15 厳密一致で検証)。修復後 kit 上で maker G1–G7 全 PASS・
  reprobe-keys.json 再生成 `3744b522` byte-identical・maker tamper
  battery 4/4 fail-closed (T1 status改変 / T2 verdict改変 / T3
  base-cache切詰 / T4 input CSV改変) を再実行。A1/A2/A3b commit
  (scripts 6・input 9・val-gate 8・canonical cache) は初回から全 pin 一致
  (無傷)。
- ③ val-gate fresh 4/4 node-exact (`.ea-host.out`):
  at2m×2 budget 2,000,000 → result 0 nodes 2,000,000 (wall 9/9s)・
  first-15m budget 15,000,000 → result 2 nodes 3,651,923 (17s)・
  second-15m budget 15,000,000 → result 2 nodes 5,040,200 (25s)。
  published baselines と (budget,result,nodes) 完全一致。
- ④ anchors (derived 30M runner・30M budget flagで再実行):
  af001 → result 2 (LOSS) nodes 2,952,432 (**published値と node-exact**・
  2-pass一致・wall 13/13s)・af029 → result 1 (WIN) nodes 4,862,485
  (**published値と node-exact**・PASS + WIN-HALT (runner rc=45 予定通り)・
  wall 23/23s)。30M derived runner end-to-end 妥当性 gate PASS。
- ⑤ targets 5/5 (`ea_local_step.sh` cross-invocation resume・2-pass
  fresh-cold @30M node-exact・MISMATCH 0・WINDOW-EXCEEDED 0):
  af003 (s5 153030) → **result 2 (LOSS) nodes 23,126,072** (126/129s)・
  af023 (s5 810351) → **result 1 (WIN) nodes 28,933,179** (155/157s・
  p1完了後 p2 が260s窓で切れ sidecar `af023.p2.truncated.024331.out`
  + P2-TRUNCATED-RETRY 1回 → 次invocationで完走・resume設計実働)・
  af034 (s5 514726) → **result 0 (EXHAUSTED @30M) nodes 30,000,000**
  (163/165s・p2同様にsidecar `af034.p2.truncated.025034.out` + retry 1回
  → 完走)・af039 (s5 2621520) → **result 2 (LOSS) nodes 19,234,232**
  (105/105s)・af048 (s5 265799) → **result 1 (WIN) nodes 17,816,616**
  (97/89s)。targets 合計 nodes 119,110,099/pass。主要wallの実測から
  当hostの処理速度は ~222k nodes/s (2M val-gate 9s)。
- ⑥ audit (`audit_ea.py`) ×3 byte-identical 全PASS
  (audit.json sha256 `5b83d166e0fb7842a0cad949404c572ba666b71a4cd87dd9e704ce97e543cff3`):
  probed 5/5・win 2・loss 2・exhausted @30M 1・window-exceeded 0・
  unprobed 0・anchors 2・val-gate 4・mismatches 0。audit tamper
  電池 (scratch copy上・本番output非破壊): TA raw nodes改変 (af003
  23,126,072→…073) → GATE FAILED (p1/p2 row mismatch)・TB af023
  WIN-HALT行除去 → GATE FAILED・TD val-gate fresh行改変 → GATE
  FAILED・control 2回 PASS (本番output byte不変 `5b83d166`)。観察記録:
  status.log片側only改変 (raw SSOT無傷) は audit の設計上 raw行が
  SSOTでstatus行は副次的 (corroboration) のため gate対象外。
- ⑦ B outputs push commit `b63569ab` (status.log `db7c7017` 13行 + raw 14 +
  truncated sidecar 2 + `.ea-host.out` 4 + audit.json `5b83d166`)・
  fetch-back API git blob sha1 全22ファイル厳密一致。
- ⑧ 完了log出版 (Part DI完了logと同形式)。

## 結果 (honest label・verdict不消費)

- batch-33 EXHAUSTED 5行 (15M条件) の 30M再probe結果
  (2-pass fresh-cold node-exact・MISMATCH 0・WIN-CONTINUE設計どおり
  WIN観測でも全drive継続):
  - **af003 = LOSS @30M** (nodes 23,126,072) — honest label。adoptionは
    別adoption Part (pinned merger `90711961…`) のみ。
  - **af023 = WIN @30M** (nodes 28,933,179) — honest label・verdict不消費。
    scrutiny owner C++第二実装 gate `9193f5b6…` 待ち。
  - **af034 = EXHAUSTED @30M** (nodes 30,000,000) — 30M条件でも
    honest UNKNOWN (同一条件再probeはしない・さらなる高budgetは別Part)。
  - **af039 = LOSS @30M** (nodes 19,234,232) — honest label。adoptionは
    別adoption Partのみ。
  - **af048 = WIN @30M** (nodes 17,816,616) — honest label・verdict不消費。
    scrutiny owner C++第二実装 gate `9193f5b6…` 待ち。
- anchors: af001 LOSS nodes 2,952,432 / af029 WIN nodes 4,862,485 —
  ともに published 15M値と node-exact (30M budget flagで再実行・search
  determinism確認)。
- batch-33 (class 34908) 54キーの15M-era集計 (LOSS 45・WIN 4・EXH 5) に対する
  本30M再probeの変化: EXH 5行のうち**2行がLOSS honest label・2行がWIN
  honest label・1行 (af034) が30M条件でもEXHAUSTED (honest UNKNOWN)**。
  ただしこの集計はbookkeepingであり閉鎖・被覆・secured coverageの主張では
  ない (class 34908 は UNKNOWNのまま・採用は未実施)。

## 結果の解釈 (interpretation guard)

- 本PartのWIN/LOSS/EXHAUSTEDいずれの結果も **probe-level honest label
  のみ**。verdict不消費: canonical adoptionは別宣言のadoption Part (pinned
  fail-closed merger `90711961…`) 経由のみ・WIN行はscrutiny owner C++第二実装
  gate `9193f5b6…` 通過まで採用されない。本Partはいかなるadoptionも行わない。
- 30M EXHAUSTED の場合は当該行は30M条件でもhonest UNKNOWNのまま
  (再びの同一条件再probeはしない・さらなる高budgetは別Partの対象)。
- **標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・
  S2 {59,60}・class 1/2/4・class 34908 (54キーすべて・本実験の結果行を含む)
  はこの時点で UNKNOWN**。nodes数・wall秒数を勝敗や距離として読まない。
