# K0961: SQUEEZE構造 — TWO-ZONE・EFFECTIVE-WINDOW・SQUEEZE-3・CHAR-3・K4-CAP — 2026-11-18

高速レーン（remo系・σ_Z算術構造）。K0960のDEEP-CAP/PAIR-MIN/K3-Aを精密化し、
(1) 紙上全称証明7件（TWO-ZONE・CO-FACTOR・EFFECTIVE-WINDOW・SQUEEZE-3・CHAR-3・K4-A・K4-CAP）、
(2) 出版センサス全10,886行（M≤2000・全t）への24述語全数機械検証（違反0）、
(3) prime-Y walk 34素数・composite-Y walk 33素数によるCHAR-3双方向錨・phantom観測、
を1回の実行で確定した。記法はK0956/K0958/K0960と同一（M素数・main regime
K=(M+1)t+κ・0≤κ≤M−2・(t,κ)≠(1,0)・Y=K+1・k₀=Mt+κ−1・N=MY−1・窓=[M,k₀]・
a=v₂(N)・kodd=Ω(N/2^a)・p₁≤…昇順は重複込み）。中核恒等式は
**N = (M+1)k₀+2M−κ**（K0956 HIT-GAP。2M−κ ≥ 2 > 0 が常に効く）。

対象は「smoothヒット」= Nが(M−1)-smoothかつ窓空（t≥2ではHIT-ARITHでσ_Z=1・
[Y ok]はYSQRとK0958 S3'で自動）。branch型ヒット・F(M)には適用しない（K0960不変）。

## 1. 命題（全称・紙上証明）

- **T1 TWO-ZONE（t≥2・全smoothヒット）**: Nの奇約数qは「2^a·q ≤ M−1」または
  「q > k₀」のどちらか一方に限られる（中間帯禁止）。
  証明: qは約数なので窓を跨がない: q > k₀ か q ≤ M−1。q ≤ M−1 のとき
  i₀ = min{i≥0 : 2^i q ≥ M}（存在・i₀≥1）とすると 2^i q (i≤a) はすべて約数。
  i₀ ≤ a なら M ≤ 2^{i₀}q ≤ 2q ≤ 2M−2 ≤ k₀（t≥2）で窓内約数が生じ矛盾。
  ゆえ i₀ > a、すなわち 2^a q ≤ M−1。∎
  （奇素数pはsmooth性から必ずp ≤ M−1側に入りK0960 ODDCAPを回収。複奇約数では
  zone 2（q > k₀）が実在する: M=1997, t=121 の 337·719 = 242,303 > k₀ = 241,816。
  これがODDCAPの「奇約数版への一般化」であり、K0960梯子論法と同構造。）
- **L2 CO-FACTOR（regime恒等式・t≥1・窓空不要）**: Nの約数dで d ≤ M−1 のものは
  N/d > (M+1)k₀/(M−1) =: X̄。
  証明: N = (M+1)k₀+2M−κ > (M+1)k₀ ゆえ
  N/d ≥ N/(M−1) = X̄ + (2M−κ)/(M−1) > X̄。∎
  （純regime算術で、smooth性・窓空性を一切使わない。auditはidentity述語
  N == (M+1)k₀+2M−κ を10,886行で確認。X̄境の鋭さ: M=1997, t=121, d=1994=2·997
  に対し N/d = 337·719 = 242,303 vs X̄ = 242,058.3（1.001倍）。）
- **T3 EFFECTIVE-WINDOW（t≥1・全ヒット）**: Nの約数で拡張窓 **[M, X̄)** に入るものは
  存在しない（窓 [M,k₀] のみならずスリバー (k₀, X̄) も空。X̄−k₀ = 2k₀/(M−1) ≈ 2t+2）。
  証明: d ∈ (k₀, X̄) を約数とし e := N/d。（i）d < X̄ ゆえ
  e > N/X̄ = N(M−1)/((M+1)k₀) ≥ M−1（N ≥ (M+1)k₀）で、整数なので e ≥ M。
  （ii）d ≥ M ゆえ e ≤ N/M = Y−1/M < Y で e ≤ Y−1。（iii）eは約数で窓を跨げない
  ので e ≥ k₀+1。（iv）d = N/e ≥ N/(Y−1) = M+(M−1)/(Y−1) > M で d ≥ M+1。
  （v）d = N/e ≤ N/(k₀+1) = M+1+(M−κ−1)/(k₀+1)。M−κ−1 < k₀+1
  （⟺ M(t−1)+2κ+1 > 0・t≥1で成立）ゆえ d < M+2 で d ≤ M+1。
  （vi）M ∤ N（N ≡ −1 mod M）かつ M+1 ∤ N（N = MY−1 ≡ −Y−1 ≡ −(κ+2) mod (M+1)
  で 2 ≤ κ+2 ≤ M）。矛盾。∎
  **作業メモの副作用条件 k₀ ≥ 2M−κ は不要**（上の証明はt≥1・κ≤M−2で閉じる）。
  auditは条件付きで機械検査し、条件外3,833行でもスリバー約数は0件（Sec.2）。
  - **系 PAIR-MIN+**: M以上の約数はすべてX̄超え。K0960 PAIR-MIN
    （k₀ < min{pᵢpⱼ ≥ M}）は min{pᵢpⱼ ≥ M} ≥ X̄ に強化される（(1+2/(M−1))倍）。
    実測: M=1997, t=121 で pairmin = 337·719 = 242,303 ≥ ⌈X̄⌉ = 242,059。
- **T4 SQUEEZE-3（kodd=3 ∧ compliant）**: N = 2^a·p₁p₂p₃ かつ 2^a·p₃ ≤ M−1
  （compliant・t≥2のヒットではK0960 ODDCAPにより自動）のとき:
  - (i) p₁p₂ > X̄
  - (ii) t·M·(M+1) ≤ (M−1)·p₁p₂ − 1（すなわち t ≤ ((M−1)p₁p₂−1)/(M(M+1))）
  - (iii) p₁p₂ ≥ Y+1 = k₀+t+3 ≥ M+3
  - (iv) 深部cap: t·M·(M+1)·2^{2a} ≤ (M−1)³ − 2^{2a}
  証明: N = (2^a p₃)·(p₁p₂) と 2^a p₃ ≤ M−1。
  (i) (M+1)k₀ < N ≤ (M−1)p₁p₂。
  (ii) N = MY−1 > MK = M((M+1)t+κ)（N−MK = M−1 > 0）ゆえ
  M(M+1)t+Mκ ≤ (M−1)p₁p₂−1、κ≥0 で左端へ。
  (iii) N/(M−1) = Y+K/(M−1) > Y（N = (M−1)Y+K）ゆえ p₁p₂ ≥ N/(M−1) を
  整数化して p₁p₂ ≥ Y+1。
  (iv) compliantから p₁,p₂ ≤ (M−1)/2^a で p₁p₂ ≤ ((M−1)/2^a)² を(ii)へ代入。∎
  （(iv)のa=1版 t ≤ ((M−1)³−4)/(4M(M+1)) はK0960 DEEP-CAP case Aの
  t < ((M−1)²+4)/(4M) を(M−1)/(M+1)因子分だけ厳密化。
  (ii)のfloor到達: argmax ρ = tM/p₁p₂ = 0.99725 @ M=1997, κ=180, t=121
  （N=2·337·719·997・p₁p₂=242,303・bound 121.21・floor到達）。
  t>60帯899行中26行が t = ⌊((M−1)p₁p₂−1)/(M(M+1))⌋ ちょうど。）
- **T5 CHAR-3（kodd=3の双方向特徴付け）**:
  - (a) **⟸ compliant ⟹ 窓空（任意のt≥1・Yの素数性不要・窓検査不要）**:
    Nの約数は 2^i・2^i p_j・2^i p_jp_k・2^i p₁p₂p₃ (0≤i≤a) のいずれか。
    2^i ≤ 2^a ≤ (M−1)/3 < M（p₃ ≥ 3）。2^i p_j ≤ 2^a p₃ ≤ M−1。
    ペア積はすべて p₁p₂ 以上で p₁p₂ ≥ Y+1 > k₀（T4(iii)）、トリプル積も同様。
    ゆえ全約数は ≤ M−1 か > k₀ で窓 [M,k₀] は必ず空。
    **complianceだけで窓空が従う**（「自己阻止」構造）。
  - (b) **⟹ t≥2のsmoothヒット ⟹ compliant**: K0960 ODDCAP（梯子に t≥2 が必要）。
  - (c) **まとめ**: t≥2・[Y ok]（Y素数∨Y=M²）では
    「kodd=3のヒット ⟺ N=2^a p₁p₂p₃ ∧ 2^a p₃ ≤ M−1」。
    t=1では(a)片方向のみ成立し、非compliantのkodd=3ヒットが実在
    （出版センサスで1,111件・T1と同様に梯子の t≥2 が本質）。
  - 系（dead排除・全称）: Y素数・Y ≥ M+2 なら gcd(κ+1, M+1) = 1
    （Y ≡ κ+1 mod M+1 で、共通約数d>1は d | Y かつ d ≤ M+1 < Y を強制）。
    ゆえ素数Yの窓空候補はdeadクラスに落ちない（walk観測 hits_dead = 0 の証明）。
- **T6 K4-A（t≥2）**: kodd=4のsmoothヒットはすべてcase A（top pair p₃p₄ ≥ M）。
  証明: case B（全ペア<M）では p₁p₂ < M からTWO-ZONEで 2^a p₁p₂ ≤ M−1、
  p₃p₄ ≤ M−1。N = (2^a p₁p₂)(p₃p₄) ≤ (M−1)²。一方 t≥2 で
  N ≥ (M+1)(2M−1)+2M−(M−2) = 2M²+2M+1 > (M−1)²。矛盾。∎
  （t=1ではcase B行が22件実在し、定理の適用範囲外であることを実証。）
- **T7 K4交叉対二分法（t≥2）**: (p₂p₃ ≥ M ∧ p₁p₄ ≥ M) と
  (p₁p₃ ≥ M ∧ p₂p₄ ≥ M) はいずれも不可能（積 p₂p₃·p₁p₄ = p₁p₄·p₂p₃ =
  p₁p₂p₃p₄ の2つの交叉分解）。
  証明: 両方 ≥ M なら両ペア積は約数なので k₀ 超え、
  N = 2^a(交叉対積1)(交叉対積2) > 2^a k₀² ≥ 2k₀²（a≥1・K0949 PARITY）。
  一方 N = (M+1)k₀+2M−κ ≤ (M+2)k₀+1（k₀ ≥ 2M−1 ⟹ 2M ≤ k₀+1）で、
  2k₀² > (M+2)k₀+1 は k₀ ≥ 2M−1（M≥3）から成立。矛盾。∎
- **T8 K4-CAP（t≥2・case Aの3分岐とt上界）**: T6より全ヒットがcase A。
  p₂p₃の位置で3分岐:
  - **(α) p₂p₃ < M ≤ p₁p₄**: TWO-ZONEで 2^a p₂p₃ ≤ M−1、p₂p₃ ≥ p₁² から
    p₁ ≤ √((M−1)/2^a)、ODDCAPで p₄ ≤ (M−1)/2^a。
    k₀ < p₁p₄ ≤ √((M−1)/2^a)·(M−1)/2^a ゆえ
    **t < ((M−1)^{3/2}/2^{3a/2}+1)/M < √M/2^a + 1/M**（a≥1）。
    （audit述語形 (2^a(Mt−1))² < M(M−1)² はこの弱い系。）
  - **(β) p₂p₃ < M ∧ p₁p₄ < M**: TWO-ZONEで 2^a p₂p₃ ≤ M−1 かつ
    2^a p₁p₄ ≤ M−1。N = (2^a p₂p₃)(p₁p₄) ≤ (M−1)²/2^a。
    (M+1)k₀ < N より (M+1)(Mt−1) < (M−1)²/2^a すなわち
    Mt−1 ≤ (M−3+4/(M+1))/2^a、**t < 1（M≥5・a≥1）ゆえ(β)は空**。
    （作業メモの「t ≤ 2^a−1（a=1なら空）」から全称空への強化・データも0行。）
  - **(γ) p₂p₃ ≥ M**: T7から p₁p₄ < M かつ p₂p₄ ≥ p₂p₃ ≥ M から p₁p₃ < M、
    さらに p₁p₂ ≤ p₁p₄ < M。TWO-ZONEで
    2^a p₁p₂, 2^a p₁p₃, 2^a p₁p₄ ≤ M−1（小素数側の3重cap）。
    - weak: k₀ < p₃p₄ ≤ ⌊(M−1)/2^a⌋² ゆえ **Mt ≤ ⌊(M−1)/2^a⌋²**。
    - sharp: k₀ < p₂p₄（p₂p₄ ≥ M・約数）かつ
      p₂ ≤ (M−1)/(2^a p₁)・p₄ ≤ (M−1)/(2^a p₁)（上の3重capの外側公式）から
      p₂p₄ ≤ ((M−1)/(2^a p₁))²。(Mt+κ−1)·2^{2a}·p₁² < (M−1)²。
      κ≥1なら **t·2^{2a}·p₁² ≤ M−2**（(M−1)²−1 = M(M−2) 整数化）、
      κ=0なら t·2^{2a}·p₁ ≤ M−2。
      センサスでは(γ)全413行がκ≥1（κ=0のγ行はM≤2000に不在）。
  - **まとめ（K4-CAP）**: kodd=4 (t≥2) ⟹
    t < max(√M/2^a + 1/M, (M−2)/(2^{2a}p₁²))（κ≥1）/
    max(√M/2^a + 1/M, (M−2)/(2^{2a}p₁))（κ=0）。
    a≥1・p₁≥3から無条件形 **t < max(√M/2 + 1/M, (M−2)/12)**、
    κ≥1（センサス全γ行）では **t ≤ max(√M/2 + 1/M, (M−2)/36)**。
    K0960 DEEP-CAP（t < M/4）のγ行側から見て9倍の厳密化。
    実測: α 139行（max t=12@M=1861・N=2·29²·31·821）・β 0行（証明どおり）・
    γ 413行（max t=37@M=1619・N=2·3·229·263·269・sharp bound 44）・
    aはα・γとも最大2。

## 2. 機械検証（squeeze_audit.py・全て0違反・決定的）

- **行ベース全数検査**: 出版smoothヒット10,886行 = K0958 hits_full（M≤1000全t）
  2,609行 + K0960 hits_strip2（1000<M≤2000全t）8,277行。各行でNを独立再因数分解
  （46,000以下の素数篩・試除割り。N < 2×10⁹ < 46,000²）し、24述語を検査:
  identity（N=(M+1)k₀+2M−κ）・recon_omega・parity・smooth・exclusive・
  twozone_t2（t≥2・T1）・effwindow_zone（T3）・squeeze_s1/s2/s3/deepcap/book
  （T4）・char3_window_vacuous・k4_dichotomy1/2（T7）・k4_alpha/beta・
  k4_gamma_p1p4/weak/sharp（T8）・k4B_sqrt・deepband_crosscheck
  （K0960出版deep_band 836行との行完全一致）・予想錨2件（下記）。**全て0違反**。
- **T1/T3の範囲外行**: t=1のTWO-ZONE違反は8,209件（定理はt≥2限定・梯子の
  k₀ ≥ 2M−2 がt=1で切れる正常な範囲外）。T3の旧条件 k₀ ≥ 2M−κ の外側3,833行でも
  スリバー約数は0件（条件不要の傍証）。
- **engine錨**（composite_core.sigma_Z・K0948-K0950ピン）: ヒット行1/37刻み+t≥150全件
  の474件は全てσ_Z=1（0失敗）・窓阻止サンプル40件は全てσ_Z≠1（0失敗）・
  phantomサンプル25件は全てσ_Z≠1（0失敗）。
- **prime-Y walk 34素数**（pinned census_walk再走査: WALK_M = ≤100の素数34個 + 大型11個）:
  候補617,906・smooth 54,203・ヒット303・窓阻止53,900。**ヒット集合は出版行と
  34素数すべて完全一致（mismatch_M=0）**。kodd=3 t≥2候補3,374件中compliant 137件は
  全て窓空（0 blocked）・非compliant窓空0件（CHAR-3 iff方向の完全一致）。
  t=1: kodd=3候補133件中compliant 24件は全て窓空（0 blocked）。
  窓阻止候補のkoddヒストは4〜6（12,759/16,741/11,668）に集中。
- **composite-Y walk 33素数**（M≤149・全Y域・ymax=(M−1)³/M）:
  smooth候補13,937件（合成Y 10,983・Y=M² 0件）。kodd=3 ∧ compliant 511件の
  **窓非空は0件**（CHAR-3⟸の合成Y域での自己阻止予言の完全成立）。
  窓空かつ合成Yの**phantom 676件**（dead 610 + live 66・全てengine錨でσ_Z≠1）。
- **決定性**: 冷再実行（__pycache__破棄・21.3秒）で出力JSON byte同一
  （sha256 5fca78b9…）。

## 3. 構造観察（有限・全称主張なし）

- **t>60帯はkodd=3一色**: M≤2000全tでt>60のsmoothヒット899行は全件kodd=3
  （M≤1000の63行を含む）。v₂≥2の例外は3行のみ
  （M=1901 κ=618 t=65・M=1987 κ=1458 t=71・M=1987 κ=1534 t=84・
  いずれも N=2²·(400前後の素数3つ)）。
- **kodd別t上限**: kodd=3 → 427@1789・kodd=4 → 37@1619・kodd=5 → 3@1097・
  kodd=6 → 2@757・kodd=7,8,9 → 1。t2-60帯のkoddヒスト: {3: 4,525, 4: 552, 5: 5, 6: 1}。
- **予想（有限検証のみ・未証明）**: (i) kodd=4 ⟹ t < √M（552行0違反・(γ)の
  理論上界(M−2)/36が√Mを超えるM>1296で真価を問う形・未証明）。
  (ii) kodd ≥ 5 ⟹ t ≤ 3（0違反）。
- **SQUEEZE-3のtightness**: ρ = tM/p₁p₂ はt>60帯で最大0.99725（M=1997）・
  中央値0.887。compliance飽和 s = 2^a p₃/(M−1) は最大1.0（飽和到達）。
  floor到達は t1帯304行・t2-60帯503行・t>60帯26行（boundのfloorちょうど）。
- **t=1集団の内部構造**: kodd=3のt=1ヒットはcompliant 791件と非compliant 1,111件
  （ODDCAP非適用の実在集団）・kodd=4のt=1でcase B 22件（T6がt≥2限定の傍証）。
  t=1全体のkoddヒスト: {1: 2, 2: 424, 3: 1,902, 4: 1,674, 5: 638, 6: 204, 7: 46, 8: 12, 9: 2}。

## 4. phantomとHIT-ARITHの適用範囲（K0956の読みの精密化）

- K0956 HIT-ARITH「窓空 ⟺ σ_Z=1」は **[Y ok]（Y素数∨Y=M²）クラス限定**である。
  composite-Yでは「窓空かつσ_Z≠1」の**phantom候補**が実在する
  （M≤149 walkで676件 = dead 610 + live 66・engine錨25/25でσ_Z≠1）。
- したがって本項の「hit」の正確な定義は σ_Z(M,K)=1 であり、窓空は
  [Y ok]クラスでのみhitと同値。smoothヒット列（K0958/K0960出版・本項の入力）は
  全て素数Yクラス（K0958のcensusは素数Y walk）なので影響はないが、
  composite-Y域で窓空だけを基準に列挙するとphantomを混入する。
  CHAR-3⟸（compliant ⟹ 窓空）はY素数性を使わないので合成Y域でも有効
  （511/511で確認）が、「窓空 ⟹ hit」への変換には[Y ok]が必要。
- dead排除の系（T5系）により素数Y域のphantomは存在しない
  （hits_dead=0はwalkで機械確認済み・証明はT5系）。

## 5. 範囲・限界・次課題

- すべての定理はsmoothヒット（main regime・素数M≥5・t≥2・窓空）向け。
  branch型初回ヒット（93.8%・K0956）には適用されない。
- 機械検証はM≤2000全tの全数アンカー（決定的完全列挙に基づく）であり、
  全称証明の代替ではない（証明はSec.1の紙上）。
- OPEN: (i) 予想(i)(ii)の全称化（γ分岐のDiophantine scarcity: なぜγ行は
  理論上界(M−2)/36に対しt≤37にとどまるのか・p₂p₃ ≥ M ∧ k₀付近のペア積の
  合同構造）。(ii) κ=0のγ行がM>2000に現れるか（sharp boundのκ≥1証明との隙間）。
  (iii) kodd=3のSQUEEZE-3 boundのfloor到達分布の理論（PAIR-MIN近接分布理論・
  K0960 OPEN(i)の継続）。(iv) M>2000延伸（sieve-walk・K0960と同じ方法）。
- t=1の非compliant集団（1,111行）の構造は未解析（ODDCAP外の実在群・
  梯子の切れるt=1固有の算術）。
- 11×11空盤・二石rootには言及しない。uv check/buildは本環境にcloneとuvがなく
  未実施（歴代remo項目と同じ扱い）。generated/とroot READMEは未編集。

## 6. ピン（sha256・先頭8桁）

- 依存core（K0956/K0958/K0960ピンと一致）: prehit_core bf8ed817…・
  composite_core 3990d67f…・sievegen_core a69f916c…・
  branch_density_core 34b4ff15…・smooth_core 928c54ca…
- 出版入力: hits_full.json 4d2243ea…・hits_strip2.json 784ca43c…・
  hits_deep_band.json 1cc020b2…
- 本実験: squeeze_audit.py 1d12e399…・
  output/squeeze_audit.json 5fca78b9…（冷再実行byte同一）
