# (4,23,5) class-split 掃引 — K1197 次前線の決着 (2026-11-21 高速レーン・IN FLIGHT)

## 位置づけ

K1197（4×22 witness-free）が明示した次前線。着手は単一オーナー宣言
[2026-11-21-four-row-q5-m23-frontier-single-owner-note](../../../log/2026-11-21-four-row-q5-m23-frontier-single-owner-note.md)
（2026-11-21T19:25Z・宣言時 HEAD `5a9cf304`）の下で実施。

- 判定: 全 piece UNSAT なら witness-free 幅集合 {21,22,23}・K0821 監査規約により
  **M_{4,5} = 21 または ≥ 25**。SAT なら M_{4,5} ∈ [24,140] に戻り witness を復号・検証する。
- 上界 U_{4,5} = 140（K0318 代入）は不変。witness 帯 m=5..20（K0833）・witness-free 21/22
  （K0857/K1197）は先行出版のままで本レーンは再検証しない。

## 器材

- 生成器: `scripts/sat.js`（md5 `0cc6021a…`）+ `sat2.js` + `sat3.js` + `sat4.js`(k-aware x2)。
  m21/m22 レーン出版正本と byte-identical（較正で CNF md5 3 件照合）。
- ソルバ: kissat 4.0.4 static linux-amd64（md5 `3a5eba830aa6008a604fcc9bbe99a325`・出版 pin 一致）。
- 較正（本環境・2026-11-21T19:20Z）: 陽性対照 (4,20,5) c0k3p1 CNF md5 `362034b2…` byte-exact 再生・
  kissat **SAT 375,415 conflicts bit-exact**（m21/m22/takeover 交差較正值）。
  (4,22,5) c0k3p0 CNF `bf26eee9…`・c0k3p0x2b1 CNF `7db59b4b…` byte-exact 再生。

## 被覆の完全性（m22 レーンと同一構造）

- 9 正準欠損クラス（mod V: 行 0↔3, 1↔2）:
  {0},{1},{0,1},{0,2},{0,3},{1,2},{0,1,2},{0,1,3},{0,1,2,3}。
- 単一クラスは k∈{0..3} × minpos p∈0..11（sound H-split: min(x1, 22−xk) ≤ 11。
  lex との併用は unsound なので全インスタンス lex なし）。
- multi は直接・INDET は krow ピンで追分解（m21 規約）。
- k3/k2 抵抗バケットは x2 第 2 石分割（k-aware: k=3→B≤21, k=2→B≤22）。
- 直接 81 + 対照 1 インスタンス。piece cap 260s（本 sandbox の bash call 上限 300s に由来。
  INDET は honest negative・不在主張ではない）。

## 運用

- runner: `runner23.sh`（resumable chunk 実行・records append-only・CNF 生成は決定的）。
- x2 driver: `x2gen23.sh <bucket>`。
- records: `output/records23.jsonl`（増分 push・append-only）。

## 結果

IN FLIGHT — 実行中。決着後に本 README を更新し K 項目へ昇格する。
