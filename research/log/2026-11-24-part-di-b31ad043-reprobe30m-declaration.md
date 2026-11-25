# Part DI 単一オーナー宣言 (2026-11-24): batch-31 (closure class 5804) last-remaining-EXHAUSTED 1行 (ad043) higher-budget (30M) reprobe — publish-then-execute・verdict不消費・11×11 UNKNOWN担保不変

Part CT先行例 (batch-28 aa050 30M再probe・
`research/experiments/n11-centralreply-class5343-b28aa050-reprobe30m-20261123/`・
完了log `research/log/2026-11-23-part-ct-b28aa050-reprobe30m.md` 系の流れ) の設計を
byte-for-byteで踏襲する。実験dir:
`research/experiments/n11-centralreply-closure-class5804-b31ad043-reprobe30m-20261124/`。

## 対象の機械抽出 (prose不使用)

- 対象キー: **ad043** (s5 212115・lo 6052837899185946628・hi 128・legal 87・
  membership 4)。published batch-31 status.log **sha256 `c69c2fec…`** (59行・
  Part CY drive-2 takeover C commit `70d79714` で出版) の EXHAUSTED 行集合は
  {ad043} のみ (機械抽出・maker G5 gateで不明瞭さ排除)。batch-31 (class 5804)
  55キー集計: LOSS 51・WIN 3 (ad024/ad028/ad055)・EXHAUSTED 1 (ad043)。
- **published 15M条件の同一条件再probeは行わない** (COMPLETED exhaustion行の
  no-same-condition-re-search規約は無傷)。本Partは**新条件 budget 30,000,000**
  の1キーprobeのみ。結果0 (30M枯渇) は再びhonest UNKNOWN。
- base-cache不在検証 (機械済み): Part DB merged canonical **6,354行
  (`04b0a239…`・現canonical chain head・Part DH A2bで出版済みsource) に
  target (lo,hi) の行は0/1 hits = 不在**。batch-31行は pre-adoption。

## 30M回収設計 (事前登録・CTと同一)

published 15M exhaustion pass wall は108s (batch-31 raw実測・nodes 15,000,000)
のため 30M 単発pass推定 ~216s で260s inner window内に収まるが、**p1+p2 (=~432s)
は260s inner windowを超える**。よって**cross-invocation p1/p2 resume** を事前登録:
published runnerの file-existence + truncated-sidecar guard がpass境界を運び、
1-3 invocation/キーで完走する (Part CS/CTで実働実証済み)。バックアップ規則
(WINDOW-EXCEEDED・事前登録): 同一passの TRUNCATED-RETRY 2回でskipし
honest unresolvedとして監査に記録 (silent dropなし)。

## kit (byte-pins・全て published bytesから復元)

- `scripts/jsreplay.js` `84585617…` (published kernel byte-clone・変更なし)
- `scripts/runbatch.sh` `f591f8c2…` (published runner byte-clone・参照用)
- **`scripts/runbatch_b31ad043-30m.sh` `3b5083b4…`** (published runnerの
  最小派生・diff EXACTLY 1行: `BUDGET=15000000` → `BUDGET=30000000` のみ。
  **byte-identical to the published Part CT 30M runner** `3b5083b4…`)
- `scripts/make_reprobe_keys_di.py` `1ffd2554…` (fail-closed maker・solver非実行・
  鍵選定なし: targetはpublished b31 status.logのEXHAUSTED行集合のpinそのまま・
  G1-G7 gates・byte-stable 2回一致)
- `scripts/di_local_step.sh` `0f935350…` (published CT `ct_local_step.sh`
  `854daf1e…` の最小派生: kit-root path・script名・headerのみ変更・
  orchestration論理同一)
- `scripts/audit_di.py` `72fc4dda…` (fail-closed row/anchor/val-gate/rules
  audit・schema `n11-centralreply-c5804-b31ad043-reprobe30m-audit-v1`)
- `input/`: ad043/ad054/ad055.input.csv = published batch-31 packet byte-clone
  (`fda5d01d…` / `9bf500fb…` / `cad75b29…`)・`batch-keys.json` =
  published b31 packet byte-clone (`d058fddc…`・budget 15000000・
  class_index 5804)・`reprobe-keys.json` `6fbf61eb…` (maker生成・
  budget 30000000・published 15M exhaustion事実 (raw sha込み)・base-cache
  不在検証込み)
- `sources/`: exh15m/ad043.p{1,2}.out (published b31 drive-2 raw・
  `5f3bf5bc…`/`1feacf0c…`) + anchor-15m/ad054.p{1,2}.out・ad055.p{1,2}.out
  (published b31 raw・`c2d1500b…`/`61704c55…`) + b31-status.log
  (`c69c2fec…`・published byte-clone) + canonical-cache-db-merged-b29loss37.cache
  (`04b0a239…`・6,354行・Part DH A2b source byte-clone)
- `val-gate/`: published 4組 (at2m×2 budget 2,000,000 / 15m×2 budget
  15,000,000・input CSV + published baselines byte-clone) + 本host fresh
  `.di-host.out` 4 (宣言後実行・出版)

## anchors (宣言後にderived runner 30Mで実行)

ad054 (published LOSS・nodes 1,644,957) / ad055 (published WIN・nodes 3,364,655)
— 解決済み行のhigher-budget flagでの再実行は探索決定性上 nodes/resultが
published値と完全一致しなければならない (budgetは上限のみ。30M派生runnerの
end-to-end妥当性gateとして事前登録)。

## 宣言前事前実行 (makerのみ・solver実行なし)

- maker byte-stable ×2 (`6fbf61eb…` 一致)。
- maker tamper battery 4/4 fail-closed: (T1) b31-status 実測値改変 → G5 sha
  pinで捕捉・(T2) EXHAUSTED→WIN-HALT改変 → G5 sha pinで捕捉・(T3) base-cache
  切り詰め → G6 sha pinで捕捉・(T4) input CSV改変 → G3 sha pinで捕捉。
  clean control byte-identical (`6fbf61eb…`)。
- 誠実記録: 宣言草案段階で pin転記ミス1件 (ad043 input CSV sha) を機械照合で
  捕捉・修正済み (未出版・CT宣言と同種の事前発見)。

## 執行順 (publish-then-execute・protocol遵守)

1. 本宣言 push (observed HEAD 記載・対抗宣言なし機械確認: 直近100 commit
   走査で Part DI / ad043再probe / class 5804継続probeの対抗レーンなし)。
2. A scaffold push (kit 28 files)。fetch-back byte検証。
3. val-gate fresh 4 (`.di-host.out`・published baselinesと node-exact 必須)。
4. anchors: ad054 → ad055 (derived runner・published値と node-exact必須)。
5. target ad043 (`di_local_step.sh`・cross-invocation resume・1-3 invocation)。
6. audit (`audit_di.py`) ×3 byte-identical + tamper電池 4 (p2 nodes+1 /
   WIN→LOSS反転 / replay_done削除 / registry budget 29999999)。
7. B outputs push (status.log + raw + truncated sidecar + `.di-host.out` 4 +
   audit.json)。C README最終 + MANIFEST-sha256。fetch-back byte検証。
8. 完了log (Part CY drive-2 takeover完了logと同形式)。

## verdict不消費・UNKNOWN担保

- WIN/LOSS/EXHAUSTED は honest label (verdict不消費)。canonical adoption は
  pinned fail-closed merger `90711961…` 経由の別adoption Part 専権。WIN行
  scrutiny は C++第二実装 gate `9193f5b6…` 専権。閉鎖・被覆・secured・
  root勝敗の主張はしない。
- **標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・
  S2 {59,60}・class 1/2/4・class 5804 (55キーすべて・ad043の30M再probeの
  結果行を含む) は本Partの実行・出版のどの時点でもUNKNOWNのまま。**
  nodes数・wall秒数を勝敗や距離として読まない。
- 非接触: Part DH (batch-28 P4第三実装・env outage記録 `879ae475` 後の
  再実行待ち・単一オーナーwindow内)・Part CP drive-3 takeover (batch-30
  ac030..ac054・宣言 `3f0aeb55`)・Part DF/DG (batch-28 P2/P3)・K1284 fast lane
  (z1ラダー)・batch-31 reaudit/adoption (merger `90711961…` 別Part専権・
  本Partは代行しない) は対象キー・実験dir完全分離。
