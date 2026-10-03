---
id: K0138
title: 全nの最小極大配置に一重被覆点があるというB078はn=1で偽
kind: proposition
status: refuted
topics:
- maximal-safe
- geometry
aliases:
- B078
relations:
- type: depends_on
  target: K0026
  note: ''
artifacts:
- path: research/verification/round47-private-cover-and-global-minima.md
  role: source
  note: n=1の退化端点とn=2..8の全最小極大の完全検査
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round50-nine-board-private-point-family.md
  role: source
  note: n=9の限定16配置での追加確認
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/hypothesis-bank-2026-09-27.md
  role: source
  note: B078の原文
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
---

# 全nの最小極大配置に一重被覆点があるというB078はn=1で偽

B078の原文は、最小極大配置Sには空点pで `b_S(p)=1` となるものが必ず存在する、という全称命題である。n=1の唯一の最小極大配置は盤面全体を占有する一石配置で、空点が存在しない。従って原文をn=1まで含めて読むと存在節は偽であり、B078は反証される。

一方、退化端点を除いた結果は強い。n=2..8では全ての最小サイズ極大配置を完全列挙し、全件で `min b=1` を確認している。n=9でも8×8極大配置から作った限定族16配置は全件 `min b=1` だったが、n=9の全最小極大カタログではない。

非退化版の一般問題はK0297へ分離する。
