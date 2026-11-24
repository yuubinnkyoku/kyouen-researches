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

## drive-2 (Part CP takeover・2026-11-24): 25/50キーで誠実打ち切り — インフラ二重故障と事前登録stop rulesによるhard-stop

Part CP drive-2 (`7aaa0525` 21:56Z宣言) の宣言sessionが3.5h無音のため、
takeover宣言 `87e19b5a` (observed HEAD `4d70d1d1`・2026-11-24) により本hostが
引き継いだ (Part U/Z/CG/CI takeover基準・publish-then-execute)。実行:
val-gate fresh 4/4 node-exact (`.d2t-host.out`) → drive-2 waves
(session script `drive2_local_step.sh` `466f475f…`・runner pinned `f591f8c2…`
不変・WIN-CONTINUE)。**verdict不消費**。閉鎖・被覆・secured・root勝敗の主張はしない。

- **成果 (drive-2新規・ac005..ac029 25キー・うち23キーは単一writerの
  clean 2-pass fresh-cold node-exact)**: WIN 3 (ac020 9,765,071 /
  ac026 3,036,572 / ac027 2,593,751)・LOSS 18・EXHAUSTED 2 (ac006/ac013・
  nodes=15M both passes・honest UNKNOWN)・incident area 2 (ac028/ac029・
  下記)。batch-30全体では29/54キーprobed (WIN 5 = 新規3 + drive-1の
  ac002/ac003・LOSS 22・EXHAUSTED 2)。
- **ac028/ac029 (racing incident対象キー)**: 最終pass文件は両キーとも
  complete pair (p1/p2 node-exact・`# replay_done`付き: ac028 5,087,946 /
  ac029 9,204,933) だが、下記インフラ二重故障により二重実行環境下で書かれた
  (sidecar 2件も同一値のcomplete pass)。**本キー2つのrowはverdict不消費のまま
  「incident area」として次drive/監査に委ねる**。
- **残25キー ac030..ac054 はfileless UNPROBEDのまま** (drive-3は別宣言)。

### インシデント記録 (誠実開示・全文は完了log `research/log/2026-11-24-part-cp-takeover-batch30-drive2.md`)

1. **実行環境リセット1回** (wave 3-key loopが外側300s制限超過): ローカル作業dir全損。
   published宣言 (`87e19b5a`) からkit復元・sha再検証 (MANIFEST fail=0)・
   val-gate fresh 4再実施 (4/4 node-exact)・drive-2をac005からやり直し。
2. **Koyeb remote command失敗 → 孤児プロセス競合**: wave invocation中にインフラ
   応答失敗。remote側stepプロセスとworkerは存続し、retryInvocationと同一
   pass file (ac028/ac029) へ競合書込み。status.logに `MISMATCH p1=<値> p2=`
   (p2空) 2行・TRUNCATED-RETRY 2行・PASS 2行が時系列混在。機械判定:
   3独立書き込みすべて節点数完全一致 (real determinism divergenceは不在・
   p2空欄はmid-write読取)。
3. **事前登録stop rules (`MISMATCH rc=42 hard-stop`) の発火**: pinned
   orchestration (`drive2_local_step.sh`の `grep MISMATCH` pre-check) が
   状態として本driveを継続不能にした。「同時書き込みは無理に押し進げず
   記録して次回へ」規約により、本drive-2は25/50キーで誠実打ち切り。
   MISMATCH行2件の意味論付与とac028/ac029の扱いはdrive-3宣言が行う。

### kit・出版 (全fetch-back byte一致)

- A′ `1edab9ed`: `drive2_local_step.sh` (sha宣言済) + val-gate 4 sidecar。
- B checkpoint1 `dd660ce7`: ac005..ac021 34 pass + truncated sidecar 1 + status.log。
- B checkpoint2 (本commit群): ac022..ac029 16 pass + racing sidecar 2 + status.log (44行)。
- C (本commit): README追記 + MANIFEST-sha256拡張 (72→139行)。
- 完了log: research/log/2026-11-24-part-cp-takeover-batch30-drive2.md。

**UNKNOWN担保**: 標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・
S2 {59,60}・class 1/2/4・class 10968・class 23964・class 5343・class 2251・
**class 34269 (本batch-30の54キーすべて・EXHAUSTED行・incident対象キーを含む)**・
class 34948 は本driveの実行・出版のどの時点でもUNKNOWNのまま。nodes数・wall秒数を
勝敗として読まない。WIN採用は scrutiny owner C++第二実装 gate `9193f5b6…` 通過後の
別adoption Part (pinned merger `90711961…` 経由) のみ。row-auditは別セッション。
