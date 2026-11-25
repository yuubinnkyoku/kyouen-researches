---
id: K0410
title: 整数円の拡大族における二重点行数・gcd・短区間構成
kind: proposition
status: proved
topics:
- geometry
- rectangles
- verification
aliases: []
relations: []
artifacts:
- path: research/experiments/fixed-width/reports/scaled-circle-gcd-short-window-and-gcd-20261009.md
  role: proof
  note: 拡大円族の構成と適用境界
- path: research/experiments/fixed-width/scripts/verify_scaled_circle_staircase.py
  role: verifier
  note: 尺度ごとの列挙・gcd検査
- path: research/experiments/fixed-width/scripts/verify_scaled_circle_independent.cpp
  role: verifier
  note: 独立整数点走査
- path: research/experiments/fixed-width/output/scaled_circle_gcd_verification.json
  role: data
  note: Python検査
- path: research/experiments/fixed-width/output/scaled_circle_gcd_verification_cpp.txt
  role: data
  note: C++検査
- path: research/log/2026-10-09-scaled-circle-gcd.md
  role: log
  note: 発見・検証経緯
scope: 研究報告に記載された拡大円族と有限短区間構成
evidence: 平方根による整数点走査、独立Python/C++検査、gcdの厳密計算。
---

拡大円族の整数点と水平二重点行を尺度因子で整理し、各尺度における短区間の二重点行数と行差gcdを記述する。原始族と特定の素因数型を持つ族を分離し、有限区間の証人表を示す。円の整数点は平方根計算で列挙され、独立C++実装とPython階段検査が一致する。

主張は報告された拡大円族の構成に限る。一般のT(w)最適性や全kの最小幅は述べない。証人・検査境界はartifact参照。
