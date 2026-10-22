---
id: K0515
title: 軸平行長方形4点禁止版7×mの最大安全石数と三角形分解一般則
kind: proposition
status: proved
topics: [variants, rectangles, maximum-safe, geometry]
aliases: []
relations:
- type: depends_on
  target: K0026
  note: 最大安全石数の定義
- type: depends_on
  target: K0504
  note: 軸平行長方形だけを禁止する規則の区別
artifacts:
- path: research/experiments/axis-rectangle-seven-20261023/report.md
  role: proof
  note: 7行の全長公式と三角形分解条件付き一般定理の全称証明
- path: research/experiments/axis-rectangle-seven-20261023/verify.py
  role: verifier
  note: m<=6の独立完全動的計画とm<=40の構成検査
- path: research/experiments/axis-rectangle-seven-20261023/results.json
  role: data
  note: 独立計算結果
scope: 軸平行長方形4点禁止、7行の全m、および辺素三角形分解を持つ幅
evidence: 数学的全称証明。有限検算は独立した支持資料
---

# 7×mの最大安全石数と三角形分解

軸平行長方形の4頂点だけを禁止する変種で、最大安全石数は任意の整数 m≥1 について

- 1≤m≤4: K_rect(7,m)=7+C(m,2)
- 5≤m≤6: K_rect(7,m)=3m
- 7≤m≤21: K_rect(7,m)=m+floor((m+21)/2)
- m≥21: K_rect(7,m)=m+21。

一般化：K_wのE=C(w,2)辺をt=E/3個の辺素三角形に分解できる場合、全m≥tで、m≤EならK_rect(w,m)=m+floor((E+m)/2)、m≥EならK_rect(w,m)=m+E。分解の存在は仮定であり、全幅への無条件主張ではない。

上界は各列が使う行対の非重複とC(a,2)≥a−1、C(a,2)≥2(a−1)−1による。下界は辺素三角形・未使用辺・単石列を使う構成。7行では012,034,056,135,146,236,245が全21行対を分割する。m≤6は転置上界で閉じる。数学的全称証明であり、有限実験を無限範囲に外挿していない。

[詳細証明と再現方法](../../experiments/axis-rectangle-seven-20261023/report.md)。標準の共円・共線禁止とは異なる規則。
