# 3×m・q=5：m=14 の線形外挿破れを弦対から独立検証（2026-11-12）

**証拠水準：有限盤の完全列挙・厳密有理数演算。無界の円数公式ではない。**

既存の `q35-circle-count-linear-break-20261112.md` は全非共線三点組から円を生成した。本検算は独立に「異なる二行の各水平弦（両端の整数点）」から円を一意に復元する。3行で5点以上を通る円は必ず少なくとも二行で2点ずつ持つので、この生成は完全である。各弦の中点の横座標は同じでなければならない。

二行 `y,z` の弦端点を `a<b`, `c<e` とすると `a+b=c+e`、`h=(a+b)/2`、`u=(b-a)^2/4`、`v=(e-c)^2/4`。円の縦中心は
```
k = (v-u+z*z-y*y)/(2*(z-y))
R² = u+(y-k)².
```
全3行の整数点を代入して5点以上の円だけを採用する。

独立列挙の結果：m=13 は42本、m=14 は52本。m=14で初めて現れる、左右端を含む円（横幅14を必要とする円）は**ちょうど4本**で、いずれも5点円。支持点集合（座標は `(x,y)`、`0≤x≤13,0≤y≤2`）は以下。

1. `(4,0),(7,0),(0,1),(11,1),(13,2)`
2. `(6,0),(9,0),(2,1),(13,1),(0,2)`
3. `(13,0),(0,1),(11,1),(4,2),(7,2)`
4. `(0,0),(2,1),(13,1),(6,2),(9,2)`

全て縦中心は `29/2` または `-25/2`、半径二乗は `425/2`。水平弦幅は3と11で、残る行の1点は片側端から13離れる。反射・上下反転による4本である。

**注意：** 52−42=10は新型10本という意味ではない。既存の幅13以下の円も右へ平行移動して新しい円を作る。線形外挿 `6m−36` からの超過4本は、ちょうどこの幅14の新型4本に対応する。

再現コード（標準Pythonのみ）：

```python
from fractions import Fraction as F
from itertools import combinations

def census(m):
    out = {}
    for y,z in combinations(range(3),2):
        for a,b in combinations(range(m),2):
            h = F(a+b,2)
            u = F((b-a)**2,4)
            for c,e in combinations(range(m),2):
                if c+e != a+b: continue
                v = F((e-c)**2,4)
                k = F(v-u+z*z-y*y, 2*(z-y))
                r2 = u+(F(y)-k)**2
                key = (h,k,r2)
                if key in out: continue
                pts = tuple((x,j) for j in range(3) for x in range(m)
                            if (F(x)-h)**2+(F(j)-k)**2 == r2)
                if len(pts)>=5: out[key] = pts
    return out

a,b = census(13),census(14)
assert (len(a),len(b)) == (42,52)
new_span = [pts for pts in b.values()
            if min(x for x,y in pts)==0 and max(x for x,y in pts)==13]
assert len(new_span)==4 and all(len(s)==5 for s in new_span)
print('OK',len(a),len(b),new_span)
```

この結果は既存の三点生成とは別の完全生成による監査であり、全称分類の主張はしない。次は弦幅3,11の整数論的発生条件を一般の弦幅対へ拡張し、新型の初出幅を式で求める。
