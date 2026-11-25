---
id: K0698
title: 道自己畳み込み再帰は最終34周期な任意の強制を周期34へ吸収する（150配置の有限観測・K0684帰納ステップの候補補題）
kind: computation
status: computed
topics: [grundy, residual-games, search-methods]
aliases: []
relations:
- type: depends_on
  target: K0682
  note: 固定核＋長の正確な再帰と有限窓定理。本実験はその再帰の非自己項B(L)を抽象的に直接与える
- type: supports
  target: K0684
  note: 帰納ステップの候補補題（Bが最終34周期なら解も最終34周期）に対する有限証拠。証明ではない
artifacts:
- path: research/experiments/path-recurrence-periodic-forcing-20261108/probe.py
  role: solver
  note: round1。arbitrary/structured各25配置をM=2000で解き最終周期を分類
- path: research/experiments/path-recurrence-periodic-forcing-20261108/probe_stress.py
  role: solver
  note: round2。強制値0..255/0..1023・大きな選択肢集合・より多くの子をM=4000で攻撃
- path: research/experiments/path-recurrence-periodic-forcing-20261108/output/probe.json
  role: data
  note: round1全50配置のonset34・最小末尾周期・最大Grundy。全件が最小周期ちょうど34
- path: research/experiments/path-recurrence-periodic-forcing-20261108/output/stress.json
  role: data
  note: round2全100配置。全件が最小周期ちょうど34・例外なし・最大Grundy27
- path: research/experiments/path-recurrence-periodic-forcing-20261108/README.md
  role: source
  note: 再帰の導出・方法・2 roundの結果・候補補題と限界
scope: 抽象再帰 g(L)=mex(B(L)∪{g(L-2)}∪{g(i)⊕p[L-3-i]:0≤i≤L-3}) について、pは裸の道の34周期Grundy、B(L)は最終34周期な集合値強制。実際の核は列挙しない。
evidence: round1（M=2000,seed20261108）でarbitrary25・structured25の全50配置、round2（M=4000,seed31415926）でarbitrary255×40・structured255×40・arbitrary1023×20の全100配置、計150配置すべてが最終的に最小周期ちょうど34へ収束。例外なし。
---

## 対象と命題（有限計算）

K0684の帰納ステップを幾何から切り出した抽象再帰

\[
 g(L)=\operatorname{mex}\bigl(B(L)\cup\{g(L-2)\}\cup\{g(i)\oplus p_{L-3-i}:0\le i\le L-3\}\bigr)
\]

を考える。`p` は裸の道のGrundy（最終周期34）。`B(L)` は核が与える非自己項
`{A_C⊕p_{L-1},B_C⊕p_{L-2}}∪{f_{C_u}(L)}∪{g(D_u)⊕p_L}` を模型化した集合値関数で、
最終34周期（ある開始以降 `B(L+34)=B(L)`）とする。この有限計算は、`B` を直接与えて
`g` を厳密整数で生成し、末尾の最小周期を分類する。実際の核・幾何は一切列挙しない。

## 方法

2系統の強制を無作為生成する。

- `arbitrary`: `B(L)` はランダムな整数集合（値域・集合サイズ・開始を変える）。開始以降は周期34。
- `structured`: `B(L)={a_k⊕p_{L+s_k}}∪{h_j[L]}`。`a_k` は定数、`s_k` は小シフト、
  `h_j` はランダムな34周期列（子核 `f_{C_u}` の模型）。

`onset34` は `g[L]≠g[L+34]` となる最後の `L` の次。`min_tail_period` は末尾 `TAIL` 項の
最小周期。空強制 `B=∅` を対照とする（34周期・onset53・最大Grundy9を確認）。

## 現在の根拠

- round1（`probe.py`, M=2000, TAIL=600, seed=20261108）: arbitrary 25/25、structured 25/25が
  最終34周期。**最小周期は全50件でちょうど34**（約数1,2,17への縮退なし）。
  onset34はarbitraryで147..768（中央501）、structuredで52..688（中央463）。最大Grundy 9..32。
- round2（`probe_stress.py`, M=4000, TAIL=900, seed=31415926）: 強制値0..255・集合サイズ最大15・
  子最大5のarbitrary255が40/40（onset最大1444）、structured255が40/40（onset最大1610）、
  さらに強制値0..1023・集合サイズ最大25のarbitrary1023が20/20（onset最大1936）。
  **計100件すべて最小周期ちょうど34・例外なし**。強制値を1023まで上げても最大Grundyは27に留まる。

合計150配置すべてが最終的に最小周期ちょうど34へ収束した。onsetの規模（中央値~500、最大1936）は
実際の核（K0682の500、六点純三点辺の637）と同じオーダーである。

## 解釈（候補補題・未証明）

この観測は次の**一般補題の候補**を強く支持する：

> `p` が最終34周期で `B(L)` が最終34周期ならば、上記再帰の解 `g` は最終的に34周期になる。

これが証明されれば、核サイズに関する帰納法でK0684が従う。任意の固定核の非自己項 `B(L)` は、
より小さい核の値 `f_{C_u}(L)`（帰納仮定で最終34周期）と定数⊕道シフトからなるので最終34周期であり、
補題が `g=f_C` の最終34周期を与える。すなわちK0684は幾何のない単一のmex再帰に関する補題へ還元される。
round2は実核よりはるかに広い任意強制（値域1023・大きな集合）でも吸収が壊れないことを示した。

## 限界

本項目は有限個の配置・有限打ち切り長さ（M=2000/4000）の**観測**であり、全称証明でも開始上界でもない。
補題自体は未証明で、K0684も依然 conjectured である。観測は抽象再帰についてのもので、特定の核の
証明書ではない。反例探索は値域・集合サイズ・開始・打ち切り長さをさらに広げてもよいが、本計算は
その有限範囲を完了したことを主張するのみである。裸の道の周期34自体は既知（K0682の文献注記参照）。