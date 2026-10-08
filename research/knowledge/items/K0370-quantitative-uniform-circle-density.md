---
id: K0370
title: 連続整数行の円の二重点行数に対する定量的一様上界
kind: proposition
status: proved
topics: [geometry, rectangles, variants]
aliases: []
relations:
- type: depends_on
  target: K0072
  note: 固定幅q点版の独立行帰着
artifacts:
- path: research/experiments/fixed-width/reports/quantitative-uniform-circle-density-20261008.md
  role: proof
  note: 素数定理の算術級数版を用いた全称証明
- path: research/experiments/fixed-width/scripts/verify_quantitative_density.py
  role: verifier
  note: 局所剰余数と中国剰余定理の独立有限検算
- path: research/experiments/fixed-width/output/quantitative_density_verification.txt
  role: data
  note: 局所剰余19099条件とCRT4条件の照合ログ
---

連続する w 本の標準整数水平行で、一本の実円が異なる整数格子点二つずつを持つ行の最大数を T(w) とする。中心・半径は w ごとに任意に変更してよい。

**全称定理（十分大きい w）**:
\[
\boxed{T(w)\le2w\exp(-\tfrac12\sqrt{\log w})}.
\]
自然対数を使う。任意の定数 A>0 について T(w)=O_A(w/(\log w)^A) が従う。

証明は、二重点行の番号差の最大公約数 g による場合分け、3 mod 4 素数の平方剰余条件、中国剰余定理、および**算術級数版素数定理**からなる。数学的導出と外部定理依存はproof artifactに記載。有限検算だけでは無界性を主張しない。

十分大きい w で q>w+2w exp(−sqrt(log w)/2) なら、標準整数格子q点版は全m≥1・全安全局面で
\[
g(S)=(w\min(m,q-1)-|S|)\bmod2,\quad M_{w,q}=q-1
\]
が成立する。開始幅は実効的に指定しない。標準q=4の空盤勝敗、任意間隔の平行線については含意しない。
