---
id: K0470
title: 任意の整数間隔の三列格子における最大共円点数の完全分類
kind: proposition
status: needs-review
topics:
- geometry
- rectangles
- variants
aliases: []
relations: []
artifacts:
- path: research/experiments/fixed-width/reports/three-column-arbitrary-d-complete-classification-20261017.md
  role: proof
  note: 任意の正整数a,b,dについての全称証明と6点円の明示構成
- path: research/experiments/fixed-width/scripts/three_column_arbitrary_d_construct_20261017.py
  role: verifier
  note: 75000組の構成監査と252盤の独立行列式完全列挙
evidence: 2026-10-20添付統合。元資料では proved または computed と報告（個別の元statusは保存ZIPを参照）。本項目の全量化範囲に対する証明・計算の再監査は未完了。有限検証の実行範囲は統合実験のVALIDATION.mdを参照。
---


> 統合監査: 以下は取込元の主張・報告。全称証明・完全列挙の監査が未完了のため、現在の採用状態は needs-review。本文中の「証明」「一致」は元資料での報告を表す。


## 命題・範囲

正整数a,b,d、g=gcd(a,b)に対して、三列無限格子 `{0,a,a+b}×dZ` の最大共円点数は `d²g | ab(a+b)` のとき6、それ以外は4。5点円の存在と6点円の存在は同値であり、成立時は6点円が無限個存在する。dに素数冪の仮定は不要。

完全指摘q点版では `q≥7`、または `q≥5` かつ条件不成立なら、すべての盤長mと全安全局面で `g(S)=(3min(m,q−1)−|S|) mod 2`、真の満容量安定化長 `M_{3,q}=q−1`。

## 現在の根拠と限界

必要性は二点列の行番号の和とVietaの積の差から `d²g | ab(a+b)` を導く。十分性は `A=a/g,B=b/g`, `Bu+Av=1`, `u≥2,v≤−1`, `N=−ab(a+b)/(d²g)` に対し `T1=N−Bu²−Av²`, `T0=T1+2u`, `T2=T1+2v` と構成し、三列の半弦長整合式を直接確認する。各Tは負で非零、同じ偶奇なので6点が得られる。証明は上記reportに全文を置く。

75,000組の構成と252有限盤の独立行列式検算は監査であり、全称証明とは区別する。6点円が存在する場合のq=5,6のGrundy一般則や、最小6点円出現行数の厳密値は未確定。
