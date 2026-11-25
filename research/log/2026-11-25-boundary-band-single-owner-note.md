# 単一オーナー宣言 K1311: 境界帯パッケージ — T-DB・L-SDB（全トークン多重度の境界行 collapse 全称確定・K0832 過渡帯頂行・予想B 回収・有限で止まらない）

- 日付: 2026-11-25
- lane: 高速レーン（短〜中時間・厳密結果）。本ノートは fast-lane の単一オーナー宣言
  （publish-then-execute: 本ノートが最初に出版され、機体・監査はその後従属）。
- 観測 HEAD: 探索着手時（前実行で tarball 取得）`6247d6a5`（Part DY batch-37 完了 log）。
  本実行冒頭の main 観測は `04c132fd`（Part EA kit 3/3・長期レーン・直交。着手以降の
  10 commit はすべて Part DZ/EA の 11×11 canonical cache 採用系列で items/log に
  knowledge 変更なし）。**push 直前に再度 main を取り直し、K1311 の空きを再確認する**
  （search_commits で 0 hits を直近確認済み・対抗宣言なし）。
- 位置づけ: K1308 Z-DIAG（ペア対角行 k=z）を「2 山面の境界行」と読み直し、
  **全多重度 n ≥ 2 の境界行 k = z+n−2** が公刊 Z-DIAG 3 分岐則 D に単一座標で崩壊することを
  全称確定する。n=2 インスタンスは公刊 Z-DIAG/T-DU′ そのもの（被包再証明）。n=3 インスタンスは
  K0832 3 トークン過渡帯の頂行 k=z+1 を全確定し、**K0832 予想 B（κ=0 スライス R=2x−1・j=2 族
  の値 2）を部分族として全称証明**する。n ≥ 4 境界行は新領域。together with 公刊 tail 系
  （k ≥ z+n−1 → H = S mod 2・K0832 Lemma P 系〔接続記録のみ・再主張しない〕）、
  n 山面の k 軸は「下帯 k ≤ z+n−3（open・O-BBL）/ 境界行（本項）/ tail（公刊系）」の
  3 層構造に整理される。
- 規約: verdict 不消費。標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は
  全時点 UNKNOWN のまま。engine は K1138 転写（sha pin 実装）であり、census は照合
  であって証明の代替ではない。

## 用語・記法（K1285/K1303/K1308/K1310 準拠）

残余ゲーム H(R; X; z)（K1138 再帰・値は mex・H(0;·)=0）。局面の選択肢（K1285 §2.0 規約）:

- **A手**（トークン w>1 を w−1 に圧縮・R→R−1・plane 不変・multiset のつくり直し込み）。
- **B手**（トークン 1 を除去・R→R−1・plane z→z+1・トークン数 n→n−1）。
- **C手**（z≥1 で子の値 1 XOR・R→R−1・plane z−1・k→k−1・multiset 不変）。

**座標**: S := ΣX・k := R − S。X は降順 X = (x1 ≥ x2 ≥ … ≥ xn ≥ 1) に正規化。
**過剰座標** E := x1 − Σ_{i≥2} x_i = 2x1 − S。範囲は E ≥ 2−n（下限は all-ones）。
**公刊 Z-DIAG 3 分岐則**（K1308・p ≥ 0 に対し）:
D(g, p) := [g odd]（g ≤ p）/ 2（g = p+1）/ [g even]（g ≥ p+2）。
g は標準合同式の偶奇（E ≤ 0・負値を含む; g=0 bed 値 0 は公刊 T-DU′ と整合）。
単一トークン閉形式 v(x, p, R) = single_token（K0832・キット engine_block.py 転写）。

## §1 主張（全称・量化は非有限・証明全文は §2）

### 定理 T-DB（境界行 collapse・全多重度）

∀ n ≥ 2, ∀ z ≥ 0, ∀ 降順 multiset X = (x1 ≥ x2 ≥ … ≥ xn ≥ 1):
境界行 k := z+n−2（≥ 0）において

  **H(S+k; X; z) = D(E, k)**,  E := 2x1 − S.

値は x2..xn の個別値に非依存（単一座標 E のみ）。値 2 は超対角 E = k+1 の直線上ちょうど。
インスタンス: n=2 は公刊 Z-DIAG（k=z）・床 g=0 は D(0,z)=0 = 公刊 T-DU′（被包）。
n=3 は境界行 k=z+1（K0832 過渡帯の頂行）。n ≥ 4 は新領域（census X2: n=4..7 で bad 0）。

### 補題 L-SDB（単一トークン境界行・K0832 閉形式から導出）

∀ x ≥ 1, ∀ z ≥ 1: **v(x, z, x+z−1) = D(x, z−1)**（単一トークンの境界行 k = z−1）。
T-DB の帰納 base（n=1）。導出は §2.1（公刊閉形式の 3 枝スライス）。

### 系（接続・被包）

- **C1（K0832 予想 B の全称証明〔部分族として〕）**: n=3 境界行で j := x−y−w−z = E−z。
  値 2 は j = 2（E = z+2 = k+1）上ちょうど。K0832 の κ=0 スライス R = 2x−1 ∧ j=2 族
  は本定理の E=z+2 境界セルと同一（帯条件 x < R < S+z+2 は R=S+z+1 で常に成立）。
  予想 A（j=0）・予想 C（j=1）は境界行の下（k=z−1, k=z）に生息し本項では**確定しない**
  （O-BBL 登録・open のまま）。
- **C2（n 山面 k 軸の 3 層フレーム）**: k ≥ z+n−1 → H = S mod 2（公刊 K0832 Lemma P 系:
  本項は接続記録と転写照合〔機体 D7〕のみで再主張しない）; k = z+n−2 → T-DB（本項）;
  k ≤ z+n−3 → 下帯（n=2 は公刊 K1303 帯域 + K1309 合同窓 + K1310 非合同窓で全確定済み・
  n ≥ 3 は open O-BBL）。n 山ごとに未確定なのは下帯のみ。
- **C3（all-ones 整合）**: 境界スライズの all-ones 値 D(2−n, k) は公刊 K0832 全 1 族
  閉形式 U の境界インスタンスと整合（機体 D10 が照合）。
- **C4（n=2 公刊被包の独立帰納）**: 本項の帰納構造（L-SDB base + typed mex・§2.2）は
  Z-DIAG/T-DU′ を独立に再証明する（ネストした単一帰納で n=2 は L-SDB base のみで閉じる）。

## §2 手証明全文

### §2.1 補題 L-SDB の導出（K0832 公刊閉形式の 3 枝スライス）

R := x+z−1 と置く（境界行 k = R−x = z−1 ⟹ z ≥ 1 が必要・ z ≥ 1 を仮定）。

- (i) z = x: R = 2x−1 は奇数かつ R ≤ 2x−1 → 閉形式は **2**。D(x, z−1) = D(x, x−1):
  g = x = p+1 → **2** ✓。
- (ii) 1 ≤ z ≤ x−1（⟺ x ≥ z+1）: m := q_odd(z)。R = x+z−1 ≥ 2z ≥ m+1 > m
  （x ≥ z+1）かつ R < x+z → 中間帯 → 値 (R+z)%2 = (x+2z−1)%2 = [x even]。
  D(x, z−1): g = x ≥ z+1 = p+2 → **[x even]** ✓。
- (iii) z ≥ x+1: m := q_odd(x) ≤ x < 2x ≤ x+z = R+1 → R > m（R = x+z−1 ≥ 2x > x ≥ m）→
  tail 枝 → 値 x%2 = [x odd]。D(x, z−1): p = z−1 ≥ x ⟹ g ≤ p → **[x odd]** ✓。

3 枝で全領域を被覆（z≥1・x≥1）。∎（機体 D1 が engine vs 申立 240 点、X3 が閉形式 vs
engine 160 点を照合。）k=0 の n=1 基地セル（z=1）も含む: D(x, 0)（x=1 は 2 =
single_token(1,1,1) ✓）。

### §2.2 T-DB の証明（typed mex・二重帰納）

**帰納構造**: 外側は n（n=1 は L-SDB・§2.1）、内側は n を固定した R についての強帰納。
**k=0 基地セルは typed 分析の外**で公刊により確定: (n=2, z=0, k=0) は公刊 Z-DIAG z=0 行
＋T-DU′ z=0（床 D(0,0)=0）。n ≥ 3 では k = z+n−2 = 0 は (z=0, n=2) しかないため
typed 分析は k ≥ 1 の全セルに適用される。

**子の型**（セル (z, X, R=S+k)・n ≥ 2・k ≥ 1・p := k）:

- **(A-a) unique-top A手**: x1 > x2 かつ x1 ≥ 2 → 子 (z, X′, R−1)。x1−1 ≥ x2 より
  max(X′) = x1−1 → E′ = E−1・k 不変。値 = **D(E−1, k)**（内側 IH）。
- **(A-b) tied-top / tail A手**: x1 == x2 ≥ 2（片方を圧縮）または tail heap xi ≥ 2 →
  max 不変 → E′ = E+1・k 不変。値 = **D(E+1, k)**（内側 IH）。
- **(B) B手**: xi = 1 を除去 → 子 (z+1, Y, R−1)・|Y| = n−1・k 不変
  （k_child = (z+1)+(n−1)−2 = k・境界 ✓）・E(Y) = E+1。値 = **D(E+1, k)**
  （n−1 = 1 は L-SDB: 子 = 単一トークン (x1) at plane z+1・L-SDB 値 D(x1, z) は
  n=2 では E = x1−1・k = z ゆえ D(E+1, k) と一致; n−1 ≥ 2 は外側 IH）。
- **(C) C手**: z ≥ 1 → 子 (z−1, X, R−1)・k_child = k−1 = (z−1)+n−2（境界 ✓）。
  選択肢値 = **1 XOR D(E, k−1)**（内側 IH・E 不変）。存在条件は k ≥ 1（budget R−1 ≥ S）で、
  n ≥ 2 ∧ z ≥ 1 のとき常に成立。

**存在補題**: (i) n ≥ 2 なら (A-b) or (B) が常に存在する（xn = 1 → B・xn ≥ 2 → (A-b)）から、
値 **D(E+1, k) の選択肢が常に存在**する。(ii) E ≥ 1 なら (A-a) が常に存在する:
E ≥ 1 ⟹ x1 = (S+E)/2 ≥ 1+(n−1) ≥ 2 かつ x1 == x2 なら E = 2x1−S ≤ 0 に矛盾し
unique top、x1 = 1 なら all-ones で E = 2−n ≤ 0 に矛盾。(iii) 逆に E ≤ 0（tied top・
all-ones・浅い unique）では (A-a) は在否が不定だが、下の区域分析で値が「存在すれば 1−c」
に落ちるため mex に影響しない。

**区域 mex 代数**（k ≥ 1・c := D(E, k)）:

- **R-I: E ≤ k−1** → c = [E odd]。(A-a)（在れば）: D(E−1, k) = [E−1 odd] = 1−c。
  (A-b/B): E+1 ≤ k → D(E+1, k) = [E+1 odd] = 1−c（**常に存在**）。
  (C): E ≤ k−1 → D(E, k−1) = [E odd] = c → 選択肢 1−c。
  opts ⊆ {1−c} かつ 1−c ∈ opts → **mex = c** ✓（all-ones: E = 2−n ≤ 0 ≤ k−1 は
  この区域に含まれ、B/C の値だけで同じく閉じる）。
- **R-II: E = k** → E ≥ 1 ゆえ (A-a) 存在・c = [k odd]。(A-a): D(k−1, k) = 1−c。
  (A-b/B): D(k+1, k) = **2**（超対角）・常に存在。(C)（在れば）: 1 XOR D(k, k−1) = 1^2 = 3。
  opts = {1−c, 2, (3)} → **mex = c** ✓。
- **R-III: E = k+1** → (A-a) 存在・c = 2。t := [k odd]。(A-a): D(k, k) = t。
  (A-b/B): D(k+2, k) = [k even] = 1−t・常に存在。(C): E ≥ (k−1)+2 →
  D(k+1, k−1) = [k+1 even] = t → 選択肢 1−t = 1^t。
  opts = {t, 1−t} = {0,1} → **mex = 2 = c** ✓。
- **R-IV: E = k+2** → (A-a) 存在・c = [k even]。(A-a): D(k+1, k) = **2**。
  (A-b/B): D(k+3, k) = [k odd] = 1−c・常に存在。(C): D(k+2, k−1) = [k even] = c → 1−c。
  opts = {2, 1−c} → **mex = c** ✓。
- **R-V: E ≥ k+3** → (A-a) 存在・c = [E even]。(A-a): D(E−1, k) = [E odd] = 1−c。
  (A-b/B): D(E+1, k) = [E odd] = 1−c・常に存在。(C): E ≥ k+2 → D(E, k−1) = [E even]
  → 1−c。opts = {1−c} → **mex = c** ✓。

全区域・全存在パターンで閉鎖。全選択肢子の budget は R−1 < R（(B) の n−1 子は
外側 IH で budget 無制限）ゆえ二重帰納は well-founded。∎

**証明の透明性に関する注記**: (A-a) の E′ = E−1 計算は unique top 条件 x1 > x2 が
圧縮後も max(X′) = x1−1 を保証する（x1−1 ≥ x2）から multiset 再ソートの影響を受けない。
tied top（x1 == x2）の圧縮は相手方 x2 が新しい max になり E′ = 2x1 − (S−1) = E+1。
(C) の存在条件は k ≥ 1 で n ≥ 2 の typed 領域では z ≥ 1 ⟺ k ≥ n−1 と同値だが、
z = 0 かつ k ≥ 1（n ≥ 3）のセルでも (C) 不在は R-I..R-V 全区域で harmless
（(C) 不在の opts は全域 {1−c} 側に寄与しない: R-I {1−c}・R-II {1−c, 2}・
R-III {t, 1−t}・R-IV {2, 1−c}・R-V {1−c} が (A-a)+(A-b/B) の常在のみで成立）。

## §3 宣言前探索（凍結・explore_db.py/.out・X1–X5）

- **X1** triples 境界行 k=z+1 全 (z,j) 値分布（z=0..6・S≤16・861 セル）:
  各 (z,j) 列は値一様（861/861）・値 2 は j=2 直線上のみ・位相は
  [(j+z) odd]（j≤1）/ [(j+z) even]（j≥3）= D(j+z, z+1) = D(E, k)。
- **X2** n=4..7 境界行 census（z≤6・heaps ≤ 8・S ≤ 16..13）: 910/910・742/742・
  441/441・210/210（bad 0）。
- **X3** n=1 L-SDB 160 点（engine vs D(x,z−1)・閉形式三者不一致 0）・n=2 境界
  963 点（pairs+beds・bad 0）・all-ones n=2..8 63 点（bad 0）。
- **X4** far stress（seed 1311・z=7..14・960 点 bad 0）・tail 行 k=z+n−1, z+n
  1,390 点（公刊系転写照合・bad 0）。
- **X5** typed mex 代数 597 点（n=2..4・申立表のみで子構成・mex==申立==engine）。

## §4 機体宣言（kit: research/experiments/boundary-band-20261125・13 ファイル）

- **verify_k1311.py** sha256 `4b5b81de90a8c45da69d36d1903ed543f40212c1394afb999c16d22ff1f20b9b`
  （19,093 B・埋込み engine block startup sha gate pin `bd5f22e4…`〔K1138/K1282..K1310
  chain と同一 bytes〕・不一致なら即時 abort）。
- **engine_block.py** `582c93c1…`（単体・K1282..K1310 kit chain と同一 bytes）。
- **explore_db.py** `5747cb9a…` / **explore_db.out** `6b48b840…`（X1–X5 凍結の正本）。
- **predry/dryrun1-4.out**（+.info）: 4 走とも byte-identical sha256
  `811d7ae3390ef43c94cc24f3ae5d77c32de179bc9336d468be49201997d44bdb`
  （約 2.2 秒/走・python 3.12）。
- **電池 12 種** counts `[240, 1628, 1353, 2303, 1659, 861, 1390, 1200, 747, 521, 7, 500]`
  総計 **12,409** 期待 overall_bad = 0:
  D1 L-SDB census（x≤20・z=1..12）240 / D2 n=2 境界アンカー（pairs+beds・z=0..10・
  a≤8・g≤20・S≤28）1,628 / D3 triples 境界 census（z=0..10・S≤16 全掃引）1,353 /
  D4 n=4..7 census（z≤6・heaps≤8）2,303 / D5 typed self-check（n=2..5・z≤6・
  heaps≤6・S≤15・申立+L-SDB 表のみで子構成・mex==申立==engine 三点一致）1,659 /
  D6 cross-engine+申立（canonical vs ordered vs D・n=2..4・z≤6）861 / D7 tail 行
  k=z+n−1, z+n（公刊系転写・n=2..4・z≤4）1,390 / D8 far stress（seed 1311/1312/1313・
  triples z7..14・quads z7..12・n=5..7 z7..9）1,200 / D9 K0832 予想B interface
  （triples z0..8・S≤14・値 2 ⇔ E=z+2 の両含意）747 / D10 all-ones n=2..14×z0..10・
  near-all-ones n=3..8・x2..8・z0..8 521 / D11 OBS-BBL 凍結表再現（triples k=z 行・
  z=1..7・naive D(E,z−1)/D(E,z) との不一致計数の 7 行照合）7 / D12 random multiset
  sweep（seed 1314・n=2..6・z=0..7・500 点）。
- **変異電池 13 種**（fail-closed・事前宣言・全て初走で一致）:
  `--tamper-engine` → rc=2（変異 sha `0ea47a80…` ≠ pin・stdout は mismatch 報告のみ）;
  `np1`〔D1〕228 / `np2`〔D2〕1,540 / `np3`〔D3〕1,297 / `np4`〔D4〕2,295 /
  `ty`〔D5 申立 flip〕1,659 / `ce`〔D6 申立 flip〕838 / `tl`〔D7 tail flip〕1,390 /
  `fs`〔D8 申立 flip〕1,199 / `kb`〔D9 2-局在反転〕747 / `ao`〔D10 申立 flip〕512 /
  `ob`〔D11 凍結表変異〕7 / `rs`〔D12 申立 flip〕490・すべて rc=1。
- **監査プロトコル**: ① fetch-back: 全ファイル size+sha256 byte 照合。
  ② 公式 4 走（fetch-back bytes から）: 同一 cwd×2〔PYTHONHASHSEED=random/1〕+
  隔離 tree/env -i×2〔99/7〕→ 全走 rc=0・stdout byte-identical（predry sha と一致確認）。
  ③ 変異電池 13 種 → 上表 bad count・rc で全 fail-closed 確認。
  ④ 成果物 output/audit_run1-4.out+.info・tamper レコード 13・detcheck.json
  （OFFICIAL-PASS 条件）・MANIFEST-sha256 出版 → fetch-back MANIFEST 全行照合。

## §4.5 主張の区別

- **全称定理（手証明 §2 + 実機照合）**: T-DB（n ≥ 2 全境界行）・L-SDB（n=1 境界行）。
  census 12,409 点は定理の実機照合であって証明の代替ではない。
- **接続記録（再主張しない）**: D7 tail 照合は公刊 K0832 Lemma P 系の転写。C1 の
  予想 B 回収は E=z+2 部分族に正確に限定。all-ones 整合（C3）は公刊 U 族との照合。
- **観測（法則主張なし）**: D11 OBS-BBL 凍結表は triples 下帯 k=z 行の実測分布の
  凍結であり、下帯を open のまま登録するための証人データ（§5 O-BBL）。
- D5 typed self-check は §2.2 の子構成・区域 mex 代数の機械点検（証明の構造検証であり
  証明の代替ではない）。

## §5 open 登録

- **O-BBL（n ≥ 3 の下帯）**: 境界行の下 k ≤ z+n−3 の一般法則は未確定。OBS-BBL 凍結表
  （triples k=z 行・z=1..7・80 セル/z）では naive D(E, z−1)/D(E, z) との不一致が
  (80,80,68)→(80,56,47)→(80,31,25)→(80,16,12)→(80,6,4)→(80,2,1)→(80,0,0) と
  z の増大で消える観測（S ≤ 15 の有限窓内でのみ正しい watershed 現象の候補として
  記録・法則は主張しない）。K0832 予想 A（j=0）・C（j=1）はこの帯に生息し open のまま。
- **O-DB2**: §2.2 の区域 mex の内側 2 行（E = k−1, k の (C) 値の遷移構造 3 = 1^2）
  が下帯の typed 化（B 手の n−1 子が境界行 z+1 に落ちる構造の逆読み）に使えるかは
  未着手。

## §6 honest 経緯

- 発見順: 前実行で K1310 出版後に K0832 過渡帯の未回収部分から境界行（頂行 k=z+1）を
  最初に探索。X1 の (z,j) 列一様性から単一過剰座標 E を同定し、公刊 K1308 Z-DIAG 3 分岐
  則 D(E, k) と突合。n=4..7 拡張（X2）で 2,303 点 bad 0 を確認後、typed mex 分析で
  全区域が閉じ、n についての二重帰納として全称証明に到達（本ノート §2 が正本）。
- 実装上の修正 2 件（宣言前・凍結正本に反映済み）: 初期探索スクリプトは
  combinations_with_replacement の昇順タプルに対し E を誤計測（X[0] を最大と誤認）して
  n=4..7 に偽の不一致 11+1 を出したが、降順正規化で解消（X2 全一致）。typed options の
  初期実装も同種の tied-top 誤検出があり同修正で解消（X5 全一致）。凍結した explore_db.py
  は修正後の正本である。
- tail 行 k ≥ z+n−1 の H = S mod 2 が K0832 Lemma P + κ=1 レジームの既刊系であることを
  確認し、本ノートは接続記録（C2・D7）に留めた。K0832 予想 B の回収は κ=0・j=2 部分族
  に正確に限定して記録した（予想 A/C は O-BBL として open のまま）。
