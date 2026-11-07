---
id: K0686
title: 純三点制約の六点Grundyは0・1・2・4のみで、値3の最小点数は値4より大きい
kind: proposition
status: computed
topics: [grundy, residual-games, geometry, variants]
aliases: []
relations:
- type: depends_on
  target: K0682
  note: 主計算は初手後の五点rank3核表を参照。独立C++ではこの表を使わない
- type: depends_on
  target: K0683
  note: 純三点残余族と最大値六型の有限整数点盤への実現
artifacts:
- path: research/experiments/pure-triple-maximum-grundy-six-20261107/proof.md
  role: proof
  note: 全六点族の有限完全分類、六軌道と八通りの辺追加区間、値0..5の最小点数
- path: research/experiments/pure-triple-maximum-grundy-six-20261107/scan.py
  role: solver
  note: 初手後の小核表による全1048576族の根値計算
- path: research/experiments/pure-triple-maximum-grundy-six-20261107/independent.cpp
  role: verifier
  note: 小核表・残余縮約を使わない全個別占有subsetのC++再帰
- path: research/experiments/pure-triple-maximum-grundy-six-20261107/audit.py
  role: verifier
  note: 全根値のbyte単位一致、全頂点置換、七点証人と具体整数幾何の監査
- path: research/experiments/pure-triple-maximum-grundy-six-20261107/output/six_census.json
  role: data
  note: 完全度数、辺数別度数、全値列SHA-256と最初の証人
- path: research/experiments/pure-triple-maximum-grundy-six-20261107/output/independent_audit.json
  role: certificate
  note: 全件一致・六軌道・最小点数・具体13点以上の整数盤証人
- path: research/log/2026-11-07-pure-triple-spectra-and-incidence-bounds.md
  role: log
  note: 小点数での欠番から少数辺数の全称上界・所属重み上界へ進んだ経緯
scope: 現在合法な六点上の全三点禁止族。二点辺なし、孤立点を許す。最小点数表は空ゲームを許し値0..5を対象。共円実現は指定有限整数点盤。
evidence: 全1048576ラベル付き族の全根値をPythonと独立C++でbyte単位比較。C++は34543617安全subsetを処理。5点以下も全数、七点達成例・六最大軌道の幾何を別検査。
---

## 六点の完全スペクトル

合法点が六個で、極小残余禁止辺が三点集合だけの場合、全2²⁰=1048576族のGrundy度数は

|g|0|1|2|3|4|5以上|
|---|---:|---:|---:|---:|---:|---:|
|件数|175252|851184|19620|0|2520|0|

である。最大は4で、途中の3は存在しない。
原始占有subsetの別C++実装で全34543617安全状態を計算し、全根値を1件ずつ比較して一致した。
全値列SHA-256は9c8c797ea841170f1a190dc7b71aaf5ab40cf4db6f6fa9037849e457456ce065。

## 最大値族の六型と最小点数

B={015,025,034,035,045,123,124}、E={012,013,014}とすると、
g=4の必要十分条件は、頂点置換後に **B⊆F⊆B∪E** と書けること。
Eの八つの追加方法を全720置換で動かした像が全2520族と一致し、同型を除くと六型。
六点でg=4を作る最小三点辺数は7、最小七辺型Bは同型を除き唯一である。

孤立点と空ゲームを許した純三点族で、Grundy値0..5の最小合法点数は

\[
 \boxed{m(0),m(1),m(2),m(3),m(4),m(5)=0,1,6,7,6,7.}
\]

5点以下は全数で値0または1。六点には2と4があり3がなく、
それぞれに孤立点を加えた七点ゲームで3と5を達成する。
孤立点なし・三点辺同士が高々一点で交わる七点のg=3証人も保存した。
最小実現点数はGrundy値に関して単調でない。

## 幾何実現と検証境界

六つの最大値型をK0683で整数点盤へ実現し、各盤の全四点と全安全局面を別検査した。
七辺型Bは **13点盤・7占有石・6合法点でg=4**。
二点競合グラフは空であり、二点だけの近似値は0となる。

本項は六点の有限完全分類と有限下界排除・達成例による最小性である。
一般点数の純三点Grundy無界性、g≥6の最小点数、全正方形格子盤での達成は未確定。
具体データと根拠は[完全分類の資料](../../experiments/pure-triple-maximum-grundy-six-20261107/proof.md)を参照。
