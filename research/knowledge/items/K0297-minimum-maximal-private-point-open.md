---
id: K0297
title: n≥2の全最小極大配置に一重被覆点があるか
kind: question
status: open
topics:
- maximal-safe
- geometry
aliases: []
relations:
- type: supersedes
  target: K0138
  note: n=1の退化反例を除外したB078の修正版
- type: depends_on
  target: K0026
  note: ''
artifacts:
- path: research/experiments/original-claims/reports/round47-private-cover-and-global-minima.md
  role: source
  note: n=2..8の全最小極大でmin b=1を完全確認
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/reports/round50-nine-board-private-point-family.md
  role: source
  note: n=9の限定16配置でもmin b=1
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
---

# n≥2の全最小極大配置に一重被覆点があるか

標準n×n盤、n≥2について、最小極大サイズs_nを達成する全ての安全極大配置Sに、`b_S(p)=1` となる空点pが存在するかを問う。これはn=1の空点なし反例を除いたB078の非退化版である。

n=2..8では全最小極大配置を完全列挙し、全件で `min_{p∉S} b_S(p)=1` を確認済み。n=9でも既知の限定16配置では全件成立するが、9×9の全最小極大配置を列挙した結果ではない。

したがって有限範囲の支持は強いが、n≥9を含む一般全称は未証明である。
