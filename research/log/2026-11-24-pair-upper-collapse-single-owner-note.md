# 単一オーナー宣言 K1308: 上半畳み込みパッケージ — T-UH・T-DU′・Z-DIAG・L-SB（K1303 O-G4 far above-diagonal k>0 の全称閉包・finite で止まらない）

- 日付: 2026-11-24
- lane: 高速レーン（短〜中時間・厳密結果）。本ノートは fast-lane の単一オーナー宣言
  （publish-then-execute: 本ノートが最初に出版され、機体・監査はその後從属）。
- 観測 HEAD（着手時・main）: 着手直前 `295b9505`（Part DW completion 22:16:48Z・11×11
  b35loss26 canonical adoption・規約どおり verdict 皆不消費の長期レーン）。過去 1 時間の
  items/log 系列は: K1303 公刊 (`4e132464`)・K1304/K1305（PG(2,9) cap games・直交）・
  **K1306 宣言** (`53d2d335`・SLB/L/E typed-child frontier・単一層トークン多重度族で非接触)・
  **K1307(仮) 宣言** (`4d2d506a`・REMO 3-branch cap<=16 r=3 sweep・非接触)・Part DV/DW
  （11×11 batch-35・非接触）。**push 直前に再度 main を取り直し、K1308 の空きを再確認する**。
- 位置づけ: K1303 が §5 open 登録 **O-G4「far above-diagonal k > 0 (untouched)」** として残した
  領域の全称確定。到達済み成果との関係: K1285 T-PS0/1/2（z0 k1..3 / z1 k2..3 / z2 k3..4 の
  [g odd]）・K1285 T-ALM 六床・K1286 T-Z1(1,·)/T-Z2(1,·)/T-Z2(2,·)（z1-k1 / z2-k1 / z2-k2）・
  K1286 T-B1/T-B2 境界床・K1303 帶域定理（k ≤ 0・全 plane）はいずれも**下位アンカー・被包**
  であり対抗宣言ではない。K1138 再帰 engine・K0832 単一トークン閉形式は既刊の依存。
- 規約: verdict 不消費。標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4
  は全時点 UNKNOWN のまま。engine はゲーム定義の転写（sha pin 実装）であり、census は照合
  であって証明の代替ではない。

## 用語・記法（K1285/K1286/K1303 準拠）

残余ゲーム H(R; X; z)（K1138 再帰・値は mex・H(0;·)=0）。局面の選択肢（K1285 §2.0 規約）:

- **A手**（トークン w>1 を w−1 に圧縮・R→R−1・plane 不変）。ペア (m, m+g) では下トークンを
  **fall**（pair (m−1, m+g)・gap g+1・k 不変）、上トークンを **compress**（pair (m, m+g−1)・
  gap g−1・k 不変）、g=1 の compress は **corner**（bed (m,m)・k 不変）と呼ぶ。
- **B手**（トークン 1 を除去・R→R−1・plane z→z+1）。m=1 の fall は B-exit 単一トークン
  v(g+1, z+1, R−1) になる。
- **C手**（z≥1 で子の値 1 XOR・R→R−1・plane z−1）。子は同 multiset で k→k−1。

**対角座標**（K1285 準拠）: k := R − 2m − g（ペア）・k := R − 2a（床）。K1303 が確定した
帶域は k ≤ 0（全 plane）。本パッケージは **k = z（対角行）と k ≥ z+1（上半 tail）** を確定する。
単一トークン閉形式 v(x, p, R) = single_token（K0832・キット engine_block.py に転写）。

## §1 主張

### 定理（全称・量化は非有界・証明全文は §2）

- **T-UH（上半 tail 一様性・真の安定化長）**: ∀ z ≥ 0, m ≥ 1, g ≥ 1, k ≥ z+1:
  **H(2m+g+k; (m, m+g); z) = [g odd]**。値は m・k・z 非依存。k ≥ z+1 が安定化の
  正確な閾値: k = z 行は下の Z-DIAG に従い一般に [g odd] と一致しない
  （g ≤ z では一致、g = z+1 で 2、g ≥ z+2 で補値 [g even] = 1−[g odd]）。
- **T-DU′（床の上半消滅）**: ∀ z ≥ 0, a ≥ 1, k ≥ z: **H(2a+k; (a, a); z) = 0**。
  z=1, k=0（b1(0)=1）・z=2, k=1（b2(1)=2・共に K1286 公刊）が閾値の直下非零例
  （シャープ）。z ≥ 3 の k = z−1 行は census で 0 に見えるが本項では主張しない（§5 O2）。
- **Z-DIAG（対角行 3 分岐則・全 plane）**: ∀ z ≥ 0, m ≥ 1, g ≥ 1, k = z:
  **H(2m+g+z; (m, m+g); z) = [g odd] (g ≤ z) / 2 (g = z+1) / [g even] (g ≥ z+2)**。
  アンカー: z=0 は f0 対角（K1286 T-PD0 の k=0 側・C1）、z=1 は Z1(1,·)（C2）・
  z=2 は Z2(2,·)（C3）と同一函数。K1285 OBS-D9 境界三角形の対角 3 脚は本定理の
  z=0,1,2 instance（公刊済み・照合）。
- **L-SB（単一トークン tail 読み・K0832 閉形式から直接導出）**: ∀ x ≥ 2, p ≥ 1, j ≥ p:
  **v(x, p, x+j) = x%2**。B-exit 境界読み（証明で使用）: v(z+1, z+1, 2z+1) = 2・
  v(z+2, z+1, 2z+2) = (z+1)%2・v(1, p, R) = 1 (R ≥ 2)・v(1, 1, 1) = 2。

### 被包関係（既刊の全称昇格・§2 で同一式として照合）

- K1285 T-PS0/1/2 ⟸ T-UH（z=0 k∈{1,2,3} / z=1 k∈{2,3} / z=2 k∈{3,4} は
  k ≥ z+1 の部分族）。
- K1285 T-ALM 六床（(m,m)@2m+2 z0 / 2m+3 z0 / 2m+2 z1 / 2m+3 z1 / 2m+3 z2 /
  2m+4 z2 = 0）⟸ T-DU′（すべて k=2,3,2,3,3,4 ≥ z=0,0,1,1,2,2）。
- K1282 T-Q corner (m,m)@2m+1 z0 = 0 ⟸ T-DU′（k=1 ≥ z=0）。参照として既刊。
- K1286 T-Z1(1,·)/Z2(2,·) ⟸ Z-DIAG の z=1/z=2 instance。K1286 C4（z2-k1 = [g odd]
  clean）は本パッケージの**境界アンカー**（z2 の window 最上段）として使用。
- K1286 T-B1/T-B2（b1(1)=0・b2(1)=2・b2(2)=0）⟸ b1(1) は T-DU′、b2(1)=2 は T-DU′ の
  閾値下、b2(2)=0 は T-DU′。シャープネス照合用の再掲。
- **面の完全閉包（到達点の要約）**: K1303（k ≤ 0・全 plane）と Z-DIAG（k=z）と T-UH
  （k ≥ z+1）と K1286 C4（z2-k1）の和で、**ペア面 z = 0, 1, 2 は全ての k（到達可能な
  全 R 域）で確定**した。同様に床は z = 0（T-B0 j ≤ 0 + T-DU′ k ≥ 0）・z = 1（b1 帶 j ≤ 0
  + T-DU′ k ≥ 1）・z = 2（b2 帶 + b2(1)=2 + T-DU′ k ≥ 2）で確定。z ≥ 3 の未確定は
  遷移窓 1 ≤ k ≤ z−1（ペア・床）のみ。

### census 予想・観測（主張は本項・§6 参加資格を明記）

- **C-SUM（census 予想・全称主張しない）**: tail 域での値は **[S odd]**（S = トークン総和）。
  既証明側: 単一 x → x%2 = [x odd] ✓、ペア {m,m+g} → [g odd] ✓（S=2m+g）、床 {a,a}
  → 0 ✓（S 偶数）。新 census: 3 重単一コピー a<b<c ≤ 8 × z0..5 × k=z+2..z+5 = 1,344 点
  bad 0・混合 3 重 {a,a,b}/{a,b,b} a<b ≤ 7 × z0..4 × k=z+2..z+5 = 840 点 bad 0・
  4 重 a<b<c<d ≤ 6 × z0..2 × k=z+3..z+6 = 180 点 bad 0。閾値構造（多重度依存）は §5 O3。
- **REFUTED（honest 記録・宣言前探索で反例確定）**: 遷移窓（1 ≤ k ≤ z−1・z ≥ 3）の
  偶奇交互予想「k ≢ z (mod 2) の行は tail 値 [g odd]」は **z ≥ 4 で反例 29 件**
  （census z3..8 × m1..3 × g1..12・非合同行 540 個中）。分布 z=4:5, z=5:2, z=6:8,
  z=7:4, z=8:10（z=3 は 0・全反例リストは機体 obs に凍結）。**予想は本項で棄却され、
  窓の真の法則は open（§5 O1）**。
- **OBS-WC（生き残り半分・観測登録・未証明）**: 窓の**合同行** k ≡ z (mod 2)（k = z−2,
  z−4, …）は **Z-DIAG(g, z) と一致**する様に見える: census z3..13 × m1..3 × g1..12 の
  合同行 1,296 点 mismatch 0。全称主張しない。
- **OBS-BW（床窓行・観測登録・未証明）**: 床の k = z−1 行は z=1 で 1・z=2 で 2
  （K1286 公刊どおり）だが **z ≥ 3 では census（a ≤ 4, z3..6）で 0**。§5 O2。

## §2 証明全文

### 2.0 帰納パケットと well-founded 性

主治法は K1285 §2 の族閉性証明の上半版 typed- mex 構文（K1286 §2 typed-children と同型）:

**パケット P(R)**（予算 R の主張族）:
- T-UH cell: pair (m, m+g)@(R=2m+g+k, z), k ≥ z+1 → [g odd]
- Z-DIAG cell: pair (m, m+g)@(R=2m+g+z, z), k = z → 3 分岐則
- T-DU′ cell: bed (a,a)@(R=2a+k, z), k ≥ z → 0

**子型閉包（全子が予算 R−1 で パケット内 または K0832 閉形式）**:
ペア cell の子は (i) fall: pair (m−1, m+g) 同 plane・k 不変（m ≥ 2）/ (i′) B-exit:
単一トークン v(g+1, z+1, R−1)（m=1）/ (iii) compress: pair (m, m+g−1) 同 plane・k 不変
（g ≥ 2）/ (iii′) corner: bed (m,m)@(R−1, z)・k 不変（g=1・床 cell で k ≥ z）/ (v) C:
pair 同 multiset・plane z−1・k−1（z ≥ 1）。床 cell の子は fall: pair (a−1, a) gap 1・k 不変
（a ≥ 2）/ B: 単一トークン 1@plane z+1（a=1）/ C: 床@plane z−1・k−1。

**k 座標の不変量**: A手子（fall/compress/corner）は **k 不変**（子の和が −1 され R も −1）。
C手子は k−1。よって:
- T-UH cell（k ≥ z+1）: fall/compress 子は同 plane で k 不変 ≥ z+1（T-UH 子・R−1）; corner
  子は床で k ≥ z+1 ≥ z（T-DU′ 子）; C 子は plane z−1 で k−1 ≥ z = (z−1)+1（T-UH 子）; 
  B-exit 子は閉形式（§2.4）。
- Z-DIAG cell（k = z）: fall/compress 子は同 plane で k = z（Z-DIAG 子）; corner 子は床で
  k = z ≥ z（T-DU′ 子）; C 子は plane z−1 で k−1 = z−1（Z-DIAG 子）; B-exit 子は閉形式。
- T-DU′ cell（k ≥ z）: fall 子は gap-1 ペアで k 不変（k ≥ z+1 → T-UH 子=1 / k = z →
  Z-DIAG 子 = Z-DIAG(1,z) ∈ {1, 2}）; C 子は plane z−1 で k−1 ≥ z−1（T-DU′ 子）; B 子は
  閉形式。

**well-founded 性**: 主張は「予算 R についての強帰納」で同時に閉じる。全子の予算は
ちょうど R−1 であり、子の型は上表のとおり常に パケットの（R−1 の）主張または既刊の
K0832 閉形式（予算非依存の閉じた結果）である。A 連鎖で z は不変・k 不変、C 連鎖で
k と z が同時に −1 されいずれも単調減少、B-exit は即時終端（閉形式）。再帰は R の自然数
順序で必ず停止し、帰納の基底部は R ≤ 3 の有限検証（下記 2.5）でよい。

### 2.1 T-UH の証明（tail 一様性）

Cell: pair (m, m+g)@(R=2m+g+k, z)、k ≥ z+1、主張 c0 := [g odd] ∈ {0,1}。選択肢:

- (i) fall（m ≥ 2）: pair gap g+1、k 不変 ≥ z+1 → 帰納値 [g+1 odd] = 1−c0。
- (i′) B（m=1）: 単一トークン x := g+1、plane p := z+1、t := R−1 = g+k+1。
  x+p = g+z+2 に対し t − (x+p) = k−z−1 ≥ 0、すなわち t = x+p+(k−z−1) で
  j := t−x = p+(k−z−1) ≥ p。L-SB（§2.4）より v = x%2 = (g+1)%2 = 1−c0。
- (iii) compress（g ≥ 2）: pair gap g−1、k 不変 → [g−1 odd] = 1−c0。
- (iii′) corner（g=1）: bed (m,m)@(R−1, z)、k_bed = k ≥ z+1 ≥ z → T-DU′（帰納）で 0。
  c0 = [1 odd] = 1 なので 1−c0 = 0 ✓。
- (v) C（z ≥ 1）: plane z−1・k−1 ≥ z = (z−1)+1 → 帰納値 [g odd] = c0、
  C 選択肢値 = 1 XOR c0 = 1−c0。

全ての選択肢値は 1−c0。選択肢集合 = {1−c0} は 1 元だから、
c0 = 0 なら mex{1} = 0 = c0、c0 = 1 なら mex{0} = 1 = c0。∎

**補足（均一化）**: 証明は「tail cell の全子が 1−c0」の均一化に尽きる。機体 D4 は
typed 子表から mex を再構成し、さらに k ≥ z+1 の全 cell で **set(children) = {1−claim}**
（均一化そのもの）を点ごと検証する。

### 2.2 Z-DIAG の証明（対角行 3 分岐・全 plane）

Cell: pair (m, m+g)@(R=2m+g+z, z)。記号: fall 値 F(g) := Z-DIAG(g+1, z)（m ≥ 2）、
compress 値 Cmp(g) := Z-DIAG(g−1, z)（g ≥ 2）、corner 値（g=1）: bed k=z → 0、
B 値（m=1）: 閉形式読み、C 値（z ≥ 1）: 1 XOR Z-DIAG(g, z−1)。使用する閉形式読み
（§2.4・B 値）: **B(g, z) = [g even] (g ≤ z−1) / 2 (g = z) / [g odd] (g ≥ z+1)**。

**領域 A（g ≤ z・主張 [g odd] =: c）**:

- g odd（c=1）: F = [g+1 odd] = 0（g ≤ z−1）、または g = z で F = Z-DIAG(z+1, z) = 2。
  Cmp = [g−1 odd] = 0（g ≥ 3）・g=1 は corner = 0。B = [g even] = 0（g ≤ z−1）・
  g = z で B = 2。C = 1 XOR [g odd] = 0（g ≤ z−1）・g = z で
  C = 1 XOR Z-DIAG(z, z−1) = 1 XOR 2 = 3。z = 0 では領域 A は空。
  いずれの分岐でも選択肢集合は 0 を含み **1 を含まない**（値 ⊆ {0, 2, 3}）→ mex = 1 = c。✓
- g even（c=0）: F = [g+1 odd] = 1（g ≤ z−1）・g = z で F = 2。Cmp = [g−1 odd] = 1
  （g ≥ 2 なので g even ⇒ compress が存在・corner はない）。B = [g even] = 1
  （g ≤ z−1）・g = z で B = 2。C = 1 XOR [g odd] = 1（g ≤ z−1）・g = z で C = 3。
  選択肢値 ⊆ {1, 2, 3} は **0 を含まない** → mex = 0 = c。✓

**領域 B（g = z+1・主張 2）**: F = Z-DIAG(z+2, z) = [z+2 even] = [z even]。
Cmp = Z-DIAG(z, z) = [z odd]。B = [g odd] = [z+1 odd] = [z even]。C = 1 XOR
Z-DIAG(z+1, z−1) = 1 XOR [z+1 even] = 1 XOR [z odd] = [z even]（g = z+1 ≥ (z−1)+2）。
m ≥ 2 なら選択肢 {F, Cmp, C} = {[z even], [z odd]}、m = 1 なら {B, Cmp, C} =
{[z even], [z odd]}。いずれも 0 と 1 を含み **2 を含まない** → mex = 2。✓
z = 0 では領域 B は g = z+1 = 1 で compress は存在せず corner になる:
m ≥ 2 なら選択肢 {corner: bed (m,m)@(2m+1, 0)（k=1 ≥ z=0 → T-DU′）= 0,
F = Z-DIAG(2, 0) = [2 even] = 1} → {0, 1} → mex 2 ✓、m = 1 なら
{corner: bed {1,1}@(2, 0) = 0, B: v(2, 1, 2) = 1} → {0, 1} → mex 2 ✓
（§2.5 基底部と同じ局面）。

**領域 C（g ≥ z+2・主張 [g even] =: v）**: F = Z-DIAG(g+1, z) = [g+1 even] = [g odd]。
Cmp = Z-DIAG(g−1, z): g−1 = z+1（g = z+2）のとき 2、それ以外は [g−1 even] = [g odd]。
B = [g odd]（g ≥ z+1）。C = 1 XOR Z-DIAG(g, z−1) = 1 XOR [g even] = 1−v
（g ≥ z+2 ≥ (z−1)+2）…すなわち C 値 = [g odd]。
- g odd（v=0）: 選択肢値 ⊆ {1, 2 (iff g=z+2), 1} = {1, 2?} → 0 を含まず mex = 0 = v。✓
- g even（v=1）: 選択肢値 ⊆ {0, 2 (iff g=z+2), 0} → 1 を含まず mex = 1 = v。✓

z = 0 対角（C なし）は同様に閉じる: 領域は g=1（主張 2: m ≥ 2 のとき
{corner=0, F=Z-DIAG(2,0)=[2 even]=1} → mex 2・m=1 のとき {corner=0, B=[g odd]=1} → 
mex 2）と g ≥ 2 = z+2（主張 [g even]: m ≥ 2 は {F=[g odd], Cmp ∈ {2 (g=2), [g odd]}}・
m=1 は {B=[g odd], Cmp 同} → g odd: {1(,2)} mex 0 ✓・g even: {0(,2)} mex 1 ✓）。∎

### 2.3 T-DU′ の証明（床の上半消滅）

Cell: bed (a,a)@(R=2a+k, z)、k ≥ z、主張 0。選択肢:

- fall（a ≥ 2）: pair (a−1, a) gap 1・k 不変。k ≥ z+1 → T-UH: [1 odd] = 1。
  k = z → Z-DIAG(1, z): z ≥ 1 なら 1 ≤ z で [1 odd] = 1、z = 0 なら g = z+1 で 2。
  いずれも ≠ 0。
- B（a=1）: 単一トークン 1@plane z+1、t = R−1 = k+1 ≥ z+1。t ≥ 2 なら
  §2.4 読み S3 で 1。t = 1（z=0, k=0: bed {1,1}@(2,0)）では v(1,1,1) = 2。いずれも ≠ 0。
- C（z ≥ 1）: 床@plane z−1・k−1 ≥ z−1 → 帰納値 0 → 選択肢値 1 XOR 0 = 1 ≠ 0。

選択肢値 ⊆ {1, 2}（いずれも非 0）→ mex = 0。∎

**シャープネス**: k ≥ z の閾値は正確。z=1・k=0: 床 (m,m)@(2m, 1) = 1（K1286 T-B1
b1(0)=1）・z=2・k=1: (m,m)@(2m+1, 2) = 2（K1286 T-B2 b2(1)=2）は 0 でない。
（z ≥ 3 の k = z−1 行は census 0・未証明・§5 O2。）

### 2.4 L-SB と B-exit 境界読み（K0832 閉形式からの直接導出）

**L-SB**: x ≥ 2, p ≥ 1, j ≥ p, R = x+j。K0832 閉形式の分岐:

- p ≥ x+1: v = x%2 は R > q_odd(x) のとき。R − q_odd(x) ≥ x+j−x = j ≥ 1 ✓。
- 1 ≤ p ≤ x−1: 中間分支の条件 R ≤ q_odd(p) は R ≥ x+p > p ≥ q_odd(p) で不成立・
  R < x+p は R = x+j ≥ x+p で不成立 → tail 分支 v = x%2。
- p = x: 分支 z==x の条件（R 奇数かつ R ≤ 2x−1）は R = x+j ≥ 2x > 2x−1 で不成立 →
  v = x%2。

よって ∀ x ≥ 2, p ≥ 1, j ≥ p: v(x,p,x+j) = x%2。（x=1: R ≥ 2 なら min/最終分支で
1。v(1,1,1) = 2 は branch z==x: R=1 奇数 ≤ 2x−1=1 → 2。）∎

**B 値 3 分岐（§2.2 で対角 cell の m=1 子に使用）**: x = g+1, p = z+1, t = g+z+1
（すなわち t = x+p−1）:

- g ≤ z−1（p ≥ x+1）: v = x%2 の条件 R > q_odd(x) は
  t − q_odd(x) = g+z+1 − q_odd(g+1) ≥ g+z+1−(g+1) = z ≥ g+1 ≥ 2 で成立 →
  v = x%2 = (g+1)%2 = [g even]。
- g = z（p = x）: branch z==x: t = 2z+1 奇数かつ t ≤ 2x−1 = 2z+1 → v = 2。
- g ≥ z+1（p ≤ x−1）: 中間分支: q_odd(p) = q_odd(z+1) ≤ z+1 < t = g+z+1（g ≥ z+1
  ≥ 1 より t ≥ 2z+2 > q_odd(z+1)）かつ t < x+p = g+z+2 ✓ → v = (t+p)%2 =
  (g+2z+2)%2 = g%2 = [g odd]。

**そのほかの境界読み**: v(z+1, z+1, 2z+1) = 2（branch z==x: R = 2z+1 奇数かつ
R ≤ 2x−1 = 2z+1 → 2。§2.4 の g = z 読みと同一式）。v(z+2, z+1, 2z+2): x = z+2,
p = z+1 = x−1 で中間分支に入る: R = 2z+2 > q_odd(p) = q_odd(z+1)（2z+2 > z+1 ≥
q_odd(z+1)・z ≥ 0）かつ R < x+p = 2z+3 → v = (R+p)%2 = (2z+2+z+1)%2 = (3z+3)%2 =
(z+1)%2。v(1, p, R) = 1 (R ≥ 2)・v(1, 1, 1) = 2（branch z==x: R = 1 奇数かつ
R ≤ 2x−1 = 1）。∎

### 2.5 基底部（R ≤ 3 の有限検証・手計算・機体 D2/D3 最小 cell と同時に照合）

- bed {1,1}@(2, z=0): 子は B 1 つ: {1}@plane 1 予算 1 → v(1,1,1) = 2 →
  選択肢 {2} → mex 0 ✓（T-DU′ k=0）。
- bed {1,1}@(3, z=0)（k=1）: 子 {1}@plane 1 予算 2 → v(1,1,2) = 1 → mex{1} = 0 ✓。
- 対角 {1,2}@(3, z=0)（k=0）: 子は corner → bed {1,1}@(2,0) = 0 と B →
  {2}@plane 1 予算 2 → v(2,1,2) = 1。選択肢 {0,1} → mex 2 ✓（Z-DIAG g=1, z=0）。
- 対角 {1,2}@(4, z=1)（k=1）: 子は corner → bed {1,1}@(3,1)（k=1 ≥ z=1 → 0）と
  B → {2}@plane 2 予算 3 → v(2,2,3): z==x: R=3 奇数かつ R ≤ 3 → 2、C →
  {1,2}@(3, z=0) = 2 → 値 1 XOR 2 = 3。選択肢 {0, 2, 3} → mex 1 ✓（Z-DIAG
  g=1, z=1 = [1 odd] = 1）。

以上で主張族の全 cell は基底部または子全て R−1 の帰納仮定で利用可能であり、
パケットは収束する。∎（§2.1–§2.3 と併せて定理 T-UH・T-DU′・Z-DIAG の証明完成）

### 2.6 honest 記録（宣言前是正・電池設計）

- **b0 電池の R ≥ 0 ガード**: K1286 T-B0 の定義域は 2m+j ≥ 0。初期の D6 電池はこの
  ガードを欠き m=1, j∈{−3,−2} の 2 個（R < 0・engine 到達不能）を誤照合した。
  predry で検出・宣言前に**電池設計瑕疵と診断**（定理反例ではない・K1303 SS2.7 と同種）・
  ガードを追加した。よって D6 count は 1,941（素朴計画 1,942 − 2 域外 cell）。定理側への
  影響はない（f0(j) は依然全域で照合）。
- **tamper=ty の bed 通過**: 型付き自己検査の tamper（ターゲット主張表のみ反転）で
  z=0 の床 10 cell（a ≥ 2 の k=0 cell 7 個・a=1 の k∈{0,1,2} cell 3 個）は反転後も
  子値が 0 を含まず mex = 0 = h が成り立つため**通過**する。よって ty の期待 bad は
  **1,502**（全 1,512 中）であり、これを事前宣言値とする（fail-closed は成立・他電池
  と同様に rc=1）。この現象は ty が床ターゲット（0 不変）を反転せず、z=0 床の子は
  閉形式または反転ペア主張 {1,2} のみを取るためで、定理とは独立の電池事情。
- **k 座標の対称性について**: Z-DIAG の g ≥ z+2 領域は tail の**補値**（[g even] =
  1−[g odd]）であり、g ≤ z 領域は tail と一致・g = z+1 で値 2。窓（1 ≤ k ≤ z−1）の
  合同行予想（OBS-WC）はこの「対角 = tail or 補値」構造の波及と整合するが、非合同行は
  反例により成立しない（§1 REFUTED）。

## §3 宣言前探索（凍結・出版キット収録: explore_upper.py / explore_upper.out・sha は §4）

- E1 T-UH census: z0..8 × m1..8 × g1..10 × k=z+1..z+5 = 3,600 点 bad 0
  （各面 400 点）。E1b far: z ∈ {10,12,14,16,18,20} × m1..12 × g1..12 × k=z+1..z+3 =
  2,592 点 bad 0。
- E2 T-DU′ census: z0..8 × a1..10 × k=z..z+6 = 630 点 bad 0。E2b far:
  z ∈ {10,14,18} × a1..14 × k=z..z+4 = 210 点 bad 0。
- E3 Z-DIAG census: z0..8 × m1..8 × g1..16 = 1,152 点 bad 0。E3b far:
  z ∈ {10,12,14} × m1..5 × g1..30 = 450 点 bad 0。
- E4 REFUTED: 窓非合同行 540 個中 29 反例（§1 に分布）。
- E4b OBS-WC: 合同行 1,296 点（z3..13）mismatch 0。
- E5 L-SB: x1..20 × p1..14 × j=p..p+8 = 2,520 点（両 engine・閉形式三者一致）bad 0。
  E5b B-exit 読み 103 点 bad 0。
- E6 C-SUM census: 3 重 1,344 点・混合 840 点・4 重 180 点、すべて bad 0。
  E6b 閾値観測: 混合 3 重は k = z+1 から既に [S odd] に見える（6 multiset ×
  (z,k) 10 点の観測表・未証明）。
- E7 cross-engine: 720 点不一致 0。E8 シャープネス表（床 k=z−1: z1→1, z2→2, z3..6→0
  (a≤4)・対角ミスマッチ証人 g=z+1 → 2）。E9 面 0/1/2 の上半完全閉包 census 648 点 bad 0。

## §4 機体宣言（publish-then-execute）

- kit: `research/experiments/pair-upper-20261124/`（本ノート出版の後、verify・engine・
  exploration を出版し、fetch-back に byte 照合した上で公式監査を実行する）。
- **verify_k1308.py**: sha256 `973c97a52a03137fbb7be4af6965593f2bb1c6c384d75ce18f3d34f3fde5c3ac`。
  埋込み engine block の起動時 sha gate: pin `bd5f22e415a78368c9b798296bc84948d5637decbf3c21a92404d45fb12e3a92`
  （K1138/K1282..K1305 公刊 chain と byte 同一）。単体 `engine_block.py` は
  `582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0`（chain 同一 bytes）。
- **電池**（stdout 決定的・volatile は stderr のみ）: D1 T-UH census 5,760 / D2 T-DU′
  census 972 / D3 Z-DIAG census 1,260 / D4 typed self-check（主張表と K0832 閉形式のみで
  子を構成し mex==claim==engine・tail 均一化 set(children)=={1−claim} を点検証・床は
  0∉children）1,512 / D5 L-SB+境界読み（閉形式・両 engine 三方）2,623 / D6 公刊
  アンカー（K1285 T-PS0/1/2・T-ALM 六床・K1286 Z1(1,·)/z2k1/Z2(2,·)・T-B1/T-B2/T-B0・
  b1(0)=1 は T-DU′ シャープネス照合）1,941 / D7 面 0/1/2 上半完全閉包 census
  （z2-k1 含む・k=1..8）1,440 / D8 C-SUM census（予想・obs 明記）2,364 / D9 REFUTED
  revheck（z=3 clean・z ≥ 4 counters の再生産・全 29 反例を obs 凍結）6 / D10
  cross-engine 1,116 / D11 stress（far-m m≤25・高面 z≤24・遠対角 z≤13 g≤24・L-SB far）
  1,594。**総計 20,588 点・期待 overall_bad = 0**。
- **predry 4 走byte-identical確定済み**: stdout sha256
  `d3e244f42f290db0cb0a28d15cd9dec482386e808fcc673db6e4995e16c88d25`
  （同一 cwd ×2 PYTHONHASHSEED=random/1 + 隔離 tree/env -i ×2 PYTHONHASHSEED=99/7・
  /usr/local/bin/python3 3.12・約 2.6 秒/走・predry 出力は kit の output/
  dryrun1-4.out+.info として出版・公式監査は fetch-back bytes から別途 4 走を取る）。
- **変異電池（事前宣言・すべて fail-closed）**: `--tamper-engine` rc=2（変異 sha
  `0ea47a80761d2b20bf414cd52b1535fba56829c3a4c232d1b2f5da3f81441882` ≠ pin）。
  `--tamper=uh` → **bad 5,760** / `du` → **972** / `zd` → **1,260** / `ty` → **1,502**
  （§2.6 更正・全 1,512 中・10 床 cell の正当通過を含む完全事前宣言） / `sb` →
  **2,623** / `ps` → **1,941** / `cs` → **2,364** / `rw` → **6**。全て rc=1。
- **公式監査 discipline**: 本ノート出版 → kit 出版 → fetch-back（全ファイル size +
  sha256 byte 照合・verify と engine_block は全文照合） → fetch-back bytes から公式
  4 走（同一 cwd ×2 PYTHONHASHSEED=random/1 + 隔離 tree/env -i ×2 PYTHONHASHSEED=99/7,
  全走 rc=0・stdout byte-identical・sha は predry と同一 `d3e244f4…` であることを確認）→
  変異電池 9 種 → 監査成果物（audit_run1-4.out+.info・tamper レコード・detcheck.json・
  MANIFEST-sha256）出版 → K item と実行 log 出版 → knowledge README 末尾 bullet append。
  各段階前に main を再取得し競合があれば無理せず記録して次回へ回す。

## §5 open 登録・未来課題（有限観測のみ・全称主張しない）

1. **O1 遷移窓（1 ≤ k ≤ z−1, z ≥ 3）の真の法則**: 偶奇交互予想は反例 29 件で棄却
   （§1）。合同行（k ≡ z mod 2）は Z-DIAG 追従が census で clean（OBS-WC・z13 以遡未
   観測）・非合同行の法則は未知。反例の値は {0,1,2} が混在し 2 の消失/再出現の周期
   構造が見える。typed 子解析の窓版（k−1 が窓に落ちる C 子を含む部分的閉包）が本命。
2. **O2 床窓行 k = z−1**: z ≥ 3 で census 0・未証明。b1(0)=1・b2(1)=2 との対比から
   z ≥ 3 での消滅則の証明候補。
3. **O3 C-SUM 予想の全称化**: 3+ トークン族の tail = [S odd] と安定化閾値の多重度
   依存構造（単一 k≥z、ペア単一コピー k≥z+1、床 k≥z、混合 3 重は k≥z+1 からの
   観測（E6b）、単一コピー 3 重 k≥z+2, 4 重 k≥z+3）。本パッケージの typed-mex 構文
   の多トークン拡張が F1 本命（3 重単一コピーから）。
4. **F1（上記 O3 の第一歩）**: 3 重単一コピー a<b<c の tail 証明: 子型は fall/B/compress×2
   （2 種）+ C で全て 2 トークン既確定族（T-UH/T-DU′/Z-DIAG @ k−Δ）に落ちる見込み。
5. **F2 11×11 巨大探索への接続**: ペア上半三角（k ≥ z・全 plane）が O(1) 評価可能に
   なった（T-UH・Z-DIAG・T-DU′・K1303 帶域の和で到達可能全域の k 軸が全域 O(1)）。
   枝刈り格子の上方拡張として巨大レーンオーナーに記録する（採用判断はオーナー側）。
   verdict 不消費・11×11 UNKNOWN 不変・Part DV/DW レーンと非接触。

## §6 主張の区別（過大主張の防止）

- **定理（全称証明・本ノート §2 に全文）**: T-UH・T-DU′・Z-DIAG・L-SB・B-exit 境界読み。
- **被包（既刊定理との同一式照合・新規性なし）**: K1285 T-PS0/1/2・T-ALM・K1286
  T-Z1(1,·)/T-Z2(2,·)/T-B1/T-B2/T-B0・K1282 T-Q。
- **census 予想（未証明・全称主張しない）**: C-SUM（3 重・混合・4 重 box は凍結
  照合・§5 O3）。
- **反例（honest 棄却）**: 窓偶奇交互予想の非合同行半分（29 反例・z ≥ 4・機体 obs 凍結）。
- **観測登録（未証明）**: OBS-WC（合同行 Z-DIAG 追従・z3..13）・OBS-BW（床 k=z−1 は
  z ≥ 3 で 0 に見える）・E6b 混合 3 重の早期安定化。
- census は証明ではない: 本キットの 20,588 点は定理の実機照合（期待 bad 0）であり、
  定理の全称性はあくまで §2 の手証明によって成立する。
