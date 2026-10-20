---
id: K0143
title: 2n−O(1)石の安全配置を無限族で作れる
kind: question
status: open
topics:
- maximum-safe
- geometry
aliases:
- B088
relations:
- type: depends_on
  target: K0026
  note: ''
artifacts:
- path: research/experiments/original-claims/reports/round61-full-split-prime-safe-construction.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/archive/hypothesis-ledgers/hypothesis-bank-2026-09-27.md
  role: source
  note: B088の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: 本文の原文量化と現在の採用境界
evidence: 原文監査 PARTIAL / explicit_full_split_prime_linear_construction
---

# 2n−O(1)石の安全配置を無限族で作れる

未確定の命題: 2n−O(1)石の安全配置を無限族で作れる。 有限体上の放物線などの整数化から、共線・共円の両方を避ける格子点族を構成できる。有限体での安全性を整数盤へ移す条件が本体。

現在の結論: p≡1 mod4の全素数でKp≥pの自足構成はあるが、原文の2n−O(1)係数に届いていない。線形下界があることだけで原文を証明済みにしない。

採用境界: p≡1 mod4でa²=-1、(t²+t,a(t²-t))の全p整数代表が安全。四点行列式8a VandermondeでKp≥pを自足証明・独立検算。既知線形下界の再構成、原文2n−O(1)は未達。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。

## 2026-10-17 bounded advance

New finite evidence: dihedral doubling of split-prime set unsafe for p=5,13,17; greedy augmentation reaches ~1.5p (p=5->9, 13->19, 17->25), not 2p. External arXiv:2607.05255 Thm. 1.5 gives non-constructive 2n-o(n) lower bound; suggests (2+lambda)n may be attainable.

Scope clarification: explicit 2n-O(1) family remains open; split-prime stays coefficient 1; 2026 result non-constructive.

Next steps: derandomize hypergraph-matching construction or prove no 2n-O(1) algebraic family. Status remains open.

## 2026-10-17 bounded advance (round 4)

New finite evidence: split-prime construction variants for p=17,29,41. Base set S_p verified safe. Sign doubling S_p ∪ S_{-a}: unsafe for all three (e.g. p=17 forbidden quad (0,0),(2,0),(12,10),(12,12)). All dihedral pairwise unions unsafe (17/29/41). Translations: 0 safe unions (3/1/5 tested). Greedy augmentation reaches ~1.4-1.5p (best totals 26,44,60 vs targets 34,58,82). Random-order greedy best 25/43/58. Coefficient scan for p=17: only b=4,13 (square roots of -1) safe. Largest constructed sets ~1.5p, not 2p.

Scope clarification: negative evidence for direct algebraic doubling routes; split-prime construction remains coefficient 1 for tested primes. K0143 remains open; no 2n-O(1) construction found.

Next steps: other algebraic families or non-doubling constructions. Status remains open.

統合監査（2026-10-20）: 上記2026-10-17の追記はローカル研究時点の報告であり、今回すべての探索・測定を再実行したものではない。再検証の範囲は `research/experiments/local-main-integration-20261020/README.md` に記す。既存の未解決性・量化の限界を維持する。
