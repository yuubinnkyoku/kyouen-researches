# K0941: 合成NのV(m)/U(m)の完全決定（LADDER-ONLY・死の二分法・E-game閉包・ラベル合成）

date: 2026-11-18
status: proved（本文の全定理は紙上全称証明。機械的証拠は `composite_verify.py` / `audit_build.py`、
監査 `output/composite_values_audit.json` sha256
97e854f7311ac24784fa7165a1a4dba55fca6727569af07e88b281e0f2558961）

## 0. 設定と依存

記法は K0937/K0939 と同一である。V(m): m人・各2石・pot 1・ptr 0・監視ラベル0、
N := 2m+1、base 正准形 F(2,1;m−1)（フェーズ1後）・監視距離 a=1。
U(m): m人・各2石・pot 2・ptr 0・監視ラベル m−1、N := 2m+3、base 正准形
F(2,0;m)・監視距離 a=1。F(w,h;n) は holdings [w]^(n−h)+[w+1]^h・pot w・
ptr 先頭。監視距離 a は円の末尾から数え、監視位置は n−a である。

依存する出版済み定理:

- K0928: 補題P（フェーズ規則）・定理RED（P(2m+1)=1+2V(m)・P(2m+2)=3+2U(m)）。
- K0931/K0933/K0934 (LAD-GEN): stretch-w の完全決定。**block** フェーズ群
  （block j: pot w・deal はフレーム位置 (j−1)(w+1)..j(w+1)−2 の w 位置に各+1・
  敗者位置 j(w+1)−1・保持 w・次 pot w）と **breaking** フェーズ
  （r<h: deal [n−r−w−1, n−r−2] の w 位置・敗者 n−r−1・保持 w+1・次 pot w+1・
  終状態 F(w+1,h−1−r;n−t);
  r≥h: deal [n−r,n)∪[0,w−r) の w 位置・敗者 bl=w−r（r≥1）または w+1
  （r=h=0,t≥2）・保持 w+1・次 pot w+1・終状態 F(w+1,h+w−r;n−t−1);
  崩壊 t=h=r=0... 厳密には t=1,r=0,h=0: block 1 の後に **collapse** フェーズ
  q=1・敗者位置0・保持 w+2・終状態 Z(w+2,w−1)）。
- K0935 (WATCH-MAP): 境界越え監視写像。
- K0937 (INV-TRACK): 生存中の stretch 開始状態は F(w,h;n) で a=h（V）/ a=h+1（U）、
  石数恒等式 T=wn+h+w（V: T=N・U: T=N−1）、死亡合同式
  「stretch-w で監視が死ぬ ⟺ a=r+1 ⟺ (w+1)|N」（ここで t,r は n=t(w+1)+r）。
- K0939 (SIEVE-PRIME / END-INV / ENTRY-LOC): 素数 N は t=0 エンドゲームに到達し
  そこでも生存（V(m)=0・U(m)=m−1）。入口は family 状態（n∈{w−1,w}・
  V: 1≤h≤min(n,w)・U: 0≤h≤min(n−1,w)・N=w(n+1)+h+s、s=0/1）。
  END-INV の遷移公式（後述の (1)）は状態局所の計算である。

K0939 が残した OPEN: **合成 N での値そのもの**（監視は死ぬことは K0937 で既知。
どのラベルが最終生存者になるか）。本項はこれを閉じる:
合成 N の V(m)/U(m) は純算術（エンジン不要）で完全決定され、
SIEVE-PRIME との合成で **全 m≥1 の V/U 値が純算術** になる（系COMPOSITE-VALUES）。

## 1. 定理A（LADDER-ONLY: 合成Nはt=0エンドゲームに到達しない）

**定理A.** N := 2m+1+s（s=0 が V、s=1 が U）を奇合成数とする。このゲームの
監視は ladder regime を生存して t=0 エンドゲームに入ることができない。
したがって（K0937 死亡合同式により）監視は ladder stretch w=spf(N)−1 で必ず死ぬ。

**証明.** 監視が stretch 2..w−1 を生存して幅 w の ladder が t=0 で終わった
（n≤w、つまり入口 family 状態に到達した）と仮定する。

(i) 死亡合同式（K0937）により、stretch j（2≤j）で監視が死ぬのは (j+1)|N の
とき、かつそのときに限る。stretch 2..w−1 を生存したので、N は 3..w のどの
数でも割れない。よって N の素因数はすべて ≥ w+1 である（N は奇なので
素因数 2 を持たない）。特に spf(N) ≥ w+1。

(ii) N は奇合成数なので N/spf(N) > 1 であり、その素因数もすべて ≥ spf(N)。
よって **N ≥ spf(N)² ≥ (w+1)²**。

(iii) 一方、K0939 ENTRY-LOC の入口位置決定（素数性は使わない。証明は
family h 範囲と石数恒等式 T=N（V）/T=N−1（U）のみを使用）により、
t=0 入口は family 状態でなければならない: n∈{w−1,w}・
N = w(n+1)+h+s・V: 1≤h≤min(n,w)・U: 0≤h≤min(n−1,w)。
n=w をとると
V: N = w(w+1)+h ≤ w²+w+w = w²+2w < (w+1)²、
U: N = w(w+1)+h+1 ≤ w²+w+(w−1)+1 = w²+2w < (w+1)²。
いずれも **N < (w+1)²** となり (ii) と矛盾する。∎

**系（死の位置）.** 奇合成 N の監視は stretch spf(N)−1 で死ぬ。
それより早い stretch j+1（j+1 < spf(N)）では死なない（j+1|N なら j+1 の
素因数 < spf(N) が N の素因数となり矛盾）。

## 2. 定理B（死の二分法と死後状態）

死亡合同式（K0937）: 死亡 ⟺ a=r+1。V は a=h、U は a=h+1 なので、

- **V死は必ず breaking 死**（r=h−1、つまり r<h）: 敗者位置 n−r−1=n−h は
  監視位置 n−a=n−h に一致し、LAD-GEN の breaking 敗者（保持 w+1）である。
  よって死の保持は w+1（hot）。
- **U死は必ず block 死**（r=h、つまり r≥h）: 敗者位置 t(w+1)−1=n−r−1=n−h−1 は
  監視位置 n−a=n−h−1 に一致し、LAD-GEN の block t の敗者（保持 w）である。
  よって死の保持は w（cold）。

**定理B（V側）.** V死の直後の状態は一様状態 **Z(w+1, n−t)** である
（全員 w+1 保持・pot w+1・人数 n−t・フレーム（ptr円）は位置 n−h+1 から）。

**証明.** r=h−1<h なので J=t−1（block は 1..t−1）。block j の deal は
[(j−1)(w+1), j(w+1)−2]、breaking の deal は [n−r−w−1, n−r−2] = [n−h−w, n−h−2]
（連続: block t−1 の deal の終端 (t−1)(w+1)−2 の次位置 (t−1)(w+1)=n−h−w から
deal が始まり、欠落は block 敗者位置 j(w+1)−1 のみ）。
したがって位置 [0, n−h−1] の残存プレイヤーは block/breaking deal で
ちょうど1回ずつ +1 を受け、元 [w] から **w+1** になる。
breaking の deal 終端は n−h−2 であり tail [n−h, n−1]（h 人・元 [w+1]）
には **触れない**（r=h−1 だから）。除去は block 敗者 t−1 人と breaking 敗者
（=監視、tail 先頭・保持 w+1）の t 人なので残りは **n−t 人**、
その保持は [0, n−h−1] 側も tail 側もすべて w+1 で一様。
pot は死亡保持 w+1、新 ptr は敗者 n−h の次 = 位置 n−h+1。∎

**定理B（U側・非崩壊）.** U block 死（r=h）の後、同一 stretch の breaking 位相が
走り（bl = w−r（r≥1）または w+1（r=h=0, t≥2））、その直後の状態は
**E(w+1; n−t−1−w, w)** である（pot w+1・人数 n−t−1・フレームは bl+1 から、
E 形式 [w+1]^α+[w+2]^w、α=n−t−1−w）。

**証明.** block 死で pot=w（cold）・残り n−t 人（block 敗者 t 人除去、
deal 済み領域 [0, t(w+1)−2] の残存はすべて w+1、tail [n−h, n−1] の h 人は
未 deal で w+1）。ここから同一 stretch の breaking 位相が走る。

- r=h≥1 のとき: breaking deal は [n−r,n)∪[0,w−r) すなわち tail の r 位置と
  先頭の [0, w−r−1]（block 1 deal 済み・w+1→w+2）、敗者 bl=w−r。
  bl は breaking deal に含まれない（deal は [0, w−r)）ので保持 w+1 のまま
  除去され、次 pot は w+1。w+2 保持者は tail r 人 + 先頭 w−r 人 = **w 人**。
- r=h=0, t≥2 のとき: breaking deal は [n,n)∪[0,w) = [0, w−1]
  （block 1 deal 済み・w+1→w+2）、敗者 bl=w+1（block 2 deal 済み・保持 w+1・
  除去され次 pot は w+1）。w+2 保持者は先頭 **w 人**。

いずれも残り人数は n−t−1（block t 人 + breaking 敗者）、w+2 保持者が β=w、
残る w+1 保持者が α=n−t−1−w、フレームは bl+1 から [w+1]^α+[w+2]^w の順で
E(w+1; n−t−1−w, w) を成す。∎

**定理B（U側・崩壊）.** (t,h,r)=(1,0,0) のとき（block 1 の敗者が監視・cold・
n=w+1）、LAD-GEN の collapse 位相（k=w・pot w・q=1・r=0・全員+1→w+2・
敗者位置0）が走り、直後の状態は **Z(w+2, w−1)** である
（全員 w+2・pot w+2・人数 w−1・フレームは位置1から）。∎

備考: (1,0,0) は m≤8000 の範囲で N=p²（p=spf(N) 奇素数）の29ゲームに
ちょうど一致する（§5 P2OBS。全称証明は未着手の観察）。

## 3. 定理C（E-game閉包と生存者位置σ）

**補題C1（E形式の自己保存・任意状態）。** 状態 E(P;α,β)（k=α+β 人・
holdings [P]^α+[P+1]^β・pot P・ptr 先頭）から1フェーズ進むと
（q=P div k・r=P mod k・敗者は ptr 基準位置 r）、

- r<α（pot block 敗者）: **E(P+q; α−r−1, β+r)**・新 pot P+q、
- r≥α（pot+1 block 敗者）: **E(P+q+1; β+2α−r−1, r−α)**・新 pot P+q+1、

である（新フレームは敗者の次から）。この計算は状態局所であり、
K0939 END-INV の帰納段と同一の式が family 入口という仮定なしで
任意の E 状態に成立する。

**補題C2（一様状態→E）。** Z(M,K)（全員 M・pot M）から1フェーズでは
q,r=M div/mod K として敗者位置 r・全員+q・敗者は M+q 保持、
新状態は **E(M+q; K−1−r, r)** である（フレームは r+1 から）。

**定理C3（生存者位置σの再帰）。** E-game E(P;α,β) の最終生存者の
**入口フレームでの位置** σ_E(P,α,β) は次の逆合成で決まる:

- 基底: k=1 で σ=0。
- 各フェーズ（人数 k・敗者位置 r）: 新フレーム位置 e は旧フレーム位置
  (r+1+e) mod k に対応するので、
  **σ_旧 = (r+1+σ_新) mod k**。

同様に **σ_Z(M,K) = (r+1+σ_E(M+q, K−1−r, r)) mod K**。
σ は Josephus 型の有限算術再帰であり、閉形式は現在知らない
（それ自体を決定結果とする。計算量は O(k)）。

E-game の1フェーズが敗者を1人除去することは明らかなので、E/uniform 状態から
の出力「入口フレーム位置 σ のラベルの生存」が決定される。

## 4. 定理D（死亡stretchフレームのラベル合成）と系COMPOSITE-VALUES

**定理D（ラベル合成）。** 合成 N のゲームについて、死亡 stretch
（w,n,t,r,h）開始時点の「フレーム位置→元ラベル」写像 LS は次で与えられる:

- 基底: V はフェーズ1後のフレーム LS[i]=(i+2) mod m（長さ m−1・元ラベル1は
  フェーズ1の敗者）、U は LS[i]=i（長さ m・ゲーム開始フレーム）。
- 生存した各 stretch w′（LAD-GEN）: 除去集合は block 敗者
  { j(w′+1)−1: 1≤j≤J′ } と breaking（または collapse）敗者 bl′ であり、
  新フレームは bl′+1 から並べ直す。この操作を stretch 2..spf(N)−2 に
  適用すると死亡 stretch 開始フレームが得られる。
- 死亡 stretch: 定理B の除去（V: block t−1 敗者 + 監視位置 n−h、
  U 非崩壊: block t 敗者 + bl、U 崩壊: 位置 w と 位置 0）を適用し、
  定理B の起源（V: n−h+1、U: bl+1、崩壊: 1）から並べると死後状態の
  フレーム（ラベル列）が得られる。

**系（COMPOSITE-VALUES）。** 合成 N について、定理B の死後状態で
定理C の σ を計算すると、最終生存者ラベル = frame[σ] である。
すなわち **V(m)/U(m)（合成 N）は純算術で決定される**。
これと K0939 SIEVE-PRIME（素数 N: V(m)=0・U(m)=m−1）を合わせ、
**全 m≥1 の V(m)/U(m) が純算術決定** となる。さらに K0928 定理RED により
**P(C)（全 C≥2）も純算術決定** である。∎

## 5. 機械的証拠（composite_verify.py・audit_build.py）

監査: `output/composite_values_audit.json`（all_ok・cold 2実行 byte 同一・
in-process 2回一致を各 cold 実行内で検証）。`sievegen_core.py` は K0937 の
byte 同一コピー（sha256 a69f916c86ed02d5eeed3d5494bbb0f44f652d0d1e4714c50bbc68bef1843499）。

- **PIN**: K0929 ピン表（sha256 8a3b318b…/58a414bc…・P(1..40) アンカー）。
- **DEATH**: 合成 m≤8000 両側 12,277 ゲーム: tracker status は全て 'died'、
  死亡 stretch w=spf(N)−1、V: r=h−1・保持 w+1、U: r=h・保持 w。
  違反 0（定理A系・定理B二分法の全範囲アンカー）。
- **FULLREPRO**: m≤8000 両側 16,000 値すべて: 純算術 predict（合成は本項、
  素数は SIEVE-PRIME）== ピン値。不一致 0（系COMPOSITE-VALUES の
  エンドツーエンド再構成）。
- **STRUCT**: 合成 m≤1500 両側 2,141 ゲーム: リテラル位置エンジンを
  フェーズごとに走らせ、死後境界の ptr 円ラベル列 == 合成フレーム、
  保持列・pot == 定理B の死後状態（Z/E 形式・値・順序）、
  最終生存者 == frame[σ]。失敗 0（定理B/C/D の構造アンカー。
  engine_run の保持記録は deal 前（pre-deal）である点は実装どおり）。
- **EGAME**: 一般 E 状態（P∈{3,7,12,25,60,120}・k≤50・全 α）8,000 状態強と
  一様状態（M∈{2,3,5,9,20,47}・K≤50）: リテラル状態エンジンの生存者 ==
  σ_E/σ_Z。失敗 0（定理C を family・死後状態の外の一般状態でアンカー）。
- **ENGINE**: m≤600 両側 1,200 ゲーム: 新規 python エンジン play_full の
  生存者ラベル == predict（素数・合成の全 m で一致。K0939 が監視生死のみ
  検証していたのを値レベルへ強化）。
- **P2OBS**（観察・m≤8000）: U 崩壊死 (t,h,r)=(1,0,0) ⟺ N=spf(N)²
  （29例↔29例の全単射）、V 側 N=p² の死亡 stretch 状態は常に
  (n,t,r,h)=(p,1,0,1)。違反 0（全称証明なしの機械観察として明記）。

## 6. 限界・観察・次課題

- σ_E/σ_Z の閉形式は未発見（Josephus 型再帰そのものが決定結果）。
  σ_Z(3,K)（K 偶数、K≤4000）で値1をとる K は豊富に存在し
  （4, 8, 12, 28, 40, 52, 72, …）、単純な倍数構造には乗らない。
- 定理B の U 崩壊ケースと N=p² の一致、V 側 N=p² の死亡状態 (p,1,0,1) は
  観察（§5 P2OBS）。紙上証明は次課題（p² 軌道の h-walk 記述が必要）。
- 定理A の証明は ENTRY-LOC の family h 範囲を本質的に使う。この隙間の
  おかげで素数 N（spf(N)=N では (i)(ii) が失敗し（w+1）²>N を強制できない）
  だけがエンドゲームに到達できる、という綺麗な二分法になる。
- 高次一般化（d 次元版・r 人対戦版の同じ「純算術閉包」）は未開拓。
  本項の構成（ladder 篩→死の二分法→E-game 閉包→ラベル合成）が
  そのまま移植できるかは次のレーンの課題。
- 11×11 などの非一様盤面レーンには直接適用しない（本項は監視縮約ゲーム
  （K0928 RED）の閉包であり、盤面探索の枝刈りには無関係）。
- 備考（他レーンへの連絡）: K0939 実験 dir の `audit_build.py` は
  main 上で中身が監査 JSON と同一になっている（出版時の混入と思われる。
  `output/sieveprime_audit.json` が本体。本項では触っていない）。
