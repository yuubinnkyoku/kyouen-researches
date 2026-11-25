# Part DZ 完了: batch-4 + batch-36 + batch-37 87-LOSS canonical adoption 完了log (2026-11-25)

単一オーナー Part DZ。宣言
`research/log/2026-11-25-part-dz-adoption-declaration.md`
(commit `f57714d1`・宣言時 observed HEAD `6247d6a5` = Part DY完了log
commit・2026-11-25T00:27:12Z時点)。commit message 機械走査で
「b4loss1」「b36loss40」「b37loss46」「Part DZ」とも total_count=0で
開始した。**11×11 空盤は UNKNOWN のまま** (本Partで採用したのは87
exact LOSS行のみ・7 WIN行 {d008, d009, d021, d026, d029, e042, e002} は
1行も不消費・batch-3 残4行 {d001, d002 (WIN), d003, d004} は raws未出版
のため本Part対象外・class 16371/20421 とも free化せず)。

## 出版物と pin (全 wave fetch-back git blob sha照合済み)

実験dir
`research/experiments/n11-centralreply-b4loss1-b36loss40-b37loss46-adoption-reaudit-20261125/`
(MANIFEST-sha256.txt 16エントリ・ローカル検証 ok 16 bad 0):

- 宣言log (wave A・commit `f57714d1`・git blob `93127c83…`)
- scripts/make_increments_dz_adoption.py `e494346e…` (wave B・commit
  `b40558b1`): maker。b36 kit MANIFEST `f4a6d53f…` (160 files・4列形式)
  と b37 kit MANIFEST `e4a9d326…` (166 files) をfile-by-file sha検証、
  batch-4 kit (MANIFESTなし) は file-level pin 8件 (status
  `63c2d969…`・batch-keys `70b8a4c8…`・e001 both-passes `84a3c287…`・
  e002 passes `81089532…`/`1914d048…`・runbatch `4e47fd12…`・jsreplay
  `84585617…`・b37のsource clone byte-cross-verify)。87キー two-pass
  fresh-cold raw再検証・status honest-history照合 (first/final/WIN-HALT
  lines pin)・raw/batch-keys (legal,lo,hi,s5,mcc) 照合・採用キーの BASE
  6,573行/quarantine `81d23160…` 不在・val-gate
- scripts/s5_union_merge.py `90711961…` (pinned merger byte-clone・
  変更なし・本Partのmerge専権)
- scripts/compare_deltas_dz_adoption.py `cfdf6e9d…` (DW版 `d20750fb…`
  のfork。verify_kit 4列MANIFEST (first=sha, last=path) 対応・WIN-HALT
  linesの行文字列精度pin・left/entered own-membership検証を追加)
- reaudit/scripts/refresh_adoption_dz.py `cbb1d2b7…` (DW `4aaabcd5…`
  のfork・CACHE pin `23d40e36…` のみ変更)
- output/increments 3本 (b4loss1 1行 `d238c7d8…`・b36loss40 40行
  `e6ac3627…`・b37loss46 46行 `835adcb0…`)・increments-manifest.json
  `bf7817f9…` (loss-only採用・WIN不採用明記)・merge-audit-run{1,2,3}.json
  3回同一 `49592ccc…`・merged cache
  `4a30b88d…` (6,660行 WIN 158 / LOSS 6,502) [wave C・commit
  `01f1fcc9`・fetch-back 8/8]
- output/decomp-deltas-dz-adoption.json `45fd2ac5…` (schema
  dz-adoption-decomp-deltas-v1)・reaudit/output/refresh-summary.json
  `7f7465ab…`・closure-classes.csv `02641235…` (807行)・
  per-root-coverage.csv `f7418e98…` (root 27 119/119)・README・
  MANIFEST-sha256.txt [wave D・commit `18e340b9`・fetch-back 6/6]
- probe-worklist.csv は体積で非出版・regen pin `9b420875…`
  (extractorがrefresh再実行でbyte一致を検証)

備考: wave D 初回pushは検証側の byte/文字数長チェックがREADMEのUTF-8
日本語で誤検知 (6,282 bytes vs 5,272 chars) したため中断した (main履歴に
痕跡なし・`01f1fcc9`と`18e340b9`は隣接)。チェック撤去後に同一bytesで
再pushして成立・fetch-back 6/6照合。

## 実行の経過 (publish-then-execute・単一host逐次)

1. wave A: 宣言log出版 (observed HEAD `6247d6a5`・racing guard
   「b4loss1」「b36loss40」「b37loss46」「Part DZ」total_count=0)
2. wave B: scripts 4出版 (fetch-back 4/4)
3. wave C: maker実行 (3-kit byte検証 → 87行 increments + manifest 生成)
   → merger ×3 (6,660行・audit 3回同一sha) → 8ファイル出版
   (fetch-back 8/8)
4. wave D: refresh fork ×2 scratch再実行 (BASE `4aaabcd5…`・adoption
   `cbb1d2b7…`) → extractor実行 (DECOMP OK changed=25 rank_churn=348
   gs_dec=0 stable=428 left=4 entered=4) → 6ファイル出版 (fetch-back 6/6)
5. wave E: 本完了log出版

## 検証の要点 (extractor fail-closed 全gate PASS)

- canonical relation: SCEN 6,660行 == BASE `23d40e36…` 6,573行 +
  87 increment rows verbatim (他は不変・WIN 158 / LOSS 6,502)
- Board機械導出: class 16371 52子 = BASE内Loss (e022 s5 546606) +
  receipt LOSS 2 {381858, 550881} + own 47 + batch-4 packet 50キー
  全て境界内 (e001採用・e002 WIN・残り48はb37再probe) → unknown 49→2
  (e002 s5 183566・e042 s5 550879・ともに不消費WIN)。class 20421 50子 =
  BASE内Loss (s5 universe外 (10378545341275312128, 131072)・verdict
  (2,0)) + own 40 + batch-3未出版4行 → unknown 49→9 (b36 WIN {528689,
  543795, 605961, 620742, 625899} + batch-3 {38215, 197253, 259023,
  300778})。87採用キー == 16371 own47 ∪ 20421 own40 (重複なし)
- closure table 807行キープ・left 4 {1530, 6241, 15393, 23410} (own 0・
  pure displacement) / entered 4 {16367, 18047, 21857, 23034} (各own 1・
  frontier改善) = 固定サイズfrontier再選択 bookkeeping・free化1クラスも
  無し・全8行 own-membership Board検証・rank churn 348行・unknown変化
  micro-class 25件 (全own 1)・stable 428行
- update8: resolved 214→256 (+42 = b36の40 + b37 {498207, 544907})・
  remaining 31,645→31,603・groups_free_now 131 static・win_hit []・
  no resolution lost
- class_status_counts 完全static (excluded 390 / excluded_now 23 /
  free_now 39 / unknown 34,497)・board_verified 39/39
- per-root: free/uncovered thirds 全root不変・root 27 119/119・
  remaining減少は root 1 (-4) / 12 (-80) / 26 (-4) / 37 (-80) のみ・
  individual greedy union 8 rootでre-selection bookkeeping (root 26
  5122→5230・36 2954→2997 は増加を含む純bookkeeping)
- joint greedy 36,943→36,511・worklist 64,535→64,420・既知universe
  752→839・cache in universe 729→816
- 87採用行合計 nodes 256,677,206/pass (b4 882,800 + b36 159,499,387 +
  b37 96,295,019)・全てbookkeeping

## 次の作業

- closure表 rank上位は class 23101 (unknown 1)・1849 (1)・2251 (1)・
  16371 (2・不消費WIN×2)・16757 (3・不消費WIN×3)・5804 (4)・34908 (9)・
  20421 (9・不消費WIN×5含む)・34269 (11)・5343 (46)
- (a) 未probeの rank上位クラス 23101/1849/2251 (unknown 1)・5804
  (unknown 4)・34908 (unknown 9・EXHAUSTED×5高budget) の次probe設計、
  (b) 7 WIN行 {d008, d009, d021, d026, d029, e042, e002} の
  scrutiny-owner C++ gate (pin `9193f5b6…`) 交叉検証、(c) batch-3 残4行
  {d001, d002 (WIN), d003, d004} raws出版後の別Part採用判定
