# 2026-11-18 N11 minimum-cover elimination structure (head-1476 class-2 top parent)

## 成果

前 commits で出版した membership 計数（`minimum-cover-root-membership-20261118.json`）を土台に、**root除外に対する359,610通りの最小coverの生存構造**を厳密計算して出版した。証明計画の優先順位づけにおいて「rootが1本使えなくなったときに代替計画がいくつ残るか」への直接的な回答。

- script: `research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/analyze_minimum_cover_elimination_structure_20261118.py`
- output: `research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/minimum-cover-elimination-structure-20261118.json`
- 全24 checks pass。二重実行 byte-identical。実行時間約7秒。

## 方法

0/1 knapsack count DP（11行mask、2048状態）を非除外rootに制限して生存cover数を数え、強制込み込み版（init_mask/init_k）で上位root間のjoint membership（両方を含むcover数）を計数。skip-if-no-new が正当なのは、size-6 coverの各rootはessential（5-coverが存在しないため）であることによる。単一除外のkill数が出版membership値と一致すること（k=1）、強制込み込みtop-1がmembership再現することで桁あわせ済み。

## 主要な新所見

1. **生存曲線（membership順で上位k本を除外）**: k=1: 58,410 kill（16.2%）、k=4: 50.7%、k=8: **90.5%**（残34,125）、k=12: 95.9%（残14,625）。上位pair rootの判定が計画空間の大半を握る。
2. **rank 8→9 に構造的な崖**: 限界killは k=8 まで 35,000台で推移し、rank 9（membership 45,030）の限界killはわずか4,875。つまりrank 9 rootのcoverの約91%は既に上位8本のいずれかを含む。上位8本は互いに「別々の計画」を代表しており、rank 9以降はその代替部品という構造。
3. **lex計画の頑健性は低い**: 出版済み辞書順最小coverの6根すべてを除外しても201,360通り（56.0%）が生存。lex計画の除外価値は44.0%で、membership上位6本の除外価値60.7%を大きく下回る。探索順を決めるうえで辞書順はmembership基準に劣る。
4. **top-10 間のjoint membership**: 最大7,605（`…c29002000000001000` と `…41801202000000080000`）。上位root同士の共起は10〜15%程度で、membershipの加減での単純推定より少ない。k=2の限界kill 44,400 = 51,990 − 7,590 がjoint表と桁あわせする。

## 解釈上の注意

「除外」は当該rootが証明計画に使えなくなった状況のモデル。計数は最小サイズ（6根）計画のみを対象とし、非最小計画の存在には何も言わない。WIN/REFUTED の示唆を含まない。REFUTED-D10・STERILE は LOSS 証明ではない。

## 11×11 状態

標準11×11空盤は **UNKNOWN**。二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4 もすべて UNKNOWN。
