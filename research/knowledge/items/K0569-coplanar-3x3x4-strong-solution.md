---
id: K0569
title: 3×3×4・4点共面禁止版は全局面強解決され空盤Grundy値は3
kind: proposition
status: computed
topics: [variants, geometry, grundy, maximal-safe, maximum-safe, strategy-length]
aliases: []
relations:
- type: depends_on
  target: K0529
  note: 同じ4点共面禁止家族の容量定理（3×3×4では最大8石・最小極大3石）とm≤3の強解決。本項目はその有限盤拡張
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
  note: 最大層1,028配置のD4×Z2軌道分割（65軌道）を再現する第三の確認
- path: research/experiments/coplanar-3x3x4-q4-20261027/results.md
  role: data
  note: m=1〜3回帰照合とm=4の全集計（層別局面数・終局数・g/h分布・初手軌道表）
scope: 3×3×4整数格子・4点共面のみ禁止・全安全局面の通常Grundyとmisère補助mex
solution:
  board: 3×3×4・4点共面禁止
  level: strong
  outcome: first-player-win
  classification: [root, first-moves, all-safe-win-loss, all-safe-grundy]
  coverage: 全525,595安全局面の通常Grundyとmisère補助mex
  conditions: 3次元共面4点のみ禁止、退化を含む、3×3×4
  verification: [exhaustive-enumeration, independent-enumeration]
  certificate: 安全集合の昇順全生成による階層mex。証明書ファイル形式ではなく再生成可能な列挙
  independent_check: PythonのLeibniz行列式列挙とC++の外積行列式DFSが、禁止組数・層別局面数・層別終局数・g/h分布・全36初手の値まで一致
  note: g(空)=3、h(空)=3。通常の勝ち初手は端面中央（1,1,0）と（1,1,3）の2点のみ。8石最大配置1,028個はD4×Z2で65軌道
---

# 3×3×4の共面4点禁止版

3×3×4整数格子（36点）で4点共面のみを禁止する版は全局面強解決された。禁止4点組は8,569、安全局面は525,595、最大安全石数は8、最小極大石数は3（容量は[K0529](K0529-coplanar-three-by-three-prism-capacity-and-cube-grundy.md)の全称結果と一致）。

空盤の通常Grundy値は3、misère補助mexは3で、全局面の最大nimberは g/h とも5。通常版の勝ち初手は端面の中央2点だけであり、子のGrundy値が0になる初手はその軌道のみである。8石の最大配置1,028個は箱対称群 D4×Z2（位数16）の下で65軌道（サイズ4が1軌道、サイズ16が64軌道）に分かれる。

層別局面数は 1, 36, 630, 7,140, 50,336, 184,496, 228,680, 53,248, 1,028。終局は3石100、5石1,120、6石60,376、7石45,816、8石1,028。

## 現在の根拠と限界

根拠は有限完全列挙であり、Python（Leibniz行列式・昇順生成・階層mex）とC++（外積行列式・DFSメモ化、点順序も異なる）の二方式が全集計と全初手値で一致した。m=1,2,3 では両方式とも K0529 の公表値に回帰一致する。数学的全称証明ではなく、3×3×5以上や他の断面への拡張は含まない（3×3×5は[K0570](K0570-coplanar-3x3x5-strong-solution.md)）。
