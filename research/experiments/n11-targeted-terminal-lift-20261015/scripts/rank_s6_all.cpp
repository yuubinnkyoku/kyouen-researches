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
 if(argc!=4){cerr<<"usage: rank_s6 loss_s7 win_s7 output.tsv\n";return 2;}
 set<U128> losses,wins,candidates;
 auto read=[&](const char*name,set<U128>&dest){ifstream f(name);string s;while(f>>s){auto m=parse128(s);if(canonical(m)!=m||countbits(m)!=7||!safe(m))throw runtime_error("bad S7 input");dest.insert(m);}};
 read(argv[1],losses);read(argv[2],wins);
 for(U128 m:losses)for(int p:points(m))candidates.insert(canonical(m^((U128)1<<p)));
 ofstream out(argv[3]);out<<"s6\ttotal_s7\tloss_s7\twin_s7\tunknown_s7\n";
 vector<tuple<int,int,int,U128>> ranks;
 int excluded=0, fully=0;
 for(U128 m:candidates){
  if(countbits(m)!=6||canonical(m)!=m||!safe(m))throw runtime_error("bad S6 candidate");
  set<U128> children;for(int p:legal(m))children.insert(canonical(m|((U128)1<<p)));
  int lc=0,wc=0;for(U128 c:children){lc+=losses.count(c);wc+=wins.count(c);}
  if(wc)excluded++;
  int missing=children.size()-lc-wc;
  if(!wc){if(!missing)fully++;ranks.emplace_back(missing,-lc,(int)children.size(),m);}
  out<<hex128(m)<<'\t'<<children.size()<<'\t'<<lc<<'\t'<<wc<<'\t'<<missing<<'\n';
 }
 sort(ranks.begin(),ranks.end());
 cout<<"S7 loss "<<losses.size()<<" S7 win "<<wins.size()<<" candidate S6 "<<candidates.size()<<" excluded by WIN "<<excluded<<" fully LOSS "<<fully<<" viable "<<ranks.size()<<"\n";
 for(int i=0;i<min(30,(int)ranks.size());i++){
  auto [missing,negative_loss,total,m]=ranks[i];cout<<i+1<<' '<<hex128(m)<<" total="<<total<<" loss="<<-negative_loss<<" missing="<<missing<<'\n';
 }
}
