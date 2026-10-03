---
id: K0112
title: 乱貪欲の最小観測サイズは真の最小極大サイズと一致しない
kind: proposition
status: observed
topics:
- maximal-safe
- search-methods
aliases:
- F-AS
- F-BC
relations:
- type: depends_on
  target: K0026
  note: ''
artifacts:
- path: research/findings.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
---

# 乱貪欲の最小観測サイズは真の最小極大サイズと一致しない

旧固定seed乱探索で8×8最小観測10、9×9は11、修正後10×10の12000試行では11。後の厳密結果はs8=8、s9=9、十盤にも安全極大10石の証人がある。従って標本内最小を一般下界として使えない。

F-ASの「標本下界」という記載は全体の最小への向きが逆。安全・極大な陽例はs_nの上界だけを与える。打切り未発見は非存在証明でない。
