---
id: K0952
title: σ_Z値1尾部のM-smooth小因子分解と有限素数対族（HIT-TAIL-SMOOTH）
kind: proposition
status: proved
topics: [residual-games, statistics, verification]
aliases: [HIT-TAIL-SMOOTH, FINITE-PRIME-PAIR-UNION, HL-LIVE]
relations:
  - type: depends_on
    target: K0950
    note: HIT-ARITHによる値1判定の算術還元を使う
  - type: generalizes
    target: K0950
    note: PAIR-2/PAIR-3の単一素数対表示を一般M・全live剰余の尾部へ拡張する
artifacts:
  - path: research/experiments/remo-smooth-factor-pair-20261118/report.md
    role: proof
    note: 全称証明と条件付きHardy–Littlewood帰結
  - path: research/experiments/remo-smooth-factor-pair-20261118/verify_smooth_pair.py
    role: verifier
    note: 直接再帰・約数窓走査・有限e和の照合
  - path: research/experiments/remo-smooth-factor-pair-20261118/output/smooth_pair_audit.json
    role: data
    note: 有限監査の固定出力
  - path: research/log/2026-11-18-remo-smooth-factor-pair.md
    role: log
    note: 発見順・反例・次課題
date: 2026-11-18
---

## 命題・範囲

Mを素数、0≤κ≤M−2、t≥max(M,3) とし

\[
K=(M+1)t+\kappa,\quad Y=K+1,\quad k_0=Mt+\kappa-1,
\]
\[
N=MY-1,\quad C=\gcd(M+1,\kappa+2),\quad Q=N/C.
\]

このときC≤M−1で、Qは整数一次式Q(t)=At+B、gcd(A,B)=1となる。値1局面は

\[
\boxed{
\sigma_Z(M,K)=1
\iff
Y\text{ が素数であり、ある }e\ge1\text{ が存在して }
Ce<M,\ e\mid Q(t),\ Q(t)/e\text{ が素数}
}
\]

と完全分類される。eの候補は有限個で \(1≤e≤\lfloor(M−1)/C\rfloor\)。各eはtの一つの剰余類を定め、対応する二つの一次式の同時素数性に帰着する。

## 証明の要点

K0950 HIT-ARITHを使う。t≥M,3からk₀≥M(M−1)、k₀²≥N、Y=M²の例外が尾部から外れる。NのM-smooth部分Dと残余P=N/Dを取る。窓に約数がなければ、M未満素因子の積がM以上に達した最小部分積は高々M(M−1)であるためD<M。またPが合成なら最小素因子はM以上かつ√N以下で窓内に入るのでPは素数で、P>k₀。C|Dよりe=D/Cとすれば主張を得る。逆にCe<MかつQ/eが素数ならN=CePで、P>k₀。従ってNに[M,k₀]内の約数はない。∎

## 条件付き帰結

live候補gcd(κ+1,M+1)=1では、e=1枝の二一次式
\[
L_1=(M+1)t+\kappa+1,\quad L_2=At+B
\]
が全素数pで局所的に許容される。したがって二一次式版Hardy–Littlewood予想の下では各live κに無限個の値1局面がある。P-KILL-TIGHTの無条件証明とは区別する。

## 現在の根拠と限界

紙上証明は全量化範囲を覆う。有限監査はM=2..17の素数・t≤100で4,542状態、直接再帰との不一致0、約数窓とM-smooth分解/e和の不一致0。局所許容性の有限検査はM≤97、p≤1000の64,680組で障害0（全称性の根拠は本文の剰余類証明）。

e>1枝ごとの局所許容性・特異級数、固定Mの完全密度、P-KILL-TIGHTの無条件無限存在は未解決。標準有限盤・11×11の勝敗には言及しない。
