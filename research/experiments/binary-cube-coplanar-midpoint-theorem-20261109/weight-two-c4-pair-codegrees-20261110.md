# 重み2層の禁止四角形：辺・辺対の共起数（2026-11-10）

## 全次元の定理

二値立方体の重み2層を完全グラフ K_d の辺集合と同一視する（既証明の `constant-weight-layers.md`）。d>=4 とする。禁止四点組は K_d の単純四角形 C4 の4辺に対応する。

1. 禁止 C4 の総数は `3*C(d,4)`。
2. 任意の一辺 e を含む禁止 C4 は `(d-2)*(d-3)` 個。
3. 異なる二辺 e,f をともに含む禁止 C4 は、e,f が端点を共有するなら `d-3` 個、端点を共有しないなら **2個**。

従って、この禁止四点組超グラフは頂点次数が一定で、二頂点共起数は元の K_d の隣接関係だけで決まる（隣接型と非隣接型の二種類）。これは全次元での数学的証明であり、有限計算からの外挿ではない。

## 証明

任意の4頂点集合上には3通りの単純 C4 が存在する。従って総数は `3*C(d,4)`。

固定辺 e={a,b} を含む四角形では、残りの2頂点を `C(d-2,2)` 通りに選び、3つの四角形のうち e を含むものは2つ。よって `2*C(d-2,2)=(d-2)(d-3)`。

e={a,b}, f={a,c} が隣接する場合、四角形は a,b,c と第四頂点 x を含み、x は残りの d-3 頂点から選ぶ。a で接する2辺をともに含む四角形は `a-b-x-c-a` の一意なものなので `d-3`。

e={a,b}, f={c,d} が非隣接の場合、四角形の頂点は a,b,c,d に固定され、両辺を含むのは `a-b-c-d-a` と `a-b-d-c-a` の2通り。以上。□

## 独立有限検算

下記の標準ライブラリのみのコードで d=4..8 の全 C4 を直接列挙し、全辺と全辺対について式を照合した。結果は全件一致。d=8 では禁止 C4 は210個。

```python
from itertools import combinations
for d in range(4, 9):
    edges = list(combinations(range(d), 2))
    cycles = []
    for a, b, c, e in combinations(range(d), 4):
        for seq in ((a,b,c,e), (a,b,e,c), (a,c,b,e)):
            cycles.append(frozenset(
                frozenset((x,y))
                for x,y in zip(seq,seq[1:]+seq[:1])
            ))
    assert len(cycles) == 3 * len(list(combinations(range(d), 4)))
    for e in edges:
        assert sum(frozenset(e) in c for c in cycles) == (d-2)*(d-3)
    for e,f in combinations(edges,2):
        expected = d-3 if len(set(e+f)) == 3 else 2
        assert sum(frozenset(e) in c and frozenset(f) in c
                   for c in cycles) == expected
    print(d, len(cycles), "ok")
```

期待出力：`4 3 ok`、`5 15 ok`、`6 45 ok`、`7 105 ok`、`8 210 ok`。

## 意義・限界

辺対の共起数は定数時間で求められるため、禁止集合の共起重みを明示列挙せずに計算できる。これは枝刈りや分岐順序の指標に利用可能だが、**実探索での高速化は未測定**。元の平面共円ゲームや重み2層の勝敗を決定する結果ではない。既存の `pair-codegrees.md` は全立方体の頂点対に関する別の公式である。
