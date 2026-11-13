# 小次元立方体での circuit / 全依存組の独立照合（2026-11-14）

## 方法

二値立方体 V_d={0,1}^d、q=d+1。全頂点を辞書順で列挙し、SymPy の有理数行列 rank でアフィン依存を判定した。サイズ2〜qの各部分集合について、依存かつ全ての一頂点除去が独立であるものを circuit とした。全依存 q 点組は別に列挙した。各 k 点集合（k≥q）について、(A) circuit を含まないか、(B) 依存 q 点組を含まないかを全数検査し、それぞれの合格数を比較した。

| d | q | k | circuit総数 | 依存q点組総数 | A合格数 | B合格数 |
|---:|---:|---:|---:|---:|---:|---:|
| 3 | 4 | 4 | 12 | 12 | 58 | 58 |
| 3 | 4 | 5 | 12 | 12 | 8 | 8 |
| 3 | 4 | 6 | 12 | 12 | 0 | 0 |
| 4 | 5 | 5 | 260 | 1360 | 3008 | 3008 |
| 4 | 5 | 6 | 260 | 1360 | 1088 | 1088 |
| 4 | 5 | 7 | 260 | 1360 | 0 | 0 |

この表は有限完全列挙の結果であり、一般命題の証明は [同日付の一般補題](2026-11-14-k6-exact-cardinality-circuit-equivalence.md) にある。d=4 で 260 と 1360 が異なるのに k≥q の合格数が一致する点が、縮約の正当性を具体的に裏付ける。

## 再現用の独立短縮コード

```python
from itertools import product, combinations
from sympy import Matrix
for d in (3, 4):
    V = list(product((0, 1), repeat=d))
    q = d + 1
    def dependent(t):
        return Matrix([[1, *V[i]] for i in t]).rank() < len(t)
    circuits = [
        t for j in range(2, q + 1)
        for t in combinations(range(len(V)), j)
        if dependent(t) and all(not dependent(u) for u in combinations(t, j-1))
    ]
    full = [t for t in combinations(range(len(V)), q) if dependent(t)]
    for k in range(q, min(len(V), q + 2) + 1):
        a = b = 0
        for t in combinations(range(len(V)), k):
            S = set(t)
            a += not any(S.issuperset(c) for c in circuits)
            b += not any(S.issuperset(c) for c in full)
        print(d, q, k, len(circuits), len(full), a, b)
```

## 留保と次の作業

これは小次元の独立検証であり、d=6 の circuit 列挙器・exactly-10 CNF・UNSAT を検証したものではない。K0568 の「circuit削減は証明に使用不可」という記述は exactly-10 判定に限れば過剰な否定である。ただしゲームの合法局面全体には使用できない。knowledge の正本を修正する際は AGENTS.md 所定の検査・生成を実行すること。
