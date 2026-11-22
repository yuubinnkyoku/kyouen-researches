# n11 central-reply batch-14 (class 23101) 41-LOSS canonical adoption reaudit (Part AS, 2026-11-22)

単一オーナー宣言 (note Part AS amendment, commit `5b6af2ed`, observed
HEAD-before-push `b394c3ca`, note blob sha1 `7a534356...`) に基づく、
batch-14 (class 23101) の41 LOSS行をcanonical cacheへ計上する採用・再監査
実験。Part AQ (batch-14 完走: 52探査キー中42キーが2-pass node-exactで解決、
41 LOSS / **1 WIN (q042)** / 枯損0 / 不一致0、事前登録WIN-HALT則で停止)
とPart AR (batch-14正本のpublication検証 144/144 byte一致) の直接後続。
batch-2 23963 / batch-10 8784 / 10324 / batch-16 10687 (Part AP) と同一の
採用形式だが、**full != loss**: 採用パケットは41 LOSS行のみで、単一WIN行
q042 (s5_index 745184, result 1, 9,149,084 nodes) は不採用・verdict不消費
(すべて機械表明・機械検査):

1. increments maker (`scripts/make_increments_batch14.py` = published Part AP
   maker `e35b545d...` のbatch-14 adapt) をpublished batch-14 raws
   (publication commit `7b211d38`) から再実行し、41 LOSS行 increment
   (sha256 `5194af934a5373823a819ec53178dd008d1c6d5b17488101aa742ca1230d0831`,
   manifest sha256 `8b5540f9...`, schema `batch14-loss41-increments-manifest-v1`)
   を導出。q042の2-pass WIN結果はrawから機械再検証のうえ除外
   (`unadopted_win_ids == ["q042"]`, `full_packet_eq_loss_only == false`,
   `win_scenario_exists == true` をmanifestが機械表明)。
2. sha-pinned fail-closed union merger (`90711961...`, byte-copy pin,
   selftest PASS) で採用前canonical cache 6,079行
   (`342e8683...`, Part AP正本) にincrementをmergeし、**canonical cache
   6,120行** (WIN 158 / LOSS 5,962, conflict 0, duplicates 0, sha256
   `be9cb24e899fbe93db51e415320c50fa733e378748bb7a41fe13fd7b22f06685`,
   251,466 bytes) を新path
   `output/merged-exact-s5-chain-plus-closure-increment-plus-batch10-plus-batch16loss52-plus-batch14loss41-20261122.cache`
   に出版 (本repoの次のcanonical exact-S5 verdict cache)。merge 2回実行・
   byte一致・merge-audit 2回byte一致 (sha256 `54c581ee...`)。
3. Part AP refresh機 (`ad3dc0e6...`) のadapt (docstring文言 + canonical
   cache path + sha期待値のcache自体からの機械抽出・3ハンク) =
   `reaudit/scripts/refresh_adoption_23101.py` を2回直列実行 (~61s/回)。
   4出力ともrun間byte一致: refresh-summary `f2008e70...`,
   closure-classes `3ee1dbb6...`, per-root-coverage `527c7e9a...`,
   probe-worklist `1c96df05...` (3.7MB, Part AH/AO/AP先例どおり不出版・
   sha記録のみ)。
4. delta extractor `scripts/compare_deltas_batch14_adoption.py` (Part AP版
   `f78f7e60...` のbatch-14 adapt) を3回実行・byte一致 (sha256
   `7155fdaa...`)・全gate PASS。graph + update8 + canonical cacheから
   class_status_counts・既知universe数・per-root被覆を再計算し、published
   BASE (Part AP reaudit正本 `b278f822...` / `7405699e...` / `ec52a56d...`,
   公式raw commit `20deb45d` で取得・sha検証) と本reaudit出力の両方に一致
   をfail-closedで保証。q042不消費は6面で機械gate (increment・BASE・
   scenario cache・quarantine・index_verdict・class 23101のscenario-unknown
   子集合)。

## 結果: class 23101のunknown境界 52 → 11 (閉鎖ではなく前進)

- canonical分類: excluded 390 / excluded_now 23 / free_now 36 / unknown
  34,500 (**全域で不変**)。遷移台帳: すべてのclassが unknown→unknown 等
  同一遷移 (機械gate済み)。excluded_now flip 0・新規free 0 (zero-WIN
  採用ではfree化・flipとも起きえない: 計算で担保されgate済み)。
- **class 23101**: BASE-unknown費用子52個のうち41個がincrementで解決。
  scenario-unknown子は**11個** (q042の745184 + 未探査10キー:
  745184, 745455..745465)。closure候補表の**rank 12 → rank 1**
  (unknown_now 11)。freeにもexcludedにもならない (q042不消費+未探査
  10キーのため)。次の一手はこの11キー (1キーはWINが既知・10キー未探査)。
- closure候補表: 810→809行 (退出7: 1250, 2233, 4912, 15394, 22002,
  22119, 22859 / 新規6: 21387, 21934, 22925, 23075, 23102, 23283 =
  台帳churn)。**class 10661 はrank 14不変** (unknown 52, batch-17候補)。
- per-root被覆: free/uncoveredの変更行**0** (全root不変・root 27 baseline
  119/119不変)。individual greedy列のみ8 rootで変化 (root 2: -227など・
  簿記)。joint greedy 38,522→**36,726** (-1,796)。probe worklist
  65,097→**64,941** (-156)。
- update8: resolved 76→**79** (+3: s5 707915, 713201, 740437, すべて
  LOSS・increment内と機械gate済み), remaining 31,783→31,780,
  groups_free 127不変。

## verdict消費の範囲とguards

- 本実験で消費したverdictはbatch-14の41 LOSS行のみ (fail-closed merger
  経由・partial-packet zero-WIN採用)。**q042 WIN行 (15番目のunconsumed
  closure WIN) は不採用・不消費**。12行のKIT評価のほかunconsumed closure
  WIN (b018/d002/e002/f017/g018/j033/h045/z003/n005/n006/p002/p003 +2 +
  q042 = 15) は不変。
- WIN行の採用は引き続きscrutiny ownerのC++第二実装ゲート
  (`cpp/solvers/kyouen_dfpn_root.cpp` pin `9193f5b6...`) 待ち。
- **標準11×11空盤・19 central-reply roots・他全classはどの時点でもUNKNOWN
  のまま。本実験の確定はcanonical cache上の分類 (class 23101のunknown
  境界52→11とrank 1) のみ。nodes数・worklist数・greedy数を勝敗として
  読まない。**

## ファイル

- `output/merged-exact-s5-chain-plus-closure-increment-plus-batch10-plus-batch16loss52-plus-batch14loss41-20261122.cache`
  — 新canonical verdict cache (6,120行・単一コミット出版)。
- `output/increment-batch14-loss41-20261122.cache` — 採用41 LOSS行
  increment (新bytes、本场で出版)。
- `output/increments-manifest.json` — 採用manifest
  (`batch14-loss41-increments-manifest-v1`, full != loss機械表明)。
- `output/merge-audit-run1.json` / `output/merge-audit-run2.json` —
  canonical merge監査 (2回byte一致, sha256 `54c581ee...`)。
- `output/decomp-deltas-batch14-adoption.json` — 採用deltaの全gate機械証明
  (sha256 `7155fdaa...`)。
- `reaudit/output/{refresh-summary.json, closure-classes.csv, per-root-coverage.csv}`
  — 採用後refresh正本 (summary sha256 `f2008e70...`・2回byte一致)。
- `reaudit/scripts/refresh_adoption_23101.py` — refresh機 (adapt版)。
- `scripts/{make_increments_batch14.py, s5_union_merge.py,
  compare_deltas_batch14_adoption.py}` — 本実験の機材 (mergerは
  published bytesのbyte-copy pin, maker/extractorはadapt版)。
- 不出版 (sha記録のみ): probe-worklist.csv (3.7MB, `1c96df05...`) は
  Part AH/AO/AP先例どおり不出版。実行log群 (merge-run*.log,
  reaudit/run*.log, extractor実行log) は採用dir内部の作業記録
  (MANIFEST対象外)。
