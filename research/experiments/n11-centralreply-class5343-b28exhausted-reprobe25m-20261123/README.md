# batch-28 (class 5343) remaining-EXHAUSTED 4-row higher-budget (25M) reprobe — Part CS (2026-11-23)

Part CS (publish-then-execute・単一オーナー・宣言
`research/log/2026-11-23-part-cs-b28exhausted-reprobe25m-declaration.md`)。
Part CQ (20M再probe・完了log `research/log/2026-11-23-part-cq-b28exhausted-reprobe.md`)
後に残った batch-28 (closure class 5343) の EXHAUSTED 4行
(aa021/aa028/aa032/aa050・published CQ audit
`n11-centralreply-c5343-b28exh-reprobe20m-audit-v1` (sha256 `6227eb2c…`) の
still_exhausted_rows と完全一致・commit-pinned 962348f9 で機械抽出) を、
**新条件 budget 25,000,000** で2-pass fresh-cold再probeする。
**verdict不消費** (WIN/LOSSのprobe行はhonest labelのまま・canonical adoptionは別adoption Part
(pinned fail-closed merger `90711961…`) 経由のみ・WIN行はさらに scrutiny owner C++第二実装
gate `9193f5b6…` 待ち)。**published 15M条件・published CQ 20M条件の同一条件再probeは
行わない** (COMPLETED exhaustion行のno-same-condition-re-search規約は無傷)。
閉鎖・被覆・secured・root勝敗の主張はしない。結果0 (25M枯渇) はhonest UNKNOWN
(same-condition再probeなし)。

## kit

- scripts byte-pins:
  - jsreplay.js `845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df`
    (published batch-28 kernel byte-clone・変更なし)
  - runbatch.sh `f591f8c2b67326e53873f8ea70f8d04d18423e7c8ef8359838cbafe8264f3b84`
    (published Part CN runner byte-clone・参照用・本Partでは実行に使わない)
  - **runbatch_b28exh25m.sh** `9048c3291d981d52c846bc177bb727f95827d88892c6fd44ae84c5a110b4ac1c`
    (**published runnerの最小派生・`diff` は EXACTLY 1行**: `BUDGET=15000000` →
    `BUDGET=25000000` のみ・他の全行byte-identical・stop rules/完全性guard/p2-pass設計すべて不変)
  - make_reprobe_keys_cs.py `d769540be0e0e33115aba5493bdb0228f14d8bf0be2009274d219d60f0b6bf88`
    (fail-closed maker・solver非実行・鍵選定なし: 鍵集合はpublished CQ auditの
    still_exhausted_rowsのpinそのまま・G1-G7ゲート・byte-stable 2回一致)
  - cs_local_step.sh `cbab00174d26ab9068b148bd87e3d7d3c9c58fa586968b160a824f507355be65`
    (session-local orchestration・single worker 1 invocation 1キー進行・timeout 260 inner /
    外側295s・WIN-CONTINUE事前登録・`if rem`空キーガード (Part CN教訓)・事前登録
    WINDOW-EXCEEDED規則: 同一passのTRUNCATED-RETRYが2回でskipしhonest unresolvedとして
    監査に記録・25M exhaustion推定~136s/passで260s inner window継使用・p1/p2 resume設計
    (published runnerのfile-existence guard) により1-3 invocation/キー)
  - audit_cs.py `9722ca42e348d1851eef35ac272aa3f4be41b4a506dffe9e082763439e577f9a`
    (fail-closed row/anchor/val-gate/rules audit・schema
    `n11-centralreply-c5343-b28exh-reprobe25m-audit-v1`・published_cq20m事実ゲート込み)
- input: 6 CSV (4 targets + 2 anchors aa036/aa004) はpublished packetのbyte-clone
  (shaはpublished CN MANIFESTと一致・maker G3ゲート込み)・batch-keys-b28.json
  `af19208f…` (published byte-clone)・reprobe-keys.json `21e7a6d9…` (maker生成の
  reprobe registry・budget 25000000・published 15M/CQ20M exhaustion事実と
  base-cache不在検証 (0/4 hits vs Part CO canonical 6,301行 `854800f3…`) を記録)
- sources: cq-aa036/aa004-published20m.p{1,2}.out (anchor基準・published CQ rawと一致・
  maker G5で検証) + exh20m/aaNNN.p{1,2}.out 4キー×2 (targetsのpublished CQ20M exhaustion
  基準・maker G4で検証)
- val-gate: published 4組 (at2m×2 budget 2,000,000 / 15m×2 budget 15,000,000・
  input CSV + published baselines byte-clone) + 本host fresh `.cs-host.out` 4 (宣言後実行)
- anchors (宣言後にderived runner 25Mで実行): aa036 (published LOSS・nodes 955,659) /
  aa004 (published CQ WIN・nodes 15,616,012) — 解決済み行のhigher-budget flagでの再実行は
  探索決定性上 nodes/resultがpublished値と完全一致しなければならない (budgetは上限のみ。
  25M派生runnerのend-to-end妥当性gateとして事前登録)。
- output: status.log (append-only・runner書込のみ) + raw/ (`aaNNN.p{1,2}.out`・
  truncated sidecar `.truncated.HHMMSS.out`はpublished runner guardがrename) +
  audit.json (audit_cs.py生成)。

## 実行記録 (宣言protocol・逐次)

(宣言出版後に追記)
