---
id: K0714
title: 四次元二値立方体・共面四点禁止版は通常とmisèreの全局面を分類
kind: computation
status: computed
topics: [variants, geometry, grundy, maximal-safe, maximum-safe]
aliases: []
relations:
- type: depends_on
  target: K0713
  note: 全次元の共面四点と中点一致の同値。有限計算は整数アフィン小行列式でも独立に判定
artifacts:
- path: research/experiments/coplanar-4cube-q4-20261109/verify.py
  role: verifier
  note: 整数アフィン小行列式による禁止組と全安全局面の再帰
- path: research/experiments/coplanar-4cube-q4-20261109/independent_midpoint_audit.py
  role: verifier
  note: 対角線中点による禁止組生成と全状態の下からの再帰
- path: research/experiments/coplanar-4cube-q4-20261109/compare_states.py
  role: verifier
  note: 頂点順序の対応を計算し全部分集合の安全性と全安全局面の値を一件ずつ照合
- path: research/experiments/coplanar-4cube-q4-20261109/state-comparison.json
  role: data
  note: 全65536部分集合と8193安全局面の比較、層別Grundy・misère集計
- path: research/experiments/coplanar-4cube-q4-20261109/results.md
  role: source
  note: 元の完全列挙集計。独立照合以前の記録として保持
scope: 四次元二値立方体の実数アフィン共面四点禁止・全安全局面。通常Grundy値とmisère手番側勝敗。
solution:
  board: 四次元二値立方体・共面四点禁止
  level: strong
  outcome: second-player-win
  classification: [root, first-moves, all-safe-win-loss, all-safe-grundy, safe-layers]
  coverage: 全65536部分集合の安全性、8193安全局面の通常Grundy値とmisère勝敗
  conditions: 相異なる4頂点が同一アフィン2平面上にあれば禁止、通常プレイとmisère
  verification: [exhaustive-enumeration, independent-enumeration]
  certificate: 有限盤の全部分集合と再帰値を再生成。保存された個別局面証明書ではない
  independent_check: アフィン小行列式・空盤からの再帰と中点生成・逆順DPを、頂点順序を対応させて全局面一件ずつ照合
  note: 通常・misèreとも空盤は後手勝ち。全16初手後は通常Grundy 1、misère手番側勝ち
---

# 四次元二値立方体の共面四点禁止版

盤 `{0,1}^4` で同一アフィン2平面の四頂点を禁止すると、禁止四点組は100個、安全局面は8193個。石数0〜7別の安全局面数は `1,16,120,560,1720,3168,2368,240`。極大配置は6石1008個・7石240個なので、最大安全石数7、最小極大石数6。

通常プレイの空盤Grundy値は0、misèreでも空盤は手番側負けで、ともに後手勝ち。全16初手の子は通常Grundy値1、misère手番側勝ち。これは[K0545](K0545-four-cube-hyperplane-strong-and-binary-rectangles.md)の**共面五点禁止**とは異なるルールである。

元の整数アフィン小行列式・再帰と、独立した中点生成・逆順DPについて、頂点順序の対応を明示して全65536部分集合の安全性、および全8193安全局面の通常Grundy値とmisère勝敗を一件ずつ照合した。元の列挙スクリプトには関数名の誤記があり、実行できなかったため修正して再計算した。これは有限完全列挙であり、他の次元の勝敗や無限族の強解決を意味しない。
