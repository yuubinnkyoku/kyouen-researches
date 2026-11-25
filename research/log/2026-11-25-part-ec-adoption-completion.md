# Part EC 完了: b33exh5loss2 (Part EA af003/af039 2-LOSS) canonical adoption 完了log (2026-11-25)

単一オーナー Part EC。宣言
`research/log/2026-11-25-part-ec-adoption-declaration.md`
(commit `7a5dcb5b`・宣言時 observed HEAD `bb4bd84e` = K1313 README
bullet commit・2026-11-25T03:20:27Z時点)。commit message 機械走査で
「Part EC」「b33exh5loss2」とも total_count=0で開始した。
**11×11 空盤は UNKNOWN のまま** (本Partで採用したのは Part EA b33exh5
30M re-probe の 2 exact LOSS行 (af003/af039) のみ・probe-level WIN行
af023/af048 と batch-33系不消費WIN {af029, af047, af050, af053} と
既存7 WIN行 {b36 d008/d009/d021/d026/d029, b37 e042, b4 e002} は
1行も不消費・af034 は EXHAUSTED 除外で honest UNKNOWN・class 34908 は
unknown 9→7 だが free化も excluded化もされず・class 16371/20421 は
byte-static)。

**本 Part の意味**: Part EA が事前宣言済み予算条件 30M (出版済み
15M EXHAUSTED 条件からの budget-condition upgrade) で class 34908 の
batch-33 EXHAUSTED 5キーを re-probe し、af003 (s5 153030) / af039
(s5 950512) の 2行が fresh exact LOSS に解決した (いずれも two-pass
fresh-cold node-exact)。この 2行のみを loss-only 採用した。40M系の
高予算 re-probe ではなく 30M での解決のため、EXHAUSTED 5キー中の
2キーが「未解決から解決済み exact LOSS」に正味転換した。

## 出版物と pin (全 wave fetch-back byte照合済み)

実験dir
`research/experiments/n11-centralreply-b33exh5loss2-adoption-reaudit-20261125/`
(MANIFEST-sha256.txt 14エントリ):

- 宣言log (wave A・commit `7a5dcb5b`・fetch-back blob一致
  `b7d3a264222ce717ea40bc646e2759909b1190cd`)
- scripts/make_increments_ec_adoption.py `a6a416ed…` (wave B・commit
  `e1917e58`): maker。BASE `c3026468…` 6,663行 pin・pinned merger
  pin・EA kit MANIFEST `42ba81bc…` 61 files・jsreplay `84585617…` /
  runbatch `f591f8c2…` / 30M runner `3b5083b4…`・reprobe-keys
  `3744b522…` / batch-33 keys `8a863381…` ・status `db7c7017…` (13行)・
  b33 source status `1f663fc8…` (66行) pin・2採用キー two-pass
  fresh-cold node-exact @30M (af003 23,126,072 / af039 19,234,232)・
  採用2キーと不採用 af023/af048 (WIN) と af034 (EXH) の
  BASE/quarantine 不在 (fresh-increment gate)・15M EXHAUSTED source
  raws pin [fetch-back 4/4]
- scripts/s5_union_merge.py `90711961…` (pinned merger byte-clone・
  selftest PASS・変更なし・本Partのmerge専権)
- scripts/compare_deltas_ec_adoption.py `548068c6…` (extractor・
  tamper battery 6/6 ABORT)
- reaudit/scripts/refresh_adoption_ec.py `73186e63…` (EB
  `b6b780a3…` のfork・docstring と CACHE path と CACHE pin
  `cecc1a0f…` のみ変更)
- output/increment-b33exh5loss2-20261125.cache `8f45a202…` (2行)・
  increments-manifest.json `9c89d3d8…` (schema
  b33exh5loss2-increments-manifest-v1・pool b33exh5のみ・unadopted
  WIN {af023, af048}・exhausted除外 {af034}・
  full_packet_eq_loss_only=false・採用計 42,360,304/pass・packet全体
  119,110,099/pass)・merge-audit-run{1,2,3}.json 3回同一 `47420bd0…`・
  merged cache `cecc1a0f…` (6,665行 WIN 158 / LOSS 6,507)
  [wave C・commit `39c27867`・fetch-back 6/6 blob一致]
- output/decomp-deltas-b33exh5loss2-adoption.json `8aa439aa…`
  (schema b33exh5loss2-adoption-decomp-deltas-v1)・
  reaudit/output/refresh-summary.json `936373e6…`・closure-classes.csv
  `0ae9749c…` (807行)・per-root-coverage.csv `06cd6561…`・README
  `01806039…` (blob)・MANIFEST-sha256.txt `90a1b704…` (blob)
  [wave D・commit `99577d5f`・fetch-back 6/6 blob一致]
- probe-worklist.csv は体積で非出版・regen pin `36bc6c6c…`
  (extractorがrefresh再実行でbyte一致を検証)

## 実行の経過 (publish-then-execute・単一host逐次)

1. wave A: 宣言log出版 (observed HEAD `bb4bd84e`・racing guard
   「Part EC」「b33exh5loss2」total_count=0)
2. wave B: scripts 4出版 (fetch-back 4/4 blob一致: e4a61f90 /
   a01ec2dc / bfafce5c / 224ca26a)
3. wave C: **隔離ツリーで publish-then-execute 再生** (出版済み
   scripts byte + pin済み入力 (EB cache・EA kit・graph/update8/
   board/policy/quarantine) のみから、本dist出力を全消去して
   end-to-end 再実行): maker PASS → merger selftest PASS → merger
   ×3 → 6,665行・audit 3回同一sha (全出力が最初の計算とsha完全一致:
   increment `8f45a202` / manifest `9c89d3d8` / merged `cecc1a0f` /
   audit `47420bd0`) → 6ファイル出版 [fetch-back 6/6 blob一致
   (5be48fe1 / 8797ba3f / 580361b3 ×3 / 116e9a6c)・277,523B merged
   cache も byte一致]
4. wave D: 隔離ツリーで refresh fork 実行 (summary `936373e6` /
   closure `0ae9749c` / per-root `06cd6561` / worklist regen
   `36bc6c6c` 全て最初の計算とbyte一致) → extractor 実行
   **DECOMP OK changed=0 rank_churn=0 gs_dec=0 stable=806 left=0
   entered=0** → 6ファイル出版 [fetch-back 6/6 blob一致]
5. wave E: 本完了log出版

## 検証の要点 (extractor fail-closed 全gate PASS)

- canonical relation: SCEN 6,665行 == BASE `c3026468…` 6,663行 +
  2 increment rows verbatim (他は不変・WIN 158 / LOSS 6,505→6,507)・
  merge-audit 3回同一sha `47420bd0…`
- Board機械導出: class 34908 56子境界 (全子 s5 mask universe 内で
  non-s5 子ゼロ = 47 BASE既知 exact LOSS + 9 unknown)。2採用後
  unknown 9→7 (残り = 6不消費WIN {af029 s5 900646, af047 961976,
  af050 962386, af053 962470, af023 810351, af048 962172} + 1
  still-EXHAUSTED {af034 s5 930660})・rank 8→8・groups_served 5→5。
  2採用キー == 34908境界own (16371 own==∅・20421 own==∅・重複なし)
- class 16371 / 20421: 本Part行は1本も境界内に無く closure行
  byte-static (16371: rank 4 / unknown 2 {e002, e042 不消費WIN} /
  groups 3。20421: rank 7 / unknown 6 {5 b36 WIN + d002} / groups 4)
- closure table 807行キープ・**left [] / entered [] (frontier交換
  行ゼロ・完全静態)**・rank churn 0行・unknown変化 class 0件・
  stable 806行
- update8: **完全不変** (resolved 259 static・remaining 31,600
  static・groups_free_now 131 static・win_hit []・newly-resolved ∅・
  lost ∅・per-root remaining 全root byte-static。両採用 s5
  {153030, 950512} は凍結 baseline requirement (31,859 s5) の外側で
  あり、どの resolution も変化しない — EB (+3解決) と対角的な結果)
- class_status_counts 完全static (excluded 390 / excluded_now 23 /
  free_now 39 / unknown 34,497)・Board検証 39/39 rejected 0
- per-root: free/uncovered thirds 全root不変 (root 0 7/112・root
  12 6/113・root 27 119/119)・individual greedy union は root 0
  (3006→3004) / root 12 (2893→2891) のみ純bookkeeping (per-root
  remaining は全root不変)
- joint greedy 36,511→36,509・worklist 64,417→64,415 (どちらも
  34908 frontier cost低下の純bookkeeping)・既知universe 842→844・
  cache in universe 819→821
- 2採用行合計 nodes 42,360,304/pass (af003 23,126,072 + af039
  19,234,232)・re-probe packet全体 119,110,099/pass (2採用 +
  WIN 2行 46,749,795 + af034 30,000,000)・全てbookkeeping

## 追加検証 (本レーンの副次成果)

- **隔離treeでの publish-then-execute end-to-end byte再生**: 本Part
  の全14出版物 (scripts 4 + outputs 6 + reaudit 4) が、出版済み
  script byte と pin済み入力のみから完全再現 (maker→merger×3→
  refresh→extractor、全sha pin一致)。出版bytesを出どころから独立に
  検証可能
- **Part EB reaudit outputs の独立再生成検証**: EB refresh fork
  `b6b780a3` を隔離tree再実行し、EB出版3出力 (refresh-summary
  `6ff36b6e` / closure `f2cf3c43` / per-root `cad355a8`) + worklist
  regen pin `15f95053` 全てbyte一致で再現 (EB reaudit 成果物の
  第三者再検証を兼ねる・extractorが比較のたびに自動実施)
- **tamper battery** (ローカル破壊試験・出版無し): maker 3/3 ABORT
  (status.log 1文字 / af003.p1.raw node値 1文字 / reprobe-keys.json
  1文字)。extractor 6/6 ABORT: (1) increments-manifest.json
  1箇所→ 即ABORT「manifest sha drift」・(2) SCEN closure-classes
  34908行 unknown 7→6改変→即ABORT「scenario closure-classes sha
  drift」・(3) SCEN merged cache af003行 result 2→1 bit反転→即
  ABORT「scenario cache sha drift」・(4) extractor内部pin
  EA_STATUS_LINES 13→12→即ABORT「manifest provenance drift」・
  (5) merged cache bit反転+SCEN sha pin を改変値に緩和しても
  refresh再実行gate (refresh_adoption_ec が CACHE pin を検証) が
  「merged cache sha256 drift」で拒否 (深層防御: sha pinを緩和して
  も出版済み refresh fork の pin が独立に閉じる)・(6) 内部pin
  stable行数 806→805→全refresh再実行後にABORT「rank churn 0/stable
  806 != pinned 0/805」(内部metric pin がsha照合とは独立に拘束)。
  各後 復元し原pin復帰を確認 (最終clean run PASS・decomp json
  `8aa439aa` 再現)
- **277KB cache の chunked round-trip**: merged cache (277,523B /
  6,666行) は read→join→write→cmp で byte-exact (sha `cecc1a0f`
  完全一致)。大容量出版の push 経路を壊していない
- **af034 の扱い**: 30M条件でも EXHAUSTED (nodes 30,000,000 全消費)・
  honest UNKNOWN。同一条件の再probeは禁止。より高い予算での
  re-probe には新規宣言が必要

## 次の作業

- closure表 rank上位 (本Part後): class 23101 (unknown 1)・1849 (1)・
  2251 (1)・16371 (2・不消費WIN×2 {af029, af047}系…e002/e042 gate
  待ち)・16757 (3)・5804 (4)・34908 (**7**・6不消費WIN {af023,
  af048, af029, af047, af050, af053} + af034 EXH: 高予算新規宣言
  待ち)・20421 (**6**・不消費WIN×6)・34269 (11)・5343 (46)
- (a) 不消費WIN 9+1行 {af023, af048 (b33exh5 30M), af029, af047,
  af050, af053 (batch-33), d002, d008, d009, d021, d026, d029, e042,
  e002…計測する行集合は gate側で確定} の scrutiny-owner C++ gate
  (pin `9193f5b6…`) 交叉検証: class 34908 と 20421 の free/excluded
  判定は不消費WIN子の消費判定が前提条件・
  (b) rank上位未probeクラス (23101/1849/2251 unknown 1・16757 (3)・
  5804 (4)・34269 (11)) の次probe設計・(c) af034 の高予算
  re-probe 新規宣言 (ただし 30M 全消費済み・コスト高)
- 11×11 は UNKNOWN のまま。本Partの全数量は bookkeeping であり
  root verdict・coverage の主張は本dirのどこにも無い
