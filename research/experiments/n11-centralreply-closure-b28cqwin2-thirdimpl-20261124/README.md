# batch-28 (closure class 5343) Part CQ 20M再probe 新解決WIN 2行 (aa004/aa035) 第三実装交叉検証 — Part CW (2026-11-24)

Part CW (publish-then-execute・単一オーナー・宣言
`research/log/2026-11-24-part-cw-b28cqwin2-thirdimpl-declaration.md`)。
Part CQ (batch-28 EXHAUSTED 11行の20M再probe・commit-pinned出版) で**新しく解決された
WIN 2行**に対するpinned第三実装 (非df-pn AND/ORミニマックス `third_impl.js` `08ea958f…`)
によるverdict-level交叉検証 + 本host pinned-replica (`jsreplay.js` `84585617…`)
2-pass fresh-cold再現 + **Part CO adoption出版物** (merged canonical cache 6,301行
`854800f3…` = Part CH 6,294 + batch-28 LOSS 7行採用後) に対するunadopted補強機械gate。
**verdict不消費** (2行はhonest labelのまま・本Partの新規採用・解放・閉鎖は一切なし・
採用はscrutiny owner C++第二実装 gate `9193f5b6…` を経て別adoption Part のみ)。
閉鎖・被覆・secured・root勝敗の主張はしない。

## 対象 (published正本から機械導出・maker `make_inputs_cw.py` `8a9fe75e…`)

- **aa004**: key (1171516445255794689, 0)・s5 118693・legal 91・membership 4・
  published CQ 20M replica result **1 (WIN行)**・nodes 15,616,012 (2-pass node-exact)。
- **aa035**: key (1152921504606846978, 4228)・s5 199720・legal 96・membership 4・
  published CQ 20M replica result **1 (WIN行)**・nodes 15,424,243 (2-pass node-exact)。

両行ともPart CQ時点 (2026-11-23) までは15M EXHAUSTED (Part CO manifest
exhausted_excluded_ids 11行のメンバ) で、20M条件で初めてWIN解決した行。
rows.json `4a69c73f…` (maker ×2回実行byte-stable PASS)。sources pin (commit-pinned
raw fetch・sha256全照合): batch-keys-b28 `af19208f…` (54キー)・status-cq.log
`afc48734…` (25行: 13 PASS + 8 WIN-HALT + 4 EXHAUSTED・重複0・retry 0)・
README-cq `e0153971…`・log-cq `be208f9c…`・raw 4 pin (aa004.p1 `82ebc402…` /
aa004.p2 `ec10d92b…` / aa035.p1 `32fc69c3…` / aa035.p2 `bb30106a…`)・
published-input 2 pin (aa004 `466f713d…` / aa035 `a54715b6…`)・BF anchor/negative
CSV 4 pin (k02a `b6174a3f…` / l1a `e13d2a6c…` / ng1 `8e64b9ad…` / ng2 `f19cd5a3…`)
・**Part CO出版物** (read-only不変): merged canonical cache `854800f3…`
(259,886 bytes・6,301 rows) / increment `bd5ef7d7…` (7 rows) /
increments-manifest `b47e07ca…` / merger `90711961…`。val-gate baselines 4
(publishedとのpin一致済み)。provenance chainはAR→BF→BK→BM→BS→BV→BW→BX→
BY→CC→CL→CM→CR→CW。

## kit

- scripts 7 (byte-pins): jsreplay.js `84585617…` (published kernel byte-clone)
  / third_impl.js `08ea958f…` (published第三実装 byte-clone) / verify_tbl.js
  `c8c52528…` (rules-engine gate byte-clone) / run_thirdimpl.sh `a0b77d83…`
  (published byte-clone) / **run_replica_cw.sh** `8c123b65…` (published Part CR
  runner `run_replica_cr.sh` `7980b2fb…` の最小派生・機能diffは予算1行のみ:
  `--exact-replay-budget=15000000` → `20000000`・他はコメント行のみ) /
  make_inputs_cw.py `8a9fe75e…` (fail-closed maker・solver非実行) /
  audit_cw.py `a7876a0a…` (fail-closed audit・schema
  `n11-centralreply-closure-b28cqwin2-thirdimpl-audit-v1`)。
- input 7: rows.json (maker生成・machine-derived) + 対象2 + anchors 2 +
  negatives 2 CSV (published byte一致・maker G0/derived-vs-published gate込み)。
- sources 17: published Part CQ正本 (raw 4 / status / README / completion log /
  batch-keys / published-input 2) + Part CO出版物 3 + published Part BF
  anchor/negative CSV 4。全ファイル commit-pinned raw fetch + sha256 pin照合済み。
- val-gate 8: published 4組 (at2m×2 budget 2,000,000 / 15m×2 budget 15,000,000・
  input CSV + published baselines byte-clone) + 本host fresh `.cw-host.out` 4
  (宣言後実行・D2)。

## 宣言protocol (publish-then-execute)

- D1: rules gate (pinned `verify_tbl.js`): replica quads 95,670 == third-impl
  quads 95,670・triples checked・mismatches 0 を `output/rules-gate.txt` に記録。
- D2: val-gate fresh 4 (本host `jsreplay.js`・published baselinesとnode-exact・
  wall_s比較外) → `val-gate/*.cw-host.out`。
- D3: negatives ng1/ng2 → GATE_FAIL設計どおり (fail-closed各theta検査)。
- D4: anchors k02a/l1a 各 a/b 2-run determinism pair (published値
  k02a 9,106,337/4,991,527・l1a 7,660,602/3,951,175 とnode-exact)。
- D5: 本host pinned-replica 2-pass fresh-cold ×2 keys (`run_replica_cw.sh`・
  budget 20M・1 invocation 1キー・inner `timeout 260`) → aa004/aa035 の
  published raw fields (result/nodes/key/legal) とのnode-exact一致をaudit G2bで
  機械検査。
- D6: targets aa004/aa035 各 a/b 2-run第三実現 (`run_thirdimpl.sh`・
  cap 300,000,000・wallcap 240・memo-power=22)。
- D7: audit `audit_cw.py` ×3回実行 byte-identical + clean control + tamper電池。
- D8: B outputs出版 → C README最終化 + MANIFEST-sha256 → 完了log出版
  (fetch-back byte一致検証)。

## 実行記録 (宣言protocol・逐次)

(宣言出版後に追記)

### 結果の解釈 (interpretation guard・verdict不消費)

- 2 WIN行は **probe-level honest labels のまま**。canonical adoptionは別宣言の
  adoption Part (pinned fail-closed merger `90711961…` 経由) のみで、WIN行はさらに
  scrutiny owner C++第二実装 gate `9193f5b6…` を通るまで採用されない。本Partは
  いかなる adoption も行わない。
- batch-28のEXHAUSTED残は Part CT後 3行 (aa021/aa028/aa032・20M条件でも未解決・
  別条件候補としてopen) — 本Partは EXHAUSTED 行に触及しない (対象はCQ解決済み
  WIN行のみ)。
- class 5343 のclosure構成・secured coverage・root勝敗には一切触及しない。
- **標準11×11空盤・19 central-reply roots・class 5343・全バッチキー (batch-28 54キー
  を含む) はこの時点で UNKNOWN**。nodes数・expansions数・ttHits数・wall秒数を
  勝敗として読まない。

## 宣言時に機械確認済みの並走状態

- Part CU宣言 `d8276573` (batch-29 class 2251 の 16-LOSS canonical adoption) と
  Part CV宣言 `a8592d9c` (batch-29 ckpt-1/3 LOSS 16行の row-audit + replica +
  第三実装交叉検証) は**非接触別レーン** (batch/class/対象キーが全く別)。
- 既存のbatch-28第三実装交叉検証は aa001/aa002 (b28win) / aa003 (drive2loss) /
  aa006/aa007 (drive2win) / aa008/aa009 (drive3win) の7行で、aa004/aa035 は
  未カバー (published experiments一覧で機械確認)。
