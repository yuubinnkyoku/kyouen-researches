# 2026-11-18 N11 minimum-cover root membership (head-1476 class-2 top parent)

## 成果

head-1476 class-2 top parent `00000000000000403800000008000000` の11行 cover 問題（最小6 root、359,610通り）について、**757個の候補rootそれぞれが何通りの最小coverに含まれるか**を組合せ的に厳密計算し、全root分を出版した。これは「359,610通りの最小coverから探索順を決める」ための基盤であり、membership上位root = 代替証明計画への寄与が最大のroot の直接の指標になる。

- script: `research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/count_minimum_cover_root_membership_20261118.py`
- output: `research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/minimum-cover-root-membership-20261118.json`
- 全32 checks pass。二重実行 byte-identical。

## 方法（組合せによる厳密計算、総当たり列挙なし）

det4候補rootの再列挙（出版censusのroot table 757本と cover_rows/occurrences 全一致を確認）の上で、

- singleton root（行iを1行cover、708本）のmembership = ways10[i]（他10行のpair重み付き完全マッチング数）
- pair root（{a,b}をcover、49本）のmembership g(a,b) =
  - Σ_{i∈R} singleton_i × pm(R\{i})（1 singleton + 5 pair型、R = 残り9行）
  - + dp2[R][5]（6-pair型・重複行が{a,b}の外: 残り5本のunionが厳密にR）
  - + pm(full\{b}) + pm(full\{a})（6-pair型・重複行がaまたはb: pは重複行をcoverする2本のうち1本で、残り5本はfull\{b}またはfull\{a}の完全マッチング）

検証は三重: (1) Σ memberships == 6 × 359,610 = 2,157,660、(2) 型別部分和 == 6×337,020 / 6×22,590、(3) 0/1 knapsack DPによる全最小cover再計数 == 359,610（本計数とは独立の経路）。なお初回実装で6-pair型の重複行ケース2項（pm(full\{a}) + pm(full\{b})）を落とし、恒等式が45,180 = 2×22,590だけ破れて検出された。これは恒等式検証が機能した実例でもある。

## 主要な新所見

1. **zero-membership rootは存在しない**。757 rootすべてが最小coverに最低1回現れる（最小membership 390）。候補rootの事前除外はこの基準ではできない。
2. **pair rootが支配的**。membership上位50本のうち49本がpair root（残る1本はsingleton）。全membership総発生の84.4%が上位50本に集中。
3. **最高membership root** `00000000200000003801000080000001`（pair）: 58,410 covers = **全最小coverの16.24%** に現れる。以降 51,990 / 51,150 / 51,090 / 51,075(2本) と続く。
4. **singleton rootのmembershipは行のみで決まる**（同一行のsingletonはすべて ways10[i] に等しい: 390〜735の6値）。lex-first cover のsingleton（行 `…0000000a`、membership 390）は全757本中rank 433と最弱クラスであり、**辞書順最小coverはmembership基準では大幅に非最適な計画**である。lex cover 6 rootのmembership合計は205,659（cover平均換算 9.5%シェア）。
5. 行毎のways10: `…0200000` 行が最大735、`…0400000`行が555、`…0200/…1000`行が630、5行が390。membershipの観点では 390行をsingletonで埋め、高membership pair rootを重用する計画が代替計画の多様性を最大化する。

## 使い方（次ステップへの接続）

- 証明計画の優先順位: 代替計画数を最大化したい局面（rootの REFUTED/PROVED 判定が他計画に流用可能な場合）は membership上位のpair rootから先に判定すると、1件の判定で平均的に最多の代替coverが確定する。
- 逆に「失敗時の代替可能性を狭めたくない」探索では、membershipの低いroot（singletonの390行）から処理しても計画多様性への寄与は小さい。

## Interpretation guard

本計算は bookkeeping・組合せ計数のみで、engine実行・verdict・fold・閉包主張は一切含まない。membershipは探索コストではなく代替計画への寄与の計数であり、WIN/REFUTED の何らの示唆もしない。REFUTED-D10・STERILE は LOSS 証明ではない。

## 11×11 状態

標準11×11空盤は **UNKNOWN**。二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4 もすべて UNKNOWN。
