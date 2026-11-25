# 重み2層の極大安全配置と長さ3の道（2026-11-10）

## 定理（全次元）

二値立方体の重み2層の点を完全グラフ (K_d) の辺に対応させる。(d\ge4) とし、選択辺からなる単純グラフ (G) が安全、すなわち四角形 (C_4) を含まないとする。

**(G) が極大安全であるための必要十分条件は、すべての非隣接頂点対 (u,v) の間に長さ3の単純な道が存在すること**である。

同値に、現在の合法追加辺は、長さ3の道で結ばれていない非隣接頂点対とちょうど一致する。

## 証明

非辺 (uv) を追加した結果初めて (C_4) が生じるなら、その四角形は新辺 (uv) を含む。残りの三辺はもともと (G) に存在し、(u) から (v) への長さ3の単純な道をなす。逆に、そのような道 (u-a-b-v) があれば、(uv) の追加によって (u-a-b-v-u) が生じる。したがって各非辺が追加不能であることと、各非辺に長さ3の道があることは同値。極大性はすべての非辺が追加不能であることにほかならない。□

**系1（連結性）**：(d\ge2) の極大安全グラフは連結である。異なる連結成分の頂点対には長さ3の道がないため。

**系2（直径）**：(d\ge2) の極大安全グラフの直径は高々3。隣接対は距離1、非隣接対は定理より距離高々3。ただし距離2の対にも長さ3の道が必要であり、単なる直径条件だけでは十分でない。

**系3（判定器）**：各頂点の隣接集合を (N(u)) とすれば、非辺 (uv) の追加が禁止される必要十分条件は (N(u)) と (N(v)) の間に辺があること。これは禁止四角形全体を保持せず判定できる。安全性の事前条件を忘れると極大安全の判定にはならない。

## 独立した有限完全列挙

(d=4,5,6) のすべての (2^{\binom d2}) 辺集合を列挙し、(A) 各非辺の追加後に共通隣接点数が2以上の頂点対があるかを直接調べる方法、(B) 元のグラフで長さ3の道があるかを調べる方法を比較した。安全なすべての集合について極大性の判定が完全一致した。

極大安全グラフの辺数別個数：

- (d=4)：4辺が12個。
- (d=5)：5辺が72個、6辺が15個。
- (d=6)：6辺が120個、7辺が900個。

既存の重み2層完全列挙記録の (d=4,5,6) とも一致する。

### 再現用 Python（標準ライブラリのみ）

```python
from itertools import combinations
for n in range(4, 7):
    edges = list(combinations(range(n), 2))
    counts = {}
    for mask in range(1 << len(edges)):
        adj = [set() for _ in range(n)]
        for k, (a, b) in enumerate(edges):
            if mask >> k & 1:
                adj[a].add(b)
                adj[b].add(a)
        def safe(A):
            return all(len(A[a] & A[b]) < 2
                       for a, b in edges)
        if not safe(adj):
            continue
        by_paths = all(
            any(y in adj[x] for x in adj[a] for y in adj[b])
            for a, b in edges if b not in adj[a]
        )
        by_additions = True
        for a, b in edges:
            if b in adj[a]:
                continue
            copy = [s.copy() for s in adj]
            copy[a].add(b)
            copy[b].add(a)
            if safe(copy):
                by_additions = False
                break
        assert by_paths == by_additions
        if by_paths:
            k = mask.bit_count()
            counts[k] = counts.get(k, 0) + 1
    print(n, counts)
```

期待出力：`4 {4: 12}`、`5 {5: 72, 6: 15}`、`6 {6: 120, 7: 900}`。

## 証拠と射程

全次元の同値は数学的証明。(d=4..6) の個数は独立判定による有限完全列挙。元の格子盤の共円禁止ゲームには直接適用できない。(d=7) 以降の最小極大辺数の一般公式や勝敗を主張するものではない。
