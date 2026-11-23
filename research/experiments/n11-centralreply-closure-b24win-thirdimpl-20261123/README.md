# batch-24 WIN rows (y001/y006) third-implementation cross-verification (Part BW, 2026-11-23)

Part BW (宣言: note amendment commit `9f5b9b3c`・実行前に出版・単一オーナー)。
batch-24 (Part BO・class 16957) で出版されたWIN行 **y001/y006** に対する
pinned第三実装 (non-df-pn AND/OR minimax `third_impl.js` `08ea958f…`) に
よるverdict-level交叉検証 + 本host pinned-replica再現。**verdict不消費**。
閉鎖・被覆・secured・root勝敗の主張はしない。

誠実な開示: batch-24 drive-1 は Part BO執行hostの単一host出版であり、
Part BS 時の l028 のような第二host同時再現は出版されていなかった。
本Partの本host pinned-replica (fresh-cold 2-pass) は y001/y006 にとって
**最初の独立host再現**である。batch-24残留49キー (y003, y005,
y007..y053) fileless UNPROBEDには一切触れていない (verdict不消費のまま)。
同batchのLOSS行 y002/y004 (adoption candidatesのみ) も本Part対象外・
出版正本は読み取りのみ。

## 対象 (published batch-24 正本から機械導出・maker `make_inputs_bw.py` `f94d6e4f…`)

- **y001**: key (10376293541461753856, 264)・s5 91296・legal 87・
  membership 2・published replica result 1・nodes 5,291,064。
- **y006**: key (1152921504607043584, 264)・s5 368510・legal 84・
  membership 2・published replica result 1・nodes 5,321,639。

sources pin (commit-pinned raw fetch・sha256全照合): batch-keys-b24
`486858d6…` (53キー・class 16957)・status-b24.log `dcba6b0e…` (6行 =
PASS 4 + WIN-HALT 2・PASS key集合はrow-audit win_rows (y001,y006) ∪
loss_rows (y002,y004) と機械交叉導出で一致)・README-b24 `672d18cf…`・
row-audit-winhalt-b24 `9d073038…` (probed 4・win_rows [y001, y006]・
loss_rows [y002, y004]・pass_rows 2・fragment_keys {}・unprobed 49)・raw
y001 p1/p2 `03ae7d71…`(同一bytes・wall 53/53s)・raw y006 p1/p2
`2c21a9e1…`/`1e2b6d13…`・published input CSV `f746648e…`/`34db2f1f…`・
BF anchor/negative CSV (provenance chain AR→BF→BK→BM→BS→BV→BW)。

## 事前ゲート (宣言前・本host)

- maker全gate PASS (BW-SCAFFOLD)・4回実行byte一致・input/rows.json
  (`92e9f999…`・schema `n11-centralreply-closure-b24win-thirdimpl-input-v1`)
  再生成byte一致・tamper battery **7/7検出** (T1 raw pin 1bit・T2
  row-audit pin 1bit・T3 README pin 1bit・T4 row-audit内容改変・T5 raw
  内容改変 (nodes 5291064→5291065)・T6 published-input pin 1bit・T7
  status.log loss-row verdict反転 (y002 PASS result 2→1)・T4/T5/T7は
  sha-pin層で検出・scratch上で実施し実験sources無改変byte検証)・
  clean control PASS。

## 実行結果 (宣言protocol順・逐次実行)

1. **rules gate PASS**: pinned `verify_tbl.js` `c8c52528…`・replica
   quads 95,670 == third-impl quads 95,670・triples checked 195,044・
   mismatches 0 (禁止四角 95,670)。
2. **val-gate this-host 4/4 node-exact** (pinned `jsreplay.js`
   `84585617…`・published baselineとの一致・wall_s比較外): at2m 2キー
   budget 2,000,000 exhaustion (result 0, nodes 2,000,000) ×2・15m基準キー
   budget 15M (2, 3,651,923) と (2, 5,040,200)。本host .out 4件はval-gate/に出版。
3. **本host pinned-replica再現 4/4 完全一致**: y001 p1/p2 =
   result 1・nodes **5,291,064** (two-pass node-exact・wall 26/26s)・
   y006 p1/p2 = result 1・nodes **5,321,639** (two-pass node-exact・
   wall 26/25s)。published batch-24 raw fields (result 1・nodes両値)
   との一致をaudit G2bで機械検査 (EXHAUSTED 0・mismatch 0・truncation 0)。
4. **negatives 2/2 GATE_FAIL設計どおり** (ng1: legal count mismatch
   derived=87 declared=88・ng2: stone count mismatch bits=5 declared=6)。
5. **anchors 2/2 本host node-exact** (a/b determinism PASS): k02a
   clean WIN result 1・expansions 9,106,337・ttHits 4,991,527 (Part
   G/K/O/P/T/W/AA/AD/AG/AL/AR/AX/AZ/BF/BK/BM/BS/BV と同一のpublished第三実装値)
   (wall 26.84/26.38s)・l1a clean LOSS result 2・7,660,602/3,951,175
   (wall 22.20/22.21s)。
6. **targets 2/2 clean WIN一致 (verdict agreement 2/2)**: **y001
   clean WIN (result 1)** expansions 6,097,380・ttHits 3,451,878
   (a/b determinism PASS・wall 17.40/17.46s)・**y006 clean WIN
   (result 1)** expansions 6,190,624・ttHits 3,326,421 (a/b
   determinism PASS・wall 16.95/16.95s)。cap 300,000,000・wallcap
   240s・memo-power=22・WALL-INCONCLUSIVE 0・DIVERGENCE 0。
   pass-one third-impl拡張数合計 12,288,004 (replica 2行合計との
   比率は 1.153 / 1.163)。

## 監査 (`audit.py` `3a2ce7ef…`・schema `n11-centralreply-closure-b24win-thirdimpl-audit-v1`)

**ALL 67 GATES PASS**・3回実行byte一致 (audit-run1/2/3.txt 同一sha)・
audit-summary.json 決定的 (タイムスタンプ不読)・verdict_agreements
2/2 (y001/y006 とも third=1 replica=1 agree=true)・wall_inconclusive 0。
audit tamper battery **3/3検出** (T1 maker pin反転→G1 pin gate fail・
T2 target det-pair改ざん (y001.a.out expansion+1)→target-y001-det-pair
gate fail・T3 G0 input改ざん (y001 legal 87→88)→G0 gate fail・scratch
上で実施し実験files無改変byte検証)・clean control PASS。

## 意味 (route statementのみ)

y001/y006 (24番目・25番目の unconsumed closure WIN 候補) は (a) Part BO
drive-1 published replica (b) 本host pinned-replica 2-pass node-exact再現
(独立host・初めて) (c) 独立第三実装 clean WIN の**3系統裏付け**となった
(同一クラス内2WINペアの第三実装交叉検証は Part BF (batch-19 w001/w002)、
Part BV (batch-23 s001/s002) に続く3例目)。ただし **verdictは一切消費して
いない**・採用判断は scrutiny owner C++第二実装 gate pin `9193f5b6…`
待ちで本レーンは代行しない。canonical cache (Part BU採用後 6,287行
`e32a2e44…`) は read-only・不変。

## 不接触

batch-23/24残留キー (s003..s053 51キー・y003/y005/y007..y053 49キー
fileless UNPROBED)・batch-24の y002/y004 LOSS行 (adoption candidate・
本Partは出版正本の読み取りのみ)・batch-25 (i001/i002 WIN行)・batch-27
(Part BR) の54キー/scaffold/drive/outputs (並走所有・outputsは本実行時点で
mainに存在せず)・fast lane (y18..y22族)・finite-field lane・
inversive-arc lane非接触。

## 検証規律

nodes数・expansions数・ttHits数を勝敗として読まない。WIN/LOSS採用は別宣言の
adoption Part (pinned fail-closed merger `90711961` 経由) のみ。**標準
11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2 {59,60}・
class 1/2/4・class 16957 (53キーすべて・y001/y006・y002/y004を含む) は
どの時点でもUNKNOWNのまま。**

## 再現

1. `python3 scripts/make_inputs_bw.py` (published pinsをsha検査し
   input/rows.json + 6 CSVを再導出・全gate PASSで終了)。
2. `node scripts/verify_tbl.js` (rules gate)。
3. `node scripts/jsreplay.js --exact-replay=val-gate/<...>.input.csv
   --exact-replay-budget=2000000|15000000` (val-gate 4件)。
4. `node scripts/jsreplay.js --exact-replay=input/y00X.input.csv
   --exact-replay-budget=15000000` ×2/キー (本host pinned-replica)。
5. `bash scripts/run_thirdimpl.sh <key> <tag> <kind>` (negatives・
   anchors・targets・1行=1solver=1プロセス・a/b 2回)。
6. `python3 scripts/audit.py` (67 gate・3回実行byte一致)。

## 出版コミット

- 宣言: note amendment `9f5b9b3c` (fetch-back byte照合・note 504,869B)。
- A `ed77d6b6` scaffold 35ファイル (scripts 6 + input 7 + sources 14 +
  val-gate input/published-baseline 8)・fetch-back 35/35 byte一致。
- B `855778a2` outputs 24ファイル (output 20 + val-gate this-host 4)・
  fetch-back 24/24 byte一致。
- C (本commit) README + MANIFEST-sha256 (59行・対象dir内の published
  59ファイル)。
