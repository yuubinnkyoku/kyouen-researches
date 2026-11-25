---
id: K0281
title: 7×7二相選択を制約solverなしの幾何だけで導く証明は未完成
kind: question
status: open
topics:
- maximum-safe
- geometry
aliases: []
relations:
- type: depends_on
  target: K0051
  note: ''
- type: depends_on
  target: K0269
  note: ''
artifacts:
- path: research/archive/discovery-summaries/FINAL_SELECTION_THEOREM.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: results/K0281_residual_witnesses.json
  role: certificate
  note: 本報告の witness 抽出結果 (exact decision + drop-one + witness quad)
- path: results/cycle34_occupancy_lattice_certificate.json
  role: certificate
  note: 既存の残差認証
- path: results/cycle40_compressed_inequalities.json
  role: certificate
  note: 既存の残差認証
- path: results/cycle40b_residual_joint_lemmas.json
  role: certificate
  note: 既存の残差認証
---

# 7×7二相選択を制約solverなしの幾何だけで導く証明は未完成

軌道共円性の局所上限と有限認証済み骨格容量・相拡張はあるが、全てのcross-shell容量・七残余例外・相liftを短い一般幾何から導いたわけではない。

全K_nの2n現象の理論説明や他盤への相構造一般化は現在のCOMPLETE有限核を越える。計算機援用定理の正当性と、solver依存を外す問いを区別する。

## 2026-10-17 bounded advance

New finite evidence: residual witness extraction re-run; 7 residual vectors with first-fail orbit (0,2) or (1,2) and binding coordinates recorded. Named phase-exclusivity quads listed (B-core+center, A-core+B-bundle elements, center+B-bundle 360 quads). Capacity decomposition M only=13, M+center=14, M+B-bundle=14 recorded.

Scope clarification: exact decision is COMPLETE but short geometric proof (named-quad cover) not yet achieved; proper-subset capacities and phase lift still solver-dependent.

Next steps: convert residual witnesses to named-quad family covers; derive proper-subset capacities geometrically. Status remains open.

## 2026-10-17 bounded advance (round 2)

New finite evidence/analysis: classified existing cycle logs into universal vs n=7-specific components. Universal: forbidden 4-set definition (D0) and orbit-circle lemma (D1/G1, all n odd/even) with o_i <= 3. n=7-specific: empty orbit (2,2) at max (D2), six-skeleton M with alpha(M)=13 (D3), phase lift/exclusivity (D4), 16 configurations/2 occupancy vectors (D5), K_7=14=2n. Other boards: n=4 K=2n-1, n=5 9 vectors, n=6 22 vectors, n=8 flexible; K_n=2n only for n=7 in known range. Enumeration counts: mandatory orbits n=4 3, n=5 4, n=6 4, n=7 6; occupancy vectors at max n=4 4, n=5 9, n=6 22, n=7 2.

Scope clarification: K0281 remains open; generalization requires re-deriving M, empty-orbit property, capacity tables, occupancy lattice, phase lift, census, and K_n for each n. No new theorem or numeric proof added.

Next steps: follow roadmap (universal reuse, generalized M, empty-orbit verification, capacity decomposition, occupancy lattice, phase lift, census, K_n determination). Status remains open.

統合監査（2026-10-20）: 上記2026-10-17の追記はローカル研究時点の報告であり、今回すべての探索・測定を再実行したものではない。再検証の範囲は `research/experiments/local-main-integration-20261020/README.md` に記す。既存の未解決性・量化の限界を維持する。
