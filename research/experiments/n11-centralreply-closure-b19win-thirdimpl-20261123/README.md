# Part BF: batch-19 (class 16513) closure WIN行 w001/w002 の第三実装交叉検証 (verdict不消費)

part-lane: n11 central-reply 19root refresh closure (単一オーナーnote
`research/log/2026-11-22-n11-centralreply-19root-refresh-closure-batch1-single-owner-note.md`)。
declaration: note amendment commit `511ae474` (observed HEAD-before-push
`9719e926`, note blob lock `eb6066e6`)、**実行前に出版**。

batch-19 (Part BE・class 16513) 最初のwaveで得られた2つのWIN行
(w001 6,639,780 nodes / w002 7,738,714 nodes・2-pass fresh-cold node-exact・
budget 15M内・publication commits `49c3bea7`/`51e73082`/`9719e926`) に対し、
前例 (Part G/K/O/P/T/W/AA/AD/AG/AL/AR/AZ) と同じpinned第三実装
(non-df-pn AND/OR minimax) によるverdict-level交叉検証を行った。
**verdict消費ゼロ**・canonical cache (6,182行 `0b594f7e…`) 不変・
採用判断はscrutiny owner (C++第二実装 gate pin `9193f5b6…`) のまま。
本実験はroot被覆・クラス閉鎖の主張をしない。

## 入力と機械導出

- source pins: published batch-19 artifacts (batch-keys `9609aaf3…`
  (53キー・class 16513・w001 s5 63802 / w002 s5 109169)、
  raw 4ファイル (`8cf13d13`×2 (w001 p1/p2 byte同一・wall_s 67/67)・
  `1faf8d15`/`feb8475b` (w002・wall_s 81/67))、status-b19.log `e3a9e5b4`、
  README-b19 `29c7ea51`、published input CSV w001 `f232a593`/w002 `574a4124`)
  + published Part AR anchor/negative CSV 4件。すべてcommit-pinned取得、
  batch-19 published MANIFEST (remote byte一致確認済み) と照合。
- maker `scripts/make_inputs_bf.py`: 全gate PASS・3回実行byte一致
  (fail-closed・手転写ゼロ)。raw 2-pass node-exact (決定性field比較) +
  `# replay_done` + result 1 in-budget、status-b19.logとrawの3-way一致
  (PASS行・WIN-HALT行・WIN-ROW-DETAIL行 (s5 index・holder classes 1363/2901
  込み)・VAL-GATE 4/4行・EXECUTION-HALTED行・51-unprobed行・19候補行)、
  README結果節照合 (`**w001: WIN (result 1)**`/`**w002: WIN (result 1)**`/
  nodes 6,639,780/7,738,714)、derived-vs-published input CSV byte-equality
  (targets 2 + AR anchors/negatives 4)。
- rows.json schema `n11-centralreply-closure-b19win-thirdimpl-input-v1`、
  `consumed_into_canonical_cache: false`。

## 手法

pinned `third_impl.js` (sha256 `08ea958f…`)・1行=1solver=1プロセス・
cap 300,000,000・wallcap 240s・`--memo-power=22`・全target/anchor a/b 2回の
determinism gate。逐次実行 (Part AXのCPU quota半減観測を継承)。
negatives ng1/ng2は入力検証fall-closed (GATE_FAIL文言)。

## 結果 (verdict-level corroboration literature)

- **targets 2/2 clean WIN (result 1)・replica verdict一致 2/2**:
  - **w001: third-impl WIN 7,682,625 expansions / 4,336,161 ttHits**
    (replica 6,639,780 nodes・ratio 1.16)。
  - **w002: third-impl WIN 8,988,730 expansions / 5,106,247 ttHits**
    (replica 7,738,714 nodes・ratio 1.16)。
  - a/b pair全同一 (determinism gate PASS)。pass-one総expansions 16,671,355。
    WIN 2・LOSS 0・WALL-INCONCLUSIVE 0・DIVERGENCE 0。
- anchors: k02a WIN 9,106,337/4,991,527・l1a LOSS 7,660,602/3,951,175 とも
  published第三実装値にnode-exact再現 (a/b同一)。negatives ng1/ng2は
  設計どおりfail-closed文言 (GATE_FAIL)。
- rules gate (`output/rules-gate.txt`): replica quads 95,670 == third-impl
  quads 95,670・triples checked 195,044 mismatches 0。
- audit (`scripts/audit.py`): **53/53 gates PASS**・2回実行byte一致
  (schema `n11-centralreply-closure-b19win-thirdimpl-audit-v1`)。全summaryは
  `output/audit-summary.json`。

## 意味と消費規則 (route statement・閉鎖主張なし)

batch-19最初のwaveの2つのWIN (w001/w002) が独立実装 (第三実装) でも
clean WINで再現された (verdict-level補強文献)。**verdict消費ゼロ**:
19 unconsumed closure WIN候補 (17 prior + w001 + w002) の採用判断は
scrutiny owner (C++ gate `9193f5b6…`) がそのまま担当する。canonical cache
不変・いかなるcacheにも書込んでいない。batch-19残51キー (w003..w053・
fresh)・batch-20 pivot (rank 16 class 5687) には触れていない。

**標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2 {59,60}・
class 16513 (残51子)・全53キーは本実験のどの時点でもUNKNOWNのまま。**
nodes数・expansions数・ttHits数は簿記であり勝敗ではない。

## ファイル

- `scripts/`: third_impl.js (`08ea958f…` pinned byte-copy), verify_tbl.js
  (`c8c52528…`), jsreplay.js (`84585617…`), run_thirdimpl.sh (汎用),
  make_inputs_bf.py (BF専用maker), audit.py (BF向けgate battery)。
- `input/`: rows.json + input CSV 6件 (targets 2 + anchors 2 + negatives 2)。
- `sources/`: published batch-19 raw 4 + status-b19.log + batch-keys-b19.json
  + README-b19.md + published-input 2 + published-input-ar 4 (AR正本CSV)。
- `output/`: targets a/b 4、anchors a/b 4、negatives 2、rules-gate.txt、
  status.log、audit-summary.json、audit-run1/2。
- `MANIFEST-sha256.txt`: 全ファイル明示列挙 (glob不使用・再帰なし)。
