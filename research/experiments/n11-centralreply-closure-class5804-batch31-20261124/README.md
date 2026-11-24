# batch-31: closure class 5804 exact-S5 probe (Part CY, 2026-11-24)

Part CY (宣言: research/log/2026-11-24-part-cy-batch31-class5804-drive1-declaration.md・commit
`afc1bcc5`・publish-then-execute・単一オーナー n11中央応答長期レーン)。Part CU正本
merged canonical cache **6,317行 (sha256
`30ddad9dc0add7e21698e864b5c8e6ebd3e396c4eb6156a85ff2d34005c4`・batch-29
16-LOSS行採用込み)** + published update8 receipts (`b658290a…`) 上のclosure候補表
**rank 38 class 5804** (mask [6053400849139367936, 0]・cost 56子中55 unknown子すべて)
を対象とする exact-S5 probe batch。**verdict不消費**。閉鎖・被覆・secured・
root勝敗の主張はしない。batch-30宣言後最初の新規closure class batch。

## 選定 (published baseから再導出・prose不使用・fail-closed maker 全gate PASS)

- **rank 38 class 5804** は re-derived ranked closure table (graph `54f9c364…` +
  CU base 6,317行 + update8 receipts による808行) が published Part CU reaudit
  closure-classes.csv (`3019d37f…`・808行) と **全808行 (rank→class, unknown)
  完全一致**した中の **first-clean行** (first-clean gate: ranks 1..37はすべて
  blocker union非空をmaker gateで強制)。
- **ranks 1..37 + 40..42 はtriple pin (WIN77 intersection / known-WIN receipt
  children / packet collision) で機械反駁**。代表例: rank 4 class 2251
  (batch-29 packet 38キー衝突・CU 16-LOSS採用済み), rank 18 class 5830 known-WIN子5,
  **rank 36 class 34269 二重block (WIN交積 {38891,178184} = ac002/ac003自身 +
  batch-30 packet全54キー衝突)**, rank 37 class 34948 pkt{415128}。
- **unconsumed WIN候補77キー (WIN77)**: 29 prior (batch-29 maker WIN33 pin辞書) ∪
  batch-28 WIN46全行 (row-audit WIN35 + re-probe 11) ∪ batch-30 drive-1 WIN2行
  (ac002 s5 38891 / ac003 s5 178184) = 77 unique s5・すべてCU baseで未消費
  (検証77/77)。class 5804の55子とのintersection 0・known WIN receipt cost child 0。
- **31 prior packets** (batches 1..30・batch-30 `79fbd166…`込み): 1,568 key rows /
  1,554 unique positions・sha pin 31/31検証。class 5804の55キーはposition衝突 0。
- class 5804 facts: s5 97381..212536昇順・batch内重複なし・legal 82..101
  (Board再計算)・membership histogram {2: 1, 3: 7, 4: 47}・quarantine 0/55・
  canonical-safe 55/55・base内解決済み1子 (s5 167863 = LOSS(2))。
- runner-up: rank 39 class 11490 (unknown 55・groups 4 [(16,48),(16,50),(48,16),
  (48,56)]・base解決済み1子 s5 376421 = LOSS(2)) 同一ゲート群 CLEAN。

## 構成 (artifact map)

- `scripts/make_batch31_keys.py` (`2681c841…`・batch-30 published makerからfork・
  上記全gateをfail-closed pinとして内蔵): 宣言前ローカル実行で `d058fddc…` を確定。
- `scripts/runbatch.sh` (`f591f8c2…`・published byte-clone・stop rules内蔵:
  WIN rc=45 / MISMATCH rc=42・p1/p2 fail rc=43/44・budget 15M・2-pass fresh-cold・
  TRUNCATED-RETRY・EXHAUSTED はhonest UNKNOWN)。
- `scripts/jsreplay.js` (`84585617…`・published byte-clone)。
- `scripts/drive1_local_step.sh` (`26347816…`・batch-30 v2から最小delta: key-id
  正規表現 ac→ad のみ・WIN-HALT 2行 wave orchestration)。
- `input/batch-keys.json` (`d058fddc862c5f62b387eea7c7ac5b78f2c5063661371b388e5078772af4ff0e`)
  + `input/ad001..ad055.input.csv` (55 single-row target CSV)。
- `val-gate/`: sanctioned 4キー (at2m×2 budget 2M・first-15m・second-15m budget 15M)
  のinput CSV + published baselines byte-copy
  (`6e902ab1…`/`eeafe3ac…`/`8035fe54…`/`91dffdec…`)。本host fresh 4/4
  node-exact (sidecar `.b31-host.out`) がdrive開始要件 (一致しなければhard-stop)。
- `output/`: raw 2-pass solver出力 (adNNN.p1.out / adNNN.p2.out) + append-only
  `status.log`。

## 結果 (drive-1・2026-11-24T01:42:23Z..02:05:32Z UTC)

**WIN-HALT wave-end at 2 distinct WIN行 (pre-registered drive-1 stop)。**
対象 ad001..ad028 (probe 28/55キー・残27キー ad029..ad055 は未probeのまま停止)。

- **WIN 2行** (result=1・15M budget内で解決): **ad024** (key_lo
  6053401124017274880・legal 86・nodes 4,360,661) と **ad028** (key_lo
  6053682324116078592・legal 82・nodes 12,803,283)。両行とも p1/p2 2-pass
  fresh-cold で node数完全一致 (MISMATCH 0)。
- **LOSS(2) 26行** (ad001..ad023 ad025..ad027・result=2・15M budget内で解決)。
- **EXHAUSTED 0行・TRUNCATED 0行・MISMATCH 0**。全28キー (56 raw出力) の
  p1/p2 は `replay,` 行 f1-8 (含む budget/result/nodes) 完全一致を機械確認。
- 合計 nodes (status.log PASS 28行の和): 138,729,770 (WIN 2行 17,163,944 +
  LOSS 26行 121,565,826)。nodes数は勝敗ではなく計測値。
- WIN行の解釈規約: 上記2行は「15M budget内での solver result=1 (WIN)」という
  honest実行記録のみ。**WIN採用は scrutiny owner C++第二実装 gate (`9193f5b6…`)
  通過後の別adoption Part (pinned fail-closed merger `90711961…` 経由) のみ**
  (本レーンは代行しない)。status.log は append-only・raw出力は出版時点のまま。
- 次wave (ad029..ad055・drive-2/3) は後続Part。EXHAUSTEDが出た場合のみ
  same-condition再probeの対象となり、それも honest UNKNOWN。

**標準11×11空盤・19 central-reply roots・二石root・S2・class 5804 (本batchの
55キーすべて・WIN/LOSS行を含む) は本実験の実行・出版のどの時点でもUNKNOWNの
まま。** nodes数・wall秒数を勝敗として読まない。
WIN採用は scrutiny owner C++第二実装 gate (`9193f5b6…`) 通過後の別adoption Part
(pinned fail-closed merger `90711961…` 経由) のみ (本レーンは代行しない)。
