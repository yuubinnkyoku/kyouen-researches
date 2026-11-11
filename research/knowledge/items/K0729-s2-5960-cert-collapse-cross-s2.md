---
id: K0729
title: S2 {59,60} の60 blockerは未知S5子のD4 orbit集合が一致する34 certificateに崩壊し、greedy順序のsecured coverageは1,447 orbitで完結する
kind: computation
status: computed
topics: [square-outcomes, certificates, verification]
aliases: []
relations:
- type: depends_on
  target: K0725
  note: 閉鎖worklist 1,447 orbitの直接の子列挙による証明書分解
- type: depends_on
  target: K0685
  note: best-S3 blocker監査・blocker選定規則
- type: depends_on
  target: K0675
  note: 78先手勝ち/16第二手勝ち五石位置oracle（94位置universe）
artifacts:
- path: research/experiments/n11-s2-cert-collapse-20261111/scripts/cert_collapse.ts
  role: source
  note: 純TS再現（BigInt盤、Bareiss幾何、D4 canon、universe閉包監査込み）。
    単独実行で34 certificate・ペア実現元・greedy曲線・1,447完結を再現。
    DO_S6=trueでmilestone-2のS6 census、DO_CROSS=nで横断worklistを再現
- path: research/log/2026-11-11-n11-s2-cert-collapse.md
  role: log
  note: 実行記録
---

# S2 {59,60} の証明書崩壊: 60 blocker → 34 certificate

二石root S2 = {60,59} のbest S3 r=61に対する60 blocker S4を、
「未知S5子（94位置universe外の合法五石子）のD4 orbit集合が完全一致する」で分類すると
**ちょうど34 class**（26ペア + 8単独）に崩壊する（78 FW oracle条件付きの完全列挙）。
S2 {59,60} を閉じるのに必要なblocker証明書は34個で確定（60個ではない）。
{5,115}と{27,93}の恒等（K0725）はこの一般化。

## 機構と限界（universeは非対称）

- 各ペア (a,b) はS3 {59,60,61} を集合として固定するStab(60)∩Stab(S3) ≅ V4
  （rot180・reflX・reflY）の元で結ばれる（全26ペアで実測確認）。
- ただし94位置oracle universe自体はD4閉包でない（rot180でさえ94位置中93が
  universe外に移る）。したがって幾何だけでなく「g対応子のuniverse所属が一致する」
  ことが各ペアで偶然成立しており、崩壊は自明な対称性の帰結ではなく条件付き観察である。
- 単独certificateは {15,23,26,31,71,73,82,104}。このうちx=5軸上（reflX固定）は
  71, 82, 104 のみで、15,23,26,31,73 は軸外（それらのV4像はblockerだがキーが異なる）。

## greedy順序とsecured coverage（S5 orbit厳密値）

追加orbit最小の証明書順: {5,115}/+54 → {27,93}/+52（計106）→ {71}/+53（159）→
{82}/+52（211）→ {104}/+50（261）→ {73}/+85（346）→ {90,96}/+86（432）→
{23}/+84（516）→ {31}/+0 → {89,97}/+0 → … → 最終 {114,116}/+2（1,447完結）。
{31} と {89,97} は既存カバーの部分集合（追加orbit 0）。全60 blocker閉鎖には
1,447 orbitすべてが必須で、K0725のworklistと整合する。

## milestone-2のS6規模（2系統一致）

greedy先頭5証明書（blocker 7個閉鎖）のS6 census:
t=71: 義務9,684 / S6 orbit 2,421、t=82: 10,156 / 2,516、t=104: 10,348 / 2,563。
累積S6 orbit union 2,191 → 4,262 → 6,517 → 8,780 → **10,988**
（41,842全体の26.3%）。第6–8位 {73}/{90,96}/{23} の単体S6 orbitは
3,868 / 4,232 / 4,416（相互union 11,794）。大きい証明書ほどS5 orbitあたりの
S6コストが高く、早期secured coverageは小証明書順が正しい。

## classA 8 S2の横断worklist地図（root 60、best S3）

- {47,60}: 75 blocker / 5,276 orbit、{69,60}: 75 / 5,286、相互共有 4,649 → union 5,913
  （鏡映崩壊なし・75 certificate）
- {35,60} と {41,60}: 111 blocker / 5,981 / 5,981、共有 5,979 → union 5,983（ほぼ同一）
- {11,60}: 113 blocker / 6,206 orbit、{28,60}: 111 / 5,916
- {59,60}≡{60,61}: 60 blocker / 1,447 orbit / 34 certificate
- {59,60}との横断共有は僅少（q47と54、q69と46）で、先に閉じても他S2への縁故効果は小さい

本計算は78先手勝ちoracleの下の条件付き観察であり、いかなるS2・空盤の勝敗も含まない。
空盤・二石root {49,60} は UNKNOWN のままである。
