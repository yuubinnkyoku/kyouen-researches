# Part EA 単一オーナー宣言 (2026-11-25): batch-33 (closure class 34908) remaining-EXHAUSTED 5行 (af003/af023/af034/af039/af048) higher-budget (30M) reprobe — publish-then-execute・verdict不消費・11×11 UNKNOWN担保不変

Part CT/DI 先行例 (batch-28 aa050・batch-31 ad043・
`research/experiments/n11-centralreply-class5343-b28aa050-reprobe30m-20261123/`・
`research/experiments/n11-centralreply-closure-class5804-b31ad043-reprobe30m-20261124/`
完了log群の流れ) の設計を byte-for-byte で踏襲する。実験dir:
`research/experiments/n11-centralreply-closure-class34908-b33exh5-reprobe30m-20261125/`。

## 対象の機械抽出 (prose不使用)

- 対象キー: **af003 / af023 / af034 / af039 / af048** (class 34908 cost
  children 5行)。published batch-33 status.log **sha256
  `1f663fc802c03b27c2e39d6130cf6c1392d62dd99b5847d6af477cd823a94b52`**
  (66行・Part DS full-batch completion commit `72877473` で最終出版) の
  EXHAUSTED 行集合は machine-extract で {af003, af023, af034, af039, af048}
  のみ (G5 gate: EXHAUSTED id set == pinned target set で不明瞭さ排除。
  WIN-HALT 集合 {af029, af047, af050, af053} と PASS 54行も同一pin)。
  batch-33 (class 34908) 54キー集計: LOSS 45・WIN 4 (af029/af047/af050/af053)
  ・EXHAUSTED 5 (対象行・上記5行) — published README (Part DS completion
  `72877473`) の aggregate と一致。
- **published 15M条件の同一条件再probeは行わない** (COMPLETED exhaustion行の
  no-same-condition-re-search規約は無傷)。本Partは**新条件 budget 30,000,000**
  の5キーprobeのみ。結果0 (30M枯渇) は再びhonest UNKNOWN。
- base-cache不在検証 (機械済み): 現canonical chain head = **Part DZ merged
  canonical 6,660行 sha256
  `4a30b88dba782138585f16e1ad0ea65da55431dbc2c59250998fc5a1331349c9`**
  (Part DZ outputs commit `01f1fcc9` 出版・completion log `517db201`) に
  5 target (lo,hi) の行は **0 hits** (EXHAUSTED行はいかなるcanonical cacheにも
  採用されない構造・maker G6 gateで検証)。

## 30M回収設計 (事前登録・CT/DIと同一)

published 15M exhaustion pass wall は 88-130s (batch-33 published raw実測:
af003 p1 130s / p2 88s ほか) のため 30M 単発pass推定 ~176-260s。**p1+p2
は単一invocationの260s inner windowを超える**可能性が高いため
**cross-invocation p1/p2 resume** を事前登録: published runnerの
file-existence + truncated-sidecar guard がpass境界を運び、1-3
invocation/キーで完走する (Part CS/CT/DI で実働実証済み)。バックアップ規則
(WINDOW-EXCEEDED・事前登録・DIと同一文言): 同一passの TRUNCATED-RETRY 2回で
skipし honest unresolved として監査に記録 (silent dropなし)。

## kit (byte-pins・全て published bytesから復元)

- `scripts/jsreplay.js` `845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df`
  (published kernel byte-clone・変更なし)
- `scripts/runbatch.sh` `f591f8c2b67326e53873f8ea70f8d04d18423e7c8ef8359838cbafe8264f3b84`
  (published runner byte-clone・参照用)
- **`scripts/runbatch_afexh5-30m.sh` `3b5083b47c043f93bbe01a5f3335baba6be6d1d6929885f4ab5b28b1778cf7b4`**
  (published runnerの最小派生・diff EXACTLY 1行: `BUDGET=15000000` →
  `BUDGET=30000000` のみ。**byte-identical to the published Part CT/DI 30M
  runner** `3b5083b4…`・本Partは再派生ではなく byte-clone)
- `scripts/make_reprobe_keys_ea.py` `97b28dd447a7c13c90f164c635e9853d0534ded72c4393e00b87b3c7614faa78`
  (fail-closed maker・solver非実行・鍵選定なし: targetはpublished b33
  status.logのEXHAUSTED行集合のpinそのまま・G1-G7 gates・byte-stable)
- `scripts/ea_local_step.sh` `0e210e90ef16a9cdcca1acd96c5f123c0e10e5a57e30988388f5856d7f5430f8`
  (published DI `di_local_step.sh` `0f935350…` の最小派生: kit-root
  path・registry/script名・headerのみ変更・orchestration論理同一)
- `scripts/audit_ea.py` `452cd81736897741d78ddb18348c81cf6cc79fff128ecfda5b3f55daf9942eb0`
  (fail-closed row/anchor/val-gate/rules audit・schema
  `n11-centralreply-c34908-b33exh5-reprobe30m-audit-v1`)
- `input/`: af003/af023/af034/af039/af048/af001/af029.input.csv = published
  batch-33 packet byte-clone (`1ab3277e…` / `0ba31256…` / `a4bff566…` /
  `e51a3c9d…` / `d619dcd7…` / `b2ef3588…` / `b5500b8d…`)・
  `batch-keys.json` = published b33 packet byte-clone (`8a863381…`・budget
  15000000・class_index 34908)・`reprobe-keys.json` `3744b522346b00108f66991cd4009943af84344ab388431652783fbf8227a663`
  (maker生成・budget 30000000・published 15M exhaustion事実 (raw sha込み)・
  base-cache不在検証込み)
- `sources/`: exh15m/{af003,af023,af034,af039,af048}.p{1,2}.out (published
  b33 raw byte-clone・p1/p2 sha pinsはG4で検証) + anchor-15m/af001.p{1,2}.out
  (`6adb122c…`×2)・af029.p{1,2}.out (`6bd7a2ac…` / `b6abaa63…`) + b33-status.log
  (`1f663fc8…`・published byte-clone) + canonical-cache-dz-merged-b4loss1-
  b36loss40-b37loss46-20261125.cache (`4a30b88d…`・6,660行・Part DZ outputs
  byte-clone)
- `val-gate/`: published 4組 (at2m×2 budget 2,000,000 / 15m×2 budget
  15,000,000・input CSV + published baselines byte-clone) + 本host fresh
  `.ea-host.out` 4 (宣言後実行・出版)

## anchors (宣言後にderived runner 30Mで実行)

af001 (published LOSS・nodes 2,952,432・s5 900507) / af029 (published WIN・
nodes 4,862,485・s5 900646) — 解決済み行のhigher-budget flagでの再実行は
探索決定性上 nodes/resultがpublished値と完全一致しなければならない (budgetは
上限のみ。30M派生runnerのend-to-end妥当性gateとして事前登録)。

## 宣言前事前実行 (makerのみ・solver実行なし)

- maker byte-stable ×2 (`3744b522346b00108f66991cd4009943af84344ab388431652783fbf8227a663`
  一致)。
- maker tamper battery 4/4 fail-closed (rc=1): (T1) b33-status 実測値改変
  (af023 EXHAUSTED nodes 14999999) → G5 sha pinで捕捉・(T2) af023
  EXHAUSTED→WIN-HALT/PASS-result-1 改変 → G5 sha pinで捕捉・(T3) base-cache
  切り詰め (先頭100,000バイト) → G6 sha pinで捕捉・(T4) af003 input CSV
  legal改変 (93→94) → G3 sha pinで捕捉。clean control rc=0 byte-identical
  (`3744b522…`)。

## 執行順 (publish-then-execute・protocol遵守)

1. 本宣言 push (observed HEAD 記載・対抗宣言なし機械確認: 直近コミット走査
   で Part EA / b33 EXH reprobe / af003..af048 30M の対抗レーン 0件)。
2. A scaffold push (kit 39 files)。fetch-back byte検証。
3. val-gate fresh 4 (`.ea-host.out`・published baselinesと node-exact 必須)。
4. anchors: af001 → af029 (derived runner・published値と node-exact必須)。
5. targets af003 → af023 → af034 → af039 → af048 (`ea_local_step.sh`・
   cross-invocation resume・1-3 invocation/キー・WIN-CONTINUE設計なので
   WIN行が観測されてもdriveは継続)。
6. audit (`audit_ea.py`) ×3 byte-identical + tamper電池 4 (scratch copy上・
   本番output非破壊)。
7. B outputs push (status.log + raw + truncated sidecar + `.ea-host.out` 4 +
   audit.json)。C README最終 + MANIFEST-sha256。fetch-back byte検証。
8. 完了log (Part DI完了logと同形式)。

## verdict不消費・UNKNOWN担保

- WIN/LOSS/EXHAUSTED は honest label (verdict不消費)。canonical adoption は
  pinned fail-closed merger `90711961…` 経由の別adoption Part 専権。WIN行
  scrutiny は C++第二実装 gate `9193f5b6…` 専権。閉鎖・被覆・secured・
  root勝敗の主張はしない。
- **標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2
  {59,60}・class 1/2/4・class 34908 (54キーすべて・本5行の30M再probeの
  結果行を含む) は本Partの実行・出版のどの時点でもUNKNOWNのまま。**
  nodes数・wall秒数を勝敗や距離として読まない。
- 非接触: Part DZ (b4loss1+b36loss40+b37loss46 87-LOSS adoption・completion
  log `517db201` で完結) は本Part開始前に完走済み・実験dir・対象キー完全
  分離。次期 clean-class probe (batch-38選定) は closure表を採用側で機械
  選定する別レーンの専権で本Partは代行しない。EXHAUSTED行の高budget再probe
  自体は Part DT/DU-b レジームで「別宣言必須」と明示されていた本項の実行
  (対抗宣言は機械走査で 0件確認済み)。
