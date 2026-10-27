---
id: K0570
title: 3×3×5・4点共面禁止版は全局面強解決され全45初手が勝ち手
kind: proposition
status: computed
topics: [variants, geometry, grundy, maximal-safe, maximum-safe, strategy-length]
aliases: []
relations:
- type: depends_on
  target: K0529
  note: 同じ4点共面禁止家族の容量定理（3×3×5では最大9石・最小極大3石、最大9の真の開始長は5）。本項目はその有限盤の強解決
artifacts:
- path: research/experiments/coplanar-3x3x4-q4-20261027/README.md
  role: proof
  note: 実験の範囲・方式・再現手順
- path: research/experiments/coplanar-3x3x4-q4-20261027/verify.py
  role: verifier
  note: Leibniz 4×4行列式・安全集合の昇順全生成・階層mex（Python）
- path: research/experiments/coplanar-3x3x4-q4-20261027/independent.cpp
  role: verifier
  note: 外積行列式・uint64_tマスク・空盤DFSメモ化による独立再計算（C++、点順序はPythonと異なる）
- path: research/experiments/coplanar-3x3x4-q4-20261027/orbits.py
  role: verifier
  note: 最大層304配置のD4×Z2軌道分割（19軌道）を再現する確認
- path: research/experiments/coplanar-3x3x4-q4-20261027/results.md
  role: data
  note: m=1〜3回帰照合とm=5の全集計（層別局面数・終局数・g/h分布・初手分類）
scope: 3×3×5整数格子・4点共面のみ禁止・全安全局面の通常Grundyとmisère補助mex
solution:
  board: 3×3×5・4点共面禁止
  level: strong
  outcome: first-player-win
  classification: [root, first-moves, all-safe-win-loss, all-safe-grundy]
  coverage: 全2,588,710安全局面の通常Grundyとmisère補助mex
  conditions: 3次元共面4点のみ禁止、退化を含む、3×3×5
  verification: [exhaustive-enumeration, independent-enumeration]
  certificate: 安全集合の昇順全生成による階層mex。証明書ファイル形式ではなく再生成可能な列挙
  independent_check: PythonのLeibniz行列式列挙とC++の外積行列式DFSが、禁止組数・層別局面数・層別終局数・g/h分布・全45初手の値まで一致
  note: g(空)=1、h(空)=2。全45初手とも子のgが0で全て勝ち手。misèreで子のhが0になるのは中央列（1,1,z）の5点のみ。9石最大配置304個はD4×Z2で19軌道（全てサイズ16）
---

# 3×3×5の共面4点禁止版

3×3×5整数格子（45点）で4点共面のみを禁止する版は全局面強解決された。禁止4点組は20,787、安全局面は2,588,710、最大安全石数は9、最小極大石数は3（容量は[K0529](K0529-coplanar-three-by-three-prism-capacity-and-cube-grundy.md)の全称結果と一致し、最大9石の真の開始長が5であることの有限側の裏付けになる）。

空盤の通常Grundy値は1、misère補助mexは2で、全局面の最大nimberは g/h とも6。全45初手とも子局面のGrundy値が0であり、全初手が通常版の勝ち手である。misère補助では中央列の5点だけが子の値を0にする。9石の最大配置304個は箱対称群 D4×Z2（位数16）の下で19軌道に分かれ、すべてサイズ16である。

層別局面数は 1, 45, 990, 14,190, 128,208, 632,296, 1,206,448, 569,960, 36,268, 304。終局は3石194、5石532、6石121,008、7石363,688、8石33,548、9石304。

## 現在の根拠と限界

根拠は有限完全列挙であり、Python（Leibniz行列式・昇順生成・階層mex）とC++（外積行列式・DFSメモ化、点順序も異なる）の二方式が全集計と全初手値で一致した。m=1,2,3 では両方式とも K0529 の公表値に回帰一致する。数学的全称証明ではない。3×3×6 は[K0571](K0571-coplanar-3x3x6-strong-solution.md)で強解決され、m≥7 の Grundy は未解決のままである。
