# Part BK: batch-21 (class 12643) closure WIN行 a003 の第三実装交叉検証 (verdict不消費)

part-lane: n11 central-reply 19root refresh closure (単一オーナーnote
`research/log/2026-11-22-n11-centralreply-19root-refresh-closure-batch1-single-owner-note.md`)。
declaration: note amendment commit `d93256ae` (Part BJ addendum + Part BK宣言・
実行前に出版)。

batch-21 (Part BJ・class 12643) のdrive-1で事前登録WIN-HALTが発火した
WIN行 a003 (canonical outputs `0022c8c5`・2-pass fresh-cold node-exact・
replica result 1・nodes 5,021,280・key (10412339930666631168, 4)・s5 115192・
legal 82) に対し、前例 (Part G/K/O/P/T/W/AA/AD/AG/AL/AR/AZ/BF) と同じ
pinned第三実装 (non-df-pn AND/OR minimax) によるverdict-level交叉検証を
行った。**verdict消費ゼロ**・canonical cache (6,235行 `f6649fe3…`) 不変・
採用判断はscrutiny owner (C++第二実装 gate pin `9193f5b6…`) のまま。
本実験はroot被覆・クラス閉鎖の主張をしない。

## 入力と機械導出

- source pins: published batch-21 canonical artifacts (batch-keys `1f9346a7…`
  (53キー・class 12643・a003 s5 115192 / membership 3)、canonical raw 2
  ファイル (`7f272ce3` (a003.p1)・`b8b19e61` (a003.p2)・wall_s 50/53)・
  status-b21.log `0c5d691a`・README-b21 `27dd1abf`・published a003 input
  CSV `3a3cae78` (scaffold `85d0c4d7`・MANIFEST `a38153a8`行と一致)) +
  published Part BF anchor/negative CSV 4件 (provenance chain AR→BF→BK・
  `b6174a3f`/`e13d2a6c`/`8e64b9ad`/`f19cd5a3`)。すべてcommit-pinned取得。
- maker `scripts/make_inputs_bk.py` (BF `20d52c75…`のbatch-21 adapt・
  ゲート変更点は誠実記録: batch-21 status.logはrunner 5行 (4 PASS + 1
  WIN-HALT) でWIN-ROW-DETAIL行は存在しないため、同batteryはPASS行・
  WIN-HALT行・README結果文言 (a003 WIN (result 1)・nodes 5,021,280・
  a001 LOSS文言・s5 115192 route statement) への照合に置換):
  全gate PASS・3回実行byte一致 (fail-closed・手転写ゼロ)。
  raw 2-pass node-exact (決定性field比較) + `# replay_done` + result 1
  in-budget + status.log 3-way照合 + derived-vs-published input CSV
  byte-equality (target 1 + BF anchors/negatives 4)。
- rows.json schema `n11-centralreply-closure-b21win-thirdimpl-input-v1`・
  `consumed_into_canonical_cache: false`・target 1行 (a003)。

## 手法

pinned `third_impl.js` (sha256 `08ea958f…`)・1行=1solver=1プロセス・
cap 300,000,000・wallcap 240s・`--memo-power=22`・全target/anchor a/b 2回の
determinism gate。逐次実行。negatives ng1/ng2は入力検証fall-closed
(GATE_FAIL文言)。rules gateはpinned `verify_tbl.js` (知識kit正本
jsreplay `84585617…`とrule engine TBL/wob全一致比較)。

## 結果 (verdict-level corroboration literature)

- **target 1/1 clean WIN (result 1)・replica verdict一致 1/1**:
  - **a003: third-impl WIN 5,806,719 expansions / 3,248,352 ttHits**
    (replica 5,021,280 nodes・ratio 1.16)。
  - a/b pair全同一 (determinism gate PASS・16.55s/16.57s)。
    WALL-INCONCLUSIVE 0・DIVERGENCE 0。pass-one総expansions 5,806,719。
- anchors: k02a WIN 9,106,337/4,991,527・l1a LOSS 7,660,602/3,951,175 とも
  published第三実装値 (Part G…) にnode-exact再現 (a/b同一)。
  negatives ng1/ng2は設計どおりfail-closed文言 (GATE_FAIL)。
- rules gate (`output/rules-gate.txt`): replica quads 95,670 == third-impl
  quads 95,670・triples checked 195,044 mismatches 0。
- audit (`scripts/audit.py`・BF `fa7dd5e6…`の単一target adapt・差分は
  EXP/SCHEMA/rows-schema文字列/target-count 4箇所のみ): **43/43 gates
  PASS**・3回実行byte一致 (schema
  `n11-centralreply-closure-b21win-thirdimpl-audit-v1`)。全summaryは
  `output/audit-summary.json`。
- tamper battery 3種 (スクラッチcopyで実施・本dir非接触): T1 canonical
  status.logのPASS行nodes改ざん → makerのsha pin gateがABORT捕捉・
  T2 target rawのverdict反転 (1→2) → auditのdet-pair gateがDIVERGENCE
  として捕捉 (rc=1)・T3 input CSVのlegal改ざん (82→83) → audit G0が
  捕捉 (rc=1)。復元後clean runとbyte一致。

## 意味と消費規則 (route statement・閉鎖主張なし)

batch-21 drive-1のWIN行 a003 が独立実装 (第三実装) でもclean WINで
再現された (verdict-level補強文献)。第二ホスト同時再現
(`research/log/2026-11-23-b21-drive1-second-host-replication.md`・
commit `ad487a2f`・全10 raw modulo-wall_s一致) と合わせ、a003のWIN labelは
(a) pinned df-pn replicaの2-pass node-exact×2ホスト、(b) 独立第三実装の
a/b determinism、の2系統で裏付けられた。**verdict消費ゼロ**:
19+1 unconsumed closure WIN候補 (既存19 + a003) の採用判断は
scrutiny owner (C++ gate pin `9193f5b6…`) がそのまま担当する。canonical
cache不変・いかなるcacheにも書込んでいない。batch-21 residual 49キー
(a005..a053・fresh)・runner-up rank 18 class 25835 (backup 31600) の
選定には触れていない。

**標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2
{59,60}・class 12643 (54子・53キーすべて)・その他全classは本実験の
どの時点でもUNKNOWNのまま。** nodes数・expansions数・ttHits数は簿記で
あって勝敗ではない。

## ファイル

- `scripts/`: third_impl.js (`08ea958f…` pinned byte-copy), verify_tbl.js
  (`c8c52528…`), jsreplay.js replica (`84585617…`), run_thirdimpl.sh
  (BF正本byte-copy `a0b77d83…`), make_inputs_bk.py (BK専用maker
  `e664c4e6…`), audit.py (BK向けgate battery `f20d83b9…`)。
- `input/`: rows.json + input CSV 5件 (target 1 + anchors 2 + negatives 2)。
- `sources/`: canonical batch-21 published artifacts 10ファイル +
  published Part BF anchor/negative CSV 4件。
- `output/`: rules-gate.txt・status.log・anchors 4・targets 2・negative 2・
  audit 4種 (run1.json/run1.txt/run2.txt/summary.json)。
