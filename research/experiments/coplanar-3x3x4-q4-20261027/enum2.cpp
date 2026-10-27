// Second independent implementation for the 3x3xm coplanar board, written
// for m=7 cross-verification. Deliberately different from independent.cpp:
// bottom-up level generation (not root DFS), Leibniz 4x4 homogeneous
// determinant (not 3D cross product), and the Python verify.py point order
// (x outer, y middle, z inner). Values are computed level by level from the
// top down with an open-addressing mask->index table per level.
#include <bits/stdc++.h>
using namespace std;
using U=uint64_t;
struct P{int x,y,z;};
P p[64];int N,m;
U blocked3[64][64][64];
long long det4(int a,int b,int c,int d){
    int v[4][4]={{p[a].x,p[a].y,p[a].z,1},{p[b].x,p[b].y,p[b].z,1},{p[c].x,p[c].y,p[c].z,1},{p[d].x,p[d].y,p[d].z,1}};
    int idx[4]={0,1,2,3};long long s=0;
    do{int inv=0;for(int i=0;i<4;i++)for(int j=i+1;j<4;j++)if(idx[i]>idx[j])inv++;
        long long term=1;for(int i=0;i<4;i++)term*=v[i][idx[i]];
        s+=(inv%2?-term:term);}while(next_permutation(idx,idx+4));
    return s;
}
static inline U splitmix64(U x){x+=0x9e3779b97f4a7c15ULL;x=(x^(x>>30))*0xbf58476d1ce4e5b9ULL;x=(x^(x>>27))*0x94d049bb133111ebULL;return x^(x>>31);}
struct OAMap{
    vector<U> keys;vector<uint32_t> vals;size_t mask;
    OAMap(){}
    OAMap(const vector<U>& level){size_t cap=1;while(cap<level.size()*2)cap<<=1;keys.assign(cap,~U(0));vals.assign(cap,0);mask=cap-1;
        for(uint32_t i=0;i<level.size();i++){size_t h=splitmix64(level[i])&mask;while(keys[h]!=~U(0))h=(h+1)&mask;keys[h]=level[i];vals[h]=i;}}
    uint32_t get(U k)const{size_t h=splitmix64(k)&mask;while(keys[h]!=k)h=(h+1)&mask;return vals[h];}
};
int main(int argc,char**argv){
    if(argc!=2)return 2;m=atoi(argv[1]);if(m<1||m>7)return 2;N=9*m;
    int i=0;for(int x=0;x<3;x++)for(int y=0;y<3;y++)for(int z=0;z<m;z++)p[i++]={x,y,z};
    long long cnt=0;
    for(int a=0;a<N;a++)for(int b=a+1;b<N;b++)for(int c=b+1;c<N;c++)for(int d=c+1;d<N;d++)
        if(det4(a,b,c,d)==0){cnt++;int q[4]={a,b,c,d};
            for(int j=0;j<4;j++){int t[3],k=0;for(int u=0;u<4;u++)if(u!=j)t[k++]=q[u];blocked3[t[0]][t[1]][t[2]]|=U(1)<<q[j];}}
    // level generation, increasing masks
    vector<vector<U>> levels;levels.push_back({0});
    vector<int> ids;ids.reserve(16);
    auto triples_blocked=[&](U s,U&bad){ids.clear();for(U t=s;t;t&=t-1)ids.push_back(__builtin_ctzll(t));bad=0;
        int n=ids.size();for(int a=0;a<n;a++)for(int b=a+1;b<n;b++)for(int c=b+1;c<n;c++)bad|=blocked3[ids[a]][ids[b]][ids[c]];};
    while(true){vector<U> nxt;const vector<U>& cur=levels.back();
        for(U s:cur){U bad;triples_blocked(s,bad);int start=ids.empty()?0:ids.back()+1;
            for(int v=start;v<N;v++)if(!(bad>>v&1))nxt.push_back(s|(U(1)<<v));}
        if(nxt.empty())break;
        sort(nxt.begin(),nxt.end());nxt.erase(unique(nxt.begin(),nxt.end()),nxt.end());
        levels.push_back(move(nxt));}
    int K=(int)levels.size()-1;
    vector<vector<uint8_t>> G(K+1),H(K+1);
    vector<long long> term(K+1,0),hg(32,0),hh(32,0);
    long long total=0;int minS=100;
    U ALL=(N==64)?~U(0):((U(1)<<N)-1);
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
            hg[gCur[ii]]++;hh[hCur[ii]]++;}
        G[k]=gCur;H[k]=hCur;
        if(k>0){nextMap=OAMap(levels[k]);gNext=G[k];hNext=H[k];}
    }
    int ri=lower_bound(levels[0].begin(),levels[0].end(),U(0))-levels[0].begin();
    cout<<"m="<<m<<" forbidden="<<cnt<<" states="<<total<<" K="<<K<<" s="<<minS<<" g(empty)="<<int(G[0][ri])<<" h(empty)="<<int(H[0][ri])<<"\n";
    for(int k=0;k<=K;k++)cout<<"layer "<<k<<" states "<<levels[k].size()<<" terminal "<<term[k]<<"\n";
    for(int k=0;k<32;k++)if(hg[k]||hh[k])cout<<"nimber "<<k<<" normal "<<hg[k]<<" misere "<<hh[k]<<"\n";
    cout<<"first_moves:";
    OAMap oneMap(levels[1]);
    for(int j=0;j<N;j++){uint32_t ci=oneMap.get(U(1)<<j);cout<<" ("<<p[j].x<<","<<p[j].y<<","<<p[j].z<<")=["<<int(G[1][ci])<<","<<int(H[1][ci])<<"]";}
    cout<<"\n";
    return 0;
}
