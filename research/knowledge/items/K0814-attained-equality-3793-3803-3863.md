---
id: K0814
title: p=3793・3803・3863は等号A(p)=(p+3)/2を達成する（サイズh+2の証人を独立整数幾何で監査）
kind: proposition
status: computed
topics: [maximum-safe, geometry, search-methods]
aliases: []
relations:
- type: depends_on
  target: K0001
  note: 共線・共円四点を含まない安全集合の定義
- type: depends_on
  target: K0771
  note: 禁止四点リストの健全・完全・重複なし（辺の非包含で安全性を判定）
- type: depends_on
  target: K0097
  note: 上界A(p)<=(p+3)/2。本項の証人はこの上界にちょうど到達する
- type: supports
  target: K0101
  note: 3701..3899 には達成側と不達成側が混在することを示す
artifacts:
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/output/witness_h2_3793.json
  role: certificate
  note: 1898点（=h+2、完全対1894）。点は(t,t² mod 3793)
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/output/witness_h2_3803.json
  role: certificate
  note: 1903点（=h+2、完全対1901）
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/output/witness_h2_3863.json
  role: certificate
  note: 1933点（=h+2、完全対1929）
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/output/audit_h2_3793.json
  role: data
  note: 辺0件・独立検証器rc=0の生出力（92.4秒）
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/output/audit_h2_3803.json
  role: data
  note: 辺0件・独立検証器rc=0の生出力（99.3秒）
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/output/audit_h2_3863.json
  role: data
  note: 辺0件・独立検証器rc=0の生出力（83.7秒）
- path: research/log/2026-11-14-new-exceptional-primes-3719-3727.md
  role: log
  note: 3701..3899 の走査全体（達成3・不達成2・未決18）
scope: p=3793, 3803, 3863 の3素数のみ。他の素数での達成は主張しない。
evidence: 3素数ともサイズh+2の点集合を辺リストと独立generic 4x4 Leibniz検証器で二重監査し、edges_inside=0・verifier_rc=0。上界(p+3)/2と合わせてA(p)=h+2が確定する。
---

## 主張

```
A(3793) = 1898 = h+2 = (p+3)/2
A(3803) = 1903 = h+2 = (p+3)/2
A(3863) = 1933 = h+2 = (p+3)/2
```

3素数とも一般上界（K0097）にちょうど到達する。**等号達成**である。

## 根拠

- サイズ `h+2` の集合は `(x,c,e) = (1,1,0)` の一クラス（原点＋一完全対＋各対一側）。
- `d` を固定した走査（`probe_driver.py`、各 d 45秒）で証人を発見:
  - p=3793: `d = 1894`、1898点
  - p=3803: `d = 1901`、1903点
  - p=3863: `d = 1929`、1933点
- 3件とも `audit_safe_set.py` で二重監査: 禁止四点リストに全包含される四点が 0 件、
  独立 generic 4×4 Leibniz 検証器が受理（`verifier_rc=0`、83〜99秒）。
- 上界 `A(p) <= (p+3)/2` は K0097 で証明済みなので、下界と合わせて等号が確定する。

## 位置づけ

3701..3899 の 23 素数を浅い走査で調べた結果:

| 判定 | 個数 | 素数 |
|---|---|---|
| 達成 | 3 | 3793, 3803, 3863 |
| 不達成（証明書つき） | 2 | 3719, 3727（K0812） |
| 未決 | 18 | 残り |

**同じ範囲に達成側と不達成側が混在している**。不達成素数は「例外的に密集している」のではなく、
散在していることが分かる。

## 限界

- 3素数についての主張のみ。3701..3899 の未決18素数やその他の範囲については何も言わない。
- 単一CNF国勢調査（30万衝突）では3素数とも unknown だった。SAT 側は `d` 固定走査の方が速い。
