# 2026-11-18 N11 cost-9 parent（00000000000000821082000000000000）最小coverのmembership・elimination・joint分析

## 成果

表で2番目に安いcover対象 parent `00000000000000821082000000000000`（18 open non-STERILE行・cost 9 exact・method perfect_matching）について、**全最小coverの総数・全687 rootのmembership・上位root除外の生存曲線・上位10 rootのjoint membership**を厳密に決定した。

- script: `research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/cost9_parent_membership_20261118.py`
- output: `research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/cost9-parent-membership-and-elimination-20261118.json`
- 24 checks all PASS（二重実行 byte-identical、実行約1.5秒）。
- 入力は出版済みpin 4件（worklist `2fee1d07`・census `9c251da3`・ledger `e8785d50`・cover表 `4e4a911d`）+ 出版済みphase-1 script（`enumerate_global_candidate_roots_20261118.py`）で再生成される候補JSONL。行数・候補数・distinct roots・span histogramがcover表の当該エントリと完全一致することを機械検証。

## 方法

maxspan=2・r=18偶数より、サイズ9の最小coverはすべてpair root 9本による**完全マッチング**（s+p=9・s+2p≧18 → s=0）。よって重み付き（重み = 同一row pairを被覆するroot本数）完全マッチングDP over 2^18で全量が厳密に計算できる。

- 総cover数 = pm(V)。membership(pair root on {a,b}) = pm(V∖{a,b})（そのrootを固定した残り16行のマッチング数）。singleton-span root（136本）のmembershipは0（機械検証）。
- root除外 = 当該pairの重みを1減らしてDP再計算 → 生存曲線が厳密に得られる。
- 行を共有する2 pairは9-root完全マッチングに共存不可能（18スロットで1 pair二重被覆 → 残7 rootで16行を被覆不能）→ joint membershipは厳密に0。
- 検証: Σmembership == 9×総cover数（恒等式）、pm(V)のlow-anchor/high-anchor独立DP一致、cover表witness 9本が全てmembership>0・互いに素・全行被覆、survival単調性。

## 主要な新所見

1. **総最小cover数 = 3,427,072,113,767（約3.4兆）**。class-2 top parentの359,610（cost 6・11行）と比較して約10^7倍。19行→18行でもpair密度（152 pair types・551 pair root・multiplicityは104 pairが4本・40 pairが3本・7 pairが2本・1 pairが1本）が cover 空間を爆発させている。
2. **membershipは極端に平坦**: 非ゼロmembershipの最小 46,475,193,794 / 最大 69,007,368,368（最大でも総数の2.01%）。**551本のpair root全てが数十億の最小coverに参加し、死んだpair rootは1本もない**（136本のsingleton-span rootのみmembership 0）。
3. **上位root除外ではcover空間を潰せない**: membership上位k本banで k=4→8.05%、k=8→15.93%、k=12→23.59% kill。約2%/本の直線的に近い減衰で、50% killには約25本以上が必要。class-2 top parent（上位8本で90.5% kill・rank 8→9に崖）と対照的で、**このparentではmembershipに基づくroot優先順位付け・候補絞り込みは機能しない**。
4. **上位rootは行ハブ {6,8,10,11} に集中**: membership上位12本はわずか4 pair（行8-10・行8-11・行6-8・行6-11）にあり、上位10本は (8,10)×4本・(8,11)×3本・(6,8)×3本の3 pairに集中。この3 pairは互いに行を共有するため**上位10 rootの45組み合わせのjoint membershipは全て厳密に0**（どの最小coverも上位rootの2本を同時に使わない、either-or構造）。
5. この結果は前回のjoint分析（このparentはcross-parent root 0本で完全孤立）と合わせると、**cost-9 parentは単独で551本規模の平らなroot候補空間を持つ、絞り込み不能な対象**であることを意味する。証明書計画（coordinator選定）では、このparent向けの候補削減はmembershipでは達成できず、verdict探索側の結果（sweep-lane管轄）に頼るほかない。

## 解釈上の注意

membershipは代替9-root計画への参加数であって探索コストでもverdictでもない。REFUTED-D10・STERILE は LOSS 証明ではない。本分析はcover計画の組合せ論のみを主張する。

## 11×11 状態

標準11×11空盤は **UNKNOWN**。二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4 もすべて UNKNOWN。
