---
id: K0102
title: 具体巨大証明書をLean核のみで検査する実装は未完成
kind: question
status: open
topics:
- formalization
- certificates
aliases: []
relations:
- type: depends_on
  target: K0009
  note: ''
artifacts:
- path: docs/PROOF_STATUS.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: Kyouen/CertificateSoundness.lean
  role: lean
  note: 一般健全性定理。具体証明書の受理を意味しない
- path: Kyouen/SmallCertificates.lean
  role: lean
  note: 1×1正方盤の具体証明書検査
- path: Kyouen/CubeCertificate.lean
  role: lean
  note: 3×3×3・5点禁止の有界具体証明書検査。native_decide 依存あり
- path: research/experiments/certificate-validation/reports/VERIFICATION_REPORT.md
  role: source
  note: 9×9証明書の外部C++検査記録
---

# 具体巨大証明書をLean核のみで検査する実装は未完成

一般健全性はLeanで形式化されているが、具体binary証明書のparseと全局所条件は外部C++/Rustに依存する。具体証明書をLean核のみで最後まで検査する開発は残件。

単にLeanがビルドできることを具体9×9勝敗の核検査完了とは表現しない。

## 2026-10-17 bounded advance

New finite evidence: `lake build` and `lake build Kyouen.CubeCertificate` succeed; check.py 430 items 0 errors. Concrete Lean checks exist for 1x1 square and 3x3x3 five-point cube (839 masks, native_decide). 9x9 certificate not represented in Lean (13,457,134 nodes, ~206 MiB).

Scope clarification: open item is concrete huge-certificate path, not abstract soundness theorem. Lean buildability alone does not imply 9x9 kernel-checked.

## 2026-10-17 round 2 bounded advance

Feasibility/cost assessment for a 9×9 certificate in Lean: 13,457,134 nodes; projected ~237 MB source and ~42.6 GB `.olean` using the most compact measured baseline (cube: 839 nodes). A 9,994-node 3×3 square certificate did not finish building in 10 minutes. New prototype: `Kyouen/SquareCert2x2.lean` (41 positions) builds in 4.1 s and proves `certValidBool = true` plus `empty_board_winning`. This does not cover 3×3 or 9×9; K0102 remains open. Details: `research/experiments/local-main-integration-20261020/source/K0102-r2-report.md` (session scratchpad).

Next steps: implement another bounded square case (3x3) in Lean without claiming 9x9 coverage; investigate compact/imported representations. Status remains open.

## 2026-10-17 bounded advance (round 2)

New finite evidence: 9x9 certificate has 13,457,134 nodes (4,630,676 losing + 8,826,458 winning); measured Lean baselines: cube 839 nodes (14,782 B source, 2,657,976 B .olean, 27.8 s), 2x2 41 nodes (9,054 B, 356,040 B, 4.1 s), 3x3 9,994 nodes did not finish in 10 min. Extrapolation: ~237 MB source, ~42.6 GB .olean, ~78 h check (optimistic). New prototype `Kyouen/SquareCert2x2.lean` (41 positions) builds in 4.1 s and proves `certValidBool = true` and `empty_board_winning`.

Scope clarification: concrete 9x9 certificate in Lean remains infeasible on the measured trajectory; external C++/Rust checker remains the practical verification path. K0102 stays open; this is feasibility/cost evidence, not 9x9 coverage.

Next steps: implement another bounded square case (3x3) without claiming 9x9 coverage; investigate compact/imported representations. Status remains open.

## 2026-10-17 bounded advance (round 3)

New finite evidence: no 9x9 KYOENC4 certificate artifact exists in the workspace (whole-workspace binary scan found zero KYOENC4 files; only KYOENC3 certificates present). Rust verifier is ready and accepts 9x9 KYOENC4: `cargo test --release` 9 library + 2 reference tests passed; self-test OK; 7x7 KYOENC3 (393,550 nodes) verified in 2.94 s. Synthetic 9x9 two-node KYOENC4 probe verified (`nodes=2`, `forbidden=29152`, root WIN). Full 9x9 empty-board KYOENC4 would be ~13.46M nodes, ~323 MB, with 1-2 GB in-RAM index; generation requires extending a 10x10-only KYOENC4 solver.

Scope clarification: format and verifier support 9x9; absence of an artifact and generation path keeps K0102 open. Estimates are not measurements of a full 9x9 KYOENC4 build/check.

Next steps: produce or obtain a selected-position 9x9 KYOENC4 DAG and verify it; consider streaming/chunked indexing for 13.4M nodes. Status remains open.

統合監査（2026-10-20）: 上記2026-10-17の追記はローカル研究時点の報告であり、今回すべての探索・測定を再実行したものではない。再検証の範囲は `research/experiments/local-main-integration-20261020/README.md` に記す。既存の未解決性・量化の限界を維持する。
