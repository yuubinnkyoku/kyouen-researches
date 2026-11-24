# Part DA (takeover): batch-29 (closure class 2251) drive-2 ckpt-2/3 LOSS 15行の第三実装交叉検証 — Three-implementation corroboration 15/15 (LOSS)

出典: 原宣言 (Part DA) `88ffdc92` 2026-11-24T02:22:43Z (宣言ノート
`research/log/2026-11-24-part-da-b29d2loss15-thirdimpl-declaration.md`) /
takeover宣言 `f2b36862` 2026-11-24 (規約時刻 05:52:43Z 通過・停滞3.5h超・
対抗宣言なし機械確認・ノート
`research/log/2026-11-24-part-da-takeover-b29d2loss15-thirdimpl.md`)。

## 対象

batch-29 (closure class 2251) の Part CI takeover drive-2
(`n11-centralreply-closure-class2251-batch29-20261123`) で 15M fresh-cold
2-pass 条件により解決した **drive-2 ckpt-2/3 LOSS 15行**
(ab017..ab027 + ab029..ab032・全行 result 2・nodes 合計 63,809,543/pass)。
15行は honest label のまま (**verdict 不消費**)。adoption (canonical cache
merge) は CU 先例の pinned fail-closed merger `90711961…` 経由の別
adoption Part 専権。WIN 行 ab028 は Part CZ `68751fd7` で成立済み
(scrutiny owner C++ gate `9193f5b6…` 通過前は採用不可)・本Part非対象。

**標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・
S2 {59,60}・class 1/2/4・class 2251 (batch-29 54キーすべて・対象15キー含む)
は全時点でUNKNOWNのまま。nodes数・expansions数・ttHits数を勝敗や距離として
読まない。被覆・secured・root勝敗の主張をしない。**

## 構成 (169 files)

- `scripts/` 7: pinned third_impl.js `08ea958f…` / jsreplay.js `84585617…` /
  audit_da.py `ca24423d…` / make_inputs_da.py `2cfe8d32…` /
  run_replica_da.sh `f0b4c6f0…` / run_thirdimpl.sh / verify_tbl.js
  `c8c52528…` (takeover 継承・sha256全pin一致検証済み)。
- `input/` 20: rows.json `8b212fd4…` + targets 15 + anchors 2 (k02a/l1a) +
  negatives 2 (ng1/ng2) CSV (published 正本と byte一致)。
- `sources/`: drive-2 raw p1/p2 30 (PIN_RAW_DA 全件 sha 一致) / status-b29.log
  `b49322d9…` / batch-keys `330c0b9f…` / CU出版物 (merged cache `30ddad9d…`
  6,317行・increment `bab011e3…`・manifest `f9f58ee1…`) / drive-2 宣言・完了log。
- `val-gate/`: published baselines+input 8 + 本host fresh 出力
  `.da-host.out` 4。
- `output/` 72: status.log (REPLICA 30 + RUN 36) / rules-gate.txt /
  replica 30 / targets 30 / anchors 4 / negative 2 / audit-summary.json /
  audit-run1-3.txt。

## 実行protocolの結果 (D1-D8 全green・takeover宣言 f2b36862 のとおり)

- **D1 rules gate**: verify_tbl.js — replica quads 95670 mine quads 95670 /
  triples checked 195044 / mismatches 0 (`output/rules-gate.txt`)。
- **D2 val-gate fresh 4/4 node-exact**: 2M×2 result 0 (budget-exhausted) /
  15M×2 result 2 nodes 3,651,923 / 5,040,200 (published baselines と
  wall_s 以外全field一致・`val-gate/*.da-host.out`)。
- **D3 negatives 2/2 fail-closed**: ng1 "legal count mismatch: derived=87
  declared=88" / ng2 "stone count mismatch: bits=5 declared=6"。
- **D4 anchors 4/4 published pin と node-exact**: k02a a/b WIN expansions
  9,106,337 ttHits 4,991,527 / l1a a/b LOSS expansions 7,660,602 ttHits
  3,951,175 (det-pair a==b)。
- **D5 replica 30/30 pass (15キー×p1/p2)**: 全pass rc=0・budget 15M・
  determinism p1==p2 (legal,st? is_or,budget,result,nodes,lo,hi)・
  published drive-2 raw と node-exact (result 2・nodes 1,835,150〜
  8,695,465・全キー一致)。
- **D6 第三実装 targets 30/30 run clean (15キー×a/b)**: 全run rc=0・det-pair
  a==b (result/expansions/ttHits/reason)・pass-one expansions 合計
  73,293,629 (ab026 2,075,693 〜 ab023 10,104,496)・**verdict 15/15 =
  result 2 で published drive-2 LOSS 行 (replica) と完全一致 =
  three-implementation corroboration 15/15**。WALL-INCONCLUSIVE 0。
- **D7 audit (audit_da.py `ca24423d…`) ×3 byte-identical**: 同一cwd
  PYTHONHASHSEED=random / 1 + 隔離tree `env -i` PYTHONHASHSEED=99 —
  **ALL 429 GATES PASS ×3** (stdout sha256
  `5cef05e33d2690657245d17b1975635b0fd603a559972561ad3d3860480070f6`・
  audit-summary.json `9d21022a…`)
  ・verdict agreements 15/15 (WIN=0 LOSS=15)・G6 unadopted補強 (15キー全員が
  merged cache 6,317行 `30ddad9d…` に row 不在・CU manifest の
  fileless_unprobed_ids roster 在籍・adopted/win/probed 系 id list 全不在)
  を機械担保。
- **D8 出版**: B1 `fd7024a4` (32) → B2 `33d746ca` (36) → B3 `4ba20863`
  (4) → B4 `77eecd66` (4) → C 本README + MANIFEST-sha256 → 完了log。
  全 fetch-back byte 一致検証済み。

## batch-29 第三実装交叉検証の全体状況 (本Part完了後)

- drive-1 ckpt-1/3 16行 (ab001..ab016): Part CV `3b6ad066` (CU 採用16行)
  corroboration 済み。
- drive-2 WIN 1行 (ab028): Part CZ `68751fd7` 成立済み。
- drive-2 ckpt-2/3 15行: **本Part (DA takeover)** で成立。
- drive-2 ckpt-3/3 22行 (ab033..ab054): Part DC `488f61f4` 成立済み。
- 以上で batch-29 54キー (LOSS 53 + WIN 1) の第三実装交叉検証が全行成立。
  ただし verdict は不消費: 採用は別 adoption Part (pinned merger
  `90711961…`) / WIN ab028 は scrutiny owner C++ gate `9193f5b6…` 通過後
  のみ。

## verdict不消費の言語 (AGENTS.md / SCHEMA.md 準拠)

本READMEの数値はいかなる意味でも勝敗確定・閉鎖・被覆ではなく、制御された
再実行・交叉検証の記録である。
