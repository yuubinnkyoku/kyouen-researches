---
id: K0572
title: 3×3×7・4点共面禁止版は全局面強解決され空盤Grundy値は2、辺中点の初手は全て負け手
kind: proposition
status: computed
topics: [variants, geometry, grundy, maximal-safe, maximum-safe, strategy-length]
aliases: []
relations:
- type: depends_on
  target: K0529
  note: 同じ4点共面禁止家族の容量定理（m≥5では最大9石・最小極大3石）。本項目は3×3×7の有限盤の強解決
artifacts:
- path: research/experiments/coplanar-3x3x4-q4-20261027/README.md
  role: proof
  note: 実験の範囲・方式・再現手順（m=4,5,6,7を収録）
- path: research/experiments/coplanar-3x3x4-q4-20261027/independent.cpp
  role: verifier
  note: 外積行列式・uint64_tマスク・空盤DFSメモ化（C++、点順序は (z,y,x)）
- path: research/experiments/coplanar-3x3x4-q4-20261027/enum2.cpp
  role: verifier
  note: Leibniz 4×4行列式・安全集合のボトムアップ全生成・上位層からのmexによる独立再計算（C++、点順序はverify.pyと同じ (x,y,z)）
- path: research/experiments/coplanar-3x3x4-q4-20261027/orbits.py
  role: verifier
  note: 最大層55,240配置のD4×Z2軌道分割（3,466軌道）を再現する確認（Python）
- path: research/experiments/coplanar-3x3x4-q4-20261027/results.md
  role: data
  note: m=1〜3回帰照合とm=7の全集計（層別局面数・終局数・g/h分布・初手軌道表）
scope: 3×3×7整数格子・4点共面のみ禁止・全安全局面の通常Grundyとmisère補助mex
solution:
  board: 3×3×7・4点共面禁止
  level: strong
  outcome: first-player-win
  classification: [root, first-moves, all-safe-win-loss, all-safe-grundy]
  coverage: 全34,414,528安全局面の通常Grundyとmisère補助mex
  conditions: 3次元共面4点のみ禁止、退化を含む、3×3×7
  verification: [exhaustive-enumeration, independent-enumeration]
  certificate: 安全集合の全生成による階層mex。証明書ファイル形式ではなく再生成可能な列挙
  independent_check: C++の外積行列式DFSと、Leibniz行列式・ボトムアップ列挙の別実装enum2.cppが、禁止組数・層別局面数・層別終局数・g/h分布・全63初手の値まで一致。最大層の軌道数はPythonの第三の生成でも一致
  note: g(空)=2、h(空)=2。勝ち初手は角28点と中央列7点の計35点で、辺中点28点は全て負け手（中央層z=3の辺中点は子のgが3）。misèreで子のhが0になる初手は辺中点28点と中央列7点の計35点。9石最大配置55,240個はD4×Z2で3,466軌道
---

# 3×3×7の共面4点禁止版

3×3×7整数格子（63点）で4点共面のみを禁止する版は全局面強解決された。禁止4点組は78,881、安全局面は34,414,528、最大安全石数は9、最小極大石数は3（容量は[K0529](K0529-coplanar-three-by-three-prism-capacity-and-cube-grundy.md)の全称結果と一致）。

空盤の通常Grundy値は2、misère補助mexも2で、全局面の最大nimberは6。初手は m=5,6（全初手勝ち）と異なり軌道できれいに割れる：角の28点と中央列 (1,1,z) の7点は子のGrundy値が0で勝ち手、辺中点の28点は全て負け手である（子の値は、中央層 z=3 の辺中点だけ3、他は1）。misère補助では逆に辺中点と中央列が子の値を0にする。9石の最大配置55,240個は箱対称群 D4×Z2（位数16）の下で3,466軌道（サイズ4が2軌道、サイズ8が24軌道、サイズ16が3,440軌道）に分かれる。

層別局面数は 1, 63, 1,953, 39,711, 516,784, 3,873,468, 12,935,728, 13,935,264, 3,056,316, 55,240。終局は3石515、5石2、6石492,592、7石4,241,496、8石2,625,044、9石55,240。

## 現在の根拠と限界

根拠は有限完全列挙であり、C++（外積行列式・DFSメモ化）と enum2.cpp（Leibniz行列式・ボトムアップ全生成・上位層からのmex、点順序も異なる）の二方式が全集計と全初手値で一致した。enum2.cpp は m=4,6 でも既存結果と完全一致する。m=1,2,3 では DFS 側が K0529 の公表値に回帰一致する。数学的全称証明ではなく、m≥8 の Grundy は未解決のままである。
