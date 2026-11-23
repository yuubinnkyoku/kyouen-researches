# batch-24: closure class 16957 exact-S5 probe (Part BO, 2026-11-23)

Part BO (宣言: note amendment commit `2c91e033`・実行前に出版)。閉包
候補表 (Part BI refresh reaudit `d57a7609…` 807行) の **rank 21 class
16957** (mask [1152921504606978048, 264]・groups served
(15,70)(48,53)(48,103)・cost 53子すべてunknown) を対象とする
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
- **rank 20 class 10968 は fail-closed overlap gate (本batch新規gate
  `PKT_COLLISION_SKIPS`) で blocked**: published packetとの1点交差
  s5 273033 = batch-12 (class 8106) key n018 (declared-but-unprobed・
  batch-12はn005/n006 WIN-HALTのためn018のrawは存在しない)。ただし
  これは evidence欠損であって **NOT route-dead・WIN反駁証拠ゼロ**
  (UNKNOWNのまま)。
- **rank 22 class 23964 も同gateでblocked**: 2点交差 s5 495193 =
  batch-13 (class 16930) key p007・s5 550880 = batch-4 (class 16371)
  key e043 (両方 declared-but-unprobed)。
- よって機械選定は **rank 21 class 16957** に移行 (cost 53子すべて
  unknown・known children {}・23-WIN交積空・packet交差ゼロ)。
  runner-up rank 23 class 30565・backup rank 24 class 1849 (両方
  route-alive・交差ゼロ・maker内で機械検証)。

## preflight (fail-closed maker `make_batch24_keys.py` `130b76dd…`)

全gate PASS・4回実行byte一致・tamper battery 7/7検出 (T1 graph sha
pin / T2 CLASS_MASK 1bit / T3 batch-23 prior packet pin / T4
prior-rows pin / T5 rank-19 evidence pin 192809→192810 / T6
PKT-collision pin 273033→273034 / T7 graph実ファイル末尾1bit)。

- 53キー y001..y053 (s5昇順 91296..561493・legal 75..95・Board再計算
  53/53・membership {2:3, 3:10, 4:40})。
- canonical cache 6,235行 `f6649fe3…` hits 0/53・quarantine 0/53。
- prior 24 published packets (batches 1..23・1,193行・1,179一意;
  cross-packet重複14位置は membership による正規重複で簿記) overlap
  0・key id prefix "y" は全packetで未使用。
- batch-keys.json `486858d6…` (schema
  `n11-centralreply-closure-class16957-batch24-input-v1`)。

## val-gate (pinned jsreplay `84585617…`・実行host)

4/4 node-exact (wall_s比較外・禁止四角 95,670):
at2m 2キー result 0 / budget 2,000,000 exhaustion・15m基準キー
(2, 3,651,923) と (2, 5,040,200)。

## drive-1 結果 (宣言commit `2c91e033`の事前登録stop rulesどおり)

- **y001 WIN (honest label): replay result 1・two-pass node-exact・
  nodes 5,291,064 (budget 15M内)・key (10376293541461753856, 264)・
  s5 index 91296・legal 87・membership 2・wall 53/53s** → 事前登録
  WIN-HALT rc=45 (worker1・最初のキー)。
- **y006 WIN (honest label): replay result 1・two-pass node-exact・
  nodes 5,321,639 (budget 15M内)・key (1152921504607043584, 264)・
  s5 index 368510・legal 84・membership 2・wall 51/45s** → 事前登録
  WIN-HALT rc=45 (worker2・y002/y004完了後3番目)。
- y002 LOSS (adoption candidateのみ): result 2・nodes 217,944・key
  (1153484454560399360, 264)・s5 166253・legal 81・membership 3。
- y004 LOSS (adoption candidateのみ): result 2・nodes 632,091・key
  (1152921779484884992, 264)・s5 272083・legal 83・membership 3。
- 残り49キー (y003, y005, y007..y053) は fresh UNPROBED
  (fileless・fragmentゼロ)。
- row-audit-winhalt (schema
  `n11-centralreply-closure-class16957-batch24-rowaudit-winhalt-v1`・
  事前登録版 script `fdebf219…`: completed/fragment/fileless はrawの
  `# replay_done` 有無とstatus.logから導出・haltキーidは一切固定し
  ない): PASS・3回実行byte一致 (json `9d073038…`・derived_state=true)・
  tamper battery 3/3検出 (p1 verdict反転 / 未probeキー y010への偽
  PASS行 / verdict行 y006除去・scratch上で実施し実験filesは無改変・
  clean control PASS)。

## 意味 (route statementのみ)

y001・y006 の2つのWIN行により (採用された場合) **class 16957 の
全LOSS閉包ルートは反駁証拠を持つ** (batch-21/22/23 と同型の反駁
パターン・同一クラス内で2つの独立WIN子)。ただし verdictは一切消費
していない: y001・y006 は **24番目・25番目の unconsumed closure WIN
候補** で、採用判断は scrutiny owner C++第二実装 gate pin
`9193f5b6…` 待ち (本レーンは代行しない)。y002・y004 のLOSS行も
adoption candidates (別宣言の adoption Part・pinned fail-closed
merger `90711961` 経由のみ)。canonical cache 6,235行 `f6649fe3…`
は read-only・不変。10968・23964 は blocked (packet交差・NOT
route-dead) のまま。次batch選定は次回のランが 23+2=25-WIN交積の
反駁簿記で行う (rank 23 class 30565・rank 24 class 1849 が
route-alive候補)。

## 検証規律

nodes数・expansions数を勝敗として読まない。WIN/LOSS採用は別宣言の
adoption Part (pinned fail-closed merger `90711961`) でのみ。
**標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・
S2 {59,60}・class 1/2/4・class 10968・class 23964・class 16957
(53キーすべて・y001/y006を含む) はどの時点でもUNKNOWNのまま。**

## 再現

1. `python3 scripts/make_batch24_keys.py` (published pinsをsha検査し
   53キーを再導出・全gate PASSで終了)。
2. `node scripts/jsreplay.js --exact-replay=val-gate/<...>.input.csv
   --exact-replay-budget=2000000|15000000` (val-gate 4件)。
3. `bash scripts/drive_batch24.sh` (残キーを2 worker 260s有界で順次
   2-pass fresh-cold・WIN-HALT rc=45は事前登録)。
4. `python3 scripts/row_audit_batch24_win_halt.py` (halt時点の部分行
   監査・byte一致JSONを再生成)。

## 出版コミット

- A `d7ee67c7` scaffold 73ファイル (scripts 7 + inputs 54 +
  val-gate 12)・fetch-back 73/73 blob一致。
- B `18420555` outputs 10ファイル (status.log・raw 8・
  row-audit-winhalt.json)・fetch-back 10/10 blob一致。
- C (本commit) README + MANIFEST-sha256.txt 83行。
