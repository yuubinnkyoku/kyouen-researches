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

### 宣言後実行 (publish-then-execute・protocol遵守)

1. **A scaffold push**: 34 files (scripts 6 / input 15 / sources 4 / val-gate 8 / README) —
   commit `dd68c4d6` (observed HEAD-before-push `699a13bc` Part CG completion log)。
   fetch-back 34/34 byte-identical (commit-pinned raw URL・sha256照合)。
   前回sessionのscaffold pushは16MiB制約で着地していなかったことをlist_commitsで確認済み
   (HEADがCQ Aを含まず・重複pushなし)。
2. **val-gate fresh 4** (宣言後に本host再実行): at2m×2 budget 2,000,000 → exhaustion
   nodes 2,000,000 (`wall_s=9`), 15m×2 budget 15,000,000 → 3,651,923 (`17`) /
   5,040,200 (`26`)。published baselinesと node-exact (f6 result / f7 nodes 一致・
   f8 wall_s は比較外・事前宣言どおり)。**4/4 PASS**。
3. **anchors** (derived runner `runbatch_b28exh20m.sh` 20M): aa036 → PASS `20000000,2,955659`
   (published とnode-exact)、aa046 → PASS `20000000,1,2185149` + WIN-HALT (rc=45・事前登録
   どおり)。**2/2 PASS**。
4. **11 target keys** (`cq_local_step.sh` 1 invocation 1キー・外側295s/inner 260s):
   全11キー2-pass fresh-cold完了・TRUNCATED-RETRY 0・WINDOW-EXCEEDED 0・determinism
   mismatch 0。各キー1 invocationでp1/p2双方完走 (実測 2m37s〜3m37s)。
   - **WIN (7行・全て15M < nodes ≦ 20Mで解決)**: aa004 15,616,012 / aa005 15,957,877 /
     aa030 16,765,560 / aa031 17,185,014 / aa035 15,424,243 / aa047 16,230,465 /
     aa053 16,685,872。全て2-pass node-exact + status.log PASS行 + WIN-HALT行。
   - **EXHAUSTED at 20M (4行・honest UNKNOWN・same-condition再probeなし)**:
     aa021 / aa028 / aa032 / aa050 (全て nodes=20,000,000 2-pass一致)。
   - **LOSS 0行・mismatch 0行**。
5. **audit** (`audit_cq.py`): PASS — probed 11/11, win 7, loss 0, exhausted @20M 4,
   window-exceeded 0, unprobed 0, anchors 2, val-gate 4。3回実行 stdout + audit.json
   byte-identical (stdout`13e1f902…` / json `6227eb2c…`)。tamper電池: (a) p2 nodes改変→
   p1/p2不一致捕捉 (b) WIN→LOSS反転→status.log PASS行照合捕捉 (c) replay_done削除→
   truncated捕捉 (d) `reprobe_condition.budget` 19999999→registry gate A捕捉、
   4/4 fail-closed、各probe復元 + cmp byte-identical。
   誠実記録: 当初の(d)probeはregistryに存在しないtop-level `budget` keyを改変しており
   ゲート不発火だった (auditor欠陥ではなく電池側のフィールド設定ミス)。正フィールド
   `reprobe_condition.budget`で再実行し捕捉を確認。また **B commit message中の
   audit.json hash `a2452e59` は手転写ミス** (正: `6227eb2cfeb14c31799d94f19436
   c07233d55c8301d8640ee266b8cc3a366692`・commit messageは取り消せないため
   MANIFEST+本記録で訂正。手転写禁止の教訓を再確認)。
6. **B outputs push**: 32 files (status.log 25行 + audit.json + raw 26 + val-gate
   `.cq-host.out` 4) — commit `962348f9` (observed HEAD-before-push `001278ac` Part CR B)。
   fetch-back 32/32 byte-identical。

### 結果の解釈 (interpretation guard)

- 7 WIN行は **probe-level honest labels のみ**。verdict不消費: canonical adoptionは別
  宣言のadoption Part (pinned fail-closed merger) 経由のみ、WIN行はさらに scrutiny
  owner C++第二実装 gate を通るまで採用されない。本Partはいかなる adoption も行わない。
- batch-28のEXHAUSTED残は 11行 → 4行 (aa021/aa028/aa032/aa050・20M条件でも未解決)。
  これらは今後の別条件 (higher budget / 構造改善 / cache活用) での再probe候補として
  openのまま。20M条件のsame-condition再probeは行わない。
- class 5343 のclosure構成・secured coverage・root勝敗には一切触及しない。
- **標準11×11空盤・class 5343・全キーはこの時点で UNKNOWN**。
