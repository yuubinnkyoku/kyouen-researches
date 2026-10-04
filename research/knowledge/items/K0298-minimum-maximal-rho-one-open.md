---
id: K0298
title: n≥2の全最小極大配置で故障耐性ρが1か
kind: question
status: open
topics:
- maximal-safe
- geometry
aliases: []
relations:
- type: supersedes
  target: K0206
  note: n=1でρが定義できない問題を除外したB361の修正版
- type: depends_on
  target: K0026
  note: ''
artifacts:
- path: research/experiments/original-claims/reports/round47-private-cover-and-global-minima.md
  role: source
  note: n=2..8の全最小極大でρ=1を完全確認
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/reports/round50-nine-board-private-point-family.md
  role: source
  note: n=9の限定16配置でもρ=1
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
---

# n≥2の全最小極大配置で故障耐性ρが1か

安全極大配置Sに対し、元から空だった点を少なくとも一つ合法に戻すために除く必要がある最小石数をρ(S)とする。n≥2の最小極大配置では常にρ(S)=1かを問う。

n=2..8では全最小極大配置を完全列挙し、全件でρ=1を確認済み。一重被覆点がある場合は、その禁止三つ組の石を一つ除けばその空点が合法になるのでK0297が成立する範囲では本問も成立する。n=9の既知限定16配置でもρ=1だが、全最小極大配置の結果ではない。

B361のn=1を含む原文はK0206で撤回し、この非退化版を一般問題として残す。
