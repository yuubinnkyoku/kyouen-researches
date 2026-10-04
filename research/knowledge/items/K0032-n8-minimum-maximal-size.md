---
id: K0032
title: 8×8の最小極大安全サイズs_8=8
kind: proposition
status: proved
topics:
- maximal-safe
aliases:
- F-BF
- B091
relations:
- type: depends_on
  target: K0026
  note: ''
artifacts:
- path: research/experiments/original-claims/reports/round46-small-saturation-and-window-reduction.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round46_sat_atmost8.json
  role: data
  note: SAT証人の独立検査と有限範囲
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/data/s8_exact.json
  role: data
  note: 7石完全排除記録
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
---

# 8×8の最小極大安全サイズs_8=8

k≤4は三点補完上界、k=5,6,7は各完全探索で排除。安全8石極大の存在と合わせs_8=8。全408安全8石極大が列挙済み。

打切り不発見を非存在証明にせず、完了フラグと幾何の独立検算を根拠とする。9×9の窓還元にもこの完全カタログを用いる。
