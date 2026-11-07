---
id: K0693
title: p=2207では剰余放物線の等号A(p)=(p+3)/2を達成する証人が存在しない（計算結果・監査待ち）
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
  target: K0101
  note: 全奇素数での等号を否定する反例候補。監査により確定する
artifacts:
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/README.md
  role: source
  note: 反例候補の方法・証拠・信頼境界・次の監査
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/build_inventory.py
  role: verifier
  note: d=1..1103の判定表を生成し、タイムアウト分は衝突予算2000万で再判定する
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/output/p2207_d_verdicts.json
  role: data
  note: 全1103 dのUNSAT判定と出所（cadicalログ／マルチプロセス／再判定）
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/validate_reduction.py
  role: verifier
  note: p<=23の全安全集合を列挙し、完全対dの集合とCNFのSAT/UNSATを全dで比較する
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/output/reduction_validation.json
  role: data
  note: 7素数の突合結果（全一致）
- path: research/experiments/parabola-equality-extension-2143-2500-20261107/output/witnesses_2143_2500.json
  role: data
  note: 隣接63素数では同じ実装がSAT側で証人を返し独立検証も通っている
scope: 奇素数p=2207のQ_p、標準q=4、等号A(p)=(p+3)/2の不達成。任意の他素数への一般化は主張しない。
evidence: 全1103 dでCNF UNSAT（cadical。4件は衝突予算2000万で再確認）。Glucose4とMinisat22もd=1,289,550,1103でUNSAT。p<=23で全数照合。DRAT証明は未検査。
---

## 命題・範囲

`Q_p = {(t, t² mod p) : 0 <= t < p}` の安全集合（共円・共線四点を含まない部分集合）の最大を `A(p)` とする。
標準 q=4 のこの構成について、**p = 2207 では等号 `A(2207) = (2207+3)/2 = 1105` が成立しない**、
すなわち `A(2207) <= 1104`。

K0097 の上界 `A(p) <= (p+3)/2` は一般に証明済みで、p <= 2143 の全奇素数では等号証人が知られていた。
本項はその範囲外で最初の「等号を達成できない」素数を与える（監査待ち）。
`A(2207)` の正確な値（1104 か、それ未満か）は未確定であり、任意の他素数への一般化も主張しない。

## 現在の根拠

1. サイズ `h+2`（`h=(p-1)/2`）の安全集合は、`0` と **ちょうど一つの完全対 `{d,p-d}`** と
   他の各対 `{i,p-i}` の一側からなる（二完全対は等脚台形で共円、完全対が一つも無ければ
   `|S| <= 1+h = h+1`）。この完全対構造は K0097 の上界証明から初等的に従う。
2. K0334 は等号 `A(p)=h+2` を「ある `d` について signed NAE3/4 と原点節の CNF が充足可能」と
   全奇素数で同値に還元している（証明済み）。
3. したがって `d = 1..h` の全 `d` で CNF が UNSAT なら `A(p) <= h+1 = 1104`。
   p=2207（h=1103）でこれを全数確認した: **UNSAT 1103 件・SAT 0 件・不明 0 件**
   （`output/p2207_d_verdicts.json`）。うち 4 件（d=289, 297, 312, 324）は 30 秒制限で
   タイムアウトしたため衝突予算 2000 万で再判定した。
4. 実装の全数照合: p = 5, 7, 11, 13, 17, 19, 23 で `Q_p` の全安全集合（サイズ `(p+3)/2`）を
   列挙し、完全対 `d` の集合と CNF の SAT/UNSAT を全 `d` で比較した結果、7 素数すべてで一致
   （`output/reduction_validation.json`）。p=23 では安全集合 8,064 個、両者の `d` 集合は `{1,...,11}`。
5. 同一実装は隣接する 63 素数（2003..2477 のうち 2207 を除く）で SAT モデルから等号証人を作り、
   探索と独立な generic 4×4 検証器で共円 0 件を確認している（`witnesses_2143_2500.json`）。
6. 別ソルバ一致: d ∈ {1, 289, 550, 1103} を Glucose4 と Minisat22（衝突予算 2000 万）でも解き、全て UNSAT。

## 限界（監査待ち）

- **UNSAT の DRAT 証明は取得していない**。本項の status は `needs-review` であり、
  「3 ソルバ一致の計算結果」以上の強さでは主張しない。cadical は DRAT を出力できるので、
  証明生成と独立検査が次の監査段階である。
- `A(2207)` の正確な値は未確定。サイズ `h+1` の集合は
  「`0` ＋各対一側（完全対なし）」または「`0` なしで一完全対＋他各対一側」の形になる。
  2026-11-08: 前者の CNF は UNSAT（31,868 節、cadical）で、この形の 1104 石は存在しない。
  後者は d=1103 から約 450 個の d で UNSAT、残りは走査中（`research/log/2026-11-08-p2207-1104-shape-search-and-drat-plan.md`）。
- p=2207 以外の反例素数は未探索（2213..2477 は証人あり、2500 以上は未走査）。
- 監査が通れば K0101 の「全奇素数で等号」は否定される。現時点では K0101 を open のまま維持する。
