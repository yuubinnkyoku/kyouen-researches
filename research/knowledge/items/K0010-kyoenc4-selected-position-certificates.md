---
id: K0010
title: KYOENC4による128-bit局面証明とRust独立検査
kind: method
status: active
topics:
- certificates
- verification
- search-methods
aliases: []
relations:
- type: depends_on
  target: K0007
  note: ''
artifacts:
- path: KYOENC4.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: docs/10X10_KYOENC4_EXPORT.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: rust/independent-verifier/KYOENC4_VALIDATION.md
  role: log
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: cpp/solvers/kyouen_solver_10_kyoenc4.cpp
  role: solver
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
---

# KYOENC4による128-bit局面証明とRust独立検査

KYOENC4は128-bit状態を扱うAND/OR証明DAG形式。10×10の4石LOSSで1,784,457ノード、5石LOSSで1,533,310ノードの実証明を生成・独立Rust検査済み。

これは選択された実局面の証明で、10×10空盤面全体の単一証明書ではない。形式・全合法手被覆・局面幅・rank条件を独立検査する範囲はvalidation記録に従う。
