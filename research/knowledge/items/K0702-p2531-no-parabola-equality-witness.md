---
id: K0702
title: p=2531でも剰余放物線の等号A(p)=(p+3)/2を達成する証人が存在しない（2例目・監査待ち）
kind: proposition
status: needs-review
topics: [maximum-safe, geometry, search-methods]
aliases: []
relations:
- type: depends_on
  target: K0097
  note: 上界A(p)<=(p+3)/2と等号集合の完全対構造
- type: depends_on
  target: K0334
  note: 等号 ⟺ あるdについてsigned NAE3/4と原点節のCNFが充足可能（全奇素数で証明済み）
- type: supports
  target: K0693
  note: 等号不達成がp=2207に限らないことを示す2例目
- type: supports
  target: K0101
  note: 全奇素数での等号を否定する2番目の反例候補
artifacts:
- path: research/experiments/parabola-equality-extension-2143-2500-20261107/output/deep_scan_2531.json
  role: data
  note: d=1265..1の全数走査（UNSAT 1265・unknown 0・SAT 0）
- path: research/experiments/parabola-equality-extension-2143-2500-20261107/scan_mp.py
  role: verifier
  note: マルチプロセス衝突予算スキャナ（8並列、dごとに独立なCNF）
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/validate_reduction.py
  role: verifier
  note: p<=23で符号化と完全対構造の全数照合
- path: research/experiments/parabola-equality-extension-2143-2500-20261107/output/witnesses_2503_2700.json
  role: data
  note: 浅いd走査で2531が最初に落ちた記録
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/output/drat_audit_full_2531.json
  role: data
  note: 標本8 dのDRAT監査結果（全てVERIFIED）
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/drat_check_incremental.cpp
  role: verifier
  note: 増分DRATチェッカー（RUP＋RAT）
scope: 奇素数p=2531のQ_p、標準q=4、等号A(p)=(p+3)/2の不達成。他素数への一般化は主張しない。
evidence: 全1265 dでCNF UNSAT（cadical、衝突予算20万、unknown 0）。標本8 dのDRAT証明は独立チェッカーでVERIFIED（8/8）。
---

## 命題・範囲

`Q_p = {(t, t² mod p)}` の安全集合の最大を `A(p)` とすると、**p = 2531 では
`A(2531) < (2531+3)/2 = 1267`**（すなわち `A(2531) <= 1266`）。
K0693（p=2207）に次ぐ**2例目の等号不達成素数**であり、K0101 の「全奇素数で等号」に対する
二つ目の反例候補である。`A(2531)` の正確な値と他素数への一般化は主張しない。

## 根拠

1. サイズ `h+2`（`h=(p-1)/2`）の安全集合は `0` と一つの完全対 `{d,p-d}` と他の各対の一側に限られ
   （K0097 の上界証明から初等的に従う）、K0334 が等号を「ある `d` について signed NAE3/4 と
   原点節の CNF が充足可能」と全奇素数で同値に還元している。
2. `scan_mp.py`（マルチプロセス、衝突予算 20 万、8 並列）で **d = 1265..1 の全 1265 個**を走査し、
   **UNSAT 1265・SAT 0・不明 0**（`output/deep_scan_2531.json`、3,109 秒）。
3. 同じ実装は隣接する 63 素数（2003..2477 の 2207 を除く）で SAT 側の等号証人を作り、
   探索と独立な generic 4×4 検証器で共円 0 件を確認している。符号化の全数照合は p<=23 で一致（K0693）。

## 限界

- 2026-11-08 の DRAT 監査: 標本 8 個の d（1, 100, 300, 500, 700, 900, 1100, 1265）の証明を
  独立チェッカー（`drat_check_incremental.cpp`）で監査し、**8/8 VERIFIED**
  （証明 14〜157,876 行、検査 1〜367 秒/件、`output/drat_audit_full_2531.json`）。
  全 1265 件の監査は未実施であり、残りはソルバ主張のまま。status は `needs-review`。
- `A(2531)` の正確な値は未確定。
- 同時期の走査で p=2539, 2543, 2549 も d=h..h-30 の範囲で証人が見つかっておらず、
  反例素数は 2207, 2531 以外にも存在する可能性がある（未確定）。
