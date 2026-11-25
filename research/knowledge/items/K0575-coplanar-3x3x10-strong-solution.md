---
id: K0575
title: 3×3×10・4点共面禁止版は全局面強解決され空盤Grundy値は2、辺中点の初手は全て負け手
kind: proposition
status: computed
topics: [variants, geometry, grundy, maximal-safe, maximum-safe, strategy-length]
aliases: []
relations:
- type: depends_on
  target: K0529
  note: 同じ4点共面禁止家族の容量定理（m≥5では最大9石・最小極大3石）。本項目は3×3×10の有限盤の強解決
- type: depends_on
  target: K0574
  note: 同じ家族の3×3×9の強解決。本項目はその次の m=10 を同じ方式で解いたもの
artifacts:
- path: research/experiments/coplanar-3x3x4-q4-20261027/README.md
  role: proof
  note: 実験の範囲・方式・再現手順（m=4,5,6,7,8,9,10を収録）
- path: research/experiments/coplanar-3x3x4-q4-20261027/enum3.cpp
  role: verifier
  note: Leibniz 4×4行列式・安全集合のボトムアップ全生成をディスク方式化したソルバ（レベルはファイル保持、評価は次レベルのハッシュシャード分割）。点順序 (x,y,z)/(z,y,x) 切替可能で、順序1では局面ハッシュを正準ラベルへ変換して集計。m=10 用に配列を99点まで拡張し、拡張後も m=7 で保存結果とバイト一致
- path: research/experiments/coplanar-3x3x4-q4-20261027/dfs_sub.cpp
  role: verifier
  note: 外積行列式・(z,y,x) 順序のDFSメモ化で、指定した1局面（初期石）を解く変種。初手サブツリーの独立検証用
- path: research/experiments/coplanar-3x3x4-q4-20261027/orbits_cpp.cpp
  role: verifier
  note: 最大層12,122,096配置のD4×Z2軌道分割（758,029軌道）を enum3 の最大層ダンプから数える確認（orbits_top.py の C++ 移植。m=9 のダンプから orbits_m9.json をバイト一致で再現して検証済み）
- path: research/experiments/coplanar-3x3x4-q4-20261027/results.md
  role: data
  note: m=1〜3回帰照合とm=10の全集計（層別局面数・終局数・g/h分布・初手の型別表）
scope: 3×3×10整数格子・4点共面のみ禁止・全安全局面の通常Grundyとmisère補助mex
solution:
  board: 3×3×10・4点共面禁止
  level: strong
  outcome: first-player-win
  classification: [root, first-moves, all-safe-win-loss, all-safe-grundy]
  coverage: 全649,610,028安全局面の通常Grundyとmisère補助mex
  conditions: 3次元共面4点のみ禁止、退化を含む、3×3×10
  verification: [exhaustive-enumeration, independent-enumeration]
  certificate: 安全集合の全生成による階層mex。証明書ファイル形式ではなく再生成可能な列挙
  independent_check: enum3.cpp の点順序2種（(x,y,z) のボトムアップ列挙と、(z,y,x) 順序・正準ラベル変換ハッシュ）が全集計・全90初手・全局面の (g,h) に対する順序非依存ハッシュ（xor=95f5c318f6491045、sum=d96c3fe53db4941b）までバイト一致。禁止組数327,602は外積C++とPythonのLeibniz数え上げでも一致し、外積DFS（dfs_sub.cpp）による角・中央・辺中点の初手サブツリー解も初手表と一致。enum3自体は99点拡張後も m=7 で既存の保存結果とバイト一致する回帰済み。最大層の軌道数は最大層ダンプ＋群作用の第三の計算（orbits_cpp.cpp、m=9で保存済みJSONとバイト一致を検証済み）で数えた
  note: g(空)=2、h(空)=2。勝ち初手は角40点と中央列10点の計50点で、辺中点40点は全て負け手（子の値は全z層で同一）。misèreで子のhが0になる初手は辺中点40点と中央列10点の計50点。最大nimberは5で、m=9から据え置き。9石最大配置12,122,096個はD4×Z2で758,029軌道。orbits_m10.json は21,982,584バイト（SHA-256 0a674a3092270ae27e9e644b26e32f9d5689efc34aef07bc59a483a1e1a09bdd）
---

# 3×3×10の共面4点禁止版

3×3×10整数格子（90点）で4点共面のみを禁止する版は全局面強解決された。禁止4点組は327,602、安全局面は649,610,028、最大安全石数は9、最小極大石数は3（容量は[K0529](K0529-coplanar-three-by-three-prism-capacity-and-cube-grundy.md)の全称結果と一致）。

空盤の通常Grundy値は2、misère補助mexも2である。初手は点の型できれいに割れる：角の40点と中央列 (1,1,z) の10点は子のGrundy値が0で勝ち手、辺中点の40点は全て子の値が1で負け手であり、子の値は全z層で同一（m=8・m=9と同じ型別パターン）。misère補助では辺中点と中央列が子の値を0にする。全局面の最大nimberは5であり、m=9に続いて5のままである（g=5 は169,344局面のみ）。9石の最大配置12,122,096個は箱対称群 D4×Z2（位数16）の下で758,029軌道（サイズ8が796軌道、サイズ16が757,233軌道）に分かれる。m=9にあったサイズ4の軌道は m=10 では現れない。

層別局面数は 1, 90, 4,005, 117,480, 2,227,588, 25,246,600, 140,138,400, 298,138,440, 171,615,328, 12,122,096。終局は3石1,480、6石4,783,440、7石56,801,624、8石111,031,104、9石12,122,096（4石・5石の終局はない）。g分布は 0:263,271,306、1:261,652,802、2:80,473,926、3:39,922,786、4:4,119,864、5:169,344。h分布は 0:261,684,972、1:263,249,554、2:80,462,566、3:39,921,968、4:4,121,968、5:169,000。

## 現在の根拠と限界

根拠は有限完全列挙であり、ディスク方式ソルバ enum3.cpp の点順序2種が全集計・全初手値・全局面の (g,h) に対する順序非依存ハッシュまでバイト一致した。幾何（禁止4点組の集合）は Leibniz 行列式・外積行列式・Python の3方式で数え上げが一致し、初手の代表サブツリーは外積DFSでも独立に解かれて一致した。数学的全称証明ではなく、m≥11 の Grundy は未解決のままである。
