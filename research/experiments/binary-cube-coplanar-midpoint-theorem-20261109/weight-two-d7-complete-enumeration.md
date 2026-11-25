# 重み2層・7次元の完全列挙（2026-11-10）

## 対象と証拠水準

二値立方体 {0,1}^7 の重み2頂点21個に限った共面四点禁止ゲーム。重み2頂点を K_7 の辺と同一視すると、禁止四点組は C4 の4辺（既存の等重み層定理）。**有限完全列挙**であり、全次元の勝敗定理ではない。

## 結果

全 2^21 = 2,097,152 個の辺集合を列挙した。C4 は105個。安全集合は **163,440** 個。極大安全集合は8辺の **5,040** 個と9辺の **6,615** 個のみ。従って最小極大サイズ8、最大安全サイズ9。通常プレイの空盤Grundy値は **1（先手勝ち）**。

| 辺数 | 安全集合数 | 極大数 |
|---:|---:|---:|
| 0 | 1 | 0 |
| 1 | 21 | 0 |
| 2 | 210 | 0 |
| 3 | 1330 | 0 |
| 4 | 5880 | 0 |
| 5 | 18564 | 0 |
| 6 | 40474 | 0 |
| 7 | 54750 | 0 |
| 8 | 35595 | 5040 |
| 9 | 6615 | 6615 |

## 再現方法と独立照合

同じ21辺のビット集合を対象に、二つの異なる禁止判定を用いた。

1. 7頂点から4頂点を選び、3通りの四角形を作って計105個の禁止マスクを生成。最大ビットの辺を追加するとき、他の3辺が存在するかで安全性を漸化的に判定。安全集合を大きいビット集合から順に処理して子局面のGrundy値の mex を取った。
2. 禁止四角形を列挙せず、各辺集合から隣接ビット集合を構成。**どの二頂点も共通隣接頂点を2個以上持たない**ことと C4 不在が同値であることを利用して全2^21集合を独立判定。極大性は一辺追加した全候補を照合した。

両実装の各石数の安全集合数と極大数は完全一致した。Grundy値1は第一実装による全安全局面の後退再帰計算であり、**Grundyの独立実装照合は未実施**。

### 再現用C++（第一実装）

```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
 const int n=7;
 vector<pair<int,int>> E;
 for(int i=0;i<n;i++) for(int j=i+1;j<n;j++) E.push_back({i,j});
 const int m=E.size(), limit=1<<m;
 vector<vector<unsigned>> closing(m);
 int cyc=0;
 for(int a=0;a<n;a++) for(int b=a+1;b<n;b++)
 for(int c=b+1;c<n;c++) for(int d=c+1;d<n;d++) {
   int v[]={a,b,c,d};
   int pairs[3][4]={{0,1,2,3},{0,2,1,3},{0,3,1,2}};
   for(auto &p:pairs) {
     unsigned f=0;
     for(auto [x,y]:vector<pair<int,int>>{
       {v[p[0]],v[p[2]]},{v[p[0]],v[p[3]]},
       {v[p[1]],v[p[2]]},{v[p[1]],v[p[3]]}}) {
       if(x>y)swap(x,y);
       for(int k=0;k<m;k++) if(E[k]==make_pair(x,y)) f|=1u<<k;
     }
     int top=31-__builtin_clz(f);
     closing[top].push_back(f^(1u<<top)); ++cyc;
   }
 }
 vector<unsigned char> safe(limit),grundy(limit);
 safe[0]=1;
 for(int s=1;s<limit;s++) {
   int k=31-__builtin_clz((unsigned)s), t=s^(1<<k);
   if(!safe[t])continue;
   bool ok=true;
   for(auto f:closing[k]) if((t&f)==f){ok=false;break;}
   safe[s]=ok;
 }
 vector<unsigned long long> count(m+1),maximal(m+1);
 for(int s=limit-1;s>=0;s--) if(safe[s]) {
   int k=__builtin_popcount((unsigned)s),seen=0,moves=0;
   count[k]++;
   for(int j=0;j<m;j++) if(!(s>>j&1)&&safe[s|(1<<j)]) {
     seen|=1<<grundy[s|(1<<j)]; ++moves;
   }
   if(!moves)maximal[k]++;
   while(seen>>grundy[s]&1)grundy[s]++;
 }
 cout<<"C4 "<<cyc<<" Grundy "<<(int)grundy[0]<<"\n";
 for(int k=0;k<=m;k++) if(count[k])
   cout<<k<<" "<<count[k]<<" "<<maximal[k]<<"\n";
}
```

### 独立判定の核

各集合の隣接ビット集合 adj[0..6] を構築し、全ての u<v に対し
`popcount(adj[u] & adj[v]) <= 1` を要求する。この条件を全2^21集合で直接評価した結果、上記の安全集合数と極大数が一致した。

## 未解決

d=7のmisère勝敗・全局面Grundy分布の独立照合、d>=8での一般則は未解決。前回のd=4..6と合わせ、重み2層の空盤Grundyは d=4:0、d=5:1、d=6:1、d=7:1。
