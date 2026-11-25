# K0943: ladder監視状態のO(1)閉形式（STATE-CF）・死亡状態閉形式（DS-CF）・p²崩壊定理（P2）− K0941レジューム(i)の完成

date: 2026-11-18
repo: yuubinnkyoku/kyouen-researches (main)
依存: K0937 (INV-TRACK・死亡合同式), K0934 (LAD-GEN (c)), K0941 (定理A/B・P2OBS), K0939 (ENTRY-LOC)
成果物: deathstate_verify.py, audit_build.py, output/deathstate_audit.json（sha256 `9bc8c2f478c98ef5bbfdd08e3edd733a4a27ec31f835327d51445f1d38e48882`, 7514 bytes）
core: sievegen_core.py = K0937 committed版のbyte同一コピー（sha256 `a69f916c86ed02d5eeed3d5494bbb0f44f652d0d1e4714c50bbc68bef1843499`）

## 0. 概要

K0941のレジューム(i)「P2OBSの全称証明」を完了した。出発点の予想に反して、
予定していたp²軌道のh-walk記述は不要だった。INV-TRACK（K0937）の状態不変量
T=wn+h+wと新規補題H-CAPだけから、ladder regimeの**すべての**stretch開始状態
（死亡stretch・素数Nのエンドゲーム入口を含む）がO(1)算術式で決定される
（定理STATE-CF）。そこから死の二分法・死後状態の石数保存・p²崩壊定理
（K0941 P2OBSの全称化）が従属的に導かれ、tracker再帰が状態列挙から完全に消える。

## 1. 記法・既存結果（本項で再証明しない）

- ゲーム: V(m)（N=2m+1, watch=0, pot0=1）/ U(m)（N=2m+3, watch=m−1, pot0=2）。
- F(w,h;n): pot=w・holdings=[w]^{n−h}+[w+1]^h・ptr先頭の正規stretch状態。
- **T**: VはT=N・UはT=N−1。INV-TRACK（K0937）: 生存中の各stretch開始状態は
  F(w,h;n)で T=wn+h+w・a=h（V）/a=h+1（U）・t=n div (w+1)・r=n mod (w+1)。
- LAD-GEN (c)（K0934・t=1拡張はK0937 T1MAP）: 生存stretch-wの終状態は
  F(w+1, h2; n2)・**h2=(h−1−r) mod (w+1)**。
- K0941定理A: 奇合成Nの監視はladderを生存できず、stretch w*=spf(N)−1で死ぬ。
- K0941定理B: V死=breaking死（保持w+1）→死後Z(w+1, n−t)。
  U死=block死（保持w）→死後E(w+1; n−t−1−w, w)、崩壊(t,h,r)=(1,0,0)→Z(w+2, w−1)。
- ENTRY-LOC（K0939）: 素数Nのt=0入口はfamily状態 F(w,h;n)（n∈{w−1,w}）。
- K0937死亡合同式: 監視はstretch wでの死亡が可能 ⟺ (w+1)|N（この条件下で
  V: r=h−1・U: r=h が監視位置等式から強制される）。

## 2. 補題H-CAP（新規・全称）

**主張**: V(m)/U(m)で監視が生存している限りのすべてのladder stretch開始状態
F(w,h;n)（w≥2）は **0≤h≤w−1** を満たす（Vはさらに **1≤h**）。
素数Nのエンドゲーム入口（t=0・family状態）でも同じ界を持つ。

**証明**（幅に関する帰納）。
基底（stretch 2）: VはF(2,1;m−1)・UはF(2,0;m)（INV-TRACK基底）で
h=1=2−1 / h=0。帰納段: 生存したstretch-w（h≤w−1・t≥1）の終状態はLAD-GEN (c)
により F(w+1, h2; n2)、h2=(h−1−r) mod (w+1) ∈ [0,w]=[0,(w+1)−1]。
よって次幅W=w+1の開始状態は常に h≤W−1。U側はこれで完了。
V側の h≥1: h=0 ⟺ W | (T−W) ⟺ W | T = N。幅Wがladder内（合成NはW≤w*=spf(N)−1、
素数NはW≤入口幅、いずれも W²<N・W≥2）のとき W の素因数はすべて
min(spf(N), N)未満なので W∤N（素数Nは自明、合成Nはspf(N)最小性）。
∎

**系EXC-UNREACH（全称）**: LAD-GEN (K0934 (e))の唯一の監視死亡例外
(h,r,t,a)=(0,0,2,w+1) はV/Uゲームで非到達（a=w+1が必要: Vはa=h≤w−1、
Uはa=h+1=w+1 ⟺ h=w がH-CAPで排除される）。

## 3. 定理STATE-CF（新規・全称）

**主張**: 監視生存中のすべてのladder stretch開始状態（t≥1）と素数Nの
エンドゲーム入口状態（t=0）に対して、

- **h = (T−w) mod w**（V: h∈[1,w−1]・U: h∈[0,w−1]）
- **n = (T−w−h)/w**（割り切れる）

が成立する。とくにstretch状態列は (side, m, w) からO(1)で計算され、
trackerの再帰（watchmap・h2/n2遷移）を一切使わない。

**証明**. INV-TRACKより状態はF(w,h;n)でT=wn+h+w。H-CAPより
h∈[1,w−1]（V）/[0,w−1]（U）。T−w=wn+h をh∈[0,w−1]で割った商と剰余は
一意（div/mod）なので h=(T−w) mod w・n=(T−w−h)/w。Vの剰余が0にならない
ことはH-CAPの証明と同じW∤N論法。∎

**ENTRY-LOCの精密化（系）**: K0939のfamily範囲 h≤min(n,w)（V）/h≤min(n−1,w)（U）
に対し、実際の界はタイトに h≤w−1（Vは1≤h≤w−1）である（H-CAP直接）。

## 4. 系DS-CF（死亡stretch状態の閉形式・全称）

N奇合成・p=spf(N)・w*=p−1のとき、死亡stretch開始状態はSTATE-CFのw=w*値

- V: h*=(N−w*) mod w* ∈[1,w*−1]・n*=(N−w*−h*)/w*
- U: h*=(N−1−w*) mod w* ∈[0,w*−1]・n*=(N−1−w*−h*)/w*

であり、死亡二分法 r*=h*−1（V）/ r*=h*（U）は合同式から再導出される:

- V: N=wn+h+w ≡ h−r−1 (mod w+1)（w≡−1・n≡−r）。死亡合同式(w+1)|Nと
  h−r−1∈[−w, w−2]（h∈[1,w−1], r∈[0,w]）より h−r−1=0。
- U: N=wn+h+w+1 ≡ h−r (mod w+1)。h−r∈[−w, w−1]より h−r=0。

死後状態（K0941定理B）の全石数（盤面+pot）は閉形式状態から算術検証される
（いずれも合同式変形、機械チェックで全合成死亡に数値確認）:

- V: Z(w*+1, n*−t*): (w*+1)(n*−t*+1) = N（r=h−1を使用）。
- U非崩壊: E(w*+1; α,β)・α=n*−t*−1−w*・β=w*:
  (w*+1)α+(w*+2)β+(w*+1) = N−1（r=hを使用）。
- U崩壊: Z(w*+2, w*−1): (w*+2)w* = N−1（N=(w*+1)²・n*=w*+1・h*=0）。

**U曖昧ケースの解消（観察）**: w* | N−1 のとき状態等式 T=wn+h+w は
(h,n)=(0,(N−1−w*)/w*) と (w*, (N−1−w*)/w*−1) の両方で満たされる（監視窓も
両立しうる）。H-CAPは実際の歩みが常に前者を取ることを含意する。
m≤30,000で14,123例（うち52例がn*=w*+1すなわちp²崩壊・14,071例がn*≥w*+2）。
全例でtrackerのh*は0（CFTRACK照合・違反0）。

## 5. 系P2（p²崩壊定理・K0941 P2OBSの全称化）

**主張**:
(i) U側: 崩壊死 (t*,h*,r*)=(1,0,0) ⟺ **N=spf(N)²**。
(ii) V側: 死亡状態 (n*,t*,r*,h*)=(p,1,0,1) ⟺ **N=p²**。

**証明**. DS-CFより死亡状態はSTATE-CF閉形式。
(i) (t,h,r)=(1,0,0) ⟺ n*=w*+1・h*=0（r=n*−(w*+1)=0）。状態等式
N−1=w*n*+h*+w*=(w*+1)²−1 より N=(w*+1)²=spf(N)²。逆は同じ式を遡る。
(ii) (n,t,r,h)=(w*+1,1,0,1)（p=w*+1）: N=w*(w*+1)+1+w*=(w*+1)²。
逆: N=p²のとき h*=(p²−p+1) mod (p−1)=1（p²−p+1=p(p−1)+1）・
n*=(p²−p)/(p−1)=p・t*,r*=divmod(p,p)=(1,0)。∎

K0941のP2OBS（m≤8,000で29例↔29例）は本項でm≤30,000・p≤241の52例↔52例
全単射として機械確認され、かつ全称証明を得た。

## 6. 帰結（WALK-CF）

- ladder regimeの全stretch状態列は (side,m) からO(spf(N))時間・O(1)メモリで
  **閉形式のみで**列挙できる（各幅w=2..w*で(n_w,h_w)を書き出す）。
  K0941定理Dのラベル合成が使う除去集合 {j(w′+1)−1: j≤J′}∪{bl′} の
  J′,bl′も閉形式から直接出る（J′=t′ or t′−1はr′,h′比較、bl′はK0934公式）。
  よって合成NのV/U値計算（frame[σ]）はtracker全体を削除して
  純閉形式+σ再帰（O(k)）だけになる。σ_E/σ_Zの閉形式は別課題のまま。
- 11×11（長期レーン）への接続: 一様盤のladder解析に現れるstretch状態の
  妥当性判定・枝刈りにSTATE-CFが使える可能性（未実施・記録のみ）。

## 7. 機械的証拠（deathstate_verify.py・audit_build.py）

決定的（時間・乱数なし）。6チェック全合格（監査JSONの集計値）:

- **COREPIN**: sievegen_core.py sha256ピン照合。
- **CFTRACK**: 両側m≤30,000・60,000ゲーム・**2,597,593 tracker step**全てが
  閉形式・H-CAP界・監視窓1≤a≤n・INV恒等式・a=h/h+1に一致。h=wは0回。
  素数N入口12,111件も閉形式+family範囲に一致（V m=1のn=0退化形は
  ENTRY-LOC既知の例外として計上）。
- **DEATHCF**: 合成死亡47,889件: w*=spf(N)−1・r=h−1/h・保持w+1/w・
  死亡位相=t・死後石数=全て一致・違反0。U曖昧14,123件統計（前述）。
- **P2**: 両方向×52例・件数一致52=52=52=52（p=3..241）・違反0。
- **SIMDEATH**: 閉形式死亡状態からstretch_sim（位置ミニエンジン）613ゲーム
  （全p²ゲーム52×両側m≤30,000を含む）: 死亡位相・保持・位相数exp_len・
  死後Z/E/Z崩壊holdings円・n2が全て一致・違反0。
- **ENGINE**: 新鮮play_full両側m≤400・800ゲーム: ladder run開始状態
  6,523件が閉形式に一致・合成525ゲームのdeath pot=w*・保持二分法一致・
  素数275ゲームsurvivor==watch。違反0。

audit_build.pyはrun_checksをin-process 1回+deathstate_verify.py
（内部2回実行で決定性検証）をcold 2回実行しbyte同一を確認して
output/deathstate_audit.jsonを書く。

## 8. 範囲と限界

- 主張は一様盤・ladder regimeのstretch開始状態に限る。E-game内部の状態遷移
  （K0941定理C）とσ再帰は本項では閉形式化しない。
- 紙上証明はK0937/K0934/K0941/K0939の出版済み証明に依存する。機械アンカーは
  その依存構造込みで: 259万step照合+47,889死亡照合+613構造シミュレーション+
  800新鮮エンジン照合が0違反で裏付ける。
- 非一様盤・11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class1/2/4は
  **UNKNOWN不変**（本項は一切言及しない）。
- `uv run check/build`・unittestは本環境にcloneとuvがないため未実施
  （K0937/K0939/K0941と同じ扱い）。generated/とroot READMEは未編集。

## 9. 次課題

1. σ_E/σ_Zの閉形式探索（K0941レジューム(ii)）: 状態側は閉形式化完了したので、
   残るはE-gameのJosephus再帰のみ。σ_Z(3,K)の値1位置列
   （4,8,12,28,40,52,72,…）の構造解析から着手。
2. r人対戦・d次元版へのSTATE-CF転写（一般化レーン）。
3. K0939実験dirのaudit_build.py混入（監査JSON本文と同一・1033 bytes）の修正候補。
