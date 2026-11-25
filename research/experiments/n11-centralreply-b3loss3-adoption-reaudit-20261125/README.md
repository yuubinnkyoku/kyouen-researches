# n11-centralreply-b3loss3-adoption-reaudit-20261125 (Part EB)

Part EB (2026-11-25): batch-3 packet
`n11-centralreply-closure-class20421-batch-20261122/` (49キー・probe行4行
{d001 LOSS, d002 WIN-HALT, d003 LOSS, d004 LOSS}) のうち **fresh LOSS行
3行のみ (d001/d003/d004)** を canonical exact-S5 chain cache に採用
(loss-only adoption・probe-level WIN行 d002 は1行も不消費) し、
reaudit (refresh fork + delta extractor) で閉鎖表・root coverage・
update8
要求の変化を fail-closed に機械検証した。

**Part DZ 宣言・README備考は batch-3 の4行を「raws が未出版」として
対象外としたが、再確認の結果、batch-3 kit の raws 8件 (d001..d004 ×
pass1/pass2) と batch-keys.json (49キー)・status.log (5行) は main に
出版済みだった** (fetch-back byte検証で確認・DZ備考の記述は誤り)。
本 Part はその採用判定 Part である。

**11x11 空盤は UNKNOWN。19 central-reply root も全て UNKNOWN。
本dirのどの行も root verdict を主張しない。nodes は bookkeeping。**

## 構成

- `scripts/make_increments_eb_adoption.py` maker (sha `b579677c…`)
  - BASE = Part DZ canonical cache `4a30b88d…` 6,660行 (WIN 158 /
    LOSS 6,502) pin・pinned merger `90711961…` pin・quarantine pin
  - kit36 `n11-centralreply-closure-class20421-batch36-20261124/`
    (MANIFEST `f4a6d53f…` 160 files・4列形式) file-by-file sha検証・
    jsreplay `84585617…` pin・batch-36 keys `d5918203…`/status
    `dd8c180b…` pin
  - batch-3 published packet byte検証: keys `ad05073a…` (49キー
    schema pin)・status `7877f4a0…` (5行・first/final/WIN-HALT lines
    pin)・raws 8件 B3_RAW_SHAS 全16進pin
  - 3採用キーの two-pass fresh-cold raw 再検証 (node-exact:
    採用 per-pass 14,962,526 / packet全体 20,322,520)・採用3キーと
    不採用 d002 の BASE 不在・quarantine 不在 (fresh-increment gate)
- `scripts/s5_union_merge.py` pinned merger byte-clone (sha `90711961…`・
  selftest PASS・3回merge同一sha)
- `scripts/compare_deltas_eb_adoption.py` extractor (sha `fd6ee3c9…`)
- `reaudit/scripts/refresh_adoption_eb.py` refresh fork
  (sha `b6b780a3…`・DZ `cbb1d2b7…` の fork・docstring と CACHE path と
  CACHE pin `c3026468…` のみ変更)
- `output/increment-b3loss3-20261125.cache` (sha `94da84da…`・3行)
- `output/increments-manifest.json` (sha `97912a39…`・schema
  b3loss3-increments-manifest-v1・pool b3のみ・unadopted WIN {d002}・
  provenance {batch36_kit_files: 160, batch3_status_lines: 5,
  batch3_raws_published: true})
- `output/merge-audit-run{1,2,3}.json` (3回とも sha `e4dd5024…`)
- `output/merged-exact-s5-chain-plus-...-plus-b37loss46-plus-b3loss3-20261125.cache`
  (sha `c3026468…`・**6,663行・WIN 158 / LOSS 6,505**)
- `output/decomp-deltas-b3loss3-adoption.json` (sha `c2a00125…`・extractor出力)
- `reaudit/output/refresh-summary.json` (sha `6ff36b6e…`)
- `reaudit/output/closure-classes.csv` (sha `f2cf3c43…`・807行・
  class 16371行 = rank 4 / unknown 2 / groups 3 (**BASEとbyte-static**)・
  class 20421行 = rank 7 / unknown 6 / groups 4)
- `reaudit/output/per-root-coverage.csv` (sha `cad355a8…`・root 27 119/119
  static・free/uncovered thirds 全root不変)
- `reaudit/output/probe-worklist.csv` は体積で非出版。
  regen pin sha `15f95053…` (refresh fork 再実行で byte一致をextractorが検証)

## 主要結果 (extractor fail-closed 検証済み・DECOMP OK)

- canonical relation: SCEN 6,663行 == BASE (Part DZ・6,660行
  `4a30b88d…`) + 3 increment rows verbatim (他は不変・WIN 158 /
  LOSS 6,502 → 6,505)・merge-audit 3回同一sha
- class 16371: **本Partの行は1本も境界内に存在せず closure行は
  byte-static** (rank 4 / unknown 2 / groups 3・不消費WIN {e002, e042}
  の2子のみ)。**free化も excluded化もされず unknown のまま**
- class 20421 (Board再生成 50子境界: 1 BASE内 exact LOSS (non-s5 cache
  row (10378545341275312128, 131072)) + 45 batch-36 keys + 4 batch-3 行):
  unknown **9→6** (残る6子 = 5 b36不消費WIN {528689, 543795, 605961,
  620742, 625899} + d002 WIN {197253})・rank 8→7・groups 4→4。
  **free化も excluded化もされず unknown のまま**
- closure table 807行キープ・**left [] / entered [] (frontier交換行
  ゼロ・完全静態)**・rank churn 1行のみ (class 34908 rank 7→8)・
  unknown変化 micro-class 0件・stable 804行
- update8: resolved 256→259 (+3 = {38215, 259023, 300778} = 採用3行
  そのもの)・remaining 31,603→31,600・groups_free_now 131 static・
  win_hit []・no resolution lost
- class_status_counts 完全 static (excluded 390 / excluded_now 23 /
  free_now 39 / unknown 34,497)
- per-root: free/uncovered thirds 全 root 不変 (root 12 113/113・
  root 37 115/115・root 27 119/119)・per-root remaining は root 12 (-6) /
  37 (-6) のみ減少・individual greedy union は root 12 (2896→2893) /
  37 (3622→3620) のみ純bookkeeping (増減付き)
- joint greedy 36,511 static・worklist 64,420→64,417 (bookkeeping)・
  既知 universe 839→842・cache in universe 816→819
- 3採用行合計 nodes 14,962,526/pass (d001 879,510 + d003 2,113,678 +
  d004 11,969,338)・probe packet全体 20,322,520/pass・全てbookkeeping

## 解釈ガード

- d002 の probe-level WIN行と既存7 WIN行 {b36 d008/d009/d021/d026/d029,
  b37 e042, b4 e002} は本 Part ではどこにも消費されない
  (scrutiny-owner C++ gate pin `9193f5b6…` 専権)
- class 16371/20421 とも不消費WIN子が残るため loss-only 採用では
  free化不可 (closure表・coverageの全変化は bookkeeping)
- 11×11 は UNKNOWN のまま。root verdict・coverage claim は本dirの
  どこにも無い
