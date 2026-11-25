---
id: K0968
title: γ_r枝（r≥4一般）のSIX-ZONE_r・P2-LOWER_r・Y-CAP_rとA-POS（a=0不在・K0966の2つのOPEN解決）
kind: proposition
status: proved
topics: [residual-games, statistics, verification]
aliases: [A-POS, GAMMA-R, GZ-R, EX-R, SIX-ZONE-R, P2-LOWER-R, BAND-R, Y-CAP-R]
relations:
  - type: depends_on
    target: K0961
    note: TWO-ZONE（t≥2・r非依存）・K4-CAP排他3分岐（γ₄⟺SIX-ZONE₄定理に使用）・CHAR-3（γ₃空のremarkに使用）・中核恒等式
  - type: depends_on
    target: K0966
    note: γ枝r=4の定理群（SIX-ZONE/P2-LOWER/SHARP-V）をr=4ケースとして回収する前提・入力 sha256ピンを共有
  - type: depends_on
    target: K0949
    note: 定理PARITY（素数M≥3のmain regimeヒットKは偶数）がA-POSの前提
  - type: depends_on
    target: K0963
    note: 出版band 406行（kodd5_band_k5rows）を行入力に使用・CAP-27（B4-3設定・t≲M/108）との鋭さ比較
  - type: depends_on
    target: K0965
    note: 出版modeb_rows_k5p（1,217行）・modeb_rows_k4_deep/kap0・modeb_rows_k3_t300plusを行入力に使用
  - type: generalizes
    target: K0966
    note: γ枝（p₂p₃≥M・r=4）をγ_r（p₂···p_{r−1}≥M・r≥4一般）へ拡張しSIX-ZONE/P2-LOWER/BAND/Y-CAPを一般rで再定式化（r=4で全定理を回収）・A-POSでK0966の仮定a≥1が自動成立することを示しOPEN「a=0未証明」を解決
  - type: supports
    target: K0965
    note: 予想(ii)反証band 406行のうち392行（B4-3 369全体・A 18・B1 2・B6-2535 3）がγ₅に属し six zone 上限壁（全奇素因数≤(M−1)/c・3p₃p₄>k₀・18p₃p₄p₅≡−1 (mod M)・k₀≤3⌊(M−1)/6⌋²・t≲M/12無条件cap）で閉じ込められることを確定（B6-max 14行はγ₅外・K0963 CAP-52/73管轄のまま）
artifacts:
  - path: research/experiments/sixzone-general-r-20261118/report.md
    role: proof
    note: A-POS・γ_r定理群（GZ_r/EX_r/SIX-ZONE_r/P2-LOWER_r/BAND_r/Y-CAP_r/γ₄⟺SIX-ZONE₄）の紙上全称証明と機械検証の正本
  - path: research/experiments/sixzone-general-r-20261118/sixzone_r_verify.py
    role: verifier
    note: 出版5入力（sha256ピン照合）の全行独立再検証（試除素数判定・約数全列挙窓空・恒等式）+γ行7述語+非γ行SIX-ZONE不成立+γ⟺SIX-ZONE census+wall rows（決定的・冷再実行byte同一・sha256 7abe04ac…）
  - path: research/experiments/sixzone-general-r-20261118/output/sixzone_r_audit.json
    role: data
    note: 全検査all_ok=true・margin・wall tightness（sha256 2c8f4e05…・2回冷実行byte同一）
  - path: research/log/2026-11-18-sixzone-general-r.md
    role: log
    note: 発見順・a=0がK0949 PARITYで閉じることに気づいた経緯・初期pinタイポ事故・次課題
date: 2026-11-18
scope: >-
  素数M≥5・main regime・t≥2・smoothヒット・r=kodd≥4・γ_r枝（p₂p₃···p_{r−1}≥M）。
  GZ_r/EX_r/SIX-ZONE_r/P2-LOWER_r/BAND_r/Y-CAP_r・γ₄⟺SIX-ZONE₄定理はこのスコープの
  紙上全称証明。A-POS（a=v₂(N)≥1自動）はmain regime・素数M≥3の全ヒット（t≥1込み・
  smooth限定なし）の系（K0949 PARITYから）。r≥5でのγ_r⟺SIX-ZONE_rの⟹方向は
  主張しない（census 0例外・OPEN）。非γ_r枝（K0963 18設定・CAP-52/73）には主張しない。
  機械検証は出版行（k5p 1,217・band 406・k4 1,741 unique・k3 19）で有限確認。
evidence: >-
  紙上全称証明（report.md §1–2: A-POSはK0949 PARITY+κ≡K (mod 2)+Y奇+N偶の一行鎖。
  EX_rは相補積R_i≥R_r=p₂···p_{r−1}≥M（γ_r）と恒等式Y−k₀=t+2からp₁pᵢ>k₀を排除
  （a=1は(M−1)t+κ>3・a≥2は3k₀>t+2・A-POSでa≥1は自動）。SIX-ZONE_rはTWO-ZONEの
  zone-2排除でi=1はmult(p₁)=1のときp₂>p₁から従う。P2-LOWER_r/BAND_r/Y-CAP_rは
  GZ_rとSIX-ZONE_rの積評価。γ₄⟺SIX-ZONE₄はK4-CAP排他3分岐+αのi=4構造的不成立）。
  機械検証: 出版5入力全行の独立再検証違反0・γ行7述語違反0（margin: r4壁余裕0
  （5行がc·pᵢ=M−1に密着・「≤M−2」への全称強化は不可能を確定）・r5壁余裕12・
  r5 GZ差+32・r5 P2-LOWER比3.75）・非γ行183行全てSIX-ZONE不成立
  （γ⟺SIX-ZONE census 2,958 unique行で0例外・不成立indexは常にi=r）・
  band 406行はk5pに全包含（共通フィールド一致）・A-POS錨（全行κ偶数・a≥1）違反0・
  冷再実行2回byte同一。限界: r≥5の⟹方向・Y-CAP_rの数値的鋭さ（r=5は≈M²/216で
  CAP-27より弱い）・LG-OPEN（kodd≥6非γ_r枝）はOPEN。
---

## 命題・範囲

記法はK0956/K0961/K0965/K0966と同一（素数M≥5・main regime・Y=K+1・
k₀=Mt+κ−1・N=MY−1・窓=[M,k₀]・a=v₂(N)・r=kodd・p₁≤…≤p_r（重複込み）・
c=2^a·p₁・恒等式Y−k₀=t+2）。対象はsmoothヒット・t≥2。

- **A-POS（証明済み・全称系）**: main regime・素数M≥3のヒットは
  **a=v₂(N)≥1（N偶数）**。K0949 PARITY（ヒットKは偶数）から
  κ偶数・Y奇数・N偶数が従う。a=0（N奇数）のヒットは存在しない
  （全kodd・t≥1込み）。K0966のOPEN「a=0未証明」を解決し、
  K0966と本項の仮定a≥1は自動成立に変わる。
- **γ_r枝（r≥4）**: **p₂p₃···p_{r−1} ≥ M**（r=4でK0966のγ枝に一致）。
  この枝のsmoothヒット（t≥2）に対し、すべて紙上全称証明:
  - **GZ_r**: p₂···p_{r−1} ≥ k₀+1。
  - **EX_r**: p₁pᵢ ≤ k₀ (∀i∈{1..r})。
  - **SIX-ZONE_r**: **c·pᵢ ≤ M−1 (∀i∈{1..r})**。a=1・p₁=3では
    N/2の全奇素因数 ≤ (M−1)/6。
  - **P2-LOWER_r**: p₂·⌊(M−1)/c⌋^{r−3} ≥ k₀+1
    （実数形 p₂ > c^{r−3}k₀/(M−1)^{r−3}・r=4でp₂>c·tを回収）。
  - **BAND_r**: Mt+κ ≤ p₂·⌊(M−1)/c⌋^{r−3} ≤ ⌊(M−1)/c⌋^{r−2}
    （band collision・r=4でt < ((M−1)²+36)/(36M)形）。
  - **Y-CAP_r**: **t·c^{r−2}·M·(M+1) < (M−1)^{r−1}+c^{r−2}**
    （κ無条件・r=4でK0966 SHARP-Vを回収・r=5でt ≲ M²/216）。
  - **CONG（恒等式）**: c·p₂···p_r = N ≡ −1 (mod M)。
- **γ₄ ⟺ SIX-ZONE₄（証明済み定理）**: K0961 K4-CAPの排他3分岐と
  α枝のi=4構造的不成立から、kodd=4ではSIX-ZONE成立とγ枝が同値。
- **r=3 remark**: γ₃（p₂≥M）はK0961 CHAR-3のcomplianceから空。
  γ_r族はr=4で始まる。
- **B4-3系（a=1・p₁=p₂=3・γ₅）**: 18p₃p₄p₅ ≡ −1 (mod M)・
  3p₃p₄ > k₀・p₃,p₄,p₅ ≤ ⌊(M−1)/6⌋・k₀ ≤ 3⌊(M−1)/6⌋²
  （**t ≲ M/12・κ無条件の新しいcap**・K0963 CAP-27（≈M/108・B4-3
  設定固有）より9倍弱いがγ₅全域無条件）。

## 現在の根拠と限界

- 根拠は紙上全称証明（report.md §1–2）。中核は補題EX_rの一般化:
  相補積R_i=N/(2^a·p₁pᵢ)の最小値がR_r=p₂···p_{r−1}（γ_rで≥M）であり、
  p₁pᵢ>k₀仮定がR_i<(M/2^a)(1+(t+2)/k₀)<Mを強制して矛盾する。
  i=1はmult(p₁)=1のときp₂>p₁からi=2の剛性で従う。A-POSはK0949 PARITYの
  一行系で、EX_rが必要としていたa≥1が全ヒットで自動成立する。
- 機械検証（sixzone_r_verify.py・出版入力sha256ピン照合・冷再実行byte同一）:
  全行独立再検証（素数判定・再因数分解・約数全列挙窓空・恒等式）違反0。
  γ行7述語違反0（k5p γ 1,040 = r5 1,023/r6 16/r7 1・band γ 392・k4 γ 1,735の
  K0966独立再現込み）。非γ行183行は全てSIX-ZONE不成立
  （γ⟺SIX-ZONE census 0例外・不成立indexは常にi=r）。
  band 406行はk5p 1,217行に全包含。A-POS錨は全3,385行（重複込み）で
  κ偶数・a≥1違反0。
- **wall tightness**: γ₄行5行（M=3607/4783/5683/6619/6703・いずれも
  a=1・p₁=3・M=6p₄+1）がc·pᵢ=M−1にちょうど密着。SIX-ZONEの壁は
  「≤M−2」へ全称的に強化できない。r=5最密着はM=7507, t=2（余裕12）。
  audit JSONのgamma_wall_rowsに壁余裕≤15の34行を全記録。
- 限界・OPEN: (i) r≥5でのγ_r⟹SIX-ZONE_r（census 0例外だが未証明・
  K0963 18設定毎の「相補積≥M」型事実が次課題） (ii) Y-CAP_rはr≥5で
  数值的に弱い（r=5≈M²/216 vs CAP-27≈M/108・γ₅の価値は構造閉じ込め）
  (iii) LG-OPEN（kodd≥6非γ_r枝・K0963 T8）は本項では閉じない
  （γ₆は16/24行・有限観察） (iv) γ₅行のκ=0は出版データに不在
  （有限観察）。11×11空盤・REMO計数側への直接の影響はない
  （σ_Z highwayの構造精密化）。`uv run check/build`・unittestは
  本環境でpackage導入禁止のため未実施（歴代remo項目と同じ扱い）。
