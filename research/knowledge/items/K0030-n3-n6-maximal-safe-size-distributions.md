---
id: K0030
title: 3×3〜6×6の極大安全集合サイズ分布
kind: proposition
status: computed
topics:
- maximal-safe
aliases:
- F-R
- F-S
- F-U
- F-V
- F-AM
- F-P
relations:
- type: depends_on
  target: K0026
  note: ''
artifacts:
- path: research/findings.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: night-research/maximal_spectrum_enum.cpp
  role: solver
  note: 安全性を維持して包含極大全数を列挙
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
---

# 3×3〜6×6の極大安全集合サイズ分布

包含極大な安全集合の全分布は次のとおり。各列はその石数の極大集合の個数で、0は存在しないことを表す。

| 盤面 | 5石 | 6石 | 7石 | 8石 | 9石 | 10石 | 11石 |
|---|---:|---:|---:|---:|---:|---:|---:|
| 3×3 | 56 | 0 | 0 | 0 | 0 | 0 | 0 |
| 4×4 | 176 | 688 | 64 | 0 | 0 | 0 | 0 |
| 5×5 | 4 | 1,136 | 11,280 | 4,340 | 100 | 0 | 0 |
| 6×6 | 0 | 8 | 3,952 | 115,496 | 199,184 | 30,492 | 464 |

6×6の全極大集合は合計349,596個であり、最大11石の464個と異なる。

5×5の最小5石4配置は単一D4軌道、6×6の最小6石8配置も単一D4軌道。分布は有限盤の全数結果で大盤へ外挿しない。
