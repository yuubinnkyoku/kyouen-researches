# 2026-10-31 高速研究：全頂点数における樹のmisère交換則反例

最新mainの AGENTS.md、research/knowledge/README.md、既存の最小反例実験、K0336 とmisère独立双子縮約の証明を確認。既存結果は「最小の樹反例は8頂点」「C6に偶数枚の葉を付けた連結無限族」であり、**全ての頂点数における樹反例の存在**は未記録だった。

既存8頂点樹の頂点0に葉を1枚加えた9頂点樹を厳密再帰で計算し、(g,h)=(3,0) の新基底を発見。既存8頂点樹の (1,4) と組み合わせ、頂点0の独立双子葉の正の偶奇縮約を適用して、nが偶数なら(1,4)、奇数なら(3,0)となる樹を全n≥8で明示構成した。n≤7の不可能性は既存の全樹完全列挙を使用。

実装：research/experiments/game-structure/misere-swap-all-tree-orders-20261031/verify.py。ビット集合と名前付き頂点集合の別実装で、n=8..19の12構成について根と全初手の通常・misère値を一致検証。Python3でPASS、不一致0。

証明：research/experiments/game-structure/misere-swap-all-tree-orders-20261031/README.md。全称性は双子縮約の数学的証明に依拠し、有限検証を外挿しない。

残件：knowledge正本への昇格と生成物再構築・全体CI、実格子残余としての実現可能性。11×11の巨大探索は実行していない。
