// Exact named-vertex Node Kayles census: k<=4, odd private leaves,
// each non-private support 0/1, then two copies of one support.
#include <bits/stdc++.h>
using namespace std;
int g(int k,const vector<int>&sigs){
  int n=k+sigs.size();
  vector<unsigned> closed(n);
  for(int i=0;i<k;i++)closed[i]=(1u<<k)-1;
  for(int j=0;j<(int)sigs.size();j++){
    int v=k+j;closed[v]=1u<<v;
    for(int i=0;i<k;i++)if((sigs[j]>>i)&1){
      closed[i]|=1u<<v;closed[v]|=1u<<i;
    }
  }
  vector<int8_t> memo(1u<<n,-1);memo[0]=0;
  auto rec=[&](auto&&self,unsigned mask)->int{
    if(memo[mask]>=0)return memo[mask];
    unsigned options=0;
    for(unsigned bits=mask;bits;bits&=bits-1){
      int i=__builtin_ctz(bits);
      options|=1u<<self(self,mask&~closed[i]);
    }
    return memo[mask]=__builtin_ctz(~options);
  };
  return rec(rec,(1u<<n)-1);
}
int main(){
  {vector<int> base={1,2,4,8,3,12};
   assert(g(4,base)==1);
   base.push_back(15);base.push_back(15);
   assert(g(4,base)==2);
  }
  for(int k=2;k<=4;k++){
    vector<int> support;
    for(int s=1;s<(1<<k);s++)
      if(__builtin_popcount((unsigned)s)>=2)support.push_back(s);
    map<int,long long> checked,failed;
    map<int,pair<int,vector<int>>> minimal;
    for(int mask=0;mask<(1<<(int)support.size());mask++){
      vector<int> a;
      for(int i=0;i<k;i++)a.push_back(1<<i);
      for(int i=0;i<(int)support.size();i++)
        if(mask>>i&1)a.push_back(support[i]);
      int base=g(k,a);
      for(int s:support){
        int rank=__builtin_popcount((unsigned)s);checked[rank]++;
        a.push_back(s);a.push_back(s);
        int changed=g(k,a);
        a.pop_back();a.pop_back();
        if(changed!=base){
          failed[rank]++;
          int extras=__builtin_popcount((unsigned)mask);
          if(!minimal.count(rank)||extras<minimal[rank].first){
            vector<int> odd(a.begin()+k,a.end());
            odd.push_back(s);
            minimal[rank]={extras,odd};
          }
        }
      }
    }
    if(k==2)assert(checked[2]==2 && failed[2]==0);
    if(k==3)assert(checked[2]==48 && checked[3]==16 &&
                    failed[2]==0 && failed[3]==0);
    if(k==4){
      assert(checked[2]==12288 && checked[3]==8192 && checked[4]==2048);
      assert(failed[2]==0 && failed[3]==0 && failed[4]==64);
      assert(minimal[4].first==2);
    }
    cout<<"k="<<k<<"\n";
    for(auto [rank,n]:checked){
      cout<<"  rank="<<rank<<" checked="<<n<<" failures="<<failed[rank];
      if(minimal.count(rank)){
        auto [extras,example]=minimal[rank];
        cout<<" minimum odd extra types="<<extras<<" supports=";
        for(int s:example)cout<<s<<",";
      }
      cout<<"\n";
    }
  }
}
