# batch-23: closure class 31600 exact-S5 probe (Part BN, 2026-11-23)

Part BN (宣言: note amendment commit `bde1c7de`・実行前に出版)。閉包
候補表 (Part BI refresh reaudit `d57a7609…` 807行) の **rank 19 class
31600** (mask [1152921505160495104, 32768]・groups served
(24,29)(24,79)(25,30)(25,85)・cost 53子すべてunknown) を対象とする
exact-S5 probe batch。**verdict不消費**。閉鎖・被覆・secured・root
勝敗の主張はしない。

## 選定 (published baseから再導出・prose不使用)

- ranks 1..16 は従来どおり反駁済み (19/20/21-WIN交積またはknown WIN
  子。5830 は receipt WIN 5子・5687 は receipt WIN子 209644・rank 1
  class 23101 の unknown 集合は q042 のみ)。
- rank 17 class 12643 (batch-21対象) は unconsumed-WIN交積 {115192}
  (published Part BJ honest WIN行 a003・verdict不消費)。
- rank 18 class 25835 (batch-22対象) は**今回の反駁証拠が確定**:
  unknown子集合と21-unconsumed-WIN集合の交積は厳密に {150241}
  (published Part BL honest WIN行 k002・2ホストreplica + Part BM第三
  実装で裏付け済み・verdict不消費)。
- よって rank 19 class 31600 が published-table 順で最初の
  route-alive 候補。runner-up rank 20 class 10968・backup rank 21
  class 16957 はともに route-alive (cost 53子すべてunknown・maker内
  で機械検証)。

## preflight (fail-closed maker `make_batch23_keys.py` `7b2c8e53…`)

全gate PASS・4回実行byte一致・tamper battery 6/6検出 (graph sha pin /
CLASS_MASK 1bit / batch-22 prior-pin 1bit / prior-rows pin+1 /
rank-18 evidence pin / graph実ファイル末尾1bit)。

- 53キー s001..s053 (s5昇順 62435..924796・legal 78..95・Board再計算
  53/53・membership {3:8, 4:45})。
- canonical cache 6,235行 `f6649fe3…` hits 0/53・quarantine 0/53。
- prior 23 published packets (batches 1..22・1,140行・1,126一意)
  overlap 0・key id prefix "s" は全packetで未使用。
- batch-keys.json `2776acaf…` (schema
  `n11-centralreply-closure-class31600-batch23-input-v1`)。

## val-gate (pinned jsreplay `84585617…`・実行host)

4/4 node-exact (wall_s比較外・禁止四角 95,670):
at2m 2キー result 0 / budget 2,000,000 exhaustion・15m基準キー
(2, 3,651,923) と (2, 5,040,200)。

## drive-1 結果 (宣言commit `bde1c7de`の事前登録stop rulesどおり)

- **s001 WIN (honest label): replay result 1・two-pass node-exact・
  nodes 5,415,927 (budget 15M内)・key (1152921505294712832, 32768)・
  s5 index 62435・legal 78・membership 4・wall 51/56s** → 事前登録
  WIN-HALT rc=45 (worker1)。
- **s002 WIN (honest label): replay result 1・two-pass node-exact・
  nodes 9,329,444 (budget 15M内)・key (3458764514374189056, 32768)・
  legal 88・membership 4・wall 94/52s** → 事前登録 WIN-HALT rc=45
  (worker2)。両workerの最初のキーがともにWINであったためfragmentは
  ゼロ (batch-22とは異なりmid-flightキーなし)。
- 残り51キー (s003..s053) は fresh UNPROBED (fileless)。
- row-audit-winhalt (schema
  `n11-centralreply-closure-class31600-batch23-rowaudit-winhalt-v1`・
  **汎用事前登録版 script `f55ae559…`**: completed/fragment/fileless
  はrawの `# replay_done` 有無とstatus.logから導出・halt キーidは
  一切固定しない): PASS・3回実行byte一致 (json `14aa7f63…`・
  derived_state=true)・tamper battery 3/3検出 (p1 verdict反転 /
  未probeキーへの偽PASS行 / verdict行除去・scratch restoreで実験
  filesはbyte検証復元)。

## 意味 (route statementのみ)

s001・s002 の2つのWIN行により (採用された場合) **class 31600 の
全LOSS閉包ルートは反駁証拠を持つ** (batch-21/22 と同型の反駁パターン・
同一クラス内で2つの独立WIN子)。ただし verdictは一切消費していない:
s001・s002 は **22番目・23番目の unconsumed closure WIN 候補** で、
採用判断は scrutiny owner C++第二実装 gate pin `9193f5b6…` 待ち
(本レーンは代行しない)。canonical cache 6,235行 `f6649fe3…` は
read-only・不変。次batch選定は次回のランが21+2-WIN交積の反駁簿記で
行う。

## 検証規律

nodes数・expansions数を勝敗として読まない。WIN/LOSS採用は別宣言の
adoption Part (pinned fail-closed merger `90711961`) でのみ。
**標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・
S2 {59,60}・class 1/2/4・class 12643・class 25835 (53キーすべて)・
class 31600 (53キーすべて・s001/s002を含む) はどの時点でもUNKNOWNの
まま。**

## 再現

1. `python3 scripts/make_batch23_keys.py` (published pinsをsha検査し
   53キーを再導出・全gate PASSで終了)。
2. `node scripts/jsreplay.js --exact-replay=val-gate/<...>.input.csv
   --exact-replay-budget=2000000|15000000` (val-gate 4件)。
3. `bash scripts/drive_batch23.sh` (残キーを2 worker 260s有界で順次
   2-pass fresh-cold・WIN-HALT rc=45は事前登録)。
4. `python3 scripts/row_audit_batch23_win_halt.py` (halt時点の
   部分行監査・byte一致JSONを再生成)。

## 出版コミット

- A `52ff9a09` scaffold 73ファイル (scripts 7 + inputs 54 +
  val-gate 12)・fetch-back 73/73 byte一致。
- B `597d810` outputs 6ファイル (status.log・raw 4・
  row-audit-winhalt.json)・fetch-back 6/6 byte一致。
- C (本commit) README + MANIFEST-sha256 79行。
