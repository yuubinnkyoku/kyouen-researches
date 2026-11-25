---
id: K0677
title: 一辺細分星の終局多項式は全qの奇数次数で接触二重根をもたず、実根数は常に0個か2個
kind: proposition
status: proved
topics: [variants, statistics, geometry, strategy-length]
aliases: []
relations:
- type: depends_on
  target: K0648
  note: 一辺細分星 G_k の全終局長差多項式 T_{k,r} の定義と係数公式
- type: depends_on
  target: K0602
  note: グラフ星型共円構成。本項はその q パラメータ族の実根構造
artifacts:
- path: research/experiments/graph-star-subdivided-star-no-contact-double-root-20261107/proof.md
  role: proof
  note: 接触二重根の不存在（定理A）と単一切替（定理B）の全称証明、有限検査は r=1,2,3 のみ
- path: research/experiments/graph-star-subdivided-star-no-contact-double-root-20261107/verify_no_contact_double_root.py
  role: verifier
  note: 判別式恒等式・M上界・接線上界・約数和条件・閾値表を完全整数／有理数で監査
- path: research/experiments/graph-star-subdivided-star-no-contact-double-root-20261107/output/no_contact_double_root.json
  role: data
  note: r<=1000 の閾値表と各検査の集計
- path: research/experiments/graph-star-subdivided-star-no-contact-double-root-20261107/regress_existing_boundaries.py
  role: verifier
  note: 既発表 q=21..210 の境界表 190 行の再計算一致検査
- path: research/experiments/graph-star-subdivided-star-no-contact-double-root-20261107/output/regression_existing_boundaries.json
  role: data
  note: 190 行の一致監査と各境界の証明方式
- path: research/experiments/graph-star-subdivided-star-general-odd-threshold-20261105/proof.md
  role: proof
  note: 先行の一般論。κ の存在・r 非減少性・発散とデカルトの上界を本項は前提にする
- path: research/log/2026-11-07-subdivided-star-no-contact-double-root.md
  role: log
  note: 発見の経緯と検証範囲
scope: 一辺細分星 G_k（K0648の構成）の全終局長差多項式 T_{k,r}、q>=4（r=q-3）、奇数次数 k>=3。定理Bは r>=2（q>=5）。
evidence: 無限族 r>=4 は代数的全称証明（判別式の平方性、約数和上界、初等的 M 上界）。r=1,2,3 のみ有限検査。
---

## 命題・範囲

一辺細分星 G_k の終局長差多項式（K0648 の構成、K0602 の q パラメータ族）

```
T_{k,r}(u) = u^{k+1} + (r+2) u^k + (r+1)^k u + r (r+1)^{k+1},   r = q-3 >= 1,  k 奇数 >= 3
```

について、次が成り立つ。標準 n×n 格子盤の勝敗・最大安全サイズ・Grundy 値への主張ではない。

- **定理A（接触二重根の不存在）** 任意の整数 `r >= 1` と奇数 `k >= 3` について `T_{k,r}` は重複実根をもたない。
  同値に、`a = (r+2)/(r+1)`、`F_{k,r}(y) = y^k(y-a) + r - y` は `1 < y < a` に `F = F' = 0` の解をもたない。
- **定理B（単一切替）** 任意の整数 `r >= 2` について、奇数 `k` に対する実根数はつねに 0 個か 2 個である。
  `κ(r) = min { 奇数 k >= 3 : min_{1<y<a} F_{k,r}(y) < 0 }` が存在し、`k < κ(r)` では実根 0 個、
  `k >= κ(r)` では相異なる負の単実根がちょうど 2 個。`κ(r)` は `r` について非減少で `r → ∞` に発散する。
- **系（κ の二側評価）** `r >= 4` について `r floor(log2 r) - 1 < κ(r) <= 5(r+1)ceil(log2(r+1))+1`。特に `κ(r) = Θ(r log r)`。
  より精密な二項漸近 `κ(r) = 2r ln r + r ln ln r + (1+ln2)r + o(r)` は K0678 で証明する。

`r = 1`（q=4）は `F(1) = 1 - a < 0` のため定理B の対象外である。実際 `r=1` では `F(0)>0`、`F(1)<0`、`F(a)<0`、`F(y)→+∞`
より常に 2 個の負実根があり、デカルト上界 2 と合わせてちょうど 2 個となる。したがって「実根数は 0 個か 2 個」という
二分法自体は `r >= 1` 全体で成立し、`r = 1` では 0 個の相が現れない。

## 現在の根拠

1. `u = -(r+1)y` による変換で実根は `y > 0` の `F` の根に対応し、負値と根は `1 < y < a` に限られる。
   `F'(y) = y^{k-1}((k+1)y - ka) - 1` は `y_* = ka/(k+1)` まで `<= -1`、以後狭義増加し `F'(a) = a^k - 1 > 0` なので、
   `F'` の正根はただ一つ `y_c ∈ (y_*, a)` にある。
2. 接触条件 `F = F' = 0` から2次式

   ```
   k y^2 - [ (k+1) r + (k-1) a ] y + k a r = 0          ...(B)
   ```

   が従い、その整数係数版の判別式は

   ```
   Δ(r,k) = ( (r^2-2) k + (r^2+2r+2) )^2 - 4 r (r+1)(r+2).
   ```

3. `Δ` が平方でなければ `(B)` は有理数体上既約で、接触点の共役は `F' = 0` の零点でもある。`F'` の正根は一意で共役は接触点と異なるから矛盾。
   よって **接触 ⟹ `Δ` は完全平方**。
4. `Δ` が平方なら `A = (r^2-2)k + (r^2+2r+2)` は `a_0 b_0 = r(r+1)(r+2)` を満たす正整数の和 `a_0 + b_0` であり、
   `A <= 2R + 1/2`、したがって `k < 2r + 9`（`r >= 4`）。
5. `r >= 4` では `M(k) = max_{1<y<a} (a-y)y^k = a^{k+1}k^k/(k+1)^{k+1}` について
   `M(2r+7) < 34/(2r+8) <= 17/8 < r - 4/3 <= r - a` が成り立つので、奇数 `k <= 2r+7` では `F > 0`（根なし）。
   これは 4. の必要条件と矛盾する。
6. `r = 1, 2, 3` は `Δ` が平方とならないことを有限の約数解析で示す（`r=2` は `k <= 19`、`r=3` は `k <= 13`、
   `r=1` は `|5-k|` と差の積が 24 となる約数対の解析で奇数解なし）。
7. `min F` は `k` について狭義単調減少で、固定した `y_0∈(1,a)` では `F_{k,r}(y_0)→-∞` なので `κ(r)` が定まり、定理A より `min F = 0` は起こらない。以上で定理B が従う。
   `κ` の非減少性・発散は先行の一般論（`graph-star-subdivided-star-general-odd-threshold-20261105`）による。
8. 系: 下界は `L = floor(log2 r)`、`k0` を `rL` 以下の最大奇数とし、`M` の `k` 単調性から `k0` のみを評価すればよい。
   `ln M(k0) <= (k0+1)/(r+1) - ln(k0+1) <= L - ln(k0+1) < ln(r-a)`（`r >= 4`、`ln2 < 0.5573 ln r` による）となり `F > 0`。
   よって `κ(r) > rL - 1`。上界は `n = ceil(log2(r+1))`、`k` を `5(r+1)n` 以上の最小奇数とすると
   `M(k) > a^{k+1}/(e(k+1))` と `ln a^{k+1} >= 5 ln(r+1)(1 - 1/(2(r+1)))` から `M(k) > r`、すなわち `F(y_*) < 0`、`κ(r) <= k`。
   `r >= 400` は解析評価、`4 <= r <= 400` は `kappa_two_sided` の両端厳密検査。

## 検証と限界

- 完全整数・有理数演算による監査: 判別式恒等式 1,500 組と `B` の定義式・`G=(r+1)^k F'` の恒等式 2,000 組の一致、
  `M(2r+7) < r-a` の `r=4..4000` 全数、`r<=300` の約数和条件（接触候補 0 件）、
  `r<=200` の許容窓内の平方判別式（0 件）、`κ(r)` 表（`r=2..1000`）、
  系の両端 `r floor(log2 r)-1` と `5(r+1)ceil(log2(r+1))+1` の `4<=r<=400` での厳密証明。
  閾値の境界は `M` 上界または接線上界（`H` の凹性による有理下界）で厳密に処理し、浮動小数点は候補提案にのみ使う。
- 既発表の q=21..210 の境界表 190 行（2026-11-07 追加の q201-q210 を含む）を独立実装で再計算し、全行一致（`k_+` 一致、`k_-` の根なし証明成立）。
- 限界: `κ(r)` の閉形式は未証明（二側評価 `Θ(r log r)` は本項の系）。表は有限範囲。`q=4` は定理B（切替）の対象外で、実根数は常に 2 個。
  終局長分布の単峰性など統計的帰結は本項から直接は従わない。
