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
  - cs_local_step.sh `cbab00174d26ab9068b148bd87e3d7d3c9c58fa586968b160a824f507355be65` (A版・runner名取りこぼし→修正版 `bb744c2c…` をA-fix commit `614750b3` で出版)
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
### 宣言後実行 (publish-then-execute・protocol遵守)

1. **A scaffold push**: 35 files (scripts 6 / input 8 / sources 12 / val-gate 8 / README)
   — commit `38624142` (observed HEAD-before-push `e31b6f8a` 本宣言)。fetch-back 35/35
   byte-identical。
2. **A-fix push**: published A版 `cs_local_step.sh` (`cbab0017…`) が旧runner名
   `runbatch_b28exh20m.sh` 参照のままだった (session-local orchestration派生時の
   1-token取りこぼし・初回step invocationでrc=127 file-not-found即検出・**targetは
   1キーもsolver実行されていない**: この時点で実行済みだったのはval-gateとanchorsのみ
   で、どちらもderived runner直接呼び出しで無関係)。修正版 `bb744c2c…`
   (EXACTLY 1-token delta) を commit `614750b3` で出版。
3. **環境リセット事故と完全復旧 (誠実記録)**: A-fix直後のfetch-back bash呼び出しで
   インフラレベルの失敗 ("Koyeb remote command…command was not rerun") が発生し
   実行環境がリセット・**ローカル作業ファイル一式 (val-gate 4・anchors 2キー分の
   raw・status.log) が消失**。publish-then-execute設計により実害ゼロ: (a) 消失したのは
   未出版のローカル実行途中成果のみで、B commitはまだ存在しない、(b) kit全体はpublished
   (commit-pinned `38624142` + A-fix `614750b3`) から全35+1ファイルをfetchして再構築
   (sha照合で pinned値と完全一致)、(c) val-gate fresh 4・anchors aa036/aa004は
   **fresh-coldで再実行**し同一結果 (4/4 node-exact・aa036 (2,955659)・aa004
   (1,15616012) + WIN-HALT rc=45) を再現 = 宣言protocolどおり。truncated passは
   証拠にならないというpublished runner guard設計の実働確認にもなった。
4. **val-gate fresh 4** (宣言後・リセット後): at2m×2 exhaustion nodes 2,000,000
   (`9`/`9`)・15m×2 3,651,923 (`17`) / 5,040,200 (`25`)。published baselinesと
   node-exact。**4/4 PASS**。
5. **anchors** (derived runner `runbatch_b28exh25m.sh` 25M): aa036 → PASS
   `25000000,2,955659`・aa004 → PASS `25000000,1,15616012` + WIN-HALT (rc=45)。
   published CQ rawとnode-exact。**2/2 PASS**。
6. **4 target keys** (`cs_local_step.sh` 修正版・外側295s/inner 260s):
   - **WIN (3行・全て20M < nodes ≦ 25Mで解決)**: aa021 22,942,323 / aa028 21,563,925 /
     aa032 20,312,294。全2-pass node-exact + PASS + WIN-HALT。
   - **EXHAUSTED at 25M (1行・honest UNKNOWN)**: aa050 (nodes=25,000,000 2-pass一致。
     p2が1回inner-timeoutでtruncated → published guardがsidecar
     `aa050.p2.truncated.234741.out` に退避・次invocationでp2のみfresh-cold再実行し
     完走。TRUNCATED-RETRY計1回 (<2) でWINDOW-EXCEEDED不発火・事前登録どおり)。
   - **LOSS 0行・mismatch 0行**。
7. **audit** (`audit_cs.py`): PASS — probed 4/4, win 3, loss 0, exhausted @25M 1,
   window-exceeded 0, unprobed 0, anchors 2, val-gate 4。3回実行 stdout +
   audit.json byte-identical (stdout`3bc1c932…` / json `c6622d57…`)。tamper電池:
   (a) p2 nodes改変→p1/p2不一致捕捉 (b) WIN→LOSS反転→status.log PASS行照合捕捉
   (c) replay_done削除→truncated捕捉 (d) registry `reprobe_condition.budget` 24999999→
   gate A捕捉 (CQ教訓どおりschema機械確認の上でフィールド指定・4/4 fail-closed)、
   各probe復元 + cmp byte-identical・clean control PASS。
8. **B outputs push**: 19 files (status.log 12行 + audit.json + raw 12 + truncated
   sidecar 1 + val-gate `.cs-host.out` 4) — commit `37c52cfb` (observed HEAD-before-push
   `4e8229fd`)。fetch-back 19/19 byte-identical。

### 結果の解釈 (interpretation guard)

- 3 WIN行は **probe-level honest labels のみ**。verdict不消費: canonical adoptionは別
  宣言のadoption Part (pinned fail-closed merger `90711961…`) 経由のみ・WIN行はscrutiny
  owner C++第二実装 gate 通過まで採用されない。本Partはいかなるadoptionも行わない。
- **batch-28のEXHAUSTED残は 4行 → 1行 (aa050のみ・15M/20M/25Mで未解決)**。
  aa050は今後の別条件候補としてopen。15M/20M/25M条件のsame-condition再probeは行わない。
- class 5343 のclosure構成・secured coverage・root勝敗には一切触及しない。
- **標準11×11空盤・class 5343・全キーはこの時点で UNKNOWN**。
