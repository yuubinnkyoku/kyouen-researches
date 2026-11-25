# n11-centralreply-b4loss1-b36loss40-b37loss46-adoption-reaudit-20261125 (Part DZ)

Part DZ (2026-11-25): 蓄積済み3 packet (batch-4 class 16371 e001 / 
batch-36 class 20421 40 LOSS / batch-37 class 16371 46 LOSS) の
**87 fresh LOSS行のみ**を canonical exact-S5 chain cache に採用
(loss-only adoption・mixed packets・WIN行は1行も不消費) し、
reaudit (refresh fork + delta extractor) で閉鎖表・根覆盖・update8
要求の変化を fail-closed に機械検証した。**3 packet 併合の単一
adoption Part** (pinned merger 専権・merge-audit 3回同一sha)。

**11x11 空盤は UNKNOWN。19 central-reply root も全て UNKNOWN。
本dirのどの行も root verdict を主張しない。nodes は bookkeeping。**

## 構成

- `scripts/make_increments_dz_adoption.py` maker (sha `e494346e…`)
  - b36 kit `n11-centralreply-closure-class20421-batch36-20261124/`
    (MANIFEST `f4a6d53f…` 160 files・4列形式) と b37 kit
    `n11-centralreply-closure-class16371-batch37-20261125/`
    (MANIFEST `e4a9d326…` 166 files) を file-by-file sha検証
  - batch-4 kit は MANIFEST なしのため file-by-file pin 8件
    (status `63c2d969…`・batch-keys `70b8a4c8…`・e001 both-passes
    `84a3c287…`・e002 passes `81089532…`/`1914d048…`・runbatch
    `4e47fd12…`・jsreplay `84585617…`)・b37 kit の batch4-packet
    source clones と byte-cross-verify
  - 92キー (45+47+2 probed外含む94行中の採用87) の two-pass
    fresh-cold raw 再検証・status.log 3/50/48行 honest-history 照合
    (first/final/WIN-HALT lines pin)・raw/batch-keys (legal,lo,hi,s5,mcc)
    照合・val-gate 12 molecule (b36 dx-host×4・b37 dy-host×4・b4
    this-host×4) node-exact・採用87キーと不採用7 WINキーの
    BASE 6,573行/quarantine `81d23160…` 不在・already-canonical e022
    (s5 546606) の BASE 内存在検証
  - 採用 per-pass nodes: b4 882,800・b36 159,499,387 (全45行
    183,921,575)・b37 96,295,019 (全47行 99,204,059)
- `scripts/s5_union_merge.py` pinned merger byte-clone (sha `90711961…`・
  selftest PASS・3回merge同一sha)
- `scripts/compare_deltas_dz_adoption.py` extractor (sha `cfdf6e9d…`)
- `reaudit/scripts/refresh_adoption_dz.py` refresh fork
  (sha `cbb1d2b7…`・DW `4aaabcd5…` の fork・docstring と CACHE pin
  `4a30b88d…` のみ変更)
- `output/increment-b4loss1-20261125.cache` (sha `d238c7d8…`・1行)
- `output/increment-b36loss40-20261125.cache` (sha `e6ac3627…`・40行)
- `output/increment-b37loss46-20261125.cache` (sha `835adcb0…`・46行)
- `output/increments-manifest.json` (sha `bf7817f9…`・schema
  dz-adoption-increments-manifest-v1・3 batches・`full_packet_eq_loss_only
  =false`・`win_scenario_exists=true`・unadopted WIN 7行
  {b36 d008/d009/d021/d026/d029, b37 e042, b4 e002}・EXHAUSTED 0・
  already-canonical e022 除外)
- `output/merge-audit-run{1,2,3}.json` (3回とも sha `49592ccc…`)
- `output/merged-exact-s5-chain-plus-...-plus-b37loss46-20261125.cache`
  (sha `4a30b88d…`・**6,660行・WIN 158 / LOSS 6,502**)
- `output/decomp-deltas-dz-adoption.json` (sha `45fd2ac5…`・extractor出力)
- `reaudit/output/refresh-summary.json` (sha `7f7465ab…`)
- `reaudit/output/closure-classes.csv` (sha `02641235…`・807行・
  class 16371行 = rank 4 / unknown 2 / groups 3・class 20421行 =
  rank 8 / unknown 9 / groups 4)
- `reaudit/output/per-root-coverage.csv` (sha `f7418e98…`・root 27 119/119)
- `reaudit/output/probe-worklist.csv` は体積 (~3.7MB) で非出版。
  regen pin sha `9b420875…` (refresh fork 再実行で byte一致をextractorが検証)

## 主要結果 (extractor fail-closed 検証済み・DECOMP OK)

- canonical relation: SCEN == BASE (Part DW・6,573行 `23d40e36…`) +
  87 increment rows verbatim (他は不変・WIN 158 / LOSS 6,502)
- class 16371 (Board再生成 52子境界: 1 BASE内 exact LOSS e022 s5 546606 +
  2 update8 receipt LOSS {381858, 550881} + 47 batch-37 keys + e001 + e002
  ※batch-4 packet 50キー全てが境界内): unknown **49→2** (残る2子 =
  不消費WIN {e002 s5 183566, e042 s5 550879})・rank 10→4・groups 3→3。
  **free化も excluded化もされず unknown のまま**
- class 20421 (Board再生成 50子境界: 1 BASE内 exact LOSS (s5 universe外キー
  (10378545341275312128, 131072)) + 45 batch-36 keys + 4 batch-3未出版行):
  unknown **49→9** (残る9子 = 5 b36不消費WIN {528689, 543795, 605961,
  620742, 625899} + 4 batch-3行 {38215, 197253, 259023, 300778})・
  rank 9→8・groups 4→4。**free化も excluded化もされず unknown のまま**
- 87採用キー == 16371境界own47 ∪ 20421境界own40 (重複なし)
- closure table 807行キープ・**left 4 {1530, 6241, 15393, 23410} (own 0・
  pure displacement) / entered 4 {16367, 18047, 21857, 23034} (各own 1・
  frontier改善)** = 固定サイズfrontier選択の re-selection bookkeeping
  (free化1クラスも無し・全8行own-membership Board検証)・rank churn 348行・
  unknown変化 micro-class 25件 (全てown 1)・stable 428行
- update8: resolved 214→256 (+42 = b36の40 + b37 {498207, 544907})・
  remaining 31,645→31,603・groups_free_now 131 static・win_hit []・
  no resolution lost
- class_status_counts 完全 static (excluded 390 / excluded_now 23 /
  free_now 39 / unknown 34,497)・board_verified 39/39
- per-root: free/uncovered thirds 全 root 不変・root 27 119/119・
  per-root remaining は root 1 (-4) / 12 (-80) / 26 (-4) / 37 (-80) のみ
  減少・individual greedy union は8 root で re-selection bookkeeping
  (root 26 5122→5230・36 2954→2997 は増加を含む純bookkeeping)
- joint greedy 36,943→36,511・worklist 64,535→64,420 (bookkeeping)
- 已知 universe 752→839・cache in universe 729→816

## 解釈ガード

- 7 WIN行 {d008, d009, d021, d026, d029, e042, e002} と batch-3 残4行
  {d001, d002 (WIN), d003, d004} (raws未出版) は本 Part ではどこにも
  消費されない (scrutiny-owner C++ gate pin `9193f5b6…`)
- class 16371/20421 とも不消費WIN子が残るため loss-only 採用では
  free化不可 (closure表・coverageの全変化は bookkeeping)
- 11×11 は UNKNOWN のまま。root verdict・coverage claim は本dirの
  どこにも無い
