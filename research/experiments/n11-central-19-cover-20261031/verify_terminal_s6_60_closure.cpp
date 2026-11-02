// Independent exact-integer 4x4 terminal strategy replay and predecessor closure.
// Input: 14440 raw strategy bytes, decoded and SHA-256 checked by the Python driver.
// A winning even-depth state needs one winning child; a winning odd-depth
// state needs ALL legal children winning (including zero-move terminals).
// These statements are for the original first player, not player-to-move.
#include <bits/stdc++.h>
using namespace std;
using u128 = unsigned __int128;
constexpr int N = 121;
const u128 FULL = (((u128)1 << 120) - 1) + ((u128)1 << 120);
struct Hash {
  size_t operator()(u128 a) const noexcept {
    return (uint64_t)a * 0x9e3779b97f4a7c15ULL ^
           (uint64_t)(a >> 64) * 0xbf58476d1ce4e5b9ULL;
  }
};
struct Row { int v[4]; };
Row rows[N];
int det3(int a[3][3]) {
  return a[0][0] * (a[1][1]*a[2][2]-a[1][2]*a[2][1])
       - a[0][1] * (a[1][0]*a[2][2]-a[1][2]*a[2][0])
       + a[0][2] * (a[1][0]*a[2][1]-a[1][1]*a[2][0]);
}
vector<u128> forb(N*N*N);
vector<uint8_t> computed(N*N*N);
u128 getforb(int a, int b, int c) {
  int key = (a*N+b)*N+c;
  if (computed[key]) return forb[key];
  computed[key] = 1;
  int cof[4];
  for (int omit=0;omit<4;omit++) {
    int mat[3][3], ids[]={a,b,c};
    for (int i=0;i<3;i++) {
      int j2=0;
      for (int j=0;j<4;j++) if (j!=omit) mat[i][j2++]=rows[ids[i]].v[j];
    }
    cof[omit]=det3(mat)*(omit%2?-1:1);
  }
  u128 mask=0;
  for (int d=0;d<N;d++) {
    if (d==a||d==b||d==c) continue;
    long long sum=0;
    for (int j=0;j<4;j++) sum+=(long long)cof[j]*rows[d].v[j];
    if (!sum) mask|=(u128)1<<d;
  }
  return forb[key]=mask;
}
vector<int> points(u128 x) {
  vector<int> p;
  while (x) {
    int j=(uint64_t)x ? __builtin_ctzll((uint64_t)x)
                      : 64+__builtin_ctzll((uint64_t)(x>>64));
    p.push_back(j);
    x^=(u128)1<<j;
  }
  return p;
}
u128 legal(u128 x) {
  auto p=points(x);
  u128 bad=x;
  for (int i=0;i<(int)p.size();i++)
    for (int j=i+1;j<(int)p.size();j++)
      for (int k=j+1;k<(int)p.size();k++)
        bad|=getforb(p[i],p[j],p[k]);
  return FULL & ~bad;
}
int main(int argc,char**argv) {
  if (argc!=2) { cerr<<"usage: closure raw-strategy.bin\n"; return 2; }
  for (int p=0;p<N;p++) {
    int x=p%11,y=p/11;
    rows[p]={{x*x+y*y,x,y,1}};
  }
  ifstream f(argv[1],ios::binary);
  vector<unsigned char> raw((istreambuf_iterator<char>(f)),{});
  u128 root=0;
  for (char c:string("00000000000000203808000000000020"))
    root=(root<<4)+(c>='a'?c-'a'+10:c-'0');
  unordered_set<u128,Hash> seen;
  int idx=0,strategies=0,edges=0,opponents=0,terminals=0;
  function<void(u128)> dfs=[&](u128 s) {
    if (!seen.insert(s).second) return;
    auto moves=legal(s);
    int n=points(s).size();
    if (n%2==0) {
      if (!moves||idx>=(int)raw.size()) throw runtime_error("missing strategy or losing terminal");
      int p=raw[idx++];
      if (p>=N||!((moves>>p)&1)) throw runtime_error("illegal strategy");
      strategies++;edges++;
      dfs(s|((u128)1<<p));
    } else if (!moves) {
      terminals++;
    } else {
      opponents++;
      for (int p:points(moves)) {edges++;dfs(s|((u128)1<<p));}
    }
  };
  dfs(root);
  if (seen.size()!=22364||strategies!=14440||opponents!=4982||
      terminals!=2942||edges!=34055||idx!=14440||
      idx!=(int)raw.size()) throw runtime_error("source terminal replay changed");

  // Each iteration only adds positions whose WIN follows from the previous
  // certified set. Candidates are one-point deletions of certified positions.
  // All positions have >=6 stones, so the root/player parity is unchanged.
  unordered_set<u128,Hash> win=seen;
  vector<int> rounds;
  for (int iter=0;iter<20;iter++) {
    unordered_set<u128,Hash> candidates;
    for (auto s:win) {
      int n=points(s).size();
      if (n<7||n>19) continue;
      for (int p:points(s)) {
        u128 pred=s^((u128)1<<p);
        if (!win.count(pred)) candidates.insert(pred);
      }
    }
    vector<u128> add;
    for (auto s:candidates) {
      int n=points(s).size();
      if (n<6) continue;
      u128 moves=legal(s);
      bool proved=false;
      if (n%2==0) {
        for (int p:points(moves))
          if (win.count(s|((u128)1<<p))) { proved=true;break; }
      } else {
        proved=true;
        for (int p:points(moves))
          if (!win.count(s|((u128)1<<p))) { proved=false;break; }
      }
      if (proved) add.push_back(s);
    }
    rounds.push_back(add.size());
    for (auto s:add) win.insert(s);
    if (add.empty()) break;
  }

  // Count D4 orbits without treating raw states as different symmetry classes.
  int trans[8][N];
  for (int p=0;p<N;p++) {
    int x=p%11,y=p/11;
    int xx[8]={x,10-y,10-x,y,10-x,10-y,x,y};
    int yy[8]={y,x,10-y,10-x,y,10-x,10-y,x};
    for (int k=0;k<8;k++) trans[k][p]=xx[k]+11*yy[k];
  }
  unordered_set<u128,Hash> canonical;
  int newS6=0,newS7=0;
  for (auto s:win) {
    u128 best=~(u128)0;
    auto ps=points(s);
    for (int k=0;k<8;k++) {
      u128 t=0;
      for (int p:ps) t|=(u128)1<<trans[k][p];
      best=min(best,t);
    }
    canonical.insert(best);
    if (!seen.count(s)) {
      if (ps.size()==6) newS6++;
      if (ps.size()==7) newS7++;
    }
  }
  if (rounds!=vector<int>({83556,19589,99467,7567,22511,291,1216,0})||
      win.size()!=256561||canonical.size()!=256193||newS6!=6||newS7!=0)
    throw runtime_error("backward closure changed");
  cout<<"{\"source_reached\":"<<seen.size()
      <<",\"closure_total_raw\":"<<win.size()
      <<",\"closure_new_raw\":"<<win.size()-seen.size()
      <<",\"closure_d4_classes\":"<<canonical.size()
      <<",\"new_s6_raw\":"<<newS6
      <<",\"new_s7_raw\":"<<newS7<<",\"rounds\":[";
  for (size_t i=0;i<rounds.size();i++) {
    if (i) cout<<",";
    cout<<rounds[i];
  }
  cout<<"]}\n";
}
