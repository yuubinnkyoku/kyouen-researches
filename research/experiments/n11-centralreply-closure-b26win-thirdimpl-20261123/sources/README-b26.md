# batch-26: closure class 1849 exact-S5 probe (Part BQ, 2026-11-23)

Part BQ (宣言: note amendment commit `8e64ba1c`・実行前に出版・publish-then-execute)。
閉包候補表 (Part BI refresh reaudit `d57a7609…` 807行) の **rank 24 class
1849** (mask [1152922672972169216, 0]・groups served (36,40)(36,80)・cost
53子すべてunknown) を対象とする exact-S5 probe batch。**verdict不消費**。
閉鎖・被覆・secured・root勝敗の主張はしない。

## 選定 (published baseから再導出・prose不使用)

- ranks 1..19 および 21・23 は従来どおり反駁済み: 27-WIN交積 (19 prior
  + a003 + k002 + s001/s002 + y001/y006 + i001/i002) または known WIN子。
  rank 17 = {115192}・rank 18 = {150241}・rank 19 = {62435, 192809}・
  rank 21 = {91296, 368510} に加え **rank 23 class 30565 は今回の反駁
  証拠が確定**: unknown子集合と 27-WIN 集合の交積は厳密に
  {68580, 191299} (published Part BP honest WIN行 i001+i002・3番目の
  WIN-PAIR反駁・verdict不消費)。
- rank 20 class 10968・rank 22 class 23964 は fail-closed overlap gate
  でblocked継続 (batch-25 packet を prior に加えても衝突ピン不変:
  10968 = {273033} = batch-12 n018・23964 = {495193, 550880} =
  batch-13 p007 + batch-4 e043。NOT route-dead・WIN反駁証拠ゼロ)。
- rank 25 class 5690 は route-dead (update8 receipt WIN子 {209644}) の
  ため選定対象外。よって機械選定は **rank 24 class 1849**。runner-up
  rank 26 class 13342・backup rank 27 class 5343 (両方 route-alive・
  交差ゼロ・maker内で機械検証)。

## preflight (fail-closed maker `make_batch26_keys.py` `a74250d6…`)

全gate PASS・4回実行byte一致・tamper battery 8/8検出 (T1 graph sha
pin / T2 CLASS_MASK 1bit / T3 batch-25 prior packet pin / T4
prior-rows pin 1299→1300 / T5 rank-23 evidence pin 191299→191300 /
T6 PKT-collision pin 273033→273034 / T7 rank-25 route-dead known-win
pin 209644→209645 / T8 EXPECTED_RANKS rank-29 pin 14103→14104)・clean
control PASS。

- 53キー l001..l053 (s5昇順 3170..81036・legal 75..101・Board再計算
  53/53・membership {4:44, 3:8, 2:1})。
- canonical cache 6,235行 `f6649fe3…` hits 0/53・quarantine 0/53。
- prior 26 published packets (batches 1..25・1,299行・1,285一意;
  cross-packet重複14位置は membership による正規重複で簿記) overlap
  0・key id prefix "l" は全packetで未使用 (未使用文字は {l, o} で
  "l" を使用)。
- batch-keys.json `f1ea43ae…` (schema
  `n11-centralreply-closure-class1849-batch26-input-v1`)。
- 新規gate: 27-WIN集合・rank-23反駁tie (== {68580, 191299})・
  EXPECTED_RANKS rank-29拡張 (14103)。

## val-gate (pinned jsreplay `84585617…`・実行host)

4/4 node-exact (wall_s比較外・禁止四角 95,670):
at2m 2キー result 0 / budget 2,000,000 exhaustion・15m基準キー
(2, 3,651,923) と (2, 5,040,200)。published-baselineはbatch-23/24/25と
同一byte-copy・this-hostは本ホスト再生成。

## drive-1 結果 (宣言commit `8e64ba1c`の事前登録stop rulesどおり)

7回の bounded invocation (2 worker・260s有界・truncatedはfresh-cold
再実行) で **l028 WIN** に到達し WIN-HALT:

- **l028 WIN (honest label)**: replay result 1・two-pass node-exact・
  nodes 4,893,014 (budget 15M内)・key (1153485622925590528, 0)・
  s5 index 81011・legal 88・membership 3・wall 52/52s → 事前登録
  WIN-HALT rc=45 (2026-11-23T08:21:45Z)。**28番目の unconsumed
  closure WIN 候補**。
- LOSS (採用候補のみ・verdict不消費) 30行: l001..l027 (27行)・l029・
  l031・l033 (worker2はWIN-HALT後も走行中でl033を完了後、次キー作業中
  に260s timeoutで停止)。すべて two-pass node-exact PASS・mismatch 0・
  budget exhaustion 0。
- fragment: **l035 のみ** (p1 truncated・`# replay_done`なし・NOT
  evidence・UNPROBED。将来の continuation で fresh-cold 再実行)。
- fileless UNPROBED: 21キー (l030・l032・l034・l036..l053)。
- 残り22キー (fragment 1 + fileless 21) は宣言済みstop ruleにより
  WIN-HALT後の非探索として UNPROBED のまま (verdict不消費)。
- row-audit-winhalt (schema
  `n11-centralreply-closure-class1849-batch26-rowaudit-winhalt-v1`・
  事前登録版 script `3bcf7857…`): PASS・3回実行byte一致 (json
  `8c91b134…`・derived_state=true)・tamper battery 3/3検出 (l028 p1
  verdict反転 / 未probeキー l040への偽verdict行 / l028 verdict行
  除去・scratch上で実施し実験filesは無改変)・clean control PASS。

## 意味 (route statementのみ)

l028 の単独WIN行により (採用された場合) **class 1849 の全LOSS閉包
ルートは反駁証拠を持つ** (batch-21..23 と同型の単独WIN子パターン)。
l001..l027・l029・l031・l033 の30 LOSS行は採用候補のみ (別宣言の
adoption Part 経由のみ)。ただし verdict は一切消費していない: 採用判断
は scrutiny owner C++第二実装 gate pin `9193f5b6…` 待ち (本レーンは
代行しない)。canonical cache 6,235行 `f6649fe3…` は read-only・不変。
10968・23964 は blocked (packet交差・NOT route-dead)・5690 は
route-dead。次batch (batch-27) 選定は 28-WIN交積 (27 + l028 (s5
81011)) の反駁簿記で maker内で機械選定する。当面のroute-alive候補は
rank 26 class 13342 (runner-up)・rank 27 class 5343 (backup)・rank 28
class 13758・rank 29 class 14103。rank 30 class 30484 以降は packet
交差の前調査必要 (rank 30..32 は衝突ありと preflight で観測済み)。

## 検証規律

nodes数・expansions数を勝敗として読まない。WIN/LOSS採用は別宣言の
adoption Part (pinned fail-closed merger `90711961`) でのみ。
**標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・
S2 {59,60}・class 1/2/4・class 10968・class 23964・class 30565・
class 1849 (53キーすべて・l028・30 LOSS行を含む) はどの時点でも
UNKNOWNのまま。** 被覆・secured・root勝敗の主張はしない。

## 再現

1. `python3 scripts/make_batch26_keys.py` (published pinsをsha検査し
   53キーを再導出・全gate PASSで終了)。
2. `node scripts/jsreplay.js --exact-replay=val-gate/<...>.input.csv
   --exact-replay-budget=2000000|15000000` (val-gate 4件)。
3. `bash scripts/drive_batch26.sh` (残キーを2 worker 260s有界で順次
   2-pass fresh-cold・WIN-HALT rc=45は事前登録・完了行は再実行しない)。
4. `python3 scripts/row_audit_batch26_win_halt.py` (halt時点の部分行
   監査・byte一致JSONを再生成)。

## 出版コミット

- 宣言 note amendment `8e64ba1c` (Part BQ宣言・blob lock
  a014be5b→5135834e・fetch-back byte一致)。
- A `309386d5` scaffold 73ファイル (scripts 7 + inputs 54 + val-gate
  12)・fetch-back 73/73 blob一致。
- B `32fbe3bb` outputs 75ファイル (status.log・raw 73〔完了31キー62
  本+truncated 10+l035断片1〕・row-audit-winhalt.json)・fetch-back
  75/75一致。
- C (本commit) README + MANIFEST-sha256.txt 148行。
