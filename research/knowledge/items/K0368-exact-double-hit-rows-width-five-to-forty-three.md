---
id: K0368
title: 標準整数格子円の二重点行数の厳密最大値（5〜43行）
kind: proposition
status: proved
topics:
- geometry
- rectangles
- variants
aliases: []
relations:
- type: depends_on
  target: K0367
  note: 有理係数と行番号差gの合同帰着
- type: depends_on
  target: K0072
  note: q点版の独立行公式
artifacts:
- path: research/experiments/fixed-width/reports/prime-modular-uniform-sublinear-density.md
  role: proof
  note: 有限合同完全排除と達成円、gcd例外の証明
- path: research/experiments/fixed-width/scripts/verify_exact_double_rows_5_43.py
  role: verifier
  note: 二方式の剰余集合照合と具体的円の整数検算
---

# 5〜43行の厳密二重点行数

T(w) は連続する w 本の整数水平行のうち、同じ一本の実円が2整数格子点を含む行の最大数。

| w | T(w) |
|---|---:|
| 5〜6 | 4 |
| 7 | 5 |
| 8〜10 | 6 |
| 11 | 7 |
| 12〜21 | 8 |
| 22 | 9 |
| 23〜24 | 10 |
| 25 | 11 |
| 26〜42 | 12 |
| 43 | 13 |

上界：gcd g が1か2ならば g と互いに素な各法の必要平方剰余条件を二つの独立構成で完全排除する。g=3 が残り得る37〜43行では、mod 11 の二重点行許容剰余類が高々7個なのに対象行集合には少なくとも9種類必要であることから排除する。

下界：整数円 x²+y²+x−3y=0, x²+y²+x−7y=0, x²+y²+x−11y−2=0, x²+y²+x−25y−6=0, x²+y²+x−47y=0 のうち各幅に応じたものが上界を達成する。整数根・円方程式への代入を検査する。従って w=14 では T(14)=8 であり、w=14 の半密度上界は偽、既証明の w≥15 が最良の開始幅。

任意の w=42a+r（0≤r<42）では分割によって T(w)≤12a+T(r)（T(0)=0、T(1..4)=1..4）。よって q>w+12a+T(r) は全長強解決の明示的な十分条件。幅44〜63の別の厳密値は K0369 に記録する。
