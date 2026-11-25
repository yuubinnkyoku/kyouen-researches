# Part DL batch-31 (class 5804) 51-LOSS canonical adoption 完了log (2026-11-24)

- 単一オーナー Part DL。宣言 `research/log/2026-11-24-part-dl-b31loss51-adoption-declaration.md`
  (commit `00e17cda04ce29dc5ea4d7011c12baef5d9437b6`, 2026-11-24T08:20:29Z)。
  インシデント (宣言出版後の実行環境 reset による宣言前成果物消失と再構築)
  は amendment
  `research/log/2026-11-24-part-dl-b31loss51-adoption-incident-amendment.md`
  (commit `e9a362fce3ddf57c9bcedee21f54a4c469c89c16`) が正本。
- **verdict 不消費。11×11 空盤は引き続き UNKNOWN。** 本 adoption は
  class 5804 の unknown children 55 → 4 という前進であり、勝敗決着ではない。

## 確定した成果 (全て fetch-back byte 照合済み)

### canonical chain head

- `output/merged-exact-s5-chain-plus-b28loss1-plus-b28loss7-plus-b29loss16-plus-b29loss37-plus-b31loss51-20261124.cache`
  = `60222707dd13902103fc8f7ef11c8487ec1be531ad0711e23e50c32154e30b84`
  (6,405行・264,619 bytes・WIN 158 / LOSS 6,247)
  = BASE (Part DB) `04b0a23987a97518e276ea5ff966496facab22f93628cd5fbc682a04c3650556`
  (6,354行) + increment 51行 fresh LOSS (nodes 合計 237,596,711)。

### pin 一覧 (再構築後の正本・宣言/amendment supersede表と整合)

| file | sha256 |
|---|---|
| `scripts/make_increments_b31loss51.py` | `d3e0e07937a77db7773508af5b3c536f540365e08edbaf976ea5a56349c404a1` |
| `scripts/s5_union_merge.py` | `907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a` (CU byte-clone) |
| `scripts/compare_deltas_b31loss51_adoption.py` | `fab162676dd7452699af68978bcf2cecd75bed440e71d511e114172a62c55b9e` |
| `reaudit/scripts/refresh_adoption_b31loss51.py` | `e92fa80e7d8d9ac46f9dd66b90fab6cebab349948fdb14a916f180c2611b81e4` |
| `output/increment-b31loss51-20261124.cache` | `e750a0e6ea4333f9705c0898914a289c388143ac78cbf58d337d640a7457c0d5` |
| `output/increments-manifest.json` | `ae06f855a34cc186eb1811629f2911958fefc7ed073e220bdceba76388575f27` |
| `output/merge-audit-run{1,2,3}.json` | `dc312c0720f81b61bbe3bb70e55736d2773de8714bd782992098c1341b531622` (3回同一) |
| `output/merged-…-plus-b31loss51-20261124.cache` | `60222707dd13902103fc8f7ef11c8487ec1be531ad0711e23e50c32154e30b84` |
| `output/decomp-deltas-b31loss51-adoption.json` | `0af301b81fbac18eb1a8a844467eb294a141828203f4585971e736e483109120` |
| `reaudit/output/refresh-summary.json` | `fea0b0d4473b34447556f3a3e8b9ecc7c57c59221b18c4bb58222e0149b2e4bc` |
| `reaudit/output/closure-classes.csv` | `50841fa47676be8af145f1f8f751b0d96f75e94417990418cbe1d2a52bd4d389` |
| `reaudit/output/per-root-coverage.csv` | `136e308a332c8ab6fe877f3ef3a3b361770931285d91a0d12a59a6dd9707b487` |
| `reaudit/output/probe-worklist.csv` (repo外) | `006ccd78d061c22838b3cee7701a91649d35abf3c8d56cecbb05931b604846d5` (regen で byte 再現) |
| `README.md` (実験dir) | `4f4187f1d79982ef8f4af854ae66cff601eb839c8abcbbce7216fceaa81dcf20` |
| `MANIFEST-sha256.txt` | `c1af8ff0a7fbe2daf5581da0318a5a8258a5356a2ddaab567f657e3dccb8240e` |

### 機械観測 (decomp deltas schema n11-b31loss51-adoption-decomp-deltas-v1)

- class 5804: BASE-unknown children 55 → 4 (採用 51、残り 4 は未消費 WIN の
  s5 {198576, 207094, 212115, 212536})。rank 38 → 4。status は unknown のまま
  (free_now でも excluded でもない)。
- WIN 4行 (ad024 (1, 4,360,661)・ad028 (1, 12,803,283)・ad055 (1, 3,364,655)
  15M WIN-HALT、ad043 15M EXHAUSTED (0, 15,000,000) → DI 30M reprobe
  (1, 18,247,029) で supersede) は**どこにも消費していない**。
  C++ 第二実装 scrutiny オーナー gate `9193f5b6…` が WIN lane を保有。
- holder union 126 (自家分布 {1:102, 2:23, 51:1}; class 5804 own 51・8730 own 2・
  8811 own 1)。closure 変化はちょうど {5804, 8730, 8811}
  (5804 (38,55)→(4,4)・8730 (60,56)→(30,54)・8811 (50,55)→(38,54))。
  churn 54 (unknown 50 / excluded_now 4)。closure left/entered 空。
- update8: resolved 141 → 142 (ad009 s5 148458 の 1行のみ)、
  remaining_now 31,718 → 31,717。
- worklist 64,765 → 64,711 (−54)。joint greedy union 36,903 → 36,854 (−49)。
  per-root greedy movers {4:−1, 5:−2, 13:−1, 25:−1, 38:−50, 49:−105}、
  free/uncovered thirds は全 root 両側不変 (root 27 = 119/119)。
- class status 計数不変: excluded 390 / excluded_now 23 / free_now 38 /
  unknown 34,498。excluded_now flips なし。

## 出版 (main 直・各wave直前に racing guard、fetch-back 全件 byte 一致)

1. amendment `e9a362fce3ddf57c9bcedee21f54a4c469c89c16`
2. wave A (scripts 4) `c92959a80a674b2f1368f67aa4220834e412dba2`
3. wave B (increment + manifest + audit×3) `fe84af0613705c76ed76dd54a48d35d9da884e5f`
4. wave C (merged cache) `7f192dd9562780afb9a1178da85f63b3f614a12c`
5. wave D (reaudit 3出力 + decomp) `2f3f46b5e115280942cf3e6d21b8a25b4642cd5e`
6. wave E (実験README + MANIFEST-sha256) `3ffd83bb7df5da4a1bc6d752fcdd69b7829b160b`
   (remote MANIFEST 14 file 逐件再検査 14 ok / 0 bad)

## honest な限界

- 再構築と公式隔離 rerun は単一 host 上の実行 (val-gate 6-host 出力は
  batch-31 kit 出版物そのものを sha 照合したもので、本Part実行の多 host 化
  を意味しない)。
- batch-31/DI の raw 実行は share_tt=0 (shared TT 不使用)・budget 15M/30M
  の逐次 2-pass。serif 系の最適化は本 Part では適用していない。
- WIN 4行は意図的に未消費 (検証オーナー gate 待ち)。class 5804 は
  unknown のまま。
- 11×11 空盤は**UNKNOWN**。19 root も全て UNKNOWN (root 27 baseline
  119/119 不変)。

次のレーン候補: class 5804 の残り 4 WIN 行の扱い (C++ scrutiny オーナー
gate の裁定待ち・裁定後は class 5804 closure candidate の再評価)、
closure table 上位の小 class (unknown 1 行クラス) の pocket 解消。
