---
id: K0734
title: Q_2539の五点削除改善は248点を避け空対18点から二点以上を追加する必要がある
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
- path: research/experiments/parabola-p2539-empty-gate-probes-20261111/output/base.cnf.gz
  role: data
  note: 保持側親に116幾何除外節を加えた51570変数144662節の共通base
- path: research/experiments/parabola-p2539-empty-gate-probes-20261111/input-audit/summary.json
  role: data
  note: 親schema・116除外のhittingと整数幾何・26正仮定の独立監査、初回18 UNKNOWNと8ソルバ負主張
- path: research/experiments/parabola-p2539-empty-gate-probes-20261111/proof-audit/summary.json
  role: manifest
  note: 8子DRATの独立反証と仮定除去した8負単位節、残る18点gate、各圧縮核・導出のhash
- path: research/experiments/parabola-p2539-empty-gate-probes-20261111/replay-output/coverage.rup.gz
  role: certificate
  note: 116幾何除外付きbaseだけから8負単位節と正18点ORを導く20491行RUP、空節なし
- path: research/experiments/parabola-p2539-empty-gate-probes-20261111/replay-output/receipt.json
  role: manifest
  note: ソルバと子DRATを使わない別処理再生で-f -UのDERIVATION受理、元の親単独の反証ではない
- path: research/experiments/parabola-p2539-empty-gate-probes-20261111/qualification.json
  role: manifest
  note: 同一seedの124点除外・18点追加条件を既存の保持条件と部分集合論証へ結合
- path: research/experiments/parabola-p2539-empty-gate-probes-20261111/regression.json
  role: data
  note: 実baseの6改変を拒否、26正point仮定の52真理値割当てを照合
- path: research/experiments/parabola-p2539-empty-gate-probes-20261111/README.md
  role: proof
  note: 26仮定中8点の独立排除、116幾何除外を前提とするRUPの範囲、大きなTへの縮小、残る18 UNKNOWN
- path: research/experiments/parabola-p2539-gate-pair-obstructions-20261111/output/certificate.json
  role: certificate
  note: gate18点の全153組を覆う7負証明と146必要障害族だけの削除証人
- path: research/experiments/parabola-p2539-gate-pair-obstructions-20261111/audit-output/summary.json
  role: manifest
  note: 独立族再構成と空障害5個・六障害packing2個の受理、実45四点の整数幾何
- path: research/experiments/parabola-p2539-gate-pair-obstructions-20261111/verify.py
  role: verifier
  note: 探索をimportせず全153組の被覆・hitting証明・削除証人と整数幾何を検査
- path: research/experiments/parabola-p2539-gate-pair-obstructions-20261111/regression.json
  role: data
  note: 実証明書8改変の拒否、小型hitting族495例の総当たり比較
- path: research/experiments/parabola-p2539-gate-pair-obstructions-20261111/README.md
  role: proof
  note: 非鏡像二組の六つの互いに素な削除障害、全7組同時追加禁止、範囲と再現
- path: research/experiments/parabola-p2539-gate-cover-20261111/output/certificate.json.gz
  role: certificate
  note: 新規20502組の5010負hitting証明と15492必要障害族だけの削除証人、97点の全18仮定被覆
- path: research/experiments/parabola-p2539-gate-cover-20261111/output/manifest.json
  role: manifest
  note: 圧縮証明書とraw bytesのSHA-256、新規97点と両状態の件数
- path: research/experiments/parabola-p2539-gate-cover-20261111/audit-output/summary.json
  role: manifest
  note: 全族の独立再構成、packing7439・branch2056 node、4891実四点の整数幾何受理
- path: research/experiments/parabola-p2539-gate-cover-20261111/verify.py
  role: verifier
  note: 探索をimportせず全1139点と18被覆仮定・負証明・削除証人を検査
- path: research/experiments/parabola-p2539-gate-cover-20261111/qualification.json
  role: manifest
  note: 既存正18点gateと97点の全仮定排除を結合した221点回避の必要条件
- path: research/experiments/parabola-p2539-gate-cover-20261111/regression.json
  role: data
  note: 実証明書8改変の拒否、特に被覆仮定の欠落と重複を拒否
- path: research/experiments/parabola-p2539-gate-cover-20261111/README.md
  role: proof
  note: 正gateから点追加被覆を得る論証、新規97点、幾何hittingとnative RUPの区別、範囲と再現
- path: research/experiments/parabola-p2539-one-gate-20261111/output/input.cnf.gz
  role: certificate
  note: 221点除外・正18点OR・153負二項節でexact-one空対追加へ制限した51570変数144921節
- path: research/experiments/parabola-p2539-one-gate-20261111/output/proof.drat.gz
  role: certificate
  note: exact-one制限入力を独立反証する60539行DRAT、RUP限定検査と別処理再生で受理
- path: research/experiments/parabola-p2539-one-gate-20261111/audit-final/summary.json
  role: manifest
  note: 全schemaと追加375節・38868四点の整数幾何・RUP反証の独立受理
- path: research/experiments/parabola-p2539-one-gate-20261111/replay.json
  role: data
  note: 採用圧縮CNF/DRATから探索コード・SATライブラリなしで独立schemaとRUPを別処理再生
- path: research/experiments/parabola-p2539-one-gate-20261111/qualification.json
  role: manifest
  note: 空対二点以上の必要条件と459既存負hitting証明を結合し27点追加排除、総248点
- path: research/experiments/parabola-p2539-one-gate-20261111/regression.json
  role: data
  note: 実CNF6改変を拒否、全262144 gate割当てでexact-oneの18通りだけを受理
- path: research/experiments/parabola-p2539-one-gate-20261111/README.md
  role: proof
  note: 大きなTからの部分集合論証で二点追加を要請、唯一の両立gateしかない27点の排除、制限反証と全体未解決の区別
scope: 指定SHA-256の1258点集合Sについて、安全集合Tが|T|>=1259かつ|S\T|<=5を満たすなら、|S\T|=5、原点と元の完全対{6,2533}の保持、本文の248点集合Uの回避、元の空対から残る18点集合Eの二点以上の追加と本文7組の同時追加回避が必要。残る候補の実在・非存在や全体最大性は主張しない。
evidence: 四点以下と原点・完全対変更を独立排除し、幾何hitting・正18点gateの被覆で221点回避を確認。221除外付きexact-one-gate入力を全schema・38868四点幾何・RUPで独立反証し別処理再生した。従ってE追加は二点以上。既存459負相互制約と結合して27点をさらに排除、総248点回避。元の親単独の反証や新規27点のnative RUPは主張せず、全体は未解決。
---

## 命題

SはSHA-256 `454f0e293fd846aa6616dd45500dbaf9b325834408ec7f69234852e3e35e22fb` の1258点安全集合。
|T|≥1259、|S∖T|≤5を満たすQ_2539内の安全集合Tがあれば、
**正確に五点を失い、原点0と元の完全対{6,2533}を全て保つ。**
安全集合の完全対は高々一つなので、完全対の位置も元の対に限られる。
さらに、後掲の248点集合Uを避け、元の空対から残る18点集合Eの二点以上を追加しなければならない。
E内の後掲7組は同時に追加できない。
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

U01=U0∪U1は116点で、T∩U01=∅が必要。負証明木はpacking248・branch99 nodeを受理した。
新規56点の根拠は整数幾何とhitting-treeであり、既存60点の親だけのRUP導出とは区別する。

## 元の空対26点からの追加が必要

Sで両側とも空の13対が作る26点集合E0は次の通り。

```
60 106 262 269 612 647 692 916 992 1021 1027 1172 1197
1342 1367 1512 1518 1547 1623 1847 1892 1927 2270 2277 2433 2479
```

A=T∖S、D=S∖Tとする。u∈A∖E0の鏡像2539−uはSにあり、元の完全対を保つためDに属する。
この鏡像写像は単射なので|A∖E0|≤|D|<|A|。従ってT∩E0≠∅が必要である。
正point変数26個のOR一行も、既存の保持側親CNFだけから-f -UでDERIVATION受理した。
これは空節ではなく、親全体UNSATを意味しない。E0とU01は交わらず、26点の個別仮定で未知部分を被覆できる。

## 空対8仮定を独立排除し124点除外・18点gateへ

保持側親へU01の116負point単位節を加えた共通base（51570変数144662節）を独立監査し、
E0の各点を選ぶ26個の異なる仮定をbudget10000で一回ずつ探索した。
18 UNKNOWN、8 SOLVER_UNSAT、SATモデルなし。負主張の8点だけをproof付き再生成し、
各子の完結DRATを固定DRAT-trimの-Uで独立受理した。追加の排除集合U2は次の8点。

```
612 1367 1518 1547 1623 1892 2277 2479
```

各子の核DRATを抽出し、¬a_uでliftして仮定を除去した。
8負単位節と、E=E0∖U2の正18点ORを、共通baseだけから-f -UでDERIVATION受理した。
20491行の結合RUPはソルバ・子DRATなしの別処理再生でも受理した。
これは**116幾何除外を含むbaseからの導出**であり、元の保持側親だけの導出や全体UNSATではない。

大きなTがu∈U2を含めば、(S∩T)∪{u}の1254点を含む1259点部分集合T'を選べる。
T'は安全性、共通1253点、原点・完全対、u、U01回避を保つので、共通baseへa_uを真とするモデル拡張ができる。
今回導いた¬a_uに反するため、T∩U2=∅。従ってU012=U01∪U2の124点を避け、次の18点集合Eからの追加が必要。

```
60 106 262 269 647 692 916 992 1021
1027 1172 1197 1342 1512 1847 1927 2270 2433
```

この18仮定は各budget10000でUNKNOWNのままであり、安全な改善証人も独立反証もない。
共通baseへ導出済み8負単位節を加えた入力は全モデルが一致する。

## 空対18点の二点同時追加に対する7組の禁止

Eの全153組について、保存済み幾何四点のS外の点がその組に含まれる障害族を作り、
五点以下の削除で全障害をhitできるかを独立検査した。次の7組は同時追加できない。

```
106 2433
269 2270
692 1847
1027 1197
1027 1512
1197 1342
1927 2433
```

鏡像5組は保持する完全対{6,2533}との四点による空障害で排除した。
非鏡像の{1027,1197}と{1927,2433}では、それぞれ六つの互いに素な削除障害を受理した。
各実四点と削除候補はexperiment README・certificateへ保存し、全族の和集合45四点を整数4×4行列式で確認した。
従って二点を共に含む安全Tには少なくとも六つの種点削除が必要となる。
この論証はTのサイズや他の追加点に依存せず、五点削除改善全体の必要条件となる。
非鏡像二組のpackingは固定点0,6,2533を含む四点を使わず、原点・元の完全対保持を仮定しなくても同じ六点削除下界が成立する。
残る146組の証人は提供された必要障害族をhitするだけで、安全な改善や全幾何辺の回避を保証しない。

## 正18点gateによる97点の被覆排除

S外の1281点から既除外U012の124点とEの18点を除く1139点uについて、各v∈Eとの新規20502組を検査した。
保存済みのS外一・二点を含む禁止四点と完全対保持の四点から障害族を作り、
5010組の負証明と15492組の必要障害族だけの削除証人を独立受理した。
全族が参照する4891四点を整数行列式で検査し、負証明のpacking7439・branch2056 nodeを受理した。
そのうち次の97点U3は、18個の全組{u,v}を高々五点の削除では実現できない。

```
211 241 344 373 378 423 439 456 468 472 495 614 688 720 767 786
846 858 951 1049 1082 1086 1096 1110 1182 1186 1188 1191 1194 1271 1280 1284
1285 1326 1327 1329 1332 1341 1380 1385 1441 1460 1466 1469 1479 1481 1526 1542
1610 1677 1682 1686 1697 1700 1732 1766 1773 1791 1797 1826 1841 1874 1883 1900
1902 1912 1955 1965 1973 2001 2017 2034 2052 2056 2078 2105 2117 2120 2121 2134
2135 2172 2210 2238 2243 2265 2288 2336 2375 2378 2414 2417 2431 2455 2483 2519 2522
```

u∈T∩U3なら、既存の正gateよりv∈T∩Eを選べる。
その組{u,v}の負hitting証明によりD=S∖Tは五点以下では存在できず、矛盾する。
従ってT∩U3=∅であり、U0123=U012∪U3の221点回避が必要。
この論証はTのサイズに依存しない。18仮定は重なってもよいが、一つも欠けてはならない。
新規97点の根拠は幾何hittingと正gateの被覆であり、新しいnative RUP導出とは区別する。
Eは同じ18点のまま、残る1042非gate点にも安全な改善証人を得たわけではない。

## 空対からの追加は二点以上必要

保持側親へU0123の221負単位節、Eの正18点OR、E内全153組の負二項節を加え、
Eから正確に一点だけ追加する新しい形状を51570変数144921節で表した。
一回のproof-enabled探索で実conflicts667・1.761秒、SOLVER_UNSATを得た。
全schemaと追加375節を探索から独立に解釈し、親の38868四点を整数行列式で確認した。
60539行DRATを固定DRAT-trimの-Uで反証受理し、採用圧縮CNF/DRATからの別処理再生も受理した。
これは221除外を含むexact-one制限形状の反証で、元の親単独や五点削除近傍全体の反証ではない。

大きな改善Tで|T∩E|=1、その一点がvなら、(S∩T)∪{v}の1254点を含む1259点部分集合T'を選べる。
T'は安全性、五点損失、原点・完全対保持、221点回避と|T'∩E|=1を保ち、制限入力へモデル拡張できる。
独立反証に矛盾するため、全ての改善Tについて|T∩E|≥2が必要。
この新しい条件は、複数E点を許していた以前の18個別UNKNOWNとは区別する。

## 二点追加条件による27点の追加排除

保存済み20502相互制約を評価すると、既除外221点以外で、Eのうち一つとの組だけが未排除となる点が27個あった。
これをU4とする。

```
4 632 813 819 824 879 937 1018 1046
1316 1358 1478 1550 1657 1665 1721 1731 1742
1811 1895 1910 1929 1931 1941 1963 2096 2160
```

各u∈U4について他の17点との負hitting証明、計459個を再検査した。
u∈TならT∩Eに入れられる点は高々一つとなり、|T∩E|≥2に反する。
従ってT∩U4=∅、U=U0123∪U4の248点回避が必要。
唯一の未排除gate点と各負証明へのhashはqualification・既存圧縮証明書に保持する。
この27点のnative RUP導出は作っておらず、制限形状の反証・部分集合論証・幾何hittingの結合として採用する。

## 未解決と限界

残る「原点と元の完全対を保持」はexact五点削除・budget100000（実conflicts100004）でUNKNOWN。
UNSATもSATも、安全な1259点証人も得ていない。
初回のU0以外1221候補には初回の障害族だけをhitする削除証人があった。
幾何障害強化後はU01以外1165候補について、完全対の障害も含めた族だけをhitする五点以下の削除証人がある。
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
