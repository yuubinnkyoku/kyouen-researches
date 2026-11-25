# Part EC 宣言: b33exh5loss2 (af003/af039 2 LOSS行・af023/af048 WIN不採用・af034 EXHAUSTED除外) の canonical adoption + reaudit deltas (2026-11-25)

単一オーナー宣言・publish-then-execute。observed HEAD `bb4bd84e`
(K1313 README bullet・2026-11-25T03:20:27Z)。
Part文字は「EC」を採用 (commit message 機械走査で「Part EC」「b33exh5loss2」
とも total_count=0。本宣言は EC の最初の出版物)。

## 対象と目的

Part EA は class 34908 (batch-33 EXHAUSTED 5キー {af003, af023,
af034, af039, af048}) を 事前宣言済み予算条件 **30,000,000** (出版済み
15M EXHAUSTED 条件からの budget-condition upgrade) で re-probe した
(packet kit `research/experiments/n11-centralreply-closure-class34908-b33exh5-reprobe30m-20261125/`・
61 files MANIFEST `42ba81bc…`・全raws出版済み・status.log 13行 honest
history: first `2026-11-25T02:33:51Z af001 PASS 30000000,2,2952432` /
final `2026-11-25T03:00:04Z af048 WIN-HALT`・WIN-HALT 3行 {af029,
af023, af048}・P2-TRUNCATED-RETRY 2行 {af023, af034}・EXHAUSTED 1行
`af034 EXHAUSTED 30000000,0,30000000`)。その結果
**af003 (s5 153030) / af039 (s5 950512) の 2行が 30M 条件で fresh
exact LOSS に解決した** (いずれも two-pass node-exact)。よって Part EC
として、この **fresh LOSS行 2行のみ** を pinned fail-closed union
merger `907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a`
(CU byte-clone・selftest PASS・merge-audit 3回同一sha) で canonical
merged cache に採用する。**probe-level WIN行 af023 / af048 は1行も
消費しない** (scrutiny owner C++ 第二実装 gate pin `9193f5b6…` 専権)。
**af034 は 30M でも EXHAUSTED (honest UNKNOWN) のため除外する**
(同一条件での re-probe 禁止・より高い予算の re-probe には新規宣言が
必要)。

- BASE = Part EB canonical merged cache・6,663行 sha256
  `c3026468c74b56e71f3a9e0cd45c13e4a8cba147d137c25703c5be62b9c4c94e`
  (WIN 158 / LOSS 6,505・EB 出版byteを改変せずそのまま pin)
- ADOPTED-CANONICAL = BASE + 2行 = 6,665行 (WIN 158 / LOSS 6,507)
  merged cache名 = EB cache名 + `-plus-b33exh5loss2`:
  `merged-exact-s5-chain-plus-b28loss1-plus-b28loss7-plus-b29loss16-plus-b29loss37-plus-b31loss51-plus-b30loss43-plus-b32loss54-plus-b33loss45-plus-b35loss26-plus-b4loss1-plus-b36loss40-plus-b37loss46-plus-b3loss3-plus-b33exh5loss2-20261125.cache`
  sha256
  `cecc1a0fae126d98d8e5f23e041657b86e4d7128f80cc1182f4f9830ed1e8626`

2採用行 (合計 nodes **42,360,304/pass** = 2-pass fresh-cold
node-exact、全行 decisive budget 30,000,000・published kit raws:

| key | lo / hi | legal | s5 | result | nodes @30M |
|---|---|---|---|---|---|
| af003 | 3458764513821589505 / 68719476736 | 93 | 153030 | 2 (LOSS) | 23,126,072 |
| af039 | 1152921504607895681 / 68719476736 | 89 | 950512 | 2 (LOSS) | 19,234,232 |

不採用 (本 Part で1行も消費しない・cache のどこにも現れない):

- probe-level WIN 2行: **af023** (lo/hi 1152921504607895553 / 68719478784・
  s5 810351・nodes 28,933,179・status `af023 WIN-HALT`) と
  **af048** (lo/hi 1152921508902862849 / 68719476736・s5 962172・
  nodes 17,816,616・status `af048 WIN-HALT`): scrutiny owner C++
  第二実装 gate (pin `9193f5b6…`) 通過後のみ採用可
- EXHAUSTED 除外 1行: **af034** (lo/hi 1152921504607911937 / 68719476736・
  s5 930660・nodes 30,000,000 全消費) — 30M 条件で
  仍未解決。honest UNKNOWN として canonical cache には入れない
- 既存の不採用WIN 6行 (b36 {d008, d009, d021, d026, d029}・b37 e042・
  b4 e002) も引き続き全て不消費 (本 Part の対象外)

なお本 Part の採用対象は loss-only 2行のみであり、**re-probeされる
packet 全体の nodes 合計 119,110,099/pass (2採用 42,360,304 + WIN 2行
46,749,795 + af034 30,000,000) のうち採用分のみが canonical 化される**。

## class 境界 (Board再生成・extractorが fail-closed 検証)

- class 34908: **56子境界 (全子とも s5 mask universe 内・non-s5 子
  ゼロ)** = 47 BASE既知 exact LOSS 子 + 9 unknown 子。2採用後の
  **unknown 子は 9→7** (残る7子 = 6不消費WIN {af029 s5 900646,
  af047 961976, af050 962386, af053 962470, af023 810351, af048
  962172} + 1 still-EXHAUSTED {af034 s5 930660})・rank 8→8・
  groups_served 5→5 (static) → **class 34908 は free化も excluded化も
  されず unknown のまま**
- class 16371 / class 20421: **本 Part の行は一本も境界内に存在せず、
  closure行は byte-static** (16371: rank 4 / unknown 2 / groups 3。
  20421: rank 7 / unknown 6 / groups 4) → 変化なし・unknown のまま
- 2採用キー全体 == 34908境界own内 (16371/20421 own==∅・重複なし・
  extractorがset等価で検証)

## reaudit (Part EB 構成の踏襲)

- refresh fork `reaudit/scripts/refresh_adoption_ec.py` (EB
  `b6b780a3fd3ef81a07a052c48002fa511f016b30cae3007f199283c6f87a3b7a`
  の fork・docstring と CACHE path と CACHE pin `cecc1a0f…` のみ変更。
  graph/update8/board/policy/quarantine pin不変)
- delta extractor `scripts/compare_deltas_ec_adoption.py` (EA kit 61
  files MANIFEST・reprobe keys `3744b522…`/batch33 keys `8a863381…`/
  status `db7c7017…` (13行)/b33 source status `1f663fc8…` (66行) pin・
  jsreplay `84585617…`/runbatch `f591f8c2…`/30M runner `3b5083b4…`
  pin・両 refresh script scratch 再実行 byte一致・Board 56子境界再生成・
  全 delta pin 照合)
- maker `scripts/make_increments_ec_adoption.py` (sha
  `a6a416ed283eff0b97dfdc38defad29d387c549adc97244e4e0031cd0a528396`・
  EA kit file-by-file sha検証 + 2採用キーの two-pass fresh-cold raw
  再検証 (node-exact) + 15M EXHAUSTED source raws pin
  (budget-condition upgrade) + BASE不在・quarantine 不在
  (fresh-increment gate) + tamper fail-closed 検証済み)

期待変化 (機械導出済み・extractorが fail-closed 検証):

- class 34908 closure行: rank 8→8・unknown 9→7・groups_served 5→5。
  class 16371 / 20421 closure行: **完全不変 (byte-static)**
- closure table: 807行キープ・**left [] / entered [] (frontier交換行
  ゼロ・完全静態)**・rank churn 0行・unknown変化 class 0件・stable 806行
- update8: **完全不変** (両採用 s5 {153030, 950512} は凍結 baseline
  requirement の外側: resolved 259 static・remaining 31,600 static・
  per-root remaining 全root byte-static・groups_free_now 131 static・
  win_hit []・newly-resolved ∅・lost ∅)
- class_status_counts: excluded 390 / excluded_now 23 / free_now 39 /
  unknown 34,497 完全 static (loss-only採用は何も free化しない)
- joint greedy 36,511→36,509 (34908 frontier cost低下による
  bookkeeping)・worklist 64,417→64,415・既知 universe 842→844・
  cache in universe 819→821
- per-root: free/uncovered thirds 全 root 不変 (root 27 119/119)。
  individual greedy union は root 0 (3006→3004) / root 12 (2893→2891)
  のみ純bookkeeping変化

**11×11 空盤は UNKNOWN のまま**。nodes は bookkeeping。WIN行は
scrutiny gate を満たさない限り一切消費しない。EXHAUSTED行は honest
UNKNOWN として採用しない。dir構成は EB 準拠 (scripts 3 + merger
byte-clone + reaudit/{scripts,output})。
実行は publish-then-execute (宣言→scripts→outputs→README/MANIFEST+
reaudit outputs→完了log の順)。probe-worklist.csv は体積で非出版、
regen pin
`36bc6c6c047dff1fa2e21d4d4ceb05eb0248213b039257ea20da6fd0d8cef9cd`
として extractor/refresh が検証する。

## pin 一覧 (出版物 byte)

- maker `a6a416ed283eff0b97dfdc38defad29d387c549adc97244e4e0031cd0a528396`・
  merger byte-clone `907119610034fb2aebfde012550a4129dfa3b086c6e11194e856747ac74606a`・
  extractor `548068c6e67f6932d4d194808214b17900822a82bf3cfcc3d6b8d6cbf05cb5e7`・
  refresh fork `73186e63037cfc8ee7a1266cc0686e827abad1cd2b5ee7d8270a60ae52dbece7`
- increment `8f45a202af94faa448ac5f39f061100e3370ce9397c475c98f75cc9ea30d04a1`,
  manifest `9c89d3d8ab37359693fbed00235763d1fe539c388637e3fc06432f1afcabe80c`
  (schema b33exh5loss2-increments-manifest-v1, pool b33exh5のみ,
  unadopted WIN {af023, af048}, exhausted除外 {af034},
  full_packet_eq_loss_only=false)
- merged cache `cecc1a0fae126d98d8e5f23e041657b86e4d7128f80cc1182f4f9830ed1e8626`・
  merge-audit 3回とも
  `47420bd02bfe0403caf9bbe2bbd6c2343a89c404563076180d4acc69dcf7b74c`
- refresh-summary
  `936373e6f16cad2b5e0b08fe9177fc577a3f3a072397208aafd72f9ff0944651`・
  closure-classes
  `0ae9749c2ef1319938bc1219136b287d98e1c56051f8e34dde076e8611340d35`・
  per-root-coverage
  `06cd656193b317c25cb1ec6dab4ea771ace93a43c74ce974c0e8897576acb389`・
  decomp-deltas json
  `8aa439aa085345bb01ed7e4486d6d4911857be63f9f1c842333d30abec477674`
- BASE (EB) pin: cache `c3026468…`・refresh-summary `6ff36b6e…`・
  closure `f2cf3c43…`・per-root `cad355a8…`・worklist regen
  `15f95053…`・EB本体README/MANIFESTはEB pin参照
