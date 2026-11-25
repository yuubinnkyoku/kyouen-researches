# Part DN batch-30 (class 34269) 43-LOSS canonical adoption 完了log (2026-11-24)

- 単一オーナー Part DN。宣言 `research/log/2026-11-24-part-dn-b30loss43-adoption-declaration.md`
  (commit `402d481fa`, 2026-11-24T12:18:48Z, publish-then-execute)。
- **verdict 不消費。11×11 空盤は引き続き UNKNOWN。** 本 adoption は
  class 34269 の unknown children 54 → 11 という前進であり、勝敗決着ではない。

## 確定した成果 (全て fetch-back byte 照合済み)

### canonical chain head (Part DN 時点)

- `output/merged-exact-s5-chain-plus-b28loss1-plus-b28loss7-plus-b29loss16-plus-b29loss37-plus-b31loss51-plus-b30loss43-20261124.cache`
  = `7bdfa2366ef9c24b48a610d078104227555dd52ec18a566082cef2f906aab0f7`
  (6,448行・266,951 bytes・WIN 158 / LOSS 6,290)
  = BASE (Part DL) `60222707dd13902103fc8f7ef11c8487ec1be531ad0711e23e50c32154e30b84`
  (6,405行) + increment 43行 fresh LOSS (nodes 合計 346,729,500, 2-pass node-exact)。
  fail-closed merger byte-clone `90711961…`・merge-audit ×3 同一 byte。

### batch-30 の確定 label (54/54, probe-complete)

- 採用 43 LOSS: 38 @15M (batch-30 kit `330128aa…` 199 files) +
  4 @20M (Part DJ exh6-20M reprobe kit `bb88fba3…` 34 files:
  ac032/ac036/ac044/ac047) + 1 @25M (Part DK exh1-25M reprobe kit
  `e05c4259…` 15 files: ac013 nodes 21,954,135, 15M/20M EXHAUSTED
  からの supersede)。
- **未消費 WIN 11**: 15M WIN 10行 (ac002/ac003/ac020/ac026/ac027/
  ac034/ac041/ac045/ac048/ac054) + ac006 @20M (DJ reprobe が 15M
  EXHAUSTED を supersede)。s5 {38891, 178184, 355050, 809575, 900276,
  900687, 941211, 956329, 957713, 958080, 958143}。increment・merged
  cache・quarantine のどこにも含まれず、class 34269 は unknown のまま。
  C++ 第二実装 scrutiny オーナー gate `9193f5b6…` が WIN lane を保有。
- drive status.log = honest history 79行 (56 PASS (ac001/ac002 restart
  複製 含む) + 11 WIN-HALT + 6 EXHAUSTED (DJ/DK reprobe で全て supersede)
  + 2 MISMATCH (retry PASS で解決済み) + 4 TRUNCATED-RETRY marker)、
  全行 pin・raw と (budget,result,nodes) 機械照合。

### pin 一覧

| file | sha256 |
|---|---|
| `scripts/make_increments_b30loss43.py` | `d4f197c08210ead282fcf9a06905aae672e1a42d22108b7e446670f672db7802` |
| `scripts/s5_union_merge.py` | `907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a` (CU byte-clone) |
| `scripts/compare_deltas_b30loss43_adoption.py` | `87cf04c255509c5c8599235bd30305dea94e8c435fe7dff6d10cb318f922d42e` |
| `reaudit/scripts/refresh_adoption_b30loss43.py` | `d45832a6569267d7a8187cb9935acab177d73395af4485bf496ba2661ec29c5b` |
| `output/increment-b30loss43-20261124.cache` | `2dc3a15685c5df8a716a74729833cfb8cd1b19aba793213feebf53b32ea07740` |
| `output/increments-manifest.json` | `800d77e99680260fd89f7315ad6a4f19f1d5af98cae7693913f9c4eec5a39e6f` |
| `output/merge-audit-run{1,2,3}.json` | `6c35b897262cc80b1374a7cf1e8fc0eb1ae7edfef1e1b2b92c48d9c613619041` (3回同一) |
| `output/merged-…-plus-b30loss43-20261124.cache` | `7bdfa2366ef9c24b48a610d078104227555dd52ec18a566082cef2f906aab0f7` |
| `output/decomp-deltas-b30loss43-adoption.json` | `d89e49e81d4acc2d214609a276fbc01cfe7469c1a48906e6129066dfc05bb105` |
| `reaudit/output/refresh-summary.json` | `8349371ca09556570f0f50f58eab4444d0e7e277a5a7e0900585f430aef3e756` |
| `reaudit/output/closure-classes.csv` | `8f68f594834ba6aa85a09cea9c45ae86866f3fa18cfa97e79643b66976a4743c` |
| `reaudit/output/per-root-coverage.csv` | `1bc7a5e58462427333bdca95adab7470d0d3ac28bfff49866ba6efde6fd4f367` |
| `reaudit/output/probe-worklist.csv` (repo外) | `bac10aee9964bde0dbfa914e0d046b2f5380638ed20d3e3273823659f3abb708` (regen で byte 再現 ×2) |
| BASE (Part DL) 側 worklist (repo外) | `006ccd78d061c22838b3cee7701a91649d35abf3c8d56cecbb05931b604846d5` (extractor scratch rerun で再現) |
| `README.md` (実験dir) | `583e52972b525a9e31fd5b8d1f2c46824d4903b68f2d99de934b4407674b8861` |
| `MANIFEST-sha256.txt` | `e61eb6bbb968ae5152a4d3188eda68411a5201d03199f080f131203c370fb6c7` |

### 機械観測 (decomp deltas schema b30loss43-adoption-decomp-deltas-v1)

- class 34269: BASE-unknown children 54 → 11 (採用 43、残り 11 は未消費
  WIN の s5 {38891, 178184, 355050, 809575, 900276, 900687, 941211,
  956329, 957713, 958080, 958143})。status は unknown のまま
  (free_now でも excluded でもない、NOT freed)。
- closure 変化はちょうど {34269, 34263, 34908}: 34269 own 43
  (54 → 11)・34263 own 1 (54 → 53)・34908 own 2 (56 → 54)。
  rank churn 58・groups_served 減少 churn 1 (16513: 5 → 4)・
  left/entered 空・完全 stable 746 行 (合計 808 行)。
- update8: resolved 142 → 185 (newly resolved 集合 == 採用 43 s5 集合と
  機械照合・喪失 0)、remaining_now 31,717 → 31,674、
  groups_free_now 131 不変。
- per-root free/uncovered thirds は全 root 両側で同一 (root 27 = 119/119
  不変)。per-root greedy remaining は root 12 −129 / root 24 −86 のみ。
- joint greedy union 36,854 → 36,902 (+48)・worklist 64,711 → 64,665
  (−46)。いずれも scheduler bookkeeping (coverage 主張ではない)。
- class status 計数不変: excluded 390 / excluded_now 23 / free_now 38
  (Board 検証 38/38) / unknown 34,498。excluded_now flips なし。
  known-universe 584 → 627・cache-in-universe 561 → 604 (いずれも +43)。

### extractor (delta照合 `87cf04c2…`)

- Base (Part DL) と SCENARIO (Part DN) 両 refresh script を scratch tree
  で byte-verbatim 再実行し、8 出力 (summary/closure/prc/worklist ×2)
  が出版 pin と byte 一致。3 kit MANIFEST 199+34+15 file を file-by-file
  再SHA。SCEN cache == BASE rows + 43 increment rows verbatim、
  Board(11) で class 34269 の canonical 5-stone child boundary を再生成し
  54 unknown → 11 を独立再計算。

### tamper battery (sandbox 9項目、全て fail-closed)

1. kit raw 追記 → maker ABORT (kit file sha drift)
2. status verdict 改変 → maker ABORT (kit file sha drift)
3. status 行追加 → maker ABORT (同上)
4. val-gate file 欠落 → maker ABORT (file missing)
5. BASE cache 改変 (LOSS→WIN) → maker ABORT (base cache sha drift)
6. merger へ WIN/LOSS conflict 注入 → GATE FAILED・出力なし
7. SCEN cache 改変 → extractor ABORT (scenario cache sha drift)
8. quarantine registry へ注入 → maker ABORT (quarantine registry sha drift)
9. 復旧後 sanity: maker・extractor とも再通過

## 出版 (main 直・各wave直前に racing guard、fetch-back 全件 byte 一致)

1. 宣言 `402d481fa` (2026-11-24T12:18:48Z)
2. wave A〜D-1 (maker + merger clone + refresh fork + increment +
   manifest + merge-audit ×3 + reaudit 3出力) `a2acac2e`
3. wave D-2 (merged cache) `32cd214d`
4. wave D-3 (delta extractor + decomp json) `954434143a`
5. wave E (実験README + MANIFEST-sha256 + 本完了log) この commit

## honest な限界

- 再構築と公式隔離 rerun は単一 host 上の実行 (val-gate multi-host
  出力は 3 kit 出版物そのものを sha 照合したものであり、本 Part 実行
  の多 host 化を意味しない)。
- batch-30/DJ/DK の raw 実行は 2-pass 逐次 (share_tt 不使用)・
  budget 15M/20M/25M。
- WIN 11行は意図的に未消費 (検証オーナー gate 待ち)。class 34269 は
  unknown のまま。
- 11×11 空盤は**UNKNOWN**。19 root も全て UNKNOWN (root 27 baseline
  119/119 不変)。

次のレーン候補: closure table 上位の小 class (23101 / 1849 / 2251 が
unknown 1、5804 が unknown 4)、class 34269 の残り 11 WIN 行の扱い
(C++ scrutiny オーナー gate の裁定待ち)。
