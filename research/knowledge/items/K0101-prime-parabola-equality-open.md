---
id: K0101
title: 全奇素数で剰余放物線上界(p+3)/2が達成されるかは未確定
kind: question
status: open
topics:
- maximum-safe
- geometry
aliases: []
relations:
- type: depends_on
  target: K0097
  note: ''
artifacts:
- path: research/experiments/structural-lemmas-2026-10-02/quadratic-constructions.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/frontier-geometry-2026-10-05/proof.md
  role: proof
  note: 禁止四点の完全対分類とNAE・原点節の厳密な分解。全素数の充足可能性は未証明
- path: research/experiments/frontier-geometry-2026-10-05/recovered-witnesses.json
  role: certificate
  note: 131..251拡張の追跡されていなかった証人を回復・保存
- path: research/experiments/frontier-geometry-2026-10-05/density-probe-witnesses.json
  role: certificate
  note: 509,1009の追加有限等号証人
---

# 全奇素数で剰余放物線上界(p+3)/2が達成されるかは未確定

Q_p内の一般上界は証明済みで、5..251の全52奇素数で安全証人が等号を達成する。
5..127の29素数は既存独立検算。131..251の23素数については追跡されていなかった証人を回復し、
generic 4×4 Leibniz展開で全選択四点を再検査した。509,1009にも独立検査した有限証人がある。
全奇素数に同じ達成構成があるかは未証明。

K0334は、等号問題をある完全対dについてsigned NAE3/4と原点由来2/3リテラル節の
同時充足可能性へ正確に帰着した。その全称充足可能性も反例素数も未確定。
認証方式の上界や全盤K_pの既知下界とは別の問い。
