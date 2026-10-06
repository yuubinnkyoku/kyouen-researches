---
id: K0068
title: 標準q=4固定幅盤はm≥3+2{C(3w−2,3)−(w−1)}で全局面偶奇式
kind: proposition
status: proved
topics:
- rectangles
- grundy
aliases:
- B212
- B215
- B216
relations:
- type: depends_on
  target: K0024
  note: ''
- type: supports
  target: K0302
  note: 本項の下界証人M_{3,4}>=24はK0302の確定値24と一致する。一般定理の上界69は十分長であり真の値ではない
- type: refutes
  target: K0154
  note: 本文の証明・証人が原文に与える帰結
- type: refutes
  target: K0155
  note: 本文の証明・証人が原文に与える帰結
- type: refutes
  target: K0262
  note: 本文の証明・証人が原文に与える帰結
- type: refutes
  target: K0263
  note: 本文の証明・証人が原文に与える帰結
artifacts:
- path: research/experiments/original-claims/reports/round4-fixed-width.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/fixed-width/scripts/q34_independent_recheck.py
  role: verifier
  note: 3種の独立判定で証人・T_w・m=6列挙行を独立に再現
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/fixed-width/reports/q34-independent-audit-2026-10-04.md
  role: log
  note: 独立監査記録とK0068の記述訂正の根拠
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
solution:
  board: w×m・標準q=4
  level: strong
  outcome: conditional
  classification:
  - root
  - first-moves
  - all-safe-win-loss
  - all-safe-grundy
  coverage: 全安全局面
  conditions: w固定、m≥T_w=3+2{C(3w−2,3)−(w−1)}
  verification:
  - mathematical-proof
  certificate: 全称証明
  independent_check: 有限長方形検算は支持
  note: g=(3w−|S|) mod2
---

# 標準q=4固定幅盤はm≥3+2{C(3w−2,3)−(w−1)}で全局面偶奇式

w固定、T_w=3+2{C(3w−2,3)−(w−1)}とする。m≥T_wなら全極大集合は3w石で、全安全局面のg(S)=(3w−|S|) mod2。
幅w=1〜6の十分長さT_wは順に 3, 9, 69, 237, 567, 1,113。

全局面強解決の一般証明で、真の最小開始長はこの上界とは限らない。幅3の最終非周期性・固定幅の部分勝ち初手が無限にあるという予想を否定する。

## 幅3・q=4の鋭い値

一般上界69は現在もこの命題の全称証明として有効だが、幅3については後続の完全排除により真の最小開始長まで閉じている。

\[
\boxed{M_{3,4}=24}.
\]

m=23 には8石の極大安全集合が存在する。具体的には、

\[
\begin{aligned}
y=0 &: \{4,15,18\},\\
y=1 &: \{18,19\},\\
y=2 &: \{9,12,18\}.
\end{aligned}
\]

この証人の70個の四点部分集合には禁止組がなく、残る61空点はすべて追加不能である。したがって \(M_{3,4}\ge24\) である。

一方、m=24..68 は有限完全列挙で不足極大集合が排除され、m≥69 は上の一般証明が覆う。したがって m≥24 の全安全局面で
\(g(S)=(9-|S|)\bmod2\) が成立する。

証明・独立監査・全長のGrundy分類は [K0302](K0302-fixed-width-five-exact-stabilization-thresholds.md) と [q34-exact-threshold.md](../../experiments/fixed-width/reports/q34-exact-threshold.md) を参照する。
