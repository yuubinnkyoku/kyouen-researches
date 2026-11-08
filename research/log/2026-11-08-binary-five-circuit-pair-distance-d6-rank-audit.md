# 固定二頂点5点回路数公式：6次元での独立階数監査

2026-11-08。最新 main の AGENTS.md、knowledge README、generated/summary.md、および [先行する全次元公式](2026-11-08-binary-five-circuit-pair-distance-all-dimensions-formula.md) を確認した。

## 結果

固定した二頂点のハミング距離を k とする。残りの全3頂点を選び、5点のアフィン階数が4で、各4点部分集合のアフィン階数が4であるものを数えた。星形判定器・先行公式は判定に使用していない。

| d | k=1 | k=2 | k=3 | k=4 | k=5 | k=6 |
|---|---:|---:|---:|---:|---:|---:|
| 5 | 50 | 40 | 40 | 40 | 50 | — |
| 6 | 180 | 110 | 98 | 98 | 110 | 180 |

全11件で先行公式と一致。各 d,k に対し、固定二頂点以外の全3点集合を完全列挙（d=6では各 C(62,3)=37,820件）。ただしこれは **d≤6 の有限独立検査**であり、全次元公式の独立証明ではない。

## 再現コード（Python 3、標準ライブラリのみ）

```python
from itertools import combinations

def rank_mod(rows, p=101):
    a = [list(r) for r in rows]
    rank = 0
    for col in range(len(a[0])):
        piv = next((i for i in range(rank, len(a)) if a[i][col] % p), None)
        if piv is None:
            continue
        a[rank], a[piv] = a[piv], a[rank]
        inv = pow(a[rank][col], -1, p)
        for i in range(rank + 1, len(a)):
            if a[i][col]:
                t = a[i][col] * inv % p
                for j in range(col, len(a[0])):
                    a[i][j] = (a[i][j] - t * a[rank][j]) % p
        rank += 1
        if rank == len(a):
            break
    return rank

def is_circuit(vs, d):
    rows = [[1] + [(v >> i) & 1 for i in range(d)] for v in vs]
    return rank_mod(rows) == 4 and all(
        rank_mod(rows[:i] + rows[i+1:]) == 4 for i in range(5)
    )

for d in (5, 6):
    for k in range(1, d + 1):
        v = (1 << k) - 1
        other = [x for x in range(1 << d) if x not in (0, v)]
        got = sum(is_circuit((0, v) + t, d) for t in combinations(other, 3))
        expected = (
            2 * ((3**k - 3*2**k + 3) // 6)
            + 3**(d-k) - 2**(d-k+1) + 1
            + (2**(k+1) - 4) * (2**(d-k) - 1)
        )
        print(d, k, got, expected)
        assert got == expected
```

階数判定は法101で行う。5行の0/1拡大座標行列の正方小行列式の絶対値は Hadamard の不等式により最大でも 5^(5/2)<101（次数4以下も同様）なので、有理数上の階数と法101の階数は一致する。

## 意義と限界

前回の d≤5 完全列挙とは別の計算経路で、未検査だった d=6 の距離別値を得た。全次元公式は既存の星形定理に依存しており、この検算だけで新たな全称定理にはならない。K6 の7点禁止最大安全サイズの上界も未解決のまま。
