---
id: K0682
title: 固定残余核と長道の周期は有限窓で認証でき、5点以下rank3核の全513型は500以降34周期
kind: proposition
status: proved
topics: [residual-games, grundy, geometry, variants, search-methods]
aliases: []
relations:
- type: generalizes
  target: K0680
  note: 特殊な三葉箒から、rank3・5点以下の全固定核と任意長道の分類へ拡張
- type: depends_on
  target: K0108
  note: 全残余辺を更新する通常ゲームと分離成分のxor
- type: depends_on
  target: K0683
  note: 任意個数の三点辺を含む核＋長道を有限整数点盤に全状態実現
- type: supports
  target: K0684
  note: 5点以下の全核について無界長道の34周期が証明済み。大きい核の一般予想は未証明
artifacts:
- path: research/experiments/rooted-core-tail-periodicity-20261107/proof.md
  role: proof
  note: 任意固定核の正確な再帰・有限窓からの全称周期帰納・全5点核の有限帰着
- path: research/experiments/rooted-core-tail-periodicity-20261107/engine.py
  role: solver
  note: 根を保つclutter正規化と有限核DAG・道分解による整数mex
- path: research/experiments/rooted-core-tail-periodicity-20261107/verify.py
  role: verifier
  note: 全6337ラベル付き核の生成と513型の周期証明書、別subset mex11980条件
- path: research/experiments/rooted-core-tail-periodicity-20261107/output/audit.json
  role: certificate
  note: 全513型の0..1069値、最小周期、開始500の鋭さとGrundy最大23
- path: research/log/2026-11-07-rooted-core-and-rank-three-universality.md
  role: log
  note: 四点核から五点核への拡張と、rank3普遍実現との統合
scope: 任意有限clutterの指定合法根に長さLの二点禁止道を付ける通常ゲームの有限周期証明規則。具体的全長分類は辺サイズ2または3・核1..5頂点の全型。標準正方形全格子盤ではない。
evidence: 根を保つ核状態DAGと道分解の全称再帰、有限窓の二重帰納法。全513型で比較500..1035・必要値0..1069を整数確認。原始subset mex11980条件・3020352安全状態で独立照合。
---

## 任意固定核に対する証明規則

指定根を持つ有限残余核Cに、根から長さLの道を二点辺で付けたゲームのGrundyをf_C(L)とする。
核内着手で根が残る子も含めた有限核DAGと、普通の道の列p_Lを考える。

N≥2,T≥1について、pとDAG内の全f_CがN..2N+T+1で周期Tを満たせば、
**全L≥Nで同じ周期が成立する**。必要な有限値は0..2N+2T+1のみ。
これは任意の核で周期が必ず存在するという主張ではなく、周期候補を無限先へ証明する規則である。

核状態間の依存は頂点数を減らすDAG。道内の手は
f_C(i)⊕p_{L−3−i}に分かれ、十分大きい添字対の片側へTを足し引きできる。
長さと核DAGの二重帰納法で選択肢集合の一致を証明する。

## 5点以下・rank3の全核の全長分類

根を0と固定し、1..5頂点の全ラベル付きclutterを生成すると、数は1,2,9,113,6212、計6337。
根付き同型を除くと全513型で、核内着手でもこの型集合に閉じる。

**計算支援全称定理：** 全513型について

\[
 \boxed{f_C(L+34)=f_C(L)\quad(L\ge500).}
\]

各型の最小最終周期も34。一様開始500は最良であり、
核(0..4)、根0、禁止辺{01,02,03,123,14}ではf(499)=4、f(533)=16となる。
全長・全型のGrundyは23以下で、核の禁止マスク(3,12,21,26)、L=141で23を達成する。
4点以下に限ると全47型、最良の一様開始340、Grundy最大18。

N=500,T=34の比較500..1035を、必要な全0..1069整数値で確認した。
全prefixと各型の開始位置は[有限証明書](../../experiments/rooted-core-tail-periodicity-20261107/output/audit.json)に保存する。
K0683により、どの型・長さも標準q=4の有限整数点盤の残局として実現可能である。

## 検証と限界

原始禁止集合から安全占有subsetを列挙する別実装11980条件・3020352安全状態で一致。
この別実装では核cleanup、道の分解、周期表を使わない。
[全称再帰と帰納証明](../../experiments/rooted-core-tail-periodicity-20261107/proof.md)と有限証明書の組合せであり、
単なる長い標本の反復ではない。
6点以上の任意核についての34周期、標準全格子盤の実現、misère版は未証明。
