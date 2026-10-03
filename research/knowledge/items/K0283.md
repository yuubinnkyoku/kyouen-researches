---
id: K0283
title: fresh-process memo-descは既知七親でdefaultとrandom双方より遅い
kind: proposition
status: observed
topics:
- search-methods
- statistics
aliases: []
relations: []
artifacts:
- path: docs/10X10_CORRECTED_PROBE_VS_SOLVER_ORDER.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: results/10x10/blind-probe-corrected/corrected-analysis.json
  role: data
  note: 独立測定の全七親
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
---

# fresh-process memo-descは既知七親でdefaultとrandom双方より遅い

10×10既知七親・batch0各20child・1M budgetで独立memo-descのfirst LOSS順位は[9,19,20,16,15,2,9]、defaultは[2,3,18,8,3,1,6]。全七で悪化、差中央値+7、順位差和49。random medianにも0better/7worse。

この結果はdescending規則と固定七親の範囲。ascendingへ方向を変えた規則や独立別cohortに同じ否定を広げない。
