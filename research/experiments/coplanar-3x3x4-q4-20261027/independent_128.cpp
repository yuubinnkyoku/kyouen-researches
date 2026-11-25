// 128-bit extension of independent.cpp for m=8 (N=72 cells exceeds
// uint64_t). Same independent design as independent.cpp: 3D cross-product
// determinant (not Leibniz), point order (z,y,x) instead of (x,y,z),
// root DFS with memoised mex (not bottom-up levels). The std::unordered_map
// memo is replaced by a flat open-addressing table (different hash) purely
// for memory scale; geometry, point order and traversal are unchanged.
// Also accumulates the same order-independent state hash as enum2_128.cpp,
// translating masks into the (x,y,z) labelling before mixing, so the two
// implementations can be compared state-by-state in aggregate.
#include <bits/stdc++.h>
using namespace std;
using U=unsigned __int128;
struct P{int x,y,z;};
P p[72];int N,M;
U forbidden[72][72][72];
int det(P a,P b,P c,P d){int x=b.x-a.x,y=b.y-a.y,z=b.z-a.z;int X=c.x-a.x,Y=c.y-a.y,Z=c.z-a.z;int xx=d.x-a.x,yy=d.y-a.y,zz=d.z-a.z;return x*(Y*zz-Z*yy)-y*(X*zz-Z*xx)+z*(X*yy-Y*xx);}
static inline uint64_t splitmix64(uint64_t x){x+=0x9e3779b97f4a7c15ULL;x=(x^(x>>30))*0xbf58476d1ce4e5b9ULL;x=(x^(x>>27))*0x94d049bb133111ebULL;return x^(x>>31);}
static inline int ctz128(U t){uint64_t lo=(uint64_t)t;if(lo)return __builtin_ctzll(lo);return 64+__builtin_ctzll((uint64_t)(t>>64));}
static inline int pop128(U t){return __builtin_popcountll((uint64_t)t)+__builtin_popcountll((uint64_t)(t>>64));}
static inline uint64_t stateMix(U s,int g,int h){uint64_t lo=(uint64_t)s,hi=(uint64_t)(s>>64);return splitmix64(lo^splitmix64(hi+0x9e3779b97f4a7c15ULL)^(uint64_t)(g*1000003+h));}
int transIdx[72]; // B label (z,y,x) -> A label (x,y,z) index
struct Table{
    vector<U> keys;vector<uint16_t> vals;size_t mask=0,used=0;
    Table(){size_t cap=1<<20;keys.assign(cap,~U(0));vals.assign(cap,0);mask=cap-1;}
    void init(int capExp){size_t cap=size_t(1)<<capExp;keys.assign(cap,~U(0));vals.assign(cap,0);mask=cap-1;used=0;}
    static inline uint64_t h128(U x){uint64_t lo=(uint64_t)x,hi=(uint64_t)(x>>64);return splitmix64(hi^splitmix64(lo+0x85ebca6bULL));}
    void grow(){vector<U> ok=move(keys);vector<uint16_t> ov=move(vals);size_t cap=(mask+1)*2;keys.assign(cap,~U(0));vals.assign(cap,0);mask=cap-1;used=0;
        for(size_t i=0;i<ok.size();i++)if(ok[i]!=~U(0)){size_t h=h128(ok[i])&mask;while(keys[h]!=~U(0))h=(h+1)&mask;keys[h]=ok[i];vals[h]=ov[i];used++;}}
    // returns pointer to value slot if present, else nullptr
    uint16_t* find(U k){size_t h=h128(k)&mask;while(true){U kk=keys[h];if(kk==k)return &vals[h];if(kk==~U(0))return nullptr;h=(h+1)&mask;}}
    void put(U k,uint16_t v){if((used+1)*10>(mask+1)*7)grow();size_t h=h128(k)&mask;while(keys[h]!=~U(0))h=(h+1)&mask;keys[h]=k;vals[h]=v;used++;}
};
Table memo;
uint64_t layer[80]={}, terminals[80]={}, histg[32]={}, histh[32]={};
int maxK=0,minS=100;
uint64_t hashXor=0,hashSum=0;
U blocked(U s){int a[72],n=0;for(U t=s;t;t&=t-1)a[n++]=ctz128(t);U r=0;for(int i=0;i<n;i++)for(int j=i+1;j<n;j++)for(int k=j+1;k<n;k++)r|=forbidden[a[i]][a[j]][a[k]];return r;}
struct Val{uint8_t g,h;};
Val dfs(U s){
    if(uint16_t* f=memo.find(s))return Val{uint8_t((*f)&255),uint8_t((*f)>>8)};
    int n=pop128(s);U legal=((U(1)<<N)-1)&~(s|blocked(s));bool gseen[64]={},hseen[64]={};
    if(!legal){terminals[n]++;minS=min(minS,n);maxK=max(maxK,n);}
    else{for(U t=legal;t;t&=t-1){U bit=t&-t;auto v=dfs(s|bit);gseen[v.g]=1;hseen[v.h]=1;}}
    int g=0,h=0;while(gseen[g])g++;if(!legal)h=1;else while(hseen[h])h++;
    memo.put(s,uint16_t(g|(h<<8)));layer[n]++;histg[g]++;histh[h]++;
    U am=0;for(U t=s;t;t&=t-1)am|=U(1)<<transIdx[ctz128(t)];
    uint64_t mx=stateMix(am,g,h);hashXor^=mx;hashSum+=mx;
    return Val{uint8_t(g),uint8_t(h)};
}
int main(int argc,char**argv){if(argc<2||argc>3)return 2;int m=atoi(argv[1]);if(m<1||m>8)return 2;if(argc==3)memo.init(atoi(argv[2]));M=m;int n=9*m;N=n;int i=0;
    for(int z=0;z<m;z++)for(int y=0;y<3;y++)for(int x=0;x<3;x++){p[i]={x,y,z};transIdx[i]=(x*3+y)*m+z;i++;}
    long long cnt=0;for(int a=0;a<n;a++)for(int b=a+1;b<n;b++)for(int c=b+1;c<n;c++)for(int d=c+1;d<n;d++)if(det(p[a],p[b],p[c],p[d])==0){cnt++;for(int j:{a,b,c,d}){int q[3],k=0;for(int t:{a,b,c,d})if(t!=j)q[k++]=t;sort(q,q+3);forbidden[q[0]][q[1]][q[2]]|=U(1)<<j;}}
    auto root=dfs(0);
    cout<<"m="<<m<<" forbidden="<<cnt<<" states="<<memo.used<<" K="<<maxK<<" s="<<minS<<" g(empty)="<<int(root.g)<<" h(empty)="<<int(root.h)<<"\n";
    cout<<"statehash_xor="<<hex<<hashXor<<" statehash_sum="<<hashSum<<dec<<"\n";
    for(int k=0;k<=n;k++)if(layer[k])cout<<"layer "<<k<<" states "<<layer[k]<<" terminal "<<terminals[k]<<"\n";
    for(int k=0;k<32;k++)if(histg[k]||histh[k])cout<<"nimber "<<k<<" normal "<<histg[k]<<" misere "<<histh[k]<<"\n";
    cout<<"first_moves:";for(int j=0;j<n;j++){auto v=dfs(U(1)<<j);cout<<" ("<<p[j].x<<","<<p[j].y<<","<<p[j].z<<")=["<<int(v.g)<<","<<int(v.h)<<"]";}cout<<"\n";return 0;}
