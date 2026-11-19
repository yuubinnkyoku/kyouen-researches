---
id: K1002
title: 2トークン残余ゲーム z=10・y>=6一様Grundy式候補
kind: proposition
status: conjectured
topics: [grundy, residual-games]
aliases: [two-token z10 y-ge6 uniform Grundy conjecture]
relations:
- type: depends_on
  target: K0832
  note: 残余ゲームのA/B/C再帰、Grundy上界、一般tailを使う候補式
artifacts:
- path: research/experiments/vertical-fiber-two-token-z10-y-ge6-census-20261119/report.md
  role: data
  note: z=10・y>=6のT/P/tail一様候補と有限監査・低y境界例外
- path: research/experiments/vertical-fiber-two-token-z10-y-ge6-census-20261119/verify_z10_y_ge6_census.py
  role: verifier
  note: 順序保持・降順正準化の二直接再帰と候補式を比較する有限検証器
- path: research/experiments/vertical-fiber-two-token-z10-y-ge6-census-20261119/output/audit.json
  role: data
  note: 227,562直接照合・20,079 tail照合・不一致0・2回byte-identical
- path: research/log/2026-11-19-vertical-fiber-two-token-z10-y-ge6-census.md
  role: log
  note: z=10の有限センサスと次の帰納証明課題
scope: >-
  κ=1残余ゲームの2トークン族H(R;(x,y);10)、全x>=y>=6・全R>=0について、
  本文と証明報告に記したT/P/tail式が成り立つという予想。全称証明は未取得。
evidence: >-
  y=6..28、d=x-y=0..96、0<=R<=x+y+19の227,562点で、順序保持と降順正準化の
  二直接mex再帰が候補式と一致。不一致0。tail offset 0..8は20,079点で一致し、
  値2位置13,317点、偶数親114,333点・奇数親113,229点でTheorem T上界違反0。
  検証器内2回と別プロセス再実行の監査JSONはbyte-identical。y=1..5の境界走査では
  不一致が22,16,11,7,2件で、y=5は対角線d=0のR=11,13だけが候補から外れる。
  これらは有限計算による支持であり、無界なy,dへの全称性を証明しない。
---

## 命題・範囲

候補はz=10の2トークン残余ゲームで、全 \(x\ge y\ge6\)、全 \(R\ge0\) に対するGrundy値0/1/2の一様閉形式である。値2位置は基本ラダー \(\{1,3,5,7,9\}\) に、d=0,4,8の前倒し点、d=11の掃引奇数帯、d>=12の定常点 \(2y+11\) を加えた集合。値1位置はdの偶奇・小さいdの過渡帯で場合分けされ、tailは \(R\ge x+y+11\) で \((x+y)\bmod2\)。完全な式は証明報告を正本とする。

## 現在の根拠と限界

有限格子で二種類の直接再帰と候補式が一致し、z=7,8,9で観察された前倒し格子・掃引行・定常ピン止め則もz=10で再現した。ただし、これは標本格子上の計算結果であり、全称証明ではない。y=5の対角線にはR=11,13の例外があるため、y>=5へ無条件に延長することもできない。

次の課題は、低yの橋渡しを明示したうえで、A/B/C署名帯表とy強帰納・x外帰納により全y>=6・全dを閉じること。z=10の全Grundy分類は依然として未解決である。
