# 奇数次元の改良 C4 極大構成の独立監査（2026-11-10）

## 対象と証拠水準

[奇数次元の構成](weight-two-odd-dimension-improved-saturation-20261110.md) の有限例を、構成の証明で使われた「長さ3の道」ではなく、**4頂点の誘導・非誘導閉路の直接検出**によって検査する。有限検算は全称証明の代替ではない。

## 独立した検算器（Python 3、標準ライブラリのみ）

```python
from itertools import combinations

def graph(k):
    n = 2*k + 3
    c, x, y = 0, 2*k+1, 2*k+2
    edges = set()
    for i in range(k):
        a, b = 2*i+1, 2*i+2
        edges.update((tuple(sorted(z)) for z in [(c,a),(c,b),(a,b)]))
    edges.add(tuple(sorted((x,1))))
    edges.add(tuple(sorted((y,c))))
    return n, edges

def contains_c4(n, edges):
    # 4点集合の3種類の分割（対角頂点の選択）を直接検査。
    for a,b,c,d in combinations(range(n),4):
        for cycle in ((a,b,c,d),(a,b,d,c),(a,c,b,d)):
            if all(tuple(sorted((cycle[i],cycle[(i+1)%4]))) in edges for i in range(4)):
                return True
    return False

for k in range(1,9):
    n, edges = graph(k)
    assert len(edges) == 3*k+2
    assert not contains_c4(n,edges)
    missing = [e for e in combinations(range(n),2) if e not in edges]
    for e in missing:
        assert contains_c4(n, edges | {e}), (k,e)
    print(n, len(edges), len(missing), "OK")
```

## 手計算による独立照合

最小例 `k=1` は5頂点5辺の閉路 C5 に同型であり、C4 を含まない。C5 の任意の弦を加えると4-cycleが生じるので極大。一般の構成の頂点数は `2k+3`、辺数は `3k+2`、欠辺数は `(2k+3)(k+1)-(3k+2)=2k²+2k+1`。

## 監査上の注意

この検査は元の構成を再実装したもので、元の証明に依存しない C4 判定を用いる。一方、有限範囲での確認にすぎず、一般の奇数次元での最適性や偶数次元への改善を意味しない。実行結果を記録する際には実際に検査器を走らせること。
