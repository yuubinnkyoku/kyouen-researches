# 2026-10-29 高速研究：奇数全中心型と混合私有葉の全称公式

作業前に main=ced7bf150d08d60ee05e45f8ea48b7bae5799f9c、AGENTS.md、research/knowledge/README.md、generated/summary.md、既存の split-even-twin-signatures、odd-private-odd-universal-arbitrary-even、partitioned-centers-multigroup-universal-parity、K0336 を確認。11×11の長時間探索には触れていない。

既存結果の間に残る「全中心型が奇数、単点型の偶奇は中心ごとに混在、その他の真の非単点型は偶数」という場合を調査。生存中心集合 R の非孤立独立点数の偶奇が |O∩R|+1 に等しいことから、三値閉形式 g=1（奇数私有型中心0個）、2（正の奇数個）、3（正の偶数個）を予想した。

中心の手・全中心型の手・任意の真部分集合型の手を全て分類し、|R| による帰納法で全称証明。独立な名前付き頂点閉近傍削除と、型別の生存中心集合再帰を Python で実行し、n=2..4の限定完全列挙964構成とn=3..6の固定乱数280構成、計1244構成で不一致0。最大名前付き再帰状態数1277。全称性は有限標本からの外挿ではない。

偶数仮定の鋭さ：n=3で全中心型1枚だけなら g=1、二点型を奇数1枚追加すると g=2。抽象分割グラフの結果であり、格子実現可能性・11×11空盤勝敗は未確認。

成果は game-structure/odd-universal-mixed-private-parity-20261029 の README.md（証明）と verify.py（再現検証器）に保存。knowledge正本への昇格、生成物の再構築、全体CIは未実施。