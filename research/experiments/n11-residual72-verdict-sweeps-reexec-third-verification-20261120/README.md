# n11 残余72行 4掃引depth-10全probe再実行第二検証（K1144）のpristine再実行第三検証（2026-11-20）

K1144（残余72行 4掃引 K1086 greedy23・K1089 replace16・K1091 replace15・K1095 replace12
のdepth-10 probe計132件全件をpinned runner v17で再実行した独立第二検証・
出版 commit `c84e2b0e`）について、出版後の第三者が**出版byteのみを起点として**機械を
pristine再実行し、132 probe × 2 pass の再実行宇宙が出版正本から完全再現できることを
確定した。単一オーナー宣言ノート
`research/log/2026-11-20-n11-residual72-verdict-sweeps-reexec-third-verification-single-owner-note.md`
（commit `9b3807a310a53285fa7d2799bd819290e52b3168`・2026-11-20T16:2xZ・先行出版）。

## 宣言ノートの転写訂正

宣言ノート本文の出版監査SHA-256に1文字転写があった
（`…8b3750596637`、正 `…8b3350596637` =
`6297c646c32a0b1e0643f9f727fe712d1135dad15c0f5b0418ba8b3350596637`・実byte再計算確定）。
宣言原文は保持し、訂正を本README・item・研究logに記録する（K1151の先例と同じ扱い）。
検証自体はharnessのfail-closed pin（実byte由来）で行うため転写は探索に影響しない。

## 入力の再取得とpin（14 pin）

出版byte 16ファイルをGitHub raw（main）から取得しSHA-256/git-blobを機械照合した。

| 対象 | SHA-256 / blob | bytes |
| --- | --- | --- |
| 第二検証機 `verify_sweeps_reexec_20261120.py` | `7f0729840a3cd6c8f3010cc16de4c5e9d8f19e8f81fa0b1687e64b9a0e8f0228` | 27,091 |
| `runner_v17.ts` | `192903714b1b06a8ea58aa80e22da23fcf9d9ef175830a65a0da5eb0ca64f3d4`（git blob `c132cc6425eee3feaeef1d697dd74f968cfedb59`） | 12,481 |
| 出版passA JSONL | `1ade916b06f887c622449613f068f99bd2bf93404527a397ee2438c0f22f6f12` | 57,079 |
| 出版passB JSONL | `e351f6cc64eca23f1b68d1811a65779e20d1ab727f0ac48e9c4a7b3624845897` | 57,085 |
| 出版assemble監査 | `6297c646c32a0b1e0643f9f727fe712d1135dad15c0f5b0418ba8b3350596637` | 7,327 |
| K1086 greedy23 record/JSONL | `3045e152…` / `773fef42…` | 21,835/27,054 |
| K1089 replace16 record/JSONL | `808fbda1…` / `75fda6ad…` | 17,511/18,808 |
| K1091 replace15 record/JSONL | `edd7ac84…` / `47165331…` | 17,963/17,633 |
| K1095 replace12 record/JSONL | `335eca5e…` / `89e2c30d…` | 16,605/14,105 |

全14 pin一致（機・ランナーSHA・ランナーblob・passA/passB・監査・4掃引record 4・4掃引JSONL 4）。

## pristine再実行（4回・各132 probe）

第二検証機本体のrunコマンド（`run 240 --pass {A,B}`・resume-safe・worker 4）を
演出上加改変なしに1パス1コマンドで実行した（実行環境の1コマンド300秒上限対策で
パス分割はしても機械への引数は出版プロトコルどおり budget 240）。

| run | 環境 | 結果 | 所要 |
| --- | --- | --- | --- |
| runA | 同一tree・同一cwd（pass A） | 132/132 ok, err 0, remaining 0 | 114.9s |
| runB | 隔離tree複製+別cwd（/tmp）+隔離HOME（pass B） | 132/132 ok, err 0 | 114.1s |
| runC | 同一tree・`PYTHONHASHSEED=random`（pass A） | 132/132 ok, err 0 | 112.3s |
| runD | 同一tree・`PYTHONHASHSEED=0`（pass A） | 132/132 ok, err 0 | 109.9s |

4 runとも全132 probeで出版記録とnodes・loss・capped・terminalStoneRange（とpilot_d6
control nodes 3,402×132）が完全一致・nodes総計 37,454,794・`error`/`timeout`/`capped` 0。
ただしmachineのrun出力JSONLはprobeごとに`wall_s`（実行秒）を含むため、run出力のbyteは
タイミングにより変わる規格（第二検証の出版passA/passB JSONLも同様）。byte再現の正本は
assemble出力の監査JSON（下記）。

## assemble正本のbyte再生（3 pair）

第二検証機をassemble modeで自前のfresh run に対して実行した。

| pair | returncode | 出力SHA-256 | 出版監査byte一致 |
| --- | --- | --- | --- |
| runA × runB | 0 | `6297c646c32a0b1e0643f9f727fe712d1135dad15c0f5b0418ba8b3350596637` | ✅ byte-identical |
| runC × runB | 0 | 同上 | ✅ byte-identical |
| runD × runB | 0 | 同上 | ✅ byte-identical |

`gates: 6/6 pass`・fresh nodes total 37,454,794 == published。**出版後の第三者が
出版byteだけから全264 probe再実行をやり直し、assemble監査正本をbyte単位で再生できた。**

## tamper gate（fail-closed・2件）

| 変異 | 対象 | 結果 |
| --- | --- | --- |
| 1 byte XOR 0x01（offset 500） | K1086 record JSON | exit 1・`k1086_greedy23 record json sha256 pin FAIL`・probe起動前に捕捉・記録未書込（改変後SHA `83520f33df362ebf…`） |
| 1 byte XOR 0x01（offset 300） | K1095 probe-records JSONL | exit 1・`k1095_replace12 probe-records jsonl sha256 pin FAIL`・記録未書込（改変後SHA `b6cf0f8601c7d635…`） |

## harness仕様

`scripts/verify_k1144_reexec_third_20261120.py`（stdlibのみ・ネットワーク不使用・fail-closed・
乱数・時刻・絶対path出力なし・SHA-256 `990977e5143bc6fd…`・16,729 bytes）。4 gate:

1. input-pin-gate: 14 pin（上記）のfail-closed照合。harness自身も出版実byte由来pinではじめにrejectする（初版でrunner ts pin定数の転写誤りを実行前捕捉した）。
2. fresh-run-semantic-gate: fresh-runs/ 4 run × 132 recordを決定論的field投影
   （label/root/ordering/depth/bit/child/cap/timeout・result nodes/loss/capped/
   terminalStoneRange・pilot_d6 control）で出版passA/passBと全件比較
   （`wall_s`は構造的にタイミング依存なので比較対象から除外・同時に欠落チェックは実施）。
3. assemble-canonical-byte-gate: tmp stageに機+runnerを複製し、3 pairのassembleを実行、
   出力が出版監査 6,297c646… とSHA・byte両方で一致。
4. tamper-fail-closed-gate: 出版入力treeの複製に2変異を個別に注入し、run 5で
   exit≠0・pin FAIL文言・記録未書込を確認。

### 監査正本

`output/third-verification-audit-20261120.json`（SHA-256
`c32a1963d3a1ab611b0c67f8b540e8d896ebebdb587ae1510df519bc4cfae467`・7,906 bytes）。
同一cwd 2回＋隔離tree/cwd/HOME+`PYTHONHASHSEED=random` 1回の3実行でbyte-identical。

### 再現コマンド

```
# 1〜4: fresh runs（1パス1コマンド・各約115秒・resume-safe）
python3 input/verify_sweeps_reexec_20261120.py run 240 --pass A --root <freshA-dir> --inputs input/sweeps
HOME=<iso-home> python3 <iso>/input/verify_sweeps_reexec_20261120.py run 240 --pass B --root <freshB-dir> --inputs <iso>/input/sweeps
# （freshBの成果を fresh-runs/runB-isolated-cwd-home/ に、freshAを runA-same-cwd/ に置く）
# harness:
python3 scripts/verify_k1144_reexec_third_20261120.py
```

machineの呼び出し規約（ARGUMENT）は第二検証出版READMEのとおり budget 240・worker 4。

## 解釈規約

- 本検証はK1144の「全probe再実行」の再現であり、depth-10 verdictのgame-theoretic値は
  1行も決めない。132 probeは12石根（root popcount 8・child popcount 7）対depth-10
  （7手先まで）の探査で、REFUTED-D10は「depth-10内の勝ちなし」証明でありLOSS証明ではない。
  WIN8-D10候補は証明書ではない。nodes数・solved数を勝敗として読まない。
- **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。**
- 採番: 本実験のitem番号はpart2出版直前に3点確認で取得する。
