---
id: K0727
title: Q_2539の五点削除改善は原点・元の完全対を保持し60候補点を避ける必要がある
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
- path: research/experiments/parabola-p2539-five-pair-split-20261111/qualification.json
  role: manifest
  note: 既存三形状排除と元の完全対変更の独立排除を同一seed・部分集合論証へ結合
- path: research/experiments/parabola-p2539-five-pair-split-20261111/audit-output/changed/input.cnf.gz
  role: certificate
  note: 原点・完全対一つ・exact五点損失の親CNFに[-B6]を加えた51570変数144546節
- path: research/experiments/parabola-p2539-five-pair-split-20261111/audit-output/changed/verified-proof.drat.gz
  role: certificate
  note: RUP限定検査と別処理再生を通った483675行DRAT
- path: research/experiments/parabola-p2539-five-pair-split-20261111/audit-output/changed/manifest.json
  role: manifest
  note: 独立schema・整数幾何・RUP/LRAT受理、採用証明とローカル保持147349行LRATのhash・所在
- path: research/experiments/parabola-p2539-five-pair-split-20261111/schema.py
  role: verifier
  note: 全構造節・損失counter・末尾のB6否定単位節を独立解釈
- path: research/experiments/parabola-p2539-five-pair-split-20261111/replay.json
  role: data
  note: 採用CNF/DRATを独立schema・整数幾何・RUPとともに別処理再生
- path: research/experiments/parabola-p2539-five-pair-split-20261111/input-audit/summary.json
  role: data
  note: 親+相補単位節のbyte完全照合と両形状の独立schema・幾何確認
- path: research/experiments/parabola-p2539-five-pair-split-20261111/regression.json
  role: data
  note: 16不正入力拒否と元の完全対に対応する実point・splitの128真理値割当て
- path: research/experiments/parabola-p2539-five-pair-split-20261111/output/retained/result.json
  role: data
  note: 原点と元の完全対を保つexact五点損失はbudget100000でUNKNOWN、実conflicts100004
- path: research/experiments/parabola-p2539-five-pair-split-20261111/README.md
  role: proof
  note: 完全対の位置も保つ部分集合論証、分割・モデル拡張、再現と限界
- path: research/experiments/parabola-p2539-five-obstructions-20261111/qualification.json
  role: manifest
  note: 同一seedの原点・完全対保持条件と追加候補60点の独立排除を結合
- path: research/experiments/parabola-p2539-five-obstructions-20261111/output/certificate.json
  role: certificate
  note: 全1281候補のうち60点の負hitting証明木と1221点の提供障害族だけをhitする削除証人
- path: research/experiments/parabola-p2539-five-obstructions-20261111/verify.py
  role: verifier
  note: 探索コードをimportせず分岐被覆・残予算・互いに素な障害と実整数幾何を確認
- path: research/experiments/parabola-p2539-five-obstructions-20261111/audit-output/summary.json
  role: data
  note: 60点排除、packing306・branch123 node受理、6514禁止四点の実検査
- path: research/experiments/parabola-p2539-five-obstructions-20261111/audit-output/geometry.json
  role: manifest
  note: generic整数4×4行列式検査の正常終了・出力・入力とsourceのhash
- path: research/experiments/parabola-p2539-five-obstructions-20261111/regression.json
  role: data
  note: 正負双方の証明木・削除証人を総当たり2224例と照合、14改変を拒否
- path: research/experiments/parabola-p2539-five-obstructions-20261111/README.md
  role: proof
  note: 一点追加の障害族と五点削除の必要条件、証明木の帰納的健全性、再現と限界
- path: research/experiments/parabola-p2539-five-pruned-20261111/output/input.cnf.gz
  role: data
  note: 保持側の親CNFに60負point単位節を追加した51570変数144606節、未解決入力
- path: research/experiments/parabola-p2539-five-pruned-20261111/output/result.json
  role: data
  note: 新しい60節付き入力もbudget100000・85.197秒でUNKNOWN、完結した負証明なし
- path: research/experiments/parabola-p2539-five-pruned-20261111/input-audit/summary.json
  role: data
  note: 親全節と追加60節の意味・hitting-tree・整数幾何監査、UNSAT監査ではない
- path: research/experiments/parabola-p2539-five-pruned-20261111/regression.json
  role: data
  note: 実入力10改変の拒否と60負point単位節の120真理値割当て
- path: research/experiments/parabola-p2539-five-pruned-20261111/README.md
  role: data
  note: 新しい除外条件を採用したprobeの再現、UNKNOWNの限界、次の手順
scope: 指定SHA-256の1258点集合Sについて、安全集合Tが|T|>=1259かつ|S\T|<=5を満たすなら、|S\T|=5、原点と元の完全対{6,2533}の保持、本文の60点集合Uの回避が必要。残る候補の実在・非存在、五点削除局所最適性、全体の最大性は主張しない。
evidence: 四点以下と原点・完全対変更の形状を独立schema・整数幾何・RUP/LRATで排除。さらに提供辺からの一点追加障害族を五点以下でhitできない60点を独立証明木と6514四点の実整数幾何で排除。部分集合縮小とhitting-tree帰納論証は有限検査と区別する。
---

## 命題

SはSHA-256 `454f0e293fd846aa6616dd45500dbaf9b325834408ec7f69234852e3e35e22fb` の1258点安全集合。
|T|≥1259、|S∖T|≤5を満たすQ_2539内の安全集合Tがあれば、
**正確に五点を失い、原点0と元の完全対{6,2533}を全て保つ。**
安全集合の完全対は高々一つなので、完全対の位置も元の対に限られる。
さらに、後掲の60点集合Uを含めることはできない。
これは改善の必要条件であり、改善の存在は未確定。

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

## 完全対の変更も独立排除

残る親CNFを、B6（元の対が完全対）と¬B6の相補的二単位節で分けた。
各子は51570変数144546節。変更側¬B6の483675行DRATをRUP限定検査で受理し、
抽出147349行LRATを空節修正版で受理した。採用圧縮DRATの別処理再生も成功した。
独立schemaは全節に加えて末尾の¬B6を照合し、38868幾何四点の整数行列式0を確認した。

大きなTの完全対が{d,2539−d}、d≠6なら、その対を含むRを選ぶ同じ縮小で、
T'も原点・五点損失・その完全対を保つ。部分集合は新しい完全対を作らないのでT'も¬B6であり、
変更側CNFの独立排除に反する。従って完全対は元の{6,2533}でなければならない。

## 一点追加障害による60点の独立排除

Uは次の60点であり、いずれもSに含まれない。

```
555 856 934 956 1095 1187 1189 1190 1277 1283
1286 1287 1288 1289 1290 1291 1292 1293 1294 1295
1296 1297 1298 1299 1300 1301 1302 1303 1304 1305
1306 1307 1308 1309 1310 1311 1312 1313 1363 1379
1448 1472 1511 1532 1567 1572 1594 1627 1647 1781
1806 1825 1835 1979 1997 2043 2171 2204 2213 2225
```

F={0,6,2533}とする。候補点uを含み、残り三点がS内にある提供禁止四点qから、
障害R=(q∖{u})∖Fを作る。F⊆Tでu∈Tなら、安全性のためD=S∖Tは全てのRをhitする必要がある。
Uの各uについて、五点以下ではhitできない証明木を独立検査した。
leafは残予算kに対するk+1個の互いに素な非空障害、または空障害。
branchは障害Rをhitする全選択v∈Rを被覆し、残りを予算k−1で排除する。
この帰納論証と、実際のpacking306・branch123 node受理を区別する。
抽出した6514四点はgeneric整数4×4行列式0を実確認し、提供辺の完全性には依存しない。
従ってT∩U=∅。この障害論証自体はTの点数に依らず、同時に複数点を追加しても成立する。

## 未解決と限界

残る「原点と元の完全対を保持」はexact五点削除・budget100000（実conflicts100004）でUNKNOWN。
UNSATもSATも、安全な1259点証人も得ていない。
U以外の1221追加候補には、提供した一点追加障害族だけをhitする五点以下の削除証人がある。
これは安全な改善証人や、他の幾何障害を全て回避する証人ではない。
その後、親の保持側CNFに60負point単位節を追加した51570変数144606節を一回探索した。
この新入力もbudget100000・85.197秒でUNKNOWNだった。入力の意味と幾何・hitting根拠は独立監査したが、負の完結証明はない。
追加60節を親CNFだけのRUPで導出したとは主張せず、元の幾何・hitting-tree根拠と区別する。
五点削除近傍全体の局所最適性やA(2539)=1258を主張しない。
現在の全体範囲1258≤A(2539)≤1271は変わらない。
有限回帰を全称証明に代用せず、検査器やコンパイラ一般の健全性、Lean形式証明は主張しない。
