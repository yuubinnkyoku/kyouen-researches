# n11 central-reply v001+v002 two-WIN if-adopted decomposition (Part BA, 2026-11-22)

単一オーナー宣言 (note Part BA amendment, commit `607c876a`, observed
HEAD-before-push `f8cc6c9d`, note blob sha1 `01e980d9...`) に基づく、
batch-18 (class 16131) の不採用WIN行 2行 (v001: s5_index 153671,
result 1, 5,656,151 nodes / v002: s5_index 207534, result 1,
7,898,204 nodes) を**同時採用した場合**のif-adopted投影計算。
Part AT (q042単一WIN if-adopted, batch-23系の直接前級) の2行版であり、
17個のunconsumed closure WINのうちif-adopted分解を欠いていた残り
2行 (v001/v002) のギャップを閉じる。scrutiny ownerの採用判断に向けた
事前計算であり、**verdictは不消費・canonical cacheはbyte不変・採用
推奨/却下いずれでもない** (すべて機械表明・機械検査):

1. increments maker (`scripts/make_increment_v001v002_win.py`) を
   published batch-18 raws (raws publication commit `3c07f51a`,
   docs `938e34f2`) から再実行し、v001/v002の2-pass WINを機械再検証の
   うえ2行 increment (sha256
   `4f8fc29bfd00492aa9a983f20a121737d395b8f80d53e2b04c271fec068bc1ee`,
   manifest sha256
   `13736030ea484a0496da7f929b9c6892a2e9ebf6522f96d1c87d2c21000945f1`,
   schema `batch18-win-v001v002-ifadopted-increment-manifest-v1`) を
   導出。maker 3回実行byte一致。BASE不在 (6,120行・absent_hits 0)・
   quarantine不在 (0 hit) をgate。
2. sha-pinned fail-closed union merger (byte-copy pin
   `907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a`,
   selftest PASS) でcanonical 6,120行 (`be9cb24e...`, 不変) + 2 WIN行を
   mergeし、**if-adopted cache 6,122行** (WIN 160 / LOSS 5,962,
   conflict 0, duplicates elided 0, sha256
   `6bfa9faa1dec17cfb827a50668e84f289ffcc7dcb115591fc3280293b1f0f0b6`,
   251,556 bytes) を
   `output/merged-exact-s5-chain-plus-closure-increment-plus-batch10-plus-batch16loss52-plus-batch14loss41-plus-b18win-v001v002-IFADOPTED-20261122.cache`
   に生成 (本repoのcanonical chainとは別物・non-canonical projection)。
   merge 2回実行・byte一致・merge-audit 2回byte一致 (sha256
   `4cdad34ba426abf9aadb04a2f9f6b4199d918185ae8a6076c98bba0aa38a1374`)。
   BASE canonicalはmerge後に再検証して不変。
3. Part AT refresh機のadapt (`reaudit/scripts/refresh_v001v002_ifadopted.py`,
   AT版 `5f9810e6...` からdocstring文言 + projection cache path +
   cache sha期待値cache自体からの機械抽出 `6bfa9faa...` の2ハンクadapt)
   を2回直列実行 (~60s/回)。4出力ともrun間byte一致:
   refresh-summary `af95270b...`, closure-classes `e5a91e15...`,
   per-root-coverage `9f59ebf8...`, probe-worklist `18429b91...`
   (3.7MB・不出版・sha記録のみ)。
4. delta extractor `scripts/compare_deltas_v001v002_ifadopted.py`
   (AT版 `207cfbcc...` の2-WIN adapt) を3回実行・byte一致 (sha256
   `e3679aaea33ed4aa020e63cadfb070b45d7a84a453eb1cde66481fb3fae5b473`)・
   全gate PASS。graph + update8 + 両cacheからclass_status_counts・
   既知universe数・per-root被覆を再計算し、published BASE (Part AS
   reaudit正本 `f2008e70...` / `3ee1dbb6...` / `527c7e9a...`) と
   if-adopted出力の両方に一致をfail-closedで保証。さらに:
   - flips == s5 153671 / 207534のgraph保持クラスの**和集合**のうち
     BASE-unknownのものの機械計算集合 (ハードコードなし)。単独
     holder集合 (v001: [4139, 16131] / v002: [5611, 6073, 16131])、
     和集合、積集合 (double holders = [16131]) をすべて機械計算。
   - **class 16131のBASE-unknown子53個 == batch-18の53キーのs5 index
     集合** (新規の強い一致gate)。
   - 純WIN採用はclassをfree化しえない (新規free空集合gate)・
     per-root被覆を動かしえない (変更行0 gate)・新規free第三手空
     集合gate。
   - verdict不消費: BASE cache不在 + BASE index_verdict不在 (両s5) の
     機械gate、v001/v002 raw 2-pass再検証 (p1/p2一致・legal一致)。
   - fail-closed改ざんテスト: increment nodes改ざん→INCR_SHA pinで
     捕捉、scenario summary count改ざん→SCEN_SUMMARY_SHA pinで捕捉、
     batch-keys s5_index改ざん→BATCH_KEYS_SHA pinで捕捉、extractor
     定数改ざん (v002 s5 / BATCH_CLASS) →manifest gateで捕捉、
     すべて改ざん後即復元・復元byte一致を確認。

## 結果: if-adopted投影 (採用した場合の分類台帳の変化)

- **flips = 4クラス** `[4139, 5611, 6073, 16131]`。すべてs5 153671
  または207534を費用子に持つgraph保持クラスで、すべてunknown→
  excluded_now遷移 (機械計算・gate済み)。遷移台帳:
  unknown→excluded_now 4 / unknown→unknown 34,496 /
  excluded→excluded 390 / excluded_now→excluded_now 23 /
  free_now→free_now 36。excluded_now回帰0 (gate)。**この4クラスの
  全LOSS閉包ルートはWIN子によって永久に反駁される** (route
  statement・閉鎖主張ではない)。各holderのunknown_now変化:
  4139: 100→99 / 5611: 107→106 / 6073: 104→103 / 16131: 53→51
  (double holderは16131のみ)。
- canonical相当分類 (投影): excluded 390 / excluded_now 23→**27** /
  free_now **36不変** / unknown 34,500→**34,496**。
- **class 16131**: 唯一のdouble holder。BASE-unknown子53個
  (= batch-18 53キー・gate済み) のうちWIN子2個が消費され、
  scenario-unknown子は**51個**。closure候補表ではrank 15→**7**
  (unknown_now 51・groups_served 5、5つのwin-hit group
  (12,50)/(12,70)/(48,20)/(48,72)/(48,100)は全て16131のgroup)。
  表行数809不変・churnなし (退出0 / 新規0)。表はprobing-worklist
  viewであり、flip自体はclass_status_countsと遷移台帳で記録。
- per-root被覆: free/uncoveredの変更行**0** (全root不変・root 27
  baseline 119/119不変)。新規free第三手0 (gate)。per-root greedyは
  root 12 (3,030→3,028) とroot 48 (2,879→2,877) が−2ずつ (簿記)。
  joint greedy 36,726→**36,724** (−2)。probe worklist
  64,941→**64,939** (−2)。
- update8: resolved 79→**81** (新規 [153671, 207534]・両WINとも
  baseline requirement内)、remaining_now 31,780→**31,729**
  (−51: class 16131の5 win-hit groupがfrozen per-group unknown和集合
  から除外され、その51個の残存unknown子は他の維持groupのremaining
  集合に現れないため・published refreshの機械計算)、groups_free_now
  127不変、win_hit_groups **[]→5** (全てclass 16131の5 closure
  groups)、lost resolutions [] (gate)。

## verdict消費の範囲とguards

- 本実験は**いかなるverdictも消費しない**。canonical cacheは出版済み
  6,120行 (`be9cb24e...`) のままbyte不変 (merge後に再検証)。
  if-adopted cache 6,122行はscrutiny owner向けのnon-canonical投影。
- **v001/v002は16番目・17番目のunconsumed closure WINのまま**
  (b018/d002/e002/f017/g018/j033/h045/z003/n005/n006/p002/p003/
  r001/r002/q042に続き)。17個すべてのunconsumed closure WINが
  if-adopted分解を持ったことになる。WIN行採用は引き続きscrutiny
  ownerのC++第二実装ゲート (`cpp/solvers/kyouen_dfpn_root.cpp` pin
  `9193f5b6...`) 待ち。投影からexcluded_now化作戦価値を読み取って
  採用を急ぐことは本Partの主張ではない (推奨/却下いずれでもない)。
- **標準11×11空盤・19 central-reply roots・class 16131 (投影で
  excluded_now・主値はUNKNOWNの子51キー)・未着手batch-18残り51キー
  他全classはどの時点でもUNKNOWNのまま。nodes数・worklist数・
  greedy数を勝敗として読まない。**

## ファイル

- `output/merged-exact-s5-chain-plus-closure-increment-plus-batch10-plus-batch16loss52-plus-batch14loss41-plus-b18win-v001v002-IFADOPTED-20261122.cache`
  — if-adopted投影cache (6,122行・non-canonical・単一コミット出版)。
- `output/increment-b18win-v001v002-ifadopted-20261122.cache` — 2 WIN行
  increment (新bytes、本场で出版)。
- `output/increment-manifest.json` — if-adopted manifest
  (`batch18-win-v001v002-ifadopted-increment-manifest-v1`,
  ifadopted_only, canonical untouched pin機械表明)。
- `output/merge-audit-run1.json` / `output/merge-audit-run2.json` —
  merge監査 (2回実行・両ファイル出版・byte一致, sha256
  `4cdad34b...`)。
- `output/decomp-deltas-v001v002-ifadopted.json` — if-adopted deltaの
  全gate機械証明 (sha256 `e3679aae...`・3回byte一致)。
- `reaudit/output/{refresh-summary.json, closure-classes.csv, per-root-coverage.csv}`
  — if-adopted refresh正本 (summary sha256 `af95270b...`・2回byte一致)。
- `reaudit/scripts/refresh_v001v002_ifadopted.py` — refresh機 (adapt版)。
- `scripts/{make_increment_v001v002_win.py, s5_union_merge.py, compare_deltas_v001v002_ifadopted.py}`
  — 本実験の機材 (mergerはpublished bytesのbyte-copy pin、
  maker/refresh/extractorはadapt版)。
- 不出版 (sha記録のみ): probe-worklist.csv (`18429b91...`) はPart
  AH/AO/AP/AS/AT先例どおり不出版。
