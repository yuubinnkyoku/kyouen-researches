---
id: K0724
title: best-S3壁のclassA分解: classA blockerは32個・8 S2のみで、すべて16第二手勝ち五石子由来（SW16部分集合）
kind: computation
status: computed
topics: [square-outcomes, certificates, verification]
aliases: []
relations:
- type: depends_on
  target: K0685
  note: 13,244 blockerのうちuniverseに触れるclassAの完全列挙
- type: depends_on
  target: K0675
  note: 78先手勝ち/16第二手勝ち五石位置oracle
artifacts:
- path: research/experiments/n11-classa-decompose-20261110/scripts/blockers_classA_decompose.ts
  role: source
  note: 純TS再現（W4=FW78部分集合の単純化、BigInt盤、Bareiss幾何）
- path: research/log/2026-11-10-n11-classa-decompose.md
  role: log
  note: 実行記録
---

# classA壁分解: 既知universeに触れるblockerは32個に完全列挙される

K0685のbest-S3 blocker計13,244件（120 S2）のうち、S5子が既知94位置universeに
触れる classA blocker は **ちょうど32件** で、出現する S2 は
q ∈ {11, 28, 35, 41, 47, 59, 61, 69} の8個のみである（per-S2粒度の完全分解）。

定義論理（T1）: blocker S4 は先手勝ち五石子を持たない。ゆえに blocker の
universe 内 S5 子はすべて第二手勝ち位置（SW16）である。数値検証:
SW16石を含む全18候補 S2 の best-S3 で classA と SW16のみによる再計算が全件一致。

classA blockA t の完全リスト:
- q=59/61（best r=61/59、blocker各60）: t ∈ {5,15,23,26,27,31}（6件、鏡映対）
- q=47（r=59、75）: t ∈ {5,23,28,67}
- q=69（r=59、75）: t ∈ {5,11,15,16,22,23,26,27,31,33,35,41}（12件、SW-A v全体）
- q=11/35/41（r=59、blocker 113/111/111）: t = 69（各1件）
- q=28（r=61、111）: t = 47

classA=0の機構は3種:
(i) q がuniverseに出現しない（62 S2。universe石は121位置中59個）
(ii) q を含むuniverse位置がすべて先手勝ち（50 S2。代表 q=51: 51を含む6位置
  {51,59,60,61,x} はすべてFIRST_WINで、それらを子に持つS4は自動的にW4となる）
(iii) SW16石を含む q でも best S3 がどのuniverse位置にも含まれない
  （q ∈ {5,15,16,22,23,26,27,31,33,67} の10個）

補足: SW16はすべて {59,60,61} を含み、12個が S4-A型 {59,60,61,69,v}、4個が
S4-B型 {47,59,60,61,v} である。

証明系への意味: 既知oracleがblockerに発話できるのはこの32個の(S2,S3,t)のみ。
残り13,212件（99.76%）は既知universeに触れず、新S5 verdict以外の情報源がない。
32個のS4はS6/S7監査・既存WIN6証明照合の最優先候補。

本計算は78先手勝ちoracle（K0675）の下の条件付き観察であり、いかなるS2・空盤の
勝敗も含まない。空盤・二石root {49,60} は UNKNOWN のままである。
