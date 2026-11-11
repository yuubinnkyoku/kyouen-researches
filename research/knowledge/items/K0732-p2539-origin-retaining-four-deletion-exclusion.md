---
id: K0732
title: Q_2539の保存1258点集合は原点を保つ4点以下の削除で改善できない（完全対変更・完全対なしも独立監査済み）
kind: proposition
status: computed
topics: [geometry, maximum-safe, reconfiguration, verification]
aliases: []
relations:
- type: depends_on
  target: K0731
  note: 同じ固定1258点集合について、原点と元の完全対6を保つ場合の独立排除
- type: generalizes
  target: K0731
  note: 完全対を固定する条件を外し、原点を保つ全クラスへ広げる
- type: depends_on
  target: K0730
  note: SHA-256固定の1258点安全証人
- type: depends_on
  target: K0097
  note: 安全集合に含まれる完全対は高々一つ
- type: depends_on
  target: K0001
  note: 標準q=4の共線・共円禁止四点に関する安全性
artifacts:
- path: research/log/2026-11-11-parabola-local-id-integration.md
  role: data
  note: 未pushローカル旧K0725から現行K0732への番号対応
- path: research/experiments/parabola-p2539-origin-local-audit-20261111/qualification.json
  role: manifest
  note: 元完全対・別完全対・完全対なしの三場合を同一seedへ結び付ける集約と部分集合論証のhash
- path: research/experiments/parabola-p2539-origin-local-audit-20261111/output/changed-pair/input.cnf.gz
  role: certificate
  note: 完全対変更の44062変数・130779節。元の完全対6を禁止し原点と1259点・削除上限4を指定
- path: research/experiments/parabola-p2539-origin-local-audit-20261111/output/changed-pair/verified-proof.drat.gz
  role: certificate
  note: RUP限定で受理し別処理でも再生した254562行DRAT
- path: research/experiments/parabola-p2539-origin-local-audit-20261111/output/no-pair/input.cnf.gz
  role: certificate
  note: 完全対なしの40302変数・123259節。原点と1259点・削除上限4を指定
- path: research/experiments/parabola-p2539-origin-local-audit-20261111/output/no-pair/verified-proof.drat.gz
  role: certificate
  note: RUP限定で受理し別処理でも再生した298208行DRAT
- path: research/experiments/parabola-p2539-origin-local-audit-20261111/output/changed-pair/manifest.json
  role: manifest
  note: 採用CNF/DRATと、ローカル保持した42292行LRATの所在・hash・独立受理
- path: research/experiments/parabola-p2539-origin-local-audit-20261111/output/no-pair/manifest.json
  role: manifest
  note: 採用CNF/DRATと、ローカル保持した33132行LRATの所在・hash・独立受理
- path: research/experiments/parabola-p2539-origin-local-audit-20261111/output/summary.json
  role: data
  note: 二つの独立schema・幾何・RUP・空節修正版LRAT受理の集約
- path: research/experiments/parabola-p2539-origin-local-audit-20261111/schema.py
  role: verifier
  note: 探索器とSATライブラリをimportせず、4値状態・exact cardinality・point定義・削除counter・幾何を全節照合
- path: research/experiments/parabola-p2539-origin-local-audit-20261111/replay.json
  role: data
  note: Git管理された採用圧縮CNF/DRATを、独立schemaと幾何を含めて別処理実再生
- path: research/experiments/parabola-p2539-origin-local-audit-20261111/regression.json
  role: data
  note: 実入力14改変の拒否、point定義128真理値割当て、部分集合選択の有限縮小例356件
- path: research/experiments/parabola-p2539-origin-local-audit-20261111/README.md
  role: proof
  note: 安全候補からのモデル拡張と、大きい改善集合をexact1259点へ縮める全称部分集合論証
scope: 指定SHA-256のQ_2539内1258点集合Sに対し、0∈T、|S\T|<=4、|T|>=1259を同時に満たす安全集合Tは存在しない。完全対は固定しない。原点を除く交換、5点以上の削除、他の種、A(2539)=1258は主張しない。
evidence: 元完全対を保つ場合はK0731、他の二場合は独立4値schema・全幾何節の整数行列式・RUP/LRAT・採用圧縮DRATの別処理再生でexact1259点を排除。安全性の遺伝性と交差集合の大きさによる部分集合論証で1259点以上の全改善集合へ拡張した。
---

## 命題

SはSHA-256 `454f0e293fd846aa6616dd45500dbaf9b325834408ec7f69234852e3e35e22fb` の1258点集合。
**0∈T、|S∖T|≤4、|T|≥1259を同時に満たすQ_2539内の安全集合Tは存在しない。**
従って改善するには、原点を除くか、少なくとも5点をSから除く必要がある。
全体の範囲1258≤A(2539)≤1271は変わらない。

## 三場合の被覆

Tの完全対は高々一つである。
元の完全対{6,2533}を含む場合はK0731で1259点以上が既に排除されている。
完全対が別の一つ、または完全対がない場合は、本監査の二CNFでexact1259点を排除した。

大きいTの被覆には部分集合論証を要する。
完全対がないTでは、S∩Tを全て含む1259点部分集合T'を選べる。|S∩T|≤1258だからである。
原点・完全対なし・削除数を保つため、完全対なしCNFで排除される。

Tが別の完全対{d,2539−d}を持つ場合、元の完全対の少なくとも片側はTにないのでr=|S∖T|≥1。
R=(S∩T)∪{d,2539−d}は|R|≤1258−r+2≤1259であり、Rを含む1259点部分集合T'をTから選べる。
新完全対・原点を保ち、|S∖T'|=r≤4なので、完全対変更CNFで排除される。
いずれのT'も安全性を受け継ぎ、矛盾する。

## 独立schemaと保存証明

各対のBOTH/NONE/LOW/HIGHのone-hot、BOTH数0または1、NONE数、point定義、種からの削除上限を全節照合した。
cardinalityは二つのAtMostへ分け、各補助変数にprefixの真入力個数という意味を独立に付けた。
point変数は対応するBOTHまたは片側選択の論理和と三節で同値であることを確認した。
補助変数領域は全て非衝突。安全なexact1259点候補から全CNF節を満たすモデルへ拡張できる。
幾何節は各入力38868個で、全て真の禁止四点とgeneric整数4x4行列式で確認した。
提供辺の完全性は排除に不要である。

二つの新生成DRATを固定RUP限定検査で受理し、抽出42292行・33132行LRATを空節処理修正版で受理した。
さらに採用圧縮CNF/DRATを、ソルバ・ローカルLRATなしで別処理実再生した。
三場合のseed・入力・証明・sourceのhash bindingをqualificationで照合した。

## 限界

K0731の完全対固定という条件を外すが、原点を保持する条件は残る。
原点の保持条件も外した同じ種の四点削除局所最適性はK0733を参照する。
5点以上の削除や原点を失う交換、他の1258点集合の局所最適性は結論しない。
14不正入力・128真理値割当て・356縮小例は有限回帰であり、部分集合の全称論証とは区別する。
検査器・コンパイラの一般健全性の形式証明やLean形式証明は主張しない。
