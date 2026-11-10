---
id: K0719
title: Q_2647の保存1300点安全集合は全1347個の単点追加を禁止四点で阻止する包含極大集合
kind: proposition
status: computed
topics: [geometry, maximal-safe, verification]
aliases: []
relations:
- type: depends_on
  target: K0001
  note: 共線または共円の四点を含まない標準q=4の安全性
- type: depends_on
  target: K0026
  note: 包含極大と最大サイズを区別する
artifacts:
- path: research/experiments/parabola-warm-improvement-20261109/output/target1299-warm1298-budget500000/candidate.txt
  role: certificate
  note: 本項で固定する1300点集合。input SHA-256 4ef5b03e...、原点と完全対1323を含む
- path: research/experiments/parabola-warm-improvement-20261109/output/target1299-warm1298-budget500000/geometry.json
  role: data
  note: この集合自体の安全性を独立整数幾何検査した受理記録
- path: research/experiments/parabola-maximal-1300-20261109/output/initial/blockers.txt
  role: certificate
  note: 各未選択tに対し、tと既存3点からなる真の禁止四点を1個ずつ記す全1347行
- path: research/experiments/parabola-maximal-1300-20261109/output/initial/audit.json
  role: data
  note: 全1347点被覆・四点の所属と整数行列式0を受理し、7不正制御を拒否したsource/binary/hash付き記録
- path: research/experiments/parabola-maximal-1300-20261109/verify_blockers.cpp
  role: verifier
  note: CNFを読まず、明示四点の幾何と補集合の重複なし完全被覆だけを検査する独立wrapper
- path: research/experiments/parabola-maximal-1300-20261109/audit.py
  role: verifier
  note: 既存CNFは候補提案だけに用い、証明を明示四点へ変換してC++で再検査するドライバ
- path: research/experiments/parabola-maximal-1300-20261109/README.md
  role: source
  note: 固定点集合、証明形式、単点追加不能から包含極大への論理と再現手順
scope: Q_2647の指定SHAの1300点集合Sだけについての包含極大性。最大安全サイズA(2647)=1300や他の1300点集合の性質は主張しない。
evidence: Sの安全性の既存独立幾何receiptと、補集合1347点すべてを被覆する明示禁止四点証明を組み合わせた有限検査。新しいC++wrapperは全行の正確な整数4×4行列式0を受理した。
---

## 対象と命題

p=2647、Q_p={(t,t² mod p):0<=t<p}、Sは指定artifactの1300パラメータの集合。
入力ファイルSHA-256は `4ef5b03ed0679a9c47bfebb3ea6581d85af5ea50b46151e219581721c5fde7ad`。
このSは安全であり、任意のt∈{0,...,2646}∖SについてS∪{t}は安全でない。
したがってSはQ_p内で包含極大である。

## 有限証明

S自体の安全性は、全118455690925四点を必要合同式と44831921候補の整数行列式で被覆した既存検査による。
追加不能性は、補集合の1347点それぞれについて、tをちょうど一度含み、残る3点はSに属する
相異なる四点を証明書に列挙して確認した。全四点の正確なgeneric整数4×4行列式は0だった。

検査器は追加tの範囲・未選択性・重複なしを調べ、証明行数がp-|S|で全補集合を被覆することを確認する。
全行が真の禁止四点なので、各S∪{t}は安全でない。
安全性は部分集合へ遺伝するため、Sを真に含む安全集合も存在し得ない。

生成では、非空対への追加は固定完全対と二つ目の完全対を作ることを使い、
空対25の50側については既存の直接投影CNFから候補を探した。
採用する証明は明示四点の幾何であり、検査器はCNFやSATモデルを読み込まない。
欠落行・余分データ・異なるp・追加点の重複・既選択点・未ソート四点・非禁止四点の7制御を拒否した。

## 限界

包含極大は最大性を意味しない。より大きい安全集合を探す場合、Sの点をいくつか置き換える必要がある。
全Q_pの最大安全サイズの現在の境界は[K0711](K0711-p2647-safe-lower-bound-1292.md)を参照する。
これは指定有限証明の検査であり、検査器・コンパイラの形式的健全性証明ではない。
