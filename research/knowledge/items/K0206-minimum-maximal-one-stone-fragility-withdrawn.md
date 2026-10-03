---
id: K0206
title: B361の全n版ρ=1はn=1で定義不全
kind: proposition
status: withdrawn
topics:
- maximal-safe
- geometry
aliases:
- B361
relations:
- type: depends_on
  target: K0026
  note: ''
artifacts:
- path: research/verification/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round47-private-cover-and-global-minima.md
  role: source
  note: ρの定義、n=1端点、n=2..8の全件検査
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round50-nine-board-private-point-family.md
  role: source
  note: n=9限定16配置のρ=1確認
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/hypothesis-bank-round2-2026-09-27.md
  role: source
  note: B361の原文
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
---

# B361の全n版ρ=1はn=1で定義不全

ρ(S)は、安全極大配置Sから石を除き、**元から空だった点**を少なくとも一つ合法に戻すために必要な最小除去数とする。除去した石の位置そのものを再着手可能になった点として数えない。

B361は全ての最小極大配置でρ(S)=1と主張していたが、n=1の唯一の最小極大配置には元から空だった点がない。この定義ではρは未定義であり、∞と拡張しても1ではない。従って原文の全n版はそのままでは数学的命題として採用せず撤回する。

非退化なn=2..8では全最小極大配置でρ=1を完全確認済みである。n=9の限定16配置も全件ρ=1だが、全最小極大を覆わない。修正版の一般問題はK0298へ分離する。
