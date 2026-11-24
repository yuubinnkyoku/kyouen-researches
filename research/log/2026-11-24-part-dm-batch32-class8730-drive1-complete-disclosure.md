# Part DM drive-1 完了log + 3-host 並走の正直開示 (2026-11-24: batch-32 class 8730)

## 1. 結果 (pre-registered stop rules で drive-1 COMPLETE)

- **54/54 キーすべて PASS (honest label result=2)**・**WIN-HALT 0行・MISMATCH 0行・
  EXHAUSTED 0行**・budget 15M・2-pass fresh-cold・pinned runner
  runbatch.sh (f591f8c2…), pinned solver jsreplay.js (84585617…)
  で全部完了 (ALL-DONE・空キーガード発火)。
- nodes: **223,769,637/pass (2-pass 合計 447,539,274)**・最小 1,706,977 (ae042)・
  最大 8,966,840 (ae034)。各キー p1==p2 node-exact (runnerの GATE で全通過)。
- **verdict不消費** (54行の honest label はどこにも採用していない)。
  canonical adoption は別adoption Part (pinned fail-closed merger 90711961…)
  のみ。次回単一オーナー Part の候補: **b32loss54 increment**・BASE は現行
  canonical chain head 7bdfa236… (6,448行, Part DN時点)。
- **標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2 {59,60}・
  class 1/2/4・class 8730 (本batch 54キーすべて) はどの時点でもUNKNOWNのまま。**
  nodes数・wall秒数を勝敗や距離として読まない。被覆・secured・root勝敗の主張をしない。

## 2. 短い経緯 (3 host 並走の正直開示)

1. **元host** (宣言 88b7fc90, 2026-11-24T10:59:34Z・kit scaffold 8d852732
   11:01:12Z・val-gate fresh 4/4 node-exact 6bcbbc95, 11:04:39Z・sidecar
   .b32-host.out) は session終了で成果出版なしに停滞。54キー全て UNPROBED。
2. **host2 (本note書き手・13:04Z開始の長期レーン後継session)**: kit 68/68 を
   commit pin 6bcbbc95 で raw fetch・MANIFEST全件 sha256一致で復元・本host
   val-gate fresh 4/4 node-exact (sidecar .b32-host2.out)・interim note
   5ff7e53a (13:22Z・宣言済みPartの同レーン後継としての継続を明記) のあと
   drive-1 を実行し随時 increment 出版: inc1 1e1578a2 (ae001..008)・
   inc2 e38abac2 (ae009..020)・inc3 30084b79 (ae021..036)・
   inc4 721f2f9a (ae037..054 + 最終 status.log 54行・ALL-DONE)。
   drive実行時間 13:34:29Z..14:18:08Z (host2 wall時計)。
3. **host3 (並走の同レーン後継session・13:5x開始と推定・host2と非調整)**:
   inc2' 37f51283 (13:59:41Z・ae009..018 raws + 18行 status.log + sidecar
   .b32-host3.out 4件)・inc3' 9c8cd171 (14:15:18Z・ae019..034 raws +
   34行 status.log)。**同一54キーの同一driveを別workspaceで同時実行していた**。

## 3. 並走の機械検証 (host2 が発見後に実施)

- **raw 52ファイル (ae009..ae034 の 26キー × p1/p2) で host2手元副本と host3
  出版bytes (pin 9c8cd171) が budget/result/nodes/key_lo/key_hi 全 field
  一致 (52/52・wall_sのみ相違) の node-exact。** 探索の cross-host 決定論性が
  生のprobe出力レベルで機械確認された (3 host val-gate 4/4×3 に加えて)。
- 発見経緯: inc4後の raw fetch-back 108件照合で ae009..ae034 の52ファイルが
  wall_s のみ相違。commit指定raw (CDNキャッシュ回避) で e38abac2 時点は
  host2 bytes・30084b79/721f2f9a 時点は host3 bytes であることを確認
  → 経路commit列挙で host3 の increment 2件 (37f51283/9c8cd171) を特定。
- **main現行の last-writer 構成 (honest記録)**: raws ae001..ae008 = host2
  (inc1)・**ae009..ae034 = host3 (inc3')**・ae035..ae054 = host2 (inc3/inc4)・
  **status.log = host2 の54行** (inc4 が host3 の34行を上書きした。host3の
  34行は pin 9c8cd171 で失われていない)。すべての (result,nodes) は host2/host3
  両ログで一致している。
- 3 host の val-gate sidecar (.b32-host.out/.b32-host2.out/.b32-host3.out) は
  published baselines と 4/4×3 全host node-exact (host3分は host2 が 14:2xZ
  に fetch照合)。

## 4. インシデント (honest)

- **host2の環境リセット (~13:30Z)**: drive step 3件を1つのbash呼び出しに束ねた
  ところ外側 300s cap 超過で環境棄却・未出版作業状態喪失 (リセット前の
  ae001..ae004 local raws は出版前で証拠化されず)。**教訓: drive step は
  1呼び出し1step厳守** (inner timeout 260 が outer cap 290-300 より先に発火
  する設計は step単位呼び出しでのみ成立)。リセット後 kit再取得→val-gate再実行
  (4/4 再現・sidecars喪失分は再生成)→ae001..004 は fresh-cold re-probe で
  **同一nodes (3,729,310/3,127,842/5,421,696/2,403,926) を再現** (host内
  決定論性の追試確認)。
- **status.log の last-writer 上書き** (上記のとおり・両者の行は (key,result,
  nodes) で完全一致しており証拠は pin群で保全)。
- **並走の回避が不十分だった**: host2 は各push前に経路commit列をref取得して
  gatingしていたが、host3 の drive進行中の非出版状態は commit列に現れないため
  検知できなかった。increment出版間隔を短縮したことが結果的に検知を早めた。
  今後の同レーン継続sessionは **開始時の最新commit列に先行 increment/interimが
  あれば自driveの継続を再評価する** ことを条件にする (interim note 5ff7e53a は
  13:22Z 出版済みだったが、host3 の session開始取得時点で見えていない可能性
  がある)。

## 5. 残務 (次回sessionへ・単一オーナーで)

1. **adoption Part (b32loss54)**: 54 LOSS行 → pinned merger 90711961… で
  canonical chain head 7bdfa236… (6,448行) に併合するadoption (DL/DNテンプレ:
  fail-closed maker pins 108 raws + status.log + val-gate 12 files + 32 prior
  packets・merge-audit×3・refresh reaudit・delta extractor・tamper battery)。
  9193f5b6… C++ scrutiny は WIN採用条件 (本batchは WIN 0行のため不使用)。
2. 実験dir READMEの結果section更新 (「## 結果 (drive-1)」 placeholder置換) と
  MANIFEST-sha256 の output entries 追加 (108 raws + status.log + sidecars
  12)。host3 が完了log・README更新を出版する場合は二重更新に注意
  (host3のその後の出版: 14:15:18Z以降 none を host2 が 14:35Z時点で確認)。
3. class 8730 closure再評価は adoption 後の refresh reaudit が機械導出する
  (unknown 54→0 になりうるが、閉鎖/被覆/中身の主張はreaudit・adoption Part
  のgate以外からはしない)。

(本logは host2 が 2026-11-24T14:33:49.641Z に出版。実行環境 (bash) が終盤で一時利用不能に
なったため、本logの出版は connector 直送で行った・MANIFEST/READMEの追加更新は
上記残務へ回した。)