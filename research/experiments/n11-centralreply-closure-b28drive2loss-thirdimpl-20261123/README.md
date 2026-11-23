# batch-28 drive-2 LOSS行 aa003 (Part CL) 第三実装交叉検証 + 本host pinned-replica 2-pass + Part CH採用row補強 (2026-11-23)

Part CL (宣言: `research/log/2026-11-23-part-cl-b28drive2loss-thirdimpl-declaration.md`
commit `7a184e92`・publish-then-execute・単一オーナー)。Part CD (batch-28 drive-2)
で出版され **Part CHでcanonical cacheに採用済み**のLOSS行 **aa003** に対するpinned第三
実装 (非df-pn AND/ORミニマックス `third_impl.js` `08ea958f…`) によるverdict-level
交叉検証 + 本host pinned-replica (`jsreplay.js` `84585617…`) 2-pass fresh-cold再現
+ 採用row byte同一性機械gate。**verdict不消費** (aa003の採用は先行する別宣言
Part CHが完了済み・本Partの新規採用・解放・閉鎖は一切なし)。閉鎖・被覆・secured・
root勝敗の主張はしない。

誠実な開示: batch-28 drive-2 (aa003の出版元) は Part CD実行hostの単一環境出版物
であり、aa003の第二実行環境同時再現は出版されていなかった。本Partのthis-host
pinned-replica 2-passはpublished source bytesのsha検証後に全工程を再実行した
ものであり node-exact一致 (result 2・nodes 4,070,373) を達成した。
**aa003 (canonical cache最新row) の最初の独立セッション再現**として記録する
(実行hostの物理的相違までは主張しない)。

## 対象 (published正本から機械導出・maker `make_inputs_ck.py` `177c4409…`)

- **aa003**: key (1152921504741064704, 4228)・s5 104943・membership 3・legal 86・
  published replica result 2 (LOSS行)・nodes 4,070,373 (2-pass node-exact)・
  **Part CHで採用済み** (`s5verdict,1152921504741064704,4228,5,2,4070373` =
  merged canonical cache 6,294行 `3124461b…` 内の採用row・increment
  `dc857bfd…` の1行・increments-manifest `017c7c30…` のloss_ids、すべて機械照合)。

sources pin (commit-pinned raw fetch・sha256全照合): batch-keys-cd `af19208f…`・
status-cd.log `343097c2…` (17行)・row-audit-cd `3e86a32b…` (probed 7・loss_rows
[aa003]・win_rows [aa001,aa002,aa006,aa007]・exhausted [aa004,aa005]・fileless 47)・
README-cd `338fc136…`・raw aa003.p1 `9fff0eea…` / p2 `a1edb177…`・published-input
aa003 `95abcd03…`・Part CH merged canonical cache `3124461b…` / increment
`dc857bfd…` / increments-manifest `017c7c30…`・BF anchor/negative CSV 4ピン
(provenance chain AR→BF→BK→BM→BS→BV→BW→BX→BY→CC→CL)。

## 実行結果 (宣言protocol順・逐次実行)

1. **rules gate PASS**: pinned `verify_tbl.js` `c8c52528…`・replica quads
   95,670 == third-impl quads 95,670・triples checked 195,044・mismatches 0
   (禁止四角 95,670)。
2. **val-gate this-host 4/4 node-exact** (pinned `jsreplay.js`・published baseline
   との一致・wall_s比較外): at2m 2キー budget 2,000,000 exhaustion (result 0,
   nodes 2,000,000) ×2・15m基準キー budget 15M (result 2, nodes 3,651,923) と
   (result 2, nodes 5,040,200)。本host `.ck-host.out` 4件はval-gate/に出版
   (audit G7でも機械gate)。
3. **negatives 2/2 GATE_FAIL設計どおり** (ng1: legal count mismatch derived=87
   declared=88・ng2: stone count mismatch bits=5 declared=6)。
4. **anchors 4/4 本host node-exact** (a/b determinism PASS): k02a clean WIN
   result 1・expansions 9,106,337・ttHits 4,991,527 (wall 26.16/25.79s)・l1a clean
   LOSS result 2・7,660,602 / 3,951,175 (wall 22.15/22.41s) — published第三実装値
   (Part G/K/O/P/T/W/AA/AD/AG/AL/AR/AX/AZ/BF/BK/BM/BS/BV/BW/BX/BY/CC) と同一。
5. **本host pinned-replica 2-pass fresh-cold**: aa003 p1/p2 = result 2・nodes
   **4,070,373** (two-pass node-exact・wall 19/19s・published 51/49s)。
   published raw fields (result 2・nodes 4,070,373) との一致をaudit G2bで機械検査。
   EXHAUSTED 0・mismatch 0。**aa003の最初の独立セッション再現**。
6. **target aa003 clean LOSS一致 (verdict agreement 1/1)**: third-impl a/b
   determinism PASS・result **2** (clean)・expansions 4,715,593・ttHits 2,592,846
   (wall 13.65/13.43s)・cap 300,000,000・wallcap 240・memo-power=22・
   WALL-INCONCLUSIVE 0・DIVERGENCE 0。pass-one third-impl拡張数 4,715,593
   (replica nodes 4,070,373 との比率 1.158)。**canonical cache最新採用rowの
   three-implementation corroboration成立** (published drive-2 replica 2-pass +
   本host pinned-replica 2-pass + 第三実装 minimax 2-run すべて result 2)。

## 監査 (`audit_ck.py` `edf0ae7c…`・schema `n11-centralreply-closure-b28drive2loss-thirdimpl-audit-v1`)

**ALL 68 GATES PASS**・3回実行byte一致 (audit-run1/2/3.txt・audit-summary-run1/2/3.json
同一sha `297e7a7f…`・audit-summary.json同)・決定的 (タイムスタンプ不読)・
verdict_agreements 1/1 (aa003 third=2 replica=2 agree=true)・wall_inconclusive 0。
gate内訳: G0 input CSV×rows.json一致 (61-bit keyのPython int完全一致)・G1 pinned
script bytes×3・rows-schema + 採用済みフラグ (`consumed_into_canonical_cache:
false` + `adopted_before_this_experiment_by_part_ch: true` + cache pin一致)・
G2 rules gate×2・G2b replica再現 (present/done/quads/det-pair/schema/key/
verdict-vs-published)・G3 anchors×2 (clean/expansions/legal/key/det-pair)・
G4 negatives×2 fail-closed・G5 target (key/legal/quads/det-pair/verdict-agree)・
**G6 採用row補強×3ソース** (merged cache pin・6,294行・採用rowちょうど1回・
同key競合rowゼロ・increment単一row一致・increments-manifestのloss_ids/
full!=loss/merger `90711961…`/base 6,293/absent-hits 0/quarantine 0/unadopted
WIN 4行 unintroduced)・**G7 val-gate 4/4 node-exact**。

- **maker tamper battery 8/8検出** (scratch /tmp copy上: T1 raw p1 nodes+1・
  T2 row-audit probed 7→8・T3 README-cd文言反転・T4 status aa003 verdict反転・
  T5 published-input legal 86→85・T6 BF anchor k02a lo+1・T7 batch-keys s5_index
  104943→104944・T8 merged cache採用row result反転 2→1)。全probeに適用実効性
  assert・battery後の実験dir bytes不変を検証。
- **audit tamper battery 4/4検出 + clean control PASS** (scratch copy上: T1
  PIN_THIRD末尾反転 → `pin-third_impl.js` gate fail・T2 targets aa003.a
  expansions+1 → `target-aa003-det-pair` fail・T3 input CSV aa003 legal 86→87 →
  `input-aa003-matches-rows` fail・T4 scratch merged-cache採用row nodes+1 →
  `adopt-pin-merged-cache` fail)。実験dir bytes不変。誠実記録: T1の第1sed
  (`s/Pin_THIRD/…`) はマッチしないno-opだったが有効tamper (第2sed・PIN末尾
  反転) の実効性assertで検出は成立 (no-opを正直開示)。

## 誠実な開示 (宣言に対する逸脱・補足)

- publish-then-execute規約に対し、宣言出版前に実施したのはread-only解析のみ
  (kit取得・sources sha検証・maker実行4回byte一致)。宣言に開示済み。
- 宣言protocolどおりの逸脱ゼロ。補足事項: (a) val-gate/replica実行は
  published .out体裁 (stdout+stderr統合) で取得した (初回4本のstdoutのみの
  取得はquads header行を欠くためbaseline体裁と不整合となり、宣言直後に
  体裁を合わせて再実行・全4本 node-exact確認。当該初回ファイルは破棄し
  最終実行のみ出版)。(b) status.logのPROTOCOL行は出力ファイル群から機械生成
  (手転写ゼロ)・生成時に1行の文言不整合 ([4] anchors行の組版ミス) を検出し
  機械修正して確定した。
- 宣言時点から見た環境メモ: 本実行hostはPart CD実行hostと異なるセッション
  (aa003 nodes 4,070,373 wall 19/19s vs published 51/49s)。

## 意味と消費規則 (route statementのみ)

- 第三実装 (非df-pn AND/OR minimax) のclean verdictがpublished replica verdict
  (result 2 = LOSS行) と1/1で一致し、本host pinned-replicaがpublished nodesを
  2-passで完全再現した。これは**Part CHで採用済みのcanonical cache最新row
  (aa003) に対するthree-implementation corroboration** (verdict-level文献) であり、
  採用 (adoption) ではない。canonical cache 6,294行 `3124461b…` はread-only不変。
- WIN 4行 (aa001/aa002/aa006/aa007) およびPart CJ drive-3で出版されたaa008/aa009
  WIN行の採用判断は引き続き scrutiny owner C++第二実装 gate pin `9193f5b6…` 待ち
  (本レーンは代行しない・aa006/aa007の第三実装検証はPart CG宣言済み)。
- 不接触: batch-28 fileless残キー (Part CK drive-4宣言済み)・batch-29 (Part CI)・
  batch 1..28 published dirs・fast lane・finite-field lane・inversive-arc lane・
  z19/z20/z21 lanes・28+2 unconsumed closure WIN候補の採用状態・legacy note。
- **標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2 {59,60}・
  class 1/2/4・class 10968・class 23964・class 5343 (54キーすべて・aa003を含む) は
  どの時点でもUNKNOWNのまま。** nodes数・expansions数・ttHits数・wall秒数を勝敗と
  して読まない。WIN/LOSS採用は別adoption Part (pinned fail-closed merger
  `90711961…` 経由) のみ。

## 出版コミット (全てcommit-pinned raw fetch-back byte照合)

- 宣言: `7a184e92` (log file 10,843B・blob `c256073d`・fetch-back byte一致)。
- A scaffold: scripts 6 + input 6 + sources 14 + val-gate 8 = 34 files。
- B outputs: rules-gate 1 + val-gate this-host 4 + replica 2 + negatives 2 +
  anchors 4 + targets 2 + audit 7 + status.log 1 = 23 files (計57 + README = 58)。
- C README + MANIFEST-sha256 (58 files pinned): 本コミット。
