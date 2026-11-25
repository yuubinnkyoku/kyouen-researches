# 2026-11-18 N11 cost-12 parent（00000000000000003800000008002000）最小coverのmembership・joint・生存分析と一般frameworkの二重検証

## 成果

cover表で3番目に安い対象 parent `00000000000000003800000008002000`（23 open non-STERILE行・cost 12 exact・partial_sterile）について、**総最小cover数・全1,385 rootのmembership（A/B型内訳つき）・上位10 rootのjoint membership・上位k本ban生存曲線**を厳密に決定した。加えて、奇数rの2型（11 pair + 1 singleton のdisjoint型と 12 pair・1行二重被覆型）を統一的に扱う一般frameworkを構築し、**出版済みの11行・18行の両membership出力（全root・A/B内訳つき）を完全再現してから23行に適用した**。

- script: `research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/general_parent_cover_membership_20261118.py`
- output: `research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/cost12-parent-cover-membership-20261118.json`
- 50 checks all PASS（二重実行 byte-identical、実行約58秒、2^23全mask DPは約4.3秒）。

## 方法

各targetの全pm値（行部分集合の重み付き完全マッチング数）を2^r全mask bottom-up DP（奇奇偶skipつき・lowest-bit anchorで数値単調減少により昇順一括計算）で一括算出し、以降の全 formula は表参照のみで厳密。

- 偶数r（18行）: 最小coverはpair rootの完全マッチングのみ（s+p=k・s+2p≥r で s=0・重なり不可）。総数 = pm(V)、pair rootのmembership = pm(V∖{a,b})、singleton rootは0。
- 奇数r（11行・23行）: 2型が共存。
  - **A型**（k−1 pair + 1 singleton・全行disjoint）: A = Σ_s w1(s)·pm(V∖{s})
  - **B型**（k pair・ちょうど1行dが二重被覆・dを含む2 pair {d,a},{d,b} は a≠b・他はdisjoint）: B = Σ_d Σ_{a<b} w(d,a)·w(d,b)·pm(V∖{d,a,b})
  - pair rootのmembershipはA型・B型それぞれ閉形式（B型はeが二重被覆pairに入る場合と入らない場合の和）。singleton rootのmembership = pm(V∖s)（A型のみ）。
  - **恒等式 Σ(A型membership) == k·A と Σ(B型membership) == k·B** が両者独立に成立（機械検証）。
- joint membershipは奇数rで全ケース解析（行共有pair同士はB型の二重被覆pairとしてのみ共存可能→pm(V∖{d,a,b})、disjointはA+B-i+B-ii、singleton×pair、singleton×singleton=0）。

## 検証（出版値との二重再現）

1. **11行 class-2 top parent**: 総数 359,610（A 337,020 + B 22,590）・**全757 rootのmembership・singleton型/six-pair型内訳が出版membership出力（blob `ab1e655f`）と0不一致**。
2. **18行 cost-9 parent**: 総数 3,427,072,113,767・**全687 rootのmembershipが出版出力（blob `a1c5c8b6`）と0不一致**。
3. cover表（blob `4e4a911d`）のwitness 12本もmembership>0・全行被覆・span和=23で検証。

## 主要な新所見（cost-12 parent）

1. **総最小cover数 = 7,583,106,405,105（約7.58兆）**: A型 6,308,328,586,560（83.2%）+ **B型 1,274,777,818,545（16.8%）**。B型（1行二重被覆12-pair計画）が6分の1超を占め、無視できない計画タイプ。
2. **全1,385 root（234 pair + 1,151 singleton）がmembership > 0**（死んだrootなし）。最大 536,200,214,130（pair (0,22)・総数の7.07%）・最小 4,993,199,190（0.066%）。平坦さはcost-9（最大2.01%）と11行top parent（16.24%）の中間。
3. **行22がハブ**: 上位10 rootはすべてpair rootで、7本が行22を含む（残り3本は行1を含む）。上位15本中10本が行22関与。234 pair typeはすべてmultiplicity 1（cost-9の104 pair×4本と対照的）。
4. **上位10 rootのjoint membershipは45組み合わせすべて非ゼロ**（最大 31,151,018,745 = pair (4,22)×(1,14)）。**行を共有するpair同士（例 (0,22)×(4,22) = 472,743,810）も非ゼロ**で、これはB型cover（行22を二重被覆）でのみ可能。偶数r（cost-9）では行共有jointは厳密に0だったのと対照的で、**B型の存在がjoint構造に直接現れている**。
5. **生存曲線**: membership上位k本banで k=1→7.07% / k=4→25.2% / k=8→44.8% / **k=12→62.5%** kill。cost-9（k=12で23.6%・絞り込み不能）より集中度は高いが、11行top parent（k=8で90.5%・崖あり）ほどではない。協調的な候補絞り込みは行22関与pairから順に一定の効果がある。

## 解釈上の注意

membershipは代替最小cover計画への参加数であって探索コストでもverdictでもない。REFUTED-D10・STERILE は LOSS 証明ではない。本分析はcover計画の組合せ論のみを主張する。

## 11×11 状態

標準11×11空盤は **UNKNOWN**。二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4 もすべて UNKNOWN。
