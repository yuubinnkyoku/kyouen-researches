# remo-foldgen-20261118 — FOLD-GEN・rung-2 fold構造・U の mod-5 力学的篩（K0951）

一様盤。K0941 定理C/Dの σ 再帰（pinned composite_core.py）と K0945 の
FAST/FOLD・センサスの上で、次を確立する。

1. **FOLD-GEN**：一般 bump-fold フレーム (1,c,k,kTop) の評価を閉形式三分法で O(1) 化
   （K0945 FOLD定理 = c=4 特殊例の一般化）。
2. **RUNG-1/2・EXCL-U-MOD5・U-RUNG2-FINAL**：K0945 が観察として残した
   「ONE-CHAR 条件の bump 展開 a=0 ⟺ σ_E(4;3u−4,3)=3u−3」と「pot 4,5,… への
   連分数様再帰」を厳密化・全称化し、U={u:σ_E(3;0,3u)=1} の fold 力学的
   mod-5 篩を導く。
3. **U センサスの 2×10⁵ 拡張**と、K0945 ONE-CHAR（証明済み）+ K0950 PAIR-3
   （証明済み）から予言される「U = 素数対集合 ∪ {2}」の独立掃引による両方向検証。

位置づけ（三角形特徴付け）：
U = ones 軌跡 {u:σ_Z(3,4u)=1}（K0945 ONE-CHAR）
  = {u:4u+1,6u+1 がともに素数} ∪ {2}（K0950 PAIR-3）
  = mod-5 残差篩（本項目 U-RUNG2-FINAL）。
3つの特徴付けが同じ集合を指すことは、3定理の全称証明から従い、
有限域での直接相互検証（下記）でも 0 不一致である。

## 主張

### 定理 FOLD-GEN（一般 bump-fold の閉形式三分法・全称）

c≥2、a≤b、入口値 x=σ_{a−1} に対する fold 再帰 σ_ℓ=(σ_{ℓ−1}+c) mod ℓ（ℓ∈[a,b]）を
D=x+c(b−a+1) とおいて評価する。**境界 a≥c−1 かつ x≤a−2** のとき:

- (i) D≤b−1 のとき σ_b=D（全面静寂）。
- (ii) b≤D≤b+c−2 のとき σ_b=D−b（レベル b ちょうど 1 回の wrap）。
- (iii) D≥b+c−1 のときカスケード:
  L₀=max(a,⌈(cb−D)/(c−1)⌉)、v₀=D+(c−1)L₀−cb∈[0,c−2] とし、
  レベル L（値 v）からの各 bite で
  m=max(L+1,⌈(cL−v)/(c−1)⌉)、v←v+(c−1)m−cL、L←m と更新し、
  m>b となった時点で σ_b=v+c(b−L)。

**証明**。巻き戻し無しの値はレベル ℓ で x+c(ℓ−a+1) だから、静寂条件は
f(ℓ)=ℓ−x−c(ℓ−a+1)≥1 と書ける。c≥2 より f は ℓ について真に単調減少で、
束縛条件は ℓ=b にある。(i) は f(b)=b−D≥1 ⟹ 全レベル静寂。(ii) は
f(b)=b−D∈[−c+2,0]（b で wrap）かつ f(b−1)=f(b)+(c−1)≥1（直前は静寂）であり、
ℓ=a のときの「直前が静寂」は境界 x≤a−2 そのもの。(iii) 最初の bite レベルは
L₀=min{ℓ∈[a,b]:f(ℓ)≤0}=max(a,⌈(ca−c−x)/(c−1)⌉)=max(a,⌈(cb−D)/(c−1)⌉)
（最後の等号は cb−D=ca−c−x）。L₀−1 が静寂なので bite 直前の値は
u≤(L₀−1)+c−1=L₀+c−2、bite で u≥L₀ より v₀=u−L₀∈[0,c−2]。
単一 wrap 条件 u<2L₀ は L₀≥c−1（境界）から u≤L₀+c−2<2L₀ として自動。
以後の各 bite も同型（レベルは真に増加、値は [0,c−2] に留まる）。∎

**正確性境界は鋭い**：反例 c=5,a=2,b=2,x=0（境界外: a<c−1）は直接計算 σ=1、
三分法は 3 を返す。foldGenChecked は境界外で foldDirect に fallback する
実装上の安全弁。実 chain（decomposeE の出力フレーム）では境界は常に充足し
（entry σ≤k−2=a−2、bump 後 k≥c−1）、FASTEQ 有限検証も 0 不一致。

### 補題 RUNG-1（U-RUNG2-FOLD・全称）

u≥2: σ_E(3;0,3u)=1 ⟺ σ_E(4;3u−4,3)=3u−3。

**証明**。E(3;0,3u) の第 1 フレームは plain level k=3u・addend 4 で、
状態は E(4;3u−4,3) に移る。ゆえ σ_E(3;0,3u)=(4+σ′) mod 3u、
σ′=σ_E(4;3u−4,3)∈[0,3u−2]。（4+σ′) mod 3u=1 ⟺ 4+σ′∈{1,3u+1} ⟺ σ′=3u−3
（σ′=−3 は範囲外）。∎（K0945 ONE-CHAR の a=0 場合の bump 展開の厳密化）

### 定理 RUNG-2 構造（全称・u≥3）

s=⌊(3u−4)/5⌋、a′=(3u−4) mod 5 とおくと、decomposeE(4,3u−4,3) の
最初のフレームは bump-fold (1,5,k₁,3u−1)、k₁=4s+a′+3 であり、bump 後の
状態は E(5;4s+2a′−2,4−a′)（k=k₁−1）、fold 区間 [k₁,3u−1]（長さ s+1）、
入口値 σ₅=σ_E(5;4s+2a′−2,4−a′) である。

**証明**。k=3u−1、P=4<k、P<a=3u−4（u≥3）より bump。skip 量
t=⌈(3u−8)/5⌉ は 3u−8=5s+a′−4、a′−4∈[−4,0] より t=s（cap k−P=3u−5、
k−1=3u−2 には到達しない）。skip 後 a=a′、b=3+4s、k=3u−1−s=k₁、
P=4<k₁ より (1,5,k₁,3u−1) を push。post-transform で
na=b+2a−P−1=4s+2a′−2、nb=P−a=4−a′、P=5、k=k₁−1。∎

### 定理 U-RUNG2-FINAL と EXCL-U-MOD5（全称・u≥2）

r=u mod 5、j=⌊u/5⌋ とおく。u∈U ⟺
r∈{0,2,3} かつ次の残差方程式（r↔a′ 対応: 0→1, 2→2, 3→0）:

- r=0: σ_E(5;12j−4,3)=12j−3
- r=2: σ_E(5;12j+2,2)=12j+3
- r=3: σ_E(5;12j+2,4)=12j+3

（u=1 は別途 u∈U: K0945 より σ_Z(3,4)=1。）

**証明**。目標は σ_E(4;3u−4,3)=3u−3=5s+a′+1（RUNG-1）。RUNG-2 構造と
FOLD-GEN（境界は自動充足: k₁≥7≥c−1、σ₅≤k₁−2）により
σ_E(4;3u−4,3)=foldGen(5,k₁,3u−1,σ₅)。D=σ₅+5(s+1)、b=3u−1=5s+a′+3 で
三分法を適用する。

(i) D≤b−1 ⟹ 出力 D ⟹ σ₅=a′−4。a′≤3 なら σ₅<0 で不能。a′=4（r=1）は
σ₅=0、すなわち σ_E(5;12j+2,0)=0 が必要だが、K0948 U0-CLASSIFY により
σ_E(P;n,0)=0 ⟺ n+1 素数 ∧ spf(P)≥n+1 であり、n+1=12j+3=3(4j+1) は
j≥1 で合成。j=0 は u=1（範囲外、実際 u=1∈U として例外成立）。

(ii) b≤D≤b+3 ⟹ 出力 D−b ⟹ σ₅∈[a′−2,a′+1] かつ目標から σ₅=5s+2a′−1。
5s+2a′−1≤a′+1 より 5s+a′≤2 ⟹ s=0,a′≤2 ⟹ 3u−4∈{0,1,2} ⟹ u=2 のみ。
u=2 は σ_E(5;2,2)=3 で実際成立（r=2, j=0 方程式）。

(iii) D≥b+4（カスケード）。L₀>k₁ なら出力≤3+5(b−k₁−1)=5s−2<5s+a′+1 で
目標に届かないから L₀=k₁ 必須。このとき出力=v₀+5(b−k₁)=v₀+5s、
v₀=σ₅−4s−a′+2。目標と比較して σ₅=4s+2a′−1、v₀=a′+1∈[0,3] より
a′∈{0,1,2}（r∈{3,0,2}）。a′=3（r=4）は v₀=4、a′=4（r=1）は v₀=5 で
v₀∈[0,c−2]=[0,3]（FOLD-GEN の定理的保証）に反し不能。第 2 bite は
m=max(k₁+1,⌈(5k₁−v₀)/4⌉)≥5s+a′+4>b 常に、ゆえ単 bite at k₁。

r の場合分けを整理すると EXCL-U-MOD5: r=4 は全ケース不能、r=1 は
(i) のみで u=1（K0948 により u≥6 不能、u=1 は例外として成立）、
r∈{0,2,3} は (iii)（u=2 は (ii)）で上の 3 方程式に帰着。∎

### 系 TERMINAL-BITE（全称・u∈U, u≥3）

u∈U、u≥3 なら rung-2 entry fold は単 bite at k₁（l0IsA）である。

**証明**。上の FINAL 証明の (iii) で、r∈{0,2,3} の u≥3 はすべて
L₀=k₁・単 bite のケースに当たる。（u=2 は (ii)、u=1 は範囲外。）∎

## 機械的証拠（foldgen_audit.json / 純JS）

| バッテリー | 規模 | 結果 |
|---|---|---|
| foldgen_grid（FOLD-GEN vs 直接fold、境界外はfallback） | 428,220 evals（closed 423,096 / fallback 5,124） | 不一致 0 |
| lcg_random（xorshift32 seed 12345） | 20,000 | 不一致 0 |
| fasteq（sigmaEFast vs sigmaENaive 実chain） | E状態 15,104 / U-rung 1,999 / σ_Z 3,156 / entry 400 | 不一致 0 |
| u_rung2_fold_identity（RUNG-1） | u∈[2,2000] 1,999 | 不一致 0 |
| segment_structure（RUNG-2） | u∈[3,2000] 1,998 | 不一致 0 |
| final_iff_u20000（FINAL ⟺ σ_E(3;0,3u)=1） | u∈[2,20000] 19,999（both 951、u mod5 内訳 [316,0,316,319,0]） | 不一致 0 |
| terminal_bite_u20000（TERMINAL-BITE） | U∩[3,20000] 950 件 | 違反 0（全部単 bite・l0IsA） |
| ones-identity（ONE-CHAR a=0） | u∈[1,2000] | 不一致 0（both 149） |
| ones-sample（(100k,200k] ランダム150点） | seed 12345 | 不一致 0 |
| excl_transfer（r∈{1,4} 排除） | u∈[2,20000] 7,999 点 | 違反 0 |
| final_iff_pair3（FINAL ⟺ K0950 PAIR-3） | u∈[2,20000] | 不一致 0 |
| census_cross_pair3（掃引 vs 素数篩、(100k,200k]） | 2,873 vs 2,873 | 完全一致・σ_Z スポット違反 0 |

出版ドメイン（deep_census.json、sha ピン一致）でも両方向 0 違反:
PAIR-3 3,658 件両方向、rhsOk 3,657 点、σ_Z スポット 3,658 点、
終端 bite 3,656 点（u≥3）全部単 bite・l0IsA、ABCD 分割リスト sha 4 本一致。

**環境注記**：本セッションは bash/Node 実行環境が利用不能であったため、
上記は CommonJS スクリプト（foldgen_core.js / census_extend.js /
foldgen_verify.js）の純JSサンドボックス転写実行による。sha256Hex は
出版ピン（空列・"hello world"）で検証した純JS実装。クロスラン再現性は
チャンクリスト sha ピン（E/F/G/H 4本）が保証する。uv による
check/build・unittest は未実施（歴代 remo 項目と同じ扱い）。

## センサス 2×10⁵ 拡張（fast_census.json）

- U(1..200000) = 6,531 件（出版 3,658 + 新規 2,873）、mod5 全体ヒストグラム
  [2143,1,2216,2171,0]（r≡1 は u=1 のみ、r≡4 は 0、EXCL-U-MOD5 と整合）。
- バケット (100000,200000]: 2,873（密度 0.02873、直近バケット 0.0316 から
  継続的に緩やかに減少。K0950 の 1/ln² 説明と整合。**観察としてのみ記録**）。
- チャンク E/F/G/H（各 25k、掃引 predicate σ_E(3;0,3u)=1）:
  742/759/709/663 件、rhs違反 0・終端 bite 異常 0・リスト sha ピン一致。
- H チャンクリストはセッション転写で 1 要素の誤植（183338: U 外・素数対なし）
  を検出し、素数対集合との対称差から 184338 を復元、修正後 sha が
  チャンクピン 3c431924… と byte 一致したことを確認して出版した
  （foldgen_audit.json > cross_batteries > h_list_transcription_recovery）。

## 観察

- **r=0 族の自己相似（rung-3）**：r=0 方程式 σ_E(5;12j−4,3)=12j−3 は
  rung-2 の目標 σ_E(4;3u−4,3)=3u−3 と M:4→5、u→4j の同形置換で一致する。
  つまり rung-3 篩（decomposeE(5,12j−4,3) の bump 構造 → rung-4 方程式）が
  同じ手法で立ち、一般 M への rung 篩の帰納的構成が次課題となる。
  K0950 K0-FAMILY・K0949 relay-prime-m と接続する可能性がある。
- **σ_E 掃引センサスの役割終了**：u>2×10⁵ の U の外延は K0950 PAIR-3 の
  素数対掃引（Eratosthenes + 2 回素数判定）が計算量的に優位であり、
  σ_E 掃引によるセンサス拡張は本項目で完成・役割終了とする。

## 範囲と限界

- 一様盤（uniform board）のみの結果であり、11×11 等の有限盤への言及はしない。
- FOLD-GEN の境界は全称証明済みだが、実 chain 上の境界充足の確認は
  FASTEQ による有限検証（0 不一致）である。一般用途では foldGenChecked を
  用いる。
- 密度の減少傾向は観察であり、全称主張ではない。
- uv check/build・unittest 未実施（環境制約、上記注記）。
  generated/ とルート README の本項目分は未編集。
- 機械的証拠は有限域の検証であり、全称定理の本体は紙上証明である
  （FOLD-GEN・RUNG-1・RUNG-2・U-RUNG2-FINAL・EXCL-U-MOD5・TERMINAL-BITE）。
