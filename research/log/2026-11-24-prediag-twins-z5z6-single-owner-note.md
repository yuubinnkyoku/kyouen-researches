# 単一オーナー宣言 K1290: pre-diag 双生児 z5/z6 の全称確定
(T-PDT5/T-BDT5 + T-PDT6/T-BDT6 — K1289 O8 の取得・sharpened C-PSF′ の w=5,6 実例化・z7/z8 OBS)

## §0 状態と採番 (single-owner protocol)

- 観測 HEAD (着手時): `68483d7da195bba2f41abf58d8e3c7d5e95c9016` (2026-11-24T13:26:22Z・Part DH takeover-2 B wave1。非接触: n11 central-reply thirdimpl レーン)。
- 本宣言 push 直前再取得 HEAD: 後段の機械記録に記載 (2026-11-24T13:4xZ・再取得タイミングでの最新 main)。
- K1290 空き確認: `research/knowledge/items/` の最新 K item = K1289 `518c4366` (12:28:14Z)。コミットログに K1290 宣言 0 件・対抗宣言なし (2026-11-24T13:3xZ 時点・本宣言 push 直前に再確認)。K1289 item 中の「K1290+ 候補」記述は番号取得ではなく未着手領域の列挙。
- 領域: K1289 lane が §5 O8 として登録した T-PDT5/T-BDT5・T-PDT6/T-BDT6 (z5/z6 pre-diag typed 全称) を取得。K1289 O8 を解決し O6/O9 側の sharpened C-PSF′ を w=5,6 まで全称実例化、z7/z8 (O9 の次の観測面) を OBS 登録する。K1286/K1287/K1288/K1289 の全定理に触れない (内面 k>0・multi-c web は非接触)。
- 規約: verdict 不消費・標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は全て UNKNOWN のまま。

## §1 主張 (claims)

座標の規約は K1286/K1288/K1289 と同一: ペア局面 H(R;(m,m+g);z)、対角座標 k := R−2m−g、
δ := R−2m、バンド域 k ≤ 0 (0 ≤ R ≤ 2m+g)。床 (bed) は (m,m) 双 Token: 
b_z(j) := H(2m+j;(m,m);z), j ≤ 0。f0 は K1286 出版の対角下バンド 1 次元崩壊関数、
g1 は K1288 出版の偶奇双生児 (T-TWIN: g1(d) = 1 ⊕ f0(d) for d ≠ 1, g1(1) = f0(1) = 2):

- f0(d) = 2 (d=1); [d odd] (d ≤ 0); [d even] (d ≥ 2)
- g1(d) = 2 (d=1); [d even] (d ≤ 0); [d odd] (d ≥ 2)

**定理パッケージ (universal, 量子化: ∀m ≥ 1, ∀g ≥ 1, 全ての有効 cell, 値は m も g も経由しない):**

- **T-PDT5 (z5 band)**: H(R;(m,m+g);5) = 2·[R odd] (R < 6); g1(δ−4) (R ≥ 6)。
- **T-BDT5 (z5 bed)**: b5(j) = 2·[R odd] (R < 6, R = 2m+j); g1(j−4) (R ≥ 6)。
- **T-PDT6 (z6 band)**: H(R;(m,m+g);6) = 2·[R odd] (R < 6); f0(δ−6) (R ≥ 6)。
- **T-BDT6 (z6 bed)**: b6(j) = 2·[R odd] (R < 6); f0(j−6) (R ≥ 6)。
  (層厚 L(5) = L(6) = 2⌈w/2⌉ = 6。z6 の偶数例外 cell (R=0,2,4) は主則 f0(δ−6) 
  と値が一致する (f0(even ≤ −6)=0, R=4: δ even ≤ 2 → δ−6 even ≤ −4 → 0) ので
  「R < 6 で 2·[R odd]」として統一できる。z5 の偶数 cell (R=0,2,4) は主則
  g1(δ−4) = 1 と衝突するので層の上書きとして本物である − K1289 の z3/z4 と
  同一の役割分担 (奇数平面の層は实質、偶数平面の層は見かけ上主則と一致)。)

**補題 (closed-form から機械照合 w ≤ 30):**

- **L-BU5G**: v(w,6,t) = 2·[t odd] (t < 6); g1(t−4) (6 ≤ t ≤ w), ∀w ≥ 2
  (単一 Token w を平面 6 に置いた局面 = B-exit 子の値 = plane-5 則のフル形式)。
- **L-BU6G**: v(w,7,t) = 2·[t odd] (t < 6); f0(t−6) (6 ≤ t ≤ w), ∀w ≥ 2。
  (t=6 の 0 = f0(0) は主則核、w=7, t=7 の 2 = f0(1) は t ≤ q_odd(7) 層と合致
  — K1289 L-BU4G の「境界値の一致」と同一構造。)

**系 (corollaries / subsumption):**

- **C1 (K1289 O8 RESOLVED)**: K1289 O5/O8 が予測として観測した z5/z6
  (D11/Y3–Y5 の OBS・low-R hist {0:215, 2:214}) は本項で全称定理化。
  層厚 6・主則 g1(δ−4) (z5) / f0(δ−6) (z6) が例外層込みで確定する。
- **C2 (sharpened C-PSF′ = K1289 O6 の w=5,6 実例化)**: 統一形式
  **H(R;(m,m+g);w) = 2·[R odd] (R < 2⌈w/2⌉); T_w(δ − 2⌊w/2⌋) (R ≥ 2⌈w/2⌉)**,
  T_w = g1 (w 奇数) / f0 (w 偶数)。この項で w ∈ {5,6} が全称証明され、
  w ∈ {0} (K1286), {1,2} (K1288), {3,4} (K1289), {5,6} (本項) と代数的に同一
  (verify D9(f) が w=0..6 全 7 面で機械照合)。w ∈ {7,8} は D11 有限 OBS のみ。
  層厚 L(w) = 2⌈w/2⌉ の一般 w 帰納は未解決 (§5 O9′)。
- **C3 (B-exit 均一性の族)**: 単一 Token @ plane z+1 は plane-z 則を継承する:
  L-BU0 (K1286)・L-BU1G/L-BU2G (K1288)・L-BU3G/L-BU4G (K1289) に続き本項の
  **L-BU5G/L-BU6G (plane-5 / plane-6)** で 7 枝が出揃った (w=7,8 token plane
  (L-BU7G/L-BU8G 相当) は D11 OBS・全称主張なし)。

**§1.1 K1289 内面との境界 (重複なし)**: K1289 D11/Y3–Y5 の z5/z6 OBS は
sharpened C-PSF′ 予測との一致 (band 各 4,500 点・bad 0) を有限観測として
持っていた。本項の主張は R 例外層値込みの全 cell を含み、K1289 が open に
した「z5/z6 の typed 証明」を定理として確定する。K1286 T-Z1 k=1 内面・
K1287 F2 web の内面 k>0 には一切触れない。K1289 の T-PDT3/T-PDT4 は
z5 の C 子として外部参照 (既刊・全 R 無条件) するのみで再証明しない。

## §2 手証明 (typed child mex, single R strong induction)

### §2.0 型付き子の分類 (pair @ plane z)

K1289 §2.0 と同一 (engine 定義から直接)。Budget R の局面 (m,m+g)@z 
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
値 {v(1,z+1,0), v(1,z+1,1)} = {0,2} — closed form・D9(i) 照合)、**C**
(1 ⊕ 床 (m,m)@(z−1), budget R−1, 床座標 j−1)。

well-founded 性: 単一の packet {T-PDT5, T-BDT5, T-PDT6, T-BDT6} 全体で R に
ついての強帰納。全ての子の budget は R−1 であり、面間参照は常に下位 budget
(z5 の C 子は z4 = K1289 既刊で全 R 無条件、z6 の C 子は z5 = packet 内で
budget R−1)。B 子・床 B 子は closed form (帰納外)。基底 R = 0: 選択肢集合は空、
mex ∅ = 0 (4 定理すべての主張値と整合: 層値 2·[0]=0・主則 f0/g1(even ≤ −4/−6)=0)。

### §2.1 T-PDT5 (z5 band) の証明

主張値 V(R,δ) := 2·[R odd] (R < 6); g1(δ−4) (R ≥ 6)。

**R = 0**: mex ∅ = 0 = 層値。

**R ∈ {1,2,3,4,5} (例外層)**: 子は全て budget R−1 ≤ 4 < 6 (z5 側の層定数) 
または z4 側 (層 R−1 < 4 / 主則 R−1 = 4) を読む:
- fall/compress/corner 子: z5 band/bed 層値 at R−1 = 2·[(R−1) odd] →
  R−1 ∈ {0,1,2,3,4} で 0/2/0/2/0 (子の δ_c に依らず定数)。
- B 子 (m=1): L-BU5G at t = R−1 < 6 → 2·[t odd] → 同一の 0/2/0/2/0。
- C 子: 1 ⊕ [z4 at (R−1)]: R−1 ∈ {0,1,2,3}: z4 層値 2·[(R−1) odd] → 
  C = 1 ⊕ (0/2/0/2) = 1/3/1/3; R−1 = 4: z4 主則 f0(δ₂−4), δ₂ = 4−2m → 
  δ₂−4 = −2m even ≤ −2 → f0 = 0 → C = 1。

よって選択肢集合 (fall/compress/corner/B は全て同値なのでどの型が現れても同一):
- R=1: {0, 1} → mex = **2** = 2·[1] ✓
- R=2: {2, 3} → mex = **0** ✓
- R=3: {0, 1} → mex = **2** ✓
- R=4: {2, 3} → mex = **0** ✓
- R=5: {0, 1} → mex = **2** ✓

(層値の読みは全て R−1 定数なので m,g 場合分け不要 — K1289 §2.1 と同一機構。)

**R = 6 (主則への継ぎ目)**: 子 budget 5 (z5 層値 2):
- fall/compress/corner: z5 層値 at 5 → **2**。
- B (m=1): L-BU5G t=5 < 6 → **2**。
- C: 1 ⊕ [T-PDT4 at (R−1)=5, main]: f0(δ₂−4), δ₂ = 5−2m odd → δ₂−4 odd ≤ −1 →
  f0 = 1 → C = **0**。
選択肢集合 = {0, 2} → mex = **1**。主張値: g1(δ−4) at R=6 (δ even, δ ≤ g):
δ−4 even ≤ 0 → g1 = 1 ✓。

**R ≥ 7 (主則)**: 子は全て主則読み (budget R−1 ≥ 6):
- fall 子: g1(δ_c − 4) at δ_c = δ+1 → **g1(δ−3)**。
- B 子 (m=1): L-BU5G main at t = R−1 = δ+1 → g1(t−4) = **g1(δ−3)**
  (fall 子と同じ表を再生 — K1288/K1289 の B-exit 再生構造の z5 版)。
- compress 子: g1(δ_c−4) at δ_c = δ−1 → **g1(δ−5)**。
- corner 子 (g=1): 床 T-BDT5 main at j_c = δ−1: g1(j_c−4) = **g1(δ−5)**
  (compress 子と同値)。
- C 子: 1 ⊕ f0(δ₂−4) at δ₂ = δ−1 → **1 ⊕ f0(δ−5)** = g1(δ−5) unless δ = 6
  (δ−5 = 1 のとき C = 1 ⊕ f0(1) = 3)。

場合分け (δ ≡ R (mod 2), δ ≤ g, B 子は m=1 すなわち δ = R−2 の行のみに出現
するが値は fall と同一なので場合分け不要):

| δ (parity, range) | fall/B g1(δ−3) | comp/corner g1(δ−5) | C 1⊕f0(δ−5) | 集合 S | mex | 主張 g1(δ−4) |
|---|---|---|---|---|---|---|
| odd, δ ≤ −1 | g1(even ≤ −4)=1 | g1(even ≤ −6)=1 | 1⊕f0(even ≤ −6)=1⊕0=1 | {1} | 0 | g1(odd ≤ −5)=[even]=0 ✓ |
| δ = 1 | g1(−2)=1 | g1(−4)=1 | 1⊕f0(−4)=1⊕0=1 | {1} | 0 | g1(−3)=[even at −3]=0 ✓ |
| δ = 3 | g1(0)=1 | g1(−2)=1 | 1⊕f0(−2)=1⊕0=1 | {1} | 0 | g1(−1)=[even at −1]=0 ✓ |
| δ = 5 (核) | g1(2)=0 | g1(0)=1 | 1⊕f0(0)=1 | {0,1} | 2 | g1(1)=2 ✓ |
| δ = 7 | g1(4)=0 | g1(2)=0 | 1⊕f0(2)=1⊕1=0 | {0} | 1 | g1(3)=[odd]=1 ✓ |
| odd, δ ≥ 9 | g1(even ≥ 6)=0 | g1(even ≥ 4)=0 | 1⊕f0(even ≥ 4)=1⊕1=0 | {0} | 1 | g1(odd ≥ 5)=[odd]=1 ✓ |
| even, δ ≤ 0 | g1(odd ≤ −3)=0 | g1(odd ≤ −5)=0 | 1⊕1=0 | {0} | 1 | g1(even ≤ −4)=[even]=1 ✓ |
| δ = 2 | g1(−1)=0 | g1(−3)=0 | 1⊕f0(−3)=1⊕1=0 | {0} | 1 | g1(−2)=1 ✓ |
| δ = 4 | g1(1)=2 | g1(−1)=0 | 1⊕f0(−1)=1⊕1=0 | {2,0} | 1 | g1(0)=1 ✓ |
| δ = 6 (C 核) | g1(3)=1 | g1(1)=2 | 1⊕f0(1)=3 | {1,2,3} | 0 | g1(2)=0 ✓ |
| even, δ ≥ 8 | g1(odd ≥ 5)=1 | g1(odd ≥ 3)=1 | 1⊕f0(odd ≥ 3)=1⊕0=1 | {1} | 0 | g1(even ≥ 4)=[odd at even]=0 ✓ |

全 δ 場合で mex = 主張値。■

### §2.2 T-BDT5 (z5 bed) の証明

主張値 b5(R,j): 2·[R odd] (R < 6); g1(j−4) (R ≥ 6), R = 2m+j, j ≤ 0。

R = 0: mex ∅ = 0 ✓。

**R ∈ {1,2,3,4,5} (例外層)**: 子 budget R−1 ∈ {0..4}:
- fall 子 (m ≥ 2): pair (m−1,m)@z5 → 層値 2·[(R−1) odd]。
- B 子 (m = 1): v(1,6,t) at t = R−1 ∈ {0,1} → 0/2 = 2·[t odd]
  (m=1 は R ≤ 2 のみ: j = R−2 ≤ 0)。
- C 子: 1 ⊕ [b4 at (R−1), 床座標 j−1]: R−1 ∈ {0,1,2,3} (< 4): b4 層値
  2·[(R−1) odd] → C = 1 ⊕ (0/2/0/2); R−1 = 4: b4 main f0((j−1)−4) = f0(j−5):
  R=5 → j = 5−2m odd → j−5 even ≤ −4 → f0 = 0 → C = 1。

選択肢集合: R=1: {0,1} → 2 ✓; R=2: {2,3} → 0 ✓; R=3 (m ≥ 2, B なし):
{0, 1} → 2 ✓; R=4: {2, 3} → 0 ✓; R=5: {0, 1} → 2 ✓。

**R = 6** (m ≥ 3, j = 6−2m ≤ 0): 子 budget 5:
- fall: pair (m−1,m)@z5 層値 at 5 → **2**。
- C: 1 ⊕ b4 at budget 5 (main): f0((j−1)−4) = f0(j−5): j even → j−5 odd ≤ −1 →
  f0 = 1 → C = **0**。
- 集合 {2, 0} → mex = **1**。主張 g1(j−4): j even → j−4 even ≤ −4 → 1 ✓。

**R ≥ 7 (主則)**: 子は主則読み (child budget ≥ 6):
- fall: pair (m−1,m)@z5 main at δ_c = (R−1)−2(m−1) = j+1 → g1(j+1−4) = **g1(j−3)**。
- C: 1 ⊕ b4 main at 座標 j−1: f0((j−1)−4) = f0(j−5) → **1 ⊕ f0(j−5)**
  = g1(j−5) for j ≠ 6 (j ≤ 0 なので常に成立)。
- B 子は m = 1 で R ≤ 2 にしか現れない (主則域外)。

| j (parity) | fall g1(j−3) | C 1⊕f0(j−5) | 集合 | mex | 主張 g1(j−4) |
|---|---|---|---|---|---|
| odd, j ≤ −1 | g1(even ≤ −4)=1 | 1⊕f0(even ≤ −6)=1⊕0=1 | {1} | 0 | g1(odd ≤ −5)=[even]=0 ✓ |
| even, j ≤ 0 | g1(odd ≤ −3)=0 | 1⊕f0(odd ≤ −5)=1⊕1=0 | {0} | 1 | g1(even ≤ −4)=[even]=1 ✓ |

■ (bed は compress/corner 子を持たない — 両減算が同じ fall 子に縮退する。)

### §2.3 T-PDT6 (z6 band) の証明

主張値 V(R,δ) := 2·[R odd] (R < 6); f0(δ−6) (R ≥ 6)。

R = 0: mex ∅ = 0 = 層値 ✓ (主則 f0(δ−6) = f0(−2m−6) = 0 とも一致)。

**R ∈ {1,2,3,4,5}**: 子 budget R−1 ∈ {0..4} < 6:
- fall/compress/corner: z6 band/bed 層値 at R−1 → 0/2/0/2/0。
- B (m=1): L-BU6G at t = R−1 < 6 → 2·[t odd] → 同一。
- C: 1 ⊕ [z5 at (R−1)]: R−1 ∈ {0..4} < 6: z5 層値 2·[(R−1) odd] →
  C = 1/3/1/3/1 (R−1=4 は z5 層値 0 → C=1)。

集合: R=1: {0,1} → **2** ✓; R=2: {2,3} → **0** (= 主則 f0(δ−6): δ even ≤ 0,
δ−6 even ≤ −6 → 0 と一致 — 偶数 cell は層値と主則が同一); R=3: {0,1} →
**2** ✓; R=4: {2,3} → **0** (主則 f0(δ−6): δ even ≤ 2 → even ≤ −4 → 0 
と一致 ✓); R=5: {0,1} → **2** ✓。

**R = 6** (継ぎ目): 子 budget 5:
- fall/compress/corner: z6 層値 at 5 → **2**。
- B: L-BU6G t=5 < 6 → **2**。
- C: 1 ⊕ [z5 at (R−1)=5, 層値 2] → C = **3**。
- 集合 {2,3} → mex = **0**。主張: f0(δ−6) at δ even ≤ 4 → δ−6 even ≤ −2 → 0 ✓。

**R ≥ 7 (主則)**: 子は全て主則読み (child budget R−1 = R−1 ≥ 6):
- fall: f0(δ_c−6) at δ_c = δ+1 → **f0(δ−5)**。
- B (m=1): L-BU6G main at t = R−1 = δ+1: f0(t−6) = **f0(δ−5)** (fall 再生)。
- compress: **f0(δ−7)**; corner (g=1): T-BDT6 main at j_c = δ−1 → **f0(δ−7)**
  (compress 子と同値)。
- C: 1 ⊕ g1(δ₂−4) at δ₂ = δ−1 → **1 ⊕ g1(δ−5)** = f0(δ−5) for δ ≠ 6
  (1 ⊕ g1(x) = f0(x) except x=1; δ=6 のとき 3)。

| δ (parity, range) | fall/B f0(δ−5) | comp/corner f0(δ−7) | C 1⊕g1(δ−5) | 集合 S | mex | 主張 f0(δ−6) |
|---|---|---|---|---|---|---|
| even, δ ≤ 0 | f0(odd ≤ −5)=1 | f0(odd ≤ −7)=1 | 1⊕g1(odd ≤ −5)=1⊕0=1 | {1} | 0 | f0(even ≤ −6)=0 ✓ |
| δ = 2 | f0(−3)=1 | f0(−5)=1 | 1⊕g1(−3)=1⊕0=1 | {1} | 0 | f0(−4)=0 ✓ |
| δ = 4 | f0(−1)=1 | f0(−3)=1 | 1⊕g1(−1)=1⊕0=1 | {1} | 0 | f0(−2)=0 ✓ |
| δ = 6 (C 核) | f0(1)=2 | f0(−1)=1 | 1⊕g1(1)=3 | {2,1,3} | 0 | f0(0)=0 ✓ |
| δ = 8 (comp 核) | f0(3)=0 | f0(1)=2 | 1⊕g1(3)=1⊕1=0 | {0,2} | 1 | f0(2)=1 ✓ |
| even, δ ≥ 10 | f0(odd ≥ 5)=0 | f0(odd ≥ 3)=0 | 1⊕g1(odd ≥ 5)=1⊕1=0 | {0} | 1 | f0(even ≥ 4)=1 ✓ |
| odd, δ ≤ 5 | f0(even ≤ 0)=0 | f0(even ≤ −2)=0 | 1⊕g1(even ≤ 0)=1⊕1=0 | {0} | 1 | f0(odd ≤ −1)=1 ✓ |
| δ = 7 (核) | f0(2)=1 | f0(0)=0 | 1⊕g1(2)=1⊕0=1 | {1,0} | 2 | f0(1)=2 ✓ |
| odd, δ ≥ 9 | f0(even ≥ 4)=1 | f0(even ≥ 2)=1 | 1⊕g1(even ≥ 4)=1⊕0=1 | {1} | 0 | f0(odd ≥ 3)=0 ✓ |

(z5 版と対称に、C 核 δ=6 では C=3 が・comp 核 δ=8 では f0(1)=2 が選択肢集合
に入り、mex を主張値に落とす。全 δ 場合で mex = 主張値。■)

### §2.4 T-BDT6 (z6 bed) の証明

主張 b6(R,j): 2·[R odd] (R < 6); f0(j−6) (R ≥ 6)。

R = 0: 0 ✓ (= 層値 = 主則 f0(−2m−6)=0)。
R = 1 (m=1, j=−1): B: v(1,7,0)=0; C: 1⊕[b5 at R−1=0 = 0]=1 → {0,1} →
mex **2** ✓。
R = 2: (m=1,j=0): B: v(1,7,1)=2; C: 1⊕[b5 at R−1=1: 層値 2]=3 → {2,3} → **0**
= 層値 = 主則 f0(j−6)=f0(−6)=0 ✓。(m=2,j=−2): fall: pair (1,2)@z6 層値 at 1: 2;
C: 1⊕[b5 at R−1=1 (m=2, j−1=−3): 層値 2]=3 → {2,3} → 0 ✓。
R = 3 (m ≥ 2): fall: pair (m−1,m)@z6 層値 at 2: 0; C: 1⊕[b5 at 2: 層値 0]=1 →
{0,1} → **2** ✓。R = 4: fall at 3: 2; C: 1⊕[b5 at 3: 2]=3 → {2,3} → **0** ✓
(主則 f0(j−6): j = 4−2m even → j−6 even ≤ −6 → 0 と一致)。R = 5:
fall at 4: 0; C: 1⊕[b5 at 4: 0]=1 → {0,1} → **2** ✓。

**R = 6** (m ≥ 3): 子 budget 5:
- fall: pair (m−1,m)@z6 層値 at 5 → 2。
- C: 1 ⊕ b5 at budget 5 (z5 層値 2) → 3。
- 集合 {2,3} → mex **0** = 主則 f0(j−6): j = 6−2m even → j−6 even ≤ 0 → 0 ✓。

**R = 7** (m ≥ 3, j odd): 子 budget 6 (両面とも主則域):
- fall: pair (m−1,m)@z6 main at δ_c = j+1 → f0(j+1−6) = **f0(j−5)**:
  j odd → j−5 even ≤ −4 → 0。
- C: 1 ⊕ b5 at budget 6 (main) 座標 j−1: g1((j−1)−4) = g1(j−5): j odd →
  j−5 even ≤ −6 → g1 = 1 → C = **0**。
- 集合 {0} → mex **1** = 主則 f0(j−6): j odd → j−6 odd ≤ −7 → 1 ✓。

**R ≥ 8 (主則)**: 子は主則読み:
- fall: **f0(j−5)**; C: 1 ⊕ g1(j−5) = **f0(j−5)** for j ≠ 6 (j ≤ 0 常に)。
- mex({f0(j−5)}) — 単一値 v なら mex = 0 (v ≠ 0), 1 (v = 0):
  - j odd: f0(even ≤ −6)=0 → mex **1** = 主張 f0(odd ≤ −5)=1 ✓。
  - j even: f0(odd ≤ −3)=1 → mex **0** = 主張 f0(even ≤ −4)=0 ✓。■

### §2.5 L-BU5G / L-BU6G の閉形式からの導出

K0832 closed form v(x,z,R) から直接読む。token plane 6, w ≥ 2:
- w ≥ 7: region 1 ≤ 6 ≤ w−1, m = q_odd(6) = 5: t ≤ 5: 2·[t odd]; 5 < t < w+6
  (t ≤ w で常に): (t+6)%2 = t%2: t 偶 → 0 = g1(t−4) (even ≥ 6 → [odd]=0),
  t 奇 → 1 = g1(t−4) (odd ≥ 7 → [odd]=1)。t = 5 ≤ m: 2 = g1(1) 
  (層と主則の境界値の一致 — K1289 L-BU4G と同一)。
- w ∈ {2,...,6}: z ≥ x+1 region: m = q_odd(w): t ≤ m: 2·[t odd] (t ≤ 5 層);
  t > m: w%2 (必要なのは w=6, t=6: 0 = g1(2) = 0 ✓ のみ — 他は t ≤ m か
  t < 6 層内)。
token plane 7, w ≥ 2:
- w ≥ 8: m = q_odd(7) = 7: t ≤ 7: 2·[t odd]; 7 < t: (t+7)%2 = 1−t%2:
  t 偶 → 1 = f0(t−6) (even ≥ 2 → [even]=1), t 奇 → 0 = f0(t−6)
  (odd ≥ 3 → 0)。t = 7: 2 = f0(1) (境界一致)。
- w ∈ {2,...,7}: z ≥ x+1: m = q_odd(w) ≤ 7: t ≤ m: 2·[t odd]
  (t < 6 は層・t=6,7 は f0(0)=0, f0(1)=2 と一致); t > m && t ≤ w:
  w%2 (w=6,t=6: 0 = f0(0) ✓; w=7,t=6,7 ≤ m=7 なので不使用)。
全 twist は機体 D9(a)/(b) が closed form × engine × 主張表の三方で w ≤ 30 照合。■

### §2.6 well-founded 性 (まとめ)

packet {T-PDT5, T-BDT5, T-PDT6, T-BDT6} の証明は単一の R 強帰納:
全子は budget R−1 (engine の子定義)。面間参照: z5 の C 子 = z4 (K1289, 全 R
無条件); z6 の C 子 = z5 (packet, budget R−1); 床 C 子 = plane−1 床 (z5 床の
C 子 = b4 = K1289 既刊)。B 子は K0832 closed form (L-BU5G/L-BU6G + w=1 
edge {0,2}) で帰納外。帰納は R のみで整礎 (m, g に依らない子値表)。各 R での
子値の列挙は §2.1–§2.4 の場合表 (R ≤ 6 は層定数読みの列挙、R ≥ 7 は δ 
parity の場合表) で全ての (m, g, k) を尽くす。

### §2.7 反例検査の誠実な記述

- 例外層 R ∈ {0,...,5} の値 2·[R odd] は宣言前探索 (§3 X1–X4) で (R,δ) 平面
  で mixed cell 0 として先に特定済み (K1289 の「slope trap」教訓を適用)。
- m 依存性・g 依存性は主張域内で一度も観測されていない (§3 Y1/Y2 広域)。
  主張は typed 証明による全称主張であり、census は照合である。

## §3 宣言前探索 (pre-declaration; explore_k1290.py / explore2_k1290.py 出力)

- X1/X3 (z5/z6 band m≤12 g≤25 k≥−60, (R,δ) 表): mixed (R,δ) cell それぞれ
  cells 468 中 0/0 (X2/X4 beds は 168 cell 中 0/0)。低 R 行 (R=0..5) が定数 0/2/0/2/0/2 (層厚 6 の直接観測)。
  R≥6 行が g1(δ−4) / f0(δ−6) に一致 (core cell δ=5:2 / δ=7:2 を含む)。
- X2/X4 (beds m≤12 j∈[−30..0]): 同一の R 層構造・mixed 0/0。
- X5/X6: L-BU5G/L-BU6G 発現 census (w ≤ 30, t ≤ w; engine vs closed form vs
  plane-5/6 法則): bad 0/0 (1,972 checks)。w=1 edge: v(1,6,{0,1})={0,2},
  v(1,7,{0,1})={0,2}。
- X7: sharpened C-PSF′ probe (z=0..8, m≤10 g≤20 k≥−50 の dedup (R,δ) 320
  cell × 9 面): bad 全 0 (z7/z8 は OBS として — K1289 X7 の z≤6 を 2 面拡張)。
- Y1/Y2: z5/z6 band+beds の wide census (D1–D4 と同一 box): 8,928/360 × 2 bad 0。
- Y3/Y4/Y5: z7/z8 OBS (band 4,500 × 2, beds 120 × 2, far-row m=12 216 × 2):
  cpsf 予測 vs engine bad 全 0 (有限観測・全称主張なし)。
- Y6: ordered vs canonical engine 交差 (z=5..8, 各 464 cells): mismatch 全 0。
- Y7: L-BU5G/L-BU6G (w ≤ 40) + 発現 L-BU7G (v(w,8,t) = plane-7 law: 2·[t odd]
  (t<8) / g1(t−6))・L-BU8G 発現 (v(w,9,t): 2·[t odd] (t<8) / f0(t−8)) を w ≤ 40
  probe: bad 0 (z=8,9 token plane は OBS)。
- Y8: T-TWIN identity d∈[−260..260] bad 0; z=0..10 dedup (R,δ) sweep: 
  全 11 面 mixed 0・cpsf bad 0 (**C-PSF′ が plane 10 まで観測拡張**・K1289 
  Y8 の z≤6 から 4 面拡張)。

## §4 機体宣言 (machine declaration, publish-then-execute)

`verify_k1290.py` (sha256 publish 時に kit で宣言 =
`b86cdaf943106a78bc7abef5c9085a0a2e3d4c4fde9b60e9a5d02eabf6ced0fd`・engine
pin `bd5f22e415a78368c9b798296bc84948d5637decbf3c21a92404d45fb12e3a92`
startup gate 内蔵・embed は K1138/K1282..K1289 と同一 bytes)。バッテリ:

| # | 内容 | 期待 count |
|---|---|---|
| D1 | z5 band census (m≤14, g≤25, k∈[max(−30,−2m−g),0]) | 8,928 |
| D2 | z5 beds census (m≤18, j∈[−36..0]) | 360 |
| D3 | z6 band census (D1 box) | 8,928 |
| D4 | z6 beds census (D2 box) | 360 |
| D5 | typed z5 slices (m≤10, g≤14, k≥−14): typed mex == claim == engine | 1,939 |
| D6 | typed z5 beds (m≤10, j≥−16) | 114 |
| D7 | typed z6 slices (D5 box) | 1,939 |
| D8 | typed z6 beds (D6 box) | 114 |
| D9 | (a) L-BU5G 493 + (b) L-BU6G 493 + (c) K1289 anchors T-PDT3/T-BDT3/T-PDT4/T-BDT4 再照合 4,690 + (d) K1288 anchors T-PDT1/T-BDT1/T-PDT2/T-BDT2 再照合 4,690 + (e) K1286 anchors T-PD0/T-B0 再照合 2,345 + (f) sharpened C-PSF′ identity sweep w=0..6 (pair box + bed box) 16,415 + (g) T-TWIN algebra d∈[−100..100] 201 + (h) closed form vs both engines (x≤16, z∈2..7, R∈x+1..x+4) 720 + (i) B-exit w=1 edge values 4 | 30,051 |
| D10 | cross-engine canonical vs ordered (z5/z6 pair m≤8, g≤10, k≥−8 + beds m≤8 j≥−8) | 1,516 |
| D11 | OBS: z7/z8 band (m≤10,g≤20,k≥−50) 4,500×2 + beds (m≤10,j≥−24) 120×2 + far-row m=12 216×2 + low-R (R<8) hist probe 1,126 + L-BU7G/L-BU8G plane-token sweep (z=8,9, w≤30) 493×2 + dedup (R,δ) sweep z=0..10 (320 × 11) 3,520 | 15,304 |

**総計 69,553 比較点・期待 overall_bad = 0** (宣言前 predry 4 走で
counts [8928,360,8928,360,1939,114,1939,114,30051,1516,15304]・
bad 全 0・stdout byte-identical sha256
`e5359335de76dee83f38375f42b61ba6d8b0d23ea6875bb8f4da6b95aa3a9621`
を確認済み)。

変異電池 (公式 run の前に期待値を宣言):
- `--tamper-engine`: rc=2・mutated sha `0ea47a80…` ≠ pin (K1282–K1289 と同一変異)。
- `--tamper=z5s`: rc=1, D1 bad 8,928。`--tamper=z5b`: rc=1, D2 bad 360。
- `--tamper=z6s`: rc=1, D3 bad 8,928。`--tamper=z6b`: rc=1, D4 bad 360。
- 他バッテリ (D5–D11) は census クレームの flip の影響を受けない
  (typed 側は flip されないので D5–D8 の 3-way 照合は主張値のまま engine と
  一致する; 対角の影響は D1–D4 の bad のみ)。

公式 4 走: 同一 cwd (PYTHONHASHSEED random/1) × 2 + 隔離 tree (env -i,
PYTHONHASHSEED 99/7) × 2、stdout byte-identical が要求 (fetch-back bytes から
走行)。

## §5 open 登録 (有限観測・予想と次課題; 全称主張なし)

- **O9′ (C-PSF′ の w 帰納 — K1289 O9 update)**: 全称は w ∈ {0..6} まで
  (本項で +2)。**Y8 dedup sweep で w=7..10 が 320 cell × 4 面で mixed 0・
  cpsf bad 0 に拡張** (K1289 の z≤6 から +4)。次の単一オーナー候補は
  T-PDT7/T-BDT7・T-PDT8/T-BDT8 (z7/z8 typed・§2 と同一構文: C 子は本項
  z5/z6 定理を参照。z7 の層厚は L(7)=8 で新世代の層定数管理が必要)。
- **O10′ (L-BUzG 族の全称形 — K1289 O10 update)**: 7 枝 (z+1 = 1..7) まで
  全称。**L-BU7G/L-BU8G (token plane 8/9 = plane-7/8 則: 2·[t odd] (t<8) /
  g1(t−6) (z=8), f0(t−8) (z=9)) を w ≤ 40 で発見・OBS 登録** (Y7・D11)。
  closed form の region 計算で一般 w に拡張可能な見込み (q_odd(z) が層核
  2·[R odd] の両端構造に対応)。
- **O11 (例外定数層の一般理論 — K1289 O11 継続)**: 層厚 L(w) = 2⌈w/2⌉ が
  w = 0..6 全称 + w = 7..10 OBS。層の中の子は (w, w−1) の層定数 (2 値) を
  R−1 パリティで読むのみで δ 非依存 — w=3 法則が w=5,6 でも同一に成立
  (§2 の R ≤ 層厚 cases は w 非依存の mex{0,1}=2 / mex{2,3}=0 機構)。
- **O12 (11×11 giant 枝刈り格子)**: T-PD0 (K1286) + K1288 + K1289 + 本項で、
  ペア面 z ∈ {0..6} の対角下全域 k ≤ 0 が R 例外層込みで O(1) 即値評価可能に
  (band は δ と R の 2 変数・床は 1 変数)。境界側格子の拡張として巨大探索
  レーンへ記録 (採用判断はオーナー)。
- **O13 (K1287 O1 残部)**: (i) SLB2/SLB3 単一層族・(ii) L/Am frontier 全称化
  は非接触のまま (K1291+ 候補・K1289 §5 O12 と同一)。

## §6 主張の区別 (過大主張の防止)

- 定理 (universal, §2 手証明): T-PDT5, T-BDT5, T-PDT6, T-BDT6, L-BU5G,
  L-BU6G, C1 (O8 解決の記述), C2 の w ≤ 6 部分 (sharpened C-PSF′ の
  w については既刊+本項の集約)。
- corollary (universal だが既刊の言い換え): C2/C3 の既刊分の再表現。
- 有限観測 (OBS): D11 (z7/z8 band/beds/far-row/lowR hist・L-BU7G/L-BU8G・
  dedup sweep z=7..10)・§3 X/Y。
- census 点数 69,553 は定理の実機照合であり全称性の主張ではない。
- 標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は
  全て UNKNOWN のまま。verdict 不消費。

(宣言ノート本文ここまで。実装は publish-then-execute: 本ノートが最先行。
kit → fetch-back → 公式 4 走 → 変異電池 → 成果物出版 → K item → README bullet
→ run log の順に進める。)
