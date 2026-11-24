# 遷移窓非合同行パッケージ — 単一オーナー宣言ノート（K1310）

publish-then-execute: 本ノートが正本。§1 主張、§2 手証明全文、§3 宣言前探索凍結、
§4 機体宣言、§4.5 主張の区別、§5 open 登録、§6 honest 構築経緯。
機体（verify_k1310.py）は §4 の実体であり、出版後に fetch-back bytes から公式監査を
実行して成果物を output/ に追記出版する。着手時 HEAD `ffde117b`（Part DX batch-36
レーン・直交。K1310 採番空き・対抗宣言なしを push 直前に再確認済み）。

座標は K1309 と同一: ペア k := R−2m−g、床 k := R−2a、窓 1≤k≤z−1。
**非合同**とは k ≢ z (mod 2) のこと。z≥2（z=2 の k=1 は自動的に非合同で、
窓帰納の induction base を兼ねる）。g* := z−2k、s := 2m+g、r := (z−1)//2、
IND(·) は 0/1 指示関数。[g odd] := IND(g odd)、[g even] := IND(g even)。

---

## §1 主張

**T-NCW-P（全称）**: ∀ z≥2, m≥1, g≥1, k∈[1, z−1]（k ≢ z mod 2）について
g* := z−2k とおくと

  H(2m+g+k; (m, m+g); z) =
    [g odd]  （g*≤0 または g>g* または s<z のとき）
    2        （それ以外、すなわち 1≤g≤g* かつ s≥z で、g=g* または g=z−2m のとき）
    [g even] （その他: 残る flip wedge {1≤g<g*, s>z}）

である。評価順はこの並び順である（N 枝が先に効く: g=z−2m でも m<k なら g>g* なので
第1枝 [g odd] に落ちる）。s≥z かつ g≤g* の楔（anomaly wedge）では
2m ≥ z−g ≥ z−g* = 2k より **m≥k は自動条件**。値 2 は楔の内部で
恰好 dominant 列 g=g*（s≡z (mod 2) を含む列）と対角線 s=z（g=z−2m, m≥k）の
2 本の直線上にのみ現れる。楔の外（s<z、g>g*）では行は決して 2 を取らない。

**T-NCW-B（全称）**: ∀ z≥2, a≥1, k∈[1, z−1]（非合同）について

  H(2a+k; (a, a); z) =
    0                        （g*<0 のとき: 2k>z。k=z−1 頂行を含む全行）
    0                        （g*≥0 かつ a≤r のとき）
    1                        （z 奇数・g*≥1 かつ a≥r+1）
    2                        （z 偶数・g*=0（ゆえ z≡2 mod 4）かつ a≥r+1）
    2 (a=r+1) / 1 (a≥r+2)   （z 偶数・g*>0 かつ a≥r+1）

注意: z 偶数で g*=0 となる k=z/2 が非合同であるには k 奇数が必要なので
この枝は z≡2 (mod 4) に限る。g*=0・z≡0 (mod 4) の k=z/2 は合同行（K1309 T-WBC)=0。

**C1（z=2 基底行）**: z=2 の窓は k=1 のみで非合同。T-NCW-P: g*=0≤0 →
ペア行は全 cell [g odd]。T-NCW-B: g*=0・z 偶 → B(a)=2（∀a≥1: r=0 で a≤r は空）。
既刊 K1286 の z2-k1 ペア行・b2(1)=2 と一致（窓 packet 帰納の base）。

**C2（k=z−1 頂行。OBS-BW の解決）**: k=z−1 は常に非合同で、g*=2−z。
z≥3 では g*<0: ペア行は全 cell [g odd]、床行は全 a で 0。z=2 は C1。
K1308 OBS-BW（床窓行 k=z−1 の z≥3 census 0・未証明観測）は定理へ昇格。

**C3（OBS-NCW 包摂）**: K1309 D10 の非合同 35 行凍結価値分布表
（z3..12, m1..3, g1..12, engine census の行ごとの {0,1,2} 出現数）は
T-NCW-P の該当 slice と cellwise に完全一致する（機体 D10 が engine 再 census・
凍結表照合・申立照合の三点を検査）。観測登録は全称定理の実例へ昇格し、
「浅い行 k∈{1,2,3} の structured 2」の正体は dominant 列・対角線の 2 である。

**C4（2 の局在と T-WC との本質的相違）**: 非合同行では窓内に 2 を生むのは
楔の 2 直線のみで、**Z-DIAG 上半則にある g=z+1 の 2 は非合同行には存在しない**
（g=z+1>g* であることから自動）。K1309 T-WC（合同行 = D(g,z)、g=z+1 で 2）と
非合同行の法則は数式的に別物であり、窓の偶奇交互予想（K1308 が 29 反例で
REFUTED）の正しい整理は「合同行は対角行の値をコピーするが、非合同行は
dominant 列 g*=z−2k が own する flip wedge 則に従う」である。
実験 X3 が 2 の完全局在（wedge 外 offband 2 = 0・2 直線 capture 100%）を凍結。

**C5（全 k 軸確定）**: ペア・床の 2 山面の k 軸は
k≤0（K1303 T-GEPSF/T-GEBED・全 w）+ 窓合同行（K1309 T-WC/T-WBC）+
窓非合同行（本項）+ k=z 対角行（K1308 Z-DIAG）+ k≥z 上半（K1308 T-UH/T-DU′）
の和集合で**全 z≥2・全 k∈Z が閉形式で確定**し、未確定帯が消滅した。
O(1) 即値化可能な行の格子は全窓に拡大完了（F2 接続は §5）。

**L2（B-exit 一様法則・K0832 から導出）**: 窓非合同ペア cell の m=1 B-exit
単一トークン v(g+1, z+1, g+k+1) = **(g+1) mod 2 = [g even]**。g・k にわたって
一様（g=z の z==x 枝の tail も (z+1)%2 で同値、§2.2）。床の a=1 B-exit
v(1, z+1, k+1) = **1**（非合同なら無条件・§2.2 終節）。

**O1′/O2（K1309 open 登録）の解決**: K1309 が「typed packet が自己参照的に
閉じない blocker」として残した非合同窓行のペア・床の真の法則が本パッケージで
全称決定。blocker の解除機構は §2.0（C 子の非合同性**保存**が packet の閉性の
核: 合同 packet では C 子が合同行に落ちて相互再帰したのに対し、非合同 packet では
C 子 (k−1, z−1) が再び非合同で**自分自身の packet に入り、R 降下で well-founded**。

---

## §2 手証明

### 2.0 typed 子と packet の閉性

窓非合同ペア cell (m,g,k,z)（R=s+k=2m+g+k, 1≤k≤z−1, k≢z）の全 option:

- **A-fall**（小山の 1 石除去・m≥2）: (m−1, g+1)、(k,z) 不変、R−1。
- **A-compress**（大山の 1 石除去・g≥2）: (m, g−1)、(k,z) 不変、R−1。
- **corner**（g=1 での compress）: 床 (a=m, k̃=k, z)、R−1=2m+k。
- **B-exit**（m=1 の小山消失）: 単一トークン v(g+1, z+1, g+k+1)（R−1・平面 z+1・
  K0832 公刊閉形式で即値・帰納外 inst base。値は L2）。
- **C**（k≥2）: 1^H(s+(k−1); (m,m+g); z−1) = 1^〔基平面 (k−1, z−1) の非合同窓
  cell (m,g) の値〕。k−1 ≢ z−1 (mod 2)（両者同時反転）で**非合同性が保存**され、
  k−1∈[0, z−2]=[0, (z−1)−1] で子は子平面の帯域 k̃=0 は  K1303、k̃≥1 は非合同窓
  （同じ packet 内・R−1）。**k=1 の C 子だけは帯域 k=0 行**（平面 z−1・荷 s・
  K1303 で即値・帰納外 inst base; 本証明で使うのは R̃=s, δ=g の
  cpsfG(z−1, s, g) = 2[s odd] (s<L(z−1)) / T_{z−1}(g − 2⌊(z−1)/2⌋) (s≥L(z−1))）。

床 cell (a,k,z)（R=2a+k）の全 option: **A**（a≥2: ペア (a−1, g=1, k, z)・R−1）/
**B**（a=1: 単一トークン v(1, z+1, k+1)=1）/**C**（k≥2: 1^〔床 (a, k−1, z−1)〕・
非合同保存・R−1/k=1: 帯域床 K1303: 1^cpsfG(z−1, 2a, 0)）。

ゆえに packet P = {T-NCW-P, T-NCW-B} の全 typed 子は「packet 内 cell (R−1,
(k,z) 不変)・packet 内 cell (R−1, (k−1, z−1))・単一トークン（K0832・公刊全称）・
帯域（K1303・公刊全称）」のいずれかに過不足なく落ちる。全子で予算はちょうど
R−1 だから、**単一 R 強帰納**（R=3 の床最小 cell まで降りきる: 基底 cell の子は
トークンと帯域のみ）で well-founded。C1 の z=2 行は packet 内で R 降下により
自力で閉じる。非合同性保存により帰納は packet 内で閉じ、合同行の値は
一切参照しない（K1309 が非合同行の値を参照しなかったのと逆方向の非依存で、
合同 packet と非合同 packet は互いに独立に閉じる）。

### 2.1 パリティ不変量

s=2m+g ≡ g (mod 2)、g* = z−2k ≡ z (mod 2)、よって:

- (P1) 対角線 s=z 上の cell は g ≡ z (mod 2) の列に限る（s≡g による）。
- (P2) dominant 列 g=g* 上は s ≡ z (mod 2) なので s=z+1 は存在しない
  （D cell の west 子が子対角線に落ちるケースを排除する）。
- (P3) flip wedge F={g<g*, s>z} は m>k≥1、すなわち **m≥2（B-exit なし）**を強制し、
  s>z は実は s≥z+1 で、s≡g (mod 2) により s=z+2, z+4, …（g≡z 列）または
  s=z+1, z+3, …（g≢z 列、s=z 不可）に分かれる。この偶奇分岐が west/north 子が
  子対角線（値 2）に落ちるか子 F（値 [g' even]）に落ちるかを決める。
- (P4) z 奇 → NCW k は偶（k=1 不可→ 床・ペアとも k=1 の帯域 C 子は z 偶に限る）。
  z 偶 → NCW k は奇。
- (P5) 床 bed 関では親平面 z の r=(z−1)//2 と子平面 z−1 の r′=(z−2)//2 の差が
  z の偶奇で 1/2 だけずれ、z 奇のとき親 a=r が子平面では a=r′+1（child 値 2 →
  子 outcome 3 で無害）になる。これが床の閾値分割 [a≤r | a≥r+1] と子平面の
  分割 [a≤r′ | a=r′+1 | a≥r′+2] を噛み合わせる接着剤。

### 2.2 L2（B-exit 一様則）の導出

σ := v(g+1, z+1, g+k+1) とおく（x=g+1, 平面 w=z+1, R′=g+k+1）。k+z は奇（非合同）。

- 枝 w≥x+1（g≤z−1）: m₀=q_odd(x)≤x<R′（k≥1）、m₀<R′<x+w=g+z+2（k≤z−1）。
  中間枝 σ=(R′+w)%2=(g+k+z)%2=（k+z 奇より）(g+1)%2。
- 枝 w=x（g=z）: R′=z+k+1 は偶（k+z 奇）。R′ 奇 ⇒ 2 は不発火、R′≤x−1=z ⇔
  k≤0 も不発火、tail σ=x%2=(z+1)%2=(g+1)%2。
- 枝 w≤x−1（g≥z+1）: mirror 枝 m₀=q_odd(w)≤w<R′（R′−w≥g+k−z≥2）、
  m₀<R′<x+w（k<z+1）→ σ=(R′+w)%2=(g+1)%2。

三枝とも σ=(g+1)%2 = [g even]。よって **m=1 非合同ペア cell の B-exit は
常に値 [g even] を注入する**。床側: a=1 の B-exit σ₁ := v(1, z+1, k+1):
x=1, w≥2: m₀=1<R′=k+1<k+2=x+w → σ₁=(k+1+z+1)%2=(k+z)%2=1。

追試（出版前・宣言後の性質確認ではなく本ノートの構築過程）: σ を
z2..60・NCW 全 k・g≤120 で閉形式に対し 108,000 点照合、bad 0（§6 参照）。

### 2.3 C-descent 子区域写像

C 子の値 v′ = 子平面 (k−1, z−1) における (m,g) の申立値。子 dominant g**=g*+1、
子窓条件 s vs z′=z−1。親区域ごと:

- N（s<z → s≤z−1=z′）: s<z′ → 子 N（v′=[g odd]）; s=z′ → 子は子対角線上
  （g=z′−2m が自動成立）で、m≥k−1 ならば g≤g** で子値 2、m<k−1 ならば
  g>g** で子 N2（v′=[g odd]）。
- N2（g>g*, s≥z>z′）: g>g*+1 → 子 N2（v′=[g odd]）; g=g*+1 → 子 dominant
  列（子値 2: 子 D 条件 s≥z′ と m≥k−1 は s≥z かつ m≥k から自動）。
- D（g=g*, s≥z）: g=g*<g** ・s>z′ → 子 F（v′=[g* even]）。
- G（s=z>z′, g≤g*<g**）→ 子 F（v′=[g even]）。
- F（g<g*, s>z>z′）→ 子 F（v′=[g even]）。
- 床 Br1–Br4: §2.5 の各分岐で子 bed 値を直接評価。

k=1 の帯域 C 子（z 偶に限る・P4）は cpsfG(z−1, s, g) として別途評価し、
各区域で outcome ∈ {領域の統一値, 3}（詳細は §2.4 の表の C 欄・§2.5）。

### 2.4 T-NCW-P: 区域 mex 代数

統一値 q := [g even] = 1−[g odd] を置くと、申立は次の 3 形に整理される:
N/N2: 申立 c=[g odd]=1−q（全 option outcome ∈ {q} ∪ {2,3}）。
F: 申立 c′=[g even]=q（全 option outcome ∈ {1−q} ∪ {2,3}）。
G/D: 申立 2（option outcomes が 0,1 をともに含み 2 を含まない）。

各区域の option 値（west=compress, north=fall, corner=g=1 の床、σ=m=1 B-exit、
C=C move outcome）:

- **N（s<z）**: west: s−1<z で子 N → [g−1 odd]=[g even]=q（g≥2; g=1 は corner:
  床 B(k,z,m)=0、q=[1 even]=0 と一致 — §2.5 の Br 全分岐で a≤r が自動）。north:
  s−1<z で子 N → [g+1 odd]=q。σ=q（L2）。C: s<z′ → v′=[g odd] → outcome q;
  s=z′ → m≥k−1: outcome 3、m<k−1: v′=[g odd] → outcome q;
  k=1（z 偶）帯域: outcome ∈ {q, 3}（s≡g と g1 の偶奇計算）。ゆえに
  outcomes ⊆ {q,2,3} かつ q ∈ outcomes → mex=1−q=[g odd]=申立 ✓。
- **N2（g>g*, s≥z）**: west: g−1>g* → q; g−1=g* → 子 D、ただし (P2) により
  s≥z+1 が自動 → 値 2。corner: g*=0 となる非合同 k は z=2 の k=1 のみで、
  その平面では g=1>g*=0 が N2 に入り、corner → 床 B(m, 1, 2) = 2
  （Br2: a=m≥r+1=1）で無害な 2。north: q（s′≥z は
  N2、s′<z は N、ともに [g+1 odd]）。σ=q。C: g>g*+1 → v′=[g odd] → outcome q;
  g=g*+1 → 子 D → outcome 3; k=1 帯域: outcome q（z=2 の g=1 cell は 3 で無害）。
  outcomes ⊆ {q,2,3}・q∈ → mex=1−q=申立 ✓。
- **F（g<g*, s>z; m>k≥1 で m≥2・σ なし）**: west: s′>z のとき子 F
  → [g−1 even]=[g odd]=1−q; s′=z のとき（(P1) により g≢z 列のみ発生）子は
  子対角線上 → 値 2。corner（g=1）: 床 B(k,z,m) は s=2m+1>z ⇒ m≥r+1 を満たし、
  値は 1（z 奇・Br4）または 1/2（z 偶・Br3）で、1=1−q・2 は無害
  （F の申立 q=[g even]=[1 even]=0、違反は 0 のみ）。north: g+1<g* かつ
  s′>z → 子 F → [g+1 even]=1−q; s′=z → 子対角線 → 2; g+1=g* → 子 D → 2。
  C: 子 F → v′=[g even]=q → outcome 1−q; k=1 帯域（z 偶・g≤g*−1=z−2k−1≤z−3）:
  cpsfG(z−1, s, g) は s>Lw(z−1)=z で主則 Tw=g1(g−s(z−1))=g1(g−z+2<0)、
  g1(負)=IND((g−z+2)%2==0)=IND(g even)=q → outcome 1−q（k≥2 と同値）。
  outcomes ⊆ {1−q, 2, 3} かつ 1−q ∈ outcomes → mex=q=申立 ✓
  （q=0 なら 1 が在り 0 が不在、q=1 なら 0 が在り 1 が不在）。
- **G（s=z, g=z−2m≤g*, m≥k, g≥1）**: t := [g even] と置く。west: s′=z−1<z →
  子 N → [g−1 odd]=t。corner（g=1 → m=(z−1)/2, z 奇・k≤r）: 床 B(k,z,r)=0=t
  （Br1/Br4 の a≤r 全分岐）。north: [g+1 odd]=t。σ（m=1 ⇒ k=1 ⇒ (P4) z 偶 ≥4,
  g=z−2）: (g+1)%2=1−z%2=t。C: 子 F → v′=[g even]=t → outcome 1−t
  （m=k では g=g*: v′=IND(g* even)=1−z%2=t で同値）; k=1 帯域: 1^cpsfG(z−1,
  z, z−2) は R̃=z=Lw(z−1) → g1(0)=1 → outcome 0=1−t（t=1）。
  outcomes = {t, 1−t} = {0,1} をともに含み 2 を含まない → mex=2=申立 ✓。
- **D（g=g*, s≥z ⇔ m≥k）**: west: m=k のとき s=z → 子 N: [g*−1 odd]=1−z%2;
  m≥k+1 のとき s≥z+2（(P2)）で s′>z, g−1<g* → 子 F: [g*−1 even]=[g* odd]=z%2。
  corner（g*=1: k=(z−1)/2 非合同は z≡1 mod 4）: 床 B(k,z,m): m=k=r → 0、
  m>r → 1（Br4）= 1−z%2（z≡1 mod 4 ⇒ 1−z%2=0 ✓ 一致）。north: [g*+1 odd]
  =IND(g* even)=1−z%2（s′≥z/N2 と s′<z/N で同値）。σ（m=1 ⇒ k=1 ⇒ z 偶 ≥4,
  g=z−2）: (z−1)%2=1−z%2。C: 子 F → v′=IND(g* even)=1−z%2 → outcome z%2;
  k=1 帯域: outcome 0。outcomes には z%2 型（C）と 1−z%2 型
  （west/north/σ/bed corner）がともに現れ ⊂{0,1} で 2 を含まない
  → mex=2=申立 ✓。m=k=1 の併合 cell（z 偶 ≥4, g=z−2, s=z）の検算:
  children {west=1−z%2, σ=1−z%2, C=0} = {1, 0}（z 偶: 1−z%2=1）→ mex=2 ✓。
  （z 奇に m=1 の D cell は存在しない: k≥2 は m=1<k を満たさず、k=1 は z 奇で
  合同行になるため。）

全区域で mex が申立に一致し、申立の値域 {0,1,2} が確定する。
**T-NCW-P 証明完了。**

### 2.5 T-NCW-B: 床区域 mex 代数

床 (a,k,z) の申立値を B とし、A/B/C 子の値を評価する。σ₁=1（§2.2）。

- **Br1（g*<0）**: 申立 0。A: pair (a−1, 1) の値は g=1>g*(<0) により
  N/N2 とも [1 odd]=1。B(a=1): σ₁=1。C（k≥2; k=1 は z≥2 で g*=z−2<0 不可）:
  子床 (a, k−1, z−1): g**=g*+1≤0: g**<0 → 子値 0 → outcome 1; g**=0
  （z 奇・k=(z+1)/2 偶 ⇔ z≡3 mod 4）→ 子値 2 (a≤r′) / 2 (a≥r′+1、z′ 偶・
  g**=0 枝は全 2) → outcome 3。outcomes ⊆ {1,3} → mex=0 ✓。
- **Br2（g*=0, z≡2 mod 4, k=z/2 奇数）**: r=z/2−1。
  a≤r: 申立 0。A: s′=2a−1≤z−3<z → N → [1 odd]=1。σ₁=1。C: z≥6 は子床
  (a, z/2−1, z−1): z′ 奇・g**=1>0: a≤r′=r → 子値 0 → outcome 1
  （z=2: a≤r=0 は空）。outcomes={1} → mex=0 ✓。
  a≥r+1: 申立 2。A: s′=2a−1≥z−1: a=r+1 → s′=z−1<z → N → 1; a≥r+2 →
  s′≥z+1, g=1>g*=0 → N2 → [1 odd]=1。C: z≥6: 子床: a≥r′+1 →（z′ 奇枝）子値
  1 → outcome 0; z=2: 帯域 1^cpsfG(1, 2a, 0): R̃=2a≥2=Lw(1) → Tw(w=1 odd=g1):
  d−s(1)=0 → g1(0)=1 → outcome 0。outcomes ⊇ {1, 0}、2 なし
  （a=1 の z=2 cell は B のみで outcomes {σ₁=1, C=0}）→ mex=2 ✓（b2(1)=2 ✓）。
- **Br3（z 偶・g*>0⇔k<z/2 奇数, k≥1）**: r=z/2−1。
  a≤r: 申立 0。A: s′≤z−3<z → N → 1。σ₁=1。C: k=1（帯域）: 1^cpsfG(z−1, 2a, 0):
  R̃=2a≤z−2<Lw(z−1)=z → 2(0)=0 → outcome 1; k≥3: 子床 z′ 奇・g**=g*+1≥3:
  a≤r′=r → 0 → outcome 1。outcomes={1} → mex=0 ✓。
  a=r+1: 申立 2。A: s′=z−1<z → N → 1。C: k=1: 1^cpsfG(z−1, z, 0):
  R̃=z=Lw → Tw(w=z−1 odd=g1)(0−s(z−1)=−(z−2)): g1(負)=IND((2−z)%2==0)=1
  (z 偶) → outcome 0; k≥3: 子床 z′ 奇: a=r+1≥r′+1 → 子値 1 → outcome 0。
  outcomes={1, 0} → mex=2 ✓（Br3 は z≥4 なので r≥1・a=r+1≥2 で A 子は常に在る。
  z=2,k=1 は g*=0 なので Br2 側）。
  a≥r+2: 申立 1。A: s′=2a−1≥z+1>z, g=1<g*（g* 偶 ≥2）→ 子 F → [1 even]=0。
  C: k=1: 1^cpsfG(z−1, 2a, 0): R̃≥z+2>Lw → g1(2−z)=1 → outcome 0; k≥3:
  子床: a≥r′+2 → 子値 1 → outcome 0。outcomes={0} → mex=1 ✓。
- **Br4（z 奇・g*≥1⇔k 偶, k≥2 (P4)）**: r=(z−1)/2, r′=r−1。
  a≤r: 申立 0。A: s′=2a−1≤z−2<z → N → 1。σ₁=1。C: 子床 z′ 偶・g**=g*+1>0:
  a≤r′=r−1 → 子値 0 → outcome 1; a=r（=r′+1, (P5)）→ 子値 2 → outcome 3。
  outcomes ⊆ {1, 3} → mex=0 ✓。
  a=r+1: 申立 1。A: pair (r, 1): s′=z → 子対角線（m=r≥k）→ 子値 2 (G; g*≥3)
  または D∩G（g*=1, z≡1 mod 4・k=r 偶）=2。C: 子床 z′ 偶: a=r+1≥r′+2 →
  子値 1 → outcome 0。outcomes={2, 0} → mex=1 ✓。
  a≥r+2: 申立 1。A: s′≥z+1: g=1 vs g*: g*≥3 → 子 F → [1 even]=0; g*=1
  （z≡1 mod 4・k=r）→ 子 D → 2。C: 同 a=r+1 枝 → outcome 0。
  outcomes={0} または {2, 0} → mex=1 ✓。

**T-NCW-B 証明完了。** §2.4–2.5 に現れる全子値は T-NCW-P/T-NCW-B 自身
（R−1・packet 内）、K0832、K1303 のみであり、§2.0 の帰納で整合する。

### 2.6 K1309 packet との差分（なぜ非合同側は単一 R で閉じたか）

K1309 合同 packet {T-WC, T-WBC} は「C 子が合同行→合同行」で packet 閉性が
成り立っていたが、窓の値が対角行値 D(g,z) であったため区域分割が g にのみ
依存した。非合同 packet では C 子 (k−1, z−1) が再び非合同（k≢z ⇒ k−1≢z−1）
で**同じ packet に入る**ため自己参照的な閉性が得られ、子の dominant が
g**=g*+1 と 1 ずつ立ち上がることで §2.3 の区域写像が全区域で確定する。
合同 packet で K1309 が例外 cell 扱いした「k=1 かつ s≤z−2 の C 子=帯域読み
2·[g odd]」は、本パッケージでは K1303 帯域 cpsfG の直接値として消解し、
例外は残らない。

---

## §3 宣言前探索（凍結・explore_ncw.out の正本）

X1 T-NCW-P census z3..16・m1..8・g1..32: 16,128 点 bad 0
（内訳 N=15,406 / T2=224 / F=498）。X2 T-NCW-B census z3..18・a1..26:
2,080 点 bad 0。X3 2 の完全局在（dominant 列+対角線の捕獲・wedge 外 2 = 0）:
16,128 点 offband_or_missing=0。X4 typed packet 閉性（手申立+公刊閉形式のみで
子構成・mex==申立==engine）: z2..12 5,616 点 bad_typed_mex=0 bad_vs_engine=0。
X5 cross-engine canonical vs ordered NCW sample: 297 点 bad 0。X6 OBS-NCW 凍結
35 行表の再現 + 申立一致: 1,260 cell frozen_mismatch=0 claim_bad=0。X7 帯域
K1303 転写ゲート w1..12: 840 点 bad 0。X8 far stress z{24, 28}・m1..6・g1..24・
a1..20: 4,264 点 bad 0（z=24: 1,968 / z=28: 2,296）。
追加 XI（構築中の性質確認・§6 参照）: L2 σ 一様則 z2..60・NCW 全 k・g≤120:
108,000 点 bad 0。

## §4 機体宣言

キット `research/experiments/ncw-window-20261124/`。engine は K1138 転写・
sha pin `bd5f22e415a78368c9b798296bc84948d5637decbf3c21a92404d45fb12e3a92`
を verify_k1310.py が起動時 gate で検査（embed bytes は K1282..K1309 chain と
同一）。単体 engine_block.py は `582c93c1…`（chain 同一 bytes）。

| file | sha256 |
|---|---|
| verify_k1310.py | `58fd5e46d52a5a62950b796506e08704987bdb0badfedc73ca754468824d94f3` |
| engine_block.py | `582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0` |
| explore_ncw.py | `5d9b41b8d6c756ffd8932275bbb651b605ced2847930af9cea2067f682bbe3d8` |
| explore_ncw.out | `3f44deffe77ed2f2d69dd67cec20ce0b5bbef8e10685a6b6b08329cdb4f78e75` |
| predry/dryrun1-4.out | 4 走とも `3c2eb51742c568536b0bf67738be3c2f7b59bf87ae8a1eba42e28ead11168949`（byte-identical） |

**電池と counts（事前宣言・期待 overall_bad = 0・総計 51,439）**:

D1 T-NCW-P pair census（z3..16・m≤8・g≤24）12,096 / D2 far stress
（z{18,20,22}・m≤4・g≤48）5,760 / D3 m 距離 stress（z{5,8,11,14}・m≤20・g≤12）
4,320 / D4 T-NCW-B census（z3..16 a≤26 + z{18,20,22} a≤14）2,058 /
D5 typed self-check（手申立+K0832/K1303 閉形式のみで子構成・z2..14 含む・
mex==申立==engine 三点一致）9,016 / D6 B-exit triple（閉形式 vs 両 engine）
1,512 / D7 帯域 k=0 + k=1 C 子 cell gate（K1303 cpsfG 転写: ペア帯域 w1..15・
床帯域 w1..15・k=1 C 子 cell z 偶 4..22）3,870 / D8 公刊アンカー（K1309 T-WC
合同行・T-WBC・K1308 Z-DIAG/T-UH/T-DU′）4,960 / D9 cross-engine 372 /
D10 OBS-NCW 凍結表サブサンプション（凍結 35 行分布再現 + 申立 cellwise）
1,295 / D11 k=1 行 stress（z 偶 4..28・m≤12・g≤30）4,680 / D12 床 k=z−1 行 +
深 tail stress（z3..20 a≤30 + z{6,10,14,18} a≤40 全非合同 k）1,500。

**変異電池（fail-closed・事前宣言・全 rc=1 / engine は rc=2）**:

- `--tamper-engine` → rc=2（変異 sha `0ea47a80…` ≠ pin）
- `--tamper=np1` → bad **12,096**（D1 全点・T-NCW-P census 期待 flip）
- `--tamper=np2` → **5,760**（D2）/ `np3` → **4,320**（D3）
- `--tamper=bd` → **2,058**（D4 全点・T-NCW-B flip）
- `--tamper=ty` → **40,690**（申立関数 P/Bm 自体を flip: D1 12,096 + D2 5,760 +
  D3 4,320 + D4 2,058 + D5 9,016 + D10 1,260 + D11 4,680 + D12 1,500。
  D6–D9 は申立関数を参照しない engine 照合電池のため 0 — 設計上の honest 値）
- `--tamper=be` → **1,512**（D6）/ `cp` → **3,870**（D7）/ `ps` → **4,960**（D8）/
  `xg` → **372**（D9）
- `--tamper=rw` → **1,261**（D10: 申立 1,260 + 凍結表 '3,2' 行の改変 1）
- `--tamper=ex` → **4,680**（D11）/ `bs` → **1,500**（D12）

**決定論**: stdout は決定論的 JSON（volatile 情報は stderr の info 行のみ）。
predry 4 走（同一 cwd PYTHONHASHSEED=random/1 + 隔離 tree env -i 99/7）は
byte-identical `3c2eb517…`、rc=0、~2.5 秒/走（python 3.12）。

**公式監査プロトコル（出版後）**: (1) fetch-back 全ファイル byte 照合。
(2) 公式 4 走（fetch-back bytes から・同一 cwd×2 [PYTHONHASHSEED random/1] +
隔離 tree/env -i×2 [99/7]）: 全走 rc=0・stdout byte-identical・
sha=宣言 predry `3c2eb517…`。counts は上表・総計 51,439・overall_bad=0。
(3) 変異電池 13 種が全て上表の bad count と rc で fail-closed。
(4) output/ 成果物出版（audit_run1-4.out+.info・tamper レコード 13 種・
detcheck.json OFFICIAL-PASS・MANIFEST-sha256）・fetch-back。

## §4.5 主張の区別

本パッケージの全称定理（T-NCW-P/T-NCW-B/L2/C1–C5）は **§2 の手証明**が正本。
機体の D1–D4・D11・D12 census は定理の実機照合であって証明の代替ではない。
D5 は手証明の typed 子恒等式と mex 代数の machineChecks（点ごと一致検査）で
あり、 universally quantified な mex 閉包の根拠は §2 の区域表。D10 は観測表の
サブサンプション（観測→定理実例の昇格の確認）であり新規法則主張ではない。
OBS→定理の昇格済み要素（OBS-NCW/OBS-BW）について以後は K1310 を引用すること。

## §5 open 登録・接続

- **O-G2 内面 k≥1（multi-c web）**: K1303/K1309 から不変・本命。
  3 山以上の窓面・多山アナロジは本項では一切扱っていない（2 山ペア・床面のみ）。
- **F1/C-SUM 3 トークン typed 化**: 不変。
- **F2 giant 接続**: C5 により 2 山面の全 k 軸が O(1) 即値可能になった
  （z≥2・全 k∈Z・全 m,g または全 a）。11×11 枝刈り格子への採用判断は
  giant レーンオーナー。
- **標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4**:
  全時点 UNKNOWN・verdict 不消費・本項はこれらに一切影響しない。

## §6 honest 構築経緯

- L2（B-exit 則）の初版手分析は g=z の cell を σ=2 と誤って予測したが、
  出版前の機械追試（z2..60・108,000 点）と K0832 branch 再解析が
  σ=(g+1)%2 一様（g=z でも同値）を示したため修正した。σ の真値 [g even] は
  各区域の子の統一値そのものであるため mex 閉包・定理・電池設計への影響は
  ない。修正後の verify_k1310.py は初回実行で 51,439 点 bad 0。
- predry 3/4 走の初回は隔離 tree で `/usr/bin/python3` 不在による rc=127
  （空出力・sha `e3b0c442…`）で失敗。`which python3`（/usr/local/bin/python3）
  に修正して再実行し、4 走 byte-identical を確立した。失敗出力は出版対象外で
  破棄済み（§4 の表は修正後の実走のみを宣言）。
- D3 電池の例示 note 欄は期待値 1 つを欠く（表示用のみ・比較には無影響）。
- 機体実装上、D3 の tamper 分岐は `None or (...)` 構文で評価されるが、
  意味は E==flip(P) の比較と同一（おおっていない部分なし・検査漏れなし）。
