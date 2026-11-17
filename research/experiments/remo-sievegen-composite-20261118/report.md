# K0937: SIEVE構造の全称完結 — 不変量INV・合成数側の死亡定理SIEVE-COMPOSITE-GEN・双子法則の全称化（2026-11-18）

高速レーン。一様盤・ゼロリセット・K0859再帰のreduced game（K0928定理RED経由）。
LAD-GEN core（`ladder_gen` / `watch_dies` / `watchmap`）は出版済みK0934/K0935/K0936
検証器からverbatim copy、`play_full` はK0928 Lemma P位相規則（K0932/K0933/K0936
検証器と同一）。本レポートの新規寄与は (1) 監視距離の不変量 INV の発見と全称証明、
(2) 死亡合同式によるspf非依存の死亡判定、(3) t=1レジームへのWATCH-MAP拡張とその
限界の特定、(4) 合成数側の完全閉包 SIEVE-COMPOSITE-GEN、(5) 双子法則の mod 210
制限の除去。機械アンカー `sievegen_verify.py`（12チェック）と `audit_build.py`
（2回in-process実行一致・2回コールド実行でbyte同一）が全前提を検証する。

## 0. 記号と既知の部品

- reduced game: m人・初期保持2・初期pot V:1 / U:2・監視ラベル V:0 / U:m−1。
  N = 2m+s（V: s=1、U: s=3）。U(m)=m−1、V(m)=0 が監視生存値。
- stretch-w: potがwである極大連続フェーズ列。K0928: pot列は各stretchでw→w+1
  （collapse時 w+2、ただし本定理ではUのt=1死亡として吸収）、単調増加。
- F(w,h;n): 保持 [w]^(n−h)+[w+1]^h、ptr基準のcircle、監視距離 a = n − wpos。
- LAD-GEN（K0934・全称）: stretch-wの状態F(w,h;n)（h≤w）のフェーズ構造:
  t = n//(w+1)、r = n mod (w+1)、J = t (r≥h) / t−1 (r<h)、
  block j = 1..J は deal元位置 (j−1)(w+1)..j(w+1)−2・敗者 j(w+1)−1（保持w）・
  最終breakingフェーズ（deal w+1位置・敗者は保持w+1; r=h=0,t=1はcollapse、
  敗者0・保持w+2）。終状態census: r<h → F(w+1, h−1−r; n−t)、
  r≥h → F(w+1, h+w−r; n−t−1)。t=1でもcensusは成立（本項T1MAPで全窓検証）。
- WATCH-MAP（K0935・t≥2で出版）: 生存監視の次stretch距離
  a2 = a−r−1 (r<h, a≥r+2)、n2−r+a (r<h, a≤r)、w+a−1 (r=h=0)、
  a+w−r (r≥h, a≤r)、a+w−r−1 (r≥h, a≥r+2)。
- 監視死亡判定: 死亡 ⟺ 監視元位置pos = n−a ∈ 排出集合
  {j(w+1)−1: 1≤j≤J} ∪ {breaking敗者}（LAD-GEN (d)・t≥1で有効）。
  K0935 (e)の「死亡 ⟺ a = r+1」はt≥2・窓1≤a≤w+1で同値
  （唯一の例外 (h,r,t,a)=(0,0,2,w+1)はbreaking敗者と一致しhot死・phase t+1）。

## 1. 基礎状態と石保全（Lemma BASE / STONE）

V(m): stretch-1は単一pot-1フェーズ（pot 1 < 人数）。ラベル0が+1を受け保持3、
ラベル1が敗者（保持2・除去）、pot=2。よってstretch-2開始状態はF(2,1;m−1)
（ptr基準circle [2,...,2,3]、監視ラベル0は末尾、距離a=1）。
U(m): stretch-2は第1フェーズから始まる。開始状態はF(2,0;m)（全保持2、
監視ラベルm−1は距離a=1）。

**T恒等式**: stretch-w開始状態F(w,h;n)の石数 T = w·n + h + w（保持総和+pot）は
stretchごとに不変（censusで pot: w→w+1、hの再編、n減少が正確に相殺;
K0934 census検証済み、本項INVGENが全stretch entryで T ≡ T0 を機械確認）。
基礎値: **V: T0 = 2m+1 = N、U: T0 = 2m+2 = N−1**。
（直観: Nは「1個の石がpotに入る前の総数」; Uは初期pot 2のうち1個が
第1フェーズで保持側に移る前の状態を基準に取るためT=N−1。）

## 2. 不変量 INV（本項の中心的発見）

**定理INV-TRACK**. 各側・各mについて、監視が生存する限りの**すべての**
stretch-w開始状態（w ≥ 2、t ≥ 1、ladder regime）はF(w,h;n)で表され

- V: **a = h**（従って h ≥ 1、a ≤ w…h≤w）、
- U: **a = h + 1**（従って h ≤ w−1（w≥3）、a ≤ w）

を満たす。t=0のendgame entry（§5）でもこの関係は保たれる（EXIT時点の値で）。

**証明**. 帰納法。基礎: V: F(2,1;m−1) で a=1=h ✓、U: F(2,0;m) で a=1=h+1 ✓。
帰納段: stretch-w開始状態がF(w,h;n)・INVを満たし、監視が生存するとする。
WATCH-MAPの事例別計算（t≥2は出版、t=1は§3で拡張）:

- r < h（監視a=h/h+1 ≥ r+2、すなわち「front式」a2=a−r−1のみ発生）:
  V: a2 = h−r−1 = h2 ✓（h2 = h−1−r）。U: a2 = h−r = h2+1 ✓。
  （a ≤ r のfront逆ケースは INV で a = h > r / a = h+1 > h > r となり発生しない。）
- r ≥ h（監視a=h/h+1 ≤ r、すなわち「back式」a2=a+w−rのみ発生）:
  V: a2 = h+w−r = h2 ✓（h2 = h+w−r）。U: a2 = h+1+w−r = h2+1 ✓。
  （a > r のback逆ケースは V: h > r ≥ h、U: r = h（死亡ケース、生存では
  r ≥ h+1 = a ⟹ a ≤ r）で発生しない。）
- r = h = 0, t ≥ 2（Vはh≥1で不成立、Uは h=0 ⟹ a=1 = r+1 で死亡）: 生存なし。

よって次stretch entryでも INV。∎

**注意（危険ケースの排除）**: INV条件下では「監視がbreaking敗者と一致して
a ≠ r+1で死亡する」配置は代数的に不可能:
r<h breaking敗者位置 n−r−1 と監視位置 n−a の一致は a=r+1（＝(e)そのもの）、
r≥h 敗者位置 w−r との一致は a = h+... V: 2r = h−1（r≥hと矛盾）、
U: 2r = h（r ≥ h ⟹ r=0=h: collapseに帰着、下記）。collapse (t,r,h)=(1,0,0):
V: h≥1で不成立。U: a=1=r+1 でblock-1敗者として死亡（§4）。collapseの敗者0
（保持w+2）はa = n = w+1 を要求し、INV-U（a=h+1=1）では w=0 が必要で不可能。
例外 (0,0,2,w+1) は U: a=1 ≠ w+1（w≥2）で不成立、V: h≥1で不成立。

## 3. t=1レジームのWATCH-MAP拡張（Lemma T1-MAP）

K0935のwatchmapは n ≥ 2w+2（t≥2）に制限されていた。t=1（w+1 ≤ n ≤ 2w+1）では:

**censusはt=1でもそのまま成立**（T1MAP: 全窓6,075グリッド・0失敗）。
**a2公式もINV関連距離（a∈{h,h+1}）ではt≥2と同一**（T1MAP: 1,075グリッド・
0失敗）。紙上証明（位置計算）:

- t=1, r < h（J=0、単一breakingフェーズ、deal 0..w−1、敗者w・保持w+1）:
  生残位置は 0..w−1 と w+1..w+r。end circle（ptr=敗者スロット基準）の順は
  [w+1..w+r, 0..w−1]。V監視 pos = w+1+r−h（先頭hot、h≥r+2で生存時 w−1以下）
  は第2 segment: end-index = r+pos、a2 = n2−index = (w+r)−(r+pos) = w−pos
  = h−r−1 = a−r−1 ✓。U監視 pos = w+r−h（h≥r+1 で ≤ w−1）も同様に
  a2 = h−r = a−r−1 ✓。
- t=1, r ≥ h（J=1、block-1 deal 0..w−1・敗者w保持w、breaking deal
  {w+1..w+r}∪{0..w−r−1}・敗者w−r保持w+1）: 生残位置 0..w+r から {w, w−r}を
  除去。end circle（breaking敗者スロット基準）: [w−r+1..w−1, w+1..w+r,
  0..w−r−1]の循環（長さn2 = w+r−1）。監視 pos = w+1+r−a: a≤r（INV）より
  pos ∈ [w+1..w+r]。第2 segment内のindexは2r−a−1 なので
  a2 = n2−index = w−r+a = h+w−r (V) / h+1+w−r (U) = h2 / h2+1 ✓。
  （census順序: hot元位置はw+1..w+rの末尾h個なのでw+2保持帯が
  circle末尾に連続する。）

**重要な限界（観測として記録）**: t=1では非INV窓ケースのa2は崩れる
（noninv_t1_map_deviations = 270件。理由: (i) r<h ∧ a≤r のfront式
a2 = n2−r+a はt=1では幾何が変化、(ii) r≥h ∧ a≥r+2 のback式 a2 = a+w−r−1 は
end circleサイズn2 = w+r−1 を超え得る）。また**t=1ではK0935 (e)の「死亡 ⟺
a=r+1」は一般には偽**（反例 (w,h,n,a)=(5,0,8,5): 監視pos=3 = breaking敗者
w−r でphase 2・保持w+1のhot死、a=r+1=3ではない）。ただしINV条件下では
§2の危険ケース排除により t=1でも「死亡 ⟺ a=r+1 ⟺ V: r=h−1 / U: r=h」が
成立する。よって本項の死亡判定は(e)ではなく**排出集合判定（位置計算）**
`death_fast` を用い、t≥1全域でengineと照合済み（DEATHFAST 5,115件・
T1MAP 6,150件・0失敗）。

## 4. 死亡合同式と合成数側の閉包

**定理（死亡合同式）**. INV条件下（t≥1の生存stretchすべてで）、stretch-wで
監視が死ぬ ⟺ a = r+1 ⟺ **(w+1) | N**。
証明: T ≡ −n+h−1 (mod w+1)（w ≡ −1）より n ≡ h−1−T。
死亡 ⟺ n ≡ a−1 (mod w+1)。両者より T ≡ h−a (mod w+1)。
V: T=N, a=h ⟺ N ≡ 0。U: T=N−1, a=h+1 ⟺ N ≡ 0。∎

**補題REGIME**. N合成（spf p）なら、stretch 2..p−1 のすべてで t ≥ 1
（ladder regime）かつゲームは終了しない。
証明: stretch-w entry（w ≤ p−1）で n ≤ w と仮定。T = wn+h+w:
V: T ≤ w²+2w ≤ (p−1)²+2(p−1) = p²−1 < p² ≤ T（N ≥ p²）。矛盾。
U: w ≥ 3 の entry では h ≤ w−2（遷移式から: r<h なら h2 = h−r−1 ≤ h−1 ≤
w'−1、r≥h なら a2 = h+1+w'−r ≤ w'（生存Uは r ≥ h+1 = a）より
h2 = a2−1 ≤ w'−1; entry の w = w'+1 に対し h = h2 ≤ w−2）。
よって T ≤ w²+(w−2)+w = w²+2w−2 ≤ (p−1)²+2(p−1)−2 = p²−3 < p²−1 ≤ T。矛盾。stretch-2 (w=2): n = m ≥ 3 = w+1（N=2m+3 ≥ 9 合成 ⟹ m ≥ 3）。
またゲーム終了（生残1人）は n2=1 を要求するが、n2=1 となるのは
(w,t,r)=(2,1,≥h) の場合のみ（t≥2では n ≤ 3 < w+1 となり矛盾; t=1, w≥3では
n2 = n−1−[r≥h] ≥ w−1 ≥ 2）、そのとき T ≤ 10、N ≤ 11 で合成は N=9 のみだが
9 = 3² は死亡合同式によりstretch-2で死亡済み。∎

**定理SIEVE-COMPOSITE-GEN（全称）**. N = 2m+s が合成数なら、監視は
**stretch spf(N)−1 で死亡**する。詳細:
- V: breaking敗者としての**hot死**（r = h−1）、保持 **spf(N)**、
  死亡フェーズ = t = n//(w+1) = そのstretchの最終フェーズ。
- U: block-t敗者としての**cold死**（r = h、t=1 かつ r=0 すなわち N=(w+1)² の
  collapse stretchでもblock-1として、保持w）、保持 **spf(N)−1**、
  死亡フェーズ = t（run長 t+1 の最終phaseの1つ前）。
- 監視はstretch 2..spf(N)−2では一切死亡しない（合同式: (w+1) | N は
  w+1 < spf(N) で不可能; w+1 > spf(N) は到達前に死亡）。

証明: REGIME + INV帰納で stretch p−1 のentry は F(p−1, h; n) with a=h/h+1。
合同式: (p−1)+1 = p | N ✓ 死亡。保持・種別: 死亡は r = h−1 (V: breaking,
保持w+1 = p) / r = h (U: block, 保持w = p−1)。t=1の場合も§3で同一結論。
∎

**系TWIN-COMP-GEN（全称）**. K0928 RED（P(2m+1) = 1+2V(m)、
P(2m+2) = 3+2U(m)）と合わせて:
- すべての**奇数合成 C ≥ 9**: P(C) ≠ 1。
- すべての**偶数 C ≥ 2 かつ C+1 合成（≥9）**: P(C) ≠ C−1。
（K0936のmod 210類制限を除去。類内の素数ピン {3,5,7}/{2,4,6} は
P(3)=P(5)=P(7)=1・P(2)=1・P(4)=3・P(6)=5 の既知ピンと組み合わせると
57+57類は即座に全類へ拡張される。）有限側: コミットP表 C ≤ 8000 で
2,993+2,993合成インスタンス・**0違反**（TWINCOMP）。

## 5. 素数側: 残るOPENの正確な特定

**定理（素数側のladder部分）**. N が素数なら、監視は**すべての t ≥ 1 stretch
を生存する**。証明: 死亡 ⟺ (w+1)|N だが、t ≥ 1 の stretch では
T = wn+h+w ≥ (w+1)(w+1) > N > w+1（w ≥ 2 で N ≤ T+1 かつ... 正確には:
(w+1)|N ⟹ w+1 = N（N素数）⟹ w = N−1 だが、その stretch の n ≥ w+1 = N は
T ≥ w·n > N で矛盾）。
（機械: INVGENで67,717件の素数ゲームすべてendgame exit・0死亡。）

**予想SIEVE-PRIME（OPEN）**. N 素数なら監視は**t=0 endgame でも生存**
（= survivor）。これは素数側の**唯一の残るギャップ**である:
素数ゲームは必ずt=0 endgame（n ≤ w の regime）に入る（n は単調減少で
n ≥ w+1 ⟺ t ≥ 1）ため、ladder理論の外のendgame解析が必要。
機械検証: m ≤ 2,600 両側（N ≤ 5,203、素数~680個×両側）で新鮮engineが
**death なし・survivor == 監視**を全件確認（TRK/SIEVEOBSGEN・0失敗）。
素数側の観測（P表: 素数C→P(C)=1・C+1素数→P(C)=C−1、1,006+1,006件・0違反）も
この予想と整合。

## 6. 機械的証拠（sievegen_verify.py・audit_build.py）

全12チェック合格・2回in-process実行一致・2回コールド実行でbyte同一
（`output/sievegen_audit.json`、
file sha256 5281e92e221ffd589b56dc712e2ad76308d12c51c792496d2216ee3657c761d2）:

| チェック | 規模 | 結果 |
|---|---|---|
| PIN | コミット表sha256・P(1..40) | ✓ |
| REDRECON | m ≤ 3,999・7,998比較 | 0不一致 |
| T1MAP | t=1全窓6,075 + INV関連1,075 + collapse 75 | 0失敗（非INV t=1 a2偏差270件は観測記録） |
| T2REG | t≥2 watchmap_ext==出版watchmap 3,258 | 0失敗 |
| DEATHFAST | death_fast==LAD-GEN elim意味 5,115 | 0失敗 |
| INVGEN | **m ≤ 200,000両側・400,000ゲーム・36,818,347 stretch entry** | INV・T恒等式・合成死亡則 0失敗（死亡332,283・endgame 67,717・最大死亡stretch **630**（spf=631, 631²=398,161）・最大spf 631） |
| FRESHPIN | m ≤ 2,600新鮮survivor==コミット表 5,200 | 0不一致 |
| CANON | tracker全stretch entry==engine（t=1含む）**86,615** | 0失敗 |
| TRK | 死亡・保持・フェーズまで照合 5,200 | 0失敗 |
| SIEVEOBSGEN | engine版spf則 m ≤ 2,600（合成3,819ゲーム） | 0失敗 |
| SV7REG | K0936回帰: domain 684対・stretch-5無死・stretch-6 ⟺ 7\|N | 0失敗 |
| TWINCOMP | P表C ≤ 8000: 合成2,993+2,993 | 0違反 |

拡大比較: K0936の機械範囲は m ≤ 700・stretch ≤ 6 だった。本項は
トラッカー法則を m ≤ 200,000（N ≤ 400,003）・死亡stretch ≤ 630 まで、
engineアンカーを m ≤ 2,600（N ≤ 5,203・死亡stretch ≤ 70・t=1 stretchを含む全
86,615 entry）まで拡張した。全称性は紙上証明（§1–§4）による。

## 7. 範囲と限界

- 一様盤・ゼロリセット・K0859再帰（K0928定理RED経由）のみ。非一様盤・
  11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class1/2/4は
  一切言及しない（**UNKNOWN不変**）。
- 素数側は**予想**（§5）。合成側のみが全称定理。P(C)=1 ⟹ C素数・
  P(C)=C−1 ⟹ C+1素数は全称だが、逆方向（C素数 ⟹ P(C)=1）は
  SIEVE-PRIME予想に依存しOPEN。
- t=1の非INV窓ケースのa2公式は**主張しない**（270件の偏差を観測として
  記録）。定理が使うのはINV関連距離のみで、これは1,075グリッド全検証+紙上証明。
- t=1ではK0935 (e)のa=r+1判定は一般に偽（§3の反例）。t≥2では出版済みの通り
  有効。本項の死亡判定は排出集合判定であって(e)に依存しない。
- K0936の `death_info` はcollapse stretchでのblock-1死亡に対し held=w+2 を
  返す（engine真理はheld=w）。K0936の published チェックは track() が
  w ≥ 6 で打ち切るためこのケースに到達せず、結果に影響しない。
  本項の `death_fast` は engine真理（held=w）に合わせ、U(23)/U(83) 型の
  collapse死亡を正しく扱う（TRKでengine照合済み）。
- `uv run check/build`・unittestは本環境にcloneとuvがないため未実施
  （前項の高速レーン項目と同じ扱い）。generated/とroot READMEは未編集。
