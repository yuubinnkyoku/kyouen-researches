---
id: K0729
title: S2 {59,60} の61 blockerは未知S5子のD4 orbit集合が一致する35 certificateに崩壊し、greedy順序のsecured coverageは1,447 orbitで完結する
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
    単独実行でcertificate分解・ペア実現元・greedy曲線・1,447完結を再現。
    DO_S6=trueでmilestone-2のS6 census、DO_CROSS=nで横断worklistを再現
- path: research/log/2026-11-11-n11-s2-cert-collapse.md
  role: log
  note: 実行記録
- path: research/log/2026-11-12-n11-s2-5960-blocker-61-audit.md
  role: log
  note: '2026-11-12監査: blocker 61 / certificate 35（26ペア+9単独）への訂正。 greedy曲線・1,447完結・milestone全数値は不変'
---

# S2 {59,60} の証明書崩壊: 61 blocker → 35 certificate

二石root S2 = {60,59} のbest S3 r=61に対するblocker S4を、
「未知S5子（94位置universe外の合法五石子）のD4 orbit集合が完全一致する」で分類すると
**35 class**（26ペア + 9単独）に崩壊する（78 FW oracle条件付きの完全列挙）。
S2 {59,60} を閉じるのに必要なblocker証明書は35個で確定（61個ではない）。
{5,115}と{27,93}の恒等（K0725）はこの一般化。
（2026-11-12監査で61 blocker / 35 certificate に訂正。旧記録は60/34で
blocker 22を数えていなかった。22は非極大（22⊂88）のため全ての
orbit数・greedy曲線・milestone数値は変わらない。）

## 機構と限界（universeは非対称）

- 各ペア (a,b) はS3 {59,60,61} を集合として固定するStab(60)∩Stab(S3) ≅ V4
  （rot180・reflX・reflY）の元で結ばれる（全26ペアで実測確認）。
- ただし94位置oracle universe自体はD4閉包でない（rot180でさえ94位置中93が
  universe外に移る）。したがって幾何だけでなく「g対応子のuniverse所属が一致する」
  ことが各ペアで偶然成立しており、崩壊は自明な対称性の帰結ではなく条件付き観察である。
- 単独certificateは {15,22,23,26,31,71,73,82,104}。このうちx=5軸上（reflX固定）は
  71, 82, 104 のみで、15,22,23,26,31,73 は軸外（それらのV4像はblockerだがキーが異なる）。
  22, 15, 23, 26, 31 は非極大（それぞれ 88, 103, 89, 92, 89 のorbit部分集合）。

## greedy順序とsecured coverage（S5 orbit厳密値）

追加orbit最小の証明書順: {5,115}/+54 → {27,93}/+52（計106）→ {71}/+53（159）→
{82}/+52（211）→ {104}/+50（261）→ {73}/+85（346）→ {90,96}/+86（432）→
{23}/+84（516）。{31} と {89,97} は追加orbit 0で証明書8の時点で既にcovered
（worklist-covered blocker はこの時点で**14/61**・11クラス。
旧記録「12 blocker」は過少）。全blocker閉鎖には1,447 orbitすべてが必須で、
K0725のworklistと整合する。

## greedy ladder完全確定（2026-11-12追記・S5 orbit厳密値）

証明書8以降のgreedy継続を完走まで測定した
（research/log/2026-11-12-n11-s2-5960-greedy-ladder-complete.md）:
{79,85}/+80（596）→ {80,84}/+77 → {100,108}/+73 → {91,95}/+70 →
{52,74}/+67 → {111,119}/+63 → {26}/+60（1,006）→ {92,94}/+0 →
{53,75}/+56 → {102,106}/+52 → {113,117}/+48 → {70,72}/+45 →
{77,87}/+41 → {99,109}/+37 → {15}/+34 → {103,105}/+0 → {22}/+30 →
{88,98}/+0 → {54,76}/+26 → {78,86}/+22 → {81,83}/+18 → {101,107}/+14 →
{110,120}/+10 → {112,118}/+6 → **{114,116}/+2（1,447完結・61/61 blocker）**。
追加orbit曲線はほぼ単調減少（80→2）。covered blocker数は
14→16→18→…→61（step 33で完結）。各証明書のS6規模は未測定
（milestone-4以降のmanifest拡張の基礎データ）。

## milestone-2のS6規模（2系統一致）

greedy先頭5証明書（blocker 7個閉鎖）のS6 census:
累積S6 orbit union 2,191 → 4,262 → 6,517 → 8,780 → **10,988**
（41,842全体の26.3%）。第6–8位 {73}/{90,96}/{23} の単体S6 orbitは
3,868 / 4,232 / 4,416（相互union 11,794）。大きい証明書ほどS5 orbitあたりの
S6コストが高く、早期secured coverageは小証明書順が正しい。
（t=71/82/104の義務数9,684/10,156/10,348はK0748の再現と一致しない。
正しくは5,186/5,472/5,577。K0748のcertStatsを正とする。）

## classA 8 S2の横断worklist地図（root 60、best S3）

- {47,60}: 75 blocker / 5,276 orbit、{69,60}: 75 / 5,286、相互共有 4,649 → union 5,913
  （鏡映崩壊なし・75 certificate）
- {35,60} と {41,60}: 111 blocker / 5,981 / 5,981、共有 5,979 → union 5,983（ほぼ同一）
- {11,60}: 113 blocker / 6,206 orbit、{28,60}: 111 / 5,916
- {59,60}≡{60,61}: 61 blocker / 1,447 orbit / 35 certificate
- {59,60}との横断共有は僅少（q47と54、q69と46）で、先に閉じても他S2への縁故効果は小さい
- 注意: 他S2のblocker数も非極大blockerの取りこぼし可能性がある（2026-11-12監査で
  {59,60}に22が見つかったため）。orbit union・閉鎖要件への影響は非極大ならゼロの
  見込みだが、再監査を今後の課題とする。

本計算は78先手勝ちoracleの下の条件付き観察であり、いかなるS2・空盤の勝敗も含まない。
空盤・二石root {49,60} は UNKNOWN のままである。
