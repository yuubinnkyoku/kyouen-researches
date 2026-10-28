---
id: K0573
title: 3×3×8・4点共面禁止版は全局面強解決され空盤Grundy値は2、辺中点の初手は全て負け手
kind: proposition
status: computed
topics: [variants, geometry, grundy, maximal-safe, maximum-safe, strategy-length]
aliases: []
relations:
- type: depends_on
  target: K0529
  note: 同じ4点共面禁止家族の容量定理（m≥5では最大9石・最小極大3石）。本項目は3×3×8の有限盤の強解決
artifacts:
- path: research/experiments/coplanar-3x3x4-q4-20261027/README.md
  role: proof
  note: 実験の範囲・方式・再現手順（m=4,5,6,7,8を収録）
- path: research/experiments/coplanar-3x3x4-q4-20261027/independent_128.cpp
  role: verifier
  note: 外積行列式・unsigned __int128マスク・空盤DFSメモ化（C++、点順序は (z,y,x)）。メモ表は自前open-addressing表
- path: research/experiments/coplanar-3x3x4-q4-20261027/enum2_128.cpp
  role: verifier
  note: Leibniz 4×4行列式・安全集合のボトムアップ全生成・上位層からのmexによる独立再計算（C++、点順序は (x,y,z)）
- path: research/experiments/coplanar-3x3x4-q4-20261027/orbits_top.py
  role: verifier
  note: 最大層473,864配置のD4×Z2軌道分割（29,670軌道）を、enum2_128の最大層ダンプから再現する確認（Python）。m=7ではorbits.pyの出力を完全再現
- path: research/experiments/coplanar-3x3x4-q4-20261027/results.md
  role: data
  note: m=1〜3回帰照合とm=8の全集計（層別局面数・終局数・g/h分布・初手の型別表）
scope: 3×3×8整数格子・4点共面のみ禁止・全安全局面の通常Grundyとmisère補助mex
solution:
  board: 3×3×8・4点共面禁止
  level: strong
  outcome: first-player-win
  classification: [root, first-moves, all-safe-win-loss, all-safe-grundy]
  coverage: 全102,167,785安全局面の通常Grundyとmisère補助mex
  conditions: 3次元共面4点のみ禁止、退化を含む、3×3×8
  verification: [exhaustive-enumeration, independent-enumeration]
  certificate: 安全集合の全生成による階層mex。証明書ファイル形式ではなく再生成可能な列挙
  independent_check: C++の外積行列式DFS（independent_128.cpp）と、Leibniz行列式・ボトムアップ列挙の別実装enum2_128.cpp（いずれも128bitマスク拡張）が、禁止組数・層別局面数・層別終局数・g/h分布・全72初手の値に加え、全 (局面, g, h) に対する順序非依存ハッシュまで一致。最大層の軌道数は最大層ダンプ＋群作用の第三の計算で一致
  note: g(空)=2、h(空)=2。勝ち初手は角32点と中央列8点の計40点で、辺中点32点は全て負け手（子の値は全z層で同一）。misèreで子のhが0になる初手は辺中点32点と中央列8点の計40点。9石最大配置473,864個はD4×Z2で29,670軌道
---

# 3×3×8の共面4点禁止版

3×3×8整数格子（72点）で4点共面のみを禁止する版は全局面強解決された。禁止4点組は134,062、安全局面は102,167,785、最大安全石数は9、最小極大石数は3（容量は[K0529](K0529-coplanar-three-by-three-prism-capacity-and-cube-grundy.md)の全称結果と一致）。

空盤の通常Grundy値は2、misère補助mexも2で、全局面の最大nimberは6（g=6は104局面のみ）。初手は点の型できれいに割れる：角の32点と中央列 (1,1,z) の8点は子のGrundy値が0で勝ち手、辺中点の32点は全て子の値が1で負け手である。子の値は全z層で同一であり、m=7にあった中央層だけの例外（z=3の辺中点の子のgが3）は現れない。misère補助では辺中点と中央列が子の値を0にする。9石の最大配置473,864個は箱対称群 D4×Z2（位数16）の下で29,670軌道（サイズ8が107軌道、サイズ16が29,563軌道）に分かれる。

層別局面数は 1, 72, 2,556, 59,640, 894,728, 7,858,880, 32,088,864, 45,707,336, 15,081,844, 473,864。終局は3石760、6石1,116,944、7石10,614,096、8石11,809,900、9石473,864（4石・5石の終局はない）。

## 現在の根拠と限界

根拠は有限完全列挙であり、C++（外積行列式・DFSメモ化）と enum2_128.cpp（Leibniz行列式・ボトムアップ全生成・上位層からのmex、点順序も異なる）の二方式を128bitマスクへ拡張したものが、全集計・全初手値・全局面の (g,h) に対する順序非依存ハッシュまで一致した。両実装は m=4〜7 で既存の保存結果と完全一致することも確認済みである。数学的全称証明ではなく、m≥9 の Grundy は未解決のままである。
