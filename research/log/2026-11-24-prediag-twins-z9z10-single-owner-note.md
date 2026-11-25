# 単一オーナー宣言 K1299: pre-diag 双生児 z9/z10 の全称確定
(T-PDT9/T-BDT9 + T-PDT10/T-BDT10 — K1294 O9″ の z9/z10 部分の取得・sharpened C-PSF′ の w=9,10 実例化・z11/z12 OBS)

## §0 状態と採番 (single-owner protocol)

- 観測 HEAD (着手時): `4377c987d71a51db89ac77085a8f41cdf354fda9` (2026-11-24T15:5xZ・実行開始時観測)。着手時点の最新 K item = K1298 (`74753b66`・parity-graded-grundy レーンが colliding K1294 から再採番)。 intervening commits (Part DP `8c3b77ae`/`7a5ee133` adoption lane・`4f731fb1` log) は全て領域直交・非接触。
- 本宣言 push 直前再取得 HEAD: `4f731fb1969bc95f9c4c97bbc08f03f436d557de` (2026-11-24T16:14:58Z・round-4 commit chain 記録 log)。
- K1299 空き確認: `research/knowledge/items/K1299-prediag-twins-z9-z10.md` 直接 path probe = not found (2026-11-24T16:15Z・本宣言 push 直前に再確認)。コミットログに K1299 宣言 0 件・対抗宣言なし。K1290/K1294 の「次候補」記述は番号取得ではなく未着手領域の列挙である点は K1290/K1294 と同一。
- 領域: K1294 lane が §5 O9″ として登録した T-PDT9/T-BDT9・T-PDT10/T-BDT10 (z9/z10 pre-diag typed 全称) を取得。K1294 O9″ の z9/z10 部分を解決し sharpened C-PSF′ を w=0..10 全称化、z11/z12 (次の観測面) を OBS 登録する。K1286/K1288/K1289/K1290/K1294 の全定理に触れない (内面 k>0・multi-c web は非接触)。K1295 (projective-blocking-kyouen・dfb38f6b)・K1296/K1297 (moment レーン)・K1298 (parity-graded) はいずれも本領域と直交。
- 規約: verdict 不消費・標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は全て UNKNOWN のまま。

## §1 主張 (claims)

座標の規約は K1286/K1288..K1294 と同一: ペア局面 H(R;(m,m+g);z)、対角座標 k := R−2m−g、
δ := R−2m、バンド域 k ≤ 0 (0 ≤ R ≤ 2m+g)。床 (bed) は (m,m) 双 Token:
b_z(j) := H(2m+j;(m,m);z), j ≤ 0。f0 は K1286 出版の対角下バンド 1 次元崩壊関数、
g1 は K1288 出版の偶奇双生児 (T-TWIN: g1(d) = 1 ⊕ f0(d) for d ≠ 1, g1(1) = f0(1) = 2):

- f0(d) = 2 (d=1); [d odd] (d ≤ 0); [d even] (d ≥ 2)
- g1(d) = 2 (d=1); [d even] (d ≤ 0); [d odd] (d ≥ 2)

**定理パッケージ (universal, 量子化: ∀m ≥ 1, ∀g ≥ 1, 全ての有効 cell, 値は m も g も経由しない):**

- **T-PDT9 (z9 band)**: H(R;(m,m+g);9) = 2·[R odd] (R < 10); g1(δ−8) (R ≥ 10)。
- **T-BDT9 (z9 bed)**: b9(j) = 2·[R odd] (R < 10, R = 2m+j); g1(j−8) (R ≥ 10)。
- **T-PDT10 (z10 band)**: H(R;(m,m+g);10) = 2·[R odd] (R < 10); f0(δ−10) (R ≥ 10)。
- **T-BDT10 (z10 bed)**: b10(j) = 2·[R odd] (R < 10); f0(j−10) (R ≥ 10)。
  (層厚 L(9) = L(10) = 2⌈w/2⌉ = 10。z10 の偶数例外 cell (R=0,2,4,6,8) は主則 f0(δ−10)
  と値が一致する (δ even ≤ 8 → δ−10 even ≤ −2 → f0 = 0) ので「R < 10 で 2·[R odd]」
  として統一できる。z9 の偶数 cell (R=0,2,4,6,8) は主則 g1(δ−8) = 1 と衝突するので
  層の上書きとして本物である − K1289 の z3/z4・K1290 の z5/z6・K1294 の z7/z8 と同一の
  役割分担 (奇数平面の層は実質、偶数平面の層は見かけ上主則と一致)。)

**補題 (closed-form から機械照合 w ≤ 30・発現 probe w ≤ 40):**

- **L-BU9G**: v(w,10,t) = 2·[t odd] (t < 10); g1(t−8) (10 ≤ t ≤ w), ∀w ≥ 2
  (単一 Token w を平面 10 に置いた局面 = B-exit 子の値 = plane-9 則のフル形式)。
- **L-BU10G**: v(w,11,t) = 2·[t odd] (t < 10); f0(t−10) (10 ≤ t ≤ w), ∀w ≥ 2。
  (t=10 の 0 = f0(0) は主則核、t=11 の 2 = f0(1) は層核の境界一致 — K1289 L-BU4G・
  K1290 L-BU6G・K1294 L-BU8G と同一構造。)

**系 (corollaries / subsumption):**

- **C1 (K1294 O9″ z9/z10 RESOLVED)**: K1294 D11/Y3–Y5 が OBS として観測し
  D9(h) identity sweep から w=9,10 未証明ゆえ除外していた z9/z10 予測面が
  本項で全称定理化。層厚 10・主則 g1(δ−8) (z9) / f0(δ−10) (z10) が例外層込みで確定。
- **C2 (sharpened C-PSF′ = K1294 O9″ の w=9,10 実例化)**: 統一形式
  **H(R;(m,m+g);w) = 2·[R odd] (R < 2⌈w/2⌉); T_w(δ − 2⌊w/2⌋) (R ≥ 2⌈w/2⌉)**,
  T_w = g1 (w 奇数) / f0 (w 偶数)。この項で w ∈ {9,10} が全称証明され、
  w ∈ {0} (K1286), {1,2} (K1288), {3,4} (K1289), {5,6} (K1290), {7,8} (K1294),
  {9,10} (本項) と代数的に同一 (verify D9(h) が w=0..10 全 11 面で機械照合)。
  w ∈ {11,12} は D11 有限 OBS のみ (dedup sweep では w=14 まで観測拡張)。層厚
  L(w) = 2⌈w/2⌉ の一般 w 帰納は未解決 (§5 O9‴)。
- **C3 (B-exit 均一性の族)**: 単一 Token @ plane z+1 は plane-z 則を継承する:
  L-BU0 (K1286)・L-BU1G/L-BU2G (K1288)・L-BU3G/L-BU4G (K1289)・L-BU5G/L-BU6G
  (K1290)・L-BU7G/L-BU8G (K1294) に続き本項の **L-BU9G/L-BU10G (plane-9 / plane-10)**
  で 11 枝になる (w=11,12 token plane (L-BU11G/L-BU12G 相当) は D11 OBS・全称主張なし)。

**§1.1 K1294 内面との境界 (重複なし)**: K1294 D11/Y3–Y5/Y7/Y8 の z9/z10 band OBS
(band 各 4,500 点・bad 0)・L-BU9G/L-BU10G 発現 probe (w ≤ 40)・dedup z=9..12 は
有限観測として本項が定理化する対象であった。本項の主張は R 例外層値込みの全 cell を
含み、K1294 が open にした「z9/z10 の typed 証明」を定理として確定する。
K1286 T-Z1 k=1 内面・K1287 F2 web の内面 k>0・K1294 の z7/z8 定理には一切触れない
(z7/z8 は z9 の C 子として外部参照 (既刊・全 R 無条件) するのみで再証明しない)。

## §2 手証明 (typed child mex, single R strong induction)

### §2.0 型付き子の分類 (pair @ plane z)

K1294 §2.0 と同一 (engine 定義から直接)。Budget R の局面 (m,m+g)@z
(バンド内 k ≤ 0) の選択肢は 5 型で全て、子は全て budget R−1 である:

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
値 {v(1,z+1,0), v(1,z+1,1)} = {0,2} — closed form・D9(k) 照合)、**C**
(1 ⊕ 床 (m,m)@(z−1), budget R−1, 床座標 j−1)。

well-founded 性: 単一の packet {T-PDT9, T-BDT9, T-PDT10, T-BDT10} 全体で R に
ついての強帰納。全ての子の budget は R−1 であり、面間参照は常に下位 budget
(z9 の C 子は z8 = K1294 既刊で全 R 無条件、z10 の C 子は z9 = packet 内で
budget R−1)。B 子・床 B 子は closed form (帰納外)。基底 R = 0: 選択肢集合は空、
mex ∅ = 0 (4 定理すべての主張値と整合: 層値 2·[0]=0・主則読みも
g1(δ−8)/f0(δ−10) は R=0 cell では層値と同一)。

### §2.1 T-PDT9 (z9 band) の証明

主張値 V(R,δ) := 2·[R odd] (R < 10); g1(δ−8) (R ≥ 10)。

**R = 0**: mex ∅ = 0 = 層値。

**R ∈ {1,...,8} (例外層前半)**: 子は全て budget R−1 ∈ {0..7}:
- fall/compress/corner 子: z9 band/床 層値 at R−1 (< 10) = 2·[(R−1) odd]
  (budget 定数・子の δ_c に依らず)。
- B 子 (m=1): L-BU9G at t = R−1 < 10 → 2·[t odd] → 同一の budget 定数。
- C 子: 1 ⊕ [z8 at (R−1)] — R−1 ∈ {0..7} は z8 層域 (厚み 8) 内 → z8 層値
  2·[(R−1) odd] → C = 1 ⊕ 2·[(R−1) odd]。

選択肢集合: R=1: {0, 1} → mex = **2** ✓; R=2: {2, 3} → **0** ✓; R=3: **2** ✓;
R=4: **0** ✓; R=5: {0,1} → **2** ✓; R=6: {2,3} → **0** ✓; R=7: {0,1} → **2** ✓
(C 子 budget 6: z8 層値 2 → 3); R=8: {2, 3} → **0** ✓ (C 子 budget 7: z8 層値
0 → 1 — z8 層域は R < 8 なので budget 7 は層値、域を跨がない)。

**R = 9 (層域横断 1 列目・K1294 §2.1 R=7 の対)**: 子 budget 8:
- fall/compress/corner 子: z9 層値 at 8 → **0** (2·[8 odd])。
- B 子 (m=1): L-BU9G t=8 < 10 → **0**。
- **C 子: 1 ⊕ [z8 at budget 8 = z8 主則域 (R ≥ 8) を読む層域横断]** —
  f0(δ₂−8), δ₂ = 8−2m (C 子の δ) → δ₂−8 = −2m even ≤ −2 → f0 = 0 → C = **1**
  (δ₂ parity 固定により値は定数 — K1294 §2.1 R=7 が z6 主則 f0(−2m)=0 を読んだ
  構造の z9 版。z8 seam 直後の主則読み)。
- 選択肢集合 = {0, 1} → mex = **2** = 2·[9 odd] ✓。

**R = 10 (主則への継ぎ目)**: 子 budget 9:
- fall/compress/corner: z9 層値 at 9 → **2**。
- B (m=1): L-BU9G t=9 < 10 → **2**。
- C: **1 ⊕ [z8 at budget 9, 主則]**: f0(δ₂−8), δ₂ = 9−2m odd ≤ 7 →
  δ₂−8 odd ≤ −1 → f0 = 1 → C = **0** (層域横断 2 列目)。
- 選択肢集合 = {2, 0} → mex = **1**。主張値: g1(δ−8) at R=10 (δ = 10−2m even ≤ 8):
  δ−8 even ≤ 0 → g1 = 1 ✓。

**R ≥ 11 (主則)**: 子は全て主則読み (budget R−1 ≥ 10):
- fall 子: g1(δ_c−8) at δ_c = δ+1 → **g1(δ−7)**。
- B 子 (m=1): L-BU9G main at t = R−1 = δ+1 ≥ 10 → g1(t−8) = **g1(δ−7)**
  (fall 子と同じ表を再生 — K1288..K1294 の B-exit 再生構造の z9 版)。
- compress 子: g1(δ_c−8) at δ_c = δ−1 → **g1(δ−9)**。
- corner 子 (g=1): 床 T-BDT9 main at j_c = δ−1: g1(j_c−8) = **g1(δ−9)**
  (compress 子と同値)。
- C 子: 1 ⊕ f0(δ₂−8) at δ₂ = δ−1 → **1 ⊕ f0(δ−9)** = g1(δ−9) unless δ = 10
  (δ−9 = 1 のとき C = 1 ⊕ f0(1) = 3)。

場合分け (δ ≡ R (mod 2), δ ≤ g; B 子・corner 子は m=1 すなわち δ = R−2 の行に
のみ出現するが値は fall/compress と同一なので場合分け不要):

| δ (parity, range) | fall/B g1(δ−7) | comp/corner g1(δ−9) | C 1⊕f0(δ−9) | 集合 S | mex | 主張 g1(δ−8) |
|---|---|---|---|---|---|---|
| odd, δ ≤ −1 | g1(even ≤ −8)=1 | g1(even ≤ −10)=1 | 1⊕f0(even ≤ −10)=1⊕0=1 | {1} | 0 | g1(odd ≤ −9)=[even]=0 ✓ |
| δ = 1 | g1(−6)=1 | g1(−8)=1 | 1 | {1} | 0 | g1(−7)=[even]=0 ✓ |
| δ = 3 | g1(−4)=1 | g1(−6)=1 | 1 | {1} | 0 | g1(−5)=[even]=0 ✓ |
| δ = 5 | g1(−2)=1 | g1(−4)=1 | 1 | {1} | 0 | g1(−3)=[even]=0 ✓ |
| δ = 7 | g1(0)=1 | g1(−2)=1 | 1⊕f0(−2)=1 | {1} | 0 | g1(−1)=[even(d odd)]=0 ✓ |
| δ = 9 (核) | g1(2)=0 | g1(0)=1 | 1⊕f0(0)=1 | {0,1} | 2 | g1(1)=2 ✓ |
| δ = 11 | g1(4)=0 | g1(2)=0 | 1⊕f0(2)=1⊕1=0 | {0} | 1 | g1(3)=[odd]=1 ✓ |
| odd, δ ≥ 13 | g1(even ≥ 6)=0 | g1(even ≥ 4)=0 | 1⊕f0(even ≥ 4)=1⊕1=0 | {0} | 1 | g1(odd ≥ 5)=[odd]=1 ✓ |
| even, δ ≤ 0 | g1(odd ≤ −7)=0 | g1(odd ≤ −9)=0 | 1⊕1=0 | {0} | 1 | g1(even ≤ −8)=[even]=1 ✓ |
| δ = 2 | g1(−5)=0 | g1(−7)=0 | 1⊕f0(−7)=1⊕1=0 | {0} | 1 | g1(−6)=1 ✓ |
| δ = 4 | g1(−3)=0 | g1(−5)=0 | 0 | {0} | 1 | g1(−4)=1 ✓ |
| δ = 6 | g1(−1)=0 | g1(−3)=0 | 1⊕f0(−3)=1⊕1=0 | {0} | 1 | g1(−2)=1 ✓ |
| δ = 8 | g1(1)=2 | g1(−1)=0 | 1⊕f0(−1)=1⊕1=0 | {2,0} | 1 | g1(0)=1 ✓ |
| δ = 10 (C 核) | g1(3)=1 | g1(1)=2 | 1⊕f0(1)=3 | {1,2,3} | 0 | g1(2)=0 ✓ |
| even, δ ≥ 12 | g1(odd ≥ 5)=1 | g1(odd ≥ 3)=1 | 1⊕f0(odd ≥ 3)=1⊕0=1 | {1} | 0 | g1(even ≥ 4)=[odd]=0 ✓ |

(この表は K1294 §2.1 z7 表の δ → δ−2 平行移動 ($\delta$-$2$ shift) と核 cell の
再核算化 (核 δ=7→9・C 核 δ=8→10) で閉じる — g1/f0 の parity 構造が平行移動で
不変なため、全 δ 場合で mex = 主張値。■)

### §2.2 T-BDT9 (z9 bed) の証明

主張値 b9(R,j): 2·[R odd] (R < 10); g1(j−8) (R ≥ 10), R = 2m+j, j ≤ 0。

R = 0: mex ∅ = 0 ✓。

**R ∈ {1,...,8} (例外層前半)**: 子 budget R−1 ∈ {0..7}:
- fall 子 (m ≥ 2): pair (m−1,m)@z9 → 層値 2·[(R−1) odd] (budget 定数)。
- B 子 (m = 1): v(1,10,t) at t = R−1 ∈ {0,1} → 0/2 = 2·[t odd]
  (m=1 は R ≤ 2 のみ: j = R−2 ≤ 0)。
- C 子: 1 ⊕ [b8 at (R−1), 床座標 j−1]: z8 床層域 (厚み 8) 内 → 2·[(R−1) odd]。

選択肢集合: R=1: {0,1} → **2** ✓; R=2: {2,3} → **0** ✓; R=3: **2** ✓; R=4: **0** ✓;
R=5: {0,1} → **2** ✓; R=6: {2,3} → **0** ✓; R=7: {0,1} → **2** ✓; R=8: {2,3} →
**0** ✓ (C 子 budget 7 は z8 床層域内)。

**R = 9 (層域横断 1 列目・m ≥ 5, j = 9−2m odd ≤ −1)**: 子 budget 8:
- fall: pair (m−1,m)@z9 層値 at 8 → **0**。
- C: **1 ⊕ b8 at budget 8 = z8 床主則域 (R ≥ 8)**: f0((j−1)−8) = f0(j−9):
  j odd ≤ −1 → j−9 even ≤ −10 → f0 = 0 → C = **1**
  (band 版 §2.1 R=9 と対)。
- 集合 {0, 1} → mex = **2** ✓ (fall 型しかない床で行の子値が層値と C のみ)。

**R = 10 (継ぎ目, m ≥ 5, j = 10−2m even ≤ 0)**: 子 budget 9:
- fall: pair (m−1,m)@z9 層値 at 9 → **2**。
- C: **1 ⊕ b8 at budget 9 (主則) 座標 j−1**: f0(j−9): j even → j−9 odd ≤ −9 →
  f0 = 1 → C = **0** (横断 2 列目)。
- 集合 {2, 0} → mex = **1**。主張 g1(j−8): j even → j−8 even ≤ −8 →
  g1 = [even] = 1 ✓。

**R ≥ 11 (主則)**: 子は主則読み (child budget ≥ 10):
- fall: pair (m−1,m)@z9 main at δ_c = (R−1)−2(m−1) = j+1 → g1(j+1−8) = **g1(j−7)**。
- C: 1 ⊕ b8 main at 座標 j−1: f0(j−9) → **1 ⊕ f0(j−9) = g1(j−9)**
  (j−9 = 1 は j ≤ 0 で不成立・常に g1(j−9))。
- B 子は m = 1 で R ≤ 2 にしか現れない (主則域外)。

| j (parity) | fall g1(j−7) | C g1(j−9) | 集合 | mex | 主張 g1(j−8) |
|---|---|---|---|---|---|
| odd, j ≤ −1 | g1(even ≤ −8)=1 | g1(even ≤ −10)=1 | {1} | 0 | g1(odd ≤ −9)=[even]=0 ✓ |
| even, j ≤ 0 | g1(odd ≤ −7)=0 | g1(odd ≤ −9)=0 | {0} | 1 | g1(even ≤ −8)=[even]=1 ✓ |

■ (bed は compress/corner 子を持たない — 両減算が同じ fall 子に縮退する。
K1294 §2.2 z7 床表の δ → δ−2 平行移動。)

### §2.3 T-PDT10 (z10 band) の証明

主張値 V(R,δ) := 2·[R odd] (R < 10); f0(δ−10) (R ≥ 10)。

R = 0: mex ∅ = 0 = 層値 ✓ (= 主則 f0(δ−10) = f0(−2m−10) = 0 とも一致)。

**R ∈ {1,...,9} (例外層)**: 子 budget R−1 ∈ {0..8} — **全て z10 層域 (< 10) 内 かつ
z9 層域 (< 10) 内** (z9/z10 の層厚が一致するため C 子は域を跨がない —
K1294 §2.3 z8 の (8,8) 横断ゼロ型の (10,10) 版・層内部で閉じる):
- fall/compress/corner: z10 band/床 層値 at R−1 → 2·[(R−1) odd]。
- B (m=1): L-BU10G at t = R−1 < 10 → 2·[t odd] → 同一。
- C: 1 ⊕ [z9 at (R−1)]: z9 層値 (packet T-PDT9, R−1 < 10) 2·[(R−1) odd]。

集合: R=1: {0,1} → **2** ✓; R=2: {2,3} → **0** (= 主則 f0(δ−10): δ even ≤ 0
→ δ−10 even ≤ −10 → 0 と一致 — 偶数 cell は層値と主則が同一); R=3: **2** ✓;
R=4: **0** (主則: δ even ≤ 2 → δ−10 ≤ −8 → 0 ✓); R=5: **2** ✓; R=6: **0**
(主則: δ ≤ 4 → δ−10 ≤ −6 → 0 ✓); R=7: **2** ✓; R=8: **0** (主則: δ ≤ 6 →
δ−10 ≤ −4 → 0 ✓); R=9: {0,1} → **2** ✓ (C 子 budget 8 は z9 層域内・横断ゼロの
帰結: 層域横断 (z9 型) とは逆に本 packet の偶数面は全子が層定数)。

**R = 10 (継ぎ目)**: 子 budget 9:
- fall/compress/corner: z10 層値 at 9 → **2**。
- B: L-BU10G t=9 < 10 → **2**。
- C: 1 ⊕ [z9 at budget 9, 層値 2] → C = **3** (z9 層域は R < 10 なので
  budget 9 はまだ層 — K1290 z6 seam (C 子 budget 5 = z5 層値 2 → 3)・
  K1294 z8 seam (C 子 budget 7 = z7 層値 2 → 3) と同一の役割)。
- 集合 {2,3} → mex = **0**。主張: f0(δ−10) at δ even ≤ 8 → δ−10 even ≤ −2 →
  0 ✓。

**R ≥ 11 (主則)**: 子は全て主則読み (budget R−1 ≥ 10):
- fall: f0(δ_c−10) at δ_c = δ+1 → **f0(δ−9)**。
- B (m=1): L-BU10G main at t = R−1 = δ+1 ≥ 10: f0(t−10) = **f0(δ−9)**
  (fall 再生)。
- compress: **f0(δ−11)**; corner (g=1): T-BDT10 main at j_c = δ−1 →
  **f0(δ−11)** (compress 子と同値)。
- C: 1 ⊕ g1(δ₂−8) at δ₂ = δ−1 → **1 ⊕ g1(δ−9)** = f0(δ−9) for δ ≠ 10
  (1 ⊕ g1(x) = f0(x) except x=1; δ=10 のとき 3)。

(K1294 §2.3 z8 表の δ → δ−2 平行移動。核 cell: 核 δ=9→11・C 核 δ=8→10・
comp 核 δ=10→12。)

| δ (parity, range) | fall/B f0(δ−9) | comp/corner f0(δ−11) | C 1⊕g1(δ−9) | 集合 S | mex | 主張 f0(δ−10) |
|---|---|---|---|---|---|---|
| even, δ ≤ 0 | f0(odd ≤ −9)=1 | f0(odd ≤ −11)=1 | 1⊕g1(odd ≤ −9)=1⊕0=1 | {1} | 0 | f0(even ≤ −10)=0 ✓ |
| δ = 2 | f0(−7)=1 | f0(−9)=1 | 1 | {1} | 0 | f0(−8)=0 ✓ |
| δ = 4 | f0(−5)=1 | f0(−7)=1 | 1 | {1} | 0 | f0(−6)=0 ✓ |
| δ = 6 | f0(−3)=1 | f0(−5)=1 | 1 | {1} | 0 | f0(−4)=0 ✓ |
| δ = 8 | f0(−1)=1 | f0(−3)=1 | 1 | {1} | 0 | f0(−2)=0 ✓ |
| δ = 10 (C 核) | f0(1)=2 | f0(−1)=1 | 1⊕g1(1)=3 | {2,1,3} | 0 | f0(0)=0 ✓ |
| δ = 12 (comp 核) | f0(3)=0 | f0(1)=2 | 1⊕g1(3)=1⊕1=0 | {0,2} | 1 | f0(2)=1 ✓ |
| even, δ ≥ 14 | f0(odd ≥ 5)=0 | f0(odd ≥ 3)=0 | 1⊕g1(odd ≥ 5)=1⊕1=0 | {0} | 1 | f0(even ≥ 4)=1 ✓ |
| odd, δ ≤ 9 | f0(even ≤ 0)=0 | f0(even ≤ −2)=0 | 1⊕g1(even ≤ 0)=1⊕1=0 | {0} | 1 | f0(odd ≤ −1)=1 ✓ |
| δ = 11 (核) | f0(2)=1 | f0(0)=0 | 1⊕g1(2)=1⊕0=1 | {1,0} | 2 | f0(1)=2 ✓ |
| odd, δ ≥ 13 | f0(even ≥ 4)=1 | f0(even ≥ 2)=1 | 1⊕g1(even ≥ 4)=1⊕0=1 | {1} | 0 | f0(odd ≥ 3)=0 ✓ |

全 δ 場合で mex = 主張値。■

### §2.4 T-BDT10 (z10 bed) の証明

主張 b10(R,j): 2·[R odd] (R < 10); f0(j−10) (R ≥ 10)。

R = 0: 0 ✓ (= 層値 = 主則 f0(−2m−10)=0)。
R = 1 (m=1, j=−1): B: v(1,11,0)=0; C: 1⊕[b9 at R−1=0 = 0]=1 → {0,1} →
mex **2** ✓。
R = 2: (m=1,j=0): B: v(1,11,1)=2; C: 1⊕[b9 at 1: 層値 2]=3 → {2,3} →
**0** = 層値 = 主則 f0(j−10)=f0(−10)=0 ✓。(m=2,j=−2): fall: pair (1,2)@z10 層値
at 1: 2; C: 1⊕[b9 at 1 (m=2, j−1=−3): 層値 2]=3 → {2,3} → 0 ✓。
R = 3 (m ≥ 2): fall: pair (m−1,m)@z10 層値 at 2: 0; C: 1⊕[b9 at 2: 0]=1 →
{0,1} → **2** ✓。R = 4: fall at 3: 2; C: 1⊕[b9 at 3: 2]=3 → {2,3} → **0** ✓
(主則 f0(j−10): j even → j−10 even ≤ −10 → 0 と一致)。R = 5: fall at 4: 0;
C: 1 → {0,1} → **2** ✓。R = 6: fall at 5: 2; C: 3 → {2,3} → **0** ✓
(主則: j even → j−10 ≤ −6 → 0 ✓)。R = 7: fall at 6: 0; C: 1 → **2** ✓。
R = 8: fall at 7: 2; C: 3 → **0** ✓ (主則: j −10 ≤ −4 → 0 ✓)。R = 9:
fall at 8: 0; C: 1⊕[b9 at 8: 層値 0]=1 → {0,1} → **2** ✓ (z9 床層域は
R < 10 なので budget 8 は層値 — 横断ゼロ)。

**R = 10 (継ぎ目, m ≥ 5, j = 10−2m even ≤ 0)**: 子 budget 9:
- fall: pair (m−1,m)@z10 層値 at 9 → 2。
- C: 1 ⊕ b9 at budget 9 (z9 床層値 at 9: 2) → 3。
- 集合 {2,3} → mex **0** = 主則 f0(j−10): j even → j−10 even ≤ −10 → 0 ✓。

**R = 11 (m ≥ 5, j odd)**: 子 budget 10 (両面とも主則域):
- fall: pair (m−1,m)@z10 main at δ_c = j+1 → f0(j+1−10) = **f0(j−9)**:
  j odd → j−9 even ≤ −4 → 0。
- C: 1 ⊕ b9 at budget 10 (main) 座標 j−1: g1((j−1)−8) = g1(j−9): j odd →
  j−9 even ≤ −8 → g1 = 1 → C = **0**。
- 集合 {0} → mex **1** = 主則 f0(j−10): j odd → j−10 odd ≤ −9 → 1 ✓。

**R ≥ 12 (主則)**: 子は主則読み:
- fall: **f0(j−9)**; C: 1 ⊕ g1(j−9) = **f0(j−9)** for j ≠ 10 (j ≤ 0 常に)。
- mex({f0(j−9)}) — 単一値 v なら mex = 0 (v ≠ 0), 1 (v = 0):
  - j odd: f0(even ≤ −10)=0 → mex **1** = 主張 f0(odd ≤ −9)=1 ✓。
  - j even: f0(odd ≤ −9)=1 → mex **0** = 主張 f0(even ≤ −10)=0 ✓。■

### §2.5 L-BU9G / L-BU10G の閉形式からの導出

K0832 closed form v(x,z,R) から直接読む。token plane 10, w ≥ 2:
- w ≥ 11: region 1 ≤ 10 ≤ w−1, m = q_odd(10) = 9: t ≤ 9: 2·[t odd] (層 t < 10
  と一致、t = 9 の 2 = g1(1) は層核と主則核の境界値の一致 — K1289 L-BU4G・
  K1290 L-BU6G・K1294 L-BU8G と同一); 9 < t < w+10 (t ≤ w で常に):
  (t+10)%2 = t%2: t 偶 → 0 = g1(t−8) (even ≥ 2 → [odd]=0), t 奇 → 1 =
  g1(t−8) (odd ≥ 3 → [odd]=1)。t = 8,9 ≤ m 層内。
- w = 10: region z = x: t 奇 ≤ 19: 2; t 偶 ≤ 9: 0 (= 層値); t=10: 偶 > 9 →
  x%2 = 0 = g1(2) = 0 (主則核 cell の一致)。
- w ∈ {2,...,9}: region z ≥ x+1: m = q_odd(w) ≤ 9: t ≤ m: 2·[t odd] (層内);
  t > m, t ≤ w: w%2 — w 偶 {2,4,6,8} で t = w が該当するのみで値 0 = 層値
  2·[w odd] = 0 と一致、w 奇は m = w で不使用。全域層値 (t ≤ w ≤ 9 < 10)。
token plane 11, w ≥ 2:
- w ≥ 12: m = q_odd(11) = 11: t ≤ 11: 2·[t odd] (t < 10 層; t=10: 0 = f0(0) =
  主則核の一致; t=11: 2 = f0(1) = 核の一致); 11 < t ≤ w: (t+11)%2 = 1−t%2:
  t 偶 → 1 = f0(t−10) (even ≥ 2 → [even]=1), t 奇 → 0 = f0(t−10)
  (odd ≥ 3 → 0)。
- w = 11: region z = x: t 奇 ≤ 21: 2 (t=11: 2 = f0(1) ✓); t 偶 ≤ 10: 0
  (t=10: 0 = f0(0) ✓); t ≤ 9 は層値と一致。
- w ∈ {2,...,10}: region z ≥ x+1: m = q_odd(w) ≤ 9: t ≤ m: 2·[t odd];
  t > m, t ≤ w ≤ 10: w%2 (w 偶: t=w のみ 0 = 層値 ✓; w=10: m=9, t=10:
  w%2 = 0 = f0(0) = 0 ✓; w 奇は m = w で不使用)。
全 twist は機体 D9(a)/(b) が closed form × canonical engine × 主張表の三方で
w ≤ 30 照合 (各 493 点)・Y7 が w ≤ 40 発現 probe で補強。■

### §2.6 well-founded 性 (まとめ)

packet {T-PDT9, T-BDT9, T-PDT10, T-BDT10} の証明は単一の R 強帰納:
全子は budget R−1 (engine の子定義)。面間参照: z9 の C 子 = z8 (K1294, 全 R
無条件); z10 の C 子 = z9 (packet, budget R−1); 床 C 子 = plane−1 床
(z9 床の C 子 = b8 = K1294 既刊; z10 床の C 子 = b9 = packet T-BDT9,
budget R−1)。B 子は K0832 closed form (L-BU9G/L-BU10G + w=1 edge {0,2}) で
帰納外。帰納は R のみで整礎 (m, g に依らない子値表)。各 R での子値の列挙は
§2.1–§2.4 の場合表 (R ≤ 10 は層定数読みの列挙、R ≥ 11 は δ parity の場合表)
で全ての (m, g, k) を尽くす。層厚 10 世代の新しい構造は §2.1/§2.2 の
「C 子 budget 8 (R=9 ・z8 seam 直後) と budget 9 (seam R=10) が下位面 (z8,
層厚 8) の主則域を読む」層域横断が **2 行に広がった** こと (値は δ₂ parity
固定により定数 0/1 に落ちる・K1294 z7 の R=7/R=8 と同型の平行移動) と、
§2.3/§2.4 の「z10 の層域横断がゼロ (z9 と層厚が一致 (10,10))」の対である。

### §2.7 反例検査の誠実な記述

- 例外層 R ∈ {0,...,9} の値 2·[R odd] は宣言前探索 (§3 X1–X4) で (R,δ) 平面
  で mixed cell 0 として先に特定済み (K1289 の「slope trap」教訓を適用)。
- m 依存性・g 依存性は主張域内で一度も観測されていない (§3 Y1/Y2 広域)。
  主張は typed 証明による全称主張であり、census は照合である。

## §3 宣言前探索 (pre-declaration; explore_k1299.py / explore2_k1299.py 出力)

- X1/X3 (z9/z10 band m≤12 g≤25 k≥−60, (R,δ) 表): mixed (R,δ) cell それぞれ
  cells 468 中 0/0 (X2/X4 beds は 168 cell 中 0/0)。低 R 行 (R=0..9) が定数
  0/2/0/2/0/2/0/2/0/2 (層厚 10 の直接観測)。R=10 seam 行 (z9 は全 1 =
  g1(even ≤ 0)、z10 は全 0 = f0(even ≤ −2))。R≥11 行が g1(δ−8) / f0(δ−10)
  に一致 (核 cell z9 δ=9 → 2・z10 δ=11 → 2 を含む)。
- X2/X4 (beds m≤12 j∈[−30..0]): 同一の R 層構造・mixed 0/0。
- X5/X6: L-BU9G/L-BU10G 発現 census (w ≤ 30, t ≤ w; engine vs closed form vs
  plane-9/10 法則): bad 0/0 (1,972 checks)。w=1 edge: v(1,10,{0,1})={0,2},
  v(1,11,{0,1})={0,2}。
- X7: sharpened C-PSF′ probe (z=0..12, m≤10 g≤20 k≥−50 の dedup (R,δ) 320
  cell × 13 面): bad 全 0。
- X8: typed 子 self-check (宣言前): 子を申立テーブル (z9/z10 申立 + K1294
  z7/z8 既刊) + closed form からのみ構成した mex が申立値・engine と一致するかを
  slices 3,878 点・beds 228 点で確認: bad 0/0 (手証明 §2 構文の宣言前検証)。
- Y1/Y2: z9/z10 band+beds の wide census (D1–D4 と同一 box): 8,928/360 × 2
  bad 0。
- Y3/Y4/Y5: z11/z12 OBS (band 4,500 × 2, beds 120 × 2, far-row m=12 216 × 2,
  low-R (R<12) hist {0:402,2:392} × 2 cells 794): cpsf 予測 vs engine bad 全 0
  (有限観測・全称主張なし)。
- Y6: ordered vs canonical engine 交差 (z=9..12, 各 464 cells): mismatch 全 0。
- Y7: L-BU9G/L-BU10G (w ≤ 40) bad 0 + 発現 **L-BU11G** (v(w,12,t) = plane-11
  law: 2·[t odd] (t<12) / g1(t−10))・**L-BU12G** 発現 (v(w,13,t): 2·[t odd]
  (t<12) / f0(t−12)) を w ≤ 40 probe: bad 0 (z=12,13 token plane は OBS)。
- Y8: T-TWIN identity d∈[−260..260] bad 0; z=0..14 dedup (R,δ) sweep:
  全 15 面 mixed 0・cpsf bad 0 (**C-PSF′ が plane 14 まで観測拡張**・K1294
  Y8 の z≤12 から 2 面拡張)。

## §4 機体宣言 (machine declaration, publish-then-execute)

`verify_k1299.py` (sha256 publish 時に kit で宣言 =
`0fa5355917788ce8b35fdafaa381657e960783f579a758f5b00d8dc5b734cd03`・engine
pin `bd5f22e415a78368c9b798296bc84948d5637decbf3c21a92404d45fb12e3a92`
startup gate 内蔵・embed は K1138/K1282..K1294 と同一 bytes)。バッテリ:

| # | 内容 | 期待 count |
|---|---|---|
| D1 | z9 band census (m≤14, g≤25, k∈[max(−30,−2m−g),0]) | 8,928 |
| D2 | z9 beds census (m≤18, j∈[−36..0]) | 360 |
| D3 | z10 band census (D1 box) | 8,928 |
| D4 | z10 beds census (D2 box) | 360 |
| D5 | typed z9 slices (m≤10, g≤14, k≥−14): typed mex == claim == engine | 1,939 |
| D6 | typed z9 beds (m≤10, j≥−16) | 114 |
| D7 | typed z10 slices (D5 box) | 1,939 |
| D8 | typed z10 beds (D6 box) | 114 |
| D9 | (a) L-BU9G 493 + (b) L-BU10G 493 + (c) K1294 anchors T-PDT7/T-BDT7/T-PDT8/T-BDT8 再照合 4,690 + (d) K1290 anchors T-PDT5/T-BDT5/T-PDT6/T-BDT6 再照合 4,690 + (e) K1289 anchors T-PDT3/T-BDT3/T-PDT4/T-BDT4 再照合 4,690 + (f) K1288 anchors T-PDT1/T-BDT1/T-PDT2/T-BDT2 再照合 4,690 + (g) K1286 anchors T-PD0/T-B0 再照合 2,345 + (h) sharpened C-PSF′ identity sweep w=0..10 (pair box + bed box) 25,795 + (i) T-TWIN algebra d∈[−100..100] 201 + (j) closed form vs both engines (x≤16, z∈2..11, R∈x+1..x+4) 1,200 + (k) B-exit w=1 edge values (v(1,10,t)/v(1,11,t), t≤1) 4 | 49,291 |
| D10 | cross-engine canonical vs ordered (z9/z10 pair m≤8, g≤10, k≥−8 + beds m≤8 j≥−8) | 1,516 |
| D11 | OBS: z11/z12 band (m≤10,g≤20,k≥−50) 4,500×2 + beds (m≤10,j≥−24) 120×2 + far-row m=12 216×2 + low-R (R<12) hist probes 794×2 + L-BU11G/L-BU12G plane-token sweep (z=12,13, w≤30) 493×2 + dedup (R,δ) sweep z=0..14 (320 × 15) 4,800 | 17,046 |

**総計 90,535 比較点・期待 overall_bad = 0** (宣言前 predry 4 走で
counts [8928,360,8928,360,1939,114,1939,114,49291,1516,17046]・
bad 全 0・stdout byte-identical sha256
`e9b3784a3323b1e9cbf4a48bb0b4f6c7df979aa909e25c4c5b23526fea515185`
を確認済み)。

変異電池 (公式 run の前に期待値を宣言):
- `--tamper-engine`: rc=2・mutated sha `0ea47a80…` ≠ pin (K1282–K1294 と同一変異)。
- `--tamper=z9s`: rc=1, D1 bad 8,928。`--tamper=z9b`: rc=1, D2 bad 360。
- `--tamper=z10s`: rc=1, D3 bad 8,928。`--tamper=z10b`: rc=1, D4 bad 360。
- 他バッテリ (D5–D11) は census クレームの flip の影響を受けない
  (typed 側は flip されないので D5–D8 の 3-way 照合は主張値のまま engine と
  一致する; 対角の影響は D1–D4 の bad のみ)。

公式 4 走: 同一 cwd (PYTHONHASHSEED random/1) × 2 + 隔離 tree (env -i,
PYTHONHASHSEED 99/7) × 2、stdout byte-identical が要求 (fetch-back bytes から
走行)。

## §5 open 登録 (有限観測・予想と次課題; 全称主張なし)

- **O9‴ (C-PSF′ の w 帰納 — K1294 O9″ update)**: 全称は w ∈ {0..10} まで
  (本項で +2)。**Y8 dedup sweep で w=11..14 が 320 cell × 4 面で mixed 0・
  cpsf bad 0・X7/Y3–Y5 band/bed/far/lowR OBS が w=11,12 を直接支持**
  (K1294 の z≤12 dedup から +2)。次の単一オーナー候補は
  T-PDT11/T-BDT11・T-PDT12/T-BDT12 (z11/z12 typed・§2 と同一構文: C 子は
  本項 z9/z10 定理 (全 R・例外層込み) を参照。z11/z12 の層厚は
  L(11) = L(12) = 2⌈11/2⌉ = 12。層域横断は z11 では C 子 budget 10,11 (R=11
  層内 + seam R=12) の 2 行が z10 主則域 (R ≥ 10) を読む・z12 では横断ゼロ
  ((12,12)・z10 型)。層核の mex{0,1}=2/mex{2,3}=0 機構は w 非依存と root 交代
  なし。完了で sharpened C-PSF′ が w=12 まで全称化)。
- **O10‴ (L-BUzG 族の全称形 — K1294 O10″ update)**: 11 枝 (z+1 = 1..11) まで
  全称。**L-BU11G/L-BU12G (token plane 12/13 = plane-11/12 則: 2·[t odd]
  (t<12) / g1(t−10) (z=12), f0(t−12) (z=13)) を w ≤ 30 (verify)・w ≤ 40
  (explore2 Y7) で発見・本項 D11 に OBS 登録**。closed form の region 計算で
  一般 w に拡張可能な見込み (q_odd(z) が層核の両端構造に対応。本項 §2.5 の
  境界一致 3 型が世代毎に再現: t = z−2 で 2 = T_w(1) 核一致・t = z−1 で
  0 = T_{w+1}(0) 核一致・t = z−3 で 2 = 層核のスキームが O10‴ の正式命題化対象)。
- **O11 (例外定数層の一般理論 — K1294 O11 継続)**: 層厚 L(w) = 2⌈w/2⌉ が
  w = 0..10 全称 + w = 11..14 OBS (dedup)。層の中の子は (w, w−1) の層定数を
  R−1 パリティで読むのみで δ 非依存 — w=3 法則が w=9,10 でも同一に成立
  (§2 の R ≤ 10 cases は w 非依存の mex{0,1}=2 / mex{2,3}=0 機構・第 5 世代)。
  **横断型 (z7/z9: 層内最終行 R = L(w)−1 の C 子が下位面 seam 直後の主則読み
  f0(−2m)=0 → C=1) と横断ゼロ型 (z8/z10: 層厚一致の対面) の 2 型が厚み 10 でも
  再現・横断行は常に 2 行 (層内 1 + seam 1)** — 一般 w 帰納は (w mod 2) で
  この 2 型に分類できる見取り (O9‴ と統合)。
- **O12 (11×11 giant 枝刈り格子)**: T-PD0 (K1286) + K1288 + K1289 + K1290 +
  K1294 + 本項で、ペア面 z ∈ {0..10} の対角下全域 k ≤ 0 が R 例外層込みで
  O(1) 即値評価可能に (band は δ と R の 2 変数・床は 1 変数)。境界側格子の
  拡張として巨大探索レーンへ記録 (採用判断はオーナー)。
- **O13 (K1287 O1 残部)**: (i) SLB2/SLB3 単一層族・(ii) L/Am frontier 全称化
  は非接触のまま (K1289 §5 O12/K1290 §5 O13/K1294 §5 O13 と同一)。

## §6 主張の区別 (過大主張の防止)

- 定理 (universal, §2 手証明): T-PDT9, T-BDT9, T-PDT10, T-BDT10, L-BU9G,
  L-BU10G, C1 (K1294 O9″ z9/z10 部分解決の記述), C2 の w ≤ 10 部分
  (sharpened C-PSF′ の w については既刊+本項の集約)。
- corollary (universal だが既刊の言い換え): C2/C3 の既刊分の再表現。
- 有限観測 (OBS): D11 (z11/z12 band/beds/far-row/lowR hist・L-BU11G/L-BU12G・
  dedup sweep z=11..14)・§3 X/Y。
- census 点数 90,535 は定理の実機照合であり全称性の主張ではない。
- 標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は
  全て UNKNOWN のまま。verdict 不消費。

(宣言ノート本文ここまで。実装は publish-then-execute: 本ノートが最先行。
kit → fetch-back → 公式 4 走 → 変異電池 → 成果物出版 → K item → README bullet
→ run log の順に進める。)
