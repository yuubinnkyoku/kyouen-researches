// Independently replay TWO terminal certificates and compute their joint D4 ranked WIN closure.
// All original-first-player WIN labels are checked by exact integer geometry;
// no cache, proof numbers, or conditional LOSS witness is trusted.
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

u128 parsehex(const string &s) {
  if(s.size()!=32) throw runtime_error("bad root");
  u128 v=0;
  for(char c:s) {
    int n=c>='0'&&c<='9'?c-'0':c>='a'&&c<='f'?c-'a'+10:-1;
    if(n<0) throw runtime_error("bad root hex");
    v=(v<<4)|n;
  }
  return v;
}
int main(int argc,char**argv) {
  if(argc!=3) {cerr<<"usage: joint first.raw second.raw\n";return 2;}
  for(int p=0;p<N;p++) {
    int x=p%11,y=p/11;
    rows[p]={{x*x+y*y,x,y,1}};
  }
  auto replay=[&](const string &filename,const string &roothex,
                  size_t expectedSeen,int expectedStrategy,
                  int expectedOpponent,int expectedTerminal,int expectedEdges) {
    ifstream f(filename,ios::binary);
    if(!f) throw runtime_error("missing strategy input");
    vector<unsigned char> raw((istreambuf_iterator<char>(f)),{});
    u128 root=parsehex(roothex);
    if(points(root).size()!=6) throw runtime_error("wrong root depth");
    unordered_set<u128,Hash> seen;
    int idx=0,strategies=0,opponents=0,terminals=0,edges=0;
    function<void(u128)> dfs=[&](u128 s) {
      if(!seen.insert(s).second) return;
      u128 moves=legal(s);
      int n=points(s).size();
      if(n%2==0) {
        if(!moves||idx>=(int)raw.size()) throw runtime_error("losing even terminal or missing strategy");
        int p=raw[idx++];
        if(p>=N||!((moves>>p)&1)) throw runtime_error("illegal strategy");
        strategies++;edges++;
        dfs(s|((u128)1<<p));
      } else if(!moves) {
        terminals++;
      } else {
        opponents++;
        for(int p:points(moves)){edges++;dfs(s|((u128)1<<p));}
      }
    };
    dfs(root);
    if(seen.size()!=expectedSeen||strategies!=expectedStrategy||
       opponents!=expectedOpponent||terminals!=expectedTerminal||
       edges!=expectedEdges||idx!=expectedStrategy||idx!=(int)raw.size())
      throw runtime_error("source strategy replay mismatch");
    return seen;
  };
  auto first=replay(argv[1],"00000000000200801002000081000000",
                    18649,12068,4027,2554,27947);
  auto second=replay(argv[2],"00000000000000203808000000000020",
                     22364,14440,4982,2942,34055);
  unordered_set<u128,Hash> combined=first;
  combined.insert(second.begin(),second.end());
  int trans[8][N];
  for(int p=0;p<N;p++) {
    int x=p%11,y=p/11;
    int xx[8]={x,10-y,10-x,y,10-x,10-y,x,y};
    int yy[8]={y,x,10-y,10-x,y,10-x,10-y,x};
    for(int k=0;k<8;k++) trans[k][p]=xx[k]+11*yy[k];
  }
  auto canonical=[&](u128 s) {
    u128 best=~(u128)0;
    auto ps=points(s);
    for(int k=0;k<8;k++) {
      u128 t=0;
      for(int p:ps) t|=(u128)1<<trans[k][p];
      best=min(best,t);
    }
    return best;
  };
  auto close=[&](const unordered_set<u128,Hash>& seeds) {
    unordered_set<u128,Hash> win;
    vector<vector<u128>> layer(21);
    for(u128 s:seeds) {
      u128 c=canonical(s);
      if(win.insert(c).second) layer[points(c).size()].push_back(c);
    }
    for(int n=18;n>=6;n--) {
      unordered_set<u128,Hash> candidates;
      for(u128 s:layer[n+1]) {
        for(int p:points(s)) {
          u128 pred=canonical(s^((u128)1<<p));
          if(!win.count(pred)) candidates.insert(pred);
        }
      }
      for(u128 s:candidates) {
        u128 moves=legal(s);
        bool proved=n%2!=0;
        for(int p:points(moves)) {
          bool child=win.count(canonical(s|((u128)1<<p)));
          if(n%2==0&&child){proved=true;break;}
          if(n%2!=0&&!child){proved=false;break;}
        }
        if(proved) {
          if(!win.insert(s).second) throw runtime_error("duplicate closure");
          layer[n].push_back(s);
        }
      }
    }
    return win;
  };
  auto a=close(first),b=close(second),both=close(combined);
  if(b.size()!=256744) throw runtime_error("second-only regression");
  for(u128 s:a) if(!both.count(s)) throw runtime_error("joint omitted first WIN");
  for(u128 s:b) if(!both.count(s)) throw runtime_error("joint omitted second WIN");
  size_t separateUnion=a.size();
  for(u128 s:b) if(!a.count(s)) separateUnion++;
  if(both.size()<separateUnion) throw runtime_error("joint closure shrank");
  vector<size_t> layers(20),novelLayers(20);
  for(u128 s:both) {
    int n=points(s).size();
    layers[n]++;
    if(!a.count(s)&&!b.count(s)) novelLayers[n]++;
  }
  cout<<"{\"first_reached\":"<<first.size()
      <<",\"second_reached\":"<<second.size()
      <<",\"source_union\":"<<combined.size()
      <<",\"first_only_classes\":"<<a.size()
      <<",\"second_only_classes\":"<<b.size()
      <<",\"separate_union_classes\":"<<separateUnion
      <<",\"joint_classes\":"<<both.size()
      <<",\"synergy_classes\":"<<both.size()-separateUnion
      <<",\"layer_counts_6_to_19\":[";
  for(int n=6;n<=19;n++){if(n!=6)cout<<",";cout<<layers[n];}
  cout<<"],\"new_beyond_either_6_to_19\":[";
  for(int n=6;n<=19;n++){if(n!=6)cout<<",";cout<<novelLayers[n];}
  cout<<"],\"two_stone_root\":\"UNKNOWN\",\"empty_board\":\"UNKNOWN\"}\n";
}
