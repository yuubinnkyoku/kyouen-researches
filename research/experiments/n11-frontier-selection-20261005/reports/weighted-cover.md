# Othello型のcache-aware proof frontierを11×11へ適用

Date: 2026-10-05

**11×11空盤勝敗はUNKNOWNのまま。**

## 問い

中心初手60・隅応手0の二石rootでは、119個の第三手をs4 classで覆う最小class数は31と既に証明されている。
しかし31個の選び方は一意でなく、各classをLOSSと確定するために必要なs5 exact root数も大きく異なり得る。

Othelloの弱解決で「全中間局面ではなく、根の証明に必要な境界局面だけを抽出して解く」方式が有効だったことに対応し、
ここでは**class数31を固定したまま、既知cacheを最大限再利用して新規s5 root数を減らせるか**を調べた。

## 方法

既存の独立Python幾何実装から、root `{60,0}` について全s4を再列挙する。

- safe raw s4 edges: **6,894**
- D4 canonical s4 classes: **3,396**
- coverage histogram: cov2=51, cov3=437, cov4=2,832, cov5=33, cov6=43

各classについて、その全raw edgeから合法な第五手を列挙し、D4 canonical s5 key集合を作る。
全3396classを通じたclass-child incidenceは372,769、異なるcanonical s5 rootは122,953。

公平な基準として、既に厳密LOSSが検証されているclass orbit `{0,1,2,60}` の全s5 child **103件**だけを既知cacheとした。
このclassは選択を強制する。

次の0-1 MILPを解いた。

- 119頂点を全てcover
- 選択class数を**ちょうど31**
- 既知LOSS classを必須
- 目的関数は各classの「103件の既知cacheに無いs5 child数」の和

これはunique childの厳密最小化ではなく、重複を二重計上する加法的proxyである。
最終選択については別にunique child数を直接数える。

比較対象は、既存の整数dual/matching証明が生成する31-class witness。

## 結果

加法的proxyのMILPは最適性gap 0で閉じた。

| 31-class skeleton | unique s5 roots | 既知103件を除くunique新規s5 roots |
|---|---:|---:|
| 既存の定理witness | 3,336 | **3,233** |
| cache-aware weighted cover | 2,938 | **2,835** |

同じ31 class、同じ119/119 coverageのまま、**3,233 → 2,835、398件減、12.31%減**となった。

既存witnessでは選択class間の新規s5 root重複はほぼ無く、unique 3,233に対して加法和との差は3件だけだった。
weighted coverは重複も積極的に利用し、unique新規2,835まで落ちた。

## 追加の保守的確認

現在repoで独立検証済みの情報から再構成できる範囲として、2個のLOSS classの103+106 child（overlap 0）を既知、検証済みWIN classを禁止として使った。
両LOSS classを強制し、WIN classを禁止した31-class weighted coverでは、加法的未解決cost **2,982**、selected unique s5 roots 3,021、known 209を除くunique新規 **2,812** となった。

class数を31..36で固定して同じ加法的目的を解くと、costは31:2982, 32:2991, 33:3000, 34:3011, 35:3023, 36:3035で、このproxyでは31を超えてclass数を増やす利益は見えなかった。

## 解釈

これは**12.31%の実時間高速化**を意味しない。
減ったのは「選択したcertificate skeletonを全部LOSS化するときに新たに解く必要がある異なるcanonical s5 root数」である。
各s5 rootの難易度は大きくばらつくため、次は件数ではなく予測/実測node costを重みにする必要がある。

それでも、現在のcoordinatorが最終certificateに必要なfrontier全体のs5仕事量を直接最小化する価値は有限実験で確認できた。
known LOSSはcost 0、known WINは候補から除外、UNKNOWNは新規s5 child集合または推定node costで重み付けし、新しいverdictが得られるたびに31-class coverを解き直すのが自然である。

これは空盤勝敗の証明ではなく、現在の二石root refutation certificateを安く作るための探索方針である。

## 再現

    uv run --locked python research/experiments/n11-frontier-selection-20261005/scripts/weighted_cover.py

出力は `research/experiments/n11-frontier-selection-20261005/output/weighted-cover.json` へ保存される。
