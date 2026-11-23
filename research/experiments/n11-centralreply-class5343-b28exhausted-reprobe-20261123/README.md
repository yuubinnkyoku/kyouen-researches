# batch-28 (class 5343) EXHAUSTED 11-row higher-budget (20M) reprobe — Part CQ (2026-11-23)

Part CQ (publish-then-execute・単一オーナー・宣言
`research/log/2026-11-23-part-cq-b28exhausted-reprobe20m-declaration.md`).
batch-28 (closure class 5343) の published EXHAUSTED 11行
(aa004/aa005/aa021/aa028/aa030/aa031/aa032/aa035/aa047/aa050/aa053・published full row-audit
`n11-centralreply-closure-class5343-batch28-rowaudit-full-v2` の exhausted_rows と完全一致)
を、**新条件 budget 20,000,000** (published 15M の 1.333...倍) で2-pass fresh-cold再probeする。
**verdict不消費** (WIN/LOSSのprobe行はhonest labelのまま・canonical adoptionは別adoption Part
(pinned fail-closed merger `90711961…`) 経由のみ・WIN行はさらに scrutiny owner C++第二実装
gate `9193f5b6…` 待ち)。**published 15M条件の同一条件再probeは行わない**
(COMPLETED exhaustion行のno-15M-re-search規約は無傷・本Partは別宣言条件の高budgetのみ)。
閉鎖・被覆・secured・root勝敗の主張はしない。結果0 (20M枯渇) は引き続きhonest UNKNOWN
(same-condition再probeなし)。

## kit

- scripts byte-pins:
  - jsreplay.js `845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df`
    (published batch-28 kernel byte-clone・変更なし)
  - runbatch.sh `f591f8c2b67326e53873f8ea70f8d04d18423e7c8ef8359838cbafe8264f3b84`
    (published Part CN runner byte-clone・参照用・本Partでは実行に使わない)
  - **runbatch_b28exh20m.sh** `c5e86d49bc851f7e511e811bef5052d4634adfbbdf85a1224d101638db284a90`
    (**published runnerの最小派生・`diff` は EXACTLY 1行**: `BUDGET=15000000` →
    `BUDGET=20000000` のみ・他の全行byte-identical・stop rules/完整性guard/p2-pass設計すべて不変)
  - make_reprobe_keys.py `70737ce34bcb362c950fdd8501f5cac15882ecb106986c85242ee29aa08aa60f` (fail-closed maker・ solver非実行・鍵選定なし:
    鍵集合はpublished row-auditのexhausted_rowsのpinそのまま)
  - cq_local_step.sh `7eda7b0ac3f9e1935647207dd921bff715d90a9732ee4ccc1d6dd9fb13ba3732` (session-local orchestration・single worker 1 invocation
    1キー進行・timeout 260 inner / 外側295s・WIN-CONTINUE事前登録・`if rem`空キーガード
    (Part CN教訓)・事前登録WINDOW-EXCEEDED規則: 同一passのTRUNCATED-RETRYが2回でskipし
    honest unresolvedとして監査に記録)
  - audit_cq.py `2ba15fec0dac962fc7080235a37724c84cb8ef2d65139149092022f9c59ec637` (fail-closed row/anchor/val-gate/rules audit・
    schema `n11-centralreply-c5343-b28exh-reprobe20m-audit-v1`)
- input: 13 CSV (11 targets + 2 anchors aa036/aa046) はpublished batch-28 packetの
  byte-clone (shaはpublished CN MANIFEST-sha256.txtと一致・maker G3/G4ゲート込み)・
  batch-keys-b28.json `af19208f…` (published byte-clone)・
  reprobe-keys.json `e8961c7e…` (maker生成のreprobe registry・budget 20000000・
  published_15m事実とbase-cache不在検証 (0/11 hits vs CO merged 6,301行 `854800f3…`) を記録)
- sources: b28-aa036/aa046-published15m.p{1,2}.out (anchor基準・published CN MANIFEST
  pinと一致・maker G4で検証)
- val-gate: published 4組 (at2m×2 budget 2,000,000 / 15m×2 budget 15,000,000・
  input CSV + published baselines byte-clone) + 本host fresh `.cq-host.out` 4 (宣言後実行)
- anchors (宣言後にderived runner 20Mで実行): aa036 (published LOSS・nodes 955,659) /
  aa046 (published WIN・nodes 2,185,149) — 解決済み行のhigher-budget flagでの再実行は
  探索決定性上 nodes/resultがpublished値と完全一致しなければならない (budgetは上限のみ。
  20M派生runnerのend-to-end妥当性gateとして事前登録)。
- output: status.log (append-only・runner書込のみ) + raw/ (`aaNNN.p{1,2}.out`・
  truncated sidecar `.truncated.HHMMSS.out`はpublished runner guardがrename) +
  audit.json (audit_cq.py生成)。

## 実行記録 (宣言protocol・逐次)

(宣言出版後に追記)

