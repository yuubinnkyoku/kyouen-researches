---
id: K0285
title: staged10k→top11→1MはV3十二親でLOSS shortlist recall12/12
kind: proposition
status: observed
topics:
- search-methods
- statistics
aliases: []
relations:
- type: depends_on
  target: K0284
  note: 同じ独立probe意味論・凍結方向
artifacts:
- path: docs/10X10_STAGED_V3_HOLDOUT_RESULT.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: results/10x10/staged-v3-holdout/primary_summary.json
  role: data
  note: 凍結primaryの完了
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: results/10x10/staged-v3-holdout/top11_shortlist.manifest.json
  role: manifest
  note: shortlist固定hash
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: results/10x10/staged-v3-holdout/top11_rank_1m.manifest.json
  role: manifest
  note: label開示前の順位hash
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
---

# staged10k→top11→1MはV3十二親でLOSS shortlist recall12/12

新凍結十二親1144childへfresh10k、事前K11shortlist132childへfresh1M、順位hashを固定してから全exact835WIN/309LOSSで検証。主要10k top11に≥1LOSSがある親は12/12、Wilson95%[.76,1]。非自明な十一親も全て達成。

secondary 1M shortlist順位中央値1、top1 recall10/12、staged probe143.44M対full1M仮定1144Mで87.5%削減。これは分類・recallの結果でnative solver wall-clock加速の結果ではない。
