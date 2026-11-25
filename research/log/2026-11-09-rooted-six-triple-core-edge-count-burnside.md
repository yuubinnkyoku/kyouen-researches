# 根付き6点純三点辺核の辺数別同型型数（Burnside精密化）

2026-11-09。対象は指定根0を固定した6頂点の三点超辺集合。既存K0684の全10688根付き同型型を、辺数別に精密化する。Grundy周期性について新たな主張はしない。

## 定理（有限組合せ論、全数について厳密）

辺数kの根付き同型型数を a_k とすると、k=0,...,20 に対し

```
k:   0  1  2  3  4  5   6   7    8    9   10   11   12  13  14  15  16  17  18 19 20
a_k: 1  2  7 24 75 192 431 806 1259 1644 1806 1644 1259 806 431 192 75 24 7  2  1
```

合計10688で既存K0684の総数と一致する。

## 証明

根を固定する頂点置換群はS5（位数120）。三点辺は6点から選ぶ20通り。置換σが20辺上に誘導する置換の巡回長をl_1,...,l_tとする。σに固定される辺数kの集合は、巡回を丸ごと採る必要があるため、生成多項式が∏_i(1+x^{l_i})となる。したがってBurnsideの補題より

A(x)= (1/120) ∑_{σ∈S5} ∏_{C∈Cycles(σ on triples)}(1+x^{|C|})

であり a_k=[x^k]A(x)。全120置換を5!通りの辞書順で走査して上の整数係数を得る。これは有限群の完全列挙による厳密な式であり、統計的推定ではない。

独立の整合性確認：各三点辺集合の補集合を取る操作はS5作用と可換な全単射なので a_k=a_{20-k}。さらにA(1)=10688。20辺上の巡回数ごとの置換個数は {20:1,14:10,12:15,8:20,6:50,4:24} であり、(2^20+10·2^14+15·2^12+20·2^8+50·2^6+24·2^4)/120=10688。

## 再現用の短いPython 3コード

```python
from itertools import combinations, permutations
T=list(combinations(range(6),3))
lookup={t:i for i,t in enumerate(T)}
acc=[0]*21
for tail in permutations(range(1,6)):
    p=(0,)+tail
    f=[lookup[tuple(sorted(p[v] for v in t))] for t in T]
    seen=set(); poly=[1]+[0]*20
    for start in range(20):
        if start in seen: continue
        j=start; length=0
        while j not in seen:
            seen.add(j); length+=1; j=f[j]
        for k in range(20,length-1,-1):
            poly[k]+=poly[k-length]
    for k in range(21): acc[k]+=poly[k]
assert all(x%120==0 for x in acc)
a=[x//120 for x in acc]
assert sum(a)==10688 and a==a[::-1]
print(a)
```

## 用途と限界

K0684の「6点純三点辺核全型」の辺数別監査に利用できる。これは核の同型型数の精密化であり、Grundy列の周期性を新たに証明するものではない。二点辺を含む混合核も対象外。
