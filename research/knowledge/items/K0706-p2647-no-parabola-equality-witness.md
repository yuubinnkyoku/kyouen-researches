---
id: K0706
title: p=2647では剰余放物線の等号A(p)=(p+3)/2を達成できない（全d監査済み）
kind: proposition
status: computed
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
- type: refutes
  target: K0101
  note: 修正版で全dのUNSAT証明を検査した反例により、全奇素数での等号を否定する
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
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/output/drat_audit_full_2647_34249932790a9e9d.json
  role: data
  note: 全1323 dでUNSAT・VERIFIED。修正版検証器ソースSHA-256付き
  commit: b52faa12b77ff8bae9cf5343b20f3561917381a6
- path: research/experiments/parabola-equality-refutation-20261109/receipt_coverage.json
  role: manifest
  note: コミット済み受理記録の完全被覆と実測範囲の独立な整合性確認
scope: 奇素数p=2647のQ_p、標準q=4、等号A(p)=(p+3)/2の不達成。他素数への一般化は主張しない。
evidence: 全1323 dでCNF UNSAT（cadical、衝突予算20万、unknown 0）。さらに全1323 dのDRAT証明を修正版（削除時に代入を失効する）独立検証器で検査し、1323/1323 VERIFIED。
---

## 命題・範囲

`Q_p = {(t, t² mod p)}` の安全集合の最大を `A(p)` とすると、**p = 2647 では
`A(2647) < (2647+3)/2 = 1325`**（すなわち `A(2647) <= 1324`）。
K0693（p=2207）、K0702（p=2531）に次ぐ**3例目の等号不達成**であり、K0101 の
「全奇素数で等号」に対する、有限計算で監査した反例である。`A(2647)` の正確な値は未確定。

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

- **2026-11-09 完了: 全 1323 d の DRAT 証明を修正版検証器（削除時に代入を失効させる）で検査し、
  1323/1323 VERIFIED（失敗 0）**。証明は 10〜52,650 行、検査 0.2〜79.3 秒/件
  （`output/drat_audit_full_2647_34249932790a9e9d.json`）。
  旧検証器の健全性不具合（K0707）を踏まえ、修正版ソースの SHA-256 ごとに新しい監査を行った。
  K0334 の還元と合わせて、p=2647の等号不達成を支える有限計算の監査が完了した
  （status は `computed`）。検証器・符号化・コンパイラ等の実装への依存は残り、Leanによる形式証明ではない。
- `A(2647)` の正確な値は未確定。
  [K0711](K0711-p2647-safe-lower-bound-1292.md) では1301点証人と修正後の1323点全4形状のRUP/LRAT反駁を独立検査し、
  監査済み範囲を1301<=A(2647)<=1322へ強化した。正確値は引き続き未確定。
- p=2647 以外にも、タイムアウトを含む浅い失敗候補が多数あるが、証人を取りこぼした可能性があり
  確定には全数走査が必要。

## 監査データの完全性（2026-11-09 確認）

`output/drat_audit_full_2647_34249932790a9e9d.json` を検査した:

- レコード 1323 件、d は 1..1323 を重複なく被覆（contiguous）。
- 全件 `verified: true`、`solver: UNSAT`、検証器の終了コードはすべて 0。
- 検査時間の合計は 9,969 秒（約 2.8 CPU 時間）。
- 検証器ソースの SHA-256 は `34249932790a9e9d…`（削除時に代入を失効させる修正版）。
