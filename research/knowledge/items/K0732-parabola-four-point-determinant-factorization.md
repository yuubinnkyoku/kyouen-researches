---
id: K0732
title: 剰余放物線の四点行列式は −(パラメータ和)×Vandermonde 積に合同で、det=0 は共円・共線と同値
kind: proposition
status: proved
topics: [geometry, maximum-safe]
aliases: []
relations:
- type: supports
  target: K0334
  note: K0334 文3 の t³ 係数ルートとは独立な第2証明を与え、等号分解の前提を裏づける
- type: supports
  target: K0731
  note: 捨て規則の和条件
artifacts:
- path: research/experiments/frontier-geometry-2026-10-05/forbidden_edges.cpp
  role: verifier
  note: det() の 3×3 実装（補題A の対象）
- path: research/experiments/frontier-geometry-2026-10-05/proof.md
  role: proof
  note: K0334 側の全称証明（本項とは独立ルート）
- path: research/log/2026-11-10-k0334-identity-verification-omp.md
  role: log
  note: 定理B・系C/D/E/F と p=2647 の会計
scope: 全奇素数 p と Q_p の相異なる四点。一般恒等式は Z 上の全称証明、有限体検査は確認範囲を明記する。
evidence: 補題A と定理B は可換環上の基本変形と Z[t] の UFD 性のみを使う全称証明。有限体全数検査（p=17,29,43,97 の全四点で系C 違反 0、p=17/29/43 の全対で系E 逆 0 件）と p=2647 の会計（928,389 = 874,503 + 53,886、0 を含む辺 4）は独立実装による確認。
---

## 命題

`Q_p={(t,t² mod p)}` の相異なる四点 `q={t_1,…,t_4} ⊂ {0,…,p−1}` について:

(i) 共円・共線判定の 4×4 巡回行列式 `D_cyc = det[x_k²+y_k², x_k, y_k, 1]` は、
第4点で平行移動した 3×3 形 `D_enc = det[Δx_k, Δy_k, Δn_k]`（k=1..3、
`forbidden_edges.cpp:7-16` の `det()`）に可換環上の恒等式として一致する（補題A）。

(ii) パラメータ行列式 `D = det[t_i^{d_j}]`、`(d_1..d_4)=(0,1,2,4)` について、
Z[t_1..t_4] 上で `D = (Σt_i)·V`、`V = ∏_{i<j}(t_j−t_i)`（定理B、整数多項式の恒等式）。

(iii) したがって mod p で `D_cyc(q) ≡ −(Σt_i)·V (mod p)`（系C）。
`D_cyc=0 ⟺ 四点が同一円または同一直線上`（系A1、整数）であり、
相異なる四点では `V ≢ 0 (mod p)` なので `D_cyc≡0 ⟹ Σt ≡ 0 (mod p)`（系C1）。
**逆は偽**（p=17 で和 0 の四点 140 組に対し禁止四点 30 組、p=43 で 2870 対 239）。

系として、完全対を含む禁止四点は二完全対（系D、一般証明）、
二完全対は必ず禁止で台形辺の総数は `C(h,2)`（系E）、
完全対を含まない辺は {0,a,b,c} 型に限られ第四点が一意（系F）。

## 限界

- 証明の確認スクリプト（CAS を使わない独立実装）は repo 外にあり artifact にできない。
  再現は repo 内実装（`forbidden_edges.cpp`）との突合による。
- p=503 の会計突合は未回収。会計の一致を確認したのは p=17, 29, 43, 97, 101, 2647。
- 本項の因数分解は K0334 本文には書かれていない。K0334 の status（proved）は変更不要で、
  同一性を K0334 に書き足す必要はない。
