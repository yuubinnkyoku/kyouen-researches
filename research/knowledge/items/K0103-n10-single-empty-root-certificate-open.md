---
id: K0103
title: 10×10空盤面全体の単一KYOENC4証明書は未統合
kind: question
status: open
topics:
- certificates
- verification
aliases: []
relations:
- type: depends_on
  target: K0022
  note: ''
- type: depends_on
  target: K0010
  note: ''
artifacts:
- path: docs/PROOF_STATUS.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: rust/independent-verifier/KYOENC4_VALIDATION.md
  role: log
  note: Rust checker validated KYOENC4 10x10 nonempty-root DAG (2 nodes) and unit tests; checker toolchain ready
- path: research/experiments/certificate-validation/reports/VERIFICATION_REPORT.md
  role: source
  note: 1x1-9x9 single-certificate verification boundary; 10x10 remains unintegrated
---

# 10×10空盤面全体の単一KYOENC4証明書は未統合

15代表の100初手分類で空盤勝敗は確定済み。一方、全初手分岐を空盤面から一本のKYOENC4 DAGに統合した検査可能資産はまだない。

これは勝敗未解決ではなく証明パッケージと信頼境界の残件。選択局面の180万ノード級検査をその全体証明に代用しない。

## 2026-10-17 bounded advance

New finite evidence: Rust verifier self-test OK; 10x10 evidence audit OK (4 files, 266 rows, 0 issues); cargo test 9 passed including KYOENC4 nonempty root; C++ and Rust agree on 7x7 empty-root certificate (393,550 nodes, SECOND PLAYER WIN); KYOENC4 10x10 smoke certificate (2 nodes, root WIN) verified. Repository scan found no 10x10 empty-board KYOENC4 certificate.

## 2026-10-17 r2 bounded attempt

Attempted empty-board 10×10 KYOENC4 generation with
`cpp/solvers/kyouen_solver_10_kyoenc4.cpp`. Attempt 1 (shrink=3, load=80)
reached 50,331,648 visited nodes in 216.687 s then failed with `memo table
full`. Attempt 2 (shrink=1, load=90) reached 184,549,376 visited nodes in
581.006 s before the ~10-minute bound. No certificate file was produced, so
no Rust verification was performed. Status remains open. Report:
`research/experiments/local-main-integration-20261020/source/K0103-r2-report.md`.

Next steps: produce/verify a single empty-board 10x10 KYOENC4 DAG. Status remains open.

## 2026-10-17 bounded advance (round 2)

New finite evidence: no 10x10 empty-board KYOENC4 certificate was generated in this bounded attempt (two runs: shrink=3/load=80 reached 50,331,648 visited nodes in 216.687 s then memo table full; shrink=1/load=90 reached 184,549,376 visited nodes in 581.006 s then 10-minute bound). No certificate file produced, so no Rust verification. Observed throughput ~317,000 visited nodes/s. Rust toolchain readiness separately verified: cargo test 9 passed; release binary built.

Scope clarification: bounded negative evidence only; no root outcome recomputed. K0103 remains open; solver throughput is far below what would be needed to complete within ~10 minutes.

Next steps: longer run or improved memo/certification path; verify any future certificate with `rust/independent-verifier/target/release/kyouen-cert-verify`. Status remains open.

統合監査（2026-10-20）: 上記2026-10-17の追記はローカル研究時点の報告であり、今回すべての探索・測定を再実行したものではない。再検証の範囲は `research/experiments/local-main-integration-20261020/README.md` に記す。既存の未解決性・量化の限界を維持する。
