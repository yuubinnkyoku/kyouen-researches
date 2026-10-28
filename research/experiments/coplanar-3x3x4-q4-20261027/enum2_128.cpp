// 128-bit extension of enum2.cpp for m=8 (N=72 cells exceeds uint64_t).
// Same design as enum2.cpp: bottom-up level generation, Leibniz 4x4
// homogeneous determinant, point order (x outer, y middle, z inner),
// level-by-level evaluation from the top with an open-addressing
// mask->index table per level. Changes vs enum2.cpp: unsigned __int128
// masks, 128-bit splitmix hash, freeing each level's masks once the level
// below has been evaluated (memory), an order-independent state hash over
// (mask, g, h) for cross-implementation comparison, and an optional dump
// of the top (maximum-size) level masks as decimal integers (argv[2]).
#include <bits/stdc++.h>
using namespace std;
using U=unsigned __int128;
struct P{int x,y,z;};
P p[72];int N,m;
U blocked3[72][72][72];
long long det4(int a,int b,int c,int d){
    int v[4][4]={{p[a].x,p[a].y,p[a].z,1},{p[b].x,p[b].y,p[b].z,1},{p[c].x,p[c].y,p[c].z,1},{p[d].x,p[d].y,p[d].z,1}};
    int idx[4]={0,1,2,3};long long s=0;
    do{int inv=0;for(int i=0;i<4;i++)for(int j=i+1;j<4;j++)if(idx[i]>idx[j])inv++;
        long long term=1;for(int i=0;i<4;i++)term*=v[i][idx[i]];
        s+=(inv%2?-term:term);}while(next_permutation(idx,idx+4));
    return s;
}
static inline uint64_t splitmix64(uint64_t x){x+=0x9e3779b97f4a7c15ULL;x=(x^(x>>30))*0xbf58476d1ce4e5b9ULL;x=(x^(x>>27))*0x94d049bb133111ebULL;return x^(x>>31);}
static inline uint64_t hash128(U x){uint64_t lo=(uint64_t)x,hi=(uint64_t)(x>>64);return splitmix64(lo^splitmix64(hi+0x9e3779b97f4a7c15ULL));}
static inline int ctz128(U t){uint64_t lo=(uint64_t)t;if(lo)return __builtin_ctzll(lo);return 64+__builtin_ctzll((uint64_t)(t>>64));}
static inline uint64_t stateMix(U s,int g,int h){uint64_t lo=(uint64_t)s,hi=(uint64_t)(s>>64);return splitmix64(lo^splitmix64(hi+0x9e3779b97f4a7c15ULL)^(uint64_t)(g*1000003+h));}
struct OAMap{
    vector<U> keys;vector<uint32_t> vals;size_t mask;
    OAMap(){}
    OAMap(const vector<U>& level){size_t cap=1;while(cap<level.size()*2)cap<<=1;keys.assign(cap,~U(0));vals.assign(cap,0);mask=cap-1;
        for(uint32_t i=0;i<level.size();i++){size_t h=hash128(level[i])&mask;while(keys[h]!=~U(0))h=(h+1)&mask;keys[h]=level[i];vals[h]=i;}}
    uint32_t get(U k)const{size_t h=hash128(k)&mask;while(keys[h]!=k)h=(h+1)&mask;return vals[h];}
};
int main(int argc,char**argv){
    if(argc<2||argc>3)return 2;m=atoi(argv[1]);if(m<1||m>8)return 2;N=9*m;
    int i=0;for(int x=0;x<3;x++)for(int y=0;y<3;y++)for(int z=0;z<m;z++)p[i++]={x,y,z};
    long long cnt=0;
    for(int a=0;a<N;a++)for(int b=a+1;b<N;b++)for(int c=b+1;c<N;c++)for(int d=c+1;d<N;d++)
        if(det4(a,b,c,d)==0){cnt++;int q[4]={a,b,c,d};
            for(int j=0;j<4;j++){int t[3],k=0;for(int u=0;u<4;u++)if(u!=j)t[k++]=q[u];blocked3[t[0]][t[1]][t[2]]|=U(1)<<q[j];}}
    // level generation, increasing masks
    vector<vector<U>> levels;levels.push_back({0});
    vector<int> ids;ids.reserve(16);
    auto triples_blocked=[&](U s,U&bad){ids.clear();for(U t=s;t;t&=t-1)ids.push_back(ctz128(t));bad=0;
        int n=ids.size();for(int a=0;a<n;a++)for(int b=a+1;b<n;b++)for(int c=b+1;c<n;c++)bad|=blocked3[ids[a]][ids[b]][ids[c]];};
    while(true){vector<U> nxt;const vector<U>& cur=levels.back();
        for(U s:cur){U bad;triples_blocked(s,bad);int start=ids.empty()?0:ids.back()+1;
            for(int v=start;v<N;v++)if(!(bad>>v&1))nxt.push_back(s|(U(1)<<v));}
        if(nxt.empty())break;
        sort(nxt.begin(),nxt.end());nxt.erase(unique(nxt.begin(),nxt.end()),nxt.end());
        levels.push_back(move(nxt));}
    int K=(int)levels.size()-1;
    if(argc==3){ofstream out(argv[2]);for(U s:levels[K]){uint64_t lo=(uint64_t)s,hi=(uint64_t)(s>>64);out<<hi<<" "<<lo<<"\n";}}
    vector<vector<uint8_t>> G(K+1),H(K+1);
    vector<long long> term(K+1,0),hg(32,0),hh(32,0);
    long long total=0;int minS=100;
    U ALL=(U(1)<<N)-1;
    uint64_t hashXor=0,hashSum=0;
    vector<uint8_t> gNext,hNext;
    OAMap nextMap;
    for(int k=K;k>=0;k--){
        const vector<U>& lev=levels[k];total+=lev.size();
        vector<uint8_t> gCur(lev.size()),hCur(lev.size());
        for(size_t ii=0;ii<lev.size();ii++){U s=lev[ii];U bad;triples_blocked(s,bad);
            U legal=ALL&~(s|bad);
            if(!legal){gCur[ii]=0;hCur[ii]=1;term[k]++;minS=min(minS,k);}
            else{bool gs[64]={},hs[64]={};
                for(U t=legal;t;t&=t-1){U bit=t&-t;uint32_t ci=nextMap.get(s|bit);gs[gNext[ci]]=1;hs[hNext[ci]]=1;}
                int g=0,h=0;while(gs[g])g++;while(hs[h])h++;gCur[ii]=g;hCur[ii]=h;}
            hg[gCur[ii]]++;hh[hCur[ii]]++;
            uint64_t mx=stateMix(s,gCur[ii],hCur[ii]);hashXor^=mx;hashSum+=mx;}
        G[k]=gCur;H[k]=hCur;
        if(k>0){nextMap=OAMap(levels[k]);gNext=G[k];hNext=H[k];
            if(k>=2&&k<K){vector<U>().swap(levels[k+1]);}}
    }
    int ri=lower_bound(levels[0].begin(),levels[0].end(),U(0))-levels[0].begin();
    cout<<"m="<<m<<" forbidden="<<cnt<<" states="<<total<<" K="<<K<<" s="<<minS<<" g(empty)="<<int(G[0][ri])<<" h(empty)="<<int(H[0][ri])<<"\n";
    cout<<"statehash_xor="<<hex<<hashXor<<" statehash_sum="<<hashSum<<dec<<"\n";
    // layer sizes for k>=2 were freed during evaluation; counts survive in G[k].size()
    for(int k=0;k<=K;k++)cout<<"layer "<<k<<" states "<<G[k].size()<<" terminal "<<term[k]<<"\n";
    for(int k=0;k<32;k++)if(hg[k]||hh[k])cout<<"nimber "<<k<<" normal "<<hg[k]<<" misere "<<hh[k]<<"\n";
    cout<<"first_moves:";
    OAMap oneMap(levels[1]);
    for(int j=0;j<N;j++){uint32_t ci=oneMap.get(U(1)<<j);cout<<" ("<<p[j].x<<","<<p[j].y<<","<<p[j].z<<")=["<<int(G[1][ci])<<","<<int(H[1][ci])<<"]";}
    cout<<"\n";
    return 0;
}
