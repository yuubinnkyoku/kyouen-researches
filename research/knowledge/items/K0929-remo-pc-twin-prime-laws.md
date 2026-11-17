---
id: K0929
kind: proposition
status: proved
title: 一様盤P(C)の双子素数法則（P(C)=1 は C 素数と同値、P(C)=C-1 は C+1 素数と同値）
relations:
  - depends_on: [K0859, K0922]
  - connects: [K0919, K0926, K0928, K0937, K0939]
artifacts:
  - research/experiments/remo-pc-twin-laws-20261117/report.md
  - research/experiments/remo-pc-twin-laws-20261117/verify_pc_twin_laws.py
  - research/experiments/remo-pc-twin-laws-20261117/output/pc_twin_laws_audit.json
  - research/experiments/remo-pc-twin-laws-20261117/data/pc_p8000.json
  - research/experiments/remo-pc-twin-laws-20261117/data/pc_uv8000.json
  - research/experiments/remo-pc-twin-laws-20261117/pc_fast.js
  - research/experiments/remo-pc-twin-laws-20261117/pc_reduced.js
date: 2026-11-17
tags: [remo, uniform-board, counting-recursion, survivor, primes, conjecture, machine-evidence]
---

## 昇格（2026-11-18）: LAW1/LAW2は全称定理化

K0939のEND-SIEVE/SIEVE-PRIME全称証明（+K0937合成数側TWIN-COMP-GEN・
K0928定理RED・ピンP(2)=1）により、LAW1/LAW2の完全iff
「P(C)=1 ⟺ C素数」「P(C)=C−1 ⟺ C+1素数」（C≥2）は**全称定理**と
なった。V予想・U予想も定理化。証明チェーンと機械監査はK0939参照。

## 主張（出版時点では予想。すべて有限機械範囲の観察に基づく）

K0922 は C <= 300 で「P(C) = 1 となる C のリストが素数とほぼ一致」することを
観察し、また「P(C) = C-1 となる C が61個ある（構造未同定）」ことを記録した。
本 item は両者を特徴付けの形に昇格する。

### LAW1（生存位置が先頭の法則・予想）

P(C) = 1 と C が素数であることは同値。

### LAW2（生存位置が末尾の法則・予想・新発見）

P(C) = C-1 と C+1 が素数であることは同値。
K0922 の61個のリストは C <= 300 における「C+1 が素数」の C の
リストと完全に一致する（61 = pi(301) - 1 個）。

### V予想・U予想（K0928 経由の同値形）

K0928 の系より LAW1 と LAW2 は次と同値:

- V予想: V(m) = 0 は 2m+1 が素数と同値
- U予想: U(m) = m-1 は 2m+3 が素数と同値

## 機械的証拠（実験→予想の段階。全称証明は未達成）

- 直接 engine（pc_fast.js）で C <= 8000 の P 表を完全計算。
  LAW1: 素数1007個すべて P=1、非素数はすべて P != 1、違反0。
  LAW2: C+1 が素数となる C は1006個、すべて P=C-1、違反0。
- K0928 の定理RED経由で U/V 表（m <= 8000）から C <= 16001 を再構成し、
  両法則を再確認（縮約側でも違反0）。スポット照合は C in
  {8011, ..., 16001} の10点で直接計算と一致（10/10）。
- K0922 の C <= 300 観察を直接側26倍・縮約側53倍に延伸した形。

## 範囲と限界

- 予想であり、全称証明ではない。本 item の機械範囲は
  C <= 8000（直接）と C <= 16001（K0928 縮約経由）まで。
- 検証器 verify_pc_twin_laws.py の10チェック（PIN/REF/TWIN/STRE/STRO/
  RED/RECON/LAWS/REDLAWS/COR）全合格、監査JSONは複数回cold実行で
  byte同一（sha256 6bc2ee08…、詳細は report.md）。
- 素数判定は試し割り（sqrtまで）で、範囲内では厳密。
- 非一様盤には一切言及しない。
