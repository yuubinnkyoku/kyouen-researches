---
id: K0110
title: 公開証明書と探索記録の圧縮比はn1〜9で有限比較できる
kind: proposition
status: computed
topics:
- certificates
- search-methods
aliases:
- F-X
relations: []
artifacts:
- path: research/archive/hypothesis-ledgers/findings.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: results/results.csv
  role: data
  note: 探索状態数
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: results/certificates.csv
  role: manifest
  note: 公開証明書のノード数
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
---

# 公開証明書と探索記録の圧縮比はn1〜9で有限比較できる

指定results/results.csvとcertificates.csvのsearch_states/certificate_nodesはn1..3で1、n4..9で約1.53,4.75,2.39,10.32,4.11,4.24。9×9では約5708万探索状態に対し13457134証明書ノード。

指定探索profileの記録と証明DAGの比較であり、全安全局面に対する網羅率や最小証明書サイズを意味しない。16byte/node、9×9raw約215MBは当該形式のサイズ。
