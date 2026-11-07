# 10×10 の 20 石安全集合 SAT（2026-11-07）

## 目的

K0141（10×10 で安全 20 石が存在するか）と K0035（19 ≤ K_10 ≤ 23）に対し、
SAT ソルバで「20 点を選び、禁止四点を一つも含まない」を直接解く。
本記録は**探索の試行とその範囲**であり、証人が得られていないことは非存在の証拠ではない。

## 構成

- `forbidden_n10.cpp`: 10×10 の全 4 点組 C(100,4)=3,921,225 を 4×4 行列式
  `|x²+y², x, y, 1|` で判定し、零（共円または共線）の組を列挙する。0.4 秒で **54,441 組**
  （K0057 の記録 `n=10: 54441` と一致）。
- `sat_n10.py`: 変数 1..100、各禁止四点に節 `(¬a ∨ ¬b ∨ ¬c ∨ ¬d)`、基数制約「≥20」を
  sequential-counter（`pysat.card`）で付加。求解後に選択集合を独立な 3×3 差分行列式で全 C(20,4)
  検査する。

## 試行結果

| ソルバ・設定 | 結果 | 時間 |
|---|---|---|
| CaDiCaL（pysat Cadical195）`conf_budget=2,000,000` | UNKNOWN | 228.5 秒 |

- CNF: 100 変数 + 基数補助 1,600 変数、57,581 節。
- 証人は得られず。**K_10 ≥ 20 も K_10 ≤ 19 も確定しない**（UNKNOWN は証明ではない）。

## 再現

```sh
g++ -O3 -std=c++17 forbidden_n10.cpp -o /tmp/forbidden_n10
/tmp/forbidden_n10 > output_quads.txt
uv run --locked --with python-sat python sat_n10.py --atleast 20 --budget 2000000
```

`solve_limited()` は CaDiCaL ラッパでは `interrupt()` 非対応のため `conf_budget` で打ち切る
（True=SAT / False=UNSAT / None=予算超過）。

## 限界

- 予算超過は UNKNOWN であり、UNSAT でも非存在の証明ではない。
- 既存の有界探索（`round57` の近傍削除探索、MILP、以前の Glucose 試行）と同じく、証人未発見のみ。
