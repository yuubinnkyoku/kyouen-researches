# 反転平面の最小ブロッキング集合と K_q = (q−1)²（宣言・2026-11-24）

## 問題

Miquelian 反転平面 `M(q)`（点 `q²+1`、円 `q+1` 点、3-(q²+1,q+1,1) 設計）の
**ブロッキング集合** `X`（すべての円と交わる点集合）の最小サイズを `τ₁(q)` とする。
K1274 の双対より

```
K_q(q) = q²+1 − τ₁(q)
```

である（`K_q` は「各円と高々 q 点」の最大集合）。

- **既知の下界**: Bruen–Rothschild (1985) が `q ≥ 9` で `τ₁ ≥ 2q`、
  Kiss–Marcugini–Pambianco (2005) が `q ≥ 4` に拡張。
- したがって一般に `K_q(q) ≤ (q−1)²`。
- 本実験の K1275 で `τ₁(4)=8`, `τ₁(5)=10` が厳密（= 2q）と分かっている。
  すなわち q=4,5 では等号が成立し `K_q = (q−1)²`。

**問い**: `τ₁(q) = 2q`（等号）は q ≥ 6 でも成り立つか？
成り立てば `K_q(q) = (q−1)²` が確定する。

## 方法

「サイズ `m` 以下のブロッキング集合」を SAT で探す。

- 変数 `y_p`（点 p を X に入れる）。
- 各円 C に対し被覆節 `∨_{p∈C} y_p`。
- 基数制約 `Σ y_p ≤ m`（sequential counter）。
- `m = 2q` から始め、SAT なら等号確定（下界 2q は既知）。
  UNSAT なら `m` を 1 ずつ増やして上界を更新する。
- 証人は独立チェッカ（全円との交わり）で検証する。

q=4,5 で `m=2q` が SAT になることを較正に使う（既知の厳密値と一致）。

## 成果物

- `scripts/blocking_sat.py`: SAT 探索と証人出力
- `scripts/verify_blocking.py`: SAT 非依存の証人検査
- `output/blocking_q*.json`, `output/results.json`
- `report.md`

## 独立性

- 盤面は出版済み `finite-field-kyouen-20261120/scripts/inversive_fast.py` の
  `build_circles`（SHA-256 記録）で構成。
- SAT はリポジトリ外の一時 venv の `python-sat`。cadical195 と glucose3 の
  2 エンジンで最終判定を確認する。
- 発見したブロッキング集合は `verify_blocking.py`（SAT 非依存）で全円被覆を検査する。

## 文献

- A. A. Bruen, B. L. Rothschild, "Lower bounds on blocking sets",
  *Pacific J. Math.* 118 (1985) 303–311.
- G. Kiss, S. Marcugini, F. Pambianco, "On blocking sets of inversive planes",
  *J. Combin. Des.* 13 (2005) 268–275.

## 結果（2026-11-24、中断時点）

- **較正**: q=4,5 でサイズ 2q のブロッキング集合を SAT が発見。
  `τ_1(4)=8`, `τ_1(5)=10`（2 エンジン、独立検証済み）。
  `K_q = q²+1−2q = (q−1)²` と整合。
- **q=7,8,9,11**: `m=2q`（および q=7 は m=15）の SAT は約 5〜20 CPU 分で
  未解決のまま中断。UNSAT 証明も証人も得られていない。
  → `τ_1(7)` は `14 ≤ τ_1 ≤ 17`（下界は Bruen–Rothschild、上界は貪欲構成）。
- **理論側**: モーメント多項式法（K1292）が q≥9 で `τ_1 ≥ 2q` を証明し、
  q=4..8 では線形計画が `2q−1` で実行可能（この方法の限界）と分かった。
  `τ_1 = 2q` の等号問題は q≥7 で依然オープン。
