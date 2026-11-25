---
id: K0349
title: 全q点版の空点・既存石の飽和曲線数は反転とMelchiorで抑えられる
kind: proposition
status: proved
topics: [geometry, variants]
aliases: []
relations:
- type: generalizes
  target: K0107
  note: 空点側q=4の局所被覆上界を全q≥4へ拡張
artifacts:
- path: research/experiments/general-q-local-cover-20261005/proof.md
  role: proof
  note: 空点・既存石を分けた全称証明、端点、最小非自明サイズの整数等号証人
- path: research/experiments/general-q-local-cover-20261005/scripts/verify.py
  role: verifier
  note: 全三点曲線と整数反転直線の独立照合・有限小盤・等号証人検査
- path: research/experiments/general-q-local-cover-20261005/output/audit.json
  role: data
  note: 4×3全4096部分集合q4..8の監査と13個の整数等号証人
scope: 任意の有限実平面q-safe点集合。q点共円・共線を禁止。q≥4。
evidence: 全称反転・Melchior証明。両側k=qで整数配置による等号。
---

# 全q点版の空点・既存石の飽和曲線数は反転とMelchiorで抑えられる

k石のq-safeな任意の実平面点集合Sで、q−1石を持つ円・直線を飽和曲線と呼ぶ。
空点p∉Sを通る飽和曲線数bについて、k≥q≥4なら

\[
 b\le\left\lfloor\frac{\binom k2-3}{\binom{q-1}2+q-4}\right\rfloor.
\]

既存石s∈Sを通る飽和曲線数aについて、k≥q≥5なら

\[
 a\le\left\lfloor\frac{\binom{k-1}2-3}{\binom{q-2}2+q-5}\right\rfloor.
\]

q=4の既存石側は `a=C(k−1,2)` が正確な値。
k≤q−2なら両方0、k=q−1なら両方高々1であり、表示式の非共線性条件を外して使わない。
両式はk=qで1となり、任意qについて明示した整数点集合で等号を達成する。
一般のkで全上界の鋭さは主張しない。

空点側のq=4はK0107の `floor(k(k−1)/6)−1` を再現する。
既存石側は既に安全なq−1石曲線を数えており、空点の追加blockerと同一視しない。
