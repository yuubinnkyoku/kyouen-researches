# 二値立方体5点アフィン回路の二頂点同時出現数：距離別の有限完全列挙

2026-11-08。最新main c9d624c2 のAGENTS.md、knowledge README、未解決索引とK0568を確認。既存の対蹠対一意性・固定頂点数とは異なり、**任意の固定二頂点が同じ5点回路に現れる数**を調べた。

## 定義と結果

C_d(k) は d 次元二値立方体のハミング距離 k の固定した相異なる二頂点を**ともに含む**5点アフィン回路の数（対蹠対である必要はない）。立方体の座標置換とビット反転によって距離 k の頂点対は推移的なので値は対の選択によらない。

| d | C_d(1) | C_d(2) | C_d(3) | C_d(4) | C_d(5) |
|---|---:|---:|---:|---:|---:|
| 3 | 2 | 4 | 2 | — | — |
| 4 | 12 | 14 | 14 | 12 | — |
| 5 | 50 | 40 | 40 | 40 | 50 |

**証拠種別：有限完全列挙（d=3,4,5に限る）。全次元公式は主張しない。**

## 再現手順

5点組の全組合せを走査し、各点 v を (1,v_1,...,v_d) に持ち上げた整数行列について、5行の階数が5未満、かつ任意の4行の階数が4であるものを5点アフィン回路と判定する。階数は整数の行基本変形で判定する（浮動小数点なし）。各回路の10頂点対をハミング距離ごとに集計し、距離kの全頂点対数 2^{d-1} binom(d,k) で割る。割り切れることも検査する。

列挙した回路総数は d=3,4,5 でそれぞれ 8,160,2080。整合性の独立した二重計数として
sum_{k=1}^d 2^{d-1} binom(d,k) C_d(k) = 10 N_d
がそれぞれ 80,1600,20800 となる。

これは既存の固定対蹠対が唯一の対蹠対となる回路数 2 S(k,3) とは異なる量である。たとえば d=5,k=1 でも C_5(1)=50。K_6<=9の上界証明には直結しない。今後の独立な回路生成器の距離別検算に利用できる。

## 検査コード（Python 3、外部依存なし）

```python
from itertools import combinations
from collections import Counter
from math import comb

def rank(rows):
    a = [list(row) for row in rows]
    r = 0
    for c in range(len(a[0])):
        pivot = next((j for j in range(r, len(a)) if a[j][c]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        t = a[r][c]
        for j in range(r + 1, len(a)):
            if a[j][c]:
                u = a[j][c]
                a[j] = [t*x-u*y for x,y in zip(a[j],a[r])]
        r += 1
        if r == len(a):
            break
    return r

for d in (3,4,5):
    counts = Counter()
    circuits = 0
    row = lambda v: [1] + [(v >> i) & 1 for i in range(d)]
    for vs in combinations(range(1 << d), 5):
        rows = [row(v) for v in vs]
        if rank(rows) != 4 or any(rank(sub) != 4 for sub in combinations(rows,4)):
            continue
        circuits += 1
        for a,b in combinations(vs,2):
            counts[(a^b).bit_count()] += 1
    by_distance = {k: counts[k] // ((1 << (d-1))*comb(d,k)) for k in range(1,d+1)}
    assert all(counts[k] % ((1 << (d-1))*comb(d,k)) == 0 for k in range(1,d+1))
    assert sum(counts.values()) == 10*circuits
    assert circuits == {3:8,4:160,5:2080}[d]
    print(d, circuits, by_distance)
```
