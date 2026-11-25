---
id: K0927
kind: proposition
status: proved
title: t=3・q=3w−1純ファイバーゲームの全安全局面Grundy分類
topics: [variants, grundy]
aliases: []
relations:
  - type: depends_on
    target: K0832
    note: K0832の厳密占有縮約と飽和ファイバー鎖分離を用いる。対象は底面跡制約なしの純ファイバーゲーム。
artifacts:
  - path: research/experiments/vertical-fiber-t3-q3w-minus1-grundy-20261118/report.md
    role: proof
    note: 残余三変数再帰、z=0/1の全称閉形式、強帰納証明
  - path: research/experiments/vertical-fiber-t3-q3w-minus1-grundy-20261118/verify_t3_q3w_minus1.py
    role: verifier
    note: ラベル付き・正準多重集合の二方式直接再帰と残余再帰の独立照合
  - path: research/experiments/vertical-fiber-t3-q3w-minus1-grundy-20261118/output/audit.json
    role: data
    note: 140組・2,069,956照合、不一致0、二回実行byte-identical
  - path: research/log/2026-11-18-vertical-fiber-t3-q3w-minus1.md
    role: log
    note: 既存成果との照合、残余再帰の発見、証明・監査・限界
scope: >-
  底面跡制約なし、ファイバー数w>=1、高さm>=1、次数閾値t=3、禁止点数q=3w-1の純ファイバーゲーム。安全条件はΣ_i min(c_i,3)<=3w-2。m>=3では飽和ファイバー鎖XORと残余H(e0,e1,e2)に分解し、m奇数はH=(3e0+2e1+e2-2) mod 2、m偶数はn=e0+e1+e2>=4でH=e1 mod 2、n<=3は有限表で全Grundy値を決定する。m=1,2は独立鎖の直和（w=1,m=2のみ容量で一手短縮）。
evidence: >-
  全称数学的証明は飽和鎖分離、残余mex再帰、n<=3の完全表、Lに関する強帰納による。独立有限監査はラベル付き110,018状態・正準多重集合1,958,310状態・残余再帰1,628状態の計2,069,956照合で不一致0。有限監査は全称性の根拠ではない。
date: 2026-11-18
tags: [vertical-fiber, t3, q3w-minus1, grundy, universal-proof]
---

# K0927: t=3・q=3w−1の全Grundy分類

## 定理

底面跡制約なし、\(w\ge1,m\ge1\)、\(q=3w-1\) とする。安全条件は

\[
\sum_i\min(c_i,3)\le3w-2.
\]

\(m\ge3\) で \(S=\{i:c_i\ge3\}\)、\(X=\bigoplus_{i\in S}((m-c_i)\bmod2)\)、\(e_j=\#\{i:c_i=j\}\ (j=0,1,2)\)、\(n=e_0+e_1+e_2\)、\(L=3e_0+2e_1+e_2\)、\(R=L-2\) と置くと

\[
G(c)=X\oplus H(e_0,e_1,e_2).
\]

- m奇数: \(H=R\bmod2\)。
- m偶数・n>=4: \(H=e_1\bmod2\)。
- m偶数・n<=3: 次の有限表。

| n | H=2 | H=1 |
|---:|---|---|
| 1 | なし | (1,0,0) |
| 2 | (1,1,0),(0,1,1) | (1,0,1) |
| 3 | (1,0,2) | (0,1,2),(0,3,0),(1,1,1),(2,1,0) |

表にない安全状態のHは0。m=1は全配置安全で \(G=\bigoplus_i((1-c_i)\bmod2)\)。m=2,w>=2は全配置安全で \(G=\bigoplus_i((2-c_i)\bmod2)\)。m=2,w=1は安全なc=0,1について \(G=1-c\)。

## 証明の要点

飽和ファイバーは独立鎖としてXOR分離できる。未飽和ファイバーの増分総数 \(L=3e_0+2e_1+e_2\) と残容量は \(R=L-2\) で一致する。占有0→1、1→2、2→3の三手から

\[
H_z=\operatorname{mex}\{H_z(e_0-1,e_1+1,e_2),\
H_z(e_0,e_1-1,e_2+1),\
z\oplus H_z(e_0,e_1,e_2-1)\},
\]

ただし各手は対応する \(e_j>0\) の場合だけ許し、\(L=2\) は終局とする。ここで \(z=(m-3)\bmod2\)。

z=0ではL強帰納で全子値が \((L-3)\bmod2\)、従ってH=R mod2。z=1ではn<=3の18状態を直接mexで閉じる。n>=4はp=e1 mod2と置きL強帰納する。n>=5では全ての合法子が1-pで、少なくとも一手あるためmex=p。n=4では唯一の子例外H(1,0,2)=2が選択肢3を生むが、親(1,0,3)には別の手で選択肢1もあるためmexは0のまま。p=1では全子が0でmex=1。従ってH=e1 mod2。

## 最大値との整合

m奇数では最大値1。m>=4偶数ではw=1で最大1、w=2で最大2、w>=3で最大3。これはK0832の任意t最大値定理と一致するが、本項目は最大値だけでなく全安全局面を分類する。

## 独立監査

ラベル付き直接再帰40組・110,018状態、正準多重集合直接再帰100組・1,958,310状態、残余再帰1,628状態で不一致0。二回の完全実行で監査JSONはbyte-identical（SHA-256 \`89f452b3b57a949b01b24d4cfc784d9aba933fc8e368e27f23fc6c646b5af1d4\`）。有限監査は全称証明の代替ではない。

## 限界

底面跡制約付き、底面係数次数制限付きの部分族、標準二次元共円ゲームの固定幅安定化長は対象外。
