# Part DQ 宣言 (2026-11-24): batch-33 (closure class 34908) 54-key probe — publish-then-execute

単一オーナー: n11中央応答レーン (長期レーン・本セッション本host)。
observed HEAD `fb88a6afee` (2026-11-24T16:51:03Z・s-parameter-kyouen lane)。
対抗宣言なし: 直近のcommit message機械走査 (2026-11-23以降・最大800件) で
使用済み Part 文字は DA..DP のみで `DQ` は存在せず、`batch-33` /
`class 34908` の probe を主張するcommit・logは存在しない (34908 の既存言及は
Part DN decomp churn (own 2) のみ・probe非主張)。part文字「DQ」は先着順採用
(DO/DP間は欠番のまま・本宣言はDQの最初の出版物)。

## 1. スコープ

closure campaign 継続として、closure class 34908 (rank 36・Part DP
b32loss54 adoption reaudit 後の現行 closure table 807行) の
**54 unknown cost children** を 2-pass fresh-cold probe する (batch-33)。
**verdict不消費** (probe結果の WIN/LOSS は honest labelのまま、canonical
adoption は別 adoption Part (pinned fail-closed merger `90711961…` 経由) のみ)。
閉鎖・被覆・secured・root勝敗の主張はしない。EXHAUSTED (budget 15M) は
honest UNKNOWN (same-condition 再probeなし)。

**BASE は Part DP 採用後の 6,502行正準cache** `1ded9a08…`
(merged-exact-s5-chain-plus-b28loss1-…-plus-b31loss51-plus-b30loss43-plus-b32loss54-20261124.cache:
Part DN 6,448行 base + batch-30 43-LOSS increment + batch-32 54-LOSS increment
を fail-closed union merger `90711961…` で併合) + published update8 receipts
(`b658290a…`)。

class 34908 の cost 56子のうち 2子 (s5 955954, 958114) は base 内 LOSS(2)
解決済みで、probe 対象は残り 54子すべて (unknown 54 == UNPROBED 54)。

## 2. 選定ゲート (本セッションで機械実施済み・正直開示)

publish-then-execute 規約に対する正直開示として、**選定ゲート検証
(read-only解析) と fail-closed maker の実行 (probe packet生成・solver不使用)
は本宣言の出版前に本hostで機械実施済み**である (maker 全 gate PASS・
package出力は§3のsha pinで固定)。solver実行 (val-gate fresh・probe) は
宣言後にのみ行う。cherry-pick不可能性は (a) 実験dir構成、(b) 入力sha pin群、
(c) stop rules、(d) 選定ゲート群 (すべて maker `make_batch33_keys.py` 内に
fail-closed pin) の事前登録により担保される。

機械確認済みゲート (すべて published 正本から再導出):

1. **closure table一致**: Part DP reaudit closure-classes.csv (`284bb069…`
   ・807行) をgraph `54f9c364…` + DP base 6,502行 + update8 receipts
   (`b658290a…`) から再導出したranked closure tableと**全807行
   (rank→class, unknown, groups) 完全一致・0不一致**。rank 36 = class 34908
   (unknown_now 54, groups_served_count 4, groups [(0,20),(0,100),(12,10),(12,110)]
   — roots first 0/12 の4 group)。
2. **graph一致**: dependency-graph.json.gz (`54f9c364…`) の
   s4_masks[34908] == [1152921504607895553, 68719476736] (closure tableの
   class_lo/class_hiと一致)、s4_status[34908] == 1 (unknown)、s4_cost[34908]
   == 56子 (うちbase解決済み s5 955954/958114 = LOSS(2)・残り54子すべてunknown)。
3. **base非解決**: DP base 6,502行に対し、class 34908 の 54 unknown子の
   ヒットは **0/54** (known children {955954: 2, 958114: 2} == pinned
   derived_known)。なお class 34908 は Part DN batch-30 採用で own-2 行が
   解決済みのクラス (その際に減った行は本probe対象に含まれない)。
4. **route-alive (WIN81)**: unconsumed closure WIN候補 **81 unique s5**
   (batch-32 published maker WIN81 list と同一集合・batch-32 (Part DM) は
   loss-only でWIN候補に増減なし) はすべて DP base で未消費 (検証81/81)。
   class 34908 の 54子との intersection **0**。known WIN receipt cost child
   も持たない (known-WIN receipt children gate: 空)。
5. **ranks 1..35機械pin + first-clean gate**: 各rankのclassification
   (unconsumed-WIN81 intersection / known-WIN receipt children / packet
   collision) をfail-closed pinとして全部機械再導出し、**rank 36 class
   34908 が first clean** (ranks 1..35はすべてblocker union非空) をgateで
   強制。追加 selection pin: ranks 1..35 + 37..51 のblocker行とrank 42
   packet衝突 (12857 / {440454}) を固定 (maker pin
   `selection_pins_ranks_1_35_37_51`・`rank42_pkt_pinned`)。
   **closure pocket (rank 1..4) は全WIN-blocked (Part DM訂正記録の維持)**:
   rank 1 class 23101 unknown 1 (s5 745184 = batch-14 q042 WIN)、rank 2
   class 1849 unknown 1 (s5 81011 = batch-26 l028 WIN)、rank 3 class 2251
   unknown 1 (s5 93815 = batch-29 ab028 WIN)、rank 4 class 5804 unknown 4
   (s5 198576/207094/212115/212536 = batch-31 WIN4行)。よって **pocket解消は
   WIN採用 (scrutiny owner C++第二実装 gate `9193f5b6…` 通過後・pinned
   merger `90711961…` 経由の別adoption Part) 待ち**であり、**Part DQは
   副作用verdictを一切支払わない**。ranks 21 (8811・WIN {198576}) /
   5 (34269・batch-30 WIN11行block) もWIN-blockedのまま。
6. **zero packet collision**: 33 published packets (batches 1..32・
   batch-32 packet `f46e663f…` 込み・計 **1,677 packet rows / 1,663 distinct
   positions**、sha pin 33/33検証) に対し、class 34908 の54キーは (lo,hi)
   positions両方で collision **0**。published key idに「af」始まりは存在
   しない (全33 packet走査済み・freshness gate)。
7. **quarantine 0 / canonical 54**: n11-s5-evidence-quarantine.json
   (`81d23160…`) との intersection **0/54**・canonical-safe形式 54/54・
   Board再計算 legal popcount 54/54 (範囲 84..101・LOCAL_RANGE pin・b32の
   88..105から再導出修正・派生物不使用)・membership histogram {2: 7, 3: 9,
   4: 38}・s5 1176..962471昇順・batch内重複なし。
8. **adoption ties (machine-pinned)**: Part DP: batch-32の54行がbase内
   LOSS(2)・batch-32はloss-only (未消費batch-32キーはゼロ)・class 8730
   unknown 0 — 継承ties (batch-20 x53 / Part BZ 6キー / Part CH aa003 /
   Part CO 7キー / Part CU batch-29 53 = CU16+DB37 / Part DL batch-31 51行+
   WIN4行 / class 16957 51行 / class 13342 50行 / class 5343 46行 / class
   2251 残1行 / class 5804 unknown 4) もすべて現行DP baseで機械検証
   (maker adoption_ties pin列 `dp_b32_54` 追加を含む)。
9. **runner-up**: rank 41 class 11490 (unknown 55・groups 4
   [(16,48),(16,50),(48,16),(48,56)]・base-resolved child s5 376421 =
   LOSS(2)・batch-31/batch-32両表のrunner-up) が同一ゲート群 CLEAN
   (target以外のclean行)。rank 36 class 34908 が published-table order
   (rank ascending) により選定。ranks 43 (14743) / 44 (15453) / 45 (16008)
   はcleanだがrank下位。
- honest開示: (a) b32 published maker からの fork の際、b32のOK-print文言
  `rank_38_39_only` (batch-31時代のrank表記がb32でも修正されず残っていた)
  が本forkにも残ったため `rank_36_41_only` に修正した (print-only・gate値
  非依存・修正後に全gateを再実行してPASS)。 (b) b32のLOCAL_RANGE pin
  (88..105) は本batch用にBoard再計算で 84..101 に差し替えた (verifier
  が型ごとに Budget再計算する設計はb32 Part DMでのpin修正lessonと同一)。

## 3. kit設計 (宣言後にscaffold)

- 実験dir: `research/experiments/n11-centralreply-closure-class34908-batch33-20261124/`
  (README・MANIFEST-sha256・scripts・input 54 CSV + batch-keys.json・output・val-gate)。
- runner: pinned byte-clone `runbatch.sh` (`f591f8c2…`・変更なし)。pre-registered
  stop rules: WIN rc=45 / MISMATCH rc=42・p1/p2 fail rc=43/44・budget 15M・
  2-pass fresh-cold・`# replay_done`のないpassファイルはTRUNCATED-RETRY
  (evidenceでない)・EXHAUSTED (result 0) はhonest UNKNOWNで継続。
- solver: jsreplay.js published byte-clone (`84585617…`)。
- maker: `make_batch33_keys.py` (sha256 `5d65addd…`・batch-32 published maker
  `2ddf4903…` からのfork・§2全gateをfail-closed pin内蔵・33 packet raw
  fetch 33/33 sha gate)。
- keys: batch-33 key ids **af001..af054** (s5昇順。freshness gate: published
  idに「af」始まりは存在しない)。batch-keys.json pin:
  `8a863381454fcfec3cb190db7130ce6801accf56170ee3a1b944402491fecbaa`
  (maker出力・宣言前ローカル実行で確定・scaffoldで出版、誰でもpublished
  bytesから再現可能)。
- session script: `drive1_local_step_b33.sh` (sha256 `ef44a49e…`・published
  batch-32 drive-1 `e43f5f83…` からの最小delta: key-id正規表現 ae→af の
  5箇所とヘッダ行のみ・機能bodyは機械diffで同等・v2 history commentは
  verbatim維持)。
- val-gate: batch-28..32方式継承 (sanctioned 4キー: at2m×2 budget 2M・
  first-15m・second-15m budget 15M・published baselines byte-copy
  `6e902ab1`/`eeafe3ac`/`8035fe54`/`91dffdec`・input CSV
  `ecc0299b`/`56aacb71`)。**本host fresh 4/4 node-exact** (sidecar suffix
  `.b33-host.out`・budget/result/nodes比較 (wall_s以外全field一致)) を宣言後
  に必須とする (不一致ならhard-stop)。
- drive-1: WIN-HALT設計 (WIN 2行distinct観測でwave halt・batch-28..32と
  同じ)。2 worker (1キー/worker) 並列上限・各workerは `timeout 260` でwrap
  (外側290s capに対しinner先発火)・空キーバグ防止ガード・status.log
  append-only・EXHAUSTEDは続行。drive進捗はincrement出版で環境reset耐性を
  持たせる (各wave後に成果分のみhonest出版・未probeキーはfileless UNPROBED
  のまま次wave/次回driveに委ねる・truncated passは再実行してから出版)。

## 4. 期待機械簿記 (事前登録)

probe結果によって class 34908 の unknown_now 54から減算される
(LOSS/EXHAUSTEDいずれも)。本宣言は結果非予告であり、いかなる勝敗も宣言
しない。WIN・EXHAUSTEDも出る可能性を事前登録する (WIN 2行distinctで
drive-1 wave halt・残キーはfileless UNPROBED維持)。closure table membership
変動 (flips/newly_free) はprobe完了後のreauditが機械導出する。nodes数は
bookkeepingであり勝敗ではない。

## 5. UNKNOWN担保

**標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2
{59,60}・class 1/2/4・class 8730 / 5804 / 34269 (出版済みの各batchキー
すべて)・class 34908 (本batch-33の54キーすべて・WIN/LOSS/EXHAUSTED行を
含む) は本Partの実行・出版のどの時点でもUNKNOWNのまま。** nodes数・wall秒数
を勝敗や距離として読まない。WIN採用は引き続き scrutiny owner C++第二実装
gate (`9193f5b6…`) 通過後の別adoption Part (pinned fail-closed merger
`90711961…` 経由) のみ (本レーンは代行しない)。

## 6. 不接触

- **Part DH** (b28 P4 9行 第三実装交叉検証・宣言 `f63c1654`) のdir・outputs・
  進行は非接触。
- K1286..K1299 fast lane (border-slices / multi-c web / pre-diag twins /
  K1298 s-parameter credit・完結済み)・projective-blockinge lane・
  s-parameter lane は非接触。
- Part DP canonical merged chain (6,502行 `1ded9a08…`) はread-only不変
  (本driveはcanonical cacheへ一切書き込まない)。
- batch 1..32 各published dir (不変)・BASE caches (`04b0a239…`・`60222707…`
  ・`7bdfa236…`・`1ded9a08…`) read-only不変。
- batch-28..31 WIN行scrutiny (C++ `9193f5b6…` 専権)・EXHAUSTED行の高budget
  再probe (別宣言条件)・19root計画・closure pocket (rank 1..4) のWIN採用
  (scrutiny owner後のadoption Part専権)。
