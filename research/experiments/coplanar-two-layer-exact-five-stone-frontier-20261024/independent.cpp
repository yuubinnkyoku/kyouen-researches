// Independent integer-cross-product census. No direction normalization or bitsets.
#include <iostream>
#include <tuple>
#include <utility>
#include <vector>
using namespace std;
struct P {int y,z;};
int det(P a,P b,P c){
    return (b.y-a.y)*(c.z-a.z)-(b.z-a.z)*(c.y-a.y);
}
bool parallel(P a,P b,P c,P d){
    return (b.y-a.y)*(d.z-c.z)==(b.z-a.z)*(d.y-c.y);
}
pair<long long,long long> census(int k,int m){
    vector<P> p;
    for(int y=0;y<k;++y)for(int z=0;z<m;++z)p.push_back({y,z});
    int n=static_cast<int>(p.size());
    long long safe=0,maximal=0;
    for(int a=0;a<n;++a)for(int b=a+1;b<n;++b)for(int c=b+1;c<n;++c){
        if(det(p[a],p[b],p[c])==0)continue;
        for(int u=0;u<n;++u)for(int v=u+1;v<n;++v){
            if(parallel(p[u],p[v],p[a],p[b])||
               parallel(p[u],p[v],p[a],p[c])||
               parallel(p[u],p[v],p[b],p[c]))continue;
            ++safe;
            bool extend=false;
            for(int t=0;t<n;++t){
                if(t==u||t==v||det(p[u],p[v],p[t])==0)continue;
                if(parallel(p[u],p[t],p[a],p[b])||
                   parallel(p[u],p[t],p[a],p[c])||
                   parallel(p[u],p[t],p[b],p[c]))continue;
                if(parallel(p[v],p[t],p[a],p[b])||
                   parallel(p[v],p[t],p[a],p[c])||
                   parallel(p[v],p[t],p[b],p[c]))continue;
                extend=true;
                break;
            }
            if(!extend)++maximal;
        }
    }
    return {safe,maximal};
}
int main(){
    const vector<tuple<int,int,long long,long long>> cases={
        {3,3,1332,532},{3,4,7528,592},{3,5,26340,332},
        {3,6,71826,18},{3,7,164556,0},{4,4,40368,304},
        {4,5,139380,44},{4,6,377096,0},{4,7,857168,0}
    };
    for(auto [k,m,s,e]:cases){
        auto [safe,maximal]=census(k,m);
        cout<<k<<"x"<<m<<" safe="<<safe<<" maximal="<<maximal<<"\n";
        if(safe!=s||maximal!=e)return 1;
    }
}
