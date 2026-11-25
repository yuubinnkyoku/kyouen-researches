# Part CI 宣言 (2026-11-23): batch-29 (closure class 2251) 54-key probe — publish-then-execute

単一オーナー: n11中央応答レーン (Part CH継続セッション・本host)。対抗宣言なし
(push直前の最新main直近40コミット中に class 2251 / batch-29 / batch-29 / class 34269
の言及ゼロをgrep確認済み)。

## 1. スコープ

Part CD系driveパターンの継続として、closure class 2251 (rank 35・Part CH reaudit
現行closure table) の54 cost childrenを2-pass fresh-cold probeする
(batch-29)。**verdict不消費** (probe結果の WIN/LOSS は honest labelのまま、canonical
adoptionは別adoption Part (pinned merger `90711961…`) 経由のみ)。閉鎖・被覆・
secured・root勝敗の主張はしない。EXHAUSTED (budget 15M) は honest UNKNOWN。

## 2. 選定ゲート (本セッションで機械実施済み・正直開示)

publish-then-execute規約に対する正直開示として、**選定ゲート検証 (read-only解析)
は本宣言の出版前に本hostで機械実施済み**である。これはスコープ固定前に published
データから選定可否を再導出しただけで、probe packet生成・probe実行は宣言後に行う。
cherry-pick不可能性は (a) 実験dir構成、(b) 入力sha pin群、(c) stop rules、
(d) 選定ゲート群 (下記) の事前登録により担保される。

機械確認済みゲート (すべて published 正本からの再導出):

1. **closure table一致**: Part CH reaudit closure-classes.csv
   (`baa2db13…`) で rank 35 = class 2251 (unknown_now 54,
   groups_served_count 1, first_group_first 37, first_group_third 81)。
2. **graph一致**: dependency-graph.json.gz (`54f9c364…`) の
   s4_masks[2251] == [1155314042043105280, 0] (closure tableのclass_lo 1155314042043105280
   と一致)、s4_status[2251] == 1 (unknown)、s4_cost[2251] == 54子。
3. **worklist一致**: Part CH refreshの probe-worklist (再生性オブジェクト・
   not published by design) のserving_class=2251行は54行で、その54キー
   (s5_index集合・(lo,hi) positions集合) はgraph s4_cost[2251]の54子と完全一致。
4. **base非解決**: Part CH merged canonical cache 6,294行 (`3124461b…`) に対し
   class 2251の54コスト子のヒットは **0/54** (WIN 0・LOSS 0・全54キー unresolved)。
5. **route-alive**: unconsumed closure WIN候補33キー (29 prior + batch-28
   aa001 (s5 28037) + aa002 (s5 87306) + aa006 (s5 129823) + aa007 (s5 135236)) との
   intersection **0** (class 2251はunconsumed WIN childを持たない。known WIN cost child
   も持たない)。
6. **zero packet collision**: 29 published packets (batches 1..27 + residual + batch-28、
   計 **1,460 packet rows / 1,448 distinct positions / 1,446 distinct s5**、28 prior
   パケットは PRIOR_BATCHES pin辞書を batch-28 makerソースから機械抽出してsha256検証
   28/28 OK、batch-28 kitは published pin `af19208f…` 検証済み) に対し、class 2251の
   54キーは positions (lo,hi)・s5_index 両方で collision **0**。
7. **quarantine 0**: n11-s5-evidence-quarantine.json (`81d23160…`) active 2キーとの
   intersection **0/54**。
8. **backup**: rank 36 class 34269 (mask [1152921504624672768, 68719476736]) も同一
   ゲート群をすべて PASS (cost 54子、worklist一致、base hits 0/54、WIN33 intersection 0、
   packet collision 0、quarantine 0)。published-table orderにより rank 35 class 2251を
   優先する。

合法手数: class 2251の54キーは legal 79..101 (worklist列の再導出)。

## 3. kit設計 (宣言後にscaffold)

- 実験dir: `research/experiments/n11-centralreply-closure-class2251-batch29-20261123/`
  (README・MANIFEST-sha256・scripts・input 54 CSV + batch-keys.json・output・val-gate)。
- runner: pinned byte-clone `runbatch.sh` (`f591f8c2…`・変更なし)。pre-registered
  stop rules: WIN rc=45 / MISMATCH rc=42 / p1/p2 fail rc=43/44。budget 15M。
  2-pass fresh-cold・`# replay_done`のないpassファイルはTRUNCATED-RETRY。
- solver: jsreplay.js published byte-clone (`84585617…`)。
- keys: batch-29 key ids **ab001..ab054** (2-letter prefix設計継承。freshness gate:
  published 1-letter形式 `^[a-z][0-9]{3}$` + published idに「ab」始まりは存在しない)。
- base: Part CH merged canonical cache 6,294行 (`3124461b…`) + published update8
  receipts (`b658290a…`)。graph `54f9c364…`、closure table (Part CH reaudit
  `baa2db13…`・`76cad2a1…`・`75e59441…`)、quarantine `81d23160…`、Board
  `954d3a10…`、policy `78655e94…` はpublished pin。
- PRIOR packets: batches 1..28 + residual (29 packets、1,460 rows) をsha pin
  (batch-28 dir追加)。
- val-gate: batch-28 drive-2のval-gate方式 (sanctioned keys・published baselines) を
  継承し、本host fresh 4/4 を要件とする (詳細はscaffold執筆時に確定し、実験dirに
  pinする)。
- drive構成: drive-1 (54キー、WIN-HALTは事前登録stop ruleどおり。WIN 2行観測で
  wave haltはbatch-28 drive-1/2と同じ設計)。EXHAUSTEDは続行。

## 4. 期待機械簿記 (事前登録)

probe結果によって class 2251 の unknown_now 54から減算される。本宣言は
結果非予告であり、いかなる勝敗も宣言しない。closure table membership変動
(flips/newly_free) はprobe完了後のreauditが機械導出する。nodes数は
bookkeepingであり勝敗ではない。

## 5. UNKNOWN担保

**標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2 {59,60}・
class 1/2/4・class 10968・class 23964・class 5343 (54キーすべて)・class 2251
(54キーすべて・本batch-29の全キーを含む)・class 34269 は本Partの実行・出版の
どの時点でもUNKNOWNのまま。** WIN採用は引き続き scrutiny owner C++第二実装 gate
(`9193f5b6…`) のみ (本レーンは代行しない)。

## 6. 不接触

Part CG (batch-28 drive2win thirdimpl・並走所有) のdir・outputs・進行、
batch 1..28各published dir (不変)、Part CE宣言済みのbatch-23 fileless 51キー・
batch-24 fileless 49キー、fast lane (y=23)・finite-field lane (K1254)・
inversive/z19 lanes、19root計画、unconsumed closure WIN候補33キーの採用状態、
BASE cache (`3124461b…` Part CH merged) read-only不変。
