---
id: K0044
title: 公開9×9証明書の末端は16石WIN十個から17石飽和LOSS一個へ閉じる
kind: proposition
status: computed
topics:
- certificates
- maximal-safe
aliases:
- F-A
- H7
relations:
- type: depends_on
  target: K0007
  note: ''
artifacts:
- path: research/archive/hypothesis-ledgers/findings.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: scripts/analysis/cert_terminal.py
  role: verifier
  note: 具体証明書末端の合法手を再生成
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
---

# 公開9×9証明書の末端は16石WIN十個から17石飽和LOSS一個へ閉じる

16石WIN末端ノード10個は各合法手1でwitnessと一致、17石LOSS末端ノード1個は合法手0。全64空点について整数幾何で追加不能を確認した。

これは公開証明書中の末端族の記述。9×9の最小極大=17でも最大安全=17でもなく、全16石局面の分類でもない。
