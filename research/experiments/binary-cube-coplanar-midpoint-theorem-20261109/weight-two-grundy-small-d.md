# 等重み2層の共面四点禁止ゲーム：小次元の全局面分類（2026-11-10）

## 問題と証拠水準
既証明の「重み2の頂点 ↔ K_d の辺、禁止共面四点 ↔ 四角形 C4」を用い、d=4,5,6 の通常プレイ（合法手がなくなった手番側が負け）の Grundy 値を**有限完全列挙**で求める。全次元の勝敗を主張しない。禁止集合の構成はグラフ側から行っているので、幾何学的同値の証明は既存の constant-weight-layers.md に依存する。

| d | 頂点（辺）数 | 禁止 C4 数 | 安全集合数 | 空盤 Grundy | 極大安全集合のサイズ別個数 |
|---|---:|---:|---:|---:|---|
| 4 | 6 | 3 | 54 | 0 | 4:12 |
| 5 | 10 | 15 | 548 | 1 | 5:72, 6:15 |
| 6 | 15 | 45 | 7984 | 1 | 6:120, 7:900 |

空盤の Grundy 値が d=4 と d=5 で異なるので、この系列で「常に後手勝ち」は成立しない。各 d の全 2^binom(d,2) 個の部分集合を走査し、C4 を含まないものを全て列挙。各安全集合の全合法手から mex を計算した。

## 再現用 Python 3（標準ライブラリのみ）

```python
from itertools import combinations
from functools import lru_cache
from collections import Counter

for d in (4, 5, 6):
    edges = list(combinations(range(d), 2))
    index = {e: i for i, e in enumerate(edges)}
    forbidden = []
    for a, b, c, e in combinations(range(d), 4):
        for cycle in ((a,b,c,e), (a,b,e,c), (a,c,b,e)):
            mask = 0
            for x, y in zip(cycle, cycle[1:] + cycle[:1]):
                mask |= 1 << index[tuple(sorted((x,y)))]
            forbidden.append(mask)
    assert len(set(forbidden)) == 3 * len(list(combinations(range(d),4)))
    safe = {s for s in range(1 << len(edges))
            if all((s & f) != f for f in forbidden)}
    @lru_cache(None)
    def grundy(s):
        successors = {grundy(t) for i in range(len(edges))
                      if not (s >> i) & 1
                      for t in (s | (1 << i),) if t in safe}
        value = 0
        while value in successors:
            value += 1
        return value
    terminal = Counter(
        s.bit_count() for s in safe
        if all((s | (1 << i)) not in safe for i in range(len(edges))
               if not (s >> i) & 1)
    )
    print(d, len(edges), len(forbidden), len(safe), grundy(0),
          dict(sorted(terminal.items())))
```

期待出力：

```text
4 6 3 54 0 {4: 12}
5 10 15 548 1 {5: 72, 6: 15}
6 15 45 7984 1 {6: 120, 7: 900}
```

## 未解決
d>=7 での空盤 Grundy と、C4-free グラフの極大配置構造。現時点では独立した別実装による照合は未実施。通常の平面共円ゲームの結果ではない。
