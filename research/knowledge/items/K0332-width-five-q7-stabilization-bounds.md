---
id: K0332
title: 5×m・q=7の満容量安定化長は19以上158以下
kind: proposition
status: proved
topics: [rectangles, variants, maximal-safe]
aliases: []
relations:
- type: depends_on
  target: K0318
  note: 初期一般上界200とcurve packingの文脈
- type: depends_on
  target: K0072
  note: 五行すべてに整数点を持つ円を排除するmod9補題
- type: depends_on
  target: K0107
  note: 反転した外部石へMelchiorの一般式を適用
- type: depends_on
  target: K0342
  note: 六石行の同和弦energyの鋭い上界29
artifacts:
- path: research/experiments/fixed-width-frontier-20261005/reports/q57-bounds-and-encoding.md
  role: proof
  note: 下界証人・一般上界・完全円生成・未完probeの区別
- path: research/experiments/fixed-width-frontier-20261005/output/q57_independent_witness.json
  role: data
  note: 5×18の29石安全極大証人と全61空点のblocker
- path: research/experiments/fixed-width-frontier-20261005/scripts/q57_witness_check.py
  role: verifier
  note: 全三点曲線生成による独立安全性・極大性検査
- path: research/experiments/fixed-width-frontier-20261005/scripts/q57_geometry.cpp
  role: solver
  note: 片根と接点を含む7/8点円の完全生成
- path: research/experiments/q57-frontier-followup-20261005/proof.md
  role: proof
  note: 同和弦予算174と五点直線Melchior上界による全称上界158
- path: research/experiments/q57-frontier-followup-20261005/scripts/verify_packing.py
  role: verifier
  note: 整数最適化、同和弦の鎖証明、mod9、実blockerの別生成監査
- path: research/experiments/q57-frontier-followup-20261005/output/packing-audit.json
  role: data
  note: 一般energyと有限監査の完了範囲
---

# 5×m・q=7の満容量安定化長は19以上158以下

標準五行整数格子の7点共円・共線禁止版について19≤M_{5,7}≤158。
5×18には行占有数(5,6,6,6,6)の29石安全極大配置が存在するため下界19。
初期上界200を、同和弦充填とMelchiorの数学的証明で158へ改善した。
不足行のblocker円は外部石型2+2+2または2+2+1に限られる。
各外部行の同和弦energy≤29より3x+y≤174、固定対象石中心の反転で
種類2+2+1円は各石22個以下なのでy≤110。従って不足行の利用不能点は
占有5点を含めて157点以下。全m≥158で各不足行に合法手が存在する。
全極大配置は30石、全安全局面はg(S)=(30−|S|) mod2となる。
この全称上界は有限SATのUNSATを根拠にしない。

下界証人は盤内全三点から生成した整数円・直線で独立に安全性を確認し、
全61空点が追加不能であることを具体的blocker付きで確認した。
短時間SATのUNKNOWNや未監査UNSATはこの不等式の根拠に含めない。
M_{5,7}の厳密値、全m≥19での満容量化は未解決である。
