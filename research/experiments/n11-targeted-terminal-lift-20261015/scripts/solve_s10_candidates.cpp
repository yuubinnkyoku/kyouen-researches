// Independent integer-determinant, cache-free 11x11 S8 LOSS certificate checker.
// All witness S10 verdicts are computed to terminal positions; no external verdict cache.
#include <bits/stdc++.h>
using namespace std;
using U128=unsigned __int128;
struct Hash128 {size_t operator()(U128 v)const {uint64_t a=(uint64_t)v,b=(uint64_t)(v>>64);return std::hash<uint64_t>{}(a ^ (b*0x9e3779b97f4a7c15ULL));}};
int xx(int p){return p%11;} int yy(int p){return p/11;}
long long det4(int a,int b,int c,int d){
    auto vec=[&](int p){long long x=xx(p)-xx(d),y=yy(p)-yy(d);return array<long long,3>{x,y,(long long)xx(p)*xx(p)+(long long)yy(p)*yy(p)-(long long)xx(d)*xx(d)-(long long)yy(d)*yy(d)};};
    auto u=vec(a),v=vec(b),w=vec(c);
    return u[0]*(v[1]*w[2]-v[2]*w[1])-u[1]*(v[0]*w[2]-v[2]*w[0])+u[2]*(v[0]*w[1]-v[1]*w[0]);
}
vector<int> points(U128 m){vector<int> a;for(int i=0;i<121;i++)if((m>>i)&1)a.push_back(i);return a;}
U128 parse128(const string&s){if(s.size()!=32)throw runtime_error("bad hex width");U128 x=0;for(char c:s){x<<=4;if(c>='0'&&c<='9')x+=c-'0';else if(c>='a'&&c<='f')x+=c-'a'+10;else throw runtime_error("bad hex");}if(x>>121)throw runtime_error("mask exceeds board");return x;}
string hex128(U128 x){string s(32,'0');for(int i=31;i>=0;i--){s[i]="0123456789abcdef"[(int)(x&15)];x>>=4;}return s;}
int countbits(U128 x){return __builtin_popcountll((uint64_t)x)+__builtin_popcountll((uint64_t)(x>>64));}
bool safe(U128 m){auto a=points(m);int n=a.size();for(int i=0;i<n;i++)for(int j=i+1;j<n;j++)for(int k=j+1;k<n;k++)for(int l=k+1;l<n;l++)if(det4(a[i],a[j],a[k],a[l])==0)return false;return true;}
vector<int> legal(U128 m){auto a=points(m);vector<int> ret;for(int p=0;p<121;p++){if((m>>p)&1)continue;bool ok=true;for(int i=0;i<(int)a.size()&&ok;i++)for(int j=i+1;j<(int)a.size()&&ok;j++)for(int k=j+1;k<(int)a.size();k++)if(det4(a[i],a[j],a[k],p)==0){ok=false;break;}if(ok)ret.push_back(p);}return ret;}
U128 canonical(U128 m){U128 best=~(U128)0;for(int t=0;t<8;t++){U128 v=0;for(int p:points(m)){int x=xx(p),y=yy(p),X=0,Y=0;switch(t){case 0:X=x;Y=y;break;case 1:X=10-y;Y=x;break;case 2:X=10-x;Y=10-y;break;case 3:X=y;Y=10-x;break;case 4:X=10-x;Y=y;break;case 5:X=10-y;Y=10-x;break;case 6:X=x;Y=10-y;break;case 7:X=y;Y=x;break;}v|=(U128)1<<(Y*11+X);}best=min(best,v);}return best;}
struct Terminal {bool loss;uint64_t states;int moves;};
unordered_map<U128,Terminal,Hash128> verdicts;
Terminal solve10(U128 m){auto it=verdicts.find(m);if(it!=verdicts.end())return it->second;
    if(countbits(m)!=10||!safe(m))throw runtime_error("invalid S10");
    auto base=points(m),p=legal(m);int n=p.size();if(n>63)throw runtime_error("unsupported >63 terminal moves");
    vector<uint64_t> bad;
    // Every forbidden combination among the candidate points has size 2,3,or 4.
    for(int i=0;i<n;i++)for(int j=i+1;j<n;j++){
        bool b=false;for(int a=0;a<10&&!b;a++)for(int c=a+1;c<10;c++)if(det4(base[a],base[c],p[i],p[j])==0){b=true;break;}
        if(b)bad.push_back((1ULL<<i)|(1ULL<<j));
    }
    auto contains_bad=[&](uint64_t s){for(uint64_t b:bad)if((s&b)==b)return true;return false;};
    for(int i=0;i<n;i++)for(int j=i+1;j<n;j++)for(int k=j+1;k<n;k++){
        uint64_t s=(1ULL<<i)|(1ULL<<j)|(1ULL<<k);if(contains_bad(s))continue;
        for(int a:base)if(det4(a,p[i],p[j],p[k])==0){bad.push_back(s);break;}
    }
    for(int i=0;i<n;i++)for(int j=i+1;j<n;j++)for(int k=j+1;k<n;k++)for(int l=k+1;l<n;l++){
        uint64_t s=(1ULL<<i)|(1ULL<<j)|(1ULL<<k)|(1ULL<<l);if(contains_bad(s))continue;
        if(det4(p[i],p[j],p[k],p[l])==0)bad.push_back(s);
    }
    vector<vector<uint64_t>> constraints(n);
    for(uint64_t b:bad)for(int i=0;i<n;i++)if(b&(1ULL<<i))constraints[i].push_back(b^(1ULL<<i));
    unordered_map<uint64_t,bool> memo;memo.reserve(1024);
    function<bool(uint64_t)> wins=[&](uint64_t s)->bool{
        auto it=memo.find(s);if(it!=memo.end())return it->second;
        for(int i=0;i<n;i++){uint64_t bit=1ULL<<i;if(s&bit)continue;bool ok=true;for(uint64_t v:constraints[i])if((s&v)==v){ok=false;break;}if(ok&&!wins(s|bit)){memo[s]=true;return true;}}
        memo[s]=false;return false;
    };
    bool loss=!wins(0);Terminal t{loss,memo.size(),n};verdicts[m]=t;return t;
}

int main(int argc,char**argv){
 if(argc!=3){cerr<<"usage: solve_s10 input output\n";return 2;}
 ifstream f(argv[1]);ofstream out(argv[2]);string s;
 size_t count=0,loss=0,win=0;uint64_t states=0;
 while(f>>s){U128 x=parse128(s);if(countbits(x)!=10||canonical(x)!=x||!safe(x))throw runtime_error("invalid s10");Terminal t=solve10(x);out<<s<<"\t"<<(t.loss?"LOSS":"WIN")<<"\t"<<t.states<<"\t"<<t.moves<<"\n";count++;loss+=t.loss;win+=!t.loss;states+=t.states;}
 cerr<<"tested="<<count<<" LOSS="<<loss<<" WIN="<<win<<" states="<<states<<"\n";
 return 0;
}
