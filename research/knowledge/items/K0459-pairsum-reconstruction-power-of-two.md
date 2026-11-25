---
id: K0459
title: 無順序二点和からのn点復元はnが2の冪のときに限り非単射
kind: proposition
status: proved
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
- path: research/experiments/knowledge-audit-20261021/README.md
  role: log
  note: 証明の論理監査・再実行範囲・判定
evidence: '2026-10-21監査。Newton恒等式の非零係数と区間分離による反例倍増構成を確認。PythonとC++を再実行。 監査記録: research/experiments/knowledge-audit-20261021/README.md。'
---


# 無順序二点和からのn点復元はnが2の冪のときに限り非単射

## 命題・範囲

`n≥2`、実数n点多重集合 `X` の無順序二点和（添字 `i<j`）を重複度込みで集めた多重集合 `P(X)` は、`n` が2の冪でなければ `X` を一意復元する。`n` が2の冪なら、`P(X)=P(Y)` だが `X≠Y` となる相異なる整数n点集合の組が存在する。

## 証明・限界

`p_k=Σx_i^k`、`Q_k=Σ_{i<j}(x_i+x_j)^k` に対し `2Q_k=(2n−2^k)p_k+Σ_{j=1}^{k−1}C(k,j)p_jp_{k−j}`。nが2の冪でないとき `k≤n` の係数は非零なので、Newton恒等式で元の根の多重集合を復元できる。

逆に2点反例 `{0,3}` と `{1,2}` から、二点和多重集合が等しい `A,B` に対し `A∪(B+t)` と `B∪(A+t)` を作る再帰で、任意の2の冪の反例が得られる。詳細・独立検査は証明資料を参照。

共円ゲームでは `r_X(s)` の一致から `X=Y` を導けるのは、同じ点数が2の冪でない場合に限る。4石・8石の弦多重集合には異なる整数配置が同一になる例がある。これは古典的な二点和復元問題の構造的帰結であり、同じ円の幾何的実現や標準盤の安定化値までは主張しない。
