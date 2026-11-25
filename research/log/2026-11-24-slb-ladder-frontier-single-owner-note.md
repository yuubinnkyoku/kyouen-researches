# 単一オーナー宣言 K1306: SLB/L/E 梯子の型付き子閉包と L 前線則 — K1287 O1 残部 (multi-c web) の第一歩

- 日付: 2026-11-24
- lane: 高速レーン（短〜中時間・厳密結果）。本ノートは fast-lane の単一オーナー宣言（publish-then-execute）。
- 観測 HEAD（着手時・main）: `4c2c4174` → 公式直近取得で `d8b849e5`（2026-11-24T21:31:12Z・
  Part DU small-pockets 探査レーン・領域直交）。push 直前に再度 main を取り直す。
- K item 採番: **K1304 は取得済み**（`items/K1304-pg2q9-small-cap-grundy.md`・PG(2,9) レーン・直交）・
  **K1305 も取得済み**（`K1305-pg2q9-five-cap-orbits.md`・同レーン）。よって本パッケージは
  **K1306** を採番する（items tree 列挙で K1306 なしを確認・push 直前に再確認）。
- 対抗宣言なし: fetch 時点で本領域（単一層トークン族 S/L/E の型付き子閉包・L 前線則）の
  単一オーナー宣言は本ノートのみ（本日の境界面レーン border-slices / lowz-window2 /
  raxis / strip / z-front / delta45 は全て pair 位置 (m,m+g)@(R,z) の帯・床・δ行であり
  トークン多重度族 S=(x^c)@… とは非接触。K1285 pair-slices / K1287 multic-web は
  到達済み領域の既刊）。
- 位置づけ: K1287（multic-web-f2）が §5 O1 として残した「SLB2/SLB3/L/Am typed 全称化」であり
  K1303 README レジューム (b)「O-G2 内面 k≥1 (multi-c web)」の直接の第一歩。
  本項は (i) その**構造的部分の全称確定**（型付き子閉包 S→L∪E・L↗P/Q/G・E の B/C 閉性）、
  (ii) **T-L0・T-S1 の全称定理 2 本**（K0832 閉形式からの直接導出 + z 帰納）、
  (iii) **census 予想 3 本**（C-LD1・C-L2+・C-SX1）、(iv) 前線 OBS の明示的登録を行う。
- 規約: verdict 不消費。標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は
  全て UNKNOWN のまま。engine はゲーム定義の転写（K1138 chain・sha 実装 pin）であり
  census は照合であって証明の代替ではない。

## 用語・記法（K1287 準拠・z は plane）

残余ゲーム H(R; X; z)（K1138 再帰・値は mex）。A手（トークン w>1 を w−1 へ・R→R−1・plane 不変）・
B手（トークン 1 を除去・R→R−1・plane z→z+1）・C手（plane z≥1 で子の値 1 XOR・R→R−1）。
H(0;·)=0。単一トークン閉形式 v(x,z,R)（K0832・本キットの engine_block.py に転写）。

パッケージ座標（すべて局面 = (トークン多重集合, 予算, plane)):

- **S(x,c,z)** := (x^c)@(x+1+z) plane z（単一層ラダー。z=1 は既刊 C-PB2 族・K1287 I11 の
  row-1 W の B-min 到達点の一般化）
- **L(zp,d,s)** := {d,(d+1)^s}@(d+2+zp) plane zp+1（K1287 I10 の B-min L 点の族。zp=−1 も
  許す: plane 0）
- **E(c,R,z)** := (1^c)@R plane z（all-1 族。B/C のみで閉じる）
- 前線族（本項では**法則を主張しない**・登録のみ）: **Q(zp,d,s)** := {d−1,(d+1)^s}@(d+1+zp)
  plane zp+1・**P(zp,d,t)** := {d^2,(d+1)^t}@(d+1+zp) plane zp+1・**G(s,zp)** := (2^s)@(zp+2) plane zp+2
- **Am(m,h,s,z)** := {m^2,(m+h)^s}@(2m+2+z) plane z（K1287 出身・アンカーに使用）

## §1 主張

### 定理（全称・量化は非有界・証明は §2 に全文）

- **T-L0 (L の s=0 列の確定)**: ∀zp ≥ −1, ∀d ≥ 1: **L(zp,d,0) = [d odd]**。
  すなわち単一トークン (d)@(d+2+zp) plane zp+1 の値は d の奇偶のみで決まる。
  系として S(x,1,z) = L(z−1,x,0)（同一局面）ゆえ **S の c=1 列の全称値は [x odd]**。
- **T-SLC (型付き子閉包代数・engine-free 位置恒等式)**:
  - I-S1: S(x,c,z) (x≥2) の A 子（値 v(x)=x の減算）はちょうど L(z−1, x−1, c−1)。
    （c=1 では L(z−1,x−1,0) = 単一トークン。）
  - I-S2: S(x,c,z) (z≥1) の C 子は S(x,c,z−1)（値は 1 XOR）。
  - I-S3: S(1,c,z) (c≥1) の B 子は E(c−1, z+1, z+1)。A 子は存在しない（x=1）。
  - I-S4: S(x,c,z) の子全体 = I-S1/I-S3 ∪ I-S2 で過不足なく尽くされる。
  - I-E1: E(c,R,z) の B 子 = E(c−1, R−1, z+1)（c≥1）。A 子は存在しない（値 1 は減算されず除去される）。
  - I-E2: E(c,R,z) (z≥1) の C 子 = 1 XOR E(c, R−1, z−1)。**E 族は B/C のみで閉じる**。
  - I-L1: L(zp,d,s) (d≥2) の d 側 A 子 = Q(zp,d,s)。
  - I-L2: L(zp,d,s) (s≥1) の (d+1) 側 A 子 = P(zp,d,s−1)。
  - I-L3: L(zp,1,s) の B 子 = G(s,zp)。
  - I-L4: L(zp,d,s) (zp≥0) の C 子 = 1 XOR L(zp−1,d,s)。
  - **帰結 (frontier closure)**: S 族の子は L ∪ S(z−1) ∪ E に閉じる（**S の値問題は
    L と E と S-z-ラダーに完全帰約**）。L の外向き子は P/Q/G と L(z−1) のみであり、
    S を証明するために必要な新規族は **P/Q/G の 3 族に限定される**（O1 の真の前線）。
- **T-S1 (S の c=1 列・z 全般)**: ∀x ≥ 2, ∀z ≥ 0: **S(x,1,z) = [x odd]**。
  （T-L0 + I-S1/I-S2 + 基底 z=0（C-PC c=1 列 = 閉形式）からの z 帰納・証明 §2.3。）
  これは exploratory に観測されていた c=1 列の全称定式化である。

### census 予想（有限照合・全称主張はしない・範囲を明示）

- **C-LD1 (L の d=1 閾値則・census zp ≤ 20, s ≤ 20 の 441 点)**:
  **L(zp,1,s) = 1 (s ≤ ⌈zp/2⌉); 2 (s > ⌈zp/2⌉ かつ zp 偶数); 0 (同・zp 奇数)**。
  （s=0 は T-L0 の d=1 行と一致。）「下は 1 の対角閾値帯・上は zp 偶奇の定数」構造。
- **C-L2+ (L の d ≥ 2 行の zp 拡張・census zp ∈ {0,1,2,3}, d 2..14, s 1..12 の 624 点)**:
  **L(zp,d,s) = [d even]**（K1287 OBS の zp≤1 を zp≤3 に拡張）。zp≥4 は §4 の境界 OBS に登録。
- **C-SX1 (x=1 列 = E の上対角則・census z 1..12, c 1..12 の 144 点)**:
  **S(1,c,z) = E(c,z+2,z) = [c odd] (c ≤ t0(z)); 2·[z odd] (c > t0(z))、t0(z) := z+1+[z even]**。
  （下は交互 [c odd] 帯・上は z 偶奇の定数。C-LD1 と双対的な「閾値帯 + 偶奇定数」構造。）

### アンカー（既刊法則の転写照合）

- **C-PC** (x^c)@(x+1) plane 0 = c=1: [x odd] / c≥2: [x even]（x 2..12, c 1..6 の 66 点）。
- **C-PB2** (x^c)@(x+2) plane 1 = S(x,c,1) 同法則（66 点・S の z=1 面）。
- **Am z 0..2**（m 1..10, h 2..6, s 0..8 の 1350 点・K1287 法則の正確な再照合:
  z=0 → 0・z=1 → s≥1 で 2・z=2 → 0 ただし (m,h,s)=(1,2,1) → 1）。

### OBS（観測登録・法則主張なし）

- **OBS-LB (L の zp≥4 境界)**: [d even] からの例外セル table（zp 4..12 × d 2..8 × s 1..6・378 点）。
  例外は (d,s)=(3,1) が zp≥4 で全て、(2,2) が zp≥5 で、(3,2) が zp≥8 で、(5,1) が zp≥8 で
  現れ、zp 11/12 では (2,4),(3,3),(4,2),(7,1) 等も加わる（機体 obs 出力の正確な記録に依る）。
- **OBS-SW (S の z-波)**: S(x,c,z) の c≥2・x≥3 の [x even] 則は z≤5 で保たれ、z≥6 で
  境界波（例: S(4,2,6)=2・S(3,3,7)=2・S(4,3,10)=2 など table）が走る。この波は
  I-S1 により L(z−1,·) 境界面の値変化として完全に記述される（D6 構成照合が engine と一致
  するすべての点で）。
- **OBS-Am3 (Am の z≥3 面)**: 値ヒストグラム（m 1..6, h 2..6, s 0..6, z 3..5 の 630 点）。
  宣言前探査では s=1 行に値 1 の構造（h=1 極限と m+h 奇数の対角系列）が z=2..8 で観測される —
  法則化は次回課題とし主張しない。
- **OBS-X1 (E の全般表)**: x1col z 1..12 × c 1..10 の生値行（D11 に収録）。

## §2 手証明

### §2.1 T-L0（K0832 閉形式からの直接導出）

L(zp,d,0) = (d)@(d+2+zp) plane zp+1。x := d, z′ := zp+1, R := d+2+zp と置くと
**R = x + z′ + 1**（予算は「x+z′ ウィンドゥ」のちょうど 1 先）であることに注意。
K0832 閉形式 v(x,z′,R) の場合分け:

1. **z′ = 0**（zp = −1）: R = d+1。閉形式は min(R,x)%2 = min(d+1, d)%2 = d%2 =
   **[d odd]** を返す ✓。
2. **z′ = x**（zp = d−1）: R = 2d+1 奇。R ≤ 2x−1 = 2d−1 は偽（R = 2d+1）。
   R 偶の分岐も偽。よって戻り値 x%2 = **[d odd]** ✓。
3. **1 ≤ z′ ≤ x−1**（zp ≤ d−2）: m = q_odd(z′) ≤ z′ ≤ d−1。
   R = d+1+z′ ≥ d+2 > m ✓（R > m）。また m < R < x+z′ は R = x+z′+1 > x+z′ により偽。
   よって第 3 戻り値 x%2 = **[d odd]** ✓。
4. **z′ ≥ x+1**（zp ≥ d）: m = q_odd(x) ≤ d < d+2 ≤ R ✓（R > m）ゆえ戻り値 x%2 =
   **[d odd]** ✓。

全 4 場合で値は [d odd] かつ R は窓 m < R < x+z′ に入らない（構造的に R = x+z′+1）。
これが T-L0。∎

### §2.2 T-SLC（手の定義からの位置恒等式・engine-free）

各恒等式は「手の定義を座標に翻訳するだけ」の位置等式であり、engine の値再帰を一切使わない:

- I-S1: S(x,c,z) のトークン x を 1 個 x−1 へ減らすと多重集合 {x−1, x^(c−1)}、
  予算 x+z、plane z。L(z−1, x−1, c−1) の定義多重集合 {x−1, x^(c−1)}・予算
  (x−1)+2+(z−1) = x+z・plane (z−1)+1 = z と一致。c=1 では {x−1}・予算 x+z・plane z =
  L(z−1, x−1, 0)（s=0 列）。∎
- I-S2: C 手は予算 x+z・plane z−1・多重集合不変 = S(x,c,z−1) そのもの。∎
- I-S3: x=1 のトークンは値 1 ゆえ A でなく B（除去）をとる: 子は {1^(c−1)}、
  予算 z+1、plane z+1 = E(c−1, z+1, z+1) の定義そのもの。∎
- I-S4: S のトークンの相異なる値は x の 1 種のみゆえ A/B 子は高々 1 型、C は 1 型。
  I-S1/I-S3（x=1）/I-S2 以外の手は存在しない。∎
- I-E1/I-E2: E のトークン値は 1 のみで A は不存在、B 子 = {1^(c−1)}@R−1 plane z+1 =
  E(c−1,R−1,z+1)、C 子 = 1 XOR E(c,R−1,z−1)。E 族は B/C で閉じる。∎
- I-L1: L の d トークン（d≥2）減算 → {d−1, (d+1)^s} 予算 d+1+zp plane zp+1 = Q(zp,d,s)。∎
- I-L2: (d+1) トークン減算 → {d, d, (d+1)^(s−1)} 予算 d+1+zp plane zp+1 = P(zp,d,s−1)
  （s=1 では {d,d} = P(zp,d,0)）。∎
- I-L3: d=1 の B → {(d+1)^s} = {2^s} 予算 zp+2 plane zp+2 = G(s,zp)。∎
- I-L4: C → 1 XOR L(zp−1,d,s)（plane zp+1 ≥ 1 ⟺ zp ≥ 0 で有効）。∎

機体 D5 がこれらの**子位置集合の完全一致**（独立実装の子列挙 vs 族座標・双方向包含）を
pointwise 照合する。∎

### §2.3 T-S1（c=1 列の z 帰納）

S(x,1,z) (x≥2) の子は I-S1/I-S2 でちょうど 2 つ:
値 L(z−1, x−1, 0) = [x−1 odd] = [x even]（T-L0）と 1 XOR S(x,1,z−1)。

帰納: z=0 では C 子がなく S(x,1,0) = (x)@(x+1) plane 0 = 閉形式 v(x,0,x+1) =
min(x+1,x)%2 = [x odd]（基底）。z ≥ 1 で帰納仮説 S(x,1,z−1) = [x odd] とすると:
- x 偶数: A 子 = [x even] = 1、C 子 = 1 XOR 0 = 1 → mex{1} = 0 = [x odd] ✓。
- x 奇数: A 子 = 0、C 子 = 1 XOR 1 = 0 → mex{0} = 1 = [x odd] ✓。∎

（x=1 列は I-S3 により E 値に帰着し、E には本項で全称則がないため C-SX1 の census どまり。）

## §3 機体 verify_k1306 と電池（出版後・fetch-back bytes から公式実行）

- 機体: `verify_k1306.py`（sha256
  **`2b05440638f28eaad00f5665e29ffb8f16d68d5a91f75f012aede515fad0811f`**）。
  engine block は埋め込み転写・startup sha ゲート（pin
  `582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0`・
  K1282..K1303 キットと byte-identical）。stdout 決定的 JSON・揮発情報は stderr のみ。
- バッテリー（D1..D11・counts ベクタ申立）:
  D1 T-L0 census（zp −1..14 × d 1..20 = **320**・engine 両実装 × 閉形式 × 法則）
  D2 C-LD1（zp 0..20 × s 0..20 = **441**）
  D3 C-L2+（zp 0..3 × d 2..14 × s 1..12 = **624**）
  D4 OBS-LB 境界 table（zp 4..12 × d 2..8 × s 1..6 = **378**・法則主張なし・table 出力）
  D5 T-SLC 子集合恒等式（S 704 + E 864 + L 576 = **2144**・独立子列挙との完全一致）
  D6 typed 構成照合（x 1..6 × c 1..6 × z 0..10 = **396**: 族子の engine 値から構成した mex ==
      engine S 値）
  D7 C-SX1（z 1..12 × c 1..12 = **144**）
  D8 アンカー（C-PC 66 + C-PB2 66 + Am z0..2 1350 = **1482**）
  D9 OBS-Am3（z 3..5 = **630**・histogram）
  D10 交差 engine（S 216 + L 324 + E 336 = **876**）
  D11 OBS 表（S-波 140 + x1col 120 = **260**）
  **counts = [320, 441, 624, 378, 2144, 396, 144, 1482, 630, 876, 260]・総計 7,695・
  expected overall_bad = 0**。
- 変異電池（fail-closed・全モード宣言値）:
  `--tamper-engine` → **rc 2**（mutated block sha
  `9fd1bd76c478f85c7bea71c5c9ee621d4d240627146f0b9a86c998b414288131` ≠ pin）。
  `--tamper=hl` → rc 1・**D1 bad 320**。`--tamper=hbd` → rc 1・**D2 bad 21**。
  `--tamper=ws` → rc 1・**D3 bad 624**。`--tamper=Ls` → rc 1・**D7 bad 6**。
  （hl=T-L0 値反転・hbd=C-LD1 閾値 +1・ws=C-L2+ 偶奇反転・Ls=C-SX1 閾値 −1。各 bad 数は
  対応 gate の census 箱内で反転が審判される点数そのもの。）
- predry（宣言前ローカル 4 走: 同一 cwd PYTHONHASHSEED random/1 + 隔離 tree env -i 99/7）:
  4 走 stdout **byte-identical** sha256
  **`e9925e18f50ee1492ed30f420a7328de6cf8a2e22d61991aa73d78dd64084291`**
  （rc 0・約 31s/走）。
- 公式 4 走は本宣言の push 後に fetch-back bytes から実行し、4 走 stdout が predry と
  byte-identical であることを detcheck.json に機械記録する。続いて変異電池 5 モードを
  宣言値どおり fail させる。tamper_engine.info は空出力（size 0）になる。

## §4 宣言前探査の全開示（battery 設計修正 3 件・honest 記録・repo 未接触）

宣言前の機体開発での失敗と修正を隠さず記録する:

1. **D5 独立子列挙の B 手 plane 誤り**: 子列挙実装が B 手（トークン 1 除去）の子を
   plane z+1 でなく z に出力していた（1,087 点 bad）。修正は列挙側 1 行。宣言値・
   engine には影響なし。
2. **D5 L の C 手有効条件の誤り**: family 側の C 子を zp≥1 としていたが、正しくは
   plane zp+1 ≥ 1 すなわち zp≥0（zp=0 の 8×9=72 点 bad）。修正後 0 bad。
3. **C-SX1 法則の refit**: 初回 fit「c 偶 → 0 / c 奇は閾値付き」は上位域の偶奇を誤読
   していた（10 点 bad）。正しい構造は「c ≤ t0(z) 交互 [c odd] / c > t0(z) 定数 2·[z odd]」
   で、x1col 全行と整合（144 点 bad 0）。上記 3 件はいずれも push 前に機体内部で修正済み。
4. **D6 census 箱の縮小**: 当初 x 1..8, c 1..8, z 0..12 を定義したが S(8,8,12) 単点で
   engine の状態空間が成長し sandbox OOM（kill）したため、x 1..6, c 1..6, z 0..10 に
   縮小した。census の範囲は本 §3 の箱が正であり、型付き構成の D6 主張はこの箱内で
   engine 全一致を検証する。

## §5 次の未解決（open 登録・verdict 不消費）

- **O-PQG**: L の外向き子族 P/Q/G の法則化（OBS-LB の zp≥4 境界・OBS-SW の波の値は
  すべてこの族の値で決まる）。P={d^2,(d+1)^t}・Q={d−1,(d+1)^s}・G=(2^s) 対角族。
- **C-LD1/C-SX1 の全称化**: E 族は 2 変数 dp (c, R−z) 構造で閉じる見込みが強い（B は
  u−2/c−1、C は u 不変/xor）。Am の s=1 行の h=1 極限系列の法則化。
- 標準 11×11 空盤・二石 root・S2・class 1/2/4 は全て UNKNOWN のまま。
