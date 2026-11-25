# n11 central-reply batch-16 (class 10687) 52-LOSS canonical adoption reaudit (Part AP, 2026-11-22)

単一オーナー宣言 (note Part AP, commit `815391db`, observed HEAD-before-push
`a71bef64`) に基づく、batch-16 (class 10687) の52 LOSS行をcanonical cacheへ
計上する採用・再監査実験。Part AM (batch-16 完走: 52/52全LOSS・2-pass
node-exact・枯損0・WIN 0) とPart AO (PLOSS52 what-if分解) の直接後続であり、
batch-2 23963 / batch-10 8784 / 10324 と同一の採用形式:

1. published increments maker (`e35b545d...`) を再実行して52 LOSS行の
   increment (sha256 `95345a5b1484614940e133e042b005ccc5963df15ecb7e5651f092761aa8a7f0`,
   manifest sha256 `28c90ba7...`) をpublished Part AO bytesとbyte一致で再導出。
2. sha-pinned fail-closed union merger (`90711961...`, selftest PASS) で
   採用前canonical cache 6,027行 (`95e868d6...`,
   `research/experiments/n11-central-reply-8784-closure-reaudit-20261122/output/merged-exact-s5-chain-plus-closure-increment-plus-batch10-20261122.cache`)
   にincrementをmergeし、**canonical cache 6,079行**
   (WIN 158 / LOSS 5,921, sha256
   `342e86838e0c2bef915798059cb397f7c91e59c65426bf74db19530ecdd7979e`, 249,622 bytes)
   を新path `output/merged-exact-s5-chain-plus-closure-increment-plus-batch10-plus-batch16loss52-20261122.cache`
   に出版 (本repoの次のcanonical exact-S5 verdict cache)。merge 2回実行・
   byte一致・WIN/LOSS conflict 0。Part AO scenario cacheとbyte同一 (機械cmp)。
3. Part Y refresh script (`88671526...`) のadapt (Part AO adapt `fb846776...`
   からdocstring文言とcache pathのみの2ハンク変更・cache sha期待値は
   `342e8683...` 不変) を2回直列実行。4出力ともrun間byte一致。
   3 CSV出力はPart AOのwhat-if出力とbyte同一
   (`7405699e...` / `ec52a56d...` / worklist `3b28ba59...`は不出版・sha記録)、
   refresh-summaryはpublished BASE 対照 (root27 119/119) を含み
   `pins.merged_cache.path` の1行のみ差分 (機械diff検証)。
4. delta extractor 3回実行・byte一致・全gate PASS
   (`scripts/compare_deltas_batch16_adoption.py` = published Part AO extractor
   `ca2a14f7...` の11箇所文言/pin adapt・再計算gate群は全て不変)。graph +
   update8 + canonical cacheからclass_status_counts・既知universe数・
   per-root被覆を再計算し、published BASE (`25987add...`) と本reaudit出力の
   両方と一致をfail-closedで保証。出力JSONはPart AO `dd6a01ef...` と文言
   3欄+pins 1欄以外全byte同一。

## 結果: class 10687の閉鎖資格確定

- canonical分類: excluded 390 / excluded_now 23 / **free_now 36** /
  unknown 34,500 (採用前: 35 / 34,501)。`board_verification`:
  free_candidates 36, **board_verified_free 36**, rejected {} — class 10687
  のfree化は独立整数幾何Boardによる全子境界再生成のもとで機械検証済み
  (what-if投影ではなくcanonical状態)。
- closure候補表: 810行 (採用前811行)。**class 10687は表から消滅**
  (grep 0行)。次のrank 14候補はclass 10661
  (mask `[1152921505697431552, 0]`, unknown 52, groups (24,30)系)
  = 機械特定された次のall-LOSS候補 (batch-17)。
- per-root: 変更行は (central, 16) のみ。free 14→16, uncovered 105→103
  (free+uncovered==119不変)、root 27 baseline 119/119不変、他18 root不変。
  新規free第三手 {(16,56),(16,64)} はpublished batch-16 groups_served_full
  と機械一致、root 16の2 group secured。
- update8: resolved 75→76 (s5 376421), remaining 31,784→31,783,
  win_hit_groups 0不変。
- スケジューリング数量 (簿記): joint greedy 35,242→38,522 (free化group
  除外後の再選択・被覆後退ではない), probe worklist 65,154→65,097 (-57)。

## verdict消費の範囲とguards

- 本実験で消費したverdictはbatch-16の52 LOSS行のみ (fail-closed merger
  経由・zero-WIN full-packet採用は合法・published manifestで機械表明)。
- WIN行の採用は引き続きscrutiny ownerのC++第二実装ゲート
  (`cpp/solvers/kyouen_dfpn_root.cpp` pin `9193f5b6...`) 待ち。14 unconsumed
  closure WIN (b018/d002/e002/f017/g018/j033/h045/z003/n005/n006/p002/p003
  +2) は不変。batch-14 (Part AQ, class 23101, in flight) とはキー・ファイル
  非交差で非接触。batch-15 (Part AN if-adopted) は本Partでは計上していない。
- **標準11×11空盤・19 central-reply roots・他全classはどの時点でもUNKNOWN
  のまま。本実験の確定はcanonical cache上の分類 (class 10687閉鎖資格) のみ。
  nodes数・worklist数・greedy数を勝敗として読まない。**

## ファイル

- `output/merged-exact-s5-chain-plus-closure-increment-plus-batch10-plus-batch16loss52-20261122.cache`
  — 新canonical verdict cache (6,079行・単一コミット出版)。
- `output/merge-audit-run1.json` / `output/merge-audit-run2.json` —
  canonical merge監査 (2回byte一致, sha256 `b69ea953...`)。
- `output/decomp-deltas-batch16-adoption.json` — 採用deltaの全gate機械証明
  (sha256 `70c1b31e...`)。
- `reaudit/output/{refresh-summary.json, closure-classes.csv, per-root-coverage.csv}`
  — 採用後refresh正本 (summary sha256 `b278f822...`)。
- `reaudit/scripts/refresh_adoption_10687.py` — refresh機 (adapt版)。
- `scripts/{make_increments_batch16.py, s5_union_merge.py,
  compare_deltas_batch16_adoption.py}` — 本実験の機材 (maker/mergerはpublished
  bytesのbyte-copy, extractorはadapt版)。
- 不出版 (sha記録のみ): 再導出increment (`95345a5b...`) とmanifest
  (`28c90ba7...`) はPart AO published bytesと同一のため本文献に再導出機跡
  のみ記録。probe-worklist.csv (3.7MB, `3b28ba59...`) はPart AH/AO先例どおり
  不出版。実行log群 (run1-maker.log, merge-run*.log, reaudit/run*.log,
  extractor-run*.log) は採用dir内部の作業記録 (MANIFEST対象外)。
