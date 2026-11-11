---
id: K0712
title: 原点と一完全対を固定した安全集合は低側・高側・空対のSATへ厳密還元できる
kind: proposition
status: proved
topics: [geometry, maximum-safe, search-methods]
aliases: []
relations:
- type: depends_on
  target: K0334
  note: 禁止四点から固定完全対dへの直接投影節の定義
- type: generalizes
  target: K0334
  note: 空対0の等号集合から、任意の空対数を持つ固定原点・完全対の集合へ拡張
artifacts:
- path: research/experiments/parabola-ternary-selection-20261109/ternary.py
  role: solver
  note: 直接投影節の点選択への変換と空対数のcardinality制約
- path: research/experiments/parabola-ternary-selection-20261109/ternary_general.py
  role: solver
  note: d を引数化した同符号化の生成器（保存 CNF は d=1323 専用なので必ず再生成する）
- path: research/experiments/parabola-ternary-selection-20261109/regression.py
  role: verifier
  note: 小素数の全三値割当と独立整数幾何の照合、444 cardinalityケースと実証人の再評価
- path: research/experiments/parabola-ternary-selection-20261109/regression.json
  role: data
  note: p=5,7,11,13,17の19392三値割当、無効one-hotと任意の二値簡約への反例
- path: research/experiments/parabola-ternary-selection-20261109/README.md
  role: source
  note: 実装、再現入力・出力、1296点構成と1300点UNKNOWNの範囲
scope: 全奇素数p、h=(p-1)/2、1<=d<=h、0<=k<=h-1。原点と完全対dを含み、他の各対から高々一側を取る安全集合でサイズh+2-k以上の存在。全安全集合の最適化と同一視しない。
evidence: 禁止四点ごとの直接投影を保つ変換の全称証明。有限回帰19392三値割当・444 cardinalityケースは実装の支持検査。
---

## 定義と命題

`Q_p={(t,t² mod p):0<=t<p}` とし、固定点集合を `F={0,d,p-d}` とする。
`i!=d` の各対 `{i,p-i}` から、低側・高側・空対のいずれか一つを選ぶ。
Boolean変数 `L_i,H_i,E_i` にexactly-oneを課し、選択集合を
`S=F ∪ {i:L_i} ∪ {p-i:H_i}` と定義する。

`C_d` は、各禁止四点からFの点を除き、非固定対の両側を要求する場合は捨て、
残る要求点が低側iならリテラル+i、高側p-iなら-iとして作る節の集合。
これはK0334の**禁止四点ごとの直接投影**であり、重複節の除去は許す。
各節の+iを `¬L_i`、-iを `¬H_i` に置き換えたものを `T_d` とする。

このとき、任意の `0<=k<=h-1` について、
**`T_d ∧ exactly-one(L_i,H_i,E_i) ∧ (ΣE_i<=k)` の充足可能性と、
上記形の安全集合Sで `|S|>=h+2-k` が存在することは同値**。
空対0なら元の二値CNFに戻る。

## 全称証明

exactly-oneによって各対の選択は三値と一対一に対応する。
禁止四点に非固定対の両側が含まれる場合、その四点はSに含まれ得ない。
それ以外ではFの点は常に選択済みであり、四点がSに含まれる条件は、
残る全ての要求点の選択変数が真となることに等しい。
これを否定した節は、定義した置換後の節そのものである。
従って全ての置換節を満たすことと、禁止四点を一つも含まないことが同値。
同じ要求を持つ重複節の除去はこの同値を変えない。

非固定対はh-1個で、非空対はちょうど一点を寄与するので
`|S|=3+(h-1)-ΣE_i=h+2-ΣE_i`。これがcardinality制約との同値を与える。
全て空対なら3点のみで常に安全であり、固定形の最適値は
`h+2-min ΣE_i` と書ける。原点を含まない形や完全対のない形まで最適化した値とは限らない。

## 二値の論理簡約を先に適用しない

任意の二値同値CNFへの書換えが、この三値拡張を保つとは限らない。
例えば二値CNF `{x},{¬x}` と `{空節}` はどちらもUNSATだが、前者の置換は
`¬L ∧ ¬H` となり空対Eで充足でき、後者は充足できない。
従って、SATの解消やUNSAT簡約を行う前の、辺ごとの直接投影節を用いる必要がある。
これは抽象CNFの注意例であり、この単位節の組が特定のQ_pから生じるという主張ではない。

## 実装検査と使用範囲

p=5,7,11,13,17の全d・全三値19392割当で、符号化と整数幾何から完全列挙した禁止四点の判定が一致。
one-hotの無効状態を拒否し、sequential counterの444ケースも独立に照合した。
実際の1292点証人を全p=2647符号化へ戻して充足を確認し、別のSAT試行から1296点を構成した（K0711）。
保存 CNF（`target1322-budget3000000/input.cnf.gz`）は **d=1323 でフィルタ済み**の産物であり、別 d では `clauses_for_pair` による再生成が必要。一般 d の生成器と d=1323 でのバイト一致は 2026-11-10 に検証済み（K0723）。
これらは実装回帰であり、上記全称証明とは区別する。
