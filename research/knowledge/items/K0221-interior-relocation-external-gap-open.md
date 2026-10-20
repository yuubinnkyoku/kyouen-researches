---
id: K0221
title: 内側の石を動かすだけで盤外の最初の合法点が遠くへ飛ぶ
kind: question
status: open
topics:
- maximum-safe
- geometry
aliases:
- B390
relations:
- type: depends_on
  target: K0026
  note: ''
artifacts:
- path: research/experiments/original-claims/reports/round16-dilation-exterior.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/archive/hypothesis-ledgers/hypothesis-bank-round2-2026-09-27.md
  role: source
  note: B390の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round16_first_appearance.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/scripts/round16_first_appearance.py
  role: verifier
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: 有限安全Sを整数平面へ固定し、盤の外でも4点共円・共線だけで合法性を定める。r(S)はSの最小軸平行外接矩形からのChebyshev距離が最小の、追加可能な外点の距離。
evidence: 原文監査 PARTIAL / finite_evidence_and_partial_general_result
---

# 内側の石を動かすだけで盤外の最初の合法点が遠くへ飛ぶ

未確定の命題: 内側の石を動かすだけで盤外の最初の合法点が遠くへ飛ぶ。 同石数の一石移動S→Tで、r(T)−r(S)を任意に大きくできる族がある。

適用文脈: 有限安全Sを整数平面へ固定し、盤の外でも4点共円・共線だけで合法性を定める。r(S)はSの最小軸平行外接矩形からのChebyshev距離が最小の、追加可能な外点の距離。

現在の結論: 拡大後r=1は最大性・最小極大性・一石移動を保存せず、原文は未決着。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。

## 2026-10-17 bounded advance

New finite evidence: one-stone relocations on n=6 maximum sets (464 sets): broad 608 safe relocations, max delta-r=+1 (1->2); strict interior box-preserving 16 moves max delta-r=0. n=7 maximum sets: 0 safe relocations. 11x11 10-stone maximal: 104 safe relocations all r'=1. Random small sets: delta-r<=+1. Prior B390: 8-stone maximal 1-swap delta-r in {0,+1}.

Scope clarification: finite evidence does not support unbounded interior jump; consistent with prior weak refutation. Strict interior relocations show delta-r=0 in tested maximal/maximum sets.

Next steps: construct proof of boundedness or growing family. Status remains open.

統合監査（2026-10-20）: 上記2026-10-17の追記はローカル研究時点の報告であり、今回すべての探索・測定を再実行したものではない。再検証の範囲は `research/experiments/local-main-integration-20261020/README.md` に記す。既存の未解決性・量化の限界を維持する。
