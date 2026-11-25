// Independent C++ integer-circle and subset audit. No repo headers.
#include <boost/multiprecision/cpp_int.hpp>
#include <algorithm>
#include <cassert>
#include <iostream>
#include <numeric>
#include <vector>
#include <tuple>
#include <utility>
using boost::multiprecision::cpp_int;
using namespace std;
using P=pair<cpp_int,cpp_int>;
cpp_int gcd_big(cpp_int a,cpp_int b){while(b!=0){cpp_int r=a%b;a=b;b=r;}return a;}
cpp_int power10(int n){cpp_int r=1;while(n--)r*=10;return r;}
cpp_int orient(const P&a,const P&b,const P&c){return (b.first-a.first)*(c.second-a.second)-(c.first-a.first)*(b.second-a.second);}
cpp_int norm(const P&a){return a.first*a.first+a.second*a.second;}
bool same_circle(const P&a,const P&b,const P&c,const P&d){
    cpp_int det=orient(a,b,c);
    assert(det!=0); // constructed boards have no collinear triples
    cpp_int x1=b.first-a.first,y1=b.second-a.second;
    cpp_int x2=c.first-a.first,y2=c.second-a.second;
    cpp_int n1=norm(b)-norm(a),n2=norm(c)-norm(a);
    cpp_int A=-n1*y2+n2*y1, B=-x1*n2+x2*n1;
    return det*(norm(d)-norm(a))+A*(d.first-a.first)+B*(d.second-a.second)==0;
}
struct Stats{int graphs=0,quad=0,subsets=0;};
tuple<int,int,int> audit(int n, const vector<pair<int,int>>&edges, Stats&stats){
    vector<cpp_int>t;
    for(int i=0;i<n;i++)t.push_back(power10(i));
    for(auto [u,v]:edges)t.push_back(-power10(u)-power10(v));
    cpp_int L=1;
    for(auto x:t){cpp_int f=x*(1+4*x*x*x*x);if(f<0)f=-f;L=L/gcd_big(L,f)*f;}
    vector<P>p{{0,0}};
    for(auto x:t){cpp_int f=1+4*x*x*x*x;p.push_back({L/(x*f),2*L*x/f});}
    int N=(int)p.size();
    for(int i=0;i<N;i++)for(int j=i+1;j<N;j++)for(int k=j+1;k<N;k++)assert(orient(p[i],p[j],p[k])!=0);
    vector<unsigned long long>bad;
    for(int a=0;a<N;a++)for(int b=a+1;b<N;b++)for(int c=b+1;c<N;c++)for(int d=c+1;d<N;d++){
        if(same_circle(p[a],p[b],p[c],p[d]))bad.push_back((1ULL<<a)|(1ULL<<b)|(1ULL<<c)|(1ULL<<d));
        stats.quad++;
    }
    vector<unsigned long long>expected;
    for(int i=0;i<(int)edges.size();i++){
        auto [u,v]=edges[i];expected.push_back((1ULL<<0)|(1ULL<<(u+1))|(1ULL<<(v+1))|(1ULL<<(n+1+i)));
    }
    sort(bad.begin(),bad.end());sort(expected.begin(),expected.end());assert(bad==expected);
    unsigned long long fixed=1;
    for(int i=n+1;i<N;i++)fixed|=1ULL<<i;
    int total=0,maxsize=0,minmax=n+1,maxmax=0,maximal=0;
    for(int mask=0;mask<(1<<n);mask++){
        unsigned long long S=fixed;
        for(int j=0;j<n;j++)if(mask>>j&1)S|=1ULL<<(j+1);
        bool geo=true;
        for(auto b:bad)if((S&b)==b){geo=false;break;}
        bool graph=true;
        for(auto [u,v]:edges)if((mask>>u&1)&&(mask>>v&1)){graph=false;break;}
        assert(geo==graph);
        stats.subsets++;
        if(!geo)continue;
        total++;int k=__builtin_popcount((unsigned)mask);maxsize=max(maxsize,k);
        bool terminal=true;
        for(int j=0;j<n;j++)if(!(mask>>j&1)){
            unsigned long long T=S|(1ULL<<(j+1));
            bool blocked=false;
            for(auto b:bad)if((T&b)==b){blocked=true;break;}
            if(!blocked){terminal=false;break;}
        }
        bool dominating=true;
        for(int j=0;j<n;j++)if(!(mask>>j&1)){
            bool neighbor=false;
            for(auto [u,v]:edges)if((u==j&&(mask>>v&1))||(v==j&&(mask>>u&1)))neighbor=true;
            if(!neighbor){dominating=false;break;}
        }
        assert(terminal==dominating);
        if(terminal){maximal++;minmax=min(minmax,k);maxmax=max(maxmax,k);}
    }
    if(n>=2 && edges.size()==(size_t)(n-1)){
        bool star=true;
        for(int j=1;j<n;j++)if(find(edges.begin(),edges.end(),make_pair(0,j))==edges.end())star=false;
        if(star){assert(total==(1<<(n-1))+1);assert(maxsize==n-1);assert(minmax==1);assert(maximal==2);}
    }
    stats.graphs++;
    return {maximal,minmax,maxmax};
}
int main(){Stats stats;
    for(int n=0;n<=4;n++){
        vector<pair<int,int>>pairs;
        for(int u=0;u<n;u++)for(int v=u+1;v<n;v++)pairs.push_back({u,v});
        for(int mask=0;mask<(1<<(int)pairs.size());mask++){
            vector<pair<int,int>>edges;
            for(int j=0;j<(int)pairs.size();j++)if(mask>>j&1)edges.push_back(pairs[j]);
            audit(n,edges,stats);
        }
    }
    for(int t=1;t<=5;t++){vector<pair<int,int>>edges;for(int j=1;j<=t;j++)edges.push_back({0,j});audit(t+1,edges,stats);}
    // The corona of a graph has one private pendant leaf per original vertex.
    // Its maximal independent sets encode all independent sets of the original graph.
    for(int n=0;n<=3;n++){
        vector<pair<int,int>>pairs;
        for(int u=0;u<n;u++)for(int v=u+1;v<n;v++)pairs.push_back({u,v});
        for(int mask=0;mask<(1<<(int)pairs.size());mask++){
            vector<pair<int,int>>edges;
            for(int j=0;j<(int)pairs.size();j++)if(mask>>j&1)edges.push_back(pairs[j]);
            int expected=0;
            for(int s=0;s<(1<<n);s++){
                bool independent=true;
                for(auto [u,v]:edges)if((s>>u&1)&&(s>>v&1))independent=false;
                if(independent)expected++;
            }
            vector<pair<int,int>>corona=edges;
            for(int i=0;i<n;i++)corona.push_back({i,n+i});
            auto [count,small,large]=audit(2*n,corona,stats);
            assert(count==expected && small==n && large==n);
        }
    }
    for(auto edges:vector<vector<pair<int,int>>>{{{0,1},{1,2},{2,3}},
        {{0,1},{0,2},{0,3},{1,2},{1,3},{2,3}}}){
        int expected=0;
        for(int s=0;s<16;s++){
            bool independent=true;
            for(auto [u,v]:edges)if((s>>u&1)&&(s>>v&1))independent=false;
            if(independent)expected++;
        }
        vector<pair<int,int>>corona=edges;
        for(int i=0;i<4;i++)corona.push_back({i,4+i});
        auto [count,small,large]=audit(8,corona,stats);
        assert(count==expected && small==4 && large==4);
    }
    cout<<"graphs="<<stats.graphs<<" quadruples="<<stats.quad<<" subsets="<<stats.subsets<<" PASS\n";
}
