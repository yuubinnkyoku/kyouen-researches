---
id: K0113
title: 負け初手後のnimberは奇数
kind: question
status: open
topics:
- residual-games
- first-moves
aliases:
- B006
relations:
- type: depends_on
  target: K0108
  note: ''
artifacts:
- path: research/experiments/original-claims/reports/round28-seven-board-original-verdicts.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/archive/hypothesis-ledgers/hypothesis-bank-2026-09-27.md
  role: source
  note: B006の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round28_n7_audited.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round28_n7_layers.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round28_n7_independent.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/n8-grundy-layer-profiles-20261101/output/n8_analysis.json
  role: data
  note: 2026-11-03 n=8全局面再走による一石層ヒストグラム（値{1:12点,3:52点}）と独立検算
scope: 本文の原文量化と現在の採用境界
evidence: 原文監査 PARTIAL / finite_complete_classification
---

# 負け初手後のnimberは奇数

未確定の命題: 負け初手後のnimberは奇数。 標準正方形盤の1石局面では非零gはすべて奇数。5×5の値3を、値そのものではなく偶奇へ弱めて延長する。

現在の結論: n≤8で一石の非零値は奇数。特にn7は全49点でg=1、n8は {1（12点）, 3（52点）} のみ。n≥9一般の一石Grundy値をこの検査から推論しない。

採用境界: 8×8までの一石・飽和・J・空盤WFTを完全検査したが、原文の無界全称は未証明。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。

## 2026-10-17 bounded advance

New finite evidence: exact Grundy enumeration for small boards validates geometry (n=4 forbidden count 194). Standard square boards n<=7: losing first moves have odd one-stone Grundy (n=4:1, n=5:3, n=7:1); n=2,3,6 have none. Rectangular counterexample 2x5 has even losing first moves (g=2), supporting standard-square scope restriction.

Scope clarification: n=8 all first moves losing but one-stone Grundy values not retained in stored artifacts. Universal unbounded claim unproved.

Next steps: rerun n=8 streaming DP with per-layer Grundy histograms. Status remains open.

## 2026-10-17 bounded advance (round 3)

New finite evidence: bounded attempt to compute exact empty 8x8 Grundy did not terminate within 15-minute bound using `grundy_cycle5` (forbidden quads 14,564; ~5-6 min, peak ~1.1 GB, no output). Capped sanity: <=4 stones evaluates 664,557 positions, empty Grundy 0, all 64 one-stone positions Grundy 1 (odd), max Grundy 1. Capped <=6 stones ran ~2 min then terminated, no output.

Scope clarification: capped values are not exact and cannot establish parity for full game; reported as bounded evidence only. K0113 remains open; no value fabricated.

Next steps: exact computation requires more time/memory or optimized solver. Status remains open.

統合監査（2026-10-20）: 上記2026-10-17の追記はローカル研究時点の報告であり、今回すべての探索・測定を再実行したものではない。再検証の範囲は `research/experiments/local-main-integration-20261020/README.md` に記す。既存の未解決性・量化の限界を維持する。

## 2026-11-03 bounded advance（n=8完全再計算）

8×8の全6,700,711,937安全局面を別実装（grundy専用ストリーミングDP）で再走査し、一石層の完全なGrundyヒストグラムを取得した。n=8は後手勝ち盤（K0018、再走で空盤g=0を再確認）で、全64初手が負け手である。一石局面の非零Grundy値は **{1（12点）、3（52点）} のみで、すべて奇数**。

Scope clarification: n≤8の有限盤の完全な分類であり、無界全称は証明しない。n≥9一般の一石Grundy値をこの検査から推論しない。statusはopenのまま。
