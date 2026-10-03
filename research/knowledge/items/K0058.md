---
id: K0058
title: 旧円上最大点数走査は半整数中心に限定され、全有理中心最大は要監査
kind: proposition
status: needs-review
topics:
- geometry
- provenance
aliases:
- F-K
relations: []
artifacts:
- path: research/findings.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: scripts/analysis/explore_circle_formula_and_collinear.py
  role: solver
  note: 中心走査の実際の範囲
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round4-circle-windows.md
  role: source
  note: 一般有理中心と円窓の解析
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
---

# 旧円上最大点数走査は半整数中心に限定され、全有理中心最大は要監査

F-Kはn=2..31の最大円点数とプラトーを述べるが、再現走査は半整数中心族を主に扱う。後日の有理中心分母・円窓解析は一般有理中心を別途扱っているため、半整数中心走査の最大を全円の最大と断定しない。

F-K本文内にもn=8..24で16という例示とn=8..11で12という列の不一致がある。一般二平方和表現数式は有効でも、有限盤最大には全中心・埋込範囲の証明が必要。現在の採用範囲は当該探索族に限る。
