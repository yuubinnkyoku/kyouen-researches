---
id: K0472
title: 任意の整数間隔の三列格子で5点円があれば6点円が無限に存在する
kind: proposition
status: proved
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
- path: research/experiments/knowledge-audit-20261021/README.md
  role: log
  note: 証明の論理監査・再実行範囲・判定
evidence: '2026-10-21監査。二次形式を保存する整数変換と零点数上界、半弦長発散を確認。1260不変式・94構成を再検査。 監査記録: research/experiments/knowledge-audit-20261021/README.md。'
---


## 命題・範囲

任意の正整数a,b,dに対して、三列無限格子 `x∈{0,a,a+b}`, `y∈dZ` 上で5点以上を通る円が存在するなら、6点を通る円が無限個存在する。最大共円点数は4または6であり、5にはならない。円そのものが5点で終わることはあり得るが、別の6点円を構成できる。

## 現在の根拠と限界

5点円の非接線列は反射で6点へ延長できる。接線列の場合は縦半弦長の整数三つ組tを得て、二次形式 `Q(t)=b t0²−(a+b)t1²+a t2²` の値 `−ab(a+b)/d²` を保つ整数変換により、最大7候補から全成分非零の解を得る。これで6点円を構成し、同変換の反復パラメータを大きくすると無限個得られる。全称証明は上記proofに記載。別方式の有理数円決定を含む有限検算は94接線例。

一般の合成数dについて `d² gcd(a,b) | ab(a+b)` が6点円存在の十分条件かどうかは、この命題からは決まらない。通常格子のK0071とも別の幾何命題。K番号は統合時に衝突確認を要する仮番号。
