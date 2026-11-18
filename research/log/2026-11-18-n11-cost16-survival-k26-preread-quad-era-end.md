# 2026-11-18 N11 cost-16 parent 生存曲線: k=26予備構造確定 — quad打ち切り時代の終焉とquint項・A型4-way quad項の導入要件（pm値を使わない純構造解析）

本logはk=25出版（commit `9c41b23a`・27 checks all PASS・marginal 52.84% = m25の52.8%〔preread予測帯51〜53%の中域〕・B_survive初の5%割れ4.9103%）を受けて、**k=26拡張が計算コストを払う前に知っておべき機構変化**を、pinned aggregate（blob `31bdefdb…`）とclassify()のみ（pm値不要）で機械確定したものである。rank-26 root `(5,16)` は**行15でもハブ行18/19でもない初めての根**であり、ここまで12回維持された2つの構造不変量が同時に崩れる。

## 発見1: quad打ち切りの終焉（I-Eに第5項が入る）

- k=25まで: 全C(k,5)個の5-subsetが構造的ゼロ（機械確認: k24で42,504個・k25で53,130個）→ I-E は kill(k) = Σm − Σj2 + Σj3 − Σj4 で打ち切り可。
- **k=26: C(26,5)=65,780個のうち1,872個が非ゼロ（すべてb_only・9行union・二重行は行18が1,121/行15が379/行19が372）で、すべてrank-26 (5,16)を含む**。したがって k=26 では I-E に第5項が加わる: kill(26) = Σm − Σj2 + Σj3 − Σj4 **+ Σj5**。
- 1,872本は全てb_only（二重行ちょうど1つ・A型quintなし）なので、**j5_B = MyPm(mask = full ∖ union) のcountでb_only quadと同一パターンで計算できる見込み**（j5_A = 0）。ただしk14で3-way項を確立したときと同様、第二lineage（PmLazy等）による交叉検証を必須とする。1,872本のMyPm countはquad時代のb_only 371本/スライス比例から見積って約5〜15分。
- k=27では2,181個（rank-27 `(12,18)` 追加で+309個・すべてb_only）。

## 発見2: A型4-way項（disjoint quad）の初出現

- k=25まで: 新quadは常に b_only/zero のみ（**disjoint 0が全12回**）。I-E のA分割は kill_A(k) = Σa − Σj2_A + Σj3_A（j4_A == 0）で打ち切り可だった。
- **k=26: 新quad 2,300本のうち233本が disjoint**（4根8行すべて異なる）。これらはj4_A > 0 のA型4-way項となり、**kill_A(26) = Σa − Σj2_A + Σj3_A − Σj4_A が必要**になる。`disjoint_joint`（k14モジュール）は「pairs (|union|=4) AND triples (|union|=6) anchored on published pairs」と宣言されており、**|union|=8への拡張はk26計算前に検証（既存のdisjoint pair/triple錨での回帰テスト + 直接pm交叉検証）が必須**。
- 3行不変量の崩壊機構: k=25まで上位全根が行{15,18,19}の少なくとも1つを含み、5本を3箱に配分する全分割が「3x行または2つの2x行」を強制してきた（正本k24 logの3行鳩の巪引数）。`(5,16)` は行{5,16}でこの不変量を破る。(5,16) + 行{15,18,19}に1本ずつの3根 → 8行すべて相異 → disjoint quad。(5,16) + 4根（2,1,1配置）→ 二重行1つのみ → b_only quint。**233 disjoint quad・147 disjoint triple（これも過去最多）・23 disjoint pair（sharedはわずか2本・行16共有1本+行5共有1本・過去最多）はすべてこの機構で説明できる**。

## k=26の完全census（次レーンの変換assert直用・pm値不要で機械確定済み）

- **rank-26 root**: `(5,16)`（root `00000000000000801202000000101002`・行 [5,16]・m26 = 120,548,011,903,090,145）。
- **新pair 25本**: shared **2**（行16共有1本・行5共有1本）/ disjoint **23**（過去最多）。
- **新triple 300本** = C(25,2): b_only **134** / zero **19** / disjoint **147**（過去最多）。
- **新quad 2,300本** = C(25,3): b_only **1,194** / zero **873** / **disjoint 233（初出現・要A型拡張）**。
- 上位26本triple census C(26,3)=2,600 = b_only **1,594** / zero **542** / disjoint **464**（k25出版census 1,460/523/317 + 新134/19/147 と一致）。
- **quint census C(26,5)=65,780**: zero **63,908** / **b_only 1,872（要j5項）** / disjoint 0。
- complete数: pair C(26,2)=325・triple 2,600・quad C(26,4)=14,950（computed quads base = 9,911 + 2,300 = 12,211）。

## k=26変換時の作業項目（要約）

1. docstring/quints checkを「all_zero」から「census（zero 63,908 / b_only 1,872）」へ変更し、**j5計算mode（quints）を新設**（b_only 1,872本のMyPm count・第二lineage交叉検証込み）。
2. finalizeのI-Eに `+ Σj5`（kill・kill_B）と `− Σj4_A`（kill_A）を追加し、**27 checksの恒等式群を拡張**（split identity・単調性・marginal ∈ [0, m26]はそのまま、A分割のreproduceはk=25まで自動的にj4_A=0で一致するはず）。
3. `disjoint_joint`の|union|=8検証（disjoint pair/triple錨で回帰 + disjoint quad数本の直接pm交叉）を本番前に実施。
4. title自己修復: 正本k25 scriptのtitleは正しいk=25文言のためanchor問題なし（k24正本のstale title由来の取り忘れはk25で解消済み）。
5. marginal予測（法則の外挿・計算前の予告）: disjoint partner 23本（過去最多）でΣj2 ≈ 23×5.3e15 ≈ 122e15 > m26 = 120.5e15のため、**j3以降の寄与次第ではmarginalが過去最低水準（50e15割れ・場合によってはさらに低い）へ急落する可能性**。marginal ∈ [0, m26]チェックが初めて実質的な制約になる可能性がある点に注意。

## 解釈上の注意・11×11 状態

生存曲線はban回避の代替最小cover計画の組合せ数であって、探索コストでもverdictでもない。REFUTED-D10・STERILE は LOSS 証明ではない。標準11×11空盤は **UNKNOWN**。二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4 もすべて **UNKNOWN**。
