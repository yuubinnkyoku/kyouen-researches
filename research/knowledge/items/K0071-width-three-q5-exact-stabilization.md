---
id: K0071
title: 3×m・q=5の真の満容量安定化長はM_{3,5}=12
kind: proposition
status: proved
topics: [rectangles, variants, grundy]
aliases: [F-BL]
relations:
- type: depends_on
  target: K0024
  note: ''
- type: depends_on
  target: K0078
  note: m=12..39の有限排除とm≥40の一般上界で閾値を閉じる
artifacts:
- path: research/q35-exact-threshold.md
  role: proof
  note: M_{3,5}=12の全証明と全長Grundy分類
  commit: 49891aaf2d402436b9581296ec91b52769e687d6
- path: research/verification/q35_exact_threshold.json
  role: data
  note: m=12..40の完全排除集計
  commit: 49891aaf2d402436b9581296ec91b52769e687d6
- path: research/verification/scripts/q35_independent_audit.cpp
  role: verifier
  note: lifted determinantによる独立円生成監査
  commit: 49891aaf2d402436b9581296ec91b52769e687d6
solution:
  board: 3×m・q=5
  level: strong
  outcome: second-player-win
  classification: [root, first-moves, all-safe-win-loss, all-safe-grundy]
  coverage: m≥12の全安全局面
  conditions: q=5,w=3,m≥12
  verification: [mathematical-proof, exhaustive-enumeration, independent-enumeration]
  certificate: 解析上界m≥40＋m=12..39有限完全排除
  independent_check: 小盤subset DPと独立determinant監査
  note: g(S)=(12-|S|) mod 2
---

# 3×m・q=5の真の満容量安定化長はM_{3,5}=12

3×11には11石の極大安全集合が存在するためM≥12。m≥40では外部三つ組・点対の被覆数上界から不足行に必ず合法点が残る。残るm=12..39は完全列挙で不足極大が0であることを確認した。

したがってM_{3,5}=12。全m≥12・全安全局面Sで全終局は12石となり、g(S)=(12-|S|) mod2。m≤11の全局面計算も合わせると、空盤先手勝ちはm=1,3だけで、全長・全安全局面のGrundy最大値は8。
