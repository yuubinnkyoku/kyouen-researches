---
id: K0734
title: Q_2539の五点削除改善は116点を避け空対26点から追加する必要がある
kind: proposition
status: computed
topics: [geometry, maximum-safe, reconfiguration, verification]
aliases: []
relations:
- type: depends_on
  target: K0733
  note: 同じ固定集合から四点以下の削除による改善は全形状で独立排除済み
- type: depends_on
  target: K0730
  note: SHA-256固定の1258点安全証人
- type: depends_on
  target: K0097
  note: 安全集合の完全対は高々一つ
- type: depends_on
  target: K0001
  note: 標準q=4の安全性は部分集合に継承される
artifacts:
- path: research/log/2026-11-11-parabola-local-id-integration.md
  role: data
  note: 未pushローカル旧K0727から現行K0734への番号対応、凍結証拠の旧番号の解釈
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
- path: research/experiments/parabola-p2539-point-rup-bridge-20261111/individual-summary.json
  role: manifest
  note: 親CNFだけから受理済みの60個別RUP導出の所在・hash、結合検査と独立した採用
- path: research/experiments/parabola-p2539-point-rup-bridge-20261111/combined-output/all-units.rup.gz
  role: certificate
  note: 60負point単位節を親CNFだけから導く追加696834・削除696774行の結合RUP、空節なし
- path: research/experiments/parabola-p2539-point-rup-bridge-20261111/combined-output/summary.json
  role: manifest
  note: 固定checkerの-f -UでDERIVATION受理、UNSAT refutationではない
- path: research/experiments/parabola-p2539-point-rup-bridge-20261111/qualification.json
  role: manifest
  note: 元の保持側CNFと60単位節付きpruned CNFの全モデル一致、既存の形状条件との結合
- path: research/experiments/parabola-p2539-point-rup-bridge-20261111/audit-output/controls.json
  role: data
  note: native partial RUP checkerで正しい単位・非単位を受理し、偽の節を拒否
- path: research/experiments/parabola-p2539-point-rup-bridge-20261111/native-controls.json
  role: data
  note: 新しい変数の単位節をRATとして受理し-Uでは拒否、guard付き導出を受理しguard欠落を拒否
- path: research/experiments/parabola-p2539-point-rup-bridge-20261111/regression.json
  role: data
  note: 独立小型UPと総当たりで561仮定下の負例・574 lift節を照合、guard欠落等を拒否
- path: research/experiments/parabola-p2539-point-rup-bridge-20261111/replay.json
  role: data
  note: SATライブラリや子証明を使わず結合RUPを別処理再生、DERIVATIONと全体UNSATを区別
- path: research/experiments/parabola-p2539-point-rup-bridge-20261111/README.md
  role: proof
  note: 仮定除去のRUP論証、個別と結合受理・初回timeoutの区別、全モデル一致と大きなTへの縮小
- path: research/experiments/parabola-p2539-pair-obstructions-20261111/qualification.json
  role: manifest
  note: 同一seedの116点除外と空対26点の正追加gateを既存の原点・完全対保持条件へ結合
- path: research/experiments/parabola-p2539-pair-obstructions-20261111/output/certificate.json
  role: certificate
  note: 1255個の完全対四点を加えた障害族で116点を排除、既存60点に新規56点を追加
- path: research/experiments/parabola-p2539-pair-obstructions-20261111/audit-output/summary.json
  role: data
  note: 全7769四点の整数幾何とpacking248・branch99 nodeの独立受理、残り1165点は必要障害族だけの削除証人
- path: research/experiments/parabola-p2539-pair-obstructions-20261111/regression.json
  role: data
  note: 小素数272 seed・528完全対四点・6084削除例、5不正入力拒否
- path: research/experiments/parabola-p2539-pair-obstructions-20261111/gate-output/empty-pair-clause.rup.gz
  role: certificate
  note: 元の空対26点から少なくとも一点を選ぶ正ORを親だけから導く一行RUP、空節ではない
- path: research/experiments/parabola-p2539-pair-obstructions-20261111/gate-output/receipt.json
  role: manifest
  note: 親の保持側CNFだけを使い-f -Uで26-literal clauseをDERIVATION受理
- path: research/experiments/parabola-p2539-pair-obstructions-20261111/gate-regression.json
  role: data
  note: 20880組の小seed/targetで鏡像単射と空対追加の必要性を検査、うち2920組が厳密改善
- path: research/experiments/parabola-p2539-pair-obstructions-20261111/README.md
  role: proof
  note: 完全対保持から単点障害を得る論証、116点除外、空対26点の追加が必要な数え上げとnative RUP
scope: 指定SHA-256の1258点集合Sについて、安全集合Tが|T|>=1259かつ|S\T|<=5を満たすなら、|S\T|=5、原点と元の完全対{6,2533}の保持、本文の116点集合Uの回避、元の空対26点集合Eから少なくとも一点の追加が必要。残る候補の実在・非存在や全体最大性は主張しない。
evidence: 四点以下と原点・完全対変更の形状を独立排除。完全対の四点を加えた7769障害で116点の負hitting証明木を独立受理。追加点の鏡像から削除点への単射でE追加が必要となり、正26-literal clauseも親だけのRUPで受理。既存60点のnative RUPと新規56点の幾何hitting根拠は区別する。
---

## 命題

SはSHA-256 `454f0e293fd846aa6616dd45500dbaf9b325834408ec7f69234852e3e35e22fb` の1258点安全集合。
|T|≥1259、|S∖T|≤5を満たすQ_2539内の安全集合Tがあれば、
**正確に五点を失い、原点0と元の完全対{6,2533}を全て保つ。**
安全集合の完全対は高々一つなので、完全対の位置も元の対に限られる。
さらに、後掲の116点集合Uを避け、元の空対26点集合Eから少なくとも一点を追加しなければならない。
これは改善の必要条件であり、改善の存在は未確定。

## 根拠

K0733によりr=|S∖T|は5。完全対数は高々一つなので、原点有無と完全対数で四形状に分かれる。
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

初回の除外集合U0は次の60点であり、いずれもSに含まれない。

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
U0の各uについて、五点以下ではhitできない証明木を独立検査した。
leafは残予算kに対するk+1個の互いに素な非空障害、または空障害。
branchは障害Rをhitする全選択v∈Rを被覆し、残りを予算k−1で排除する。
この帰納論証と、実際のpacking306・branch123 node受理を区別する。
抽出した6514四点はgeneric整数4×4行列式0を実確認し、提供辺の完全性には依存しない。
従ってT∩U0=∅。この障害論証自体はTの点数に依らず、同時に複数点を追加しても成立する。

## 完全対保持の障害で116点へ強化

u∉S、2539−u∈Sなら、{6,2533,u,2539−u}も禁止四点である。
固定対を保ってuを追加するには2539−uを削除する必要があり、障害族へ単点{2539−u}を追加できる。
1255個のこの四点を加え、全7769四点を整数行列式0と実確認した。
強化した障害族の独立証明木で、新規56点U1を排除した。

```
27 258 265 324 352 417 489 520 604 648 690 703 729 756
826 863 913 927 961 1016 1055 1132 1193 1282 1317 1354 1381 1396
1447 1458 1632 1694 1748 1787 1796 1803 1805 1822 1856 1858 1862 1872
1901 1991 2039 2057 2082 2109 2186 2199 2222 2312 2355 2387 2402 2435
```

U=U0∪U1は116点で、T∩U=∅が必要。負証明木はpacking248・branch99 nodeを受理した。
新規56点の根拠は整数幾何とhitting-treeであり、既存60点の親だけのRUP導出とは区別する。

## 元の空対26点からの追加が必要

Sで両側とも空の13対が作る26点集合Eは次の通り。

```
60 106 262 269 612 647 692 916 992 1021 1027 1172 1197
1342 1367 1512 1518 1547 1623 1847 1892 1927 2270 2277 2433 2479
```

A=T∖S、D=S∖Tとする。u∈A∖Eの鏡像2539−uはSにあり、元の完全対を保つためDに属する。
この鏡像写像は単射なので|A∖E|≤|D|<|A|。従ってT∩E≠∅が必要である。
正point変数26個のOR一行も、既存の保持側親CNFだけから-f -UでDERIVATION受理した。
これは空節ではなく、親全体UNSATを意味しない。EとUは交わらず、26点の個別仮定で未知部分を被覆できる。

## 未解決と限界

残る「原点と元の完全対を保持」はexact五点削除・budget100000（実conflicts100004）でUNKNOWN。
UNSATもSATも、安全な1259点証人も得ていない。
初回のU0以外1221候補には初回の障害族だけをhitする削除証人があった。
強化後はU以外1165候補について、完全対の障害も含めた族だけをhitする五点以下の削除証人がある。
これは安全な改善証人や、他の幾何障害を全て回避する証人ではない。
その後、親の保持側CNFに60負point単位節を追加した51570変数144606節を一回探索した。
この新入力もbudget100000・85.197秒でUNKNOWNだった。入力の意味と幾何・hitting根拠は独立監査したが、負の完結証明はない。
その後、この60節それぞれを親CNFだけから導くRUP証明を独立受理した。
各a_u仮定下の子証明へ¬a_uを付けて仮定を除去し、親Fだけで全追加を-f -U検査した。
60個別導出と結合版、SATライブラリ・子証明を使わない別処理再生がDERIVATIONとして受理された。
したがってFと60単位節付きpruned CNFは全モデルが一致する。これは空節のない導出で、全体UNSATではない。
大きな改善TがU0の除外点uを含めば、(S∩T)∪{u}の1254点を含む1259点部分集合を取り、親Fへモデル拡張できる。
原点と元の完全対はS∩Tに保たれ、a_uと今回導いた¬a_uが矛盾するため、同じ60点回避の別根拠となる。
元の幾何hitting証明と今回の親だけのRUP導出は独立した根拠として保持する。
五点削除近傍全体の局所最適性やA(2539)=1258を主張しない。
現在の全体範囲1258≤A(2539)≤1271は変わらない。
有限回帰を全称証明に代用せず、検査器やコンパイラ一般の健全性、Lean形式証明は主張しない。
