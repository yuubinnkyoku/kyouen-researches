---
id: K1215
title: "(6,6) witness band extends to m=24 — two new 29-stone row-deficient maximal safe configurations; M_{6,6} is 25..495"
kind: proposition
status: computed
topics: [maximal-safe, rectangles, search-methods, verification, frontier-bookkeeping]
aliases: []
date: 2026-11-22
scope: "6 x 24（および 6 x 22..24 witness 幅）の整数格子盤・q=6・標準ルール"
evidence: "kissat 4.0.4 class-split SAT 判定と decode 証明書、sat.js 整数 verifyConfig、Python Fraction 独立検証器による 2 系統検証、出版 K0818 アンカー bit-exact 再現、純並進 census の交差検査"
relations:
  - {type: extends, target: K0815, note: "dai-6 の (6,6) witness chain を 6x23 から 6x24 へ 1 幅延長"}
  - {type: related, target: K0806, note: "上界 U_{6,6}=495（K0318 代入）は不変で本下界更新と合わせ M_{6,6} ∈ [25,495]"}
  - {type: related, target: K1206, note: "witness 新規性判定に格子同型分類（D4+平行移動の石集合比較）を適用"}
  - {type: depends_on, target: K0765, note: "全曲線の all-triples census 構成（K0810 core sat.js）"}
artifacts:
  - {path: research/experiments/six-row-q6-m24-class-split-20261121/README.md, role: log, note: "実験README（主張・ゲート・erratum・再現手順）"}
  - {path: research/experiments/six-row-q6-m24-class-split-20261121/MANIFEST.sha256, role: manifest, note: "37ファイルのsha256"}
  - {path: research/experiments/six-row-q6-m24-class-split-20261121/output/records.jsonl, role: data, note: "9走査行（2 SAT witness ×2run・honest negatives）"}
  - {path: research/experiments/six-row-q6-m24-class-split-20261121/witness/w6x24_class1.json, role: certificate, note: "class{1} witness 29石 rows [5,4,5,5,5,5] decode+verify"}
  - {path: research/experiments/six-row-q6-m24-class-split-20261121/witness/w6x24_class2.json, role: certificate, note: "class{2} witness 29石 rows [5,5,4,5,5,5] decode+verify"}
  - {path: research/experiments/six-row-q6-m24-class-split-20261121/output/controls/census_gates.json, role: data, note: "census アンカー 4/4 MATCH"}
  - {path: research/experiments/six-row-q6-m24-class-split-20261121/output/controls/ctrl_6x23q6_c1.txt, role: data, note: "陽性対照 K0818 アンカー conflicts 77932 bit-exact（decode JSON は出版正本と byte-identical）"}
  - {path: research/log/2026-11-21-six-row-q6-m24-class-split-session-log.md, role: log, note: "session log"}
---

# (6,6) witness band extends to m=24

## 命題（computed・有限機械計算）

6×24 整数格子盤（q=6・q点共円/共線禁止・標準ルール）に**行欠損の極大安全配置**
（29石・全容量 6×5=30石に対して欠損）が存在する。具体的に:

1. class {1}（行1欠損・rows [5,4,5,5,5,5]）・kissat 4.0.4 SAT・1,837,912 conflicts（2回実行で bit-一致）。
2. class {2}（行2欠損・rows [5,5,4,5,5,5]）・SAT・404,422 conflicts（同上）。

いずれも decode 証明書が整数 verifyConfig（sat.js 系）と Python Fraction 独立検証器の
2 系統で安全+極大を検証済み（tamper 対照は Fraction 系で unsafe 検出）。両 witness の石集合は
6×24 矩形上の D4 像+全平行移動 embedding の意味で、K0815/K0818 の 6×23 witness（正本アンカー）とも
互いとも非合同（新規の格子同型類）。

## 帰結（frontier-bookkeeping）

- (6,6) の witness 帯は m=6..24 に伸び、**M_{6,6} ∈ [25, 495]**（下界 24 → 25 の更新・
  上界は K0318 代入 U=495〔K0806〕不変）。
- これは K0821-audit 規約でいう「M 候補集合から 24 が消えて 25..495 が残る」更新であり、
  witness-free 幅は 1 も新たに確定していない（不在主張は本項に含まれない）。
- 6×25 は未決着: class {1}/{2} の plain（250s）と krow固定 k=4（260s）掃引は INDET
  （1,222,228/1,207,894/1,126,385/1,294,221 conflicts・cap 到達 honest negatives・不在不主張）。
  残り 33 クラスは未走査。
- 追加観測（witness 側の構造）: 両 witness の bbox 幅は 22 で、正規化純並進配置は
  6×22/6×23/6×24 の 3 幅すべて極大安全（純並進 R(S)=24 で停止）。高速並進 census
  （整数正規化曲線キー・BLOCKED 前計算・translate_census2.py）と Fraction 検証器の
  交差検査 4 点で一致。

## 根拠と検証状態

- 機材: K0818/K0819 class-split 機材（sat3.js sha256 `e04581eb…`・sat2/sat.js pin・
  kissat 4.0.4 公式バイナリ sha256 `21da5d98…`）。全63非空欠損クラス→35正準代表の被覆は
  K0818 の被覆論と同じ（本項の主張は SAT 2 クラスのみで成立し、被覆は不在主張にのみ必要）。
- ゲート: census アンカー (5,12,6)=212/(5,15,5)=629/(5,23,6)=996/(5,27,5)=2355 が 4/4 再現
  （6×24 q6 = 2,088 曲線）・陽性対照 6×23 q=6 class{1} SAT 77,932 conflicts が出版 K0818
  アンカーと bit-exact（decode JSON 全体が出版 witness json と byte-identical）・
  陰性対照 2×9 q=4 class{0} UNSAT 517 bit-exact。
- 限界: 有限機械計算であり、census 完全性（all-triples 構成・自明に全曲線を列挙）と
  kissat の正確性まで。SAT 判定は充填充足的証拠（witness 本体が独立検証済み）なので
  solver の UNSAT 側健全性には依存しない。
- 標準 11×11 空盤・二石 root・S2・class 1/2/4 は非接触（UNKNOWN のまま）。

## 更新履歴

- 2026-11-22: 本項作成（実験 `six-row-q6-m24-class-split-20261121`・下界 24→25）。
  K0815 が 6x8..6x23 witness を出版したことに続き 6x24 を追加。6x25 以降は未決着のまま
  （残作業: {1}/{2} の krow/minpos 分解・bounded surgery・全クラス走査・band 494 までの持続性）。
