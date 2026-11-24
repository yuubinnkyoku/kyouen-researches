# Part CT 完了log: batch-28 (class 5343) 最終残EXHAUSTED 1行 (aa050) の30M再probe — aa050 WIN解決・EXHAUSTED残消滅 (2026-11-23宣言・2026-11-24T00:05-00:15Z実行)

Part CT (publish-then-execute・単一オーナー・宣言
`research/log/2026-11-23-part-ct-b28aa050-reprobe30m-declaration.md`・commit `353fdfb0`)。
実験dir `research/experiments/n11-centralreply-class5343-b28aa050-reprobe30m-20261123/`。
Part CS 完了logが委ねていた「aa050の別条件 (30M) 再probe・cross-invocation設計」を完遂。

## 成果

- **aa050 (key (1152921504640401408, 4228)・s5 legal 94) は新条件budget 30,000,000で
  WIN解決**: result 1・nodes **25,541,199** (25M < nodes ≦ 30M)・2-pass fresh-cold
  node-exact・p1/p2ともwall 137sで生rawはwall込みbyte-identical。
- **batch-28 (closure class 5343) のEXHAUSTED残は 1行 → 0行**。54キーすべてが
  probe-level honest label確定 (46 WIN unconsumed / 8 LOSS (Part CH/CO で canonical
  adoption済み) / EXHAUSTED 0・window-exceeded 0・mismatch 0)。
  これはbookkeeping観察でありclosure・被覆・secured・root勝敗の主張ではない。
- verdict不消費: aa050 WIN行はscrutiny owner C++第二実装 gate `9193f5b6…` 待ちで
  unconsumed。canonical adoptionは別宣言adoption Part (merger `90711961…`) のみ。
- **cross-invocation p1/p2 resume設計の実働実証** (宣言どおり): 30M単発pass実測137s
  ( published 25M 131s・推定157sより高速) でp1は260s inner window内に完走・p2は
  inner timeout 260sで切断→published guardがsidecar退避 (P2-TRUNCATED-RETRY 1回 <2
  でWINDOW-EXCEEDED不発火)→次invocationでp2のみfresh-cold完走。**CS完了logの
  「単発invocation設計では回収不能」課題を設計変更ゼロ (published runner 1行diffのみ) で解決**。

## 監査 (audit_ct.py・schema `n11-centralreply-c5343-b28aa050-reprobe30m-audit-v1`)

- audit.json `9bf586b1ee8216b626a584153677da28af45b56bb70f476912d2232cfb1e1265`
  (stdout `b7f8badc…`)・3回実行byte-identical。ALL GATES PASS:
  probed 1/1・win 1・loss 0・exhausted @30M 0・window-exceeded 0・unprobed 0・
  anchors 2・val-gate 4。
- anchors (派生runner 30Mでend-to-end妥当性): aa036 → PASS `30000000,2,955659`・
  aa004 → PASS `30000000,1,15616012` + WIN-HALT (rc=45)。published値とnode-exact 2/2。
- val-gate fresh 4/4 node-exact (at2m×2 exhaustion 2,000,000・15m 3,651,923/5,040,200・
  wall 9/9/17/25s・at2m-1のみwall 9 vs published 8でnode比較外)。
- **tamper電池4/4捕捉**: (a) p2 nodes +1 → p1/p2不一致 (b) WIN→LOSS反転 →
  status.log PASS行照合 (c) replay_done削除 → truncated fragment (d) registry
  `reprobe_condition.budget` 29999999 → gate A (registry schema機械確認の上でフィールド指定・
  CQ/CS教訓適用)。各probe復元cmp・clean control byte一致。

## 出版 (全fetch-back byte一致)

- 宣言 `353fdfb0` (observed HEAD `41e3c3d6`・対抗宣言なし機械確認)。**誠実記録**:
  初回push `d14ce692` は実行側の本文抽出ミスで 15B `[object Object]` 混入 → 同一分内に
  正本 6,201B (sha256 `9bb9e7f4…`) を上書き (fetch-back byte一致確定)。
- A `d06c4d92` 30 files (scripts 6: jsreplay `84585617…` byte-clone / runbatch
  `f591f8c2…` 参照用 / derived runner `3b5083b4…` EXACTLY 1行diff
  (BUDGET 15000000→30000000) / maker `5b605215…` G1-G9 fail-closed・byte-stable
  (registry `f0ae762f…`) / step `854daf1e…` / audit `a3749094…`・input 5・sources 10
  (exh15m/exh20m/exh25m aa050 published raw全ピン + CQ anchors)・val-gate 8・README)。
  fetch-back 30/30。
- B `bf49af4f` 13 files (status.log 6行 + audit.json + raw 7 (truncated sidecar
  `a8ef85b8…` 1込み) + `.ct-host.out` 4)。fetch-back 13/13。
- C `2d3d4d87` README最終 (実行記録1-7 + interpretation guard) + MANIFEST-sha256
  (43 entries)。fetch-back 2/2。
- 実行timestampは2026-11-24T00:05-00:15Z (UTC)・dir/宣言ラベルの2026-11-23は
  本レーンセッション開始日。

## 運用知見 (今回new)

- (a) **run_typescriptからローカルファイルを読んでpushするときはfile_system.read_file
  戻り値の `.content` フィールドを使う** (`.text` ではない・objectをそのままString()化すると
  `[object Object]` 15Bが出版される・宣言初回push事故の原因・即時fetch-back検証が
  事故を1分以内に捕捉)。
- (b) README/宣言草案の手書きpinは機械sha検証で転置ミス2件を出版前に捕捉
  (pin転写は必ず機械経由の再実証)。
- (c) 30M級の2-pass超windowキーは「published runnerのfile-existence guardに任せる
  cross-invocation resume」で回収可能 (新設計不要・CSでaa050自体に実働実証済みの
  guardの再利用)。p1/p2が同wallだと生rawがwall込みでbyte-identicalになる。

## レジューム (着手前に必ず最新main再取得・hourly並走注意)

- (a) **batch-28全54キーprobe完了** (EXHAUSTED 0)。batch-28系のdrive/reprobe Partは完結。
  15M/20M/25M/30Mの全条件でexhaustion行は消えた。verdictはWIN 46 unconsumed (第三実装
  交叉検証はaa001/aa002/aa006/aa007/aa008/aa009のみcorroboration済み・CQ 7+CS 3+CT 1の
  11行は交叉検証open)・LOSS 8行は全行adoption済み。
- (b) 次に価値が高いのは (並走状況確認の上): **CQ/CS/CTで新たに解決したWIN 11行
  (aa004/aa005/aa021/aa028/aa030/aa031/aa032/aa035/aa047/aa053/aa050) の第三実装交叉検証**
  (Part CM/CG/CR形式・third_impl `08ea958f…`)。ただしaa050 (25.5M nodes) は第三実装
  1-runが260s窓を超える可能性が高く窓設計注意。
- (c) **Part CP (batch-30 drive-2・宣言 `7aaa0525` 21:56Z)** と **Part CI (batch-29・
  checkpoint `a5a159d7` 21:52Z)** はoutputs停滞継続ならtakeover規約判定
  (CIはab001..ab016の16 LOSSがcheckpoint 1/3・残ab017..ab054)。
- (d) **標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2 {59,60}・
  class 1/2/4・class 10968・class 23964・class 5343 (54キーすべて・aa050を含む) は
  どの時点でもUNKNOWNのまま。nodes数を勝敗として読まない。被覆・secured・root勝敗の
  主張をしない。**
