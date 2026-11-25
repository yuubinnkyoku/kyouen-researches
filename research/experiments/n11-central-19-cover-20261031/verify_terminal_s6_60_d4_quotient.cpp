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


  // D4-equivariant proof closure: quotient all certified states by all eight
  // board symmetries before evaluating predecessors.  A canonical class is
  // added only when the AND/OR rule is satisfied by ALREADY certified children.
  // Descending stone count is sound because all legal moves increase size.
  int trans[8][N];
  for (int p=0;p<N;p++) {
    int x=p%11,y=p/11;
    int xx[8]={x,10-y,10-x,y,10-x,10-y,x,y};
    int yy[8]={y,x,10-y,10-x,y,10-x,10-y,x};
    for (int k=0;k<8;k++) trans[k][p]=xx[k]+11*yy[k];
  }
  auto canonical=[&](u128 s) {
    u128 best=~(u128)0;
    auto ps=points(s);
    for (int k=0;k<8;k++) {
      u128 t=0;
      for (int p:ps) t|=(u128)1<<trans[k][p];
      best=min(best,t);
    }
    return best;
  };
  unordered_set<u128,Hash> win;
  vector<vector<u128>> layer(21);
  for (u128 s:seen) {
    u128 c=canonical(s);
    if (win.insert(c).second) layer[points(c).size()].push_back(c);
  }
  if (layer[6].size()!=1||layer[7].size()!=1)
    throw runtime_error("unexpected source low-stone layers");
  vector<int> added(20),candidateCount(20);
  for (int n=18;n>=6;n--) {
    unordered_set<u128,Hash> candidates;
    for (u128 s:layer[n+1]) {
      for (int p:points(s)) {
        u128 pred=canonical(s^((u128)1<<p));
        if (!win.count(pred)) candidates.insert(pred);
      }
    }
    candidateCount[n]=candidates.size();
    for (u128 s:candidates) {
      u128 moves=legal(s);
      bool proved=(n%2!=0);
      for (int p:points(moves)) {
        bool child=win.count(canonical(s|((u128)1<<p)));
        if (n%2==0 && child) {proved=true;break;}
        if (n%2!=0 && !child) {proved=false;break;}
      }
      if (proved) {
        if (!win.insert(s).second) throw runtime_error("duplicate addition");
        layer[n].push_back(s);
        added[n]++;
      }
    }
  }
  const vector<int> expected={
    0,0,0,0,0,0,7,1,296,36,10294,1124,114567,11369,
    104007,9994,4651,378,19,1,0
  };
  for (int n=6;n<=19;n++) if (layer[n].size()!=(size_t)expected[n])
    throw runtime_error("D4-quotient layer count changed at n="+to_string(n));
  if (win.size()!=256744||layer[6].size()!=7||layer[7].size()!=1)
    throw runtime_error("D4-quotient closure total changed");

  // Independently reconstruct the unquotiented closure (K0630), then
  // compare the actual canonical sets rather than merely their cardinalities.
  unordered_set<u128,Hash> rawWin=seen;
  vector<vector<u128>> rawLayer(21);
  for (u128 s:seen) rawLayer[points(s).size()].push_back(s);
  for (int n=18;n>=6;n--) {
    unordered_set<u128,Hash> candidates;
    for (u128 s:rawLayer[n+1]) {
      for (int p:points(s)) {
        u128 pred=s^((u128)1<<p);
        if (!rawWin.count(pred)) candidates.insert(pred);
      }
    }
    for (u128 s:candidates) {
      u128 moves=legal(s);
      bool proved=(n%2!=0);
      for (int p:points(moves)) {
        bool child=rawWin.count(s|((u128)1<<p));
        if (n%2==0&&child) {proved=true;break;}
        if (n%2!=0&&!child) {proved=false;break;}
      }
      if (proved) {rawWin.insert(s);rawLayer[n].push_back(s);}
    }
  }
  unordered_set<u128,Hash> rawCanonical;
  for (u128 s:rawWin) rawCanonical.insert(canonical(s));
  if (rawWin.size()!=256561||rawCanonical.size()!=256193)
    throw runtime_error("original unquotiented closure mismatch");
  for (u128 s:rawCanonical)
    if (!win.count(s)) throw runtime_error("D4 quotient omitted old WIN class");
  vector<int> newByLayer(21);
  for (u128 s:win)
    if (!rawCanonical.count(s)) newByLayer[points(s).size()]++;
  const vector<int> expectedNew={
    0,0,0,0,0,0,0,0,0,0,38,6,156,20,285,46,0,0,0,0,0
  };
  if (newByLayer!=expectedNew||win.size()-rawCanonical.size()!=551)
    throw runtime_error("strict D4-quotient improvement mismatch");
  cout<<"{\"source_reached\":"<<seen.size()
      <<",\"d4_quotient_win_classes\":"<<win.size()
      <<",\"certified_s6_classes\":"<<layer[6].size()
      <<",\"certified_s7_classes\":"<<layer[7].size()
      <<",\"layer_counts_6_to_19\":[";
  for (int n=6;n<=19;n++) {if (n!=6) cout<<",";cout<<layer[n].size();}
  cout<<"],\"added_6_to_18\":[";
  for (int n=6;n<=18;n++) {if (n!=6) cout<<",";cout<<added[n];}
  cout<<"],\"candidate_6_to_18\":[";
  for (int n=6;n<=18;n++) {if (n!=6) cout<<",";cout<<candidateCount[n];}
  cout<<"],\"additional_d4_classes\":551,\"additional_by_layer_6_to_19\":[";
  for (int n=6;n<=19;n++) {if (n!=6) cout<<",";cout<<newByLayer[n];}
  cout<<"],\"two_stone_root\":\"UNKNOWN\",\"empty_board\":\"UNKNOWN\"}\n";
}
