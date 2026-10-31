---
id: K0588
title: 任意交差・異容量の二制約ゲームでは極大配置多項式が閉形式を持ち終局長は常に連続する
kind: proposition
status: proved
topics: [maximal-safe, maximum-safe, residual-games, strategy-length, variants]
aliases: []
relations:
- type: generalizes
  target: K0587
  note: 共通点数0〜2・同じ容量q−1から任意の共通点数と異なる二容量へ拡張
artifacts:
- path: research/experiments/two-quota-terminal-spectrum-20261031/proof.md
  role: proof
  note: 三つの排反飽和型による全称母関数と連続終局長の証明
- path: research/experiments/two-quota-terminal-spectrum-20261031/verify.py
  role: verifier
  note: 6372構成5275338部分集合の独立追加判定と20000標本の検算
scope: 任意有限集合上の二つの非冗長容量制約 |S∩A|≤p、|S∩B|≤r、交差数任意、容量は異なってよい。全極大配置と終局長。
evidence: 極大集合の飽和状態を排反分類した数学的全称証明。6372有限構成の点別完全列挙で独立照合。
---

# 任意交差の二容量ゲーム：終局長に欠番はない

A固有点数X、B固有点数Y、共有点数C、自由点数Zとし、非冗長容量0≤p<X+C、0≤r<Y+Cを課す。

両方の容量が飽和する極大集合では共有点をt個選ぶと、極大石数はp+r−t+Z、配置数は \(\binom Ct\binom X{p-t}\binom Y{r-t}\)。片方だけ飽和する場合の補正項も含む**全極大配置母関数**を proof.md に与えた。

L=max(0,p−X,r−Y)、U=min(C,p,r) とすると、**L≤U の場合の終局長はちょうど p+r−U+Z から p+r−L+Z の全整数**である。L>U なら終局長は1種類のみ。従って最小極大石数sと最大安全石数Kの間に欠番はなく、K−s≤C。共有点数Cに制限はなく、容量p,rは異なってよい。

X=Y=C=p=r=3、Z=0では終局長3,4,5,6がすべて実現し、幅Cを達成する。数学的証明に加え、6372構成・5275338部分集合の独立点別判定で不一致0。有限実験から全称性を推測したのではない。

**適用境界**：K0587の平面二担い手モデルを一般化し、途中局面で二つの残容量が異なる場合も扱う。残りの禁止条件が正確にこの二制約だけである必要があり、三本目の禁止条件がある残局や任意の11×11局面には無条件に適用しない。通常・misèreの最適戦略やGrundy値は本定理の対象外。