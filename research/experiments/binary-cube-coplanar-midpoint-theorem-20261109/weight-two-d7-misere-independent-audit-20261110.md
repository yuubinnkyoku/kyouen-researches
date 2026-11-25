# 重み2層・7次元 misère 勝敗の独立検算（2026-11-10）

## 結果

先行の `weight-two-d7-misere-retrograde-20261110.md` の全石数別勝敗表を、独立に実装した **共通隣接点による C4 判定** と後退再帰で再検算した。完全一致。

| 石数 | 負け | 勝ち |
|---:|---:|---:|
| 0 | 1 | 0 |
| 1 | 0 | 21 |
| 2 | 210 | 0 |
| 3 | 0 | 1330 |
| 4 | 5880 | 0 |
| 5 | 0 | 18564 |
| 6 | 31444 | 9030 |
| 7 | 2100 | 52650 |
| 8 | 30555 | 5040 |
| 9 | 0 | 6615 |

安全局面 163440、空盤は負け（後手勝ち）。対象は K7 の辺を頂点とし、四角形を作る手を禁止するゲーム。終端を勝ちとする misère 規則。

## 独立検算コード

先行実装の禁止四角形105個の列挙・包含判定を使わず、各部分集合の隣接行列から「2頂点が共通隣接点を2つ以上持つ」ことを C4 の必要十分条件として使用した。安全性は最下位の1ビットを外した部分集合の安全性を利用し、降順に全局面の勝敗を決める。

```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  constexpr int d=7, E=21, L=1<<E;
  vector<pair<int,int>> edges;
  for(int i=0;i<d;i++) for(int j=i+1;j<d;j++) edges.emplace_back(i,j);
  vector<unsigned char> safe(L), win(L);
  int count[10][2] = {};
  safe[0]=1;
  for(int s=1;s<L;s++) {
    int p=s&(s-1);
    if(!safe[p]) continue;
    int adj[7]={};
    for(int j=0;j<E;j++) if((s>>j)&1) {
      auto [a,b]=edges[j];
      adj[a]|=1<<b; adj[b]|=1<<a;
    }
    bool bad=false;
    for(int a=0;a<d&&!bad;a++)
      for(int b=a+1;b<d;b++)
        if(__builtin_popcount((unsigned)(adj[a]&adj[b]))>=2) {
          bad=true; break;
        }
    safe[s]=!bad;
  }
  for(int s=L-1;s>=0;s--) if(safe[s]) {
    bool any=false, can=false;
    for(int j=0;j<E;j++) if(!((s>>j)&1) && safe[s|(1<<j)]) {
      any=true;
      if(!win[s|(1<<j)]) can=true;
    }
    win[s]=!any || can;
    count[__builtin_popcount((unsigned)s)][win[s]]++;
  }
  int total=0;
  for(int i=0;i<10;i++) {
    cout<<i<<" "<<count[i][0]<<" "<<count[i][1]<<"\n";
    total+=count[i][0]+count[i][1];
  }
  cout<<"total "<<total<<" root "<<int(win[0])<<"\n";
}
```

`g++ -O3 -std=c++17 audit.cpp -o audit && ./audit` で上表と `total 163440 root 0` を再現。独立の C4 判定は、単純無向グラフに C4 が存在することと、ある異なる2頂点が共通隣接点を2つ以上持つことの同値性に基づく。

## 証拠の範囲

**有限完全列挙の独立検算**。安全局面判定と勝敗再帰を別実装で照合した。一般次元への外挿はできない。全局面の結果を固定した計算であり、形式証明書の検査ではない。
