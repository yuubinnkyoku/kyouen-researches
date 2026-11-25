# 10頂点11辺の C4 飽和グラフは存在しない：二重閉路の直径による排除（2026-11-11）

## 結論と証拠水準

**定理（既存の葉なし定理と有限構造分類による証明）。** 10頂点11辺の C4 飽和単純グラフは存在しない。

先行する `research/log/2026-11-11-c4-saturated-n-plus-one-leaf-free.md` により、仮に存在すれば最小次数は2以上である。本記録では残る場合を排除する。重要なのは **C4 飽和なら直径は3以下** だが、**10頂点11辺・最小次数2以上の単純グラフは直径4以上** という食い違いである。

## 補題1：C4 飽和グラフの直径は3以下

任意の非隣接頂点 u,v について、辺 uv を加えたときに新たにできる C4 は必ず uv を含む。したがって元のグラフには u と v を結ぶ長さ3の単純路が存在する。隣接頂点の距離は1なので、任意の2頂点の距離は3以下。特にグラフは連結である。

## 補題2：10頂点11辺・最小次数2以上なら直径4以上

次数和は22であり、各頂点の次数が2以上だから、超過次数 `Σ(deg(v)-2)=2`。次数列は (4,2^9) または (3,3,2^8) の二択。

連結性と次数2頂点の道の縮約から、前者は1頂点で交わる二つの閉路（figure-eight）、後者は二つの次数3頂点を結ぶ3本の内部頂点素な道（theta）、または二つの閉路を道で結んだもの（dumbbell）である。これは連結・最小次数2・閉路階数2の全分類であり、他の核はない。

各場合の整数パラメータを全列挙する。閉路長は3以上、thetaの3本の道長は正整数で、単純グラフでは長さ1の道を2本持てない。

* theta: `a≤b≤c, a+b+c=11`。可能な9組は (1,2,8), (1,3,7), (1,4,6), (1,5,5), (2,2,7), (2,3,6), (2,4,5), (3,3,5), (3,4,4)。直径は順に **5,5,5,5,4,4,4,4,4**。
* figure-eight: `3≤a≤b, a+b=11`。可能な3組は (3,8), (4,7), (5,6)。直径はすべて **5**。
* dumbbell: `3≤a≤b, t≥1, a+b+t=11`（tは二閉路間の橋道の辺数）。可能な9組は (3,3,5), (3,4,4), (3,5,3), (3,6,2), (3,7,1), (4,4,3), (4,5,2), (4,6,1), (5,5,1)。直径は順に **7,7,6,6,5,7,6,6,5**。

直径値は各構造の距離式からも算出できる。figure-eightでは `floor(a/2)+floor(b/2)`、dumbbellでは `floor(a/2)+t+floor(b/2)`。thetaについては端点を0,1とし、各道の内部点 i,j 間の距離を、同一道なら `min(|i-j|, i+j+min(other path lengths), (a-i)+(a-j)+min(other path lengths))` 等とするより、下記の独立再現器で全頂点対の最短路を直接計算するのが確実である。上の9組の最大距離は4以上。

従っていずれの形でも直径3以下にはならず、補題1と矛盾する。□

## 独立再現器（Python標準ライブラリのみ）

以下は核の3種類を直接構築し、BFSで直径を検査する。NetworkXや C4 判定器を使わない。

```python
from collections import deque

def graph(edges):
    adj = {}
    for u, v in edges:
        adj.setdefault(u, set()).add(v)
        adj.setdefault(v, set()).add(u)
    return adj

def diameter(edges):
    adj = graph(edges)
    distances = []
    for s in adj:
        d = {s: 0}
        q = deque([s])
        while q:
            u = q.popleft()
            for v in adj[u]:
                if v not in d:
                    d[v] = d[u] + 1
                    q.append(v)
        assert len(d) == len(adj)
        distances.extend(d.values())
    return len(adj), len(edges), max(distances)

def cycle(start, length):
    vs = list(range(start, start + length))
    return list(zip(vs, vs[1:] + vs[:1]))

def theta(a, b, c):
    edges, next_id = [], 2
    for length in (a, b, c):
        prev = 0
        for _ in range(length - 1):
            edges.append((prev, next_id))
            prev, next_id = next_id, next_id + 1
        edges.append((prev, 1))
    return edges

def figure_eight(a, b):
    e = cycle(0, a)
    vs = [0] + list(range(a, a + b - 1))
    return e + list(zip(vs, vs[1:] + vs[:1]))

def dumbbell(a, b, t):
    e = cycle(0, a) + cycle(a, b)
    prev, nxt = 0, a + b
    for _ in range(t - 1):
        e.append((prev, nxt))
        prev, nxt = nxt, nxt + 1
    e.append((prev, a))
    return e

counts = [0, 0, 0]
for a in range(1, 12):
    for b in range(a, 12):
        c = 11 - a - b
        if c < b or c < 1 or (a == b == 1):
            continue
        n, m, d = diameter(theta(a, b, c))
        assert (n, m) == (10, 11) and d >= 4
        counts[0] += 1
for a in range(3, 12):
    b = 11 - a
    if b < a:
        continue
    n, m, d = diameter(figure_eight(a, b))
    assert (n, m) == (10, 11) and d >= 4
    counts[1] += 1
for a in range(3, 12):
    for b in range(a, 12):
        t = 11 - a - b
        if t < 1:
            continue
        n, m, d = diameter(dumbbell(a, b, t))
        assert (n, m) == (10, 11) and d >= 4
        counts[2] += 1
assert counts == [9, 3, 9], counts
print(counts)
```

## 証拠境界と意義

これは11辺を持つ10頂点の全ラベル付きグラフを列挙したものではない。既存の**全称的な葉なし定理**と、次数和から得られる**二重閉路の全構造分類**を用い、残る21個の整数パラメータだけを厳密に排除した証明である。11×11盤の勝敗や s_n の値を示すものではない。従来の「葉なしの場合が未解決」という研究上の課題を閉じる。形式証明器での独立形式化は未実施。
