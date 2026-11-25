# batch-25: closure class 30565 exact-S5 probe (Part BP, 2026-11-23)

Part BP (宣言: note amendment commit `b54fbdd6`・実行前に出版)。閉包
候補表 (Part BI refresh reaudit `d57a7609…` 807行) の **rank 23 class
30565** (mask [1152921505143717888, 1081344]・groups served
(25,80)(36,41)(36,91)・cost 53子すべてunknown) を対象とする
exact-S5 probe batch。**verdict不消費**。閉鎖・被覆・secured・root
勝敗の主張はしない。

## 選定 (published baseから再導出・prose不使用)

- ranks 1..16 は従来どおり反駁済み (19/20/21-WIN交積またはknown WIN
  子。5830 は receipt WIN 5子・5687 は receipt WIN子 209644・rank 1
  class 23101 の unknown 集合は q042 のみ)。
- rank 17 class 12643 は unconsumed-WIN交積 {115192} (Part BJ a003)。
- rank 18 class 25835 は unconsumed-WIN交積 {150241} (Part BL k002)。
- rank 19 class 31600 は unconsumed-WIN交積 {62435, 192809}
  (Part BN s001/s002)。
- **rank 21 class 16957 (batch-24対象) は今回の反駁証拠が確定**:
  unknown子集合と25-WIN (unconsumed) 集合の交積は厳密に
  {91296, 368510} (published Part BO honest WIN行 y001+y006・2番目の
  WIN-PAIR反駁・verdict不消費)。
- rank 20 class 10968・rank 22 class 23964 は fail-closed overlap gate
  でblocked継続 (batch-24 packetをpriorに加えても衝突ピン不変:
  10968 = {273033} = batch-12 n018・23964 = {495193, 550880} =
  batch-13 p007 + batch-4 e043。NOT route-dead・WIN反駁証拠ゼロ)。
- **rank 25 class 5690 は route-dead** (新事実): update8 receipt WIN子
  {209644} を持つ。よって機械選定は **rank 23 class 30565**。
  runner-up rank 24 class 1849・backup rank 26 class 13342 (両方
  route-alive・交差ゼロ・maker内で機械検証)。

## preflight (fail-closed maker `make_batch25_keys.py` `6b461049…`)

全gate PASS・4回実行byte一致・tamper battery 7/7検出 (T1 graph sha
pin / T2 CLASS_MASK 1bit / T3 batch-24 prior packet pin / T4
prior-rows pin / T5 rank-21 evidence pin 368510→368511 / T6
PKT-collision pin 273033→273034 / T7 rank-25 route-dead known-win
pin 209644→209645)。

- 53キー i001..i053 (s5昇順 68580..903169・legal 76..94・Board再計算
  53/53・membership {4:45, 3:8})。
- canonical cache 6,235行 `f6649fe3…` hits 0/53・quarantine 0/53。
- prior 25 published packets (batches 1..24・1,246行・1,232一意;
  cross-packet重複14位置は membership による正規重複で簿記) overlap
  0・key id prefix "i" は全packetで未使用 (未使用文字は {i, l, o})。
- batch-keys.json `272c0c13…` (schema
  `n11-centralreply-closure-class30565-batch25-input-v1`)。
- 新規gate: 25-WIN集合・rank-21反駁tie (== {91296, 368510})・
  rank-25 route-dead gate (ranked[24] == 5690・known_win ==
  {209644})・EXPECTED_RANKS 25..28拡張 (5690/13342/5343/13758)。

## val-gate (pinned jsreplay `84585617…`・実行host)

4/4 node-exact (wall_s比較外・禁止四角 95,670):
at2m 2キー result 0 / budget 2,000,000 exhaustion・15m基準キー
(2, 3,651,923) と (2, 5,040,200)。published-baselineはbatch-23/24と
同一byte-copy・this-hostは本ホスト再生成。

## drive-1 結果 (宣言commit `b54fbdd6`の事前登録stop rulesどおり)

- **i001 WIN (honest label): replay result 1・two-pass node-exact・
  nodes 13,251,132 (budget 15M内)・key (1152921505277935616,
  1081344)・s5 index 68580・legal 88・membership 4・wall 150/68s** →
  事前登録 WIN-HALT rc=45 (worker1・最初のキー)。
- **i002 WIN (honest label): replay result 1・two-pass node-exact・
  nodes 7,207,180 (budget 15M内)・key (3458764514357411840, 1081344)・
  s5 index 191299・legal 82・membership 4・wall 77/75s** → 事前登録
  WIN-HALT rc=45 (worker2・最初のキー)。両workerの最初のキーがともに
  WINであったためfragmentはゼロ。
- 残り51キー (i003..i053) は fresh UNPROBED (fileless)。
- row-audit-winhalt (schema
  `n11-centralreply-closure-class30565-batch25-rowaudit-winhalt-v1`・
  事前登録版 script `7b61123e…`: completed/fragment/fileless はrawの
  `# replay_done` 有無とstatus.logから導出・haltキーidは一切固定し
  ない): PASS・3回実行byte一致 (json `cc84d1b3…`・derived_state=true)・
  tamper battery 3/3検出 (p1 verdict反転 / 未probeキー i010への偽
  PASS行 / verdict行 i002除去・scratch上で実施し実験filesは無改変・
  clean control PASS)。

## 意味 (route statementのみ)

i001・i002 の2つのWIN行により (採用された場合) **class 30565 の
全LOSS閉包ルートは反駁証拠を持つ** (batch-21..24 と同型の反駁
パターン・同一クラス内で2つの独立WIN子)。ただし verdictは一切消費
していない: i001・i002 は **26番目・27番目の unconsumed closure WIN
候補** で、採用判断は scrutiny owner C++第二実装 gate pin
`9193f5b6…` 待ち (本レーンは代行しない)。canonical cache 6,235行
`f6649fe3…` は read-only・不変。10968・23964 は blocked (packet交差・
NOT route-dead) のまま・5690 は route-dead。次batch選定は次回の
ランが 25+2=27-WIN交積の反駁簿記で行う (rank 24 class 1849
(runner-up)・rank 26 class 13342 (backup) が当面のroute-alive候補)。

## 検証規律

nodes数・expansions数を勝敗として読まない。WIN/LOSS採用は別宣言の
adoption Part (pinned fail-closed merger `90711961`) でのみ。
**標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・
S2 {59,60}・class 1/2/4・class 10968・class 23964・class 16957・
class 30565 (53キーすべて・i001/i002を含む) はどの時点でもUNKNOWNの
まま。**

## 再現

1. `python3 scripts/make_batch25_keys.py` (published pinsをsha検査し
   53キーを再導出・全gate PASSで終了)。
2. `node scripts/jsreplay.js --exact-replay=val-gate/<...>.input.csv
   --exact-replay-budget=2000000|15000000` (val-gate 4件)。
3. `bash scripts/drive_batch25.sh` (残キーを2 worker 260s有界で順次
   2-pass fresh-cold・WIN-HALT rc=45は事前登録)。
4. `python3 scripts/row_audit_batch25_win_halt.py` (halt時点の部分行
   監査・byte一致JSONを再生成)。

## 出版コミット

- A `2cc4a69a` scaffold 73ファイル (scripts 7 + inputs 54 +
  val-gate 12)・fetch-back 73/73 blob一致。
- B `3b1a6283` outputs 6ファイル (status.log・raw 4・
  row-audit-winhalt.json)・fetch-back 6/6 blob一致。
- C (本commit) README + MANIFEST-sha256.txt 79行。
