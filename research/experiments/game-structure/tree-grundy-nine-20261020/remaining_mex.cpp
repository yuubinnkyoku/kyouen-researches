// Independent recurrence: state is the surviving induced vertex set.
#include <bits/stdc++.h>
using namespace std;
int main(){ios::sync_with_stdio(false);cin.tie(nullptr);int n;
while(cin>>n && n){vector<uint32_t> adj(n);for(auto &a:adj)cin>>a;
vector<int8_t> memo(1u<<n,-1);memo[0]=0;
auto sg=[&](auto&& self,uint32_t remain)->int{
  auto &res=memo[remain]; if(res>=0)return res;
  uint32_t children=0, temp=remain;
  while(temp){uint32_t b=temp&-temp;temp-=b;int v=__builtin_ctz(b);
    int g=self(self,remain & ~(b|adj[v])); children|=1u<<g;
  }
  int val=0;while(children&(1u<<val))++val;
  return res=val;
};cout<<sg(sg,(1u<<n)-1)<<'\n';
}}
