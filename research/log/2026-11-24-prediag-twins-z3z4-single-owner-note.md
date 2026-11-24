# 単一オーナー宣言 K1289: pre-diag 双生児 z3/z4 の全称確定
(T-PDT3/T-BDT3 + T-PDT4/T-BDT4 — K1288 O5 の例外層込み解決・sharpened C-PSF′ の w=3,4 実例化・z5/z6 OBS)

## §0 状態と採番 (single-owner protocol)

- 観測 HEAD (着手時): `6a6e3a340fe738609d61d0e3f78a3105ca70b490` (2026-11-24T11:54:30Z)。
- 本宣言 push 直前再取得 HEAD: `402d481fadd26087aaedfaab221e9574c64b1d28` (2026-11-24T12:18:48Z・Part DN batch-30 adoption 宣言。非接触: n11 central-reply adoption レーン)。
- K1289 空き確認: `research/knowledge/items/` の最新 K item = K1288 `dbc59af1` (10:36:49Z)。repository code search `filename:K1289` 0 件・コミットメッセージに K1289 宣言 0 件 (2026-11-24T12:18Z 時点)。対抗宣言なし。
- 領域: K1288 lane が自項目 §次課題 1–2 として登録した T-PDT3/T-BDT3・T-PDT4/T-BDT4 (z3/z4 pre-diag typed 全称) を取得。K1288 O5 を解決し O6 (C-PSF) を sharpen して w=3,4 を実例化、z5/z6 を OBS 登録する。K1286/K1287/K1288 の全定理に触れない (内面 k>0・multi-c web は非接触)。
- 規約: verdict 不消費・標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は全て UNKNOWN のまま。

## §1 主張 (claims)

座標の規約は K1286/K1288 と同一: ペア局面 H(R;(m,m+g);z)、対角座標 k := R−2m−g、
δ := R−2m、バンド域 k ≤ 0 (0 ≤ R ≤ 2m+g)。床 (bed) は (m,m) 双 Token: 
b_z(j) := H(2m+j;(m,m);z), j ≤ 0。f0 は K1286 出版の対角下バンド 1 次元崩壊関数、
g1 は K1288 出版の偶奇双生児 (T-TWIN: g1(d) = 1 ⊕ f0(d) for d ≠ 1, g1(1) = f0(1) = 2):

- f0(d) = 2 (d=1); [d odd] (d ≤ 0); [d even] (d ≥ 2)
- g1(d) = 2 (d=1); [d even] (d ≤ 0); [d odd] (d ≥ 2)

**定理パッケージ (universal, 量子化: ∀m ≥ 1, ∀g ≥ 1, 全ての有効 cell, 値は m も g も経由しない):**

- **T-PDT3 (z3 band)**: H(R;(m,m+g);3) = 2·[R odd] (R ≤ 3); g1(δ−2) (R ≥ 4)。
- **T-BDT3 (z3 bed)**: b3(j) = 2·[R odd] (R ≤ 3, R = 2m+j); g1(j−2) (R ≥ 4)。
- **T-PDT4 (z4 band)**: H(R;(m,m+g);4) = 2·[R odd] (R < 4); f0(δ−4) (R ≥ 4)。
- **T-BDT4 (z4 bed)**: b4(j) = 2·[R odd] (R < 4); f0(j−4) (R ≥ 4)。
  (z4 の偶数例外 cell (R=0,2) は主則 f0(δ−4) と値が一致する − f0(−2m−4)=0,
  f0(δ−4) at R=2: δ even ≤ 0 → 0 − ので層の記述は「R<4 で 2·[R odd]」として統一
  できる。z3 の偶数 cell (R=0,2) は主則と衝突する (g1(δ−2)=1 となる) ので層の
  上書きとして本物である。)

**補題 (closed-form から機械照合 w ≤ 30):**

- **L-BU3G**: v(w,4,t) = 2·[t odd] (t ≤ 3); g1(t−2) (4 ≤ t ≤ w), ∀w ≥ 2
  (単一 Token w を平面 4 に置いた局面 = B-exit 子の値 = plane-3 則のフル形式)。
- **L-BU4G**: v(w,5,t) = 2·[t odd] (t < 4); f0(t−4) (4 ≤ t ≤ w), ∀w ≥ 2。
  (t=5 の 2 は f0(1)=2 と合致: 主則の核 f0(1)=2 がそのまま単一 Token 側にも現れる。)

**系 (corollaries / subsumption):**

- **C1 (K1288 O5 RESOLVED)**: K1288 O5 が exception layer 未解決として観測した
  「z3 R∈{2,3} の δ-local value mixing (even δ {0,1} / odd δ {0,2})」・
  「z4 odd δ {1,2}」・「low-R probe hist 0:144/2:144」は、すべて
  **定数 R 例外層 2·[R odd の厚み 4 (z3) / 実効 {1,3} (z4)]** の見え方であった。
  δ-mixing は (R,δ) 平面でならば消える (explore X1/X3: mixed (R,δ) cell 0)。
  m 分裂・g 分裂は残らない。
- **C2 (sharpened C-PSF′ = K1288 O6 UPDATE)**: 全ての平面 w ≥ 0 に対する統一形式
  **H(R;(m,m+g);w) = 2·[R odd] (R < 2⌈w/2⌉); T_w(δ − 2⌊w/2⌋) (R ≥ 2⌈w/2⌉)**,
  ここで T_0 = f0 (w 偶数) / T_w = g1 (w 奇数)。この項で w ∈ {3,4} が全称証明され、
  w ∈ {0} (K1286 T-PD0: 層厚 0), w ∈ {1,2} (K1288 T-PDT1/T-PDT2: 層厚 2) は
  既刊定理と代数的に同一 (verify D9(e) が機械照合する)。w ∈ {5,6} は有限 OBS のみ
  (D11・全称主張なし)。層厚 L(w) = 2⌈w/2⌉ の一般 w 帰納は未解決 (§5 O9)。
- **C3 (B-exit 均一性の族)**: 単一 Token @ plane z+1 は plane-z 則を継承する:
  L-BU0 (K1286: v(w,1,t)=f0(t)=plane-0)、L-BU1G/L-BU2G (K1288: v(w,2,t)=plane-1
  g1 / v(w,3,t)=plane-2 f0(t−2))、そして本項 L-BU3G/L-BU4G (plane-3 / plane-4)。
  本項の typed overlap で計 5 枝が出揃った (族の全称形は §5 O9)。

**§1.1 K1288 内面との境界 (重複なし)**: K1288 の T-PDT3 候補は R ≥ 4 の広 box
(bad 0) を OBS として持っていた。本項の主張は R 例外層値込みの全 cell を含み、
K1288 が open にした「層の構造」を定理として確定する。K1286 T-Z1 の k=1 内面・
K1287 F2 web の内面 k>0 には一切触れない。

## §2 手証明 (typed child mex, single R strong induction)

### §2.0 型付き子の分類 (pair @ plane z)

Budget R の局面 (m,m+g)@z (バンド内 k ≤ 0) の engine の選択肢は次の 5 型で全て、
子は全て budget R−1 である (engine 定義から直接):

1. **fall** (小 Token 減算, m ≥ 2): child (m−1, m+g)@z, k 不変, δ_c = δ+1
   (row m−1, gap g+1; なお k_c = k ≤ 0 なので child もバンド内)。
2. **B-exit** (m = 1): 小 Token の減算で Token が消え、child は単一 Token
   w = g+1 @ plane z+1, budget t = R−1 (**t ≤ w**: k ≤ 0 → R ≤ 2+g → t ≤ g+1)。
   値は K0832 closed form による L-BUzG 表から直接 (帰納外)。
3. **compress** (大 Token 減算, g ≥ 2): child (m, m+g−1)@z, k 不変, δ_c = δ−1
   (バンド内)。
4. **corner** (g = 1, 大 Token 減算): child (m,m)@z = 床, 床座標 j_c = δ−1 = k ≤ 0
   (バンド内保証: δ ≤ g = 1)。
5. **C** (z ≥ 1): child = 1 ⊕ H(R−1;(m,m+g);z−1) (平面 z−1 の同ペア, budget R−1。

床 (m,m)@z の子は 3 型: **fall** (Token 減算, m ≥ 2: child = pair (m−1,m)@z,
gap 1, k_c = j), **B** (m=1: child 単一 Token 1 @ plane z+1, t = R−1 = j+1 ≤ 1,
値 {v(1,z+1,0), v(1,z+1,1)} = {0,2} — closed form・D9(h) 照合), **C**
(1 ⊕ 床 (m,m)@(z−1), budget R−1, 床座標 j−1)。

well-founded 性: 単一の packet {T-PDT3, T-BDT3, T-PDT4, T-BDT4} 全体で R に
ついての強帰納。全ての子の budget は R−1 であり、面間参照は常に下位 budget
(z3 の C 子は z2 = K1288 既刊で全 R 無条件、z4 の C 子は z3 = packet 内で
budget R−1)。B 子・床 B 子は closed form (帰納外)。基底 R = 0: 選択肢集合は空、
mex ∅ = 0 (4 定理すべての主張値と整合: T-PDT3/T-PDT4 の層値 2·[0]=0)。

### §2.1 T-PDT3 (z3 band) の証明

主張値 V(R,δ) := 2·[R odd] (R ≤ 3); g1(δ−2) (R ≥ 4)。

**R = 0**: mex ∅ = 0 = 層値。

**R ∈ {1,2,3} (例外層)**: 子は全て budget R−1 で z3-band/z3-bed/L-BU3G/C の
層値を読む:
- fall/compress/corner 子: z3 層値 at R−1 = 2·[(R−1) odd] → R−1 ∈ {0,1,2} で
  0/2/0 (子の δ_c に依らず定数)。
- B 子 (m=1): L-BU3G at t = R−1:
  t ∈ {0,1,2} → 0/2/0 (t ≤ 3 層)。
- C 子: 1 ⊕ [T-PDT2 at (R−1, z2)]: R−1 ∈ {0,1,2}:
  R−1=0 → f0(δ₂−2), δ₂ = 0−2m = −2m → f0(−2m−2)=0 → C = 1;
  R−1=1 → z2 例外層 2 → C = 3;
  R−1=2 → f0(−2m−2)=0 → C = 1。

よって選択肢集合:
- R=1: {0 (fall/compress/corner/B), 1 (C)} → mex = **2** = 2·[1 odd] ✓
- R=2: {2, 3} → mex = **0** = 2·[0] ✓
- R=3: {0, 1} → mex = **2** = 2·[1] ✓

(どの型が現れるかは m,g に依るが、層値の読みは全て同一の R−1 定数なので
場合分け不要 — これが R 例外層を「値として主張する」ことの利点。)

**R = 4 (主則への継ぎ目)**: 子の budget 3 (層値 2):
- fall/compress/corner: z3 層値 at R−1=3 → **2**。
- B (m=1, g ≥ 2): L-BU3G t=3 → **2**。
- C: T-PDT2 main at R−1=3: f0(δ₂−2), δ₂ = 3−2m; δ₂−2 = 1−2m (odd ≤ 0) →
  f0 = 1 → C = **0**。

選択肢集合 = {0, 2} → mex = **1**。主張値: g1(δ−2) at R=4 (δ even, δ−2 ≤ 0
または δ=g+k−2 ≤ 1−2 = −1 → δ−2 ≤ 0, even → [d even] = 1) ✓。

**R ≥ 5 (主則)**: 子は全て主則読み (R−1 ≥ 4):
- fall 子: g1(δ_c − 2) at δ_c = δ+1 → **g1(δ−1)**。
- B 子 (m=1): L-BU3G main at t = R−1 = 2m+g+k−1−... k... m=1 のとき
  δ = R−2, t = R−1 = δ+1, main g1(t−2) = **g1(δ−1)** (fall 子と同じ表を再生
  — K1288 の B-exit 再生構造の z3 版)。
- compress 子: g1(δ_c−2) at δ_c = δ−1 → **g1(δ−3)**。
- corner 子 (g=1): 床 T-BDT3 main at j_c = δ−1: g1(j_c−2) = **g1(δ−3)**
  (compress 子と同値)。
- C 子: 1 ⊕ f0(δ₂−2) at δ₂ = δ−1 → **1 ⊕ f0(δ−3)**。

T-TWIN (g1 = 1 ⊕ f0, d ≠ 1) より 1 ⊕ f0(δ−3) = g1(δ−3) unless δ = 4。
場合分け (δ ≡ R (mod 2), δ の範囲は全整数, δ ≤ g):

| δ (parity, range) | fall/B | compress/corner | C | 集合 S | mex | 主張 g1(δ−2) |
|---|---|---|---|---|---|---|
| odd, δ ≤ 1 | g1(δ−1)=1 (δ−1 even ≤ 0) | 1 (δ−3 even ≤ −2) | 1⊕f0(δ−3) = 1⊕0 = 1 | {1} | 0 | g1(δ−2)=[even] at odd δ−2 ≤ −1 → 0 ✓ |
| δ = 3 (核) | g1(2)=0 | g1(0)=1 | 1⊕f0(0)=1 | {0,1} | 2 | g1(1)=2 ✓ |
| odd, δ ≥ 5 | g1(δ−1)=0 (even ≥ 4) | g1(δ−3)=0 (even ≥ 2) | 1⊕f0(δ−3)=1⊕1=0 | {0} | 1 | g1(δ−2)=[odd] at δ−2 ≥ 3 → 1 ✓ |
| even, δ ≤ 0 | g1(δ−1)=0 (odd ≤ −1) | 0 (δ−3 odd ≤ −3) | 1⊕f0(δ−3)=1⊕1=0 | {0} | 1 | g1(δ−2)=1 (even ≤ −2) ✓ |
| δ = 2 | g1(1)=2 | g1(−1)=0 | 1⊕f0(−1)=0 | {2,0} | 1 | g1(0)=1 ✓ |
| δ = 4 (核) | g1(3)=1 | g1(1)=2 | 1⊕f0(1)=3 | {1,2,3} | 0 | g1(2)=0 ✓ |
| even, δ ≥ 6 | g1(δ−1)=1 (odd ≥ 5) | g1(δ−3)=1 (odd ≥ 3) | 1⊕f0(δ−3)=1⊕0=1 | {1} | 0 | g1(δ−2)=0 (even ≥ 4) ✓ |

全 δ 場合で mex = 主張値。■

### §2.2 T-BDT3 (z3 bed) の証明

主張値 b3: 2·[R odd] (R ≤ 3); g1(j−2) (R ≥ 4), R = 2m+j, j ≤ 0。

R = 0: mex ∅ = 0 ✓。

**R ∈ {1,2,3} (例外層)**: 子は budget R−1 の層定数を読む:
- fall 子 (m ≥ 2): pair (m−1, m)@z3 at R−1 → 層値 2·[(R−1) odd]。
- B 子 (m = 1): v(1,4,t) at t = R−1 ∈ {0,1} → 0/2 = 2·[t odd]。
- C 子: 1 ⊕ [T-BDT2 at R−1]: R−1=0: f0(j−3) at j = −1 (R=1 は m=1,j=−1 のみ):
  f0(−4)=0 → C=1; R−1=1 (R=2): z2 床例外層 2 → C=3; R−1=2 (R=3):
  T-BDT2 main f0(j−3): j = R−2m: = 1−2m or −1−2m or −3−2m (m ≥ 2):
  j−3 = −2−2m−... いずれも even ≤ −4 → f0=0 → C=1。

選択肢集合: R=1: {0,1} → 2 ✓ (層値 2); R=2: {2,3} → 0 ✓; R=3: {0,1} → 2 ✓。

**R = 4** (m ≥ 2, j = 4−2m ≤ 0): 子 budget 3:
- fall: pair (m−1,m)@z3 層値 at R−1=3 → **2**。
- C: 1 ⊕ T-BDT2 at R−1=3: main f0(j−3): j even (j = 4−2m) → j−3 odd ≤ −3 →
  f0 = 1 → C = **0**。
- 集合 {2, 0} → mex = **1**。主張 g1(j−2): j even → j−2 even ≤ −2 → 1 ✓。

**R ≥ 5** (主則): 子は主則読み:
- fall: pair (m−1,m)@z3 main at δ_c = (R−1)−2(m−1) = j+1 → g1(j+1−2) = **g1(j−1)**。
- C: 1 ⊕ T-BDT2 main at 座標 j−1: f0((j−1)−2) = f0(j−3) → **1 ⊕ f0(j−3)**
  = g1(j−3) for j ≠ 4 (j ≤ 0 なので常に成立)。
- B 子は m = 1 で R ≤ 2 にしか現れない (主則域外)。

| j (parity) | fall g1(j−1) | C | 集合 | mex | 主張 g1(j−2) |
|---|---|---|---|---|---|
| odd, j ≤ −1 | g1(even ≤ −2)=1 | 1⊕f0(even ≤ −4)=1 | {1} | 0 | g1(odd ≤ −3)=[even]=0 ✓ |
| even, j ≤ 0 | g1(odd ≤ −1)=0 | 1⊕f0(odd ≤ −3)=0 | {0} | 1 | g1(even ≤ −2)=1 ✓ |

■ (bed は compress/corner 子を持たない — 両減算が同じ fall 子に縮退する。)

### §2.3 T-PDT4 (z4 band) の証明

主張値 V(R,δ) := 2·[R odd] (R < 4); f0(δ−4) (R ≥ 4)。

R = 0: mex ∅ = 0 = 層値 2·[0] ✓ (主則 f0(δ−4) = f0(−2m−4) = 0 とも一致)。

**R ∈ {1,2,3}**: 子 budget R−1:
- fall/compress/corner: z4-band/z4-bed 層値 at R−1: R−1 ∈ {0,1,2} → 0/2/0。
- B (m=1): L-BU4G at t = R−1 ∈ {0,1,2} → 0/2/0。
- C: 1 ⊕ [T-PDT3 at (R−1, z3)]: 層値 2·[(R−1) odd]:
  R−1=0: 0 → C=1; R−1=1: 2 → C=3; R−1=2: 0 → C=1。

集合: R=1: {0,1} → mex **2** = 層値 2 ✓; R=2: {2,3} → **0**
(= 主則 f0(δ−4): δ even ≤ 0, δ−4 even ≤ −4 → [odd]=0 と一致 — 層値 2·[0]=0
とも同一 ✓); R=3: {0,1} → **2** = 層値 ✓。

**R = 4**: 子 budget 3:
- fall/compress/corner: z4 層値 at 3 → **2**。
- B: L-BU4G t=3 → **2** (t<4 層)。
- C: 1 ⊕ T-PDT3 at R−1=3: z3 層値 2 → C = **3**。
- 集合 {2,3} → mex = **0**。主張: f0(δ−4) at δ even ≤ 2 → δ−4 ≤ −2 even → 0 ✓。

**R ≥ 5** (主則):
- fall: f0(δ_c−4) at δ_c = δ+1 → **f0(δ−3)**。
- B (m=1): L-BU4G main at t = R−1 = δ+1: f0(δ+1−4) = **f0(δ−3)** (fall 再生)。
- compress: **f0(δ−5)**; corner (g=1): T-BDT4 main at j_c = δ−1 → **f0(δ−5)**。
- C: 1 ⊕ g1(δ₂−2) at δ₂ = δ−1 → **1 ⊕ g1(δ−3)** = f0(δ−3) for δ ≠ 4
  (1 ⊕ g1(x) = f0(x) except x=1; δ=4 のとき 3)。

| δ (parity, range) | fall/B | compress/corner | C | 集合 S | mex | 主張 f0(δ−4) |
|---|---|---|---|---|---|---|
| even, δ ≤ 0 | f0(δ−3)=1 (odd ≤ −3) | f0(δ−5)=1 | 1⊕g1(odd ≤ −3)=1⊕0=1 | {1} | 0 | f0(even ≤ −4)=0 ✓ |
| δ = 2 | f0(−1)=1 | f0(−3)=1 | 1⊕g1(−1)=1 | {1} | 0 | f0(−2)=0 ✓ |
| δ = 4 (核) | f0(1)=2 | f0(−1)=1 | 1⊕g1(1)=3 | {2,1,3} | 0 | f0(0)=0 ✓ |
| δ = 6 | f0(3)=0 | f0(1)=2 | 1⊕g1(3)=0 | {0,2} | 1 | f0(2)=1 ✓ |
| even, δ ≥ 8 | f0(δ−3)=0 (odd ≥ 5: [even]=0) | f0(δ−5)=0 | 1⊕g1(odd ≥ 5)=1⊕1=0 | {0} | 1 | f0(even ≥ 4)=1 ✓ |
| odd, δ ≤ −1 | f0(even ≤ −4)=0 | f0(even ≤ −6)=0 | 1⊕g1(even ≤ −4)=1⊕1=0 | {0} | 1 | f0(odd ≤ −5)=1 ✓ |
| δ = 1 | f0(−2)=0 | f0(−4)=0 | 1⊕g1(−2)=1⊕1=0 | {0} | 1 | f0(−3)=1 ✓ |
| δ = 3 | f0(0)=0 | f0(−2)=0 | 1⊕g1(0)=0 | {0} | 1 | f0(−1)=1 ✓ |
| δ = 5 (核) | f0(2)=1 | f0(0)=0 | 1⊕g1(2)=1⊕0=1 | {1,0} | 2 | f0(1)=2 ✓ |
| odd, δ ≥ 7 | f0(even ≥ 4)=1 | f0(even ≥ 2)=1 | 1⊕g1(even ≥ 4)=1⊕0=1 | {1} | 0 | f0(odd ≥ 3)=0 ✓ |

全 δ 場合で mex = 主張値。■

### §2.4 T-BDT4 (z4 bed) の証明

主張 b4: 2·[R odd] (R < 4); f0(j−4) (R ≥ 4)。

R = 0: mex ∅ = 0 ✓ (= 層値 = 主則 f0(−2m−4)=0)。
R = 1 (m=1, j=−1): 子: B: v(1,5,0)=0; C: 1⊕[T-BDT3 at R−1=0 = 0]=1 → {0,1} →
mex **2** ✓。
R = 2: (m=1,j=0): B: v(1,5,1)=2; C: 1⊕[b3 at R−1=1: 層値 2]=3 → {2,3} → **0**
= 層値 = 主則 f0(j−4)=f0(−2)=0 ✓。(m=2,j=−2): fall: pair (1,2)@z4 層値 at
R−1=1: 2; C: 1⊕[b3 at R−1=1 (m=2, j=−3): 層値 2]=3 → {2,3} → 0 ✓。
R = 3: fall: pair (m−1,m)@z4 層値 at R−1=2: 0; B (m=1,j=1 不在): なし;
C: 1⊕[b3 at R−1=2: 層値 0]=1 → {0,1} → **2** ✓ (層値). (m=1 は j=1>0 不可。)
R = 4: (m ≥ 2): fall: pair 層値 at R−1=3: 2; C: 1⊕[b3 at R−1=3: 層値 2]=3 →
{2,3} → **0** = 主則 f0(j−4): j = 4−2m even → j−4 even ≤ −4 → 0 ✓。
R ≥ 5 (主則): 子:
- fall: pair (m−1,m)@z4 main at δ_c = j+1 → **f0(j−3)**。
- C: 1 ⊕ b3 main at j−1: g1((j−1)−2) = g1(j−3) → **1 ⊕ g1(j−3)**
  = f0(j−3) for j ≠ 4 (j ≤ 0 常に)。

 mex({f0(j−3)}) — 集合の要素が単一値 v なら mex = 0 (v ≠ 0), 1 (v = 0):
- j odd: f0(even ≤ −4)=0 → mex **1** = 主張 f0(odd j−4 ≤ −5)=1 ✓。
- j even: f0(odd ≤ −3)=1 → mex **0** = 主張 f0(even ≤ −4)=0 ✓。■

### §2.5 L-BU3G / L-BU4G の閉形式からの導出

K0832 closed form v(x,z,R) から直接読む。z=4, w ≥ 2:
- w ≥ 5: region 1 ≤ 4 ≤ w−1, m = q_odd(4) = 3: t ≤ 3: 2·[t odd]; 3 < t < w+4:
  (t+4)%2 = t%2: t 偶 → 0 = g1(t−2) (even ≥ 2, [odd]=0), t 奇 → 1 = g1(t−2)
  (odd ≥ 3, [odd]=1)。t ≤ w で tail region に入らない。
- w ∈ {2,3,4}: z ≥ x+1 region: m = q_odd(w): t ≤ m: 2·[t odd]; t > m: w%2
  (=層域外は現れない: 例 w=4, t=4 = w: v=0: f0(0)=0 ✓ — w%2=0 ✓)。
z=5, w ≥ 2: w ≥ 6: m = q_odd(5) = 5: t ≤ 5: 2·[t odd]; 5 < t: (t+5)%2 =
1−t%2: t=6: 1 = f0(2)=1 ✓; t=7: 0 = f0(3)=0 ✓ (= f0(t−4) と一致)。
t=5 ≤ m: 2·[t odd] = 2 = f0(1) = f0(t−4) ✓ (層と主則の境界値の一致)。
w ∈ {2,..,5}: z ≥ x+1: m = q_odd(w) ≤ 3: t ≤ m: 2·[t odd] (t ≤ 3 は層);
t > m && t < 4: w%2: w=3, t=2 > 3? 不可 — w=3: m=3: t ≤ 3 層のみで t ≤ w = 3。
全 twist は機体 D9(a)/(b) が closed form × engine × 主張表の三方で w ≤ 30 照合。■

### §2.6 well-founded 性 (まとめ)

packet {T-PDT3, T-BDT3, T-PDT4, T-BDT4} の証明は単一の R 強帰納:
全子は budget R−1 (engine の子定義)。面間参照: z3 の C 子 = z2 (K1288, 全 R
無条件); z4 の C 子 = z3 (packet, budget R−1); 床 C 子 = plane−1 床。B 子は
K0832 closed form (L-BU3G/L-BU4G + w=1 edge {0,2}) で帰納外。帰納は R のみ
で整礎 (m, g に依らない子値表)。各 R での子値の列挙は §2.1–§2.4 の場合表
(R ≤ 4 は層定数読みの列挙、R ≥ 5 は δ parity の場合表) で全ての (m, g, k) を
尽くす。

### §2.7 反例検査の誠実な記述

- K1288 O5 の「δ-local value mixing」観測は (δ 固定行で R を動かした混在)
  であった。本宣言前の探索 (§3 X1/X3) は (R,δ) 両軸で収集し、mixed (R,δ)
  cell が 0 個であることから層が R 定数層であることを先に特定した。
- m 依存性・g 依存性は主張域内で一度も観測されていない (§3 Y1/Y2 広域)。
  主張は typed 証明による全称主張であり、census は照合である。

## §3 宣言前探索 (pre-declaration; explore_k1289.py / explore2_k1289.py 出力)

- X1/X3 (z3/z4 band m≤12 g≤25 k≥−60, (R,δ) 表): mixed (R,δ) cell それぞれ 0/0。
  低 R 行が定数 0/2/0/2。R≥4 行が g1(δ−2) / f0(δ−4) に一致。z4 の R=0,2 行は
  主則と合致 (層は奇数 cell 2 個のみ実効)。
- X2/X4 (beds m≤12 j∈[−30..0]): 同一の R 層構造。mixed 0/0。
- X5/X6: L-BU3G/L-BU4G 発見 census (w ≤ 30, t ≤ w; engine vs closed form vs
  plane-3/plane-4 law): bad 0/0 (1,972 checks)。w=1 edge: v(1,4,{0,1})={0,2},
  v(1,5,{0,1})={0,2}。
- X7: sharpened C-PSF′ probe (z=0..6, m≤10 g≤20 k≥−50 の dedup (R,δ) 320 cell
  × 7 面): bad 全 0 (z5/z6 は OBS として)。
- Y1/Y2: z3/z4 band+beds の wide census (D1–D4 と同一 box): bad 0。
- Y3/Y4/Y5: z5/z6 OBS (band 4,500 × 2, beds 120 × 2, far-row m=12 216 × 2):
  cpsf 予測 vs engine bad 全 0 (有限観測・全称主張なし)。
- Y6: ordered vs canonical engine 交差 (z=3..6, 各 464 cells): mismatch 全 0。
- Y7: L-BU3G/L-BU4G (w ≤ 40) + 発見 L-BU5G (v(w,6,t)=plane-5 law)・L-BU6G 発見
  (v(w,7,t)=plane-6 law) probe: bad 0 (z=6,7 は OBS)。
- Y8: T-TWIN identity d∈[−260..260] bad 0; z=0..6 dedup (R,δ) sweep: mixed 0・
  cpsf bad 0。

## §4 機体宣言 (machine declaration, publish-then-execute)

`verify_k1289.py` (sha256 publish 時に kit で宣言・engine pin
`bd5f22e415a78368c9b798296bc84948d5637decbf3c21a92404d45fb12e3a92`
startup gate 内蔵・embed は K1138/K1282..K1288 と同一 bytes)。バッテリ:

| # | 内容 | 期待 count |
|---|---|---|
| D1 | z3 band census (m≤14, g≤25, k∈[max(−30,−2m−g),0]) | 8,928 |
| D2 | z3 beds census (m≤18, j∈[−36..0]) | 360 |
| D3 | z4 band census (D1 box) | 8,928 |
| D4 | z4 beds census (D2 box) | 360 |
| D5 | typed z3 slices (m≤10, g≤14, k≥−14): typed mex == claim == engine | 1,939 |
| D6 | typed z3 beds (m≤10, j≥−16) | 114 |
| D7 | typed z4 slices (D5 box) | 1,939 |
| D8 | typed z4 beds (D6 box) | 114 |
| D9 | (a) L-BU3G 493 + (b) L-BU4G 493 + (c) K1288 anchors T-PDT1/2・T-BDT1/2 再照合 4,690 + (d) K1286 anchors T-PD0/T-B0 再照合 2,345 + (e) sharpened C-PSF′ identity sweep w=0..4 (pair box + bed box) 11,725 + (f) T-TWIN algebra d∈[−100..100] 201 + (g) closed form vs both engines (x≤16, z∈2..5, R∈x+1..x+4) 480 + (h) B-exit w=1 edge 4 | 20,431 |
| D10 | cross-engine canonical vs ordered (z3/z4 pair m≤8, g≤10, k≥−8 + beds m≤8 j≥−8) | 1,516 |
| D11 | OBS: z5/z6 band (m≤10,g≤20,k≥−50) 4,500×2 + beds (m≤10,j≥−24) 120×2 + far-row m=12 216×2 + low-R (R<6) hist probe | 10,530 |

**総計 55,159 比較点・期待 overall_bad = 0** (宣言前 predry 4 走で
counts [8928, 360, 8928, 360, 1939, 114, 1939, 114, 20431, 1516, 10530]・
bad 全 0 を確認済み・stdout 4 走 byte-identical)。

変異電池 (公式 run の前に期待値を宣言):
- `--tamper-engine`: rc=2・mutated sha `0ea47a80…` ≠ pin (K1282–K1288 と同一変異)。
- `--tamper=z3s`: rc=1, D1 bad 8,928。`--tamper=z3b`: rc=1, D2 bad 360。
- `--tamper=z4s`: rc=1, D3 bad 8,928。`--tamper=z4b`: rc=1, D4 bad 360。
- 他バッテリ (D5–D11) は census クレームの flip の影響を受けない
  (typed 側は flip されないので D5–D8 の 3-way 照合は主張値のまま engine と
  一致する; 対角の影響は D1–D4 の bad のみ)。

公式 4 走: 同一 cwd (PYTHONHASHSEED random/1) × 2 + 隔離 tree (env -i,
PYTHONHASHSEED 99/7) × 2、stdout byte-identical が要求。predry の PATH
artifact (env -i で /usr/local/bin 不足による空出力) は同梱の predry 正走で
置き換え済み (honest 記録)。

## §5 open 登録 (有限観測・予想と次課題; 全称主張なし)

- **O8 (z5/z6 typed proofs)**: T-PDT5/T-BDT5/T-PDT6/T-BDT6 候補。D11/Y3–Y5 の
  OBS は sharpened C-PSF′ 予測 (層厚 2·[R odd], R<6; 主則 g1(δ−4) (z5) /
  f0(δ−6) (z6)) と engine の一致。C 子は本項の z3/z4 定理 (全 R) を参照する
  ため、§2.3/§2.4 と同一構文で typed 証明可能な見通し。次回最有力単一
  オーナー候補。
- **O9 (C-PSF′ の w 帰納)**: §2.1–§2.4 の場合表は、主則域の mex 閉包が
  双子恒等式の組合せ (T_w 主則子対 {T_w(δ+1−s), T_w(δ−1−s)} と 1 ⊕
  T_{w−1}(δ−1−s)) の代数的帰結であることを w=3,4 で示した。一般 w の
  mex 恒等式は T-TWIN 族で単純に閉じる可能性が高いが、**例外層の厚み
  L(w) = 2⌈w/2⌉ の帰納** (層の中の子は他面の層定数を読む) が主要障壁。
  z3 の証明では z2 の層 {1} だけが必要だった。一般 w では 3 世代の層
  (w−2, w−1, w) の同時管理になる見込み。
- **O10 (L-BUzG 族の全称形)**: 単一 Token @ plane z+1 = plane-z 則の継承
  (L-BU0/…/L-BU4G の 5 枝が出揃い、z=6/7 個別は Y7 OBS)。closed form の
  region 計算で一般 w に拡張可能な見込み (q_odd(z) = z − [z even] が層核
  2·[R odd] を両端で残す構造と対応)。
- **O11 (11×11 giant 枝刈り格子)**: T-PD0 (K1286) + K1288 + 本項で、ペア面
  z ∈ {0,1,2,3,4} の対角下全域 k ≤ 0 が R 例外層込みで O(1) 即値評価可能に
  (band は δ と R の 2 変数・床は 1 変数)。境界側格子の拡張として巨大探索
  レーンへ記録 (採用判断はオーナー)。
- **O12 (内面 k > 0 の z≥3 面)**: K1287 F2 web (multi-c) の面間接続は
  非接触のまま (本項の m=1 B-exit 単一 Token の話題と K1287 multi-c web / Am 領域は
  領域直交)。

## §6 主張の区別 (過大主張の防止)

- 定理 (universal, §2 手証明): T-PDT3, T-BDT3, T-PDT4, T-BDT4, L-BU3G,
  L-BU4G, C1 (O5 解決の記述), C3′ (既刊定理との代数同一性)。
- corollary (universal だが既刊の言い換え): C2 の w ≤ 4 部分
  (sharpened C-PSF′ は w については CONJECTURE、O9)。
- 有限観測 (OBS): D11/Y3–Y5/Y7(z=6,7)/z5/z6 low-R hist。
- census 点数 55,159 は定理の実機照合であり全称性の主張ではない。
- 標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は
  全て UNKNOWN のまま。verdict 不消費。

(宣言ノート本文ここまで。実装は publish-then-execute: 本ノートが最先行。
kit → fetch-back → 公式 4 走 → 変異電池 → 成果物出版 → K item → README bullet
→ run log の順に進める。)
