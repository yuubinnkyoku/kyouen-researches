---
id: K0724
title: Q_2539の保存1258点集合は原点・完全対固定で4点以下を除く改善ができない（独立schema・RUP/LRAT監査済み）
kind: proposition
status: computed
topics: [geometry, maximum-safe, reconfiguration, verification]
aliases: []
relations:
- type: depends_on
  target: K0723
  note: 対象とするSHA-256固定の1258点安全証人
- type: depends_on
  target: K0097
  note: 安全集合の完全対は高々一つであり、完全対6を含めば他の各対は低側・高側・空対に限られる
- type: depends_on
  target: K0712
  note: 原点・完全対固定の三値選択と空対数によるサイズ表示
- type: depends_on
  target: K0001
  note: 標準q=4の共円・共線禁止四点を含まない安全性
artifacts:
- path: research/experiments/parabola-p2539-exchange-20261110/output/target1258-remove3/candidate.txt
  role: certificate
  note: 固定する1258点集合S、SHA-256 454f0e293fd846aa6616dd45500dbaf9b325834408ec7f69234852e3e35e22fb
- path: research/experiments/parabola-p2539-exchange-audit-20261110/output/input.cnf.gz
  role: certificate
  note: 23883変数・86583節、1259点以上かつ種からの削除上限4を課す採用入力
- path: research/experiments/parabola-p2539-exchange-audit-20261110/output/core.lrat.gz
  role: certificate
  note: 元228249行DRATから抽出し局所修正版で検査した64571行LRAT
- path: research/experiments/parabola-p2539-exchange-audit-20261110/output/manifest.json
  role: manifest
  note: 固定種・CNF・採用圧縮LRAT・検査sourceのhashと局所排除の範囲
- path: research/experiments/parabola-p2539-exchange-audit-20261110/output/schema.json
  role: data
  note: 全節を38868幾何節・5072 one-hot節・31388空対counter節・11255削除counter節へ独立照合
- path: research/experiments/parabola-p2539-exchange-audit-20261110/output/geometry.json
  role: data
  note: 各幾何節に対応する38868四点をgeneric整数4x4行列式で実検査
- path: research/experiments/parabola-p2539-exchange-audit-20261110/output/rup.json
  role: data
  note: 固定upstream DRAT-trimのRUP限定受理
- path: research/experiments/parabola-p2539-exchange-audit-20261110/output/lrat.json
  role: data
  note: 空節処理修正版LRAT検査器の受理
- path: research/experiments/parabola-p2539-exchange-audit-20261110/replay.json
  role: data
  note: 元DRAT・探索builder・辺cacheを読まない、採用圧縮CNF/LRATと独立schema・幾何の別処理実再生
- path: research/experiments/parabola-p2539-exchange-audit-20261110/schema.py
  role: verifier
  note: SATライブラリや探索器をimportせず、各counter補助変数をprefix個数へ解釈して全節の拡張可能性を確認
- path: research/experiments/parabola-p2539-exchange-audit-20261110/regression.json
  role: data
  note: 2064 prefix割当て、六つの破損schema、modular和0の非禁止四点の拒否
- path: research/experiments/parabola-p2539-exchange-audit-20261110/rup-controls.json
  role: data
  note: K0707の四偽証明拒否・resolution受理・SAT偽空節拒否の六制御
- path: research/experiments/parabola-p2539-exchange-audit-20261110/lrat-controls.json
  role: data
  note: 空節処理修正の五制御。原版の偽受理を再現し、採用する局所修正版で拒否
- path: research/experiments/parabola-p2539-exchange-audit-20261110/README.md
  role: proof
  note: 安全候補から全CNF節を満たす補助変数への拡張証明、再現手順と信頼境界
scope: 指定1258点集合Sに対し、Q_2539内で0,6,2533を保ち、|S\T|<=4かつ|T|>=1259となる安全集合Tは存在しない。他の種、固定点の変更、5点以上の削除、条件なしの局所最適性、A(2539)=1258は主張しない。
evidence: 独立schemaが全86583節の安全候補からの拡張可能性を確認。38868幾何節は真の禁止四点へ整数幾何で照合し、二counterの補助変数は互いに素な領域でprefix個数を表す。元DRATのRUP限定受理、抽出LRATの局所修正版受理、圧縮証明・schema・幾何・固定種の別処理再生が成功。
---

## 命題

Sはartifactで固定した1258パラメータの集合、F={0,6,2533}とする。
**F⊆T、|S∖T|≤4、|T|≥1259を同時に満たすQ_2539内の安全集合Tは存在しない。**
固定原点・完全対を保つ条件では、改善のために少なくとも5点をSから除く必要がある。
原点や完全対を変える交換については結論しない。

## 独立schemaからCNFへの拡張

安全なTがFを含めば、他の各対から選べるのは低側・高側・空対の三値である。
各対のone-hot状態をTから定めると5072構造節を満たす。
幾何節は負の点選択変数だけからなり、対応する要求点とFの一部で禁止四点を作ることを全節で確認した。
その38868四点はgeneric整数行列式で全て0だった。
従って安全なTは各幾何節を満たす。提供辺の完全性は必要ない。

空対数をEとすると|T|=1271−Eなので、|T|≥1259ならE≤12。
固定Fを除く種の1255点について、点を選ばないことを入力literalにすれば、その真の個数が|S∖T|である。
各counter補助変数には、入力列の位置iまでで真の入力がj個以上というprefix意味を独立に割り当てた。
許容した節は入力の導入、prefixの単調な持ち越し、真入力による増分、上限を超える増分の禁止だけ。
最初の三型はprefixの定義から常に満たされ、最後の型は全真入力数が上限以下なら満たされる。
二つの補助変数領域は3808..18879と18880..23883で、点選択領域および互いと交差しない。
この割当てが全counter節を満たすので、仮定したTは全CNFのモデルへ拡張できる。

元DRATのRUP限定監査と抽出64571行LRATの検査によって、このCNFにモデルが存在しないことを確認した。
したがって上記条件のTは存在しない。

## 独立検査と限界

schemaは探索器・投影builder・CardEncをimportしない。幾何も辺cacheを読まない。
採用圧縮CNF/LRATを別処理で再生し、schema・幾何・固定種へのhash bindingを照合した。
2064小規模prefix割当て、六つの破損schema、合同式だけを満たす非禁止四点、RUP/LRAT制御を検査した。
これらは有限回帰であり、検査器やコンパイラの一般健全性の形式証明ではない。
LRATはK0718の空節問題を修正した固定sourceを使い、原版の受理は根拠にしない。
この局所排除はK0723の全体範囲1258≤A(2539)≤1271を狭めるものではない。
