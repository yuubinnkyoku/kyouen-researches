# Part DM 宣言 (2026-11-24): batch-32 (closure class 8730) 54-key probe — publish-then-execute

単一オーナー: n11中央応答レーン (長期レーン・本セッション本host)。対抗宣言なし
(push直前の最新mainコミット列 (直近20件) に batch-32 / class 8730 / Part DM の言及
ゼロ・`research/log/` に part-dm ファイル不存在を機械確認済み・observed HEAD
`88a810b0733e3e9d37b1abdaa0b576bcac95f3bc` (2026-11-24T10:40:49Z)。並走中レーン:
Part DH (b28 P4 9行 第三実装交叉検証・takeover宣言 `a4e00aa3` + interim note
`076e05c1`・実行中) はいずれも非接触。part文字「DM」は先着順採用
(DH/DK/DLは同日他レーン使用済み・log走査でpart-dm不存在を機械確認)。

## 1. スコープ

closure campaign継続として、closure class 8730 (rank 30・Part DL/b31loss51
adoption reaudit後の現行closure table) の **54 unknown cost children** を
2-pass fresh-cold probeする (batch-32)。**verdict不消費** (probe結果の WIN/LOSS は
honest labelのまま、canonical adoptionは別adoption Part (pinned fail-closed merger
`90711961…`) 経由のみ)。閉鎖・被覆・secured・root勝敗の主張はしない。
EXHAUSTED (budget 15M) は honest UNKNOWN (same-condition再probeなし)。

**BASEはPart DL採用後の6,405行正準cache** `60222707…`
(merged-exact-s5-chain-plus-b28loss1-…-plus-b31loss51-20261124.cache・BASE
`04b0a239…` (Part DB) + batch-29 16-LOSS `854800f3…` 系 (Part CU `30ddad9d…`) +
batch-31 51-LOSS increment `e750a0e6…` をfail-closed union merger
`90711961…` で併合) + published update8 receipts (`b658290a…`)。

class 8730のcost 58子のうち4子 (s5 144458, 212464, 310606, 311726) はbase内
LOSS(2)解決済みで、probe対象は残り54子すべて (unknown 54 == UNPROBED 54)。

## 2. 選定ゲート (本セッションで機械実施済み・正直開示)

publish-then-execute規約に対する正直開示として、**選定ゲート検証 (read-only解析)
とfail-closed makerの実行 (probe packet生成・solver不使用) は本宣言の出版前に
本hostで機械実施済み**である (maker全gate PASS・package出力は§3のsha pinで固定)。
solver実行 (val-gate fresh・probe) は宣言後にのみ行う。cherry-pick不可能性は
(a) 実験dir構成、(b) 入力sha pin群、(c) stop rules、(d) 選定ゲート群 (すべてmaker
`make_batch32_keys.py` 内にfail-closed pin) の事前登録により担保される。

機械確認済みゲート (すべて published 正本からの再導出):

1. **closure table一致**: Part DL/b31loss51 reaudit closure-classes.csv
   (`50841fa4…`・808行) をgraph `54f9c364…` + DL base 6,405行 + update8
   receipts (`b658290a…`) から再導出したranked closure tableと**全808行
   (rank→class, unknown) 完全一致・0不一致** (この検証自体も本hostで
   published bytesから再実施)。rank 30 = class 8730 (unknown_now 54,
   groups_served_count 4, groups [(5,58),(5,62),(38,55),(38,65)])。
   (honest開示: 旧deriveスクリプトのFIRST-CLEAN事実印刷にstale変数バグがあり、
   fail-closed makerのLOCAL_RANGE pinがこれを検出した。真のclass 8730 legal
   popcount範囲 88..105 (Board再計算) でpinを修正の上、全gateを再実行して
   PASSした。修正は本宣言の先行作業として完了・派生物は不使用。)
2. **graph一致**: dependency-graph.json.gz (`54f9c364…`) の
   s4_masks[8730] == [6052837899185946656, 0] (closure tableのclass_lo/class_hi
   と一致)、s4_status[8730] == 1 (unknown)、s4_cost[8730] == 58子
   (うちbase解決済み4子 s5 144458/212464/310606/311726 = LOSS(2)・残り54子
   すべてunknown)。
3. **base非解決**: DL base 6,405行に対し、class 8730の54 unknown子のヒットは
   **0/54** (known children {144458: 2, 212464: 2, 310606: 2, 311726: 2} ==
   pinned derived_known)。
4. **route-alive (WIN81)**: unconsumed closure WIN候補 **81 unique s5**
   (WIN77〔batch-31 Part CY §2 gate 4と同一集合〕 + batch-31 WIN 4行
   ad024 (s5 198576) / ad028 (s5 207094) / ad043 (s5 212115・15M EXHAUSTEDの
   Part DI 30M reprobe WIN supersede) / ad055 (s5 212536)) はすべてDL baseで
   未消費 (検証81/81)。class 8730の54子とのintersection **0**。known WIN
   receipt cost childも持たない。
5. **ranks 1..29機械pin + first-clean gate**: 各rankのclassification
   (unconsumed-WIN81 intersection / known-WIN receipt children / packet
   collision) をfail-closed pinとして全部機械再導出し、**rank 30 class 8730が
   first clean** (ranks 1..29はすべてblocker union非空) をgateで強制。追加
   selection pin: ranks 1..29 + 31 + 44のblocker行とrank 42 packet衝突を固定
   (maker pin `selection_pins_ranks_1_29_31_44`・`rank42_pkt_pinned`)。
   **closure pocket (rank 1..4) は全WIN-blocked**: rank 1 class 23101 unknown 1
   (s5 745184 = batch-14 q042 WIN・WIN81 block + prior packet衝突の二重block)、
   rank 2 class 1849 unknown 1 (s5 81011 = batch-26 l028 WIN)、rank 3 class 2251
   unknown 1 (s5 93815 = batch-29 ab028 WIN)、rank 4 class 5804 unknown 4
   (s5 198576/207094/212115/212536 = batch-31 WIN4行 ad024/ad028/ad043/ad055)。
   よって **pocket解消はWIN採用 (scrutiny owner C++第二実装 gate `9193f5b6…`
   通過後・pinned merger `90711961…` 経由の別adoption Part) 待ち**であり、
   **Part DMは副作用verdictを一切支払わない**。本宣言はこの「pocket (rank 1..4)
   = 全unknownキーが未消費WIN候補 (WIN-blocked)」という機械確定を訂正記録として
   正本に残す (以後のREADME/K表現はこの確定に合わせて維持される。pocketの
   解消経路をfresh LOSS probeのみに帰する表現は現行closure tableでは誤り)。
6. **zero packet collision**: 32 published packets (batches 1..31・batch-31
   packet `d058fddc…` 込み・計 **1,623 packet rows / 1,609 distinct
   positions**、sha pin 32/32検証) に対し、class 8730の54キーは (lo,hi)
   positions両方で collision **0**。published key idに「ae」始まりは存在しない
   (全32 packet走査済み・freshness gate)。
7. **quarantine 0 / canonical 54**: n11-s5-evidence-quarantine.json
   (`81d23160…`) とのintersection **0/54**・canonical-safe形式 54/54・
   Board再計算legal popcount 54/54 (範囲 88..105・LOCAL_RANGE pin修正後)・
   membership histogram {2: 1, 3: 4, 4: 49}・s5 30596..311727昇順・
   batch内重複なし。
8. **adoption ties (machine-pinned)**: Part DL: batch-31の51 LOSS行がbase内
   LOSS(2)・class 5804 unknown 4 (WIN4行とも未消費)・batch-31 packetの他54キー
   はいずれもbaseで未消費 — 継承ties (batch-20 x53 / Part BZ 6キー / Part CH
   aa003 / Part CO 7キー / Part CU batch-29 16-LOSS / class 16957 51行 /
   class 13342 50行 / class 5343 46行 / class 2251 残1行) もすべて現行baseで
   機械検証 (maker adoption_ties pin列)。
9. **runner-up**: rank 41 class 11490 (unknown 55・groups 4
   [(16,48),(16,50),(48,16),(48,56)]・base-resolved child s5 376421 = LOSS(2))
   が同一ゲート群 CLEAN (target以外のclean行)。rank 30 class 8730が
   published-table order (rank ascending) により選定。ranks 43 (class 14743) /
   44 (class 15453) はcleanだがrank下位。

## 3. kit設計 (宣言後にscaffold)

- 実験dir: `research/experiments/n11-centralreply-closure-class8730-batch32-20261124/`
  (README・MANIFEST-sha256・scripts・input 54 CSV + batch-keys.json・output・val-gate)。
- runner: pinned byte-clone `runbatch.sh` (`f591f8c2…`・変更なし)。pre-registered
  stop rules: WIN rc=45 / MISMATCH rc=42・p1/p2 fail rc=43/44・budget 15M・
  2-pass fresh-cold・`# replay_done`のないpassファイルはTRUNCATED-RETRY
  (evidenceでない)・EXHAUSTED (result 0) はhonest UNKNOWNで継続。
- solver: jsreplay.js published byte-clone (`84585617…`)。
- maker: `make_batch32_keys.py` (sha256 `2ddf4903…`・batch-31 published maker
  `2681c841…` からのfork・§2全gateをfail-closed pin内蔵・32 packet raw
  fetch 32/32 sha gate)。
- keys: batch-32 key ids **ae001..ae054** (s5昇順。freshness gate: published
  idに「ae」始まりは存在しない)。batch-keys.json pin:
  `f46e663f1676111ae67f5686f4a7807a8c1f7e4e1d9910ddb96ba61bcb5e705d`
  (maker出力・宣言前ローカル実行で確定・再実行byte一致確認済み・scaffoldで出版、
  誰でもpublished bytesから再現可能)。
- session script: `drive1_local_step_b32.sh` (sha256 `e43f5f83…`・published
  batch-31 drive-1 v2 `26347816…` からの最小delta: key-id正規表現 ad→ae の
  4箇所とヘッダ行のみ・機能bodyは機械diffで同等・v2 history commentはverbatim
  維持)。
- val-gate: batch-28..31方式継承 (sanctioned 4キー: at2m×2 budget 2M・
  first-15m・second-15m budget 15M・published baselines byte-copy
  6e902ab1/eeafe3ac/8035fe54/91dffdec・input CSV ecc0299b/56aacb71)。
  **本host fresh 4/4 node-exact** (sidecar suffix `.b32-host.out`・
  budget/result/nodes比較 (wall_s以外全field一致)) を宣言後に必須とする
  (不一致ならhard-stop)。
- drive-1: WIN-HALT設計 (WIN 2行distinct観測でwave halt・batch-28..31と同じ)。
  2 worker (1キー/worker) 並列上限・各workerは `timeout 260` でwrap (外側
  290s capに対しinner先発火)・空キーバグ防止ガード・status.log append-only・
  EXHAUSTEDは続行。誠実打ち切り時は成果分のみhonest出版・未probeキーは
  fileless UNPROBEDのまま次回driveに委ねる。

## 4. 期待機械簿記 (事前登録)

probe結果によって class 8730 の unknown_now 54から減算される (LOSS/EXHAUSTED
いずれも)。本宣言は結果非予告であり、いかなる勝敗も宣言しない。EXHAUSTEDも
出る可能性を事前登録する。closure table membership変動 (flips/newly_free) は
probe完了後のreauditが機械導出する。nodes数はbookkeepingであり勝敗ではない。

## 5. UNKNOWN担保

**標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2 {59,60}・
class 1/2/4・class 5804 (55キーすべて)・class 8730 (本batch-32の54キー
すべて・WIN/LOSS/EXHAUSTED行を含む) は本Partの実行・出版のどの時点でも
UNKNOWNのまま。** nodes数・wall秒数を勝敗や距離として読まない。WIN採用は
引き続き scrutiny owner C++第二実装 gate (`9193f5b6…`) 通過後の別adoption Part
(pinned merger `90711961…` 経由) のみ (本レーンは代行しない)。

## 6. 不接触

- **Part DH** (b28 P4 9行 第三実装交叉検証・takeover `a4e00aa3`・interim
  `076e05c1`・実行中) のdir・outputs・進行は非接触。
- K1286/K1287/K1288 fast lane (border-slices / multic-web F2 / pre-diag
  twins z1/z2・完結済み) は非接触。
- Part DL canonical merged chain (6,405行 `60222707…`) はread-only不変
  (本driveはcanonical cacheへ一切書き込まない)。
- batch 1..31 各published dir (不変)・BASE caches (`04b0a239…`・`30ddad9d…`・
  `60222707…`) read-only不変。
- batch-28..31 WIN行scrutiny (C++ `9193f5b6…` 専権)・EXHAUSTED行の高budget
  再probe (別宣言条件)・19root計画・fast lane・finite-field lane・inversive lane。
