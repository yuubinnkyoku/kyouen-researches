# batch-28 (class 5343) last-remaining-EXHAUSTED 1-row (aa050) higher-budget (30M) reprobe — Part CT (2026-11-23)

Part CT (publish-then-execute・単一オーナー・宣言
`research/log/2026-11-23-part-ct-b28aa050-reprobe30m-declaration.md`)。
Part CS (25M再probe・完了log `research/log/2026-11-23-part-cs-b28exhausted-reprobe25m.md`)
により残った batch-28 (closure class 5343) の EXHAUSTED 最終1行
(aa050・published CS audit
`n11-centralreply-c5343-b28exh-reprobe25m-audit-v1` (sha256 `c6622d57…`) の
still_exhausted_rows と完全一致・commit-pinned `37c52cfb` でfetch・maker G8ゲートで機械抽出) を、
**新条件 budget 30,000,000** で2-pass fresh-cold再probeする。
**verdict不消費** (WIN/LOSSのprobe行はhonest labelのまま・canonical adoptionは別adoption Part
(pinned fail-closed merger `90711961…`) 経由のみ・WIN行はさらに scrutiny owner C++第二実装
gate `9193f5b6…` 待ち)。**published 15M条件・published CQ 20M条件・published CS 25M条件の
同一条件再probeは行わない** (COMPLETED exhaustion行のno-same-condition-re-search規約は無傷)。
閉鎖・被覆・secured・root勝敗の主張はしない。結果0 (30M枯渇) はhonest UNKNOWN
(same-condition再probeなし)。

## 30M回収設計 (事前登録)

published 25M pass wall は131s (CS raw実測) のため30M単発pass推定~157sで260s inner window内に
収まるが、**p1+p2 (=~314s) は260s inner windowを超える** (CS完了logのとおり単発invocation設計では
回収不能)。よって**cross-invocation p1/p2 resume** を事前登録する: published runnerの
file-existence + truncated-sidecar guard (Part CSでこのキーaa050自体に実働実証済み) がpass境界を
運び、1-3 invocation/キーで完走する。バックアップ規則 (WINDOW-EXCEEDED・事前登録): 同一passの
TRUNCATED-RETRY 2回でskipしhonest unresolvedとして監査に記録 (silent dropなし)。

## kit

- scripts byte-pins:
  - jsreplay.js `845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df`
    (published batch-28 kernel byte-clone・変更なし)
  - runbatch.sh `f591f8c2b67326e53873f8ea70f8d04d18423e7c8ef8359838cbafe8264f3b84`
    (published Part CN runner byte-clone・参照用・本Partでは実行に使わない)
  - **runbatch_b28aa050-30m.sh** `3b5083b47c043f93bbe01a5f3335baba6be6d1d6929885f4ab5b28b1778cf7b4`
    (**published runnerの最小派生・`diff` は EXACTLY 1行**: `BUDGET=15000000` →
    `BUDGET=30000000` のみ・他の全行byte-identical・stop rules/完全性guard/p2-pass設計すべて不変)
  - make_reprobe_keys_ct.py `5b605215a3714650814198f4eb08e9f2b55e1ac33ec9975f6878557a93a8f7df`
    (fail-closed maker・solver非実行・鍵選定なし: 鍵集合はpublished CS auditの
    still_exhausted_rowsのpinそのまま・G1-G9ゲート・byte-stable 2回一致)
  - ct_local_step.sh `854daf1e5c135e2d4cb37b208c2a99fd159395a5c8cfcd9d051d7ec4bc48560f`
    (session-local orchestration・single worker 1 invocation 1キー進行・timeout 260 inner /
    外側290s・WIN-CONTINUE事前登録・`if rem`空キーガード (Part CN教訓)・事前登録
    WINDOW-EXCEEDED規則: 同一passのTRUNCATED-RETRYが2回でskipしhonest unresolvedとして
    監査に記録・30M exhaustion推定~157s/passで260s inner window継使用・cross-invocation
    p1/p2 resume設計 (published runnerのfile-existence guard) により1-3 invocation/キー)
  - audit_ct.py `a37490940b3255af50831ce651a9df5539952cc8be6e8fc4c672e36b79b94fbf`
    (fail-closed row/anchor/val-gate/rules audit・schema
    `n11-centralreply-c5343-b28aa050-reprobe30m-audit-v1`・published 15M/20M/25M事実ゲート込み)
- input: 3 CSV (1 target aa050 + 2 anchors aa036/aa004) はpublished packetのbyte-clone
  (shaはpublished CN/CQ MANIFESTと一致・maker G3ゲート込み)・batch-keys-b28.json
  `af19208f…` (published byte-clone)・reprobe-keys.json `f0ae762f…` (maker生成の
  reprobe registry・budget 30000000・published 15M/CQ20M/CS25M exhaustion事実 (raw sha込み)
  と base-cache不在検証 (0/1 hits vs Part CO canonical 6,301行 `854800f3…`) を記録)
- sources: exh15m/aa050.p{1,2}.out (published Part CN drive-5 raw 15M exhaustion基準・
  maker G4) + exh20m/aa050.p{1,2}.out (published CQ20M exhaustion基準・maker G5) +
  exh25m/aa050.p{1,2}.out (published CS25M exhaustion基準・maker G6) +
  cq-aa036/aa004-published20m.p{1,2}.out (anchor基準・published CQ rawと一致・maker G7)
- val-gate: published 4組 (at2m×2 budget 2,000,000 / 15m×2 budget 15,000,000・
  input CSV + published baselines byte-clone) + 本host fresh `.ct-host.out` 4 (宣言後実行)
- anchors (宣言後にderived runner 30Mで実行): aa036 (published LOSS・nodes 955,659) /
  aa004 (published CQ WIN・nodes 15,616,012) — 解決済み行のhigher-budget flagでの再実行は
  探索決定性上 nodes/resultがpublished値と完全一致しなければならない (budgetは上限のみ。
  30M派生runnerのend-to-end妥当性gateとして事前登録)。
- output: status.log (append-only・runner書込のみ) + raw/ (`aaNNN.p{1,2}.out`・
  truncated sidecar `.truncated.HHMMSS.out`はpublished runner guardがrename) +
  audit.json (audit_ct.py生成)。

## 実行記録 (宣言protocol・逐次)

(宣言出版後に追記)
