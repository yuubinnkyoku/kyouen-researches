# batch-32: closure class 8730 exact-S5 probe (Part DM, 2026-11-24)

Part DM (宣言: research/log/2026-11-24-part-dm-batch32-class8730-drive1-declaration.md・commit
`88b7fc90`・publish-then-execute・単一オーナー n11中央応答長期レーン)。Part DL正本
merged canonical cache **6,405行 (sha256
`60222707dd13902103fc8f7ef11c8487ec1be531ad0711e23e50c32154e30b84`・batch-31
51-LOSS行採用込み)** + published update8 receipts (`b658290a…`) 上のclosure候補表
**rank 30 class 8730** (mask [6052837899185946656, 0]・cost 58子中unknown子54すべて)
を対象とする exact-S5 probe batch。**verdict不消費**。閉鎖・被覆・secured・
root勝敗の主張はしない。batch-31 (Part DL) 採用後最初の新規closure class batch。

## 選定 (published baseから再導出・prose不使用・fail-closed maker 全gate PASS)

- **rank 30 class 8730** は re-derived ranked closure table (graph `54f9c364…` +
  DL base 6,405行 + update8 receipts による808行) が published Part DL/b31loss51
  reaudit closure-classes.csv (`50841fa4…`・808行) と **全808行 (rank→class,
  unknown) 完全一致**した中の **first-clean行** (first-clean gate: ranks 1..29は
  すべてblocker union非空をmaker gateで強制・追加selection pin ranks 31/44 +
  rank 42 packet衝突)。
- **closure pocket (rank 1..4) は全WIN-blocked (訂正記録)**: rank 1 class 23101
  unknown 1 = s5 745184 (batch-14 q042 WIN・WIN81 block + prior packet衝突)・
  rank 2 class 1849 unknown 1 = s5 81011 (batch-26 l028 WIN)・rank 3 class 2251
  unknown 1 = s5 93815 (batch-29 ab028 WIN)・rank 4 class 5804 unknown 4 = s5
  {198576, 207094, 212115, 212536} (= batch-31 WIN4行 ad024/ad028/ad043/ad055・
  ad043の15M EXHAUSTEDはPart DI 30M reprobe WIN supersede鎖込み)。pocket解消は
  WIN採用 (scrutiny owner C++ gate `9193f5b6…` 通過後・pinned merger
  `90711961…` 経由の別adoption Part) 待ちであり、本Partは副作用verdictを
  一切支払わない。
- **unconsumed WIN候補81キー (WIN81)**: WIN77 (batch-31 Part CY §2 gate 4と同一
  集合) ∪ batch-31 WIN4行 = 81 unique s5・すべてDL baseで未消費 (検証81/81)。
  class 8730の54子とのintersection 0・known WIN receipt cost child 0。
- **32 prior packets** (batches 1..31・batch-31 packet `d058fddc…`込み): 1,623
  key rows / 1,609 unique positions・sha pin 32/32検証。class 8730の54キーは
  position衝突 0。published key idに「ae」始まりは存在しない (freshness gate)。
- class 8730 facts: s5 30596..311727昇順・batch内重複なし・legal 88..105
  (Board再計算・LOCAL_RANGE pin)・membership histogram {2: 1, 3: 4, 4: 49}・
  quarantine 0/54・canonical-safe 54/54・base内解決済み4子 (s5 144458, 212464,
  310606, 311726 = LOSS(2))。cost 58 = known 4 + unknown 54。
- runner-up: rank 41 class 11490 (unknown 55・groups 4 [(16,48),(16,50),(48,16),
  (48,56)]・base解決済み1子 s5 376421 = LOSS(2)) 同一ゲート群 CLEAN。
  ranks 43 (class 14743) / 44 (class 15453) はcleanだがrank下位。
- honest開示: 旧deriveスクリプトのFIRST-CLEAN事実印刷にstale変数バグがあり、
  fail-closed makerのLOCAL_RANGE pinが検出 (rank 60近傍クラスのlegal範囲誤印刷)。
  真のclass 8730 legal 88..105でpin修正の上、全gate再実行PASS。派生物は不使用。

## 構成 (artifact map)

- `scripts/make_batch32_keys.py` (`2ddf4903…`・batch-31 published maker
  `2681c841…` からfork・上記全gateをfail-closed pinとして内蔵): 宣言前
  ローカル実行で `f46e663f…` (batch-keys.json) を確定。
- `scripts/runbatch.sh` (`f591f8c2…`・published byte-clone・stop rules内蔵:
  WIN rc=45 / MISMATCH rc=42・p1/p2 fail rc=43/44・budget 15M・2-pass
  fresh-cold・TRUNCATED-RETRY・EXHAUSTED はhonest UNKNOWN)。
- `scripts/jsreplay.js` (`84585617…`・published byte-clone)。
- `scripts/drive1_local_step_b32.sh` (`e43f5f83…`・published batch-31 drive-1
  v2 `26347816…` から最小delta: key-id正規表現 ad→ae の4箇所とヘッダ行のみ・
  機能body機械diff同等・WIN-HALT 2行 wave orchestration)。
- `input/batch-keys.json` (`f46e663f1676111ae67f5686f4a7807a8c1f7e4e1d9910ddb96ba61bcb5e705d`)
  + `input/ae001..ae054.input.csv` (54 single-row target CSV)。
- `val-gate/`: sanctioned 4キー (at2m×2 budget 2M・first-15m・second-15m
  budget 15M) のinput CSV + published baselines byte-copy
  (`6e902ab1…`/`eeafe3ac…`/`8035fe54…`/`91dffdec…`・batch-31/val-gateと
  同一bytes)。本host fresh 4/4 node-exact (sidecar `.b32-host.out`) がdrive
  開始要件 (一致しなければhard-stop)。
- `output/`: raw 2-pass solver出力 (aeNNN.p1.out / aeNNN.p2.out) + append-only
  `status.log` (drive実行後に出版)。

## 結果 (drive-1・2026-11-24T13:34:29Z..14:48:51Z UTC・ALL-DONE)

**54/54キーすべて probe-complete (ALL-DONE・session scriptのempty-key guard
により runbatch空起動なし)。**

- **PASS 54行・すべて honest-label result=2 (LOSS)。WIN 0行・EXHAUSTED
  0行・TRUNCATED 0行・MISMATCH 0。** 全108 raw出力 (54キー × p1/p2) は
  `replay,` 行 f1-8 (budget/result/nodes含む) 完全一致を機械確認
  (2-pass fresh-cold・budget 15M)。
- 合計 nodes (status.log PASS 54行の和): **223,769,637/pass** (2-pass
  node-exact・計447,539,274 expansions)。最小 1,706,977 (ae042)・最大
  8,966,840 (ae034)・平均 4,143,882。nodes数は勝敗ではなく計測値。
- 実行host構成 (honest): **host2** (`.b32-host2.out` val-gate 4/4) が
  ae001..ae008 (increment 1 `1e1578a2`)・**host3** (`.b32-host3.out` 4/4)
  が ae009..ae034 (increments 2-3 `37f51283`/`9c8cd171`)・**host4**
  (`.b32-host4.out` 4/4・host3の外側timeoutによる環境reset後にcommit pin
  `9c8cd171` からkit再建) が ae035..ae054 (increments 4-5)。host3の
  環境resetで未出版の ae035..ae046 ローカル成果 (PASS 12行) は破棄され
  fileless UNPROBED に戻ったのち host4 が再driveし**同一 nodes 12/12 を
  再現** (破棄前host3計算値との一致で、host間の追加の決定性検証になった・
  interim 3 note commit `25f71289` 参照)。
- **verdict不消費 (honest label)。** class 8730 の54 unknown cost children
  はこれで probe-level label がすべて LOSS になったが、**canonical adoption
  は別adoption Part (pinned fail-closed merger `90711961…` 経由) の専権**
  であり、本batchの成果はhonest labelのみ (閉鎖・被覆・secured・root勝敗の
  主張はしない)。本batchにWIN行・EXHAUSTED行が存在しないため、scrutiny
  owner C++第二実装 gate を要する行は本batchにはない (adoption規約自体は
  別Partの宣言が定める)。

**標準11×11空盤・19 central-reply roots・二石root・S2・class 5804 (55キー
すべて)・class 8730 (本batchの54キーすべて・WIN/LOSS/EXHAUSTED行を含む) は
本実験の実行・出版のどの時点でもUNKNOWNのまま。** nodes数・wall秒数を勝敗や
距離として読まない。WIN採用は scrutiny owner C++第二実装 gate (`9193f5b6…`)
通過後の別adoption Part (pinned fail-closed merger `90711961…` 経由) のみ
(本レーンは代行しない)。
