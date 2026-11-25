// Find second moves that force a terminal fourth move against every third.
// A 4-set is terminal iff its four lifted rows have affine rank <=2,
// for a cube of side >=3 (the entire lifted board has affine rank 4).
#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <vector>
using U=__uint128_t;
using P=std::array<int64_t,4>;
int64_t det3(const P& a,const P& b,const P& c,int i,int j,int k) {
    return a[i]*(b[j]*c[k]-b[k]*c[j])-a[j]*(b[i]*c[k]-b[k]*c[i])
           +a[k]*(b[i]*c[j]-b[j]*c[i]);
}
int main(int argc,char**argv) {
    if(argc!=2) return 2;
    int side=std::stoi(argv[1]),n=side*side*side;
    if(side<3 || n>128) return 2;
    uint64_t choose[129][5]{};
    for(int i=0;i<=n;i++) {
        choose[i][0]=1;
        for(int j=1;j<=4;j++)if(i)choose[i][j]=choose[i-1][j]+choose[i-1][j-1];
    }
    auto index=[&](int a,int b,int c){return choose[a][1]+choose[b][2]+choose[c][3];};
    std::vector<P> points;
    for(int x=0;x<side;x++)for(int y=0;y<side;y++)for(int z=0;z<side;z++)
        points.push_back({x*x+y*y+z*z,x,y,z});
    std::vector<U> fourth(choose[n][3]);
    uint64_t terminals=0;
    for(int a=0;a<n;a++)for(int b=a+1;b<n;b++)for(int c=b+1;c<n;c++) {
        P v{},w{};
        for(int j=0;j<4;j++){v[j]=points[b][j]-points[a][j];w[j]=points[c][j]-points[a][j];}
        for(int d=c+1;d<n;d++) {
            P t{};for(int j=0;j<4;j++)t[j]=points[d][j]-points[a][j];
            if(det3(v,w,t,0,1,2)||det3(v,w,t,0,1,3)||det3(v,w,t,0,2,3)||det3(v,w,t,1,2,3))continue;
            ++terminals;
            fourth[index(a,b,c)]|=U(1)<<d;
            fourth[index(a,b,d)]|=U(1)<<c;
            fourth[index(a,c,d)]|=U(1)<<b;
            fourth[index(b,c,d)]|=U(1)<<a;
        }
    }
    std::cout<<"{\"side\":"<<side<<",\"terminal_four_sets\":"<<terminals<<",\"opening_orbits\":[";
    bool first=true;
    for(int x=0;x<=(side-1)/2;x++)for(int y=x;y<=(side-1)/2;y++)for(int z=y;z<=(side-1)/2;z++) {
        int a=(x*side+y)*side+z;
        std::vector<std::pair<int,int>> ranked;
        for(int b=0;b<n;b++)if(b!=a) {
            int missed=0;
            for(int c=0;c<n;c++)if(c!=a && c!=b) {
                int ids[3]{a,b,c};std::sort(ids,ids+3);
                missed+=!fourth[index(ids[0],ids[1],ids[2])];
            }
            ranked.emplace_back(missed,b);
        }
        std::sort(ranked.begin(),ranked.end());
        if(!first)std::cout<<",";
        first=false;
        std::cout<<"{\"first\":"<<a<<",\"best_uncovered_thirds\":"<<ranked[0].first<<",\"best_replies\":[";
        bool f=true;
        for(auto [missed,b]:ranked)if(missed==ranked[0].first){if(!f)std::cout<<",";f=false;std::cout<<b;}
        std::cout<<"]}";
    }
    std::cout<<"]}\n";
}
