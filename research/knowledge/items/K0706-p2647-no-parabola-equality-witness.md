---
id: K0706
title: p=2647でも剰余放物線の等号A(p)=(p+3)/2を達成する証人が存在しない（3例目・監査待ち）
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
  note: 等号不達成がp=2207に限らないこと
- type: supports
  target: K0702
  note: 2531に続く3例目
- type: supports
  target: K0101
  note: 全奇素数での等号を否定する3番目の反例候補
artifacts:
- path: research/experiments/parabola-equality-extension-2143-2500-20261107/output/deep_scan_2647.json
  role: data
  note: d=1323..1の全数走査（UNSAT 1323・unknown 0・SAT 0、2,899秒）
- path: research/experiments/parabola-equality-extension-2143-2500-20261107/scan_mp.py
  role: verifier
  note: マルチプロセス衝突予算スキャナ（4並列、dごとに独立なCNF）
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/validate_reduction.py
  role: verifier
  note: p<=23で符号化と完全対構造の全数照合
scope: 奇素数p=2647のQ_p、標準q=4、等号A(p)=(p+3)/2の不達成。他素数への一般化は主張しない。
evidence: 全1323 dでCNF UNSAT（cadical、衝突予算20万、unknown 0）。DRAT証明の監査は未実施。
---

## 命題・範囲

`Q_p = {(t, t² mod p)}` の安全集合の最大を `A(p)` とすると、**p = 2647 では
`A(2647) < (2647+3)/2 = 1325`**（すなわち `A(2647) <= 1324`）。
K0693（p=2207）、K0702（p=2531）に次ぐ**3例目の等号不達成**であり、K0101 の
「全奇素数で等号」に対する三つ目の反例候補である。`A(2647)` の正確な値は未確定。

## 根拠

1. サイズ `h+2`（`h=(p-1)/2`）の安全集合は `0` と一つの完全対 `{d,p-d}` と他の各対の一側に限られ
   （K0097 の上界証明から初等的に従う）、K0334 が等号を「ある `d` について signed NAE3/4 と
   原点節の CNF が充足可能」と全奇素数で同値に還元している。
2. `scan_mp.py`（マルチプロセス、衝突予算 20 万、4 並列）で **d = 1323..1 の全 1323 個**を走査し、
   **UNSAT 1323・SAT 0・不明 0**（`output/deep_scan_2647.json`、2,899 秒）。
3. この素数は「浅い走査で 6 個の d がすべて UNSAT 証明済み（タイムアウト 0）で証人なし」という
   条件で選ばれた唯一の新候補であり、時間のかかる深い d の試行をせずに確定に至った
   （2026-11-08 の交絡訂正で導入した基準）。
4. 同じ実装は隣接する 63 素数（2003..2477 の 2207 を除く）で SAT 側の等号証人を作り、
   探索と独立な generic 4×4 検証器で共円 0 件を確認している。符号化の全数照合は p<=23 で一致。

## 限界

- **DRAT 証明の監査は未実施**。p=2207 では標本 21 d、p=2531 では全 d の監査が進行中（400 件超が
  VERIFIED）。p=2647 の監査はまだ行っていない。status は `needs-review`。
- `A(2647)` の正確な値は未確定。
- p=2647 以外にも、タイムアウトを含む浅い失敗候補が多数あるが、証人を取りこぼした可能性があり
  確定には全数走査が必要。
