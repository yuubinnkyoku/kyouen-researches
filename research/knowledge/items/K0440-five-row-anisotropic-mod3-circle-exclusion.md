---
id: K0440
title: 異方整数格子の五行で9点円は存在せず、3進付値条件下で全長強解決する
kind: proposition
status: proved
topics:
- rectangles
- geometry
- variants
- grundy
aliases: []
relations:
- type: depends_on
  target: K0001
  note: 完全指摘・通常プレイのルール
- type: depends_on
  target: K0002
  note: Grundy値と勝敗の定義
artifacts:
- path: research/experiments/fixed-width/reports/five-row-anisotropic-mod3-20261016.md
  role: proof
  note: 3進付値に基づく無界の全称証明
- path: research/experiments/fixed-width/scripts/verify_five_row_anisotropic_mod3_20261016.py
  role: verifier
  note: 法9の16初期組と14有限盤の整数幾何による独立検査
- path: research/experiments/fixed-width/output/five_row_anisotropic_mod3_audit_20261016.txt
  role: data
  note: 有限盤監査の再現出力
- path: research/experiments/knowledge-audit-20261021/README.md
  role: log
  note: 証明の論理監査・再実行範囲・判定
solution:
  board: 五本の異方整数格子水平行・q点版
  level: strong
  outcome: conditional
  classification:
  - root
  - first-moves
  - all-safe-win-loss
  - all-safe-grundy
  coverage: 全m≥1・全安全局面
  conditions: h,d≥1、v₃(d)≤v₃(h)、q≥9、五本の等間隔水平行
  verification:
  - mathematical-proof
  - independent-enumeration
  certificate: 3進降下法と法9の16剰余組の全称証明
  independent_check: 14種類の有限盤で全非共線三点から円を生成・整数係数で照合
  note: M=q−1、g(S)=(5min(m,q−1)−|S|) mod2
evidence: '2026-10-21監査。二根差平方の差分、法9の16組、接点を持つ場合の3進降下を確認。14有限盤を再実行。 監査記録: research/experiments/knowledge-audit-20261021/README.md。'
---


# 異方格子五行の9点円の不在と全長強解決

任意の正整数 h,d に対し、五本の無限水平格子
`{(x₀+hj,t+di):j∈Z,0≤i≤4}` 上に**ちょうど9点**を持つ円は存在しない。

さらに `v₃(d)≤v₃(h)` なら円は高々8点なので、q≥9の有限盤では禁止q点集合は水平直線上のものに限る。全m≥1・全安全局面で

`g(S)=(5min(m,q−1)−|S|) mod2`、真の満容量安定化長は `M=q−1`。

証明は水平二根の整数和から弦差平方の二階差分を導き、3進付値による場合分けと法9平方剰余の16組完全検査で閉じる。有限の14盤検査は支持資料であり、全称性の根拠ではない。

`v₃(d)>v₃(h)` では10点円の存在は未確定。有限盤がそのうち9点だけを切り取る可能性があるため、上記の強解決式をこの場合に拡張しない。
