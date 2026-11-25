# Part EB 完了: batch-3 3-LOSS canonical adoption 完了log (2026-11-25)

単一オーナー Part EB。宣言
`research/log/2026-11-25-part-eb-adoption-declaration.md`
(commit `2d62b038`・宣言時 observed HEAD `a56083ab` = K1311 README
bullet commit・2026-11-25T01:30:50Z時点)。log ファイル名機械走査で
存在する part 文字列は …DX, DY, DZ, EA が最後で「EB」total 0、commit
message 機械走査 (直近60) でも「EB」「b3loss3」とも total_count=0
で開始した。**11×11 空盤は UNKNOWN のまま** (本Partで採用したのは
batch-3 の 3 exact LOSS行のみ・probe-level WIN行 d002 と既存7 WIN行
{b36 d008/d009/d021/d026/d029, b37 e042, b4 e002} は1行も不消費・
class 16371 は byte-static・class 20421 は unknown 9→6 だが
free化も excluded化もされず)。

**本 Part の前提発見**: Part DZ 宣言・README備考は batch-3 の4行を
「raws が未出版」のため対象外としていたが、batch-3 kit
`n11-centralreply-closure-class20421-batch-20261122/` の raws 8件
(d001..d004 × pass1/pass2) と input/batch-keys.json (49キー)・
output/status.log (5行) が main に出版済みであることを fetch-back
byte検証で確認した (DZ備考の記述は誤り)。これが EB 採用の blocked
条件を解除した。

## 出版物と pin (全 wave fetch-back byte照合済み)

実験dir
`research/experiments/n11-centralreply-b3loss3-adoption-reaudit-20261125/`
(MANIFEST-sha256.txt 14エントリ):

- 宣言log (wave A・commit `2d62b038`・fetch-back byte一致)
- scripts/make_increments_eb_adoption.py `b579677c…` (wave B・commit
  `52139ee7`): maker。BASE `4a30b88d…` 6,660行 pin・pinned merger pin・
  kit36 MANIFEST `f4a6d53f…` 160 files・b36 keys `d5918203…`/status
  `dd8c180b…` pin・b3 keys `ad05073a…` (49キー schema)/status
  `7877f4a0…` (5行・first/final/WIN-HALT lines) pin・raws 8件
  B3_RAW_SHAS 全16進pin・3採用キー two-pass fresh-cold node-exact
  (採用 per-pass 14,962,526 / packet全体 20,322,520)・採用3キーと
  d002 の BASE/quarantine 不在 (fresh-increment gate) [fetch-back 4/4]
- scripts/s5_union_merge.py `90711961…` (pinned merger byte-clone・
  変更なし・本Partのmerge専権)
- scripts/compare_deltas_eb_adoption.py `fd6ee3c9…` (extractor)
- reaudit/scripts/refresh_adoption_eb.py `b6b780a3…` (DZ
  `cbb1d2b7…` のfork・docstring と CACHE path と CACHE pin `c3026468…`
  のみ変更)
- output/increment-b3loss3-20261125.cache `94da84da…` (3行)・
  increments-manifest.json `97912a39…` (schema
  b3loss3-increments-manifest-v1・pool b3のみ・unadopted WIN {d002}・
  provenance batch3_raws_published=true)・merge-audit-run{1,2,3}.json
  3回同一 `e4dd5024…`・merged cache `c3026468…` (6,663行 WIN 158 /
  LOSS 6,505) [wave C・commit `ce51de0a`・fetch-back 6/6]
- output/decomp-deltas-b3loss3-adoption.json `c2a00125…` (schema
  b3loss3-adoption-decomp-deltas-v1)・reaudit/output/refresh-summary.json
  `6ff36b6e…`・closure-classes.csv `f2cf3c43…` (807行)・
  per-root-coverage.csv `cad355a8…`・README・MANIFEST-sha256.txt
  [wave D・commit `3a8059aa`・fetch-back 6/6]
- probe-worklist.csv は体積で非出版・regen pin `15f95053…`
  (extractorがrefresh再実行でbyte一致を検証)

## 実行の経過 (publish-then-execute・単一host逐次)

1. wave A: 宣言log出版 (observed HEAD `a56083ab`・racing guard
   「Part EB」「b3loss3」total_count=0)
2. wave B: scripts 4出版 (fetch-back 4/4 byte一致)
3. wave C: maker実行 PASS (increment 3行 + manifest 生成) →
   merger ×3 (6,663行・audit 3回同一sha) → 6ファイル出版
   (fetch-back 6/6・277KB merged cache もbyte一致)
4. wave D: refresh fork 両側 scratch再実行 (BASE cbb1d2b7 (DZ)・
   SCEN b6b780a3 (EB)・closure/per-root/worklist byte一致検証) →
   extractor実行 **DECOMP OK changed=0 rank_churn=1 gs_dec=0
   stable=804 left=0 entered=0** → 6ファイル出版 (fetch-back 6/6)
5. wave E: 本完了log出版

## 検証の要点 (extractor fail-closed 全gate PASS)

- canonical relation: SCEN 6,663行 == BASE `4a30b88d…` 6,660行 +
  3 increment rows verbatim (他は不変・WIN 158 / LOSS 6,505)・
  merge-audit 3回同一sha `e4dd5024…`・makerのemit sha equality gate
- Board機械導出: class 20421 50子 = BASE内Loss (non-s5 cache row
  (10378545341275312128, 131072)) + 45 b36 keys + 4 batch-3行 →
  unknown 9→6 (5 b36不消費WIN {528689, 543795, 605961, 620742,
  625899} + d002 WIN {197253})・rank 8→7・groups 4→4。
  class 16371 52子に本Part行は1本も無く closure行 byte-static
  (rank 4 / unknown 2 {e002, e042} / groups 3)。3採用キー ==
  20421境界own (16371 own==∅・重複なし)
- closure table 807行キープ・**left [] / entered [] (frontier交換
  bookkeeping行ゼロ・完全静態)**・rank churn 1行のみ (class 34908
  rank 7→8)・unknown変化 micro-class 0件・stable 804行
- update8: resolved 256→259 (+3 = {38215, 259023, 300778} = 採用3行)・
  remaining 31,603→31,600・groups_free_now 131 static・win_hit []・
  no resolution lost
- class_status_counts 完全static (excluded 390 / excluded_now 23 /
  free_now 39 / unknown 34,497)
- per-root: free/uncovered thirds 全root不変 (root 12 113/113・
  37 115/115・27 119/119)・remaining減少は root 12 (-6) / 37 (-6)
  のみ・individual greedy union は root 12 (2896→2893) / 37
  (3622→3620) のみ純bookkeeping
- joint greedy 36,511 static・worklist 64,420→64,417・既知universe
  839→842・cache in universe 816→819
- 3採用行合計 nodes 14,962,526/pass (d001 879,510 + d003 2,113,678 +
  d004 11,969,338)・packet全体 20,322,520/pass・全てbookkeeping

## 追加検証 (本レーンの副次成果)

- **Part DZ-87 reaudit outputs の独立再生成検証**: BASE refresh
  fork (cbb1d2b7) の scratch再実行で DZ-87 出版3出力 (closure
  `02641235…` / per-root `f7418e98…` / worklist regen pin
  `9b4208758e22be467919e09d6f83eb15443fa84b8e84495b6ff87cbae150ceae`)
  を byte一致で再現 (BASE_WORKLIST regen 90版とも全桁一致)。
  これは DZ-87 出版成果物の第三者再検証を兼ねる
- **tamper spot-check** (ローカル破壊試験・出版無し): (1) batch-3
  status.log 1文字改変 → maker 即ABORT「batch-3 packet status sha
  drift」・(2) d001.p1.out 1文字 (node値) 改変 → maker 即ABORT
  「raw d001.p1.out sha drift vs the pinned published bytes」
  (各0.14s)・復元後に raws 8件/status が原pinに復帰し採用成果物
  (increment/manifest) が完全無変化なことを確認。DZ-87 が battery
  を出版しなかった方針に倣い本Partの battery も非出版
- **pin転写誤記の訂正** (本レーン内部): extractor の B3_KEYS_SHA は
  正しくは `ad05073a845e511669d28fde3691fe9f3bf9f08eef2021039c884f1411f6dd3f`
  (3691fe9f。「3611」は誤記) など、systematic な全pin突合で
  MERGER_SHA・KIT37_KEYS_SHA (f483dbe) を含む計3箇所の転写誤記を
  原典照合で修正してから extractor を実行した。ABORT-first修正方式
  (エラーのたびに原典と突合) が有効だった
- 90版ローカルkit (b3b4b36b37loss90) は出版しない: 90 = 87+3 byte
  関係は本Partの merged cache c3026468 (== DZ-87 4a30b88d + 3 verbatim)
  として出版済みであり、独立した価値が残らないため

## 次の作業

- closure表 rank上位は class 23101 (unknown 1)・1849 (1)・2251 (1)・
  16371 (2・不消費WIN×2 {e002, e042})・16757 (3・不消費WIN×3)・
  5804 (4)・34908 (9・rank 7→8 churn・EXHAUSTED×5高budget)・
  20421 (**6**・不消費WIN×6 {5 b36 WIN + d002})・34269 (11)・
  5343 (46)
- (a) 未probeの rank上位クラス 23101/1849/2251 (unknown 1)・5804
  (unknown 4)・34908 (unknown 9・EXHAUSTED×5高budget) の次probe設計、
  (b) 8 WIN行 {d002, d008, d009, d021, d026, d029, e042, e002} の
  scrutiny-owner C++ gate (pin `9193f5b6…`) 交叉検証 (g++環境の
  別レーン)。両クラスとも不消費WIN子の消費 (採用か棄却か) が
  free/excluded 判定の前提条件
- 11×11 は UNKNOWN のまま。本Partの全数量は bookkeeping であり
  root verdict・coverage の主張は本dirのどこにも無い
