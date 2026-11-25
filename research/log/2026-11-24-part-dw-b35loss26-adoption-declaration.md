# Part DW 宣言: batch-35 (closure class 16757) 26 LOSS行 (probe-complete・mixed packet) の canonical adoption + reaudit deltas (2026-11-24)

単一オーナー宣言・publish-then-execute。observed HEAD `4d2d506a`
(K1307(仮) REMO lane・2026-11-24T22:03:42Z)。
Part文字は「DW」を採用 (直近 main の commit message 機械走査で
「b35loss26」は total_count=0、「Part DW」も total_count=0。本宣言は
DW の最初の出版物)。

## 対象と目的

Part DV batch-35 (closure class 16757) は probe-complete で、published kit
(`research/experiments/n11-centralreply-closure-class16757-batch35-20261124/`・
MANIFEST `791996c1…` 109 files) の全28キーが honest two-pass fresh-cold
label (budget 15M・status.log 30行 = 28 PASS verdict行 {26 LOSS, 2 WIN} +
2 WIN-HALT marker・EXHAUSTED 0・RETRY 0・MISMATCH 0) を持つ。**mixed
packet から26行の fresh LOSS行のみを** pinned fail-closed union merger
`907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a`
(CU byte-clone・selftest PASS) で canonical merged cache に採用 (merge)
する:

- BASE = Part DT canonical merged cache・6,547行 sha256
  `973bcd19309eae1d73b26c40c3d6839a2f35baa74658e0794f19da6f9412ca5b`
  (WIN 158 / LOSS 6,389・DT 出版byteを改変せずそのまま pin)
- ADOPTED-CANONICAL = BASE + 26行 = 6,573行 (WIN 158 / LOSS 6,415)
  merged cache名 = DT cache名 + `-plus-b35loss26`:
  `merged-exact-s5-chain-plus-b28loss1-plus-b28loss7-plus-b29loss16-plus-b29loss37-plus-b31loss51-plus-b30loss43-plus-b32loss54-plus-b33loss45-plus-b35loss26-20261124.cache`
  sha256
  `23d40e36ed1730ace4986461995dfc0ee606a380da9b156cdddaf09ef8a29822`
  (6,573行)

26採用行 (合計 nodes **67,593,391/pass** = 2-pass fresh-cold node-exact、
全行 decisive budget 15,000,000・published batch-35 kit raws):

| key | lo / hi | legal | s5 | membership | result | nodes @15M |
|---|---|---|---|---|---|---|
| b021 | 1153204079095218176 / 65536 | 83 | 535179 | 4 | 2 (LOSS) | 2,770,116 |
| b022 | 1153204079095316480 / 65536 | 79 | 537545 | 4 | 2 (LOSS) | 2,713,847 |
| b023 | 1153204079095447552 / 65536 | 76 | 539592 | 4 | 2 (LOSS) | 720,025 |
| b024 | 1153204079095709696 / 65536 | 83 | 541610 | 4 | 2 (LOSS) | 3,705,880 |
| b025 | 1153204079097282560 / 65536 | 87 | 545364 | 4 | 2 (LOSS) | 3,468,028 |
| b026 | 1153204079111962624 / 65536 | 72 | 546902 | 3 | 2 (LOSS) | 1,067,011 |
| b027 | 1153204079128739840 / 65536 | 75 | 548070 | 4 | 2 (LOSS) | 1,974,075 |
| b028 | 1153204079162294272 / 65536 | 83 | 549153 | 4 | 2 (LOSS) | 1,173,126 |
| b029 | 1153204079632056320 / 65536 | 81 | 551777 | 4 | 2 (LOSS) | 2,722,700 |
| b030 | 1153204081242669056 / 65536 | 87 | 554104 | 4 | 2 (LOSS) | 4,019,890 |
| b031 | 1153204083390152704 / 65536 | 86 | 555161 | 4 | 2 (LOSS) | 2,770,498 |
| b033 | 1153206278118440960 / 65536 | 83 | 558018 | 4 | 2 (LOSS) | 2,517,807 |
| b034 | 1153208477141696512 / 65536 | 84 | 558054 | 4 | 2 (LOSS) | 1,461,826 |
| b035 | 1153212875188207616 / 65536 | 83 | 558079 | 4 | 2 (LOSS) | 1,871,250 |
| b036 | 1171218477604667392 / 65536 | 84 | 558120 | 4 | 2 (LOSS) | 3,697,849 |
| b037 | 1157707678722555904 / 65536 | 72 | 558183 | 4 | 2 (LOSS) | 1,372,777 |
| b038 | 1152922604118507520 / 65792 | 86 | 558228 | 4 | 2 (LOSS) | 5,301,385 |
| b039 | 1152922604185583616 / 65792 | 82 | 558261 | 4 | 2 (LOSS) | 1,109,565 |
| b040 | 1152922741557428224 / 65792 | 81 | 558283 | 4 | 2 (LOSS) | 1,939,794 |
| b041 | 1152922604118474756 / 65792 | 88 | 558334 | 4 | 2 (LOSS) | 4,022,755 |
| b042 | 1152922604118474754 / 65792 | 88 | 558367 | 4 | 2 (LOSS) | 3,914,018 |
| b043 | 1152922604118474753 / 65792 | 78 | 558393 | 3 | 2 (LOSS) | 2,503,635 |
| b044 | 1152922604118491136 / 65792 | 80 | 558410 | 4 | 2 (LOSS) | 3,184,076 |
| b045 | 1152922604118482944 / 65792 | 87 | 558443 | 4 | 2 (LOSS) | 4,325,847 |
| b046 | 1152922604152029184 / 65792 | 81 | 558486 | 4 | 2 (LOSS) | 1,811,583 |
| b047 | 1152922604135251968 / 65792 | 74 | 558506 | 3 | 2 (LOSS) | 1,454,028 |
不採用 (本 Part で1行も消費しない):

- probe-level WIN **b032** (s5 556117, nodes 2,678,305) / **b048**
  (s5 558553, nodes 3,485,963): scrutiny owner C++ 第二実装 gate
  (pin `9193f5b6…`) 通過後のみ採用可
- batch-1 probe-level WIN **b018** (s5 528497・2026-11-22): batch-35 packet
  外 (key set から除外済み)・引続き不消費
- EXHAUSTED 0 (batch-35 に EXHAUSTED 行は存在しない)

## class 16757 境界 (Board再生成・extractorが fail-closed 検証)

49子 = 19 BASE内 exact LOSS + 1 update8 receipt LOSS (s5 558600) +
28 batch-35 keys + b018。26採用後の unknown 子は **3 (b018, b032, b048
全て不消費WIN)** → **class 16757 は free化も excluded化もされず unknown
のまま** (closure table 807行キープ・left/entered 0)。

## reaudit (Part DT 構成の踏襲)

- refresh fork `reaudit/scripts/refresh_adoption_b35loss26.py` (DT
  `5533b3f9…` の fork・docstring と CACHE pin `23d40e36…` のみ変更。
  graph `54f9c364…`/update8 `b658290a…`/board `954d3a10…`/policy
  `78655e94…`/quarantine `81d23160…` pin不変)
- delta extractor `scripts/compare_deltas_b35loss26_adoption.py`
  (20+ artifact sha pin・kit 109検証・両 refresh script scratch 再実行
  byte一致・Board 49子境界再生成・全 delta pin 照合)

期待変化 (機械導出・extractorが fail-closed 検証):

- class 16757 closure行: rank 7→4・unknown 29→3・groups_served 5→5
  (static)
- closure table: 807行キープ・rank churn 28行・unknown変化 micro-class
  2件 (30118: 55→54 own 1 / 30484: 54→52 own 2・Board own-membership検証)
- update8: resolved 188→214 (+26 = 採用26 s5全てが baseline requirement
  内)・remaining 31,671→31,645・groups_free_now 131 static
- class_status_counts: excluded 390 / excluded_now 23 / free_now 39 /
  unknown 34,497 完全 static (loss-only採用は何も free化しない)
- root 27: 119/119 キープ。per-root remaining は root 36 (-78) / 48 (-52)
  のみ減少。per-root free/uncovered thirds は全 root で不変
- joint greedy 36,849→36,943 (+94・re-selection bookkeeping)・worklist
  64,564→64,535 (bookkeeping)
- 既知 universe 726→752・cache in universe 703→729

**11×11 空盤は UNKNOWN のまま**。nodes は bookkeeping。WIN行は
scrutiny gate を満たさない限り一切消費しない。dir構成は DT 準拠
(scripts 3 + merger byte-clone + reaudit/{scripts,output})。
実行は publish-then-execute (宣言→scripts→outputs→reaudit outputs→
完了log の順)。
