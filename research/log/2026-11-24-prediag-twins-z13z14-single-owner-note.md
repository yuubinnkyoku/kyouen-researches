# 単一オーナー宣言 K1302: pre-diag 双生児 z13/z14 の全称確定
(T-PDT13/T-BDT13 + T-PDT14/T-BDT14 — K1301 O9⁗ の z13/z14 部分の取得・sharpened C-PSF′ の w=13,14 実例化・z15/z16 OBS)

## §0 状態と採番 (single-owner protocol)

- 観測 HEAD (着手時): `1f08b0bc1a502cf74ba70a297b6b60dc2af33287` (2026-11-24T19:19:40Z・PG(2,8)/AG(2,8) cap games レーン)。着手時点の最新 K item = **K1301** (`84ee5369`・本高速レーンの先行実行が出版。なお K1301 chain は先行実行と本実行の 2 実行に分割誠実記録済み)。intervening commits (`ff3e99c1` W_24 s-spectrum・`1f08b0bc` cap games) は全て領域直交・非接触。
- K1301 は本レーンの先行実行が取得済み (`research/knowledge/items/K1301-prediag-twins-z11-z12.md`・同 README bullet)。よって本 package は **K1302** を使用。K1302 空き確認: search_commits "K1302" = 0 件・最新 items-touching commits に K1302 なし・**push 直前に再確認** (§0 末尾)。
- 領域: K1301 が §5 O9⁗ として登録した T-PDT13/T-BDT13・T-PDT14/T-BDT14 (z13/z14 pre-diag typed 全称) を取得。K1301 O9⁗ の z13/z14 部分を解決し sharpened C-PSF′ を w=0..14 全称化、z15/z16 (次の観測面) を OBS 登録する (dedup sweep は z=0..18 に拡張)。K1286/K1288/K1289/K1290/K1294/K1299/K1301 の全定理に触れない (内面 k>0・multi-c web は非接触)。K1295/K1296/K1297 (projective-blocking/moment)・K1298 (parity-graded)・K1299・K1300 (s-parameter)・W 系列・cap games/Pg 系列はいずれも本領域と直交。
- 規約: verdict 不消費・標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は全て UNKNOWN のまま。
- 本 package の chain は**単一実行内で完結** (K1301 と異なり分割なし): 探索 (X/Y・宣言前 self-check) → 検証機体構築 → 宣言前ローカル修正 (§2.7) → predry 4 走 → 本ノート出版 → kit → 公式 4 走 → 変異電池 → 成果物 → K item → README bullet。

## §1 主張 (claims)

座標の規約は K1286/K1288..K1301 と同一: ペア局面 H(R;(m,m+g);z)、対角座標 k := R−2m−g、
δ := R−2m、バンド域 k ≤ 0 (0 ≤ R ≤ 2m+g)。床 (bed) は (m,m) 双 Token:
b_z(j) := H(2m+j;(m,m);z), j ≤ 0。f0 は K1286 出版の対角下バンド 1 次元崩壊関数、
g1 は K1288 出版の偶奇双生児 (T-TWIN: g1(d) = 1 ⊕ f0(d) for d ≠ 1, g1(1) = f0(1) = 2):

- f0(d) = 2 (d=1); [d odd] (d ≤ 0); [d even] (d ≥ 2)
- g1(d) = 2 (d=1); [d even] (d ≤ 0); [d odd] (d ≥ 2)

**定理パッケージ (universal, 量子化: ∀m ≥ 1, ∀g ≥ 1, 全ての有効 cell, 値は m も g も経由しない):**

- **T-PDT13 (z13 band)**: H(R;(m,m+g);13) = 2·[R odd] (R < 14); g1(δ−12) (R ≥ 14)。
- **T-BDT13 (z13 bed)**: b13(j) = 2·[R odd] (R < 14, R = 2m+j); g1(j−12) (R ≥ 14)。
- **T-PDT14 (z14 band)**: H(R;(m,m+g);14) = 2·[R odd] (R < 14); f0(δ−14) (R ≥ 14)。
- **T-BDT14 (z14 bed)**: b14(j) = 2·[R odd] (R < 14); f0(j−14) (R ≥ 14)。
  (層厚 L(13) = L(14) = 2⌈w/2⌉ = 14。z14 の偶数例外 cell (R=0,2,...,12) は主則 f0(δ−14)
  と値が一致する (δ even ≤ 12 → δ−14 even ≤ −2 → f0 = 0) ので「R < 14 で 2·[R odd]」
  として統一できる。z13 の偶数 cell は主則 g1(δ−12) = 1 (δ even ≤ 10 → δ−12 even ≤ −2 は
  g1 = 1) と衝突するので層の上書きとして本物である − K1289 z3/z4・K1290 z5/z6・
  K1294 z7/z8・K1299 z9/z10・K1301 z11/z12 と同一の役割分担 (奇数平面の層は実質・
  偶数平面の層は見かけ上主則と一致)。)

**補題 (closed-form から機械照合 w ≤ 30・発現 probe w ≤ 40):**

- **L-BU13G**: v(w,14,t) = 2·[t odd] (t < 14); g1(t−12) (14 ≤ t ≤ w), ∀w ≥ 2
  (単一 Token w を平面 14 に置いた局面 = B-exit 子の値 = plane-13 則のフル形式)。
- **L-BU14G**: v(w,15,t) = 2·[t odd] (t < 14); f0(t−14) (14 ≤ t ≤ w), ∀w ≥ 2。
  (t=14 の 0 = f0(0) は主則核、t=15 の 2 = f0(1) は核の境界一致 (w ≥ 16 の q_odd(15)=15
  region) — K1289 L-BU4G・K1290 L-BU6G・K1294 L-BU8G・K1299 L-BU10G・K1301 L-BU12G
  と同一構造。)

**系 (corollaries / subsumption):**

- **C1 (K1301 O9⁗ z13/z14 RESOLVED)**: K1301 D11/Y7/Y8 が OBS として観測し
  D9(j) identity sweep から w=13,14 未証明ゆえ除外していた z13/z14 予測面が
  本項で全称定理化。K1301 O9⁗ が予告した構造 (z13 は層域横断 2 行 = C 子 budget
  12,13 (層内最終行 R=13 + seam R=14) が z12 主則域 (R ≥ 12) を読む・z14 は横断ゼロ
  ((14,14) 層厚一致)) がそのまま成立した。
- **C2 (sharpened C-PSF′ = K1301 O9⁗ の w=13,14 実例化)**: 統一形式
  **H(R;(m,m+g);w) = 2·[R odd] (R < 2⌈w/2⌉); T_w(δ − 2⌊w/2⌋) (R ≥ 2⌈w/2⌉)**,
  T_w = g1 (w 奇数) / f0 (w 偶数)。この項で w ∈ {13,14} が全称証明され、
  w ∈ {0} (K1286), {1,2} (K1288), {3,4} (K1289), {5,6} (K1290), {7,8} (K1294),
  {9,10} (K1299), {11,12} (K1301), {13,14} (本項) と代数的に同一 (verify D9(j) が
  w=0..14 全 15 面で機械照合)。w ∈ {15,16} は D11 有限 OBS のみ (dedup sweep では
  w=18 まで観測拡張)。層厚 L(w) = 2⌈w/2⌉ の一般 w 帰納は未解決 (§5 O9(5))。
- **C3 (B-exit 均一性の族)**: 単一 Token @ plane z+1 は plane-z 則を継承する:
  L-BU0 (K1286)・L-BU1G/L-BU2G (K1288)・L-BU3G/L-BU4G (K1289)・L-BU5G/L-BU6G
  (K1290)・L-BU7G/L-BU8G (K1294)・L-BU9G/L-BU10G (K1299)・L-BU11G/L-BU12G (K1301)
  に続き本項の **L-BU13G/L-BU14G (plane-13 / plane-14)** で **15 枝**になる
  (w=15,16 token plane (L-BU15G/L-BU16G 相当) は D11 OBS・全称主張なし)。

**§1.1 K1301 内面との境界 (重複なし)**: K1301 D11/Y3–Y5/Y7/Y8 の z13/z14 band OBS
(band 各 4,500 点・bad 0)・L-BU13G/L-BU14G 発現 probe (w ≤ 40)・dedup z=9..16 は
有限観測として本項が定理化する対象であった。本項の主張は R 例外層値込みの全 cell を
含み、K1301 が open にした「z13/z14 の typed 証明」を定理として確定する。
K1301 の z11/z12 定理には一切触れない (z11/z12 は z13 の C 子として外部参照
(既刊・全 R 無条件) するのみで再証明しない)。本項の typed 子 mex 構文は
K1288–K1301 の packet 構文の第 7 世代である点のみ既刊構文と同一。

## §2 手証明 (typed child mex, single R strong induction)

### §2.0 型付き子の分類 (pair @ plane z)

K1294 §2.0 / K1299 §2.0 / K1301 §2.0 と同一 (engine 定義から直接)。Budget R の局面
(m,m+g)@z (バンド内 k ≤ 0) の選択肢は 5 型で全て、子は全て budget R−1 である:

1. **fall** (小 Token 減算, m ≥ 2): child (m−1, m+g)@z, k 不変, δ_c = δ+1
   (row m−1, gap g+1; k_c = k ≤ 0 なので child もバンド内)。
2. **B-exit** (m = 1): 小 Token の減算で Token が消え、child は単一 Token
   w = g+1 @ plane z+1, budget t = R−1 (**t ≤ w**: k ≤ 0 → R ≤ 2+g → t ≤ g+1)。
   値は K0832 closed form による L-BU(z)G 表から直接 (帰納外)。
3. **compress** (大 Token 減算, g ≥ 2): child (m, m+g−1)@z, k 不変, δ_c = δ−1
   (バンド内)。
4. **corner** (g = 1, 大 Token 減算): child (m,m)@z = 床, 床座標 j_c = k = δ−1 ≤ 0
   (バンド内保証: δ ≤ g = 1)。
5. **C** (z ≥ 1): child = 1 ⊕ H(R−1;(m,m+g);z−1) (平面 z−1 の同ペア,
   budget R−1, k_c = k−1 ≤ 0)。

床 (m,m)@z の子は 3 型: **fall** (m ≥ 2: pair (m−1,m)@z, gap 1, k_c = j)、
**B** (m=1: child 単一 Token 1 @ plane z+1, t = R−1 = j+1 ≤ 1,
値 {v(1,z+1,0), v(1,z+1,1)} = {0,2} — closed form・D9(m) 照合)、**C**
(1 ⊕ 床 (m,m)@(z−1), budget R−1, 床座標 j−1)。

well-founded 性: 単一の packet {T-PDT13, T-BDT13, T-PDT14, T-BDT14} 全体で R に
ついての強帰納。全ての子の budget は R−1 であり、面間参照は常に下位 budget
(z13 の C 子は z12 = K1301 既刊で全 R 無条件、z14 の C 子は z13 = packet 内で
budget R−1)。B 子・床 B 子は closed form (帰納外)。基底 R = 0: 選択肢集合は空、
mex ∅ = 0。主張値は R=0 cell では層値 2·[0] = 0 と整合する
(z14 は主則 f0(δ−14) = f0(−2m−14) = 0 とも一致)。

### §2.1 T-PDT13 (z13 band) の証明

主張値 V(R,δ) := 2·[R odd] (R < 14); g1(δ−12) (R ≥ 14)。

**R = 0**: mex ∅ = 0 = 層値。

**R ∈ {1,...,12} (例外層前半)**: 子は全て budget R−1 ∈ {0..11}:
- fall/compress/corner 子: z13 band/床 層値 at R−1 < 14 = 2·[(R−1) odd]
  (budget 定数・子の δ_c に依らず)。
- B 子 (m=1): L-BU13G at t = R−1 < 14 → 2·[t odd] → 同一の budget 定数。
- C 子: 1 ⊕ [z12 at (R−1)] — R−1 ∈ {0..11} は z12 層域 (厚み 12) 内 → z12 層値
  2·[(R−1) odd] → C = 1 ⊕ 2·[(R−1) odd]。

選択肢集合: R=1: {0, 1} → mex = **2** ✓; R=2: {2, 3} → **0** ✓; R=3: **2** ✓;
R=4: **0** ✓; ... (R 奇数で {0,1} → 2、R 偶数で {2,3} → 0 の交互) ...; R=11:
{0,1} → **2** ✓; R=12: {2,3} → **0** ✓ (C 子 budget 11 は z12 層域 (R<12) 内 —
域を跨がない)。

**R = 13 (層域横断 1 列目・K1299 §2.1 R=9・K1301 §2.1 R=11 の対)**: 子 budget 12:
- fall/compress/corner 子: z13 層値 at 12 → **0** (2·[12 odd])。
- B 子 (m=1): L-BU13G t=12 < 14 → **0**。
- **C 子: 1 ⊕ [z12 at budget 12 = z12 主則域 (R ≥ 12) を読む層域横断]** —
  f0(δ₂−12), δ₂ = 12−2m (C 子の δ) → δ₂−12 = −2m even ≤ −2 → f0 = 0 → C = **1**
  (δ₂ parity 固定により値は定数 — K1301 §2.1 R=11 が z10 主則 f0(δ₂−10) を読んだ
  構造の δ−2 平行移動。z12 seam 直後の主則読み)。
- 選択肢集合 = {0, 1} → mex = **2** = 2·[13 odd] ✓。

**R = 14 (主則への継ぎ目・横断 2 列目)**: 子 budget 13:
- fall/compress/corner/B: z13 層値 at 13 → **2** (B: L-BU13G t=13 < 14 → 2)。
- C: **1 ⊕ [z12 at budget 13, 主則]**: f0(δ₂−12), δ₂ = 13−2m odd ≤ 11 →
  δ₂−12 odd ≤ −1 → f0 = 1 → C = **0** (層域横断 2 列目)。
- 選択肢集合 = {2, 0} → mex = **1**。主張値: g1(δ−12) at R=14 (δ = 14−2m even ≤ 12):
  δ−12 even ≤ 0 → g1 = 1 ✓。

**R ≥ 15 (主則)**: 子は全て主則読み (budget R−1 ≥ 14):
- fall 子: g1(δ_c−12) at δ_c = δ+1 → **g1(δ−11)**。
- B 子 (m=1): L-BU13G main at t = R−1 = δ+1 ≥ 14 → g1(t−12) = **g1(δ−11)**
  (fall 子と同じ表を再生 — B-exit 再生構造の z13 版)。
- compress 子: **g1(δ−13)**; corner 子 (g=1): 床 T-BDT13 main at j_c = δ−1 →
  **g1(δ−13)** (compress 子と同値)。
- C 子: 1 ⊕ f0(δ₂−12) at δ₂ = δ−1 → **1 ⊕ f0(δ−13) = g1(δ−13)** (δ = 14 のとき
  δ−13 = 1 で C = 1 ⊕ f0(1) = 3 のみ例外)。

場合分け (δ ≡ R (mod 2), δ ≤ g; B 子・corner 子は m=1/g=1 の行にのみ出現するが
値は fall/compress と同一なので場合分け不要)。この表は K1301 §2.1 z11 表の
δ → δ−2 平行移動 (核 cell δ=11→13・C 核 δ=12→14 の再核算化) で閉じる:

| δ (parity, range) | fall/B g1(δ−11) | comp/corner g1(δ−13) | C 1⊕f0(δ−13) | 集合 S | mex | 主張 g1(δ−12) |
|---|---|---|---|---|---|---|
| odd, δ ≤ −1 | g1(even ≤ −12)=1 | g1(even ≤ −14)=1 | 1⊕f0(even ≤ −14)=1⊕0=1 | {1} | 0 | g1(odd ≤ −13)=[even]=0 ✓ |
| δ = 1 | g1(−10)=1 | g1(−12)=1 | 1 | {1} | 0 | g1(−11)=[even]=0 ✓ |
| δ = 3 | g1(−8)=1 | g1(−10)=1 | 1 | {1} | 0 | g1(−9)=[even]=0 ✓ |
| δ = 5 | g1(−6)=1 | g1(−8)=1 | 1 | {1} | 0 | g1(−7)=[even]=0 ✓ |
| δ = 7 | g1(−4)=1 | g1(−6)=1 | 1 | {1} | 0 | g1(−5)=[even]=0 ✓ |
| δ = 9 | g1(−2)=1 | g1(−4)=1 | 1 | {1} | 0 | g1(−3)=[even]=0 ✓ |
| δ = 11 | g1(0)=1 | g1(−2)=1 | 1 | {1} | 0 | g1(−1)=[even]=0 ✓ |
| δ = 13 (核) | g1(2)=0 | g1(0)=1 | 1⊕f0(0)=1 | {0,1} | 2 | g1(1)=2 ✓ |
| δ = 15 | g1(4)=0 | g1(2)=0 | 1⊕f0(2)=1⊕1=0 | {0} | 1 | g1(3)=[odd]=1 ✓ |
| odd, δ ≥ 17 | g1(even ≥ 6)=0 | g1(even ≥ 4)=0 | 1⊕f0(even ≥ 4)=1⊕1=0 | {0} | 1 | g1(odd ≥ 5)=[odd]=1 ✓ |
| even, δ ≤ 0 | g1(odd ≤ −11)=0 | g1(odd ≤ −13)=0 | 1⊕f0(odd ≤ −13)=1⊕1=0 | {0} | 1 | g1(even ≤ −12)=[even]=1 ✓ |
| δ = 2 | g1(−9)=0 | g1(−11)=0 | 1⊕f0(−11)=1⊕1=0 | {0} | 1 | g1(−10)=1 ✓ |
| δ = 4 | g1(−7)=0 | g1(−9)=0 | 0 | {0} | 1 | g1(−8)=1 ✓ |
| δ = 6 | g1(−5)=0 | g1(−7)=0 | 0 | {0} | 1 | g1(−6)=1 ✓ |
| δ = 8 | g1(−3)=0 | g1(−5)=0 | 0 | {0} | 1 | g1(−4)=1 ✓ |
| δ = 10 | g1(−1)=0 | g1(−3)=0 | 1⊕f0(−3)=1⊕1=0 | {0} | 1 | g1(−2)=1 ✓ |
| δ = 12 | g1(1)=2 | g1(−1)=0 | 1⊕f0(−1)=1⊕1=0 | {2,0} | 1 | g1(0)=1 ✓ |
| δ = 14 (C 核) | g1(3)=1 | g1(1)=2 | 1⊕f0(1)=3 | {1,2,3} | 0 | g1(2)=0 ✓ |
| even, δ ≥ 16 | g1(odd ≥ 5)=1 | g1(odd ≥ 3)=1 | 1⊕f0(odd ≥ 3)=1⊕0=1 | {1} | 0 | g1(even ≥ 4)=[odd]=0 ✓ |

全 δ 場合で mex = 主張値。■

### §2.2 T-BDT13 (z13 bed) の証明

主張値 b13(R,j): 2·[R odd] (R < 14); g1(j−12) (R ≥ 14), R = 2m+j, j ≤ 0。

R = 0: mex ∅ = 0 ✓。

**R ∈ {1,...,12} (例外層前半)**: 子 budget R−1 ∈ {0..11}:
- fall 子 (m ≥ 2): pair (m−1,m)@z13 → 層値 2·[(R−1) odd] (budget 定数)。
- B 子 (m = 1): v(1,14,t) at t = R−1 ∈ {0,1} → 0/2 = 2·[t odd]
  (m=1 は R ≤ 2 のみ: j = R−2 ≤ 0)。
- C 子: 1 ⊕ [b12 at (R−1), 床座標 j−1]: z12 床層域 (厚み 12) 内 → 2·[(R−1) odd]。

選択肢集合: R 奇数: {0,1} → **2** ✓; R 偶数: {2,3} → **0** ✓ (C 子 budget 11 までは
z12 床層域内・R=12 まで域を跨がない)。

**R = 13 (層域横断 1 列目・m ≥ 7, j = 13−2m odd ≤ −1)**: 子 budget 12:
- fall: pair (m−1,m)@z13 層値 at 12 → **0**。
- C: **1 ⊕ b12 at budget 12 = z12 床主則域 (R ≥ 12)**: f0((j−1)−12) = f0(j−13):
  j odd → j−13 even ≤ −14 → f0 = 0 → C = **1** (band 版 §2.1 R=13 と対)。
- 集合 {0, 1} → mex = **2** ✓。

**R = 14 (継ぎ目・m ≥ 7, j = 14−2m even ≤ 0)**: 子 budget 13:
- fall: pair (m−1,m)@z13 層値 at 13 → **2**。
- C: **1 ⊕ b12 at budget 13 (主則) 床座標 j−1**: f0(j−13): j even → j−13 odd ≤ −11 →
  f0 = 1 → C = **0** (横断 2 列目)。
- 集合 {2, 0} → mex = **1**。主張 g1(j−12): j even → j−12 even ≤ −12 →
  g1 = [even] = 1 ✓。

**R ≥ 15 (主則)**: 子は主則読み (child budget ≥ 14):
- fall: pair (m−1,m)@z13 main at δ_c = (R−1)−2(m−1) = j+1 → g1(j+1−12) = **g1(j−11)**。
- C: 1 ⊕ b12 main at 床座標 j−1: f0(j−13) → **1 ⊕ f0(j−13) = g1(j−13)**
  (j−13 ≤ −13 なので f0 の核 d=1 は不成立・常に g1)。
- B 子は m = 1 で R ≤ 2 にしか現れない (主則域外)。

| j (parity) | fall g1(j−11) | C g1(j−13) | 集合 | mex | 主張 g1(j−12) |
|---|---|---|---|---|---|
| odd, j ≤ −1 | g1(even ≤ −12)=1 | g1(even ≤ −14)=1 | {1} | 0 | g1(odd ≤ −13)=[even]=0 ✓ |
| even, j ≤ 0 | g1(odd ≤ −11)=0 | g1(odd ≤ −13)=0 | {0} | 1 | g1(even ≤ −12)=[even]=1 ✓ |

■ (bed は compress/corner 子を持たない — 両減算が同じ fall 子に縮退する。
K1301 §2.2 z11 床表の δ → δ−2 平行移動。)

### §2.3 T-PDT14 (z14 band) の証明

主張値 V(R,δ) := 2·[R odd] (R < 14); f0(δ−14) (R ≥ 14)。

R = 0: mex ∅ = 0 = 層値 ✓ (= 主則 f0(δ−14) = f0(−2m−14) = 0 とも一致)。

**R ∈ {1,...,13} (例外層)**: 子 budget R−1 ∈ {0..12} — **全て z14 層域 (< 14) 内 かつ
z13 層域 (< 14) 内** (z13/z14 の層厚が一致するため C 子は域を跨がない —
K1294 §2.3 z8 の (8,8)・K1299 §2.3 z10 の (10,10)・K1301 §2.3 z12 の (12,12)
横断ゼロ型の (14,14) 版・層内部で閉じる):
- fall/compress/corner: z14 band/床 層値 at R−1 → 2·[(R−1) odd]。
- B (m=1): L-BU14G at t = R−1 < 14 → 2·[t odd] → 同一。
- C: 1 ⊕ [z13 at (R−1)]: z13 層値 (packet T-PDT13, R−1 < 14) 2·[(R−1) odd]。

集合: R 奇数: {0,1} → **2** ✓; R 偶数: {2,3} → **0** (= 主則 f0(δ−14): δ even ≤ 10
→ δ−14 even ≤ −4 → 0 と一致 — 偶数 cell は層値と主則が同一); R=13: {0,1} → **2** ✓
(C 子 budget 12 は z13 層域内・横断ゼロの帰結: 層域横断 (z11/z13 型) とは逆に本
packet の偶数面は全子が層定数)。

**R = 14 (継ぎ目)**: 子 budget 13:
- fall/compress/corner: z14 層値 at 13 → **2**。
- B: L-BU14G t=13 < 14 → **2**。
- C: 1 ⊕ [z13 at budget 13, 層値 2] → C = **3** (z13 層域は R < 14 なので
  budget 13 はまだ層 — K1290 z6 seam・K1294 z8 seam・K1299 z10 seam・K1301 z12 seam
  (C 子 budget = 下位面層値 2 → 3) と同一の役割)。
- 集合 {2,3} → mex = **0**。主張: f0(δ−14) at δ even ≤ 12 → δ−14 even ≤ −2 →
  0 ✓。

**R ≥ 15 (主則)**: 子は全て主則読み (budget R−1 ≥ 14):
- fall: f0(δ_c−14) at δ_c = δ+1 → **f0(δ−13)**。
- B (m=1): L-BU14G main at t = R−1 = δ+1 ≥ 14: f0(t−14) = **f0(δ−13)**
  (fall 再生)。
- compress: **f0(δ−15)**; corner (g=1): T-BDT14 main at j_c = δ−1 →
  **f0(δ−15)** (compress 子と同値)。
- C: 1 ⊕ g1(δ₂−12) at δ₂ = δ−1 → **1 ⊕ g1(δ−13) = f0(δ−13)** for δ ≠ 14
  (δ=14 のとき 3)。

(K1301 §2.3 z12 表の δ → δ−2 平行移動。核 cell: 核 δ=13→15・C 核 δ=12→14・
comp 核 δ=14→16。)

| δ (parity, range) | fall/B f0(δ−13) | comp/corner f0(δ−15) | C 1⊕g1(δ−13) | 集合 S | mex | 主張 f0(δ−14) |
|---|---|---|---|---|---|---|
| even, δ ≤ 12 | f0(odd ≤ −1)=1 | f0(odd ≤ −3)=1 | 1⊕g1(odd ≤ −1)=1⊕0=1 | {1} | 0 | f0(even ≤ −2)=0 ✓ |
| δ = 14 (C 核) | f0(1)=2 | f0(−1)=1 | 1⊕g1(1)=3 | {2,1,3} | 0 | f0(0)=0 ✓ |
| δ = 16 (comp 核) | f0(3)=0 | f0(1)=2 | 1⊕g1(3)=1⊕1=0 | {0,2} | 1 | f0(2)=1 ✓ |
| even, δ ≥ 18 | f0(odd ≥ 5)=0 | f0(odd ≥ 3)=0 | 1⊕g1(odd ≥ 5)=1⊕1=0 | {0} | 1 | f0(even ≥ 4)=1 ✓ |
| odd, δ ≤ 13 | f0(even ≤ 0)=0 | f0(even ≤ −2)=0 | 1⊕g1(even ≤ 0)=1⊕1=0 | {0} | 1 | f0(odd ≤ −1)=1 ✓ |
| δ = 15 (核) | f0(2)=1 | f0(0)=0 | 1⊕g1(2)=1⊕0=1 | {1,0} | 2 | f0(1)=2 ✓ |
| odd, δ ≥ 17 | f0(even ≥ 4)=1 | f0(even ≥ 2)=1 | 1⊕g1(even ≥ 4)=1⊕0=1 | {1} | 0 | f0(odd ≥ 3)=0 ✓ |

全 δ 場合で mex = 主張値。■

### §2.4 T-BDT14 (z14 bed) の証明

主張 b14(R,j): 2·[R odd] (R < 14); f0(j−14) (R ≥ 14)。

R = 0: 0 ✓ (= 層値 = 主則 f0(−2m−14)=0)。

R ∈ {1..13}: 層内部 (上記 §2.3 と同一の (14,14) 横断ゼロ): fall 子 = pair
(m−1,m)@z14 層値、B 子 (m=1, R ≤ 2) = v(1,15,t) t∈{0,1} = {0,2} = 2·[t odd]、
C 子 = 1 ⊕ b13 at (R−1) (z13 床層域・厚み 14 内 → 層値)。集合: R odd:
{0,1} → **2** ✓; R even: {2,3} → **0** ✓ (主則 f0(j−14): j even → j−14 even
≤ −14 → 0 と一致)。

**R = 14 (継ぎ目, m ≥ 7, j = 14−2m even ≤ 0)**: 子 budget 13:
- fall: pair (m−1,m)@z14 層値 at 13 → 2。
- C: 1 ⊕ b13 at budget 13 (z13 床層値 at 13: 2) → 3 (z13 床層域は R < 14 なので
  budget 13 は層 — 横断ゼロ)。
- 集合 {2,3} → mex **0** = 主則 f0(j−14): j even → j−14 even ≤ −14 → 0 ✓。

**R = 15 (m ≥ 8, j odd)**: 子 budget 14 (両面とも主則域):
- fall: pair (m−1,m)@z14 main at δ_c = j+1 → f0(j+1−14) = **f0(j−13)**:
  j odd → j−13 even ≤ −12 → 0。
- C: 1 ⊕ b13 at budget 14 (main) 床座標 j−1: g1((j−1)−12) = g1(j−13): j odd →
  j−13 even ≤ −12 → g1 = 1 → C = **0**。
- 集合 {0} → mex **1** = 主則 f0(j−14): j odd → j−14 odd ≤ −13 → 1 ✓。

**R ≥ 16 (主則)**: 子は主則読み:
- fall: **f0(j−13)**; C: 1 ⊕ g1(j−13) = **f0(j−13)** for j ≠ 14 (j ≤ 0 常に)。
- mex({f0(j−13)}) — 単一値 v なら mex = 0 (v ≠ 0), 1 (v = 0):
  - j odd: f0(even ≤ −12)=0 → mex **1** = 主張 f0(odd ≤ −13)=1 ✓。
  - j even: f0(odd ≤ −13)=1 → mex **0** = 主張 f0(even ≤ −14)=0 ✓。■

### §2.5 L-BU13G / L-BU14G の閉形式からの導出

K0832 closed form v(x,z,R) から直接読む。token plane 14, w ≥ 2 (L-BU13G):
- w ≥ 15: region 1 ≤ 14 ≤ w−1, m = q_odd(14) = 13: t ≤ 13: 2·[t odd] (層 t < 14
  と一致、t = 13 の 2 = g1(1) は層核と主則核の境界値の一致 — K1289 L-BU4G・
  K1290 L-BU6G・K1294 L-BU8G・K1299 L-BU10G・K1301 L-BU12G と同一); 13 < t ≤ w:
  (t+14)%2 = t%2: t 偶 → 0 = g1(t−12) (even ≥ 2 → [odd]=0), t 奇 → 1 =
  g1(t−12) (odd ≥ 3 → [odd]=1)。
- w = 14: region z = x: t 奇 ≤ 27: 2; t 偶 ≤ 13: 0 (= 層値); t=14: 偶 > 13 →
  x%2 = 0 = g1(2) = 0 (主則核 cell の一致)。
- w ∈ {2,...,13}: region z ≥ x+1: m = q_odd(w) ≤ 13: t ≤ m: 2·[t odd] (層内);
  t > m, t ≤ w: w%2 — w 偶 {2,...,12} で t = w が該当するのみで値 0 = 層値
  2·[w odd] = 0 と一致、w 奇は m = w で不使用。全域層値 (t ≤ w ≤ 13 < 14)。
token plane 15, w ≥ 2 (L-BU14G):
- w ≥ 16: m = q_odd(15) = 15: t ≤ 15: 2·[t odd] (t < 14 層; t=14: 0 = f0(0) =
  主則核の一致; t=15: 2 = f0(1) = 核の一致); 15 < t ≤ w: (t+15)%2 = 1−t%2:
  t 偶 → 1 = f0(t−14) (even ≥ 2 → [even]=1), t 奇 → 0 = f0(t−14)
  (odd ≥ 3 → 0)。
- w = 15: region z = x: t 奇 ≤ 29: 2 (t=15: 2 = f0(1) ✓); t 偶 ≤ 14: 0
  (t=14: 0 = f0(0) ✓); t ≤ 13 は層値と一致。
- w ∈ {2,...,14}: region z ≥ x+1: m = q_odd(w) ≤ 13: t ≤ m: 2·[t odd];
  t > m, t ≤ w ≤ 14: w%2 (w 偶: t=w のみ 0 = 層値 ✓; w=14: m=13, t=14:
  w%2 = 0 = f0(0) = 0 ✓; w 奇は m = w で不使用)。
全 twist は機体 D9(a)/(b) が closed form × canonical engine × 主張表の三方で
w ≤ 30 照合 (各 493 点)・Y7 が w ≤ 40 発現 probe で補強。■

### §2.6 well-founded 性 (まとめ)

packet {T-PDT13, T-BDT13, T-PDT14, T-BDT14} の証明は単一の R 強帰納:
全子は budget R−1 (engine の子定義)。面間参照: z13 の C 子 = z12 (K1301, 全 R
無条件); z14 の C 子 = z13 (packet, budget R−1); 床 C 子 = plane−1 床
(z13 床の C 子 = b12 = K1301 既刊; z14 床の C 子 = b13 = packet T-BDT13,
budget R−1)。B 子は K0832 closed form (L-BU13G/L-BU14G + w=1 edge {0,2}) で
帰納外。帰納は R のみで整礎 (m, g に依らない子値表)。各 R での子値の列挙は
§2.1–§2.4 の場合表 (R ≤ 14 は層定数読みの列挙、R ≥ 15 は δ parity の場合表)
で全ての (m, g, k) を尽くす。層厚 14 世代の構造は §2.1/§2.2 の「C 子 budget 12
(R=13・z12 seam 直後) と budget 13 (seam R=14) が下位面 (z12, 層厚 12) の主則域
を読む」層域横断が **2 行** (値は δ₂ parity 固定により定数 0/1 に落ちる・
K1299 z9 の R=9/R=10・K1301 z11 の R=11/R=12 と同型の平行移動) と、§2.3/§2.4 の
「z14 の層域横断がゼロ (z13 と層厚が一致 (14,14))」の対である (第 7 世代・
横断型 = 奇数世代 w=13・横断ゼロ型 = 偶数世代 w=14 の mod 2 ペア構造は
K1289/K1290/K1294/K1299/K1301 と同一)。

### §2.7 検証機体の宣言前修正の誠実な記述

- 例外層 R ∈ {0,...,13} の値 2·[R odd] は宣言前探索 (§3 X1–X4) で (R,δ) 平面
  で mixed cell 0 として先に特定済み (K1289 の「slope trap」教訓を適用)。
- m 依存性・g 依存性は主張域内で一度も観測されていない (§3 Y1/Y2 広域)。
  主張は typed 証明による全称主張であり、census は照合である。
- honest 記録: 検証機体 verify_k1302.py は K1301 kit の verify_k1301.py からの
  機械的 surgery (宣言・主張関数・typed 電池・D 電池の構文平行移動) で生成したが、
  初回生成では **D1–D8 の engine 呼び出しの plane 実引数が古いまま (11/12) 残り**、
  宣言前ローカル初回実行が bad 2,376 (D1 1,137・D2 25・D3 794・D4 12・D5–D8
  計 408・engine は正しく主張面 13/14 が誤り) を指摘した。これは定理側の反例
  ではなく機体生成の機械的瑕疵であり、plane 引数 4 箇所×2 を 13/14 に修正し
  docstring/stale comment も全面書き換えた後に bad 0・全電池 PASS を確認して
  から本宣言に至った (修正後 sha256 が §4 の宣言 sha。探索 X/Y は修正前に
  最初から正しい plane で走っているので影響なし)。
- honest 記録 2: D11 far-row 電池の設計は K1301 §2.7 の教訓を最初から適用し、
  z15/z16 の層厚 16 に対して R ≥ 16 guard (主則域行のみ) + low-R (R<16) は
  hist probe として分離した。よって宣言前の電池設計修正は今回は不要であった。

## §3 宣言前探索 (pre-declaration; explore_k1302.py / explore2_k1302.py 出力)

- X1/X3 (z13/z14 band m≤12 g≤25 k≥−60, (R,δ) 表): mixed (R,δ) cell それぞれ
  cells 468 中 0/0 (X2/X4 beds m≤12 j∈[−30..0] は 168 cell 中 0/0)。低 R 行
  (R=0..13) が定数 0/2/0/2/.../2 (層厚 14 の直接観測)。R=14 seam 行 (z13 は全 1 =
  g1(even ≤ 0)、z14 は全 0 = f0(even ≤ −2))。R≥15 行が g1(δ−12) / f0(δ−14) に一致
  (表示窓内の非核 cell の一致。窓外の核 cell z13 δ=13 → 2・z14 δ=15 → 2 は
  X8 typed self-check・Y1/Y2 wide census で確認)。
- X2/X4 (beds): 同一の R 層構造・mixed 0/0 (R=14 行: z13 全 1・z14 全 0)。
- X5/X6: L-BU13G/L-BU14G 発現 census (w ≤ 30, t ≤ w; engine vs closed form vs
  plane-13/14 法則): 1,972 checks bad 0/0。w=1 edge: v(1,14,{0,1})={0,2},
  v(1,15,{0,1})={0,2}。
- X7: sharpened C-PSF′ probe (z=0..16, 320 (R,δ) cell × 17 面): bad 全 0。
- X8: typed 子 self-check (宣言前): 子を申立テーブル (z13/z14 申立 + K1301
  z11/z12 既刊) + closed form からのみ構成した mex が申立値・engine と一致するかを
  slices 3,878 点・beds 228 点で確認: bad 0/0 (手証明 §2 構文の宣言前検証)。
- Y1/Y2: z13/z14 band+beds の wide census (D1–D4 と同一 box): 8,928/360 × 2
  bad 0。
- Y3/Y4/Y5: z15/z16 OBS (band 4,500 × 2, beds 120 × 2, far-row m=12 R ≥ 16
  210 × 2 (low-R 行は事前に分離済み), low-R (R<16) hist {0:637, 2:616} × 2
  cells 1,253): cpsf 予測 vs engine bad 全 0 (有限観測・全称主張なし)。
- Y6: ordered vs canonical engine 交差 (z=13..16, 各 464 cells): mismatch 全 0。
- Y7: L-BU13G/L-BU14G (w ≤ 40, 858 cells each) bad 0 + 発現 **L-BU15G**
  (v(w,16,t) = plane-15 law: 2·[t odd] (t<16) / g1(t−14))・**L-BU16G** 発現
  (v(w,17,t): 2·[t odd] (t<16) / f0(t−16)) を w ≤ 40 probe: bad 0
  (z=16,17 token plane は OBS)。
- Y8: T-TWIN identity d∈[−260..260] bad 0; z=0..18 dedup (R,δ) sweep:
  全 19 面 mixed 0・cpsf bad 0 (**C-PSF′ が plane 18 まで観測拡張**・K1301 Y8
  の z≤16 から 2 面拡張)。

## §4 機体宣言 (machine declaration, publish-then-execute)

`verify_k1302.py` (sha256 publish 時に kit で宣言 =
`336aaf7a80f518a56e5dee70307ffe6bfedc96d24b0420819fec0815e5fafb16`・engine
pin `bd5f22e415a78368c9b798296bc84948d5637decbf3c21a92404d45fb12e3a92`
startup gate 内蔵・embed は K1138/K1282..K1301 と同一 bytes)。engine_block.py
sha256 `582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0`
(K1282–K1301 kit と byte-identical・explore 系 import 用単体)。バッテリ:

| # | 内容 | 期待 count |
|---|---|---|
| D1 | z13 band census (m≤14, g≤25, k∈[max(−30,−2m−g),0]) | 8,928 |
| D2 | z13 beds census (m≤18, j∈[−36..0]) | 360 |
| D3 | z14 band census (D1 box) | 8,928 |
| D4 | z14 beds census (D2 box) | 360 |
| D5 | typed z13 slices (m≤10, g≤14, k≥−14): typed mex == claim == engine | 1,939 |
| D6 | typed z13 beds (m≤10, j≥−16) | 114 |
| D7 | typed z14 slices (D5 box) | 1,939 |
| D8 | typed z14 beds (D6 box) | 114 |
| D9 | (a) L-BU13G 493 + (b) L-BU14G 493 + (c) K1301 anchors T-PDT11/T-BDT11/T-PDT12/T-BDT12 再照合 4,690 + (d) K1299 anchors 再照合 4,690 + (e) K1294 anchors 再照合 4,690 + (f) K1290 anchors 再照合 4,690 + (g) K1289 anchors 再照合 4,690 + (h) K1288 anchors 再照合 4,690 + (i) K1286 anchors 再照合 2,345 + (j) sharpened C-PSF′ identity sweep w=0..14 (pair box + bed box) 35,175 + (k) T-TWIN algebra d∈[−100..100] 201 + (l) closed form vs both engines (x∈2..16, z∈2..15, R∈x+1..x+4) 1,680 + (m) B-exit w=1 edge values (v(1,14,t)/v(1,15,t), t≤1) 4 | 68,531 |
| D10 | cross-engine canonical vs ordered (z13/z14 pair m≤8, g≤10, k≥−8 + beds m≤8 j≥−8) | 1,516 |
| D11 | OBS: z15/z16 band (m≤10,g≤20,k≥−50) 4,500×2 + beds (m≤10,j≥−24) 120×2 + far-row m=12 R≥16 210×2 + low-R (R<16) hist probes 1,253×2 + L-BU15G/L-BU16G plane-token sweep (z=16,17, w≤30) 493×2 + dedup (R,δ) sweep z=0..18 (320 × 19) 6,080 | 19,232 |

**総計 111,961 比較点・期待 overall_bad = 0** (宣言前 predry 4 走で
counts [8928,360,8928,360,1939,114,1939,114,68531,1516,19232]・
bad 全 0・stdout byte-identical sha256
`f6f26e095f1cb44b597fd2a3b7043c170e111f99119524c3099ac34630b43b0e`
を確認済み・約 19–20s/走)。

変異電池 (公式 run の前に期待値を宣言):
- `--tamper-engine`: rc=2・mutated sha `0ea47a80761d2b20bf414cd52b1535fba56829c3a4c232d1b2f5da3f81441882` ≠ pin (K1282–K1301 と同一変異)。
- `--tamper=z13s`: rc=1, D1 bad 8,928。`--tamper=z13b`: rc=1, D2 bad 360。
- `--tamper=z14s`: rc=1, D3 bad 8,928。`--tamper=z14b`: rc=1, D4 bad 360。
- 他バッテリ (D5–D11) は census クレームの flip の影響を受けない
  (typed 側は flip されないので D5–D8 の 3-way 照合は主張値のまま engine と
  一致する; 対角の影響は D1–D4 の bad のみ)。

公式 4 走: 同一 cwd (PYTHONHASHSEED random/1) × 2 + 隔離 tree (env -i,
PYTHONHASHSEED 99/7) × 2、stdout byte-identical が要求 (fetch-back bytes から
走行)。

## §5 open 登録 (有限観測・予想と次課題; 全称主張なし)

- **O9(5) (C-PSF′ の w 帰納 — 系列第四次update: K1299 O9‴ → K1301 O9⁗ → 本項)**:
  全称は w ∈ {0..14} まで (本項で +2)。**Y8 dedup sweep で z=15..18 が 320 cell × 4 面で
  mixed 0・cpsf bad 0・X3/Y3–Y5 band/bed/far/lowR OBS が w=15,16 を直接支持**
  (K1301 の z≤16 dedup から +2)。次の単一オーナー候補は
  T-PDT15/T-BDT15・T-PDT16/T-BDT16 (z15/z16 typed・§2 と同一構文: C 子は
  本項 z13/z14 定理 (全 R・例外層込み) を参照。z15/z16 の層厚は
  L(15) = L(16) = 2⌈15/2⌉ = 16。層域横断は z15 では C 子 budget 14,15 (R=15
  層内 + seam R=16) の 2 行が z14 主則域 (R ≥ 14) を読む・z16 では横断ゼロ
  ((16,16)・z14 型)。層核の mex{0,1}=2/mex{2,3}=0 機構は w 非依存と root 交代
  なし。完了で sharpened C-PSF′ が w=16 まで全称化)。
- **O10(5) (L-BUzG 族の全称形 — K1299 O10‴ → K1301 O10⁗ の系列update)**: 15 枝
  (z+1 = 1..15) まで全称。**L-BU15G/L-BU16G (token plane 16/17 = plane-15/16 則:
  2·[t odd] (t<16) / g1(t−14) (z=16), f0(t−16) (z=17)) を w ≤ 30 (verify)・
  w ≤ 40 (explore2 Y7) で発見・本項 D11 に OBS 登録**。closed form の region 計算で
  一般 w に拡張可能な見込み (q_odd(z) が層核の両端構造に対応。本項 §2.5 の
  境界一致 3 型が世代毎に再現: L-BU13G では t=13 → 2 = g1(1) 核一致・
  t=14 → 0 = g1(2) 主則 first-cell 一致・層 t<14 は R 定数、L-BU14G では
  t=14 → 0 = f0(0) 核一致・t=15 → 2 = f0(1) 核一致 (w ≥ 16 の q_odd(15)=15
  region) — この 3 型境界一致スキームの一般 w 命題化が O10(5) の本命対象)。
- **O11 (例外定数層の一般理論 — K1294/K1299/K1301 O11 継続)**: 層厚
  L(w) = 2⌈w/2⌉ が w = 0..14 全称 + w = 15..18 OBS (dedup)。層の中の子は
  (w, w−1) の層定数を R−1 パリティで読むのみで δ 非依存 — w=3 法則が w=13,14
  でも同一に成立 (§2 の R ≤ 14 cases は w 非依存の mex{0,1}=2 / mex{2,3}=0 機構・
  第 7 世代)。**横断型 (z7/z9/z11/z13: 層内最終行 R = L(w)−1 の C 子が下位面 seam
  直後の主則読み f0(−2m)=0 → C=1) と横断ゼロ型 (z8/z10/z12/z14: 層厚一致の対面)
  の 2 型が厚み 14 でも再現・横断行は常に 2 行 (層内 1 + seam 1)** — 一般 w 帰納は
  (w mod 2) でこの 2 型に分類できる見取り (O9(5) と統合)。
- **O12 (11×11 giant 枝刈り格子)**: T-PD0 (K1286) + K1288 + K1289 + K1290 +
  K1294 + K1299 + K1301 + 本項で、ペア面 z ∈ {0..14} の対角下全域 k ≤ 0 が
  R 例外層込みで O(1) 即値評価可能に (band は δ と R の 2 変数・床は 1 変数)。
  境界側格子の拡張として巨大探索レーンへ記録 (採用判断はオーナー)。
- **O13 (K1287 O1 残部)**: (i) SLB2/SLB3 単一層族・(ii) L/Am frontier 全称化
  は非接触のまま (K1289/K1290/K1294/K1299/K1301 と同一)。

## §6 主張の区別 (過大主張の防止)

- 定理 (universal, §2 手証明): T-PDT13, T-BDT13, T-PDT14, T-BDT14, L-BU13G,
  L-BU14G, C1 (K1301 O9⁗ z13/z14 部分解決の記述), C2 の w ≤ 14 部分
  (sharpened C-PSF′ の w については既刊+本項の集約)。
- corollary (universal だが既刊の言い換え): C2/C3 の既刊分の再表現。
- 有限観測 (OBS): D11 (z15/z16 band/beds/far-row/lowR hist・L-BU15G/L-BU16G・
  dedup sweep z=15..18)・§3 X/Y。
- census 点数 111,961 は定理の実機照合であり全称性の主張ではない。
- 標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は
  全て UNKNOWN のまま。verdict 不消費。

(宣言ノート本文ここまで。実装は publish-then-execute: 本ノートが最先行。
kit → fetch-back → 公式 4 走 → 変異電池 → 成果物出版 → K item → README bullet
→ run log の順に進める。)
