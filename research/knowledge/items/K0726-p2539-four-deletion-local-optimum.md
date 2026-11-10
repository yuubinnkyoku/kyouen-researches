---
id: K0726
title: Q_2539の保存1258点集合は4点以下の削除で改善できない（原点・完全対の保持条件なし）
kind: proposition
status: computed
topics: [geometry, maximum-safe, reconfiguration, verification]
aliases: []
relations:
- type: depends_on
  target: K0725
  note: 同じ固定1258点集合について原点を保つ全クラスの独立排除
- type: generalizes
  target: K0725
  note: 原点を保持する条件を外し、全ての改善候補へ広げる
- type: depends_on
  target: K0723
  note: SHA-256固定の1258点安全証人
- type: depends_on
  target: K0097
  note: 安全集合の完全対は高々一つ
- type: depends_on
  target: K0001
  note: 標準q=4の共線・共円禁止四点に関する安全性
artifacts:
- path: research/experiments/parabola-p2539-without-origin-20261111/qualification.json
  role: manifest
  note: 原点保持のK0725と原点なし二クラスを同一seedへ結び付ける集約、部分集合論証のhash
- path: research/experiments/parabola-p2539-without-origin-20261111/audit-output/B0/input.cnf.gz
  role: certificate
  note: 原点なし・完全対なしの36556変数115767節、exact1259点・総削除数4以下
- path: research/experiments/parabola-p2539-without-origin-20261111/audit-output/B0/verified-proof.drat.gz
  role: certificate
  note: RUP限定検査と別処理再生を通った23072行DRAT
- path: research/experiments/parabola-p2539-without-origin-20261111/audit-output/B1/input.cnf.gz
  role: certificate
  note: 原点なし・完全対一つの40320変数123294節、exact1259点・総削除数4以下
- path: research/experiments/parabola-p2539-without-origin-20261111/audit-output/B1/verified-proof.drat.gz
  role: certificate
  note: RUP限定検査と別処理再生を通った205896行DRAT
- path: research/experiments/parabola-p2539-without-origin-20261111/audit-output/B0/manifest.json
  role: manifest
  note: 採用CNF/DRATとローカル保持1277行LRATの所在・hash・独立受理
- path: research/experiments/parabola-p2539-without-origin-20261111/audit-output/B1/manifest.json
  role: manifest
  note: 採用CNF/DRATとローカル保持22797行LRATの所在・hash・独立受理
- path: research/experiments/parabola-p2539-without-origin-20261111/audit-output/summary.json
  role: data
  note: 二クラスの独立schema・幾何・RUP・空節修正版LRAT受理
- path: research/experiments/parabola-p2539-without-origin-20261111/schema.py
  role: verifier
  note: SATライブラリ・探索builderを使わず全節を解釈し、原点の損失1と非原点削除上限3を区別する
- path: research/experiments/parabola-p2539-without-origin-20261111/replay.json
  role: data
  note: 採用圧縮CNF/DRATを独立schema・幾何とともに別処理実再生
- path: research/experiments/parabola-p2539-without-origin-20261111/regression.json
  role: data
  note: 14不正入力の拒否、128 point真理値割当て、原点損失を含む部分集合縮小例152件
- path: research/experiments/parabola-p2539-without-origin-20261111/README.md
  role: proof
  note: 安全候補からのモデル拡張、exact1259から全改善集合への部分集合論証、再現と限界
scope: 指定SHA-256のQ_2539内1258点集合Sに対し、|S\T|<=4かつ|T|>=1259となる安全集合Tは存在しない。原点・完全対は固定しない。他の種、5点以上の削除、A(2539)=1258は主張しない。
evidence: 原点保持はK0725による。原点なしの完全対数0/1の両exact1259点CNFを独立schema・整数幾何・RUP/LRAT・採用圧縮DRAT実再生で排除。原点が失われるためr>=1となる部分集合論証を用い、1259点以上の任意の改善候補へ拡張した。
---

## 命題

SはSHA-256 `454f0e293fd846aa6616dd45500dbaf9b325834408ec7f69234852e3e35e22fb` の1258点集合。
**|S∖T|≤4、|T|≥1259を同時に満たすQ_2539内の安全集合Tは存在しない。**
従って、原点や完全対をどう変更しても、改善にはSから少なくとも5点を失う必要がある。
これは固定Sの四点削除近傍での局所最適性であり、全体の最大性ではない。
現在の範囲1258≤A(2539)≤1271は変わらない。

## 原点なしの場合の独立排除

原点を保つ候補はK0725で既に排除したので、0∉Tだけを扱う。
完全対は高々一つであり、完全対数0/1の二クラスに分かれる。
exact1259点では空対数がそれぞれ10/11となる。
種Sは原点を含むため、その損失だけで削除数1を使い、非原点1257点の削除上限は3。
この点を独立schemaで確認し、総削除上限4と非原点上限3を混同しない。

各対の4値one-hot・BOTH数・NONE数・point定義・削除counterを全節照合した。
counter補助変数は独立prefix意味へ解釈し、全領域の非衝突を確認した。
原点なしの幾何節は四つの負のpoint変数だけを持ち、各38866四点を整数行列式0と確認した。
安全な候補から全CNFのモデルへ拡張できるため、提供辺の完全性は不要。
両CNFのDRATを固定RUP限定検査で受理し、抽出1277行・22797行LRATを空節修正版で受理した。
採用圧縮CNF/DRATの別処理実再生も成功した。

## exact1259から全改善集合へ

0∉T、|S∖T|≤4、|T|≥1259とする。r=|S∖T|は原点の損失により1以上。
完全対なしならS∩Tを全て含む1259点部分集合T'を選び、安全性・原点なし・削除数rを保てる。
完全対{d,2539−d}があるなら、R=(S∩T)∪{d,2539−d}は|R|≤1258−r+2≤1259。
Rを含む1259点部分集合T'を選び、安全性・原点なし・完全対・削除数rを保てる。
いずれも対応するexact1259点CNFの排除に反する。
原点保持と原点なしの二場合で全てを覆い、命題が従う。

## 限界

他の1258点集合や、5点以上の削除を伴う改善については結論しない。
14不正入力・128真理値割当て・152縮小例は有限回帰であり、全称部分集合論証とは区別する。
検査器・コンパイラの一般健全性やLean形式証明は主張しない。
