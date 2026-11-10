---
id: K0723
title: Q_2539の安全最大サイズは1258以上1271以下、保存1258点集合は包含極大
kind: proposition
status: computed
topics: [geometry, maximum-safe, maximal-safe, verification]
aliases: []
relations:
- type: depends_on
  target: K0001
  note: 共線または共円四点を含まない標準q=4の安全性
- type: depends_on
  target: K0097
  note: 一般上界A(p)<=(p+3)/2をp=2539に適用
- type: depends_on
  target: K0334
  note: 整数禁止四点のパラメータ和が0 mod pとなる必要条件による完全フィルタ
- type: depends_on
  target: K0026
  note: 固定集合の包含極大性と最大サイズを区別する
- type: depends_on
  target: K0712
  note: 空対を許す固定原点・完全対の三値選択を候補探索に使う。安全下界の採用は独立幾何による
artifacts:
- path: research/experiments/parabola-p2539-exchange-20261110/maximal-output/candidate.txt
  role: certificate
  note: 現在の1258パラメータ。SHA-256 454f0e293fd846aa6616dd45500dbaf9b325834408ec7f69234852e3e35e22fb
- path: research/experiments/parabola-p2539-exchange-20261110/maximal-output/blockers.txt
  role: certificate
  note: 現在の集合外1281点すべてに対する、追加点と既存三点からなる明示禁止四点
- path: research/experiments/parabola-p2539-exchange-20261110/maximal-output/verification.json
  role: data
  note: 新規安全性receiptへのhash bindingと全阻止四点の独立Bareiss受理
- path: research/experiments/parabola-p2539-exchange-20261110/audit-output/summary.json
  role: data
  note: 1255〜1258点の全モデル・入力byte再生成・独立整数幾何。二つの負の結果はソルバ主張のまま
- path: research/experiments/parabola-p2539-exchange-20261110/audit.py
  role: verifier
  note: 全モデルを直接評価して点を別に抽出し、探索辺・CNFに依存しない整数幾何を実行
- path: research/experiments/parabola-p2539-exchange-20261110/certify_maximal.py
  role: verifier
  note: 現在の安全性receiptへ結び付け、全補集合の明示四点を別Bareiss検査へ渡す
- path: research/experiments/parabola-p2539-exchange-20261110/search.py
  role: solver
  note: 完全対d=6を保つ有界交換。補助変数の予約上限を保持した二つのcounter
- path: research/experiments/parabola-p2539-exchange-20261110/regression.json
  role: data
  note: 小素数の13194三値割当てで点数下限・種からの削除上限・整数幾何を全数照合
- path: research/experiments/parabola-p2539-exchange-20261110/output/target1259-remove3/result.json
  role: manifest
  note: 除去上限3のソルバUNSATとローカル保持proof.drat.gzの解凍後hash・行数。独立未監査
- path: research/experiments/parabola-p2539-exchange-20261110/output/target1259-remove4/result.json
  role: manifest
  note: 除去上限4のソルバUNSATとローカル保持228249行proof.drat.gzのhash。独立未監査
- path: research/experiments/parabola-p2539-exchange-20261110/README.md
  role: source
  note: 交換探索・保存証拠監査・極大性証明の再現手順と非達成の未確定性
- path: research/experiments/parabola-p2539-pair-pilot-20261110/augmented-output/candidate.txt
  role: certificate
  note: 改善前の1254点極大集合。今回の四段階の交換の種として保持
- path: research/experiments/parabola-p2539-pair-pilot-20261110/replay.json
  role: data
  note: 改善前1254点集合の別処理実再生と全1285阻止四点のPython Bareiss独立検査、五制御
- path: research/experiments/parabola-p2539-pair-pilot-20261110/verify_saved.py
  role: verifier
  note: ソルバ・辺cache・局所モデルを読まず固定集合と全阻止証拠を再検査
- path: research/experiments/parabola-local-repair-20261109/verify_subset.cpp
  role: verifier
  note: 完全な合同式フィルタとgeneric 4x4 Leibniz整数行列式による集合安全性
- path: research/experiments/parabola-p2539-pair-pilot-20261110/regression.json
  role: data
  note: 小素数192割当ての符号化全数照合、修復制御、不正阻止証拠五種の拒否
- path: research/experiments/parabola-p2539-pair-pilot-20261110/projection-controls.json
  role: data
  note: 非自明辺のあるp17,p19の6656割当てを全数照合し安全・禁止の両側を検査
- path: research/experiments/parabola-p2539-pair-pilot-20261110/output/plan.json
  role: manifest
  note: 固定完全対12件の有限予算pilot、source・入力hashと元cache所在
- path: research/experiments/parabola-p2539-pair-pilot-20261110/output/summary.json
  role: data
  note: UNKNOWN 11件とソルバのみのUNSAT 1件。等号不達成の証明としては採用しない
- path: research/experiments/parabola-p2539-pair-pilot-20261110/local-output/summary.json
  role: data
  note: 三つの局所探索からの修復結果。最良1253点を独立幾何で検査してから拡張
- path: research/experiments/parabola-p2539-pair-pilot-20261110/augmented-output/trials.json
  role: data
  note: 九つの貪欲拡張trialと最良集合の由来。全trialの独立安全性は主張しない
- path: research/experiments/parabola-p2539-pair-pilot-20261110/README.md
  role: source
  note: 再現手順・証拠の保存境界・探索と独立検査の区別
scope: Q_2539={(t,t² mod 2539):0<=t<2539}の1258<=A(2539)<=1271、および指定SHA-256の1258点集合Sの包含極大性。正確値、等号1271の達成・不達成、他の1258点集合の極大性、点交換不能は主張しない。
evidence: 下界は指定集合の全103857542570四点を被覆する合同式フィルタと40996021候補のgeneric整数4x4検査。集合外1281点を一度ずつ覆う明示四点の所属と零行列式を独立Python Bareissで確認し、安全性receiptと入力hashを照合。上界はK0097の一般証明。
---

## 命題と固定集合

**1258 <= A(2539) <= 1271**。交換experimentのmaximal-output/candidate.txtの集合Sは安全であり、包含極大である。
各パラメータtは整数座標(t,t² mod 2539)へ写す。
SのSHA-256は `454f0e293fd846aa6616dd45500dbaf9b325834408ec7f69234852e3e35e22fb`。
原点と完全対{6,2533}を含み、空対は13個である。
最大サイズの上界1271はK0097による。安全下界と固定集合の極大性は2026-11-10の有限独立検査による。

## 安全性と極大性の検査

generic整数4x4 Leibniz検査器は、K0334の必要条件に基づき選択三点から唯一の第四候補を列挙する。
全103857542570四点を被覆し、合同式を満たす40996021候補すべての整数行列式が非零だった。
合同式を満たすことだけを共円性とは扱わない。

集合外の全1281点tについて、tとS内の相異なる三点からなる禁止四点をblockers.txtへ保存した。
追加点の重複・欠落がないこと、四点の相異性・範囲・所属、整数行列式0を確認した。
探索辺からの生成とは別のPython fraction-free Bareiss検査で全1281行を受理した。
安全性の独立幾何receipt、候補入力、阻止証拠のhash bindingも確認した。
Sは安全だが各S∪{t}は安全でないため、Sを真に含む安全集合も存在しない。
この証明は探索辺cacheの完全性やソルバの判定に依存しない。

## 探索の経緯と未解決部分

固定完全対dの12ケースを各10万衝突で試したところ、11件がUNKNOWN、d=1237だけがソルバUNSATだった。
後者のDRATは独立未検査であり、全dの排除でもない。
三ケースの局所探索と削除修復で得た最良1253点集合に、降順拡張で2533を追加して旧1254点極大集合を得た。
その後、完全対d=6と原点を固定し、各段階で3点以下を除く交換を四回行って1255,1256,1257,1258点へ改善した。
四つの保存入力をbyte再生成し、全モデルの節評価・独立な点抽出・交換差分・各集合の独立整数幾何を確認した。
1258点から1259点を求める除去上限3と4の二入力はソルバUNSATだったが、DRAT独立監査は未実施。
この二結果を交換不能や全体上界の根拠には採用しない。
局所探索の違反節数最小化や貪欲修復は最適性を保証しない。

小素数p=5,7,11で全192符号割当てを直接整数幾何と比較し、完全対辺を除いた投影CNFの同値性を照合した。
この三素数の非自明辺は空なので、別にp=17,19の6656割当てを全数照合し、非空節と安全・禁止の両側を検査した。
保存証拠の欠落・重複・既選択点・重複頂点・非零行列式を含む五改変を拒否した。
これらは有限回帰であり、検査器やコンパイラ全体の形式的健全性証明ではない。
交換の二counterについてはp=5,7,17の全13194三値割当てで点数・削除上限と直接整数幾何を照合した。
包含極大性は最大性や点交換による改善不能を意味しない。
**A(2539)の正確値と等号達成は未解決**であり、不達成が独立監査された四素数へ2539を追加しない。
