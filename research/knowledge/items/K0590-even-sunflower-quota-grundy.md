---
id: K0590
title: 偶数本のひまわり型容量制約ゲームの通常・misère全安全局面を残容量の最小値と偶奇だけで強解決
kind: proposition
status: proved
topics: [grundy, residual-games, variants, strategy-length]
aliases: []
relations:
- type: depends_on
  target: K0002
  note: 通常Grundy値とmisère補助mexの定義
artifacts:
- path: research/experiments/even-sunflower-grundy-20261101/proof.md
  role: proof
  note: 全局面の閉形式と8分類16行のmex恒等式による無界の全称証明
- path: research/experiments/even-sunflower-grundy-20261101/verify.py
  role: verifier
  note: 偶数r=2,4,6,8の139515圧縮局面、54盤7551点別局面を独立照合
scope: r>=2が偶数、共通芯Hと互いに素な花弁P_i、自由点Z、各|P_i|>=p_i>=1の有限抽象容量ゲーム。通常・misèreの全安全局面。
evidence: 8分類16行のmex恒等式と残着手数帰納法による全称証明。139515圧縮局面・7551点別局面の独立有限検証。
---

# 偶数本のひまわり型容量制約ゲームの完全なGrundy閉形式

c を未着手芯点数、b_i を各制約の残容量、f を自由点の残数、m=min_i b_i、p=(f+Σ_i b_i) mod 2 とする。

| 条件 | 通常 g | misère補助 h |
|---|---:|---:|
| c=0 または m=0 | p | 1-p |
| c>=m>=1, m 奇数 | 2+p | 2+p |
| c>=m>=2, m 偶数 | p | p |
| 0<c<m, c 奇数 | 1-p | p |
| 0<c<m, c 偶数, m=c+1 | p | 2+p |
| 0<c<m, c 偶数, m>=c+2 | p | 1-p |

**任意の偶数本、任意の盤面サイズ・残容量について g,h<=3**。奇数本はK0589の偶奇式で解決済みなので、これで全 r>=2 のひまわり型容量ゲームの通常・misère版が全局面強解決された。最適手は合法な子の閉形式を評価して求められる。

花弁点数が容量以上なので、残容量が正の花弁には必ず合法手がある。最小容量の花弁への着手、他の花弁・自由点への着手、芯への着手の3遷移だけが値に影響する。後者は偶数本の制約を一斉に1減らすため偶奇 p が変わらない。8種類の (c,m) の排反な場合分けと16行のmex恒等式により、残着手数の帰納法で無界に証明できる。証明表はartifact参照。

例：r=4,c=2,b_i=3,f=0 では (g,h)=(0,2) で、misère値は単純な0/1交換ではない。

**限界**：抽象容量ゲームの定理。任意の平面共円ゲームにそのまま適用できず、残局の残余禁止条件が正確にこのひまわり型であることが必要。11×11の空盤勝敗は未解決。有限検証は全称証明の代替ではない。
