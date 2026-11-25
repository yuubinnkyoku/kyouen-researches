# Part DZ 宣言: batch-4 (e001) + batch-36 (40 LOSS) + batch-37 (46 LOSS) の計87 LOSS行 (mixed 3-packet) の canonical adoption + reaudit deltas (2026-11-25)

単一オーナー宣言・publish-then-execute。observed HEAD `6247d6a5`
(Part DY batch-37 完了log・2026-11-25T00:27:12Z)。
Part文字は「DZ」を採用 (commit message 機械走査で「b4loss1」「b36loss40」
「b37loss46」「Part DZ」とも total_count=0。本宣言は DZ の最初の出版物)。

## 対象と目的

蓄積済み3 packet から **fresh LOSS行のみ計87行** を pinned fail-closed union
merger `907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a`
(CU byte-clone・selftest PASS・merge-audit 3回同一sha) で canonical
merged cache に採用 (merge) する。WIN行は1行も消費しない。

- batch-4 (closure class 16371・2026-11-22 宣言のみ kit): 2キー
  probe-complete (e001 LOSS + e002 WIN-HALT)。**e001 の1行のみ採用**。
  kit MANIFEST はないため file-by-file pin (status.log `63c2d969…`
  3行 honest-history・batch-keys `70b8a4c8…` 50キー・e001 両pass
  `84a3c287…` byte-identical・e002 passes `81089532…`/`1914d048…`
  field-equal・runbatch `4e47fd12…`・jsreplay `84585617…`) で検証し、
  batch-37 kit の batch4-packet source clones と byte-cross-verify済み。
  val-gate 4 molecule node-exact (this-host)
- batch-36 (closure class 20421・Part DX probe drive): 45キー
  probe-complete (40 LOSS + 5 WIN・MISMATCH 0・RETRY 0)。**40 LOSS行のみ
  採用**。kit `research/experiments/n11-centralreply-closure-class20421-batch36-20261124/`
  (MANIFEST `f4a6d53f…` 160 files・4列形式)。val-gate 4 molecule × 2 host
  (dx-host×4) node-exact
- batch-37 (closure class 16371・Part DY probe drive): 47キー
  probe-complete (46 LOSS + 1 WIN e042・already-canonical e022 は選択時除外)。
  **46 LOSS行のみ採用**。kit `research/experiments/n11-centralreply-closure-class16371-batch37-20261125/`
  (MANIFEST `e4a9d326…` 166 files)。val-gate 4 molecule × 2 host (dy-host×4)
  node-exact

- BASE = Part DW canonical merged cache・6,573行 sha256
  `23d40e36ed1730ace4986461995dfc0ee606a380da9b156cdddaf09ef8a29822`
  (WIN 158 / LOSS 6,415・DW 出版byteを改変せずそのまま pin)
- ADOPTED-CANONICAL = BASE + 87行 = 6,660行 (WIN 158 / LOSS 6,502)
  merged cache名 = DW cache名 + `-plus-b4loss1-plus-b36loss40-plus-b37loss46`:
  `merged-exact-s5-chain-plus-b28loss1-plus-b28loss7-plus-b29loss16-plus-b29loss37-plus-b31loss51-plus-b30loss43-plus-b32loss54-plus-b33loss45-plus-b35loss26-plus-b4loss1-plus-b36loss40-plus-b37loss46-20261125.cache`
  sha256
  `4a30b88dba782138585f16e1ad0ea65da55431dbc2c59250998fc5a1331349c9`

87採用行 (合計 nodes **256,677,206/pass** = 2-pass fresh-cold
node-exact、全行 decisive budget 15,000,000・published kit raws):

### batch-4 (1行・nodes 882,800/pass)

| key | lo / hi | legal | s5 | membership | result | nodes @15M |
|---|---|---|---|---|---|---|
| e001 | 10376575016706768896 / 16 | 88 | 93170 | 4 | 2 (LOSS) | 882,800 |

### batch-36 (40行・nodes 159,499,387/pass・全45行合計 183,921,575)

| key | lo / hi | legal | s5 | membership | result | nodes @15M |
|---|---|---|---|---|---|---|
| d005 | 1155173304420601856 / 131072 | 87 | 356378 | 4 | 2 (LOSS) | 2,497,042 |
| d006 | 1155173304420536320 / 131073 | 85 | 393798 | 4 | 2 (LOSS) | 2,448,235 |
| d007 | 1155173304420536352 / 131072 | 82 | 441775 | 4 | 2 (LOSS) | 2,835,651 |
| d010 | 1155173304420537344 / 131072 | 86 | 565995 | 4 | 2 (LOSS) | 4,464,813 |
| d011 | 1155173304422633472 / 131072 | 79 | 570139 | 4 | 2 (LOSS) | 9,671,556 |
| d012 | 1155173308715503616 / 131072 | 91 | 574236 | 4 | 2 (LOSS) | 3,794,414 |
| d013 | 1155182100513558528 / 131072 | 89 | 578232 | 4 | 2 (LOSS) | 5,818,726 |
| d014 | 1173187702930018304 / 131072 | 83 | 582153 | 4 | 2 (LOSS) | 3,545,649 |
| d015 | 1155173304420536320 / 135168 | 91 | 585861 | 4 | 2 (LOSS) | 4,654,637 |
| d016 | 1153062242096250880 / 532480 | 89 | 589727 | 4 | 2 (LOSS) | 3,825,579 |
| d017 | 1153062242096250880 / 17301504 | 89 | 593275 | 4 | 2 (LOSS) | 1,966,996 |
| d018 | 1153062242096250880 / 34360262656 | 88 | 596738 | 4 | 2 (LOSS) | 4,747,380 |
| d019 | 1155173304420536832 / 131072 | 88 | 602640 | 4 | 2 (LOSS) | 5,262,509 |
| d020 | 1155173304421584896 / 131072 | 85 | 605690 | 4 | 2 (LOSS) | 2,907,985 |
| d022 | 1155173306568019968 / 131072 | 80 | 608779 | 4 | 2 (LOSS) | 6,359,951 |
| d023 | 1155177702467047424 / 131072 | 89 | 611801 | 4 | 2 (LOSS) | 3,080,674 |
| d024 | 1164180503675277312 / 131072 | 91 | 614833 | 4 | 2 (LOSS) | 5,763,753 |
| d025 | 1155173304420536320 / 133120 | 86 | 617672 | 4 | 2 (LOSS) | 3,676,924 |
| d027 | 1153062242096250880 / 34078720 | 88 | 623364 | 4 | 2 (LOSS) | 3,664,311 |
| d028 | 1155173854176350208 / 131072 | 82 | 625189 | 4 | 2 (LOSS) | 1,533,976 |
| d030 | 1155173304420536576 / 131072 | 89 | 630432 | 4 | 2 (LOSS) | 4,904,993 |
| d031 | 1155175503443791872 / 131072 | 80 | 636913 | 4 | 2 (LOSS) | 4,682,372 |
| d032 | 1155173304420536320 / 132096 | 86 | 641189 | 4 | 2 (LOSS) | 3,604,850 |
| d033 | 1153062242096250880 / 557056 | 85 | 643424 | 4 | 2 (LOSS) | 2,780,990 |
| d034 | 1153062242096250880 / 67633152 | 80 | 645317 | 3 | 2 (LOSS) | 2,430,527 |
| d035 | 1155173304420536448 / 131072 | 90 | 650304 | 4 | 2 (LOSS) | 6,414,338 |
| d036 | 1155173304420798464 / 131072 | 83 | 651925 | 4 | 2 (LOSS) | 6,935,869 |
| d037 | 1155173304957407232 / 131072 | 89 | 653505 | 4 | 2 (LOSS) | 4,395,429 |
| d038 | 1155173304420536320 / 131584 | 81 | 655969 | 4 | 2 (LOSS) | 2,879,174 |
| d039 | 1153062242096250880 / 589824 | 70 | 657407 | 3 | 2 (LOSS) | 968,369 |
| d040 | 1155173304420536384 / 131072 | 90 | 662182 | 4 | 2 (LOSS) | 3,483,061 |
| d041 | 1155173304688971776 / 131072 | 85 | 664455 | 4 | 2 (LOSS) | 4,830,084 |
| d042 | 1155173304420569088 / 131072 | 81 | 669726 | 4 | 2 (LOSS) | 5,099,461 |
| d043 | 1155173304420552704 / 131072 | 84 | 671112 | 4 | 2 (LOSS) | 1,536,412 |
| d044 | 1155173304454090752 / 131072 | 85 | 671120 | 4 | 2 (LOSS) | 2,213,835 |
| d045 | 1155173373140013056 / 131072 | 80 | 671129 | 3 | 2 (LOSS) | 2,928,981 |
| d046 | 1155173304420536321 / 131072 | 84 | 671133 | 3 | 2 (LOSS) | 2,953,291 |
| d047 | 1155173304420536322 / 131072 | 82 | 671137 | 4 | 2 (LOSS) | 2,289,816 |
| d048 | 1155173304420536324 / 131072 | 85 | 671143 | 4 | 2 (LOSS) | 7,013,481 |
| d049 | 1155173304437313536 / 131072 | 86 | 671146 | 3 | 2 (LOSS) | 4,633,293 |

### batch-37 (46行・nodes 96,295,019/pass・全47行合計 99,204,059)

| key | lo / hi | legal | s5 | membership | result | nodes @15M |
|---|---|---|---|---|---|---|
| e003 | 5764888998279380992 / 16 | 88 | 306951 | 4 | 2 (LOSS) | 872,116 |
| e004 | 1153202979851993088 / 17 | 75 | 399422 | 4 | 2 (LOSS) | 2,444,351 |
| e005 | 1153202979851993088 / 18 | 92 | 480806 | 4 | 2 (LOSS) | 1,436,764 |
| e006 | 1153202979851993090 / 16 | 93 | 498207 | 4 | 2 (LOSS) | 2,044,730 |
| e007 | 1153202979851993092 / 16 | 86 | 502385 | 4 | 2 (LOSS) | 1,274,455 |
| e008 | 1153202979851993096 / 16 | 92 | 505442 | 4 | 2 (LOSS) | 2,246,752 |
| e009 | 1153202979851993104 / 16 | 85 | 509234 | 4 | 2 (LOSS) | 2,701,133 |
| e010 | 1153202979851993152 / 16 | 90 | 512923 | 4 | 2 (LOSS) | 1,323,011 |
| e011 | 1153202979851993216 / 16 | 93 | 516385 | 4 | 2 (LOSS) | 1,926,841 |
| e012 | 1153202979851993600 / 16 | 93 | 522643 | 4 | 2 (LOSS) | 1,755,039 |
| e013 | 1153202979851994112 / 16 | 87 | 525693 | 4 | 2 (LOSS) | 1,292,880 |
| e014 | 1153202979851997184 / 16 | 82 | 528188 | 3 | 2 (LOSS) | 2,504,820 |
| e015 | 1153202979852001280 / 16 | 88 | 530117 | 4 | 2 (LOSS) | 3,397,717 |
| e016 | 1153202979852009472 / 16 | 89 | 532225 | 4 | 2 (LOSS) | 1,681,334 |
| e017 | 1153202979852025856 / 16 | 87 | 534675 | 4 | 2 (LOSS) | 1,254,583 |
| e018 | 1153202979852124160 / 16 | 91 | 537035 | 4 | 2 (LOSS) | 2,163,651 |
| e019 | 1153202979852517376 / 16 | 89 | 541141 | 4 | 2 (LOSS) | 5,473,304 |
| e020 | 1153202979853041664 / 16 | 84 | 543110 | 4 | 2 (LOSS) | 3,070,360 |
| e021 | 1153202979854090240 / 16 | 92 | 544907 | 4 | 2 (LOSS) | 2,032,926 |
| e023 | 1153202979885547520 / 16 | 86 | 547319 | 4 | 2 (LOSS) | 1,261,430 |
| e024 | 1153202979919101952 / 16 | 80 | 548819 | 4 | 2 (LOSS) | 2,080,409 |
| e025 | 1154328879758835712 / 16 | 80 | 549855 | 4 | 2 (LOSS) | 2,180,425 |
| e026 | 1153202980388864000 / 16 | 87 | 550280 | 4 | 2 (LOSS) | 1,270,547 |
| e027 | 1153202980925734912 / 16 | 79 | 550330 | 4 | 2 (LOSS) | 2,851,789 |
| e028 | 1153202981999476736 / 16 | 89 | 550357 | 4 | 2 (LOSS) | 1,392,689 |
| e029 | 1153202984146960384 / 16 | 91 | 550403 | 4 | 2 (LOSS) | 2,604,085 |
| e030 | 1153203048571469824 / 16 | 74 | 550446 | 3 | 2 (LOSS) | 1,651,408 |
| e031 | 1153205178875248640 / 16 | 84 | 550549 | 4 | 2 (LOSS) | 2,186,798 |
| e032 | 1153207377898504192 / 16 | 88 | 550593 | 4 | 2 (LOSS) | 1,591,928 |
| e033 | 1153211775945015296 / 16 | 93 | 550622 | 4 | 2 (LOSS) | 1,887,012 |
| e034 | 1171217378361475072 / 16 | 86 | 550719 | 4 | 2 (LOSS) | 1,896,242 |
| e035 | 1162210179106734080 / 16 | 86 | 550757 | 4 | 2 (LOSS) | 4,309,181 |
| e036 | 1157706579479363584 / 16 | 83 | 550795 | 4 | 2 (LOSS) | 2,017,628 |
| e037 | 1154047404580798464 / 1028 | 82 | 550839 | 4 | 2 (LOSS) | 2,061,203 |
| e038 | 1154047404580798464 / 1032 | 84 | 550868 | 4 | 2 (LOSS) | 4,704,883 |
| e039 | 1153202979851993088 / 528 | 80 | 550876 | 4 | 2 (LOSS) | 1,990,057 |
| e040 | 1153202979851993088 / 1040 | 77 | 550877 | 4 | 2 (LOSS) | 2,079,262 |
| e041 | 1157425104234221568 / 268435712 | 84 | 550878 | 3 | 2 (LOSS) | 3,166,673 |
| e043 | 1157425104234217473 / 268435712 | 76 | 550880 | 3 | 2 (LOSS) | 1,348,152 |
| e044 | 1154047404580798464 / 33555456 | 87 | 550882 | 4 | 2 (LOSS) | 1,391,767 |
| e045 | 1154047404580798464 / 16778240 | 94 | 550883 | 4 | 2 (LOSS) | 1,792,096 |
| e046 | 1154047404580798464 / 17408 | 90 | 550884 | 4 | 2 (LOSS) | 1,777,014 |
| e047 | 1157425104234217474 / 268435712 | 94 | 550885 | 4 | 2 (LOSS) | 1,693,883 |
| e048 | 1154047404580798464 / 9216 | 92 | 550886 | 4 | 2 (LOSS) | 1,657,429 |
| e049 | 1154047404580798464 / 33792 | 91 | 550887 | 4 | 2 (LOSS) | 1,143,085 |
| e050 | 1154047404580798464 / 66560 | 76 | 550888 | 3 | 2 (LOSS) | 1,411,177 |

不採用 (本 Part で1行も消費しない):

- probe-level WIN 7行: batch-36 **d008** (s5 528689) / **d009** (543795) /
  **d021** (605961) / **d026** (620742) / **d029** (625899)、
  batch-37 **e042** (s5 550879)、batch-4 **e002** (s5 183566): scrutiny
  owner C++ 第二実装 gate (pin `9193f5b6…`) 通過後のみ採用可
- already-canonical **e022** (s5 546606・batch-14 q007 dual-class): BASE
  内既存行につき batch-37 選択時に除外・本 Part は何もしない
- batch-3 残4行 **{d001, d002 (WIN), d003, d004}** (s5 {38215, 197253,
  259023, 300778}・2026-11-22): **raws が未出版**のため本 Part の対象外。
  raws 出版後に別 Part で採用判定する
- EXHAUSTED 0 (3 packet とも EXHAUSTED 行は存在しない)

## class 境界 (Board再生成・extractorが fail-closed 検証)

- class 16371: 52子 = 1 BASE内 exact LOSS (e022 s5 546606) + 2 update8
  receipt LOSS (s5 {381858, 550881}) + 47 batch-37 keys (全47キーが境界内:
  46採用 + e042 WIN) + e001 (採用) + e002 (WIN) (batch-4 packet 50キー全てが
  境界内: e003..e050 minus e022 = batch-37が再probe)。87採用後の unknown 子は
  **2 (e002 s5 183566, e042 s5 550879: ともに不消費WIN)** →
  **class 16371 は free化も excluded化もされず unknown のまま**
- class 20421: 50子 = 1 BASE内 exact LOSS (s5 universe 外キー
  (10378545341275312128, 131072)) + 45 batch-36 keys (全45キーが境界内:
  40採用 + 5 WIN) + 4 batch-3未出版行。採用後の unknown 子は **9 (5 b36 WIN
  {528689, 543795, 605961, 620742, 625899} + 4 batch-3行)** →
  **class 20421 も free化も excluded化もされず unknown のまま**
- 87採用キー全体 == 16371境界own47 ∪ 20421境界own40 (重複なし・
  extractorがset等価で検証)

## reaudit (Part DW 構成の踏襲・3 packet 拡張)

- refresh fork `reaudit/scripts/refresh_adoption_dz.py` (DW `4aaabcd5…`
  の fork・docstring と CACHE pin `4a30b88d…` のみ変更。graph `54f9c364…`
  /update8 `b658290a…`/board `954d3a10…`/policy `78655e94…`/quarantine
  `81d23160…` pin不変)
- delta extractor `scripts/compare_deltas_dz_adoption.py`
  (20+ artifact sha pin・kit 160/166検証 + batch-4 file pin 8件・両 refresh
  script scratch 再実行 byte一致・Board 52子/50子境界再生成・全 delta pin 照合)

期待変化 (機械導出済み・extractorが fail-closed 検証):

- class 16371 closure行: rank 10→4・unknown 49→2・groups_served 3→3
  (static)。class 20421 closure行: rank 9→8・unknown 49→9・groups_served
  4→4 (static)
- closure table: 807行キープ (left 4 / entered 4 = 固定サイズ frontier
  選択の re-selection bookkeeping。left {1530, 6241, 15393, 23410} は
  own 0・pure displacement。entered {16367, 18047, 21857, 23034} は
  各own 1・frontier改善。**free化は1クラスも無し**)・rank churn 348行・
  unknown変化 micro-class 25件 (全て own 1・Board own-membership検証)・
  stable 428行
- update8: resolved 214→256 (+42 = b36の40 + b37 {498207, 544907}。
  e001 s5 93170 は baseline requirement 外)・remaining 31,645→31,603・
  groups_free_now 131 static・win_hit []
- class_status_counts: excluded 390 / excluded_now 23 / free_now 39 /
  unknown 34,497 完全 static (loss-only採用は何も free化しない)・
  board_verified 39/39
- root 27: 119/119 キープ。per-root remaining は root 1 (-4) / 12 (-80) /
  26 (-4) / 37 (-80) のみ減少。per-root free/uncovered thirds は全 root
  で不変。individual greedy union は8 root で re-selection bookkeeping
  (root 26 5122→5230・36 2954→2997 は増加を含む純bookkeeping)
- joint greedy 36,943→36,511・worklist 64,535→64,420 (bookkeeping)
- 既知 universe 752→839・cache in universe 729→816

**11×11 空盤は UNKNOWN のまま**。nodes は bookkeeping。WIN行は
scrutiny gate を満たさない限り一切消費しない。dir構成は DW 準拠
(scripts 3 + merger byte-clone + reaudit/{scripts,output})。
実行は publish-then-execute (宣言→scripts→outputs→reaudit outputs→
README/MANIFEST→完了log の順)。probe-worklist.csv は体積 (~3.7MB) で
非出版、regen pin `9b420875…` として extractor/refresh が検証する。
