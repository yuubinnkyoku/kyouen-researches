---
id: K0080
title: 10×10 subset CSVのstateは入力座標で、D4正規形とは限らない
kind: proposition
status: computed
topics:
- provenance
aliases:
- F-B
relations: []
artifacts:
- path: research/archive/hypothesis-ledgers/findings.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: scripts/analysis/cache_core_classify.py
  role: verifier
  note: 入力座標とD4正規形の照合
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
---

# 10×10 subset CSVのstateは入力座標で、D4正規形とは限らない

results/10x10のsubset表は入力局面を保存し、outcome cacheのキーはD4正規形。例えば[2,61,90]の正規形は[9,16,20]。異なる局面を各々正規化すると同じ元盤の点ラベルの対応は保たれない。

固定ルートR内で共通点を調べるなら同一座標frameで行う。canonical局面間の文字通りの包含判定を、元のRのsubset包含と同一視しない。
