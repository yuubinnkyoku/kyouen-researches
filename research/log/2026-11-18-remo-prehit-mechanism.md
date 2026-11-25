# 2026-11-18 remo-prehit-mechanism（K0956）作業ログ

目的: K0950のHIT-ARITHとK0952の枝分解の間のpre-tailヒット機構を全称定理化し、
K0954のfrom-start BHモデルの欠陥を修正してM≤2000までの決定的監査で確定する。

## 発見順

1. **smoke test失敗（仕様の勘違い）**: 最初のengine照合で不一致多数。原因は
   σ_Z(M,K)が生存者位置（0..K−1）を返す仕様で、ヒット判定はσ_Z==1（位置1番）を
   使う必要があった。判定側を直して生窓述語と一致。
2. **HIT-GAPの発見**: 生窓述語（[M,k₀]内約数なし）をD*(N)<Mに置き換えられることに
   気づく。核心は N−(M+1)k₀=2M−κ>0。t非依存のこの不等式が⟸方向の矛盾を閉じる。
   レジーム k₀≥√N の全域判定はf(κ)=k₀²−Nのκ単調性（f(0)=M²t(t−1)−3Mt−M+2）で
   M≥4,t≥2全域ほか場合分け完了。(3,2,0)のみM=3,t=2での例外で、ここでもHIT-GAP自体は成立。
3. **SPLITの証明**: 最初の試み（B₁=uvのv>√N分析）はv≥√B₁≥√Nという誤りを含み、
   smooth実例M=61,κ=6,t=8（N=2·23²·29・B₁=529=23²・v=23<√N）で破綻したことに
   気づいて再構成。正しい骨子: (a) B₁>N/D*は窓により>k₀、(b) k₀超の約数の余因子は
   N/k₀<M+1とM∤Nで≤M−1、(c) C≤M+1<大因子（素数）ならgcd論法でC|余因子→branch、
   (d) 第3因子が√N以下に落ちたら3因子とも≤M−1でsmooth・N≤(M−1)³、
   (e) 再帰は大因子が半減して終止。排他性はN>(M−1)²とbranchのP=N/d>k₀から両立不可。
4. **SEAM**: smooth側のt上限 (M−1)(M−2)/(M+1)<M−3（M≥7）。K0952のseam
   max(M,3)を改良。M=3とM=2はsmooth不在でPAIR-2/3と整合。
5. **GAP-GRID/SPLIT-GRID実装と実行**: engine錨をK≤7440へ拡大（30,502状態・3-way
   不一致0）。SPLIT-GRID（M≤199・t∈[2,M−2]）24,763ヒット・違反0・nonliveヒット0。
   smooth-only 29状態を全記録。
6. **修正BH（binningバグの発見と修正）**: K0954のt_hatはpair_integralがn=0近傍で
   発散（κ=0,e=1枝はc1=1）しSimpson格子依存で非単調になることを再現して特定。
   定義域を枝ごとに修正（n_min(e)=2/1/0・整数nはbin[n,n+1)積分）し、単調・有限化。
   FIRSTHIT-PRED: pooled Spearman 0.0758→0.1614、t_first≥2の1,014クラスで
   median Λ*(t_first)=0.755≈ln2（Poisson競争較正）。
7. **FIRSTHIT M≤2000**: 103,185 liveクラスがt_cap=7ln²(M+1)+100内で全ヒット。
   F-fitのM≤199点はK0950出版1.767·M^1.509と完全一致、M≤2000では2.977·M^1.386、
   M∈[200,2000]は指数1.280に平坦化。初回ヒット型はbranch 93.8%・smooth 6.1%。
8. **T1-CHANNEL**: t=1ヒット532件はY(1)素数クラス（liveの72%）から発生、209は窓阻止。

## 機械結果の要約

- GAP-GRID-A/B: 30,502状態・3-way不一致0（engine錨K≤7440）。
- SPLIT-GRID: 24,763ヒット（24,734 branch/29 smooth）・SPLIT/SEAM違反0・nonlive 0。
- T1-CHANNEL: 532ヒット（435 branch/97 smooth）・209窓阻止。
- FIRSTHIT: n_nohit=0・tier3/firsthit_pred 0不一致・Fは全Mでbranch型。
- FIRSTHIT-PRED: Spearman 0.1614（within-M 0.0087・順序はノイズ支配を維持）。
- RATE-PROFILE: BH比 M=23: 0.88-1.01・M=199: 1.2-1.35。
- SMOOTH-LAW: 29状態の全記録・最大N=428446（M=199）≪198³・max t=10≪上限195。
- 監査は決定的（2回cold実行でout/とout2/がbyte同一）。

## 次課題

- F(M)の遠域平坦化の機構（1.509→1.386→1.280）: tier3完全データでのFの再フィットと
  F/(M ln²M)の漸近形。P-KILL-TIGHT掃引のK上限拡大とt_cap予測子の全称化。
- smooth-onlyヒットの集中構造（t≪解析上限）の説明: smooth状態の(M,κ,t)分布則。
- within-M順序を支配する変数の探索（C・κの別統計量・Λ*の条件付き分布）。
- 11×11レーンへの接続: HIT-GAP/SPLITの枝刈り（D*<M判定は窓約数判定より
  因子分解1回で済む）がn11の残余ゲーム計算に使えるか別レーンで評価。
