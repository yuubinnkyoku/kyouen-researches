---
id: K0697
title: 核＋道の周期34末尾は裸の道の普遍シフトではない（六点純三点辺1825種・五点以下134種の末尾分類）
kind: computation
status: computed
topics: [grundy, residual-games, search-methods, variants]
aliases: []
relations:
- type: depends_on
  target: K0682
  note: 裸の道Grundy pと五点以下513型の認証済みprefix、有限窓認証の枠組み
- type: supports
  target: K0684
  note: 末尾が全て周期34であることを構造面から支持するが、核が道をシフトするだけではないことを示す
artifacts:
- path: research/experiments/core-path-shift-structure-20261108/analyze.py
  role: solver
  note: 裸の道pと二つの認証済み族のprefixからシフト一致・末尾ブロック・最小周期・核Grundy相関を計算
- path: research/experiments/core-path-shift-structure-20261108/output/shift_probe.json
  role: data
  note: 六点純三点辺10688型の集計（1825末尾ブロック・3445純シフト・核Grundy相関）
- path: research/experiments/core-path-shift-structure-20261108/output/per_type.json
  role: data
  note: 六点純三点辺全10688型のbest_shift・best_match・perfect_shiftフラグ
- path: research/experiments/core-path-shift-structure-20261108/output/shift_probe_le5.json
  role: data
  note: 五点以下513型の集計（134末尾ブロック・134純シフト・offset 1..7・核Grundy相関）
- path: research/experiments/core-path-shift-structure-20261108/output/per_type_le5.json
  role: data
  note: 五点以下全513型のbest_shift・best_match・perfect_shiftフラグ
scope: K0682の手法で全長認証済みの二族。六点純三点辺核10688型（prefix 0..1343、末尾窓L=900..1300）と五点以下rank≤3核513型（prefix 0..1069、末尾窓L=600..1000）。裸の道Grundy p、シフトs=-10..80の決定論的全走査。
evidence: 六点純三点辺は純シフト3445型（offset 1:429,2:2891,3:52,7:73）、末尾1825種（path-shiftは4種）。五点以下は純シフト134型（offset 1..7）、末尾134種（path-shiftは7種）。両族とも全型の末尾最小周期は34（1・2・17への退化は零）。純シフトの核Grundy相関は族依存：六点純三点辺は1か2のみ、五点以下は0・3も含む。
---

## 問いと設定

K0684は任意の固定核Cに長道を付けたGrundy f_C(L)が最終的に周期34になると予想する。
裸の道（path上のNode-Kayles）のGrundy列 p も最終周期34である。
もし f_C(L)=p_{L+s(C)}（核に依存するシフト）が全てのCで成り立つなら、
周期34は p から直ちに継承され、K0684の簡単な構造証明になる。
これを二つの認証済み族について検証した：六点純三点辺核10688型と、五点以下rank≤3核513型。

## 計算結果

各型を末尾窓で f_C(L)=p_{L+s}（s=-10..80）と走査し、完全一致を純シフトと判定する。

**六点純三点辺（窓L=900..1300、401点）：**
- 純シフトは **3445型（32%）** のみ。offset別 s=1:429、s=2:2891、s=3:52、s=7:73。
  最大クラス2891型は同一末尾ブロック（pの2シフト）を共有。
- 周期34末尾ブロック f_C(1000..1033) は **1825種**、うち p のシフトは **4種** だけ。
- 残り7243型は真に新しい周期34列。

**五点以下（窓L=600..1000、401点）：**
- 純シフトは **134型（26%）**。offsetは s=1:39、2:52、3:10、4:12、5:18、6:1、7:2 と広い。
- 末尾ブロック f_C(700..733) は **134種**、うち p のシフトは **7種**。
- 残り379型は新しい周期34列。

**両族共通：**
- 全型（10688＋513）の末尾最小周期は **34** で、周期1・2・17に退化する型は零。
- シフトに定数xorを許す f_C(L)=p_{L+s}⊕c も純シフトと同じ型しか拾わず、全て c=0。
  xor緩和は新しい型を生まない。

## 純シフトの核Grundy相関は族依存

純シフト型自身の（道を付けない）Grundy ordinary(C) とoffsetの対応は族で異なる。
六点純三点辺では g0=1（s=1,2,7）と g0=2（s=3）に限られ、g0=0の2018型・g0=4の30型は零。
一方五点以下では g0=0（s=4、12型）や g0=3（s=5、18型）にも純シフトが現れる。
したがって「g0≤2が必要」は六点純三点辺族の性質であり、普遍ではない。
どちらの族でも純シフトは十分条件ではなく（g0が同じでも非シフト型が多い）、部分族に過ぎない。

## 解釈と限界

両族とも大多数の核は p のシフトではない **真に新しい周期34列** を作る
（六点1821/1825種・五点以下127/134種の末尾が非シフト）。
したがってK0684の普遍周期34は「核が道をシフトするだけ」という機構では説明できず、
再帰自体の頑健な性質として理解する必要がある。
これは核が道をシフトするだけという証明戦略を排除する有限計算であり、K0684の証明・反証ではない。
対象は認証済みの六点純三点辺核と五点以下核に限る。二点辺混在の六点核や7点以上の末尾構造は別途である。