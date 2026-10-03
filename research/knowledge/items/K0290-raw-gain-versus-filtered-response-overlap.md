---
id: K0290
title: 9×9 raw gainとfiltered responseのpair重複は異なる量
kind: proposition
status: proved
topics:
- geometry
- search-methods
aliases: []
relations:
- type: depends_on
  target: K0085
  note: ''
artifacts:
- path: docs/MOVE_ORDERING_AUDIT.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: docs/10X10_HOLDOUT_CONFIRMATION_RESULT.md
  role: source
  note: raw/filtered訂正と回帰範囲
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: scripts/kyouen9_pairsum.py
  role: verifier
  note: 二つの量を別modeで計算
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: tests/test_pairsum.py
  role: verifier
  note: raw重複fixtureとC++照合
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
---

# 9×9 raw gainとfiltered responseのpair重複は異なる量

raw pair gainはT(new distinct)+E(existing danger)+O(overlap)。全局所量の過大計数を調べるraw modeと、「他の禁止四点を全て除いた安全応答」のfiltered modeを分ける。filteredではE′=O′=0になる構成を使う。

旧標本1635/1635のpairTop=exactTop、約18万対O0はfiltered量であり、raw量の重複不在を証明しない。raw O>0/E>0 fixtureを含むC++照合回帰でモードを分離した。
