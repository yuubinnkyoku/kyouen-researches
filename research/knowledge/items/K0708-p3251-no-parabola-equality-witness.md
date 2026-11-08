---
id: K0708
title: p=3251でも剰余放物線の等号A(p)=(p+3)/2を達成する証人が存在しない（4例目）
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
  target: K0706
  note: 2647に続く4例目
- type: supports
  target: K0101
  note: 全奇素数での等号を否定する4番目の反例候補
- type: depends_on
  target: K0707
  note: DRAT検証器の削除時代入失効の修正。本項はソルバ主張のみで、DRAT監査は別途
artifacts:
- path: research/experiments/parabola-equality-extension-2143-2500-20261107/output/deep_scan_3251.json
  role: data
  note: d=1625..1の全数走査（UNSAT 1625・unknown 0・SAT 0、4,694秒）
- path: research/experiments/parabola-equality-extension-2143-2500-20261107/scan_mp.py
  role: verifier
  note: マルチプロセス衝突予算スキャナ（4並列、dごとに独立なCNF）
scope: 奇素数p=3251のQ_p、標準q=4、等号A(p)=(p+3)/2の不達成。他素数への一般化は主張しない。
evidence: 全1625 dでCNF UNSAT（cadical、衝突予算20万、unknown 0）。DRAT証明の監査は未実施。
---

## 命題・範囲

`Q_p = {(t, t² mod p)}` の安全集合の最大を `A(p)` とすると、**p = 3251 では
`A(3251) < (3251+3)/2 = 1627`**（すなわち `A(3251) <= 1626`）。
K0693（2207）、K0702（2531）、K0706（2647）に次ぐ**4例目の等号不達成**であり、
K0101 の「全奇素数で等号」に対する四つ目の反例候補である。`A(3251)` の正確な値は未確定。

## 根拠

1. サイズ `h+2`（`h=(p-1)/2`）の安全集合は `0` と一つの完全対 `{d,p-d}` と他の各対の一側に限られ
   （K0097 の上界証明から初等的に従う）、K0334 が等号を「ある `d` について signed NAE3/4 と
   原点節の CNF が充足可能」と全奇素数で同値に還元している。
2. `scan_mp.py`（マルチプロセス、衝突予算 20 万、4 並列）で **d = 1625..1 の全 1625 個**を走査し、
   **UNSAT 1625・SAT 0・不明 0**（`output/deep_scan_3251.json`、4,694 秒）。
3. この素数は「浅い走査で 6 個の d がすべて UNSAT 証明済み（タイムアウト 0）で証人なし」という
   2026-11-08 の交絡訂正で導入した基準で選ばれた候補であり、2647 に続いて同基準から確定した。

## 限界

- **DRAT 証明の監査は未実施**。しかも 2026-11-09 に旧増分検証器の健全性不具合（K0707）が見つかったため、
  本項は「cadical の UNSAT 主張（タイムアウトなし）」の強さでしか主張しない。status は `needs-review`。
- 既存の K0693/K0702 の DRAT 記録も、修正版検証器での再監査が完了するまで独立証拠として採用しない。
- `A(3251)` の正確な値は未確定。
