---
id: K1058
title: 共円ゲームの有限体盤・反転平面盤への移行と転送閾値
kind: proposition
status: computed
topics: [variants, geometry, maximum-safe, grundy]
aliases: []
relations:
- type: depends_on
  target: K0001
  note: 四点共円・共線を整数行列式で判定する完全指摘ルールの定義
- type: depends_on
  target: K0504
  note: 幾何学的禁止条件を変える変種の比較研究課題
- type: supports
  target: K0504
  note: 有限体盤・反転平面盤という具体的変種の有限結果
artifacts:
- path: research/experiments/finite-field-kyouen-20261120/README.md
  role: source
  note: AG(2,q) 盤の構造・転送閾値・最大安全サイズ
- path: research/experiments/finite-field-kyouen-20261120/INVERSIVE.md
  role: source
  note: 反転平面盤の3-設計検証・全Grundy・層サイズ公式
- path: research/experiments/finite-field-kyouen-20261120/STRATEGY.md
  role: source
  note: 初手値の分布と5×5部分勝ち
- path: research/experiments/finite-field-kyouen-20261120/FIVE_BY_FIVE.md
  role: source
  note: 5×5勝ち初手の中心菱形
- path: research/experiments/finite-field-kyouen-20261120/scripts/ff_kyouen.py
  role: solver
  note: AG(2,q) と整数格子の禁止四点列挙・Grundy計算
- path: research/experiments/finite-field-kyouen-20261120/scripts/inversive_plane.py
  role: solver
  note: P^1(F_{q^2}) 模型による反転平面の構成と3-設計検査
- path: research/experiments/finite-field-kyouen-20261120/scripts/det_threshold.py
  role: verifier
  note: 整数行列式の最大絶対値 D(n) の厳密計算
- path: research/experiments/finite-field-kyouen-20261120/scripts/transfer_threshold.py
  role: verifier
  note: q>D(n) での禁止集合一致の検証
- path: research/experiments/finite-field-kyouen-20261120/output/det_threshold.json
  role: data
  note: n=2..7 の D(n) と極値配置（四点組全列挙）
- path: research/experiments/finite-field-kyouen-20261120/output/transfer_threshold.json
  role: data
  note: 44通りの閾値一致検査
- path: research/experiments/finite-field-kyouen-20261120/output/inversive_plane.json
  role: data
  note: q=3,5 の反転平面ゲーム全値
- path: research/experiments/finite-field-kyouen-20261120/scripts/ag2_fast_target.py
  role: solver
  note: AG(2,q)の対称性利用高速完全探索
- path: research/experiments/finite-field-kyouen-20261120/ALGEBRAIC_ROUTE.md
  role: source
  note: 放物面上のcap・反転平面3-arcへの再定式化
- path: research/experiments/finite-field-kyouen-20261120/LARGE_BLOCK_PATTERN.md
  role: source
  note: 大きなブロックの有無がK/qを決める
- path: research/experiments/finite-field-kyouen-20261120/K_EQUALS_Q_REFUTED.md
  role: source
  note: K=q予想の反例（q=5でK=6）
- path: research/experiments/finite-field-kyouen-20261120/BOUND_TIGHTNESS_Q9.md
  role: source
  note: q=9の上界付近の不存在確認
- path: research/experiments/finite-field-kyouen-20261120/BOUND_TIGHTNESS.md
  role: source
  note: 上界付近のサイズの不存在確認
- path: research/experiments/finite-field-kyouen-20261120/ARC_STRUCTURE.md
  role: source
  note: 最大3-arcの円プロファイル
- path: research/experiments/finite-field-kyouen-20261120/PROFILE_NO_IMPROVEMENT.md
  role: source
  note: プロファイルが上界を改善しないことの証明
- path: research/experiments/finite-field-kyouen-20261120/LITERATURE_AXIOMS.md
  role: source
  note: 反転平面の公理I.1-I.3の確認
- path: research/experiments/finite-field-kyouen-20261120/TWO_ARC_RESOLUTION.md
  role: proof
  note: 2-arcの最大が2であることの証明と不整合の解決
- path: research/experiments/finite-field-kyouen-20261120/LITERATURE_3ARC_5.md
  role: source
  note: arcの定義確定とAd(q)の特定
- path: research/experiments/finite-field-kyouen-20261120/LITERATURE_3ARC_2.md
  role: source
  note: Sonninoの(q+5)-arcと我々のKの不整合
- path: research/experiments/finite-field-kyouen-20261120/LITERATURE_3ARC_3.md
  role: source
  note: 射影平面arcの定義確認
- path: research/experiments/finite-field-kyouen-20261120/LITERATURE_3ARC_4.md
  role: source
  note: 反転平面の公理(A1)の確認
- path: research/experiments/finite-field-kyouen-20261120/LITERATURE_3ARC.md
  role: source
  note: 3-arcの文献調査記録
- path: research/experiments/finite-field-kyouen-20261120/FOUR_FAILED_ROUTES.md
  role: source
  note: q=3 mod 4の上界改善4手法の失敗記録
- path: research/experiments/finite-field-kyouen-20261120/BOUNDS_SUMMARY.md
  role: source
  note: 全上界の総括とgapの比較
- path: research/experiments/finite-field-kyouen-20261120/COVERING_BOUND.md
  role: source
  note: 被覆による上界が弱いことの分析
- path: research/experiments/finite-field-kyouen-20261120/BOUND_GAP_ANALYSIS.md
  role: source
  note: 上界が達成されない理由の分析
- path: research/experiments/finite-field-kyouen-20261120/WHY_NO_SIZE6.md
  role: source
  note: AG(2,3)でサイズ6が不可能な理由
- path: research/experiments/finite-field-kyouen-20261120/PROPERTY_TRIVIAL.md
  role: proof
  note: 全三点ブロック性が恒真であることの確認
- path: research/experiments/finite-field-kyouen-20261120/MULTI_PAIR_BOUND.md
  role: proof
  note: ペンシル議論では上界が改善しないことの証明
- path: research/experiments/finite-field-kyouen-20261120/BOUND_IMPROVE_ATTEMPT.md
  role: source
  note: 次数議論の失敗記録
- path: research/experiments/finite-field-kyouen-20261120/BOUND_TEST_Q11.md
  role: source
  note: q=11での上界検証とK=9確定
- path: research/experiments/finite-field-kyouen-20261120/LAMBDA2_BOUND.md
  role: proof
  note: 一般上界K<=lambda_2+2=q+3の証明
- path: research/experiments/finite-field-kyouen-20261120/scripts/lambda2_bound.py
  role: verifier
  note: lambda_2の一様性検証
- path: research/experiments/finite-field-kyouen-20261120/TRIPLE_COVERAGE.md
  role: source
  note: 全三点ブロック性のq<=9での普遍性
- path: research/experiments/finite-field-kyouen-20261120/EXTREMAL_STRUCTURE.md
  role: source
  note: 極値配置の全三点ブロック構造
- path: research/experiments/finite-field-kyouen-20261120/BOUND_Q3MOD4.md
  role: source
  note: q=3 mod 4の上界比較
- path: research/experiments/finite-field-kyouen-20261120/CROSS_SHARP.md
  role: proof
  note: 十字上界の改良K<=q+2の証明
- path: research/experiments/finite-field-kyouen-20261120/scripts/cross_sharp2.py
  role: verifier
  note: 十字の交わり構造の検証
- path: research/experiments/finite-field-kyouen-20261120/DEGENERATION_QUANT.md
  role: source
  note: 退化とKの定量的関係（K/q≈1）
- path: research/experiments/finite-field-kyouen-20261120/DEGENERATION_K.md
  role: source
  note: 円の退化がKを大きくする証拠（q=17対19）
- path: research/experiments/finite-field-kyouen-20261120/SERIES_SUMMARY.md
  role: source
  note: K系列の総括と乖離の分析
- path: research/experiments/finite-field-kyouen-20261120/AG13_FAMILIES.md
  role: source
  note: AG(2,13)のブロック族別分析
- path: research/experiments/finite-field-kyouen-20261120/AG2_Q13_Q16.md
  role: source
  note: q=13,16のAG K下界
- path: research/experiments/finite-field-kyouen-20261120/Q11_EXACT.md
  role: source
  note: q=11のK=9（両盤）
- path: research/experiments/finite-field-kyouen-20261120/Q13_RESULTS.md
  role: source
  note: q=13の反転平面K=10・AG K>=13
- path: research/experiments/finite-field-kyouen-20261120/scripts/sym_exact.py
  role: solver
  note: 対称性破壊による一般完全探索
- path: research/experiments/finite-field-kyouen-20261120/AG2_Q9_EXACT.md
  role: source
  note: K(AG(2,9))=9の厳密決定
- path: research/experiments/finite-field-kyouen-20261120/INVERSIVE_Q9_EXACT.md
  role: source
  note: K(反転平面q=9)=9の厳密決定
- path: research/experiments/finite-field-kyouen-20261120/scripts/ag9_sym_dfs.py
  role: solver
  note: 2-推移性による対称性破壊探索
- path: research/experiments/finite-field-kyouen-20261120/scripts/inv9_sym_dfs.py
  role: solver
  note: 3-推移性による対称性破壊探索
- path: research/experiments/finite-field-kyouen-20261120/GROWTH_FIT.md
  role: source
  note: 成長率フィットの比較と信頼性評価
- path: research/experiments/finite-field-kyouen-20261120/GROWTH_RATE.md
  role: source
  note: Kの成長率（q^0.33対2n）
- path: research/experiments/finite-field-kyouen-20261120/AG2_Q9_SIZE10.md
  role: source
  note: AG(2,9)サイズ10の探索空間分析
- path: research/experiments/finite-field-kyouen-20261120/AG2_BOUNDS.md
  role: source
  note: 上界の比較（cross/second moment/triple）
- path: research/experiments/finite-field-kyouen-20261120/AG2_LINE_BOUNDS.md
  role: source
  note: 直線制約と共線三点の限界
- path: research/experiments/finite-field-kyouen-20261120/AG2_CROSS_GENERAL.md
  role: proof
  note: 十字ブロックによる一般上界3q^2/(2q-1)
- path: research/experiments/finite-field-kyouen-20261120/AG2_Q9_CROSS.md
  role: source
  note: AG(2,9)の分解座標と十字ブロック
- path: research/experiments/finite-field-kyouen-20261120/DET_LINEAR_GAP.md
  role: source
  note: 線形ギャップ不等式（c>=7/2）
- path: research/experiments/finite-field-kyouen-20261120/DET_MONOTONE.md
  role: source
  note: 積の最大は最大面積で達成される（a<=9）
- path: research/experiments/finite-field-kyouen-20261120/DET_CENTRE_FORMULA.md
  role: source
  note: ラグランジュ恒等式・中心公式・バウンディングボックス条件
- path: research/experiments/finite-field-kyouen-20261120/DET_CENTRE_CASES.md
  role: source
  note: 中心の内外による場合分け
- path: research/experiments/finite-field-kyouen-20261120/DET_AREA_POWER.md
  role: source
  note: Area*power<=a^4/4の鋭い上界
- path: research/experiments/finite-field-kyouen-20261120/DET_GAMMA_AREA.md
  role: proof
  note: gamma=-2*Areaの証明と|gamma|<=a^2
- path: research/experiments/finite-field-kyouen-20261120/DET_TRADEOFF.md
  role: source
  note: gammaとpowerの逆相関と積の上界
- path: research/experiments/finite-field-kyouen-20261120/AG_VS_INVERSIVE.md
  role: source
  note: AG(2,8)=8と反転平面7の乖離
- path: research/experiments/finite-field-kyouen-20261120/AG2_PRIME_POWER.md
  role: source
  note: AG(2,q)の素数冪拡張と円個数公式の破綻
- path: research/experiments/finite-field-kyouen-20261120/scripts/ag2_prime_power.py
  role: solver
  note: 素数冪AG(2,q)の構成と完全探索
- path: research/experiments/finite-field-kyouen-20261120/DET_CONTINUOUS.md
  role: source
  note: 連続緩和の正しい値と格子との差1
- path: research/experiments/finite-field-kyouen-20261120/scripts/det_continuous_exact.py
  role: verifier
  note: 凸凹場合分けによる連続最大の厳密計算
- path: research/experiments/finite-field-kyouen-20261120/INVERSIVE_Q8.md
  role: source
  note: q=8のK=7厳密決定と高速化
- path: research/experiments/finite-field-kyouen-20261120/scripts/inv_fast_target.py
  role: solver
  note: 対称性利用とfail-firstによる高速完全探索
- path: research/experiments/finite-field-kyouen-20261120/INVERSIVE_VARIANTS.md
  role: source
  note: misèreとk点版の完全計算
- path: research/experiments/finite-field-kyouen-20261120/scripts/inv_variants.py
  role: solver
  note: 変種の勝敗計算
- path: research/experiments/finite-field-kyouen-20261120/FIVE_BY_FIVE_STRUCTURE.md
  role: source
  note: 5x5のD4軌道分解
- path: research/experiments/finite-field-kyouen-20261120/AG2_MAX.md
  role: source
  note: AG(2,q)のK厳密値と反転平面との一致
- path: research/experiments/finite-field-kyouen-20261120/scripts/ag2_exact_max.py
  role: solver
  note: AG(2,q)の固定サイズ完全探索
- path: research/experiments/finite-field-kyouen-20261120/INVERSIVE_PRIME_POWER.md
  role: source
  note: 全素数冪への拡張とq=3,4,5,7のK厳密値
- path: research/experiments/finite-field-kyouen-20261120/scripts/inversive_bfs.py
  role: solver
  note: 全素数冪の反転平面構成（BFS円生成）
- path: research/experiments/finite-field-kyouen-20261120/scripts/inv_max_all_q.py
  role: solver
  note: 固定サイズ完全探索によるK決定
- path: research/experiments/finite-field-kyouen-20261120/INVERSIVE_Q7.md
  role: source
  note: 反転平面q=7のK=6厳密決定
- path: research/experiments/finite-field-kyouen-20261120/scripts/inv7_exact_target.py
  role: solver
  note: 固定サイズ完全探索による不存在証明
- path: research/experiments/finite-field-kyouen-20261120/TORUS.md
  role: source
  note: トーラス盤とAG(2,p)の一致、合成数での乖離
- path: research/experiments/finite-field-kyouen-20261120/DET_MAX_TRIPLE.md
  role: source
  note: 三点分解によるD(n)のn≤12全数確認
- path: research/experiments/finite-field-kyouen-20261120/scripts/det_max_structure.py
  role: verifier
  note: 余因子展開による三点分解D(n)計算
- path: research/experiments/finite-field-kyouen-20261120/DET_MAX.md
  role: source
  note: D(n)閉形式の証拠と残る証明課題
- path: research/experiments/finite-field-kyouen-20261120/scripts/torus_board.py
  role: verifier
  note: トーラス盤と平面盤の禁止集合比較・ゲーム値
- path: research/experiments/finite-field-kyouen-20261120/output/torus_vs_ag.json
  role: data
  note: n=3,4,5,7,11,13 の一致判定
scope: 標準q=4の禁止条件 det[x,y,x^2+y^2,1]=0 を可換環上で読むことで定義される有限体盤 AG(2,q)（q は奇素数）、位数qの反転平面（3-(q^2+1,q+1,1)設計）、および周期境界を課したトーラス盤 Z_n^2 上の完全指摘・通常プレイゲーム。q=3,5 の完全計算、n≤12 の行列式上界、トーラス盤とAG(2,p)の一致（p≤13）。
evidence: 有限完全計算（q≤5 の全安全局面 Grundy、q≤7 の最大安全サイズ厳密値（q=3,4,5,7）、n≤12 の D(n)、p≤13 のトーラス一致）と、3-設計公理の機械検査。D(n)=a^2*floor(a^2/2) は n≤12 の全数確認済みだが全称証明ではない。層サイズ公式は k≤5 の範囲で証明、k≥6 は反例あり。トーラス盤とAG(2,p)の一致は Z_p=F_p から従うが全数確認は p≤13。
---

# 共円ゲームの有限体盤・反転平面盤への移行と転送閾値

## 命題・範囲

標準共円ゲームの禁止条件は四点 `(x_i,y_i)` に対する整数行列式

```
Delta = det[[x_i, y_i, x_i^2+y_i^2, 1]] = 0
```

である。この多項式は任意の可換環で意味を持つので、盤を `F_q^2`（アフィン平面 AG(2,q)）や
反転平面に取り替えても同じ規則が定義できる。本項はその移行で何が保たれ何が壊れるかを記録する。

## 現在の根拠と限界

### 1. AG(2,q) 盤の円構造は q mod 4 で二分する（機械確認済み）

`x^2+y^2` の等方性が切り替わるため、円の構造が q mod 4 で変質する。

| q | q mod 4 | −1 は平方か | 円の個数 | 円サイズ分布 |
|---:|---:|---|---:|---|
| 3 | 3 | いいえ | 18 | {4: 18} |
| 5 | 1 | はい | 125 | {4: 100, 9: 25} |
| 7 | 3 | いいえ | 294 | {8: 294} |
| 11 | 3 | いいえ | 1,210 | {12: 1210} |
| 13 | 1 | はい | 2,197 | {12: 2028, 25: 169} |
| 17 | 1 | はい | 4,913 | {16: 4624, 33: 289} |
| 19 | 3 | いいえ | 6,498 | {20: 6498} |

q ≡ 3 (mod 4) では `x^2+y^2` が非等方で、全円がちょうど q+1 点（ユークリッド円の忠実な類似）。
q ≡ 1 (mod 4) では `x^2+y^2=(x+iy)(x−iy)` と分解し、円が直線対に退化する。
したがって「有限体版共円ゲーム」は q mod 4 で別ゲームであり、単一の族として扱えない。

### 2. 整数盤から有限体盤への転送は閾値付きでのみ成立する

素朴な期待「整数安全集合を mod q 還元すると AG(2,q) でも安全」は**偽**である。
n=4, q=5 では 5,811 個中 2,120 個、n=5, q=5 では 151,394 個中 122,168 個が反例になる。
原因は `Delta` が q の非零倍数になること。

正しい形は閾値定理である。`D(n) = max |Delta|`（n×n 格子の全四点組）とすると、
**q > D(n) なら `Delta ≡ 0 (mod q)` と `Delta = 0`（整数）が同値**になり、
整数盤の禁止集合がそのまま再現される。

| n | D(n) | 禁止四点 | 極値配置 |
|---:|---:|---:|---|
| 2 | 0 | 1 | — |
| 3 | 8 | 14 | (0,0),(2,0),(1,1),(0,2) |
| 4 | 36 | 194 | (0,0),(3,0),(1,1),(0,3) |
| 5 | 128 | 826 | (0,0),(4,0),(2,2),(0,4) |
| 6 | 300 | — | (0,0),(5,0),(2,2),(0,5) |
| 7 | 648 | — | (0,0),(6,0),(3,3),(0,6) |

観測値は `D(n) = a²⌊a²/2⌋`（`a=n−1`）に一致する。極値配置は常に
「三隅 (0,0),(a,0),(0,a) ＋ 対角点 (t,t)」で、その行列式は `−2a²t(a−t)`。
q > D(n) の 44 通りで禁止集合の完全一致を確認した（不一致 0）。

**補題（証明済み）**：三点の座標から定まる係数 gamma（x²+y² の係数）は
`gamma = −2·Area(p1,p2,p3)` を満たす。三点が `[0,a]²` 内なら `Area ≤ a²/2` なので `|gamma| ≤ a²`。

**連続上界の核心**：`|Delta| = |gamma|·|power|` で `|gamma| = 2·Area` なので、連続上界は
`Area · max|power| ≤ a⁴/4` と同値。a ≤ 7 の全三点で違反 0 で、最悪値がちょうど `a⁴/4` に一致する（鋭い上界）。
最悪ケースは a 奇数なら角の直角三角形 `(0,0),(a,0),(0,a)`（Area=a²/2, power=a²/2）、
a 偶数なら `(0,0),(a,0),(a/2,a/2)`（Area=a²/4, power=a²）。

**代数的整理**：`u=p2−p1`、`v=p3−p1` とおくと、ラグランジュの恒等式 `|u|²|v|² = (u×v)² + (u·v)²` と
外接円公式 `Area·R² = |u|²|v|²|u−v|²/(8|u×v|)` が使える。中心は
`O = ((|u|²v_y − |v|²u_y)/(2c), (|v|²u_x − |u|²v_x)/(2c))`（`c=|u×v|`）。
四点 `{0,u,v,O}` のバウンディングボックスが一辺 a に収まる条件の下で、`Area·R²` の最大は
**a ≤ 9 でちょうど `a⁴/4`** になる（極値は正方形の3角を結ぶ直角三角形）。`n`積は面積について単調ではないが、**最大は常に最大面積 `a²/2` で達成される**（a ≤ 9 の全数）。`n`さらに線形ギャップ不等式 `Area·R² ≤ a⁴/4 − c·(a²/2 − Area)` が `c ≥ 7/2` で成立する（a ≤ 8）。`n`これが示せれば「面積が最大でない場合」の評価が従う。

**連続緩和との関係**：四点目を実数に許した連続最大は `a⁴/2 + [a奇数]/2` で、
格子最大 `a²⌊a²/2⌋` との差は **a 奇数でちょうど 1**、a 偶数で 0 である（a ≤ 8 の全数計算）。
この分解により証明は「連続最大の評価」と「奇数のとき格子点で 1 下がること」の2段階に分かれる。
なお `Delta` は `gamma` の符号で凸にも凹にもなり、凹の場合は最大が内部（円の中心付近）で
達成されるため、「最大は常に角」という素朴な議論は誤りである。

**この閾値は実用上きわめて強い制約である**：D(n) は n について 4 次で増えるので、
n=11 では D(11) ≈ 5×10^5 となり、11×11 を埋め込める有限体は巨大な体に限られる。
つまり有限体盤は整数格子の近似として使えない。

### 3. 反転平面盤は q mod 4 依存を解消する

ユークリッド円の本質的性質「相異なる三点がちょうど一つの円を定める」を公理とした
有限構造が反転平面で、位数 q のそれは 3-(q²+1, q+1, 1) 設計である。
古典模型 `P¹(F_{q²})`（円は `P¹(F_q)` の `PGL(2,F_{q²})` による像）は全素数冪 q で存在する。

**全素数冪への拡張**：`F_{q²} = F_p[t]/(f)`（f は次数 2e の既約多項式）とし、
`F_q = {x : x^q = x}`（Frobenius 固定体）と取れば標数2も扱える。
円の列挙は「`P¹(F_q)` の PGL(2) 軌道」を BFS で生成する（生成元の拡大は**原始元**を選ぶ必要がある。
そうでないと軌道が部分群に閉じ、円の個数がちょうど半分になる。q=3,5 で実際に観測）。

| q | 体 | 点 | 円 | 円サイズ | 3-設計 |
|---:|---|---:|---:|---|---|
| 3 | F_9 | 10 | 30 | 4 | **True** |
| 4 | F_16 | 17 | 68 | 5 | **True** |
| 5 | F_25 | 26 | 130 | 6 | **True** |
| 7 | F_49 | 50 | 350 | 8 | **True** |
| 8 | F_64 | 65 | 520 | 9 | **True** |
| 9 | F_81 | 82 | 738 | 10 | **True** |

いずれも理論値 `n=q²+1`、`b=q(q²+1)`、`s=q+1` と一致し、全三点の一意被覆を全数確認した。
q=2 は 5点・円サイズ3で4点が同一円に載らず、ゲームが自明になるため除外する。

q=3,5 では全安全局面の Grundy まで計算した。

| q | 点 | 安全局面 | K | s | g(空盤) | Grundy 分布 | 勝ち初手 |
|---:|---:|---:|---:|---:|---:|---|---:|
| 3 | 10 | 428 | 5 | 5 | 1 | {0:202, 1:226} | 10/10 |
| 5 | 26 | 47,152 | 6 | 5 | 1 | {0:18226, 1:17226, 2:11700} | 26/26 |
| 7 | 50 | — | **6（厳密）** | 5 | — | — | — |

q=7 は全安全局面の列挙が不可能なので、最大安全サイズだけを固定サイズ完全探索で決定した。
サイズ6の安全集合は実在し、サイズ7は**存在しない**（2,551,236 ノードで全空間を尽くして確認）。
この探索は q=5 で較正済み（サイズ6発見・サイズ7不存在を再現）。
さらに q=7 の K=6 は**二つの独立実装**でノード数まで一致した
（素数専用の二次拡大構成と、一般素数冪構成＋BFS 円生成）。

数え上げ上界 `C(k,3) ≤ b` は q=7 で k≤13 を与えるが、実際の K は 6 で**差が7**。
円が q+1 点と大きいため、少数の点でも三点が同一円に集中し、組合せ的余裕がほとんどない。

| q | 点 | 円 | 円サイズ | K（厳密） | 数え上げ上界 | 差 |
|---:|---:|---:|---:|---:|---:|---:|
| 3 | 10 | 30 | 4 | 5 | 6 | 1 |
| 4 | 17 | 68 | 5 | **5** | 8 | 3 |
| 5 | 26 | 130 | 6 | 6 | 10 | 4 |
| 7 | 50 | 350 | 8 | **6** | 13 | **7** |
| 8 | 65 | 520 | 9 | **7** | 15 | **8** |

AG(2,q) 側は q=8 で K=8（64点・556ブロック、サイズ9が不存在を943,265ノードで確認）。反転平面の 7 より 1 大きい。

AG(2,q) 側は q=8 で K=8（64点・556ブロック、サイズ9が不存在を943,265ノードで確認）。
反転平面の 7 より 1 大きい。

K は 5, 5, 6, 6 とほとんど伸びず、上界との差は 1→3→4→7 と広がる。
q=8 は K=7 を厳密決定（サイズ8が不存在、1,371,617 ノード）。q=9 はサイズ8の実在のみ確認し 8≤K≤17。

**成長率**：q ≤ 8 の5点（K = 5,5,6,6,7）で log-log フィットすると `K ≈ 3.39·q^0.33` となるが、
データ点が少なく成長率の主張としては弱い（線形フィットの SSE 0.419 に対しべき乗は 0.013 だが、
実質的な情報は「K が 5 から 7 へ緩やかに増える」ことだけ）。
対照的に整数格子は `K_n ≈ 2n`（線形）。密度 K/n は q=8 で反転平面 0.108 対 整数 0.234 と約2倍の差。
初等的な数え上げ上界（triple, pair）はいずれも `O(q)` を与えるので、
観測された K の小ささは単純な数え上げでは説明できない。

### 4. 層サイズの厳密公式（k ≤ 5）

`B_c` を「円 c 上に4点以上載る」事象とすると、相異なる二円がともに成立するには
`|S| ≥ 4+4−2 = 6` が必要（二円は高々2点で交わる）。よって **k ≤ 5 では事象が互いに素**で

```
L_k = C(n,k) − b · Σ_{j=4}^{min(k,s)} C(s,j) C(n−s, k−j)      (k ≤ 5)
```

が成り立つ。q=3,5 の全 k ≤ 5 で厳密一致を確認。**k=6 では破綻する**
（q=5 の k=6 で厳密値 5,200 に対し公式は −156,000）。

### 5. 最大安全サイズ

AG(2,q) 盤（円と直線の両方がブロック）：

| q | 盤の点数 | ブロック数 | 厳密 K | 貪欲下界 | 数え上げ上界 |
|---:|---:|---:|---:|---:|---:|
| 3 | 9 | 30 | **5** | 5 | 6 |
| 4 | 16 | 78 | **5** | 5 | 8 |

注意：円の個数が q²(q−1) になるのは **q が奇素数のときのみ**。q=4（標数2）では
x²+y²=(x+y)² と分解して円が退化し、実測 58 個（理論値 48）になる。
q≡1 (mod 4) でも退化が起きる（q=5 でサイズ4の円が100個）。
| 5 | 25 | 155 | **6** | 6 | 10 |
| 7 | 49 | 350 | **6** | 6 | 13 |
| 11 | 121 | 1,342 | — | 9 | 21 |
| 13 | 169 | 2,379 | — | 13 | 24 |
| 17 | 289 | 5,219 | — | 17 | 31 |
| 19 | 361 | 6,878 | — | 14 | 35 |

**一般上界（証明済み）**：`q ≡ 1 (mod 4)` かつ `k ≥ q` のとき **`K(AG(2,q)) ≤ q + 2`**。

粗い版は `3q²/(2q−1) ≈ 1.5q`。改良版の証明は次の通り。
`−1` が平方なので `x²+y² = (x+iy)(x−iy)` と分解し、円の方程式が `s·t+a·s+b·t+c=0` になる。
`ab=c` の退化円は「列＋行」の十字（`2q−1` 点）で、これが `q²` 個ある。
安全集合は各十字に高々3点なので、`a_c + b_r − x_{cr} ≤ 3` が成り立つ。

1. `r` について和を取ると `(q−1)a_c ≤ 3q − k`。`k ≥ q` なら `a_c < 3` なので **各列・各行は高々2点**。
2. 2点を持つ列 `C₂` と行 `R₂` について、`c∈C₂, r∈R₂` なら交点が必須なので `S` は `C₂×R₂` を含む。
3. 各列は高々2点なので `|C₂|·|R₂| ≤ 2|C₂|` より `|R₂| ≤ 2`、同様に `|C₂| ≤ 2`。
4. よって `k ≤ 2·2 + (q−2)·1 = q+2`。□

q=5,9,13,17 で十字の個数が `q²` に一致し、2つの十字の交わりが「2点」または「q点」であることを確認した。

**上界の比較**：単純な組合せ上界はいずれも緩い。q=7 で triple 上界13・second moment 16・直線のみ21・4点部分集合47 に対し真値は6。
second moment（`λ₂=q+1` は一様）は triple より弱い。直線制約だけでは q=5 で k=6 のキャップが存在するため何も排除できない。
十字上界が最強（q≡1 mod 4）で、改良版 `q+2` は `K/q ≈ 1` という観測と整合する。

**全 q で有効な一般上界（無条件）**：`K ≤ λ₂ + 2 = q + 3`。

「任意の三点が同一円または同一直線上にある」は**恒真**である：三点が一直線なら直線ブロック上、
そうでなければその三点を通る円が一意に存在する。したがって下の証明は前提なしで成立する。

証明：`p,q ∈ S` を固定すると、`S\{p,q}` の各点 `r` について三点 `{p,q,r}` はブロック上にあり、
そのブロックは `p,q` を通るので `λ₂` 個のペンシルのいずれかである。
異なる `r` は異なるブロックを与える（同じなら4点を含み安全集合に矛盾）。
よって `|S| − 2 ≤ λ₂`。AG(2,q) も反転平面も `λ₂ = q+1`（一様、機械確認）なので `K ≤ q+3`。
これは `q ≡ 3 (mod 4)` で triple 上界 1.82q を大きく改善する（q=19 で 22 対 35）。
ただし真値との差は q とともに広がる（q=3 で1、q=7 で4、q=11 で5）。

**この上界はペンシル議論では改善できない**：`m` 点を固定して `C(m,2)` 個のペンシルを使っても、
包除の補正項と必要量が打ち消し合い、上界は `λ₂ + 2` のまま `m` に依らない（m=3..8 で確認）。
次数による議論も `k ≤ 2q+4` 程度で弱い。改善には別の原理が必要である。

**上界が達成されない理由**：差は q=3,5,7,9 で **1,2,4,3** と単調ではない（q=7 で最大、q=9 で減少）。
なお「q≡1 (mod 4) なら K=q」という予想は **q=5 で反例**があるため撤回した（K=6 > q=5）。

**K/q を決める決定的な要因**：**大きなブロック（サイズ > q+1）の有無**である。

| q | 大きなブロック | K/q |
|---:|---|---:|
| 7 | なし（最大 q+1） | **0.86** |
| 11 | なし（最大 q+1） | **0.82** |
| 4 | あり（2q、標数2退化） | 1.25 |
| 5 | あり（2q−1、十字） | 1.20 |
| 8 | あり（2q、標数2退化） | 1.00 |
| 9 | あり（2q−1、十字） | 1.00 |

大きなブロックは十字（`q≡1 mod 4`）または標数2の退化円（`q` 偶数）から生じる。
これらは「列＋行」や「退化した直線対」の構造を持ち、1点ずつ各列・各行に置く置換行列型の配置を
可能にするため、`K ≈ q` が達成される。
大きなブロックがない場合（q=7,11）は円がサイズ q+1 で均一なのでそのような構造が作れず `K < q` になる。

q=5 ではサイズ7,8 が、q=7 ではサイズ8,9,10 が、q=9 ではサイズ10,11,12 がいずれも不存在であることを
完全探索で確認した（ノード数は q=5:881、q=7:22,341、q=9:378,101 と急増するが完全探索可能）。
AG(2,3) では6点部分集合84個**すべて**がサイズ4の円を完全に含むため、
サイズ6の安全集合は存在しない（全数検査）。
円の被覆構造が上界との差を生んでいると考えられるが、**被覆による上界は一般には弱い**：
ランダムな k-部分集合に含まれるブロックの期待値 `E[f]` が 1 を超えるのは
q=3 で k≈6、q=5 で k=9、q=7 で k≈25 であり、真値（q=5,7 で K=6）と大きく乖離する。
被覆が効くのは盤が小さい q=3 のみである。

**上界の総括**：`q ≡ 1 (mod 4)` では十字上界 `q+2` により gap が 1〜2 に収まる
（q=5:1, q=9:2, q=13:≤2, q=17:≤2）。
一方 `q ≡ 3 (mod 4)` では λ₂ 上界 `q+3` のみで gap が 4〜9 に広がる（q=7:4, q=11:5, q=19:≤9）。
**`q ≡ 3 (mod 4)` の上界改善が最大の課題**である。試した4手法はいずれも失敗した：

1. 次数 `(k−1)(q+2−k/2) ≤ q²+q` は制約なし
2. 複数ペンシルは `λ₂+2` のまま
3. 被覆は q=3 のみ有効
4. 使用済み円のペア `C(k,2)C(k−2,2) ≤ 2C(C(k,3),2)` は常に成立し制約なし
5. 円のプロファイル（3点円 = `C(k,3)`、2点円 = `C(k,2)(q−k+3)`）は `λ₂+2` を再現するのみで改善しない

初等的な数え上げはすべて係数 ≥1 を与え、観測された `K/q ≈ 0.68〜0.86` を下回れない。
係数1未満には代数幾何・設計論・加法的組合せ論など別の原理が必要と考えられる。

**代数的再定式化**：各点を持ち上げて `v_p = (x, y, x²+y², 1) ∈ F_q⁴` とすると、
四点の共円・共線は `det[v_p1,v_p2,v_p3,v_p4] = 0`、すなわち**4ベクトルの線形従属**と同値。
よって安全集合は「どの4つも従属でない」集合であり、これは**放物面 `Z=X²+Y²` 上の cap**、
反転平面の言葉では **3-arc**（どの円とも3点以下で交わる集合）に他ならない。
符号理論的には「パリティ検査行列の任意3列が独立」に対応するが、Singleton 限界は下界しか与えない。
文献調査では最大 3-arc サイズの明示的な既知結果を確認できなかった。

Sonnino は奇数の q に対して (q+5)-arc を構成しているが、これは**別問題**であることが判明した。
反転平面の「k-arc」は各円と高々2点と定義され、公理 (A1)（任意の三点が一意に円を定める）から
**2-arc の最大サイズは 2** である（q=3,4,5,7 で計算確認）。
したがって Sonnino の arc は別の定義か、Ad(q) が標準的でない反転平面であり、
我々の K（3-arc の最大）とは直接比較できない。

なお反転平面の公理 (I.1)「任意の三点が一意に円を定める」、(I.2)「二円は一点で接する円が一意」、
(I.3)「同一円上にない4点が存在する」を文献で確認した。
我々が使った性質（三点の一意被覆、二円の高々2点交差）はすべて公理から従い、
恒真性の主張と整合する。

AG(2,11) ではサイズ10,11,12 がいずれも不存在であることを完全探索で確認し、**K=9 が確定**した。

**q ≡ 3 (mod 4) では十字がない**：ブロックは直線（サイズ q）と真円（サイズ q+1）のみ。
初等的な上界は triple `C(k,3) ≤ q³+q` から `k ≈ 1.82q` が最良
（pair は `q·C(k,2) ≤ 3b` で 2.4q、incidence は `deg·k ≤ 3b` で 2.7q とより緩い）。

**極値配置の構造**（恒真性の確認）：q=3,5,7,9 の**すべて**で、最大安全集合は
**任意の三点が同一円または同一直線上にある**（完全探索で確認：10/10, 20/20, 20/20, 84/84）。
さらに各点が同じ数の満杯ブロック（3点を持つブロック）に載る（q=7 で各点10個、q=11 で各点28個）。
これは「キャップ」（どの三点も共線でない集合）の逆の極端な構造である。
ただし `C(k,3) ≤ b` は飽和しない（q=9 で 84 対 819）ので、triple 上界の改善には直結しない。

上界/真値の比は q≡1 (mod 4) で 1.1〜1.2、q≡3 (mod 4) で 2.2〜2.7 であり、
**十字ブロックの有無が上界の鋭さを決めている**。

上界は `C(k,3) ≤ q²(q−1)+q(q+1) = q³+q`（安全集合の各三点が一意に円または直線を定め、
そのブロックは高々3点しか持てない）。整数格子の `K_n ≈ 2n` と対照的に、有限体盤は相対的に疎である。

q=7 の K=6 は固定サイズ完全探索で決定した（サイズ7が不存在、2,276,002 ノード）。

**AG(2,q) と反転平面の K は q ≤ 7 で一致するが、q=8 で乖離する**（AG=8、反転平面=7）。
点数はほぼ同じ（q² 対 q²+1）だがブロック構造は大きく異なる（AG は円と直線、
反転平面は円のみで各円 q+1 点）。q=8 で AG(2,8)=8、反転平面=7 となり**初めて乖離する**（AG が大きい）。

q=9 では**両者とも K=9 で厳密に一致**する。AG(2,9) は AGL の2-推移性、
反転平面は PGL(2,81) の3-推移性を使って対称性破壊し、サイズ10が不存在であることを
完全探索で確認した（それぞれ 261,023 ノード・21,212 ノード）。

q=11 でも**両者とも K=9 で一致**（AG は 5,524,351 ノード、反転平面は 226,681 ノードでサイズ10の不存在を確認）。
**q=9 から q=11 へ増えても K は 9 のまま**で、成長が止まる。

q=13 で**大きな乖離が現れる**：反転平面は K=10（厳密、サイズ11が不存在を217万ノードで確認）、
AG(2,13) は K≥13（サイズ13まで実在、14以上は未判定）。

| q | 3 | 4 | 5 | 7 | 8 | 9 | 11 | 13 | 16 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| AG(2,q) | 5 | 5 | 6 | 6 | **8** | 9 | 9 | **≥13** | **≥12** |
| 反転平面 | 5 | 5 | 6 | 6 | **7** | 9 | 9 | **10** | — |

AG の K は q=11→13 で 9→13以上へ跳ね上がるが、反転平面は 9→10 と緩やか。
AG のブロック構造が反転平面より緩いためと考えられる。

q=13 は `q ≡ 1 (mod 4)` なので円が退化し、サイズ12の退化円 2,028 個と
サイズ25の十字 169 個に分かれる（サイズ14の真円は存在しない）。
族別に測ると円のみで ≥14、直線のみで ≥23、全体で ≥13 であり、
**AG の円族は反転平面のサイズ14円より緩い**ことが乖離の一因と考えられる。

q=16（標数2）でも AG は K≥12 で、増加傾向が続く。

**円の退化が K を大きくする**（仮説を支持する証拠）：

| q | q mod 4 | 点 | ブロックサイズ | K |
|---:|---:|---:|---|---:|
| 17 | 1 | 289 | {16:4624, 17:306, 33:289} | **≥17** |
| 19 | 3 | 361 | {19:380, 20:6498} | **≥13** |

点数は q=19 の方が多い（361 対 289）のに、K の下界は q=17 の方が大きい（17 対 13）。
q≡1 (mod 4) では円がサイズ q−1 に退化して制約が弱まるためと考えられる。

**定量的なパターン**：`q ≡ 1 (mod 4)` では `K/q ≈ 1.00` で一定（q=9,13,17 で 1.00、q=5 で 1.20）。
これは平均ブロックサイズがちょうど `q` になることと対応する（退化円 `q−1` と十字 `2q−1` が釣り合う）。
一方 `q ≡ 3 (mod 4)` では平均サイズが `q` より大きく（真円 `q+1` が支配的）、
`K/q` は 1.67→0.86→0.82→0.68 と減少する。

q≡1 (mod 4) の q=5,9,13,17 は K が 6,9,≥13,≥17 と伸び、
q≡3 (mod 4) の q=7,11,19 は 6,9,≥13 と伸びが遅い。

同じ点数での比較では有限体盤の方がはるかに疎である：
7×7 整数の K=14 に対し AG(2,7) は 6（半分以下）。

### 6. 初手値の分布（3型）

完全計算できた盤では、初手の値の分布は3型に限られた。

| 盤 | g(空盤) | 勝ち初手 | 型 |
|---|---:|---:|---|
| 2×2, 3×3 整数 | 1 | 全点 | 全初手勝ち |
| 4×4 整数 | 0 | 0 | 全初手負け |
| **5×5 整数** | 1 | **9/25** | **部分勝ち** |
| AG(2,3), AG(2,5) | 1 | 全点 | 全初手勝ち |
| 反転平面 q=3,5 | 1 | 全点 | 全初手勝ち |

5×5 の勝ち初手は中心菱形を成す：

```
W = { (x,y) : x+y ≡ 0 (mod 2) かつ |x−2|+|y−2| ≤ 2 }
```

25 点全数で照合し不一致 0。負け初手 16 個はすべて Grundy 値 3。
この閉形式は n=5 固有の観測であり、n=3 には当てはまらない（n=3 は全初手勝ち）。

### 7. トーラス盤は素数位数で AG(2,p) と一致する

`Z_n × Z_n` に周期境界を課し、同じ行列式を mod n で評価した「トーラス盤」を考える。

| n | 素数か | トーラス禁止四点 | AG(2,n) 禁止四点 | 一致 |
|---:|---|---:|---:|---|
| 3 | はい | 18 | 18 | **True** |
| 4 | いいえ | 924 | 696 | False |
| 5 | はい | 3,150 | 3,150 | **True** |
| 7 | はい | 22,540 | 22,540 | **True** |
| 11 | はい | 642,510 | 642,510 | **True** |
| 13 | はい | 3,030,170 | 3,030,170 | **True** |

n が素数なら `Z_n = F_n` なので、トーラス盤はアフィン平面盤と点集合・禁止集合ともに同一である。
n=4 では `Z_4` が体でなく `AG(2,4)=F_4²` と異なるため、トーラス盤に 228 個の余分な禁止四点が生じる。
全 n で平面盤の禁止四点はトーラス盤に含まれる（`Delta=0 ⇒ Delta≡0 (mod n)`）。

ゲーム値では n=4 が劇的に異なる：平面盤は後手必勝（K=7）だが、
トーラス盤は先手必勝（K=4）になる。禁止四点を増やすと勝者が反転する明示例である。

### 8. 変種：misère と k 点版

反転平面ゲームの2変種を q ≤ 4 で完全計算した。

| q | 禁止点数 | ルール | 安全局面 | K | 空盤の勝者 |
|---:|---:|---|---:|---:|---|
| 3 | 4 | 通常 | 428 | 5 | 先手 |
| 3 | 4 | misère | 428 | 5 | **後手** |
| 3 | 5 | 通常 | 1,024 | 10 | **後手** |
| 3 | 5 | misère | 1,024 | 10 | **先手** |
| 4 | 4 | 通常 | 4,914 | 5 | 先手 |
| 4 | 4 | misère | 4,914 | 5 | **後手** |
| 4 | 5 | 通常 | 48,604 | 9 | 先手 |
| 4 | 5 | misère | 48,604 | 9 | **後手** |

**misère は 4 例すべてで通常版の勝敗を反転させた**（初手の勝敗も完全に反転）。
反転平面では全極大安全集合が同じ石数になる可能性が高く（q=3,4 の k=4 で最小極大 = 最大 = K）、
そうなら手番数が固定されて通常版と misère 版の勝者は必ず入れ替わる。
ただしこれは観測であって証明ではない。

**k=5 版は K をほぼ倍にする**（q=3 で 5→10、q=4 で 5→9）。
円が q+1 点しかないため、5 点そろえるのは 4 点よりずっと難しい。
k=5 版の勝者は q に依存する（q=3 は後手必勝、q=4 は先手必勝）。

## 限界

- 完全計算は q ≤ 5（反転平面の Grundy）、q ≤ 8（反転平面の K）、q ≤ 7（AG の K）、n ≤ 5（整数盤の初手）、p ≤ 13（トーラス一致）に限る。q=9 は 8≤K≤17 の範囲のみ。
- `D(n) = a²⌊a²/2⌋` は n ≤ 12 の全数確認済みだが全称証明ではない。
- 層サイズ公式は k ≤ 5 のみ。k ≥ 6 の一般公式は未取得。
- misère 反転は 4 例の観測。全極大が同石数であることの証明は未取得。
- k 点版は k ≤ 5、q ≤ 4 のみ。
- 有限体盤・反転平面盤の勝敗と整数格子盤の勝敗の関係は、閾値 q > D(n) の外側では何も主張しない。
- 5×5 の菱形がなぜその形になるか、負け初手の Grundy が全て 3 である理由は未解明。
