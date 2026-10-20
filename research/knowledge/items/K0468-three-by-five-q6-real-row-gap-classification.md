---
id: K0468
title: 3×5・q=6は任意の正実数行間隔で6点円が最大4本、空盤Grundyは円1本の場合のみ0
kind: proposition
status: needs-review
topics:
- rectangles
- variants
- geometry
- grundy
- maximal-safe
- statistics
aliases: []
relations:
- type: depends_on
  target: K0002
  note: 通常プレイのGrundy定義
artifacts:
- path: research/experiments/fixed-width/reports/q36-real-row-gap-m5.md
  role: proof
  note: 全正実数間隔への代数的分類、13場合への帰着と有限局面分類
- path: research/experiments/fixed-width/scripts/q36_real_row_gap_m5.py
  role: verifier
  note: 弦和・積に基づく場合生成と15点全局面のmex再帰
- path: research/experiments/fixed-width/scripts/q36_real_row_gap_m5_independent.cpp
  role: verifier
  note: 全6点組の4×4整数行列式を使う独立円検査とmex再帰
- path: research/experiments/fixed-width/output/q36_real_row_gap_m5.json
  role: data
  note: 13場合の円・Grundy・極大配置の完全結果
- path: research/experiments/fixed-width/output/q36_real_row_gap_m5_cases.tsv
  role: data
  note: 独立検証用13有理数代表と期待値
solution:
  board: 3×5・q=6・実数行間隔
  level: strong
  outcome: conditional
  classification:
  - root
  - first-moves
  - all-safe-win-loss
  - all-safe-grundy
  coverage: 全a,b>0、各場合の全安全局面
  conditions: 横座標{0,1,2,3,4}共通、縦座標{0,a,a+b}、q=6
  verification:
  - mathematical-proof
  - exhaustive-enumeration
  - independent-enumeration
  certificate: 円成立条件の6直線・13場合への全称帰着と15点全局面mex
  independent_check: 全13代表の5005個の6点組を4×4整数行列式で独立生成し全局面結果と照合
  note: 空盤g=0 iff 円1本、それ以外は1。最大円4本はa=b=1のみ
scope: 横座標{0,1,2,3,4}、行座標{0,a,a+b}、a,b>0の全実数、q=6・円と直線禁止・通常プレイ。全安全局面は各幾何型の有限完全列挙。
evidence: 2026-10-20添付統合。元資料では proved または computed と報告（個別の元statusは保存ZIPを参照）。本項目の全量化範囲に対する証明・計算の再監査は未完了。有限検証の実行範囲は統合実験のVALIDATION.mdを参照。
---


> 統合監査: 以下は取込元の主張・報告。全称証明・完全列挙の監査が未完了のため、現在の採用状態は needs-review。本文中の「証明」「一致」は元資料での報告を表す。


# 3×5・q=6の任意実数行間隔の完全分類

\(U=1/[a(a+b)],V=1/[b(a+b)]\) とすると、6点円の成立条件は

\[
 2U=1,\ 2V=1,\ 2(U+V)=1,\ 3U=1,\ 3V=1,\ 3(U+V)=1
\]

のいずれかに限る。係数2の各条件は円2本、係数3の各条件は円1本に対応する。正象限での交点は6個、三重交点はない。従って円は最大4本、4本は \(a=b=1\) に限る。中央行の中央点 \((2,a)\) は全行間隔でどの6点円にも属さない。

幾何条件を13場合に分類すると禁止集合は同型を除いて7種類。全15点の安全局面の完全mex再帰から、空盤Grundyは**円がちょうど1本のとき0、それ以外で1**。全安全局面での最大Grundyは、標準等間隔 \(a=b=1\) で5、その他の場合は高々3。標準等間隔では安全局面30866、極大配置は11石1個・12石58個・13石9個。

数学的全称証明の範囲は行間隔の分類。各型のGrundy値・局面数・極大配置は有限完全列挙であり、独立C++行列式検証と一致した。標準整数格子の一般の3×mについての安定化長・Grundyを新たに決めるものではない。
