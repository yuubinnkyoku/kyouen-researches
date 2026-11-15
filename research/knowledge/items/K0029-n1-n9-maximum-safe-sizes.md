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
- path: research/experiments/n9-k9-upper-sat-20261115/README.md
  role: verifier
  note: F_9両系センサス一致とW9第三系検証・at-least-19 CNF・19石SLS
- path: research/experiments/n9-k9-upper-sat-20261115/scripts/gen_n9_cnf.mjs
  role: verifier
  note: センサス・W9検証・CNF生成・W9充足対照の再現スクリプト
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

## 下界18の第三系検証と上界のSAT準備 (2026-11-15)

F_9=29,152 (共線3,156・共円25,996) を2実装 (差分三角形一次形式・正規化曲線カタログ) で一致させた上で、18石証人W9を第三系で検証した (全禁止四点組への違反0、C(18,4)=3,060組の独立実装4×4整数行列式もすべて非零)。W9は極大で、63空点のどの点を追加しても禁止四点組は3つ以上増える (最小3)。D4軌道は8。

上界は引き続き先行結果の採用であり、K_9=18は未確定として扱う。at-least-19 CNF (1,449変数・34,525節) を生成済みで、W9がat-least-18 CNF (1,386変数・34,274節) を違反0で充足する陽性対照も検証済み (実験記録はartifacts参照)。kissatでge19がUNSATならK_9<=18がrepo内で確定し、SATなら19石証人により先行上界を反証できる。19石SLS (約27,743手・2実行) はE=0に達せず最小E=3 (W9+最小addcost点) で、その1-swap近傍にもE<=2がない。これはヒューリスティックな負の証拠であり、上界を含意しない。
