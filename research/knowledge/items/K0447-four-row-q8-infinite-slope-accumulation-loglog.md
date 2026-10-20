---
id: K0447
title: 四行8点円の実現傾きは無限個の集積点を持ち種類数は対数×二重対数以上
kind: proposition
status: needs-review
topics:
- geometry
- rectangles
- variants
aliases: []
relations:
- type: depends_on
  target: K0432
  note: 既約傾きと正規形の定義を使用
artifacts:
- path: research/experiments/fixed-width/reports/q48-infinite-accumulation-loglog-lower-20261016.md
  role: proof
  note: 固定傾きPellと双対Pellの二重族、開区間分離、定量下界の全称証明
- path: research/experiments/fixed-width/scripts/q48_accumulation_loglog_20261016.py
  role: verifier
  note: 4×3世代、840件の4点共円行列式と区間分離の整数監査
- path: research/experiments/fixed-width/output/q48_accumulation_loglog_20261016.txt
  role: data
  note: 独立検算の出力
scope: 標準4連続整数行の非局所8点円。既約傾きA/Bの集積点とA,B<=Hの種類数R(H)。
evidence: 2026-10-20添付統合。元資料では proved または computed と報告（個別の元statusは保存ZIPを参照）。本項目の全量化範囲に対する証明・計算の再監査は未完了。有限検証の実行範囲は統合実験のVALIDATION.mdを参照。
---


> 統合監査: 以下は取込元の主張・報告。全称証明・完全列挙の監査が未完了のため、現在の採用状態は needs-review。本文中の「証明」「一致」は元資料での報告を表す。


実現可能な傾きの集合には無限個の相異なる無理数集積点があり、それらは厳密増加して47/6に収束する。従って47/6は集積点集合の集積点である。

D=4096105の正Pell基本単元を Lambda とすると、実現可能な既約傾きの種類数 R(H) は

```
liminf_(H->infinity) R(H)/(log H log log H)
  >= 1/(4 log Lambda) > 0.
```

詳細な二重Pell構成、重複しない開区間の証明、定数の明示値は添付証明書を参照。840件の行列式検算は有限監査であり全称証明の代用ではない。正確な増加次数は未解決。
