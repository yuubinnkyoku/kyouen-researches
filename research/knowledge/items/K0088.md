---
id: K0088
title: 9×9 factorial全体符号差は共有親interactionよりmembership差に由来
kind: proposition
status: observed
topics:
- statistics
aliases: []
relations:
- type: depends_on
  target: K0087
  note: ''
artifacts:
- path: docs/9X9_FACTORIAL_EFFECT_HETEROGENEITY.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: results/9x9/factorial/effect-heterogeneity/o-full-census-summary.json
  role: data
  note: 不足子補完後のfull801/702記述
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: results/9x9/factorial/effect-heterogeneity/o-full-4outcome.csv
  role: data
  note: 470親のinteraction
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
---

# 9×9 factorial全体符号差は共有親interactionよりmembership差に由来

O共有親419でE0 net−6・E1 net−7、interaction−1。O0-only296 net+27、O1-only220 net+4でoverall差−24=(-1)+4−27。E共有親254のnet−3/−6に対しonly側+46/+32。

不足201 unique childを解いてfull O801/702を再構成した後、net+19/+6、4outcome全470親はI−1:2,0:466,+1:2、|I|=2なし。初期「full census再構成不可」は後日の補完で更新済み。これはsecondary/exploratoryでprimary Holmは変えない。
