# 2026-11-18 N11 runner-up parent（00000000000000003800000009000000・29行）最小coverのmembership・joint厳密解析（共有memo lazy matching DP）

## 成果

cover表で2番目に安い対象 parent `00000000000000003800000009000000`（29 open non-STERILE行・cost 15 exact・class-2 ranking 2位）について、**総最小cover数・全1,854 rootのmembership（A/B型内訳つき）・上位10 rootのjoint membership**を厳密に決定した。2^29全mask DPがこの環境（RAM 3.2 GB）に載らないため、**共有memoつきanchored lazy matching DP（PmLazy）**を新規実装し、出版済み出力に対する完全再現で検証してから適用した。前段の予備測定で「各28行rootのanchored到達可能状態空間は約51.4万状態（DFS約3秒）」であることを確認済みで、これが29行への厳密適用を可能にした。

- script: `research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/runnerup29_cover_membership_20261118.py`
- output: `research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/runnerup29-cover-membership-20261118.json`（blob `05f54eb5`）
- 18 checks all PASS（二重実行 byte-identical、全体約2分: pair membership 71秒 + joint 24秒）。

## 方法

出版済み偶数/奇数r一般frameworkのformula（A型 = 14 pair + 1 singleton disjoint、B型 = 15 pair・1行二重被覆、membership/jointの全閉形式）をそのまま用い、pm値（行部分集合の重み付き完全マッチング数）のみをPmLazyで供給する。PmLazyは未計算maskをstack DFSで列挙しpopcount昇順に評価、結果を全formula間で共有する（state cap 12M・wall budget 1500秒）。

- 実装検証: 出版済みcost-12 parent output（blob `c05de9d0`）の**全1,151 singleton membershipをPmLazyが完全再現（0不一致）**。singleton membership = pm(V∖s) なので、23行parent全体で独立な23値の全root分が一致したことで実装を検証。
- 恒等式検証: Σ(A型membership) = 15·A = 559,766,766,530,770,575、Σ(B型membership) = 15·B = 129,479,048,753,742,285、Σ(全membership) = 15·総数 = 689,245,815,284,512,860 がそれぞれ独立に成立。
- A・Bは定義からの直接再計算（A = Σ_s w1(s)·pm(V∖s)、B = Σ_d Σ_{a<b} w(d,a)w(d,b)pm(V∖{d,a,b})）とも一致。
- 環境制約の記録: 単一の共有memoで全位相を通すと、pair membership位相で9,198,514状態（推定1.4〜1.8 GB）に達し、続くjoint位相の21〜23行新規maskでOOM killされた。**位相間でmemoを解放して再構築する設計**（pair位相9.2M状態→解放→joint位相3.28M状態）で全体を完了。この2段階memo設計は本環境での大規模parent解析の再現可能パターン。

## 主要な新所見（runner-up parent）

1. **総最小cover数 = 45,949,721,018,967,524（約4.59e16）**: A型 37,317,784,435,384,705（81.21%）+ B型 8,631,936,583,582,819（18.79%）。A比はcost-12 parent（83.2%）とほぼ同等で、B型比率は行数の増大でやや拡大。
2. **全1,854 root（349 pair + 1,505 singleton）がmembership > 0**（死んだrootなし）。最大 2,410,014,432,522,432（総数の5.245%）・最小 21,158,852,144,010（0.046%）。349 pair typeはすべてmultiplicity 1。
3. **pair rootがmembershipを独占**: pair最小 1,405,559,570,680,620 ≫ singleton最大 28,801,346,064,703（約49倍）。上位10 rootはすべてpair rootで、行-index 16を4本・10を5本・3を3本が含む（行indexはscript内のtarget整列順）。上位10 rootのmembership単純和は総数の50.69%（ban後の真の生存数はjoint重複を含む再計算が必要で、今回は未実施・次回候補）。
4. **上位10 rootのjoint membershipは45組み合わせすべて非ゼロ**。うち22組み合わせは行を共有（B型の二重被覆pairとしてのみ共存可能で、B型存在の直接構造証拠）。最大 joint は {4,10}×{16,22} = 128,221,248,621,342。行0はpair degree 28（他全行と接続する最大ハブ）、bottleneckは行22（cover options 62）。
5. 計算資源: pm gets 2,419,680回・最終memo 3,284,623状態（pair位相ピーク9,198,514状態）。anchored lazy DPにより、2^29表を必要としない29行parentの厳密な全root定量化が本環境の RAM 制約内で成立した。

## 解釈上の注意

membershipは代替最小cover計画への参加数であって探索コストでもverdictでもない。上位rootへの数値の集中はcover計画の偏りを示すだけである。REFUTED-D10・STERILE は LOSS 証明ではない。本分析はcover計画の組合せ論のみを主張する。

## 11×11 状態

標準11×11空盤は **UNKNOWN**。二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4 もすべて UNKNOWN。
