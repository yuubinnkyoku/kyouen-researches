// Independent full enumeration: direct 4x4 integer determinant per subset.
#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <map>
#include <unordered_map>
#include <vector>
using namespace std;
using P=array<long long,4>;
long long determinant(array<P,4> a){
    long long sum=0;
    for(int i=0;i<4;i++)for(int j=0;j<4;j++)if(i!=j)
    for(int k=0;k<4;k++)if(k!=i&&k!=j){
        int l=6-i-j-k;
        int inv=(i>j)+(i>k)+(i>l)+(j>k)+(j>l)+(k>l);
        sum+=(inv%2?-1:1)*a[0][i]*a[1][j]*a[2][k]*a[3][l];
    }
    return sum;
}
int mex(const vector<int>& values){int x=0;while(find(values.begin(),values.end(),x)!=values.end())x++;return x;}
int main(int argc,char**argv){
    int m=argc>1?stoi(argv[1]):6;
    vector<P> pts;
    for(int x=0;x<2;x++)for(int y=0;y<2;y++)for(int z=0;z<m;z++)pts.push_back({x,y,z,1});
    int n=pts.size();
    if(n>60)return 2;
    vector<vector<uint64_t>> layers(6);
    vector<int> current;
    auto safe=[&](const vector<int>& ids){
        int k=ids.size();
        for(int a=0;a<k;a++)for(int b=a+1;b<k;b++)for(int c=b+1;c<k;c++)for(int d=c+1;d<k;d++)
            if(determinant({pts[ids[a]],pts[ids[b]],pts[ids[c]],pts[ids[d]]})==0)return false;
        return true;
    };
    auto dfs=[&](auto&&self,int start,uint64_t mask)->void{
        if(safe(current))layers[current.size()].push_back(mask);
        else return;
        if(current.size()==5)return;
        for(int i=start;i<n;i++){
            current.push_back(i);
            self(self,i+1,mask|(1ULL<<i));
            current.pop_back();
        }
    };
    dfs(dfs,0,0);
    unordered_map<uint64_t,pair<int,int>> values;
    map<int,int> maximal;
    for(int k=5;k>=0;k--){
        for(uint64_t mask:layers[k]){
            vector<int> gs,hs;
            for(int p=0;p<n;p++)if(!(mask>>p&1)){
                uint64_t child=mask|(1ULL<<p);
                auto it=values.find(child);
                if(it!=values.end()){
                    gs.push_back(it->second.first);
                    hs.push_back(it->second.second);
                }
            }
            if(gs.empty())maximal[k]++;
            values[mask]={mex(gs),gs.empty()?1:mex(hs)};
        }
    }
    cout<<"m="<<m<<" n="<<n<<" safe="<<values.size()<<" K=";
    int K=0,s=100;
    for(int k=0;k<=5;k++)if(layers[k].size())K=k;
    for(auto [k,v]:maximal)if(v)s=min(s,k);
    cout<<K<<" s="<<s<<" root="<<values[0].first<<","<<values[0].second;
    for(int k=0;k<=5;k++)cout<<" layer"<<k<<"="<<layers[k].size()<<" terminal"<<k<<"="<<maximal[k];
    cout<<"\n";
    if(m>=3){
        for(int k=0;k<=5;k++)for(uint64_t mask:layers[k]){
            auto [g,h]=values.at(mask);
            if(g!=((5-k)&1)||h!=(((5-k)&1)^1)){
                cerr<<"PARITY FAILURE m="<<m<<" k="<<k<<" mask="<<mask<<" g="<<g<<" h="<<h<<"\n";
                return 1;
            }
        }
    }
}
