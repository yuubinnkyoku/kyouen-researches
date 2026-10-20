---
id: K0459
title: 無順序二点和からのn点復元はnが2の冪のときに限り非単射
kind: proposition
status: needs-review
topics:
- geometry
- rectangles
- variants
aliases: []
relations:
- type: depends_on
  target: K0342
  note: 同和弦energyの幾何的利用との接続（復元定理の証明自体は独立）
artifacts:
- path: research/experiments/pairsum-reconstruction-20261018/proof.md
  role: proof
  note: Newton恒等式による全称一意性と2の冪の整数反例の再帰構成
- path: research/experiments/pairsum-reconstruction-20261018/verify.py
  role: verifier
  note: Python整数演算による構成・恒等式・有限小例の検査
- path: research/experiments/pairsum-reconstruction-20261018/audit_independent.cpp
  role: verifier
  note: 別初期値からのC++独立検査
- path: research/experiments/pairsum-reconstruction-20261018/audit.json
  role: data
  note: Python実行結果
evidence: 2026-10-20添付統合。元資料では proved または computed と報告（個別の元statusは保存ZIPを参照）。本項目の全量化範囲に対する証明・計算の再監査は未完了。有限検証の実行範囲は統合実験のVALIDATION.mdを参照。
---


> 統合監査: 以下は取込元の主張・報告。全称証明・完全列挙の監査が未完了のため、現在の採用状態は needs-review。本文中の「証明」「一致」は元資料での報告を表す。


# 無順序二点和からのn点復元はnが2の冪のときに限り非単射

## 命題・範囲

`n≥2`、実数n点多重集合 `X` の無順序二点和（添字 `i<j`）を重複度込みで集めた多重集合 `P(X)` は、`n` が2の冪でなければ `X` を一意復元する。`n` が2の冪なら、`P(X)=P(Y)` だが `X≠Y` となる相異なる整数n点集合の組が存在する。

## 証明・限界

`p_k=Σx_i^k`、`Q_k=Σ_{i<j}(x_i+x_j)^k` に対し `2Q_k=(2n−2^k)p_k+Σ_{j=1}^{k−1}C(k,j)p_jp_{k−j}`。nが2の冪でないとき `k≤n` の係数は非零なので、Newton恒等式で元の根の多重集合を復元できる。

逆に2点反例 `{0,3}` と `{1,2}` から、二点和多重集合が等しい `A,B` に対し `A∪(B+t)` と `B∪(A+t)` を作る再帰で、任意の2の冪の反例が得られる。詳細・独立検査は証明資料を参照。

共円ゲームでは `r_X(s)` の一致から `X=Y` を導けるのは、同じ点数が2の冪でない場合に限る。4石・8石の弦多重集合には異なる整数配置が同一になる例がある。これは古典的な二点和復元問題の構造的帰結であり、同じ円の幾何的実現や標準盤の安定化値までは主張しない。
