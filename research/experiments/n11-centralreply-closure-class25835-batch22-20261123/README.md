# batch-22: closure class 25835 exact-S5 probe (Part BL, 2026-11-23)

Part BL (宣言: note amendment commit `8b27515b`・実行前に出版)。閉包
候補表 (Part BI refresh reaudit `d57a7609…` 807行) の **rank 18 class
25835** (mask [1152921504606982144, 8]・groups served
(12,17)(12,67)(15,20)(15,75)・cost 53子すべてunknown) を対象とする
exact-S5 probe batch。**verdict不消費**。閉鎖・被覆・secured・root
勝敗の主張はしない。

## 選定 (published baseから再導出・prose不使用)

- ranks 1..16 は従来どおり反駁済み (19/20-WIN交積またはknown WIN子。
  5830 は receipt WIN 5子・5687 は receipt WIN子 209644・rank 1
  class 23101 の unknown 集合は q042 のみ)。
- rank 17 class 12643 (batch-21対象) は**今回の反駁証拠が確定**:
  unknown子集合と20-unconsumed-WIN集合の交積は厳密に {115192}
  (published Part BJ honest WIN行 a003・verdict不消費)。
- よって rank 18 class 25835 が published-table 順で最初の
  route-alive 候補。runner-up rank 19 class 31600・backup rank 20
  class 10968 はともに route-alive (cost 53子すべてunknown)。

## preflight (fail-closed maker `make_batch22_keys.py` `945ba254…`)

全gate PASS・3回実行byte一致・tamper battery 4/4検出 (target rank
pin / prior-rows pin / a003 WIN行除去 / rank-17 evidence pin)。

- 53キー k001..k053 (s5昇順 91297..810380・legal 77..96・Board再計算
  53/53・membership {2:1, 3:8, 4:44})。
- canonical cache 6,235行 `f6649fe3…` hits 0/53・quarantine 0/53。
- prior 22 published packets (batches 1..21・1,087行・1,073一意)
  overlap 0・key id prefix "k" は全packetで未使用。
- batch-keys.json `b5f567bd…` (schema
  `n11-centralreply-closure-class25835-batch22-input-v1`)。

## val-gate (pinned jsreplay `84585617…`・実行host)

4/4 node-exact (wall_s比較外・禁止四角 95,670):
at2m 2キー result 0 / budget 2,000,000 exhaustion・15m基準キー
(2, 3,651,923) と (2, 5,040,200)。

## drive-1 結果 (宣言commit `8b27515b`の事前登録stop rulesどおり)

- **k002 WIN (honest label): replay result 1・two-pass node-exact・
  nodes 10,542,704 (budget 15M内)・key (1153484454560403456, 8)・
  s5 index 150241・legal 87・membership 4・wall 113/112s** → 事前登録
  WIN-HALT rc=45・batch停止。
- k001 fragment (UNPROBED): p1 は complete single-pass bookkeeping
  (result 0・nodes 15,000,000 budget exhaustion・**evidenceではない**)・
  p2 は drive timeout (260s) による truncated断片 (`# replay_done` なし)。
  published completeness guard により将来の continuation で
  fresh-cold 再実行。15M同一条件の再probe禁止規則は完走行のみに binding。
- 残り51キー (k003..k053) は fresh UNPROBED。
- row-audit-winhalt (schema
  `n11-centralreply-closure-class25835-batch22-rowaudit-winhalt-v1`・
  script `31e927e7…`): PASS・3回実行byte一致 (json `c6f7585c…`)・
  tamper battery 3/3検出 (p2 verdict反転 / status.log key-id改ざん /
  p1 key改ざん・scratch restoreで実験filesはbyte検証復元)。

## 意味 (route statementのみ)

k002 WIN行により **class 25835 の全LOSS閉包ルートは反駁証拠を持った**
(batch-21 class 12643 と同型の反駁パターン)。ただし verdictは一切
消費していない: k002 は **21番目の unconsumed closure WIN 候補** で、
採用判断は scrutiny owner C++第二実装 gate pin `9193f5b6…` 待ち
(本レーンは代行しない)。canonical cache 6,235行 `f6649fe3…` は
read-only・不変。

## 検証規律

nodes数・expansions数を勝敗として読まない。WIN/LOSS採用は別宣言の
adoption Part (pinned fail-closed merger `90711961`) でのみ。
**標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・
S2 {59,60}・class 1/2/4・class 25835 (53キーすべて・k002を含む)・
class 12643はどの時点でもUNKNOWNのまま。**

## 再現

1. `python3 scripts/make_batch22_keys.py` (published pinsをsha検査し
   53キーを再導出・全gate PASSで終了)。
2. `node scripts/jsreplay.js --exact-replay=val-gate/<...>.input.csv
   --exact-replay-budget=2000000|15000000` (val-gate 4件)。
3. `bash scripts/drive_batch22.sh` (残キーを2 worker 260s有界で順次
   2-pass fresh-cold・WIN-HALT rc=45は事前登録)。
4. `python3 scripts/row_audit_batch22_win_halt.py` (halt時点の
   部分行監査・byte一致JSONを再生成)。

## 出版コミット

- A `106c469` scaffold 72ファイル (scripts 6 + inputs 54 +
  val-gate 12)・fetch-back 72/72 byte一致。
- B `2ed5b90` outputs 7ファイル (status.log・raw 4・
  row-audit-winhalt.json・winhalt監査script)・fetch-back 7/7 byte一致。
- C (本commit) README + MANIFEST-sha256 79行。
