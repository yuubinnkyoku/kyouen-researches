# Part DA takeover宣言: batch-29 (class 2251) drive-2 ckpt-2/3 LOSS 15行 (ab017..ab027+ab029..ab032) 第三実装交叉検証 (2026-11-24)

単一オーナーtakeover宣言・publish-then-execute (Part CX先例 `c48aa56b` と同一規約)。
observed HEAD `9abe5e66` (Part DG B outputs・2026-11-24T05:46:48Z。停滞確認
走査時点のHEADは `33cb9306`・05:31:21Z・両時点で本実験dirへの新commitなし)。

## takeover 事由の機械確認

- 原宣言: `88ffdc92` (単一オーナー宣言・2026-11-24T02:22:43Z) —
  対象は Part CI takeover drive-2 ckpt-2/3 LOSS 15行 (budget 15M・全行
  result 2・nodes 63,809,543/pass合計) の pinned第三実装
  `third_impl.js` `08ea958f…` 交叉検証 + 本host pinned-replica
  `jsreplay.js` `84585617…` 2-pass fresh-cold (runner `f0b4c6f0…`) +
  Part CU出版物 unadopted 補強 G6。
- scaffold A 完結: `267fec1a` (A 1/3 scripts+input・02:23:04Z) →
  `9e0d71be` (A 2/3 sources・02:23:16Z) → `c5ccfbd3` (A 3/3 raw+val-gate・
  02:23:28Z・計92 file kit complete)。
- 以降の実験dir (`research/experiments/n11-centralreply-closure-b29d2loss15-thirdimpl-20261124/`)
  への commitは**皆無** (observed HEAD `33cb9306` 時点で 02:23:28Z から
  3時間超停滞)・output/ 未出版・D1-D8 未実施。
- earliest_takeover = 原宣言時刻 + 3.5h = 2026-11-24T05:52:43Z を通過。
  直近12 commit (`33cb9306`→`9abe5e66`) を機械走査し、(a) 本実験dirへの
  新commit、(b) 対象15キー (batch-29 drive-2 ckpt-2/3 LOSS) の第三実装
  交叉検証を宣言した対抗レーン・takeover宣言、のいずれも存在しない
  ことを確認 (`9abe5e66` は Part DG B (batch-28 P3・aa*キー) のoutputs
  出版で非接触)。
- 原宣言sessionは長期レーンの別実行 (本takeover実行者は原宣言と別の
  長期レーン定期実行)。原宣言の対象・protocol・pinを一切変更せず継承。

## kit復元とpin検証 (takeover着手時に実施・solver未実行)

published scaffold (commit pin `267fec1a`/`9e0d71be`/`c5ccfbd3`) から
92ファイルを raw fetch し、sha256照合:

- 宣言pin一致 (7点): rows.json `8b212fd4…`・make_inputs_da.py
  `2cfe8d32…`・audit_da.py `ca24423d…`・third_impl.js `08ea958f…`・
  jsreplay.js `84585617…`・run_replica_da.sh `f0b4c6f0…`・verify_tbl.js
  `c8c52528…`。
- rows.json sources pin一致 (7点): batch-keys `330c0b9f…`・status-b29.log
  `b49322d9…`・drive1 prefix `6b877344…`・completion log `46c461bd…`・
  merged cache (CU) `30ddad9d…` (6,317行)・increment `bab011e3…`・
  increments-manifest `f9f58ee1…`。
- input CSV 15件が sources/published-input/ と byte一致・
  anchors/negatives 4件が published-input-bf/ と byte一致。
- D1 rules gate 用 knowledge lane-kit
  `/home/user/knowledge/kyouen-research/_class1297036830122704896-lane-kit/inv/jsreplay.js`
  のsha256が `84585617…` と一致 (verify_tbl.js `c8c52528…` の参照path)。
- maker再実行はしない: input/rows.json は published pin `8b212fd4…` と
  一致検証済み・audit G0 (rows.jsonとの整数完全一致) と G1 (script pin)
  が機械gateするため (CX takeoverと同一扱い)。

## 継承protocol (原宣言から変更なし・再掲)

- D1 rules gate (pinned `verify_tbl.js`): output/rules-gate.txt
  (期待: replica quads 95670 mine quads 95670・mismatches 0)。
- D2 val-gate fresh 4 (本host・published baselines node-exact・wall_s
  比較外・出力は `val-gate/*.da-host.out`)。
- D3 negatives ng1 (legal+1) / ng2 (stones 6) GATE_FAIL設計どおり。
- D4 anchors k02a/l1a 各a/b (published値 node-exact: k02a WIN expansions
  9,106,337・ttHits 4,991,527 / l1a LOSS expansions 7,660,202・ttHits
  3,951,175)。
- D5 replica 15キー×p1/p2 (runner `run_replica_da.sh`・budget 15M・
  inner timeout 260・determinism p1==p2・published raw fields node-exact)。
- D6 targets 15キー×a/b第三実装 (cap 300M・wallcap 240・memo-power 22)。
  WALL-INCONCLUSIVE は誠実記録し勝敗とは読まない (audit G5設計)。
- D7 audit `audit_da.py` ×3 byte-identical (schema
  `n11-centralreply-closure-b29d2loss15-thirdimpl-audit-v1`。
  2走は同一cwdでPYTHONHASHSEED=random/1・1走は隔離tree+`env -i`+
  PYTHONHASHSEED=99) + audit-summary.json 出版。
- D8 出版: B1 output/ (status.log / rules-gate.txt / audit-summary.json /
  audit run1-3 / replica 30 / targets 30 / anchors 4 / negative 2) →
  B2 val-gate host 4本 (`.da-host.out`) → C README.md + MANIFEST-sha256
  (全file fetch-back byte一致) → 完了log。全push直前に最新main再取得・
  競合時は無理押しせず記録して次回へ。

## verdict不消費・非接触 (原宣言の担保を全部継承)

- 15行はhonest labelのまま・adoption/解放/閉鎖/被覆/root勝敗の主張を
  しない。採用はCU先例のpinned merger `90711961…` 経由の別adoption Part
  専権。WIN行 ab028 はPart CZ `68751fd7` 成立済み・scrutiny owner C++
  gate `9193f5b6…` 通過前は採用不可・非接触。
- canonical merged cache 6,317行 `30ddad9d…` は読みのみ (G6 pin対象)。
- 長時間探索・driveは行わない (本Partは交叉検証と監査のみ)。
- 並走非接触: Part DF (batch-28 P2・aa*キー)・Part DG (batch-28 P3・aa*キー)・
  K1282 (fast lane完了)・batch-30/31レーン (class 34269/5804)・queue
  registry (batch-28 WIN46) は対象キー・実験dir完全分離。
- **標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・
  S2 {59,60}・class 1/2/4・class 2251 (batch-29 54キーすべて・対象15キー
  含む) は全時点でUNKNOWNのまま。nodes数・expansions数・ttHits数を勝敗や
  距離として読まない。被覆・secured・root勝敗の主張をしない。**
