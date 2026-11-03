---
id: K0664
title: 道型グラフ星共円ゲームの中心付き終局長多項式は全根が負の実数
kind: proposition
status: proved
topics: [geometry, maximal-safe, statistics, strategy-length, variants]
aliases: []
relations:
- type: depends_on
  target: K0602
  note: 中心付き極大配置と支配的削除集合の重み付き全単射を使用
- type: depends_on
  target: K0657
  note: 道の削除区間が内部長1/2・端点長0/1に限られる分類を使用
artifacts:
- path: research/experiments/path-terminal-real-roots-20261103/proof.md
  role: proof
  note: 一般の正重み付き長さ1/2/3敷き詰めの実根定理と道型への全単射・全称証明
- path: research/experiments/path-terminal-real-roots-20261103/verify.py
  role: verifier
  note: 64三方式完全照合・36長い道・64爪なし・315一般重み・745 Newton監査
scope: K0602の整数平面グラフ星型構成でG=P_n（n>=2）、整数q>=4、中心点を含む極大配置の終局長差。さらに任意正実数の位置依存重みを持つ長さ1/2/3タイル敷き詰め。中心なしの極大配置と標準全格子盤は対象外。
evidence: タイルとの重み保存全単射、長さ2/3区間競合グラフの爪なし性、正有理重みの真の双子置換、Chudnovsky–Seymour実根定理、正実重みへの連続性。1,224有限監査は独立検証。
---

# 道型の中心付き終局長分布は実根多項式

K0602の整数点構成でG=P_n、n>=2、q>=4、r=q-3、s=N-(n-1)とする。中心点を含む極大配置のs+k石の個数をa_{n,k}(r)、h=floor((n-1)/2)とすると

\[
\boxed{F_{n,r}(u)=\sum_{k=0}^{h}a_{n,k}(r)u^k\text{ の全根は厳密に負の実数。}}
\]

従って係数は強い対数凹性と単峰性を持ち、中心付き極大配置を一様に選んだ終局長差はh個の独立Bernoulli変数の和と同分布である。

**より一般に、長さLの線分を長さ1・2・3のタイルで敷き詰め、長さ1のタイルに任意の正実重み、長さ2/3のタイルに任意の正実重み×uを与えた多項式は全根が負の実数になる。** 長さ2/3区間の重なりグラフは爪なしで、正有理重みは真の双子置換で重みなし独立集合多項式に還元できる。実重みは極限で従う。

道型では辺位置0,...,n-2をタイルで敷き詰める。長さ2/3タイルは内部の削除区間、長さ1タイルは残存辺または端点削除に対応する。長さ1の重みはn>=3なら両端r+1・内部r、n=2ならr+2。長さ2/3の重みはu。これがK0657の全係数を重み保存で実現する。

全称証明は[proof.md](../../experiments/path-terminal-real-roots-20261103/proof.md)、独立検証は[verify.py](../../experiments/path-terminal-real-roots-20261103/verify.py)。削除集合・タイル・二項和の64条件、長い道36条件、爪なし64条件、不均一重み315条件、Newton不等式745条件の計1,224条件で不一致0。

**中心なしを含めた全分布は実根とは限らない。** P_5,q=4の全極大配置多項式はu^s(4+12u+u²+u³)で判別式-6352<0。K0662のサイクル型と同じく、中心付きに限定した定理である。標準11×11の勝敗やs_n・K_nへの直接の結論ではない。
