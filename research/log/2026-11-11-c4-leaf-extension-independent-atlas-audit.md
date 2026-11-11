# C4飽和グラフの葉削除・追加定理：独立有限照合（2026-11-11）

## 対象と結論

既存の `research/log/2026-11-11-c4-saturation-leaf-deletion-extension-iff.md` の必要十分条件を、元グラフ H が3〜7頂点の場合について、NetworkX graph_atlas_g() の非同型単純グラフ全件と各頂点 a に対して照合した。

- 検査対象: (H,a) 合計 **8,470組**（非同型 H の各頂点を a として試す）。
- 条件の両辺が真: **30組**。
- 不一致: **0組**。
- 証拠水準: **有限完全照合**（7頂点以下の非同型グラフ全件について）。一般の必要十分性は既存の数学的証明によるもので、本計算から一般化していない。

元の証明をそのまま再実装するのでなく、C4不在を「異なる2頂点が共通隣接点を2つ持たない」で判定し、欠辺の飽和性を「長さ3の単純路がある」で直接判定した。葉を追加した G に対する判定と、H に対する条件判定は別々に実施した。

## 再現コード

```python
import networkx as nx

def saturated(g):
    vertices = list(g)
    adj = {v: set(g[v]) for v in vertices}
    # C4 の存在は、異なる2頂点が2つ以上の共通隣接点を持つことと同値。
    for i, u in enumerate(vertices):
        for v in vertices[i+1:]:
            if len(adj[u] & adj[v]) >= 2:
                return False
    # 欠辺 uv を足して C4 ができる iff 元から長さ3の単純路 u-x-y-v がある。
    for i, u in enumerate(vertices):
        for v in vertices[i+1:]:
            if v in adj[u]:
                continue
            if not any(y in adj[v]
                       for x in adj[u]
                       for y in adj[x]
                       if x != v and y != u and y != v):
                return False
    return True

tested = positive = mismatches = 0
for h in nx.graph_atlas_g():
    n = len(h)
    if n < 3:
        continue
    for a in h:
        g = h.copy()
        g.add_edge(a, n)  # atlas は頂点 0,...,n-1
        rhs = saturated(h) and all(
            any(y in h[x] for y in h[a] if y != x)
            for x in h if x != a
        )
        lhs = saturated(g)
        tested += 1
        positive += int(lhs)
        mismatches += (lhs != rhs)
assert (tested, positive, mismatches) == (8470, 30, 0)
print(tested, positive, mismatches)
```

実行環境: Python 3 / NetworkX 3.6.1。なお、両辺が真の30組は頂点指定つきの組数であり、非同型な拡張後グラフの個数ではない。

## 次の課題

10頂点11辺の葉あり候補を除外するには、8頂点9辺・9頂点10辺の C4 飽和グラフの存在と、葉追加可能な支持頂点を厳密に調べる必要がある。上の検査は7頂点以下なので、その非存在を示していない。
