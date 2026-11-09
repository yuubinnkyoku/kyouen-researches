---
id: K0716
title: Q_2647の保存1302点安全集合は全1345個の単点追加を禁止四点で阻止する包含極大集合
kind: proposition
status: computed
topics: [geometry, maximal-safe, verification]
aliases: []
relations:
- type: depends_on
  target: K0001
  note: 共線または共円四点を含まない標準q=4の安全性
- type: depends_on
  target: K0026
  note: 包含極大と最大サイズを区別する
- type: depends_on
  target: K0711
  note: 指定1302点集合自体の安全性を確認した独立整数幾何receipt
artifacts:
- path: research/experiments/parabola-bounded-exchange-20261109/output/target1302-remove3-budget100000/candidate.txt
  role: certificate
  note: 本項で固定する1302点集合。SHA-256 5395d232...、原点と完全対d=1323を含む
- path: research/experiments/parabola-bounded-exchange-20261109/output/target1302-remove3-budget100000/geometry.json
  role: data
  note: 指定集合自体の安全性を独立整数幾何で確認した受理記録
- path: research/experiments/parabola-maximal-1302-20261109/output/initial/blockers.txt
  role: certificate
  note: 未選択1345点すべてに、追加tと既存3点からなる明示的禁止四点を1個ずつ指定
- path: research/experiments/parabola-maximal-1302-20261109/output/initial/audit.json
  role: data
  note: 全補集合被覆・相異性・所属・整数行列式0を受理し7不正制御を拒否。sourceと証拠hash付き
- path: research/experiments/parabola-maximal-1300-20261109/verify_blockers.cpp
  role: verifier
  note: CNFを読まず、明示四点の整数幾何と補集合の完全被覆を検査する既存C++wrapper
- path: research/experiments/parabola-maximal-1302-20261109/audit.py
  role: verifier
  note: CNFは候補提案のみに使い、全行を明示四点へ変換して別C++実装で検査
- path: research/experiments/parabola-maximal-1302-20261109/README.md
  role: source
  note: 対象集合・証明形式・再現と包含極大性の論理
scope: 指定SHA-256のQ_2647内1302点集合Sの包含極大性だけ。他の1302点集合、最大安全サイズA(2647)=1302、点交換不能は主張しない。
evidence: Sの安全性の既存独立幾何検査と、全未選択1345点に対する明示禁止四点証明を組み合わせた有限検査。検査器はCNF・SATソルバを使わず全四点の整数4×4行列式0を受理した。
---

## 対象と命題

p=2647、Q_p={(t,t² mod p):0<=t<p}とし、Sは指定artifactの1302パラメータの集合。
入力SHA-256は `5395d2326e08dfe8ac43b57103cc1d469ceddf68a0b522b4d7092e9db342000b`。
このSは安全であり、任意のt∈{0,...,2646}∖SについてS∪{t}は安全でない。
従ってSは包含極大である。

## 有限証明

S自体の安全性は、全119187179475四点を完全な合同式フィルタと45110020候補の
generic整数4×4行列式で被覆した、同じinput hashの既存検査による。
今回は未選択1345点すべてについて、tをちょうど一度含み、他の3点がSに属する
相異なる四点を明示した。整数行列式は全行で0だった。

検査器は追加点の範囲・未選択性・重複なし・全補集合の被覆を確認する。
各S∪{t}に禁止四点が含まれるため追加不能であり、安全性の部分集合への遺伝性から
Sを真に含む安全集合も存在しない。生出力は `VERIFIED_BLOCKERS 2647 1302 1345`、終了コード0。

生成では非空対1299側に二完全対の四点を使い、空対23の46側には直接投影CNFから候補を得た。
採用する証拠は明示四点の幾何であり、検査器はCNFやSATモデルを読まない。
欠落・余分データ・異なるp・追加点重複・既選択点・未ソート四点・非禁止四点の7制御を全拒否した。

## 限界と既存項目との区別

K0715は別の保存1300点集合を固定した包含極大性であり、本項は現在の保存1302点集合を固定する。
包含極大は最大性や点交換不能を意味しない。現在の全体範囲はK0711を参照する。
1302点から4点以下除去で1303点を要求した探索は10万衝突予算でUNKNOWNだが、
その未確定性とは独立に本項の単点追加不能を確認した。
検証器・コンパイラの一般健全性の形式証明やLean形式証明は主張しない。
