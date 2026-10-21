---
id: K0484
title: 五行九点版は全長で行容量だけに分離しM_{5,9}=8
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
  target: K0072
  note: 法9平方剰余による連続行の障害と比較
- type: depends_on
  target: K0002
  note: 通常プレイGrundy値の定義
artifacts:
- path: research/experiments/fixed-width/reports/q59-five-row-nine-point-exact-20261016.md
  role: proof
  note: 五連続行の法9障害と全長のGrundy・真の閾値の証明
- path: research/experiments/fixed-width/scripts/q59_no_nine_circle_verify_20261016.py
  role: verifier
  note: 法9全16初期剰余と独立整数行列式円生成の監査
- path: research/experiments/fixed-width/output/q59_no_nine_circle_audit_20261016.txt
  role: data
  note: 六種類の盤長で全円の点数を直接確認した有限結果
- path: research/experiments/knowledge-audit-20261021/README.md
  role: log
  note: 証明の論理監査・再実行範囲・判定
scope: 標準整数格子の連続5水平行、q=9、全m≥1、全安全局面。
evidence: '2026-10-21監査。五行の法9障害と容量8・閾値8を確認。16初期組と6有限盤を再実行。 監査記録: research/experiments/knowledge-audit-20261021/README.md。'
solution:
  board: 5×m・q=9
  level: strong
  outcome: conditional
  classification:
  - root
  - first-moves
  - all-safe-win-loss
  - all-safe-grundy
  coverage: 全m≥1・全安全局面
  conditions: 標準整数格子・q=9,w=5・完全指摘・通常プレイ
  verification:
  - mathematical-proof
  - independent-enumeration
  certificate: 五連続行の平方剰余mod9による全称証明
  independent_check: m=4,5,7,9,12,14の全非共線三点から整数行列式で円を再生成
  note: g=(5min(m,8)−|S|) mod2。m≥8は後手勝ち。M_{5,9}=8
---


標準整数格子の五連続行にある円は、9点の格子点を含めない。したがってq=9の禁止集合は水平直線上の9点のみであり、任意のmと任意の安全局面Sについて

\[
g(S)=(5\min(m,8)-|S|)\bmod2.
\]

全ての極大安全集合は `5min(m,8)` 石。満容量40石への真の安定化長は `M_{5,9}=8`。空盤はm=1,3,5,7で先手勝ち、その他のmでは後手勝ち。

証明は、円の二根の差の平方が五連続行で二階差分−8を満たすことと、法9の平方剰余が `{0,1,4,7}` に限られることによる。最初の四項が平方剰余なら `(1,0,0,1)` しかなく、五項目は3となり矛盾する。二重点行があれば根の和は整数なので、他の占有行の反対側の根も整数になる。9点円は必ず5行を全て通り二重点行を持つため不可能。

全称証明と有限盤の直接円列挙は区別する。任意間隔の平行線やw≥6には主張しない。K0331の五行q=8の安定化長16とは矛盾しない。
