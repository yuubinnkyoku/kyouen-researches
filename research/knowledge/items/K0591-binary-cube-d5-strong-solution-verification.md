---
id: K0591
title: 五次元共六点禁止ゲームのK0546強解決を全局面独立再計算で完全再現し、包含極小禁止集合の誤用を確認
kind: verification
status: verified
topics: [variants, geometry, grundy, verification, maximum-safe]
aliases: []
relations:
- type: verifies
  target: K0546
  note: 安全局面数・最大石数・全Grundy分布・空盤値・初手分類・misère勝敗を独立実装で8項目すべて再現
- type: refutes
  target: K0568
  note: K0568のcircuit削減CNF（19,484,942節）は包含極小化の誤用でK_6上界の証明に使えないことを確認
artifacts:
- path: research/experiments/binary-cube-hyperplane-d5-strong-20261030/README.md
  role: log
  note: 手法・照合表・教訓・再現手順
- path: research/experiments/binary-cube-hyperplane-d5-strong-20261030/solve_d5.cpp
  role: verifier
  note: rank-check DFS列挙とpopcount降順DPの独立実装。57秒で全1,108,073局面
- path: research/experiments/binary-cube-hyperplane-d5-strong-20261030/results_d5.txt
  role: data
  note: 実行出力。安全局面分布・Grundy分布・初手分類
- path: research/experiments/binary-cube-hyperplane-d5-strong-20261030/results.json
  role: data
  note: 機械可読な照合結果と教訓
scope: 二値五次元超立方体 V_5={0,1}^5 の6点共超平面禁止ゲーム（退化含む）の全安全局面の再計算。K0546の結論の独立性検証と、石追加ゲームの包含極小禁止集合の構造確認。d≠5は対象外。
evidence: 独立実装（rank計算を追加点を含むC(k,5)個の6点組だけに行うDFS列挙＋真のゲーム子関係でのpopcount降順DP）で、安全局面1,108,073・最大石数7・Grundy分布（g=0が454,464、g=1が546,569、g=2が107,040）・空盤g=1・全32初手勝ち・misère後手必勝・misère全初手負けを再現し、K0546の記載8項目すべてと一致。
---

# K0546五次元強解決の独立再現とcircuit削減の誤り確認

二値五次元立方体の6点共超平面禁止ゲームについて、
[K0546](K0546-five-cube-hyperplane-strong-and-general-lower-bound.md)の
強解決を独立実装で全局面から再計算したところ、次の8項目がすべて一致した。

| 量 | 本検証 | K0546 |
|---|---:|---|
| 安全局面数 | 1,108,073 | 1,108,073 |
| 最大安全石数 | 7 | K=7 |
| 七石局面数 | 309,056 | 309,056 |
| Grundy分布 | 0: 454,464 / 1: 546,569 / 2: 107,040 | 0,1,2のみ |
| g=2の範囲 | 五石局面107,040個 | 五石局面107,040個 |
| 空盤通常Grundy | 1 | 1 |
| 通常の勝ち初手 | 全32点 | 全32初手勝ち |
| misère空盤・初手 | 後手必勝・全初手負け | 後手必勝・全初手負け |

## 教訓（一般に成り立つ構造）

1. **石追加ゲームの包含極小禁止集合**は「禁止サイズの依存集合そのもの」である。
   依存サイズ未満の集合は合法なので、依存(禁止サイズ)集合をcircuit化
   （包含極小化）すると禁止が緩み、証明が無効になる。
   K0568でd=6に適用したcircuit削減CNFはこの誤りを含むため、
   そのCNFでのkissat実行（8h10mでSIGTERM終了しUNSAT判定は未取得）は
   K_6上界の証明にならない。
2. **全局面列挙型ソルバの子関係**は「未使用頂点のうち着手可能な全て」から
   再計算しなければならない。列挙のDFS経路（昇順追加）で子を記録すると
   子集合が真に小さくなり、Grundy値が誤る（空盤g=7という誤値が出た）。

## 計算

実装はC++1つ（`solve_d5.cpp`、WSL1コアで57秒）。
rank判定は $p=2^{61}-1$ 上の消去で、Hadamard限界 $6^3<p$ により
整数rankと同値。misèreのP局面は546,569個で通常g=1の個数と一致し、
0↔1交換則の成分とも整合する。

d=6以上への同方式の直接適用、Grundy値の個別局面リストは対象外。
