---
id: K0105
title: 11×11の真の空盤勝敗は現在の主要未解決問題
kind: question
status: open
topics:
- square-outcomes
aliases: []
relations:
- type: depends_on
  target: K0023
  note: ''
- type: depends_on
  target: K0028
  note: ''
- type: depends_on
  target: K0312
  note: 最小極大サイズの境界は空盤勝敗と別の確定結果
- type: depends_on
  target: K0313
  note: 最大安全サイズの存在下界は空盤勝敗を決めない
- type: depends_on
  target: K0355
  note: reply27の有限証明境界の進捗。二石rootと空盤の勝敗は未確定
- type: depends_on
  target: K0372
  note: solver/cache 葉への依存の信頼境界を参照
artifacts:
- path: research/log/claim-audit/N11-DFPN-NIGHT-REPORT-2026-09-30.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/n11-search-methods/reports/N11-RESULT.md
  role: source
  note: 層0..5の厳密列挙と層6以降の資源下界
- path: research/experiments/saturation/reports/saturation-20261003.md
  role: source
  note: 8≤s_11≤10の有限完全排除と10石証人
- path: research/experiments/saturation/reports/saturation-20261003-extra.md
  role: source
  note: K_11≥21の独立検査済み安全配置
- path: research/experiments/n11-s6-terminal-loss-20261015/verify_s6_terminal.py
  role: verifier
  note: 固定先手 S6 LOSS の cache-free 終局証明; 483 S10 LOSS 葉, 1,028,621 状態; 6 S5 LOSS 親; 空盤 winner は未確定
- path: research/experiments/n11-s7-fifth-terminal-20261015/fifth_verify_standalone.py
  role: verifier
  note: S7 WIN の第5独立終局証明; 35 S8, 738 S9-S10 辺, 468 S10 葉, 93,481 状態; 空盤 winner は未確定
- path: research/experiments/n11-s9-second-target-20261015/verify.py
  role: verifier
  note: S9 葉 64 件の C++/Python 一致終局検証; 49 LOSS / 15 WIN; 7,629 状態
scope: 標準q=4・完全指摘・通常プレイの11×11空盤勝敗。層列挙・極大サイズ・misère勝敗とは別。
---

# 11×11の真の空盤勝敗は現在の主要未解決問題

標準通常版11×11の真の空盤勝敗はUNKNOWN。厳密な安全局面列挙は層0..5までで、層5には未計算の合法辺2,439,393,194本が残る。層5を終局にした旧DP勝敗は撤回済み。

層6の安全局面数は一般被覆評価でも3,194,106,864以上となり、既存環境での全状態DPは資源上困難。df-pn系探索の局所完了・途中統計は空盤全体の完了を意味しない。

周辺では8≤s_11≤10とK_11≥21が確定している。前者の8・9石極大の有無、後者の真の最大サイズは未確定であり、いずれも空盤勝敗とは別の問題である。

空盤の決着には真の終局まで閉じるAND/OR証明または正しい完了求解が必要。旧one-wordのK_11=11、打切りDP、proof numberを勝敗根拠にしない。

中央初手後のreply27について、保存済みexact境界の回収と現在の検証範囲は[K0355](K0355-n11-reply27-cache-recovery-frontier.md)を参照する。この局所的な進捗から二石rootや空盤の勝敗を推定しない。

[K0372の独立監査](K0372-n11-independent-exact-evidence-trust-audit.md)は上位証明の幾何・伝播とsolver/cache葉への信頼を分離した。少数のterminalまで閉じた独立minimax certificateは得られたが、空盤の証明は未完了であり、この問いのstatusはopenを維持する。

## 2026-10-17 bounded advance

New finite evidence: three local terminal certificates independently verified (all verifiers exit 0): S6 fixed-first LOSS (483 S10 LOSS leaves, 1,028,621 states, 6 S5 LOSS parents); S7 WIN (35 S8, 738 S9-S10 edges, 468 S10 leaves, 93,481 states); S9 leaves 64 (49 LOSS / 15 WIN, C++/Python agree). Saturation bounds 8<=s_11<=10 and K_11>=21 remain separate.

Scope clarification: these are local terminal certificates only; they do not close the empty-board winner or two-stone root. 11x11 empty-board winner remains UNKNOWN; layer 5 still has 2,439,393,194 uncomputed legal edges.

Next steps: integrate first-move branches into a single empty-root KYOENC4 DAG; continue layer-5/6+ DP. Status remains open.

## 2026-10-17 bounded advance (round 2)

New finite evidence: independent audit of local S8/S9 terminal certificate chains on 11x11 standard q=4. S9: 64 terminal leaves (49 LOSS, 15 WIN), 7,629 states; S7 WIN: 35 S8 children, 738 S9-S10 edges, 468 unique S10, 93,481 states; S6 fixed-first LOSS: 483 terminal S10 LOSS leaves, 1,028,621 states; S8 targeted: 171+16 S8 WIN roots and 3 S8 LOSS roots. C++ and Python agreed; SHA-256 consistency checks passed; mutation/negative controls rejected tampered certificates; clean-room reproduction PASS. reuse_certificates.py verification.passed=true.

Scope clarification: local terminal certificates and propagation only; does not close empty-board winner, two-stone root, layer 5 (2,439,393,194 uncomputed legal edges), or saturation bounds 8 <= s_11 <= 10 / K_11 >= 21. K0105 remains open; no solve claimed.

Next steps: continue referencing K0355/K0372 for trust boundaries; optional add S8 verifier artifacts (`research/experiments/n11-targeted-terminal-lift-20261015/scripts/verify_s8_batch_cpp.cpp`, `verify_s8_batch_python.py`, `verify_s8_loss_batch_cpp.cpp`, `verify_s8_loss_batch_python.py`, and `certificates/new_s8_171_terminal.cert`, `new_s8_win_sixteen_terminal.cert`, `new_s8_loss_three_terminal.cert`). Preserve warnings about truncated DP/old win-loss claims. Status remains open.

統合監査（2026-10-20）: 上記2026-10-17の追記はローカル研究時点の報告であり、今回すべての探索・測定を再実行したものではない。再検証の範囲は `research/experiments/local-main-integration-20261020/README.md` に記す。既存の未解決性・量化の限界を維持する。
