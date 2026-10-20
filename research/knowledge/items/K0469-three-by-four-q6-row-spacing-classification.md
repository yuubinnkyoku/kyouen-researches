---
id: K0469
title: 3×4・6点版は行間隔の3等式で禁止円数と空盤Grundyが完全に決まる
kind: proposition
status: needs-review
topics:
- rectangles
- variants
- geometry
- grundy
aliases: []
relations:
- type: depends_on
  target: K0001
  note: 6点共円・共線禁止の通常プレイ
- type: depends_on
  target: K0002
  note: Grundy数の定義
artifacts:
- path: research/experiments/three-by-four-q6-row-spacings-20261018/proof.md
  role: proof
  note: 全正実数行間隔の代数的分類と75型mex表
- path: research/experiments/three-by-four-q6-row-spacings-20261018/verify.py
  role: verifier
  note: 有理数行列式と4096局面の再帰mex
- path: research/experiments/three-by-four-q6-row-spacings-20261018/verify_independent.cpp
  role: verifier
  note: 整数行列式と反復mexによる独立照合
- path: research/experiments/three-by-four-q6-row-spacings-20261018/audit-python.json
  role: data
  note: 5代表間隔の検算と群占有数の照合
- path: research/experiments/three-by-four-q6-row-spacings-20261018/audit-cpp.txt
  role: data
  note: 独立C++実行記録
- path: research/experiments/three-column-four-row-q6-20261018/proof.md
  role: proof
  note: 正実数間隔の全称幾何分類と有限型の完全再帰
- path: research/experiments/three-column-four-row-q6-20261018/verify.py
  role: verifier
  note: 整数行列式の独立幾何判定と4096盤の監査
- path: research/experiments/three-column-four-row-q6-20261018/independent_recurrence.py
  role: verifier
  note: 198安全状態の縮約再帰による独立検算
- path: research/experiments/three-column-four-row-q6-20261018/results.json
  role: data
  note: 4096整数盤の検算結果と3類型の全局面度数
scope: V={(x,y):x=0,1,2,3; y=0,a,a+b}, a,b>0。q=6、円または直線、通常プレイ。
evidence: 2026-10-20添付統合。元資料では proved または computed と報告（個別の元statusは保存ZIPを参照）。本項目の全量化範囲に対する証明・計算の再監査は未完了。有限検証の実行範囲は統合実験のVALIDATION.mdを参照。
---



> 統合監査: 以下は取込元の主張・報告。全称証明・完全列挙の監査が未完了のため、現在の採用状態は needs-review。本文中の「証明」「一致」は元資料での報告を表す。


# 3×4・6点版は行間隔の3等式で禁止円数と空盤Grundyが完全に決まる

上記盤の禁止6点集合は `ab=2`、`a(a+b)=2`、`b(a+b)=2` の成立数だけ存在する。0個なら空盤 `g=0`（4096安全局面）、1個なら `g=1`（4032安全局面）、2個なら `a=b=1` に限り `g=0`（3972安全局面）。0・1個では全安全局面のGrundy値はそれぞれ `(12-|S|) mod2`、`(11-|S|) mod2`。

二円の場合、禁止集合は2点で交わる6点組2個。全安全局面のnimber度数は `0:1378, 1:1378, 2:608, 3:608`、全12初手が負け手。極大配置は10石16通り、11石2通り。

円の全称分類は三行の弦の積の二階差商で証明する。二円の場合のゲーム値は、2点共通群・4点ずつの専有群・2点の外部群という75型の完全mex表で証明する。検算は有理数行列式＋再帰DPと独立した整数行列式＋反復DP。

**量化の限界:** 横座標は3行とも共通の `0,1,2,3`。任意の非等間隔横座標には拡張しない。標準整数格子 `M_{3,6}=9` を変更する結果ではない。

座標を交換し全体をdで割ると、不等間隔3列×等間隔4行の版も同じ命題となる。この別版の証明・198安全縮約状態による検算を同じ項目のartifactへ統合した。別版の証拠監査も未完了。
