# n11-centralreply-b33exh5loss2-adoption-reaudit-20261125 (Part EC)

Part EC (2026-11-25): Part EA b33exh5 30M re-probe packet
(class 34908 の batch-33 EXHAUSTED 5キー {af003, af023, af034,
af039, af048}; 予算条件 15M EXHAUSTED → 30M 再probe) のうち
**fresh LOSS行 2行のみ (af003, af039)** を canonical exact-S5 chain
cache に採用 (loss-only adoption) し、reaudit (refresh fork + delta
extractor) で閉鎖表・root coverage・update8 要求の変化を
fail-closed に機械検証した。**probe-level WIN行 af023 / af048 は1行も
消費しない** (scrutiny owner C++ 第二実装 gate pin `9193f5b6…` 専権)。
**af034 は 30M でも EXHAUSTED (nodes 30,000,000 全消費) のため
honest UNKNOWN として除外** (同一条件 re-probe 禁止・高予算
re-probe には新規宣言が必要)。

**11x11 空盤は UNKNOWN。19 central-reply root も全て UNKNOWN。
本dirのどの行も root verdict を主張しない。nodes は bookkeeping。**

## 構成

- `scripts/make_increments_ec_adoption.py` maker (sha `a6a416ed…`)
  - BASE = Part EB canonical cache `c3026468…` 6,663行 (WIN 158 /
    LOSS 6,505) pin・pinned merger `90711961…` pin・quarantine pin
  - EA kit
    `research/experiments/n11-centralreply-closure-class34908-b33exh5-reprobe30m-20261125/`
    (MANIFEST `42ba81bc…` 61 files) file-by-file sha検証・
    jsreplay `84585617…`/runbatch `f591f8c2…`/30M runner
    `3b5083b4…`・reprobe-keys `3744b522…`/batch-33 keys
    `8a863381…`/status `db7c7017…` (13行)・b33 source status
    `1f663fc8…` (66行) pin
  - 2採用キーの two-pass fresh-cold raw 再検証 (node-exact @30M:
    af003 23,126,072 / af039 19,234,232 = 採用計 42,360,304/pass・
    packet全体 119,110,099/pass)・採用2キーと不採用 af023/af048 (WIN)
    と af034 (EXH) の BASE 不在・quarantine 不在 (fresh-increment gate)・
    15M EXHAUSTED source raws pin (budget-condition upgrade)・
    status.log 13行 first/final/WIN-HALT/RETRY/EXHAUSTED 行 pin
  - tamper battery: 3/3 ABORT fail-closed(spots: status.log /
    reprobe raw / reprobe-keys.json 1文字ずつ)
- `scripts/s5_union_merge.py` pinned merger byte-clone (sha `90711961…`・
  selftest PASS・3回merge同一sha)
- `scripts/compare_deltas_ec_adoption.py` extractor
  (sha `548068c6…`・全delta pin 照合・tamper battery: 6/6 ABORT。
  manifest byte / SCEN closure byte / SCEN cache verdict bit 反転 /
  内部pin EA_STATUS_LINES / tamper+sha pin緩和の深層 (refresh再実行
  gateがmerged-cache sha driftで拒否) / 内部pin stable行数)
- `reaudit/scripts/refresh_adoption_ec.py` refresh fork
  (sha `73186e63…`・EB `b6b780a3…` の fork・docstring と CACHE
  path と CACHE pin `cecc1a0f…` のみ変更)
- `output/increment-b33exh5loss2-20261125.cache` (sha `8f45a202…`・2行)
- `output/increments-manifest.json` (sha `9c89d3d8…`・schema
  b33exh5loss2-increments-manifest-v1・pool b33exh5のみ・unadopted WIN
  {af023, af048}・exhausted除外 {af034}・
  full_packet_eq_loss_only=false)
- `output/merge-audit-run{1,2,3}.json` (3回とも sha `47420bd0…`)
- `output/merged-exact-s5-chain-plus-...-plus-b3loss3-plus-b33exh5loss2-20261125.cache`
  (sha `cecc1a0f…`・**6,665行・WIN 158 / LOSS 6,507**)
- `output/decomp-deltas-b33exh5loss2-adoption.json`
  (sha `8aa439aa…`・extractor出力)
- `reaudit/output/refresh-summary.json` (sha `936373e6…`)
- `reaudit/output/closure-classes.csv` (sha `0ae9749c…`・807行・
  class 34908行 = rank 8 / unknown 9→**7** / groups 5 (**free化も
  excluded化も不可: 6不消費WIN {af029, af047, af050, af053, af023,
  af048} + still-EXHAUSTED af034 残り**)・class 16371行 = rank 4 /
  unknown 2 / groups 3 (**byte-static**)・class 20421行 = rank 7 /
  unknown 6 / groups 4 (**byte-static**))
- `reaudit/output/per-root-coverage.csv` (sha `06cd6561…`・root 27
  119/119 static・free/uncovered thirds 全root不変)
- `reaudit/output/probe-worklist.csv` は体積で非出版。
  regen pin sha `36bc6c6c…` (refresh fork 再実行で byte一致を
  extractorが検証)

publish-then-execute: 宣言→scripts→outputs→本 commit (README/MANIFEST
+ reaudit outputs)→完了log の順に出版し、各段階で fetch-back byte検証
(blob sha1 一致)。出力物は出版済みスクリプトを隔離ツリーで
end-to-end 再実行して byte同一再生 (maker → merger x3 → refresh →
extractor、全sha pin一致) した上で出版した。

## 主要結果 (extractor fail-closed 検証済み・DECOMP OK)

- canonical relation: SCEN 6,665行 == BASE (Part EB・6,663行
  `c3026468…`) + 2 increment rows verbatim (他は不変・WIN 158 /
  LOSS 6,505 → 6,507)・merge-audit 3回同一sha
- class 34908 (Board再生成 56子境界: 全子 s5 mask universe 内で
  non-s5 子ゼロ = 47 BASE既知 exact LOSS + 9 unknown): unknown
  **9→7** (2採用後の残り7子 = 6不消費WIN {af029, af047, af050,
  af053, af023, af048} + 1 still-EXHAUSTED {af034})・rank 8→8・groups
  5→5 → **free化も excluded化もされず unknown のまま**
- class 34908 closure行補足: 上記残り7子のs5は {af029 900646, af047
  961976, af050 962386, af053 962470, af023 810351, af048 962172,
  af034 930660}
- class 16371 / class 20421: **本Partの行は1本も境界内に存在せず
  closure行は byte-static** → 変化なし・unknown のまま
- closure table 807行キープ・**left [] / entered [] (frontier交換行
  ゼロ・完全静態)**・rank churn 0行・unknown変化 class 0件・
  stable 806行
- update8: **完全不変** (両採用 s5 {153030, 950512} は凍結 baseline
  requirement の外側: resolved 259 static・remaining 31,600 static・
  per-root remaining 全root byte-static・groups_free_now 131 static・
  newly-resolved ∅・lost ∅・win_hit [])
- class_status_counts 完全 static (excluded 390 / excluded_now 23 /
  free_now 39 / unknown 34,497)・Board検証 39/39 rejected 0
- joint greedy 36,511→36,509・worklist 64,417→64,415
  (bookkeeping)・既知 universe 842→844・cache in universe 819→821
- per-root: free/uncovered thirds 全 root 不変 (root 27 119/119)。
  individual greedy union は root 0 (3006→3004) / root 12
  (2893→2891) のみ純bookkeeping変化
- 2採用行合計 nodes 42,360,304/pass (af003 23,126,072 + af039
  19,234,232)・re-probe packet全体 119,110,099/pass (2採用 +
  af023 28,933,179 + af048 17,816,616 + af034 30,000,000)・
  全てbookkeeping

## 解釈ガード

- af023 / af048 の probe-level WIN行は本 Part ではどこにも消費されない
  (scrutiny-owner C++ gate pin `9193f5b6…` 専権)。既存7 WIN行
  {b36 d008/d009/d021/d026/d029, b37 e042, b4 e002} も引き続き全て
  不消費
- af034 は 30M 条件で EXHAUSTED。**honest UNKNOWN** として本 Part の
  どこにも採用されず、同一条件の再probeは禁止 (高予算 re-probe には
  新規宣言が必要)
- class 34908 は 7 unknown子 (6不消費WIN + 1 EXH) が残るため
  loss-only 採用では free化不可 (closure表・coverageの全変化は
  bookkeeping)
- 11×11 は UNKNOWN のまま。root verdict・coverage claim は本dirの
  どこにも無い
