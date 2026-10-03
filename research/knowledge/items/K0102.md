---
id: K0102
title: 具体巨大証明書をLean核のみで検査する実装は未完成
kind: question
status: open
topics:
- formalization
- certificates
aliases: []
relations:
- type: depends_on
  target: K0009
  note: ''
artifacts:
- path: docs/PROOF_STATUS.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
---

# 具体巨大証明書をLean核のみで検査する実装は未完成

一般健全性はLeanで形式化されているが、具体binary証明書のparseと全局所条件は外部C++/Rustに依存する。具体証明書をLean核のみで最後まで検査する開発は残件。

単にLeanがビルドできることを具体9×9勝敗の核検査完了とは表現しない。
