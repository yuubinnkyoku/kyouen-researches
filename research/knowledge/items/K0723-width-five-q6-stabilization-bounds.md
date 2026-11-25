---
id: K0723
title: 5×m・q=6の満容量安定化長は16以上249以下
kind: proposition
status: proved
topics: [rectangles, variants, maximal-safe]
aliases: []
relations:
- type: depends_on
  target: K0318
  note: 曲線充填上界への(5,6)代入による一般上界249
- type: depends_on
  target: K0024
  note: より弱い初期上界T=2965は参考
artifacts:
- path: research/experiments/q56-five-row-20261110/report.md
  role: proof
  note: 下界証人・blocker・上界代入・限界
- path: research/experiments/q56-five-row-20261110/output/q56_witness_5x15.json
  role: data
  note: 5×15の24石安全極大証人と全51空点のblocker記録
- path: research/experiments/q56-five-row-20261110/scripts/q56_witness_check.ts
  role: verifier
  note: 全三点組・整数行列式による独立安全性・極大性・上界検査
---

# 5×m・q=6の満容量安定化長は16以上249以下

標準五行整数格子の6点共円・共線禁止版について16<=M_{5,6}<=249。
q>2wの全長定理の外側で、repoに個別の明示的境界の記録がなかった
(w,q)=(5,6)の空白を埋める最初の両側境界である。

下界16: 5×15に行占有(5,5,5,5,4)の24石安全極大配置が存在する。
全石三点組から生成した盤内円353本と全点対直線のいずれにも石数5以下。
51空点すべてが追加不能（y=0..3は行満杯、y=4の11空点は5石blocker円）。
検査は整数演算のみ（4x4 Bareiss、gcd約分）で独立実行し PASS。

上界249: K0318の曲線充填上界への(5,6)代入。N=20, Q=1100, d0=10,
d1=4, P=150, e=4, Y=124、整数最適化でH=244、U=5+244=249。
この上界は有限SATのUNSATを根拠にしない。

予想M_{5,6}=16（M_{4,6}=16との類推）は予想としてのみ記録し、
境界の根拠に含めない。厳密値は未解決である。
