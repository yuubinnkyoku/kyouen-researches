# 10頂点11辺の C4-飽和候補：葉が3個の場合の有限完全排除（2026-11-11）

## 結論と証拠水準

単純グラフで C4 を含まず、任意の欠辺の追加で C4 が生じるものを C4-飽和とする。**10頂点11辺で葉がちょうど3個の C4-飽和グラフは存在しない。** これは以下の構造補題と **8,568 通りの有限完全列挙**による結論であり、全頂点数についての一般定理ではない。

既存の葉数上界（2026-11-11 の leaf-support-clique 記録）を利用する。異なる葉の支持頂点は異なり、互いに隣接する。3葉の支持頂点 a,b,c は三角形をなす。三角形外の頂点 x が支持頂点のうち2個に接すると、三角形の残る頂点を通る C4 ができるため、x は高々1個の支持頂点に接する。

10頂点を支持頂点 0,1,2、葉 3,4,5（各々 0,1,2 に接続）、その他 6,7,8,9 と固定する。必須辺は支持三角形3辺と葉辺3辺の合計6辺。残る5辺は、その他4頂点内の6候補および支持頂点とその他頂点の12候補から選ぶ以外にない。その他頂点は葉でないので次数2以上でなければならない。従って全候補を **C(18,5)=8,568** 通り列挙すれば完全である。

## 再現用 Python 3（標準ライブラリのみ）

```python
from itertools import combinations

supports = range(3)
outer = range(6, 10)
fixed = {(0, 1), (0, 2), (1, 2), (0, 3), (1, 4), (2, 5)}
optional = list(combinations(outer, 2)) + [
    (a, x) for a in supports for x in outer
]
assert len(optional) == 18

def saturated(edges):
    adj = [set() for _ in range(10)]
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    if any(len(adj[x]) < 2 for x in outer):
        return False
    if any(len(adj[x].intersection(supports)) > 1 for x in outer):
        return False
    # C4 がある iff 異なる二頂点に共通隣接頂点が2個以上ある
    for a, b in combinations(range(10), 2):
        if len(adj[a] & adj[b]) >= 2:
            return False
    # 欠辺 ab の追加で C4 ができる iff a-b 間に長さ3の道がある
    for a, b in combinations(range(10), 2):
        if b in adj[a]:
            continue
        if not any((adj[v] & adj[b]) - {a} for v in adj[a]):
            return False
    return True

tested = found = 0
for choice in combinations(optional, 5):
    tested += 1
    found += saturated(fixed | set(choice))
assert tested == 8568
assert found == 0
print(tested, found)
```

出力：`8568 0`（2026-11-11、Python で実行確認）。

## 限界・次の課題

これは10頂点11辺の不可能性全体を再証明したものではなく、**葉が3個の枝だけを排除**する。残る葉数0、1、2の枝について、同様の固定骨格・次数制約を使った小さな検証を設計する余地がある。独立言語による再検査は未実施。既存の10頂点11辺の完全列挙を置き換えたと主張しない。
