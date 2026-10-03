---
id: K0038
title: 10×10には安全な十石極大配置が存在する
kind: proposition
status: proved
topics:
- maximal-safe
aliases:
- F-AT
relations:
- type: depends_on
  target: K0026
  note: ''
- type: refutes
  target: K0146
  note: 本文の証明・証人が原文に与える帰結
artifacts:
- path: research/verification/round49-ten-stone-maximal-counterexample.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round49_s10_verified.json
  role: data
  note: 全四点安全性と全外点極大性の独立検算
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
---

# 10×10には安全な十石極大配置が存在する

点番号x+10yでS=[21,27,31,35,36,46,65,81,29,48]。全210四点組が安全、全90外点が禁止でありs_10≤10。

旧F-ATの不安全な三例は使わない。同じ存在命題の現在の正しい証人へ更新する。これだけから最小極大=10や最大安全=10を結論しない。
