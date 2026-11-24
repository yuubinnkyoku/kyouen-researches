# 単一オーナー宣言 K1301: pre-diag 双生児 z11/z12 の全称確定
(T-PDT11/T-BDT11 + T-PDT12/T-BDT12 — K1299 O9‴ の z11/z12 部分の取得・sharpened C-PSF′ の w=11,12 実例化・z13/z14 OBS)

## §0 状態と採番 (single-owner protocol)

- 観測 HEAD (着手時): `907327886947648c48d18819a32314a2891c7f21` (2026-11-24T17:03:15Z・Part DQ kit wave C・batch-33 (class 34908) 宣言レーン)。着手時点の最新 K item = **K1300** (`a20b5e258be423f237736185fa683757aee74e2f`・s-parameter-kyouen レーン・2026-11-24T16:40:53Z)。intervening commits (Part DQ 宣言 `c8388b71`/kit waves `dfdae79e`/`f57f406f`/`90732788`・`1f7d26f6` parity characterization・`fb88a6af`/`d0557d48` s-parameter 追加) は全て領域直交・非接触。
- K1300 は s-parameter-kyouen レーンが取得済み (`research/knowledge/items/K1300-s-parameter-kyouen.md`・direct path probe で実在確認)。よって本 package は **K1301** を使用。K1301 空き確認: search_commits "K1301" = 0 件・最新 25 items-touching commits に K1301 なし・**push 直前に再確認** (§0 末尾)。
- 領域: K1299 が §5 O9‴ として登録した T-PDT11/T-BDT11・T-PDT12/T-BDT12 (z11/z12 pre-diag typed 全称) を取得。K1299 O9‴ の z11/z12 部分を解決し sharpened C-PSF′ を w=0..12 全称化、z13/z14 (次の観測面) を OBS 登録する。K1286/K1288/K1289/K1290/K1294/K1299 の全定理に触れない (内面 k>0・multi-c web は非接触)。K1295/K1296/K1297 (projective-blocking/moment)・K1298 (parity-graded)・K1299・K1300 (s-parameter) はいずれも本領域と直交。
- 規約: verdict 不消費・標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は全て UNKNOWN のまま。

## §1 主張 (claims)

座標の規約は K1286/K1288..K1299 と同一: ペア局面 H(R;(m,m+g);z)、対角座標 k := R−2m−g、
δ := R−2m、バンド域 k ≤ 0 (0 ≤ R ≤ 2m+g)。床 (bed) は (m,m) 双 Token:
b_z(j) := H(2m+j;(m,m);z), j ≤ 0。f0 は K1286 出版の対角下バンド 1 次元崩壊関数、
g1 は K1288 出版の偶奇双生児 (T-TWIN: g1(d) = 1 ⊕ f0(d) for d ≠ 1, g1(1) = f0(1) = 2):

- f0(d) = 2 (d=1); [d odd] (d ≤ 0); [d even] (d ≥ 2)
- g1(d) = 2 (d=1); [d even] (d ≤ 0); [d odd] (d ≥ 2)

**定理パッケージ (universal, 量子化: ∀m ≥ 1, ∀g ≥ 1, 全ての有効 cell, 値は m も g も経由しない):**

- **T-PDT11 (z11 band)**: H(R;(m,m+g);11) = 2·[R odd] (R < 12); g1(δ−10) (R ≥ 12)。
- **T-BDT11 (z11 bed)**: b11(j) = 2·[R odd] (R < 12, R = 2m+j); g1(j−10) (R ≥ 12)。
- **T-PDT12 (z12 band)**: H(R;(m,m+g);12) = 2·[R odd] (R < 12); f0(δ−12) (R ≥ 12)。
- **T-BDT12 (z12 bed)**: b12(j) = 2·[R odd] (R < 12); f0(j−12) (R ≥ 12)。
  (層厚 L(11) = L(12) = 2⌈w/2⌉ = 12。z12 の偶数例外 cell (R=0,2,...,10) は主則 f0(δ−12)
  と値が一致する (δ even ≤ 10 → δ−12 even ≤ −2 → f0 = 0) ので「R < 12 で 2·[R odd]」
  として統一できる。z11 の偶数 cell は主則 g1(δ−10) = 1 (δ even ≤ 8 → δ−10 even ≤ −2 は
  g1 = 1) と衝突するので層の上書きとして本物である − K1289 z3/z4・K1290 z5/z6・
  K1294 z7/z8・K1299 z9/z10 と同一の役割分担 (奇数平面の層は実質・偶数平面の層は
  見かけ上主則と一致)。)

**補題 (closed-form から機械照合 w ≤ 30・発現 probe w ≤ 40):**

- **L-BU11G**: v(w,12,t) = 2·[t odd] (t < 12); g1(t−10) (12 ≤ t ≤ w), ∀w ≥ 2
  (単一 Token w を平面 12 に置いた局面 = B-exit 子の値 = plane-11 則のフル形式)。
- **L-BU12G**: v(w,13,t) = 2·[t odd] (t < 12); f0(t−12) (12 ≤ t ≤ w), ∀w ≥ 2。
  (t=12 の 0 = f0(0) は主則核、t=13 の 2 = f0(1) は核の境界一致 (w ≥ 14 の q_odd(13)=13
  region) — K1289 L-BU4G・K1290 L-BU6G・K1294 L-BU8G・K1299 L-BU10G と同一構造。)

**系 (corollaries / subsumption):**

- **C1 (K1299 O9‴ z11/z12 RESOLVED)**: K1299 D11/Y3–Y5 が OBS として観測し
  D9(i) identity sweep から w=11,12 未証明ゆえ除外していた z11/z12 予測面が
  本項で全称定理化。K1299 O9‴ が予告した構造 (z11 は層域横断 2 行 = C 子 budget
  10,11 (層内最終行 R=11 + seam R=12) が z10 主則域 (R ≥ 10) を読む・z12 は横断ゼロ
  ((12,12) 層厚一致)) がそのまま成立した。
- **C2 (sharpened C-PSF′ = K1299 O9‴ の w=11,12 実例化)**: 統一形式
  **H(R;(m,m+g);w) = 2·[R odd] (R < 2⌈w/2⌉); T_w(δ − 2⌊w/2⌋) (R ≥ 2⌈w/2⌉)**,
  T_w = g1 (w 奇数) / f0 (w 偶数)。この項で w ∈ {11,12} が全称証明され、
  w ∈ {0} (K1286), {1,2} (K1288), {3,4} (K1289), {5,6} (K1290), {7,8} (K1294),
  {9,10} (K1299), {11,12} (本項) と代数的に同一 (verify D9(i) が w=0..12 全 13 面で
  機械照合)。w ∈ {13,14} は D11 有限 OBS のみ (dedup sweep では w=16 まで観測拡張)。層厚
  L(w) = 2⌈w/2⌉ の一般 w 帰納は未解決 (§5 O9⁗)。
- **C3 (B-exit 均一性の族)**: 単一 Token @ plane z+1 は plane-z 則を継承する:
  L-BU0 (K1286)・L-BU1G/L-BU2G (K1288)・L-BU3G/L-BU4G (K1289)・L-BU5G/L-BU6G
  (K1290)・L-BU7G/L-BU8G (K1294)・L-BU9G/L-BU10G (K1299) に続き本項の
  **L-BU11G/L-BU12G (plane-11 / plane-12)** で **13 枝**になる (w=13,14 token plane
  (L-BU13G/L-BU14G 相当) は D11 OBS・全称主張なし)。

**§1.1 K1299 内面との境界 (重複なし)**: K1299 D11/Y3–Y5/Y7/Y8 の z11/z12 band OBS
(band 各 4,500 点・bad 0)・L-BU11G/L-BU12G 発現 probe (w ≤ 40)・dedup z=9..14 は
有限観測として本項が定理化する対象であった。本項の主張は R 例外層値込みの全 cell を
含み、K1299 が open にした「z11/z12 の typed 証明」を定理として確定する。
K1299 の z9/z10 定理には一切触れない (z9/z10 は z11 の C 子として外部参照
(既刊・全 R 無条件) するのみで再証明しない)。本項の typed 子 mex 構文は
K1288–K1299 の packet 構文の第 6 世代である点のみ既刊構文と同一。

## §2 手証明 (typed child mex, single R strong induction)

### §2.0 型付き子の分類 (pair @ plane z)

K1294 §2.0 / K1299 §2.0 と同一 (engine 定義から直接)。Budget R の局面 (m,m+g)@z
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
値 {v(1,z+1,0), v(1,z+1,1)} = {0,2} — closed form・D9(l) 照合)、**C**
(1 ⊕ 床 (m,m)@(z−1), budget R−1, 床座標 j−1)。

well-founded 性: 単一の packet {T-PDT11, T-BDT11, T-PDT12, T-BDT12} 全体で R に
ついての強帰納。全ての子の budget は R−1 であり、面間参照は常に下位 budget
(z11 の C 子は z10 = K1299 既刊で全 R 無条件、z12 の C 子は z11 = packet 内で
budget R−1)。B 子・床 B 子は closed form (帰納外)。基底 R = 0: 選択肢集合は空、
mex ∅ = 0。主張値は R=0 cell では層値 2·[0] = 0 と整合する
(z12 は主則 f0(δ−12) = f0(−2m−12) = 0 とも一致)。

### §2.1 T-PDT11 (z11 band) の証明

主張値 V(R,δ) := 2·[R odd] (R < 12); g1(δ−10) (R ≥ 12)。

**R = 0**: mex ∅ = 0 = 層値。

**R ∈ {1,...,10} (例外層前半)**: 子は全て budget R−1 ∈ {0..9}:
- fall/compress/corner 子: z11 band/床 層値 at R−1 < 12 = 2·[(R−1) odd]
  (budget 定数・子の δ_c に依らず)。
- B 子 (m=1): L-BU11G at t = R−1 < 12 → 2·[t odd] → 同一の budget 定数。
- C 子: 1 ⊕ [z10 at (R−1)] — R−1 ∈ {0..9} は z10 層域 (厚み 10) 内 → z10 層値
  2·[(R−1) odd] → C = 1 ⊕ 2·[(R−1) odd]。

選択肢集合: R=1: {0, 1} → mex = **2** ✓; R=2: {2, 3} → **0** ✓; R=3: **2** ✓;
R=4: **0** ✓; R=5: {0,1} → **2** ✓; R=6: {2,3} → **0** ✓; R=7: **2** ✓;
R=8: **0** ✓; R=9: {0,1} → **2** ✓; R=10: {2,3} → **0** ✓ (C 子 budget 9 は
z10 層域 (R<10) 内 — 域を跨がない)。

**R = 11 (層域横断 1 列目・K1299 §2.1 R=9 の対)**: 子 budget 10:
- fall/compress/corner 子: z11 層値 at 10 → **0** (2·[10 odd])。
- B 子 (m=1): L-BU11G t=10 < 12 → **0**。
- **C 子: 1 ⊕ [z10 at budget 10 = z10 主則域 (R ≥ 10) を読む層域横断]** —
  f0(δ₂−10), δ₂ = 10−2m (C 子の δ) → δ₂−10 = −2m even ≤ −2 → f0 = 0 → C = **1**
  (δ₂ parity 固定により値は定数 — K1299 §2.1 R=9 が z8 主則 f0(δ₂−8) を読んだ
  構造の δ-2 平行移動。z10 seam 直後の主則読み)。
- 選択肢集合 = {0, 1} → mex = **2** = 2·[11 odd] ✓。

**R = 12 (主則への継ぎ目・横断 2 列目)**: 子 budget 11:
- fall/compress/corner/B: z11 層値 at 11 → **2** (B: L-BU11G t=11 < 12 → 2)。
- C: **1 ⊕ [z10 at budget 11, 主則]**: f0(δ₂−10), δ₂ = 11−2m odd ≤ 9 →
  δ₂−10 odd ≤ −1 → f0 = 1 → C = **0** (層域横断 2 列目)。
- 選択肢集合 = {2, 0} → mex = **1**。主張値: g1(δ−10) at R=12 (δ = 12−2m even ≤ 10):
  δ−10 even ≤ 0 → g1 = 1 ✓。

**R ≥ 13 (主則)**: 子は全て主則読み (budget R−1 ≥ 12):
- fall 子: g1(δ_c−10) at δ_c = δ+1 → **g1(δ−9)**。
- B 子 (m=1): L-BU11G main at t = R−1 = δ+1 ≥ 12 → g1(t−10) = **g1(δ−9)**
  (fall 子と同じ表を再生 — B-exit 再生構造の z11 版)。
- compress 子: **g1(δ−11)**; corner 子 (g=1): 床 T-BDT11 main at j_c = δ−1 →
  **g1(δ−11)** (compress 子と同値)。
- C 子: 1 ⊕ f0(δ₂−10) at δ₂ = δ−1 → **1 ⊕ f0(δ−11) = g1(δ−11)** (δ = 12 のとき
  δ−11 = 1 で C = 1 ⊕ f0(1) = 3 のみ例外)。

場合分け (δ ≡ R (mod 2), δ ≤ g; B 子・corner 子は m=1/g=1 の行にのみ出現するが
値は fall/compress と同一なので場合分け不要)。この表は K1299 §2.1 z9 表の
δ → δ−2 平行移動 (核 cell δ=9→11・C 核 δ=10→12 の再核算化) で閉じる:

| δ (parity, range) | fall/B g1(δ−9) | comp/corner g1(δ−11) | C 1⊕f0(δ−11) | 集合 S | mex | 主張 g1(δ−10) |
|---|---|---|---|---|---|---|
| odd, δ ≤ −1 | g1(even ≤ −10)=1 | g1(even ≤ −12)=1 | 1⊕f0(even ≤ −12)=1⊕0=1 | {1} | 0 | g1(odd ≤ −11)=[even]=0 ✓ |
| δ = 1 | g1(−8)=1 | g1(−10)=1 | 1 | {1} | 0 | g1(−9)=[even]=0 ✓ |
| δ = 3 | g1(−6)=1 | g1(−8)=1 | 1 | {1} | 0 | g1(−7)=[even]=0 ✓ |
| δ = 5 | g1(−4)=1 | g1(−6)=1 | 1 | {1} | 0 | g1(−5)=[even]=0 ✓ |
| δ = 7 | g1(−2)=1 | g1(−4)=1 | 1 | {1} | 0 | g1(−3)=[even]=0 ✓ |
| δ = 9 | g1(0)=1 | g1(−2)=1 | 1 | {1} | 0 | g1(−1)=[even]=0 ✓ |
| δ = 11 (核) | g1(2)=0 | g1(0)=1 | 1⊕f0(0)=1 | {0,1} | 2 | g1(1)=2 ✓ |
| δ = 13 | g1(4)=0 | g1(2)=0 | 1⊕f0(2)=1⊕1=0 | {0} | 1 | g1(3)=[odd]=1 ✓ |
| odd, δ ≥ 15 | g1(even ≥ 6)=0 | g1(even ≥ 4)=0 | 1⊕f0(even ≥ 4)=1⊕1=0 | {0} | 1 | g1(odd ≥ 5)=[odd]=1 ✓ |
| even, δ ≤ 0 | g1(odd ≤ −9)=0 | g1(odd ≤ −11)=0 | 1⊕f0(odd ≤ −11)=1⊕1=0 | {0} | 1 | g1(even ≤ −10)=[even]=1 ✓ |
| δ = 2 | g1(−7)=0 | g1(−9)=0 | 1⊕f0(−9)=1⊕1=0 | {0} | 1 | g1(−8)=1 ✓ |
| δ = 4 | g1(−5)=0 | g1(−7)=0 | 0 | {0} | 1 | g1(−6)=1 ✓ |
| δ = 6 | g1(−3)=0 | g1(−5)=0 | 0 | {0} | 1 | g1(−4)=1 ✓ |
| δ = 8 | g1(−1)=0 | g1(−3)=0 | 1⊕f0(−3)=1⊕1=0 | {0} | 1 | g1(−2)=1 ✓ |
| δ = 10 | g1(1)=2 | g1(−1)=0 | 1⊕f0(−1)=1⊕1=0 | {2,0} | 1 | g1(0)=1 ✓ |
| δ = 12 (C 核) | g1(3)=1 | g1(1)=2 | 1⊕f0(1)=3 | {1,2,3} | 0 | g1(2)=0 ✓ |
| even, δ ≥ 14 | g1(odd ≥ 5)=1 | g1(odd ≥ 3)=1 | 1⊕f0(odd ≥ 3)=1⊕0=1 | {1} | 0 | g1(even ≥ 4)=[odd]=0 ✓ |

全 δ 場合で mex = 主張値。■

### §2.2 T-BDT11 (z11 bed) の証明

主張値 b11(R,j): 2·[R odd] (R < 12); g1(j−10) (R ≥ 12), R = 2m+j, j ≤ 0。

R = 0: mex ∅ = 0 ✓。

**R ∈ {1,...,10} (例外層前半)**: 子 budget R−1 ∈ {0..9}:
- fall 子 (m ≥ 2): pair (m−1,m)@z11 → 層値 2·[(R−1) odd] (budget 定数)。
- B 子 (m = 1): v(1,12,t) at t = R−1 ∈ {0,1} → 0/2 = 2·[t odd]
  (m=1 は R ≤ 2 のみ: j = R−2 ≤ 0)。
- C 子: 1 ⊕ [b10 at (R−1), 床座標 j−1]: z10 床層域 (厚み 10) 内 → 2·[(R−1) odd]。

選択肢集合: R=1: {0,1} → **2** ✓; R=2: {2,3} → **0** ✓; R=3: **2** ✓; R=4: **0** ✓;
R=5: {0,1} → **2** ✓; R=6: {2,3} → **0** ✓; R=7: **2** ✓; R=8: **0** ✓;
R=9: {0,1} → **2** ✓; R=10: {2,3} → **0** ✓ (C 子 budget 9 は z10 床層域内)。

**R = 11 (層域横断 1 列目・m ≥ 6, j = 11−2m odd ≤ −1)**: 子 budget 10:
- fall: pair (m−1,m)@z11 層値 at 10 → **0**。
- C: **1 ⊕ b10 at budget 10 = z10 床主則域 (R ≥ 10)**: f0((j−1)−10) = f0(j−11):
  j odd → j−11 even ≤ −12 → f0 = 0 → C = **1** (band 版 §2.1 R=11 と対)。
- 集合 {0, 1} → mex = **2** ✓。

**R = 12 (継ぎ目・m ≥ 6, j = 12−2m even ≤ 0)**: 子 budget 11:
- fall: pair (m−1,m)@z11 層値 at 11 → **2**。
- C: **1 ⊕ b10 at budget 11 (主則) 座標 j−1**: f0(j−11): j even → j−11 odd ≤ −9 →
  f0 = 1 → C = **0** (横断 2 列目)。
- 集合 {2, 0} → mex = **1**。主張 g1(j−10): j even → j−10 even ≤ −10 →
  g1 = [even] = 1 ✓。

**R ≥ 13 (主則)**: 子は主則読み (child budget ≥ 12):
- fall: pair (m−1,m)@z11 main at δ_c = (R−1)−2(m−1) = j+1 → g1(j+1−10) = **g1(j−9)**。
- C: 1 ⊕ b10 main at 座標 j−1: f0(j−11) → **1 ⊕ f0(j−11) = g1(j−11)**
  (j−11 ≤ −11 なので f0 の核 d=1 は不成立・常に g1)。
- B 子は m = 1 で R ≤ 2 にしか現れない (主則域外)。

| j (parity) | fall g1(j−9) | C g1(j−11) | 集合 | mex | 主張 g1(j−10) |
|---|---|---|---|---|---|
| odd, j ≤ −1 | g1(even ≤ −10)=1 | g1(even ≤ −12)=1 | {1} | 0 | g1(odd ≤ −11)=[even]=0 ✓ |
| even, j ≤ 0 | g1(odd ≤ −9)=0 | g1(odd ≤ −11)=0 | {0} | 1 | g1(even ≤ −10)=[even]=1 ✓ |

■ (bed は compress/corner 子を持たない — 両減算が同じ fall 子に縮退する。
K1299 §2.2 z9 床表の δ → δ−2 平行移動。)

### §2.3 T-PDT12 (z12 band) の証明

主張値 V(R,δ) := 2·[R odd] (R < 12); f0(δ−12) (R ≥ 12)。

R = 0: mex ∅ = 0 = 層値 ✓ (= 主則 f0(δ−12) = f0(−2m−12) = 0 とも一致)。

**R ∈ {1,...,11} (例外層)**: 子 budget R−1 ∈ {0..10} — **全て z12 層域 (< 12) 内 かつ
z11 層域 (< 12) 内** (z11/z12 の層厚が一致するため C 子は域を跨がない —
K1294 §2.3 z8 の (8,8)・K1299 §2.3 z10 の (10,10) 横断ゼロ型の (12,12) 版・
層内部で閉じる):
- fall/compress/corner: z12 band/床 層値 at R−1 → 2·[(R−1) odd]。
- B (m=1): L-BU12G at t = R−1 < 12 → 2·[t odd] → 同一。
- C: 1 ⊕ [z11 at (R−1)]: z11 層値 (packet T-PDT11, R−1 < 12) 2·[(R−1) odd]。

集合: R=1: {0,1} → **2** ✓; R=2: {2,3} → **0** (= 主則 f0(δ−12): δ even ≤ 0
→ δ−12 even ≤ −12 → 0 と一致 — 偶数 cell は層値と主則が同一); R=3: **2** ✓;
R=4: **0** (主則: δ even ≤ 2 → δ−12 ≤ −10 → 0 ✓); R=5: **2** ✓; R=6: **0**
(主則: δ ≤ 4 → 0 ✓); R=7: **2** ✓; R=8: **0** (δ ≤ 6 → 0 ✓); R=9: **2** ✓;
R=10: **0** (δ ≤ 8 → 0 ✓); R=11: {0,1} → **2** ✓ (C 子 budget 10 は z11 層域内・
横断ゼロの帰結: 層域横断 (z9/z11 型) とは逆に本 packet の偶数面は全子が層定数)。

**R = 12 (継ぎ目)**: 子 budget 11:
- fall/compress/corner: z12 層値 at 11 → **2**。
- B: L-BU12G t=11 < 12 → **2**。
- C: 1 ⊕ [z11 at budget 11, 層値 2] → C = **3** (z11 層域は R < 12 なので
  budget 11 はまだ層 — K1290 z6 seam・K1294 z8 seam・K1299 z10 seam (C 子 budget
  = 下位面層値 2 → 3) と同一の役割)。
- 集合 {2,3} → mex = **0**。主張: f0(δ−12) at δ even ≤ 10 → δ−12 even ≤ −2 →
  0 ✓。

**R ≥ 13 (主則)**: 子は全て主則読み (budget R−1 ≥ 12):
- fall: f0(δ_c−12) at δ_c = δ+1 → **f0(δ−11)**。
- B (m=1): L-BU12G main at t = R−1 = δ+1 ≥ 12: f0(t−12) = **f0(δ−11)**
  (fall 再生)。
- compress: **f0(δ−13)**; corner (g=1): T-BDT12 main at j_c = δ−1 →
  **f0(δ−13)** (compress 子と同値)。
- C: 1 ⊕ g1(δ₂−10) at δ₂ = δ−1 → **1 ⊕ g1(δ−11) = f0(δ−11)** for δ ≠ 12
  (δ=12 のとき 3)。

(K1299 §2.3 z10 表の δ → δ−2 平行移動。核 cell: 核 δ=11→13・C 核 δ=10→12・
comp 核 δ=12→14。)

| δ (parity, range) | fall/B f0(δ−11) | comp/corner f0(δ−13) | C 1⊕g1(δ−11) | 集合 S | mex | 主張 f0(δ−12) |
|---|---|---|---|---|---|---|
| even, δ ≤ 10 | f0(odd ≤ −1)=1 | f0(odd ≤ −3)=1 | 1⊕g1(odd ≤ −1)=1⊕0=1 | {1} | 0 | f0(even ≤ −2)=0 ✓ |
| δ = 12 (C 核) | f0(1)=2 | f0(−1)=1 | 1⊕g1(1)=3 | {2,1,3} | 0 | f0(0)=0 ✓ |
| δ = 14 (comp 核) | f0(3)=0 | f0(1)=2 | 1⊕g1(3)=1⊕1=0 | {0,2} | 1 | f0(2)=1 ✓ |
| even, δ ≥ 16 | f0(odd ≥ 5)=0 | f0(odd ≥ 3)=0 | 1⊕g1(odd ≥ 5)=1⊕1=0 | {0} | 1 | f0(even ≥ 4)=1 ✓ |
| odd, δ ≤ 11 | f0(even ≤ 0)=0 | f0(even ≤ −2)=0 | 1⊕g1(even ≤ 0)=1⊕1=0 | {0} | 1 | f0(odd ≤ −1)=1 ✓ |
| δ = 13 (核) | f0(2)=1 | f0(0)=0 | 1⊕g1(2)=1⊕0=1 | {1,0} | 2 | f0(1)=2 ✓ |
| odd, δ ≥ 15 | f0(even ≥ 4)=1 | f0(even ≥ 2)=1 | 1⊕g1(even ≥ 4)=1⊕0=1 | {1} | 0 | f0(odd ≥ 3)=0 ✓ |

全 δ 場合で mex = 主張値。■

### §2.4 T-BDT12 (z12 bed) の証明

主張 b12(R,j): 2·[R odd] (R < 12); f0(j−12) (R ≥ 12)。

R = 0: 0 ✓ (= 層値 = 主則 f0(−2m−12)=0)。

R ∈ {1..11}: 層内部 (上記 §2.3 と同一の (12,12) 横断ゼロ): fall 子 = pair
(m−1,m)@z12 層値、B 子 (m=1, R ≤ 2) = v(1,13,t) t∈{0,1} = {0,2} = 2·[t odd]、
C 子 = 1 ⊕ b11 at (R−1) (z11 床層域・厚み 12 内 → 層値)。集合: R odd:
{0,1} → **2** ✓; R even: {2,3} → **0** ✓ (主則 f0(j−12): j even → j−12 even
≤ −12 → 0 と一致)。

**R = 12 (継ぎ目, m ≥ 6, j = 12−2m even ≤ 0)**: 子 budget 11:
- fall: pair (m−1,m)@z12 層値 at 11 → 2。
- C: 1 ⊕ b11 at budget 11 (z11 床層値 at 11: 2) → 3 (z11 床層域は R < 12 なので
  budget 11 は層 — 横断ゼロ)。
- 集合 {2,3} → mex **0** = 主則 f0(j−12): j even → j−12 even ≤ −12 → 0 ✓。

**R = 13 (m ≥ 7, j odd)**: 子 budget 12 (両面とも主則域):
- fall: pair (m−1,m)@z12 main at δ_c = j+1 → f0(j+1−12) = **f0(j−11)**:
  j odd → j−11 even ≤ −10 → 0。
- C: 1 ⊕ b11 at budget 12 (main) 座標 j−1: g1((j−1)−10) = g1(j−11): j odd →
  j−11 even ≤ −10 → g1 = 1 → C = **0**。
- 集合 {0} → mex **1** = 主則 f0(j−12): j odd → j−12 odd ≤ −11 → 1 ✓。

**R ≥ 14 (主則)**: 子は主則読み:
- fall: **f0(j−11)**; C: 1 ⊕ g1(j−11) = **f0(j−11)** for j ≠ 12 (j ≤ 0 常に)。
- mex({f0(j−11)}) — 単一値 v なら mex = 0 (v ≠ 0), 1 (v = 0):
  - j odd: f0(even ≤ −12)=0 → mex **1** = 主張 f0(odd ≤ −11)=1 ✓。
  - j even: f0(odd ≤ −11)=1 → mex **0** = 主張 f0(even ≤ −12)=0 ✓。■

### §2.5 L-BU11G / L-BU12G の閉形式からの導出

K0832 closed form v(x,z,R) から直接読む。token plane 12, w ≥ 2:
- w ≥ 13: region 1 ≤ 12 ≤ w−1, m = q_odd(12) = 11: t ≤ 11: 2·[t odd] (層 t < 12
  と一致、t = 11 の 2 = g1(1) は層核と主則核の境界値の一致 — K1289 L-BU4G・
  K1290 L-BU6G・K1294 L-BU8G・K1299 L-BU9G と同一); 11 < t < w+12 (t ≤ w で常に):
  (t+12)%2 = t%2: t 偶 → 0 = g1(t−10) (even ≥ 2 → [odd]=0), t 奇 → 1 =
  g1(t−10) (odd ≥ 3 → [odd]=1)。
- w = 12: region z = x: t 奇 ≤ 23: 2; t 偶 ≤ 11: 0 (= 層値); t=12: 偶 > 11 →
  x%2 = 0 = g1(2) = 0 (主則核 cell の一致)。
- w ∈ {2,...,11}: region z ≥ x+1: m = q_odd(w) ≤ 11: t ≤ m: 2·[t odd] (層内);
  t > m, t ≤ w: w%2 — w 偶 {2,4,6,8,10} で t = w が該当するのみで値 0 = 層値
  2·[w odd] = 0 と一致、w 奇は m = w で不使用。全域層値 (t ≤ w ≤ 11 < 12)。
token plane 13, w ≥ 2:
- w ≥ 14: m = q_odd(13) = 13: t ≤ 13: 2·[t odd] (t < 12 層; t=12: 0 = f0(0) =
  主則核の一致; t=13: 2 = f0(1) = 核の一致); 13 < t ≤ w: (t+13)%2 = 1−t%2:
  t 偶 → 1 = f0(t−12) (even ≥ 2 → [even]=1), t 奇 → 0 = f0(t−12)
  (odd ≥ 3 → 0)。
- w = 13: region z = x: t 奇 ≤ 25: 2 (t=13: 2 = f0(1) ✓); t 偶 ≤ 12: 0
  (t=12: 0 = f0(0) ✓); t ≤ 11 は層値と一致。
- w ∈ {2,...,12}: region z ≥ x+1: m = q_odd(w) ≤ 11: t ≤ m: 2·[t odd];
  t > m, t ≤ w ≤ 12: w%2 (w 偶: t=w のみ 0 = 層値 ✓; w=12: m=11, t=12:
  w%2 = 0 = f0(0) = 0 ✓; w 奇は m = w で不使用)。
全 twist は機体 D9(a)/(b) が closed form × canonical engine × 主張表の三方で
w ≤ 30 照合 (各 493 点)・Y7 が w ≤ 40 発現 probe で補強。■

### §2.6 well-founded 性 (まとめ)

packet {T-PDT11, T-BDT11, T-PDT12, T-BDT12} の証明は単一の R 強帰納:
全子は budget R−1 (engine の子定義)。面間参照: z11 の C 子 = z10 (K1299, 全 R
無条件); z12 の C 子 = z11 (packet, budget R−1); 床 C 子 = plane−1 床
(z11 床の C 子 = b10 = K1299 既刊; z12 床の C 子 = b11 = packet T-BDT11,
budget R−1)。B 子は K0832 closed form (L-BU11G/L-BU12G + w=1 edge {0,2}) で
帰納外。帰納は R のみで整礎 (m, g に依らない子値表)。各 R での子値の列挙は
§2.1–§2.4 の場合表 (R ≤ 12 は層定数読みの列挙、R ≥ 13 は δ parity の場合表)
で全ての (m, g, k) を尽くす。層厚 12 世代の構造は §2.1/§2.2 の「C 子 budget 10
(R=11・z10 seam 直後) と budget 11 (seam R=12) が下位面 (z10, 層厚 10) の主則域
を読む」層域横断が **2 行** (値は δ₂ parity 固定により定数 0/1 に落ちる・
K1299 z9 の R=9/R=10 と同型の平行移動) と、§2.3/§2.4 の「z12 の層域横断がゼロ
(z11 と層厚が一致 (12,12))」の対である (第 6 世代・横断型 = 奇数世代 w=11・
横断ゼロ型 = 偶数世代 w=12 の mod 2 ペア構造は K1289/K1290/K1294/K1299 と同一)。

### §2.7 反例検査の誠実な記述

- 例外層 R ∈ {0,...,11} の値 2·[R odd] は宣言前探索 (§3 X1–X4) で (R,δ) 平面
  で mixed cell 0 として先に特定済み (K1289 の「slope trap」教訓を適用)。
- m 依存性・g 依存性は主張域内で一度も観測されていない (§3 Y1/Y2 広域)。
  主張は typed 証明による全称主張であり、census は照合である。
- honest 記録: verify 機体 D11 far-row 電池の初期設計は m=12, k∈[−12..−1],
  g∈[1..18] box を K1299 と同一に使ったが、この box の R=13 行 (k=−12, g=1 の
  1 cell) は z13/z14 の層厚 14 に対して**例外層内**に入り、初回ローカル実行が
  まさにその 2 cell (z13far/z14far で h=2 vs 予測 0/1) を指摘した。R ≥ 14 guard
  を入れて宣言前に修正した (当該 cell の値 2 は層値の主張どおりで、定理側の
  反例ではなく電池設計の誤り)。修正後 D11 bad 0。

## §3 宣言前探索 (pre-declaration; explore_k1301.py / explore2_k1301.py 出力)

- X1/X3 (z11/z12 band m≤12 g≤25 k≥−60, (R,δ) 表): mixed (R,δ) cell それぞれ
  cells 468 中 0/0 (X2/X4 beds は 168 cell 中 0/0)。低 R 行 (R=0..11) が定数
  0/2/0/2/.../2 (層厚 12 の直接観測)。R=12 seam 行 (z11 は全 1 = g1(even ≤ 0)、
  z12 は全 0 = f0(even ≤ −2))。R≥13 行が g1(δ−10) / f0(δ−12) に一致
  (核 cell z11 δ=11 → 2・z12 δ=13 → 2 を含む)。
- X2/X4 (beds m≤12 j∈[−30..0]): 同一の R 層構造・mixed 0/0。
- X5/X6: L-BU11G/L-BU12G 発現 census (w ≤ 30, t ≤ w; engine vs closed form vs
  plane-11/12 法則): 1,972 checks bad 0/0。w=1 edge: v(1,12,{0,1})={0,2},
  v(1,13,{0,1})={0,2}。
- X7: sharpened C-PSF′ probe (z=0..14, m≤10 g≤20 k≥−50 の dedup (R,δ) 320
  cell × 15 面): bad 全 0。
- X8: typed 子 self-check (宣言前): 子を申立テーブル (z11/z12 申立 + K1299
  z9/z10 既刊) + closed form からのみ構成した mex が申立値・engine と一致するかを
  slices 3,878 点・beds 228 点で確認: bad 0/0 (手証明 §2 構文の宣言前検証)。
- Y1/Y2: z11/z12 band+beds の wide census (D1–D4 と同一 box): 8,928/360 × 2
  bad 0。
- Y3/Y4/Y5: z13/z14 OBS (band 4,500 × 2, beds 120 × 2, far-row m=12 R ≥ 14
  215 × 2 (R=13 の層内 1 cell は除外・値 2 は層値と一致),
  low-R (R<14) hist {0:582, 2:567} × 2 cells 1,149): cpsf 予測 vs engine
  bad 全 0 (有限観測・全称主張なし)。
- Y6: ordered vs canonical engine 交差 (z=11..14, 各 464 cells): mismatch 全 0。
- Y7: L-BU11G/L-BU12G (w ≤ 40, 858 cells each) bad 0 + 発現 **L-BU13G**
  (v(w,14,t) = plane-13 law: 2·[t odd] (t<14) / g1(t−12))・**L-BU14G** 発現
  (v(w,15,t): 2·[t odd] (t<14) / f0(t−14)) を w ≤ 40 probe: bad 0
  (z=14,15 token plane は OBS)。
- Y8: T-TWIN identity d∈[−260..260] bad 0; z=0..16 dedup (R,δ) sweep:
  全 17 面 mixed 0・cpsf bad 0 (**C-PSF′ が plane 16 まで観測拡張**・K1299 Y8
  の z≤14 から 2 面拡張)。

## §4 機体宣言 (machine declaration, publish-then-execute)

`verify_k1301.py` (sha256 publish 時に kit で宣言 =
`6026e07f8f61f4434c5a23738d5471bdcf871b4c91fa8aac4286a15667ff5b05`・engine
pin `bd5f22e415a78368c9b798296bc84948d5637decbf3c21a92404d45fb12e3a92`
startup gate 内蔵・embed は K1138/K1282..K1299 と同一 bytes)。engine_block.py
sha256 `582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0`
(K1282–K1299 kit と byte-identical・explore 系 import 用単体)。バッテリ:

| # | 内容 | 期待 count |
|---|---|---|
| D1 | z11 band census (m≤14, g≤25, k∈[max(−30,−2m−g),0]) | 8,928 |
| D2 | z11 beds census (m≤18, j∈[−36..0]) | 360 |
| D3 | z12 band census (D1 box) | 8,928 |
| D4 | z12 beds census (D2 box) | 360 |
| D5 | typed z11 slices (m≤10, g≤14, k≥−14): typed mex == claim == engine | 1,939 |
| D6 | typed z11 beds (m≤10, j≥−16) | 114 |
| D7 | typed z12 slices (D5 box) | 1,939 |
| D8 | typed z12 beds (D6 box) | 114 |
| D9 | (a) L-BU11G 493 + (b) L-BU12G 493 + (c) K1299 anchors T-PDT9/T-BDT9/T-PDT10/T-BDT10 再照合 4,690 + (d) K1294 anchors 再照合 4,690 + (e) K1290 anchors 再照合 4,690 + (f) K1289 anchors 再照合 4,690 + (g) K1288 anchors 再照合 4,690 + (h) K1286 anchors 再照合 2,345 + (i) sharpened C-PSF′ identity sweep w=0..12 (pair box + bed box) 30,485 + (j) T-TWIN algebra d∈[−100..100] 201 + (k) closed form vs both engines (x≤16, z∈2..13, R∈x+1..x+4) 1,440 + (l) B-exit w=1 edge values (v(1,12,t)/v(1,13,t), t≤1) 4 | 58,911 |
| D10 | cross-engine canonical vs ordered (z11/z12 pair m≤8, g≤10, k≥−8 + beds m≤8 j≥−8) | 1,516 |
| D11 | OBS: z13/z14 band (m≤10,g≤20,k≥−50) 4,500×2 + beds (m≤10,j≥−24) 120×2 + far-row m=12 R≥14 215×2 + low-R (R<14) hist probes 1,149×2 + L-BU13G/L-BU14G plane-token sweep (z=14,15, w≤30) 493×2 + dedup (R,δ) sweep z=0..16 (320 × 17) 5,440 | 18,394 |

**総計 101,503 比較点・期待 overall_bad = 0** (宣言前 predry 4 走で
counts [8928,360,8928,360,1939,114,1939,114,58911,1516,18394]・
bad 全 0・stdout byte-identical sha256
`70206d62b8a8e91d97bed7403dfaf6d970db47b4c32de4cecc98e7358a5d562c`
を確認済み)。

変異電池 (公式 run の前に期待値を宣言):
- `--tamper-engine`: rc=2・mutated sha `0ea47a80761d2b20bf414cd52b1535fba56829c3a4c232d1b2f5da3f81441882` ≠ pin (K1282–K1299 と同一変異)。
- `--tamper=z11s`: rc=1, D1 bad 8,928。`--tamper=z11b`: rc=1, D2 bad 360。
- `--tamper=z12s`: rc=1, D3 bad 8,928。`--tamper=z12b`: rc=1, D4 bad 360。
- 他バッテリ (D5–D11) は census クレームの flip の影響を受けない
  (typed 側は flip されないので D5–D8 の 3-way 照合は主張値のまま engine と
  一致する; 対角の影響は D1–D4 の bad のみ)。

公式 4 走: 同一 cwd (PYTHONHASHSEED random/1) × 2 + 隔離 tree (env -i,
PYTHONHASHSEED 99/7) × 2、stdout byte-identical が要求 (fetch-back bytes から
走行)。

## §5 open 登録 (有限観測・予想と次課題; 全称主張なし)

- **O9⁗ (C-PSF′ の w 帰納 — K1299 O9‴ update)**: 全称は w ∈ {0..12} まで
  (本項で +2)。**Y8 dedup sweep で w=13..16 が 320 cell × 4 面で mixed 0・
  cpsf bad 0・X7/Y3–Y5 band/bed/far/lowR OBS が w=13,14 を直接支持**
  (K1299 の z≤14 dedup から +2)。次の単一オーナー候補は
  T-PDT13/T-BDT13・T-PDT14/T-BDT14 (z13/z14 typed・§2 と同一構文: C 子は
  本項 z11/z12 定理 (全 R・例外層込み) を参照。z13/z14 の層厚は
  L(13) = L(14) = 2⌈13/2⌉ = 14。層域横断は z13 では C 子 budget 12,13 (R=13
  層内 + seam R=14) の 2 行が z12 主則域 (R ≥ 12) を読む・z14 では横断ゼロ
  ((14,14)・z12 型)。層核の mex{0,1}=2/mex{2,3}=0 機構は w 非依存と root 交代
  なし。完了で sharpened C-PSF′ が w=14 まで全称化)。
- **O10⁗ (L-BUzG 族の全称形 — K1299 O10‴ update)**: 13 枝 (z+1 = 1..13) まで
  全称。**L-BU13G/L-BU14G (token plane 14/15 = plane-13/14 則: 2·[t odd]
  (t<14) / g1(t−12) (z=14), f0(t−14) (z=15)) を w ≤ 30 (verify)・w ≤ 40
  (explore2 Y7) で発見・本項 D11 に OBS 登録**。closed form の region 計算で
  一般 w に拡張可能な見込み (q_odd(z) が層核の両端構造に対応。本項 §2.5 の
  境界一致 3 型が世代毎に再現: L-BU11G では t=11 → 2 = g1(1) 核一致・
  t=12 → 0 = g1(2) 主則 first-cell 一致・層 t<12 は R 定数、L-BU12G では
  t=12 → 0 = f0(0) 核一致・t=13 → 2 = f0(1) 核一致 (w ≥ 14 の q_odd region) —
  この 3 型境界一致スキームの一般 w 命題化が O10⁗ の本命対象)。
- **O11 (例外定数層の一般理論 — K1294/K1299 O11 継続)**: 層厚 L(w) = 2⌈w/2⌉ が
  w = 0..12 全称 + w = 13..16 OBS (dedup)。層の中の子は (w, w−1) の層定数を
  R−1 パリティで読むのみで δ 非依存 — w=3 法則が w=11,12 でも同一に成立
  (§2 の R ≤ 12 cases は w 非依存の mex{0,1}=2 / mex{2,3}=0 機構・第 6 世代)。
  **横断型 (z7/z9/z11: 層内最終行 R = L(w)−1 の C 子が下位面 seam 直後の主則読み
  f0(−2m)=0 → C=1) と横断ゼロ型 (z8/z10/z12: 層厚一致の対面) の 2 型が厚み 12
  でも再現・横断行は常に 2 行 (層内 1 + seam 1)** — 一般 w 帰納は (w mod 2) で
  この 2 型に分類できる見取り (O9⁗ と統合)。
- **O12 (11×11 giant 枝刈り格子)**: T-PD0 (K1286) + K1288 + K1289 + K1290 +
  K1294 + K1299 + 本項で、ペア面 z ∈ {0..12} の対角下全域 k ≤ 0 が R 例外層込みで
  O(1) 即値評価可能に (band は δ と R の 2 変数・床は 1 変数)。境界側格子の
  拡張として巨大探索レーンへ記録 (採用判断はオーナー)。
- **O13 (K1287 O1 残部)**: (i) SLB2/SLB3 単一層族・(ii) L/Am frontier 全称化
  は非接触のまま (K1289/K1290/K1294/K1299 と同一)。

## §6 主張の区別 (過大主張の防止)

- 定理 (universal, §2 手証明): T-PDT11, T-BDT11, T-PDT12, T-BDT12, L-BU11G,
  L-BU12G, C1 (K1299 O9‴ z11/z12 部分解決の記述), C2 の w ≤ 12 部分
  (sharpened C-PSF′ の w については既刊+本項の集約)。
- corollary (universal だが既刊の言い換え): C2/C3 の既刊分の再表現。
- 有限観測 (OBS): D11 (z13/z14 band/beds/far-row/lowR hist・L-BU13G/L-BU14G・
  dedup sweep z=13..16)・§3 X/Y。
- census 点数 101,503 は定理の実機照合であり全称性の主張ではない。
- 標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は
  全て UNKNOWN のまま。verdict 不消費。

(宣言ノート本文ここまで。実装は publish-then-execute: 本ノートが最先行。
kit → fetch-back → 公式 4 走 → 変異電池 → 成果物出版 → K item → README bullet
→ run log の順に進める。)
