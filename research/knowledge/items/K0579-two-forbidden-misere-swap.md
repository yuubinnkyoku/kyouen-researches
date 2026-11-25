---
id: K0579
title: 包含極小禁止集合が高々二つの配置ゲームでは通常・misèreのGrundy交換則が全安全局面で成立する
kind: proposition
status: proved
topics: [grundy, variants, residual-games, first-moves]
aliases: []
relations:
- type: depends_on
  target: K0483
  note: 二禁止集合の通常Grundy閉公式と値の上界3
- type: depends_on
  target: K0002
  note: 終局を1とするmisère補助mex値の定義
artifacts:
- path: research/experiments/two-forbidden-misere-swap-20261031/proof.md
  role: proof
  note: 低値の子補題とmex交換恒等式による全称帰納証明
- path: research/experiments/two-forbidden-misere-swap-20261031/verify.py
  role: verifier
  note: n≤7全10795族とn=8..12の1000標本、2383752安全局面の直接mex照合
scope: 任意有限集合の一点追加ゲーム、包含極小禁止集合0〜2個、通常・misère二人ゲーム、全安全局面
evidence: K0483の閉公式から各非終局局面に通常値0または1の子があることを証明し、mexと0・1交換の可換性から全称帰納法で導出。独立の直接再帰2383752安全局面で不一致0。
---

# 二禁止集合ゲームの通常・misère交換則

$\tau(0)=1,\tau(1)=0,\tau(k)=k$ ($k\ge2$) とする。包含極小禁止集合が高々二つなら、**すべての安全局面Sで $h(S)=\tau(g(S))$** が成立する。K0483により通常値gは3以下なので、misère値と全勝ち初手も既存の四領域残数の閉公式から得られる。

証明の要点は、各非終局局面に通常値0または1の子が存在するという補題。K0483の公式から場合分けで証明できる。子値集合Xが0または1を含めば $\operatorname{mex}(\tau(X))=\tau(\operatorname{mex}(X))$ なので、終局の(0,1)から帰納する。

n≤7の全10,795禁止集合対とn=8..12の固定乱数1,000組について、2,383,752安全局面を占有集合直接mexで独立検証した。抽象的な配置ゲームの全称定理であり、3個以上の極小禁止集合や任意の共円残局への無条件適用はしない。
