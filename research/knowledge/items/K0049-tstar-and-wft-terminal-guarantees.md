---
id: K0049
title: 勝敗維持終局集合T*と固定長強制集合WFTの区別・偶奇則
kind: proposition
status: proved
topics:
- strategy-length
aliases: []
relations:
- type: depends_on
  target: K0002
  note: ''
artifacts:
- path: research/experiments/original-claims/reports/round28-seven-board-original-verdicts.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
---

# 勝敗維持終局集合T*と固定長強制集合WFTの区別・偶奇則

T*はN局面でP子、P局面で全合法子の終局サイズ集合を和集合にする。
WFTはN局面でP子の和集合、P局面で全合法子の積集合を取る。
終局では双方が現在石数だけを含む単元集合。WFT⊆T*で、T*内の終局石数の偶奇は `(|S|+1_{g(S)>0}) mod2`。

全ての勝敗維持対局で同じ勝者が保証されても、相手の選択を越えて事前宣言した終局サイズを保証できるとは限らない。固定証明書witness戦略の長さ集合とも別。
