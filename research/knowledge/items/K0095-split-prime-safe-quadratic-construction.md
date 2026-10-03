---
id: K0095
title: p≡1 mod4の全素数に安全p点の有限体二次構成がある
kind: proposition
status: proved
topics:
- maximum-safe
- geometry
aliases: []
relations:
- type: depends_on
  target: K0001
  note: ''
- type: supports
  target: K0143
  note: 本文の証明・証人が原文に与える帰結
artifacts:
- path: research/verification/round61-full-split-prime-safe-construction.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round61_split_prime_verified.json
  role: data
  note: 三点・四点合同式と独立整数検算
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
---

# p≡1 mod4の全素数に安全p点の有限体二次構成がある

a²=−1 modp、全t∈F_pで(x,y)=(t²+t,a(t²−t))の0..p−1整数代表を取る。x−a^-1 y=2tで単射、四点行列式は8a Vandermondeで非零modpだから整数でも非零。K_p≥p。

全12素数5..101の独立検算は証明を支持する有限資料。既知線形下界の自足再構成で、B088の2n−O(1)や全盤最大の改善は示さない。
