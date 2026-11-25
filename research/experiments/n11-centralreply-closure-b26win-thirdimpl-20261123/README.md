# Part BS: batch-26 (class 1849) closure WIN行 l028 の第三実装交叉検証 + 本host pinned-replica再現 (verdict不消費)

part-lane: n11 central-reply 19root refresh closure (単一オーナーnote
`research/log/2026-11-22-n11-centralreply-19root-refresh-closure-batch1-single-owner-note.md`)。
declaration: note amendment commit `c4dd29a6` (Part BS宣言・実行前に出版・
observed HEAD-before-push `efe21bd35`・push時点のnote blob lock
`01bd66f8` 447,798 bytes を照合)。

batch-26 (Part BQ・class 1849) のdrive-1で事前登録WIN-HALTが発火した
WIN行 l028 (canonical outputs `32fbe3bb`・scaffold `309386d5`・README+
MANIFEST `9eda46af`・2-pass fresh-cold node-exact・replica result 1・
nodes 4,893,014・key (1153485622925590528, 0)・s5 81011・legal 88・
membership 3) に対し、前例 (Part G/K/O/P/T/W/AA/AD/AG/AL/AR/AZ/BF/BK/
BM) と同じpinned第三実装 (non-df-pn AND/OR minimax) によるverdict-level
交叉検証と、**宣言で事前登録した本host pinned-replica 2-pass再現**
(Part BKにはなかった工程・Part BJ第二ホスト再現と同型) を実行した。
さらに本レーンはbatch-26 drive-1を第二ホストとして同時実行しており
(第二ホスト再現記録 `e38a49f03` 出版済み)、l028のreplica行は2ホスト
でbyte一致再現済みだった。**verdict消費ゼロ**・canonical cache
(6,235行 `f6649fe3…`) 不変・採用判断はscrutiny owner (C++第二実装
gate pin `9193f5b6…`) のまま。本実験はroot被覆・クラス閉鎖の主張を
しない。

## 入力と機械導出

- source pins: published batch-26 canonical artifacts (batch-keys
  `f1ea43ae…` (53キー・class 1849・l028 s5 81011 / membership 3)・
  canonical raw 2ファイル (l028.p1/p2 とも `1e499c11…`)・
  status-b26.log `4e167469…` (42行 = PASS 31 + WIN-HALT 1 +
  P1/P2-TRUNCATED-RETRY 10)・row-audit-winhalt-b26.json `8c91b134…`・
  README-b26 `602fb209…`・published l028 input CSV `52d79efc…`
  (scaffold `309386d5`・MANIFEST `9eda46af` 行と一致)) + published
  Part BF anchor/negative CSV 4件 (provenance chain AR→BF→BK→BM→BS・
  `b6174a3f`/`e13d2a6c`/`8e64b9ad`/`f19cd5a3`)。すべて
  commit-pinned取得。
- maker `scripts/make_inputs_bs.py` (BM `d560b8cd…`のbatch-26
  adapt・ゲート変更点は誠実記録: batch-26 status.logはrunner 42行
  battery (PASS 31 + WIN-HALT 1 + TRUNCATED-RETRY 10) でbatch-22の
  2行batteryを置き換え、**PASS key集合 == row-audit
  loss_rows∪win_rows (30+1) の機械交叉導出**、row-audit-winhalt
  battery (schema・win_rows [l028]・probed 31・pass_rows 30・
  fragment l035 evidence=false probed=false・unprobed_count 22・
  derived_state true・input_sha256 pin照合) とREADME文言battery
  (l028 WIN honest label・nodes 4,893,014・28番目の unconsumed
  closure WIN 候補・batch-27 pointer rank 26 class 13342) を追加):
  全gate PASS・4回実行byte一致 (`__pycache__`衛生・fail-closed・
  手転写ゼロ)。raw 2-pass node-exact (決定性field比較) +
  `# replay_done` + result 1 in-budget + status/row-audit/README
  3-way照合 + derived-vs-published input CSV byte-equality (target
  1 + BF anchors/negatives 4)。
- rows.json schema `n11-centralreply-closure-b26win-thirdimpl-input-v1`・
  `consumed_into_canonical_cache: false`・target 1行 (l028)。
- maker tamper battery (宣言時点・scratch上): 5/5検出 (T1 raw pin
  1bit・T2 row-audit pin 1bit・T3 README pin 1bit・T4 row-audit内容
  改変 (pass_rows 30→31)・T5 raw内容改変 (nodes 4893014→4893015))・
  clean control PASS・実験sources無改変。

## 手法

pinned `third_impl.js` (sha256 `08ea958f…`)・1行=1solver=1プロセス・
cap 300,000,000・wallcap 240s・`--memo-power=22`・全target/anchor a/b
2回のdeterminism gate。逐次実行。negatives ng1/ng2は入力検証
fall-closed (GATE_FAIL文言)。rules gateはpinned `verify_tbl.js`
(replica jsreplay `84585617…` とrule engine TBL/wob全一致比較)。

## 結果 (verdict-level corroboration literature)

- **本host pinned-replica再現 (宣言protocol step 2)**: l028を
  fresh-cold budget 15Mで逐次2回 → **p1/p2ともに result 1・nodes
  4,893,014でpublished raw fieldsと完全一致** (two-pass node-exact・
  wall 24s/25s)。これでl028のreplica行はbatch-26 drive-1実行host・
  本host (drive-1第二ホスト `e38a49f03`) の2ホストに加え、宣言
  protocol step 2の独立再現を合わせて**3系統のreplicaで同値**。
  exhaustion/mismatch/truncationゼロ。
- **rules gate (宣言protocol step 1)**: replica quads 95,670 ==
  mine quads 95,670・triples checked 195,044 mismatches 0
  (`output/rules-gate.txt`)。
- **negatives ng1/ng2 GATE_FAIL文言どおり** (legal count mismatch /
  stone count mismatch・rc=1) → **anchors k02a WIN
  9,106,337/4,991,527 (25.99s/26.15s)・l1a LOSS
  7,660,602/3,951,175 (22.42s/22.75s)** がpublished第三実装値に
  node-exact再現 (a/b同一)。
- **target 1/1 clean WIN (result 1)・replica verdict一致 1/1**:
  - **l028: third-impl WIN 5,646,148 expansions / 3,187,475 ttHits**
    (replica 4,893,014 nodes・ratio 1.154)。
  - a/b pair全同一 (determinism gate PASS・16.65s/16.60s)。
    WALL-INCONCLUSIVE 0・DIVERGENCE 0。
- これにより **l028 WIN (honest label) は (a) batch-26 drive-1
  のpinned df-pn replica 2-pass node-exact (第一ホスト)・
  (b) drive-1第二ホスト再現 `e38a49f03` (byte同一)・(c) 宣言
  protocol step 2の本host fresh-cold replica再現・(d) 独立第三実装
  a/b determinism pair の4系統で裏付けられた** (28番目の
  unconsumed closure WIN 候補・**verdict不消費**)。採用判断は
  scrutiny owner C++第二実装 gate pin `9193f5b6…` のまま。
- audit `audit.py` (BS向けgate battery `afc4da1d…`): **50/50 gates
  PASS**・3回実行byte一致 (schema
  `n11-centralreply-closure-b26win-thirdimpl-audit-v1`・gate内訳:
  input 5 + pins 3 + rows/count 2 + rules 2 + replica-thishost 7 +
  anchors 18 + negatives 2 + targets 10)。audit tamper battery
  (scratch上) 3/3検出 (T1 maker README pin反転→ABORT rc=1・
  T2 target det-pair改ざん (l028.b result 1→2)→DIVERGENCE
  `target-l028-det-pair` rc=1・T3 G0 input改ざん (legal 88→89)→
  `input-l028-matches-rows` gate fail rc=1)・clean control PASS・
  実験filesはbattery前後でbyte同一を検証 (`__pycache__`衛生)。
- UNKNOWN担保: 標準11×11空盤・19 central-reply roots・二石root
  {49,60}/{59,60}・S2 {59,60}・class 1/2/4・class 1849 (53キー
  すべて・l028を含む) は本実験のどの時点でもUNKNOWNのまま。
  nodes数・expansions数・ttHits数を勝敗として読まない。WIN/LOSS
  採用は別宣言のadoption Part (pinned fail-closed merger
  `90711961`) 経由のみ。

## ファイル

- `scripts/`: third_impl.js (pinned `08ea958f…`), verify_tbl.js
  (`c8c52528…`), jsreplay.js (pinned replica `84585617…`),
  run_thirdimpl.sh (BF正本byte-copy `a0b77d83…`),
  make_inputs_bs.py (BS専用maker `313a8d71…`), audit.py (BS向け
  gate battery `afc4da1d…`)。
- `input/`: rows.json + input CSV 5件 (target 1 + anchors 2 +
  negatives 2)。
- `sources/`: canonical batch-26 published artifacts 11ファイル +
  published Part BF anchor/negative CSV 4件。
- `output/`: rules-gate.txt・status.log・replica 2 (本host再現raw)・
  anchors 4・targets 2・negative 2・audit 4種 (audit-run1..3.txt +
  audit-summary.json)。

## 再現

1. `python3 scripts/make_inputs_bs.py` (published pinsをsha検査し
   rows.json + input CSV 5件を再導出・全gate PASSで終了)。
2. `node scripts/verify_tbl.js` (rules gate)。
3. `node scripts/jsreplay.js --exact-replay=input/l028.input.csv
   --exact-replay-budget=15000000` を2回 (本host replica再現・
   fresh-cold・逐次)。
4. `bash scripts/run_thirdimpl.sh ng1 a negative`・`ng2 a negative`・
   `k02a a anchor`・`k02a b anchor`・`l1a a anchor`・`l1a b anchor`・
   `l028 a target`・`l028 b target` (宣言protocol順)。
5. `python3 scripts/audit.py` (50 gates・byte一致JSONを再生成)。

## 出版コミット

- 宣言 note amendment `c4dd29a6` (Part BS宣言・note blob lock
  `01bd66f8`→`0910a569`・fetch-back blob照合)。※運用記録: 宣言
  push時に埋め込み変数未置換の誤コミット `f4ada6a6` (宣言本文で
  なく'...'3文字を追記) を一度成立させてしまい、直後の検証で検知
  して `c4dd29a6` が同一セッション内で修正した (base 329,972
  charsのbyte検証込み)。履歴には誤コミットが残る (誠実記録)。
- A `01851bc9` scaffold 23ファイル (scripts 6 + inputs 6 +
  sources 11)・fetch-back 23/23一致。
- B `77d3cadf` outputs 16ファイル (replica 2・targets 2・anchors
  4・negative 2・rules-gate・status.log・audit 4)・fetch-back
  16/16一致。
- C (本commit): README + MANIFEST-sha256 39行。
