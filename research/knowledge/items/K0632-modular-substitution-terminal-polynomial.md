---
id: K0632
title: 有界商グラフ置換木のq点共円終局長母関数と多項式時間厳密計数
kind: proposition
status: proved
topics: [geometry, maximal-safe, statistics, strategy-length, variants]
aliases: []
relations:
- type: depends_on
  target: K0602
  note: 任意グラフの整数共円実現と支配集合による極大配置公式
- type: generalizes
  target: K0631
  note: 和・完全結合の二分構成木を任意の有界次数商グラフによる置換木へ拡張
artifacts:
- path: research/experiments/modular-substitution-20261102/proof.md
  role: proof
  note: 商グラフの支配集合と内部支配条件による二変数母関数の全称再帰証明
- path: research/experiments/modular-substitution-20261102/verify.py
  role: verifier
  note: 424置換式の直接部分集合照合と103条件の禁止超辺独立完全列挙
- path: research/experiments/modular-substitution-20261102/weighted-total-proof.md
  role: proof
  note: q>=4の終局総数に対する一変数重み付き支配集合再帰と計算量上界
- path: research/experiments/modular-substitution-20261102/verify_weighted_total.py
  role: verifier
  note: q=4,5,6,9の1708条件で直接部分集合列挙と全係数照合
- path: research/experiments/modular-substitution-20261102/amortized-proof.md
  role: proof
  note: 最小共通祖先への一意な課金による全節点償却計算量の全称証明
- path: research/experiments/modular-substitution-20261102/verify_amortized.py
  role: verifier
  note: 全1099順序木形と600乱数木形で課金の重複がないことを独立監査
scope: 少なくとも1辺を持つ有限単純グラフGを、各内部節点が高々k個の非空モジュールを持つグラフ置換式木で与える。任意q>=4のK0602整数共円構成。標準全格子盤は対象外。
evidence: 商グラフ上の支配集合の必要十分条件と誘導辺数の全称恒等式に基づく帰納証明。有限完全列挙は独立監査。
---

# 有界商グラフ置換木で全極大終局長分布を厳密計数

単頂点から始め、各節点で高々k個の非空グラフを任意の商グラフHの頂点へ置換して得られるn頂点グラフGを考える。少なくとも1辺があり、式木が入力として与えられるなら、任意q>=4についてK0602の整数平面上の共円・共線禁止ゲームの全極大配置の石数別母関数を

\[
\boxed{O(2^k k^2 n^{k+4})\text{ 回の整数演算}}
\]

で厳密に計算できる。次数別切片（各子の残存頂点数を固定し、内部辺数は一変数多項式の畳み込みでまとめる）を用い、節点ごとの子の大きさの積を最小共通祖先へ一意に課金する。従来の節点数を一律n倍した上界 O(2^k k² n^{k+5}) を償却で改善した。従来の単項式直積による上界 O(2^k k² n^{3k+1}) から、k≥3で n の指数を2k−3削減した。係数のビット長はO(n+n²log(q+1))。特に固定kでは多項式時間である。

**q=4の極大配置総数のみ**なら、商グラフの支配集合を列挙する再帰により

\[
\boxed{O(2^k k^2 n)\text{ 回の整数演算}}
\]

で計算できる。k=2の和・完全結合の場合はK0631を含み、k=4ではコグラフでない無界木幅族も扱う。

**q>=4の極大配置総数のみ**なら、誘導辺数を次数として保存せず、各残存頂点数aについて重み付き係数を保持する一変数再帰により

\[
\boxed{O(2^k k^2 n^k)\text{ 回の整数演算}}
\]

で厳密計算できる。従来の O(2^k k² n^{k+1}) を最小共通祖先への一意な課金で改善した。k=2のコグラフではO(n²)回。r=q−3とし、支配集合Rの誘導辺数e(R)にr^{e(R)}を掛けて合計すれば、終局総数は1+Σ_{R支配}r^{e(R)}である。再帰式の全称証明と独立検証1708条件は[専用証明](../../experiments/modular-substitution-20261102/weighted-total-proof.md)・[専用検証器](../../experiments/modular-substitution-20261102/verify_weighted_total.py)に保存した。q=4のO(2^k k² n)上界は引き続き有効。

例としてP4の各頂点をK_mへ置換したグラフG_mは誘導P4を持ち、K_(2m)を含むため木幅・頂点被覆数がともに無界である。a=2^m−1とするとq=4の極大配置総数は

\[
\boxed{P_{G_m}(1)=1+4a^2+4a^3+a^4}.
\]

m=1,2,3では10、226、3970通り。全mへの閉式は数学的証明による。

[全称証明](../../experiments/modular-substitution-20261102/proof.md)と[独立検証器](../../experiments/modular-substitution-20261102/verify.py)を保存。4頂点の全64商グラフと360個の置換式（計424条件）、41グラフに対するq4/q5/q6の禁止超辺直接列挙（103条件）、P4クリーク置換m≤3で不一致0。従来の単項式直積方式に加え、次数別切片方式を独立実装して全部分集合列挙と照合した。有限計算を無界命題の証明と混同しない。

全節点を一律に最大サイズnで評価せず、各節点の子の葉数の積を数えると、同じ子数hを持つ節点への総課金は \(\binom{n}{h}\) 以下となる。したがって総数の O(2^k k² n^k)、全分布の O(2^k k² n^{k+4}) は**全称的な償却上界**である。[証明](../../experiments/modular-substitution-20261102/amortized-proof.md)と[独立課金監査](../../experiments/modular-substitution-20261102/verify_amortized.py)を参照。既存の重み付き再帰1708条件の独立照合も維持する。

**限界**：式木の入力を前提とし、kが無界でも多項式時間であるとは主張しない。標準11×11盤の勝敗や一般の全格子盤には直接適用しない。
