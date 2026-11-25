# Part DN — batch-30 (class 34269) 43-LOSS canonical adoption (b30loss43)

2026-11-24。単一オーナー Part DN。**11×11 空盤は引き続き UNKNOWN**
(verdict 不消費)。本実験dirは class 34269 の batch-30 43行 fresh LOSS
を canonical chain に接続した記録であり、勝敗の決着ではない。
宣言 `research/log/2026-11-24-part-dn-b30loss43-adoption-declaration.md`
(commit `402d481fa`, 2026-11-24T12:18:48Z, publish-then-execute)。

## 何が確定したか (機械観測)

- canonical chain head (merged cache):
  `output/merged-exact-s5-chain-plus-b28loss1-plus-b28loss7-plus-b29loss16-plus-b29loss37-plus-b31loss51-plus-b30loss43-20261124.cache`
  sha256 `7bdfa2366ef9c24b48a610d078104227555dd52ec18a566082cef2f906aab0f7`
  (6,448行・266,951 bytes・WIN 158 / LOSS 6,290)。
  BASE `60222707…` (Part DL, 6,405行) + `output/increment-b30loss43-20261124.cache`
  `2dc3a156…` (43行 fresh LOSS, node 合計 346,729,500, 2-pass node-exact)
  を fail-closed union merger (CU byte-clone 90711961…) で併合
  (merge-audit ×3 同一 byte)。
- batch-30 は probe-complete: 54/54 キーが honest two-pass label を持つ。
  採用 43 LOSS = 38 @15M (batch-30 kit raws) + 4 @20M (Part DJ exh6-20M
  reprobe: ac032/ac036/ac044/ac047) + 1 @25M (Part DK exh1-25M reprobe:
  ac013, 15M/20M EXHAUSTED の supersede, nodes 21,954,135)。
  manifest `800d77e9…` (schema b30loss43-increments-manifest-v1,
  loss-only ではなく full_packet_eq_loss_only=false)。
  drive status.log は honest history (79行 = 56 PASS (ac001/ac002 restart
  複製 含む) + 11 WIN-HALT + 6 EXHAUSTED + 2 MISMATCH (retry で解決済み)
  + 4 TRUNCATED-RETRY marker、全行 pin)。
- **WIN 11行 (ac002/ac003/ac020/ac026/ac027/ac034/ac041/ac045/ac048/ac054
  の 15M WIN 10行と、Part DJ 20M reprobe で 15M EXHAUSTED を supersede した
  ac006 の WIN) はどこにも消費していない**: increment にも merged cache
  にも含まれず、class 34269 は unknown のまま (unknown 54 → 11,
  s5 残り {38891, 178184, 355050, 809575, 900276, 900687, 941211,
  956329, 957713, 958080, 958143})。WIN 行の scrutiny は C++ 第二実装
  オーナー gate (9193f5b6…) に属する。
- refresh (reaudit): class status 計数は不変 (free_now 38 / excluded_now 23 /
  unknown 34,498 / excluded 390, Board 検証 38/38)。update8 は resolved
  142 → 185 (ちょうど +43、newly resolved 集合 == 採用 43 s5 集合と
  機械照合)、remaining 31,717 → 31,674。joint greedy union 36,854 →
  36,902、probe worklist 64,711 → 64,665、per-root remaining は
  root 12 −129 / root 24 −86 のみ (いずれも scheduler bookkeeping で
  coverage 主張ではない)。per-root free/uncovered thirds は全 root
  両側で同一 (root 27 = 119/119 不変)。
- closure 変化はちょうど {34269, 34263, 34908}: class 34269 own 43
  (54 → 11)、holder 34263 own 1 (54 → 53)、34908 own 2 (56 → 54)。
  rank churn 58・groups_served 減少 churn 1 (16513: 5 → 4)・
  left/entered 空・完全stable 746 行。
- decomp deltas: `output/decomp-deltas-b30loss43-adoption.json`
  (schema b30loss43-adoption-decomp-deltas-v1, delta extractor
  `87cf04c2…`): 両 refresh script (BASE Part DL `e92fa80e…` / SCEN
  `d45832a6…`) を scratch tree で byte-verbatim 再実行し 8/8 出力が
  出版 pin と byte 一致 (worklists 含む: BASE `006ccd78…`, SCEN
  `bac10aee…`)。
- tamper battery (sandbox, 9項目): kit raw 改変 / status 改変 /
  status 行追加 / val-gate file 欠落 / BASE cache 改変 / WIN-LOSS conflict
  注入 (merger 出力なし) / SCEN cache 改変 / quarantine 注入 → 全て
  fail-closed ABORT、復旧後 sanity 再通過。

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

次のレーン候補: closure table 上位の小 class (23101 unknown 1 / 1849
unknown 1 / 2251 unknown 1 / 5804 unknown 4)、class 34269 の残り 11 WIN
行の扱い (C++ scrutiny オーナー gate の裁定待ち)。
