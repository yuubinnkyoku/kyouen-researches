# n11 central-reply JOINT 17-WIN if-adopted decomposition (Part BB, 2026-11-22)

単一オーナー宣言 (note Part BB amendment, commit `dafe9651`, observed
HEAD-before-push `53e7fae9`, note blob sha1 `762fc545...`) に基づく、
本repo履歴に存在する**すべてのunconsumed closure WIN行17行**
(b018 d002 e002 f017 g018 h045 j033 z003 n005 n006 / p002 p003 /
r001 r002 / q042 / v001 v002) を**単一投影で同時採用した場合**の
if-adopted投影計算。Part AT (q042単一WIN)・Part BA (v001+v002の2行)
の拡張であり、17個それぞれの個別分解は既に出版済みのため、本Partは
**全17行同時採用**の組み合わせケースを閉じる。scrutiny ownerの採用
判断に向けた事前計算であり、**verdictは不消費・canonical cacheは
byte不変・採用推奨/却下いずれでもない** (すべて機械表明・機械検査):

1. joint increments maker (`scripts/make_increment_17win_joint.py`,
   sha256 `4585c416...`) は勝敗行をrawから再導出しない。代わりに
   **5つのpublished source increment**をsha256 pinで upstream正道
   (main) から検証し (Part AJ wins10 `fe2c6f68...`・batch-13
   `bb238f67...`・batch-15 `05c10e1f...`・batch-14 q042
   `b4958328...`・batch-18 v001/v002 `4f8fc29b...`、各manifestも
   pin: `74fb877d...` / `43143fd5...` / `d6ed7b93...` /
   `894e9420...` / `13736030...`)、その17 WIN行が BASE不在
   (absent_hits 0)・quarantine不在 (0)・canonical-safe・s5 universe
   内であることを機械gateしたうえで、**17行joint increment**
   (sha256
   `04003820756b72bc3b35ac67746d9f6dd3dffd7315dbd2f36d50d497485cbe87`,
   joint manifest
   `509cc941fb77b6efccde23b64b7cc38c48814153d457c27a7b3576c47be9866d`,
   schema `joint17win-ifadopted-increment-manifest-v1`) を導出。
   maker 3回実行byte一致。17キーの一意性・q042/b18 manifestの
   key/s5/nodes機械交差・`win_s5_in_update8_baseline_requirement
   = 12` (update8 baseline requirement 31,859との機械交差) をgate。
2. sha-pinned fail-closed union merger (byte-copy pin
   `907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a`,
   selftest PASS) でcanonical 6,120行 (`be9cb24e...`, 不変) + 17 WIN行
   をmergeし、**joint if-adopted cache 6,137行** (WIN 175 /
   LOSS 5,962, conflict 0, duplicates elided 0, sha256
   `f8c2fd970e836eaf17f955b139b18e2e81c0e899c4652edfb0bc05d0790bf7e9`)
   を `output/merged-joint17win-IFADOPTED-20261122.cache` に生成
   (本repoのcanonical chainとは別物・non-canonical projection)。
   merge 2回実行・byte一致・merge-audit 2回byte一致 (双方 sha256
   `ae19b239cb4db449c3a5cd571e6f6447f2eddb9962d6c2d8b7d1cac701bac435`)。
   BASE canonicalはmerge後に再検証して不変。
3. Part BA refresh機のadapt (`reaudit/scripts/refresh_17win_ifadopted.py`,
   BA版 `d3fd8498...` から docstring文言 + projection cache path +
   cache sha期待値cache自体からの機械抽出 `f8c2fd97...` の3ハンク
   adapt) を3回直列実行 (~60s/回)。4出力ともrun間byte一致:
   refresh-summary `5cee4086...`, closure-classes `0c3c31f3...`,
   per-root-coverage `5ead108d...`, probe-worklist `4ca9e21b...`
   (3.7MB・不出版・sha記録のみ)。
4. delta extractor `scripts/compare_deltas_17win_ifadopted.py`
   (sha256 `1163b7c3...`, BA版 `c1c39b50...` の17-WIN拡張) を3回
   実行・byte一致 (delta json sha256
   `115677e6f4502967cf5ee5d787fb36f6f19006e9f35416ee970334ab4498e1c9`,
   39,648 bytes, schema
   `n11-joint17win-ifadopted-decomp-deltas-v1`)・全gate PASS:
   - **joint incrementを5つのsha-pinned source incrementからbyte再構築**
     し、published joint incrementと行単位でbyte一致を保証 (raw再検証は
     各source出版時の機械検査に委ね、そのbyte chainを二重pin)。
   - if-adopted cache == BASE + 17 (行数・shared行verdict一致・
     scenario-only行==17 WINキー)・WIN 158→175・LOSS 5,962不変。
   - **verdict不消費17/17**: 全17 WIN s5 indexが BASE cache不在 かつ
     BASE index_verdict (receipts込み) 不在 (機械gate)。
   - flips == 17 WIN s5のgraph保持クラス**和集合**のうちBASE-unknownの
     もの (per-s5 holder ledger + union + 交差、ハードコードなし)。
     各遷移はunknown→excluded_now・回帰0・新規free空集合gate・
     per-root free/uncovered変更行0 gate・新規free第三手空集合gate。
   - **13 source-class ledger** (provenance: upstream per-batch
     実験dir・うち4 classはsource manifest `class_index` と機械一致):
     BASE-unknown境界の和が17 WIN子**全て**を被覆 (機械gate)、
     13中12がflips内、**class 5830 (batch-15) は機械検証済みの例外**:
     BASEで既に別WIN子
     (`[126017, 131631, 162106, 197665, 206386]`) によりexcluded_now
     済みのためr001/r002採用はここに新規flipを作らない (共有費用子の
     効果はclass 2634側に現れる)。
   - class 16131のBASE-unknown子53個 == batch-18 53キー (BAと同じ強い
     一致gate)・scenario-unknown 51 == BASE-unknown minus {153671, 207534}。
   - update8: lost resolutions [] (gate)・newly-resolved ==
     baseline requirement ∩ 17 WIN s5 (機械再計算・12 index)・
     resolved 79→91 (delta == 12 == manifest `in_baseline_req`)
     算術一致・win_hit groupのserving classは全てflip集合内 (gate)。
   - closure候補表: 13 source classの全行について scenario unknown_now ==
     BASE minus 消費WIN子 (機械gate)・他の閉包表観測は簿記。
5. fail-closed改ざんテスト7種 (各改ざん後即復元・復元byte一致):
   joint increment nodes改ざん→INCR_SHA pin捕捉・if-adopted cache
   nodes改ざん→SCEN_CACHE_SHA pin捕捉・scenario summary count改ざん→
   SCEN_SUMMARY_SHA pin捕捉・extractor baseline定数改ざん (34500→
   34499) →再計算gate捕捉・extractor source-class pin改ざん
   (16930→16931) →ledger機械gate捕捉・upstream batch-13 increment
   改ざん→source sha pin捕捉・scenario closure CSV改ざん→SCEN_CLOSURE_SHA
   pin捕捉。すべてGATE FAILEDで終了し復元後再実行PASS。

## 結果: if-adopted投影 (採用した場合の分類台帳の変化)

- **flips = 42クラス** `[1518, 2634, 4139, 4843, 4864, 4889, 4892,
  4903, 5007, 5011, 5255, 5282, 5307, 5471, 5473, 5501, 5513, 5611,
  5613, 5626, 5632, 5748, 6030, 6073, 6147, 6166, 8106, 8785, 12264,
  12327, 14776, 15640, 16131, 16371, 16757, 16930, 20421, 23092,
  23101, 23115, 23938, 30345]`。遷移台帳: unknown→excluded_now 42 /
  unknown→unknown 34,458 / excluded→excluded 390 /
  excluded_now→excluded_now 23 / free_now→free_now 36。excluded_now
  回帰0 (gate)。**この42クラスの全LOSS閉包ルートはWIN子によって
  永久に反駁される** (route statement・閉鎖主張ではない)。
- canonical相当分類 (投影): excluded 390 / excluded_now 23→**65** /
  free_now **36不変** / unknown 34,500→**34,458**。
- **13 source classのunknown_now変化** (簿記・gate済み): 1518:
  51→50 / 2634: 51→48 (h045単独ではなく r001/r002との共有費用子込み
  で3子消費) / 5473: 51→50 / 5830: 52→50 (excluded_now済みだが
  unknown境界は残る) / 8106: 52→50 / 8785: 51→50 / 12264: 51→50 /
  16131: 53→51 / 16371: 49→48 / 16757: 29→28 / 16930: 52→50 /
  20421: 49→48 / 23101: 11→10。closure候補表のchurn: 退出
  `[5746]`・新規 `[5748]` (flipsによるworklist再構成・簿記)。
  class 16131はrank 15→**14** (unknown_now 51)。
- per-root被覆: free/uncoveredの変更行**0** (全root不変・root 27
  baseline 119/119不変)。新規free第三手0 (gate)。per-root greedy
  movers (簿記): root 0 −56・root 48 −6・root 49 +5・root 12 −3・
  root 14 +1・root 38 −2・root 26 −2・root 24 −1・root 36 −1・
  root 37 −1・root 5 −1。joint greedy 36,726→**36,727** (+1)。
  probe worklist 64,941→**64,917** (−24)。
- update8: resolved 79→**91** (新規12 index `[103558, 103560, 103561,
  153671, 184684, 188395, 197253, 198530, 207534, 219608, 415095,
  528497]`・すべてbaseline requirement内・機械再計算一致)、
  remaining_now 31,780→**31,389** (−391: 34 win-hit groupがfrozen
  per-group unknown和集合から除外される・published refreshの機械
  計算)、groups_free_now 127不変、win_hit_groups **[]→34** (34 group
  すべてflip集合内のclassがserve・gate)、lost resolutions [] (gate)。

## verdict消費の範囲とguards

- 本実験は**いかなるverdictも消費しない**。canonical cacheは出版済み
  6,120行 (`be9cb24e...`) のままbyte不変 (merge後に再検証)。
  if-adopted cache 6,137行はscrutiny owner向けのnon-canonical投影。
- 17 WIN行は全て**unconsumed closure WINのまま**。これで17個すべての
  unconsumed closure WINが単独・2行・10行・17行両極のif-adopted分解を
  持った。WIN行採用は引き続きscrutiny ownerのC++第二実装ゲート
  (`cpp/solvers/kyouen_dfpn_root.cpp` pin `9193f5b6...`) 待ち。投影
  からexcluded_now化作戦価値を読み取って採用を急ぐことは本Partの
  主張ではない (推奨/却下いずれでもない)。
- **標準11×11空盤・19 central-reply roots・全classはどの時点でも
  UNKNOWNのまま。nodes数・worklist数・greedy数を勝敗として読まない。**

## ファイル

- `output/merged-joint17win-IFADOPTED-20261122.cache` — joint
  if-adopted投影cache (6,137行・non-canonical・単一コミット出版)。
- `output/increment-17win-joint-IFADOPTED-20261122.cache` — 17 WIN行
  joint increment (新bytes、本场で出版)。
- `output/increment-manifest.json` — joint if-adopted manifest
  (`joint17win-ifadopted-increment-manifest-v1`, ifadopted_only,
  canonical untouched pin機械表明、5 source sha pin内包)。
- `output/merge-audit-run1.json` / `output/merge-audit-run2.json` —
  merge監査 (2回実行・両ファイル出版・byte一致, sha256
  `ae19b239...`)。
- `output/decomp-deltas-joint17win-ifadopted.json` — if-adopted
  deltaの全gate機械証明 (sha256 `115677e6...`・3回byte一致)。
- `reaudit/output/{refresh-summary.json, closure-classes.csv,
  per-root-coverage.csv}` — joint if-adopted refresh正本 (summary
  sha256 `5cee4086...`・3回byte一致)。
- `reaudit/scripts/refresh_17win_ifadopted.py` — refresh機 (adapt版)。
- `scripts/{make_increment_17win_joint.py, s5_union_merge.py,
  compare_deltas_17win_ifadopted.py}` — 本実験の機材 (mergerは
  published bytesのbyte-copy pin、maker/refresh/extractorはadapt版)。
- 不出版 (sha記録のみ): probe-worklist.csv (`4ca9e21b...`) はPart
  AH/AO/AP/AS/AT/BA先例どおり不出版。input/の作業用コピーは
  upstream正道bytesとsha一致検証済み (commit-pinned rawで再検証) の
  ため再出版せず、下記status.logに取得根拠を記録。
