# 2026-11-18 N11 cost-18 36行parent 2本（cover表rank 6/7）の厳密total frontier測定

## 成果

cover表で6・7番目（同率cost 18）の36行 parent `00000000000000003802000000000020`・`00000000000000805082000000000000` について、**偶数r=36の最小cover意味論を確定し（全最小cover = 18本のpair rootによる完全マッチング）、pm(full) anchored木の状態空間を測定**した。**両parentとも8M状態capを超過**し、**36行parentの厳密totalは現行環境クラスの到達範囲外**であることを確定した（31行までは到達済み・今回のB16出版で完遂）。

- script: `research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/cost18_parent36_totals_20261118.py`
- output: 同dir `output/cost18-36row-parent-totals-20261118.json`
- 20 checks all PASS・三重実行byte-identical（sha256 `7a9c27f6…`）・cap 8M到達まで45秒/parent（約175K状態/秒）。

## 意味論（偶数r）

36行 = 偶数r では最小cover 18本は「18 pair root の完全マッチング」に限られる: (a) 二重被覆行があれば他の行が未被覆になる、(b) 17 pair + 1 singleton は35行しか被覆できない。よって **total = 加重完全マッチング計数 = pm(full)**。Tutte行列ランク法（GF(1000000007)/GF(998244353) の2素体・algebraic）で max matching = 18 を確認し、孤立行なし（pair degree min 51/54）を確認してから測定した。

## 主要数値（frontier測定）

1. **両parentの pm(full) anchored木は8,000,000状態を超過**（cap到達時 8,000,007 / 8,000,002 状態）。31行cost-16 parentの飽和memo（3,524,561状態）の**2.3倍以上**で到達した時点で打ち切り。真の木サイズは未確定（>8M）。
2. **12M cap試行はhostのOOM-killで中断**（tracebackなし・8M試行は完走）。本環境クラス（~2GB実効）での単一PmLazy木の実用上限は8〜12M状態。
3. **結論: 厳密totalのfrontierは31行**（cost-16 parentで完遂・A+B計2.97e18）。36行は slice設計でも first-move分解 (Σ_{b∈N(v)} w(v,b)·pm(V∖{v,b}) の34行木) が主体で、やはり8M超の見込み。36行以降は大きいホストか別の計算設計が必要。
4. **新規構造事実: mult-2 pair typeの初出現**。36行parent 2本は pair type 609/620 のうち 488/494 type が multiplicity 2（cost-16までの安価parentは全type mult 1）。pair degree 51-68/54-69（31行の27-30より高密度）で、これが状態空間膨張の主因と整合する。加重辺としての扱い（mult 2 = 2本のrootが同型被覆）は pm計算に正しく反映済み（edge_w = 型のroot本数）。

## 検証

- 構造照合: cover表（blob `4e4a911d`）と行数36・候補2,679/2,526・root 1,582/1,412・span histogram・cost 18 exact・下界18を全一致。
- Tutte 2素体一致・max matching 18・孤立行なし。
- 三重実行byte-identical（states_at_capは決定的な cap+過剰分で同一）。
- 8M cap試行は2回とも完走・45秒/parent、12M試行は2回ともOOM-kill（実験的事実として記録）。

## 解釈上の注意

本測定はcover計画の組合せ論とその計算可能性の測定のみを主張する。REFUTED-D10・STERILE は LOSS 証明ではない。

## 11×11 状態

標準11×11空盤は **UNKNOWN**。二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4 もすべて UNKNOWN。
