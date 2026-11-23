# Part CP 宣言 (2026-11-23): batch-30 (closure class 34269) 54-key probe — publish-then-execute

単一オーナー: n11中央応答レーン (長期レーン・本セッション本host)。対抗宣言なし
(push直前の最新main直近12コミットに batch-30 / class 34269 / Part CP の言及ゼロを
機械確認済み・observed HEAD `8b75b7866ea52689e133ef7806b39ad34a9534d3`
2026-11-23T21:41:48Z「Part CI takeover drive-1 val-gate」。Part CI (batch-29
class 2251) はtakeover sessionが所有中・本宣言は非接触)。

## 1. スコープ

closure campaign継続として、closure class 34269 (rank 36・Part CO reaudit現行
closure table) の54 cost childrenを2-pass fresh-cold probeする (batch-30)。
**verdict不消費** (probe結果の WIN/LOSS は honest labelのまま、canonical
adoptionは別adoption Part (pinned fail-closed merger `90711961…`) 経由のみ)。
閉鎖・被覆・secured・root勝敗の主張はしない。EXHAUSTED (budget 15M) は
honest UNKNOWN (same-condition再probeなし)。

**BASEはPart CO採用後の6,301行正準cache** `854800f3…` (Part CH 6,294行
`3124461b…` + batch-28 7-LOSS行) を最初のbatchとして使用する。batch-28
completion後初の新規closure class batchである。

## 2. 選定ゲート (本セッションで機械実施済み・正直開示)

publish-then-execute規約に対する正直開示として、**選定ゲート検証 (read-only解析)
とfail-closed makerの実行 (probe packet生成・solver不使用) は本宣言の出版前に
本hostで機械実施済み**である。solver実行 (val-gate fresh・probe) は宣言後にのみ
行う。cherry-pick不可能性は (a) 実験dir構成、(b) 入力sha pin群、(c) stop rules、
(d) 選定ゲート群 (下記、全てmaker `make_batch30_keys.py` 内にfail-closed pin)
の事前登録により担保される。

機械確認済みゲート (すべて published 正本からの再導出):

1. **closure table一致**: Part CO reaudit closure-classes.csv
   (`9d3965d9…`・808行) をgraph + CO base 6,301行 + update8 receipts
   (`b658290a…`) から再導出したranked closure tableと**全808行
   (rank→class, unknown) 完全一致・0不一致**。rank 36 = class 34269
   (unknown_now 54, groups_served_count 1, first_group_first 12,
   first_group_third 108)。
2. **graph一致**: dependency-graph.json.gz (`54f9c364…`) の
   s4_masks[34269] == [1152921504624672768, 68719476736] (closure
   tableのclass_lo/class_hiと一致)、s4_status[34269] == 1 (unknown)、
   s4_cost[34269] == 54子。
3. **base非解決**: CO merged canonical cache 6,301行 (`854800f3…`) に対し
   class 34269の54コスト子のヒットは **0/54** (known children {}・
   derived_known == pinned {})。
4. **route-alive (WIN64)**: unconsumed closure WIN候補 **64キー**
   (published batch-29 makerのWIN33 pin辞書33キー
   `44575cb2…`掲載の29 prior + batch-28 aa001/aa002/aa006/aa007 +
   published batch-28 row-audit.json `00c32383`系のWIN 35行・全体で
   33+35−4重複=64 unique s5) はすべてCO baseで未消費 (検証64/64)。
   class 34269の54子とのintersection **0**。known WIN receipt cost child
   も持たない。
5. **ranks 1..35 + 37の機械pin (triple分類)**: 各rankの classification
   (unconsumed-WIN64 intersection / known-WIN receipt children / packet
   collision) をfail-closed triple pinとして全部機械再導出・一致を確認。
   代表例: rank 4 class 5343 unknown 46 (win35・ pkt46), rank 16 class 5830
   (win2 + kwin5・batch-29先行例のwinknown継続), rank 20 class 5687 /
   rank 27 class 5690 (knownwin {209644}), rank 21 class 12643
   win{115192} (**batch-21 a003自身の未消費WIN候補による反駁・Part CO
   レジュームの「次点class 12643」は機械判定により選定不可と確認**),
   rank 23 class 10968 pkt{273033}・rank 24 class 23964 pkt{495193,550880}
   ほかpublished packet由來のpkt-block継続, **rank 35 class 2251 は
   batch-29 published packet全54キーによるpkt完全衝突 (batch-29進行中・
   二重probe禁止)**, rank 37 class 34948 pkt{415128} (batch-29 maker
   RANK37 bookkeeping pinの継承)。
6. **zero packet collision**: 30 published packets (batches 1..28 +
   batch-14 residual + **batch-29**、計 **1,514 packet rows / 1,500
   distinct positions**、sha pin 30/30検証・batch-29 packet
   `330c0b9f…`) に対し、class 34269の54キーは (lo,hi) positions両方で
   collision **0**。
7. **quarantine 0 / canonical 54**: n11-s5-evidence-quarantine.json
   (`81d23160…`) とのintersection **0/54**・canonical-safe形式 54/54・
   mask_to_index == derived s5 index 54/54・Board再計算legal popcount
   54/54 (範囲 76..97)・membership histogram {2: 9, 3: 8, 4: 37}
   (graph cost関係から再導出)。
8. **adoption ties (machine-pinned)**: batch-20 x53キーすべて base内
   LOSS(2)・class 12457 unknown 0 / Part BZ 6キー LOSS・class 16957
   unknown 51・class 13342 unknown 50 / Part CH aa003 LOSS / **Part CO
   7キー (aa015/aa017/aa018/aa023/aa024/aa029/aa036) すべて base内
   LOSS(2)・class 5343 unknown 46** — 全て現在baseで機械検証。
9. **runner-up**: rank 38 class 5804 (unknown 55・groups 4
   [(38,59),(38,61),(49,58),(49,62)]) が同一ゲート群 CLEAN (target以外の
   最初のclean行)。rank 36 class 34269がpublished-table orderにより選定。

合法手数: class 34269の54キーは legal 76..97。s5 36668..958143昇順。

## 3. kit設計 (宣言後にscaffold)

- 実験dir: `research/experiments/n11-centralreply-closure-class34269-batch30-20261123/`
  (README・MANIFEST-sha256・scripts・input 54 CSV + batch-keys.json・output・val-gate)。
- runner: pinned byte-clone `runbatch.sh` (`f591f8c2…`・変更なし)。pre-registered
  stop rules: WIN rc=45 / MISMATCH rc=42・p1/p2 fail rc=43/44・budget 15M・
  2-pass fresh-cold・`# replay_done`のないpassファイルはTRUNCATED-RETRY
  (evidenceでない)・EXHAUSTED (result 0) はhonest UNKNOWNで継続。
- solver: jsreplay.js published byte-clone (`84585617…`)。
- keys: batch-30 key ids **ac001..ac054** (2-letter prefix設計継承。
  freshness gate: published idに「ac」始まりは存在しない、全30 published
  packet走査済み)。
- batch-keys.json pin: `79fbd1664f4ad66ea62d9c8a8aa5aaff5d16bcdaa397895119ce4d8f47961232`
  (maker出力・宣言前ローカル実行で確定・scaffoldで出版、誰でもpublished
  bytesから再現可能)。
- PRIOR packets: 30 packets (上記) をsha pin。base: CO merged 6,301行
  (`854800f3…`) + update8 receipts (`b658290a…`)。
- val-gate: batch-28/29方式継承 (sanctioned 4キー: at2m×2 budget 2M・
  15m×2 budget 15M・published baselines byte-copy
  6e902ab1/eeafe3ac/8035fe54/91dffdec)。**本host fresh 4/4 node-exact**
  を宣言後に必須とする (scaffold A出版要件・不一致ならhard-stop)。
- drive-1: WIN-HALT設計 (WIN 2行観測でwave halt・batch-28 drive-1/2・
  batch-29と同じ)。2 worker (1キー/worker) 並列上限・各workerは
  `timeout 260`でwrap (外側呼び出し上限290sに対しinner先発火・Part CN
  運用知見継承)・残キー列挙が空の場合のsession script空キーバグ防止
  `if rem` ガード事前登録。status.logはappend-only。EXHAUSTEDは続行。
- orchestration層 (stop rulesとは独立): session-local
  `drive1_local_step.sh` をscaffoldに同梱出版。

## 4. 期待機械簿記 (事前登録)

probe結果によって class 34269 の unknown_now 54から減算される。本宣言は
結果非予告であり、いかなる勝敗も宣言しない。closure table membership変動
(flips/newly_free) はprobe完了後のreauditが機械導出する。nodes数は
bookkeepingであり勝敗ではない。

## 5. UNKNOWN担保

**標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2
{59,60}・class 1/2/4・class 10968・class 23964・class 5343 (54キーすべて・
EXHAUSTED 11行含む)・class 2251 (batch-29全キーを含む54キーすべて)・
class 34269 (本batch-30の54キーすべて) は本Partの実行・出版のどの時点でも
UNKNOWNのまま。** nodes数・wall秒数を勝敗として読まない。WIN採用は
引き続き scrutiny owner C++第二実装 gate (`9193f5b6…`) 通過後の別adoption
Part (pinned merger `90711961…` 経由) のみ (本レーンは代行しない)。

## 6. 不接触

Part CI takeover (batch-29 drive-1進行中・最新出版 val-gate `8b75b786`)
のdir・outputs・進行、Part CG (batch-28 drive2win thirdimpl・takeover宣言
`d5e9acc2` 18:01Z以降outputs停滞・CI takeover宣言も非接触明記) の
dir・outputs・進行 (本レーンも着手しない・次回以降のtakeover規約判定に
委ねる)、batch 1..29各published dir (不変)、BASE caches (`3124461b…`
Part CH merged・`854800f3…` Part CO merged) read-only不変、fast lane
(min>=4 band・K1273以降)・finite-field lane・inversive lane・19root計画、
EXHAUSTED行の高budget再probe (別宣言条件)・WIN 64候補キーの採用状態、
scrutiny owner C++ gate (`9193f5b6…`) 専権事項。
