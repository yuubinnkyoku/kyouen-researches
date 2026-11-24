# Part DP 宣言: batch-32 (closure class 8730) 54 LOSS行 (probe-complete・loss-only packet) の canonical adoption + reaudit deltas (2026-11-24)

単一オーナー宣言・publish-then-execute。observed HEAD `dfb38f6b`
(round 4 PG(2,q) blocking-set Kyouen lane・2026-11-24T16:02:27Z)。
Part文字は「DP」を採用 (直近 commit 機械走査で使用中の Part D* は
DF/DG/DH/DK/DL/DM/DN のみで、`-part-dp-` は research/log 配下に存在せず、
commit message 機械走査で「b32loss54」は Drive 完了log `38e6efe8` の本文のみで
adoption 主張は存在しない。本宣言は DP の最初の出版物)。

## 対象と目的

Part DM drive-1 batch-32 (closure class 8730) は probe-complete で、
published kit の全54キーが honest two-pass fresh-cold label
(15M・全て result=2 LOSS・WIN 0 / EXHAUSTED 0 / MISMATCH 0 /
TRUNCATED 0・status.log 54 PASS行) を持つ。**54 fresh LOSS行を丸ごと**
pinned fail-closed union merger
`907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac46a74606a`
(CU byte-clone・selftest PASS) で canonical merged cache に採用 (merge) する:

- BASE = Part DN canonical merged cache・6,448行 sha256
  `7bdfa2366ef9c24b48a610d078104227555dd52ec18a566082cef2f906aab0f7`
  (WIN 158 / LOSS 6,290・DN 出版byteを改変せずそのまま pin)
- ADOPTED-CANONICAL = BASE + 54行 = 6,502行 (WIN 158 / LOSS 6,344)
  merged cache名 = DN cache名 + `-plus-b32loss54`:
  `merged-exact-s5-chain-plus-b28loss1-plus-b28loss7-plus-b29loss16-plus-b29loss37-plus-b31loss51-plus-b30loss43-plus-b32loss54-20261124.cache`
  sha256 `1ded9a083feabc095dd998c92002b47efc05b8666adf030501bcffc2873a9dd6`
  (6,502行・269,441 bytes)

54行 (合計 nodes **223,769,637/pass** = 2-pass fresh-cold node-exact、
全行 decisive budget 15,000,000・published batch-32 kit raws):

| key | lo / hi | legal | s5 | membership | result | nodes @15M |
|---|---|---|---|---|---|---|
| ae001 | 6052837899320164384 / 0 | 96 | 30596 | 3 | 2 (LOSS) | 3,729,310 |
| ae002 | 10412322613358493696 / 262144 | 94 | 102313 | 3 | 2 (LOSS) | 3,127,842 |
| ae003 | 6052837899185946657 / 0 | 98 | 227811 | 4 | 2 (LOSS) | 5,421,696 |
| ae004 | 1188950576503718912 / 262144 | 100 | 227869 | 4 | 2 (LOSS) | 2,403,926 |
| ae005 | 6052837899185948704 / 0 | 103 | 233201 | 4 | 2 (LOSS) | 4,773,521 |
| ae006 | 1188950576503718400 / 262144 | 104 | 233301 | 4 | 2 (LOSS) | 4,450,622 |
| ae007 | 6052837899190140960 / 0 | 97 | 238388 | 4 | 2 (LOSS) | 4,181,208 |
| ae008 | 1188950576503718144 / 262144 | 102 | 238453 | 4 | 2 (LOSS) | 4,607,542 |
| ae009 | 6052837907775881248 / 0 | 103 | 243426 | 4 | 2 (LOSS) | 5,025,299 |
| ae010 | 6052837899185946656 / 8192 | 104 | 243470 | 4 | 2 (LOSS) | 5,719,747 |
| ae011 | 6052855491371991072 / 0 | 103 | 248258 | 4 | 2 (LOSS) | 3,272,592 |
| ae012 | 6052837899185946656 / 4 | 104 | 248342 | 4 | 2 (LOSS) | 5,664,027 |
| ae013 | 6052838174063853600 / 0 | 96 | 251425 | 3 | 2 (LOSS) | 2,768,066 |
| ae014 | 6052837899185946658 / 0 | 105 | 255023 | 4 | 2 (LOSS) | 5,741,083 |
| ae015 | 1188950576505815040 / 262144 | 104 | 255105 | 4 | 2 (LOSS) | 5,040,670 |
| ae016 | 6052837899185950752 / 0 | 96 | 259174 | 4 | 2 (LOSS) | 2,925,237 |
| ae017 | 1188950576504766464 / 262144 | 100 | 259246 | 4 | 2 (LOSS) | 5,830,686 |
| ae018 | 6052837899194335264 / 0 | 101 | 263258 | 4 | 2 (LOSS) | 3,637,481 |
| ae019 | 1188950576504242176 / 262144 | 102 | 263323 | 4 | 2 (LOSS) | 2,693,629 |
| ae020 | 6052837916365815840 / 0 | 100 | 267197 | 4 | 2 (LOSS) | 3,970,119 |
| ae021 | 6052837899185946656 / 16384 | 102 | 267253 | 4 | 2 (LOSS) | 2,790,531 |
| ae022 | 6052873083558035488 / 0 | 98 | 270978 | 4 | 2 (LOSS) | 4,730,974 |
| ae023 | 6052837899185946656 / 8 | 104 | 271035 | 4 | 2 (LOSS) | 4,311,795 |
| ae024 | 6052837899185946660 / 0 | 91 | 276288 | 4 | 2 (LOSS) | 3,956,699 |
| ae025 | 1188950580798685184 / 262144 | 99 | 276352 | 4 | 2 (LOSS) | 4,984,219 |
| ae026 | 6052837899185954848 / 0 | 102 | 279610 | 4 | 2 (LOSS) | 4,035,462 |
| ae027 | 1188950578651201536 / 262144 | 101 | 279678 | 4 | 2 (LOSS) | 3,532,465 |
| ae028 | 6052837899202723872 / 0 | 93 | 282568 | 4 | 2 (LOSS) | 4,463,589 |
| ae029 | 1188950577577459712 / 262144 | 97 | 282635 | 4 | 2 (LOSS) | 5,059,660 |
| ae030 | 6052837933545685024 / 0 | 98 | 285488 | 4 | 2 (LOSS) | 3,031,657 |
| ae031 | 6052837899185946656 / 32768 | 99 | 285539 | 4 | 2 (LOSS) | 6,305,981 |
| ae032 | 6052908267930124320 / 0 | 95 | 288280 | 4 | 2 (LOSS) | 1,981,997 |
| ae033 | 6052837899185946656 / 16 | 93 | 288347 | 4 | 2 (LOSS) | 2,296,664 |
| ae034 | 1188959372596740096 / 262144 | 103 | 290817 | 4 | 2 (LOSS) | 8,966,840 |
| ae035 | 6052837899185963040 / 0 | 93 | 293375 | 4 | 2 (LOSS) | 3,205,767 |
| ae036 | 1188954974550228992 / 262144 | 97 | 293452 | 4 | 2 (LOSS) | 4,713,799 |
| ae037 | 6052837899219501088 / 0 | 92 | 295673 | 4 | 2 (LOSS) | 3,974,706 |
| ae038 | 1188952775526973440 / 262144 | 101 | 295743 | 4 | 2 (LOSS) | 3,176,793 |
| ae039 | 6052837967905423392 / 0 | 92 | 297981 | 4 | 2 (LOSS) | 3,910,081 |
| ae040 | 6052837899185946656 / 65536 | 97 | 298037 | 4 | 2 (LOSS) | 2,667,008 |
| ae041 | 6052978636674301984 / 0 | 100 | 300134 | 4 | 2 (LOSS) | 3,458,396 |
| ae042 | 6052837899185946656 / 32 | 99 | 300216 | 4 | 2 (LOSS) | 1,706,977 |
| ae043 | 6052837899185946672 / 0 | 100 | 302188 | 4 | 2 (LOSS) | 5,406,352 |
| ae044 | 1206964975013199872 / 262144 | 104 | 302257 | 4 | 2 (LOSS) | 3,917,841 |
| ae045 | 6052837899185979424 / 0 | 99 | 304124 | 4 | 2 (LOSS) | 3,360,772 |
| ae046 | 1197957775758458880 / 262144 | 104 | 304196 | 4 | 2 (LOSS) | 3,905,480 |
| ae047 | 6052837899253055520 / 0 | 91 | 305925 | 4 | 2 (LOSS) | 3,632,700 |
| ae048 | 1193454176131088384 / 262144 | 96 | 305986 | 4 | 2 (LOSS) | 3,475,879 |
| ae049 | 6052838036624900128 / 0 | 100 | 307575 | 4 | 2 (LOSS) | 4,405,745 |
| ae050 | 6052837899185946656 / 131072 | 102 | 307627 | 4 | 2 (LOSS) | 4,670,080 |
| ae051 | 6053119374162657312 / 0 | 91 | 309085 | 4 | 2 (LOSS) | 6,473,086 |
| ae052 | 6052837899185946656 / 64 | 94 | 309139 | 4 | 2 (LOSS) | 5,156,590 |
| ae053 | 5800636594931105792 / 262144 | 88 | 311698 | 3 | 2 (LOSS) | 1,981,997 |
| ae054 | 1188950576503717888 / 262146 | 96 | 311727 | 2 | 2 (LOSS) | 5,136,752 |

**WIN行はゼロ** (採用packet は loss-only・`full_packet_eq_loss_only=true`・
`win_scenario_exists=false`)。したがって本 Part に verdict 不消費の残務は
なく、WIN行採用の scrutiny gate (C++ 第二実装 `9193f5b6…`) は本 Part の
scope 外のまま。

## 入力証拠 (全て published bytes・宣言前に本セッションでfile-by-file検証)

- batch-32 kit: `research/experiments/n11-centralreply-closure-class8730-batch32-20261124/`
  MANIFEST sha256 `7c2c159ae24bab8836e23a8e2502615d62650eb4fb555979513ca55f71e7dec8`
  (manifest 194行 = file 193 + 注記1・本セッションで194/194行取得し sha一致)
- drive status.log: `a78135d79438e5cf0d6f95378c1b68f9ca1aa06ef564d141cf03e4b93a32eed4`
  (54行・全行 PASS・行ごとに raw pair と (15M, 2, nodes) 一致を maker が検証)
- batch-keys: `f46e663f1676111ae67f5686f4a7807a8c1f7e4e1d9910ddb96ba61bcb5e705d`
  (schema n11-centralreply-closure-class8730-batch32-input-v1・class 8730・
  budget 15M・54キー・kit選択時点 rank 30・runner-up 11490・
  published_base_canonical_rows 6,405 の frozen snapshot・groups_served_count 4)
- jsreplay.js: `845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df`
  (pinned solver image・過去3 kit と同一byte)
- val-gate: 4 molecule × 5 host (published-baseline + b32-host〜b32-host4)
  全て node-exact
- 採用54キーは BASE (6,448行)・quarantine registry
  `81d231604d3a095c115135e05ca393d6be83e1aadde4f614d3b5a9cc67d17fe9`
  (active 2 entry) の双方に不在 (fresh-increment gate・機械確認済)。

## 単一オーナー・非接触の機械確認 (observed HEAD dfb38f6b)

- **Part DM** (batch-32 drive実行 lane・完了 commit `38e6efe8`): 本 Part の
  入力証拠は読み込み専用。非接触。
- **Part DN** (b30loss43 adoption): BASE を提供・非接触 (DN出版物の byte は
  変更しない)。
- **batch-32 (class 8730) adoption**: observed HEAD 時点で未宣言
  (b32loss54 採用主張なし・実験dir `n11-centralreply-class8730-b32loss54-adoption-reaudit-20261124` 未存在)。
  もし本宣言以降・wave C (merged cache出版) より先に他レーンが同 adoption を
  出版した場合は即時停止し BASE 再計画の上で次回へ引き継ぐ (racing guard)。
- round 4 PG(2,q) / K-item lanes (K1294〜K1297等): 別 asset 体系・非接触。

## 事前宣言する期待機械観測 (本セッションの dry-run で一度生成済み・
## 出版後に独立 rerun で byte 再現を検証する)

全て reaudit refresh (Board による子検証 fail-closed) と decomp delta
extractor (両 refresh script の byte-verbatim 再実行) から得た機械観測:

- **class 8730 (58子) は unknown から free_now へ遷移**
  (54採用 + BASE既知LOSS 4子 s5 {144458, 212464, 310606, 311726} =
  58子全て exact LOSS)。Board 検証 39/39 (free_candidates 39・rejected 0)、
  free_now 38→39、unknown 34,498→34,497。**free_now は Board-derived な
  scheduling bookkeeping であり、root 勝敗でも coverage 主張でもない。**
- closure 表: 808→807行、left=[8730] (free化による離脱)、entered=空、
  完全 stable 27行、rank churn のみ 779行、groups_served 減少 churn 0、
  unknown 変化は class 8811 のみ (54→52、own採用 2)。
- per-root coverage (4つの class-8730 serve group のみ):
  root 38 free 13→15 / uncovered 106→104・root 5 free 8→10 /
  uncovered 111→109。root 27 は 119/119 不変。unique_groups 2,119→2,115。
  joint greedy union は 36,902→36,968 (**増加**: class-8730 member が
  nonfree best-option 集合から離脱する再選択 churn であって coverage
  後退ではない)。update8 resolved 185→187 (新規 s5 {285539, 311727}、
  ともに採用54内)、remaining 31,674→31,672、groups_free_now 131 静止、
  probe worklist 64,665→64,609、cache_rows_in_universe 604→658、
  per-root remainingのオフセット {5: -5, 25: -2, 38: -4}。
- **閉鎖・被覆・secured・root勝敗の主張は一切しない。標準11×11空盤・
  19 central-reply roots・二石root・S2・class 8730・batch-32全キーは
  UNKNOWNのまま。nodes数を勝敗として読まない。**

## 実行計画 (宣言後・publish-then-execute)

実験dir: `research/experiments/n11-centralreply-class8730-b32loss54-adoption-reaudit-20261124/`

1. wave B: scripts 4 = maker `make_increments_b32loss54.py`
   (sha256 `44331adcf00ed9f70d68f48634467c96619a943af739251cbb83926c3473aa55`・
   kit MANIFEST 193 file・54行2-pass・status行照合・BASE/quarantine 不在・
   val-gate node-exact の fail-closed gates)・merger `s5_union_merge.py`
   (byte-clone `90711961…`)・extractor
   `compare_deltas_b32loss54_adoption.py`
   (sha256 `4c16da6e6e0365ef2bd4c21884875435678d8e101bccef3fa9a1f6399fc52982`)・
   refresh fork `reaudit/scripts/refresh_adoption_b32loss54.py`
   (DN `d45832a6…` の fork・sha256
   `41bf706fd0e2d0eb831ecfdf35eb52bf448dece8107b792856fb2d65fe93a366`・
   CACHE=merged cache・graph/update8/board/policy/quarantine pin)。
2. wave C: increment `increment-b32loss54-20261124.cache`
   (sha256 `ca4af3e7704f2a72649b8386c83916ea129152bfc85c1363a30f4be54590dadb`・
   54行) + `increments-manifest.json`
   (sha256 `3f906dc81e1eb74a2f0a74113e474e215673755eee7d719e42ce42424e86a2f4`・
   schema b32loss54-increments-manifest-v1) + merge-audit-run1/2/3
   (3回とも sha256 `5ebfdbfb4aefefb2cd1d6c020f1bbe946f60c1196ee2bd2b63a998fe0305ae52`)
   + merged cache (sha256 `1ded9a08…` 6,502行)。
3. wave D: reaudit 3出力 (refresh-summary.json
   `74f5dd9b6d8752964ca622ebb40388694aac1bd787d615e184a06e25693a5179`・
   closure-classes.csv
   `284bb069d7c0efb7bb04addd7e1947716dfd2db5f0caf47ca3942bfa5cfa493f`・
   per-root-coverage.csv
   `096a9c37c1e6624ec1d17eaed957ceaf331f4ed7c5787a0c88fd5bdc6075e9c0`
   probe-worklist.csv は体積で非出版・regen pin
   `87c2ebd63015ca399a13e0ef561796bce655003ff69cb01b8f8177818f1bf368`)
   + decomp deltas
   (`output/decomp-deltas-b32loss54-adoption.json` sha256
   `7def99020d7cb2787d8c6ca825546e3432f25c32b1174370f8875f8981271be8`)
   + README + MANIFEST-sha256。
4. wave E: 完了log (tamper battery 記録含む)。
5. tamper battery (sandbox stage - T1〜T8) を maker/merger/refresh に施行し
   rc=1 捕捉と復旧後 sanity rc=0 を記録する。

本 Part の計算実行は全て単一host・逐次 (4並列目安以内)。大規模中間fileの
作成なし (probe-worklist regen ~3.7MB・repo外)。

verdict不消費の残務なし (loss-only packet)・11×11 UNKNOWN担保不変。
