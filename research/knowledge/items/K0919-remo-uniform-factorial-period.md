---
id: K0919
title: 一様盤REMO計数再帰のLCM周期性（定理PER・全称証明） — E(C+lcm(1..r),r)=E(C,r) for all C ≥ 1, r ≥ 2・最小周期はr≤9で機械確定・r!は周期だが一般に最小でない
kind: proposition
status: proved
topics: [variants, multiplayer, strategy-length]
aliases: [REMO uniform period, counting recursion lcm periodicity, theorem PER]
relations:
- type: depends_on
  target: K0859
  note: 定理Dの計数再帰（Δ=0一様盤・全称）が本定理の対象。定理Dにより本定理は一様盤REMO全般に転写され、K0859出版表84エントリは双子実装のアンカー
- type: depends_on
  target: K0861
  note: 定理E′（軌道簡約・全称）によりキーのverdictは実現盤面すべてに転写
- type: depends_on
  target: K0906
  note: 定理J（全称・r方向の安定化）との対比: 本定理はC方向の周期性。E6プラトーは定理J帰結の有限アンカー
- type: depends_on
  target: K0881
  note: cap≤12 r=2,7,8 committed列（E5アンカー・ピン照合）
- type: depends_on
  target: K0876
  note: cap≤12 r=3..6 committed列（同上）
- type: depends_on
  target: K0912
  note: cap≤12 r=9 committed列（同上・E5はemb経由のr=9アクセスも使用）
- type: depends_on
  target: K0893
  note: cap≤10 r=9 committed列・K0882順序保存埋め込みの根拠
- type: depends_on
  target: K0895
  note: cap≤10 r=10 committed列（同上）
- type: depends_on
  target: K0897
  note: cap≤10 r=11 committed列（同上）
- type: depends_on
  target: K0898
  note: cap≤10 r=12 committed列（同上）
- type: depends_on
  target: K0902
  note: cap≤10 r=13 committed列（同上）
artifacts:
- path: research/experiments/remo-uniform-factorial-period-20261117/report.md
  role: proof
  note: 定理PERの全称証明（均一オフセット帰納法・補題L/Q・閉形式X_1=T, X_h=T/(k_h+1)）・最小周期r≤9機械測定・定理Jとの対比（r方向安定化 vs C方向周期）・E6プラトー観察・限界・再現
- path: research/experiments/remo-uniform-factorial-period-20261117/verify_remo_uniform_factorial_period.py
  role: verifier
  note: 自己完結・決定的・stdlibのみ・新規スイープなし（入力はsha256ピン留め14本のcommitted packed列のみ・機構はK0859 verbatimブロック+閉形式双子）。7機械チェック全合格・assemble二重実行byte同一・二回cold実行で監査byte同一・所要約140秒
- path: research/experiments/remo-uniform-factorial-period-20261117/output/remo_uniform_factorial_period_audit.json
  role: data
  note: 監査JSON（sha256 75a315f7…・E2/E3/E4のper-r内訳・E6プラトーP(C)列40ピン込み）。本項は新規データ列を出版せずcommitted列の再読みのみ
scope: 'K0859定理Dの計数再帰（Δ=0一様盤・終端サイズC・r人・巡回配分と敗者石除去）について、Q(r)=lcm(1..r)とするとすべてのr ≥ 2とすべてのC ≥ 1でE(C+Q(r),r)=E(C,r)（敗者全列と生存者の完全一致・全称証明・均一オフセット帰納法: 保存条件はr|Tとk(k+1)|T for k=2..r-1で、そのlcmが補題Qによりちょうどlcm(1..r)と一致）。Q(r)の任意の正の倍数も周期で、とくにr!は周期。最小周期はr=2..9で機械的にちょうどQ(r)と確定（Q(r)の全真約数がelim/survivor両列で棄却・完全走査・Q序列2,6,12,60,60,420,840,2520でr!一般には最小でない）。r ≥ 10の最小性と必要性方向（周期は必ずQ(r)の倍数）はOPEN。定理Dにより一様盤REMO全般に転写されるがΔ≠0の非一様盤には一切言及しない。E6プラトー（S(C,r)はr ≥ Cで一定・P(C)列C=1..40）は定理J帰結の有限アンカーおよび観察で閉形式は主張しない。順位の安定性は扱わない。11×11空盤・クラスフロンティアは本項と無関係でUNKNOWNのまま'
evidence: 'verify_remo_uniform_factorial_period.py全チェック合格（7/7・assemble二重実行byte同一・二回cold実行で監査JSON byte同一・sha256 75a315f7…）。入力は14本のcommitted packed列のみ（PIN: sha256・行数・添字連続性・ピンは各出版項目と同一）。E1: K0859 verbatim per-stone再帰==閉形式双子（r=2..7全C∈[1,r!]完全走査+層化r=8,9+出版表84エントリ一致）。E2: 定理PER機械アンカー（Q(r)周期: r=2..9全C∈[1,Q(r)] 3,920ペア完全走査・Q(r)|r!・r!アンカー: r=2..9全C∈[1,r!] 409,112ペア完全走査）。E3: 最小性（r=2..9・Q(r)の全真約数がelim/survivor両列で棄却・完全走査）。E4: 均一オフセット帰納データチェック（T=Q(r)はr=2..9全C・T=r!はr=2..8全C〔r=9のr!データチェックは実行時間のため省略し周期性自体はE2が全走査〕で各フェーズk/t/li/loser/turn同一・counts差==D_h厳密・X_h==T−k_h·D_h・閉形式X_1=T, X_h=T/(k_h+1)・s差==k_h·D_h・受領差==X_h/k_h一様・敗者受領数==q_h〔補題L〕・k_h|X_h・違反0）。E5: 定理Dアンカー（cap≤12 Δ=0 1,512プロファイル×r=2..9の8列+cap≤10 Δ=0 728プロファイル×r=9..13の5列・r=9はK0882埋め込み経由・15,736レコード0不一致・埋め込み15,863位置再現）。E6: プラトー有限アンカー（C≤24・r≤3C+3一定性+P(C)列40ピン）。定理PER本体は全称証明で機械チェックは独立検証アンカー。E1の層化部分とE6は有限観察。r ≥ 10の最小性・必要性方向はOPEN'
---

# 一様盤REMO計数再帰のLCM周期性（全C・全r・全称証明）

## 命題（定理PER・全称）

K0859定理Dの計数再帰 E(C,r)（一様盤・終端サイズC・r人・巡回
配分・敗者石除去）について、**Q(r) := lcm(1,2,…,r)** とおくと:

**定理PER**: すべての r ≥ 2 とすべての C ≥ 1 に対し

> E(C + Q(r), r) = E(C, r)（敗者全列と生存者が完全一致）

が成立（全称証明）。Q(r) の任意の正の倍数も周期で、とくに
r! も周期（Q(r) | r!）。

## 証明（均一オフセット帰納法）

フェーズh開始時に両盤（C と C+T）で active・turn が同一で
counts差が全active者について一様 D_h（D_1 = 0）と置く。配分石数
差 X_h = T − k_h·D_h が k_h で割り切れれば、(1) 商・剰余の配分
パターンが同一（t同一・受領差は全active者ちょうど X_h/k_h）、
(2) 敗者オフセット li が同一（敗者は補題Lによりちょうど q_h 個
受領後に両盤で除去・リセット）、(3) 除去後の turn も同一、で
不変式が保存される。閉形式は D_{h+1} = T/k_h、X_1 = T、
X_h = T/(k_h+1)（h ≥ 2）となり、保存条件は

> r | T（フェーズ1）かつ k(k+1) | T（k = 2..r−1）

でちょうど「T は Q(r) の倍数」と同値（補題Q: この条件集合の
lcmは lcm(1..r) に一致。p^e ≤ r は p^e ≥ 4 なら k = p^e−1 の
k(k+1) が含み、p^e ∈ {2,3} は r 自身または 2·3=6 が含む）。

### 数値と最小周期

Q(2)=2, Q(3)=6, Q(4)=**12**, Q(5)=60, Q(6)=**60**（r!=720より
真に小さい）, Q(7)=420, Q(8)=840, Q(9)=2520。**最小周期は
r = 2..9 で機械的にちょうど Q(r) と確定**（全真約数棄却・
elim/survivor両列・完全走査・E3）。r ≥ 10 の最小性と「周期は
必ずQ(r)の倍数」という必要性方向は OPEN。

## 定理Jとの対比

- 定理J（K0906・全称）は **r 方向の安定化**（sv/det は
  r ≥ max(M,2) で一定）。定理PERは **C 方向の周期性**（周期
  Q(r)）。一様盤の計数再帰は「r方向に有界窓で安定化し、
  C方向に周期 Q(r) で反復する」。
- E6（有限アンカー）: S(C,r) は r ≥ C で一定（C ≤ 24）で、
  P(C) = S(C,C) 列 C=1..40 =
  [0,1,1,3,1,5,1,5,5,9,1,11,1,5,7,15,1,17,1,15,17,21,1,21,11,
  15,7,27,1,29,1,27,17,21,11,35,1,5,7,39] をピン。
  P(C)の閉形式は主張しない。

## 限界

- 本定理は Δ=0一様盤（定理D域）の主張で、非一様盤には一切
  言及しない（K0859の合成反例のとおり）。
- 最小性は r ≤ 9 の機械測定。r ≥ 10 でも Q(r) が周期である
  こと自体は全称証明済み。
- E1 の層化サンプル（r=8,9）と E6 は有限観察。閉形式双子は
  r ≤ 7 完全走査・出版表84エントリ・E5の15,736 committed列
  照合で独立に支持。
- 11×11空盤・クラスフロンティアは本項と無関係でUNKNOWNのまま。

## 再現

`verify_remo_uniform_factorial_period.py`（自己完結・決定的・
stdlibのみ・入力はsha256ピン留め14本のcommitted packed列のみ・
機構はK0859 verbatimブロック+閉形式双子）。7機械チェック全合格・
二回cold実行で監査JSON byte同一（sha256 75a315f7…）。
所要約140秒。
