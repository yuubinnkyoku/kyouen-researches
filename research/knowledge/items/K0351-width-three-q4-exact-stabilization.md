---
id: K0351
title: 3×m・q=4の真の満容量安定化長はM_{3,4}=24
kind: proposition
status: proved
topics: [rectangles, variants, grundy]
aliases: []
relations:
- type: depends_on
  target: K0024
  note: 固定幅q点版の一般的な満容量安定化枠組み
artifacts:
- path: research/experiments/fixed-width/reports/q34-exact-threshold.md
  role: proof
  note: M_{3,4}=24の全証明、全長の空盤Grundy分類、例外下方閉包補題
- path: research/experiments/fixed-width/output/q34_exact_threshold.json
  role: data
  note: m=24..68の不足極大配置完全排除集計
- path: research/experiments/fixed-width/scripts/q34_independent_audit.cpp
  role: verifier
  note: lifted determinantによる独立円生成監査とm=23証人検査
- path: research/experiments/fixed-width/scripts/q34_exceptional_audit.cpp
  role: verifier
  note: 短い終局・例外下方閉包・mex遷移の独立監査
solution:
  board: 3×m・q=4
  level: strong
  outcome: first-player-win
  classification: [root, first-moves, all-safe-win-loss, all-safe-grundy]
  coverage: m≥24の全安全局面
  conditions: q=4,w=3,m≥24
  verification: [mathematical-proof, exhaustive-enumeration, independent-enumeration]
  certificate: m≥69の解析上界＋m=24..68有限完全排除＋m=23不足極大証人
  independent_check: lifted determinant監査、m=7全安全局面直接照合、m=7と23の例外遷移監査
  note: g(S)=(9-|S|) mod 2
---

# 3×m・q=4の真の満容量安定化長はM_{3,4}=24

標準三行盤では、全極大安全集合が9石になる最小の安定化長は

\[
M_{3,4}=24
\]

である。m≥69は外部三つ組と点対が不足行上で塞げる点数の一般上界から従う。残るm=24..68は一行被覆問題へ正確に縮約した完全列挙で不足極大配置が存在しない。m=23には8石の極大安全集合があり、lifted determinantを直接使う独立検証器でも安全性と極大性を確認している。したがって境界24は鋭い。

よって全m≥24・全安全局面Sで終局までの手数は常に9-|S|で、

\[
g(S)=(9-|S|)\bmod 2.
\]

一次資料では短い極大集合の下方閉包だけを解く補題も用い、全正整数mの空盤Grundy数を

\[
g(\varnothing)=
\begin{cases}
0,&m\in\{2,5,8\},\\
2,&m\in\{4,7,9\},\\
1,&\text{otherwise}
\end{cases}
\]

と分類している。したがって空盤の後手勝ちはm=2,5,8だけである。全長・全安全局面を通じたGrundy値の最大値は6で、m=7に値6の具体局面がある。

安定化概念は一致しない。空盤先手勝ちはm≥9、空盤Grundy値1はm≥10、全初手勝ちはm≥11で安定する一方、全極大集合9石・全局面の容量偶奇式が安定するのはm≥24である。

無限末尾は数学的証明、m=24..68の排除と短盤分類は有限完全列挙、乱択標本は実装の独立監査であり、これらを同じ証拠水準として扱わない。
