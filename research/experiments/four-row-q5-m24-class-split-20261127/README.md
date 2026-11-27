# (4,24,5) class-split 掃引 — K1197+m23 完了後の次前線 (2026-11-27 高速レーン・IN FLIGHT)

単一オーナー宣言:
[2026-11-27-four-row-q5-m24-frontier-single-owner-note](../../../log/2026-11-27-four-row-q5-m24-frontier-single-owner-note.md)

## 位置づけ

- witness 帯 m=5..20 (K0833)・witness-free {21,22,23} (K0857/K1197/m23 sweep
  2026-11-23 完了・111 record 全 UNSAT)・**M_{4,5} = 21 または ≥ 25**。
- 判定: 全 piece UNSAT なら witness-free {21,22,23,24}・**M_{4,5} = 21 または
  ≥ 26**。SAT なら witness 帯 m=5..24・**M_{4,5} ∈ [25, 140]**。
- 上界 U_{4,5}=140 (K0318) 不変。先行出版 (m21/m22/m23) は再検証しない。

## 器材 (すべて m23 kit 出版 byte)

- 生成器: sat.js (`0cc6021a…`) + sat2.js (`282ae832…`) + sat3.js (`d03f908e…`)
  + sat4.js k-aware x2 (`df472efc…`)・verify_witness.py (`0530d16…`)。
- ソルバ: kissat 4.0.4 static linux-amd64 (md5 `3a5eba83…`・出版 pin)。
- runner: `runner24.sh` (resumable chunk・records24.jsonl append-only・
  CAP=220s piece cap・BUDGET=60s chunk 先行制限)・`x2gen24.sh`
  (k=3: B∈p+1..22 = m−2・k=2: B∈p+1..23 = m−1)・
  `multigen24.sh` (INDET multi の krow ピン分解)・
  `coverage_check24.py` (M=24・被覆完全性監査 v2)。

## 被覆の完全性 (m23 と同一構造)

- 9 正準欠損クラス (mod V: 行 0↔3, 1↔2): {0},{1},{0,1},{0,2},{0,3},{1,2},
  {0,1,2},{0,1,3},{0,1,2,3}。
- 単一クラス {0},{1} は k∈{0..3} × minpos p∈0..11 (sound H-split:
  min(x₁, 23−x_k) ≤ floor(23/2) = 11)。lex との併用は unsound ので全
  インスタンス lex なし。
- multi クラス直接・INDET は krow ピンで追分解。k3/k2 抵抗バケットは
  x2 第2石分割 (k-aware)。
- **追分解 v2 (2026-11-27 宣言
  [2026-11-27-four-row-q5-m24-multi-krow-decomposition-declaration](../../../log/2026-11-27-four-row-q5-m24-multi-krow-decomposition-declaration.md))**:
  INDET multi c01/c02/c03/c12 は `multigen24.sh` で 16 厳密数ピース
  (k0,k1)∈{0..3}² に分解・k0≥1 抵抗ピースは minpos p=0..11 副分割。
  `coverage_check24.py` v2 は multi を「直接 UNSAT」または「16 ピース全 UNSAT」
  で決着判定し、k2/k3 直接 INDET bucket の完全 x2 副分割による決着も受理する。
- 陽性対照 (4,20,5) c0k3p1 は CNF md5 `362034b2…` byte-exact・kissat
  **SAT 375,415 conflicts bit-exact** (m21/m22/m23 交差較正値と同一・本
  host 2026-11-27 再現)。

## 運用

- 実行: `CAP=220 bash runner24.sh` を bash call 上限内で繰り返す
  (各 chunk は BUDGET 60s 内に新 piece を開始・最大 ~280s)。
- records: `output/records24.jsonl` (増分 push・append-only・resumable)。
- INDET は honest negative・不在主張ではない。

## 結果

IN FLIGHT — 決着後に本 README を更新し K 項目へ昇格する。

## Not claimed

- 4×24 の不在は全 piece UNSAT のときのみ (個別 INDET は主張しない)。
- (4,q≠5)・w 行族・Grundy・11×11 は一切不消費 (全時点 UNKNOWN)。
