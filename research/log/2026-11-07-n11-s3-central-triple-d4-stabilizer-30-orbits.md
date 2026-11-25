# 11×11 中央三石の四石応手：対称性で110手を30軌道へ縮約（2026-11-07）

対象の三石局面は `{59,60,61}`（行優先0始まり、座標 `(4,5),(5,5),(6,5)`）。四石目の候補は残り118点で、4点共円・共線を禁じる標準規則では合法手110点。

この局面を固定するD4部分群は恒等変換、左右反転 `(x,y)->(10-x,y)`、上下反転 `(x,y)->(x,10-y)`、180度回転の4元。合法な四石子110個をこの群で同一視すると **30軌道**。軌道サイズは2が5軌道、4が25軌道（`5*2+25*4=110`）。固定点1の軌道はない。

既存のS4-A `{59,60,61,69}` とS4-B `{47,59,60,61}` は上下反転で対応する**同一軌道**（69=(3,6), 47=(3,4)）。したがってこの三石局面の全合法四石応手を勝敗証明する際、既存の2局面は独立した2軌道ではなく、既知は1軌道、残りは**29軌道**。これは証明義務の対称性による縮約であり、未証明の29軌道の勝敗を意味しない。

再現コード（標準ライブラリのみ、整数行列式で幾何判定）：

```python
from itertools import combinations, permutations
from math import prod
S = (59, 60, 61)
def det4(rows):
    return sum((-1)**sum(p[i]>p[j] for i in range(4) for j in range(i+1,4))
               * prod(rows[i][p[i]] for i in range(4))
               for p in permutations(range(4)))
def legal(i):
    pts = [(v%11, v//11) for v in (*S, i)]
    return det4([[x*x+y*y, x, y, 1] for x,y in pts]) != 0
children = [i for i in range(121) if i not in S and legal(i)]
def orbit(i):
    x,y = i%11,i//11
    return tuple(sorted({yy*11+xx for xx,yy in
        ((x,y),(10-x,y),(x,10-y),(10-x,10-y))}))
orbits = {orbit(i) for i in children}
assert len(children)==110
assert len(orbits)==30
assert sum(len(o)==2 for o in orbits)==5
assert sum(len(o)==4 for o in orbits)==25
assert orbit(69)==orbit(47)
```

注意：四石時点での手番と「元先手WIN」の極性は別途保持すること。S4-A/Bの既存勝敗証明はK0676を参照。三石・二石・空盤は依然 UNKNOWN。
