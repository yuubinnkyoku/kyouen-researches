# Part DN 宣言: batch-30 (closure class 34269) 43 LOSS行 (54キー中・11 WIN行不採用) の canonical adoption + reaudit deltas (2026-11-24)

単一オーナー宣言・publish-then-execute。observed HEAD `6a6e3a340`
(Part DK takeover完了log・2026-11-24T11:54:30Z)。
Part文字は「DN」を採用 (直近100 commit機械走査で使用中の Part D* は
DF/DG/DH/DK/DL/DM のみ・当日の DB/DI/DJ と対峙せず・research/log配下に
`-part-dn-` は存在せず。本宣言は DN の最初の出版物)。

## 対象と目的

batch-30 (closure class 34269) の drive・DJ 20M再probe・DK 25M再probeで
probe-complete となった published証拠 (全54キー honest label) のうち、
**43 fresh LOSS行** を pinned fail-closed union merger
`907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a`
(CU byte-clone・selftest PASS) で canonical merged cache に採用 (merge) する:

- BASE = Part DL canonical 6,405行 `60222707dd13902103fc8f7ef11c8487ec1be531ad0711e23e50c32154e30b84` (WIN 158 / LOSS 6,247)
- ADOPTED-CANONICAL = BASE + 43行 = 6,448行 (予想・WIN 158 / LOSS 6,290)

43行 (合計 nodes **346,729,500/pass** = 2-pass fresh-cold node-exact):

- 38行 @ budget 15,000,000 (published batch-30 kit raws)
- 4行 @ budget 20,000,000 (published Part DJ exh6-20M reprobe kit raws: ac032/ac036/ac044/ac047)
- 1行 @ budget 25,000,000 (published Part DK 25M再probe kit raws: ac013)

| key | lo / hi | legal | s5 | membership | result | nodes | decisive budget | raw kit |
|---|---|---|---|---|---|---|---|---|
| ac001 | 1152921504758890496 / 68719476736 | 88 | 36668 | 2 | 2 (LOSS) | 5,635,468 | 15,000,000 | b30 |
| ac004 | 1152921779502579712 / 68719476736 | 89 | 257581 | 4 | 2 (LOSS) | 5,816,333 | 15,000,000 | b30 |
| ac005 | 5764607523052060672 / 68719476736 | 92 | 259840 | 4 | 2 (LOSS) | 7,941,333 | 15,000,000 | b30 |
| ac007 | 1152921504624672768 / 68719476737 | 95 | 357255 | 3 | 2 (LOSS) | 6,320,372 | 15,000,000 | b30 |
| ac008 | 1152921504624672800 / 68719476736 | 87 | 440522 | 4 | 2 (LOSS) | 3,722,379 | 15,000,000 | b30 |
| ac009 | 1152921504624672768 / 68719476738 | 92 | 442454 | 4 | 2 (LOSS) | 14,494,291 | 15,000,000 | b30 |
| ac010 | 1153202979601383424 / 68719476736 | 80 | 542960 | 2 | 2 (LOSS) | 4,730,437 | 15,000,000 | b30 |
| ac011 | 1152921504624672768 / 68719476992 | 80 | 544425 | 2 | 2 (LOSS) | 3,413,023 | 15,000,000 | b30 |
| ac012 | 1152922054380486656 / 68719476736 | 93 | 604378 | 4 | 2 (LOSS) | 6,067,761 | 15,000,000 | b30 |
| ac013 | 1155173304438358016 / 68719476736 | 93 | 605817 | 4 | 2 (LOSS) | 21,954,135 | 25,000,000 | dk |
| ac014 | 1152921504624672768 / 68719477248 | 88 | 625811 | 4 | 2 (LOSS) | 8,535,077 | 15,000,000 | b30 |
| ac015 | 1152921504893108224 / 68719476736 | 87 | 715677 | 4 | 2 (LOSS) | 6,725,969 | 15,000,000 | b30 |
| ac016 | 1152921504691781632 / 68719476736 | 91 | 731067 | 4 | 2 (LOSS) | 3,000,128 | 15,000,000 | b30 |
| ac017 | 1152921504624672768 / 68719477760 | 95 | 732474 | 4 | 2 (LOSS) | 10,672,726 | 15,000,000 | b30 |
| ac018 | 1152921504624803840 / 68719476736 | 91 | 799572 | 4 | 2 (LOSS) | 6,927,463 | 15,000,000 | b30 |
| ac019 | 1161928703879413760 / 68719476736 | 91 | 800491 | 4 | 2 (LOSS) | 10,173,232 | 15,000,000 | b30 |
| ac021 | 1152921504624672768 / 68719478784 | 91 | 810549 | 4 | 2 (LOSS) | 9,916,865 | 15,000,000 | b30 |
| ac022 | 1152921504624672832 / 68719476736 | 88 | 858406 | 4 | 2 (LOSS) | 3,441,401 | 15,000,000 | b30 |
| ac023 | 1170935903134154752 / 68719476736 | 96 | 859149 | 4 | 2 (LOSS) | 8,979,741 | 15,000,000 | b30 |
| ac024 | 1152921504624672784 / 68719476736 | 81 | 865769 | 4 | 2 (LOSS) | 9,826,442 | 15,000,000 | b30 |
| ac025 | 1152921504624672768 / 68719480832 | 78 | 866494 | 4 | 2 (LOSS) | 3,428,856 | 15,000,000 | b30 |
| ac028 | 1152921505161543680 / 68719476736 | 87 | 916195 | 4 | 2 (LOSS) | 5,087,946 | 15,000,000 | b30 |
| ac029 | 1152923703647928320 / 68719476736 | 93 | 916640 | 4 | 2 (LOSS) | 9,204,933 | 15,000,000 | b30 |
| ac030 | 1152921504658227200 / 68719476736 | 92 | 920775 | 4 | 2 (LOSS) | 7,072,780 | 15,000,000 | b30 |
| ac031 | 1152921504624672768 / 68721573888 | 97 | 921287 | 4 | 2 (LOSS) | 10,125,646 | 15,000,000 | b30 |
| ac032 | 1152921504624934912 / 68719476736 | 92 | 939058 | 4 | 2 (LOSS) | 19,707,272 | 20,000,000 | dj |
| ac033 | 1152925902671183872 / 68719476736 | 86 | 939315 | 4 | 2 (LOSS) | 5,912,106 | 15,000,000 | b30 |
| ac035 | 1152921504624672768 / 68723671040 | 93 | 941466 | 4 | 2 (LOSS) | 8,904,715 | 15,000,000 | b30 |
| ac036 | 1152921504624672896 / 68719476736 | 90 | 951686 | 4 | 2 (LOSS) | 16,605,302 | 20,000,000 | dj |
| ac037 | 1152930300717694976 / 68719476736 | 86 | 951830 | 4 | 2 (LOSS) | 3,818,788 | 15,000,000 | b30 |
| ac038 | 1152921504624672776 / 68719476736 | 95 | 952950 | 4 | 2 (LOSS) | 5,018,863 | 15,000,000 | b30 |
| ac039 | 1152921504624672768 / 68727865344 | 97 | 953103 | 4 | 2 (LOSS) | 11,367,923 | 15,000,000 | b30 |
| ac040 | 1152921504624672769 / 68719476736 | 84 | 955954 | 3 | 2 (LOSS) | 3,119,506 | 15,000,000 | b30 |
| ac042 | 1152921504624672772 / 68719476736 | 95 | 956625 | 4 | 2 (LOSS) | 3,007,885 | 15,000,000 | b30 |
| ac043 | 1152921504624673024 / 68719476736 | 82 | 956972 | 3 | 2 (LOSS) | 6,210,354 | 15,000,000 | b30 |
| ac044 | 1152921504624673280 / 68719476736 | 92 | 957287 | 4 | 2 (LOSS) | 16,323,488 | 20,000,000 | dj |
| ac046 | 1152921504625197056 / 68719476736 | 92 | 957935 | 4 | 2 (LOSS) | 5,216,563 | 15,000,000 | b30 |
| ac047 | 1152921504626769920 / 68719476736 | 94 | 958064 | 4 | 2 (LOSS) | 17,394,041 | 20,000,000 | dj |
| ac049 | 1152921504607895556 / 73014444032 | 90 | 958082 | 4 | 2 (LOSS) | 3,095,290 | 15,000,000 | b30 |
| ac050 | 1152921504607903744 / 73014444032 | 82 | 958097 | 3 | 2 (LOSS) | 8,586,185 | 15,000,000 | b30 |
| ac051 | 1152921504607895554 / 73014444032 | 89 | 958105 | 4 | 2 (LOSS) | 9,625,374 | 15,000,000 | b30 |
| ac052 | 1152921504607895553 / 73014444032 | 86 | 958114 | 3 | 2 (LOSS) | 5,349,962 | 15,000,000 | b30 |
| ac053 | 1152921504624672768 / 73014444032 | 80 | 958125 | 2 | 2 (LOSS) | 4,251,146 | 15,000,000 | b30 |

supersede鎖 (全て published bytes・maker が逐鎖検証):
- 15M drive: 6キーEXHAUSTED (ac006/ac013/ac032/ac036/ac044/ac047)・10キーWIN-HALT・38キーLOSS PASS
- ac006: 15M EXHAUSTED → DJ 20M WIN (1, 18,182,847)〔今回は不採用〕
- ac032/ac036/ac044/ac047: 15M EXHAUSTED → DJ 20M PASS result 2〔今回採用〕
- ac013: 15M EXHAUSTED → DJ 20M EXHAUSTED → DK 25M PASS result 2 (21,954,135)〔今回採用〕

**WIN 11行 は採用しない** (verdict不消費。WIN行採用は scrutiny owner C++
第二実装 gate `9193f5b6…` 専権のまま):
- ac002: s5 38891・result 1・nodes 10,752,246 (decisive budget 15,000,000・batch-30 15M・2-pass fresh-cold node-exact)
- ac003: s5 178184・result 1・nodes 8,036,766 (decisive budget 15,000,000・batch-30 15M・2-pass fresh-cold node-exact)
- ac006: s5 355050・result 1・nodes 18,182,847 (decisive budget 20,000,000・Part DJ 20M再probe・2-pass fresh-cold node-exact)
- ac020: s5 809575・result 1・nodes 9,765,071 (decisive budget 15,000,000・batch-30 15M・2-pass fresh-cold node-exact)
- ac026: s5 900276・result 1・nodes 3,036,572 (decisive budget 15,000,000・batch-30 15M・2-pass fresh-cold node-exact)
- ac027: s5 900687・result 1・nodes 2,593,751 (decisive budget 15,000,000・batch-30 15M・2-pass fresh-cold node-exact)
- ac034: s5 941211・result 1・nodes 14,853,857 (decisive budget 15,000,000・batch-30 15M・2-pass fresh-cold node-exact)
- ac041: s5 956329・result 1・nodes 10,959,413 (decisive budget 15,000,000・batch-30 15M・2-pass fresh-cold node-exact)
- ac045: s5 957713・result 1・nodes 2,530,544 (decisive budget 15,000,000・batch-30 15M・2-pass fresh-cold node-exact)
- ac048: s5 958080・result 1・nodes 4,701,704 (decisive budget 15,000,000・batch-30 15M・2-pass fresh-cold node-exact)
- ac054: s5 958143・result 1・nodes 2,236,690 (decisive budget 15,000,000・batch-30 15M・2-pass fresh-cold node-exact)

よって **class 34269 は freeにもexcludedにもならない**: BASE-unknown
54子 = 43採用 + 残11 = 上記未消費WIN 11の s5 {38891, 178184, 355050,
809575, 900276, 900687, 941211, 956329, 957713, 958080, 958143} のみ。
scenario status は unknown のまま (**unknown_now 54 → 11**・rank変化は
reauditで機械観測後に報告)。**閉鎖・被覆・secured・root勝敗の主張は
一切しない。標準11×11空盤・19 central-reply roots・class 34269・
batch-30全キー (WIN 11行を含む) はUNKNOWNのまま**。nodes数を勝敗として
読まない。WIN/LOSS canonical採用は gate `9193f5b6…` 通過後の 別adoption
Part (pinned merger経由) のみ。

## 入力証拠 (全て published bytes・宣言前に本セッションでfile-by-file検証)

- batch-30 kit: `research/experiments/n11-centralreply-closure-class34269-batch30-20261123/`・
  MANIFEST sha256 `330128aa1bcff45b52dac46e7e8bf9bbf57836f90d8f342fa269ee85ae77d845`
  (199 files・input 55 (54 csv + batch-keys)・output/raw 112 (108 primary + 4 truncated retry sidecar)・
  scripts 6・val-gate 24・README・status.log 79行)
- Part DJ kit: `research/experiments/n11-centralreply-closure-class34269-batch30-exh6-20m-20261124/`・
  MANIFEST `bb88fba3338a2e4188cd9a6a6fc8a1208507ccaa42fac36e9facb3fd0833a907`
  (34 files・DJ MANIFEST は raws/status.log を `output/` 相対で記録する
  published tree との表記ゆれあり・実体は両方存在し sha一致で解決)
- Part DK kit: `research/experiments/n11-centralreply-closure-class34269-batch30-exh1-25m-20261124/`・
  MANIFEST `e05c4259cdc5b004fc340fb770044ba57e443de0591c7d57a4b6a3b349707375`
  (15 files)
- 検証済み (ローカル取得・published MANIFEST対照 199+34+15 = 248/248 file sha一致):
  全54キー 2-pass raw node-exact + `# replay_done` both passes・
  15M/20M/25M 3世代・val-gate 4 pattern × 5 host
  (published-baseline/b30-host/d2t-host/d3t-host/d3u-host) node-exact
  (at2m×2 (0, 2,000,000)・first-15m (2, 3,651,923)・second-15m (2, 5,040,200))・
  DJ val-gate first-20m-vgo/second-20m-vgo (2, 3,651,923)/(2, 5,040,200) @20M・
  DK val-gate first-25m dkt/dkvv ×2 (2, 3,651,923)/(2, 5,040,200) @25M・
  jsreplay.js `845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df`
  (3 kit同一byte)・input csv 7枚 (6 reprobe + ac013) kit間同一 byte。
- status.log台帳 (honest history・全行pin対象):
  - batch-30 drive `88a474b5ef544ecb015f5a4058bc2dcb969afaca6f1b2816887307cd720c632c`
    (79行 = PASS 56 (54キー + ac001/ac002のretry重複2)・WIN-HALT 11 (10キー + ac002重複1)・
    EXHAUSTED 6・MISMATCH 2 (ac028/ac029・retryで解決済)・TRUNCATED-RETRY 4)
  - DJ `62f66b6a76eef059f42c225353003de4d4f9c638b33438c8217ec411df4da3c9` (16行)
  - DK `6a345a8bb33bb1e4536a30cb4d7ff974ab06a74eeed520f7756b37f32653d569` (1行 PASS ac013)
- batch-keys: batch-30 `79fbd1664f4ad66ea62d9c8a8aa5aaff5d16bcdaa397895119ce4d8f47961232`
  (class 34269・budget 15M・54キー・kit選択時点 rank 36・base 6,301行の frozen snapshot)・
  DJ subset `a80f402befaf2e8cf7b0484b4c51a125b525ccfd536a31ad7dea52b555011068`・
  DK subset `797467ec1009fc835c3fa9b92a29ebdbac6c3431777abbcde11a8a6fc1df88d5`
- 採用43キーは BASE (6,405行)・quarantine registry
  `81d231604d3a095c115135e05ca393d6be83e1aadde4f614d3b5a9cc67d17fe9` (active 2 entry・
  batch-30キーと衝突なし) の双方に不在 (fresh-increment gate・機械確認済)。

## 単一オーナー・非接触の機械確認 (observed HEAD 6a6e3a340)

- **Part DK** (本セッションの前工程・完了済): ac013 25M再probe lane。
  本PartのDK取得物は読み込み専用の入力証拠。非接触。
- **Part DM** (宣言 `88b7fc902`・batch-32 class 8730 54-key probe実行中):
  別class・別バッチ・verdict不消費probe専権レーン。非接触。
- **batch-30 (class 34269) adoption**: observed HEAD時点で未宣言
  (直近35 commit機械走査: canonical adoption主張なし・実験dir
  未存在)。もし本Partのmerge wave (C) より先に他レーンが batch-30行
  canonical adoption を出版した場合は即時停止し BASE再計画の上で次回へ
  引き継ぐ (racing guard)。
- Part DH (b28 P4 第三実装交叉検証・停滞): 非接触。

## 本Partの DL先例 (Part DL `00e17cda…`) からの差分

DL (b31loss51) と同一の構成 (maker → merger ×3 → refresh → extractor・
fail-closed・verdict不消費) を踏襲するが、差分がある:
1. 対象が batch-30 (class 34269)・43行 (DLはbatch-31 class 5804・51行)。
2. BASE が DL head (`60222707…` 6,405行) (DLはDB head `04b0a239…` 6,354行)。
3. supersede鎖が3世代 (15M→20M DJ→25M DK・DLは ad043 の2世代) で、
   15M EXHAUSTED 6キーのうち5キーは DJ 20M、1キー (ac013) は更に DK 25M。
4. status.log が honest history (retry重複 PASS 2行・MISMATCH 2行解決済・
   TRUNCATED-RETRY 4行・sidecar 4+6枚) を含む (DLは59行のクリーン形状)。
   maker/extractorはこの形状を段階pinで検証する。
5. **事前宣言pin登録を段階方式とする** (DLは宣言時に全出力pin事前登録
   だったが、本レーンは DLの env reset incident 同種のリスクが当日に
   実在した (本セッションも作業中に1回reset発生・成果は失っていない)
   ため、宣言 (入力pinのみ) → wave A-E の各wave直前に出力pinを出版する
   段階登録を正直に取る。各waveでlist_commits racing guard・
   fetch-back sha検証を必須とする。最終成果 (merged cache・reaudit・
   decomp) はDL同様に公式隔離rerunで再現検証してから出版する)。

## 実行計画 (宣言後・publish-then-execute)

実験dir: `research/experiments/n11-centralreply-class34269-b30loss43-adoption-reaudit-20261124/`

1. wave A: scripts 4 (maker `make_increments_b30loss43.py`・merger
   `s5_union_merge.py` byte-clone・refresh `refresh_adoption_b30loss43.py`
   (DL refresh の port・CACHE=merged cache)・extractor
   `compare_deltas_b30loss43_adoption.py`)。maker は全入力 kit MANIFEST
   file-by-file・43行2-pass・supersede鎖 (15M EXH raw pair → DJ 20M →
   DK 25M byte/node検証)・BASE/quarantine不在・val-gate node-exactの
   fail-closed gates。
2. wave B: increment `increment-b30loss43-20261124.cache` + `increments-manifest.json`
   (schema `b30loss43-increments-manifest-v1`) + merge-audit-run1/2/3。
3. wave C: merged cache (名前 = DL cache名 + `-plus-b30loss43`)。
4. wave D: reaudit 3出力 (refresh-summary.json・closure-classes.csv・
   per-root-coverage.csv・probe-worklist.csv は体積で非出版・DL refresh
   script をDL tree上で実行の regen手続) + decomp-deltas json。
5. wave E: 実験README + MANIFEST-sha256 (repo内実験dir fileのsha)・
   完了log。
6. tamper battery (T1-T6相当) を maker/merger/extractor に施行し
   rc=1捕捉とcontrolの無改変rc=0を記録する。

本Partの計算実行は全て単一host・逐次 (4並列目安以内・実際は1-2 procs)。
大規模中間fileの作成なし (probe-worklist regen ~3.7MB・repo外)。

## 事前宣言済み機械観測 (本宣言前に実施済み)

- 54/54キー 2-pass node-exact (15M 108 files・20M 12 files・25M 2 files・
  いずれも `# replay_done` 両pass)。
- decisive labels: LOSS 43 (38@15M・4@20M・1@25M)・WIN 11 (10@15M・
  ac006@20M)・EXHAUSTED 0 — batch-30 54キーにEXHAUSTED行は残っていない。
- loss総nodes = 346,729,500/pass。
- 採用43キー・不採用WIN11キーともに BASE/quarantine 不在。
- closure巨大変化 (class 34269 unknown_now 54 → 11) は maker/refreshで
  再計算の上、 wave Dで機械報告する。その他class (batch-30キーの
  membershipは2-4 classに及ぶ) への波及も機械観測後に報告する。

verdict不消費・11×11 UNKNOWN担保不変。
