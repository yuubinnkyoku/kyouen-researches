---
id: K0951
title: "一般bump-fold閉形式三分法（FOLD-GEN）・rung-2 fold構造とUのmod-5力学的篩（U-RUNG2-FOLD・EXCL-U-MOD5・U-RUNG2-FINAL）・Uセンサス2×10^5拡張"
kind: proposition
status: proved
topics: [variants, multiplayer, strategy-length]
aliases: []
relations:
- type: depends_on
  target: K0941
- type: depends_on
  target: K0945
- type: depends_on
  target: K0948
- type: related
  target: K0946
- type: related
  target: K0949
- type: related
  target: K0950
artifacts:
- path: research/experiments/remo-foldgen-20261118/report.md
  role: proof
  note: "FOLD-GEN（一般bump-foldフレーム(1,c,k,kTop)のO(1)三分法）・RUNG-1/2・EXCL-U-MOD5・Uのmod-5 fold力学的篩の全称証明レポート"
- path: research/experiments/remo-foldgen-20261118/foldgen_core.js
  role: solver
  note: "CommonJS foldエンジン（純JSサンドボックス転写実行・出版pin検証済みsha256Hex）"
- path: research/experiments/remo-foldgen-20261118/foldgen_verify.js
  role: verifier
  note: "純JS検証器（クロスラン再現性はチャンクリストsha ピンE/F/G/H 4本が保証）"
- path: research/experiments/remo-foldgen-20261118/census_extend.js
  role: solver
  note: "Uセンサスの2×10^5拡張掃引機"
- path: research/experiments/remo-foldgen-20261118/composite_core.py
  role: solver
  note: "K0941定理C/D σ再帰のpinned byte同一コピー"
- path: research/experiments/remo-foldgen-20261118/sievegen_core.py
  role: solver
  note: "K0937 committed版byte同一コピー"
- path: research/experiments/remo-foldgen-20261118/output/fast_census.json
  role: data
  note: "U(1..200000)=6,531件のセンサス正本（出版3,658+新規2,873・mod5全体ヒストグラム[2143,1,2216,2171,0]）"
- path: research/experiments/remo-foldgen-20261118/output/foldgen_audit.json
  role: data
  note: "機械的証拠監査バッテリー表（foldgen_grid 428,220事象等）"
date: 2026-11-18
tags: [remo, uniform-board, josephus, fold, closed-form, machine-evidence]
---

一様盤。K0941 定理C/Dの σ 再帰（pinned composite_core.py）・K0945 FOLD/FAST・
K0948 U0-CLASSIFY の上で、K0945 が観察として残した「ONE-CHAR 条件の bump 展開
a=0 ⟺ σ_E(4;3u−4,3)=3u−3」「pot 4,5,… への連分数様再帰」を厳密化・全称化する。

U={u:σ_E(3;0,3u)=1} には 3 つの特徴付けが揃った（三角形）:
**U = ones 軌跡 {u:σ_Z(3,4u)=1}（K0945）= {u:4u+1,6u+1 がともに素数}∪{2}
（K0950）= mod-5 残差篩（本項目）**。
3 定理とも全称証明済みで、直接相互検証（u≤20000、出版ドメイン 3,658 件、
拡張域 2,873 件）はすべて 0 不一致である。

## 主張

### 定理 FOLD-GEN（一般bump-foldの閉形式三分法・全称）

c≥2、a≤b、入口 x の fold σ_ℓ=(σ_{ℓ−1}+c) mod ℓ（ℓ∈[a,b]）、D=x+c(b−a+1)。
**境界 a≥c−1 かつ x≤a−2** で:
(i) D≤b−1 → σ_b=D（全面静寂）; (ii) b≤D≤b+c−2 → σ_b=D−b（b ちょうど
1 wrap）; (iii) D≥b+c−1 → カスケード L₀=max(a,⌈(cb−D)/(c−1)⌉)、
v₀=D+(c−1)L₀−cb∈[0,c−2]、各 bite で m=max(L+1,⌈(cL−v)/(c−1)⌉)、
v←v+(c−1)m−cL、m>b で σ_b=v+c(b−L)。

**証明**。静寂 slack f(ℓ)=ℓ−x−c(ℓ−a+1) は c≥2 で真に単調減少するから
最初の bite レベルは L₀=max(a,⌈(cb−D)/(c−1)⌉)（束縛は ℓ=b）。
L₀−1 の静寂から bite 直前値 u≤L₀+c−2、単一 wrap u<2L₀ は境界 L₀≥c−1
から自動、v₀=u−L₀∈[0,c−2]。x≤a−2 は L₀=a のときの静寂 at a−1 条件。
以後の bite も同型（レベル真に増加・値は [0,c−2] に留まる）。∎

境界は鋭い: 反例 c=5,a=2,b=2,x=0（直接 1、三分法 3）。実 chain では境界は
常に充足し（entry σ≤k−2、bump 後 k≥c−1）、foldGenChecked は境界外 fallback。

### 補題 U-RUNG2-FOLD（全称・u≥2）

σ_E(3;0,3u)=1 ⟺ σ_E(4;3u−4,3)=3u−3。
（第 1 フレーム plain level 3u・addend 4 → E(4;3u−4,3)、
(4+σ′) mod 3u=1 ⟺ σ′=3u−3 の一意性。K0945 ONE-CHAR a=0 の厳密化。）∎

### 定理 RUNG-2 構造（全称・u≥3）

s=⌊(3u−4)/5⌋、a′=(3u−4) mod 5 のとき decomposeE(4,3u−4,3) の最初の
フレームは bump-fold (1,5,k₁,3u−1)、k₁=4s+a′+3、bump 後状態
E(5;4s+2a′−2,4−a′)、入口 σ₅=σ_E(5;4s+2a′−2,4−a′)。
（skip 量 t=⌈(3u−8)/5⌉=s、post-transform の直接計算。）∎

### 定理 U-RUNG2-FINAL + EXCL-U-MOD5（全称・u≥2）

r=u mod 5、j=⌊u/5⌋ として、u∈U ⟺ r∈{0,2,3} かつ
r=0: σ_E(5;12j−4,3)=12j−3 / r=2: σ_E(5;12j+2,2)=12j+3 /
r=3: σ_E(5;12j+2,4)=12j+3。（u=1 は別途 u∈U。）

**証明**。目標 σ_E(4;3u−4,3)=3u−3=5s+a′+1（U-RUNG2-FOLD）。RUNG-2 構造と
FOLD-GEN（境界自動充足）で foldGen(5,k₁,3u−1,σ₅)、D=σ₅+5(s+1)、
b=5s+a′+3 を三分法で評価。(i) 静寂は σ₅=a′−4<0（a′≤3）で不能、
a′=4（r=1）は σ_E(5;12j+2,0)=0 を要求するが K0948 U0-CLASSIFY により
12j+3=3(4j+1) 合成（j≥1）で不能（j=0 は u=1 例外）。(ii) σ₅∈[a′−2,a′+1]
と目標 σ₅=5s+2a′−1 より 5s+a′≤2 → u=2 のみ（r=2, j=0 方程式）。
(iii) カスケードは L₀>k₁ で出力≤5s−2<目標より L₀=k₁ 必須、出力=v₀+5s
と目標比較で σ₅=4s+2a′−1、v₀=a′+1∈[0,3] → a′∈{0,1,2}（r∈{3,0,2}）。
a′=3（r=4）は v₀=4、a′=4（r=1）は v₀=5 で FOLD-GEN の v₀∈[0,c−2] に反し
不能（EXCL）。第 2 bite は m≥5s+a′+4>b 常にで単 bite at k₁。∎

### 系 TERMINAL-BITE（全称・u∈U, u≥3）

u∈U、u≥3 なら rung-2 entry fold は単 bite at k₁（l0IsA）である。
（FINAL 証明 (iii) で r∈{0,2,3} の u≥3 はすべてこのケース。）∎

## 機械的証拠

foldgen_audit.json（純JS、全バッテリー 0 不一致）: foldgen_grid 428,220 evals
（fallback 5,124、不一致 0）、xorshift32 乱数 20,000 点 0、fasteq（実chain
15,104+1,999+3,156+400）0、U-RUNG2-FOLD u∈[2,2000] 0、RUNG-2 構造
u∈[3,2000] 0、FINAL⟺σ_E(3;0,3u)=1 u∈[2,20000] 0（both 951）、
TERMINAL-BITE U∩[3,20000] 950 件違反 0、ONES-CHAR 1,999+標本150点 0、
EXCL 移転 7,999 点 0、FINAL⟺PAIR-3（K0950）u∈[2,20000] 0、
census cross (100k,200k] 素数篩 2,873=2,873 完全一致。
出版ドメイン（deep_census sha ピン一致、3,658 件）: PAIR-3 両方向 0、
rhsOk 3,657 点 0、σ_Z スポット 3,658 点 0、終端 bite 3,656 点全部単 bite、
ABCD 分割 sha 4 本一致。

fast_census.json: U(1..200000)=6,531 件（出版 3,658+新規 2,873）、
mod5 ヒストグラム [2143,1,2216,2171,0]、チャンク E/F/G/H
742/759/709/663 件・リスト sha ピン一致・rhs/終端bite 違反 0。
バケット (100000,200000] 密度 0.02873（直近バケット 0.0316、K0950 の
1/ln² 説明と整合。観察としてのみ記録）。

## 観察

- r=0 方程式 σ_E(5;12j−4,3)=12j−3 は rung-2 目標 σ_E(4;3u−4,3)=3u−3 の
  M:4→5、u→4j 同形（rung-3 篩）。一般 M の rung 篩の帰納的構成が次課題。
  K0950 K0-FAMILY・K0949 relay-prime-m と接続候補。
- u>2×10⁵ の U の外延は K0950 PAIR-3 の素数対掃引が計算量的に優位。
  σ_E 掃引センサスは本項目で完成・役割終了。

## 範囲と限界

- 一様盤のみ。11×11 等の有限盤には言及しない。
- bash/Node 実行環境が本セッションで利用不能だったため、機械的証拠は
  CommonJS スクリプトの純JSサンドボックス転写実行による。
  sha256Hex は出版ピン（空列・hello world）で検証済みの純JS実装、
  チャンクリスト sha ピン（E/F/G/H）がクロスラン再現性を保証する。
  uv check/build・unittest 未実施（歴代 remo 項目と同じ扱い）。
- H チャンクリストのセッション転写で 1 要素の誤植（183338）を検出し、
  素数対集合との対称差から 184338 を復元、修正後 sha がチャンクピン
  3c431924… と一致したことを確認して出版した。
- 密度は全称主張しない。有限検証は全称定理の補助であり、本体は紙上証明。
