# batch-28: closure class 5343 exact-S5 probe (Part CB, 2026-11-23)

Part CB (宣言: note amendment commit `395219833f80a5d345c0acf999407b31e66832cb`・
publish-then-execute・宣言host実行)。Part BZ正本 merged scenario cache 6,293行
(sha256 `9115be9eca1e60828a90c50041f511b598ef79fc0be76d5e16821816e478e93e`) 上の
closure候補表 **rank 27 class 5343** (mask `[1171516445255794688, 0]`・
cost 54子すべてunknown) を対象とする exact-S5 probe batch。**verdict不消費**。
閉鎖・被覆・secured・root勝敗の主張はしない。

## 選定 (published baseから再導出・prose不使用・29-WIN交積)

- **rank 27 class 5343** は29-WIN交積空 (28 + o002 (s5 209134))・known WIN cost
  childゼロ・28 published packets (1,406行・1,392 unique・14 shared positions) と
  交差ゼロ・canonical hits 0/54・quarantine 0/54 (事前登録 maker
  `d1ffe72f7a92c190db4982bbb59d10da9d1a967a6425fbc75cf745a255422f16` 全gate
  PASS・4回実行byte一致・全55ファイル identical)。
- rank 22 class 10968・rank 23 class 23964 は PKT-collision blocked継続。
  rank 28 class 13758 (= unknown {459528} = batch-27 key o031)・rank 29 class
  14103 (= {460145} = o037) は batch-27 published packet (Part BR) と衝突する
  ため本選定では除外 (両クラスはreaudit後の将来回)。rank 2 class 1849 ==
  {81011} (l028)・rank 6 class 13342 == {209134} (o002)・rank 10 class 16957 ==
  {91296, 368510}・rank 20 class 12643 == {115192}・rank 21 class 31600 ==
  {62435, 192809}・rank 24 class 25835 == {150241}・rank 25 class 30565 ==
  {68580, 191299}。rank 19 class 5687・rank 26 class 5690 は receipt WIN子
  209644 で route-dead。
- BZ adoption tie (maker gate): batch-24 y002/y004 + batch-27 o001/o003/o005/o007
  の6 LOSS行がbase内LOSS(2)・class 16957 unknown 51・class 13342 unknown 50・
  published候補表 (807行) と ranks 1..30 全行一致・5830 receipt wins 5。
- 54キー **aa001..aa054** (2文字prefix `aa` は新設計: 26単文字は packets
  1..27で使用済み。makerは prior 28 packets全key idが ^[a-z][0-9]{3}$ 形式で
  あることをfail-closed gateで固定)。s5昇順 28037..199739・legal 64..96・
  membership {4:44, 3:9, 2:1}・Board再計算 54/54。
  batch-keys.json sha256
  `af19208fafb61cc20892fa968bc373fe2c4f79da94744dfeed9d2f40ea8481e5`
  (schema `n11-centralreply-closure-class5343-batch28-input-v1`・budget
  15,000,000)。
- script pins: jsreplay.js
  `845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df`
  (byte-copy)・runbatch.sh
  `f591f8c2b67326e53873f8ea70f8d04d18423e7c8ef8359838cbafe8264f3b84`
  (byte-copy)・runwave.sh
  `8efd78c258619d4b7e8795acf22f5eeeb017290c622b28e35edc3972f90c9b84`
  (byte-copy)・drive_batch28.sh
  `08dc059c55f4337d2c0a58c7e644a529af604a052a9137381345c3af6b6a2a5f`・
  row_audit_batch28.py
  `656cac31fd95f7193c3df12efa05512cf2e746063740cfee7e5c574a5be66d56`・
  row_audit_batch28_win_halt.py (修正版・下記事故記録1)
  `9686728207f3cbb3015e4ca0a3be03bcc1f585ef573dd149889c4e82ac499e7d`。

## val-gate (pinned jsreplay `84585617…`)

- **cb-host 4ファイル (`*.cb-host.out`) は本実行hostの再生成: 4/4 node-exact
  (wall_s比較外・禁止四角 95,670)**: at2m 2キー result 0 / budget 2,000,000
  exhaustion (nodes 2,000,000)・15m基準キー result 2 / nodes 3,651,923 と
  5,040,200・`# replay_done` x4 (truncationなし)。
- published-baseline 4組は batch-27 published kitのbyte-copy (本Partの実行
  前提条件: published baselineに対するnode数完全一致・達成)。

## drive-1 結果 (宣言commit `39521983`の事前登録stop rulesどおり)

- drive invocation 1回 (drive_batch28.sh・2 worker・260s有界・2-pass fresh
  cold・budget 15M) で **両workerとも最初のキーで事前登録 WIN-HALT rc=45**
  (aa002: 2026-11-23T15:22:39Z・aa001: 2026-11-23T15:23:55Z)。
- **aa002 WIN (honest label)**: replay result 1・two-pass node-exact・nodes
  6,527,041 (budget 15M内)・key (1171516445390012416, 0)・s5 index 87306・
  legal 86 (published packetのBoard再計算一致)・membership 2・wall 72/73s。
- **aa001 WIN (honest label)**: replay result 1・two-pass node-exact・nodes
  13,183,855・key (1315631633331650560, 0)・s5 index 28037・legal 88・
  membership 4・wall 147/75s。
- 両WIN行は **30番目・31番目の unconsumed closure WIN候補** として誠実記録
  (29候補 (o002込み) と書き込みとも非接触・採用判断は scrutiny owner C++
  第二実装 gate pin `9193f5b6…` 待ち・本レーンは代行しない)。
- 残り52キー (aa003..aa054) は fileless UNPROBED。EXHAUSTED 0・MISMATCH 0
  (rc=42不発)・truncated断片 0 (260s有界内に両workerとも最初のキーが完走)。
- row-audit-winhalt (schema
  `n11-centralreply-closure-class5343-batch28-rowaudit-winhalt-v1`・
  completed/fragment/fileless はrawの `# replay_done` 有無とstatus.logから
  導出・haltキーidは一切固定しない): PASS (completed 2 = WIN 2・LOSS 0・
  fragment 0・fileless 52・unprobed 52)・3回実行byte一致 (json sha256
  `3f50b4f6df4e5139c9559e9a8a727bcfa170edf07e2623ecaf23e4732707cbd6`)・
  tamper battery 7/7検出 (verdict反転 / nodes改竄 / packet legal改竄
  (batch-keys.json) / status WIN-pair除去 / replay_done strip / budget改竄 /
  nondigit nodes・すべてscratch copy上で実施し実験filesはbattery前後で
  byte同一)。

## 意味 (route statementのみ)

2つの独立的な単WIN子 (aa001・aa002) により (いずれかが採用された場合)
**class 5343 の全LOSS閉包ルートは反駁証拠を持つ** (batch-21 a003・batch-22
k002・batch-26 l028・batch-27 o002 に続くsnapshots)。verdictは不消費のまま・
採用は別adoption Part (pinned fail-closed merger `90711961…`) 経由のみ。

## honest事故記録 (Part CB)

1. 事前登録版 `scripts/row_audit_batch28_win_halt.py` (宣言pin sha256
   `730ef5505deb9ea54c8a0c2986f88e9d071a1b76d138f4c26b9859208c637438`) は
   batch-26版からのsed適用時に単文字前提のkey id gate (len 4・first letter・
   `o\d{3}`) が残っており、batch-28の2文字prefix `aa###` に対して
   fail-closeした (数値・監査対象ファイルへの影響なし)。差分は該当gate
   1箇所を `aa[0-9]{3}` 形式に修正するだけの最小派生版を出版し全行監査に
   使用した (fail-close自体もここに誠実記録する)。
2. tamper battery構築時の2件 (input CSV直接改竄・sedパターン不一致による
   無効なbattery) はbattery側の構築ミスであり監査のgapではない
   (実験filesは無改変・正規battery 7/7検出で裏どり済み)。

## UNKNOWN担保

標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2
{59,60}・class 1/2/4・class 10968・class 23964・class 5343 (54キーすべて・
aa001/aa002を含む) は本batchの実行・出版のどの時点でもUNKNOWNのまま。
nodes数・wall秒数を勝敗として読まない。WIN採用は別adoption Part (pinned
merger `90711961…` 経由) のみ。
