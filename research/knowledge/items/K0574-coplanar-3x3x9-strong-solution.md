---
id: K0574
title: 3×3×9・4点共面禁止版は全局面強解決され空盤Grundy値は2、辺中点の初手は全て負け手
kind: proposition
status: computed
topics: [variants, geometry, grundy, maximal-safe, maximum-safe, strategy-length]
aliases: []
relations:
- type: depends_on
  target: K0529
  note: 同じ4点共面禁止家族の容量定理（m≥5では最大9石・最小極大3石）。本項目は3×3×9の有限盤の強解決
artifacts:
- path: research/experiments/coplanar-3x3x4-q4-20261027/README.md
  role: proof
  note: 実験の範囲・方式・再現手順（m=4,5,6,7,8,9を収録）
- path: research/experiments/coplanar-3x3x4-q4-20261027/enum3.cpp
  role: verifier
  note: Leibniz 4×4行列式・安全集合のボトムアップ全生成をディスク方式化したソルバ（レベルはファイル保持、評価は次レベルのハッシュシャード分割）。点順序 (x,y,z)/(z,y,x) 切替可能で、順序1では局面ハッシュを正準ラベルへ変換して集計
- path: research/experiments/coplanar-3x3x4-q4-20261027/dfs_sub.cpp
  role: verifier
  note: 外積行列式・(z,y,x) 順序のDFSメモ化で、指定した1局面（初期石）を解く変種。初手サブツリーの独立検証用
- path: research/experiments/coplanar-3x3x4-q4-20261027/orbits_top.py
  role: verifier
  note: 最大層2,610,624配置のD4×Z2軌道分割（163,323軌道）を、enum3の最大層ダンプから再現する確認（Python）
- path: research/experiments/coplanar-3x3x4-q4-20261027/results.md
  role: data
  note: m=1〜3回帰照合とm=9の全集計（層別局面数・終局数・g/h分布・初手の型別表）
scope: 3×3×9整数格子・4点共面のみ禁止・全安全局面の通常Grundyとmisère補助mex
solution:
  board: 3×3×9・4点共面禁止
  level: strong
  outcome: first-player-win
  classification: [root, first-moves, all-safe-win-loss, all-safe-grundy]
  coverage: 全266,673,210安全局面の通常Grundyとmisère補助mex
  conditions: 3次元共面4点のみ禁止、退化を含む、3×3×9
  verification: [exhaustive-enumeration, independent-enumeration]
  certificate: 安全集合の全生成による階層mex。証明書ファイル形式ではなく再生成可能な列挙
  independent_check: enum3.cpp の点順序2種（(x,y,z) のボトムアップ列挙と、(z,y,x) 順序・正準ラベル変換ハッシュ）が全集計・全81初手・全局面の (g,h) に対する順序非依存ハッシュまでバイト一致。禁止組数215,140は外積C++とPythonのLeibniz数え上げでも一致し、外積DFS（dfs_sub.cpp）による角・中央・辺中点の初手サブツリー解も初手表と一致。enum3自体は m=7（両順序）・m=8 で既存の保存結果とバイト一致する回帰済み。最大層の軌道数は最大層ダンプ＋群作用の第三の計算で一致
  note: g(空)=2、h(空)=2。勝ち初手は角36点と中央列9点の計45点で、辺中点36点は全て負け手（子の値は全z層で同一）。misèreで子のhが0になる初手は辺中点36点と中央列9点の計45点。最大nimberは5で、m=7・m=8の6から低下した。9石最大配置2,610,624個はD4×Z2で163,323軌道
---

# 3×3×9の共面4点禁止版

3×3×9整数格子（81点）で4点共面のみを禁止する版は全局面強解決された。禁止4点組は215,140、安全局面は266,673,210、最大安全石数は9、最小極大石数は3（容量は[K0529](K0529-coplanar-three-by-three-prism-capacity-and-cube-grundy.md)の全称結果と一致）。

空盤の通常Grundy値は2、misère補助mexも2である。初手は点の型できれいに割れる：角の36点と中央列 (1,1,z) の9点は子のGrundy値が0で勝ち手、辺中点の36点は全て子の値が1で負け手であり、子の値は全z層で同一（m=8と同じ型別パターン）。misère補助では辺中点と中央列が子の値を0にする。全局面の最大nimberは5であり、m=7・m=8 の 6 から低下した（g=5 は219,208局面のみ）。9石の最大配置2,610,624個は箱対称群 D4×Z2（位数16）の下で163,323軌道（サイズ4が6軌道、サイズ8が309軌道、サイズ16が163,008軌道）に分かれる。

層別局面数は 1, 81, 3,240, 85,320, 1,448,600, 14,560,840, 69,968,568, 123,329,864, 54,666,072, 2,610,624。終局は3石1,084、6石2,399,328、7石25,153,736、8石39,030,572、9石2,610,624（4石・5石の終局はない）。

## 現在の根拠と限界

根拠は有限完全列挙であり、ディスク方式ソルバ enum3.cpp の点順序2種が全集計・全初手値・全局面の (g,h) に対する順序非依存ハッシュまでバイト一致した。幾何（禁止4点組の集合）は Leibniz 行列式・外積行列式・Python の3方式で数え上げが一致し、初手の代表サブツリーは外積DFSでも独立に解かれて一致した。数学的全称証明ではなく、m≥10 の Grundy は未解決のままである。
