// Subtree checker derived from independent_128.cpp: same cross-product
// determinant geometry, same (z,y,x) point order, same root-DFS + memoised
// mex -- but instead of solving the empty board it solves one given
// position (stones passed as "x,y,z;x,y,z;..." in argv[3], possibly the
// empty string), so a single first-move subtree of a board too large for
// a full DFS (m=9) can be verified independently. The memo is fresh for
// each run; Grundy values depend only on the stone set, not on the path,
// so a per-subtree solve is exact. Prints the forbidden-quadruple count
// of the whole board as a by-product (a third geometry check).
#include <bits/stdc++.h>
using namespace std;
using U=unsigned __int128;
struct P{int x,y,z;};
P p[81];int N,M;
U forbidden[81][81][81];
int det(P a,P b,P c,P d){int x=b.x-a.x,y=b.y-a.y,z=b.z-a.z;int X=c.x-a.x,Y=c.y-a.y,Z=c.z-a.z;int xx=d.x-a.x,yy=d.y-a.y,zz=d.z-a.z;return x*(Y*zz-Z*yy)-y*(X*zz-Z*xx)+z*(X*yy-Y*xx);}
static inline uint64_t splitmix64(uint64_t x){x+=0x9e3779b97f4a7c15ULL;x=(x^(x>>30))*0xbf58476d1ce4e5b9ULL;x=(x^(x>>27))*0x94d049bb133111ebULL;return x^(x>>31);}
static inline int ctz128(U t){uint64_t lo=(uint64_t)t;if(lo)return __builtin_ctzll(lo);return 64+__builtin_ctzll((uint64_t)(t>>64));}
static inline int pop128(U t){return __builtin_popcountll((uint64_t)t)+__builtin_popcountll((uint64_t)(t>>64));}
struct Table{
    vector<U> keys;vector<uint16_t> vals;size_t mask=0,used=0;
    Table(){size_t cap=1<<20;keys.assign(cap,~U(0));vals.assign(cap,0);mask=cap-1;}
    void init(int capExp){size_t cap=size_t(1)<<capExp;keys.assign(cap,~U(0));vals.assign(cap,0);mask=cap-1;used=0;}
    static inline uint64_t h128(U x){uint64_t lo=(uint64_t)x,hi=(uint64_t)(x>>64);return splitmix64(hi^splitmix64(lo+0x85ebca6bULL));}
    void grow(){vector<U> ok=move(keys);vector<uint16_t> ov=move(vals);size_t cap=(mask+1)*2;keys.assign(cap,~U(0));vals.assign(cap,0);mask=cap-1;used=0;
        for(size_t i=0;i<ok.size();i++)if(ok[i]!=~U(0)){size_t h=h128(ok[i])&mask;while(keys[h]!=~U(0))h=(h+1)&mask;keys[h]=ok[i];vals[h]=ov[i];used++;}}
    uint16_t* find(U k){size_t h=h128(k)&mask;while(true){U kk=keys[h];if(kk==k)return &vals[h];if(kk==~U(0))return nullptr;h=(h+1)&mask;}}
    void put(U k,uint16_t v){if((used+1)*10>(mask+1)*7)grow();size_t h=h128(k)&mask;while(keys[h]!=~U(0))h=(h+1)&mask;keys[h]=k;vals[h]=v;used++;}
};
Table memo;
U blocked(U s){int a[81],n=0;for(U t=s;t;t&=t-1)a[n++]=ctz128(t);U r=0;for(int i=0;i<n;i++)for(int j=i+1;j<n;j++)for(int k=j+1;k<n;k++)r|=forbidden[a[i]][a[j]][a[k]];return r;}
struct Val{uint8_t g,h;};
Val dfs(U s){
    if(uint16_t* f=memo.find(s))return Val{uint8_t((*f)&255),uint8_t((*f)>>8)};
    U legal=((U(1)<<N)-1)&~(s|blocked(s));bool gseen[64]={},hseen[64]={};
    if(legal){for(U t=legal;t;t&=t-1){U bit=t&-t;auto v=dfs(s|bit);gseen[v.g]=1;hseen[v.h]=1;}}
    int g=0,h=0;while(gseen[g])g++;if(!legal)h=1;else while(hseen[h])h++;
    memo.put(s,uint16_t(g|(h<<8)));
    return Val{uint8_t(g),uint8_t(h)};
}
int main(int argc,char**argv){if(argc<4)return 2;int m=atoi(argv[1]);if(m<1||m>9)return 2;memo.init(atoi(argv[2]));M=m;int n=9*m;N=n;int i=0;
    for(int z=0;z<m;z++)for(int y=0;y<3;y++)for(int x=0;x<3;x++)p[i++]={x,y,z};
    long long cnt=0;for(int a=0;a<n;a++)for(int b=a+1;b<n;b++)for(int c=b+1;c<n;c++)for(int d=c+1;d<n;d++)if(det(p[a],p[b],p[c],p[d])==0){cnt++;for(int j:{a,b,c,d}){int q[3],k=0;for(int t:{a,b,c,d})if(t!=j)q[k++]=t;sort(q,q+3);forbidden[q[0]][q[1]][q[2]]|=U(1)<<j;}}
    U init=0;string spec=argv[3];
    if(!spec.empty()){stringstream ss(spec);string tok;
        while(getline(ss,tok,';')){int x,y,z;sscanf(tok.c_str(),"%d,%d,%d",&x,&y,&z);
            int found=-1;for(int j=0;j<n;j++)if(p[j].x==x&&p[j].y==y&&p[j].z==z)found=j;
            if(found<0){cerr<<"no such cell "<<tok<<"\n";return 2;}
            init|=U(1)<<found;}}
    auto t0=chrono::steady_clock::now();
    auto v=dfs(init);
    auto t1=chrono::steady_clock::now();
    cout<<"m="<<m<<" forbidden="<<cnt<<" init_stones="<<pop128(init)
        <<" g="<<int(v.g)<<" h="<<int(v.h)<<" visited="<<memo.used
        <<" seconds="<<chrono::duration_cast<chrono::milliseconds>(t1-t0).count()/1000.0<<"\n";
    return 0;}
