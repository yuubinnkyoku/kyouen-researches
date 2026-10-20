---
id: K0472
title: 任意の整数間隔の三列格子で5点円があれば6点円が無限に存在する
kind: proposition
status: needs-review
topics:
- geometry
- rectangles
- variants
aliases: []
relations: []
artifacts:
- path: research/experiments/fixed-width/reports/three-column-five-to-six-universal-20261017.md
  role: proof
  note: 任意の正整数a,b,dに対する全称証明、明示構成、量化範囲
- path: research/experiments/fixed-width/scripts/three_column_five_to_six_verify.py
  role: verifier
  note: 二次形式不変性と独立円決定による有限検算
evidence: 2026-10-20添付統合。元資料では proved または computed と報告（個別の元statusは保存ZIPを参照）。本項目の全量化範囲に対する証明・計算の再監査は未完了。有限検証の実行範囲は統合実験のVALIDATION.mdを参照。
---


> 統合監査: 以下は取込元の主張・報告。全称証明・完全列挙の監査が未完了のため、現在の採用状態は needs-review。本文中の「証明」「一致」は元資料での報告を表す。


## 命題・範囲

任意の正整数a,b,dに対して、三列無限格子 `x∈{0,a,a+b}`, `y∈dZ` 上で5点以上を通る円が存在するなら、6点を通る円が無限個存在する。最大共円点数は4または6であり、5にはならない。円そのものが5点で終わることはあり得るが、別の6点円を構成できる。

## 現在の根拠と限界

5点円の非接線列は反射で6点へ延長できる。接線列の場合は縦半弦長の整数三つ組tを得て、二次形式 `Q(t)=b t0²−(a+b)t1²+a t2²` の値 `−ab(a+b)/d²` を保つ整数変換により、最大7候補から全成分非零の解を得る。これで6点円を構成し、同変換の反復パラメータを大きくすると無限個得られる。全称証明は上記proofに記載。別方式の有理数円決定を含む有限検算は94接線例。

一般の合成数dについて `d² gcd(a,b) | ab(a+b)` が6点円存在の十分条件かどうかは、この命題からは決まらない。通常格子のK0071とも別の幾何命題。K番号は統合時に衝突確認を要する仮番号。
