---
id: K0581
title: 平面q点禁止ゲームのN=2q−1・q≥6では担い手が高々二本で全安全局面に閉公式がある
kind: proposition
status: proved
topics: [geometry, variants, grundy, residual-games, first-moves, maximal-safe]
aliases: []
relations:
- type: depends_on
  target: K0483
  note: 二つのq点禁止組の通常Grundy閉公式
- type: depends_on
  target: K0579
  note: 二禁止組のmisère交換則
artifacts:
- path: research/experiments/short-board-2qminus1-20261031/proof.md
  role: proof
  note: 担い手分類、整数格子実現、型IIIの全安全局面mex閉公式と交換則の全称証明
- path: research/experiments/short-board-2qminus1-20261031/verify.py
  role: verifier
  note: q≤50残数再帰、q≤8整数幾何・全安全部分集合直接mex、二禁止組と小格子全盤検査
scope: q≥6、N=2q−1個の相異なる実平面点、共円または共線q点禁止、通常・misère二人ゲーム、全安全局面
evidence: 異なる担い手の交点数≤2から二担い手三型に帰着。型IIIは残容量のmex帰納法で閉公式を証明。整数有理円構成と独立列挙で検証。
---

# N=2q−1の全安全局面強解決（q≥6）

禁止q点組数は正確に

$$
f\in\{0,2,q+2\}\cup\left\{\binom mq:q\le m\le2q-1\right\}.
$$

全候補は整数格子上で実現可能。担い手（q点以上含む直線・円）は高々二本。二本なら (q,q,共有1点,外部0点)、(q,q,共有2点,外部1点)、(q+1,q,共有2点,外部0点) の三型のみ。

担い手なし・一本なら全終局長が固定し、通常・misère値は残手数の偶奇。二本がともにq点ならK0483/K0579で全局面を閉形式で解ける。二本のサイズがq+1とqの場合も、共通部占有数cと両担い手の残容量U,Vによる七行の閉公式が成立し、全安全局面で h=τ(g)（τは0と1を交換）が成立する。数学的証明と全場合分けはproof.mdを参照。

型IIIでは極大安全集合の石数は \(2q-3\) と \(2q-4\) だけで、個数はそれぞれ \(2q-1\) と \(\binom{q-1}{2}(q-2)\)。完了した合法着手履歴の総数は \((2q-1)(2q-3)!+\binom{q-1}{2}(q-2)(2q-4)!\)。これらも全称的な組合せ論的証明がある。

空盤の (g,h) は、担い手なし (1,0)、一本でm点なら ((3q−2−m) mod2, 1−((3q−2−m) mod2))、二本ともq点 (1,0)、q+1点とq点 (0,1)。

独立検証は整数幾何による禁止組の直接判定、全安全部分集合mex、残数再帰、二つの小格子の全盤列挙で実施。**全称性は数学的証明に依拠**し、q=4,5や既存大盤の任意の残局には無条件適用しない。
