# Part CP 宣言 (2026-11-23): batch-30 (closure class 34269) drive-2 (WIN-CONTINUE) — 残50キー ac005..ac054 完走 — publish-then-execute

単一オーナー: n11中央応答レーン (長期レーン・本セッション本host: Part CP drive-1
`189a2e8e` と同一workdir・同一kit継続)。push直前の最新main直近コミット群に
batch-30 drive-2 / Part CP続行 / class 34269 への対抗宣言・takeover宣告なしを
機械確認済み (observed HEAD `a93fca9d4ac8cac2b72995da1f1043f77cc8edf7`・確認時刻 2026-11-23T21:55Z時点)。Part CI
takeover (batch-29 class 2251・checkpoint 1/3 `a5a159d7` 21:5xZ時点) ・Part CG
(batch-28 drive2win thirdimpl・takeover宣言 `d5e9acc2` 18:01Z以降outputs停滞)
・fast lane等すべて非接触。

## 1. スコープ

drive-1 (宣言 `189a2e8e`・outputs `05a5ac94`・完了log `a93fca9d`) でprobed済みの
4キー (ac001 LOSS 5,635,468 / ac002 WIN 10,752,246 / ac003 WIN 8,036,766 /
ac004 LOSS 5,816,333・全2-pass fresh-cold node-exact) を除く**残50キー
ac005..ac054 をWIN-CONTINUE設計で完走**する。**verdict不消費**
(probe結果のWIN/LOSSはhonest labelのまま・canonical adoptionは別adoption Part
(pinned fail-closed merger `90711961…`) 経由のみ)。閉鎖・被覆・secured・
root勝敗の主張はしない。EXHAUSTED (budget 15M) はhonest UNKNOWN
(same-condition再probeなし) でwave続行。

**WIN-CONTINUE** (Part CE/CK/CN先例): WIN行観測でwaveは停止しない。
runner内蔵stop rules (pinned `f591f8c2…`: WIN rc=45は当該キー単位 /
MISMATCH rc=42 hard-stop / p1/p2 fail rc=43/44) は一切不変で、
orchestration層のみrc=45後も次キーへ進む。完走条件は「50キーすべてに
PASS/EXHAUSTED判定 (2-pass node-exact)」または**session時間制約による
誠実打ち切り** (打ち切り時は成果分のみhonest出版・未probeキーはfileless
UNPROBEDのまま次回driveに委ねる)。

## 2. kit・pins (batch-30 scaffold `281d58e6` 所収・すべて不変)

- batch-keys.json `79fbd166…` (54キー・ac001..ac054)・runner runbatch.sh
  `f591f8c2…` (published byte-clone)・solver jsreplay.js `84585617…`
  (published byte-clone)。
- 出発状態: B commit `05a5ac94` のpublished outputs (status.log 9行・v1
  harness regexバグ由来の重複3行を append-onlyで含むまま継続・raw pass
  8ファイル)。done-setの機械再導出はstatus.logのdedup (v2正規表現) による
  (=ac001..ac004)。パスファイルはpublished bytesと同一 (drive-1で本hostが
  生成・fetch-back照合済み)。pinned runnerのtruncated-pass guard /
  replay_done guardが再開安全性を担保する。
- session script: **drive2_local_step.sh** (sha256 `95c3f15b5441e680031d2daf4c9c10fa965f6e8aa3af75c2c294acc57c4411f3`・published
  drive-1 session script v2 `e7b627a8…` からの最小delta: orchestration層の
  WIN-HALT wave 2判定のみ除去。dedup done-set・空キーガード・MISMATCH
  hard-stop・timeout 260 wrapperは継承)。**v1は使用禁止** (README・完了log
  開示のregexバグ)。wave成果物とともにB' commitでkitに同梱出版する。
- val-gate: 宣言後に本host fresh 4を再実施 (at2m×2 budget 2M・first-15m・
  second-15m budget 15M・published baselines `6e902ab1…`/`eeafe3ac…`/
  `8035fe54…`/`91dffdec…` とnode-exact比較・不一致ならhard-stop)。
  sidecar `.d2-host.out` 4ファイルは成果物出版に含める。

## 3. 期待機械簿記 (事前登録)

probe結果によって class 34269 の unknown_now 54から減算される
(reauditはprobe完了後の別機械導出)。本宣言は結果非予告であり、いかなる
勝敗も宣言しない。nodes数はbookkeepingであり勝敗ではない。

## 4. UNKNOWN担保

**標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2
{59,60}・class 1/2/4・class 10968・class 23964・class 5343 (54キーすべて)・
class 2251 (batch-29全キーを含む54キーすべて)・class 34269 (本batch-30の
54キーすべて・EXHAUSTED行を含む) は本driveの実行・出版のどの時点でも
UNKNOWNのまま。** nodes数・wall秒数を勝敗として読まない。WIN採用は
引き続き scrutiny owner C++第二実装 gate (`9193f5b6…`) 通過後の別adoption
Part (pinned merger `90711961…` 経由) のみ。

## 5. 不接触

Part CI takeover (batch-29 drive-1継続中) のdir・outputs・進行、Part CG
(aa006/aa007 thirdimpl) のdir・outputs・進行 (本レーンは着手しない・
takeover規約判定は次回以降に委ねる)、batch 1..29各published dir (不変)、
BASE caches (`3124461b…` Part CH merged・`854800f3…` Part CO merged)
read-only不変、fast lane (min>=4 band・K1273以降)・finite-field lane・
inversive lane・19root計画、EXHAUSTED行の高budget再probe (別宣言条件)・
WIN 64候補キーの採用状態、scrutiny owner C++ gate (`9193f5b6…`) 専権事項。
