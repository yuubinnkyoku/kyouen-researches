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

1. **宣言 push**: commit `ba08e1cf` (observed HEAD `f6635144` Part CU D)・
   fetch-back byte一致 `4be7b5a3…`。対抗宣言なし・batch-28 aa004/aa035未カバー
   をpublished rows.json対象一覧で機械確認済み。
2. **A scaffold push**: 40 files — commit `ae00894d`。fetch-back検証で
   **1 files (sources/canonical-cache-co-merged-b28loss7.cache) が不一致**:
   読み取り側toolが1回あたり64KBで打ち切るpagination仕様のため、259,886 bytes
   中64,000 bytesのみ配置されていた (他39 filesはbyte一致)。**A-fix**
   commit `d56968e` で行offset paginationにより全文再取得・上書きし、
   fetch-back sha `854800f3…` byte一致で確定 (教訓: 64KB超fileは
   pagination必須・push後にapi contents size欄でsize検査)。
3. **環境リセット事故 (誠実開示)**: D1 (rules gate 1回目 PASS) と
   D2 (at2m 2件の実行) を終えた時点 (~00:27Z) で実行環境が同期失敗で
   リセットされ、ローカルscratch (kit一式+D1/D2出力) を喪失した
   (Part CRの同一事象と同型)。kitはpublished commits `ae00894d` + `d56968e`
   から全40 fileを再取得し、scripts/inputの全pin sha + source pin (maker
   再実行で全battery gate PASS・rows.json再生成 byte-identical
   `4a69c73f…`) で復元検証したうえで、**D1..D7を最初から全再実行した**
   (決定的項目は再実行でも同一値: rules gate出力・val-gate全field・
   anchors/targets/replicaのnodes数すべて1回目の実行観察と同一)。
   以下の実行記録・published outputsは再実行版。判定への影響なし
   (auditはoutputsの実行値のみ機械検査)。
4. **D1 rules gate PASS** (`verify_tbl.js` `c8c52528…`): replica quads
   95,670 == third-impl quads 95,670・triples checked 195,044・mismatches 0
   (CRと同一の決定的出力) → `output/rules-gate.txt`。
5. **D2 val-gate fresh 4/4 node-exact** (本host・wall_s比較外): at2m×2
   budget 2,000,000 → exhaustion (result 0, nodes 2,000,000; wall 9s/9s)・
   15m×2 budget 15,000,000 → (result 2, nodes 3,651,923; wall 17s) /
   (result 2, nodes 5,040,200; wall 26s)。published baselinesと全決定
   field一致。注記: at2m 2本目のhost出力はwall_s=9がpublished baselineと
   同じ整数秒だったためfile byte自体が一致 (sha同一・正当な一致)。
   `.cw-host.out` 4件をval-gate/に出版。
6. **D3 negatives 2/2 GATE_FAIL設計どおり**: ng1 "legal count mismatch:
   derived=87 declared=88"・ng2 "stone count mismatch: bits=5 declared=6"
   (CRと同一文言・fail-closed)。
7. **D4 anchors 4/4 published値とnode-exact・a/b det-pair PASS**:
   k02a clean result 1・expansions 9,106,337・ttHits 4,991,527 (wall
   26.37/26.68s)・l1a clean result 2・7,660,602・3,951,175 (22.67/22.75s)。
8. **D5 本host pinned-replica 2-pass fresh-cold ×2 keys PASS**
   (`run_replica_cw.sh`・budget 20M): aa004 p1/p2 = result 1・nodes
   **15,616,012** (wall 86/85s)・aa035 p1/p2 = result 1・nodes
   **15,424,243** (wall 85/85s)。**published CQ raw fields
   (result/nodes/key/legal) とnode-exact一致** (audit G2bで機械検査)。
   EXHAUSTED 0・mismatch 0・TRUNCATED-RETRY 0。誠実注記: runnerの
   外側終了コードが成功時もrc=1になる (`[ "$RC" -ne 0 ] && exit "$RC"` の
   短絡評価が最終ループ文になるbash仕様・CR版から不変)。per-passの
   正しいrc=0はstatus.logに記録済みで、実行成否の判定はaudit G2bが機械検査。
9. **D6 targets clean verdict一致 (agreement 2/2・WIN=2・LOSS=0)**:
   aa004 a/b det-pair PASS・result **1 (clean)**・expansions **18,707,043**・
   ttHits 9,558,720 (wall 53.31/51.77s)・aa035 a/b det-pair PASS・result
   **1 (clean)**・expansions **18,461,728**・ttHits 9,389,275 (52.45/52.10s)。
   cap 300,000,000・wallcap 240・memo-power=22・WALL-INCONCLUSIVE 0・
   DIVERGENCE 0。pass-one第三実装拡張数合計 **37,168,771**。
   **両行のthree-implementation corroboration成立** (published CQ replica
   2-pass + 本host pinned-replica 2-pass + 第三実装 minimax 2-run、すべて
   verdict WIN一致)。
10. **D7 audit (`audit_cw.py`)**: **ALL 103 GATES PASS** (CR 148 gateの
    2-target版)・3回実行 byte-identical (stdout `72b07e76…` ×3・
    audit-summary.json `684acf45…`)・verdict agreements 2/2 (WIN=2
    LOSS=0)・wall_inconclusive 0・決定的 (タイムスタンプ不読)。
    gate内訳: G0 input CSV×rows.json一致・G1 pinned script bytes×3 +
    rows-schema + target-count 2 + verdict-kinds [1,1]・G2 rules gate×2・
    G2b replica×2 targets (present/done/quads/det-pair/schema(20M)/key/
    verdict-vs-published)・G3 anchors×2・G4 negatives×2 fail-closed・
    G5 targets×2 (key/legal/quads/det-pair/verdict-agree)・**G6 unadopted
    補強** (raw pin aa004/aa035 p1/p2×4・merged cache pin 6,301行・対象row
    不在・同key競合rowゼロ・increment 7 rows byte一致・manifest全pin +
    **宣言済みbatch-28適合**: 対象idがadopted/win系id list全不在
    (target-not-in-adopted-lists) かつexhausted_excluded_ids/probed_ids/
    resolved_ids member bookkeepingに所在 (target-in-member-books)・
    exhausted roster 11行機械照合)・**G7 val-gate 4/4 node-exact**。
    - **audit tamper電池 4/4検出 + clean control PASS** (scratch copy上:
      A1 PIN_THIRD末尾反転 → `pin-third_impl.js` fail・A2 aa004.b
      expansions+1 → `target-aa004-det-pair` fail・A3 input aa004 legal
      91→90 → `input-aa004-matches-rows` fail・A4 PIN_MERGED_CANONICAL
      末尾反転 → `rows-schema` fail。efficacy-asserted sed・電池後の
      実験dir bytes不変・clean controlはaudit-summary.jsonが実験dir版と
      byte-identical)。
    - **maker tamper電池 8/8検出** (A push前に実施、宣言に記載): 初回
      T3/T5はsed不適合で無効果だったためefficacy-assertedで再実行し検出
      (clean control rows.json byte-identical・実験dir bytes不変)。
11. **補助確認 (宣言どおり・pinned kit gateとは別の記録)**: Part CU出版の
    最新canonical merged chain cache (6,317行・sha256 `30ddad9d…`
    fetch照合) に、aa004 key (1171516445255794689,0) と aa035 key
    (1152921504606846978,4228) のs5verdict rowは **0行** (機械検査)。
    verdict不消費を最新snapshotに対しても確認。本Partはcanonical cacheに
    一切書込んでいない (read-only不変 `854800f3…`)。
12. **B outputs push**: 24 files (rules-gate + status.log 14行 +
    audit-summary + audit-run×3 + targets 4 + anchors 4 + negative 2 +
    replica 4 + val-gate `.cw-host.out` 4) — commit `a892601e` (observed
    HEAD-before-push `d56968e` 本A-fix)。fetch-back 24/24 byte-identical。

### 結果の解釈 (interpretation guard)

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
