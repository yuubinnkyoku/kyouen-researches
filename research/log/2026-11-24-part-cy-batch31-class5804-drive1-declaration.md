# Part CY 宣言 (2026-11-24): batch-31 (closure class 5804) 55-key probe — publish-then-execute

単一オーナー: n11中央応答レーン (長期レーン・本セッション本host)。対抗宣言なし
(push直前の最新mainコミット列に batch-31 / class 5804 / Part CY の言及ゼロを機械確認
済み・observed HEAD `07bb3afba34feddb05f2d7627e422afa170e8721` (2026-11-24T01:30:27Z)。並走中レーン: Part CI takeover
(batch-29 class 2251 drive-2・宣言 `ec9c7191` 01:26:07Z) と Part CP takeover (batch-30
class 34269 drive-2・宣言 `87e19b5a` 01:28:22Z) はいずれも進行中・本宣言は非接触)。

## 1. スコープ

closure campaign継続として、closure class 5804 (rank 38・Part CU reaudit現行
closure table・Part CU採用後) の **55 unknown cost children** を2-pass fresh-cold
probeする (batch-31)。**verdict不消費** (probe結果の WIN/LOSS は honest labelのまま、
canonical adoptionは別adoption Part (pinned fail-closed merger `90711961…`) 経由のみ)。
閉鎖・被覆・secured・root勝敗の主張はしない。EXHAUSTED (budget 15M) は
honest UNKNOWN (same-condition再probeなし)。

**BASEはPart CU採用後の6,317行正準cache** `30ddad9d…` (Part CO 6,301行
`854800f3…` + batch-29 16-LOSS行採用) + published update8 receipts (`b658290a…`)
を最初のbatchとして使用する。batch-30 (Part CP進行中) の成果は未採用のため
本BASEには含まれない (ac002/ac003 WIN行も未消費honest labelとしてWIN77候補集合に入る)。

class 5804のcost 56子のうち1子 (s5 167863) はbase内LOSS(2)解決済みで、
probe対象は残り55子すべて (unknown 55 == UNPROBED 55)。

## 2. 選定ゲート (本セッションで機械実施済み・正直開示)

publish-then-execute規約に対する正直開示として、**選定ゲート検証 (read-only解析)
とfail-closed makerの実行 (probe packet生成・solver不使用) は本宣言の出版前に
本hostで機械実施済み**である (maker全gate PASS・package出力は§3のsha pinで固定)。
solver実行 (val-gate fresh・probe) は宣言後にのみ行う。cherry-pick不可能性は
(a) 実験dir構成、(b) 入力sha pin群、(c) stop rules、(d) 選定ゲート群 (全てmaker
`make_batch31_keys.py` 内にfail-closed pin) の事前登録により担保される。

機械確認済みゲート (すべて published 正本からの再導出):

1. **closure table一致**: Part CU reaudit closure-classes.csv
   (`3019d37f…`・808行) をgraph + CU base 6,317行 + update8 receipts
   (`b658290a…`) から再導出したranked closure tableと**全808行
   (rank→class, unknown) 完全一致・0不一致** (この検証自体も本hostで
   published bytesから再実施)。rank 38 = class 5804 (unknown_now 55,
   groups_served_count 4, groups [(38,59),(38,61),(49,58),(49,62)])。
2. **graph一致**: dependency-graph.json.gz (`54f9c364…`) の
   s4_masks[5804] == [6053400849139367936, 0] (closure tableのclass_lo/class_hi
   と一致)、s4_status[5804] == 1 (unknown)、s4_cost[5804] == 56子
   (うちbase解決済み1子 s5 167863 = LOSS(2)・残り55子すべてunknown)。
3. **base非解決**: CU base 6,317行に対しclass 5804の55 unknown子のヒットは
   **0/55** (known children {167863: 2} == pinned derived_known)。
4. **route-alive (WIN77)**: unconsumed closure WIN候補 **77 unique s5**
   (batch-29 maker WIN33 pin辞書の29 prior + published batch-28 WIN46全行
   〔row-audit WIN35 + re-probe解決11: aa004/aa005/aa021/aa028/aa030/aa031/
   aa032/aa035/aa047/aa050/aa053・35/46重複解消済み〕 + batch-30 drive-1
   WIN 2行 ac002 (s5 38891) / ac003 (s5 178184)) はすべてCU baseで未消費
   (検証77/77)。class 5804の55子とのintersection **0**。known WIN receipt
   cost childも持たない。
5. **ranks 1..37 + 40..42の機械triple pin + first-clean gate**: 各rankの
   classification (unconsumed-WIN77 intersection / known-WIN receipt children /
   packet collision) をfail-closed triple pinとして全部機械再導出・一致確認。
   さらに**first-clean gate**: ranks 1..37はすべてblocker union非空であることを
   gateで強制 (rank 38 class 5804がfirst clean)。代表例: rank 4 class 2251
   (unknown 38・batch-29 packet 38キー衝突・CU 16-LOSS採用済み), rank 18 class
   5830 known-WIN子5 (batch-29先行例の継続), rank 21 class 5687 / rank 28 class
   5690 knownwin {209644}, **rank 36 class 34269 二重block (WIN交積
   {38891, 178184} = batch-30自身の未消費WIN候補ac002/ac003 + batch-30 published
   packet全54キー衝突)**, rank 37 class 34948 pkt{415128} (batch-29/30 maker
   bookkeeping pinの継承), rank 40 class 12857 pkt1, ranks 41/42 (classes
   14743/15453) はcleanだがrank下位 (本target以前の候補ではない)。
6. **zero packet collision**: 31 published packets (batches 1..28 +
   batch-14 residual + batch-29 + **batch-30**、計 **1,568 packet rows /
   1,554 distinct positions**、sha pin 31/31検証・batch-30 packet
   `79fbd166…`) に対し、class 5804の55キーは (lo,hi) positions両方で
   collision **0**。published key idに「ad」始まりは存在しない (全31 packet
   走査済み・freshness gate)。
7. **quarantine 0 / canonical 55**: n11-s5-evidence-quarantine.json
   (`81d23160…`) とのintersection **0/55**・canonical-safe形式 55/55・
   mask_to_index == derived s5 index 55/55・Board再計算legal popcount 55/55
   (範囲 82..101)・membership histogram {2: 1, 3: 7, 4: 47} (graph cost関係から
   再導出)・s5 97381..212536昇順・batch内重複なし。
8. **adoption ties (machine-pinned)**: **Part CU: batch-29の16 LOSS行
   ab001..ab016 (s5 3964, 9935, 15659, 21341, 26610, 33712, 38148, 42711,
   51145, 53947, 56596, 60153, 63620, 67275, 73062, 76023) がすべてbase内
   LOSS(2)・class 2251 unknown 38・batch-29 packetの他54キーはいずれもbaseで
   未消費** — 継承ties (batch-20 x53キーすべてbase内LOSS(2)・class 12457
   unknown 0 / Part BZ 6キー LOSS・class 16957 unknown 51・class 13342 unknown
   50 / Part CH aa003 LOSS / Part CO 7キー (aa015/aa017/aa018/aa023/aa024/
   aa029/aa036) すべてbase内LOSS(2)・class 5343 unknown 46) も全て現行baseで
   機械検証。
9. **runner-up**: rank 39 class 11490 (unknown 55・groups 4
   [(16,48),(16,50),(48,16),(48,56)]・base-resolved child s5 376421 = LOSS(2))
   が同一ゲート群 CLEAN (target以外のclean行)。rank 38 class 5804が
   published-table order (rank ascending) により選定。

## 3. kit設計 (宣言後にscaffold)

- 実験dir: `research/experiments/n11-centralreply-closure-class5804-batch31-20261124/`
  (README・MANIFEST-sha256・scripts・input 55 CSV + batch-keys.json・output・val-gate)。
- runner: pinned byte-clone `runbatch.sh` (`f591f8c2…`・変更なし)。pre-registered
  stop rules: WIN rc=45 / MISMATCH rc=42・p1/p2 fail rc=43/44・budget 15M・
  2-pass fresh-cold・`# replay_done`のないpassファイルはTRUNCATED-RETRY
  (evidenceでない)・EXHAUSTED (result 0) はhonest UNKNOWNで継続。
- solver: jsreplay.js published byte-clone (`84585617…`)。
- maker: `make_batch31_keys.py` (sha256 `2681c841…`・batch-30 published maker
  からのfork・§2全gateをfail-closed pin内蔵・31 packet raw fetch 31/31 sha gate)。
- keys: batch-31 key ids **ad001..ad055** (s5昇順。freshness gate: published idに
  「ad」始まりは存在しない)。batch-keys.json pin:
  `d058fddc862c5f62b387eea7c7ac5b78f2c5063661371b388e5078772af4ff0e`
  (maker出力・宣言前ローカル実行で確定・再実行byte一致確認済み・scaffoldで出版、
  誰でもpublished bytesから再現可能)。
- session script: `drive1_local_step.sh` (sha256 `26347816…`・published batch-30
  v2 `e7b627a8…` からの最小delta: key-id正規表現 ac→ad の4箇所とヘッダ行のみ・
  機能bodyは機械diffで同等・v2 history commentはverbatim維持)。
- val-gate: batch-28/29/30方式継承 (sanctioned 4キー: at2m×2 budget 2M・
  first-15m・second-15m budget 15M・published baselines byte-copy
  6e902ab1/eeafe3ac/8035fe54/91dffdec)。**本host fresh 4/4 node-exact**
  (sidecar suffix `.b31-host.out`・budget/result/nodes比較) を宣言後に必須とする
  (不一致ならhard-stop)。
- drive-1: WIN-HALT設計 (WIN 2行distinct観測でwave halt・batch-28/29/30と同じ)。
  2 worker (1キー/worker) 並列上限・各workerは `timeout 260`でwrap (外側290s
  capに対しinner先発火)・空キーバグ防止 `if rem` ガード・status.log append-only・
  EXHAUSTEDは続行。誠実打ち切り時は成果分のみhonest出版・未probeキーはfileless
  UNPROBEDのまま次回driveに委ねる。

## 4. 期待機械簿記 (事前登録)

probe結果によって class 5804 の unknown_now 55から減算される (LOSS/EXHAUSTED
いずれも)。本宣言は結果非予告であり、いかなる勝敗も宣言しない。EXHAUSTEDも
出る可能性を事前登録する。closure table membership変動 (flips/newly_free) は
probe完了後のreauditが機械導出する。nodes数はbookkeepingであり勝敗ではない。

## 5. UNKNOWN担保

**標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2 {59,60}・
class 1/2/4・class 10968・class 23964・class 5343 (54キーすべて)・class 2251
(batch-29全キーを含む)・class 34269 (batch-30全キーを含む)・class 5804
(本batch-31の55キーすべて) は本Partの実行・出版のどの時点でもUNKNOWNのまま。**
nodes数・wall秒数を勝敗として読まない。WIN採用は引き続き scrutiny owner C++
第二実装 gate (`9193f5b6…`) 通過後の別adoption Part (pinned merger `90711961…`
経由) のみ (本レーンは代行しない)。

## 6. 不接触

- **Part CI takeover drive-2** (batch-29 class 2251 残38キー・宣言 `ec9c7191`
  01:26Z・並走所有) のdir・outputs・進行は非接触。
- **Part CP takeover drive-2** (batch-30 class 34269 残50キー・宣言 `87e19b5a`
  01:28Z・並走所有) のdir・outputs・進行は非接触 (batch-30 published packet・
  drive-1 outputs・WIN2行はread-only参照のみ)。
- **Part CX** (batch-28 CQ-WIN残5行第三実装・宣言 `1300c10d` 00:49Z・並走所有)
  非接触。
- K1276 fast lane (z=8スライス・宣言 `f4dcf92e`・A/B/C出版済み `685cce3a`/
  `c0ef88d5`/`4d70d1d1`・README bullet `07bb3afba`) 完結・非接触。
- Part CU canonical merged chain (6,317行 `30ddad9d…`) はread-only不変
  (本driveはcanonical cacheへ一切書き込まない)。
- batch 1..30各published dir (不変)・BASE caches (`3124461b…`・`854800f3…`・
  `30ddad9d…`) read-only不変。
- batch-28/29/30 WIN行scrutiny (C++ `9193f5b6…` 専権)・EXHAUSTED行の高budget
  再probe (別宣言条件)・19root計画・fast lane・finite-field lane・inversive lane。
