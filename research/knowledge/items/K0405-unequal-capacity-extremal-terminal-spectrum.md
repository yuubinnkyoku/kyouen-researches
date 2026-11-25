---
id: K0405
title: 容量上限Mの全異容量ゲームで均一容量が終局スペクトル3指標を同時最大化
kind: proposition
status: proved
topics:
- variants
- maximal-safe
- statistics
- strategy-length
aliases: []
relations:
- type: depends_on
  target: K0403
  note: 一般容量の終局閾値・差分分類を使う
artifacts:
- path: research/experiments/capacity-unequal-extremal-spectrum-20261010/README.md
  role: proof
  note: 3指標の鋭い全称上界・同時達成
- path: research/experiments/capacity-unequal-extremal-spectrum-20261010/verify.py
  role: verifier
  note: 独立極大配置列挙
- path: research/experiments/capacity-unequal-extremal-spectrum-20261010/verify.log
  role: data
  note: 有限監査記録
scope: 容量上限Mを持つ全異容量上位h列ゲーム
evidence: 一般容量の終局差分上界と均一容量による鋭さ。
---

上位h列和制約、列数w、各容量 `0<=c_i<=M` を考える。`n=w−h`, `Delta=max(0,min(M,floor(r/h))−max(0,r−(h−1)M))` と置けば、全容量ベクトル上の鋭い最大値は終局石数の幅 `n Delta`、欠番数 `max(0,n−1)Delta`、相異なる終局石数 `1+(Delta if n>0 else 0)`。3つとも均一容量で同時達成する。

任意容量の極大閾値区間・差分から上界を証明し、均一容量で等号を構成する全称定理。有限全占有列挙は監査である。Grundy値や幾何盤実現は対象外。
