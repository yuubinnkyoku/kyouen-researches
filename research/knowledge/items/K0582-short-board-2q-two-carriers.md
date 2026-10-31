---
id: K0582
title: 平面q点禁止ゲームのN=2q・q≥7は七つの二担い手型に分類でき全安全局面を二次時間で強解決できる
kind: proposition
status: proved
topics: [geometry, variants, grundy, residual-games, first-moves, maximal-safe, strategy-length]
aliases: []
relations:
- type: depends_on
  target: K0001
  note: 完全指摘・安全追加ルール
- type: depends_on
  target: K0002
  note: 通常Grundy数とmisère補助値の定義
artifacts:
- path: research/experiments/short-board-2q-20261031/proof.md
  role: proof
  note: 担い手の七型分類、整数格子実現、四変数再帰の全称正当性、極大配置計数とq=6の反例
- path: research/experiments/short-board-2q-20261031/verify.py
  role: verifier
  note: q=7,8の557748全安全局面の独立mex照合、整数幾何判定、q≤50の極大配置計数検証
scope: q≥7、相異なるN=2q個の実平面点、共円または共線q点禁止、通常・misère二人ゲーム、全安全局面
evidence: 三担い手の包除下界3q−6>2q、二担い手の交差≤2、置換対称性による四変数mex再帰を数学的に証明。整数格子上の全型実現と極大配置数を導出し、独立全局面再帰で検証。
---

# N=2qの七型分類と強解法（q≥7）

担い手（q点以上含む円・直線）は高々二本。二本の場合、各担い手の点数(a,b)と共有点数cは

\[
(q,q,0),(q,q,1),(q,q,2),(q+1,q,1),(q+1,q,2),(q+1,q+1,2),(q+2,q,2)
\]

の七型に限られ、すべて整数格子で実現できる。禁止q点組数は

\[
f\in\{0,2,q+2,2(q+1),\binom{q+2}{2}+1\}
\cup\{\binom mq:q\le m\le2q\}.
\]

担い手なし・一本は全終局長が固定し、通常・misère値は残手数の偶奇で決まる。二本の場合も、両担い手の固有点、共有点、外部点の占有数を用いた**高々9(q+3)²状態の厳密mex再帰**により、すべての安全局面の通常Grundy数・misère補助値・勝ち初手を計算できる。七型の極大安全集合の石数別個数も閉形式で決定した（証明本文に表を掲載）。任意人数の終局履歴分布もそこから計算可能。

q=6、N=12では三担い手の明示的な有理点反例があり、q≥7という境界は鋭い。q=7,8の七型について557,748安全局面を独立の占有ビット集合再帰と照合し、不一致0。

**留保**：空盤の七型Grundy値について q=7..50 の一部で共通パターンを観測したが、無界qにわたる値の閉公式は未証明。本項の全称主張は七型分類、全型実現、二次時間の厳密強解法、極大配置計数であり、観測した空盤値を無界定理とはしない。既存の大盤の任意の残局には無条件適用しない。
