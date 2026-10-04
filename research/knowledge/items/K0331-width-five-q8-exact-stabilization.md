---
id: K0331
title: 5×m・q=8の真の満容量安定化長はM_{5,8}=16
kind: proposition
status: proved
topics: [rectangles, variants, grundy, certificates]
aliases: []
relations:
- type: depends_on
  target: K0072
  note: mod9と円係数の分母から五行の8点円を四行の二点対へ限定する
- type: depends_on
  target: K0318
  note: 無界な末尾m≥186の一般上界を使用
artifacts:
- path: research/experiments/fixed-width-frontier-20261005/reports/q58-exact-threshold.md
  role: proof
  note: 定義・CNF等価性・有限完全排除・無限末尾・下界証人
- path: research/experiments/fixed-width-frontier-20261005/output/q58_finite_certificate_manifest.json
  role: manifest
  note: m=16..185と対象行0,1,2の全510 UNSAT・DRAT検査記録とhash
- path: research/experiments/fixed-width-frontier-20261005/output/q58_independent_audit.json
  role: data
  note: 独立円生成の全集合一致と5×15の34石安全極大証人
- path: research/experiments/fixed-width-frontier-20261005/output/q58_integration_recheck.json
  role: data
  note: 統合時の全510 CNF hash一致と全510 DRAT再検査成功
- path: research/experiments/fixed-width-frontier-20261005/scripts/q58_sat.py
  role: solver
  note: 整数弦差による完全円生成と不足極大のCNF化
- path: research/experiments/fixed-width-frontier-20261005/scripts/q58_certify.py
  role: verifier
  note: CaDiCaLトレースを別実装drat-trimで全て再検査する再現器
- path: research/experiments/fixed-width-frontier-20261005/scripts/q58_geometry_audit.cpp
  role: verifier
  note: 弦差式を使わない同一和二点対の積による独立円生成
- path: research/experiments/fixed-width-frontier-20261005/scripts/q58_independent_check.py
  role: verifier
  note: 全有限長の円集合照合と全三点組による証人検査
solution:
  board: 5×m・q=8
  level: strong
  outcome: first-player-win
  classification: [root, first-moves, all-safe-win-loss, all-safe-grundy]
  coverage: m≥16の全安全局面
  conditions: 標準整数格子・q=8,w=5,m≥16・通常プレイ
  verification: [mathematical-proof, exact-search, independent-enumeration]
  certificate: m=16..185の510 CNFを全DRAT検査、m≥186は曲線充填一般証明
  independent_check: 全有限長の円集合が別C++生成と一致、m=15証人は全三点曲線で検査
  note: g(S)=(35-|S|) mod2。境界3トレースを保存、他はhashと再生成コードを保存
---

# 5×m・q=8の真の満容量安定化長はM_{5,8}=16

標準五行整数長方形盤の8点共円・共線禁止版で、全m≥16の極大安全集合は35石。
従って全安全局面でg(S)=(35−|S|) mod2。空盤は先手勝ちで、全初手が勝ち手となる。

下界は5×15の34石安全極大配置。上界はm=16..185の有限SAT完全排除と、
既存の全称充填上界m≥186を結んでいる。有限部分の全510 UNSATトレースは
solverと独立のdrat-trimで検査した。

円生成は別定式化のC++実装と全有限長で一致し、下界証人は全三点曲線生成で
安全性と全41空点の追加不能を独立確認した。SATトレース検査・円生成は
通常の実装検証境界にあり、Lean核内証明ではない。
m<16の全Grundy分類、q=6,7、標準q=4の五行閾値には主張を拡張しない。
