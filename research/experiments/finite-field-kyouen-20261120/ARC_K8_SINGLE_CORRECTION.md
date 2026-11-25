# 重要な訂正：単一円プロファイルは k=7 の結果だった

2026-11-20。`finite-field-kyouen-20261120` の第218部。

前項で「k=8 の単一円プロファイル `(5,)`, `(6,)` が欠落している」と
報告したが、**これは誤りだった。**

## 1. 発見

**k=7 と k=8 の単一円プロファイルを全数列挙で比較した**（q=5）：

| k | 単一円プロファイル |
|---:|---|
| **7** | `{6: 2600}` |
| **8** | `{}` （**存在しない**） |

**`(6,) = 2,600` は k=7 の結果だった。** k=8 では単一円プロファイルは
**1つも存在しない。**

## 2. なぜ k=8 では存在しないか

k=8 の単一円プロファイルとは「8点のうち `j ≥ 5` 点が1つの円 `D` 上に
あり、他の4円を持たない」ものである。

q=5 では `s = 6` なので `j = 5, 6` が可能。しかし**全数探索で0件**。

**理由**：`D` 上の5点または6点に外点を加えると、**必ず別の4円ができる**。
q=5 は点が密（`n = 26`）なので、外点が既存の円と4点を作りやすい。

**k=7 では `(6,)` が存在した**（6点円 + 外1点）。外点が1個だけなら
4円を作りにくい。k=8 では外点が2個以上必要になり、4円ができやすい。

## 3. 前項の誤りの内容

前項（第217部）で「q=9 の組み立ての差 119,024,640 は `(5,)` と `(6,)`
の寄与」と結論したが、**これは誤り**。

**正しい理解**：
- k=8 の単一円プロファイルは q=5 で 0 件
- q=9 で存在するかは未検証
- 差 119,024,640 の原因は**別にある**

## 4. 差の原因（再検討）

q=9 の組み立ての差 119,024,640 は、単一円プロファイルでは説明できない。

**他の候補**：

1. **プロファイル公式の破綻**：`#4円 = 1 + v2 + u3 + z4` が q=9 で
   成り立たない可能性（k=7 で q=7 のときに起きたのと同じ種類の問題）
2. **多重度定理の破綻**：`÷n4` が q=9 で成り立たない
3. **`(j,)` 以外の欠落プロファイル**

**q=9 のプロファイル公式を検証する必要がある。**

## 5. 意義

1. **前項の診断を撤回した**（単一円プロファイルは k=7 の結果だった）。
2. **k=8 の単一円プロファイルは q=5 で 0 件**と確定。
3. **q=9 の差の原因は別**と判明（未特定）。
4. **k=7 と k=8 を混同していた**という自己修正。

## 6. 限界

- q=9 の差の原因は未特定。
- q=9 のプロファイル公式は未検証。
- q=11 の k=8 は実行中。

## 7. 再現

```sh
cd research/experiments/finite-field-kyouen-20261120/scripts
python -c "
import sys; sys.path.insert(0,'.')
from inversive_all_q import build_field, build_inversive_plane
import itertools
from collections import Counter
q=5
F,sub=build_field(q)
points,circles=build_inversive_plane(q)
idx={p:i for i,p in enumerate(points)}
blocks=[tuple(sorted(idx[p] for p in c)) for c in circles]
n=len(points)
coq={}
for k,BB in enumerate(blocks):
    for quad in itertools.combinations(BB,4): coq[quad]=k
for kk in (7,8):
    single=Counter()
    for S in itertools.combinations(range(n),kk):
        Sset=set(S); hits={}
        for quad in itertools.combinations(S,4):
            cj=coq.get(quad)
            if cj is None: continue
            hits[cj]=len(Sset & set(blocks[cj]))
        if len(hits)==1: single[next(iter(hits.values()))]+=1
    print(kk, dict(sorted(single.items())))
"
```
