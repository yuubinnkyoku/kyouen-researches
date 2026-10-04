---
id: K0029
title: 1×1〜9×9の最大安全サイズの既知値
kind: proposition
status: computed
topics:
- maximum-safe
aliases: []
relations:
- type: depends_on
  target: K0026
  note: ''
artifacts:
- path: docs/RELATED_WORK.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/log/discovery-cycles/CYCLE5_GRUNDY_STRUCTURE.md
  role: source
  note: 小盤・7/8の完全最大探索
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/reports/round55-eighteen-stone-original-counterexample.md
  role: source
  note: 18石証人の独立検算と上界の信頼境界
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
---

# 1×1〜9×9の最大安全サイズの既知値

| 盤面 | 最大安全サイズK_n |
|---|---:|
| 1×1 | 1 |
| 2×2 | 3 |
| 3×3 | 5 |
| 4×4 | 7 |
| 5×5 | 9 |
| 6×6 | 11 |
| 7×7 | 14 |
| 8×8 | 15 |
| 9×9 | 18 |

小盤全数、7×7・8×8の完全最大探索、9×9の先行公開値という根拠の違いを維持する。

本repoの9×9証明書は17石までで下界しか与えない。Round55で先行18石図の安全性を独立に検算したが、その検算自体は上界18や全軌道一意性を証明しない。K_9=18の上界は先行結果の採用である。
