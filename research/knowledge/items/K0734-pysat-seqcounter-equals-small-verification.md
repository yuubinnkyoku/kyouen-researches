---
id: K0734
title: pysat の seqcounter による CardEnc.equals は build と同一の呼び出し形で小規模全件「ちょうど bound 個」を満たす
kind: verification
status: verified
topics: [verification, search-methods]
aliases: []
relations:
- type: supports
  target: K0731
  note: 前提(3) の範囲限定格上げ
artifacts:
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/cardenc_verify.py
  role: verifier
  note: 全主割当の拡張可能性を自前 DPLL と Cadical assumption の2系統で判定する照合器
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/output/w15-cardenc-verify.json
  role: data
  note: 473 ケース・1,588,640 割当・不一致 0・構造不変量 0（negative_control は未保存）
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/search_shape_class.py
  role: solver
  note: 照合対象の build() 呼び出し形
scope: pysat 1.9.dev21 の CardEnc.equals（EncType.seqcounter）。単体 variant（contiguous/strided/chained）は n<=12、joint（chained equals の連鎖）は n<=7。一般の n は範囲外。
evidence: 全主割当 1,588,640 件について、主割当の列挙から独立に計算した真値と、2系統の完全判定器（自前 DPLL・Cadical assumption）が一致し、符号化の拡張可能性との不一致は 0。SAT 側 46,414 件と UNSAT 側 1,542,226 件の両方向で一致。
---

## 検証内容

`search_shape_class.build()` と同一の呼び出し形
（`CardEnc.equals(..., encoding=EncType.seqcounter)`、`top_id` 連鎖、
`aux = card_n.nv`）のもとで、pysat 1.9.dev21 の `equals` は
単体 n<=12・連鎖 n<=7 の**全主割当**について
「CNF が補助変数へ拡張可能 ⟺ 主変数上でちょうど bound 個」を満たした
（473 ケース、1,588,640 割当、**不一致 0**）。
補助変数が主変数以下に落ちる件数 `aux_alias_main` と `.nv` を超えるリテラル
`lit_above_nv` はいずれも全 473 ケースで 0。
joint の bound 被覆は c>e 84 件、c<e 84 件、c==e 35 件で、build() が c と e を
独立に与える使い方を両順序とも覆っている。対象は `equals`+`seqcounter` のみ。

## 限界

- 有限範囲の全件照合であり、**一般 n の証明ではない**。実用は h=1323 で、
  検証済み n=12 からの外挿は「同じコード経路が一様に動く」という仮定に立つ。
- **負の対照（検出力）の証拠が保存 JSON に無い**（`negative_control` キー不在）。
  「不一致 0」は符号化の正しさの証拠だが、ハーネスが誤りを検出できることの
  保存された証拠は欠く。真値が独立計算と2系統の判定器で両方向一致しているため
  本項は `verified`（範囲限定）とするが、この留保は残る。
- 前提(4)（ソルバ健全性）には触れない。
- K0712 の regression の 444 cardinality ケースとは別ハーネスであり、包含関係は未確認。
