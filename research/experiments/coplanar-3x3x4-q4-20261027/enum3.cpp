// Disk-backed bottom-up solver for the 3x3xm 4-coplanar-points-forbidden
// game, built for m=9 (81 cells, ~3e8 safe states) where the in-RAM design
// of enum2_128.cpp no longer fits. Same mathematics as enum2_128.cpp:
// Leibniz 4x4 homogeneous determinant, canonical-parent level generation
// (children add a cell larger than every cell present, so each safe set is
// generated exactly once and no dedup is needed), top-down mex evaluation
// of the normal Grundy g and the misere auxiliary h, and the same
// order-independent state hash over (mask, g, h).
//
// Differences are purely about scale: levels live as raw unsigned __int128
// arrays in files (workdir/L<k>.bin), generation streams parents and
// appends children, and evaluation processes each level in shards -- for
// shard s of S only next-level states with hash128(mask) % S == s are
// loaded into the open-addressing index, so peak memory stays bounded.
// argv[3] selects the point order: 0 = (x,y,z) (canonical), 1 = (z,y,x);
// in order 1 the state hash is accumulated after translating each mask
// into the canonical (x,y,z) labelling, so the two orders must produce
// byte-identical output. Phases: gen writes the level files and meta.txt;
// eval reads them back (rerunnable after a crash without regenerating).
#include <bits/stdc++.h>
using namespace std;
using U=unsigned __int128;
struct P{int x,y,z;};
P p[81];int N,m,ORDER;
int transIdx[81]; // label -> canonical (x,y,z) index
U blocked3[81][81][81];
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
    vector<U> keys;vector<uint32_t> vals;size_t mask=0;
    void init(size_t expected){size_t cap=1;while(cap<expected*2)cap<<=1;keys.assign(cap,~U(0));vals.assign(cap,0);mask=cap-1;}
    void put(U k,uint32_t v){size_t h=hash128(k)&mask;while(keys[h]!=~U(0))h=(h+1)&mask;keys[h]=k;vals[h]=v;}
    uint32_t get(U k)const{size_t h=hash128(k)&mask;while(keys[h]!=k)h=(h+1)&mask;return vals[h];}
};
string workdir;
string levelPath(int k){return workdir+"/L"+to_string(k)+".bin";}
// stream a level file, calling f(mask, position) for each entry
template<class F> void streamLevel(int k,F&&f){
    ifstream in(levelPath(k),ios::binary);if(!in){cerr<<"cannot open "<<levelPath(k)<<"\n";exit(2);}
    vector<U> buf(1<<20);uint64_t pos=0;
    while(in){in.read(reinterpret_cast<char*>(buf.data()),buf.size()*sizeof(U));size_t got=in.gcount()/sizeof(U);
        for(size_t i=0;i<got;i++)f(buf[i],pos++);}
}
int idsBuf[81];
inline U triples_blocked(U s,int&n){
    n=0;for(U t=s;t;t&=t-1)idsBuf[n++]=ctz128(t);U bad=0;
    for(int a=0;a<n;a++)for(int b=a+1;b<n;b++)for(int c=b+1;c<n;c++)bad|=blocked3[idsBuf[a]][idsBuf[b]][idsBuf[c]];
    return bad;
}
void buildGeometry(){
    int i=0;
    if(ORDER==0){for(int x=0;x<3;x++)for(int y=0;y<3;y++)for(int z=0;z<m;z++){p[i]={x,y,z};transIdx[i]=i;i++;}}
    else{for(int z=0;z<m;z++)for(int y=0;y<3;y++)for(int x=0;x<3;x++){p[i]={x,y,z};transIdx[i]=(x*3+y)*m+z;i++;}}
    N=9*m;
}
long long buildBlocked(){
    long long cnt=0;
    for(int a=0;a<N;a++)for(int b=a+1;b<N;b++)for(int c=b+1;c<N;c++)for(int d=c+1;d<N;d++)
        if(det4(a,b,c,d)==0){cnt++;int q[4]={a,b,c,d};
            for(int j=0;j<4;j++){int t[3],k=0;for(int u=0;u<4;u++)if(u!=j)t[k++]=q[u];blocked3[t[0]][t[1]][t[2]]|=U(1)<<q[j];}}
    return cnt;
}
int doGen(){
    long long cnt=buildBlocked();
    vector<unsigned long long> counts;counts.push_back(1);
    {ofstream out(levelPath(0),ios::binary);U z=0;out.write(reinterpret_cast<char*>(&z),sizeof(U));}
    for(int k=0;;k++){
        unsigned long long produced=0;
        ofstream out(levelPath(k+1),ios::binary|ios::trunc);
        vector<U> wbuf;wbuf.reserve(1<<20);
        auto flush=[&](){out.write(reinterpret_cast<const char*>(wbuf.data()),wbuf.size()*sizeof(U));wbuf.clear();};
        streamLevel(k,[&](U s,uint64_t){
            int n;U bad=triples_blocked(s,n);
            int start=n?idsBuf[n-1]+1:0;
            for(int v=start;v<N;v++)if(!(bad>>v&1)){wbuf.push_back(s|(U(1)<<v));produced++;
                if(wbuf.size()>=(1<<20))flush();}
        });
        flush();out.close();
        cerr<<"level "<<k<<" -> "<<produced<<" states\n";
        if(!produced){std::filesystem::remove(levelPath(k+1));break;}
        counts.push_back(produced);
    }
    ofstream meta(workdir+"/meta.txt");
    meta<<"m "<<m<<"\norder "<<ORDER<<"\nforbidden "<<cnt<<"\nlevels "<<counts.size()<<"\n";
    for(auto c:counts)meta<<c<<"\n";
    cerr<<"gen done: K="<<counts.size()-1<<" forbidden="<<cnt<<"\n";
    return 0;
}
int doEval(const char* dumpfile){
    ifstream meta(workdir+"/meta.txt");if(!meta){cerr<<"no meta.txt; run gen first\n";return 2;}
    string key;long long forbidden=0;int mm=-1,oo=-1,nlev=0;
    meta>>key>>mm>>key>>oo>>key>>forbidden>>key>>nlev;
    if(mm!=m||oo!=ORDER){cerr<<"meta mismatch\n";return 2;}
    vector<unsigned long long> counts(nlev);for(int i=0;i<nlev;i++)meta>>counts[i];
    int K=nlev-1;
    buildBlocked();
    U ALL=(N==128)?~U(0):((U(1)<<N)-1);
    vector<long long> term(K+1,0),hg(32,0),hh(32,0);
    uint64_t hashXor=0,hashSum=0;long long total=0;int minS=100;
    vector<uint8_t> gNext,hNext;
    vector<pair<int,int>> firstMoves; // by label index
    auto hashLevel=[&](int k,const vector<uint8_t>&G,const vector<uint8_t>&H){
        streamLevel(k,[&](U s,uint64_t ii){
            U cm=s;if(ORDER==1){cm=0;for(U t=s;t;t&=t-1){int b=ctz128(t);cm|=U(1)<<transIdx[b];}}
            uint64_t mx=stateMix(cm,G[ii],H[ii]);hashXor^=mx;hashSum+=mx;});
    };
    // top level: every state is terminal
    {
        unsigned long long n=counts[K];
        gNext.assign(n,0);hNext.assign(n,1);term[K]=n;minS=min(minS,K);total+=n;
        for(unsigned long long i=0;i<n;i++){hg[0]++;hh[1]++;}
        hashLevel(K,gNext,hNext);
        if(dumpfile){ofstream out(dumpfile);streamLevel(K,[&](U s,uint64_t){out<<(uint64_t)(s>>64)<<" "<<(uint64_t)s<<"\n";});}
        cerr<<"level "<<K<<" done (terminal)\n";
    }
    vector<uint8_t> gCur,hCur;
    for(int k=K-1;k>=0;k--){
        unsigned long long nk=counts[k],nn=counts[k+1];total+=nk;
        int S=(int)max(1LL,(long long)((nn+11999999ULL)/12000000ULL));
        vector<uint32_t> gs(nk,0),hs(nk,0);vector<uint8_t> hasLegal(nk,0);
        for(int sh=0;sh<S;sh++){
            OAMap mp;size_t expect=nn/S+1024;mp.init(expect);
            streamLevel(k+1,[&](U s,uint64_t ii){if(hash128(s)%(uint64_t)S==(uint64_t)sh)mp.put(s,(uint32_t)ii);});
            streamLevel(k,[&](U s,uint64_t ii){
                int n;U bad=triples_blocked(s,n);
                U legal=ALL&~(s|bad);
                if(sh==0)hasLegal[ii]=(legal!=0);
                for(U t=legal;t;t&=t-1){U bit=t&-t;U cm=s|bit;
                    if(hash128(cm)%(uint64_t)S==(uint64_t)sh){uint32_t ci=mp.get(cm);
                        int gv=gNext[ci],hv=hNext[ci];
                        if(gv>=32||hv>=32){cerr<<"nimber >= 32 at level "<<k<<"\n";exit(3);}
                        gs[ii]|=1u<<gv;hs[ii]|=1u<<hv;}}
            });
        }
        gCur.assign(nk,0);hCur.assign(nk,0);
        for(unsigned long long ii=0;ii<nk;ii++){
            if(!hasLegal[ii]){gCur[ii]=0;hCur[ii]=1;term[k]++;minS=min(minS,k);}
            else{int g=0,h=0;while(gs[ii]>>g&1)g++;while(hs[ii]>>h&1)h++;gCur[ii]=g;hCur[ii]=h;}
            hg[gCur[ii]]++;hh[hCur[ii]]++;
        }
        hashLevel(k,gCur,hCur);
        if(k==1){firstMoves.clear();for(int j=0;j<N;j++)firstMoves.push_back({gCur[j],hCur[j]});}
        gNext.swap(gCur);hNext.swap(hCur);
        cerr<<"level "<<k<<" done (S="<<S<<")\n";
    }
    cout<<"m="<<m<<" forbidden="<<forbidden<<" states="<<total<<" K="<<K<<" s="<<minS
        <<" g(empty)="<<int(gNext[0])<<" h(empty)="<<int(hNext[0])<<"\n";
    cout<<"statehash_xor="<<hex<<hashXor<<" statehash_sum="<<hashSum<<dec<<"\n";
    for(int k=0;k<=K;k++)cout<<"layer "<<k<<" states "<<counts[k]<<" terminal "<<term[k]<<"\n";
    for(int k=0;k<32;k++)if(hg[k]||hh[k])cout<<"nimber "<<k<<" normal "<<hg[k]<<" misere "<<hh[k]<<"\n";
    cout<<"first_moves:";
    int invTrans[81];for(int i=0;i<N;i++)invTrans[transIdx[i]]=i;
    for(int c=0;c<N;c++){int j=invTrans[c];auto[g,h]=firstMoves[j];
        cout<<" ("<<p[j].x<<","<<p[j].y<<","<<p[j].z<<")=["<<g<<","<<h<<"]";}
    cout<<"\n";
    return 0;
}
int main(int argc,char**argv){
    if(argc<5)return 2;m=atoi(argv[1]);workdir=argv[2];ORDER=atoi(argv[3]);
    if(m<1||m>9||(ORDER!=0&&ORDER!=1))return 2;
    buildGeometry();
    string phase=argv[4];
    if(phase=="gen")return doGen();
    if(phase=="eval")return doEval(argc>=6?argv[5]:nullptr);
    return 2;
}
