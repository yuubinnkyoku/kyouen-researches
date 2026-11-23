# batch-29: closure class 2251 exact-S5 probe (Part CI, 2026-11-23)

Part CI (宣言: research/log/2026-11-23-part-ci-batch29-declaration.md・commit
`efd2d488`・publish-then-execute・単一オーナー n11中央応答レーン)。Part CH正本
merged scenario cache 6,294行 (sha256
`3124461b14e4f73a7248cbf5b96c7ff59ebfdcc05258adeb9c81791d86cc461e`・aa003
LOSS採用込み) + published update8 receipts (`b658290a…`) 上のclosure候補表
**rank 35 class 2251** (mask `[1155314042043105280, 0]`・cost 54子すべてunknown)
を対象とする exact-S5 probe batch。**verdict不消費**。閉鎖・被覆・secured・
root勝敗の主張はしない。

## 選定 (published baseから再導出・prose不使用・fail-closed maker 全gate PASS)

- **rank 35 class 2251** はWIN33交積空 (unconsumed closure WIN候補33キー:
  29 prior + batch-28 aa001/aa002/aa006/aa007)・known WIN cost childゼロ・
  29 published packets (1,460行・1,446 unique positions) と交差ゼロ・
  canonical hits 0/54・quarantine 0/54。maker
  `44575cb244ad02535a6878a4dd5d105971dc791354d3b8bc536004fd6970d873`
  (schema `n11-centralreply-closure-class2251-batch29-input-v1`) 全gate PASS。
- ranks 1..34の分類を機械pin (宣言どおり・正確なs5集合込み):
  ranks 1..15, 17..19, 21, 22, 25, 26 はWIN交積で反駁済み (例: rank 1
  class 23101 == {745184}、rank 3 class 16757 == {528497}、rank 11 class 2634
  == {103558, 103560, 103561}・rank 19 class 5343 ==
  {28037, 87306, 129823, 135236})。rank 16 class 5830 はWIN交積
  {103560, 103561} とknown WIN子 {126017, 131631, 162106, 197665, 206386} の
  **双方**で反駁済み。ranks 20 (class 5687)・27 (class 5690) は receipt WIN子
  209644でroute-dead。ranks 23 (class 10968) == {273033}・24 (class 23964) ==
  {495193, 550880}・28 (class 13758) == {459528}・29 (class 14103) ==
  {460145}・30 (class 30484) == {546902, 558506}・31 (class 34263) ==
  {528281, 553923}・32 (class 16901) == {528689}・33 (class 19749) ==
  {657407}・34 (class 23482) == {550446, 561141} は PKT-collision blocked。
  rank 37 class 34948 == {415128} もPKT-blocked (将来batch-30選定用の簿記pin)。
- runner-up: rank 36 class 34269 (groups [(12, 108)]) は全gate PASS・
  published-table orderにより rank 35 class 2251 (groups [(37, 81)])を優先。
- closure再導出はpublished Part CH reaudit closure-classes.csv (807行・
  `baa2db13…`) とrank→class・unknown全行一致。adoption ties (batch-20 53 x-keys
  全LOSS・BZ 6キー LOSS・class 16957 unknown 51・class 13342 unknown 50・
  Part CH aa003 LOSS・class 5343 unknown 53) はすべてbase内で機械検証。
- 54キー **ab001..ab054** (2文字prefix継続: `ab`はpublished packets全体で
  未使用をfail-closed gateで固定)。s5昇順 3964..93841・legal 79..101・
  membership {4: 48, 3: 5, 2: 1}・Board再計算 54/54。
  batch-keys.json sha256
  `330c0b9f3166e9f6e21b739a851a881d800ab9f58a14dccaa0c772118dee716c`
  (budget 15,000,000)。

## kit (published batch-28 kit runnerのbyte-clone)

- jsreplay.js
  `845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df`
  (byte-copy)・runbatch.sh
  `f591f8c2b67326e53873f8ea70f8d04d18423e7c8ef8359838cbafe8264f3b84`
  (byte-copy)。pre-registered stop rules: WIN rc=45 / MISMATCH rc=42・
  p1/p2 fail rc=43/44・budget 15M・2-pass fresh-cold・`# replay_done`のない
  passファイルはTRUNCATED-RETRY (evidenceでない)・EXHAUSTED 15Mは
  honest UNKNOWN (same-condition再probeなし)。
- val-gate: batch-28 drive-2方式を継承 (sanctioned 4キー: at2m×2 budget 2M・
  15m×2 budget 15M・published baselines byte-copy)。

## val-gate (本実行host fresh実行・scaffold時点で実施済み)

- **batch29-host 4ファイル (`*.batch29-host.out`) は本実行hostの再生成:
  4/4 node-exact (wall_s比較外)**: at2m 2キー result 0 / budget 2,000,000
  exhaustion (nodes 2,000,000)・15m基準キー result 2 / nodes 3,651,923 と
  5,040,200・`# replay_done` x4 (truncationなし)。
- published-baseline 4組は batch-28 drive-2 published kitのbyte-copy
  (本Partの実行前提条件: published baselineに対するnode数完全一致・達成)。

## drive-1 (実行予定・宣言protocol)

runbatch.shの直接起動 (未完キーずつ・2 solver並列上限)・各キー2-pass
fresh-cold・budget 15M。事前登録stop rulesどおりWIN-HALT rc=45でwave終了。
結果はstatus.log + raw outsを本dirのoutput/に蓄積し、完成後に出版・
row-auditは別セッションで実施予定 (宣言どおり)。

## honest記録 (scaffold時点)

Part CI宣言では「28 priorパケットはbatch-28 makerソースから機械抽出 sha検証
28/28」と記録済み。本scaffoldのmaker執筆時、PRIOR_BATCHES 29 pinsのうち
batch-21 (class 12643) パケットsha pin 1件に転写由来の1字不足 (66文字)が
あり、fetch実測 (batch-21 published packet sha256
`1f9346a7027e95b162f24ecb933bddec05151473d87ab7ed35832619026ae675`) との
不一致として機械検出・修正した (fail-closed設計が作動した実例。残り28 pins
は実測と完全一致)。またmaker初回実行時に (a) rank 16 class 5830の分類pinが
known WIN子5キーの併存を考慮していなかった点、(b) runner-up gateのindex
誤り (ranked[34]→ranked[35]) を、fail-closed gateがそれぞれ検出、修正後
全gate PASS。実験数値・選定結果への影響はない。

## UNKNOWN担保

標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2
{59,60}・class 1/2/4・class 10968・class 23964・class 5343 (aa001 WIN行を
含む54キーすべてが不消費のまま)・**class 2251 (54キーすべて・本batch-29の
全キーを含む)・class 34269** は本batchの実行・出版のどの時点でもUNKNOWNの
まま。nodes数・wall秒数を勝敗として読まない。WIN採用は scrutiny owner C++
第二実装 gate `9193f5b6…` を経由する別adoption Part (pinned merger
`90711961…`) のみ (本レーンは代行しない)。

## 不接触

Part CG (batch-28 drive2win thirdimpl・並走所有) のdir・outputs・進行、
batch 1..28各published dir (不変)、Part CE宣言済みのbatch-23 fileless 51キー・
batch-24 fileless 49キー、fast lane (y=23)・finite-field lane (K1254)・
inversive/z19 lanes、19root計画、BASE cache (`3124461b…` Part CH merged)
read-only不変。
