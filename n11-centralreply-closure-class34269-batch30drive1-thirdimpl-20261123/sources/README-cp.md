# batch-30: closure class 34269 exact-S5 probe (Part CP, 2026-11-23)

Part CP (宣言: research/log/2026-11-23-part-cp-batch30-class34269-drive1-declaration.md・commit
`189a2e8e`・publish-then-execute・単一オーナー n11中央応答長期レーン)。Part CO正本
merged canonical cache **6,301行 (sha256
`854800f38349277924bc77c50d92a6d5252f11bdb2b2cdb54a14ca2b4f6b087d`・batch-28
7-LOSS行採用込み・WIN 158 / LOSS 6,143)** + published update8 receipts
(`b658290a…`) 上のclosure候補表 **rank 36 class 34269** (mask
[1152921504624672768, 68719476736]・cost 54子すべてunknown) を対象とする
exact-S5 probe batch。**verdict不消費**。閉鎖・被覆・secured・root勝敗の
主張はしない。batch-28 completion後最初の新規closure class batch
(新BASE初適用)。

## 選定 (published baseから再導出・prose不使用・fail-closed maker 全gate PASS)

- **rank 36 class 34269** は re-derived ranked closure table (graph
  `54f9c364…` + CO base 6,301行 + update8 receipts による808行) が
  published Part CO reaudit closure-classes.csv (`9d3965d9…`・808行) と
  **全808行 (rank→class, unknown) 完全一致**した中の first-clean行。
- **ranks 1..35 + 37 はtriple pin (win intersection / known-WIN receipt
  children / packet collision) で全行機械反駁**。代表例: rank 4 class 5343
  (unknown 46・win35/pkt46), rank 21 class 12643 win{115192} (batch-21 a003
  自身の未消費WIN候補による反駁。Part COレジュームの「次点 class 12643」は
  機械判定により選定不可と確定), rank 35 class 2251 (batch-29 published
  packet全54キーとのpkt完全衝突・Part CI takeover進行中で二重probe禁止),
  rank 37 class 34948 pkt{415128} (batch-29 maker bookkeeping pinの継承)。
- **unconsumed WIN候補64キー (WIN64)**: published batch-29 maker WIN33 pin辞書
  (`44575cb2…`・33キー) ∪ published batch-28 row-audit.json (`00c32383`系)
  WIN 35行 (4重複) = 64 unique s5、すべてCO baseで未消費 (検証64/64)。
  class 34269の54子とのintersection 0・known WIN receipt cost child 0。
- 30 published packets (batches 1..28 + batch-14 residual + batch-29・
  計 **1,514 rows / 1,500 distinct positions**・sha pin 30/30・batch-29 packet
  `330c0b9f…`) とのposition衝突 0・quarantine 0/54・canonical-safe 54/54。
- runner-up: rank 38 class 5804 (unknown 55・groups 4)。published-table
  orderにより rank 36 class 34269 (groups [(12, 108)]) を優先。
- verdictは宣言で非予告 (事前登録はUNKNOWN担保のみ)。
- adoption ties machine-pinned: batch-20 x53 LOSS / class 12457 unknown 0 /
  BZ 6 LOSS / class 16957 51・class 13342 50 / CH aa003 LOSS / CO 7 LOSS
  (aa015/aa017/aa018/aa023/aa024/aa029/aa036) / class 5343 46。

## 54キー (maker出力・s5昇順)

**ac001..ac054** (2-letter prefix継続: 全30 published packet走査で「ac」
始まりのkey idは存在しないfail-closed gate)。s5 36668..958143・legal
76..97・membership {2: 9, 3: 8, 4: 37}・Board再計算54/54。
batch-keys.json sha256
`79fbd1664f4ad66ea62d9c8a8aa5aaff5d16bcdaa397895119ce4d8f47961232`
(budget 15,000,000・schema
`n11-centralreply-closure-class34269-batch30-input-v1`)。

## kit (published runnerのbyte-clone)

- jsreplay.js `84585617…` (byte-copy)・runbatch.sh `f591f8c2…`
  (byte-copy)。pre-registered stop rules: WIN rc=45 / MISMATCH rc=42・
  p1/p2 fail rc=43/44・budget 15M・2-pass fresh-cold・`# replay_done`の
  ないpassファイルはTRUNCATED-RETRY (evidenceでない)・EXHAUSTED (result 0)
  はhonest UNKNOWN (same-condition再probeなし)。
- maker make_batch30_keys.py (fail-closed・全pin機械埋込み・宣言前
  read-only実行でbyte-stable x2確認済み)。

## val-gate (宣言後に本host fresh実行)

- **b30-host 4ファイル fresh 4/4 node-exact (published baselinesと
  nodes完全一致・wall_s比較外)**: at2m 2キー result 0 / budget
  2,000,000 exhaustion (nodes 2,000,000 x2)・first-15m result 2 /
  nodes **3,651,923**・second-15m result 2 / nodes **5,040,200**・
  `# replay_done` x4 (truncationなし)。published-baseline 4組は
  batch-28/29 kitのbyte-copy (sha `6e902ab1`/`eeafe3ac`/`8035fe54`/
  `91dffdec`)。
- 実行順序の正直開示: 宣言 `189a2e8e` (2026-11-23T21:43Z) の後に
  val-gate fresh 4 (21:44-21:45Z)、続いてdrive-1 wave (21:46-21:50Z) を
  実行し、その後に本scaffoldを出版した (publish-then-execute規約は宣言が
  probeに先行することを要求しており、順守。scaffold出版順は規約対象外。

## drive-1 (WIN-HALT wave・完走)

- **probed 4 = WIN 2・LOSS 2・EXHAUSTED 0・fileless 50・MISMATCH 0**。
  すべて2-pass fresh-cold node-exact (PASS = p1/p2 replay行の
  budget/result/nodes完全一致)。
  - ac001 PASS result **2 (LOSS)** nodes 5,635,468 (adoption候補のみ・
    verdict不消費)
  - ac002 PASS result **1 (WIN)** nodes 10,752,246
  - ac003 PASS result **1 (WIN)** nodes 8,036,766
  - ac004 PASS result **2 (LOSS)** nodes 5,816,333 (adoption候補のみ・
    verdict不消費)
- 事前登録stop rule「WIN 2 distinctキー観測でwave halt」により
  ac002/ac003でwave終了。残50キー ac005..ac054 は fileless UNPROBED
  (drive-2以降は別の短い宣言で継続可)。
- **honest記録 (v1 session harnessバグ・開示)**: drive1_local_step.sh
  v1のdone判定正規表現が実status行形式 (`acNNN PASS`) と逆 (`PASS acNNN`)
  になっていたため、完了直後の2回目invocationが ac001/ac002 を再invoke
  した。**pinned runnerのreplay_doneガードが作動しsolver再実行は一切
  発生せず**、既存pass fileからの再読み出しでstatus.logに同一値の重複行
  (PASS/WIN-HALT各1行ずつ計3行) がappendされたのみ (append-only規約で
  出版・計算への影響ゼロ)。また同一キーのWIN-HALT重複行を「2 WIN」と
  誤読し一時誤haltした。v2はdistinct-key WIN集計に修正済み (本dirの
  drive1_local_step.shはv2)。batchキーのevidence (raw p1/p2) は全キー
  無傷・各キー実行は各1回のみ。

## 出力 (drive-1)

- output/status.log (9行・append-only・v1由来の重複行3行を含む)。
- output/raw/ac001..ac004 の p1/p2 各8ファイル (各 `# replay_done` 保持)。
  出力sha256 pinsは完了log (research/log/2026-11-23-part-cp-batch30-drive1.md)
  に記載。

## UNKNOWN担保

標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2
{59,60}・class 1/2/4・class 10968・class 23964・class 5343 (54キーすべて・
EXHAUSTED 11行含む)・class 2251 (batch-29全54キーを含む)・**class 34269
(54キーすべて・本batch-30の全キーを含む)** は本batchの実行・出版のどの
時点でもUNKNOWNのまま。nodes数・wall秒数を勝敗として読まない。WIN/LOSS
採用は scrutiny owner C++第二実装 gate `9193f5b6…` 通過後の別adoption
Part (pinned fail-closed merger `90711961…` 経由) のみ (本レーンは
代行しない)。

## 不接触

Part CI takeover (batch-29 drive-1進行中・`8b75b786`) のdir・outputs・進行、
Part CG (batch-28 drive2win thirdimpl・`d5e9acc2`) のdir・outputs・進行、
batch 1..29各published dir (不変)、BASE caches (`3124461b…`・
`854800f3…`) read-only不変、fast lane・finite-field・inversive・19root計画、
EXHAUSTED行の高budget再probe (別宣言条件)・scrutiny owner C++ gate専権事項。
