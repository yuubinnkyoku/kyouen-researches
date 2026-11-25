# Part CZ 完了: batch-29 (class 2251) drive-2 WIN 1行 ab028 の第三実装交叉検証 — three-implementation corroboration 成立 (verdict不消費) (2026-11-24)

実験dir `research/experiments/n11-centralreply-closure-b29ab028win-thirdimpl-20261124/`。
宣言 `research/log/2026-11-24-part-cz-b29win-thirdimpl-declaration.md`
(commit `4c741798`・observed HEAD `39f29652`) → A kit 36 files
(`161373f9`・fetch-back 36/36) → D1-D7 実行 → B outputs 17 files
(`66baba24`・fetch-back 17/17) → C README + MANIFEST-sha256 (`66943fbc`)。
**verdict不消費**: ab028はhonest labelのまま・adoptionはscrutiny owner
C++第二実装 gate `9193f5b6…` 経由の別adoption Part専権。

## 対象

- **ab028**: key (1297036830121656320, 131074)・s5 93815・legal 80・
  membership 3・published Part CI takeover drive-2 result **1 (WIN)**・
  nodes **3,167,121** (2-pass node-exact・status-b29.log 55行中の
  WIN-HALT対象キー・budget 15M)。

batch-29で初の第三実装交叉検証 (Part CV はckpt-1/3 LOSS 16行
ab001..ab016のみ・ab028は未カバーだった)。

## 結果 (全てnode-exact・audit `audit_cz.py` `3c95e32f…` 79/79 GATES
PASS ×3 byte-identical・verdict agreements 1/1・inconclusive 0)

- **D1 rules gate PASS**: replica quads 95,670 == third-impl quads
  95,670・triples checked 195,044・mismatches 0。
- **D2 val-gate fresh 4/4 node-exact** (at2m×2 result 0 / nodes 2,000,000・
  15m×2 result 2 / nodes 3,651,923・5,040,200)。
- **D3 negatives 2/2 GATE_FAIL設計どおり** (legal+1 / stones 6)。
- **D4 anchors 4/4 node-exact**: k02a WIN (expansions 9,106,337・ttHits
  4,991,527)・l1a LOSS (7,660,602・3,951,175)・a/b det-pair一致。
- **D5 本host pinned-replica 2-pass fresh-cold (budget 15M)**: ab028
  p1/p2 = result 1・nodes **3,167,121** (wall 15/16s)・published drive-2
  raw fieldsとnode-exact一致。
- **D6 第三実装 (非df-pn AND/ORミニマックス) a/b 2-run**: ab028
  result **1 (WIN, clean)**・expansions **3,595,562**・ttHits 2,114,848
  (wall 10.54/10.90s)・det-pair一致。
- **three-implementation corroboration成立**: published drive-2 host
  2-pass (result 1 / nodes 3,167,121) + 本host pinned-replica 2-pass
  (result 1 / nodes 3,167,121) + 第三実装 minimax 2-run (result 1)。
  3実装すべてverdict WIN一致・DIVERGENCE 0。
- **D7 audit 79/79 GATES PASS ×3 byte-identical** (audit-summary.json
  `c618767a…`)。G6 unadopted補強: CU merged canonical cache `30ddad9d…`
  (6,317行) pin一致・ab028のs5verdict row 0行 (採用されていない)・同key
  競合rowゼロ・CU manifest (increment `bab011e3…` 16行・manifest
  `f9f58ee1…`) 上でab028はfileless_unprobed_ids (38キー) にのみ存在。

## 誠実記録

- 宣言前にaudit `audit_cz.py` を合成データkit上でスモークテストし、
  79 gate PASS ×3 byte-identical + tamper電池10/10 fail-closed検出を
  確認済み (宣言に開示)。この過程で malformed third行がtracebackクラッシュ
  する弱点を発見し、fail-closed名前付きgateとして処理するよう修正
  (`3c95e32f…` が修正後のsha・宣言のpinと一致)。
- maker tamper電池 8/8検出 (efficacy-asserted・宣言に開示)。
- D5 runnerの外側終了コードが成功時もrc=1 (`[ "$RC" -ne 0 ] && exit "$RC"`
  の短絡評価・published CW runnerと同一の既知クセ)。per-pass rc=0は
  status.log記録どおり。
- D2 at2m 2本目のhost出力はwall_s=9がpublished baselineと同整数秒の
  ためfile byteが一致 (正当な一致・CW時と同一事象)。

## これにより確定したこと・していないこと

- 確定: ab028のWIN verdictが (df-pn jsreplay + 第三実装minimax + published
  host) の3実装で一致 (nodes含む決定 fieldすべて再現)。batch-29全54キーの
  probeは完了 (LOSS 53・WIN 1・EXHAUSTED 0)。
- 未確定: ab028のcanonical adoption (scrutiny owner C++ gate経由の別Part)・
  class 2251のclosure構成・secured coverage・root勝敗。
- **標準11×11空盤・19 central-reply roots・class 2251・全バッチキーは
  この時点で UNKNOWN**。nodes数・expansions数を勝敗や距離として読まない。

## 並走 (非接触)

Part CP takeover (batch-30・`87e19b5a`)・Part CY drive-2 (batch-31・
`21fef631`)・Part CX (batch-28 CQ WIN 5行・`1300c10d`)。いずれも対象キー・
class・バッチが全く別。Part CZの実行中に CY/CP の3 commitを観測したが
競合なし (pushは全てfast-forward成功・fetch-back検証済み)。
