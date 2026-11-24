---
id: K1275
title: 反転平面の K_4・K_5 厳密値と s=q 行の下界（SAT 二重実装、q<=9）
kind: computation
status: computed
topics: [geometry, maximum-safe, statistics, search-methods, certificates]
aliases:
- exact K_4 values for inversive planes
- K_s spectrum exact values q<=9
- SAT exact s-arc bounds
relations:
- type: supports
  target: K1274
  note: スペクトル上界 (s-2)(q+1)+2 の非自明例と tight 点（s=q+1, d=q-1）を与える
- type: depends_on
  target: K1058
  note: 反転平面盤の定義・既知の K_3 値と設計パラメータ
- type: related
  target: K1251
  note: K_3（弧）の厳密値・下界データの s 方向への拡張
artifacts:
- path: research/experiments/inversive-spectrum-20261124/scripts/build_board.py
  role: source
  note: 出版済み inversive_fast.build_circles から盤面を構成し設計パラメータを検査（SHA-256 記録）
- path: research/experiments/inversive-spectrum-20261124/scripts/spectrum_sat.py
  role: solver
  note: SAT（cadical195 主、glucose3 副）で K_s を厳密計算。基数制約と3点対称性破りを使用
- path: research/experiments/inversive-spectrum-20261124/scripts/brute_force.py
  role: verifier
  note: SAT 非依存の全探索（q<=5）で K_s を再計算
- path: research/experiments/inversive-spectrum-20261124/scripts/verify_witness.py
  role: verifier
  note: SAT 非依存の証人検査（全円との交点数を盤面 JSON に照合）
- path: research/experiments/inversive-spectrum-20261124/output/spectrum_results.json
  role: data
  note: 厳密値・ソルバ・実行時間・証人パス・双対量 tau_d の正本
- path: research/experiments/inversive-spectrum-20261124/output/bounds_partial.json
  role: data
  note: q=8,9 の部分境界と s=q 行の下界、tau_1 上界
- path: research/experiments/inversive-spectrum-20261124/output/summary.md
  role: data
  note: 人間向けの表
- path: research/experiments/inversive-spectrum-20261124/independent/REPORT.md
  role: log
  note: SAT 非依存の独立実装（C 全探索・分枝限定・独自体模型）による 3 値の再確認
- path: research/experiments/inversive-spectrum-20261124/independent/results.json
  role: certificate
  note: 独立検証の結果（3/3 confirmed, discrepancies 0, 3-推移性 117600/117600, モーメント 200 試行×3）
- path: research/experiments/inversive-spectrum-20261124/independent/verify_all.py
  role: verifier
  note: 独立検証のドライバ（既存 SAT/全探索コードを import しない）
scope: Miquelian 反転平面 M(q)（q 素数冪、q<=9）。s-弧＝各円と高々 s 点で交わる点集合、K_s はその最大サイズ。厳密値は q<=7 と (q,s)=(9,3)、部分境界は (8,4),(9,4)、s=q 行の下界は q=7,8,9。
evidence: q=3,4,5,9 の K_3 は既知値（5,5,6,9）と一致しパイプラインを較正。新規厳密値 K_4(4)=9, K_4(5)=10, K_4(7)=13, K_5(5)=16 は (i) 貪欲証人または SAT モデルの独立証人検査、(ii) 最終 UNSAT の cadical195/glucose3 二重確認、(iii) q<=5 の独立全探索一致、で確定。さらに SAT 非依存の独立実装（独自の体模型で 350/350 円を再構成、C 全探索と分枝限定、q=7 は 3-推移性で固定 3 点）が 3 値を再確認し discrepancies 0（independent/results.json）。q=8,s=4 は 14<=K<=15（n=16,17,18 の UNSAT を cadical195、n=18 を glucose3 でも確認）、q=9,s=4 は 16<=K<=22。s=q 行は k=33,45,57 の明示的 q-弧（各円と q 点以下）で下界。双対 tau_d=q^2+1-K_s は定理 K1274 の d(q+1) 下界と整合（全行で >=）。残余の証人検証は scripts/verify_witness.py による。
---

# 反転平面の K_4・K_5 厳密値と s=q 行の下界（SAT 二重実装、q<=9）

## 計算した量

`K_s(q) = max{|S| : |S∩C| ≤ s for every circle C}`（K1274 のスペクトル）。
`K_3 = K` は既存の弧。本項は `s = 4,5` と `s = q` 行、および `s=3` の較正を扱う。

## 厳密値

| q | s | `K_s` | 上界 `(s-2)(q+1)+2` | 確定方法 |
|---:|---:|---:|---:|---|
| 3 | 3 | **5** | 6 | SAT + 全探索（既知値と一致） |
| 4 | 3 | **5** | 7 | SAT + 全探索 |
| 4 | 4 | **9** | 12 | SAT + 全探索 |
| 5 | 3 | **6** | 8 | 全探索 |
| 5 | 4 | **10** | 14 | SAT + 全探索 |
| 5 | 5 | **16** | 20 | SAT |
| 7 | 4 | **13** | 18 | SAT（2 エンジン） |
| 9 | 3 | **9** | 12 | SAT（既知 K(9)=9 と一致） |

`s = q` 行（`τ_1 = q²+1-K_q`）:

| q | `K_q ≥` | `τ_1 ≤` | 既知下界 `2q` | `(q-1)²` |
|---:|---:|---:|---:|---:|
| 4 | **9**（厳密） | 8（厳密） | 8 | 9 |
| 5 | **16**（厳密） | 10（厳密） | 10 | 16 |
| 7 | 33 | 17 | 14 | 36 |
| 8 | 45 | 20 | 16 | 49 |
| 9 | 57 | 25 | 18 | 64 |

q=4,5 では `τ_1 = 2q`（Bruen–Rothschild 下界が tight）で `K_q = (q-1)²`。

## 部分境界

| q | s | 下界（証人） | 上界（証明） |
|---:|---:|---:|---|
| 8 | 4 | 14 | 15（n=16,17,18 の UNSAT。n=18 は 2 エンジン） |
| 9 | 4 | 16 | 22（定理上界。SAT は n=17 で 90 秒タイムアウト） |

## 方法

- 盤面は出版済み `finite-field-kyouen-20261120/scripts/inversive_fast.py` の
  `build_circles` で構成（SHA-256 を board JSON に記録）。設計パラメータ検査と、
  q<=5 での三重ループ実装 `inversive_all_q` との集合一致を含む。
- SAT: 円ごとの (s+1)-部分集合禁止節 + 基数 `Σx_p ≥ n`（sequential counter）
  + 3 点対称性破り（`∞,0,1` を含むとしてよい; PGL(2,q²) の 3-推移性）。
  貪欲下界から n を上げ、最初の UNSAT で厳密値。
- 最終 UNSAT は cadical195 と glucose3 の 2 エンジンで確認。
- q<=5 は SAT 非依存の全探索 `brute_force.py` と一致。
- 全証人は `verify_witness.py` で盤面 JSON に照合。

## 限界と未確定

- q=8,9 の s=4 は未確定（n=16 の求解は長時間）。
- s=5 以上（q>=7）は基数制約が弱く UNSAT が困難で未計算。
- `τ_1` の上界 17,20,25 は貪欲構成の産物で、最小性は未証明。
- SAT 求解時間はソルバ依存。cadical195 の一部実行はファイル証拠を残していない
  （glucose3 の n=18 は `output/q8s4_second_engine.log`）。
