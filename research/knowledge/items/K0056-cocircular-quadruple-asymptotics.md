---
id: K0056
title: 非共線共円四点組数C_nはΘ(n^5)
kind: proposition
status: proved
topics:
- geometry
aliases: []
relations:
- type: refutes
  target: K0055
  note: 真円共円Θ(n^6)という旧漸近主張を否定
- type: refutes
  target: K0151
  note: 本文の証明・証人が原文に与える帰結
artifacts:
- path: research/experiments/original-claims/reports/round13-four-point-circles.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/reports/round17-original-scope-audit.md
  role: source
  note: 有限fitと公刊一般定理の訂正照合
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
---

# 非共線共円四点組数C_nはΘ(n^5)

repoのRound13はGhosal–Goenka–Keevashの公刊Theorem1.3を一次資料確認し、C_n=Θ(n^5)を採用する。原文B142のn^(4+o(1))は偽、Round5のn^6有力説も正しくない。

このK項目は既存資料に記録された外部定理の採用で、本repo独自の初出やLean形式化済みとは主張しない。repo内の論証はその定理を前提に派生結果を導く。
