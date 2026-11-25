# batch-27: closure class 13342 exact-S5 probe (Part BR, 2026-11-23・takeover実行)

Part BR (宣言: note amendment commit `14ee1873`・scaffold commit `93ef3f89`・実行前に
出版・takeover amendment commit `d2e345e6`)。閉包候補表 (Part BI refresh reaudit
`d57a7609…` 807行) の **rank 26 class 13342** (mask [1188950301642588192, 0]・
groups served (5,24)(5,30)(5,55)(5,65)(24,5)(24,55)・cost 54子すべてunknown) を
対象とする exact-S5 probe batch。**verdict不消費**。閉鎖・被覆・secured・root
勝敗の主張はしない。

## 選定 (published baseから再導出・prose不使用・28-WIN交積)

- **rank 26 class 13342** は28-WIN交積空・known WIN子ゼロ・packet交差ゼロ・
  canonical hits 0/54・quarantine 0/54 (事前登録 maker `9ab4523a…` 全gate
  PASS・4回実行byte一致・tamper battery 8/8検出)。
  runner-up rank 27 class 5343・backup rank 28 class 13758。
- rank 24 class 1849 は unconsumed-WIN交積 {81011} (Part BQ l028)・rank 17
  class 12643 {115192} (a003)・rank 18 class 25835 {150241} (k002)・rank 19
  class 31600 {62435, 192809} (s001/s002)・rank 21 class 16957 {91296,
  368510} (y001/y006)・rank 23 class 30565 {68580, 191299} (i001/i002)。
- rank 20 class 10968・rank 22 class 23964 は PKT-collision blocked 継続
  (10968 = {273033}・23964 = {495193, 550880}・NOT route-dead)。rank 25
  class 5690 は route-dead (receipt WIN子 209644)。

## preflight・takeover時の再照合 (takeover host)

- 54キー o001..o054 (prefix "o"は27 published packets で未使用。s5昇順
  98526..460214・legal 74..100・Board再計算 54/54・membership {4:45, 3:8,
  2:1})。batch-keys.json `67814ed6…` (schema
  `n11-centralreply-closure-class13342-batch27-input-v1`)。
- takeover host (本実行host) で published script・input pins を再照合:
  drive_batch27.sh `9114e211…`・jsreplay.js `84585617…`・runbatch.sh
  `f591f8c2…`・runwave.sh `8efd78c2…`・make_batch27_keys.py `9ab4523a…`・
  row_audit_batch27.py `ed21debe…`・row_audit_batch27_win_halt.py
  `7d920f2b…` すべて byte一致。54 input CSV の (id, lo, hi, legal) と
  batch-keys 全行一致 (bad 0)。

## val-gate (pinned jsreplay `84585617…`)

- this-host 4ファイル (published) は宣言hostのpreflight再生成
  (wall_s 9/10/20/28)。
- **takeover-host 4ファイル (`*.takeover-host.out`) は本実行hostの再生成:
  4/4 node-exact (wall_s比較外・禁止四角 95,670)**: at2m 2キー result 0 /
  budget 2,000,000 exhaustion・15m基準キー (2, 3,651,923) と (2, 5,040,200)
  (wall_s 19/19/36/44)。

## drive-1 結果 (宣言commit `14ee1873`の事前登録stop rulesどおり・takeover host実行)

- drive invocation 1回 (drive_batch27.sh・2 worker・260s有界・2-pass fresh
  cold・budget 15M) で **worker2 rc=45 事前登録 WIN-HALT**。
- **o002 WIN (honest label): replay result 1・two-pass node-exact・nodes
  4,589,084 (budget 15M内)・key (3494793310856282144, 0)・s5 index
  209134・legal 79・membership 4・wall 45/47s** → worker2の最初のキーで
  事前登録 WIN-HALT rc=45・**29番目の unconsumed closure WIN候補**。
- worker1はworker2のWIN-HALT後に自workerの260s有界区間を継続し
  (driverのwait設計・runbatchは他workerの停止を観測しない)
  o001/o003/o005/o007 を完了後、o009実行中に timeout 124 で打ち切り:
  **o001/o003/o005/o007 はいずれも LOSS (採用候補のみ・verdict不消費)**
  (nodes 2,829,495 / 2,400,082 / 2,093,259 / 6,644,942・2-pass node-exact)。
- **fragment o009 (UNPROBED)**: o009.p1.out は `# replay_done` 付き完全
  単一パス (bookkeepingのみ・result 2 / nodes 9,082,839・証拠ではない)・
  o009.p2.out はtimeout打ち切りのtruncated断片 (verdict行なし)。published
  completeness guardが以降のcontinuationでfresh-cold再実行する。
- 残り48キー (o004, o006, o008, o010..o054) は fileless UNPROBED。
  EXHAUSTED 0・MISMATCH 0 (rc=42不発)・truncated-retry 0件 (retry再実行は
  未実施)。
- row-audit-winhalt (schema
  `n11-centralreply-closure-class13342-batch27-rowaudit-winhalt-v1`・事前
  登録版 script `7d920f2b…`: completed/fragment/fileless はrawの
  `# replay_done` 有無とstatus.logから導出・haltキーidは一切固定しない):
  PASS (completed 5 = WIN 1 + LOSS 4・fragment 1・fileless 48・unprobed
  49)・3回実行byte一致 ( json sha256 `530fe947…`)・tamper
  battery 3/3検出 (T1 o001 verdict反転→WIN-HALT pair照合gate・T2 未probe
  キー o010への偽PASS行→verdict-ish gate・T3 o002 verdict行除去→WIN-HALT
  pair照合gate・scratch上で実施し実験filesはbattery前後でbyte同一・
  clean control PASS)。

## 意味 (route statementのみ)

単独WIN子 o002 により (採用された場合) **class 13342 の全LOSS閉包ルートは
反駁証拠を持つ** (batch-21 a003・batch-22 k002・batch-26 l028 に続く4回目の
単独WIN子パターン)。ただし verdictは一切消費していない: 採用判断は
scrutiny owner C++第二実装 gate pin `9193f5b6…` 待ち (本レーンは代行しない)。
canonical cache (Part BU採用後 6,287行 `e32a2e44…`) は read-only・不変。
10968・23964 は blocked (packet交差・NOT route-dead)・5690 は route-deadの
まま。次batch (batch-28) 選定は **29-WIN交積** (28 + o002 (s5 209134)) の
反駁簿記でmaker内で機械選定する (当面のroute-alive候補: rank 27 class 5343
(runner-up)・rank 28 class 13758 (backup)・rank 29 class 14103。rank 30..
30484以降は要packet交差確認。prefix未使用文字は要再確認)。

## 検証規律

nodes数・expansions数を勝敗・距離として読まない。WIN/LOSS採用は別宣言の
adoption Part (pinned fail-closed merger `90711961`) 経由のみ。
**標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2
{59,60}・class 1/2/4・class 10968・class 23964・class 13342 (54キーすべて・
o002を含む) はどの時点でもUNKNOWNのまま。**

## 再現

1. `python3 scripts/make_batch27_keys.py` (published pinsをsha検査し54キーを
   再導出・全gate PASSで終了)。
2. `node scripts/jsreplay.js --exact-replay=val-gate/<...>.input.csv
   --exact-replay-budget=2000000|15000000` (val-gate 4件)。
3. `bash scripts/drive_batch27.sh` (残キーを2 worker 260s有界で順次
   2-pass fresh-cold・WIN-HALT rc=45は事前登録)。
4. `python3 scripts/row_audit_batch27_win_halt.py` (halt時点の部分行監査・
   byte一致JSONを再生成)。

## 出版コミット

- 宣言 note amendment `14ee1873` (Part BR宣言・実行前に出版)。
- scaffold `93ef3f89` 92ファイル予定のうち74ファイル (scripts 7 + input
  55 + val-gate 12)・fetch-back済み。
- takeover amendment `d2e345e6` (note・実行前に出版・all pins再照合)。
- outputs `28cf8c2f` 18ファイル (status.log・raw 12・row-audit-winhalt.json・
  val-gate takeover-host 4)・fetch-back 18/18 byte一致。
- (本commit) README + MANIFEST-sha256.txt 92行。
