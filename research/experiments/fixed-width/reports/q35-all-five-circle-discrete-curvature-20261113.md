# 3×m・q=5：全5点円数の離散曲率（2026-11-13）

**証拠水準：既存の全称計数式からの代数的帰結。** 対象は円上の格子点がちょうど5個の円の本数 F₅(m) であり、5点部分集合数ではない。先行資料 `q35-five-circle-diophantine-first-width-20261112.md` と `q35-tangent-complete-pell-classification-20261113.md` を前提とする。

## 定理（全称・正確）

整数 m≥2 に対して Δ²F₅(m)=F₅(m+1)−2F₅(m)+F₅(m−1) とおく。接線型の弦幅列を A={8,48,280,1632,…} とする。整数三つ組 (a,b,k) が

- a,b≥1、k≥1、a≡b≡k (mod 2)
- a²+k²+8=2b²、k>W=max(a,b)

を満たす集合を S とし、L=(W+k)/2 とする。このとき

```
Δ²F₅(m) = 2·1[m∈A] + 4·#{(a,b,k)∈S : L=m} − 4·#{(a,b,k)∈S : k=m}.
```

各 m に関わる組は有限個である。特に、F₅(m) は一般に凸ではない。F₅(8)=0、F₅(9)=6、F₅(10)=8 より Δ²F₅(9)=−4 である。なお m=8 の正の変化は接線型 (8,6,0) と片側切断型 (3,7,9) の両方に由来し、Δ²F₅(8)=6 となる。

## 証明

先行の必要十分条件より、接線型の寄与は 2(m−a)₊、片側切断型の寄与は 4 min((m−L)₊,D)、D=(k−W)/2=k−L。整数 m に対して (x)₊=max(0,x) と書けば

```
min((m−L)₊,D) = (m−L)₊ − (m−k)₊.
```

また Δ²(m−t)₊=1[m=t]。各固定 m に寄与する三つ組は L≤m または k≤m に制限され、k>W≥a,b なので有限である。従って項別に二階差分を取れる。接線型は完全分類により A のみ。式を得る。

m=8,9,10 の値は先行の独立列挙と一致し、m=9 の負の二階差分は直接の反例である。

## 独立の整数検算

以下は元の計数式を整数で実装し、上の二階差分の式と m=2..100 で突き合わせる。証明自体は上の恒等式に依拠する。

```python
from math import isqrt
def count(m):
    s=0
    for a in range(1,m):
        for b in range(1,m):
            z=2*b*b-a*a-8
            if z<0 or (a-b)%2: continue
            k=isqrt(z)
            if k*k!=z or (k-a)%2: continue
            W=max(a,b)
            if k==0: s+=2*(m-W)
            elif k>W: s+=4*min(max(0,m-(W+k)//2),(k-W)//2)
    return s
def curvature(m):
    v=0
    a,b=8,6
    while a<=m:
        if a==m: v+=2
        a,b=3*a+4*b,2*a+3*b
    for a in range(1,m+1):
        for b in range(1,m+1):
            z=2*b*b-a*a-8
            if z<0 or (a-b)%2: continue
            k=isqrt(z)
            if k*k!=z or (k-a)%2: continue
            W=max(a,b)
            if k>W:
                L=(W+k)//2
                v+=4*(L==m)-4*(k==m)
    return v
assert [count(m) for m in (8,9,10)]==[0,6,8]
assert all(count(m+1)-2*count(m)+count(m-1)==curvature(m) for m in range(2,101))
```

## 範囲と意義

これは F₅ 全体の**厳密な離散二階差分公式**であり、接線型の階段公式とは異なる。無界の漸近次数や q=5 の勝敗を確定しない。片側切断型の初出 L と飽和 k がそれぞれ正・負の曲率を発生させるため、接線型だけから F₅ の凸性を推論できない。
