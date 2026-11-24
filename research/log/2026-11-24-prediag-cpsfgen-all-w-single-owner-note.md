# 単一オーナー宣言 K1303: pre-diag の一般 w 帰納 — sharpened C-PSF′ の全 w ≥ 0 全称確定
(T-GEPSF/T-GEBED + L-BU-GEN — K1301 O9⁗残余・O10⁗・O11 の一括解決・K1286..K1302 全 per-plane 定理の包摂)

## §0 状態と採番 (single-owner protocol)

- 観測 HEAD (着手時): `1f08b0bc1a502cf74ba70a297b6b60dc2af33287` (2026-11-24T19:19:40Z・PG(2,8)/AG(2,8) cap games レーン)。着手以降に同一 fast-lane の並走実行が **K1302** (pre-diag 双生児 z13/z14・宣言 `4905228a` 19:26:09Z → kit `3f436333` → 成果物 `021236fc` 19:31:31Z → item `afcc2ba2`・README `23595bb3` 19:34:30Z) を出版したのを再取得で確認 (honest 記録・下記採番)。出版直前の再取得で観測 HEAD は **`f01fc77b`** (2026-11-24T19:41:59Z・PG(2,9) cap census レーン) に進行・intervening commits (K1302 item/README・Part DT b33loss45 採用レーン 5 commits・PG(2,8) 独立検証 `e2612e81`・PG(2,9) cap census `f01fc77b`) は全て領域直交・非接触・**K1303 以上の fast-lane 番号の取得なし**。
- 本 package は着手時に K1302 採番を仮に準備していたが (機体名 verify_k1302 として構築)、上記取得を確認した時点で **K1303 に再採番** (AGENTS.md 規約「仮番号・統合時再採番・main の番号は変更しない」・仮番号は未出版ゆえ競合なし)。**K1303 空き確認**: items 直接 path probe (`research/knowledge/items/K1303-*.md` 存在せず)・items path の commits 履歴に K1303 なし・対抗宣言なし・**push 直前に再確認** (§0 末尾)。
- 領域: K1286 (z0)・K1288 (z1/z2)・K1289 (z3/z4)・K1290 (z5/z6)・K1294 (z7/z8)・K1299 (z9/z10)・K1301 (z11/z12)・K1302 (z13/z14) が到達した per-plane 主張群を **一般 w 帰納で全 w ≥ 0 に一挙に拡張** する。K1301 §5 O9⁗ (層厚 L(w)=2⌈w/2⌉ の一般 w 帰納・z13/z14 部分は K1302 が取得済み)、O10⁗ (L-BUzG 族の一般 w 全称形)、O11 (例外定数層の一般理論・(w mod 2) 2 型分類) を本項で解決する。内面 k>0 (K1285/K1287 multi-c web)・巨大探索レーン・cap games/moment/s-parameter/projective-blocking 各レーンには一切触れない。
- 規約: verdict 不消費・標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は全て UNKNOWN のまま。engine はゲーム定義の転写 (K1138 chain) であり定理はその帰納定義に対する証明・census は照合であって証明の代替ではない。

## §1 主張 (claims)

座標規約は K1286..K1302 と同一: ペア局面 H(R;(m,m+g);z)、k := R−2m−g ≤ 0 (バンド)、δ := R−2m、
床 b_z(j) := H(2m+j;(m,m);z), j ≤ 0。f0 は K1286、g1 は K1288 (T-TWIN: g1(d) = 1⊕f0(d) for d ≠ 1・g1(1) = f0(1) = 2):

- f0(d) = 2 (d=1); [d odd] (d ≤ 0); [d even] (d ≥ 2)
- g1(d) = 2 (d=1); [d even] (d ≤ 0); [d odd] (d ≥ 2)

一般化平面族記号: **L(w) := 2⌈w/2⌉** (層厚)、**s(w) := 2⌊w/2⌋** (主則シフト)、**T_w := g1 (w 奇数) / f0 (w 偶数)**。

**定理パッケージ (universal・量子化は全て非有界・値は m も g も経由しない):**

- **T-GEPSF (CPSF-GEN) — 一般 w ペア則**: ∀w ≥ 0, ∀m ≥ 1, g ≥ 1, 0 ≤ R ≤ 2m+g:
  **H(R;(m,m+g);w) = 2·[R odd] (R < L(w)); T_w(δ − s(w)) (R ≥ L(w))**。
- **T-GEBED (BED-GEN) — 一般 w 床則**: ∀w ≥ 0, m ≥ 1, 0 ≤ R ≤ 2m (j = R−2m ≤ 0):
  **b_w(R,j) = 2·[R odd] (R < L(w)); T_w(j − s(w)) (R ≥ L(w))**。
- **L-BU-GEN — 一般 w B-exit 均一性 (帰納外・K0832 閉形式から直接導出)**:
  ∀w ≥ 0, ∀x ≥ 1, 0 ≤ t ≤ x: **v(x, w+1, t) = 2·[t odd] (t < L(w)); T_w(t − s(w)) (t ≥ L(w))**
  (K1286 L-BU0〔w=0〕は既刊のまま・一般形の下限と整合)。

**系 (corollaries):**

- **C1 (全 per-plane 定理の包摂)**: T-GEPSF/T-GEBED の w∈{0..14} 実例は K1286/K1288/K1289/K1290/K1294/K1299/K1301/K1302 の全 per-plane 定理 (T-PD0..T-PDT14・T-B0..T-BDT14) と同一。**∀w ≥ 15 は本項で初めて定理化** (K1302 D11 の z15/z16 band/beds/far-row OBS と dedup z≤18・ならびに本項で初観測の z19/z20 は instance の有限観測から全称定理へ昇格)。
- **C2 (sharpened C-PSF′ の全 w 全称化・O9⁗ 完全解決)**: 統一形式
  H = 2·[R odd] (R < 2⌈w/2⌉); T_w(δ−2⌊w/2⌋) (R ≥ 2⌈w/2⌉) が **全 w ≥ 0** で成立。per-plane 増築 (世代パッケージ) は原理的に完了・以後の平面追加は不要。
- **C3 (L-BUzG 族の一般形・O10⁗ 解決)**: L-BU0/L-BU1G..L-BU14G の 15 枝は L-BU-GEN の実例。**任意の w ≥ 15 の token plane (w+1) も含めて族は完結**。
- **C4 (例外定数層の一般理論・O11 解決)**: 層値 2·[R odd] は w 非依存で全世代共通・例外機構 mex{0,1}=2 / mex{2,3}=0 は w に依らない定数計算 (§2.3/§2.4 の d-表は w を含まない)。「層域横断 2 行 (奇数 w 世代) / 横断ゼロ (偶数 w 世代)」の (w mod 2) 2 型ペア構造が一般形として確定 (K1289/K1290/K1294/K1299/K1301/K1302 の記録の一般化)。

**§1.1 既刊との境界 (重複なし)**: K1302 の主張 (T-PDT13/T-BDT13/T-PDT14/T-BDT14) は本項の w=13/14 実例であり再証明しない (D7 が転写一致を機械照合)。K1302 の z15/z16 OBS は本項の定理化対象であった有限観測。K1286..K1301 の全定理にも触れない (本項は上位の一般形として含むのみで、C 子の外部参照も本項内の一般表 w−1 読みで完結)。内面 (k ≥ 1) は非接触のまま (K1285/K1287)。

## §2 手証明 (typed child mex・二重帰納: 外側 w・内側 R 強帰納)

### §2.0 型付き子の分類 (pair @ plane w)

K1294 §2.0 / K1299 §2.0 / K1301 §2.0 / K1302 §2.0 と同一 (engine 定義から直接)。Budget R の局面 (m,m+g)@w (バンド内 k ≤ 0) の選択肢は 5 型で全て子 budget R−1:

1. **fall** (小 Token 減算, m ≥ 2): child (m−1, m+g)@w — row m−1, gap g+1, k 不変, δ_c = δ+1。値は T-GEPSF(w) at budget R−1 (packet 内・帰納)。
2. **B-exit** (m = 1): child は単一 Token x = g+1 @ plane w+1, budget t = R−1 (**t ≤ x**: k ≤ 0 → R ≤ 2+g)。値は K0832 閉形式から L-BU-GEN 表で直接 (帰納外)。
3. **compress** (大 Token 減算, g ≥ 2): child (m, m+g−1)@w, δ_c = δ−1。T-GEPSF(w)。
4. **corner** (g = 1): child 床 (m,m)@w, 床座標 j_c = δ−1 ≤ 0 (バンド内保証: δ ≤ g = 1)。T-GEBED(w)。
5. **C** (w ≥ 1): child = 1 ⊕ H(R−1;(m,m+g);w−1) (平面 w−1 の同ペア, k_c = k−1 ≤ 0)。T-GEPSF(w−1) at budget R−1 (**外側帰納: w−1 は全 R 無条件で既知**)。

床 (m,m)@w の子は 3 型: **fall** (m ≥ 2: pair (m−1,m)@w, gap 1, δ_c = j+1)、**B** (m=1: child 単一 Token 1 @ plane w+1, t = j+1 ≤ 1・値 {0,2} = 2·[t odd]、L-BU-GEN x=1)、**C** (1 ⊕ 床 (m,m)@(w−1), 床座標 j−1)。

well-founded 性: **外側帰納 w** (基底 w ∈ {0,1,2} = K1286/K1288 既刊) → step w ≥ 3 は **w−1 のみ** を参照 (C 子)。**内側は packet {T-GEPSF(w), T-GEBED(w)} で R に強帰納** (全子 budget R−1; fall/compress/corner/B は packet 内 [corner は床、fall は pair]、C は w−1 既刊、B は閉形式帰納外)。基底 R = 0: mex ∅ = 0 = 層値 2·[0] (= w 偶数では主則 f0(δ−s) = f0(even ≤ −s ≤ 0) = 0 とも一致)。
**決定的な単純化 (本項の核)**: 子の主則読みは全て **d := δ−s(w)** (pair) / (床は j 側の同型座標) の **単一変数の w を含まない表** に落ち、層域内の子は **budget 定数 2·[(R−1) odd]** に落ちる。よって §2.3/§2.4 の 2 表 (奇数 w・偶数 w 各 1 枚) と境界行 (層・横断・seam の定数計算) が全 (m,g,R) の場合を尽くす。これが w 帰納を可能にする構造である。

### §2.1 対称性 (T-TWIN)

f0/g1 は d ≠ 1 で g1(d) = 1⊕f0(d) (K1288 T-TWIN・D9 機体照合 d∈[−260..260])。核: f0(1) = g1(1) = 2 ゆえ **1⊕f0(1) = 3** (C 子の核例外値)。C 子は主則域で 1 ⊕ [plane w−1 主則値] であり、T_{w−1}(·) = (w−1 の偶奇に応じた f0/g1) から T-w 表の「1⊕T」項に還元される。

### §2.2 L-BU-GEN の閉形式からの導出 (∀w ≥ 0・3 region)

K0832 閉形式 v(x,z,R) を z = w+1, R = t ≤ x で読む。3 region:

**(i) z ≥ x+1 (x ≤ w)**: m := q_odd(x)。t ≤ m → 2·[t odd]; t > m (x 偶数の t = x のみ) → x%2 = 0 = 2·[x odd]。
→ 全 t ≤ x で閉形式値は 2·[t odd]。x ≤ w では奇数 w の L = w+1 > w より全域が層域・偶数 w は t = w = x のみ主則核 cell だが f0(0) = 0 = 2·[w odd] で一致し、いずれも L-BU-GEN と整合。
**(ii) z == x (x = w+1)**: t 奇 (t ≤ x) → 2; t 偶 ≤ x−1 → 0; t = x 偶 → x%2。
→ t < x では 2·[t odd] (層域: t ≤ x−1 ≤ w)。t = x = w+1 は主則核 cell: w 偶数なら x 奇で閉形式値 2 = f0(1) ✓; w 奇数なら x 偶で閉形式値 x%2 = 0 = g1(2) ✓。いずれも L-BU-GEN 主則と一致。
**(iii) 1 ≤ z ≤ x−1 (x ≥ w+2)**: m := q_odd(w+1)。
- **w 奇数** (z = w+1 偶 → m = w): t ≤ m = w → 2·[t odd] (t ≤ w < L = w+1 は全域層域・境界 t = w の閉形式値 2 = 層値 2·[w odd] ✓)。m < t ≤ x → (t+z)%2 = t%2: t 奇 → 1・t 偶 → 0。主則主張 g1(t−(w−1)) は t ≥ w+1 で arg = 奇 ≥ 3 → g1 = 1 (t 奇)・arg = 偶 ≥ 2 → g1 = 0 (t 偶) となり全域一致。
- **w 偶数** (z = w+1 奇 → m = w+1): t ≤ m = w+1 → 2·[t odd] (t = w: 0 = f0(0)・t = w+1: 2 = f0(1) で核 cell 一致)。m < t ≤ x → (t+z)%2 = 1−t%2: t 偶 → 1 = f0(t−w) (t ≥ w+2 → arg = 偶 ≥ 2 → f0 = 1)、t 奇 → 0 = f0(t−w) (arg = 奇 ≥ 3 → f0 = 0)。**いずれの偶奇 w も L-BU-GEN と全域一致**。

x = 1 (床 B 子): region (i) (z ≥ 2): m = 1: t ≤ 1 → {0, 2} = 2·[t odd] ✓。w = 0 (z = 1): 閉形式 1 ≤ z ≤ x−1 は x=1 で空、z==x (x=1,z=1)・t∈{0,1} → {0,2} = f0(t) (f0(0)=0, f0(1)=2) ✓ (L(0)=0・s(0)=0)。■

### §2.3 T-GEPSF の奇数 w ステップ (w = 2u+1 ≥ 3・s = w−1・L = w+1・T_w = g1)

**R = 0**: mex ∅ = 0 = 層値 ✓。

**層行 R ∈ {1..w−1}**: 子 budget t = R−1 ≤ w−2 < L。fall/compress/corner 子: 層値 2·[t odd] (= T-GEPSF/T-GEBED(w) at budget t < w+1)。B 子 (m=1): L-BU-GEN at t ≤ w−2 < L → 2·[t odd] (同一の budget 定数)。C 子: T-GEPSF(w−1) 〔even plane・L(w−1) = w−1〕 at budget t ≤ w−2 < w−1 → 層値 2·[t odd] → C = 1⊕2·[t odd]。
選択肢集合: R odd: {0, 1} → mex **2** (= 層値 2·[R odd]) ✓; R even: {2, 3} → mex **0** ✓。

**横断行 R = w (層内最終行・w 奇数)**: 子 budget t = w−1。fall/compress/corner: 層値 at t = w−1 < L → 2·[even] = 0。B: L-BU-GEN t = w−1 < L → 0。
**C 子: budget t = w−1 = L(w−1) → plane w−1 主則域の読み (層域横断)**: f0((δ−1) − s(w−1)) = f0(δ−1−(w−1)) = f0(δ−w)。δ = w−2m (R=w 奇数・偶数 m) → δ−w = −2m ∈ even ≤ −2 → f0 = 0 → **C = 1** (δ の偶奇固定により定数・K1299/K1301 の横断の一般化)。
選択肢集合 {0, 1} → mex **2** = 層値 2·[w odd] ✓。

**seam 行 R = w+1 = L (主張は主則 g1(δ−s))**: 子 budget t = w < L → fall/compress/corner/B: 層値 2·[w odd] = 2。C 子: plane w−1 主則 f0(δ−w): δ = w+1−2m (偶) → arg = δ−w = 1−2m 奇 ≤ −1 → f0 = 1 → **C = 0** (横断 2 列目)。
集合 {2, 0} → mex **1**。主張: g1(δ−(w−1)) at δ = w+1−2m → arg = 2−2m ∈ even ≤ 0 → g1 = [even] = 1 ✓。

**主則 R ≥ w+2**: 子 budget t = R−1 ≥ w+1 ≥ L → 全て主則読み:
- fall 子: g1((δ+1)−s) = **g1(d+1)** (d := δ−s)。
- B 子 (m=1): L-BU-GEN(w) 主則 at t = R−1 = δ+1 ≥ L: g1(t−s) = **g1(d+1)** (fall 再生)。
- compress 子: **g1(d−1)**; corner 子 (g=1): 床主則 at j_c = δ−1 → **g1(d−1)** (compress と同値)。
- C 子: 1 ⊕ T-GEPSF(w−1) 主則 at budget t, δ₂ = δ−1: 1 ⊕ f0((δ−1)−(w−1)) = **1 ⊕ f0(d−1)** (d−1 = 1 すなわち d = 2 のみ C = 3 核例外)。

**一般 mex 表 (d 全域・w を含まない)**:

| d (偶奇・範囲) | fall/B g1(d+1) | comp/corner g1(d−1) | C (d=2 → 3) | 集合 S | mex | 主張 g1(d) |
|---|---|---|---|---|---|---|
| odd, d ≤ −1 | g1(even ≤ 0) = 1 | g1(even ≤ −2) = 1 | 1⊕f0(even ≤ −2) = 1 | {1} | 0 | [even] = 0 ✓ |
| d = 1 (核) | g1(2) = 0 | g1(0) = 1 | 1⊕f0(0) = 1 | {0,1} | 2 | g1(1) = 2 ✓ |
| d = 3 | g1(4) = 0 | g1(2) = 0 | 1⊕f0(2) = 0 | {0} | 1 | [odd] = 1 ✓ |
| odd, d ≥ 5 | 0 | 0 | 0 | {0} | 1 | 1 ✓ |
| even, d ≤ −2 | g1(odd) = 0 | g1(odd) = 0 | 1⊕f0(odd ≤ −3) = 0 | {0} | 1 | [even] = 1 ✓ |
| d = 0 | g1(1) = 2 | g1(−1) = 0 | 1⊕f0(−1) = 0 | {2,0} | 1 | g1(0) = 1 ✓ |
| d = 2 (C 核) | g1(3) = 1 | g1(1) = 2 | 3 | {1,2,3} | 0 | g1(2) = 0 ✓ |
| even, d ≥ 4 | 1 | 1 | 1 | {1} | 0 | 0 ✓ |

d は主則域で全整数を取る (m を通じて d = δ−s = R−2m−s・R ≥ w+2 で m ≥ 1 を任意に動かせば全 d; バンド条件 k ≤ 0 は g ≥ δ を選べば常成立)。全行 mex = 主張。■

### §2.4 T-GEPSF の偶数 w ステップ (w = 2u ≥ 4・s = w・L = w・T_w = f0)

**R = 0**: 0 ✓ (= f0(−2m−w) = 0 とも一致)。

**層行 R ∈ {1..w−1}**: 子 budget t ≤ w−2。fall/compress/corner: 層値 2·[t odd]。B: 層値。C 子: T-GEPSF(w−1) 〔odd plane・L(w−1) = w〕at budget t ≤ w−2 < w → 層値 2·[t odd] → C = 1⊕2·[t odd] (**層厚一致 (w, w) で横断ゼロ**)。集合 {0,1}/{2,3} → 2/0 ✓。

**seam 行 R = w (crossing-zero の継ぎ目)**: 子 budget t = w−1 < L。fall/compress/corner: 層値 2·[(w−1) odd] = 2 (w 偶数)。B: 同一。C 子: budget t = w−1 < L(w−1) = w → plane w−1 の**層値** 2·[(w−1) odd] = 2 → **C = 3** (下位面の層値 2 を読む {2,3}→0 型・K1290 z6/K1294 z8/K1299 z10/K1301 z12/K1302 z14 の一般化)。
集合 {2, 3} → mex **0**。主張 f0(δ−w) at δ = w−2m 偶 → arg even ≤ −2 → 0 ✓。

**主則 R ≥ w+1**: 子 budget t = R−1 ≥ w = L → 全て主則読み:
- fall/B: f0((δ+1)−w) = **f0(d+1)** (d := δ−w・B は L-BU-GEN(w) 主則 f0(t−w) = f0(d+1) で fall 再生)。
- compress/corner: **f0(d−1)**。
- C 子: 1 ⊕ T-GEPSF(w−1) 主則 at budget t ≥ w = L(w−1): T_{w−1} = g1, δ₂ = δ−1 → 1 ⊕ g1((δ−1)−(w−2)) = **1 ⊕ g1(d+1)** (d+1 = 1 すなわち d = 0 のみ C = 3 核例外)。

**一般 mex 表 (d 全域・w を含まない)**:

| d (偶奇・範囲) | fall/B f0(d+1) | comp/corner f0(d−1) | C (d=0 → 3) | 集合 S | mex | 主張 f0(d) |
|---|---|---|---|---|---|---|
| odd, d ≤ −1 | f0(even ≤ 0) = 0 | f0(even ≤ −2) = 0 | 1⊕g1(even ≤ 0) = 0 | {0} | 1 | [odd] = 1 ✓ |
| d = 1 (核) | f0(2) = 1 | f0(0) = 0 | 1⊕g1(2) = 1 | {1,0} | 2 | f0(1) = 2 ✓ |
| odd, d ≥ 3 | f0(even ≥ 4) = 1 | f0(even ≥ 2) = 1 | 1⊕g1(even ≥ 4) = 1 | {1} | 0 | [even] = 0 ✓ |
| even, d ≤ −2 | f0(odd) = 1 | f0(odd) = 1 | 1⊕g1(odd ≤ −1) = 1 | {1} | 0 | f0(even ≤ −2) = 0 ✓ |
| d = 0 (C 核) | f0(1) = 2 | f0(−1) = 1 | 3 | {2,1,3} | 0 | f0(0) = 0 ✓ |
| d = 2 (comp 核) | f0(3) = 0 | f0(1) = 2 | 1⊕g1(3) = 0 | {0,2} | 1 | f0(2) = 1 ✓ |
| even, d ≥ 4 | 0 | 0 | 0 | {0} | 1 | 1 ✓ |

全行 mex = 主張。■

### §2.5 T-GEBED の証明 (奇数 w・偶数 w・床)

床 (m,m)@w, R = 2m+j, j ≤ 0。子: fall (m ≥ 2: pair (m−1,m)@w, δ_c = j+1)、B (m=1: {0,2})、C (1 ⊕ b_{w−1}(R−1, j−1))。

**層行 R < L (両偶奇)**: fall: 層値 2·[t odd] (budget t = R−1); B: 同一 (m=1: R ≤ 2 のみ); C: b_{w−1} 層値 (budget t < L(w−1): 奇数 w は t ≤ L−2 = w−1 < w ✓; 偶数 w は t ≤ L−1 = w−1 < w ✓ いずれも平面 w−1 の層域内) → C = 1⊕2·[t odd]。集合 {0,1}/{2,3} → 2/0 = 層値 ✓。

**奇数 w・横断行 R = w**: 子 budget t = w−1 = L(w−1): fall: 層値 at t = w−1 < L → 0 (2·[even])。C: b_{w−1} 主則 f0((j−1)−(w−1)) = f0(j−w): j = w−2m 奇 → arg = −2m even ≤ −4 (m ≥ 2: R=w ≥ 3 → j ≤ −1 → m ≥ 2) → f0 = 0 → C = 1。集合 {0,1} → mex 2 = 層値 2·[w odd] ✓。(m = 1 は R = w ≥ 3 で不成立・B 子なし。)

**奇数 w・seam 行 R = w+1 (= L・床)**: 子 budget t = R−1 = w < L → fall: 層値 2·[w odd] = 2 (w ≥ 3 では m ≥ 2 で B 子なし。w=1, j=0 の m=1 列は B 子の選択肢 {0,2} ⊆ S で結論不変)。C 子: plane w−1 主則 f0((j−1)−(w−1)) = f0(j−w): j = w+1−2m 偶 ≤ 0 → arg = j−w = 偶−奇 = 奇 ≤ −w (w ≥ 3 で ≤ −3・w=1, j=0 で −1・いずれも ≤ −1) → f0 = 1 → **C = 0** (横断 2 列目・K1299/K1301 横断面の一般化)。集合 {2, 0} → mex **1**。主張 g1(j−(w−1)) = g1(偶 ≤ 0) = 1 ✓。

**奇数 w・主則 R ≥ w+2**: fall 子は plane w の pair 主則を δ_c = j+1 で読む: g1(δ_c − s(w)) = g1((j+1)−w) = **g1(j−w+2)**。C 子は plane w−1 (偶数面・床上の座標 j−1) を読む: T_{w−1} = f0, s(w−1) = w−1 なので arg = (j−1)−(w−1) = j−w → **C = 1 ⊕ f0(j−w) = g1(j−w)** (j ≤ 0・w ≥ 1 → 引数 ≤ −1 ≠ 1 で T-TWIN 適用可)。
表 (j = R−2m・m ≥ (w+2)/2。d := j−(w−1) は §2.3 の mex 表の d に一致し、以下は同表の該当行の床実現):
- **j 奇 (j ≤ −1)**: fall 引数 j−w+2 = 偶 ≤ 1−w ≤ 0 → g1 = 1・C 引数 j−w = 偶 ≤ −2 → **C = 1⊕f0(偶 ≤ −2) = 1** → S = {1} → mex **0** = 主張 g1(奇 ≤ −1) = 0 ✓
- **j 偶 (j ≤ 0), w ≥ 3**: fall 引数 = 奇 ≤ −1 → g1 = 0・C 引数 = 奇 ≤ −3 → **C = 1⊕f0(奇 ≤ −3) = 0** → S = {0} → mex **1** = 主張 g1(偶 ≤ −2) = 1 ✓
- **境界 j = 0, w = 1** (R = 2m・m ≥ 2): fall 引数 1 → g1(1) = 2・C 引数 −1 → **C = 1⊕f0(−1) = 0** → S = {2, 0} → mex **1** = 主張 g1(0) = 1 ✓

**偶数 w・seam 行 R = w**: fall: 層値 at t = w−1 → 2·[(w−1) odd] = 2。B (m=1: R = w ≤ 2 は w ≤ 2 のみ・w ≥ 4 なら不成立; w=2 は K1288 基底)。C: b_{w−1} at budget t = w−1 < L(w−1) = w → 層値 2·[(w−1) odd] = 2 → C = 3。集合 {2,3} → mex 0。主張 f0(j−w): j = w−2m 偶 → arg even ≤ −w ≤ −4 → 0 ✓。

**偶数 w・主則 R ≥ w+1**: fall: f0((j+1)−w) = **f0(j−w+1)**; C: 1 ⊕ T_{w−1} 床主則 = 1 ⊕ g1((j−1)−(w−2)) = 1 ⊕ g1(j−w+1) = **f0(j−w+1)** (arg = j−w+1 ≤ 1−w ≤ −3 ≠ 1・T-TWIN; corner 系核 d=0 例外は j = w で不在)。集合 {f0(j−w+1)}: j 奇 → arg even ≤ 2−w ≤ −2 → 0 → mex 1 = f0(odd ≤ −w−1) = 1 ✓; j 偶 → arg odd ≤ 1−w ≤ −3 → 1 → mex 0 = f0(even ≤ −w) = 0 ✓。■

### §2.6 帰納構造のまとめ (well-founded 性)

- **外側帰納 (w)**: 基底 w = 0 (K1286 T-PD0/T-B0)・w = 1, 2 (K1288 T-PDT1/T-BDT1/T-PDT2/T-BDT2) は既刊。step: **偶奇ごとの 2 case** (§2.3 奇数・§2.4 偶数) で packet {T-GEPSF(w), T-GEBED(w)} を **T-GEPSF(w−1)/T-GEBED(w−1) の全 R 値 (外側帰納仮定) のみから** 導出 (C 子)。
- **内側帰納 (R)**: packet 内で R に強帰納 (全子 budget R−1・corner は床・fall は pair で相互参照も budget 低下で閉じる)。
- B 子 (pair・床の m=1) と B-exit 再生子は **L-BU-GEN (§2.2・閉形式から帰納外に全称済み)** で評価・参照は K0832 既刊閉形式のみ。
- 場合表は §2.3/§2.4/§2.5 の **w を含まない表** (d の偶奇と範囲・境界行の定数) のみで、**全ての (m, g, R) を尽くす** (d = δ−s は主則域で全整数を取る・バンド条件は子の座標で自動保存 [k_c = k ≤ 0 / j_c ≤ 0 は各 child 型で直接確認済み・explore2 Y4 が境界行の engine 再照合 895 点])。
- per-plane 世代パッケージ (K1289..K1302) の δ-平行移動表が全て本項の一般表の実例であったことがこれで構造的に確定する (添字の核 cell: 奇数 w は d = 1 = 層核 (nucleation・mex{0,1}=2) と d = 2 = C 核・偶数 w は d = 1 = 核・d = 0 = C 核・d = 2 = comp 核 (mex{0,2}=1)。mex{0,1}=2 / mex{2,3}=0 / mex{0,2}=1 の 3 core 機構は例外層 R-定数値を含め w 非依存 (C4))。

### §2.7 honest 記述 (宣言前に捕捉した電池設計の誤り)

- explore1 X4 (crossing/seam 行の徹底調査) の初版は床 side の R window filter `L−2 ≤ Rb ≤ L+4` に **Rb ≥ 0 guard を欠き**、w ∈ {0,1,2} の L−2 < 0 で R = −1/−2 の 無効 cell (engine 定義域外・H(−1,·) の recursion fallthrough が値 2 を返す) 8 cell を bad として指摘した。宣言前の調査で当該 8 cell が电池設計の誤り (定義域外) と判明し guard を追加して再実行 (X4 77,060 点 bad 0)。定理側の反例ではなく K1301 §2.7 と同一趣旨の honest 記録としてここに残す。
- m・g 依存性は宣言前探索全域 (planes 0..24・m ≤ 32 の far-m・dedup 320 (R,δ) cell × 21 面 mixed 0) で一度も観測されていない。主張は §2 の手証明による全称主張であり census は照合である。

## §3 宣言前探索 (pre-declaration; explore_k1303.py / explore2_k1303.py 出力)

- **X1** 一般 band census planes w=0..16 (m≤12, g≤25, k∈[max(−60,−2m−g),0]) **137,700 点 bad 0** (17 面全域で per-plane 主張と一般則が完全一致)。
- **X2** 一般 bed census planes 0..16 (m≤14, j∈[−30..0]) **3,808 点 bad 0**。
- **X3** typed 自己検査 (子を一般申立テーブル plane w / w−1 + 閉形式のみで構成した mex が申立値・engine と一致) planes 0..16, m≤10, g≤14, k≥−14 + 床 m≤10, j≥−16: **34,901 点 bad 0** (手証明 §2 構文の全 cell 機械検証)。
- **X4** crossing/seam 行徃底 R∈[max(0,L−2),L+4] planes 0..16, m≤26, g≤40 (k∈[−40..0]) + 床行 m≤26: **77,060 点 bad 0** (8 無効 cell は §2.7 参照)。
- **X5** L-BU-GEN 閉形式×一般則×engine w≤30, x≤34 (3 region 被覆): **19,499 点 bad 0**。
- **X6** 新規面 w=17..20 (m≤12, g≤16, k≥−40 + 床): **17,952 点 bad 0** (z19/z20 は K1303 以前に未観測)。
- **X7** dedup (R,δ) sweep z=0..20: **全 21 面 mixed 0 (320 cell/面)・cpsf_bad 0** (K1302 は z≤18 まで)。
- **X8** cross-engine ordered vs canonical planes {0,5,11,13,16,19}: **3,648 点 mismatch 0**。
- **Y1** **シンボリック mex 表メタ検査 d∈[−3000..3000]**: 奇数 w 表 mex{g1(d+1), g1(d−1), 1⊕f0(d−1) (d=2 → 3)} = g1(d)・偶数 w 表 mex{f0(d+1), f0(d−1), 1⊕g1(d+1) (d=0 → 3)} = f0(d)・**12,002 点 bad 0** (§2.3/§2.4 の 2 表が d の偶奇別全範囲で閉じることの直接照合)。
- **Y2** L-BU-GEN wide w≤36, x≤48, t≤x: **45,288 点 bad 0**。
- **Y3** 核心/核 cell 遠方 m≤48, planes {3,9,13,16}, δ−s∈{0,1,2,3} (k=0 行): **768 点 bad 0**。
- **Y4** 奇数 w 横断・seam 行の C 子定数性 (engine 直接 vs 表 w∈{3,5,...,21}, R∈{w,w+1}, m≤20, g≤12): **895 点 bad 0**。

## §4 機体宣言 (machine declaration, publish-then-execute)

`verify_k1303.py` sha256 (kit で宣言):
`1efdcf9e2776e4e57ee452f3d1fee823d1fa2d7eaa87e7ff853ba9a4edf2af0c`
・engine pin `bd5f22e415a78368c9b798296bc84948d5637decbf3c21a92404d45fb12e3a92`
startup gate 内蔵 (embed は K1138/K1282..K1302 と同一 bytes)。engine_block.py (import 用単体) sha256
`582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0`
(K1282..K1302 kit と byte-identical)。全 battery が同一の一般則関数 cpsfG を plane 0..24 で走査 (per-plane 特殊分岐なし・typed 構造は D3 が全平面で同型)。

| # | 内容 | 期待 count |
|---|---|---|
| D1 | 一般 band census engine vs CPSF-GEN planes w=0..16 (m≤12, g≤25, k∈[max(−60,−2m−g),0]) | 137,700 |
| D2 | 一般 bed census engine vs BED-GEN planes w=0..16 (m≤14, j∈[−30..0]) | 3,808 |
| D3 | typed 一般自己検査 (typed mex == 申立 == engine) planes 0..16, m≤10, g≤14, k≥−14・床 j≥−16 | 34,901 |
| D4 | crossing/seam 行 census R∈[max(0,L−2),L+4] planes 0..16, m≤18, g≤26 (k∈[−26..0])・床行同 window (R≥0 guard 付) | 41,124 |
| D5 | L-BU-GEN 閉形式 == CPSF-GEN(w,t,t) == engine (w≤30, x≤34) | 19,499 |
| D6 | 単一トークン閉形式×両 engine (x≤16, z∈2..13, R∈[x+1..x+4]) | 1,440 |
| D7 | 包摂 identity sweep: 既刊 per-plane 主張転写 (z0..z14) == CPSF-GEN == engine, w=0..14 (m≤10, g≤18, k≥−12・床 j≥−12) | 35,175 |
| D8 | 新規面 census w=17..20 (m≤12, g≤16, k≥−40・床 j≥−24) | 17,952 |
| D9 | T-TWIN 代数恒等式 d∈[−260..260] | 521 |
| D10 | cross-engine canonical vs ordered planes {0,5,11,13,16,19} | 3,954 |
| D11 | stress: far-m 行 (planes {3,9,13,16}, m∈[13..32]) 23,520 + dedup (R,δ) z=0..20 6,720 + spot planes w=21..24 6,132 | 36,372 |

**総計 332,446 点・期待 overall_bad 0**。predry 4 走 (同一 cwd・PYTHONHASHSEED random/1/99/7): stdout **byte-identical sha256 `af25dfac45327bea7769bffb03197b26f76f7e67799919e5d68f07b0d79109f2566`** (= 本項で宣言)。

**変異電池 (5 種・期待値を事前宣言)**:
- `--tamper-engine`: rc 2 (engine の `q_odd` を 1 文字変異 → embed sha256 `0ea47a80…` ≠ pin・tamper_engine.info は size 0)。
- `--tamper=hl` (D1 band census の申立 flip〔0↔1, 2→1〕): rc 1・**bad D1 = 137,700** (全 cell 不一致)・他 0。
- `--tamper=hbd` (D2 bed census flip): rc 1・**bad D2 = 3,808**・他 0。
- `--tamper=ws` (T_w 偶奇入替 g1↔f0 を全 battery に適用・グローバル): rc 1・bad = **[91832, 2072, 23274, 29788, 7145, 0, 26447, 4242, 0, 0, 27432]** (D6/D9/D10 は主張表に非依存のため 0)・総 bad **212,232**。
- `--tamper=Ls` (層厚 L(w)+2 を全 battery に適用): rc 1・bad = **[6880, 250, 2144, 8631, 270, 0, 1765, 705, 0, 0, 457]**・総 bad **21,102**。

公式監査 discipline: kit 出版 → raw fetch-back byte 照合 (verify sha・engine_block・predry 4 走) → 公式 4 走 (fetch-back bytes から・同一 cwd×2 [PYTHONHASHSEED random/1] + 隔離 tree×2 [isoA/isoB・env -i・PYTHONHASHSEED 99/7])、全走 stdout byte-identical であること・detcheck.json は 4 走 sha 一致を機械記録 → 変異電池 5 種の rc/bad 個数が本宣言に一致すること → 成果物出版 (audit_run1-4.out+.info・tamper 5 種×2・detcheck.json・MANIFEST-sha256) + fetch-back。

## §5 open 登録 (本項で新規・継承)

- **O-G1 (giant 接続・継承)**: ペア面 z∈{0..∞} の対角下全域 k ≤ 0 が **全 w で O(1) 即値評価化** した (本項で全平面が閉形式に)。11×11 巨大探索の枝刈り格子の境界側拡張として 4象限… 接続記録のみ・採用判断は giant レーンオーナー (K1286 以来の取り扱いを維持)。
- **O-G2 (内面 k ≥ 1)**: multi-c web F2/F3 (K1285/K1287) は非接触・open のまま。
- **O-G3 (3-トークン以上)**: ペア (2 Token)・床 の一般則は本項で完結。3 Token 以上の plane-shift 構造は**未着手・データなし** (将来レーン)。
- **O-G4 (far above-diagonal)**: k > 0 の上半域 (pre-band 上方) はこれまで通り open (本項のバンド k ≤ 0 と K1286 境界の外)。

## §6 主張の区別 (honest)

- **全称定理**: T-GEPSF / T-GEBED / L-BU-GEN / C1..C4 (§2 の手証明・.games 定義の帰納からの導出)。
- **有限照合 (census)**: D1..D11 332,446 点・explore X/Y 系。定理の実機照合であって証明の一部ではない。
- **非主張**: 11×11 標準空盤・19 central-reply roots・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 の勝敗は全時点 UNKNOWN・verdict 不消費・被覆/secured は主張しない。nodes 数等を勝敗として読まない。
