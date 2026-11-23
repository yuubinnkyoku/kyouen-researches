# Part BM: batch-22 (class 25835) closure WIN行 k002 の第三実装交叉検証 + 本host pinned-replica再現 (verdict不消費)

part-lane: n11 central-reply 19root refresh closure (単一オーナーnote
`research/log/2026-11-22-n11-centralreply-19root-refresh-closure-batch1-single-owner-note.md`)。
declaration: note amendment commit `578638b3` (Part BM宣言・実行前に出版・
observed HEAD-before-push `cc20473c4`)。

batch-22 (Part BL・class 25835) のdrive-1で事前登録WIN-HALTが発火した
WIN行 k002 (canonical outputs `2ed5b90`・2-pass fresh-cold node-exact・
replica result 1・nodes 10,542,704・key (1153484454560403456, 8)・s5
150241・legal 87・membership 4) に対し、前例 (Part G/K/O/P/T/W/AA/AD/
AG/AL/AR/AZ/BF/BK) と同じpinned第三実装 (non-df-pn AND/OR minimax) に
よるverdict-level交叉検証と、**宣言で事前登録した本host pinned-replica
2-pass再現** (Part BKにはなかった追加工程・Part BJ第二ホスト再現
`ad487a2f` と同型) を実行した。**verdict消費ゼロ**・canonical cache
(6,235行 `f6649fe3…`) 不変・採用判断はscrutiny owner (C++第二実装
gate pin `9193f5b6…`) のまま。本実験はroot被覆・クラス閉鎖の主張を
しない。

## 入力と機械導出

- source pins: published batch-22 canonical artifacts (batch-keys
  `b5f567bd…` (53キー・class 25835・k002 s5 150241 / membership 4)・
  canonical raw 2ファイル (`baf468a3` (k002.p1)・`0ef25c4a` (k002.p2))・
  status-b22.log `27dc7e7c`・row-audit-winhalt-b22.json `c6f7585c`・
  README-b22 `eab65d4f`・published k002 input CSV `2736d30a` (scaffold
  `106c469`・MANIFEST `a83da90`行と一致)) + published Part BF
  anchor/negative CSV 4件 (provenance chain AR→BF→BK→BM・
  `b6174a3f`/`e13d2a6c`/`8e64b9ad`/`f19cd5a3`)。すべてcommit-pinned取得。
- maker `scripts/make_inputs_bm.py` (BK `e664c4e6…`のbatch-22 adapt・
  ゲート変更点は誠実記録: batch-22 status.logはrunner 2行 (1 PASS +
  1 WIN-HALT)・batch-21の4-PASS batteryを置き換え、row-audit-winhalt
  battery (schema・win_rows [k002]・probed 1・fragment k001
  evidence=false・unprobed 52・input_sha256 pin照合) とREADME文言
  batteryを追加): 全gate PASS・4回実行byte一致 (fail-closed・手転写
  ゼロ)。raw 2-pass node-exact (決定性field比較) + `# replay_done`
  + result 1 in-budget + status/row-audit/README 3-way照合 +
  derived-vs-published input CSV byte-equality (target 1 + BF
  anchors/negatives 4)。
- rows.json schema `n11-centralreply-closure-b22win-thirdimpl-input-v1`・
  `consumed_into_canonical_cache: false`・target 1行 (k002)。

## 手法

pinned `third_impl.js` (sha256 `08ea958f…`)・1行=1solver=1プロセス・
cap 300,000,000・wallcap 240s・`--memo-power=22`・全target/anchor a/b
2回のdeterminism gate。逐次実行。negatives ng1/ng2は入力検証
fall-closed (GATE_FAIL文言)。rules gateはpinned `verify_tbl.js`
(replica jsreplay `84585617…` とrule engine TBL/wob全一致比較)。

## 結果 (verdict-level corroboration literature)

- **本host pinned-replica再現 (宣言protocol step 1)**: k002を
  fresh-cold budget 15Mで逐次2回 → **p1/p2ともに result 1・nodes
  10,542,704でpublished raw fieldsと完全一致** (two-pass node-exact・
  wall 53s/54s)。これでk002のreplica行はbatch-22実行hostと本hostの
  **2ホストで同値再現**となった。exhaustion/mismatch/truncationゼロ。
- **target 1/1 clean WIN (result 1)・replica verdict一致 1/1**:
  - **k002: third-impl WIN 12,457,901 expansions / 6,625,269 ttHits**
    (replica 10,542,704 nodes・ratio 1.18)。
  - a/b pair全同一 (determinism gate PASS・34.04s/33.95s)。
    WALL-INCONCLUSIVE 0・DIVERGENCE 0。
- anchors: **k02a WIN 9,106,337/4,991,527**・**l1a LOSS 7,660,602/
  3,951,175** ともpublished第三実装値 (Part G…) にnode-exact再現
  (a/b同一・25.29/25.51s・21.68/21.58s)。
- negatives ng1/ng2は設計どおりfail-closed文言 (ng1 GATE_FAIL
  "legal count mismatch: derived=87 declared=88"・ng2 GATE_FAIL
  "stone count mismatch: bits=5 declared=6")。
- rules gate (`output/rules-gate.txt`): replica quads 95,670 ==
  third-impl quads 95,670・triples checked 195,044 mismatches 0。
- audit (`scripts/audit.py`・BK `f20d83b9…`のbatch-22 adapt・
  新設replica-thishost gate family込み): **50/50 gates PASS**・
  3回+最終再実行の4回すべてbyte一致 (schema
  `n11-centralreply-closure-b22win-thirdimpl-audit-v1`)。
  gate内訳: input 5・script pins 3・rows-schema/target-count 2・
  rules-gate 2・replica-thishost 7・anchors 18・negatives 2・
  target 10 (決定性・鍵・legal・quads・det-pair・verdict-agree)。
- tamper battery 5種 (スクラッチcopyで実施・本dir非接触・実験files
  はbyte検証で無変更): T1a status-b22.log nodes tamper → maker sha-pin
  ABORT・T1b README-b22文言tamper → maker sha-pin ABORT・T2 target raw
  verdict反転 (1→2) → audit det-pair gateがDIVERGENCEとして捕捉
  (rc=1)・T3 input CSV legal tamper (87→88) → audit G0が捕捉 (rc=1)・
  T4 replica両pass verdict反転 (1→2) → audit
  replica-verdict-vs-published gateが捕捉 (rc=1)。

## 意味と消費規則 (route statement・閉鎖主張なし)

batch-22 drive-1のWIN行 k002 が独立実装 (第三実装) でもclean WINで
再現された (verdict-level補強文献)。さらに本host pinned-replicaが
published raw fieldsと完全一致したことで、k002のWIN labelは

- (a) pinned df-pn replicaの2-pass node-exact×2ホスト (batch-22実行
  host + 本host fresh-cold再現)、
- (b) 独立第三実装のa/b determinism pair (clean WIN)

の2系統で裏付けられた。**verdict消費ゼロ**: 21 unconsumed closure
WIN候補 (既存19 + a003 + k002) の採用判断は scrutiny owner (C++
gate pin `9193f5b6…`) がそのまま担当する。canonical cache不変・
いかなるcacheにも書込んでいない。batch-22 residual 52キー (k001
fresh-cold再実行 + k003..k053 fresh)・Part BH (`de1383a7`)・batch-23
選定 (rank 19 class 31600) には本実験では一切触れていない。

**標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2
{59,60}・class 25835 (53キーすべて・k002を含む)・class 12643・その他
全classは本実験のどの時点でもUNKNOWNのまま。** nodes数・expansions数・
ttHits数は簿記であって勝敗ではない。

## ファイル

- `scripts/`: third_impl.js (`08ea958f…` pinned byte-copy),
  verify_tbl.js (`c8c52528…`), jsreplay.js replica (`84585617…`),
  run_thirdimpl.sh (BF正本byte-copy `a0b77d83…`), make_inputs_bm.py
  (BM専用maker `d560b8cd…`), audit.py (BM向けgate battery
  `79f4b7e5…`)。
- `input/`: rows.json + input CSV 5件 (target 1 + anchors 2 +
  negatives 2)。
- `sources/`: canonical batch-22 published artifacts 11ファイル +
  published Part BF anchor/negative CSV 4件。
- `output/`: rules-gate.txt・status.log・replica 2 (本host再現raw)・
  anchors 4・targets 2・negative 2・audit 4種
  (run1.json/run1.txt/run2.txt/summary.json)。

## 再現

1. `python3 scripts/make_inputs_bm.py` (published pinsをsha検査し
   rows.json + input CSV 5件を再導出・全gate PASSで終了)。
2. `node scripts/jsreplay.js --exact-replay=input/k002.input.csv
   --exact-replay-budget=15000000` を2回 (本host replica再現・
   fresh-cold・逐次)。
3. `bash scripts/run_thirdimpl.sh ng1 a negative`・`ng2 a negative`・
   `k02a a anchor`・`k02a b anchor`・`l1a a anchor`・`l1a b anchor`・
   `k002 a target`・`k002 b target` (宣言protocol順)。
4. `node scripts/verify_tbl.js` (rules gate)。
5. `python3 scripts/audit.py` (50 gates・byte一致JSONを再生成)。

## 出版コミット

- A (scaffold 23ファイル): scripts 6 + inputs 6 + sources 11。
- B (solver outputs 16ファイル): replica 2・targets 2・anchors 4・
  negative 2・rules-gate・status.log・audit 4。
- C (本commit): README + MANIFEST-sha256 39行。
