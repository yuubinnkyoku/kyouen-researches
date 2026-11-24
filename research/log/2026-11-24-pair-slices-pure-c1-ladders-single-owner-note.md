# 単一オーナー宣言ノート: ペア対角スライス理論と pure-c1 ラダーの全称確定（K1285 lane）

- 日付: 2026-11-24
- lane: 高速レーン（短〜中時間・厳密結果）。本ノートは fast-lane の単一オーナー宣言。
- 観測 HEAD（着手時・main）: `0b113ef3`（Part DJ batch-30 宣言・
  探査レーン・非接触）。**push 直前再取得**: `81ae89f1`（Part DJ A
  scaffold・実験dir 15 file・探査レーン・非接触）。0b113ef3 →
  81ae89f1 間のコミットは全て Part CP drive-3 / Part DJ 探査系で、
  本トピック（ペア対角スライス・pure-c1 ラダー）に接触しない。
- K item 番号: **K1285 は空き**（items dir のコミット履歴で最新
  K item は K1284 = 7abca71f〔items/K1284-z1-delta45-ladder.md〕、
  K1285 を取得したコミットなしを push 直前に再確認）。
- 対抗宣言なし（fetch 時点で本領域の単一オーナー宣言は本ノートのみ）。
- 規約: publish-then-execute（K1282–K1284 実務と同一。宣言ノート先頭出版 →
  キット出版 → fetch-back 照合 → 公式 4 走 → 監査成果物出版 → K item・run log・
  knowledge README bullet）。

## 用語・記法（repo 標準に準拠）

- 局面: H(R; X; z)。X = 多重集合 {m^c, …}（m = 行、c = 段数）、R = 予算
  （残り手数）、z = pass 残数。H は Grundy 値。手は A（トークン w>1 を
  w−1 へ・予算 R -> R−1）/ B（row-1 トークン除去: z -> z+1、R -> R−1・
  min>=2 の行では B 不可）/ C（pass: z>=1 で子の値は 1 XOR・予算
  R -> R−1）。
- ペア: X = (m, m+g)、g >= 1。**対角座標** k := R − 2m − g。行内ペアは全て
  (m, m+g) 形に正規化できる。
- [P] = 1 if P else 0。
- 単一トークン閉形式（K0832 公刊・v(x, z, R)）: z = 0 は
  v = min(R, x)%2。z ∈ {1, 2, 3} は tail 分岐型: 記法 q_odd(z) =
  z が奇数番目 (z∈{1,3,…}) かどうかで水平帯の先頭行 m を定め、
  1 <= z <= x−1 なら m := q_odd(z)、m < R < x+z なら (R+z)%2、
  それ以外は x%2。本ノートで使う読みは §2.9 に明記。
- 有限観測 (OBS) と全称定理 (THM) を明確に区別する。

## §1 主張一式

- **T-PS0 (z0 スライス)**: ∀ m>=1, g>=1, k∈{1,2,3}:
  H(2m+g+k; (m, m+g); 0) = [g odd]。
- **T-PS1 (z1 スライス)**: ∀ m, g, k∈{2,3}:
  H(2m+g+k; (m, m+g); 1) = [g odd]。
- **T-PS2 (z2 スライス)**: ∀ m, g, k∈{3,4}:
  H(2m+g+k; (m, m+g); 2) = [g odd]。
- **T-L1 (pure-c1 z0 ラダー)**: ∀ d>=1, m>=1:
  H(2m+d+2; (m, (m+d)^1); 0) = [d odd]。（T-PS0 k=2, g=d の再添字。）
- **T-L2 (pure-c1 z1 ラダー)**: ∀ d, m:
  H(2m+d+3; (m, m+d); 1) = [d odd]。（T-PS1 k=3, g=d。）
- **T-L3 (pure-c1 z2 ラダー)**: ∀ d, m:
  H(2m+d+4; (m, m+d); 2) = [d odd]。（T-PS2 k=4, g=d。）
- **T-ALM (allm-2 族の 6 床)**: ∀ m>=1:
  (m,m)@2m+2 z0 = 0、(m,m)@2m+3 z0 = 0、
  (m,m)@2m+2 z1 = 0（公刊 T-E1 の instance・重複掲載は照合用）、
  (m,m)@2m+3 z1 = 0、(m,m)@2m+3 z2 = 0、(m,m)@2m+4 z2 = 0。
- **L-EMPTY**: ∀ R>=0, z>=0: H(R; ∅; z) = 0。
- **L-11z0**: H(3; (1,1); 0) = 0、H(4; (1,1); 0) = 0。
- **L-1s**: H(2; (1); 1) = H(3; (1); 1) = H(4; (1); 1) = 1。
- **C-PB2**: ∀ x>=2, c>=1:
  H(x+2; (x^c); 1) = (c=1: [x odd]; c>=2: [x even])。
- **C-PC**: ∀ x>=2, c>=1:
  H(x+1; (x^c); 0) = (c=1: [x odd]; c>=2: [x even])。
- 解決登録: 上記 T-L2 の d=1 行、すなわち
  **(j, j+1)@2j+4 z1 = 1 ∀j は K1284 open 登録 C-PC1z1-d4 の c=1 半分の
  全称解決**（c>=2 半分は open 継続）。z2 面は K1283/K1284 の時点で
  open だった領域の最初の体系的確定。

## §2 証明

### §2.0 手分類と証明原理

ペア局面 P = (R; (m, m+g); z)、R = 2m+g+k の手は次のいずれかに帰着する
（これが族の閉性）:

- (i) A on min（fall）: m>=2 のとき子 = (R−1; (m−1, m+g); z)。
  これは行 m−1 のペア (m−1, m+g)、g′ = g+1、k′ = k（予算チェック:
  (R−1) − 2(m−1) − (g+1) = R − 2m − g = k ✓）。m=1 のときはこの手が
  B 手（トークン除去）で子 = (R−1; (m+g); z+1) = 単一トークン
  v(g+1, z+1, g+k+1)（m=1 のとき R−1 = g+k+1）。
- (ii) A on upper（upper-drop: トークン m+g → m+g−1。K1281 の呼称では
  g>=2 の場合 stair・g=1 の場合 compress に相当するが、本ノートでは
  子の族を統一するためいずれも「compress 子」と総称する）:
  g>=2 のとき子 = (R−1; (m, m+g−1); z):
  g′ = g−1、k 不変。g=1 のとき子 = (R−1; (m, m); z):
  allm-2 床 (m,m)@2m+k・平面 z。
- (iii) C（z>=1）: 子の値 = 1 XOR H(R−1; (m, m+g); z−1):
  同じペア、k′ = k−1、平面 z−1。

全主張を**予算 R に関する強帰納法**でまとめて証明する。各証明で現れる子
は全て予算 R−1 であるため、well-founded（§2.8）。基底部は
単一トークン閉形式 v（公刊・既に閉形式で即値評価）、床 L-EMPTY / L-11z0 /
L-1s（§2.1・手証明）、公刊 T-Q（z0-k1 g=1 の compress 角）、公刊 T-E1
（z1-k2 g=1 の compress 角、= T-ALM の (2,1) 項と同一局面）。

補助事実（全 k∈{1,2,3}・z∈{0,1,2} で使う）: §2.9 の v readings より

- z0 スライスの B 子（m=1）: v(g+1, 1, g+k+1) = [g even] for k∈{1,2,3}。
- z1 スライスの B 子: v(g+1, 2, g+k+1) = [g even] for k∈{2,3}。
- z2 スライスの B 子: v(g+1, 3, g+k+1) = [g even] for k∈{3,4}。

### §2.1 床

- **L-EMPTY**: z=0 は手なし、H = 0。z>=1 は C のみ: 子 = 1 XOR H(R−1; ∅; z−1)。
  z に関する帰納で全て 0 を得る。∎
- **L-1s**: R∈{2,3,4}: B 子 = (R−1; ∅; 2) = 0（L-EMPTY）、C 子 =
  1 XOR H(R−1; (1); 0) = 1 XOR 0 = 0（H(R−1;(1);0) は B のみで
  mex{(R−2;∅;1)} = mex{0} = 1 ゆえ 1 XOR 1 = 0）。全子 = 0 で mex{0} = 1。∎
- **L-11z0**: 2 つの 1-トークンの B 子は同じ (1)@(R−1) z1。R=3: (1)@2 z1
  = 1（L-1s）、R=4: (1)@3 z1 = 1（L-1s）。ともに mex{1} = 0。∎

### §2.2 allm-2 族（T-ALM）

局面 (2m+j; (m, m); z)、(j, z) ∈ {(2,0), (3,0), (2,1), (3,1), (3,2), (4,2)}。

- A 子（fall）: (2m+j−1; (m−1, m); z) = ペア k=j・g=1・平面 z の
  スライス値 [1 odd] = 1（帰納法。§2.2 内では §2.3–2.5 を子として使うが
  予算は 1 減: スライスの compress 角として本床を参照する場合も互いに
  予算が減少していることで循環なし、§2.8）。
- B 子（m=1 のときのみ）: (1)@(1+j) z+1 の単一トークン:
  v(1, 1, 3) = v(1, 1, 4) = 1、v(1, 2, 3) = v(1, 2, 4) = 1、
  v(1, 3, 4) = v(1, 3, 5) = 1。全て 1。
- C 子（z>=1 のときのみ）: 1 XOR (m,m)@2m+j−1 平面 z−1 の値:
  (2,1) → 1 XOR (2m+1 床 z0)（T-Q 型角。公刊: 0）= 1、
  (3,1) → 1 XOR (m,m)@2m+2 z0 = 1 XOR 0 = 1、
  (3,2) → 1 XOR (m,m)@2m+2 z1 = 1 XOR 0（公刊 T-E1 instance）= 1、
  (4,2) → 1 XOR (m,m)@2m+3 z1 = 1 XOR 0 = 1。

全子 = 1（≠0 のみ）ゆえ mex = 0。∎

（注: (m,m)@2m+1 z0 すなわち compress 角 (j=1, z=0) は公刊 T-Q が m>=2 を
担保しているため本定理には含めない。照合系は m>=2 を検査する。）

（注: z2 スライス k=3/k=4 の compress 角は (3,2)/(4,2) の 2 項のみでよい:
g=1 compress 子の予算は 2m+k、k∈{3,4} ゆえ j∈{3,4} に対応。）

### §2.3 z0 スライス（k∈{1,2,3}・T-PS0）

P = (2m+g+k; (m, m+g); 0)。子は fall（または m=1 で B）と compress のみ
（z0 ゆえ C なし）。

(a) **g odd（主張 1）**: 0-witness は fall 子（m>=2）: 行 m−1 のペア
g+1（even）ゆえ [(g+1) odd] = 0。m=1 なら B 子 v(g+1, 1, g+k+1) = 0。
1 が現れないこと: fall 子 = 0 ✓（上記）。compress 子: g>=3 なら
[g−1 odd] = [even] = 0 ✓、g=1 なら allm-2 角 (m,m)@2m+k z0:
k=1 は (m,m)@2m+1 = T-Q 角（公刊 0; m=1 は L-11z0(3)）、
k=2 は Wa_2 = 0、k=3 は Wa_2′ = 0（§2.2 の (2,0), (3,0) 項）。✓
m=1 の B 子 = [g even] = 0 ✓。よって全子 ∌ 1、mex = 1。✓

(b) **g even（主張 0）**: 全子が 1: fall 子 = [(g+1) odd] = 1、
compress 子 = [g−1 odd] = 1（g>=2 ゆえ角なし）、B 子 = [g even] = 1。
mex{1} = 0。✓ ∎

### §2.4 z1 スライス（k∈{2,3}・T-PS1）

子: fall/B、compress、C = 1 XOR（z0 スライス k−1 の同 (m,g) 値 [g odd]
（予算 1 減で帰納法適用可））。

(a) **g odd**: 0-witness: fall 子 = 0。1 は現れない: compress: g>=3 は 0、g=1 は
角 (m,m)@2m+k z1: k=2 は (m,m)@2m+2 z1 = 0（公刊 T-E1 = §2.2 (2,1) 項）、
k=3 は (m,m)@2m+3 z1 = 0（§2.2 (3,1) 項）。C 子 =
1 XOR [g odd] = 1 XOR 1 = 0 ✓。B 子 = [g even] = 0 ✓。mex = 1。✓

(b) **g even**: 全子 1: fall 1、compress 1（角なし）、
C = 1 XOR 0 = 1、B = 1。mex = 0。✓ ∎

### §2.5 z2 スライス（k∈{3,4}・T-PS2）

子: fall/B、compress、C = 1 XOR（z1 スライス k−1 の値 [g odd]）。

(a) **g odd**: 0-witness: fall 0。1 は現れない: compress: g>=3 は 0、g=1 は角
(m,m)@2m+k z2: k=3 は §2.2 (3,2) 項 = 0、k=4 は (4,2) 項 = 0。
C = 1 XOR 1 = 0 ✓。B = 0 ✓。mex = 1。✓

(b) **g even**: 全子 1（角なし・C = 1 XOR 0 = 1）。mex = 0。✓ ∎

### §2.6 ラダー系（T-L1/L2/L3・再添字による即時系）

(m, (m+d)^1) はペア (m, m+d)、g = d。よって:

- T-L1: H(2m+d+2; …; 0) = T-PS0(k=2, g=d) = [d odd]。
- T-L2: H(2m+d+3; …; 1) = T-PS1(k=3, g=d) = [d odd]。
- T-L3: H(2m+d+4; …; 2) = T-PS2(k=4, g=d) = [d odd]。∎

**C-PC1z1-d4（c=1）の解決**: (j, (j+1)^1)@2j+4 z1 は T-L2 の
d=1, m=j 行。値 = [1 odd] = 1 ∀j。K1284 open 登録のうち c=1 半分が
全称確定（c>=2 半分は open 継続）。

### §2.7 pre-band 単層族（C-PB2 / C-PC）

- **C-PB2**: PB2(x, c) = (x^c)@x+2 z1、x>=2。公刊 T-B1′(i)（K1283）の
  instance: 行 m = x、R = x+2 ∈ [x+2, 2x] は帯底。ゆえ H =
  v(Σ, 1, x+2)、Σ = cx。c=1: v(x, 1, x+2) = x%2 = [x odd]（§2.9）。
  c>=2: v(cx, 1, x+2): z=1、Σ>=4、1<=z、m=q_odd(1)=1、
  1 < R=x+2 < Σ+1 = cx+1 ⟺ x(c−1) > 1 ✓（x>=2, c>=2）ゆえ
  (R+z)%2 = (x+3)%2 = [x even]。∎
- **C-PC**: PC(x, c) = (x^c)@x+1 z0。公刊 T-B0′(i)（K1282）の instance:
  R = x+1 ∈ [x+1, 2x] 帯底。H = min(R, Σ)%2 = min(x+1, cx)%2。
  c=1: min(x+1, x) = x → [x odd]。c>=2: cx >= 2x >= x+2 > x+1 ∴
  min = x+1 → (x+1)%2 = [x even]。∎

### §2.8 予算帰納の well-founded 性

共同主張集合 C = {PS0, PS1, PS2, ALM, PB2/PC, 床}。各主張の証明内で
参照する子の予算は全て「当該局面の予算 − 1」であり、参照先の主張は
（ペア→ペア、ペア→allm-2、allm-2→スライス g=1、スライス→allm-2 角、
いずれの向きでも）予算が真に減少する。最小予算の主張は床と単一トークン
閉形式（予算 <= 4）ですべて手証明済みで、無限後退はない。したがって
予算 R に関する強帰納法で全主張が同時に確定する。

（整合性の独立再導出: T-H1 は T-PS0 の k=1, g=1 行、公刊 T-E1 の
instance は T-ALM の (2,1) 項と同一局面。本ノートの証明はどちらも
独立に再導出しており、公刊値との一致を照合系 D1–D10 が機械確認する。）

### §2.9 本ノートで使う単一トークン v readings（K0832 公刊形式から）

z=0: v = min(R, x)%2。z∈{1,2,3} は tail 分岐（x%2 に帰着する帯）を含む。
本ノートで使うのは次の値（いずれも閉形式の直截計算）:

- v(g+1, 1, g+k+1) = [g even]、k∈{1,2,3}: x = g+1、z = 1、R = g+k+1:
  R が x+z = g+2 以上の領域（k>=1）で tail 分岐 x%2。
- v(g+1, 2, g+k+1) = [g even]、k∈{2,3}: 同様に tail（g=1 の角 v(2,2,4)
  = v(2,2,5) = 0 も x%2 と一致）。
- v(g+1, 3, g+k+1) = [g even]、k∈{3,4}: 同様に tail（g=1: v(2,3,·) = 0、
  g=2: v(3,3,·) = 1 = [g even] ✓、g>=3 は水平帯・tailとも x%2）。
- v(1, ·, ·) = 1（§2.2 の B 子）、v(x,1,x+2) = x%2、
  v(cx,1,x+2) = (x+3)%2（§2.7）。

## §3 宣言前探索実績（explore_k1285）

- `explore_k1285.py / explore_k1285.out`: E1（ペア k スライス族の発見表:
  z0-k1..3 / z1-k2..3 / z2-k3..4 の g-parity 予想の finite 支持と
  k が外れる例の提示）、E2（J-family・pure-c1 ラダー d-parity の
  finite 確認）、E3（pre-band 単層則 C-PB2/C-PC の finite 確認）、
  E4（境界三角形 z0-k0/z1-k1/z2-k2/z2-k1 の census と法則の観測的提示）、
  E5（multi-c web: F(1,c>=2)=0 / G(1,2)=0 / G(1,c>=3)=2 / A_a>=3
  非自明値 / G(d,c>=2)・Y族 spread の有限観測）、E6（z2 pre-band
  (x^c)@(x+3) z2 の census と z2-band 崩壊 blocker の観測）。
- これらは**宣言前探索 (OBS)** であり、本ノートの定理群とは区別する。
  alive-run は全て dryrun と label する（§4 機体が宣言値で照合済みの
  有限 battery を公式 runs として出版する）。
  出力は決定的（seed 非依存・PYTHONHASHSEED 4 走で byte-identical を
  ローカル確認済み）。

## §4 機体宣言（verify_k1285.py）

- sha256: `a4165f68b48d2a6c95e9a6d728b9503bab226f93f48dfb28d568147b6e7edd`
- engine block pin（embedded 文字列の sha）:
  `bd5f22e415a78368c9b798296bc84948d5637decbf3c21a92404d45fb12e3a92`
  （K1283/K1284 と同一の公刊 block を verbatim 同梱。起動時ゲート）
- 検査 battery D1–D10 と点数: D1 z0-slices 1296（T-PS0）、D2 z1-slices
  864（T-PS1）、D3 z2-slices 864（T-PS2）、D4 pure-c1 ladders 768
  （T-L1/L2/L3）、D5 allm-2 六床 180（T-ALM）、D6 床 400
  （L-EMPTY/L-1s、L-11z0 は D1 の m=1 行に包含も独立点として含む）、
  D7 PB2/PC 130（C-PB2/C-PC）、D8 T-H1/T-E1/Q/E1-instance 再照合
  4200（公刊定理との衝突検査）、D9 境界三角形 census 560（OBS 添付）、
  D10 multi-c web census 532（OBS 添付）。総 9,794 点、bad = 0。
- **公式 runs（宣言値）**: 4 走とも stdout byte-identical、rc 0。
  stdout sha256:
  **`41762e1b986d08494f4afd0ab4d8f1eb5a406e3608bc8696991b2019df735730`**
  （同一 cwd × PYTHONHASHSEED = random / 1、隔離 tree・env -i ×
  PYTHONHASHSEED = 99 / 7 の組で決定性を確認）。
- **TAMPER 変異電池**: `--tamper-engine`（engine 改変検知）rc 2。
  `--tamper=zz0|zz1|zz2|lad|alm|fl|pb`: bad = 1296 / 864 / 864 / 768 /
  180 / 5 / 130、rc 1（fl は床への消失検知**5 点**・宣言値）。
- キット（research/experiments/pair-slices-20261124/）: README.md、
  verify_k1285.py、engine_block.py、explore_k1285.py、explore_k1285.out、
  output/dryrun*。公式監査成果物（audit_run1-4.json + .info、
  detcheck.json、MANIFEST-sha256）は公式走後に出版する。

## §5 open 登録と K1286 ロードマップ

- **OBS-D9 境界三角形（D10 OBS として有限観測のみ登録・全称は open）**:
  z0-k0 = [2, 1, 0, [g even]]、z1-k1 = [1, 2, 0, [g even]]、
  z2-k2 = [1, 0, 2, [g even]]（m の小さい順・最終成分は g-parity tail）、
  z2-k1 = [g odd]（clean 観測）。証明には z1-k0 → z0-k(−1) への
  カスケードが必要で、k<0 座標系の拡張が blocker。**未来課題 F1**。
- **OBS-D10 multi-c web**: F(1, c>=2) = 0、G(1, 2) = 0、
  G(1, c>=3) = 2、A-ladder a>=3 の非自明値、G(d, c>=2)・Y族 spread。
  c>=2 の行構造はペア理論の外にあり、**spread 理論（c 方向の帰納）**が
  本命。z2 pre-band (x^c)@(x+3) z2 の確定は z2-band 崩壊が blocker。
  **未来課題 F2**。
- **C-PC1z1-d4 の c>=2 半分**: spread 理論待ち。**未来課題 F3**。
- **11×11 巨大探索との接続**: ペア対角スライスは枝刈り格子としてそのまま
  使える（ペア局面の子が全て既知族に落ちるため値即値評価が可能）。
  verdict は消費しない。

## Honest 記録

- 本ノートの公式 4 走は push 後の fetch-back 機体から実行する
  （publish-then-execute）。宣言前のローカル runs は dryrun として
  label し成果物に含める。
- 計算・検証は今回の高速レーン実行環境内で行った（GPU/外部リソース不使用）。
- 並走レーン（batch-30 など）との非接触: 担当領域が直交（探索系 vs
  本ノートの証明・照合系）であり、push は宣言ノート・キット・K item の
  追加のみで既存ファイルを書き換えない。
