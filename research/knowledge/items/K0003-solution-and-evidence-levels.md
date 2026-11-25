---
id: K0003
title: 解決段階と計算・証明書・監査の区別
kind: definition
status: active
topics:
- rules
- verification
aliases: []
relations: []
artifacts:
- path: README.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: docs/PROOF_STATUS.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
---

# 解決段階と計算・証明書・監査の区別

超弱解決は空盤の結果のみ、弱解決は初期局面からその結果を実現する戦略、強解決は任意の合法局面の勝敗と最適手を決定すること。全安全局面P/Nがあれば子を列挙して勝ち手を選べる。全Grundyはさらに強い情報。

全初手の分類と空盤の勝敗は別の知識。独立CSV監査、全局所条件を検査する証明書、探索器の完了計算、Leanの一般健全性は異なる根拠。solution metadataは段階・範囲・条件・証明書・独立検査を別に記録する。
