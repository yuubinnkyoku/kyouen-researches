# batch-25 WIN rows (i001/i002) third-implementation cross-verification (Part BX, 2026-11-23)

Part BX (宣言: note amendment commit `8b3aa95d`・実行前に出版・単一オーナー)。
batch-25 (Part BP・class 30565) で出版されたWIN行 **i001/i002** に対する
pinned第三実装 (non-df-pn AND/OR minimax `third_impl.js` `08ea958f…`) に
よるverdict-level交叉検証 + 本host pinned-replica再現。**verdict不消費**。
閉鎖・被覆・secured・root勝敗の主張はしない。

誠実な開示: batch-25 drive-1 は Part BP執行hostの単一host出版であり、
第二host同時再現は出版されていなかった。本Partの本host pinned-replica
(fresh-cold 2-pass) は i001/i002 にとって**最初の独立host再現**である。
batch-25残留51キー (i003..i053) fileless UNPROBEDには一切触れていない
(verdict不消費のまま)。batch-25にはLOSS行が存在しない (row-audit
loss_rows空・PASS 2行のみ) のでadoption候选行情報も本Part対象外。
本host val-gate 4件は宣言前のhost健全性確認として1度取得済みで、
protocol step 2で上書き再取得したものを出版した (両回ともnode-exact
4/4・wall_s比較外)。

## 対象 (published batch-25 正本から機械導出・maker `make_inputs_bx.py` `e1def905…`)

- **i001**: key (1152921505277935616, 1081344)・s5 68580・legal 88・
  membership 4・published replica result 1・nodes 13,251,132
  (**26番目の unconsumed closure WIN 候補**・honest label)。
- **i002**: key (3458764514357411840, 1081344)・s5 191299・legal 82・
  membership 4・published replica result 1・nodes 7,207,180
  (**27番目の unconsumed closure WIN 候補**・honest label)。

sources pin (commit-pinned raw fetch・sha256全照合): batch-keys-b25
`272c0c13…` (53キー・class 30565・schema
`n11-centralreply-closure-class30565-batch25-input-v1`)・status-b25.log
`0b12b101…` (4行 = PASS 2 + WIN-HALT 2・PASS key集合はrow-audit
win_rows (i001,i002) と機械交叉導出で一致・truncated-retry行ゼロ)・
README-b25 `67ec6ef9…`・row-audit-winhalt-b25 `cc84d1b3…` (probed 2・
win_rows [i001, i002]・loss_rows []・pass_rows 0・fragment_keys {}・
unprobed_count 51・derived_state true)・raw i001 p1/p2
`4e9e2de2…`/`bc6417d2…`・raw i002 p1/p2 `da09e97a…`/`2730ee6d…`・
published input CSV `cba4b6cb…`/`1af3487a…`・BF anchor/negative CSV
(provenance chain AR→BF→BK→BM→BS→BV→BW→BX)。

## 事前ゲート (宣言前・本host)

- maker全gate PASS (BX-SCAFFOLD)・4回実行byte一致・input/rows.json
  (`3cbbdabc…`・schema `n11-centralreply-closure-b25win-thirdimpl-input-v1`)
  再生成byte一致・tamper battery **7/7検出** (T1 raw i001.p1 nodes内容
  改変 13251132→13251133・T2 row-audit内容改変 probed 2→3・T3 README文言
  改変 i001 WIN→LOSS・T4 status.log i002 PASS verdict反転 1→2・T5
  published-input i001 legal 88→87・T6 BF anchor CSV k02a lo +1・T7
  batch-keys s5_index 191299→191300・**全tamperに適用実効性assert**
  (改変前後sha照合)・T1/T2/T3/T4/T7はsha-pin層・T5/T6はderived-vs-
  published byte等価層で検出・scratch (/tmp) 上で実施し実験sources
  無改変byte検証)・clean control PASS。
- batch-25固有の適合点: loss行ゼロのためBW版のloss-row gateは除去し
  「status.logの各PASS行はtarget WIN行 (result 1・published nodes) で
  なければABORT」gateへ置換 (row-audit loss_rows空との交叉導出)。

## 実行結果 (宣言protocol順・逐次実行)

1. **rules gate PASS**: pinned `verify_tbl.js` `c8c52528…`・replica
   quads 95,670 == third-impl quads 95,670・triples checked 195,044・
   mismatches 0 (禁止四角 95,670)。
2. **val-gate this-host 4/4 node-exact** (pinned `jsreplay.js`
   `84585617…`・published baselineとの一致・wall_s比較外): at2m 2キー
   budget 2,000,000 exhaustion (result 0, nodes 2,000,000) ×2・15m基準キー
   budget 15M (2, 3,651,923) と (2, 5,040,200)。本host .out 4件は
   val-gate/に出版。
3. **本host pinned-replica再現 4/4 node-exact**: i001 p1/p2 =
   result 1・nodes **13,251,132** (two-pass node-exact・wall 65/69s・
   published 150/68s)・i002 p1/p2 = result 1・nodes **7,207,180**
   (two-pass node-exact・wall 36/36s・published 77/75s)。published
   batch-25 raw fields (result 1・nodes両値) との一致をaudit G2bで
   機械検査 (EXHAUSTED 0・mismatch 0・truncation 0)。**i001/i002の
   最初の独立host再現**。
4. **negatives 2/2 GATE_FAIL設計どおり** (ng1: legal count mismatch
   derived=87 declared=88・ng2: stone count mismatch bits=5 declared=6)。
5. **anchors 2/2 本host node-exact** (a/b determinism PASS): k02a
   clean WIN result 1・expansions 9,106,337・ttHits 4,991,527 (Part
   G/K/O/P/T/W/AA/AD/AG/AL/AR/AX/AZ/BF/BK/BM/BS/BV/BW と同一の
   published第三実装値) (wall 26.20/25.93s)・l1a clean LOSS result 2・
   7,660,602 / 3,951,175 (wall 22.01/21.91s)。
6. **targets 2/2 clean WIN一致 (verdict agreement 2/2)**: **i001
   clean WIN (result 1)** expansions 15,723,649・ttHits 8,504,237
   (a/b determinism PASS・wall 44.56/44.18s)・**i002 clean WIN
   (result 1)** expansions 8,292,120・ttHits 4,721,313 (a/b
   determinism PASS・wall 23.96/24.25s)。cap 300,000,000・wallcap
   240s・memo-power=22・WALL-INCONCLUSIVE 0・DIVERGENCE 0。
   pass-one third-impl拡張数合計 24,015,769 (replica 2行合計
   20,458,312 との比率は 1.187 / 1.151)。

## 監査 (`audit.py` `19351ab5…`・schema `n11-centralreply-closure-b25win-thirdimpl-audit-v1`)

**ALL 67 GATES PASS**・3回実行byte一致 (audit-run1/2/3.txt 同一sha)・
audit-summary.json 決定的 (タイムスタンプ不読)・verdict_agreements
2/2 (i001/i002 とも third=1 replica=1 agree=true)・wall_inconclusive 0。
audit tamper battery **3/3検出** (T1 maker pin反転→ABORT (rc=1)・T2
audit target det-pair改ざん (i001.b expansions +1)→target-i001-det-pair
gate fail (rc=1)・T3 G0 input改ざん (i001 CSV legal 88→89)→
input-i001-matches-rows gate fail (rc=1)・scratch (/tmp) 上で実施・
実験files無改変byte検証)・clean control PASS。

## 出版コミット (全てcommit-pinned raw fetch-backでbyte照合)

- 宣言 (note amendment): `8b3aa95d` (note blob `35c37e46…`・
  fetch-back byte一致)。
- A scaffold: `f1adc061` (35 files・35/35 byte一致: scripts 6 +
  input 7 + sources 14 + val-gate 8)。
- B outputs: `3e078e2a` (27 files・27/27 byte一致: rules-gate +
  val-gate this-host 4 + replica p1/p2 + negatives 2 + anchors a/b 4 +
  targets a/b 4 + audit 3回分 7 + status.log)。
- C README + MANIFEST-sha256: 本コミット (63行 = scaffold 35 +
  outputs 27 + README・マニフェスト対象は本dirの全.published files)。

## 意味と消費規則 (route statementのみ)

- 第三実装 (非df-pn AND/OR minimax) のclean verdictがpublished
  replica verdict (result 1 = WIN row) と2/2で一致した。これは
  **verdict-level文献** (three-implementation corroboration) であり、
  採用 (adoption) ではない。i001/i002 の採用判断は引き続き scrutiny
  owner C++ 第二実装 gate pin `9193f5b6…` 待ち (本レーンは代行しない)。
  canonical cache (Part BU採用後 6,287行 `e32a2e44…`) read-only不変。
  採用された場合のroute statement: i001/i002 の2独立WIN子により
  class 30565 の全LOSS閉包ルートは反駁証拠を持つ (batch-25 READMEと
  同一の文言・閉鎖/被覆/secured/root勝敗の主張はしない)。
- 不接触: batch-23/24/25残留キー (s003..s053・y003/y005/y007..y053・
  i003..i053 fileless UNPROBED)・batch-24 y002/y004・batch-27
  o001/o003/o005/o007 LOSS行 (adoption candidates)・batch-26/27
  (Part BQ/BT/BR) scaffold・drive・outputs・fast lane・finite-field
  lane・inversive-arc lane。
- **標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・
  S2 {59,60}・class 1/2/4・class 10968・class 23964・class 16957・
  class 1849・class 13342・class 30565 (53キーすべて・i001/i002を含む)
  はどの時点でもUNKNOWNのまま。** nodes数・expansions数・ttHits数を
  勝敗として読まない。WIN/LOSS採用は別宣言の adoption Part (pinned
  fail-closed merger `90711961` 経由) のみ。
