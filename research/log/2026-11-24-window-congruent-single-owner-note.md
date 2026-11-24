# 単一オーナー宣言 K1309: 遷移窓合同行の全称崩壊 — T-WC（窓合同ペア行 = Z-DIAG(g,z)・k 非依存）・T-WBC（窓合同床行 = 0）+ L-BE/L-C 導出表（K1308 O1 合同半分の解決・OBS-WC 全称化・publish-then-execute）

- 日付: 2026-11-24
- lane: 高速レーン（短〜中時間・厳密結果）。本ノートは fast-lane の単一オーナー宣言
  （publish-then-execute: 本ノートが最初に出版され、機体・公式監査はこれに從属する）。
- 観測 HEAD（着手時・main）: 着手直前 `42cb2abc`（K1308 README bullet 22:54:32Z）。着手後の出版前
  直近再取得も `42cb2abc`・publish 直前に再度 main を取り直し K1309 の空きを再確認する。
  過去 2 時間の items/log 系列は: K1303 公刊 (`4e132464`)・K1304/K1305（PG(2,9) cap games レーン・
  直交）・K1306 宣言（`53d2d335`・SLB/L/E typed-child frontier レーン・単一層トークン多重度族で
  非接触）・K1307(仮) 宣言（`4d2d506a`・REMO 3 枝 cap≤16 r=3 sweep レーン・非接触）・K1308
  公刊（上半畳み込み `eabcb742`..`635488d0`・本ノートの下位定理の出版者であって対抗ではない）・
  Part DV/DW/DH（11×11 adoption レーン・非接触）。
- K 採番: 着手時点の main items 最高番号は K1308（pair-upper レーン・22:35Z 出版 chain）。K1309 は
  items 直接 probe で空洞（`"id: K1309"` code search 0 件・K1309 指摘 commit 0 件）。
- 対抗宣言なし: fetch 時点で本領域（遷移窓 1≤k≤z−1 の合同行 k≡z (mod 2) の値法則）の単一オーナー
  宣言は本ノートのみ。K1308 はOBS-WC を観測登録のみで残しており（§5 O1・「合同行 Z-DIAG 追従
  z3..13 census・未証明」）、本ノートがその全称化（定理化）を最初に宣言する。K1306/K1307 レーン
  とは領域・定理ともに非接触（SLB/L/E トークン多重度族・REMO 計数ゲーム）。
- 規約: verdict 不消費。標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は
  全時点 UNKNOWN のまま。engine はゲーム定義の転写（K1138 chain・sha pin 実装）であり、
  census は照合であって証明の代替ではない。

## 用語・記法（K1285/K1286/K1303/K1308 準拠）

残余ゲーム H(R; X; z)（K1138 再帰・値は mex・H(0;·)=0）。局面の選択肢（K1285 §2.0 規約）:

- **A手**（トークン w>1 を w−1 に圧縮・R→R−1・plane 不変）。ペア (m, m+g) では下トークンの
  圧縮を **fall**（pair (m−1, m+g)・gap g+1・k 不変）、上トークンの圧縮を **compress**
  （pair (m, m+g−1)・gap g−1・k 不変）、g=1 の compress は **corner**（bed (m,m)・k 不変）。
- **B手**（トークン 1 を除去・R→R−1・plane z→z+1）。m=1 のペアの fall 位置に相当する
  B-exit は単一トークン v(g+1, z+1, R−1) になる。
- **C手**（z≥1 で子の値 1 XOR・R→R−1・plane z−1）。子は同 multiset・k→k−1。

**対角座標**（K1305/K1308 準拠）: ペアでは k := R − 2m − g・床では k := R − 2a。
既刊の到達域: k ≤ 0 帯域（K1303 T-GEPSF/T-GEBED・全 plane 全称）・k = z 対角行と
k ≥ z+1 上半 tail（K1308 T-UH/T-DU′/Z-DIAG・全 plane 全称）。**残る未確定は遷移窓
1 ≤ k ≤ z−1 のみ**で、K1308 は非合同行（k ≢ z mod 2）の交互予想を 29 反例で棄却し、
合同行（k ≡ z mod 2）の Z-DIAG(g,z) 追従を OBS-WC（z3..13・1,296 点・未証明）として残した。
本パッケージは**合同半分を全称定理化**する。窓合同行は z ≥ 3 でのみ非空（z=2 の窓 k=1 は
非合同・z≤1 は空）なので、以下の量化はすべて z ≥ 3・k ∈ [1, z−1]・k ≡ z (mod 2)。

記法: IND(b)=1/0・[g odd] := IND(g 奇)・**D(g,z) := Z-DIAG 則** =
[g odd] (g ≤ z) / 2 (g = z+1) / [g even] (g ≥ z+2)。単一トークン閉形式 v(x,p,R)
（K0832・キット engine_block.py 転写）。q_odd(t) := t (t 奇) / t−1 (t 偶)。
K1303 帯域法則の転写: cpsfG(w,R,d) = 2·(R mod 2) (R < L(w)) / T_w(d − s(w))
（L(w)=2⌈w/2⌉・s(w)=2⌊w/2⌋・T_w = g1 (w 奇) / f0 (w 偶)）。ペア帯域では d := R−2m
（k ≤ 0）・床帯域では d := j := R−2a（j ≤ 0）。

## §1 主張

### 定理（全称・量化は非有界・証明は §2 に全文）

- **T-WC（窓合同ペア行の崩壊）**: ∀ z ≥ 3, m ≥ 1, g ≥ 1, k ∈ [1, z−1]（k ≡ z mod 2）:
  **H(2m+g+k; (m, m+g); z) = D(g, z)**。
  値は k にも m にも非依存で、対角行 k=z の Z-DIAG 則の値と一致する（K1308 OBS-WC の全称化）。
  系として K1308 E4b の合同行 census（z3..13・1,296 点）は本定理の実例。
- **T-WBC（窓合同床行の消滅）**: ∀ z ≥ 3, a ≥ 1, k を窓合同として:
  **H(2a+k; (a, a); z) = 0**。
  K1308 T-DU′ は k ≥ z で 0 を示したが、本定理は**窓の合同行すべて**で 0 を示す
  （非合同の OBS-BW 行 k=z−1 は含まず・open のまま）。

### 導出補題（published 閉形式からの直接導出・証明 §2.1/§2.2）

- **L-BE（m=1 B-exit 表・k 非依存性）**: 窓合同ペア (m=1) の B-exit 単一トークン
  v(g+1, z+1, g+k+1) は
  **[g even] (g ≤ z−1) / 2 (g = z) / [z even] (g = z+1) / [g odd] (g ≥ z+2)**
  であり、窓の k に非依存。
- **L-C（窓ペアの C 子表）**: 窓合同ペアの C 子の値（1 XOR の前）は
  **D(g, z−1)**（k ≥ 2 のときは常に・k=1 で 2m+g ≥ z−1 のとき）であり、
  唯一の例外は **k=1 かつ 2m+g ≤ z−2** の小帯域 cell で **2·[g odd]**。
  窓床の C 子の値は（k ≥ 2 では T-WBC 再帰・k=1 では K1303 帯域の両分岐で）**0**。

### 位置恒等式（代数定理・engine-free・multiset+予算等式）

ペア窓合同 cell の全選択肢は次の型に**過不足なく**落ちる（§2.0）:
fall → 窓合同ペア（k,z 不変）・compress → 窓合同ペア（k,z 不変）・corner → 窓合同床
（k,z 不変）・B-exit（m=1）→ 単一トークン v(g+1, z+1, R−1)・C → 窓合同ペア
（k−1, z−1）または帯域 k=0 行（plane z−1）。床窓合同 cell の全選択肢は:
A → 窓合同ペア gap 1（k,z 不変）・B(a=1) → 単一トークン v(1, z+1, k+1)・
C → 窓合同床（k−1, z−1）または帯域 k=0 床（plane z−1）。

### 被包関係

- K1308 **OBS-WC**（合同行 Z-DIAG 追従・z3..13 census）⟸ T-WC（全称昇格）。
- K1308 **O1 の合同半分**は本パッケージで完了。残る窓未確定は**非合同行
  1 ≤ k ≤ z−1, k ≢ z (mod 2)**（ペア・床とも）のみ。
- 到達点: ペア・床とも、**全 k 軸のうち未確定は非合同窓行のみ**になった
  （K1303 帯域 k≤0・K1308 対角/上半 k≥z・本定理の合同窓行の和集合が残り全部）。

### 観測登録（有意義だが主張しない）

- **OBS-NCW**（D10 凍結表）: 非合同窓行の値分布（z3..12・m1..3・g1..12・計 12,960 cell→
  35 行凍結）: 深い非合同行は {0,1} のみで g 奇偶 18/18 分割（[g odd] と整合）だが、
  k ∈ {1,2,3} の浅い行に 2 が発生し、発生位置は k と z の差で構造化される
  （k=1: z≥4 で 5 個以下・k=3: z≥8 で 1 個・k=2: z 奇で 2..3 個）。法則は open・主張しない。

## §2 手証明全文

### 2.0 packet と well-founded 性（帰納の枠組み）

**Packet の定義**: 本証明の帰納 packet は次の主張族の連言である:

- PAIR: T-WC（窓合同ペア cell すべて）
- BED: T-WBC（窓合同床 cell すべて）

**帰納は予算 R 上の同時強帰納**（R = 2m+g+k または 2a+k）: cell 予算 R の値の証明には
**子の値のみ**を使い、子はすべて予算 R−1 を持つ。子の評価は次のいずれかで行う:

1. **packet 内の主張**（子が窓合同 cell・予算 R−1 < R → 帰納仮定）
2. **既刊の全称定理**（子が帯域 k≤0 cell → K1303 T-GEPSF/T-GEBED・子が単一トークン →
   K0832 閉形式・いずれも全予算で公刊済み）

**子の型閉包（位置恒等式の証明）**: 窓合同ペア cell (m, m+g)@(2m+g+k) plane z の選択肢は:

- fall（m ≥ 2）: multiset {m−1, m+g}・予算 R−1 = 2(m−1)+(g+1)+k → 同じ k の窓合同ペア
  （k 不変・z 不変・合同性は k≡z (mod 2) のままで不変）。
- compress（g ≥ 2）: {m, m+g−1} → 同じ k の窓合同ペア（gap g−1）。
- corner（g = 1）: {m, m} → 予算 R−1 = 2m+k → 同じ k の窓合同**床**cell。
- B（m = 1）: 下トークン 1 を除去 → 単一トークン (g+1)@(R−1 = g+k+1) plane z+1
  → K0832 閉形式。
- C（z ≥ 3 ≥ 1）: 同 multiset・plane z−1・k → k−1。k−1 ≥ 1 なら (k−1) ≡ (z−1)
  (mod 2)（合同性は減算で保存）・1 ≤ k−1 ≤ z−2 なので窓合同ペア cell（plane z−1 ≥ 2）。
  k−1 = 0 なら帯域 k=0 のペア cell（plane z−1）→ K1303 T-GEPSF。
  **注意**: 窓 (z,k) から C で到達できる plane 2 の行は k=0（帯域）のみ
  （plane 2 の窓合同行は存在しない: 1 ≤ k ≤ 1 かつ k ≡ 0必要 → 空）。

これで選択肢が過不足なく列挙された（A手は w>1 のトークンすべてに適用されるが、
ペアでは下トークン m>1 なら fall・上トークン m+g>1 は常に成立し compress/corner・
m=1 の下トークンは A の対象外で B の対象・床 (a,a) では 2 つの A 手が同一 multiset
{a−1, a} を与える以外の選択肢は B(a=1)・C）。床 cell の選択肢:

- A（a ≥ 2）: {a−1, a}・予算 2(a−1)+1+k → 同じ k の窓合同ペア gap 1。
- B（a = 1）: 単一トークン (1)@(k+1) plane z+1。
- C: k−1 ≥ 1 なら窓合同床（plane z−1）・k=1 なら帯域 k=0 床（plane z−1）→ T-GEBED。

**基底（予算最小 cell）**: 窓合同床の最小予算は R = 3（a=1, k=1, z ≥ 3）。この値を
packet なしで直接評価する:

- B → v(1, z+1, 2): K0832 で p = z+1 ≥ 4 ≥ x+1 = 2 の分岐・R=2 > q_odd(1)=1 →
  x%2 = **1**。
- C → 床 (1,1)@2 plane z−1: k=0 帯域・j = 0・T-GEBED: cpsfG(z−1, 2, 0):
  z ≥ 4 なら 2 < L(z−1)=2⌈(z−1)/2⌉ までの分岐は 2·(2 mod 2) = 0（L(z−1) ≥ 4 ⟺ z ≥ 4）・
  z = 3 なら L(2)=2 なので主則 f0(0 − s(2)) = f0(−2) = 0。よって C 子 = 1 XOR 0 = **1**。
- 選択肢値集合 = {1} → mex = **0**。T-WBC がこの cell で成立。

窓合同ペアの最小予算は R = 4（(m,g,k) = (1,1,1), z ≥ 3）:

- compress（上トークン 2→1）→ 床 (1,1)@3 plane z = 窓合同床予算 3 → **0**（直前の基底）。
- B（m=1）→ v(2, z+1, 3) = 0（L-BE 表: g=1 ≤ z−1 → [1 even] = 0。導出は §2.1 依存
  だが K0832 直接でも p ≥ x+1 分岐・R=3 > q_odd(2)=1 → x%2 = 0 と機械的に同一）。
- C → ペア (1,2)@3 plane z−1: k = 3−2−1 = 0 帯域・delta = R−2m = 1・T-GEPSF:
  cpsfG(z−1, 3, 1): z = 3 なら L(2)=2・主則 f0(1−s(2)) = f0(−1) = 1 → 子 = 1 XOR 1 = **0**。
  z ≥ 4 なら (z−1 ≥ 3 → L(z−1) ≥ 4) 3 < L(z−1) → 2·(3 mod 2) = 2 → 子 = 1 XOR 2 = **3**。
- 選択肢値集合 = {0}（z=3）または {0, 3}（z ≥ 4）→ いずれも mex = **1**。
  D(1, z) = [1 odd] = 1 なので T-WC が成立。

よって: R=0,1,2 には窓 cell が存在せず、R=3 の床・R=4 のペアを上記の通り直接評価し、
R についての同時強帰納（子はすべて R−1・packet 内か既刊定理で評価）が全窓 cell を尽くす。
∎（枠組み）

### 2.1 L-BE の証明（K1308 と同じ K0832 転写から導出）

m=1 の窓合同ペアの B-exit: 単一トークン x = g+1 ≥ 2・plane p = z+1 ≥ 4・予算 R′ = g+k+1
= x+k（k ≡ z (mod 2)・1 ≤ k ≤ z−1）。K0832 閉形式の分岐に照らす:

(i) **g ≤ z−1**（p ≥ x+1 = g+2 ⟺ z ≥ g+1）: 分岐 z ≥ x+1。m_opts = q_odd(x) ≤ x。
R′ = x+k ≥ x+1 > x ≥ m_opts → 主則 x%2 = (g+1)%2 = **[g even]**。
(ii) **g = z**（p = x）: 分岐 z = x。R′ = x+k ≤ x+(x−2) = 2x−2 < 2x−1 かつ
k ≡ z = x−1 (mod 2) より R′ = x+k ≡ x+(x−1) = 2x−1 ≡ 奇 → 「R 奇 かつ R ≤ 2x−1」
条件が常に成立し **2**。（R 偶条件 R′ ≤ x−1 は不成立。）
(iii) **g = z+1**（p = x−1）: 分岐 1 ≤ p ≤ x−1。m_opts = q_odd(p) = q_odd(z+1) ≤ z+1。
R′ = x+k = z+2+k ≥ z+3 > m_opts → 主則 (R′+p)%2 = (z+2+k+z+1)%2 = (k+3)%2
= k+1 (mod 2)。k ≡ z より **[z even]**。（R′ < x+p = 2z+3 は k ≤ z−1 から常に成立。）
(iv) **g ≥ z+2**（p ≤ x−1）: R′ = x+k ≤ x+z−1 < x+p = x+z+1 ✓・
R′ = g+1+k ≥ g+2 > q_odd(z+1)（q_odd(z+1) ≤ z+1 < g+2）→ 主則
(R′+p)%2 = (g+1+k+z+1)%2 = (g+k+z)%2 = g%2（k ≡ z）= **[g odd]**。

いずれも窓内で k に非依存。∎

### 2.2 L-C の証明（K1303 帯域法則の転写から導出）

窓合同ペアの C 子: 同 multiset・plane z−1・予算 R−1 = 2m+g+k−1・子の k = k−1。

(i) **k ≥ 2**: k−1 ≥ 1 かつ k−1 ≡ z−1 (mod 2)・1 ≤ k−1 ≤ z−2 → 子は plane z−1 の窓合同
ペア（PAIR 主張・予算 R−1）。C 子の値 = 1 XOR **D(g, z−1)**。
(ii) **k = 1**（このとき z は奇・子の k = 0 → 帯域）: T-GEPSF で
delta = R−1−2m = g・予算 R′ = 2m+g:
  - 2m+g < L(z−1) = z−1（⟺ 2m+g ≤ z−2・z 奇より L(z−1) = z−1）: 帯域小分岐
    2·(R′ mod 2) = 2·(g mod 2) = **2·[g odd]**。R′ の奇偶は 2m 非依存（これが
    例外 cell でも m 依存しない理由）。
  - 2m+g ≥ z−1: 主則 T_{z−1}(g − s(z−1)) = f0(g − (z−1))（z−1 偶）。t := g−z+1:
    t ≤ 0 ⟺ g ≤ z−1: f0(t) = [t odd] = [g odd]（z 奇より t ≡ g mod 2）・
    t = 1 ⟺ g = z: f0(1) = 2・t > 1 ⟺ g ≥ z+1: f0(t) = [t even] = [g even]。
    これは **D(g, z−1)** の定義と逐点一致する（g ≤ z−1 → [g odd]・g = z → 2
    （this is g = (z−1)+1）・g ≥ z+1 = (z−1)+2 → [g even]）。
  - したがって k=1 でも 2m+g ≥ z−1 の限り C 子の値 = 1 XOR D(g, z−1)。

窓合同床の C 子: k−1 ≥ 1 なら T-WBC（BED 主張・値 0）。k=1 なら T-GEBED で
j = R−1−2a = 0・予算 2a: 2a < L(z−1) = z−1 分岐は 2·(2a mod 2) = 0・主分岐は
f0(0 − (z−1)) = f0(1−z) = [1−z odd] = 0（z 奇）→ **0**。∎

### 2.3 T-WBC の証明（床の窓合同行）

帰納（§2.0）により子の値を評価する。床 cell (a,a)@(2a+k) plane z・窓合同 k:

- A（a ≥ 2）: fall → 同じ k の窓合同ペア (a−1, a)、gap 1。§2.2 と同形式で T-WC から
  **D(1, z) = [1 odd] = 1**（窓は z ≥ 3 なので g=1 ≤ z は常に成立）。
- B（a = 1）: v(1, z+1, k+1): K0832 の p ≥ x+1 分岐（k+1 ≥ 2 > q_odd(1) = 1）→ **1**。
- C: 1 XOR L-C（床）= 1 XOR 0 = **1**。

選択肢値集合 = {1}（a ≥ 2 では A/C とも 1・a=1 では B/C とも 1）→ mex = **0**。
T-WBC 成立。∎

### 2.4 T-WC の証明（ペアの窓合同行・区域表）

帰納（§2.0）により子の値を評価する。区域: **A**: g ≤ z−2・**A2**: g = z−1・**B**: g = z・
**C**: g = z+1・**D1**: g = z+2・**D2**: g ≥ z+3。隣接値と L-BE/L-C 表:

- D(g±1, z): A/A2 では [g±1 odd] = 1−[g odd]（g±1 ≤ z に留意・A の境界 g+1 = z−1 ✓）。
  B: D(g+1, z) = D(z+1, z) = **2**・D(g−1, z) = D(z−1, z) = [z−1 odd] = 1−[z odd]。
  C: D(g+1, z) = D(z+2, z) = [z+2 even] = **[z even]**・D(g−1, z) = D(z, z) = **[z odd]**。
  D1: D(g−1, z) = D(z+1, z) = **2**・D(g+1, z) = D(z+3, z) = [z+3 even] = 1−[z+2 even] = 1−D。
  D2: D(g±1, z) = [g±1 even] = 1−[g even]（g±1 ≥ z+2 ✓）。
- c := D(g, z−1)（L-C 通常値）: g ≤ z−1 → [g odd] = D(g,z)・g = z → **2**・
  g = z+1 → **[z odd]**・g ≥ z+2 → [g even] = D(g,z)。
  **例外値**（k=1 かつ 2m+g ≤ z−2）: **2·[g odd]**。
- b := L-BE（m=1 のみ）: [g even] (g ≤ z−1) / 2 (g = z) / [z even] (g = z+1) /
  [g odd] (g ≥ z+2)。

**例外 cell の所在**: 例外条件 2m+g ≤ z−2 は区域 B/C/D1/D2 では不成立
（B: 2m+g ≥ 2+z > z−2・それ以外はさらに大きい）。また 2m+g ≤ z−2 の两端は
g ≤ z−2−2m ≤ z−4 なので**例外は区域 A 内（g ≤ z−4）に限る**（区域 A2 g = z−1 も
2m+g ≥ z−1 > z−2 で不成立）。区域 A では D = [g odd] である。

各区域・m クラスの子値集合 S と mex を列挙する（fall は m ≥ 2 のみ・b は m=1 のみ）:

**区域 A（g ≤ z−2, D = [g odd]）**:
- 通常（m ≥ 2）: S = {fall D(g+1,z) = 1−D, compress D(g−1,z) = 1−D, 1 XOR c = 1−D}
  = **{1−D}** → mex: D=0 → {1}→mex 0 = D ✓ / D=1 → {0}→mex 1 = D ✓。
  （g=1 の corner では compress 値 0 = 1−D（D=1）で同じ: S = {0, 0, 0}={0}→mex 1 ✓。）
- 通常（m = 1）: S = {compress/corner 1−D, b = [g even] = 1−D, 1 XOR c = 1−D} =
  **{1−D}** → mex = D ✓（g=1: corner 0・b = 0・c = D(1,z−1) = 1 → 子 0: S = {0} →
  mex 1 = D ✓）。
- 例外（S_C = 3 if g odd else 1）: m ≥ 2: g 奇: S = {1−D=0, 0, 3} = {0,3} → mex 1 =
  D ✓ / g 偶: S = {1,1,1} = {1} → mex 0 = D ✓。m = 1: g 奇: S = {0, 0, 3} =
  {0,3} → mex 1 = D ✓ / g 偶: S = {1,1,1} = {1} → mex 0 = D ✓。

**区域 A2（g = z−1, D = [z−1 odd]）**: 通常のみ（例外不成立）。隣接 D(g±1, z) =
1−D・c = D・b = [g even] = 1−D。
- m ≥ 2: S = {1−D, 1−D, 1−D} = {1−D} → mex = D ✓。
- m = 1: S = {1−D, 1−D, 1−D} = {1−D} → mex = D ✓。

**区域 B（g = z, D = [z odd]）**: fall D(g+1,z) = 2・compress D(g−1,z) = 1−D・
c = 2 → C 子 = 1 XOR 2 = 3・b = 2。
- m ≥ 2: S = {2, 1−D, 3}: z 奇: D=1 → {0,2,3} → mex 1 = D ✓ / z 偶: D=0 →
  {1,2,3} → mex 0 = D ✓。
- m = 1: S = {1−D, 2, 3}: z 奇: {0,2,3} → mex 1 ✓ / z 偶: {1,2,3} → mex 0 ✓。

**区域 C（g = z+1, D = 2）**: compress D(g−1,z) = D(z,z) = [z odd]・
fall D(g+1,z) = D(z+2,z) = [z+2 even] = [z even]・c = [z odd] → C 子 = [z even]・
b = [z even]。
- m ≥ 2: S = {[z even], [z odd], [z even]} = {0,1}（両奇偶を含む）→ mex **2** = D ✓。
- m = 1: S = {[z odd], [z even]} = {0,1} → mex 2 = D ✓。

**区域 D1（g = z+2, D = [z+2 even] = [z even]）**: compress D(g−1,z) = D(z+1,z) =
**2**・fall D(g+1,z) = D(z+3,z) = [z+3 even] = 1−D（z 偶 → z+3 奇 → 0 = 1−D ✓ /
z 奇 → z+3 偶 → 1 = 1−D ✓）・c = D（g ≥ z+2 → c = D）→ C 子 = 1−D・
b = [g odd] = 1−D。
- m ≥ 2: S = {fall 1−D, 2, 1−D} = {1−D, 2}: z 偶: D=1 → {0,2} → mex **1** = D ✓ /
  z 奇: D=0 → {1,2} → mex **0** = D ✓。
- m = 1: S = {2, 1−D, 1−D} = {1−D, 2}: z 偶: {0,2} → mex 1 = D ✓ /
  z 奇: {1,2} → mex 0 = D ✓。

**区域 D2（g ≥ z+3, D = [g even]）**: fall/compress D(g±1,z) = [g±1 even] = 1−D
（g±1 ≥ z+2 ✓）・c = D → C 子 = 1−D・b = [g odd] = 1−D。
- m ≥ 2: S = {1−D, 1−D, 1−D} = {1−D} → mex = D ✓。
- m = 1: S = {1−D, 1−D, 1−D} = {1−D} → mex = D ✓。

全区域・全 m クラス・例外/通常で mex = D(g, z) が confirmed。各ケースは列挙した
子値集合（高々 3 要素）に mex を適用した有限計算であって、量化は包含の確認を
残すのみ: 各区域・クラスの主張は g・z の全整数値で同型の有限表計算として成立
（table 中の値は奇偶 IND のみで、z・g の具体値に非依存）。∎

（機体 D5 が本 §2.4 の表を typed children として z3..16・m1..6・g1..24 の 8,736 点で
点ごとに再現し、engine 値と三方一致することを機械検証する。census は証明の代替ではない。）

## §3 宣言前探索（凍結・explore_wc.out sha256 `7e57e2e4…`（全文 `7e57e2e4181bc17eda1244dfe1bd203aadc8b099d51965b099f9de2f6ded43d7`）・engine_block 582c93c1 chain bytes）

- X1 T-WC census: z3..16・m1..8・g1..24・全窓合同 k: **10,752 点 bad 0**。
- X1b far: z{18,20,22}・m1..4・g1..32: **3,456 bad 0**。X1c m 距離: z{5,8,11,14}・
  m1..20・g1..12: **3,840 bad 0**（値の m 非依存を m=20 まで確認）。
- X2/X2b T-WBC census: z3..16 a1..12（672）+ far z{18,20,22} a1..8（216）: **888 bad 0**。
- X3 L-BE 表 vs 転写閉形式: 窓 box 1,344 点 **bad 0**。
- X4 typed packet 自己検査（子を手表のみで構成・cpsfG 経由）: 8,736 点
  **typed mex vs 申立 bad 0・typed mex vs engine bad 0**（packet の閉性を点ごと確認）。
- X5 cross-engine: 341 点 bad 0。X6 K1308 E4b box 再現: 1,296 点 mismatch 0。
- X8 非合同行 obs: 35 行の分布を凍結（機体 D10 と同一表・主張なし）。
- 実行時間: 全段階約 1 秒（python3 3.12）。

## §4 機体宣言（publish-then-execute・本ノート出版後に从属実行）

- 機体: `verify_k1309.py` sha256
  `cd1328e37acb445d67e8525877582814ee39ef61508689c9e7542657a5bd3414`。
  埋込み engine block の起動 sha gate: pin
  `bd5f22e415a78368c9b798296bc84948d5637decbf3c21a92404d45fb12e3a92`
  （K1138/K1282..K1308 chain と同一 embedded bytes・単体 engine_block.py
  `582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0` は
  K1282..K1308 kit と同一 bytes）。
- 電池（期待値）: counts `[10752, 3456, 3840, 888, 8736, 1344, 3740, 2600, 341, 35, 4680]`
  総計 **40,412**・期待 **overall_bad = 0**:
  D1 T-WC census（X1 box）・D2 T-WC far（X1b box）・D3 T-WC m 距離（X1c box）・
  D4 T-WBC census（X2/X2b box）・D5 typed 自己検査（手表 T-WC/T-WBC/L-BE/L-C のみで
  子構成・mex == 申立 == engine の三点一致・X4 box）・D6 L-BE vs 転写閉形式 vs 両
  engine（窓 box）・D7 帯域・L-C engine ゲート（k=0 ペア帯域 w2..15 m1..6 g1..20・
  k=0 床帯域 w2..15 a1..10・k=1 C 子 L-C 手表 z 奇 3..21 m1..8 g1..24）・
  D8 公刊アンカー（K1308 Z-DIAG k=z z3..10 m1..6 g1..18・T-DU′ z0..6 a1..8 k z..z+3・
  T-UH z0..6 m1..6 g1..12 k z+1..z+3）・D9 cross-engine（X5 box）・
  D10 非合同行 obs 凍結表（35 行・値分布の完全一致主張は**観測の再現性**であって
  法則主張ではない）・D11 k=1 行 stress（z 奇 3..27・m1..12・g1..30・例外 cell
  650 個を含む）。
- 決定性: stdout は byte-identical（predry 4 走で同一 sha
  `3b5aa0b153569026d1e3312d5e1a1a6ffb46a6046417e388fdd5f0c0049cc8dd`・
  約 1.3 秒/走）。
- 変異電池（12 種・事前宣言・全て fail-closed を期待）:
  `--tamper-engine` → rc=2（変異 sha `0ea47a80761d2b20bf414cd52b1535fba56829c3a4c232d1b2f5da3f81441882` ≠ pin・
  stdout は mismatch 報告のみ）:
  - `--tamper=wc1` → rc=1・bad D1=10,752 + D5=672（D5 の typed 表も FLIP されるため
    672 点が正当不一致を起こす・honest 値）
  - `--tamper=wc2` → rc=1・bad D2=3,456 + D5=672
  - `--tamper=wc3` → rc=1・bad D3=3,840 + D5=672
  - `--tamper=bw` → rc=1・bad D4=888
  - `--tamper=ty` → rc=1・bad D5=8,736（typed 構成と申立の両 FLIP で全点不一致）
  - `--tamper=be` → rc=1・bad D6=1,344・`--tamper=cp` → rc=1・bad D7=3,740
  - `--tamper=ps` → rc=1・bad D8=2,600・`--tamper=xg` → rc=1・bad D9=341
  - `--tamper=rw` → rc=1・bad D10=1（凍結表 1 行改変）・`--tamper=ex` → rc=1・bad D11=4,680
- 公式監査: fetch-back bytes から公式 4 走（同一 cwd ×2 PYTHONHASHSEED=random/1 +
  隔離 tree/env -i ×2 PYTHONHASHSEED=99/7）→ 全走 rc=0・stdout byte-identical
  （predry sha と一致確認）→ 変異電池 12 種 → 成果物（audit_run1-4.out/.info・
  tamper レコード・detcheck.json OFFICIAL-PASS・MANIFEST-sha256）出版。

## §4.5 主張の区別（過大主張の防止）

- **定理（全称・手証明 §2）**: T-WC・T-WBC。
- **導出補題（published からの直接導出・証明 §2.1/§2.2）**: L-BE・L-C。
- **代数定理（engine-free 位置恒等式・§2.0）**: 子の型閉包。
- **観測（主張なし）**: OBS-NCW の D10 凍結表・非合同行の構造は open。
- census は証明ではない: 40,412 点は定理・手表の実機照合であり、全称性は手証明による。

## §5 open 登録（次候補）

- **O1′（非合同窓行）**: 残る窓未確定は非合同行のみ（ペア・床とも）。D10 凍結表が
  入力データ。深い非合同行は {0,1} のみ（g 奇偶分割と整合）だが、k ∈ {1,2,3} の
  浅い行に 2 が構造化して発生。typed 解析（C 子は非合同行に落ちるため本ノートの
  packet では閉じない・非合同ペア行の値問題が blocker）として登録。
- **O2（床非合同行・OBS-BW 含む）**: 床 k=z−1 行（K1308 OBS-BW census 0・未証明）は
  C 子が再び床非合同行に落ち A 子が非合同ペア行に落ちるため、O1′ と同じ blocker。
- **F2（11×11 接続）**: 窓合同行が全 plane で O(1) 評価可能になった。これで枝刈り
  格子の O(1) 行は「k ≤ 0 帯域・k ≥ z 上半・k = z 対角・窓合同行」であり、残る非
  即値域は非合同窓行のみ。巨大探索レーンオーナーへの記録のみ（採用判断はオーナー側）。
- **F1（K1308 次課題・C-SUM）**: 変更なし（3 トークン typed 解析は未着手のまま）。

## §6 honest 記録（宣言前の構築経緯）

- 機体初回ローカル起動で 2 件の構築誤りを検出・宣言前に是正した:
  (a) 埋込み engine block 末尾に `from functools import lru_cache` を誤って block 内に
  追加し、startup sha gate が pin 不一致（sha `1fd030f1…`）で即時 abort
  （gate が設計どおりに機能）→ K1308 published embedded block bytes をそのまま
  転写して修正。(b) module 直下の functools import 欠落による NameError →
  import 追加。いずれも宣言前であって、sha `cd1328e3…` は修正後ファイル。
  （K1302 §2.7「宣言前 stale 引数検査」規律の適用。）
- §2.4 区域 D1 の初回テーブル記述で [z+3 even] の IND 向きを一時誤記し、通常
  z 偶ケースの S を {0,1,2}（mex 3）と誤算したが、機対 D5 typed 検査（8,736 点
  bad 0）と矛盾するため宣言前に表を再計算して是正した（正: fall = 0 = 1−D・
  S = {0,2} → mex 1 = D）。修正後の §2.4 が正本である。
- 例外 cell の分析で「例外は区域 A 内のみ」を確認した際、L-C の主則値が
  D(g, z−1) と逐点一致すること（z 奇の k=1 行に限る）を手計算で検証した。
