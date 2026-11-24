# 単一オーナー宣言 K1294: pre-diag 双生児 z7/z8 の全称確定
(T-PDT7/T-BDT7 + T-PDT8/T-BDT8 — K1290 O9′ の z7/z8 部分の取得・sharpened C-PSF′ の w=7,8 実例化・z9/z10 OBS)

## §0 状態と採番 (single-owner protocol)

- 観測 HEAD (着手時): `739e8428732ae2d670f69611396d02027ed00e85` 系の 2026-11-24T15:31:04Z state (K1293 YAML fix)。実行開始時の観測最新 K item = K1293 (`7a1e183c` 15:25:20Z・`739e8428` fix 15:31:04Z)。
- 本宣言 push 直前再取得 HEAD: `a461445f9b173de444b7ba826bb2fcadf361b3b1` (2026-11-24T15:35:17Z・design-kyouen-witt レーンの独立検証器証跡追記。領域直交・非接触)。
- K1294 空き確認: `research/knowledge/items/` の最新 K item = K1293。コミットログに K1294 宣言 0 件・対抗宣言なし (2026-11-24T15:3xZ 時点・本宣言 push 直前に再確認)。K1290 item 中の「K1291+ 候補」記述は番号取得ではなく未着手領域の列挙である点は K1290 と同一 (K1291/K1292 は moment-polynomial certificate レーン・K1293 は Witt/affine Steiner 3-design レーンが取得済み・いずれも本領域と直交)。
- 領域: K1290 lane が §5 O9′ として登録した T-PDT7/T-BDT7・T-PDT8/T-BDT8 (z7/z8 pre-diag typed 全称) を取得。K1290 O9′ の z7/z8 部分を解決し sharpened C-PSF′ を w=9..12 の OBS 拡張まで進め、z9/z10 (次の観測面) を OBS 登録する。K1286/K1287/K1288/K1289/K1290 の全定理に触れない (内面 k>0・multi-c web は非接触)。
- 規約: verdict 不消費・標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は全て UNKNOWN のまま。

## §1 主張 (claims)

座標の規約は K1286/K1288/K1289/K1290 と同一: ペア局面 H(R;(m,m+g);z)、対角座標 k := R−2m−g、
δ := R−2m、バンド域 k ≤ 0 (0 ≤ R ≤ 2m+g)。床 (bed) は (m,m) 双 Token:
b_z(j) := H(2m+j;(m,m);z), j ≤ 0。f0 は K1286 出版の対角下バンド 1 次元崩壊関数、
g1 は K1288 出版の偶奇双生児 (T-TWIN: g1(d) = 1 ⊕ f0(d) for d ≠ 1, g1(1) = f0(1) = 2):

- f0(d) = 2 (d=1); [d odd] (d ≤ 0); [d even] (d ≥ 2)
- g1(d) = 2 (d=1); [d even] (d ≤ 0); [d odd] (d ≥ 2)

**定理パッケージ (universal, 量子化: ∀m ≥ 1, ∀g ≥ 1, 全ての有効 cell, 値は m も g も経由しない):**

- **T-PDT7 (z7 band)**: H(R;(m,m+g);7) = 2·[R odd] (R < 8); g1(δ−6) (R ≥ 8)。
- **T-BDT7 (z7 bed)**: b7(j) = 2·[R odd] (R < 8, R = 2m+j); g1(j−6) (R ≥ 8)。
- **T-PDT8 (z8 band)**: H(R;(m,m+g);8) = 2·[R odd] (R < 8); f0(δ−8) (R ≥ 8)。
- **T-BDT8 (z8 bed)**: b8(j) = 2·[R odd] (R < 8); f0(j−8) (R ≥ 8)。
  (層厚 L(7) = L(8) = 2⌈w/2⌉ = 8。z8 の偶数例外 cell (R=0,2,4,6) は主則 f0(δ−8)
  と値が一致する (δ even ≤ 6 → δ−8 even ≤ −2 → f0 = 0) ので「R < 8 で 2·[R odd]」
  として統一できる。z7 の偶数 cell (R=0,2,4,6) は主則 g1(δ−6) = 1 と衝突するので
  層の上書きとして本物である − K1289 の z3/z4・K1290 の z5/z6 と同一の役割分担
  (奇数平面の層は実質、偶数平面の層は見かけ上主則と一致)。)

**補題 (closed-form から機械照合 w ≤ 30):**

- **L-BU7G**: v(w,8,t) = 2·[t odd] (t < 8); g1(t−6) (8 ≤ t ≤ w), ∀w ≥ 2
  (単一 Token w を平面 8 に置いた局面 = B-exit 子の値 = plane-7 則のフル形式)。
- **L-BU8G**: v(w,9,t) = 2·[t odd] (t < 8); f0(t−8) (8 ≤ t ≤ w), ∀w ≥ 2。
  (t=8 の 0 = f0(0) は主則核、t=9 の 2 = f0(1) は層核の境界一致 — K1289 L-BU4G・
  K1290 L-BU6G と同一構造。)

**系 (corollaries / subsumption):**

- **C1 (K1290 O9′ z7/z8 RESOLVED)**: K1290 D11/Y3–Y5 が OBS として観測し
  D9(f)…当時 w=7,8 未証明ゆえ identity sweep から外していた z7/z6 予測面が
  本項で全称定理化。層厚 8・主則 g1(δ−6) (z7) / f0(δ−8) (z8) が例外層込みで確定。
- **C2 (sharpened C-PSF′ = K1290 O9′ の w=7,8 実例化)**: 統一形式
  **H(R;(m,m+g);w) = 2·[R odd] (R < 2⌈w/2⌉); T_w(δ − 2⌊w/2⌋) (R ≥ 2⌈w/2⌉)**,
  T_w = g1 (w 奇数) / f0 (w 偶数)。この項で w ∈ {7,8} が全称証明され、
  w ∈ {0} (K1286), {1,2} (K1288), {3,4} (K1289), {5,6} (K1290), {7,8} (本項)
  と代数的に同一 (verify D9(g) が w=0..8 全 9 面で機械照合)。w ∈ {9,10} は
  D11 有限 OBS のみ (dedup sweep では w=12 まで観測拡張)。層厚 L(w) = 2⌈w/2⌉ の
  一般 w 帰納は未解決 (§5 O9″)。
- **C3 (B-exit 均一性の族)**: 単一 Token @ plane z+1 は plane-z 則を継承する:
  L-BU0 (K1286)・L-BU1G/L-BU2G (K1288)・L-BU3G/L-BU4G (K1289)・L-BU5G/L-BU6G
  (K1290) に続き本項の **L-BU7G/L-BU8G (plane-7 / plane-8)** で 9 枝になる
  (w=9,10 token plane (L-BU9G/L-BU10G 相当) は D11/Y7 OBS・全称主張なし)。

**§1.1 K1290 内面との境界 (重複なし)**: K1290 D11/Y3–Y5/Y7/Y8 の z7/z8 band OBS
(band 各 4,500 点・bad 0)・L-BU7G/L-BU8G 発現 probe・dedup z=7..10 は有限観測として
本項が定理化する対象であった。本項の主張は R 例外層値込みの全 cell を含み、
K1290 が open にした「z7/z8 の typed 証明」を定理として確定する。
K1286 T-Z1 k=1 内面・K1287 F2 web の内面 k>0・K1290 の z5/z6 定理には一切触れない
(z5/z6 は z7 の C 子として外部参照 (既刊・全 R 無条件) するのみで再証明しない)。

## §2 手証明 (typed child mex, single R strong induction)

### §2.0 型付き子の分類 (pair @ plane z)

K1290 §2.0 と同一 (engine 定義から直接)。Budget R の局面 (m,m+g)@z
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
値 {v(1,z+1,0), v(1,z+1,1)} = {0,2} — closed form・D9(j) 照合)、**C**
(1 ⊕ 床 (m,m)@(z−1), budget R−1, 床座標 j−1)。

well-founded 性: 単一の packet {T-PDT7, T-BDT7, T-PDT8, T-BDT8} 全体で R に
ついての強帰納。全ての子の budget は R−1 であり、面間参照は常に下位 budget
(z7 の C 子は z6 = K1290 既刊で全 R 無条件、z8 の C 子は z7 = packet 内で
budget R−1)。B 子・床 B 子は closed form (帰納外)。基底 R = 0: 選択肢集合は空、
mex ∅ = 0 (4 定理すべての主張値と整合: 層値 2·[0]=0・主則読みも
g1(δ−6)/f0(δ−8) は R=0 cell では層値と同一)。

### §2.1 T-PDT7 (z7 band) の証明

主張値 V(R,δ) := 2·[R odd] (R < 8); g1(δ−6) (R ≥ 8)。

**R = 0**: mex ∅ = 0 = 層値。

**R ∈ {1,...,7} (例外層)**: 子は全て budget R−1 ∈ {0..6}:
- fall/compress/corner 子: z7 band/床 層値 at R−1 (< 8) = 2·[(R−1) odd]
  (budget 定数・子の δ_c に依らず)。
- B 子 (m=1): L-BU7G at t = R−1 < 8 → 2·[t odd] → 同一の budget 定数。
- **C 子: 1 ⊕ [z6 at (R−1)]** — K1290 の z6 層域は R < 6 (厚み 6) なので、
  R−1 ∈ {0..5} (R ≤ 6) は z6 層値 2·[(R−1) odd] を読むが、
  **R−1 = 6 (R = 7) では z6 主則域 (R ≥ 6) を読む** (K1290 が予告した
  層域を跨ぐ読み・本 packet の新しい局面):
  - R−1 = 6: z6 主則 f0(δ₂−6), δ₂ = 6−2m (C 子の δ) → δ₂−6 = −2m even ≤ −2
    → f0 = 0 → C = 1。

選択肢集合 (fall/compress/corner/B は同値、出現する型によらず同一):
- R=1: {0, 1} → mex = **2** = 2·[1] ✓ (C: 1 ⊕ z6@0 = 1)
- R=2: {2, 3} → mex = **0** ✓
- R=3: {0, 1} → mex = **2** ✓
- R=4: {2, 3} → mex = **0** ✓
- R=5: {0, 1} → mex = **2** ✓ (C 子 budget 4: z6 層値 0 → 1)
- R=6: {2, 3} → mex = **0** ✓ (C 子 budget 5: z6 層値 2 → 3)
- R=7: {0, 1} → mex = **2** ✓ (fall/B/corner: z7 層値 at 6 = 0;
  C 子 budget 6 = **z6 主則読み** f0(−2m) = 0 → C = 1)

**R = 8 (主則への継ぎ目)**: 子 budget 7:
- fall/compress/corner: z7 層値 at 7 → **2**。
- B (m=1): L-BU7G t=7 < 8 → **2**。
- C: 1 ⊕ [z6 at budget 7, 主則]: f0(δ₂−6), δ₂ = 7−2m odd ≤ 5 →
  δ₂−6 odd ≤ −1 → f0 = 1 → C = **0**。
選択肢集合 = {2, 0} → mex = **1**。主張値: g1(δ−6) at R=8 (δ = 8−2m even ≤ 6):
δ−6 even ≤ 0 → g1 = 1 ✓。

**R ≥ 9 (主則)**: 子は全て主則読み (budget R−1 ≥ 8):
- fall 子: g1(δ_c−6) at δ_c = δ+1 → **g1(δ−5)**。
- B 子 (m=1): L-BU7G main at t = R−1 = δ+1 ≥ 8 → g1(t−6) = **g1(δ−5)**
  (fall 子と同じ表を再生 — K1288..K1290 の B-exit 再生構造の z7 版)。
- compress 子: g1(δ_c−6) at δ_c = δ−1 → **g1(δ−7)**。
- corner 子 (g=1): 床 T-BDT7 main at j_c = δ−1: g1(j_c−6) = **g1(δ−7)**
  (compress 子と同値)。
- C 子: 1 ⊕ f0(δ₂−6) at δ₂ = δ−1 → **1 ⊕ f0(δ−7)** = g1(δ−7) unless δ = 8
  (δ−7 = 1 のとき C = 1 ⊕ f0(1) = 3)。

場合分け (δ ≡ R (mod 2), δ ≤ g; B 子・corner 子は m=1 すなわち δ = R−2 の行に
のみ出現するが値は fall/compress と同一なので場合分け不要):

| δ (parity, range) | fall/B g1(δ−5) | comp/corner g1(δ−7) | C 1⊕f0(δ−7) | 集合 S | mex | 主張 g1(δ−6) |
|---|---|---|---|---|---|---|
| odd, δ ≤ −1 | g1(even ≤ −6)=1 | g1(even ≤ −8)=1 | 1⊕f0(even ≤ −8)=1⊕0=1 | {1} | 0 | g1(odd ≤ −7)=[even]=0 ✓ |
| δ = 1 | g1(−4)=1 | g1(−6)=1 | 1⊕f0(−6)=1 | {1} | 0 | g1(−5)=[even]=0 ✓ |
| δ = 3 | g1(−2)=1 | g1(−4)=1 | 1 | {1} | 0 | g1(−3)=[even]=0 ✓ |
| δ = 5 | g1(0)=1 | g1(−2)=1 | 1⊕f0(−2)=1 | {1} | 0 | g1(−1)=[even]=0 ✓ |
| δ = 7 (核) | g1(2)=0 | g1(0)=1 | 1⊕f0(0)=1 | {0,1} | 2 | g1(1)=2 ✓ |
| δ = 9 | g1(4)=0 | g1(2)=0 | 1⊕f0(2)=1⊕1=0 | {0} | 1 | g1(3)=[odd]=1 ✓ |
| odd, δ ≥ 11 | g1(even ≥ 6)=0 | g1(even ≥ 4)=0 | 1⊕f0(even ≥ 4)=1⊕1=0 | {0} | 1 | g1(odd ≥ 5)=[odd]=1 ✓ |
| even, δ ≤ 0 | g1(odd ≤ −5)=0 | g1(odd ≤ −7)=0 | 1⊕1=0 | {0} | 1 | g1(even ≤ −6)=[even]=1 ✓ |
| δ = 2 | g1(−3)=0 | g1(−5)=0 | 1⊕f0(−5)=1⊕1=0 | {0} | 1 | g1(−4)=1 ✓ |
| δ = 4 | g1(−1)=0 | g1(−3)=0 | 1⊕f0(−3)=1⊕1=0 | {0} | 1 | g1(−2)=1 ✓ |
| δ = 6 | g1(1)=2 | g1(−1)=0 | 1⊕f0(−1)=1⊕1=0 | {2,0} | 1 | g1(0)=1 ✓ |
| δ = 8 (C 核) | g1(3)=1 | g1(1)=2 | 1⊕f0(1)=3 | {1,2,3} | 0 | g1(2)=0 ✓ |
| even, δ ≥ 10 | g1(odd ≥ 5)=1 | g1(odd ≥ 3)=1 | 1⊕f0(odd ≥ 3)=1⊕0=1 | {1} | 0 | g1(even ≥ 4)=[odd]=0 ✓ |

(この表は K1290 §2.1 z5 表の δ → δ−2 平行移動 ($\delta$-$2$ shift) と核 cell の
再核算化 (核 δ=5→7・C 核 δ=6→8) で閉じる — g1/f0 の parity 構造が平行移動で
不変なため、全 δ 場合で mex = 主張値。■)

### §2.2 T-BDT7 (z7 bed) の証明

主張値 b7(R,j): 2·[R odd] (R < 8); g1(j−6) (R ≥ 8), R = 2m+j, j ≤ 0。

R = 0: mex ∅ = 0 ✓。

**R ∈ {1,...,7} (例外層)**: 子 budget R−1 ∈ {0..6}:
- fall 子 (m ≥ 2): pair (m−1,m)@z7 → 層値 2·[(R−1) odd] (budget 定数)。
- B 子 (m = 1): v(1,8,t) at t = R−1 ∈ {0,1} → 0/2 = 2·[t odd]
  (m=1 は R ≤ 2 のみ: j = R−2 ≤ 0)。
- C 子: 1 ⊕ [b6 at (R−1), 床座標 j−1]:
  - R−1 ∈ {0..5}: z6 床層値 (K1290, 厚み 6) 2·[(R−1) odd]。
  - **R−1 = 6 (R = 7): z6 床主則域** f0((j−1)−6) = f0(j−7): R=7 → j = 7−2m,
    m ≥ 4 → j odd ≤ −1 → j−7 even ≤ −8 → f0 = 0 → C = 1 (層域を跨ぐ読み・
    band 版 §2.1 R=7 と対)。

選択肢集合: R=1: {0,1} → 2 ✓; R=2: {2,3} → 0 ✓; R=3: {0,1} → 2 ✓;
R=4: {2,3} → 0 ✓; R=5: {0,1} → 2 ✓; R=6: {2,3} → 0 ✓;
R=7: {0,1} → 2 ✓ (fall: z7 pair 層値 at 6 = 0; C: 1)。

**R = 8 (継ぎ目, m ≥ 4)**: 子 budget 7:
- fall: pair (m−1,m)@z7 層値 at 7 → **2**。
- C: 1 ⊕ b6 at budget 7 (主則) 座標 j−1: f0(j−7): j = 8−2m even ≤ 0 →
  j−7 odd ≤ −7 → f0 = 1 → C = **0**。
- 集合 {2, 0} → mex = **1**。主張 g1(j−6): j even → j−6 even ≤ −6 →
  g1 = [even] = 1 ✓。

**R ≥ 9 (主則)**: 子は主則読み (child budget ≥ 8):
- fall: pair (m−1,m)@z7 main at δ_c = (R−1)−2(m−1) = j+1 → g1(j+1−6) = **g1(j−5)**。
- C: 1 ⊕ b6 main at 座標 j−1: f0(j−7) → **1 ⊕ f0(j−7)**
  = g1(j−7) for j ≠ 6 (j ≤ 0 なので常に成立)。
- B 子は m = 1 で R ≤ 2 にしか現れない (主則域外)。

| j (parity) | fall g1(j−5) | C 1⊕f0(j−7) | 集合 | mex | 主張 g1(j−6) |
|---|---|---|---|---|---|
| odd, j ≤ −1 | g1(even ≤ −6)=1 | 1⊕f0(even ≤ −8)=1⊕0=1 | {1} | 0 | g1(odd ≤ −7)=[even]=0 ✓ |
| even, j ≤ 0 | g1(odd ≤ −5)=0 | 1⊕f0(odd ≤ −7)=1⊕1=0 | {0} | 1 | g1(even ≤ −6)=[even]=1 ✓ |

■ (bed は compress/corner 子を持たない — 両減算が同じ fall 子に縮退する。
K1290 §2.2 z5 床表の平行移動。)

### §2.3 T-PDT8 (z8 band) の証明

主張値 V(R,δ) := 2·[R odd] (R < 8); f0(δ−8) (R ≥ 8)。

R = 0: mex ∅ = 0 = 層値 ✓ (主則 f0(δ−8) = f0(−2m−8) = 0 とも一致)。

**R ∈ {1,...,7} (例外層)**: 子 budget R−1 ∈ {0..6} — **全て z8 層域 (< 8) 内**
(z7 の C 子も z7 層域 (厚み 8) 内・z7/z8 の層厚が一致するため域を跨がない —
K1290 の z5/z6 packet (厚み 6 双子) と対角的に、本 packet は w=3,4 世代
(K1289: C 子が層域 4 の外 budget 4 = z3 seam を読んだ) とは逆に
**層内部で閉じる初の世代**):
- fall/compress/corner: z8 band/床 層値 at R−1 → 0/2/...(R−1 定数)。
- B (m=1): L-BU8G at t = R−1 < 8 → 2·[t odd] → 同一。
- C: 1 ⊕ [z7 at (R−1)]: z7 層値 (packet T-PDT7, R−1 < 8) 2·[(R−1) odd]。

集合: R=1: {0,1} → **2** ✓; R=2: {2,3} → **0** (= 主則 f0(δ−8): δ even ≤ 0
→ δ−8 even ≤ −8 → 0 と一致 — 偶数 cell は層値と主則が同一); R=3: {0,1} →
**2** ✓; R=4: {2,3} → **0** (主則: δ even ≤ 2 → δ−8 ≤ −6 → 0 ✓); R=5: {0,1} →
**2** ✓; R=6: {2,3} → **0** (主則: δ ≤ 4 → δ−8 ≤ −4 → 0 ✓); R=7: {0,1} →
**2** ✓。

**R = 8 (継ぎ目)**: 子 budget 7:
- fall/compress/corner: z8 層値 at 7 → **2**。
- B: L-BU8G t=7 < 8 → **2**。
- C: 1 ⊕ [z7 at budget 7, 層値 2] → C = **3** (z7 層域は R < 8 なので
  budget 7 はまだ層 — K1290 z6 seam (C 子 budget 5 = z5 層値 2 → 3) と同一。
  z5/z6 世代では seam で C 子が z5 主則を読んだ点 (K1290 §2.3 R=6:
  「1 ⊕ z5 at budget 5: 層値 2」) と同一の役割分担)。
- 集合 {2,3} → mex = **0**。主張: f0(δ−8) at δ even ≤ 6 → δ−8 even ≤ −2 → 0 ✓。

**R ≥ 9 (主則)**: 子は全て主則読み (child budget R−1 ≥ 8):
- fall: f0(δ_c−8) at δ_c = δ+1 → **f0(δ−7)**。
- B (m=1): L-BU8G main at t = R−1 = δ+1 ≥ 8: f0(t−8) = **f0(δ−7)** (fall 再生)。
- compress: **f0(δ−9)**; corner (g=1): T-BDT8 main at j_c = δ−1 → **f0(δ−9)**
  (compress 子と同値)。
- C: 1 ⊕ g1(δ₂−6) at δ₂ = δ−1 → **1 ⊕ g1(δ−7)** = f0(δ−7) for δ ≠ 8
  (1 ⊕ g1(x) = f0(x) except x=1; δ=8 のとき 3)。

(K1290 §2.3 z6 表の δ → δ−2 平行移動。核 cell: 核 δ=7→9・C 核 δ=6→8・
comp 核 δ=8→10。)

| δ (parity, range) | fall/B f0(δ−7) | comp/corner f0(δ−9) | C 1⊕g1(δ−7) | 集合 S | mex | 主張 f0(δ−8) |
|---|---|---|---|---|---|---|
| even, δ ≤ 0 | f0(odd ≤ −7)=1 | f0(odd ≤ −9)=1 | 1⊕g1(odd ≤ −7)=1⊕0=1 | {1} | 0 | f0(even ≤ −8)=0 ✓ |
| δ = 2 | f0(−5)=1 | f0(−7)=1 | 1 | {1} | 0 | f0(−6)=0 ✓ |
| δ = 4 | f0(−3)=1 | f0(−5)=1 | 1 | {1} | 0 | f0(−4)=0 ✓ |
| δ = 6 | f0(−1)=1 | f0(−3)=1 | 1 | {1} | 0 | f0(−2)=0 ✓ |
| δ = 8 (C 核) | f0(1)=2 | f0(−1)=1 | 1⊕g1(1)=3 | {2,1,3} | 0 | f0(0)=0 ✓ |
| δ = 10 (comp 核) | f0(3)=0 | f0(1)=2 | 1⊕g1(3)=1⊕1=0 | {0,2} | 1 | f0(2)=1 ✓ |
| even, δ ≥ 12 | f0(odd ≥ 5)=0 | f0(odd ≥ 3)=0 | 1⊕g1(odd ≥ 5)=1⊕1=0 | {0} | 1 | f0(even ≥ 4)=1 ✓ |
| odd, δ ≤ 7 | f0(even ≤ 0)=0 | f0(even ≤ −2)=0 | 1⊕g1(even ≤ 0)=1⊕1=0 | {0} | 1 | f0(odd ≤ −1)=1 ✓ |
| δ = 9 (核) | f0(2)=1 | f0(0)=0 | 1⊕g1(2)=1⊕0=1 | {1,0} | 2 | f0(1)=2 ✓ |
| odd, δ ≥ 11 | f0(even ≥ 4)=1 | f0(even ≥ 2)=1 | 1⊕g1(even ≥ 4)=1⊕0=1 | {1} | 0 | f0(odd ≥ 3)=0 ✓ |

全 δ 場合で mex = 主張値。■

### §2.4 T-BDT8 (z8 bed) の証明

主張 b8(R,j): 2·[R odd] (R < 8); f0(j−8) (R ≥ 8)。

R = 0: 0 ✓ (= 層値 = 主則 f0(−2m−8)=0)。
R = 1 (m=1, j=−1): B: v(1,9,0)=0; C: 1⊕[b7 at R−1=0 = 0]=1 → {0,1} →
mex **2** ✓。
R = 2: (m=1,j=0): B: v(1,9,1)=2; C: 1⊕[b7 at R−1=1: 層値 2]=3 → {2,3} →
**0** = 層値 = 主則 f0(j−8)=f0(−8)=0 ✓。(m=2,j=−2): fall: pair (1,2)@z8 層値
at 1: 2; C: 1⊕[b7 at R−1=1 (m=2, j−1=−3): 層値 2]=3 → {2,3} → 0 ✓。
R = 3 (m ≥ 2): fall: pair (m−1,m)@z8 層値 at 2: 0; C: 1⊕[b7 at 2: 層値 0]=1 →
{0,1} → **2** ✓。R = 4: fall at 3: 2; C: 1⊕[b7 at 3: 2]=3 → {2,3} → **0** ✓
(主則 f0(j−8): j = 4−2m even → j−8 even ≤ −8 → 0 と一致)。R = 5:
fall at 4: 0; C: 1⊕[b7 at 4: 0]=1 → {0,1} → **2** ✓。R = 6: fall at 5: 2;
C: 1⊕[b7 at 5: 2]=3 → {2,3} → **0** ✓ (主則: j = 6−2m even → j−8 ≤ −4 → 0 ✓)。
R = 7: fall at 6: 0; C: 1⊕[b7 at 6: 層値 0]=1 → {0,1} → **2** ✓ (z7 床層域は
R < 8 なので budget 6 は層値 — 域を跨がない)。

**R = 8 (継ぎ目, m ≥ 4, j = 8−2m even ≤ 0)**: 子 budget 7:
- fall: pair (m−1,m)@z8 層値 at 7 → 2。
- C: 1 ⊕ b7 at budget 7 (z7 床層値 at 7: 2) → 3。
- 集合 {2,3} → mex **0** = 主則 f0(j−8): j even → j−8 even ≤ −8 → 0 ✓。

**R = 9 (m ≥ 4, j odd)**: 子 budget 8 (両面とも主則域):
- fall: pair (m−1,m)@z8 main at δ_c = j+1 → f0(j+1−8) = **f0(j−7)**:
  j odd → j−7 even ≤ −6 → 0。
- C: 1 ⊕ b7 at budget 8 (main) 座標 j−1: g1((j−1)−6) = g1(j−7): j odd →
  j−7 even ≤ −8 → g1 = 1 → C = **0**。
- 集合 {0} → mex **1** = 主則 f0(j−8): j odd → j−8 odd ≤ −9 → 1 ✓。

**R ≥ 10 (主則)**: 子は主則読み:
- fall: **f0(j−7)**; C: 1 ⊕ g1(j−7) = **f0(j−7)** for j ≠ 8 (j ≤ 0 常に)。
- mex({f0(j−7)}) — 単一値 v なら mex = 0 (v ≠ 0), 1 (v = 0):
  - j odd: f0(even ≤ −8)=0 → mex **1** = 主張 f0(odd ≤ −7)=1 ✓。
  - j even: f0(odd ≤ −3)=1 → mex **0** = 主張 f0(even ≤ −6)=0 ✓。■

### §2.5 L-BU7G / L-BU8G の閉形式からの導出

K0832 closed form v(x,z,R) から直接読む。token plane 8, w ≥ 2:
- w ≥ 9: region 1 ≤ 8 ≤ w−1, m = q_odd(8) = 7: t ≤ 7: 2·[t odd] (層 t < 8
  と一致、t = 7 の 2 = g1(1) は層核と主則核の境界値の一致 — K1289 L-BU4G・
  K1290 L-BU6G と同一); 7 < t < w+8 (t ≤ w で常に): (t+8)%2 = t%2:
  t 偶 → 0 = g1(t−6) (even ≥ 2 → [odd]=0), t 奇 → 1 = g1(t−6)
  (odd ≥ 3 → [odd]=1)。t = 6,7 ≤ m 層内。
- w = 8: region z = x: t 奇 ≤ 15: 2; t 偶 ≤ 7: 0 (= 層値); t=8: 偶 > 7 →
  x%2 = 0 = g1(2) = 0 (主則核 cell の一致)。
- w ∈ {2,...,7}: region z ≥ x+1: m = q_odd(w) ≤ 7: t ≤ m: 2·[t odd] (層内);
  t > m, t ≤ w: w%2 — w 偶 {2,4,6} で t = w が該当するのみで値 0 = 層値
  2·[w odd] = 0 と一致、w 奇は m = w で不使用。全域層値 (t ≤ w ≤ 7 < 8)。
token plane 9, w ≥ 2:
- w ≥ 10: m = q_odd(9) = 9: t ≤ 9: 2·[t odd] (t < 8 層; t=8: 0 = f0(0) =
  主則核の一致; t=9: 2 = f0(1) = 核の一致); 9 < t ≤ w: (t+9)%2 = 1−t%2:
  t 偶 → 1 = f0(t−8) (even ≥ 2 → [even]=1), t 奇 → 0 = f0(t−8)
  (odd ≥ 3 → 0)。
- w = 9: region z = x: t 奇 ≤ 17: 2 (t=9: 2 = f0(1) ✓); t 偶 ≤ 8: 0
  (t=8: 0 = f0(0) ✓); t ≤ 7 は層値と一致。
- w ∈ {2,...,8}: region z ≥ x+1: m = q_odd(w) ≤ 7: t ≤ m: 2·[t odd];
  t > m, t ≤ w: w%2 (w 偶: t=w のみ 0 = 層値 ✓; w=8: m=7, t=8: w%2 = 0 =
  f0(0) = 0 ✓; w 奇は m = w で不使用)。
全 twist は機体 D9(a)/(b) が closed form × engine × 主張表の三方で w ≤ 30 照合。■

### §2.6 well-founded 性 (まとめ)

packet {T-PDT7, T-BDT7, T-PDT8, T-BDT8} の証明は単一の R 強帰納:
全子は budget R−1 (engine の子定義)。面間参照: z7 の C 子 = z6 (K1290, 全 R
無条件); z8 の C 子 = z7 (packet, budget R−1); 床 C 子 = plane−1 床
(z7 床の C 子 = b6 = K1290 既刊; z8 床の C 子 = b7 = packet T-BDT7,
budget R−1)。B 子は K0832 closed form (L-BU7G/L-BU8G + w=1 edge {0,2}) で
帰納外。帰納は R のみで整礎 (m, g に依らない子値表)。各 R での子値の列挙は
§2.1–§2.4 の場合表 (R ≤ 8 は層定数読みの列挙、R ≥ 9 は δ parity の場合表)
で全ての (m, g, k) を尽くす。層厚 8 世代の新しい構造は §2.1/§2.2 R=7 の
「C 子 budget 6 が下位面 (z6, 層厚 6) の主則域を読む」層域横断が初出
(値は δ₂ parity 固定により定数 0 に落ちる) のと、§2.3/§2.4 の
「z8 の層域横断がゼロ (z7 と層厚が一致)」の対である。

### §2.7 反例検査の誠実な記述

- 例外層 R ∈ {0,...,7} の値 2·[R odd] は宣言前探索 (§3 X1–X4) で (R,δ) 平面
  で mixed cell 0 として先に特定済み (K1289 の「slope trap」教訓を適用)。
- m 依存性・g 依存性は主張域内で一度も観測されていない (§3 Y1/Y2 広域)。
  主張は typed 証明による全称主張であり、census は照合である。

## §3 宣言前探索 (pre-declaration; explore_k1294.py / explore2_k1294.py 出力)

- X1/X3 (z7/z8 band m≤12 g≤25 k≥−60, (R,δ) 表): mixed (R,δ) cell それぞれ
  cells 468 中 0/0 (X2/X4 beds は 168 cell 中 0/0)。低 R 行 (R=0..7) が定数
  0/2/0/2/0/2/0/2 (層厚 8 の直接観測)。R=8 seam 行 (z7 は全 1 = g1(even ≤ 0)
  ・z8 は全 0 = f0(even ≤ −2))。R≥9 行が g1(δ−6) / f0(δ−8) に一致
  (核 cell z7 δ=7 → 2・z8 δ=9 → 2 を含む)。
- X2/X4 (beds m≤12 j∈[−30..0]): 同一の R 層構造・mixed 0/0。
- X5/X6: L-BU7G/L-BU8G 発現 census (w ≤ 30, t ≤ w; engine vs closed form vs
  plane-7/8 法則): bad 0/0 (1,972 checks)。w=1 edge: v(1,8,{0,1})={0,2},
  v(1,9,{0,1})={0,2}。
- X7: sharpened C-PSF′ probe (z=0..10, m≤10 g≤20 k≥−50 の dedup (R,δ) 320
  cell × 11 面): bad 全 0 (z9/z10 は OBS として — K1290 X7 の z≤8 を 2 面拡張)。
- X8: typed 子 self-check (宣言前): 子を申立テーブル (z7/z8 申立 + K1290 z5/z6
  既刊) + closed form からのみ構成した mex が申立値・engine と一致するかを
  slices 3,878 点・beds 228 点で確認: bad 0/0 (手証明 §2 構文の宣言前検証)。
- Y1/Y2: z7/z8 band+beds の wide census (D1–D4 と同一 box): 8,928/360 × 2 bad 0。
- Y3/Y4/Y5: z9/z10 OBS (band 4,500 × 2, beds 120 × 2, far-row m=12 216 × 2,
  low-R (R<10) hist {0:346, 2:340} × 2): cpsf 予測 vs engine bad 全 0
  (有限観測・全称主張なし)。
- Y6: ordered vs canonical engine 交差 (z=7..10, 各 464 cells): mismatch 全 0。
- Y7: L-BU7G/L-BU8G (w ≤ 40) bad 0 + 発現 L-BU9G (v(w,10,t) = plane-9 law:
  2·[t odd] (t<10) / g1(t−8))・L-BU10G 発現 (v(w,11,t): 2·[t odd] (t<10) /
  f0(t−10)) を w ≤ 40 probe: bad 0 (z=10,11 token plane は OBS)。
- Y8: T-TWIN identity d∈[−260..260] bad 0; z=0..12 dedup (R,δ) sweep:
  全 13 面 mixed 0・cpsf bad 0 (**C-PSF′ が plane 12 まで観測拡張**・K1290
  Y8 の z≤10 から 2 面拡張)。

## §4 機体宣言 (machine declaration, publish-then-execute)

`verify_k1294.py` (sha256 publish 時に kit で宣言 =
`b3974b63e43a67c32689d247377558d34720a66d303b54bda5485be5c69edf81`・engine
pin `bd5f22e415a78368c9b798296bc84948d5637decbf3c21a92404d45fb12e3a92`
startup gate 内蔵・embed は K1138/K1282..K1290 と同一 bytes)。バッテリ:

| # | 内容 | 期待 count |
|---|---|---|
| D1 | z7 band census (m≤14, g≤25, k∈[max(−30,−2m−g),0]) | 8,928 |
| D2 | z7 beds census (m≤18, j∈[−36..0]) | 360 |
| D3 | z8 band census (D1 box) | 8,928 |
| D4 | z8 beds census (D2 box) | 360 |
| D5 | typed z7 slices (m≤10, g≤14, k≥−14): typed mex == claim == engine | 1,939 |
| D6 | typed z7 beds (m≤10, j≥−16) | 114 |
| D7 | typed z8 slices (D5 box) | 1,939 |
| D8 | typed z8 beds (D6 box) | 114 |
| D9 | (a) L-BU7G 493 + (b) L-BU8G 493 + (c) K1290 anchors T-PDT5/T-BDT5/T-PDT6/T-BDT6 再照合 4,690 + (d) K1289 anchors T-PDT3/T-BDT3/T-PDT4/T-BDT4 再照合 4,690 + (e) K1288 anchors T-PDT1/T-BDT1/T-PDT2/T-BDT2 再照合 4,690 + (f) K1286 anchors T-PD0/T-B0 再照合 2,345 + (g) sharpened C-PSF′ identity sweep w=0..8 (pair box + bed box) 21,105 + (h) T-TWIN algebra d∈[−100..100] 201 + (i) closed form vs both engines (x≤16, z∈2..9, R∈x+1..x+4) 960 + (j) B-exit w=1 edge values (v(1,8,t)/v(1,9,t), t≤1) 4 | 39,671 |
| D10 | cross-engine canonical vs ordered (z7/z8 pair m≤8, g≤10, k≥−8 + beds m≤8 j≥−8) | 1,516 |
| D11 | OBS: z9/z10 band (m≤10,g≤20,k≥−50) 4,500×2 + beds (m≤10,j≥−24) 120×2 + far-row m=12 216×2 + low-R (R<10) hist probes 686×2 + L-BU9G/L-BU10G plane-token sweep (z=10,11, w≤30) 493×2 + dedup (R,δ) sweep z=0..12 (320 × 13) 4,160 | 16,190 |

**総計 80,059 比較点・期待 overall_bad = 0** (宣言前 predry 4 走で
counts [8928,360,8928,360,1939,114,1939,114,39671,1516,16190]・
bad 全 0・stdout byte-identical sha256
`c424a680cb2b9711893edac4029c61faca253afe103d0e0d978554d572e8af50`
を確認済み)。

変異電池 (公式 run の前に期待値を宣言):
- `--tamper-engine`: rc=2・mutated sha `0ea47a80…` ≠ pin (K1282–K1290 と同一変異)。
- `--tamper=z7s`: rc=1, D1 bad 8,928。`--tamper=z7b`: rc=1, D2 bad 360。
- `--tamper=z8s`: rc=1, D3 bad 8,928。`--tamper=z8b`: rc=1, D4 bad 360。
- 他バッテリ (D5–D11) は census クレームの flip の影響を受けない
  (typed 側は flip されないので D5–D8 の 3-way 照合は主張値のまま engine と
  一致する; 対角の影響は D1–D4 の bad のみ)。

公式 4 走: 同一 cwd (PYTHONHASHSEED random/1) × 2 + 隔離 tree (env -i,
PYTHONHASHSEED 99/7) × 2、stdout byte-identical が要求 (fetch-back bytes から
走行)。

## §5 open 登録 (有限観測・予想と次課題; 全称主張なし)

- **O9″ (C-PSF′ の w 帰納 — K1290 O9′ update)**: 全称は w ∈ {0..8} まで
  (本項で +2)。**Y8 dedup sweep で w=9..12 が 320 cell × 4 面で mixed 0・
  cpsf bad 0 に拡張** (K1290 の z≤10 から +2)。次の単一オーナー候補は
  T-PDT9/T-BDT9・T-PDT10/T-BDT10 (z9/z10 typed・§2 と同一構文: C 子は本項
  z7/z8 定理 (全 R・例外層込み) を参照。z9 の層厚は L(9)=L(10)=10。層域
  横断は本項 §2.1/§2.2 の R=7 型が幅広くなる: z9 では C 子 budget 8,9 が
  z8 主則域 (R ≥ 8) を読む (2 列)・z10 では C 子 budget 0..9 全てが z9
  層域内 (横断ゼロ・z8 型)。層核の mex{0,1}=2/mex{2,3}=0 機構は
  w 非依存と root 交代なし)。
- **O10″ (L-BUzG 族の全称形 — K1290 O10′ update)**: 9 枝 (z+1 = 1..9) まで
  全称。**L-BU9G/L-BU10G (token plane 10/11 = plane-9/10 則: 2·[t odd]
  (t<10) / g1(t−8) (z=10), f0(t−10) (z=11)) を w ≤ 40 で発見・OBS 登録**
  (Y7・D11)。closed form の region 計算で一般 w に拡張可能な見込み
  (q_odd(z) が層核の両端構造に対応。本項 §2.5 の境界一致 3 型が世代毎に
  再現: t = z−1 で 2 = T_w(1) 核一致・t = z−1 − (z−1)%2… スキームは
  O10″ の正式命題化対象)。
- **O11 (例外定数層の一般理論 — K1290 O11 継続)**: 層厚 L(w) = 2⌈w/2⌉ が
  w = 0..8 全称 + w = 9..12 OBS (dedup)。層の中の子は (w, w−1) の層定数を
  R−1 パリティで読むのみで δ 非依存 — w=3 法則が w=7,8 でも同一に成立
  (§2 の R ≤ 8 cases は w 非依存の mex{0,1}=2 / mex{2,3}=0 機構・第 4 世代)。
  **本項で初の「層域横断」型 (z7 R=7 の C 子 budget 6 が z6 主則域を読む
  (値は parity 固定で定数)) と「横断ゼロ」型 (z8: 層厚一致の対面) の
  2 型が出揃った** — 一般 w 帰納は (w mod 4) でこの 2 型に分類できる
  見取り (O9″ と統合)。
- **O12 (11×11 giant 枝刈り格子)**: T-PD0 (K1286) + K1288 + K1289 + K1290 +
  本項で、ペア面 z ∈ {0..8} の対角下全域 k ≤ 0 が R 例外層込みで O(1) 即値
  評価可能に (band は δ と R の 2 変数・床は 1 変数)。境界側格子の拡張として
  巨大探索レーンへ記録 (採用判断はオーナー)。
- **O13 (K1287 O1 残部)**: (i) SLB2/SLB3 単一層族・(ii) L/Am frontier 全称化
  は非接触のまま (K1291+ 候補・K1289 §5 O12/K1290 §5 O13 と同一)。

## §6 主張の区別 (過大主張の防止)

- 定理 (universal, §2 手証明): T-PDT7, T-BDT7, T-PDT8, T-BDT8, L-BU7G,
  L-BU8G, C1 (K1290 O9′ z7/z8 部分解決の記述), C2 の w ≤ 8 部分
  (sharpened C-PSF′ の w については既刊+本項の集約)。
- corollary (universal だが既刊の言い換え): C2/C3 の既刊分の再表現。
- 有限観測 (OBS): D11 (z9/z10 band/beds/far-row/lowR hist・L-BU9G/L-BU10G・
  dedup sweep z=9..12)・§3 X/Y。
- census 点数 80,059 は定理の実機照合であり全称性の主張ではない。
- 標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は
  全て UNKNOWN のまま。verdict 不消費。

(宣言ノート本文ここまで。実装は publish-then-execute: 本ノートが最先行。
kit → fetch-back → 公式 4 走 → 変異電池 → 成果物出版 → K item → README bullet
→ run log の順に進める。)
