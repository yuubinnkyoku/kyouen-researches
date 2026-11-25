# batch-28 drive-3 WIN-HALT行 aa008/aa009 (Part CM) 第三実装交叉検証 + 本host pinned-replica 2-pass + 未採用WIN行補強 (2026-11-23)

Part CM (宣言: `research/log/2026-11-23-part-cm-b28drive3win-thirdimpl-declaration.md`
commit `27217816`・publish-then-execute・単一オーナー)。Part CJ (batch-28 drive-3)
で出版された **WIN-HALT行 aa008/aa009** に対するpinned第三実装 (非df-pn AND/OR
ミニマックス `third_impl.js` `08ea958f…`) によるverdict-level交叉検証 + 本host
pinned-replica (`jsreplay.js` `84585617…`) 2-pass fresh-cold再現 + 未採用性機械
gate。**verdict不消費** (aa008/aa009はhonest WIN labelのまま・本Partの新規採用・
解放・閉鎖は一切なし・採用はscrutiny owner C++第二実装 gate pin `9193f5b6…` を
経て別adoption Part (pinned fail-closed merger `90711961…`) のみ)。閉鎖・被覆・
secured・root勝敗の主張はしない。

誠実な開示: batch-28 drive-3 (aa008/aa009の出版元) は Part CJ実行hostの単一環境
出版物であり、aa008/aa009の第二実行環境同時再現は出版されていなかった。本Partの
this-host pinned-replica 2-passはpublished source bytesのsha検証後に全工程を再実行
したものであり node-exact一致 (aa008 nodes 5,270,340・aa009 nodes 7,319,605・
いずれもresult 1) を達成した。**aa008/aa009 (drive-3 WIN行) の最初の独立セッション
再現**として記録する (実行hostの物理的相違までは主張しない)。aa008/aa009の意味は
route statementのみ (unconsumed closure WIN候補34/35番目)。

## 対象 (published正本から機械導出・maker `make_inputs_cm.py` `f926b5be…`)

- **aa008**: key (1171516445255794704, 0)・s5 140489・membership 4・legal 85・
  published replica result 1 (WIN行)・nodes 5,270,340 (2-pass node-exact)。
- **aa009**: key (1747977197559218176, 0)・s5 142299・membership 4・legal 91・
  published replica result 1 (WIN行)・nodes 7,319,605 (2-pass node-exact)。

sources pin (commit-pinned raw fetch・sha256全照合): batch-keys-cd `af19208f…`・
status-cj.log `1a5c08c5…` (21行: PASS 9・WIN-HALT 6・EXHAUSTED 2・TRUNCATED-RETRY
4)・row-audit-cj `eb1d1e98…` (probed 9・win 6 [aa001,aa002,aa006,aa007,aa008,aa009]・
loss [aa003]・exhausted [aa004,aa005]・fileless 45 [aa010..aa054]・mismatch 0)・
README-cj `3615b5c1…`・raw aa008.p1 `f87c2ae9…` / aa008.p2 `5546ed29…` /
aa009.p1 `50c32fd5…` / aa009.p2 `d79fc6d8…`・published-input aa008 `3aaf4e1b…` /
aa009 `47ce8cf9…`・未採用性補強用 (read-only・Part CH出版物): merged canonical
cache `3124461b…` (6,294行) / increment `dc857bfd…` / increments-manifest
`017c7c30…`・BF anchor/negative CSV 4ピン (provenance chain AR→BF→BK→BM→BS→
BV→BW→BX→BY→CC→CL→CM)。val-gate baselines 4 (drive-3 kitとbyte同一確認済み)。

## 実行結果 (宣言protocol順)

1. **rules gate PASS** (0.82s): pinned `verify_tbl.js` `c8c52528…`・replica quads
   95,670 == third-impl quads 95,670・triples checked 195,044・mismatches 0。
2. **val-gate this-host 4/4 node-exact** (pinned `jsreplay.js`・published baseline
   との一致・wall_s比較外・stdout+stderr統合取得): at2m 2キー budget 2,000,000
   exhaustion (result 0, nodes 2,000,000) ×2・15m基準キー budget 15M (result 2,
   nodes 3,651,923) と (result 2, nodes 5,040,200)。本host `.cm-host.out` 4件は
   val-gate/に出版 (audit G7で機械gate)。
3. **negatives 2/2 GATE_FAIL設計どおり** (ng1: legal count mismatch derived=87
   declared=88・ng2: stone count mismatch bits=5 declared=6)。
4. **anchors 4/4 本host node-exact** (a/b determinism PASS): k02a clean WIN
   result 1・expansions 9,106,337・ttHits 4,991,527 (wall 25.98/26.03s)・l1a clean
   LOSS result 2・7,660,602 / 3,951,175 (wall 22.20/22.53s) — published第三実装値
   (Part CC/CLと同一) と同一。
5. **本host pinned-replica 2-pass fresh-cold**: aa008 p1/p2 = result 1・nodes
   **5,270,340** (wall 24/25s・published 51/52s)・aa009 p1/p2 = result 1・nodes
   **7,319,605** (wall 35/36s・published 76/50s)。published raw fieldsとのnode-exact
   一致をaudit G2bで機械検査。EXHAUSTED 0・mismatch 0。**drive-3 WIN行2行の最初の
   独立セッション再現**。
6. **targets clean WIN一致 (verdict agreement 2/2)**: aa008 third-impl a/b
   determinism PASS・result **1** (clean)・expansions 6,247,727・ttHits 3,349,810
   (wall 16.76/16.84s)・replica nodes 5,270,340との比率 1.185。aa009 result **1**
   (clean)・expansions 8,663,677・ttHits 4,539,319 (wall 23.52/23.38s)・比率
   1.183。cap 300,000,000・wallcap 240・memo-power=22・WALL-INCONCLUSIVE 0・
   DIVERGENCE 0。pass-one third-impl拡張数合計 14,911,404。**drive-3 WIN行2行の
   three-implementation corroboration成立** (published drive-3 replica 2-pass +
   本host pinned-replica 2-pass + 第三実装 minimax 2-run、すべて result 1)。

## 監査 (`audit_cm.py` `3f9a29fa…`・schema `n11-centralreply-closure-b28drive3win-thirdimpl-audit-v1`)

**ALL 101 GATES PASS**・3回実行byte一致 (audit-run1/2/3.txt 同一sha `2754d27c…`・
audit-summary-run1/2/3.json・audit-summary.json 同一sha `dcee79ed…`)・決定的
(タイムスタンプ不読)・verdict_agreements 2/2 (aa008 third=1 replica=1・aa009
third=1 replica=1)・wall_inconclusive 0。gate内訳: G0 input CSV×rows.json一致
(61-bit keyのPython int完全一致)・G1 pinned script bytes×3・rows-schema
(`consumed_into_canonical_cache: false` + `unadopted_win_rows: true` + canonical
cache sha不変pin) + target-count (2 WIN行)・G2 rules gate×2・G2b replica再現×2
targets (present/done/quads/det-pair/schema/key/verdict-vs-published)・G3
anchors×2 (clean/expansions/legal/key/det-pair)・G4 negatives×2 fail-closed・
G5 targets (key/legal/quads/det-pair/verdict-agree)・**G6 未採用WIN行補強×2
targets** (raw pin aa008/aa009 p1/p2×4・merged cache pin `3124461b…`・6,294行・
対象row不在0回・同key競合rowゼロ・increment pin aa003単一row・manifest pin +
loss_ids [aa003] + unadopted_win_ids [aa001,aa002,aa006,aa007] + row_counts wins
4·fileless 47 + 対象idがmanifest内いかなるid listにも不在〔注記文中のfileless
範囲言及"aa008..aa054"はid listでなく機械区別済み〕・merger `90711961…`)・
**G7 val-gate 4/4 node-exact**。

- **maker tamper battery 8/8検出** (scratch /tmp copy上: T1 raw aa008.p1 nodes+1・
  T2 row-audit probed 9→10・T3 README-cj文言反転・T4 status-cj aa008 PASS verdict
  反転・T5 published-input aa008 legal反転・T6 BF anchor k02a lo+1・T7 batch-keys
  aa008 s5_index+1・T8 merged cache採用aa003 row nodes+1)。全probe適用実効性
  assert・battery後の実験dir bytes不変を検証。
- **audit tamper battery 4/4検出 + clean control PASS** (scratch copy上: T1
  PIN_THIRD末尾反転 → `pin-third_impl.js` fail・T2 targets aa008.a expansions+1 →
  `target-aa008-det-pair` fail・T3 input CSV aa009 legal 91→90 →
  `input-aa009-matches-rows` fail・T4 scratch merged-cache aa003 row nodes+1 →
  `unadopted-pin-merged-cache-aa008` fail)。clean controlはbyte-identical
  audit-summary (rc=0)。実験dir bytes不変。

## 誠実な開示 (宣言に対する逸脱・補足)

- publish-then-execute規約に対し、宣言出版前に実施したのはread-only解析のみ (kit
  取得・sources sha検証・maker 4回実行byte一致)。宣言に開示済み。
- 宣言protocolの実行順の補足: audit (8)・maker tamper (9)・audit tamper (10) を
  status.log機械生成 (7) の前に実行し、PROTOCOL行は全出力確定後に出力ファイル群
  から機械生成した (Part CLと同型・判定には無影響)。
- 実装上の設計段階修正1件 (実行前): 未採用性gateの最初の設計はmanifest全文の
  raw文字列scanだったが、「(aa008..aa054)」という注記文中のfileless範囲言及が
  誤ABORTすると的事前検出し、id-list構造検査へ機械修正した (マニフェストの
  proseは正規のid listと機械区別)。fail-closed設計の作動実例。

## 状態 (verdict不消費)

**標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2 {59,60}・
class 1/2/4・class 10968・class 23964・class 5343 (54キーすべて・aa008/aa009を含む) は
どの時点でもUNKNOWNのまま。** nodes数・expansions数・ttHits数・wall秒数を勝敗として
読まない。WIN行 (aa008/aa009を含む6行) の採用判断はscrutiny owner C++第二実装
gate pin `9193f5b6…` 待ちで不変。canonical cache 6,294行 `3124461b…` はread-only
不変。EXHAUSTED 2行 (aa004/aa005) はhonest UNKNOWN。被覆・secured・root勝敗の
主張はしない。
