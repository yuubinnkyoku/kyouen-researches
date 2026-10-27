---
id: K0571
title: 3×3×6・4点共面禁止版は全局面強解決され全54初手が勝ち手、最大nimberは7
kind: proposition
status: computed
topics: [variants, geometry, grundy, maximal-safe, maximum-safe, strategy-length]
aliases: []
relations:
- type: depends_on
  target: K0529
  note: 同じ4点共面禁止家族の容量定理（m≥5では最大9石・最小極大3石）。本項目は3×3×6の有限盤の強解決
artifacts:
- path: research/experiments/coplanar-3x3x4-q4-20261027/README.md
  role: proof
  note: 実験の範囲・方式・再現手順（m=4,5,6を収録）
- path: research/experiments/coplanar-3x3x4-q4-20261027/verify.py
  role: verifier
  note: Leibniz 4×4行列式・安全集合の昇順全生成・階層mex（Python）
- path: research/experiments/coplanar-3x3x4-q4-20261027/independent.cpp
  role: verifier
  note: 外積行列式・uint64_tマスク・空盤DFSメモ化による独立再計算（C++、点順序はPythonと異なる）
- path: research/experiments/coplanar-3x3x4-q4-20261027/orbits.py
  role: verifier
  note: 最大層5,376配置のD4×Z2軌道分割（338軌道）を再現する確認
- path: research/experiments/coplanar-3x3x4-q4-20261027/results.md
  role: data
  note: m=1〜3回帰照合とm=6の全集計（層別局面数・終局数・g/h分布・初手分類）
scope: 3×3×6整数格子・4点共面のみ禁止・全安全局面の通常Grundyとmisère補助mex
solution:
  board: 3×3×6・4点共面禁止
  level: strong
  outcome: first-player-win
  classification: [root, first-moves, all-safe-win-loss, all-safe-grundy]
  coverage: 全10,447,786安全局面の通常Grundyとmisère補助mex
  conditions: 3次元共面4点のみ禁止、退化を含む、3×3×6
  verification: [exhaustive-enumeration, independent-enumeration]
  certificate: 安全集合の昇順全生成による階層mex。証明書ファイル形式ではなく再生成可能な列挙
  independent_check: PythonのLeibniz行列式列挙とC++の外積行列式DFSが、禁止組数・層別局面数・層別終局数・g/h分布・全54初手の値まで一致
  note: g(空)=1、h(空)=2。全54初手とも子のgが0で全て勝ち手。misèreで子のhが0になるのは中央列（1,1,z）の6点のみ。全局面の最大nimberは7（g=7は8局面のみ）。9石最大配置5,376個はD4×Z2で338軌道
---

# 3×3×6の共面4点禁止版

3×3×6整数格子（54点）で4点共面のみを禁止する版は全局面強解決された。禁止4点組は42,519、安全局面は10,447,786、最大安全石数は9、最小極大石数は3（容量は[K0529](K0529-coplanar-three-by-three-prism-capacity-and-cube-grundy.md)の全称結果と一致）。

空盤の通常Grundy値は1、misère補助mexは2。全54初手とも子局面のGrundy値が0であり、全初手が通常版の勝ち手である（3×3×5と同型の初手構造）。misère補助では中央列の6点だけが子の値を0にする。全局面の最大nimberは7で、g=7 を取る局面は8個しかない。9石の最大配置5,376個は箱対称群 D4×Z2（位数16）の下で338軌道（サイズ8が4軌道、サイズ16が334軌道）に分かれる。

層別局面数は 1, 54, 1,431, 24,804, 273,732, 1,705,368, 4,494,080, 3,473,456, 469,484, 5,376。終局は3石324、5石164、6石217,608、7石1,482,728、8石423,680、9石5,376。

## 現在の根拠と限界

根拠は有限完全列挙であり、Python（Leibniz行列式・昇順生成・階層mex）とC++（外積行列式・DFSメモ化、点順序も異なる）の二方式が全集計と全初手値で一致した。m=1,2,3 では両方式とも K0529 の公表値に回帰一致する。数学的全称証明ではなく、m≥7 の Grundy は未解決のままである（m=7 は安全局面数がさらに桁で増える見込みで、今回の素朴な全列挙の単純延長では重い）。
