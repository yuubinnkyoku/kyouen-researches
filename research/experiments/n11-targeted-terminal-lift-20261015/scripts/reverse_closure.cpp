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

int main(int argc,char**argv){
 if(argc!=3){cerr<<"usage: closure cache.tsv out.tsv\n";return 2;}
 ifstream f(argv[1]);string h,v;unordered_set<U128,Hash128> s10loss,s9loss,s8cand;
 while(f>>h>>v){if(v=="LOSS"){auto x=parse128(h);if(countbits(x)!=10||canonical(x)!=x){cerr<<"bad input";return 3;}s10loss.insert(x);}}
 cerr<<"s10 loss "<<s10loss.size()<<"\n";
 for(auto s10:s10loss)for(int p:points(s10))s9loss.insert(canonical(s10^((U128)1<<p)));
 cerr<<"s9 parents "<<s9loss.size()<<"\n";
 for(auto s9:s9loss)for(int p:points(s9))s8cand.insert(canonical(s9^((U128)1<<p)));
 cerr<<"s8 candidates "<<s8cand.size()<<"\n";
 unordered_map<U128,int,Hash128> covered;
 for(auto s9:s9loss)for(int p:points(s9))covered[canonical(s9^((U128)1<<p))]++;
 vector<pair<int,U128>> ranked;for(auto [s,n]:covered)ranked.emplace_back(n,s);
 sort(ranked.begin(),ranked.end(),[](auto a,auto b){return a.first!=b.first?a.first>b.first:a.second<b.second;});
 cerr<<"top coverage ";for(int i=0;i<min(20,(int)ranked.size());i++)cerr<<ranked[i].first<<" ";cerr<<"\n";
 ofstream o(argv[2]);o<<"s8\tknown_s9\tall_s9\tmissing\n";
 int count=0,complete=0;for(auto [n,s8]:ranked){if(n<12)break;auto ps=legal(s8);unordered_set<U128,Hash128> children;for(int p:ps)children.insert(canonical(s8|((U128)1<<p)));
 int missing=0;for(auto s9:children)if(!s9loss.count(s9))missing++;
 if(missing<=5){o<<hex128(s8)<<"\t"<<n<<"\t"<<children.size()<<"\t"<<missing<<"\n";if(!missing)complete++;}
 count++;}
 cerr<<"checked >=12 "<<count<<" complete "<<complete<<"\n";
}
