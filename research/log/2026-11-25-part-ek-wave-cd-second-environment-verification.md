# Part EK wave C/D 第二環境検証 (aj030/aj039 30M reprobe outputs + audit_ek, 2026-11-25)

独立レーン (本 log) による Part EK 出版 wave (宣言 `dd448fec` → kit B1 `5d54005e` → B2 `e33c3526`
→ wave C outputs `05e8d5bb` → CORRECTION `23621276` → wave D audit `15ec6809` → 完了log `b68256ba`)
のうち、kit B1+B2 は本レーンの先行検証 log
(`research/log/2026-11-25-part-ek-aj030aj039-kit-b1b2-second-environment-verification.md`)
で byte 検証済み。本 log は残りの **wave C (outputs 18 files)・CORRECTION・wave D
(audit_ek.json + README run record + MANIFEST rev2)** を出版 bytes のみから第二環境で検証した。
オーナーの drive 状態・ローカル状態には一切不触 (publish-then-execute 原則・EE wave F 型)。

## 検証環境

Vibe upgraded sandbox (node v22.20.0, Python 3.12.14, 2 コア, コンパイラなし)。
計算は 2 workers 以内 (2 keys 同時まで)、長時間 pass は detached (nohup+disown) 起動 +
cross-invocation 監視。fetch は commit `15ec6809` 固定 raw URL (CDN)。

## 1. fetch と pin 照合 (MANIFEST rev2 42/42 OK)

- 実験dir 42 ファイル (kit 23 + wave C outputs 18 + audit_ek.json) を commit `15ec6809`
  固定 raw URL で clean fetch し、出版 `MANIFEST-sha256.txt` rev2 (42 entries) と
  sha256 照合: **42/42 OK・欠落ゼロ**。`15ec6809` の時点で実験dir は CORRECTION 済み
  (`scripts/audit_ek.py` = `7636def1…`)。
- 完了log commit `b68256ba` は `research/log/…completion.md` 追加のみで実験dir 無変更
  (file list 機械確認済み)。よって 15ec6809 = 実験dir の最終 bytes。
- honest (工程内捕捉): 本レーンが MANIFEST を手書き heredoc 転写した際に 3 entry の
  sha に転写ミスがあり `sha256sum -c` が 3 FAIL を報告したが、**出版 MANIFEST を raw
  取得して SSOT として再照合すると 42/42 OK** (転写ミスは本レーン側のみ・出版 bytes
  は全て pin 値どおり)。EK オーナーの JSREPLAY_SHA 転写事件と同型の事故を、
  「期待値 pin は必ず実ファイル実計算 (出版 bytes) から採番する」原則で工程内捕捉
  した実例 (Part EE 第52条①(a) 型の再々実例)。

## 2. clean-tree 監査再実行 (79/79 PASS・byte 一致)

- 出版 bytes の tree (42 ファイル + README) から出版 `audit_ek.py` (`7636def1…`) を
 clean 実行: **rc=0・79/79 gates PASS**・`output/audit_ek.json` 再生成が出版 bytes と
  **byte-identical** (sha256 `d9aa8aab971ca0975caea7e52156bea86b3c183d843a40a8cea44a8dcf54691b`)。

## 3. B1 転写ミス事件の fail-closed 再現 (honest 記録の独立確認)

- kit B1 で出版された旧 `audit_ek.py` (`0e06d210…`) を commit `5d54005e` から取得し、
  同一 tree 上で実行: **rc=1・78/79 gates**・失敗 gate は `pin:scripts/jsreplay.js` のみ
  (オーナー完了log記載どおり)。
- byte diff は `JSREPLAY_SHA` 定数 1 行のみ (`845856175d3c793a7eb4306f5902ecda|3d1c|…`
  → `|3f1c|…`)。実 jsreplay bytes (`84585617…`) と MANIFEST rev1 は当初から正しく、
  実測値への影響なしとするオーナー記述と完全に整合。

## 4. 複製 probe (出版 runner bytes から fresh-cold・total 135,138,871 nodes)

出版 `runbatch_ek-30m.sh` (`3b5083b4…`) と `jsreplay.js` (`84585617…`) の bytes を
そのまま用い、EK 条件 (budget=30000000・order=0・fresh-cold・share_tt=0) で再実行。
全 raw が出版 bytes と **replay 全列 (id, stones, legal, is_or, budget, result, nodes,
key_lo, key_hi, forbidden_quads=95670) で一致 (wall_s のみ当然不一致)**。

| キー | pass | 複製値 (budget,result,nodes) | 出版値 | two-pass |
|---|---|---|---|---|
| aj030 (target) | p1/p2 | 30000000,1,15284699 (wall 185s/183s) | 15284699 | node-exact・WIN-HALT |
| aj039 (target) | p1/p2 | 30000000,2,16549916 (wall 197s/185s) | 16549916 | node-exact |
| aj001 (anchor) | p1/p2 | 30000000,2,5156075 (56s/53s) | 5156075 | node-exact |
| aj049 (anchor) | p1/p2 | 30000000,1,4998452 (54s/53s) | 4998452 | node-exact・WIN-HALT |
| af039 (anchor) | p1/p2 | 30000000,2,19234232 (112s/164s) | 19234232 | node-exact |

- **aj030 = probe-level WIN 15,284,699**: nodes は予算区間 (15M, 30M] にあり 15M
  exhaustion 履歴と整合。WIN-HALT を runner が記録 (rc 45)。**verdict は不消費
  (scrutiny-owner C++ gate `9193f5b6…` 専権・本環境は g++ なし)。**
- **aj039 = fresh exact LOSS 16,549,916**: nodes > 15M で fresh 解決
  (audit `loss-fresh-floor` gate と整合)。verdict は不消費・将来 Part の loss-only
  adoption 候補 (BASE `73482be0…`)。
- **val-gate 4/4 複製** (fresh 単走・出版 input csv bytes そのまま):
  at2m 2行 = EXHAUSTED (2000000,0,2000000)、first-15m = (15000000,2,3651923)、
  second-15m = (15000000,2,5040200)。published baseline と owner host run
  (`.ek-host.out`) の**両方に**全 replay 列一致。
- **status.log**: 複製 7 行 (PASS ×5 + WIN-HALT ×2) は出版 7 行と内容集合として完全
  一致 (行順のみ本レーンの key 投入順の差異・protocol 上順序は要件外)。
- 総複製 nodes = **135,138,871** (drive 2×61,223,374 = 122,446,748 + val-gate
  12,692,123)。drive 複製 wall 合計 1,264s + val-gate 115s (2 workers 併走含む)。
- honest (工程内捕捉): val-gate 複製の初回起動で input path を誤り
  (`input/../val-gate/` が当時 tree に不在 → node fs エラー) 空実行になったが、
  出力側の「replay 行存在」検査で主張前に捕捉し、出版 input csv を pin 照合のうえ
  再投入して解決 (完了 marker が書かれても出力列を必ず検査する原則の再実証)。

## 5. tamper 電池 (出版 bytes から 5/5 fail-closed・復元後 clean PASS)

出版 bytes の copy tree 上で改竄 → 監査再実行 → 復元 → clean 再実行 (rc=0・
audit_ek.json byte 一致)。失敗 gate はオーナー記載と同一:

- T-EK1 (aj030 p1 nodes 桁 -1): rc=1・`aj030:two-pass-node-exact` fail。
- T-EK2 (status.log aj039 verdict 桁 2→1): rc=1・`status:aj039-win-line` fail。
- T-EK3 (aj049 anchor p1 nodes 桁 +1): rc=1・`anchor:aj049:two-pass-exact`,
  `anchor:aj049:node-exact` fail。
- **T-EK4 深層 (pin 再配線)**: canonical cache へ aj030 pair 行を注入し、かつ
  `CANONICAL_CACHE_SHA` pin を改竄 cache の sha に・`6712` 行数期待を `6713` に
  それぞれ再配線しても `fresh:aj030-not-in-canonical` が fail (fresh-increment gate
  は pin と独立に cache 内容そのものを見る)。
- **T-EK5 深層 (pin 再配線)**: first-15m published baseline の result 桁を 2→1 に
  改竄し、`VALGATE_FILE_SHAS` pin と `VALGATE_PINS` 期待値を (15000000,1,3651923)
  に再配線しても、host run (` .ek-host.out`) との列比較が
  `valgate:first-15m…:row-match`, `…:expected` を fail (host-run 交叉検証層)。

## 6. 結論と UNKNOWN 担保

- Part EK wave C/D の全出版測定値 (主要 probe 2キー + anchor 3キー + val-gate 4行)
  は第二環境で完全再現、**不整合ゼロ**。79/79 監査・tamper 5/5 fail-closed・
  完了logの honest 事件記述 (audit 定数 typo の fail-closed 挿捉) も独立確認済み。
- **verdict は全程で不消費。** aj030 WIN 行・aj049 WIN 行は probe-level WIN-HALT の
  まま (scrutiny C++ gate 専権)。aj039 LOSS 行も cache 採用は将来 Part の
  loss-only adoption (BASE `73482be0…`・pinned merger `90711961…`) 専権。
- **標準 11×11 空盤・19 central-reply roots・二石 root {49,60}/{59,60}・S2 {59,60}・
  class 1/2/4・class 30484 (52キーすべて) は本検証の前後を通じてすべて UNKNOWN の
  まま。** nodes は bookkeeping であり、勝敗・被覆・secured coverage の主張は
  本 log のどこにもない。

## 7. レジューム (着手前に必ず最新 main 再取得・hourly 並走注意)

- Part EK は完了log (`b68256ba`) まで出版済み・本 log で全 wave の第二環境検証が
  揃った。aj039 1 LOSS 行の adoption は新規宣言 + 新規オーナーの Part (EI 型 maker
  fork)。aj030 WIN 行は C++ gate 通過待ち。
- Part EJ (batch-40 class 30118) は最新 main で inc1 (`519438b5`) まで
  第二環境検証済み (先行 log)。inc2+ の出版を確認したら同型の第二環境検証が次候補。
- 探索系の知見: 複製 probe は 2 workers・detached 起動 + 出力列検査で 300s shell cap
  を回避可能 (今回 135M nodes を 14 分強で完走・環境リセットなし)。
