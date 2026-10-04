---
id: K0087
title: 9×9 pair成分factorial四比較はHolm補正後いずれも棄却なし
kind: proposition
status: observed
topics:
- statistics
- search-methods
aliases: []
relations: []
artifacts:
- path: research/experiments/9x9-factorial/reports/9X9_FACTORIAL_EXACT_PC_RUN_RESULT.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: results/9x9/factorial/primary-summary.csv
  role: data
  note: 四本の事前Holm家族と記述量
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/9x9-factorial-execution-base/holdout.manifest.csv
  role: manifest
  note: 凍結対象と除外規則
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
---

# 9×9 pair成分factorial四比較はHolm補正後いずれも棄却なし

凍結holdoutで4/4比較、3403/3403行exact完了、失敗・memo-over0。E@O0 n1024、O@E0 n715、E@O1 n1024、O@E1 n639。Holm pは0.2033282,0.7188043,0.7188043,0.9057226でFWER0.05の棄却なし。

記述ΔLOSSは+0.041992,+0.029371,+0.025391,−0.004695。O比較は事前固定の未観測有限母集団censusで、p値を標本抽出誤差と解釈しない。freeze commit9ebc79ea1e8c2b35fe8d76c397491cf984f216e2。
