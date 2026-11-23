# batch-23 WIN rows (s001/s002) third-implementation cross-verification (Part BV, 2026-11-23)

Part BV (宣言: note amendment commit `d58afadd`・実行前に出版・単一オーナー)。
batch-23 (Part BN・class 31600) で出版されたWIN行 **s001/s002** に対する
pinned第三実装 (non-df-pn AND/OR minimax `third_impl.js` `08ea958f…`) に
よるverdict-level交叉検証 + 本host pinned-replica再現。**verdict不消費**。
閉鎖・被覆・secured・root勝敗の主張はしない。

誠実な開示: batch-23 drive-1 は Part BN執行hostの単一host出版であり、
Part BS 時の l028 のような第二host同時再現は出版されていなかった。
本Partの本host pinned-replica (fresh-cold 2-pass) は s001/s002 にとって
**最初の独立host再現**である。batch-23残留51キー (s003..s053) fileless
UNPROBEDには一切触れていない (verdict不消費のまま)。

## 対象 (published batch-23 正本から機械導出・maker `make_inputs_bv.py` `a4031abe…`)

- **s001**: key (1152921505294712832, 32768)・s5 62435・legal 78・
  membership 4・published replica result 1・nodes 5,415,927。
- **s002**: key (3458764514374189056, 32768)・s5 192809・legal 88・
  membership 4・published replica result 1・nodes 9,329,444。

sources pin (commit-pinned raw fetch・sha256全照合): batch-keys-b23
`2776acaf…` (53キー)・status-b23.log `1e4ccea9…` (4行 = PASS 2 +
WIN-HALT 2)・README-b23 `f38922ca…`・row-audit-winhalt-b23 `14aa7f63…`
(probed 2・win_rows [s001, s002]・fragment_keys {}・unprobed 51)・raw
s001 p1/p2 `84463069…`/`cd7633fb…`・raw s002 p1/p2 `39664259…`/
`8ce83037…`・published input CSV `422161a1…`/`32257e8e…`・BF
anchor/negative CSV (provenance chain AR→BF→BK→BM→BS→BV)。

## 事前ゲート (宣言前・本host)

- maker全gate PASS (BV-SCAFFOLD)・4回実行byte一致・input/rows.json
  (`61703c08…`・schema `n11-centralreply-closure-b23win-thirdimpl-input-v1`)
  再生成byte一致・tamper battery **6/6検出** (T1 raw pin 1bit・T2
  row-audit pin 1bit・T3 README pin 1bit・T4 row-audit内容改変・T5 raw
  内容改変 (nodes 5415927→5415928)・T6 published-input pin 1bit・T4/T5は
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
3. **本host pinned-replica再現 4/4 完全一致**: s001 p1/p2 =
   result 1・nodes **5,415,927** (two-pass node-exact・wall 26/25s)・
   s002 p1/p2 = result 1・nodes **9,329,444** (two-pass node-exact・
   wall 46/48s)。published batch-23 raw fields (result 1・nodes両値)
   との一致をaudit G2bで機械検査 (EXHAUSTED 0・mismatch 0・truncation 0)。
4. **negatives 2/2 GATE_FAIL設計どおり** (ng1: legal count mismatch
   derived=87 declared=88・ng2: stone count mismatch bits=5 declared=6)。
5. **anchors 2/2 本host node-exact** (a/b determinism PASS): k02a
   clean WIN result 1・expansions 9,106,337・ttHits 4,991,527 (Part
   G/K/O/P/T/W/AA/AD/AG/AL/AR/AX/AZ/BF/BK/BM/BS と同一のpublished第三実装値)
   (wall 25.83/26.16s)・l1a clean LOSS result 2・7,660,602/3,951,175
   (wall 22.69/22.33s)。
6. **targets 2/2 clean WIN一致 (verdict agreement 2/2)**: **s001
   clean WIN (result 1)** expansions 6,227,131・ttHits 3,553,011
   (a/b determinism PASS・wall 18.11/18.47s)・**s002 clean WIN
   (result 1)** expansions 11,072,137・ttHits 6,076,075 (a/b
   determinism PASS・wall 32.06/32.49s)。cap 300,000,000・wallcap
   240s・memo-power=22・WALL-INCONCLUSIVE 0・DIVERGENCE 0。
   pass-one third-impl拡張数合計 17,299,268 (replica 2行合計との
   比率は 1.150 / 1.187)。

## 監査 (`audit.py` `08bdebce…`・schema `n11-centralreply-closure-b23win-thirdimpl-audit-v1`)

**ALL 67 GATES PASS**・3回実行byte一致 (audit-run1/2/3.txt 同一sha)・
audit-summary.json 決定的 (タイムスタンプ不読)・verdict_agreements
2/2 (s001/s002 とも third=1 replica=1 agree=true)・wall_inconclusive 0。
audit tamper battery **3/3検出** (T1 maker pin反転→G1 pin gate fail・
T2 target det-pair改ざん (s001.a.out expansion+1)→target-s001-det-pair
gate fail・T3 G0 input改ざん (s001 legal 78→79)→G0 gate fail・scratch
上で実施し実験files無改変byte検証)・clean control PASS。

## 意味 (route statementのみ)

s001/s002 (22番目・23番目の unconsumed closure WIN 候補) は (a) Part BN
drive-1 published replica (b) 本host pinned-replica 2-pass node-exact再現
(独立host・初めて) (c) 独立第三実装 clean WIN の**3系統裏付け**となった
(同一クラス内2WINペアの第三実装交叉検証は Part BF (batch-19 w001/w002)
以来2例目)。ただし **verdictは一切消費していない**・採用判断は scrutiny
owner C++第二実装 gate pin `9193f5b6…` 待ちで本レーンは代行しない。
canonical cache (Part BU採用後 6,287行 `e32a2e44…`) は read-only・不変。

## 不接触

batch-21/22残留キー・batch-23残留51キー (s003..s053)・batch-27 (Part BR)
の54キー/scaffold/drive/outputs (並走所有・outputsは本実行時点でmainに
存在せず)・batch-24/25 (y001/y006・i001/i002 WIN行は本Part候補外)・
fast lane (y18..y22族)・finite-field lane・inversive-arc lane非接触。

## 検証規律

nodes数・expansions数・ttHits数を勝敗として読まない。WIN/LOSS採用は別宣言の
adoption Part (pinned fail-closed merger `90711961` 経由) のみ。**標準
11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2 {59,60}・
class 1/2/4・class 31600 (53キーすべて・s001/s002を含む) はどの時点でも
UNKNOWNのまま。**

## 再現

1. `python3 scripts/make_inputs_bv.py` (published pinsをsha検査し
   input/rows.json + 6 CSVを再導出・全gate PASSで終了)。
2. `node scripts/verify_tbl.js` (rules gate)。
3. `node scripts/jsreplay.js --exact-replay=val-gate/<...>.input.csv
   --exact-replay-budget=2000000|15000000` (val-gate 4件)。
4. `node scripts/jsreplay.js --exact-replay=input/s00X.input.csv
   --exact-replay-budget=15000000` ×2/キー (本host pinned-replica)。
5. `bash scripts/run_thirdimpl.sh <key> <tag> <kind>` (negatives・
   anchors・targets・1行=1solver=1プロセス・a/b 2回)。
6. `python3 scripts/audit.py` (67 gate・3回実行byte一致)。

## 出版コミット

- 宣言: note amendment `d58afadd` (fetch-back byte照合・note 489,824B)。
- A `db195667` scaffold 35ファイル (scripts 6 + input 7 + sources 14 +
  val-gate input/published-baseline 8)・fetch-back 35/35 byte一致。
- B `8b6a1048` outputs 24ファイル (output 20 + val-gate this-host 4)・
  fetch-back 24/24 byte一致。
- C (本commit) README + MANIFEST-sha256 (59行・対象dir内の published
  59ファイル)。
