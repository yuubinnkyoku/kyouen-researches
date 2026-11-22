---
id: K1217
title: "(6,6) witness band extends to m=25 — a 29-stone row-deficient maximal safe configuration on 6x25; M_{6,6} is 26..495"
kind: proposition
status: computed
topics: [maximal-safe, rectangles, search-methods, verification, frontier-bookkeeping]
aliases: []
date: 2026-11-22
scope: "6 x 25（および 6 x 23..25 witness 幅）の整数格子盤・q=6・標準ルール"
evidence: "kissat 4.0.4 class-split SAT 判定と decode 証明書、sat.js 整数 verifyConfig、Python Fraction 独立検証器による 2 系統検証、出版 K0818 アンカー bit-exact 再現、採用前 pair との 3 ラン決定性、純並進 census の交差検査"
relations:
  - {type: extends, target: K1215, note: "6x24 witness band を 6x25 へ 1 幅延長（frontier を解決し 6x26 へ前進）"}
  - {type: related, target: K0806, note: "上界 U_{6,6}=495（K0318 代入）は不変で本下界更新と合わせ M_{6,6} ∈ [26,495]"}
  - {type: related, target: K1206, note: "witness 新規性判定に格子同型分類（D4+平行移動の石集合比較）を適用"}
  - {type: depends_on, target: K0765, note: "全曲線の all-triples census 構成（K0810 core sat.js）"}
artifacts:
  - {path: research/experiments/six-row-q6-m25-frontier-crunch-20261122/README.md, role: log, note: "実験README（主張・経緯・ゲート・再現手順）"}
  - {path: research/experiments/six-row-q6-m25-frontier-crunch-20261122/MANIFEST.sha256, role: manifest, note: "全ファイルのsha256"}
  - {path: research/experiments/six-row-q6-m25-frontier-crunch-20261122/output/records.jsonl, role: data, note: "8走査行（SAT×3ラン・INDET honest negatives 7行・provenance付）"}
  - {path: research/experiments/six-row-q6-m25-frontier-crunch-20261122/witness/w6x25_class2.json, role: certificate, note: "class{2} witness 29石 rows [5,5,4,5,5,5] decode+verify"}
  - {path: research/experiments/six-row-q6-m25-frontier-crunch-20261122/witness/census_class2.json, role: data, note: "純並進census R(S)=25（widths 23..25被覆）"}
  - {path: research/experiments/six-row-q6-m25-frontier-crunch-20261122/output/controls/census_gates.json, role: data, note: "census アンカー 4/4 MATCH・6x25=2,302 新アンカー"}
  - {path: research/experiments/six-row-q6-m25-frontier-crunch-20261122/output/controls/ctrl_6x23q6_c1.txt, role: data, note: "陽性対照 K0818 アンカー conflicts 77,932・model bit-exact（decode JSON は出版正本と byte-identical）"}
  - {path: research/log/2026-11-22-six-row-q6-m25-adopt-single-owner-note.md, role: log, note: "採用宣言（中断 2c3254ef9f レーンの引き取り）"}
  - {path: research/log/2026-11-22-six-row-q6-m25-frontier-crunch-session-log.md, role: log, note: "session log（採用セッション執筆・元宣言の予定path）"}
---

# (6,6) witness band extends to m=25

## 命題（computed・有限機械計算）

6×25 整数格子盤（q=6・q点共円/共線禁止・標準ルール）に**行欠損の極大安全配置**
（29石・全容量 6×5=30石に対して欠損）が存在する。具体的に:

1. class {2}（行2欠損・rows [5,5,4,5,5,5]）の krow=2:4 固定 + minpos=11 分解インスタンスが
   kissat 4.0.4 SAT（**3,574,244 conflicts**・採用前 pair と採用再現 run を含む3コールドランで
   conflicts・model 完全一致）。

decode 証明書は整数 verifyConfig（sat.js 系）と Python Fraction 独立検証器の2系統で安全+極大を
検証済み（tamper 対照は移動・削除で not maximal、追加で unsafe を検出）。石集合は 6×25 矩形上の
D4 像+全平行移動 embedding の意味で、K0815/K0818 の 6×23 witness（正本アンカー）とも
K1215 の 6×24 class{1}/class{2} witness とも非合同（新規の格子同型類）。

## 帰結（frontier-bookkeeping）

- (6,6) の witness 帯は m=6..25 に伸び、**M_{6,6} ∈ [26, 495]**（下界 25 → 26 の更新・
  上界は K0318 代入 U=495〔K0806〕不変）。
- K0821-audit 規約でいう「M 候補集合から 25 が消えて 26..495 が残る」更新であり、
  witness-free 幅は 1 も新たに確定していない（不在主張は本項に含まれない）。
- 6×26 が新 frontier。6×25 の未走査クラス（class{1} の krow=1:1..1:3 分解・残り正準クラスの
  cap 内掃引 INDET 7行を除く未実行分）は不在不主張のまま。
- 追加観測（witness 側の構造）: bbox 幅は 23 で、正規化純並進配置は 6×23/6×24/6×25 の3幅すべて
  極大安全（純並進 R(S)=25 で停止）。高速並進 census と Fraction 検証器の交差検査 4点で一致
 （6×24 は t=1 で被覆・t=0 は not maximal (23,2)）。
- 前線更新の知見: 6×25 class{2} は plain 250s / krow固定 260s で INDET（K1215 記録）だったが、
  krow=2:4+minpos=11 への2重分解で SAT に到達。行ごとの人数固定と左端ピン（H-split）の組合せは
  frontier 幅の追い込みにおける次の定石候補。

## 根拠と検証状態

- 機材: K0818/K0819 class-split 機材（sat3.js sha256 `e04581eb…`・sat2/sat.js pin・
  kissat 4.0.4 公式バイナリ sha256 `21da5d98…`）。CNF は決定的再生成可能（sha256 `46c485af…`・
  中断レーンの CNF と byte-identical を採用時に確認）。
- ゲート: census アンカー (5,12,6)=212/(5,15,5)=629/(5,23,6)=996/(5,27,5)=2355 が 4/4 再現
 （6×23 q6=1,890・6×24 q6=2,088・**6×25 q6=2,302〔新アンカー〕**）・陽性対照 6×23 q=6 class{1}
  SAT 77,932 conflicts が出版 K0818 アンカーと model 全数 bit-exact（decode JSON は出版 witness
  json と byte-identical）・陰性対照 2×9 q=4 class{0} UNSAT 517。
- 限界: 有限機械計算であり、census 完全性（all-triples 構成）と検証系の健全性まで。
  SAT 判定は充填充足的証拠（witness 本体が独立検証済み）なので solver の UNSAT 側健全性には
  依存しない。6×25 の不在側は一切主張しない。
- 標準 11×11 空盤・二石 root・S2・class 1/2/4 は非接触（UNKNOWN のまま）。

## 更新履歴

- 2026-11-22: 本項作成（実験 `six-row-q6-m25-frontier-crunch-20261122`・下界 25→26）。
  中断された crunch レーン（単一オーナー宣言 `2c3254ef9f`）の staged witness を
  adopt+republish 手続（(6,5) 6×31 の `bc11e28b` 前例）で検証・出版。
  K1215 に続き 6x24 から 6x25 への1幅延長。6x26 以降は未決着のまま
 （残作業: 6×26 の分解掃引・class{1} krow 残・band 494 までの持続性）。
