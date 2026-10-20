---
id: K0446
title: 四行8点円の最大弦長1億までの有限完全分類
kind: computation
status: needs-review
topics:
- geometry
- rectangles
- statistics
aliases: []
relations:
- type: supports
  target: K0317
  note: 既存Pell族の第四世代と新しい別傾きを有限範囲で確認
artifacts:
- path: research/experiments/fixed-width/reports/q48-gaussian-circle-census-100m-20261015.md
  role: proof
  note: ガウス整数列挙の完全性証明と有限実行結果
- path: research/experiments/fixed-width/scripts/q48_gaussian_circle_census_20261015.cpp
  role: verifier
  note: 1億までの完全因数分解列挙器
- path: research/experiments/fixed-width/scripts/q48_gaussian_census_independent_audit_20261015.py
  role: verifier
  note: 全15型の整数円行列式監査。全1億の独立列挙ではない
- path: research/experiments/fixed-width/output/q48_gaussian_census_B100000000_20261015.csv
  role: data
  note: 最大弦長1億以下の全15弦長型
scope: 標準4連続整数行・各行2点の円、最大弦長100000000以下
evidence: 2026-10-20添付統合。元資料では proved または computed と報告（個別の元statusは保存ZIPを参照）。本項目の全量化範囲に対する証明・計算の再監査は未完了。有限検証の実行範囲は統合実験のVALIDATION.mdを参照。
---


> 統合監査: 以下は取込元の主張・報告。全称証明・完全列挙の監査が未完了のため、現在の採用状態は needs-review。本文中の「証明」「一致」は元資料での報告を表す。


最大弦長1億以下の8点円弦長列は、局所型 `(1,3,3,1)` と増加7型および上下反転7型の計15型に限る。増加型の最大弦長は `73,2773,105301,1067653,1893727,3998665,75476575`。任意の `1<=m<=100000001` に対し `C8(m)=[m-3]_+ +2Σ_D[m-D]_+` が有限範囲で厳密。`C8(100000001)=1334910478`。

無界のガウス整数列挙法の完全性は数学的に証明したが、1億までの型リストは一方式の有限完全計算である。独立した弦長対全列挙との照合は100万まで。1億超の全分類、全円数の漸近次数は未確定。
