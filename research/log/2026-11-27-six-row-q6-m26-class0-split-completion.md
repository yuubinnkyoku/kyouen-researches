# 2026-11-27 (6,6) 6x26 class {0} krow/minpos decomposition: 完了報告 (高速レーン)

## 対応宣言

- 単一オーナー宣言 `research/log/2026-11-27-six-row-q6-m26-class0-minpos-declaration.md`
  (commit `a9dde1d3`, 宣言時 HEAD `fe07ef8d`, publish-then-execute)。
- 本完了報告に至る全測定は宣言の後の実行であり、宣言内容からの逸脱はない。

## 結果 (全12 probe INDET - honest negative)

6x26 q=6 class {0} (欠損行 = 行0のみ) を krow=0:4 (行0ちょうど4石・
単一欠損 29石族) で固定し、minpos (行0の最左石位置) P=0..11 を
完全分割掃引した (12 disjoint sub-instances・sound H-split)。

| probe | minpos P | verdict | conflicts | cap |
|---|---|---|---|---|
| m26-c0k4p0 | 0 | INDET | 2,402,216 | 272s |
| m26-c0k4p1 | 1 | INDET | 2,509,295 | 272s |
| m26-c0k4p2 | 2 | INDET | 2,678,856 | 272s |
| m26-c0k4p3 | 3 | INDET | 1,355,457 | 272s |
| m26-c0k4p4 | 4 | INDET | 1,373,740 | 272s |
| m26-c0k4p5 | 5 | INDET | 1,396,332 | 272s |
| m26-c0k4p6 | 6 | INDET | 1,588,848 | 272s |
| m26-c0k4p7 | 7 | INDET | 1,666,278 | 272s |
| m26-c0k4p8 | 8 | INDET | 1,719,671 | 272s |
| m26-c0k4p9 | 9 | INDET | 1,822,575 | 272s |
| m26-c0k4p10 | 10 | INDET | 1,848,761 | 272s |
| m26-c0k4p11 | 11 | INDET | 4,053,417 | 272s |

- V鏡映 (行反転) で class {0} ≡ class {5} であり、本掃引は行5エッジ行族も被覆。
- **判定: 全 INDET のため M_{6,6} ∈ [26, 495] 不変・前線 6x26 のまま**
  (宣言どおり)。個別 INDET は honest negative であり不在主張でない。

## 較正・対照 (受入条件 1, 2)

- **陽性対照**: 6x25 q=6 class {2} krow=2:4 minpos=11 は
  **SAT 3,574,244 conflicts (241.07s) で出版 K1217 値の bit-exact 再生**
  (受入条件 1 PASS)。生ログ `output/r6x25q6_c2k4p11_mine.txt`。
- 追加観察 probe: 6x25 class {0} krow=0:4 minpos=11 INDET 4,280,184 @272s
  (既知幅 m=25 に対する class {0} 応答の bookkeeping・下界に影響なし)。
- 全12 probe は各 272s cap・kissat 1走 (受入条件 2 PASS)。
- 受入条件 3 (SAT 時の witness 検証) は SAT がなかったため適用外。

## 観察

- class {0} の conflicts 帯 (1.36M-4.05M) は同じ cap での
  class {2} 帯 (3.73M-4.12M) より低い。特に P=3..5 の谷 (約1.36M-1.40M) は
  同 cap で class {2} のいずれの bucket より 40% 以上低く、
  エッジ行欠損族は分岐因子が構造的に小さいことを示唆する。
  ただし cap 内 INDET は不在主張でなく、より長い cap での再実行が
  UNSAT 収束の唯一の厳密ルート。
- 前回 (class {2} minpos 10..13) と同様、P=11 (最右 bucket) は
  P=0..10 の帯より顕著に重い (4.05M)。

## 器材

- sat3.js `e04581eb…` / sat2.js `14ceb854…` / sat.js `fcc0cfd8…` /
  verify_frac.py `837fe24b…` (m26 kit から sha 照合の byte-clone)。
- kissat 4.0.4 公式 linux-amd64 (`21da5d98…`, release zip `63282e51…`
  から展開・sha 照合済み)。
- CNF は再生成 (size policy・非出版)。生ログ 14 本・meta json 14 本・
  records.jsonl (14行)・summary.json を kit として出版:
  `research/experiments/six-row-q6-m26-class0-split-20261127/`。

## 未掃引 (次回候補・不在主張でない)

- 6x26 multi-deficiency classes・krow k≤3 の深欠損族・6x27。
- README「Coordination disclosure」: 79ad283a の aggregator が
  本宣言を「executing」として引用しているため、その側の class {0}
  実行結果が出版された場合は本 kit とは独立の cross-check として扱う
  (SIGTERM cut の conflicts は bit-exact 期待不可)。

## Not claimed

- 個別 INDET は不在主張でない。multi-class・krow k≤3・6x27 は対象外。
- (6,q≠6)・w 行族・Grundy・11×11 は一切不消費 (全時点 UNKNOWN)。
