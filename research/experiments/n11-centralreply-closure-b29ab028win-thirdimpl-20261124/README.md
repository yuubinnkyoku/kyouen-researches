# batch-29 (closure class 2251) Part CI takeover drive-2 WIN 1行 (ab028) 第三実装交叉検証 — Part CZ (2026-11-24)

Part CZ (publish-then-execute・単一オーナー・宣言
`research/log/2026-11-24-part-cz-b29win-thirdimpl-declaration.md`・commit
`4c741798`)。Part CI takeover drive-2 (batch-29 全54キー probe-complete・
commit `141cf80c`) で **15M fresh-cold 2-pass条件で解決した唯一のWIN行**
に対するpinned第三実装 (非df-pn AND/ORミニマックス `third_impl.js`
`08ea958f…`) によるverdict-level交叉検証 + 本host pinned-replica
(`jsreplay.js` `84585617…`) 2-pass fresh-cold再現 + **Part CU adoption出版物**
(merged canonical cache 6,317行 `30ddad9d…` = CO base 6,301行 + batch-29
drive-1 LOSS 16行採用後) に対するunadopted補強機械gate。**verdict不消費**
(ab028はhonest labelのまま・本Partの新規採用・解放・閉鎖は一切なし・採用は
scrutiny owner C++第二実装 gate `9193f5b6…` を経て別adoption Part
(pinned fail-closed merger `90711961…` 経由) のみ)。閉鎖・被覆・secured・
root勝敗の主張はしない。

## 対象 (published正本から機械導出・maker `make_inputs_cz.py` `782e8937…`)

- **ab028**: key (1297036830121656320, 131074)・s5 93815・legal 80・
  membership 3・published batch-29 drive-2 replica result **1 (WIN行)**・
  nodes **3,167,121** (2-pass node-exact)。

batch-29 (class 2251) 54キー中、Part CI drive-1 で16行LOSSがPart CUにて
canonical採用済み・38行がfileless UNPROBED、残るdrive-2 15M fresh-cold
probeで resolver解決 53行 + WIN 1行 (ab028)。ab028はCU increments-manifest
上 **fileless UNPROBED roster (38キー) のメンバ** で、 Part CV
(ckpt-1/3 LOSS 16行 ab001..ab016 の交叉検証・完了 `3b6ad066`) の対象外。
本Partが初めて第三実装交叉検証する行。rows.json `d8c53d29…` (maker ×2回
実行byte-stable PASS)。sources pin (commit-pinned raw fetch・sha256全照合):
batch-keys-b29 `330c0b9f…` (54キー)・status-b29.log `b49322d9…` (55行 =
54 PASS + 1 WIN-HALT・drive-1 prefix `6b877344…` = CU manifest status pin
とbyte一致)・README-b29 `56fa34e3…`・drive-2 declaration/completion logs
`8819c366…`/`46c461bd…`・raw 2 pin (ab028.p1 `af6e6fe4…` / ab028.p2
`77a47364…`)・published-input ab028 `1d0416af…`・BF anchor/negative CSV
4 pin (k02a `b6174a3f…` / l1a `e13d2a6c…` / ng1 `8e64b9ad…` / ng2
`f19cd5a3…`)・**Part CU出版物** (read-only不変): merged canonical cache
`30ddad9d…` (260,590 bytes・6,317 rows) / increment `bab011e3…` (16 rows) /
increments-manifest `f9f58ee1…` / merger `90711961…` / CO base `854800f3…`
(6,301 rows)。val-gate baselines 4 (published pin一致)。provenance chainは
AR→BF→BK→BM→BS→BV→BW→BX→BY→CC→CL→CM→CR→CW→**CZ**。

## kit (36 files — A scaffold commit `161373f9`・fetch-back 36/36 byte一致)

- scripts 7 (byte-pins): jsreplay.js `84585617…` (published kernel
  byte-clone) / third_impl.js `08ea958f…` (published第三実装 byte-clone) /
  verify_tbl.js `c8c52528…` (rules-engine gate byte-clone) /
  run_thirdimpl.sh `a0b77d83…` (published byte-clone) /
  **run_replica_cz.sh** `cb909064…` (published Part CW runner
  `run_replica_cw.sh` `8c123b65…` の最小派生・機能diffは予算1行のみ:
  `--exact-replay-budget=20000000` → `15000000`) /
  make_inputs_cz.py `782e8937…` (fail-closed maker・solver非実行時点で宣言) /
  audit_cz.py `3c95e32f…` (fail-closed audit・schema
  `n11-centralreply-closure-b29ab028win-thirdimpl-audit-v1`)。
- input 6: rows.json (maker生成・machine-derived) + 対象1 + anchors 2 +
  negatives 2 CSV (published byte一致・maker G0/derived-vs-published gate込み)。
- sources 15: published batch-29 drive-2正本 (raw 2 / status-b29.log /
  README-b29 / drive-2 logs 2 / batch-keys / published-input 1 / BF
  anchor-negative CSV 4) + Part CU出版物 3。
- val-gate 8: published 4組 (at2m×2 budget 2,000,000 / 15m×2 budget
  15,000,000・input CSV + published baselines byte-clone) + 本host fresh
  `.cz-host.out` 4 (宣言後実行・D2)。

## 宣言protocol (publish-then-execute): D1-D8 は宣言ノートどおり

## 実行記録 (宣言protocol・逐次)

1. **宣言 push**: commit `4c741798` (observed HEAD `39f29652` Part CY B)
   ・push戻り blob sha1 `2a5940e5…` がローカル git-blob-sha1 と一致・
   fetch-back sha256 `40f8527c…` byte一致。対抗宣言なし・ab028未カバーを
   published Part CV rows.json対象一覧で機械確認済み。
2. **A scaffold push**: 36 files — commit `161373f9`。fetch-back検証
   **36/36 byte一致** (260,590 bytesのmerged cacheは行offset pagination
   7chunk連結で全長を読み取り・Part CWのA-fix事故は再発なし)。
3. **D1 rules gate PASS** (`verify_tbl.js` `c8c52528…`): replica quads
   95,670 == third-impl quads 95,670・triples checked 195,044・mismatches 0
   → `output/rules-gate.txt` (`88c0b78b…`)。
4. **D2 val-gate fresh 4/4 node-exact** (本host・wall_s比較外): at2m×2
   budget 2,000,000 → exhaustion (result 0, nodes 2,000,000; wall 9s/9s)・
   15m×2 budget 15,000,000 → (result 2, nodes 3,651,923; wall 17s) /
   (result 2, nodes 5,040,200; wall 26s)。published baselinesと全決定
   field一致。注記: at2m 2本目のhost出力はwall_s=9がpublished baselineと
   同じ整数秒だったためfile byte自体が一致 (sha同一・正当な一致・CWと
   同一事象)。
5. **D3 negatives 2/2 GATE_FAIL設計どおり**: ng1 "legal count mismatch:
   derived=87 declared=88"・ng2 "stone count mismatch: bits=5 declared=6"
   (fail-closed文言はCWと同一)。
6. **D4 anchors 4/4 published値とnode-exact・a/b det-pair PASS**:
   k02a clean result 1・expansions 9,106,337・ttHits 4,991,527 (wall
   26.81/27.23s)・l1a clean result 2・7,660,602・3,951,175 (22.52/22.82s)。
7. **D5 本host pinned-replica 2-pass fresh-cold PASS** (`run_replica_cz.sh`
   `cb909064…`・budget 15M): ab028 p1/p2 = result 1・nodes **3,167,121**
   (wall 15/16s)。**published drive-2 raw fields (result/nodes/key/legal)
   とnode-exact一致** (audit G2bで機械検査)。誠実注記: runnerの外側終了
   コードが成功時もrc=1になる (`[ "$RC" -ne 0 ] && exit "$RC"` の短絡評価
   が最終ループ文になるbash仕様・CW版から不変)。per-passの正しいrc=0は
   status.logに記録済み。
8. **D6 target clean verdict一致 (agreement 1/1・WIN=1・LOSS=0)**:
   ab028 a/b det-pair PASS・result **1 (clean)**・expansions **3,595,562**・
   ttHits 2,114,848 (wall 10.54/10.90s)。cap 300,000,000・wallcap 240・
   memo-power=22・WALL-INCONCLUSIVE 0・DIVERGENCE 0。pass-one第三実装
   拡張数合計 **3,595,562**。**three-implementation corroboration成立**
   (published drive-2 host 2-pass + 本host pinned-replica 2-pass + 第三実装
   minimax 2-run、すべて verdict WIN一致)。
9. **D7 audit (`audit_cz.py` `3c95e32f…`)**: **ALL 79 GATES PASS**・3回実行
   byte-identical (audit-summary.json `c618767a…` ×3)・verdict agreements
   1/1 (WIN=1 LOSS=0)・wall_inconclusive 0・決定的 (タイムスタンプ不読)。
   gate内訳: G0 input CSV×rows.json一致×5・G1 pinned script bytes×3 +
   rows-schema + target-count 1 + verdict-kinds [1]・G2 rules gate×2・G2b
   replica (present/done/quads/det-pair/schema(15M)/key/verdict-vs-published)・
   G3 anchors×2・G4 negatives×2 fail-closed・G5 target (key/legal/quads×2/
   det-pair/verdict-agree)・**G6 unadopted補強** (raw pin ab028 p1/p2×2・
   merged cache pin 6,317行・対象row不在・同key競合rowゼロ・increment
   16 rows pin + ADOPTED set header・manifest全pin + flags + row_counts
   (16/16/0/0/0/38) + status prefix pin `6b877344…` 16行・fileless roster
   38キー機械照合 + **宣言済みbatch-29/CU適合**: ab028が全adopted/win/probed
   id listに不在 (target-not-in-adopted-lists) かつ fileless_unprobed_ids
   に所在 (target-in-fileless-roster))・**G7 val-gate 4/4 node-exact**。
   宣言開示済み: 実行前に合成kit上で79 gate PASS ×3 byte-identical +
   audit-side tamper 電池10/10 fail-closed検出 (malformed third行の
   tracebackクラッシュをfail-closed名前付きgateに修正済み)。
10. **B outputs push**: 17 files (rules-gate + status.log 10行 +
    audit-summary + replica 2 + targets 2 + anchors 4 + negative 2 +
    val-gate `.cz-host.out` 4) — commit `66baba24` (observed
    HEAD-before-push `68f80a85` Part CY drive-2 val-gate)。fetch-back
    **17/17 byte一致**。
11. **C README最終 + MANIFEST-sha256** (本commit): 計53 file 全sha256記録。

### 結果の解釈 (interpretation guard)

- ab028のWIN行は **probe-level honest label のまま**。canonical adoptionは
  別宣言のadoption Part (scrutiny owner C++第二実装 gate `9193f5b6…` +
  pinned fail-closed merger `90711961…` 経由) のみ。本Partはいかなる
  adoption も行わない。
- batch-29 (class 2251) のclosure構成・secured coverage・root勝敗には一切
  触及しない。54キー中53キーがLOSS honest label (16採用済み + 37未採用)・
  1キーがWIN honest label (ab028・本Partで交叉検証済み・未採用)・
  EXHAUSTED 0だが、これはbatchのprobe完了を意味するのみで閉鎖を意味しない。
- **標準11×11空盤・19 central-reply roots・class 2251・全バッチキー
  (batch-29 54キーを含む) はこの時点で UNKNOWN**。nodes数・expansions数・
  ttHits数・wall秒数を勝敗として読まない。

## 宣言時に機械確認済みの並走状態

- Part CP takeover (batch-30 class 34269・宣言 `87e19b5a`)・Part CY
  (batch-31 class 5804・宣言 `afc1bcc5`・drive-1完了→drive-2宣言
  `21fef631`)・Part CX (batch-28 CQ WIN 5行交叉検証・宣言 `1300c10d`) は
  **いずれも非接触別レーン** (対象キー・class・バッチが全く別)。
- 既存のbatch-29第三実装交叉検証は Part CV のckpt-1/3 LOSS 16行
  (ab001..ab016) のみで、**ab028 は未カバー**だった (published rows.json
  対象一覧で機械確認済み・本Partが初回)。
