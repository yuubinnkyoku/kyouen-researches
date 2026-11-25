# Part DV 完了: batch-35 (closure class 16757・rank 7) clean 28キー probe drive 完了log (2026-11-24)

単一オーナー Part DV。宣言
`research/log/2026-11-24-part-dv-batch35-class16757-declaration.md`
(commit `63028eea`・宣言log sha 571d4de2 部位は宣言出版時点のもの)。
**11×11 空盤は UNKNOWN のまま** (本 Part は probe drive のみで、verdict は
1行も canonical cache に消費していない)。

## ドライブ結果 (28/28 キー honest two-pass fresh-cold @ 15M)

drive 21:38:56Z (b021) → 21:51:39Z (b048)。status.log 30行 =
28 PASS verdict行 + 2 WIN-HALT marker行 (EXHAUSTED 0・RETRY 0・MISMATCH 0):

- **26 LOSS** (2-pass node-exact、採用は後続 Part で実施)
- **2 WIN**: b032 `15000000,1,2678305` @21:43:44Z / b048 `15000000,1,3485963`
  @21:51:39Z。ともに pre-registered WIN-HALT marker・honest label・
  **verdict 不消費** (scrutiny owner C++ 第二実装 gate pin `9193f5b6…`
  通過後のみ採用可。本実行環境に C++ コンパイラなしで gate 実行不能は
  本 Part でも再確認済み)
- batch-1 probe-level WIN b018 (`15000000,1,3549602`・2026-11-22) も引続き
  不消費 (batch-35 key set からは除外済み)
- nodes (per-pass): 28キー全体 73,757,659 / 採用26キー 67,593,391
  (両pass合計 147,515,318・nodes は bookkeeping で勝敗ではない)

## kit と出版物 (全て fetch-back byte検証済み・MANIFEST 109 files 自己検証)

`research/experiments/n11-centralreply-closure-class16757-batch35-20261124/`
(MANIFEST self-sha `791996c1ad86…`・109エントリ = input 29 + output/raw 56 +
status.log + batch-audit 1 + scripts 3 + sources 7 + val-gate 12):

- 宣言: `63028eea` / scripts 3: `2ea54d0f` / sources 7: `ff9c08bb` /
  val-gate 8: `c0399036` / input 29: `2d62d4eb`
- outputs: inc1 `fec4063c` (raw b021-b026 12) / inc2 `f19fa6f5`
  (b027-b034 16・b032 WIN node-exact) / inc3 `ba673bfb` (b035-b042 16) /
  inc4 `e4e61897` (b043-b048 6 + status.log 30行 [sha `d7c3b42c…`] +
  val-gate `.dv-host.out` 4)
- wave D: `47dfbb72` (batch-audit.json sha `24a04833…` [26 LOSS + 2 WIN
  honest・EXH/MISMATCH 0] + experiment README `2c4a0d0e…` + MANIFEST)
- 採用者バンク: maker `make_batch35_keys.py` sha `69025eba…` (gates
  G1-G6・3x byte-identical・tamper battery 6/6 + control)
- solver pins: jsreplay.js `84585617…` / runbatch.sh `f591f8c2…` /
  batch-keys-b35.json `d5bd4c89…`
- val-gate: 4 molecule x 2 host (published-baseline + dv-host) node-exact
  (at2m 2m,0 / first-15m 15m,2,3651923 / second-15m 15m,2,5040200)

## 状態と次の作業

- class 16757 (49子境界): unknown 29 → 採用前時点で 28 clean + b018。
  本 Part は probe のみで cache 不変 (BASE 6,547行 `973bcd19…` のまま)。
- 26 LOSS行の canonical adoption は **Part DW** として宣言→kit→outputs→
  reaudit の順で実施する (本 Part の直後に同一セッションで着手)。
- EXHAUSTED 残は 0 (高budget再probe 不要)。WIN 3行 (b018/b032/b048) の
  交叉検証は別 Part (scrutiny gate 実行可環境が前提)。
