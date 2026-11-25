# Part EB 宣言: batch-3 (d001/d003/d004 3 LOSS行・d002 WIN不採用) の canonical adoption + reaudit deltas (2026-11-25)

単一オーナー宣言・publish-then-execute。observed HEAD `a56083ab`
(K1311 README bullet・2026-11-25T01:30:50Z)。
Part文字は「EB」を採用 (log ファイル名機械走査で存在する part 文字列は
…DX, DY, DZ, EA が最後で「EB」total 0。commit message 機械走査
(直近60 commit) でも「EB」「b3loss3」とも total_count=0。本宣言は
EB の最初の出版物)。

## 対象と目的

Part DZ 宣言は batch-3 残4行 {d001, d002 (WIN), d003, d004} を
「raws が未出版」のため対象外とした。**本レーンの再確認で
batch-3 packet kit
`research/experiments/n11-centralreply-closure-class20421-batch-20261122/`
の raws 8件 (d001/d002/d003/d004 × pass1/pass2) と input/batch-keys.json
(49キー)・output/status.log (5行) が main に出版済みであることを
fetch-back byte検証で発見した** (DZ README備考の「raws未出版」は
誤り)。よって Part EB として、batch-3 packet のうち **fresh LOSS行
3行 (d001, d003, d004) のみ** を pinned fail-closed union merger
`907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a`
(CU byte-clone・selftest PASS・merge-audit 3回同一sha) で canonical
merged cache に採用する。**d002 の probe-level WIN行は1行も消費しない**
(scrutiny owner C++ 第二実装 gate pin `9193f5b6…` 専権)。

- BASE = Part DZ canonical merged cache・6,660行 sha256
  `4a30b88dba782138585f16e1ad0ea65da55431dbc2c59250998fc5a1331349c9`
  (WIN 158 / LOSS 6,502・DZ 出版byteを改変せずそのまま pin)
- ADOPTED-CANONICAL = BASE + 3行 = 6,663行 (WIN 158 / LOSS 6,505)
  merged cache名 = DZ cache名 + `-plus-b3loss3`:
  `merged-exact-s5-chain-plus-b28loss1-plus-b28loss7-plus-b29loss16-plus-b29loss37-plus-b31loss51-plus-b30loss43-plus-b32loss54-plus-b33loss45-plus-b35loss26-plus-b4loss1-plus-b36loss40-plus-b37loss46-plus-b3loss3-20261125.cache`
  sha256
  `c3026468c74b56e71f3a9e0cd45c13e4a8cba147d137c25703c5be62b9c4c94e`

3採用行 (合計 nodes **14,962,526/pass** = 2-pass fresh-cold
node-exact、全行 decisive budget 15,000,000・published kit raws):

| key | lo / hi | legal | s5 | membership | result | nodes @15M |
|---|---|---|---|---|---|---|
| d001 | 1155173304554754048 / 131072 | 77 | 38215 | 4 | 2 (LOSS) | 879,510 |
| d003 | 1155173579298443264 / 131072 | 86 | 259023 | 4 | 2 (LOSS) | 2,113,678 |
| d004 | 5766859322847924224 / 131072 | 86 | 300778 | 4 | 2 (LOSS) | 11,969,338 |

不採用 (本 Part で1行も消費しない):

- probe-level WIN 1行: batch-3 **d002** (lo 3461016313634230272 / 131072・
  legal 73・s5 197253・membership 4・nodes 5,359,994・status
  `d002 PASS 15000000,1,5359994` + `d002 WIN-HALT`): scrutiny owner C++
  第二実装 gate (pin `9193f5b6…`) 通過後のみ採用可
- 既存の不採用WIN 6行 (b36 {d008, d009, d021, d026, d029}・b37 e042・
  b4 e002) も引き続き全て不消費 (本 Part の対象外)
- EXHAUSTED 0 (batch-3 packet に EXHAUSTED 行は存在しない)

なお本 Part の採用対象は loss-only 3行のみであり、**probe 済み packet 全体の
nodes 合計 20,322,520/pass (3採用 + d002 不採用) のうち採用分のみが
canonical 化される**。

## class 境界 (Board再生成・extractorが fail-closed 検証)

- class 20421: 50子 = 1 BASE内 exact LOSS (non-s5 cache row
  (10378545341275312128, 131072)) + 45 batch-36 keys + 4 batch-3 行。
  **3採用後の unknown 子は 9→6** (残る6子 = 5 b36不消費WIN {528689,
  543795, 605961, 620742, 625899} + d002 WIN {197253})・rank 8→7・
  groups_served 4→4 (static) → **class 20421 は free化も excluded化も
  されず unknown のまま**
- class 16371: **本 Part の行は一本も境界内に存在せず、closure行は
  byte-static** (rank 4 / unknown 2 {e002, e042 不消費WIN} / groups 3)。
  → **class 16371 は変化なし・unknown のまま**
- 3採用キー全体 == 20421境界own内 (16371 own==∅・重複なし・
  extractorがset等価で検証)

## reaudit (Part DZ 構成の踏襲)

- refresh fork `reaudit/scripts/refresh_adoption_eb.py` (DZ
  `cbb1d2b753975563efa193b06a56919b6e1758ab13bcfcedc77d0bfd76751e56`
  の fork・docstring と CACHE path と CACHE pin `c3026468…` のみ変更。
  graph/update8/board/policy/quarantine pin不変)
- delta extractor `scripts/compare_deltas_eb_adoption.py`
  (kit36 MANIFEST 160 files・b3 keys `ad05073a…`/status `7877f4a0…`
  pin・両 refresh script scratch 再実行 byte一致・Board 52子/50子境界
  再生成・全 delta pin 照合)

期待変化 (機械導出済み・extractorが fail-closed 検証):

- class 20421 closure行: rank 8→7・unknown 9→6・groups_served 4→4
  (static)。class 16371 closure行: **完全不変 (byte-static)**
- closure table: 807行キープ・**left [] / entered [] (frontier交換なし・
  rank-bookkeeping exchange行ゼロ)**・rank churn 1行のみ (class 34908
  rank 7→8)・unknown変化 micro-class 0件・stable 804行
- update8: resolved 256→259 (+3 = {38215, 259023, 300778})・
  remaining 31,603→31,600・groups_free_now 131 static・win_hit []・
  per-root remaining は root 12 (-6) / 37 (-6) のみ減少
- class_status_counts: excluded 390 / excluded_now 23 / free_now 39 /
  unknown 34,497 完全 static (loss-only採用は何も free化しない)
- joint greedy 36,511 static・worklist 64,420→64,417 (bookkeeping)・
  既知 universe 839→842・cache in universe 816→819
- per-root: free/uncovered thirds 全 root 不変 (root 12 113/113・
  root 37 115/115・root 27 119/119)。individual greedy union は
  root 12 (2896→2893) / 37 (3622→3620) のみ純bookkeeping変化

**11×11 空盤は UNKNOWN のまま**。nodes は bookkeeping。WIN行は
scrutiny gate を満たさない限り一切消費しない。dir構成は DZ 準拠
(scripts 3 + merger byte-clone + reaudit/{scripts,output})。
実行は publish-then-execute (宣言→scripts→outputs→README/MANIFEST+
reaudit outputs→完了log の順)。probe-worklist.csv は体積で非出版、
regen pin
`15f95053cf50ce9f388f4b267d5bcce2cbba2f4abaf80fc57d20dfa9ab28cbb1`
として extractor/refresh が検証する。
