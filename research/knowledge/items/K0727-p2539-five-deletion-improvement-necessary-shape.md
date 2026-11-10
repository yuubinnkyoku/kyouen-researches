---
id: K0727
title: Q_2539の保存1258点集合を五点以下の削除で改善するには原点と完全対一つが必要
kind: proposition
status: computed
topics: [geometry, maximum-safe, reconfiguration, verification]
aliases: []
relations:
- type: depends_on
  target: K0726
  note: 同じ固定集合から四点以下の削除による改善は全形状で独立排除済み
- type: depends_on
  target: K0723
  note: SHA-256固定の1258点安全証人
- type: depends_on
  target: K0097
  note: 安全集合の完全対は高々一つ
- type: depends_on
  target: K0001
  note: 標準q=4の安全性は部分集合に継承される
artifacts:
- path: research/experiments/parabola-p2539-exact-five-20261111/qualification.json
  role: manifest
  note: 四点削除排除・exact五点三形状・未解決形状を同一seedと部分集合論証へ結合
- path: research/experiments/parabola-p2539-exact-five-20261111/audit-output/x0-B0/input.cnf.gz
  role: certificate
  note: 原点なし・完全対なし、42818変数127040節
- path: research/experiments/parabola-p2539-exact-five-20261111/audit-output/x0-B0/verified-proof.drat.gz
  role: certificate
  note: RUP限定検査と別処理再生を通った318386行DRAT
- path: research/experiments/parabola-p2539-exact-five-20261111/audit-output/x0-B1/input.cnf.gz
  role: certificate
  note: 原点なし・完全対一つ、46582変数134567節
- path: research/experiments/parabola-p2539-exact-five-20261111/audit-output/x0-B1/verified-proof.drat.gz
  role: certificate
  note: RUP限定検査と別処理再生を通った312040行DRAT
- path: research/experiments/parabola-p2539-exact-five-20261111/audit-output/x1-B0/input.cnf.gz
  role: certificate
  note: 原点あり・完全対なし、47810変数137026節
- path: research/experiments/parabola-p2539-exact-five-20261111/audit-output/x1-B0/verified-proof.drat.gz
  role: certificate
  note: RUP限定検査と別処理再生を通った486382行DRAT
- path: research/experiments/parabola-p2539-exact-five-20261111/audit-output/summary.json
  role: manifest
  note: 三入力の独立schema・整数幾何・RUP・空節修正版LRAT受理とローカルLRATのhash・所在
- path: research/experiments/parabola-p2539-exact-five-20261111/schema.py
  role: verifier
  note: 探索builderとSATライブラリを使わずexact損失の上下両counterを全照合
- path: research/experiments/parabola-p2539-exact-five-20261111/replay.json
  role: data
  note: 採用圧縮CNF/DRATから独立schema・幾何・RUPを別処理再生
- path: research/experiments/parabola-p2539-exact-five-20261111/schema-regression.json
  role: data
  note: 実入力27改変の拒否、point定義192割当て、部分集合縮小例342件
- path: research/experiments/parabola-p2539-exact-five-20261111/regression.json
  role: data
  note: 小素数のexact点数・損失・原点会計131940割当ての有限回帰
- path: research/experiments/parabola-p2539-exact-five-20261111/output/x1-B1-target1259-remove5/result.json
  role: data
  note: 原点あり・完全対一つは100000 conflictsでUNKNOWN、独立排除も安全証人もない
- path: research/experiments/parabola-p2539-exact-five-20261111/README.md
  role: proof
  note: 安全候補からのモデル拡張、exact1259から全改善集合への部分集合論証、再現と限界
scope: 指定SHA-256の1258点集合Sについて、安全集合Tが|T|>=1259かつ|S\T|<=5を満たすなら、|S\T|=5、0∈T、完全対数1が必要。残る形状の実在・非存在や五点削除局所最適性、全体の最大性は主張しない。
evidence: K0726で四点以下を排除。exact五点削除の原点なし二形状と原点あり完全対なしを独立schema・整数幾何・RUP/LRATと採用DRAT再生で排除。S∩Tと必要な完全対を含む1259点部分集合への縮小で大きな改善集合へ拡張する。
---

## 命題

SはSHA-256 `454f0e293fd846aa6616dd45500dbaf9b325834408ec7f69234852e3e35e22fb` の1258点安全集合。
|T|≥1259、|S∖T|≤5を満たすQ_2539内の安全集合Tがあれば、
**正確に五点を失い、原点0を含み、完全対を正確に一つ持つ。**
完全対の位置は固定しない。これは改善の必要条件であり、改善の存在は未確定。

## 根拠

K0726によりr=|S∖T|は5。完全対数は高々一つなので、原点有無と完全対数で四形状に分かれる。
exact1259点の三形状（原点なしの二形状、原点あり・完全対なし）を独立排除した。
全節を独立schemaで解釈し、損失の上下両counterと原点損失1を確認した。
各幾何節を実四点へ戻して整数行列式0を検査し、DRATのRUP限定受理、
抽出30890/53298/103010行LRATの空節修正版受理、採用圧縮DRATの別処理再生が成功した。
提供辺cacheの完全性に頼らず、安全候補から全CNFモデルへの拡張を根拠とする。

大きなTに対して、S∩T（1253点）と存在すれば完全対二点を含むRは高々1255点。
Rを含むTの1259点部分集合T'を選ぶと、安全性、削除数5、原点有無、完全対数を保つ。
Sが0を含むため、Tが0を含む場合はS∩Tによって0も保たれる。
従って排除済み三形状のTは存在しない。有限独立排除とこの全称縮小論証を区別して記録する。

## 未解決と限界

残る「原点あり・完全対一つ」はexact五点削除・100000 conflictsでUNKNOWN。
UNSATもSATも、安全な1259点証人も得ていない。
五点削除近傍全体の局所最適性やA(2539)=1258を主張しない。
現在の全体範囲1258≤A(2539)≤1271は変わらない。
有限回帰を全称証明に代用せず、検査器やコンパイラ一般の健全性、Lean形式証明は主張しない。
