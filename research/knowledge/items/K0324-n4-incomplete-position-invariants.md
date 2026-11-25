---
id: K0324
title: 4×4では幾何・局所手・極大拡張の各集計が一致しても勝敗が異なる
kind: proposition
status: computed
topics: [grundy, geometry, residual-games, maximal-safe]
aliases: [B291, B292, B293, B294, B295, B296, B298]
relations:
- type: depends_on
  target: K0001
  note: 標準4×4・通常プレイ
artifacts:
- path: research/experiments/original-claims/scripts/round69_scope_witness_check.py
  role: verifier
  note: 全5811安全集合・928極大・64最大から原文の条件を再検算
- path: research/experiments/original-claims/output/round69_scope_witness_check.json
  role: data
  note: B291–B296とB298の一致特徴と異なるg
- path: research/experiments/original-claims/reports/round69-b251-b300-original-scope-audit.md
  role: source
  note: 旧コードの代理指標を原文条件に修正
---

# 4×4では幾何・局所手・極大拡張の各集計が一致しても勝敗が異なる

点ID=4y+x。以下の各行は別の反例であり、全特徴が同時に一致する一対という主張ではない。

|旧ID|P集合|N集合|一致する情報|g(P),g(N)|
|---|---|---|---|---|
|B291|{1,2,4,5}|{1,2,3,4}|k4、最小絶対円判定行列式2、合法5、占有点の初期禁止次数和215|0,2|
|B292|{0,1,4,6}|{0,2,4,5}|k4、距離平方多重集合[1,1,2,2,4,5]、境界距離[0,0,0,1]|0,3|
|B293|{0,2,3,5}|{0,2,3,4}|k4、三点補完数多重集合[0,1,1,3]|0,3|
|B294|{2,3,4,5}|{0,1,3,8}|k4、合法9、全子の合法数多重集合[1,1,3,3,3,4,5,5,5]|0,3|
|B295|{0,1,5,6}|{0,3,4,5}|k4、全サイズ別極大拡張個数（六石6・七石2）|0,3|
|B296|{0,1,2,4}|{0,2,3,4}|k4、j=1..3のP部分集合個数[0,4,0]|0,3|
|B298|{1,3,9}|{0,1,2}|k3、合法12。P側最大七石拡張4対0、残容量4対3で両方多い|0,1|

初期次数d(p)は全禁止四点族内の次数。動的三点補完数との代用をしない。極大拡張と最大拡張は区別する。有限反例であり、完全残余ハイパーグラフの同型や全継続木が一致する反例ではない。

