# n11 central-reply q042 single-WIN if-adopted decomposition (Part AT, 2026-11-22)

単一オーナー宣言 (note Part AT amendment, commit `58938933`, observed
HEAD-before-push `2f88a495`, note blob sha1 `9a5dfdb7...`) に基づく、
batch-14 (class 23101) の不採用WIN行 q042 (s5_index 745184, result 1,
9,149,084 nodes) 単独採用時の**if-adopted投影**計算。Part AS
(batch-14 41 LOSS行採用reaudit・canonical 6,120行 `be9cb24e...` 出版)
の直接後続。scrutiny ownerの採用判断に向けた事前計算であり、
**verdictは不消費・canonical cacheはbyte不変・採用推奨/却下いずれでも
ない** (すべて機械表明・機械検査):

1. increments maker (`scripts/make_increment_q042_win.py` = published
   Part AS maker `e35b545d...` 系のq042-WIN adapt) をpublished batch-14
   raws (publication commit `7b211d38`) から再実行し、q042の2-pass WIN
   を機械再検証のうえ単一行 increment
   (sha256 `b4958328270f11b24d3a638e1099a0c6047dbebb242e3116217b0473ef63f9b6`,
   manifest sha256 `894e9420...`, schema
   `batch14-q042-win-ifadopted-increment-manifest-v1`) を導出。
   BASE不在 (6,120行)・quarantine不在 (0 hit) をgate。
2. sha-pinned fail-closed union merger (`90711961...`, byte-copy pin,
   selftest PASS) でcanonical 6,120行 (`be9cb24e...`, 不変) + 1 WIN行を
   mergeし、**if-adopted cache 6,121行** (WIN 159 / LOSS 5,962, conflict
   0, duplicates 0, sha256
   `1434c68bc572a9817eca9c9a4ab442005762339cf539f22cb3acb0b24bc5ffe0a`,
   251,513 bytes) を
   `output/merged-exact-s5-chain-plus-closure-increment-plus-batch10-plus-batch16loss52-plus-batch14loss41-plus-q042win-IFADOPTED-20261122.cache`
   に生成 (本repoのcanonical chainとは別物・non-canonical projection)。
   merge 3回実行・byte一致・merge-audit 3回byte一致 (sha256
   `e1d11a66...`)。BASE canonicalはmerge後に再検証して不変。
3. Part AS refresh機のadapt (3ハンク: docstring文言 + canonical cache
   path + sha期待値のcache自体からの機械抽出 `1434c68b...`) =
   `reaudit/scripts/refresh_q042_ifadopted.py` を2回直列実行 (~61s/回)。
   4出力ともrun間byte一致: refresh-summary `029cc3b6...`,
   closure-classes `987c4ecb...`, per-root-coverage `ec71c81b...`,
   probe-worklist `af0c28c5...` (不出版・sha記録のみ)。
4. delta extractor `scripts/compare_deltas_q042_ifadopted.py` (Part AS版
   `9e885ae0...` のWIN if-adopted adapt) を3回実行・byte一致 (sha256
   `8e6ce1c6...`)・全gate PASS。graph + update8 + 両cacheから
   class_status_counts・既知universe数・per-root被覆を再計算し、published
   BASE (Part AS reaudit正本 `f2008e70...` / `3ee1dbb6...` /
   `527c7e9a...`) とif-adopted出力の両方に一致をfail-closedで保証。
   flips == s5 745184のBASE-unknownグラフ保持クラスの機械計算集合
   (ハードコードなし)、純WIN採用はclassをfree化しえない
   (新規free空集合gate)・per-root被覆を動かしえない (変更行0 gate)・
   新規free第三手空集合gate、q042不消費 (BASE cache不在 +
   BASE index_verdict不在の機械gate)、raw 2-pass再検証。

## 結果: if-adopted投影 (採用した場合の分類台帳の変化)

- **flips = 4クラス** `[23092, 23101, 23115, 23938]`。すべて
  s5 745184を費用子に持つgraph保持クラスで、すべてunknown→
  excluded_now遷移 (機械計算・gate済み)。遷移台帳:
  unknown→excluded_now 4 / unknown→unknown 34,496 /
  excluded→excluded 390 / excluded_now→excluded_now 23 /
  free_now→free_now 36。excluded_now回帰0 (gate)。**この4クラスの
  全LOSS閉包ルートはWIN子によって永久に反駁される** (route
  statement・閉鎖主張ではない)。
- canonical相当分類 (投影): excluded 390 / excluded_now 23→**27** /
  free_now **36不変** / unknown 34,500→**34,496**。
- **class 23101**: 保持クラスのひとつ。BASE-unknown子11個
  (q042の745184 + 未探査10キー) のうちWIN子が消費され、
  scenario-unknown子は**10個** (745455..745465・未探査のまま)。
  closure候補表には**rank 1・unknown_now 10のまま残る** (表は
  probing-worklist viewであり、flip自体はclass_status_countsと
  遷移台帳で記録)。表行数809不変・churnなし (退出0 / 新規0)。
  **class 10661 はrank 14不変** (unknown 52, batch-17候補)。
- per-root被覆: free/uncoveredの変更行**0** (全root不変・root 27
  baseline 119/119不変)。新規free第三手0 (gate)。per-root greedyは
  root 24のみ変化 (10 third free・個別greedy 2,785→2,784, −1・簿記)。
  joint greedy 36,726→**36,725** (−1)。probe worklist
  64,941→**64,940** (−1)。
- update8: resolved **79不変** (新規解決0・s5 745184はupdate8 baseline
  requirement外と機械判明)、remaining 31,780不変、groups_free 127不変、
  win_hit_groups BASE [] → scenario [] 不変、lost resolutions []
  (gate)。

## verdict消費の範囲とguards

- 本実験は**いかなるverdictも消費しない**。canonical cacheは出版済み
  6,120行 (`be9cb24e...`) のままbyte不変 (merge後に再検証)。if-adopted
  cache 6,121行はscrutiny owner向けのnon-canonical投影。
- **q042は15番目のunconsumed closure WINのまま**
  (b018/d002/e002/f017/g018/j033/h045/z003/n005/n006/p002/p003/r001/r002/
  q042)。WIN行採用は引き続きscrutiny ownerのC++第二実装ゲート
  (`cpp/solvers/kyouen_dfpn_root.cpp` pin `9193f5b6...`) 待ち。
  投影からexcluded_now化作戦価値を読み取って採用を急ぐことは本
  Partの主張ではない (推奨/却下いずれでもない)。
- **標準11×11空盤・19 central-reply roots・class 23101 (投影で
  excluded_now・主値はUNKNOWNの子10キー)・未着手q043-q052他全classは
  どの時点でもUNKNOWNのまま。nodes数・worklist数・greedy数を勝敗と
  して読まない。**

## ファイル

- `output/merged-exact-s5-chain-plus-closure-increment-plus-batch10-plus-batch16loss52-plus-batch14loss41-plus-q042win-IFADOPTED-20261122.cache`
  — if-adopted投影cache (6,121行・non-canonical・単一コミット出版)。
- `output/increment-q042-win-ifadopted-20261122.cache` — 単一WIN行
  increment (新bytes、本场で出版)。
- `output/increment-manifest.json` — if-adopted manifest
  (`batch14-q042-win-ifadopted-increment-manifest-v1`,
  ifadopted_only, canonical untouched pin機械表明)。
- `output/merge-audit-run1.json` / `output/merge-audit-run2.json` —
  merge監査 (3回実行・2ファイル出版・byte一致, sha256
  `e1d11a66...`)。
- `output/decomp-deltas-q042-ifadopted.json` — if-adopted deltaの全gate
  機械証明 (sha256 `8e6ce1c6...`・3回byte一致)。
- `reaudit/output/{refresh-summary.json, closure-classes.csv, per-root-coverage.csv}`
  — if-adopted refresh正本 (summary sha256 `029cc3b6...`・2回byte一致)。
- `reaudit/scripts/refresh_q042_ifadopted.py` — refresh機 (adapt版)。
- `scripts/{make_increment_q042_win.py, s5_union_merge.py, compare_deltas_q042_ifadopted.py}`
  — 本実験の機材 (mergerはpublished bytesのbyte-copy pin,
  maker/extractorはadapt版)。
- 不出版 (sha記録のみ): probe-worklist.csv (`af0c28c5...`) はPart
  AH/AO/AP/AS先例どおり不出版。実行log群 (merge-run*.log) は採用dir
  内部の作業記録 (MANIFEST対象外)。
