# batch-27 WIN row (o002) third-implementation cross-verification (Part BY, 2026-11-23)

Part BY (宣言: note amendment commit `7a3a3f27`・実行前に出版・単一オーナー)。
batch-27 (Part BR・takeover実行・class 13342) で出版されたWIN行 **o002**
に対するpinned第三実装 (non-df-pn AND/OR minimax `third_impl.js`
`08ea958f…`) によるverdict-level交叉検証 + 本host pinned-replica再現。
**verdict不消費**。閉鎖・被覆・secured・root勝敗の主張はしない。

誠実な開示: batch-27 drive-1 は Part BR takeover実行hostの単一host出版
であり第二host同時再現は出版されていなかった。本Partの本host
pinned-replica (fresh-cold 2-pass) は o002 にとって**最初の独立host
再現**である。batch-27残留キー (o004/o006/o008/o010..o054 fileless
UNPROBED)・fragment o009 (p1完全単一パスはbookkeepingのみで証拠では
ない) には一切触れていない。同batchの o001/o003/o005/o007 の4 LOSS行
(adoption candidatesのみ) も本Part対象外・出版正本は読み取りのみ。
本host val-gate 4件は宣言前のhost健全性確認として1度取得済みで、
protocol step 2で上書き再取得したものを出版した (両回ともnode-exact
4/4・wall_s比較外)。

実行事故の記録 (honest): l1a anchor a-pass 実行中に実行環境の同期
エラーが発生し、空の `l1a.a.out` とstatus.logのRUN行欠落という不整合
状態が生じた。当該部分成果物は破棄し、l1a a/b をクリーンに再実行して
status.log整合を回復した (published出版bytesはすべて再実行後のもの)。

## 対象 (published batch-27 正本から機械導出・maker `make_inputs_by.py` `359abebc…`)

- **o002**: key (3494793310856282144, 0)・s5 209134・legal 79・
  membership 4・published replica result 1・nodes 4,589,084
  (**29番目の unconsumed closure WIN 候補**・honest label)。

sources pin (commit-pinned raw fetch・sha256全照合): batch-keys-b27
`67814ed6…` (54キー・class 13342・published MANIFEST-sha256 92行
(`a55813ee` 時点) と全行一致)・status-b27.log `50a4f407…` (6行 =
LOSS PASS 4 (o001/o003/o005/o007・result 2) + WIN PASS 1 (o002・
result 1) + WIN-HALT 1・PASS key集合はrow-audit win_rows ∪ loss_rows
と機械交叉導出で一致・truncated-retry行ゼロ・fragment o009はstatus行
に非出現)・README-b27 `1ee2666e…`・row-audit-winhalt-b27 `530fe947…`
(probed 5・win_rows [o002]・loss_rows [o001,o003,o005,o007]・
pass_rows 4・fragment_keys {o009: p1完全単一パス true / p2完全単一
パス false / evidence false / probed false}・unprobed_count 49)・raw
o002 p1/p2 `56fdf7a4…`/`cf1ce8ff…`・published input CSV
`d083f5c3…`・BF anchor/negative CSV (provenance chain AR→BF→BK→BM→
BS→BV→BW→BX→BY)。

## 事前ゲート (宣言前・本host)

- maker全gate PASS (BY-SCAFFOLD)・4回実行byte一致・input/rows.json
  (`cfd8bd06…`・schema `n11-centralreply-closure-b27win-thirdimpl-input-v1`)
  再生成byte一致・loss-row gate復元 (各status PASS行はtarget WIN行
  またはpublished LOSS行のいずれかでなければABORT)・fragment gate新設
  (o009はstatus行非出現かつrow-audit fragment_keys厳密照合)・tamper
  battery **7/7検出** (T1 raw o002.p1 nodes内容改変 4589084→4589085・
  T2 row-audit内容改変 probed 5→6・T3 README文言改変 o002 WIN→LOSS・
  T4 status.log o001 LOSS行 verdict反転 2→1・T5 published-input o002
  legal 79→78・T6 BF anchor CSV k02a lo +1・T7 batch-keys s5_index
  209134→209135・**全tamperに適用実効性assert** (改変前後sha照合)・
  scratch (/tmp) 上で実施し実験sources無改変byte検証)・clean control
  PASS。

## 実行結果 (宣言protocol順・逐次実行)

1. **rules gate PASS**: pinned `verify_tbl.js` `c8c52528…`・replica
   quads 95,670 == third-impl quads 95,670・triples checked 195,044・
   mismatches 0 (禁止四角 95,670)。
2. **val-gate this-host 4/4 node-exact** (pinned `jsreplay.js`
   `84585617…`・published baselineとの一致・wall_s比較外): at2m 2キー
   budget 2,000,000 exhaustion (result 0, nodes 2,000,000) ×2・15m基準キー
   budget 15M (2, 3,651,923) と (2, 5,040,200)。本host .out 4件は
   val-gate/に出版。
3. **本host pinned-replica再現 2/2 node-exact**: o002 p1/p2 =
   result 1・nodes **4,589,084** (two-pass node-exact・wall 22/22s・
   published 45/47s)。published batch-27 raw fields (result 1・nodes)
   との一致をaudit G2bで機械検査 (EXHAUSTED 0・mismatch 0・truncation
   0)。**o002の最初の独立host再現**。
4. **negatives 2/2 GATE_FAIL設計どおり** (ng1: legal count mismatch
   derived=87 declared=88・ng2: stone count mismatch bits=5 declared=6)。
5. **anchors 2/2 本host node-exact** (a/b determinism PASS): k02a
   clean WIN result 1・expansions 9,106,337・ttHits 4,991,527 (Part
   G/K/O/P/T/W/AA/AD/AG/AL/AR/AX/AZ/BF/BK/BM/BS/BV/BW/BX と同一の
   published第三実装値) (wall 26.39/26.22s)・l1a clean LOSS result 2・
   7,660,602 / 3,951,175 (wall 22.14/21.75s)。
6. **target 1/1 clean WIN一致 (verdict agreement 1/1)**: **o002
   clean WIN (result 1)** expansions 5,303,699・ttHits 2,988,749
   (a/b determinism PASS・wall 15.13/15.15s)。cap 300,000,000・
   wallcap 240s・memo-power=22・WALL-INCONCLUSIVE 0・DIVERGENCE 0。
   pass-one third-impl拡張数 5,303,699 (replica 4,589,084 との比率
   1.156)。

## 監査 (`audit.py` `7f7fa3d1…`・schema `n11-centralreply-closure-b27win-thirdimpl-audit-v1`)

**ALL 50 GATES PASS**・3回実行byte一致 (audit-run1/2/3.txt 同一sha)・
audit-summary.json 決定的 (タイムスタンプ不読)・verdict_agreements
1/1 (o002 third=1 replica=1 agree=true)・wall_inconclusive 0。audit
tamper battery **3/3検出** (T1 maker pin反転→ABORT (rc=1)・T2 audit
target det-pair改ざん (o002.b expansions +1)→target-o002-det-pair
gate fail (rc=1)・T3 G0 input改ざん (o002 CSV legal 79→80)→
input-o002-matches-rows gate fail (rc=1)・scratch (/tmp) 上で実施・
実験files無改変byte検証)・clean control PASS。

## 出版コミット (全てcommit-pinned raw fetch-backでbyte照合)

- 宣言 (note amendment): `7a3a3f27` (note blob `106a8abe…`・
  fetch-back byte一致)。
- A scaffold: `5ed729d1` (31 files・31/31 byte一致: scripts 6 +
  input 6 + sources 11 + val-gate 8)。
- B outputs: `821b8a9e` (23 files・23/23 byte一致: rules-gate +
  val-gate this-host 4 + replica p1/p2 + negatives 2 + anchors a/b 4 +
  target a/b 2 + audit 3回分 7 + status.log)。
- C README + MANIFEST-sha256: 本コミット (55行 = scaffold 31 +
  outputs 23 + README・マニフェスト対象は本dirの全published files)。

## 意味と消費規則 (route statementのみ)

- 第三実装 (非df-pn AND/OR minimax) のclean verdictがpublished
  replica verdict (result 1 = WIN row) と1/1で一致した。これは
  **verdict-level文献** (three-implementation corroboration) であり、
  採用 (adoption) ではない。o002 (29番目の unconsumed closure WIN候補)
  の採用判断は引き続き scrutiny owner C++ 第二実装 gate pin
  `9193f5b6…` 待ち (本レーンは代行しない)。canonical cache (Part BU
  採用後 6,287行 `e32a2e44…`) read-only不変。採用された場合のroute
  statement: 単独WIN子 o002 により class 13342 の全LOSS閉包ルートは
  反駁証拠を持つ (batch-27 READMEと同一の文言・閉鎖/被覆/secured/
  root勝敗の主張はしない)。
- 不接触: batch-23/24/25/27残留キー・fragment o009・batch-24
  y002/y004・batch-27 o001/o003/o005/o007 LOSS行 (adoption
  candidates)・batch-26/27 (Part BQ/BT/BR) scaffold・drive・outputs・
  fast lane・finite-field lane・inversive-arc lane。
- **標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・
  S2 {59,60}・class 1/2/4・class 10968・class 23964・class 16957・
  class 1849・class 30565・class 13342 (54キーすべて・o002を含む) は
  どの時点でもUNKNOWNのまま。** nodes数・expansions数・ttHits数を
  勝敗として読まない。WIN/LOSS採用は別宣言の adoption Part (pinned
  fail-closed merger `90711961` 経由) のみ。
