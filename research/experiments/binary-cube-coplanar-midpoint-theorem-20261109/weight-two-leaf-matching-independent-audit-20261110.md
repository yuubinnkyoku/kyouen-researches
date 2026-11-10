# 葉近傍完全マッチング補題の独立監査（2026-11-10）

## 対象
既存の「極大 C4 禁止グラフ G に葉 x があれば、支持点 v の近傍 N(v)\{x} が完全マッチングを誘導する」という全称命題。ここでは**証明の追加ではなく、独立した有限完全列挙による照合**のみを行う。

## 独立した判定方法
各 n=4,5,6 のラベル付き単純グラフを全列挙する。任意の異なる二頂点 a,b の共通隣接点が2個以上あれば C4 が存在すると判定する。C4 を含まない G の全欠辺を一本ずつ追加し、すべて C4 を生じるものだけを極大とする。各葉 x の唯一の隣接点 v に対し、集合 S=N(v)\{x} の各 u が S 内でちょうど1個の隣接点を持つことを検査する。これは S の誘導グラフが完全マッチングであることと同値。

## 結果（全ラベル付きグラフ）
| n | 極大 C4 禁止グラフ | 葉の出現数（各グラフ内の葉を加算） | 違反 |
|---:|---:|---:|---:|
| 4 | 12 | 12 | 0 |
| 5 | 87 | 120 | 0 |
| 6 | 1020 | 810 | 0 |

全グラフ数はそれぞれ 2^6, 2^10, 2^15。極大性は全欠辺追加による直接検査、C4 は共通隣接点数による判定であり、葉の局所条件を極大性の判定に使用していない。

## 再現用 Python 3
```python
from itertools import combinations

for n in (4, 5, 6):
    edges = list(combinations(range(n), 2))
    def graph(mask):
        adj = [set() for _ in range(n)]
        for k, (a, b) in enumerate(edges):
            if mask >> k & 1:
                adj[a].add(b)
                adj[b].add(a)
        return adj
    def c4(adj):
        return any(len(adj[a] & adj[b]) >= 2
                   for a, b in combinations(range(n), 2))
    sat = leaves = bad = 0
    for mask in range(1 << len(edges)):
        adj = graph(mask)
        if c4(adj):
            continue
        if any(not (mask >> k & 1) and not c4(graph(mask | (1 << k)))
               for k in range(len(edges))):
            continue
        sat += 1
        for x in range(n):
            if len(adj[x]) != 1:
                continue
            leaves += 1
            v = next(iter(adj[x]))
            S = adj[v] - {x}
            if any(len(adj[u] & S) != 1 for u in S):
                bad += 1
    print(n, sat, leaves, bad)
```

## 証拠境界
n=4..6 の全ラベル付きグラフに対する有限完全列挙である。全次元への一般化は既存の数学的証明に依存する。独立監査は局所条件の取り違えや小次元反例を検出する目的であり、無界の証明の代替ではない。
