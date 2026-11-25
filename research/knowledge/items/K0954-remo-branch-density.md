---
id: K0954
title: σ_Z値1尾部の全枝局所許容性・ν分類・特異級数とU_M密度（ALL-ADM・SS-STRUCT・DENSITY-CLASSIFY・U_M-DENSITY）
kind: proposition
status: proved
topics: [residual-games, statistics, verification]
aliases: [ALL-ADM, SS-STRUCT, DENSITY-CLASSIFY, U_M-DENSITY, PRE-TAIL-FIRSTHIT, TAIL-FIRSTHIT-PRED, TAIL-CLEAN]
relations:
  - type: depends_on
    target: K0952
    note: 枝分解HIT-TAIL-SMOOTH・gcd(A,B)=1・枝集合E(M,kappa)の定義を使う
  - type: depends_on
    target: K0950
    note: HIT-ARITH系の記法・SS2/SS3錨・census/FIRSTHIT-GROWTHデータを使う
  - type: generalizes
    target: K0952
    note: e=1枝の局所許容性を全枝へ拡張し特異級数を閉形式化する
  - type: generalizes
    target: K0950
    note: M=2,3のU_M密度積分を一般素数M・全liveクラスへBH条件付きで拡張する
  - type: connects
    target: K0946
    note: STARVATION疎尾部のpre-tail再解釈とlive剰余のクラス構造で接続する
artifacts:
  - path: research/experiments/remo-branch-density-20261118/report.md
    role: proof
    note: 全称証明（ALL-ADM・SS-STRUCT・U_M-DENSITY）と機械結果の正本
  - path: research/experiments/remo-branch-density-20261118/branch_density_core.py
    role: verifier
    note: 枝構造・nu_pair/nu_case・obstructed・特異級数・BH積分・初回ヒット予測の中核実装
  - path: research/experiments/remo-branch-density-20261118/um_sweep.py
    role: verifier
    note: U_M掃引（M<=31）とBH比・テールシーム照合
  - path: research/experiments/remo-branch-density-20261118/census_starvation.py
    role: verifier
    note: census再現・per-kappa再集計・sparse/starvation統計
  - path: research/experiments/remo-branch-density-20261118/firsthit_predict.py
    role: verifier
    note: PRE-TAIL-FIRSTHIT確定とTAIL-FIRSTHIT-PRED二分探索
  - path: research/experiments/remo-branch-density-20261118/audit_build.py
    role: verifier
    note: BRANCH-EXACT・ALL-ADM・SS-FORM・各錨の統合監査
  - path: research/experiments/remo-branch-density-20261118/composite_core.py
    role: verifier
    note: K0950ピン（sha一致・census素数表供用）
  - path: research/experiments/remo-branch-density-20261118/sievegen_core.py
    role: verifier
    note: K0950ピン（sha一致）
  - path: research/experiments/remo-branch-density-20261118/output/branch_density_audit.json
    role: data
    note: 統合監査出力（sha256 541d1aca50fd95b1aaa26d63e2ed3ebac99cd497ab105311dde2d655d528c718・all_ok）
  - path: research/experiments/remo-branch-density-20261118/output/um_sweep.json
    role: data
    note: U_M掃引23行・BH比・枝別計数・seam照合
  - path: research/experiments/remo-branch-density-20261118/output/census.json
    role: data
    note: census 8/8錨・per-kappa計数
  - path: research/experiments/remo-branch-density-20261118/output/starvation.json
    role: data
    note: sparse 69・per-kappa 385・(M,C)群統計
  - path: research/experiments/remo-branch-density-20261118/output/firsthit_pred.json
    role: data
    note: 1,546クラスの初回ヒットとtail予測t_hat
  - path: research/log/2026-11-18-remo-branch-density.md
    role: log
    note: 発見順・1/e修正・反例・次課題
date: 2026-11-18
---

## 命題・範囲

記法はK0952と同一。M素数・0<=κ<=M-2・live: gcd(κ+1,M+1)=1・C=gcd(M+1,κ+2)・
A=M(M+1)/C・B=(M(κ+1)-1)/C・gcd(A,B)=1。枝集合 E(M,κ)={e: 1<=e<=floor((M-1)/C), gcd(e,A)=1}、
各eの枝ペアは Y_e(n)=(M+1)e·n+c1（c1=(M+1)t_e+κ+1）と P_e(n)=A·n+c2（c2=(At_e+B)/e）、
t_e=(-B·A^{-1}) mod e。全n>=0で恒等式 M·Y_e(n)-1=C·e·P_e(n) が成り立つ。

- **TAIL-CLEAN（全称）**: Y=M^2例外（κ=0・t=M-1）はテールt>=t0=max(M,3)に現れない。
  テールではK0952の枝分解とengine判定が完全に一致する（BRANCH-EXACTで機械確認）。
- **ALL-ADM（全称）**: live κの全枝 e∈E(M,κ) について、枝ペアは全素数qで局所許容
  （ν_e(q)=#{n mod q: q|Y_e(n) or q|P_e(n)}<q）。障害は(a)q|(M+1)e∧q|c1、(b)q|A∧q|c2、
  (c)q=2で両根被覆の3形態のみで、(a)はq|M+1側はlive条件・q|e側は恒等式（0≡1矛盾）で、
  (b)はgcd(e,A)=1とgcd(A,B)=1で、(c)はM=2でP_e=(2Y_e-1)/(Ce)が常に奇・M奇では
  c1≡κ+1≡1 (mod 2)で、それぞれ排除される。両形式がmod qで根を共有することはない
  （共通根があれば恒等式で0≡1）。K0952のe=1許容性の全枝一般化。
- **SS-STRUCT（全称）**: ν_e(q)の完全分類。
  ν=0 ⟺ q|M+1 ∧ v_q(C)<v_q(M+1)。ν=1 ⟺ [q|M] ∨ [q|e ∧ q∤M+1] ∨ [q|M+1 ∧ v_q(C)=v_q(M+1)]。
  それ以外（q∤e·M·(M+1)、または該当しない組合せ）はν=2。q=2はM=2でν=1、
  M奇でv_2(C)とv_2(M+1)の比較に帰着（実装nu_caseと同一）。
  系として SS_e = G(M,C) · Π_{q|e, q∤M(M+1)} (q-1)/(q-2)、G(M,C)=SS_{e=1}。
- **DENSITY-CLASSIFY（系・全称）**: ν分類・SS_e・枝の積分形状はκをCのみ経由して決まる。
  BH条件付きでliveクラスのテールヒット密度はC=gcd(M+1,κ+2)のみの関数。
- **U_M-DENSITY（BH条件付き）**: κ=0族の小テールヒット数s（engine事実・t<t0）を足して
  U_M(N) = s + Σ_{e∈E(M,0)} SS_e·∫_0^{(N-t_e)/e} dn/(ln Y_e(n)·ln P_e(n))。
  積分に1/eを掛けない（t側積分のJacobi行列dt=e·dnと剰余類密度1/eが相殺）。K0950の
  「一般MのU_M密度OPEN」をBH条件付きで解決する。
- **PRE-TAIL-FIRSTHIT（有限計算）**: live 1,546クラス（素数M<=199・K<=10^7・tier3素数表）の
  初回ヒットは1,545クラスがテールシームt0未満、唯一の例外(M,κ)=(43,20)はt=43=t0ちょうど
  （シーム上=枝レジーム内）。max t_first/t0=0.923。出版FIRSTHIT-GROWTH
  F~1.767·M^1.5088（R^2=0.8991）は丸ごとpre-tail現象。反例(M,t)=(3,2): engineは
  σ_Z=1だがY=9合成で枝分解は非成立、pre-tailが別レジームであることの実証。
- **TAIL-FIRSTHIT-PRED（BH条件付き）**: 枝レジームのみのBH期待値が1に達する時点t_hat
  （二分探索）は全1,546クラスで有限。median t_hat/t0=1.07（q10=1.04・q90=1.16）、
  M>=100では[1.04,1.11]、小Mではt_hat≫t0（M=2:36.7・M=3:27.3・M=5:2.60）。
  per-M回帰 F_hat=12.77·M^1.4814（R^2=0.9125）は観測Fと指数が一致するがcrossover産物
  （大MでF_hat≈(1.10-1.33)·M^2で観測の2.5-22倍）。within-Mの
  Spearman(ln K_first, ln K_hat)平均=0.095（M>=50: 0.137）で、テール密度はpre-tail
  初回ヒットの順序を予測しない（否定結果）。

## 証明の要点

恒等式 M·Y_e(n)-1=C·e·P_e(n) が中核。共通根があればmod qで0≡1となり両形式は決して
根を共有しない。q|e∧q|c1なら全nでY_e(n)≡0かつCe·P_e(n)≡0から-1≡0、q|Aなら
c2≡B·e^{-1}≢0（gcd(A,B)=1）、q|Mならc2≡-C^{-1}≢0、q|M+1ならc1≡κ+1≢0（live）。
SS因子はν=0がq^2/(q-1)^2・ν=1がq/(q-1)・ν=2がq(q-2)/(q-1)^2で、eの素因子のうち
q∤M(M+1)のものだけがν=2→1に動き因子比(q-1)/(q-2)。全証明はreport.md。

## 機械的証拠（audit_build.py・監査sha256 541d1aca50fd95b1aaa26d63e2ed3ebac99cd497ab105311dde2d655d528c718・2回cold実行byte同一・all_ok）

- **BRANCH-EXACT**: 3,898状態（M∈{2,3,5,7,11,13}・全κ（dead込み）・t∈[t0,120]）で
  engineのσ_Z=1と枝分解判定が不一致0・ヒット213。
- **ALL-ADM**: live 1,546クラス（素数M<=199）・47,907枝のO(1)障害走査（q<=1000）障害0。
  seeded LCG 1,200枝×q<=200のnu_pair全走査54,556照合でobstructed⟺ν=qの不一致0。
- **SS-FORM**: live 1,154枝（M<=60）でnu_case==nu_pair（q<=1000）不一致0。
  129枝の数値SS実積と閉形式の対照: max rel diff 3.48e-7（素数積打ち切り誤差のオーダー）。
- **SS-ANCHORS**: SS_2=3.960971・SS_3=5.281295はK0950出版値と一致。
- **U_M-ANCHORS**: M=3: U=1e5で3,658・U=1e6で25,860（K0950正確カウント一致）。
  M=2: U=66,666で2,025（K0950 DEEP2の2,024+特殊t=1ヒット1）・U=333,333で7,751（7,750+1）。
  テールシーム943状態で小テール終了と積分下限の不一致0。
  BH比 exact/pred: 23行全体0.9501-1.0242、U>=1e5の15行で0.9821-1.0155。
- **CENSUS-ANCHORS**: M∈{3,5,7,11,13,17,19,23}のK<=2e5総ヒット8/8が出版CENSUS-REPROと
  一致（2,057・2,005・2,603・3,003・3,220・3,475・3,629・3,739）。BH総数比0.9776-1.0114。
- **STARVATION再解釈（有限観察）**: 出版sparse 69クラス（K<=2e5でcnt<=2）は全て
  bh_pred_at_2e5=0（min M=991でcensus窓T=floor(2e5/(M+1))<t0=M）。疎尾部は「テール密度が低い」
  のではなく「窓がpre-tailに達しない」現象。p-2型濃縮48/69=69.6%・single-branch 13/69・
  median C/M=0.077はpre-tail側の記述として保存。per-κ再集計（素数M<=100・live 385クラス・
  K<=2e5）: Spearman(count, BH予測)=0.9825・log-log傾斜0.9664。(M,C)群（n>=3・総ヒット>=12）
  44群中35群でvar/mean∈[0.25,3]（Poisson 95%帯）で、DENSITY-CLASSIFYの予測する
  (M,C)群内交換可能性と整合。

## 現在の根拠と限界

- ALL-ADM・SS-STRUCT・TAIL-CLEANは紙上全称証明。機械検証は有限アンカーであり全称性の
  根拠は証明本文のみ。
- U_M-DENSITY・TAIL-FIRSTHIT-PRED・per-κ BH予測はBateman-Horn型予想の枝ペアへの
  条件付き適用。exact/anchor一致・BH比0.98-1.02は有限計算事実であってHLの証拠ではない。
- PRE-TAIL-FIRSTHIT・STARVATION統計は有限観察。pre-tail（t<t0）のσ_Z=1構造と
  FIRSTHIT-GROWTHの冪則の説明は未解決の別レジーム問題。
- P-KILL-TIGHTの無条件無限存在は未解決（BH+ALL-ADMでe=1枝のみで十分という点は
  K0952と不変・全枝許容は密度の話に効く）。
- G(M,C)の閉形式・平均次数、(M,C)群内交換可能性の更なる統計的検定は次課題。
- 11×11空盤・二石root・標準有限盤には言及しない。uv check/buildは本環境にcloneとuvが
  なく未実施（歴代remo項目と同じ扱い）。generated/とroot READMEは未編集。
