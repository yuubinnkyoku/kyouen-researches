---
id: K0449
title: 4行8点円の奇数分母傾きは法64で4合同類に限られる
kind: proposition
status: needs-review
topics:
- geometry
- rectangles
- variants
aliases: []
relations:
- type: depends_on
  target: K0431
  note: 全非局所円のPell正規形
- type: depends_on
  target: K0432
  note: 既約傾きの定義
artifacts:
- path: research/experiments/fixed-width/reports/q48-mod64-residue-class-20261015.md
  role: proof
  note: 3(mod4)素因数障害と法64合同類の全称証明
- path: research/experiments/fixed-width/scripts/q48_mod64_residue_class_independent_20261015.py
  role: verifier
  note: 平方剰余集合を使う独立有限監査
- path: research/experiments/fixed-width/output/q48_mod64_residue_class_independent_20261015.txt
  role: data
  note: 既知5型と有限候補735組の検査結果
- path: research/experiments/fixed-width/reports/q48-mod64-odd-denominator-obstruction-20261015.md
  role: proof
  note: 2進局所分類と3(mod4)素因数障害を組み合わせた全称証明
- path: research/experiments/fixed-width/scripts/q48_mod64_odd_denominator_audit_20261015.py
  role: verifier
  note: 法64平方剰余による独立有限監査
- path: research/experiments/fixed-width/output/q48_mod64_odd_denominator_audit_20261015.txt
  role: data
  note: 有限監査の実行結果
scope: 標準整数4連続行に各2点を持つ非局所8点円の既約傾きA/B、B奇数の場合の全盤長
evidence: 2026-10-20添付統合。元資料では proved または computed と報告（個別の元statusは保存ZIPを参照）。本項目の全量化範囲に対する証明・計算の再監査は未完了。有限検証の実行範囲は統合実験のVALIDATION.mdを参照。
---


> 統合監査: 以下は取込元の主張・報告。全称証明・完全列挙の監査が未完了のため、現在の採用状態は needs-review。本文中の「証明」「一致」は元資料での報告を表す。


既約傾き `A/B` の `B` が奇数なら、必ず

```
A * B^(-1) (mod 64) ∈ {9,23,41,55}.
```

同値に `A²−B²≡16 (mod64)`、`A²−9B²≡8 (mod64)`。従って `A/B=63/5` は実現不可能。証明は `QM²−PL²=8` の法8・法64解析と `3(mod4)` 素因数障害による全称的排除。独立検算では既存必要条件を通る735組のうち、奇数B99組から60組を追加排除した。B偶数、条件を満たす候補の実現可能性、全円数には何も主張しない。
