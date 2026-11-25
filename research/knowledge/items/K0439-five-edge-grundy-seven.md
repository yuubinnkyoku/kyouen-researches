---
id: K0439
title: 5個の残余禁止集合でGrundy値7を達成する抽象回避ゲーム
kind: proposition
status: proved
topics:
- grundy
- residual-games
- variants
aliases: []
relations: []
artifacts:
- path: research/experiments/fastlane-five-edge-nimber-seven-20261019/README.md
  role: proof
  note: 5辺の値7、4点一様5辺の値6、任意hへの直和拡張と限界
- path: research/experiments/fastlane-five-edge-nimber-seven-20261019/verify.py
  role: verifier
  note: 全占有ビット集合による完全mex計算
- path: research/experiments/fastlane-five-edge-nimber-seven-20261019/independent.cpp
  role: verifier
  note: 未占有集合を用いた独立C++再帰検算
- path: research/experiments/fastlane-five-edge-nimber-seven-20261019/crosscheck.py
  role: verifier
  note: 全4864部分集合についてPythonと独立C++の状態表を完全照合
- path: research/experiments/fastlane-five-edge-nimber-seven-20261019/result.json
  role: data
  note: 全局面のハッシュとGrundy分布
- path: research/experiments/knowledge-audit-20261021/README.md
  role: log
  note: 証明の論理監査・再実行範囲・判定
evidence: '2026-10-21監査。全4864部分集合を占有集合Pythonと未占有集合C++で照合。3点禁止成分の値0・4点禁止成分の値1による直和拡張を確認。 監査記録: research/experiments/knowledge-audit-20261021/README.md。'
---


## 命題・範囲

包含極小禁止集合をちょうど5個持ち、各禁止集合の大きさが2〜4である有限抽象回避ゲームには、空局面Grundy値7を実現する9頂点の例がある。また、禁止集合がちょうど5個ですべて4点の場合にも、空局面Grundy値6を実現する12頂点の例がある。

任意の整数 `h>=5` について、禁止集合がちょうどh個、各集合の大きさ2〜4である抽象回避ゲームで空局面Grundy値7を実現できる。さらに、6個すべて4点の禁止集合で空局面Grundy値7を実現できる。

## 現在の根拠と限界

`research/experiments/fastlane-five-edge-nimber-seven-20261019/README.md` に明示した禁止集合について、全ビット集合のmexをPythonと独立C++で照合し、全4864局面で一致した。9頂点例の頂点0は自由点であり、残り8頂点のGrundy値6に1を排他的論理和して7を得る。9頂点例の初手子Grundy値は `[6,1,2,5,4,3,2,0,4]` である。無限hへの拡張は、Grundy値0の独立した3点禁止集合の直和と排他的論理和による数学的証明。

上界や最小頂点数は主張しない。整数格子の共円・共線禁止4点組としての実現、標準正方形盤の実際の残余局面としての実現は未確認。各集合が2点や3点になることは、元の4点禁止集合ゲームで既に石が置かれた場合の抽象的残余制約に対応するが、幾何的な実現可能性を意味しない。
