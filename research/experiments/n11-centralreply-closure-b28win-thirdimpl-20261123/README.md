# batch-28 WIN rows (aa001/aa002) third-implementation cross-verification (Part CC, 2026-11-23)

Part CC (宣言: note amendment commit `0e2114913a593340c39a05a8fc4f4a6bbfe46937`・
publish-then-execute・単一オーナー)。batch-28 (Part CB・class 5343) で出版された
WIN行 **aa001** と **aa002** に対するpinned第三実装 (非df-pn AND/ORミニマックス
`third_impl.js` `08ea958f…`) によるverdict-level交叉検証 + 本host pinned-replica
(fresh-cold 2-pass) 再現。**verdict不消費**。閉鎖・被覆・secured・root勝敗の主張は
しない。

誠実な開示: batch-28 drive-1 は Part CB実行hostの単一環境出版物であり、aa001/aa002
の第二実行環境同時再現は出版されていなかった。本Partのthis-host pinned-replica
2-passはpublished source bytesのsha検証後に全工程を再実行したものであり、両行とも
node-exact一致を達成した (aa001 13,183,855・aa002 6,527,041)。aa001/aa002に対する
最初の「独立セッション再現」として記録する (実行hostの物理的相違までは主張しない)。
batch-28残り52キー (aa003..aa054 fileless UNPROBED) には一切触れていない。

## 対象 (published batch-28 正本から機械導出・maker `make_inputs_cc.py` `8255d0ad…`)

- **aa001**: key (1315631633331650560, 0)・s5 28037・legal 88・membership 4・
  published replica result 1・nodes 13,183,855 (**30番目の unconsumed closure
  WIN 候補**・honest label)。
- **aa002**: key (1171516445390012416, 0)・s5 87306・legal 86・membership 2・
  published replica result 1・nodes 6,527,041 (**31番目**)。

sources pin (commit-pinned raw fetch・sha256全照合・published MANIFEST 81行
(`4f9d2cef` 時点) と全行一致): batch-keys-b28 `af19208f…` (54キー・class 5343)・
status-b28.log `e98b5d23…` (4行 = WIN PASS 2 (aa001/aa002・result 1) + WIN-HALT 2・
retry/fragment/loss行ゼロ・PASS key集合はrow-audit win_rows [aa001, aa002] と機械
交叉導出で一致)・README-b28 `1b9f87b1…`・row-audit-winhalt-b28 `3f50b4f6…`
(probed 2・pass_rows 0・loss_rows []・win_rows [aa001, aa002]・fileless_unprobed
52・fragment_keys {})・raw 4ピン (aa001.p1 `b3f396bd…` / aa001.p2 `59a3e8a1…` /
aa002.p1 `07d9d643…` / aa002.p2 `7d2d26a8…`)・published input CSV 2ピン
(aa001 `8083b62e…` / aa002 `6310e641…`)・BF anchor/negative CSV 4ピン
(provenance chain AR→BF→BK→BM→BS→BV→BW→BX→BY→CC)。

## 事前ゲート (宣言前・本host)

- maker全gate PASS (CC-SCAFFOLD)・4回実行byte一致・input/rows.json
  (`b7222edf…`・schema `n11-centralreply-closure-b28win-thirdimpl-input-v1`)
  再生成byte一致。maker内gate: sources 4+raw 4+published input 2+BF 4ピン・
  status 4行構成 (WIN PASS 2 + WIN-HALT 2)・row-audit battery (probed/win_rows/
  loss_rows/fileless 52/fragment {})・README文言 (両WIN honest label・nodes 2件・
  30番目・31番目候補・fileless UNPROBED・scrutiny owner継続・class 5343/Part CB
  識別)。2文字prefix `aa###` gate (batch-26単文字前提事故 (Part CB事故記録1) の
  再発防止)。
- maker tamper battery **7/7検出** (T1 raw aa001.p1 nodes+1 / T2 row-audit
  probed 2→3 / T3 README aa001 WIN→LOSS / T4 status aa001 verdict反転 1→2 /
  T5 published-input aa002 legal 86→85 / T6 BF anchor k02a lo+1 / T7
  batch-keys s5_index 28037→28038・全tamperに適用実効性確認・scratch (/tmp) 上で
  実施し実験sources無改変byte検証)・clean control PASS。

## 実行結果 (宣言protocol順・逐次実行)

1. **rules gate PASS**: pinned `verify_tbl.js` `c8c52528…`・replica quads
   95,670 == third-impl quads 95,670・triples checked 195,044・mismatches 0
   (禁止四角 95,670)。
2. **val-gate this-host 4/4 node-exact** (pinned `jsreplay.js` `84585617…`・
   published baseline (batch-28 kitのbyte-copy) との一致・wall_s比較外): at2m
   2キー budget 2,000,000 exhaustion (result 0, nodes 2,000,000) ×2・15m基準キー
   budget 15M (2, 3,651,923) と (2, 5,040,200)。本host .out 4件はval-gate/に出版。
3. **本host pinned-replica再現 2/2 node-exact**: aa001 p1/p2 = result 1・nodes
   **13,183,855** (two-pass node-exact・wall 84/91s・published 147/75s)・aa002
   p1/p2 = result 1・nodes **6,527,041** (two-pass node-exact・wall 42/43s・
   published 72/73s)。published batch-28 raw fields (result 1・nodes) との一致を
   audit G2bで機械検査。EXHAUSTED 0・mismatch 0・truncation 0。
   **aa001/aa002の最初の独立セッション再現**。
4. **negatives 2/2 GATE_FAIL設計どおり** (ng1: legal count mismatch
   derived=87 declared=88・ng2: stone count mismatch bits=5 declared=6)。
5. **anchors 2/2 本host node-exact** (a/b determinism PASS): k02a clean WIN
   result 1・expansions 9,106,337・ttHits 4,991,527 (Part
   G/K/O/P/T/W/AA/AD/AG/AL/AR/AX/AZ/BF/BK/BM/BS/BV/BW/BX/BY と同一の published
   第三実装値) (wall 32.90/32.49s)・l1a clean LOSS result 2・7,660,602 /
   3,951,175 (wall 28.36/28.89s)。
6. **targets 2/2 clean WIN一致 (verdict agreement 2/2)**: **aa001 clean WIN
   (result 1)** expansions 15,677,345・ttHits 8,277,865 (a/b determinism
   PASS・wall 56.97/55.07s)・**aa002 clean WIN (result 1)** expansions
   7,624,309・ttHits 4,113,380 (a/b determinism PASS・wall 27.22/27.08s)。cap
   300,000,000・wallcap 240s・memo-power=22・WALL-INCONCLUSIVE 0・DIVERGENCE 0。
   pass-one third-impl拡張数合計 23,301,654 (replica nodes 13,183,855 /
   6,527,041 との比率 aa001 1.189・aa002 1.168)。

## 監査 (`audit.py` `b7cfb0ce…`・schema `n11-centralreply-closure-b28win-thirdimpl-audit-v1`)

**ALL 67 GATES PASS**・3回実行byte一致 (audit-run1/2/3.txt 同一sha
`df402055…`・audit-summary 4ファイル同一sha `9c22c1e7…`)・決定的 (タイム
スタンプ不読)・verdict_agreements 2/2 (aa001 third=1 replica=1 agree=true・
aa002 third=1 replica=1 agree=true)・wall_inconclusive 0。audit tamper battery
**3/3検出** (T1 script pin反転 (PIN_THIRD末尾1桁) → pin-third_impl.js gate
fail (rc=1)・T2 targets aa002.a expansions +1 → target-aa002-det-pair gate fail
(rc=1)・T3 G0 input改ざん (aa002 CSV legal 86→87) → input-aa002-matches-rows
gate fail (rc=1)・scratch (/tmp) 上で実施・実験files無改変byte検証)・clean
control PASS。

## 出版コミット (全てcommit-pinned raw fetch-backでbyte照合)

- 宣言 (note amendment): `0e211491` (note blob `9703ae8f…`・fetch-back byte
  一致・対抗宣言なし機械確認済み)。
- A scaffold: `1f38deb8` (35 files・scripts 6 + input 7 + sources 14 + val-gate
  8・35/35 byte一致)。
- B outputs: `31ddca98` (27 files・rules-gate + val-gate this-host 4 + replica
  4 + negatives 2 + anchors 4 + targets 4 + audit 3回分 7 + status.log・27/27
  byte一致)。
- C README + MANIFEST-sha256: 本コミット (63 files = scaffold 35 + outputs 27 +
  README・マニフェスト対象は本dirの全published files)。

## 意味と消費規則 (route statementのみ)

- 第三実装 (非df-pn AND/OR minimax) のclean verdictがpublished replica verdict
  (result 1 = WIN row) と2/2で一致した。これは**verdict-level文献**
  (three-implementation corroboration) であり、採用 (adoption) ではない。
  aa001 (30番目)・aa002 (31番目) の unconsumed closure WIN候補の採用判断は
  引き続き scrutiny owner C++ 第二実装 gate pin `9193f5b6…` 待ち (本レーンは
  代行しない)。canonical cache (Part BZ採用後 6,293行 `9115be9e…`)
  read-only不変。採用された場合のroute statement: 単WIN子 aa001/aa002のいずれか
  により class 5343 の全LOSS閉包ルートは反駁証拠を持つ (batch-28 READMEと同一
  文言・閉鎖/被覆/secured/root勝敗の主張はしない)。
- 不接触: batch-28 fileless 52キー (aa003..aa054)・Part CA (batch-27 residual)・
  batch 1..28 published dirs・fast lane・finite-field lane・inversive-arc lane・
  z19 lanes・28 unconsumed closure WIN候補の採用状態。
- **標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2
  {59,60}・class 1/2/4・class 10968・class 23964・class 5343 (54キーすべて・
  aa001/aa002を含む) はどの時点でもUNKNOWNのまま。** nodes数・expansions数・
  ttHits数・wall秒数を勝敗として読まない。WIN/LOSS採用は別宣言の adoption
  Part (pinned fail-closed merger `90711961…` 経由) のみ。
